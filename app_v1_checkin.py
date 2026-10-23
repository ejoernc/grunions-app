"""Grunions Water Polo check-in prototype. Flask + SQLite, all data local."""
import csv, io, os, re, sqlite3, datetime as dt, functools
import qrcode, qrcode.image.svg
from flask import Flask, request, redirect, url_for, session, g, render_template_string, Response, abort

DB = os.environ.get("GRUNIONS_DB", os.path.join(os.path.dirname(__file__), "grunions.db"))
COACH_PIN = os.environ.get("COACH_PIN", "4545")
PUBLIC_URL = os.environ.get("PUBLIC_URL")  # e.g. https://checkin.example.com
app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev-change-me")

SCHEMA = """
CREATE TABLE IF NOT EXISTS members(id INTEGER PRIMARY KEY, first TEXT NOT NULL, last TEXT NOT NULL,
  email TEXT NOT NULL UNIQUE, phone TEXT, created TEXT DEFAULT CURRENT_TIMESTAMP,
  usawp_status TEXT DEFAULT 'unknown', usawp_raw TEXT, usawp_number TEXT, usawp_valid_until TEXT, usawp_updated TEXT);
CREATE TABLE IF NOT EXISTS checkins(id INTEGER PRIMARY KEY, member_id INTEGER REFERENCES members(id),
  practice_date TEXT NOT NULL, location TEXT, at TEXT DEFAULT CURRENT_TIMESTAMP, UNIQUE(member_id, practice_date));
"""
def db():
    if "db" not in g:
        g.db = sqlite3.connect(DB); g.db.row_factory = sqlite3.Row; g.db.executescript(SCHEMA)
    return g.db
@app.teardown_appcontext
def _close(e):
    d = g.pop("db", None)
    if d: d.close()

def norm(s): return re.sub(r"[^a-z]", "", (s or "").lower())
def location_for(d):
    wd = dt.date.fromisoformat(d).weekday()
    return {1: "Marina High School (Tue)", 4: "Westminster High School (Fri)"}.get(wd, "Other")
def coach_required(f):
    @functools.wraps(f)
    def w(*a, **k):
        if not session.get("coach"): return redirect(url_for("coach_login", next=request.path))
        return f(*a, **k)
    return w

BASE = """<!doctype html><meta name=viewport content="width=device-width,initial-scale=1"><title>Grunions</title>
<style>body{font-family:system-ui;max-width:760px;margin:auto;padding:16px}input,select,button{font-size:18px;padding:8px;margin:4px 0;width:100%;box-sizing:border-box}
table{width:100%;border-collapse:collapse}td,th{border-bottom:1px solid #ddd;padding:6px;text-align:left}
.verified{color:#fff;background:#2a7}.expired{color:#fff;background:#c33}.unknown{background:#ddd}.pending{background:#fc3}
.tag{padding:2px 8px;border-radius:8px;font-size:13px}nav a{margin-right:12px}.msg{background:#eef;padding:8px}
.inline button{width:auto}@media print{nav,.noprint{display:none}}</style>
{% if session.coach %}<nav><a href=/coach>Check-in</a><a href=/members>Members</a><a href=/import>USAWP import</a><a href=/qr>QR</a><a href=/logout>Log out</a></nav>{% endif %}
<h2>🐟 Grunions Water Polo</h2>{% for m in get_flashed_messages() %}<p class=msg>{{m}}</p>{% endfor %}"""
from flask import flash
def page(body, **kw): return render_template_string(BASE + body, **kw)

@app.route("/", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        f = {k: (request.form.get(k) or "").strip() for k in ("first", "last", "email", "phone")}
        if not all(f.values()) or "@" not in f["email"]:
            flash("Please fill in every field."); return redirect("/")
        email = f["email"].lower()
        d = db(); row = d.execute("SELECT id FROM members WHERE email=?", (email,)).fetchone()
        if row:
            d.execute("UPDATE members SET first=?,last=?,phone=? WHERE id=?", (f["first"], f["last"], f["phone"], row["id"]))
        else:
            d.execute("INSERT INTO members(first,last,email,phone) VALUES(?,?,?,?)", (f["first"], f["last"], email, f["phone"]))
        d.commit()
        return page("<h3>Thanks, {{n}}! You're signed up.</h3><p>Find a coach on deck to get checked in. Practices: Tue at Marina HS, Fri at Westminster HS, 7–8:30 PM. $45/mo membership starts in November. A current USA Water Polo membership is required.</p>", n=f["first"])
    return page("""<h3>First practice? Sign up</h3><form method=post>
<label>Legal first name<input name=first required autocomplete=given-name></label>
<label>Legal last name<input name=last required autocomplete=family-name></label>
<label>Email (use the one on your USA Water Polo account)<input name=email type=email required></label>
<label>Phone<input name=phone type=tel required></label><button>Sign up</button></form>""")

def signup_url(): return (PUBLIC_URL or request.host_url.rstrip("/")) + "/"
@app.route("/qr.svg")
def qr_svg():
    img = qrcode.make(signup_url(), image_factory=qrcode.image.svg.SvgPathImage, box_size=20)
    buf = io.BytesIO(); img.save(buf); return Response(buf.getvalue(), mimetype="image/svg+xml")
@app.route("/qr")
@coach_required
def qr_page():
    return page("""<div style=text-align:center><h1>New to Grunions? Scan to sign up</h1><img src=/qr.svg style="width:80%;max-width:500px">
<p>{{u}}</p><button class=noprint onclick=print()>Print</button></div>""", u=signup_url())

@app.route("/coach/login", methods=["GET", "POST"])
def coach_login():
    if request.method == "POST":
        if request.form.get("pin") == COACH_PIN:
            session["coach"] = True; return redirect(request.args.get("next") or "/coach")
        flash("Wrong PIN.")
    return page("<h3>Coach login</h3><form method=post><input name=pin type=password inputmode=numeric placeholder=PIN autofocus><button>Enter</button></form>")
@app.route("/logout")
def logout(): session.clear(); return redirect("/")

@app.route("/coach", methods=["GET", "POST"])
@coach_required
def coach():
    d = db(); date = request.values.get("date") or dt.date.today().isoformat()
    if request.method == "POST":
        mid = int(request.form["member_id"])
        if request.form.get("action") == "undo":
            d.execute("DELETE FROM checkins WHERE member_id=? AND practice_date=?", (mid, date))
        else:
            d.execute("INSERT OR IGNORE INTO checkins(member_id,practice_date,location) VALUES(?,?,?)", (mid, date, location_for(date)))
        d.commit(); return redirect(url_for("coach", date=date, q=request.form.get("q", "")))
    q = request.args.get("q", "").strip()
    rows = d.execute("""SELECT m.*, c.id AS cid FROM members m LEFT JOIN checkins c ON c.member_id=m.id AND c.practice_date=?
      WHERE (?='' OR m.first||' '||m.last||' '||m.email LIKE '%'||?||'%') ORDER BY c.id IS NULL, m.last, m.first""", (date, q, q)).fetchall()
    n = sum(1 for r in rows if r["cid"])
    return page("""<form class=noprint><input type=date name=date value="{{date}}" onchange=this.form.submit()><input name=q value="{{q}}" placeholder="Search name or email"></form>
<h3>{{date}} · {{loc}} · {{n}} checked in</h3><table>{% for r in rows %}<tr><td>{{r.first}} {{r.last}}<br><small>{{r.email}}</small></td>
<td><span class="tag {{r.usawp_status}}">USAWP {{r.usawp_status}}</span></td><td><form method=post class=inline><input type=hidden name=member_id value={{r.id}}><input type=hidden name=date value={{date}}><input type=hidden name=q value="{{q}}">
{% if r.cid %}✅ <button name=action value=undo>Undo</button>{% else %}<button>Check in</button>{% endif %}</form></td></tr>{% endfor %}</table>""",
        date=date, q=q, rows=rows, n=n, loc=location_for(date))

@app.route("/members")
@coach_required
def members():
    rows = db().execute("""SELECT m.*, (SELECT COUNT(*) FROM checkins WHERE member_id=m.id) AS visits,
      (SELECT MAX(practice_date) FROM checkins WHERE member_id=m.id) AS lastp FROM members m ORDER BY last, first""").fetchall()
    return page("""<h3>Members ({{rows|length}}) <a href=/members.csv style=font-size:14px>export CSV</a></h3><table><tr><th>Name</th><th>Contact</th><th>USAWP</th><th>Visits</th></tr>
{% for r in rows %}<tr><td>{{r.first}} {{r.last}}</td><td>{{r.email}}<br>{{r.phone}}</td><td><span class="tag {{r.usawp_status}}">{{r.usawp_status}}</span>
<br><small>{{r.usawp_raw or ''}} {{r.usawp_number or ''}} {% if r.usawp_valid_until %}thru {{r.usawp_valid_until}}{% endif %}</small></td><td>{{r.visits}}<br><small>{{r.lastp or ''}}</small></td></tr>{% endfor %}</table>""", rows=rows)
@app.route("/members.csv")
@coach_required
def members_csv():
    out = io.StringIO(); w = csv.writer(out)
    w.writerow(["first", "last", "email", "phone", "usawp_status", "usawp_raw", "member_number", "valid_until"])
    for r in db().execute("SELECT * FROM members ORDER BY last"): w.writerow([r["first"], r["last"], r["email"], r["phone"], r["usawp_status"], r["usawp_raw"], r["usawp_number"], r["usawp_valid_until"]])
    return Response(out.getvalue(), mimetype="text/csv", headers={"Content-Disposition": "attachment; filename=grunions-members.csv"})

# ---- USAWP (Sport:80 Smart List export) import ----
ALIASES = {  # normalized header -> field. Sport:80 Smart List columns vary by chosen columns, so match loosely.
    "first": ["firstname", "forename", "givenname", "legalfirstname"],
    "last": ["lastname", "surname", "familyname", "legallastname"],
    "name": ["name", "fullname", "membername", "profilename"],
    "email": ["email", "emailaddress", "primaryemail", "profileemail"],
    "status": ["status", "membershipstatus", "individualmembershipstatus", "addonstatus"],
    "number": ["membernumber", "membershipnumber", "membershipid", "memberid", "usawpid", "individualmembershipmembernumber"],
    "valid": ["validuntil", "validthrough", "expirydate", "expirationdate", "expires", "enddate", "individualmembershipvaliduntil", "individualmembershipexpirydate"],
}
def map_headers(headers):
    m = {}
    for i, h in enumerate(headers):
        n = norm(h)
        for field, al in ALIASES.items():
            if field not in m and (n in al or any(n.endswith(a) for a in al if len(a) > 5)): m[field] = i
    return m
def parse_date(v):
    if isinstance(v, (dt.date, dt.datetime)): return v.date() if isinstance(v, dt.datetime) else v
    v = (str(v or "")).strip()[:10]
    for f in ("%Y-%m-%d", "%m/%d/%Y", "%d/%m/%Y", "%m/%d/%y"):
        try: return dt.datetime.strptime(v, f).date()
        except ValueError: pass
def classify(raw, valid):
    s = norm(raw)
    if valid and valid < dt.date.today(): return "expired"
    if s in ("current", "active", "valid", "approved", "paid"): return "verified"
    if s in ("expired", "lapsed", "cancelled", "canceled", "inactive", "suspended", "revoked"): return "expired"
    if s in ("pendingapproval", "actionrequired", "pending"): return "pending"
    return "unknown"
def read_rows(fname, data):
    if fname.lower().endswith((".xlsx", ".xlsm")):
        import openpyxl
        ws = openpyxl.load_workbook(io.BytesIO(data), read_only=True, data_only=True).active
        rows = [list(r) for r in ws.iter_rows(values_only=True)]
    else:
        rows = list(csv.reader(io.StringIO(data.decode("utf-8-sig", errors="replace"))))
    # header row = first row containing a name-ish column (skips title rows in exports)
    for i, r in enumerate(rows[:10]):
        hm = map_headers([str(c or "") for c in r])
        if ("email" in hm or "name" in hm or "last" in hm) and "status" in hm: return hm, rows[i + 1:]
    return None, rows
def import_roster(fname, data):
    hm, rows = read_rows(fname, data)
    if not hm: return None
    d = db(); now = dt.datetime.now().isoformat(timespec="minutes")
    members = d.execute("SELECT id, first, last, email FROM members").fetchall()
    by_email = {m["email"]: m["id"] for m in members}
    by_name = {}
    for m in members: by_name.setdefault(norm(m["first"]) + "|" + norm(m["last"]), []).append(m["id"])
    stats = {"rows": 0, "matched": 0, "unmatched": []}; best = {}
    cell = lambda r, k: (r[hm[k]] if k in hm and hm[k] < len(r) else None)
    for r in rows:
        if not any(r): continue
        stats["rows"] += 1
        first, last = str(cell(r, "first") or "").strip(), str(cell(r, "last") or "").strip()
        if not (first and last) and cell(r, "name"):
            parts = str(cell(r, "name")).strip().split()
            first, last = parts[0], parts[-1] if len(parts) > 1 else ""
        email = str(cell(r, "email") or "").strip().lower()
        raw = str(cell(r, "status") or "").strip(); valid = parse_date(cell(r, "valid"))
        mid = by_email.get(email) if email else None
        if not mid:
            ids = by_name.get(norm(first) + "|" + norm(last), [])
            mid = ids[0] if len(ids) == 1 else None
        if not mid: stats["unmatched"].append(f"{first} {last} <{email}> {raw}"); continue
        st = classify(raw, valid); rank = {"verified": 3, "pending": 2, "expired": 1, "unknown": 0}[st]
        if mid not in best or rank > best[mid][0]:  # keep best status if someone appears twice
            best[mid] = (rank, st, raw, str(cell(r, "number") or ""), valid.isoformat() if valid else None)
    for mid, (_, st, raw, num, valid) in best.items():
        d.execute("UPDATE members SET usawp_status=?,usawp_raw=?,usawp_number=?,usawp_valid_until=?,usawp_updated=? WHERE id=?", (st, raw, num, valid, now, mid))
    d.commit(); stats["matched"] = len(best); return stats

@app.route("/import", methods=["GET", "POST"])
@coach_required
def import_page():
    stats = None
    if request.method == "POST":
        f = request.files.get("file")
        if not f or not f.filename: flash("Choose a file.")
        else:
            stats = import_roster(f.filename, f.read())
            if stats is None: flash("Couldn't find name/email and status columns in that file.")
    return page("""<h3>Import USAWP roster (Sport:80)</h3>
<ol><li>Log in at <a href=https://usawp.sport80.com>usawp.sport80.com</a> and switch to the Grunions club admin profile.</li>
<li>Members → Smart Lists → Actions → Edit Columns: include Name (or First/Last), Email, Individual Membership Status, Member Number, Valid Until/Expiry.</li>
<li>Actions → Export Report. Sport:80 emails you an Excel file. Upload it here (.xlsx or .csv).</li></ol>
<form method=post enctype=multipart/form-data><input type=file name=file accept=".csv,.xlsx"><button>Import</button></form>
{% if stats %}<p class=msg>Read {{stats.rows}} rows · updated {{stats.matched}} members · {{stats.unmatched|length}} roster rows not signed up in the app.</p>
{% if stats.unmatched %}<details><summary>Unmatched roster rows</summary><ul>{% for u in stats.unmatched %}<li>{{u}}</li>{% endfor %}</ul></details>{% endif %}{% endif %}
<p><small>Matching: email first, then exact legal first+last name. Status: Current → verified; Expired/Lapsed → expired; Pending Approval/Action Required → pending; not found in any import → unknown (earlier imports are kept).</small></p>""", stats=stats)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5055)))
