"""Grunions Water Polo team app prototype: member login, team chat, admin check-in tools. Flask + SQLite."""
import csv, io, os, re, sqlite3, secrets, hashlib, datetime as dt, functools
import json, urllib.request
import qrcode, qrcode.image.svg
from markupsafe import Markup
import ui
from ui import T
from flask import (Flask, request, redirect, url_for, session, g, render_template_string, Response, abort, flash, jsonify)

DATA_DIR = os.environ.get("DATA_DIR") or os.path.dirname(os.path.abspath(__file__))  # persistent disk in production
os.makedirs(DATA_DIR, exist_ok=True)
DB = os.environ.get("GRUNIONS_DB", os.path.join(DATA_DIR, "grunions.db"))
PUBLIC_URL = os.environ.get("PUBLIC_URL")
ADMIN_EMAILS = {e.strip().lower() for e in os.environ.get("ADMIN_EMAIL", "").split(",") if e.strip()}  # bootstrap admins (comma-separated)
ADMIN_EMAIL = next(iter(sorted(ADMIN_EMAILS)), "")
LINK_MINUTES = int(os.environ.get("LINK_MINUTES", 15))
SMTP = {k: os.environ.get(k) for k in ("SMTP_HOST", "SMTP_PORT", "SMTP_USER", "SMTP_PASSWORD", "MAIL_FROM")}
EXPIRING_DAYS = int(os.environ.get("EXPIRING_DAYS", 30))
VERIFY_WEBHOOK_URL = os.environ.get("VERIFY_WEBHOOK_URL")  # outbound: new verification requests are POSTed here
VERIFY_WEBHOOK_KEY = os.environ.get("VERIFY_WEBHOOK_KEY")  # if set, Authorization: Bearer <key> (unless HEADER overrides)
VERIFY_WEBHOOK_HEADER = os.environ.get("VERIFY_WEBHOOK_HEADER")  # if set, this header carries the raw key
BOT_API_KEY = os.environ.get("BOT_API_KEY")  # inbound: bearer token for /api/verify-requests
CRON_KEY = os.environ.get("CRON_KEY")  # lets a scheduler call /api/expiring without a session
DEV_SHOW_LINKS = os.environ.get("DEV_SHOW_LINKS", "0") == "1"  # local testing only: show magic link on screen
UPLOADS = os.environ.get("GRUNIONS_UPLOADS", os.path.join(DATA_DIR, "uploads"))
MAX_UPLOAD = 8 * 1024 * 1024
REACTIONS = ["👍", "❤️", "😂", "🔥", "🤽", "👏"]
app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = MAX_UPLOAD + 64 * 1024
app.secret_key = os.environ.get("SECRET_KEY") or secrets.token_hex(32)
app.config.update(SESSION_COOKIE_HTTPONLY=True, SESSION_COOKIE_SAMESITE="Lax",
                  SESSION_COOKIE_SECURE=os.environ.get("SECURE_COOKIES", "1" if (PUBLIC_URL or "").startswith("https://") else "0") == "1",
                  PERMANENT_SESSION_LIFETIME=dt.timedelta(days=60))
if os.environ.get("BEHIND_PROXY", "1" if PUBLIC_URL else "0") == "1":  # Render etc. terminate HTTPS in front of us
    from werkzeug.middleware.proxy_fix import ProxyFix
    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1)

SCHEMA = """
CREATE TABLE IF NOT EXISTS members(id INTEGER PRIMARY KEY, first TEXT NOT NULL, last TEXT NOT NULL,
  email TEXT NOT NULL UNIQUE, phone TEXT, created TEXT DEFAULT CURRENT_TIMESTAMP, is_admin INTEGER DEFAULT 0,
  usawp_status TEXT DEFAULT 'unknown', usawp_raw TEXT, usawp_number TEXT, usawp_valid_until TEXT, usawp_updated TEXT);
CREATE TABLE IF NOT EXISTS checkins(id INTEGER PRIMARY KEY, member_id INTEGER REFERENCES members(id),
  practice_date TEXT NOT NULL, location TEXT, at TEXT DEFAULT CURRENT_TIMESTAMP, UNIQUE(member_id, practice_date));
CREATE TABLE IF NOT EXISTS login_tokens(token_hash TEXT PRIMARY KEY, member_id INTEGER, expires TEXT, used INTEGER DEFAULT 0);
CREATE TABLE IF NOT EXISTS requirements(id INTEGER PRIMARY KEY, name TEXT NOT NULL, applies_to TEXT DEFAULT 'all',
  keywords TEXT, expires INTEGER DEFAULT 1, active INTEGER DEFAULT 1);
CREATE TABLE IF NOT EXISTS member_reqs(member_id INTEGER, req_id INTEGER, completed_on TEXT, expires_on TEXT, source TEXT, by TEXT, at TEXT,
  PRIMARY KEY(member_id, req_id));
CREATE TABLE IF NOT EXISTS practices(id INTEGER PRIMARY KEY, date TEXT NOT NULL, start TEXT DEFAULT '19:00', end TEXT DEFAULT '20:30',
  location TEXT, note TEXT, cancelled INTEGER DEFAULT 0, UNIQUE(date, location));
CREATE TABLE IF NOT EXISTS rsvps(practice_id INTEGER, member_id INTEGER, going INTEGER, at TEXT DEFAULT CURRENT_TIMESTAMP, PRIMARY KEY(practice_id, member_id));
CREATE TABLE IF NOT EXISTS verify_requests(id INTEGER PRIMARY KEY, member_id INTEGER REFERENCES members(id), name TEXT, email TEXT,
  member_number TEXT, requested_by TEXT, status TEXT DEFAULT 'pending', created TEXT, answered TEXT, result TEXT, note TEXT, webhook TEXT);
CREATE TABLE IF NOT EXISTS reactions(message_id INTEGER, member_id INTEGER, emoji TEXT, PRIMARY KEY(message_id, member_id, emoji));
CREATE TABLE IF NOT EXISTS notices(id INTEGER PRIMARY KEY, member_id INTEGER REFERENCES members(id), body TEXT, at TEXT DEFAULT CURRENT_TIMESTAMP, seen INTEGER DEFAULT 0);
CREATE TABLE IF NOT EXISTS usawp_submits(id INTEGER PRIMARY KEY, member_id INTEGER, at TEXT);
CREATE TABLE IF NOT EXISTS messages(id INTEGER PRIMARY KEY, member_id INTEGER REFERENCES members(id), body TEXT NOT NULL,
  announcement INTEGER DEFAULT 0, at TEXT DEFAULT CURRENT_TIMESTAMP);
"""
def db():
    if "db" not in g:
        g.db = sqlite3.connect(DB); g.db.row_factory = sqlite3.Row; g.db.executescript(SCHEMA)
        cols = [r[1] for r in g.db.execute("PRAGMA table_info(members)")]
        for c, t in (("is_admin", "INTEGER DEFAULT 0"), ("role", "TEXT DEFAULT 'athlete'"), ("usawp_verified_by", "TEXT"), ("usawp_verified_at", "TEXT")):
            if c not in cols: g.db.execute(f"ALTER TABLE members ADD COLUMN {c} {t}")
        if not g.db.execute("SELECT 1 FROM requirements").fetchone():
            g.db.executemany("INSERT INTO requirements(name,applies_to,keywords,expires) VALUES(?,?,?,?)", DEFAULT_REQS); g.db.commit()
        mcols = [r[1] for r in g.db.execute("PRAGMA table_info(messages)")]
        if "channel" not in mcols: g.db.execute("ALTER TABLE messages ADD COLUMN channel TEXT DEFAULT 'team'")
        if "image" not in mcols: g.db.execute("ALTER TABLE messages ADD COLUMN image TEXT")
        expire_sweep(g.db)
        if "sport80_contact_id" not in cols: g.db.execute("ALTER TABLE members ADD COLUMN sport80_contact_id TEXT")
        for e in ADMIN_EMAILS: g.db.execute("UPDATE members SET is_admin=1 WHERE email=?", (e,))
        g.db.commit()
    return g.db
# applies_to: all | athlete | coach. keywords: normalized substrings to find this item's columns in a Sport:80 export.
DEFAULT_REQS = [("SafeSport training", "all", "safesport", 1), ("Background screening", "coach", "background", 1),
                ("Club waiver", "all", "waiver", 0), ("Concussion training", "coach", "concussion", 1)]
def req_keywords(d):
    return [k for r in d.execute("SELECT keywords FROM requirements") for k in (r[0] or "").split(",") if k]
def requirements_for(d, member):
    return d.execute("SELECT * FROM requirements WHERE active=1 AND (applies_to='all' OR applies_to=?) ORDER BY id", (member["role"] or "athlete",)).fetchall()
def clearance(d, member):
    """Cleared to play = USAWP membership current AND every required item completed and not expired."""
    today = dt.date.today().isoformat(); reasons = []; items = []
    if member["usawp_status"] != "verified": reasons.append(f"Membership {member['usawp_status']}")
    for q in requirements_for(d, member):
        mr = d.execute("SELECT * FROM member_reqs WHERE member_id=? AND req_id=?", (member["id"], q["id"])).fetchone()
        if not mr or not (mr["completed_on"] or mr["expires_on"]): st = "missing"
        elif mr["expires_on"] and mr["expires_on"] < today: st = "expired"
        elif q["expires"] and not mr["expires_on"]: st = "no date"
        else: st = "ok"
        items.append(dict(req=q, mr=mr, status=st, days_left=days_left(mr["expires_on"]) if mr else None))
        if st in ("missing", "expired"): reasons.append(f"{q['name']} {st}")
    return dict(ok=not reasons, reasons=reasons, checks=items)
app.jinja_env.globals.update(clearance=lambda m: clearance(db(), m))
def expire_sweep(d):
    """Auto-flip: anyone whose expires_on (usawp_valid_until) has passed becomes expired."""
    d.execute("UPDATE members SET usawp_status='expired', usawp_raw='Expired '||usawp_valid_until WHERE usawp_status IN ('verified','pending') AND usawp_valid_until IS NOT NULL AND usawp_valid_until < ?", (dt.date.today().isoformat(),)); d.commit()
def expiry_report(d, days=None):
    days = days or EXPIRING_DAYS; today = dt.date.today()
    rows = d.execute("SELECT id, first, last, email, phone, usawp_status, usawp_valid_until FROM members WHERE usawp_valid_until IS NOT NULL ORDER BY usawp_valid_until").fetchall()
    rq = d.execute("""SELECT m.id, m.first, m.last, m.email, m.phone, 'verified' AS usawp_status, x.expires_on AS usawp_valid_until, q.name AS item
      FROM member_reqs x JOIN members m ON m.id=x.member_id JOIN requirements q ON q.id=x.req_id
      WHERE q.active=1 AND (q.applies_to='all' OR q.applies_to=m.role) AND x.expires_on IS NOT NULL""").fetchall()
    out = {"expired": [], "within_7": [], "within_%d" % days: []}
    for r in sorted([dict(r, item="USAWP membership") for r in rows] + [dict(r) for r in rq], key=lambda x: x["usawp_valid_until"]):
        left = (dt.date.fromisoformat(r["usawp_valid_until"]) - today).days
        item = dict(r, days_left=left)
        if left < 0 or r["usawp_status"] == "expired": out["expired"].append(item)
        elif left <= 7: out["within_7"].append(item)
        elif left <= days: out["within_%d" % days].append(item)
    return out
def days_left(v):
    return (dt.date.fromisoformat(v) - dt.date.today()).days if v else None
def remind(d, mid, by="Grunions"):
    r = d.execute("SELECT first, usawp_valid_until FROM members WHERE id=?", (mid,)).fetchone()
    if not r: return
    n = days_left(r["usawp_valid_until"])
    when = "has expired" if n is not None and n < 0 else (f"expires in {n} days ({r['usawp_valid_until']})" if n is not None else "needs to be confirmed")
    d.execute("INSERT INTO notices(member_id, body) VALUES(?,?)", (mid, f"Hi {r['first']}, your USA Water Polo membership {when}. Renew at usawp.sport80.com with Grunions as your club so you can keep playing. ({by})"))
app.jinja_env.globals.update(days_left=days_left, EXPIRING_DAYS=EXPIRING_DAYS)
def admin_alert():
    if not (me() and me()["is_admin"]): return None
    rep = expiry_report(db()); n7 = len(rep["within_7"]) + len(rep["within_%d" % EXPIRING_DAYS]); ne = len(rep["expired"])
    return (ne, n7) if (ne or n7) else None
app.jinja_env.globals.update(admin_alert=admin_alert)
@app.teardown_appcontext
def _close(e):
    d = g.pop("db", None)
    if d: d.close()

def norm(s): return re.sub(r"[^a-z]", "", (s or "").lower())
def location_for(d):
    wd = dt.date.fromisoformat(d).weekday()
    return {1: "Marina HS · Tue", 4: "Westminster HS · Fri"}.get(wd, "Other")
def me():
    if "me" not in g:
        mid = session.get("mid")
        g.me = db().execute("SELECT * FROM members WHERE id=?", (mid,)).fetchone() if mid else None
    return g.me
def login_required(f):
    @functools.wraps(f)
    def w(*a, **k):
        if not me(): return redirect(url_for("login", next=request.path))
        return f(*a, **k)
    return w
def admin_required(f):
    @functools.wraps(f)
    def w(*a, **k):
        if not me(): return redirect(url_for("login", next=request.path))
        if not me()["is_admin"]: abort(403)
        return f(*a, **k)
    return w
def is_staff(m=None):
    m = m or me(); return bool(m and (m["is_admin"] or m["role"] == "coach"))
def role_label(m): return "admin" if m["is_admin"] else ("coach" if m["role"] == "coach" else "member")
app.jinja_env.globals.update(is_staff=is_staff, role_label=role_label)
def staff_required(f):
    @functools.wraps(f)
    def w(*a, **k):
        if not me(): return redirect(url_for("login", next=request.path))
        if not is_staff(): abort(403)
        return f(*a, **k)
    return w
# CSRF: per-session token on every POST form/fetch
def csrf_token():
    if "csrf" not in session: session["csrf"] = secrets.token_urlsafe(16)
    return session["csrf"]
@app.before_request
def _csrf():
    if request.method == "POST" and not request.path.startswith("/api/verify-requests/"):  # bot API uses bearer auth, no cookies
        t = request.form.get("csrf") or request.headers.get("X-CSRF")
        if not t or t != session.get("csrf"): abort(400, "Bad CSRF token, reload the page.")
def csrf_field(): return Markup('<input type=hidden name=csrf value="%s">' % csrf_token())
def admin_notices():
    if not (me() and me()["is_admin"]): return []
    d = db(); rows = d.execute("SELECT * FROM notices WHERE member_id=? AND seen=0 ORDER BY id DESC", (me()["id"],)).fetchall()
    d.execute("UPDATE notices SET seen=1 WHERE member_id=? AND seen=0", (me()["id"],)); d.commit(); return rows
app.jinja_env.globals.update(REACTIONS=REACTIONS, csrf_token=csrf_token, csrf_field=csrf_field, admin_notices=admin_notices, me=me)
def start_session(mid):
    session.clear(); session.permanent = True; session["mid"] = mid; csrf_token()

def page(body, tab="", **kw): return render_template_string(ui.BASE + body + ui.TABS, tab=tab, **kw)

# ---------- public: signup + login ----------
@app.route("/manifest.webmanifest")
def webmanifest():
    return Response(json.dumps({
        "name": "Grunions Water Polo", "short_name": "Grunions", "start_url": "/", "scope": "/", "display": "standalone",
        "background_color": "#0a0a0b", "theme_color": "#0a0a0b",
        "icons": [
            {"src": "/static/icons/icon-192.png", "sizes": "192x192", "type": "image/png", "purpose": "any"},
            {"src": "/static/icons/icon-512.png", "sizes": "512x512", "type": "image/png", "purpose": "any"},
            {"src": "/static/icons/maskable-512.png", "sizes": "512x512", "type": "image/png", "purpose": "maskable"},
        ],
    }), mimetype="application/manifest+json")
@app.route("/")
def index(): return redirect("/home" if me() else "/join")

@app.route("/join", methods=["GET", "POST"])
def join():
    if request.method == "POST":
        f = {k: (request.form.get(k) or "").strip() for k in ("first", "last", "email", "phone")}
        if not all(f.values()) or not re.match(r"[^@\s]+@[^@\s]+\.[^@\s]+$", f["email"]):
            flash("Please fill in every field with a valid email."); return redirect("/join")
        email = f["email"].lower(); d = db()
        if d.execute("SELECT 1 FROM members WHERE email=?", (email,)).fetchone():
            flash("You already have an account. We sent you a login link instead.")
            return send_link(email)
        cur = d.execute("INSERT INTO members(first,last,email,phone,is_admin) VALUES(?,?,?,?,?)",
                        (f["first"], f["last"], email, f["phone"], int(email in ADMIN_EMAILS)))
        d.commit(); start_session(cur.lastrowid)
        flash(f"Welcome to the Grunions, {f['first']}! Find a coach on deck to get checked in.")
        return redirect("/home")
    return page(T["join"])

def smtp_ready(): return all(SMTP.values())
def send_email(to, subject, text):
    """Send via SMTP (Gmail app password, Resend, Brevo...). Port 465 = SSL, otherwise STARTTLS."""
    import smtplib, ssl
    from email.message import EmailMessage
    msg = EmailMessage(); msg["From"] = SMTP["MAIL_FROM"]; msg["To"] = to; msg["Subject"] = subject; msg.set_content(text)
    port = int(SMTP["SMTP_PORT"]); ctx = ssl.create_default_context()
    if port == 465: srv = smtplib.SMTP_SSL(SMTP["SMTP_HOST"], port, context=ctx, timeout=15)
    else: srv = smtplib.SMTP(SMTP["SMTP_HOST"], port, timeout=15); srv.starttls(context=ctx)
    with srv: srv.login(SMTP["SMTP_USER"], SMTP["SMTP_PASSWORD"]); srv.send_message(msg)
def send_link(email):
    m = db().execute("SELECT id, first FROM members WHERE email=? AND COALESCE(role,'')!='system'", (email,)).fetchone()
    link = None
    if m:
        tok = secrets.token_urlsafe(32)
        db().execute("INSERT INTO login_tokens VALUES(?,?,?,0)", (hashlib.sha256(tok.encode()).hexdigest(), m["id"],
                     (dt.datetime.utcnow() + dt.timedelta(minutes=LINK_MINUTES)).isoformat())); db().commit()
        link = (PUBLIC_URL.rstrip("/") if PUBLIC_URL else request.host_url.rstrip("/")) + "/auth/" + tok
        if smtp_ready():
            try: send_email(email, "Your Grunions login link", f"Hi {m['first']},\n\nTap to sign in to the Grunions team app:\n{link}\n\n"
                            f"This link works once and expires in {LINK_MINUTES} minutes. If you didn't ask for it, ignore this email.\n\nGrunions Water Polo")
            except Exception as e: app.logger.error("login email to %s failed: %s", email, e)
        elif DEV_SHOW_LINKS: app.logger.warning("MAGIC LINK for %s: %s", email, link)
        else: app.logger.error("No SMTP configured; login link for %s not sent", email)
    msg = f"If that email is on the team, a login link is on its way (valid {LINK_MINUTES} minutes)."
    if DEV_SHOW_LINKS and link: msg += f'<br><b>Dev mode:</b> <a href="{link}">open your login link</a>'
    flash(msg); return redirect("/login")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST": return send_link((request.form.get("email") or "").strip().lower())
    return page(T["login"])

@app.route("/auth/<tok>")
def auth(tok):
    d = db(); h = hashlib.sha256(tok.encode()).hexdigest()
    r = d.execute("SELECT * FROM login_tokens WHERE token_hash=?", (h,)).fetchone()
    if not r or r["used"] or r["expires"] < dt.datetime.utcnow().isoformat():
        flash("That login link is invalid or expired. Request a new one."); return redirect("/login")
    d.execute("UPDATE login_tokens SET used=1 WHERE token_hash=?", (h,)); d.commit()
    start_session(r["member_id"]); return redirect("/home")
# ---------- Sign in with Google (OpenID Connect) ----------
GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID"); GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET")
oauth = None
def google_enabled(): return bool(GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET)
def google_client():
    global oauth
    if oauth is None:
        from authlib.integrations.flask_client import OAuth
        oauth = OAuth(app)
        oauth.register("google", client_id=GOOGLE_CLIENT_ID, client_secret=GOOGLE_CLIENT_SECRET,
                       server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
                       client_kwargs={"scope": "openid email profile"})
    return oauth.google
def google_redirect_uri(): return (PUBLIC_URL.rstrip("/") if PUBLIC_URL else request.host_url.rstrip("/")) + "/auth/google/callback"
def google_authorize_redirect():  # Authlib stores state + nonce in the session and checks them on return
    return google_client().authorize_redirect(google_redirect_uri(), nonce=secrets.token_urlsafe(16), prompt="select_account")
def google_userinfo():  # exchanges the code, verifies state, ID-token signature, audience and nonce
    return google_client().authorize_access_token().get("userinfo") or {}
app.jinja_env.globals.update(google_enabled=google_enabled)

@app.route("/auth/google")
def auth_google():
    if not google_enabled(): abort(404)
    return google_authorize_redirect()

@app.route("/auth/google/callback")
def auth_google_callback():
    if not google_enabled(): abort(404)
    try: info = google_userinfo()
    except Exception as e:
        app.logger.warning("Google sign-in failed: %s", e); flash("Google sign-in didn't work. Try again or use an email link."); return redirect("/login")
    email = (info.get("email") or "").strip().lower()
    if not email or info.get("email_verified") not in (True, "true"):
        flash("Your Google email isn't verified. Use an email login link instead."); return redirect("/login")
    d = db(); m = d.execute("SELECT id, role FROM members WHERE lower(email)=?", (email,)).fetchone()
    if m and (m["role"] or "") == "system": abort(403)
    if not m:  # same as /join (open signup); admin only via ADMIN_EMAIL
        first = (info.get("given_name") or (info.get("name") or email.split("@")[0]).split()[0]).strip()
        last = (info.get("family_name") or " ".join((info.get("name") or "").split()[1:]) or "-").strip()
        mid = d.execute("INSERT INTO members(first,last,email,phone,is_admin) VALUES(?,?,?,?,?)", (first, last, email, "", int(email in ADMIN_EMAILS))).lastrowid
        d.commit(); start_session(mid)
        flash(f"Welcome to the Grunions, {first}! Find a coach on deck to get checked in."); return redirect("/home")
    start_session(m["id"]); return redirect("/home")

@app.route("/logout")
def logout(): session.clear(); return redirect("/login")

# ---------- member ----------
@app.route("/home", methods=["GET", "POST"])
@login_required
def home():
    m = me(); d = db()
    if request.method == "POST":
        num = (request.form.get("usawp_number") or "").strip()
        if not re.fullmatch(r"[0-9]{4,10}", num):
            flash("Membership number must be 4-10 digits."); return redirect("/home")
        since = (dt.datetime.now() - dt.timedelta(hours=1)).isoformat(timespec="seconds")
        if d.execute("SELECT COUNT(*) FROM usawp_submits WHERE member_id=? AND at>=?", (m["id"], since)).fetchone()[0] >= 3:
            flash("You can only submit a membership number 3 times per hour."); return redirect("/home")
        d.execute("UPDATE members SET usawp_number=? WHERE id=?", (num, m["id"]))
        d.execute("INSERT INTO usawp_submits(member_id, at) VALUES(?,?)", (m["id"], dt.datetime.now().isoformat(timespec="seconds")))
        create_verify_request(d, m["id"], update_pending=True)
        return redirect("/home")
    hist = d.execute("SELECT practice_date, location FROM checkins WHERE member_id=? ORDER BY practice_date DESC", (m["id"],)).fetchall()
    month = dt.date.today().strftime("%Y-%m")
    ensure_schedule(d)
    nextp = d.execute("SELECT * FROM practices WHERE date>=? AND cancelled=0 ORDER BY date LIMIT 1", (dt.date.today().isoformat(),)).fetchone()
    nextp_n = d.execute("SELECT COUNT(*) FROM rsvps WHERE practice_id=? AND going=1", (nextp["id"],)).fetchone()[0] if nextp else 0
    nextp_mine = d.execute("SELECT going FROM rsvps WHERE practice_id=? AND member_id=?", (nextp["id"], m["id"])).fetchone() if nextp else None
    nextp_mine = nextp_mine[0] if nextp_mine else None
    notices = d.execute("SELECT * FROM notices WHERE member_id=? AND seen=0 ORDER BY id DESC", (m["id"],)).fetchall()
    d.execute("UPDATE notices SET seen=1 WHERE member_id=? AND seen=0", (m["id"],)); d.commit()
    ann = d.execute("SELECT m.*, p.first FROM messages m JOIN members p ON p.id=m.member_id WHERE announcement=1 AND channel='team' ORDER BY m.id DESC LIMIT 1").fetchone()
    vr_pending = d.execute("SELECT 1 FROM verify_requests WHERE member_id=? AND status='pending'", (m["id"],)).fetchone() is not None
    return page(T["home"], tab="home", m=m, hist=hist, nmonth=sum(1 for h in hist if h['practice_date'].startswith(month)), ann=ann, notices=notices, nextp=nextp, nextp_n=nextp_n, nextp_mine=nextp_mine, vr_pending=vr_pending)

# ---------- chat ----------
def msg_dict(r):
    return {"id": r["id"], "body": r["body"], "ann": bool(r["announcement"]), "at": r["at"] + "Z",
            "who": f'{r["first"]} {r["last"][:1]}.', "mine": r["member_id"] == me()["id"], "admin": bool(r["is_admin"]),
            "image": {"thumb": f"/media/{r['id']}/thumb", "full": f"/media/{r['id']}/full"} if r["image"] else None}
def can_read(ch): return ch == "team" or (ch == "coaches" and is_staff())
def save_image(f):
    """Validate + re-encode an upload. Returns stored base name. Strips metadata, fixes rotation, resizes (max 1600px, thumb 480px)."""
    from PIL import Image, ImageOps
    try:
        import pillow_heif; pillow_heif.register_heif_opener()
    except ImportError: pass
    data = f.read(MAX_UPLOAD + 1)
    if len(data) > MAX_UPLOAD: raise ValueError("Image is larger than 8 MB.")
    try:
        im = Image.open(io.BytesIO(data)); fmt = (im.format or "").upper(); im.load()
    except Exception: raise ValueError("That file isn't a supported image.")
    if fmt not in ("JPEG", "PNG", "GIF", "WEBP", "HEIF", "HEIC"): raise ValueError("Use JPG, PNG, GIF, WEBP or HEIC.")
    os.makedirs(UPLOADS, exist_ok=True); name = secrets.token_hex(12)
    if fmt == "GIF" and getattr(im, "is_animated", False) and len(data) <= MAX_UPLOAD:
        open(os.path.join(UPLOADS, name + ".gif"), "wb").write(data); ext = "gif"   # keep animation
    else:
        im = ImageOps.exif_transpose(im); im = im.convert("RGBA" if im.mode in ("RGBA", "LA", "P") and fmt in ("PNG", "WEBP", "GIF") else "RGB")
        im.thumbnail((1600, 1600)); im.save(os.path.join(UPLOADS, name + ".webp"), "WEBP", quality=85); ext = "webp"
    th = Image.open(os.path.join(UPLOADS, f"{name}.{ext}")); th = th.convert("RGBA" if th.mode in ("RGBA", "P") else "RGB"); th.thumbnail((480, 480))
    th.save(os.path.join(UPLOADS, name + "_t.webp"), "WEBP", quality=80)
    return f"{name}.{ext}"
@app.route("/media/<int:mid>/<kind>")
@login_required
def media(mid, kind):
    r = db().execute("SELECT channel, image FROM messages WHERE id=?", (mid,)).fetchone()
    if not r or not r["image"] or kind not in ("thumb", "full"): abort(404)
    if not can_read(r["channel"]): abort(403)
    from flask import send_from_directory
    fn = r["image"].rsplit(".", 1)[0] + "_t.webp" if kind == "thumb" else r["image"]
    resp = send_from_directory(UPLOADS, fn, max_age=86400); resp.headers["Cache-Control"] = "private, max-age=86400"; return resp
@app.errorhandler(413)
def too_big(e): return jsonify(error="Image is larger than 8 MB."), 413
@app.route("/api/messages/<int:mid>/react", methods=["POST"])
@login_required
def react(mid):
    d = db(); r = d.execute("SELECT channel FROM messages WHERE id=?", (mid,)).fetchone()
    if not r: abort(404)
    if not can_read(r["channel"]): abort(403)
    e = (request.get_json(silent=True) or {}).get("emoji")
    if e not in REACTIONS: return jsonify(error="unsupported emoji"), 400
    if d.execute("DELETE FROM reactions WHERE message_id=? AND member_id=? AND emoji=?", (mid, me()["id"], e)).rowcount == 0:
        d.execute("INSERT INTO reactions VALUES(?,?,?)", (mid, me()["id"], e))
    d.commit(); return jsonify(reactions_for(d, r["channel"]).get(str(mid), {}))
def reactions_for(d, ch):
    out = {}
    for x in d.execute("""SELECT x.message_id, x.emoji, COUNT(*) n, SUM(x.member_id=?) mine FROM reactions x JOIN messages m ON m.id=x.message_id
        WHERE m.channel=? AND m.id > (SELECT COALESCE(MAX(id),0)-300 FROM messages WHERE channel=?) GROUP BY x.message_id, x.emoji""", (me()["id"], ch, ch)):
        out.setdefault(str(x["message_id"]), {})[x["emoji"]] = {"n": x["n"], "mine": bool(x["mine"])}
    return out
@app.route("/api/reactions")
@login_required
def api_reactions():
    ch = request.args.get("c", "team")
    if ch not in ("team", "coaches") or not can_read(ch): abort(403)
    return jsonify(reactions_for(db(), ch))
@app.route("/chat")
@login_required
def chat():
    ch = request.args.get("c", "team")
    if ch == "coaches" and not is_staff(): abort(403)
    if ch not in ("team", "coaches"): ch = "team"
    return page(T["chat"], tab="chat", ch=ch)
@app.route("/api/messages", methods=["GET", "POST"])
@login_required
def api_messages():
    d = db(); ch = request.args.get("c", "team")
    if ch not in ("team", "coaches") or (ch == "coaches" and not is_staff()): abort(403)
    if request.method == "POST":
        image = None
        if request.files.get("image"):
            j = request.form
            try: image = save_image(request.files["image"])
            except ValueError as e: return jsonify(error=str(e)), 400
        else: j = request.get_json(silent=True) or {}
        body = (j.get("body") or "").strip()[:2000]
        if not body and not image: abort(400)
        ann = 1 if (j.get("announcement") in (True, "true", "1") and me()["is_admin"] and ch == "team") else 0
        d.execute("INSERT INTO messages(member_id,body,announcement,channel,image) VALUES(?,?,?,?,?)", (me()["id"], body, ann, ch, image)); d.commit()
        return jsonify(ok=True)
    after = request.args.get("after", 0, type=int)
    rows = d.execute("""SELECT m.*, p.first, p.last, p.is_admin FROM messages m JOIN members p ON p.id=m.member_id
      WHERE m.id>? AND m.channel=? ORDER BY m.id DESC LIMIT 200""", (after, ch)).fetchall()
    return jsonify([msg_dict(r) for r in reversed(rows)])

# ---------- practices ----------
RECURRING = {1: ("Marina High School", "19:00", "20:30"), 4: ("Westminster High School", "19:00", "20:30")}  # Tue, Fri
def ensure_schedule(d, weeks=4):
    today = dt.date.today()
    for i in range(weeks * 7):
        day = today + dt.timedelta(days=i)
        if day.weekday() in RECURRING:
            loc, a, b = RECURRING[day.weekday()]
            d.execute("INSERT OR IGNORE INTO practices(date,start,end,location) VALUES(?,?,?,?)", (day.isoformat(), a, b, loc))
    d.commit()
def fmt_t(t): h, m = map(int, t.split(":")); return f"{(h-1)%12+1}:{m:02d}{'pm' if h>=12 else 'am'}"
def fmt_d(s):
    d = dt.date.fromisoformat(s); return d.strftime("%a %b ") + str(d.day)
app.jinja_env.globals.update(fmt_t=fmt_t, fmt_d=fmt_d)
@app.route("/practices", methods=["GET", "POST"])
@login_required
def practices():
    d = db(); ensure_schedule(d)
    if request.method == "POST":
        a = request.form.get("action"); pid = request.form.get("pid", type=int)
        if a in ("going", "notgoing", "clear"):
            if a == "clear": d.execute("DELETE FROM rsvps WHERE practice_id=? AND member_id=?", (pid, me()["id"]))
            else: d.execute("INSERT INTO rsvps(practice_id,member_id,going) VALUES(?,?,?) ON CONFLICT DO UPDATE SET going=excluded.going, at=CURRENT_TIMESTAMP", (pid, me()["id"], int(a == "going")))
        elif not me()["is_admin"]: abort(403)
        elif a == "add":
            try: d.execute("INSERT INTO practices(date,start,end,location,note) VALUES(?,?,?,?,?)", (request.form["date"], request.form.get("start") or "19:00", request.form.get("end") or "20:30", request.form.get("location") or "TBD", request.form.get("note")))
            except sqlite3.IntegrityError: flash("A practice already exists at that place on that date.")
        elif a == "edit":
            d.execute("UPDATE practices SET start=?, end=?, location=?, note=? WHERE id=?", (request.form["start"], request.form["end"], request.form["location"], request.form.get("note"), pid))
        elif a in ("cancel", "restore"):
            d.execute("UPDATE practices SET cancelled=? WHERE id=?", (int(a == "cancel"), pid))
        d.commit(); return redirect("/home" if "/home" in (request.referrer or "") else "/practices#p%s" % (pid or ""))
    ps = d.execute("SELECT * FROM practices WHERE date>=? ORDER BY date, start LIMIT 16", (dt.date.today().isoformat(),)).fetchall()
    data = []
    for p in ps:
        rv = d.execute("SELECT r.going, m.first, m.last, m.id FROM rsvps r JOIN members m ON m.id=r.member_id WHERE practice_id=? ORDER BY m.first", (p["id"],)).fetchall()
        mine = next((r["going"] for r in rv if r["id"] == me()["id"]), None)
        data.append(dict(p=p, going=[r for r in rv if r["going"]], notgoing=[r for r in rv if not r["going"]], mine=mine))
    return page(T["practices"], tab="practices", data=data)

# ---------- verification requests (bot) ----------
BOT_EMAIL = "bot@grunions.local"
def bot_member_id(d):
    r = d.execute("SELECT id FROM members WHERE email=?", (BOT_EMAIL,)).fetchone()
    if r: return r["id"]
    return d.execute("INSERT INTO members(first,last,email,phone,role) VALUES('Grunions','bot',?,'','system')", (BOT_EMAIL,)).lastrowid
def vr_dict(r):
    return {k: r[k] for k in ("id", "member_id", "name", "email", "member_number", "requested_by", "status", "created", "answered", "note")} | {"result": json.loads(r["result"]) if r["result"] else None}
def webhook_headers():
    h = {"Content-Type": "application/json"}
    if VERIFY_WEBHOOK_KEY:
        h[VERIFY_WEBHOOK_HEADER or "Authorization"] = VERIFY_WEBHOOK_KEY if VERIFY_WEBHOOK_HEADER else "Bearer " + VERIFY_WEBHOOK_KEY
    return h
def post_verify_webhook(row):
    """POST a newly created verify request. Failures are logged and never raised."""
    if not VERIFY_WEBHOOK_URL: return "skipped (no VERIFY_WEBHOOK_URL)"
    payload = {"request_id": row["id"], "member_id": row["member_id"], "name": row["name"], "email": row["email"],
               "member_number": row["member_number"], "requested_by": row["requested_by"], "app_url": PUBLIC_URL}
    try:
        req = urllib.request.Request(VERIFY_WEBHOOK_URL, data=json.dumps(payload).encode(), headers=webhook_headers(), method="POST")
        with urllib.request.urlopen(req, timeout=5) as resp: return f"sent ({resp.status})"
    except Exception as e:
        app.logger.warning("verify webhook failed: %s", e)
        return f"failed: {e.__class__.__name__}"
def create_verify_request(d, mid, update_pending=False):
    m = d.execute("SELECT * FROM members WHERE id=?", (mid,)).fetchone()
    pending = d.execute("SELECT id FROM verify_requests WHERE member_id=? AND status='pending' ORDER BY id DESC LIMIT 1", (mid,)).fetchone()
    if pending:
        if not update_pending: return "A verification request is already pending."
        d.execute("UPDATE verify_requests SET member_number=? WHERE id=?", (m["usawp_number"], pending["id"])); d.commit()
        return f"Updated the pending verification request for {m['first']} {m['last']}."
    now = dt.datetime.now().isoformat(timespec="seconds")
    rid = d.execute("INSERT INTO verify_requests(member_id,name,email,member_number,requested_by,created) VALUES(?,?,?,?,?,?)",
                    (mid, f"{m['first']} {m['last']}", m["email"], m["usawp_number"], f"{me()['first']} {me()['last']}", now)).lastrowid
    d.commit(); r = d.execute("SELECT * FROM verify_requests WHERE id=?", (rid,)).fetchone(); wh = post_verify_webhook(r)
    d.execute("UPDATE verify_requests SET webhook=? WHERE id=?", (wh, rid)); d.commit()
    return f"Asked Grunions to verify {m['first']} {m['last']}. Webhook {wh}."
def bot_auth():
    h = request.headers.get("Authorization", "")
    if not BOT_API_KEY or not h.startswith("Bearer ") or not secrets.compare_digest(h[7:], BOT_API_KEY): abort(401)
@app.route("/api/verify-requests")
def api_verify_list():
    bot_auth(); st = request.args.get("status")
    rows = db().execute("SELECT * FROM verify_requests WHERE (? IS NULL OR status=?) ORDER BY id", (st, st)).fetchall()
    return jsonify([vr_dict(r) for r in rows])
@app.route("/api/verify-requests/<int:rid>/result", methods=["POST"])
def api_verify_result(rid):
    bot_auth(); d = db(); j = request.get_json(silent=True)
    if not isinstance(j, dict) or not isinstance(j.get("verified"), bool): return jsonify(error="JSON body with boolean 'verified' required"), 400
    r = d.execute("SELECT * FROM verify_requests WHERE id=?", (rid,)).fetchone()
    if not r: return jsonify(error="not found"), 404
    if r["status"] != "pending": return jsonify(error="already answered"), 409
    now = dt.datetime.now().isoformat(timespec="minutes"); mid = r["member_id"]
    exp = parse_date(j.get("membership_expires_on")); num = (str(j.get("member_number") or "").strip() or None)
    if j["verified"]:
        st = "expired" if exp and exp < dt.date.today() else "verified"
        d.execute("""UPDATE members SET usawp_status=?, usawp_raw='Verified by Grunions bot', usawp_number=COALESCE(?,usawp_number),
          usawp_valid_until=COALESCE(?,usawp_valid_until), usawp_updated=?, usawp_verified_by='Grunions bot', usawp_verified_at=? WHERE id=?""",
          (st, num, exp and exp.isoformat(), now, now, mid))
    else:
        d.execute("UPDATE members SET usawp_status='expired', usawp_raw='Bot: not verified', usawp_number=COALESCE(?,usawp_number), usawp_updated=? WHERE id=?", (num, now, mid))
    applied, unknown = [], []
    for item, val in (j.get("compliance") or {}).items():
        q = next((q for q in d.execute("SELECT * FROM requirements") if norm(q["name"]) == norm(item) or any(k and k in norm(item) for k in (q["keywords"] or "").split(","))), None)
        e = parse_date(val)
        if not q or not e: unknown.append(item); continue
        d.execute("""INSERT INTO member_reqs VALUES(?,?,?,?,'bot','Grunions bot',?) ON CONFLICT(member_id,req_id) DO UPDATE SET
          expires_on=excluded.expires_on, completed_on=COALESCE(completed_on,excluded.completed_on), source='bot', by='Grunions bot', at=excluded.at""",
          (mid, q["id"], dt.date.today().isoformat(), e.isoformat(), now)); applied.append(q["name"])
    note = (str(j.get("note") or "")[:500]) or None
    d.execute("UPDATE verify_requests SET status='done', answered=?, result=?, note=? WHERE id=?", (now, json.dumps(j), note, rid))
    expire_sweep(d)
    text = f"Verification for {r['name']}: {'verified' if j['verified'] else 'NOT verified'}"
    if exp: text += f", membership expires {exp.isoformat()}"
    if applied: text += f"; updated {', '.join(applied)}"
    if note: text += f". Note: {note}"
    d.execute("INSERT INTO messages(member_id,body,channel) VALUES(?,?,'coaches')", (bot_member_id(d), text))
    for a in d.execute("SELECT id FROM members WHERE is_admin=1").fetchall(): d.execute("INSERT INTO notices(member_id, body) VALUES(?,?)", (a["id"], text))
    d.commit()
    return jsonify(ok=True, request_id=rid, member_id=mid, applied_compliance=applied, ignored_compliance=unknown)

# ---------- admin ----------
def signup_url(): return (PUBLIC_URL or request.host_url.rstrip("/")) + "/join"
@app.route("/qr.svg")
@admin_required
def qr_svg():
    img = qrcode.make(signup_url(), image_factory=qrcode.image.svg.SvgPathImage, box_size=20)
    buf = io.BytesIO(); img.save(buf); return Response(buf.getvalue(), mimetype="image/svg+xml")
@app.route("/qr")
@admin_required
def qr_page():
    return page(T["qr_page"], tab="admin", u=signup_url())

@app.route("/admin", methods=["GET", "POST"])
@staff_required
def admin():
    d = db(); date = request.values.get("date") or dt.date.today().isoformat()
    if request.method == "POST":
        mid = int(request.form["member_id"])
        if request.form.get("action") in ("verify", "req", "role", "ask_bot") and not me()["is_admin"]: abort(403)
        if request.form.get("action") == "verify":
            num = (request.form.get("number") or "").strip()[:20] or None
            vu = parse_date(request.form.get("valid_until")); now = dt.datetime.now().isoformat(timespec="minutes")
            if vu and vu < dt.date.today(): flash("That expiration date is in the past, so not marked verified.")
            elif not vu and not request.form.get("no_date"): flash("Please enter the expiration date from Sport:80 (or tick 'no date').")
            else:
                d.execute("""UPDATE members SET usawp_status='verified', usawp_raw='Manually verified', usawp_number=COALESCE(?,usawp_number),
                  usawp_valid_until=COALESCE(?,usawp_valid_until), usawp_updated=?, usawp_verified_by=?, usawp_verified_at=? WHERE id=?""",
                  (num, vu.isoformat() if vu else None, now, f"{me()['first']} {me()['last']}", now, mid))
        elif request.form.get("action") == "ask_bot":
            flash(create_verify_request(d, mid))
        elif request.form.get("action") == "req":
            rid = int(request.form["req_id"]); done = parse_date(request.form.get("completed_on")); exp = parse_date(request.form.get("expires_on"))
            q = d.execute("SELECT * FROM requirements WHERE id=?", (rid,)).fetchone()
            if q and q["expires"] and not exp: flash(f"Please enter the expiration date for {q['name']}.")
            elif not (done or exp): flash("Enter a completed or expiration date.")
            else:
                d.execute("""INSERT INTO member_reqs VALUES(?,?,?,?,'manual',?,?) ON CONFLICT(member_id,req_id) DO UPDATE SET completed_on=excluded.completed_on,
                  expires_on=excluded.expires_on, source='manual', by=excluded.by, at=excluded.at""", (mid, rid, done and done.isoformat(), exp and exp.isoformat(),
                  f"{me()['first']} {me()['last']}", dt.datetime.now().isoformat(timespec="minutes")))
        elif request.form.get("action") == "role":
            role = request.form.get("role")
            if role != "admin" and is_last_admin(d, mid): flash("Can't remove the last admin."); return redirect(request.full_path)
            d.execute("UPDATE members SET role=?, is_admin=? WHERE id=?", ("coach" if role in ("coach", "admin") else "athlete", 1 if role == "admin" else 0, mid))
        elif request.form.get("action") == "undo":
            d.execute("DELETE FROM checkins WHERE member_id=? AND practice_date=?", (mid, date))
        else:
            d.execute("INSERT OR IGNORE INTO checkins(member_id,practice_date,location) VALUES(?,?,?)", (mid, date, location_for(date)))
        d.commit(); return redirect(url_for("admin", date=date, q=request.form.get("q", "")))
    q = request.args.get("q", "").strip()
    pr = d.execute("SELECT * FROM practices WHERE date=? AND cancelled=0 ORDER BY start LIMIT 1", (date,)).fetchone()
    rows = d.execute("""SELECT m.*, c.id AS cid, rv.going AS going,
      (SELECT status FROM verify_requests WHERE member_id=m.id ORDER BY id DESC LIMIT 1) AS vr_status,
      (SELECT note FROM verify_requests WHERE member_id=m.id ORDER BY id DESC LIMIT 1) AS vr_note FROM members m LEFT JOIN checkins c ON c.member_id=m.id AND c.practice_date=?
      LEFT JOIN rsvps rv ON rv.member_id=m.id AND rv.practice_id=?
      WHERE COALESCE(m.role,'')!='system' AND (?='' OR m.first||' '||m.last||' '||m.email LIKE '%'||?||'%') ORDER BY COALESCE(rv.going,-1)=1 DESC, c.id IS NULL, m.last, m.first""", (date, pr["id"] if pr else -1, q, q)).fetchall()
    n = sum(1 for r in rows if r["cid"])
    return page(T["admin"],
        tab="admin", date=date, q=q, rows=rows, n=n, loc=(pr["location"] if pr else location_for(date)), pr=pr, rsvp_n=sum(1 for r in rows if r["going"] == 1))

@app.route("/expiring", methods=["GET", "POST"])
@admin_required
def expiring():
    d = db(); days = request.args.get("days", EXPIRING_DAYS, type=int)
    if request.method == "POST":
        ids = [int(request.form["member_id"])] if request.form.get("member_id") else [x["id"] for k, v in expiry_report(d, days).items() for x in v]
        for mid in ids: remind(d, mid, by=f"{me()['first']} {me()['last']}")
        d.commit(); flash(f"In-app reminder posted to {len(ids)} member(s)."); return redirect(url_for("expiring", days=days))
    rep = expiry_report(d, days)
    return page(T["expiring"], tab="admin", rep=rep, days=days)
@app.route("/requirements", methods=["GET", "POST"])
@admin_required
def requirements_page():
    d = db()
    if request.method == "POST":
        a = request.form.get("action")
        if a == "add" and request.form.get("name", "").strip():
            d.execute("INSERT INTO requirements(name,applies_to,keywords,expires) VALUES(?,?,?,?)", (request.form["name"].strip(), request.form.get("applies_to", "all"),
                      norm(request.form.get("keywords") or request.form["name"].split()[0]), 1 if request.form.get("expires") else 0))
        elif a == "save":
            d.execute("UPDATE requirements SET applies_to=?, expires=?, active=?, keywords=? WHERE id=?", (request.form.get("applies_to", "all"), 1 if request.form.get("expires") else 0,
                      1 if request.form.get("active") else 0, ",".join(norm(k) for k in request.form.get("keywords", "").split(",") if norm(k)), int(request.form["id"])))
        d.commit(); return redirect("/requirements")
    reqs = d.execute("SELECT * FROM requirements ORDER BY id").fetchall()
    return page(T["requirements_page"], tab="admin", reqs=reqs)

@app.route("/api/expiring")
def api_expiring():
    ok = (me() and me()["is_admin"]) or (CRON_KEY and secrets.compare_digest(request.args.get("key", ""), CRON_KEY))
    if not ok: abort(403)
    return jsonify(date=dt.date.today().isoformat(), window_days=request.args.get("days", EXPIRING_DAYS, type=int), **expiry_report(db(), request.args.get("days", EXPIRING_DAYS, type=int)))

def is_last_admin(d, mid):
    r = d.execute("SELECT is_admin FROM members WHERE id=?", (mid,)).fetchone()
    return bool(r and r["is_admin"]) and d.execute("SELECT COUNT(*) FROM members WHERE is_admin=1").fetchone()[0] <= 1
@app.route("/admins", methods=["GET", "POST"])
@admin_required
def admins():
    d = db()
    if request.method == "POST":
        mid = int(request.form.get("member_id") or 0); act = request.form.get("action")
        m = d.execute("SELECT * FROM members WHERE id=? AND COALESCE(role,'')!='system'", (mid,)).fetchone()
        if not m: abort(404)
        if act == "make_admin": d.execute("UPDATE members SET is_admin=1 WHERE id=?", (mid,))
        elif act == "remove_admin":
            if is_last_admin(d, mid): flash("Can't remove the last admin."); return redirect("/admins")
            if m["email"] in ADMIN_EMAILS: flash(f"{m['first']} is set as admin by the ADMIN_EMAIL setting; change it there."); return redirect("/admins")
            d.execute("UPDATE members SET is_admin=0 WHERE id=?", (mid,))
        elif act == "make_coach": d.execute("UPDATE members SET role='coach' WHERE id=?", (mid,))
        elif act == "remove_coach": d.execute("UPDATE members SET role='athlete' WHERE id=?", (mid,))
        else: abort(400)
        d.commit(); flash(f"Updated {m['first']} {m['last']}."); return redirect("/admins")
    rows = d.execute("SELECT * FROM members WHERE COALESCE(role,'')!='system' ORDER BY is_admin DESC, role='coach' DESC, last, first").fetchall()
    return page(T["admins"], tab="admin", rows=rows, n_admins=sum(1 for r in rows if r["is_admin"]), boot=ADMIN_EMAILS)

@app.route("/members")
@admin_required
def members():
    rows = db().execute("""SELECT m.*, (SELECT COUNT(*) FROM checkins WHERE member_id=m.id) AS visits,
      (SELECT MAX(practice_date) FROM checkins WHERE member_id=m.id) AS lastp FROM members m WHERE COALESCE(role,'')!='system' ORDER BY last, first""").fetchall()
    c = {s: sum(1 for r in rows if r["usawp_status"] == s) for s in ("verified", "pending", "expired", "unknown")}
    return page(T["members"],
        tab="admin", rows=rows, c=c)
@app.route("/members.csv")
@admin_required
def members_csv():
    out = io.StringIO(); w = csv.writer(out)
    w.writerow(["first", "last", "email", "phone", "usawp_status", "usawp_raw", "member_number", "valid_until", "verified_by", "verified_at"])
    for r in db().execute("SELECT * FROM members ORDER BY last"): w.writerow([r["first"], r["last"], r["email"], r["phone"], r["usawp_status"], r["usawp_raw"], r["usawp_number"], r["usawp_valid_until"], r["usawp_verified_by"], r["usawp_verified_at"]])
    return Response(out.getvalue(), mimetype="text/csv", headers={"Content-Disposition": "attachment; filename=grunions-members.csv"})

# ---- USAWP (Sport:80 Smart List export) import ----
ALIASES = {  # normalized header -> field. Sport:80 Smart List columns vary by chosen columns, so match loosely.
    "first": ["firstname", "forename", "givenname", "legalfirstname"],
    "last": ["lastname", "surname", "familyname", "legallastname"],
    "name": ["name", "fullname", "membername", "profilename"],
    "email": ["email", "emailaddress", "primaryemail", "profileemail"],
    "status": ["status", "membershipstatus", "individualmembershipstatus", "addonstatus"],
    "number": ["idnumber", "usawpnumber", "membernumber", "membershipnumber", "membershipid", "memberid", "usawpid", "individualmembershipmembernumber"],
    "contact": ["contactid", "sportcontactid", "profileid"],
    "valid": ["validuntil", "membershipexpirydate", "membershipexpirationdate", "membershipvaliduntil", "expiry", "validthrough", "expirydate", "expirationdate", "expires", "enddate", "individualmembershipvaliduntil", "individualmembershipexpirydate"],
}
EXCLUDE_KW = [k for r in DEFAULT_REQS for k in r[2].split(",")]
def map_headers(headers):
    m = {}
    for i, h in enumerate(headers):
        n = norm(h)
        if any(k in n for k in EXCLUDE_KW): continue  # e.g. "Background Screening Expiration Date" is not membership expiry
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
        if ("email" in hm or "name" in hm or "last" in hm) and ("status" in hm or "number" in hm or "valid" in hm): return hm, rows[i + 1:], [str(c or "") for c in r]
    return None, rows, []
def import_roster(fname, data):
    hm, rows, hdr = read_rows(fname, data)
    if not hm: return None
    d = db()
    global EXCLUDE_KW; EXCLUDE_KW = req_keywords(d)
    reqcols = {}  # req_id -> {"exp": col, "done": col, "status": col}
    for q in d.execute("SELECT * FROM requirements WHERE active=1"):
        for i, h in enumerate(hdr):
            n = norm(h)
            if not any(k and k in n for k in (q["keywords"] or "").split(",")): continue
            kind = "exp" if any(x in n for x in ("expir", "validthrough", "validuntil", "validto", "enddate")) else "done" if any(x in n for x in ("complet", "date", "signed")) else "status" if "status" in n else None
            if kind: reqcols.setdefault(q["id"], {}).setdefault(kind, i)
    now = dt.datetime.now().isoformat(timespec="minutes")
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
        for rid, cols in reqcols.items():
            g_ = lambda k: r[cols[k]] if k in cols and cols[k] < len(r) else None
            exp, done, sraw = parse_date(g_("exp")), parse_date(g_("done")), norm(str(g_("status") or ""))
            if not done and sraw in ("current", "complete", "completed", "valid", "passed", "approved", "yes", "signed"): done = dt.date.today()
            if exp or done:
                d.execute("""INSERT INTO member_reqs VALUES(?,?,?,?,'Sport:80 import','import',?) ON CONFLICT(member_id,req_id) DO UPDATE SET
                  completed_on=COALESCE(excluded.completed_on,completed_on), expires_on=COALESCE(excluded.expires_on,expires_on), source=excluded.source, at=excluded.at""",
                  (mid, rid, done.isoformat() if done else None, exp.isoformat() if exp else None, now))
                stats["req_updates"] = stats.get("req_updates", 0) + 1
        if cell(r, "contact"): d.execute("UPDATE members SET sport80_contact_id=? WHERE id=?", (str(cell(r, "contact")).strip(), mid))
        st = classify(raw, valid)
        if st == "unknown" and not raw and valid and valid >= dt.date.today(): st = "verified"  # no status column: future expiry = current
        rank = {"verified": 3, "pending": 2, "expired": 1, "unknown": 0}[st]
        if mid not in best or rank > best[mid][0]:  # keep best status if someone appears twice
            best[mid] = (rank, st, raw, str(cell(r, "number") or ""), valid.isoformat() if valid else None)
    for mid, (_, st, raw, num, valid) in best.items():
        d.execute("UPDATE members SET usawp_status=?,usawp_raw=?,usawp_number=?,usawp_valid_until=COALESCE(?,usawp_valid_until),usawp_updated=? WHERE id=?", (st, raw, num, valid, now, mid))
        if st == "verified": d.execute("UPDATE members SET usawp_verified_by='Sport:80 import', usawp_verified_at=? WHERE id=?", (now, mid))
    expire_sweep(d)
    d.commit(); stats["matched"] = len(best); return stats

@app.route("/import", methods=["GET", "POST"])
@admin_required
def import_page():
    stats = None
    if request.method == "POST":
        f = request.files.get("file")
        if not f or not f.filename: flash("Choose a file.")
        else:
            stats = import_roster(f.filename, f.read())
            if stats is None: flash("Couldn't find name/email and status columns in that file.")
    return page(T["import_page"], tab="admin", stats=stats)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5055)))
