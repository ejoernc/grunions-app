import os, re, tempfile
os.environ["GRUNIONS_DB"] = tempfile.mktemp(suffix=".db"); os.environ["ADMIN_EMAIL"] = "eli@example.com"; os.environ["DEV_SHOW_LINKS"] = "1"; os.environ["GRUNIONS_SHEET_SYNC"] = "inline"
import app as A
def client():
    c = A.app.test_client(); return c
def csrf(c, path):
    return re.search(r'(?:name=csrf value=|const CSRF=)"([^"]+)"', c.get(path).get_data(as_text=True)).group(1)
def join(c, first, last, email):
    return c.post("/join", data=dict(csrf=csrf(c, "/join"), first=first, last=last, email=email, phone="555-0100"), follow_redirects=True)
ok = lambda cond, name: print(("PASS " if cond else "FAIL ") + name) or cond
def people_row(html, name):
    i = html.find(">" + name + "</span>")
    if i < 0: return ""
    start = html.rfind("<div class=li", 0, i)
    quoted = html.rfind('<div class="li', 0, i)
    if quoted > start: start = quoted
    end = html.find("<!--endrow-->", i)
    return html[start:end if end >= 0 else None]
eli, jane, x = client(), client(), client()
ok("Welcome" in join(eli, "Eli", "Joern", "eli@example.com").get_data(as_text=True), "QR signup creates account + logs in")
import sqlite3 as _sq
_ec = _sq.connect(os.environ["GRUNIONS_DB"]); _ec.execute("UPDATE members SET role='coach' WHERE email='eli@example.com'"); _ec.commit(); _ec.close()
join(jane, "Jane", "Doe", "jane@example.com"); join(client(), "John", "Smith", "john@example.com")
ok(x.post("/join", data=dict(first="a", last="b", email="c@d.co", phone="1")).status_code == 400, "POST without CSRF rejected")
ok(x.get("/home").status_code == 302, "anon -> login redirect")
ok(jane.get("/admin").status_code == 403 and jane.get("/members").status_code == 403 and jane.get("/import").status_code == 403 and jane.get("/qr").status_code == 403, "member blocked from admin pages")
ok(eli.get("/admin").status_code == 200, "admin can open check-in")
# magic link
r = x.post("/login", data=dict(csrf=csrf(x, "/login"), email="jane@example.com"), follow_redirects=True).get_data(as_text=True)
link = re.search(r'href="(http[^"]+/auth/[^"]+)"', r).group(1).split("localhost")[1]
ok("Hi, Jane" in x.get(link, follow_redirects=True).get_data(as_text=True), "magic link logs in")
ok("invalid or expired" in client().get(link, follow_redirects=True).get_data(as_text=True), "magic link single-use")
r = client(); t = r.post("/login", data=dict(csrf=csrf(r, "/login"), email="nobody@example.com"), follow_redirects=True).get_data(as_text=True)
ok("/auth/" not in t and "If that email" in t, "unknown email: no link, no account enumeration")
# chat
tok = csrf(jane, "/chat")
jane.post("/api/messages", json={"body": "See everyone Tuesday at Marina! <b>hi</b>", "announcement": True}, headers={"X-CSRF": tok})
tok_e = csrf(eli, "/chat")
eli.post("/api/messages", json={"body": "Heads up: $45/mo membership starts in November for all practices.", "announcement": True}, headers={"X-CSRF": tok_e})
eli.post("/api/messages", json={"body": "Bring dark + white caps Friday."}, headers={"X-CSRF": tok_e})
msgs = jane.get("/api/messages?after=0").get_json()
ok(len(msgs) == 3 and not msgs[0]["ann"] and msgs[1]["ann"], "chat posts visible; non-admin cannot announce")
ok(jane.get("/api/messages?after=%d" % msgs[1]["id"]).get_json()[0]["body"].startswith("Bring"), "poll returns only new messages")
ok(jane.post("/api/messages", json={"body": "x"}).status_code == 400, "chat POST without CSRF rejected")
ok("$45/mo" in jane.get("/home").get_data(as_text=True), "announcement shown on member home")
# admin import + checkin
with open("sample_sport80_export.csv", "rb") as f:
    t = eli.post("/import", data=dict(csrf=csrf(eli, "/transfer"), file=(f, "x.csv")), content_type="multipart/form-data").get_data(as_text=True)
ok("updated 2 members" in t, "Sport:80 import")
eli.post("/admin", data=dict(csrf=tok_e, member_id=2, date="2026-10-27")); eli.post("/admin", data=dict(csrf=tok_e, member_id=2, date="2026-10-23"))
h = x.get("/home").get_data(as_text=True)
xp = x.get("/profile").get_data(as_text=True)
ok("USAWP #1234567" in h and "expires 2027-08-31" in xp and "1234567" in h and "2027-08-31" in xp and "2 practices attended" in xp and "<summary>Attendance</summary>" not in h and "Cleared for water polo" not in h and A.fmt_phone("7205355925") == "(720) 535-5925", "member home shows the membership number on the practice card, and the practice count lives on the profile page")
ok("Checked in (1)" in eli.get("/admin?date=2026-10-27").get_data(as_text=True) and "Checked in 1 / Going" not in eli.get("/admin?date=2026-10-27").get_data(as_text=True), "check-in count per practice")
ok(eli.get("/qr.svg").data.startswith(b"<?xml"), "QR svg")
qr_page = eli.get("/qr").get_data(as_text=True)
ok("<h1>Join QR</h1>" in qr_page and "Anyone who scans this joins the team." in qr_page and "src=/qr.svg" in qr_page and ">Copy link</button>" in qr_page and ">Share</button>" in qr_page and ">Print</button>" in qr_page, "QR page has the code, share, and copy link")
# manual verify
t = eli.get("/admin?date=2026-10-27").get_data(as_text=True)
ok("Verify John on Sport:80" in eli.get("/admin/member/3").get_data(as_text=True) and "usawp.sport80.com" in eli.get("/admin/member/3").get_data(as_text=True), "Verify shown only for non-verified")
ok(jane.post("/admin", data=dict(csrf=tok, member_id=3, action="verify")).status_code == 403, "member cannot mark verified")
eli.post("/admin", data=dict(csrf=tok_e, member_id=3, date="2026-10-27", action="verify", number="7654321", valid_until="2027-08-31"))
t = eli.get("/members").get_data(as_text=True); raw = eli.get("/members.csv").data; r = raw.decode("utf-8-sig")
ok(raw.startswith(b"\xef\xbb\xbf") and "John,Smith," in r and "7654321" in r and "2027-08-31" in r, "manual verify records number, date, admin, time")
ok(">All</a>" in t and ">Coaches</a>" in t and ">Admins</a>" in t and ">Expiring</a>" in t and ">Not cleared</a>" in t and ">Referees</a>" in t and "Search people..." in t and "class=alpha" in t and t.find("class=fchips") < t.find('class="t2 sm peoplesum"') < t.find("class=alpha") and ">Members</a>" not in t and t.find(">People</h1>") < t.find("id=growthCard") < t.find('placeholder="Search people..."') and " members · +" in t and "id=growthCard" not in eli.get("/admin").get_data(as_text=True), "People has search, letter headers, filter chips, and a growth chart")
eli.post("/admin", data=dict(csrf=tok_e, member_id=1, date="2026-10-27", action="verify", valid_until="2020-01-01"))
ok("Eli,Joern," in eli.get("/members.csv").data.decode("utf-8-sig") and "2020-01-01" not in eli.get("/members.csv").data.decode("utf-8-sig"), "past valid-until rejected")
# expiry
import datetime as dt, sqlite3
_g_today = dt.date(2026, 10, 31)
_g_day = A.growth_chart([_g_today - dt.timedelta(days=5), _g_today], [], _g_today)
_g_week = A.growth_chart([_g_today - dt.timedelta(days=40), _g_today - dt.timedelta(days=10), _g_today], [_g_today - dt.timedelta(days=10)], _g_today)
_g_month = A.growth_chart([_g_today - dt.timedelta(days=200), _g_today], [], _g_today)
_g_quarter = A.growth_chart([_g_today - dt.timedelta(days=800), _g_today], [], _g_today)
_g_one = A.growth_chart([_g_today], [], _g_today)
_g_zero = A.growth_chart([], [], _g_today)
ok(_g_day["kind"] == "day" and _g_week["kind"] == "week" and _g_month["kind"] == "month" and _g_quarter["kind"] == "quarter" and _g_one["kind"] == "day" and _g_zero["total"] == 0 and "No signups yet" in str(_g_zero["html"]) and 'r="3.5"' in str(_g_one["html"]) and "<polyline" in str(_g_week["html"]) and 'stroke="#F2F6F1"' in str(_g_week["html"]) and 'stroke="#BEC9C1"' in str(_g_week["html"]) and _g_week["total"] == 3 and _g_week["delta"] == 3 and "chart.js" not in str(_g_week["html"]), "growth buckets follow the history length and only plot real dates")
join(A.app.test_client(), "Ana", "Lopez", "ana@example.com")
D = sqlite3.connect(os.environ["GRUNIONS_DB"]); soon = (A.today_pt()+dt.timedelta(days=5)).isoformat()
eli.post("/admin", data=dict(csrf=tok_e, member_id=4, date="2026-10-27", action="verify", valid_until=soon))
ok("Please enter the expiration" in eli.post("/admin", data=dict(csrf=tok_e, member_id=1, date="2026-10-27", action="verify"), follow_redirects=True).get_data(as_text=True), "Mark verified asks for expiration date")
D.execute("UPDATE members SET usawp_status='verified', usawp_valid_until=? WHERE id=2", ((A.today_pt()-dt.timedelta(days=1)).isoformat(),)); D.commit()
t = eli.get("/admin?date=2026-10-27").get_data(as_text=True)
ok(A.fmt_long(soon) in eli.get("/admin/member/4").get_data(as_text=True) and "USAWP: " not in t and 'class="usawpcall' not in t and "grunionsUsawpCall" not in t and all('class="usawpcall' not in eli.get(p).get_data(as_text=True) and "USAWP: " not in eli.get(p).get_data(as_text=True) for p in ("/members", "/expiring", "/transfer", "/requirements", "/qr")), "admin pages have no USAWP expiry callout")
ok(D.execute("SELECT usawp_status FROM members WHERE id=2").fetchone()[0] == "expired", "auto-flip to expired after expires_on")
j = eli.get("/api/expiring").get_json()
ok(len(j["expired"]) >= 1 and any(r["first"]=="Ana" for r in j["within_7"]), "expiry report endpoint")
ok(jane.get("/api/expiring").status_code == 403, "report endpoint admin-only")
eli.post("/expiring", data=dict(csrf=tok_e, member_id=4))
exp_page = eli.get("/expiring").get_data(as_text=True)
ok(">Expired <" in exp_page and ">Next 7 days <" in exp_page and ">Next 30 days <" in exp_page and 'href="/admin/member/' in exp_page and ">Recheck</a>" in exp_page and "data-focus=membership" not in exp_page and "Ask Grunions to recheck all" in exp_page and ("d left" in exp_page or "d ago" in exp_page or ">Today<" in exp_page), "expiring groups dates, a days badge, and recheck")
ana = A.app.test_client(); rr = ana.post("/login", data=dict(csrf=csrf(ana,"/login"), email="ana@example.com"), follow_redirects=True).get_data(as_text=True)
h = ana.get(re.search(r'href="http://localhost(/auth/[^"]+)"', rr).group(1), follow_redirects=True).get_data(as_text=True)
ok("expires in <b>5 days" in ana.get("/profile").get_data(as_text=True) and "notice" in h, "member home expiry warning + in-app reminder")
def _around(html, name):
    i = html.find(">" + name + "<")
    return html[max(0, i - 80):i + 320] if i >= 0 else ""
_one = (A.today_pt() + dt.timedelta(days=1)).isoformat()
_zero = A.today_pt().isoformat()
_edge = (A.today_pt() + dt.timedelta(days=30)).isoformat()
_far = (A.today_pt() + dt.timedelta(days=31)).isoformat()
_past = (A.today_pt() - dt.timedelta(days=1)).isoformat()
D.execute("UPDATE members SET usawp_valid_until=? WHERE id=4", (_one,)); D.commit()
_one_row = _around(eli.get("/admin").get_data(as_text=True), "Ana Lopez") + _around(eli.get("/members").get_data(as_text=True), "Ana Lopez")
D.execute("UPDATE members SET usawp_valid_until=? WHERE id=4", (_zero,)); D.commit()
_zero_row = _around(eli.get("/admin").get_data(as_text=True), "Ana Lopez") + _around(eli.get("/members").get_data(as_text=True), "Ana Lopez")
D.execute("UPDATE members SET usawp_valid_until=? WHERE id=4", (_edge,)); D.commit()
_edge_row = _around(eli.get("/members").get_data(as_text=True), "Ana Lopez")
D.execute("UPDATE members SET usawp_valid_until=? WHERE id=4", (_far,)); D.commit()
_far_row = _around(eli.get("/admin").get_data(as_text=True), "Ana Lopez") + _around(eli.get("/members").get_data(as_text=True), "Ana Lopez")
D.execute("UPDATE members SET usawp_valid_until=? WHERE id=4", (_past,)); D.commit()
_past_row = _around(eli.get("/admin").get_data(as_text=True), "Ana Lopez") + _around(eli.get("/members").get_data(as_text=True), "Ana Lopez")
D.execute("UPDATE members SET usawp_valid_until=? WHERE id=4", (soon,)); D.commit()
ok("· expires in 5 days" in eli.get("/admin").get_data(as_text=True) and "· expires in 5 days" in eli.get("/members").get_data(as_text=True) and "· expires in 1 day" in _one_row and "· expires in 1 days" not in _one_row and "· expires today" in _zero_row and "· expires in 0" not in _zero_row and "· expires in 30 days" in _edge_row and "· expires" not in _far_row and "· expires" not in _past_row, "the status line counts down a membership inside 30 days and stays quiet otherwise")

# roles, channels, practices
D.execute("UPDATE members SET role='coach' WHERE id=3"); D.commit()
john = A.app.test_client(); rr = john.post("/login", data=dict(csrf=csrf(john,"/login"), email="john@example.com"), follow_redirects=True).get_data(as_text=True)
john.get(re.search(r'href="http://localhost(/auth/[^"]+)"', rr).group(1))
tj = csrf(john, "/chat")
ok(john.post("/api/messages?c=coaches", json={"body":"Coaches only: lineup for Friday"}, headers={"X-CSRF": tj}).status_code == 200, "coach posts to #coaches")
ok(jane.get("/api/messages?c=coaches").status_code == 403 and jane.get("/chat?c=coaches").status_code == 403, "#coaches private from members")
ok(len(eli.get("/api/messages?c=coaches").get_json()) == 1 and all("Coaches only" not in m["body"] for m in jane.get("/api/messages").get_json()), "channels separated")
ok(john.get("/admin").status_code == 200 and john.get("/import").status_code == 403 and john.post("/admin", data=dict(csrf=tj, member_id=2, action="verify")).status_code == 403 and 'class="usawpcall' not in john.get("/admin").get_data(as_text=True), "coach can check in but not use admin tools")
p = jane.get("/practices").get_data(as_text=True); ok("Marina High School" in p and "Westminster High School" in p and "class=datetile" in p and "I'm going" in p and "I'm not going" in p, "recurring Tue/Fri practices generated")
sched = eli.get("/admin").get_data(as_text=True)
sched_head = sched.split("<main>", 1)[0]
past_day = (A.today_pt() - dt.timedelta(days=9)).isoformat()
D.execute("INSERT OR IGNORE INTO practices(date,start,end,location) VALUES(?,?,?,?)", (past_day, "19:00", "20:30", "Past Pool"))
D.commit()
past_id = D.execute("SELECT id FROM practices WHERE date=? AND cancelled=0", (past_day,)).fetchone()[0]
past_admin = eli.get("/admin?date=" + past_day).get_data(as_text=True)
linked = eli.get("/practices/%d?from=admin" % past_id).get_data(as_text=True)
plain = eli.get("/practices/%d" % past_id).get_data(as_text=True)
ok(">Schedule</a>" in sched_head and ">People</a>" in sched_head and sched_head.find(">Schedule</a>") < sched_head.find(">People</a>") < sched_head.find(">Events</a>") < sched_head.find(">Expiring</a>") and ">Check-in</a>" not in sched_head and ">Check in</button>" in sched and "evcard" in sched and ">Details</a>" not in sched and "class=calpick" in sched and 'placeholder="Search players..."' in sched and ">Going (" in sched and "checkprog" not in sched and ('href="/practices/%d?from=admin"' % past_id) in past_admin and "Past Pool" in past_admin and ('href="/admin?date=%s"' % past_day) in linked.split("<main>", 1)[0] and 'href="/practices"' in plain.split("<main>", 1)[0] and ('href="/admin?date=%s"' % past_day) not in plain.split("<main>", 1)[0], "admin Schedule opens any practice, and Back returns to that date")
pid = D.execute("SELECT id, date FROM practices WHERE location='Marina High School' ORDER BY date LIMIT 1").fetchone()
tj2 = csrf(jane, "/practices"); jane.post("/practices", data=dict(csrf=tj2, pid=pid[0], action="going"))
john.post("/practices", data=dict(csrf=tj, pid=pid[0], action="notgoing"))
ok("1 going" in jane.get("/practices").get_data(as_text=True), "RSVP headcount")
ok(jane.post("/practices", data=dict(csrf=tj2, pid=pid[0], action="cancel")).status_code == 403, "members cannot cancel practices")
eli.post("/admin", data=dict(csrf=tok_e, member_id=2, date=pid[1]))
c = eli.get("/admin?date=%s" % pid[1]).get_data(as_text=True)
ok(c.find(">Going <") < c.find("Jane Doe") < c.find(">Everyone else <") < c.find("Eli Joern") and ">✓ Checked in</button>" in c[c.find("Jane Doe"):c.find(">Everyone else <")] and "Checked in " in c and "Walk-in" not in c and "Add and check in" not in c and "action=walkin" not in c and "RSVP ✓" not in c and "Not cleared" in c and "Search players..." in c, "check-in lists who is going, then everyone else, and keeps the checked-in button")
ok(eli.post("/admin", data=dict(csrf=tok_e, action="walkin", first="Walk", last="In", date=pid[1])).status_code == 400 and not D.execute("SELECT 1 FROM members WHERE first='Walk' AND last='In'").fetchone(), "check-in does not accept a walk-in")
eli.post("/practices", data=dict(csrf=tok_e, pid=pid[0], action="edit", start="19:30", end="21:00", location="Marina High School", note="Pool B"))
eli.post("/practices", data=dict(csrf=tok_e, pid=pid[0], action="cancel"))
ok(tuple(D.execute("SELECT cancelled, start, note FROM practices WHERE id=?", (pid[0],)).fetchone()) == (1, "19:30", "Pool B"), "admin edit + cancel practice")
eli.post("/practices", data=dict(csrf=tok_e, action="add", date="2026-12-05", start="09:00", end="11:00", location="Huntington Beach", note="Holiday scrimmage"))
ok(D.execute("SELECT COUNT(*) FROM practices WHERE date='2026-12-05'").fetchone()[0] == 1, "admin add practice")
_jp = x.get("/profile").get_data(as_text=True); _yd = (A.today_pt()-dt.timedelta(days=1)).isoformat()
ok('class="dot bad"' in x.get("/home").get_data(as_text=True) and ('<span class=rowtitle><span class="dot bad" aria-hidden=true></span>USAWP #1234567</span><span class=v>expires ' + _yd) in _jp and ("Membership expired " + _yd) in _jp and ">Water Polo Membership<" in _jp and ">Status<" not in _jp and "Cleared for water polo" not in x.get("/home").get_data(as_text=True), "member home shows Not cleared (membership ok, compliance missing)")
D.execute("UPDATE members SET usawp_status='verified', usawp_valid_until='2027-08-31' WHERE id=2"); D.commit()
eli.post("/admin", data=dict(csrf=tok_e, member_id=2, date="2026-10-27", action="req", req_id=1, completed_on="2026-01-10", expires_on="2027-01-10"))
eli.post("/admin", data=dict(csrf=tok_e, member_id=2, date="2026-10-27", action="req", req_id=3, completed_on="2026-10-01"))
h = x.get("/home").get_data(as_text=True); p = x.get("/profile").get_data(as_text=True); ok('class="dot ok"' in h and '<span class=rowtitle><span class="dot ok" aria-hidden=true></span>SafeSport training</span><span class=v>expires 2027-01-10</span>' in p and "Not cleared for water polo" not in h and 'class="st st-bad">Not cleared' not in p and ">Status<" not in p, "manual compliance entry -> Cleared")
D.execute("UPDATE member_reqs SET expires_on=? WHERE member_id=2 AND req_id=1", ((A.today_pt()+dt.timedelta(days=10)).isoformat(),)); D.commit()
ok(any(r.get("item")=="SafeSport training" for r in eli.get("/api/expiring").get_json()["within_30"]), "compliance item in expiring report")
D.execute("UPDATE member_reqs SET expires_on='2026-01-01' WHERE member_id=2 AND req_id=1"); D.commit()
ok("SafeSport expired " + A.fmt_long("2026-01-01") in eli.get("/admin/member/2").get_data(as_text=True) and "Not cleared" in eli.get("/admin?date=2026-10-27").get_data(as_text=True), "expired compliance -> Not cleared with reason on the member page")

# verification requests (bot API)
A.BOT_API_KEY = "test-bot-key"; H = {"Authorization": "Bearer test-bot-key"}
hits = []
import threading, http.server
class Hook(http.server.BaseHTTPRequestHandler):
    def do_POST(self):
        n = int(self.headers.get("Content-Length") or 0)
        hits.append({"json": json.loads(self.rfile.read(n) or b"{}"), "authorization": self.headers.get("Authorization"),
                     "x_verify_token": self.headers.get("X-Verify-Token"), "content_type": self.headers.get("Content-Type")})
        self.send_response(204); self.end_headers()
    def log_message(self, *a): pass
import json
srv = http.server.HTTPServer(("127.0.0.1", 0), Hook); threading.Thread(target=srv.serve_forever, daemon=True).start()
A.PUBLIC_URL = "https://grunions.example"
A.VERIFY_WEBHOOK_URL = "http://127.0.0.1:%d/hook" % srv.server_port
r = eli.post("/admin", data=dict(csrf=tok_e, member_id=4, date="2026-10-27", action="ask_bot"), follow_redirects=True).get_data(as_text=True)
body = hits[0]["json"] if hits else {}
ok("Webhook sent" in r and body == {"request_id": body.get("request_id"), "member_id": 4, "name": "Ana Lopez", "preferred_first": None, "email": "ana@example.com", "member_number": None, "requested_by": "Eli Joern", "member_submitted": False, "app_url": "https://grunions.example"} and hits[0]["authorization"] is None and hits[0]["content_type"] == "application/json", "Ask Grunions creates request + POSTs webhook")
ok("already pending" in eli.post("/admin", data=dict(csrf=tok_e, member_id=4, date="2026-10-27", action="ask_bot"), follow_redirects=True).get_data(as_text=True), "no duplicate pending request")
ok(jane.post("/admin", data=dict(csrf=tj2, member_id=4, action="ask_bot")).status_code == 403, "members cannot request verification")
ok("verification requested" not in eli.get("/admin?date=2026-10-27").get_data(as_text=True) and "Ana Lopez" in eli.get("/admin?date=2026-10-27").get_data(as_text=True), "a pending request does not add source text on the check-in row")
c0 = A.app.test_client()
ok(c0.get("/api/verify-requests").status_code == 401 and c0.get("/api/verify-requests", headers={"Authorization": "Bearer nope"}).status_code == 401, "API requires bearer token")
L = c0.get("/api/verify-requests?status=pending", headers=H).get_json(); ok(len(L) == 1 and L[0]["name"] == "Ana Lopez", "GET pending requests")
rid = L[0]["id"]
ok(c0.post("/api/verify-requests/%d/result" % rid, json={"verified": "yes"}, headers=H).status_code == 400, "result validates body")
_r = c0.post("/api/verify-requests/%d/result" % rid, headers=H, json={"verified": True, "member_number": "5555555", "membership_expires_on": "2027-08-31",
      "compliance": {"SafeSport training": "2027-05-01", "Background screening": "2028-01-01", "Mystery cert": "2027-01-01"}, "note": "Checked Sport:80 club list"}); res = _r.get_json()
ok(res["ok"] and "SafeSport training" in res["applied_compliance"] and res["ignored_compliance"] == ["Mystery cert"], "POST result applies membership + compliance")
row = D.execute("SELECT usawp_status, usawp_number, usawp_valid_until, usawp_verified_by FROM members WHERE id=4").fetchone()
ok(tuple(row) == ("verified", "5555555", "2027-08-31", "Grunions bot"), "member updated from bot result")
ok(D.execute("SELECT status FROM verify_requests WHERE id=?", (rid,)).fetchone()[0] == "done" and c0.get("/api/verify-requests?status=pending", headers=H).get_json() == [], "request marked done")
ok(c0.post("/api/verify-requests/%d/result" % rid, json={"verified": True}, headers=H).status_code == 409, "cannot answer twice")
cm = eli.get("/api/messages?c=coaches").get_json()
team = eli.get("/api/messages").get_json()
ok(cm and not any("Verification for" in m["body"] or (m.get("who") or "").startswith("Grunions") for m in cm + team), "verification result is not posted to chat")
bot_id = D.execute("INSERT INTO members(first,last,email,phone,role) VALUES('Grunions','bot','bot@grunions.local','','system')").lastrowid
eli_id = D.execute("SELECT id FROM members WHERE email='eli@example.com'").fetchone()[0]
D.execute("INSERT INTO messages(member_id,body,channel) VALUES(?,?,'coaches')", (bot_id, "Verification for Old Member: verified"))
old_id = D.execute("SELECT id FROM messages WHERE body='Verification for Old Member: verified'").fetchone()[0]
D.execute("INSERT INTO reactions(message_id,member_id,emoji) VALUES(?,?,?)", (old_id, eli_id, "👍"))
D.execute("INSERT INTO messages(member_id,body,channel) VALUES(?,?,'team')", (bot_id, "Verification for Old Member: NOT verified"))
D.execute("INSERT INTO messages(member_id,body,channel) VALUES(?,?,'team')", (bot_id, "See you Tuesday"))
D.execute("INSERT INTO messages(member_id,body,channel) VALUES(?,?,'team')", (eli_id, "Verification for the weekend: bring caps"))
D.commit()
jane.get("/home")
bodies = [r[0] for r in D.execute("SELECT body FROM messages").fetchall()]
ok("Bring dark + white caps Friday." in bodies and "See you Tuesday" in bodies and "Verification for the weekend: bring caps" in bodies and not any(b.startswith("Verification for Old") for b in bodies) and D.execute("SELECT COUNT(*) FROM reactions WHERE message_id=?", (old_id,)).fetchone()[0] == 0, "old bot verification messages are deleted from chat")
a = eli.get("/admin?date=2026-10-27").get_data(as_text=True)
ok("Verification for Ana Lopez" in a and "bot answered" not in a and "verification requested" not in a, "admin notification stays, and the row does not say who answered")
members_now = eli.get("/members").get_data(as_text=True)
ok("bot@grunions.local" not in members_now and "Grunions bot" not in members_now.split(">Verified<")[0], "bot account hidden from member list")
ahome = ana.get("/profile").get_data(as_text=True)
ok((">Verified %s<" % A.today_pt().isoformat()) in ahome and "Grunions bot" not in ahome, "member verified row shows only the date")
ana_page = eli.get("/admin/member/4").get_data(as_text=True)
ok((">Verified %s<" % A.today_pt().isoformat()) in ana_page and "Verified by" not in ana_page and ">Water Polo Membership<" in ana_page and ">Status</span>" not in ana_page and ">Status<select" in ana_page, "member page shows the verified date beside the section label")
# reactions + images + schedule toggle
A.UPLOADS = tempfile.mkdtemp()
from PIL import Image
def img_bytes(fmt="PNG", size=(2400, 1800)):
    b = io.BytesIO(); Image.new("RGB", size, (30, 90, 200)).save(b, fmt); b.seek(0); return b
import io
tj3 = csrf(jane, "/chat"); te3 = csrf(eli, "/chat")
mid0 = jane.get("/api/messages").get_json()[-1]["id"]
ok(jane.post(f"/api/messages/{mid0}/react", json={"emoji": "🤽"}, headers={"X-CSRF": tj3}).get_json()["🤽"] == {"n": 1, "mine": True}, "add reaction")
eli.post(f"/api/messages/{mid0}/react", json={"emoji": "🤽"}, headers={"X-CSRF": te3})
ok(jane.get("/api/reactions?c=team").get_json()[str(mid0)]["🤽"] == {"n": 2, "mine": True}, "reaction counts via polling endpoint")
jane.post(f"/api/messages/{mid0}/react", json={"emoji": "🤽"}, headers={"X-CSRF": tj3})
ok(jane.get("/api/reactions?c=team").get_json()[str(mid0)]["🤽"] == {"n": 1, "mine": False}, "toggle own reaction off")
ok(jane.post(f"/api/messages/{mid0}/react", json={"emoji": "nope"}, headers={"X-CSRF": tj3}).status_code == 400, "a word is not a reaction")
cmid = eli.get("/api/messages?c=coaches").get_json()[-1]["id"]
ok(jane.post(f"/api/messages/{cmid}/react", json={"emoji": "👍"}, headers={"X-CSRF": tj3}).status_code == 403 and jane.get("/api/reactions?c=coaches").status_code == 403, "no reactions on private channel for members")
r = jane.post("/api/messages", data={"body": "Pool photo", "image": (img_bytes(), "pool.png")}, headers={"X-CSRF": tj3}, content_type="multipart/form-data")
m = jane.get("/api/messages").get_json()[-1]
ok(r.status_code == 200 and m["image"] and m["body"] == "Pool photo", "image upload creates message")
full = jane.get(m["image"]["full"]); th = jane.get(m["image"]["thumb"])
ok(full.status_code == 200 and max(Image.open(io.BytesIO(full.data)).size) == 1600 and max(Image.open(io.BytesIO(th.data)).size) == 480, "auto-resize full 1600 / thumb 480")
ok(A.app.test_client().get(m["image"]["full"]).status_code == 302, "images need login")
ok(jane.post("/api/messages", data={"image": (io.BytesIO(b"not an image at all"), "x.png")}, headers={"X-CSRF": tj3}, content_type="multipart/form-data").status_code == 400, "reject non-image")
ok(jane.post("/api/messages", data={"image": (io.BytesIO(b"0" * (9 * 1024 * 1024)), "big.jpg")}, headers={"X-CSRF": tj3}, content_type="multipart/form-data").status_code == 413, "reject >8MB")
b = io.BytesIO(); Image.new("RGB", (40, 40)).save(b, "BMP"); b.seek(0)
ok(jane.post("/api/messages", data={"image": (b, "x.bmp")}, headers={"X-CSRF": tj3}, content_type="multipart/form-data").status_code == 400, "reject unsupported type (BMP)")
try:
    import pillow_heif; pillow_heif.register_heif_opener(); hb = io.BytesIO(); Image.new("RGB", (64, 48), (200, 10, 10)).save(hb, "HEIF"); hb.seek(0)
    ok(jane.post("/api/messages", data={"image": (hb, "x.heic")}, headers={"X-CSRF": tj3}, content_type="multipart/form-data").status_code == 200, "HEIC accepted (converted)")
except Exception as e: print("SKIP heic", e)
eli.post("/api/messages?c=coaches", data={"body": "lineup", "image": (img_bytes("JPEG", (300, 200)), "l.jpg")}, headers={"X-CSRF": te3}, content_type="multipart/form-data")
cm = eli.get("/api/messages?c=coaches").get_json()[-1]
ok(eli.get(cm["image"]["thumb"]).status_code == 200 and jane.get(cm["image"]["full"]).status_code == 403 and jane.get(cm["image"]["thumb"]).status_code == 403, "#coaches images private")
pg = jane.get("/practices").get_data(as_text=True)
ok('href="/practices/' in pg and " going</span>" in pg and "class=nxtitle>Water Polo Practice</div>" in pg and "class=nxhead" not in pg and "class=datetile" in pg and "I'm going" in pg and "Edit practice" not in pg and "Assign coaches" not in pg and 'class=morebtn' not in pg, "a practice card links to its page, and a member has no More menu")
ch = jane.get("/chat").get_data(as_text=True)
ca = eli.get("/chat").get_data(as_text=True)
cc = eli.get("/chat?c=coaches").get_data(as_text=True)
ok("rows=1" in ch and "scrollbar-width:none" in ch and "shiftKey" in ch and 'id=attach' in ch and 'id=ann' not in ca and '>Announce<' not in ca and 'id=ann' not in cc and '>Announce<' not in cc and 'aria-label=Send' in ch and 'aria-label=Send' in ca and 'aria-label=Send' in cc and 'class="iconbtn send"' in ch and 'class="iconbtn send"' in cc, "composer: icon send on team and coaches, no announce checkbox")

# member USAWP number on the Not cleared card
jh = jane.get("/home").get_data(as_text=True)
jp = jane.post("/home", data=dict(csrf=csrf(jane, "/home"), usawp_number="99998888"), follow_redirects=True).get_data(as_text=True)
jprof = jane.get("/profile").get_data(as_text=True)
ok('class="dot bad"' in jh and "USAWP #1234567" in jh and "name=usawp_number" not in jh and "name=usawp_number" not in jprof and ">Edit<" not in jh and "id=trialOpen" not in jh and "Reverify membership" not in jh and "SafeSport expired 2026-01-01" in jprof and "already verified" in jp and D.execute("SELECT usawp_number FROM members WHERE email='jane@example.com'").fetchone()[0] == "1234567", "verified member sees read-only USAWP number; Edit is hidden and the number cannot be changed")
ok("Membership & requirements" not in jh and "Membership &amp; requirements" not in jh and 'class="card playcard"' not in jh and "Cleared for water polo" not in jh and 'class="dot bad"' in jh and "Cleared to coach" not in jh and 'href="/profile#membership"' in jh and ">USA Water Polo<" not in jh and '<span class=rowtitle><span class="dot ok" aria-hidden=true></span>USAWP #1234567</span><span class=v>expires 2027-08-31</span>' in jprof and '<span class=rowtitle><span class="dot bad" aria-hidden=true></span>SafeSport training</span><span class=v>expired</span>' in jprof and jprof.find("id=membership") < jprof.find(">Personal<") and ">Expires<" not in jprof and ">Status<" not in jprof, "home shows the membership dot on the practice card and profile holds the details")
D.execute("UPDATE member_reqs SET expires_on='2027-06-01' WHERE member_id=2 AND req_id=1"); D.commit()
ok("USAWP Membership #" not in jane.get("/home").get_data(as_text=True) and "USAWP #1234567" in jane.get("/home").get_data(as_text=True) and 'class="dot ok"' in jane.get("/home").get_data(as_text=True) and '<span class=rowtitle><span class="dot ok" aria-hidden=true></span>SafeSport training</span><span class=v>expires 2027-06-01</span>' in jane.get("/profile").get_data(as_text=True) and "Club waiver" not in jane.get("/home").get_data(as_text=True), "form hidden once verified and cleared; number stays read-only")
casey = A.app.test_client(); join(casey, "Casey", "Ng", "casey@example.com")
cid = D.execute("SELECT id FROM members WHERE email='casey@example.com'").fetchone()[0]
ssid = D.execute("SELECT id FROM requirements WHERE lower(keywords) LIKE '%safesport%'").fetchone()[0]
D.execute("UPDATE members SET role='coach', usawp_status='verified', usawp_valid_until='2027-06-07', usawp_number='659226' WHERE id=?", (cid,))
D.execute("INSERT INTO member_reqs(member_id,req_id,completed_on,expires_on,source,by,at) VALUES(?,?,NULL,'2027-05-11','test','test','2026-10-23T00:00')", (cid, ssid)); D.commit()
chome = casey.get("/home").get_data(as_text=True)
cprof = casey.get("/profile").get_data(as_text=True)
plain_home = jane.get("/home").get_data(as_text=True)
ok('class="dot ok"' in chome and '<span class=rowtitle><span class="dot ok" aria-hidden=true></span>SafeSport training</span><span class=v>expires 2027-05-11</span>' in cprof and "Needs:" not in cprof and "Club waiver" not in cprof and "Concussion" not in cprof and "SafeSport training" in cprof and "Not cleared to coach" in cprof and '<span class=rowtitle><span class="dot bad" aria-hidden=true></span>Background screening</span><span class=v>missing</span>' in cprof and "Not cleared to coach" not in plain_home and "Cleared to coach" not in plain_home and "Background screening missing" not in plain_home and "Club waiver" not in eli.get("/requirements").get_data(as_text=True) and "Club waiver" not in eli.get("/admin").get_data(as_text=True), "an active coach needs background screening, and a member who is not an active coach does not")
bgid_casey = D.execute("SELECT id FROM requirements WHERE lower(keywords) LIKE '%background%'").fetchone()[0]
far_bg = (A.today_pt() + dt.timedelta(days=400)).isoformat()
soon_bg = (A.today_pt() + dt.timedelta(days=5)).isoformat()
past_bg = (A.today_pt() - dt.timedelta(days=2)).isoformat()
D.execute("INSERT INTO member_reqs(member_id,req_id,completed_on,expires_on,source,by,at) VALUES(?,?,NULL,?,'test','test','2026-01-01')", (cid, bgid_casey, far_bg))
D.execute("UPDATE members SET membership_type='Head Coach' WHERE id=?", (cid,)); D.commit()
bg_row = '<span class=rowtitle><span class="dot ok" aria-hidden=true></span>Background screening</span><span class=v>expires ' + far_bg + '</span>'
panel_bg = '<span class=rowtitle><span class="dot ok" aria-hidden=true></span>Background screening</span><span class=v>' + A.fmt_long(far_bg) + '</span>'
ok('>Coaching</span><span class=v>cleared</span>' in casey.get("/profile").get_data(as_text=True) and "Cleared to coach" not in casey.get("/profile").get_data(as_text=True) and "Coach eligible" not in casey.get("/home").get_data(as_text=True) and bg_row in casey.get("/profile").get_data(as_text=True) and panel_bg in eli.get("/admin/member/%d" % cid).get_data(as_text=True) and panel_bg not in eli.get("/members").get_data(as_text=True) and panel_bg not in eli.get("/admin").get_data(as_text=True) and ('class="st st-ok">Background screening expires ' + far_bg) not in eli.get("/members").get_data(as_text=True) and ('class="st st-ok">Background screening expires ' + far_bg) not in eli.get("/admin").get_data(as_text=True), "background screening stays on the member page, not on People rows or the check-in list")
D.execute("UPDATE member_reqs SET expires_on=? WHERE member_id=? AND req_id=?", (soon_bg, cid, bgid_casey)); D.commit()
ok(('<span class=rowtitle><span class="dot warn" aria-hidden=true></span>Background screening</span><span class=v>expires ' + soon_bg + '</span>') in casey.get("/profile").get_data(as_text=True), "background screening is amber inside the expiring window")
D.execute("UPDATE member_reqs SET expires_on=? WHERE member_id=? AND req_id=?", (past_bg, cid, bgid_casey)); D.commit()
expired_home = casey.get("/profile").get_data(as_text=True)
ok('<span class=rowtitle><span class="dot ok" aria-hidden=true></span>SafeSport training</span><span class=v>expires 2027-05-11</span>' in expired_home and "Not cleared to coach" in expired_home and ('<span class=rowtitle><span class="dot bad" aria-hidden=true></span>Background screening</span><span class=v>expires ' + past_bg + '</span>') in expired_home and ">Reverify background screening<" in expired_home, "an expired background screening is red, blocks coach clearance, and offers reverify")
casey.post("/home", data=dict(csrf=csrf(casey, "/home"), action="reverify_background"), follow_redirects=True)
ok(D.execute("SELECT status FROM verify_requests WHERE member_id=? ORDER BY id DESC LIMIT 1", (cid,)).fetchone()[0] == "pending" and ">Status<" not in casey.get("/profile").get_data(as_text=True) and 'class="dot warn"' in casey.get("/home").get_data(as_text=True), "reverify background screening asks Grunions to verify")
D.execute("DELETE FROM verify_requests WHERE member_id=?", (cid,))
D.execute("UPDATE member_reqs SET expires_on=? WHERE member_id=? AND req_id=?", (far_bg, cid, bgid_casey)); D.commit()
cur = D.execute("INSERT INTO requirements(name,applies_to,keywords,expires,active) VALUES('Club waiver','all','waiver',0,1)")
wid = cur.lastrowid
D.execute("INSERT INTO member_reqs(member_id,req_id,completed_on,expires_on,source,by,at) VALUES(?,?, '2026-01-01', NULL, 'test','test','2026-01-01T00:00')", (cid, wid))
kept = D.execute("SELECT COUNT(*) FROM member_reqs WHERE req_id=?", (ssid,)).fetchone()[0]
nmembers = D.execute("SELECT COUNT(*) FROM members").fetchone()[0]
D.commit(); A.drop_club_waiver(D); A.drop_club_waiver(D)
ok(D.execute("SELECT COUNT(*) FROM requirements WHERE lower(name)='club waiver' OR lower(ifnull(keywords,'')) LIKE '%waiver%'").fetchone()[0] == 0 and D.execute("SELECT COUNT(*) FROM member_reqs WHERE req_id=?", (wid,)).fetchone()[0] == 0 and D.execute("SELECT COUNT(*) FROM member_reqs WHERE req_id=?", (ssid,)).fetchone()[0] == kept and D.execute("SELECT COUNT(*) FROM members").fetchone()[0] == nmembers and '<span class=rowtitle><span class="dot ok" aria-hidden=true></span>SafeSport training</span><span class=v>expires 2027-05-11</span>' in casey.get("/profile").get_data(as_text=True) and "Club waiver" not in casey.get("/home").get_data(as_text=True), "migration removes Club waiver only and the member stays cleared")
sam = A.app.test_client(); join(sam, "Sam", "River", "sam@example.com")
sh = sam.get("/home").get_data(as_text=True)
ok('name=usawp_number inputmode=numeric value=""' in sh and "Enter your USAWP membership number" in sh and "USAWP Membership #" in sh and "class=usawpchip" not in sh and '<span class=rowtitle><span class="dot bad" aria-hidden=true></span>SafeSport training</span><span class=v>missing</span>' in sam.get("/profile").get_data(as_text=True) and "Verification pending" not in sh and "id=trialOpen" in sh and ">2-week USAWP trial<" in sh, "empty membership form for a new member")
ok(sam.post("/home", data=dict(usawp_number="4321")).status_code == 400, "membership form requires CSRF")
ts = csrf(sam, "/home"); sid = D.execute("SELECT id FROM members WHERE email='sam@example.com'").fetchone()[0]
def sam_post(num): return sam.post("/home", data=dict(csrf=ts, usawp_number=num), follow_redirects=True)
bad = sam_post("12ab").get_data(as_text=True)
ok("4-10 digits" in bad and all("4-10 digits" in sam_post(n).get_data(as_text=True) for n in ("123", "12345678901", "12 34")) and D.execute("SELECT COUNT(*) FROM verify_requests WHERE member_id=?", (sid,)).fetchone()[0] == 0 and D.execute("SELECT usawp_number FROM members WHERE id=?", (sid,)).fetchone()[0] in (None, ""), "rejects numbers that are not 4-10 digits")
import urllib.request
_open = urllib.request.urlopen
def _spy(req, timeout=None, **k):
    _spy.timeout = timeout
    return _open(req, timeout=timeout)
urllib.request.urlopen = _spy
before = len(hits)
page = sam_post("4321")
urllib.request.urlopen = _open
vr = D.execute("SELECT id, member_number, status, requested_by, name, email FROM verify_requests WHERE member_id=?", (sid,)).fetchone()
body = hits[-1]["json"]
sp = page.get_data(as_text=True)
ok(page.status_code == 200 and 'class="toast noprint" role=status>Sent to Grunions for verification' in sp and "setTimeout" in sp and "3000" in sp and ">Status<" not in sam.get("/profile").get_data(as_text=True) and ">Water Polo Membership<" in sam.get("/profile").get_data(as_text=True) and 'class="dot warn"' in sp and 'class="st st-bad">Not cleared' not in sp and "USAWP #4321" in sp and "id=trialOpen" not in sp and "name=usawp_number" not in sp and 'name=usawp_number' in sam.get("/profile").get_data(as_text=True) and D.execute("SELECT usawp_number FROM members WHERE id=?", (sid,)).fetchone()[0] == "4321" and vr[1] == "4321" and vr[2] == "pending", "submit saves number, hides the input, toasts, and shows Pending")
ok(_spy.timeout == 5 and len(hits) == before + 1 and body == {"request_id": vr[0], "member_id": sid, "name": "Sam River", "preferred_first": None, "email": "sam@example.com", "member_number": "4321", "requested_by": "Sam River", "member_submitted": True, "app_url": "https://grunions.example"}, "member submit POSTs the webhook payload with a 5s timeout")
ok("verification requested" not in eli.get("/admin").get_data(as_text=True) and "bot answered" not in eli.get("/admin").get_data(as_text=True) and any(x["id"] == vr[0] and x["member_number"] == "4321" and x["status"] == "pending" for x in c0.get("/api/verify-requests?status=pending", headers=H).get_json()), "a pending request stays on the bot API without source text on the check-in row")
quiet = sam.get("/home").get_data(as_text=True)
ok("class=\"toast" not in quiet and "Sent to Grunions for verification" not in quiet and ">Status<" not in sam.get("/profile").get_data(as_text=True) and 'class="dot warn"' in quiet and "USAWP #4321" in quiet and "name=usawp_number" not in quiet, "reload keeps the pending card without repeating the toast")
edit = sam_post("55555")
ok(tuple(D.execute("SELECT COUNT(*), MAX(member_number) FROM verify_requests WHERE member_id=? AND status='pending'", (sid,)).fetchone()) == (1, "55555") and len(hits) == before + 2 and hits[-1]["json"]["request_id"] == vr[0] and hits[-1]["json"]["member_number"] == "55555" and hits[-1]["json"]["member_submitted"] is True and hits[-1]["json"]["requested_by"] == "Sam River" and 'class="toast noprint" role=status>Sent to Grunions for verification' in edit.get_data(as_text=True) and "USAWP #55555" in edit.get_data(as_text=True) and D.execute("SELECT requested_by FROM verify_requests WHERE id=?", (vr[0],)).fetchone()[0] == "Sam River", "edit save updates the pending number, re-sends the webhook, and toasts again")
sam_post("666666")
blocked = sam_post("7777777").get_data(as_text=True)
ok("3 times per hour" in blocked and D.execute("SELECT usawp_number FROM members WHERE id=?", (sid,)).fetchone()[0] == "666666" and D.execute("SELECT member_number FROM verify_requests WHERE id=?", (vr[0],)).fetchone()[0] == "666666", "rate limit is 3 submissions per member per hour")
pat = A.app.test_client(); join(pat, "Pat", "Ng", "pat@example.com")
pid = D.execute("SELECT id FROM members WHERE email='pat@example.com'").fetchone()[0]
n0 = len(hits)
eli.post("/admin", data=dict(csrf=csrf(eli, "/admin"), member_id=pid, action="ask_bot"), follow_redirects=True)
ph = pat.post("/home", data=dict(csrf=csrf(pat, "/home"), usawp_number="246810"), follow_redirects=True).get_data(as_text=True)
prow = D.execute("SELECT id, member_number, requested_by FROM verify_requests WHERE member_id=? AND status='pending'", (pid,)).fetchall()
ok("Sent to Grunions for verification" in ph and len(prow) == 1 and tuple(prow[0])[1:] == ("246810", "Eli Joern") and len(hits) == n0 + 2 and hits[-1]["json"]["request_id"] == prow[0][0] and hits[-1]["json"]["member_number"] == "246810", "member form updates the admin's pending request and re-sends the webhook")
kim = A.app.test_client(); join(kim, "Kim", "Lee", "kim@example.com"); tk = csrf(kim, "/home")
A.VERIFY_WEBHOOK_KEY = "hook-secret"
kim.post("/home", data=dict(csrf=tk, usawp_number="10001"), follow_redirects=True)
ok(hits[-1]["authorization"] == "Bearer hook-secret" and hits[-1]["json"]["member_number"] == "10001", "VERIFY_WEBHOOK_KEY is sent as a bearer token")
A.VERIFY_WEBHOOK_HEADER = "X-Verify-Token"
kid = D.execute("SELECT id FROM members WHERE email='kim@example.com'").fetchone()[0]
D.execute("DELETE FROM verify_requests WHERE member_id=?", (kid,)); D.commit()
kim.post("/home", data=dict(csrf=tk, usawp_number="10002"), follow_redirects=True)
ok(hits[-1]["x_verify_token"] == "hook-secret" and hits[-1]["authorization"] is None, "VERIFY_WEBHOOK_HEADER sends the raw key under that name")
import logging
logged = []
class _H(logging.Handler):
    def emit(self, rec): logged.append(rec.getMessage())
A.app.logger.addHandler(_H())
A.VERIFY_WEBHOOK_URL = "http://127.0.0.1:9/hook"
D.execute("DELETE FROM verify_requests WHERE member_id=?", (kid,)); D.commit()
fail = kim.post("/home", data=dict(csrf=tk, usawp_number="10003"), follow_redirects=True)
wh = D.execute("SELECT webhook, status, member_number FROM verify_requests WHERE member_id=?", (kid,)).fetchone()
ok(fail.status_code == 200 and "Sent to Grunions for verification" in fail.get_data(as_text=True) and wh[0].startswith("failed:") and wh[1] == "pending" and wh[2] == "10003" and any("verify webhook failed" in m for m in logged), "webhook failure is logged and does not break the page")
res = c0.post("/api/verify-requests/%d/result" % vr[0], headers=H, json={"verified": True, "member_number": "666666", "membership_expires_on": "2027-08-31", "compliance": {"SafeSport training": "2027-05-01", "Club waiver": "2027-01-01"}}).get_json()
shome = sam.get("/home").get_data(as_text=True)
ok(res["ok"] and D.execute("SELECT status FROM verify_requests WHERE id=?", (vr[0],)).fetchone()[0] == "done" and tuple(D.execute("SELECT usawp_status, usawp_number FROM members WHERE id=?", (sid,)).fetchone()) == ("verified", "666666") and '<span class=rowtitle><span class="dot ok" aria-hidden=true></span>SafeSport training</span><span class=v>expires 2027-05-01</span>' in sam.get("/profile").get_data(as_text=True) and 'class="dot ok"' in shome and "Verification pending" not in shome and "USAWP Membership #" not in shome and "USAWP #666666" in shome and ">Edit<" not in shome and "name=usawp_number" not in sam.get("/profile").get_data(as_text=True), "bot result answers the member request and shows Cleared with a read-only number")
kr = D.execute("SELECT id FROM verify_requests WHERE member_id=? AND status='pending'", (kid,)).fetchone()
c0.post("/api/verify-requests/%d/result" % kr[0], headers=H, json={"verified": False, "note": "no matching membership"})
kh = kim.get("/home").get_data(as_text=True)
ok('<span class=rowtitle><span class="dot bad" aria-hidden=true></span>SafeSport training</span><span class=v>missing</span>' in kim.get("/profile").get_data(as_text=True) and 'class="dot bad"' in kh and "Verification pending" not in kh and "USAWP #10003" in kh and "name=usawp_number" in kim.get("/profile").get_data(as_text=True) and "id=trialOpen" not in kh, "bot not-verified result restores the red Not cleared card")
ACK = "I will complete the USA Water Polo 2-week trial membership before I get in the pool. I understand I need to get a full USAWP membership soon, otherwise I will not be able to practice."
alex = A.app.test_client(); join(alex, "Alex", "Trial", "alex@example.com")
ah = alex.get("/home").get_data(as_text=True)
ok("id=trialOpen" in ah and ">2-week USAWP trial<" in ah and ACK in ah and A.TRIAL_JOIN_URL in ah and "target=_blank" in ah and "rel=noopener" in ah and ">I confirm<" in ah and ">Get USAWP trial membership<" in ah and "class=usawpchip" not in ah and '<span class=rowtitle><span class="dot bad" aria-hidden=true></span>SafeSport training</span><span class=v>missing</span>' in alex.get("/profile").get_data(as_text=True), "empty card offers the 2-week trial acknowledgment")
ok(alex.post("/home", data=dict(action="trial")).status_code == 400, "trial confirm requires CSRF")
jane.post("/home", data=dict(csrf=csrf(jane, "/home"), action="trial"), follow_redirects=True)
ok(D.execute("SELECT trial_acknowledged_at FROM members WHERE email='jane@example.com'").fetchone()[0] in (None, ""), "a verified membership cannot start a trial")
kim.post("/home", data=dict(csrf=tk, action="trial"), follow_redirects=True)
ok(D.execute("SELECT trial_acknowledged_at FROM members WHERE email='kim@example.com'").fetchone()[0] in (None, ""), "a saved USAWP number cannot start a trial")
def md(d): return d.strftime("%b ") + str(d.day)
today = A.today_pt(); end = today + dt.timedelta(days=14); start = today.isoformat()
ap = alex.post("/home", data=dict(csrf=csrf(alex, "/home"), action="trial"), follow_redirects=True).get_data(as_text=True)
stamp = D.execute("SELECT trial_acknowledged_at FROM members WHERE email='alex@example.com'").fetchone()[0]
aprof = alex.get("/profile").get_data(as_text=True)
ok(stamp and stamp[:10] == start and 'class="toast noprint" role=status>2-week USAWP trial started' in ap and 'class="dot warn"' in aprof and "Trial · expires in 14 days" in aprof and 'class="usawpchip warn"' in ap and ">Trial</a>" in ap and "id=trialOpen" not in ap and 'name=usawp_number inputmode=numeric value=""' in ap and ">Status<" not in aprof and 'class="st st-bad">Not cleared' not in aprof and "Needs:" not in aprof, "confirm records the trial and shows a yellow Trial countdown")
again = alex.post("/home", data=dict(csrf=csrf(alex, "/home"), action="trial"), follow_redirects=True).get_data(as_text=True)
ok(D.execute("SELECT trial_acknowledged_at FROM members WHERE email='alex@example.com'").fetchone()[0] == stamp and "2-week USAWP trial started" not in again, "a second confirm does not reset the trial")
adm = eli.get("/admin").get_data(as_text=True); mem = eli.get("/members").get_data(as_text=True); csv = eli.get("/members.csv").get_data(as_text=True)
alex_member = eli.get("/admin/member/%d" % D.execute("SELECT id FROM members WHERE email='alex@example.com'").fetchone()[0]).get_data(as_text=True)
alex_checkin = eli.get("/admin").get_data(as_text=True)
ok("Trial · expires in 14 days" in alex_member and 'class="dot warn"' in alex_member and 'class="psub ell st-warn"' in alex_checkin and '>Trial</span><span class=strest> · expires in 14 days' in alex_checkin and 'class="psub ell st-warn"' in mem and '>Trial</span><span class=strest> · expires in 14 days' in mem and ".psub.st-warn::before{background:var(--color-status-attention)}" in mem and stamp[:10] in csv and end.isoformat() in csv, "check-in, People, and the member page count the trial in yellow")
added = alex.post("/home", data=dict(csrf=csrf(alex, "/home"), usawp_number="88821"), follow_redirects=True).get_data(as_text=True)
ok('class="toast noprint" role=status>Sent to Grunions for verification' in added and ">Status<" not in alex.get("/profile").get_data(as_text=True) and 'class="dot warn"' in added and "USAWP #88821" in added and "name=usawp_number" not in added and "Trial · 14 days left" not in added and "Ends %s" % md(end) not in added and D.execute("SELECT trial_acknowledged_at FROM members WHERE email='alex@example.com'").fetchone()[0] == stamp and D.execute("SELECT member_number, status FROM verify_requests WHERE member_id=(SELECT id FROM members WHERE email='alex@example.com')").fetchone() == ("88821", "pending"), "a trial member can submit a USAWP number and the card shows Pending")
aid = D.execute("SELECT id FROM members WHERE email='alex@example.com'").fetchone()[0]
avr = D.execute("SELECT id FROM verify_requests WHERE member_id=? AND status='pending'", (aid,)).fetchone()[0]
c0.post("/api/verify-requests/%d/result" % avr, headers=H, json={"verified": True, "member_number": "88821", "membership_expires_on": "2027-08-31", "compliance": {"SafeSport training": "2027-05-01"}})
vh = alex.get("/home").get_data(as_text=True)
ok('<span class=rowtitle><span class="dot ok" aria-hidden=true></span>SafeSport training</span><span class=v>expires 2027-05-01</span>' in alex.get("/profile").get_data(as_text=True) and 'class="dot ok"' in vh and "USAWP #88821" in vh and "Trial ·" not in vh and "Last day of trial" not in vh and ("Ends %s" % md(end)) not in vh and "Verification pending" not in vh and ">Edit<" not in vh, "a verified membership replaces the trial display")
drew = A.app.test_client(); join(drew, "Drew", "Lane", "drew@example.com")
drew.post("/home", data=dict(csrf=csrf(drew, "/home"), action="trial"), follow_redirects=True)
D.execute("UPDATE members SET trial_acknowledged_at=? WHERE email='drew@example.com'", ((today - dt.timedelta(days=13)).isoformat() + "T08:00:00",)); D.commit()
one = drew.get("/profile").get_data(as_text=True)
ok("Trial · expires in 1 day" in one and "expires in 1 days" not in one and 'class="dot warn"' in one and ">Status<" not in one and "Not cleared for water polo" not in one, "one day left uses the singular trial countdown")
D.execute("UPDATE members SET trial_acknowledged_at=? WHERE email='drew@example.com'", ((today - dt.timedelta(days=14)).isoformat() + "T08:00:00",)); D.commit()
last = drew.get("/profile").get_data(as_text=True)
ok("Trial · expires today" in last and "expires in 0" not in last and 'class="dot warn"' in last and ">Status<" not in last and 'class="st st-bad">Not cleared' not in last, "the trial end date counts as expires today")
ended_on = today - dt.timedelta(days=1)
D.execute("UPDATE members SET trial_acknowledged_at=? WHERE email='drew@example.com'", ((today - dt.timedelta(days=15)).isoformat() + "T08:00:00",)); D.commit()
eh = drew.get("/home").get_data(as_text=True)
eprof = drew.get("/profile").get_data(as_text=True)
ok('<span class=rowtitle><span class="dot bad" aria-hidden=true></span>SafeSport training</span><span class=v>missing</span>' in eprof and "class=usawpchip" not in eh and ("Trial ended %s" % md(ended_on)) in eprof and "id=trialOpen" not in eh and "Last day of trial" not in eh and 'name=usawp_number inputmode=numeric value=""' in eh and "Cleared for water polo" not in eh, "an ended trial returns to Not cleared and keeps the membership form")
ok(("Trial membership ended " + A.fmt_long(ended_on)) in eli.get("/admin/member/%d" % D.execute("SELECT id FROM members WHERE email='drew@example.com'").fetchone()[0]).get_data(as_text=True) and ("Trial ended %s" % md(ended_on)) in eli.get("/members").get_data(as_text=True), "an ended trial is on the member page and the roster")
D.execute("UPDATE members SET trial_acknowledged_at=? WHERE email='alex@example.com'", ((today - dt.timedelta(days=15)).isoformat() + "T08:00:00",)); D.commit()
ok('class="dot ok"' in alex.get("/home").get_data(as_text=True) and '<span class=rowtitle><span class="dot ok" aria-hidden=true></span>SafeSport training</span><span class=v>expires 2027-05-01</span>' in alex.get("/profile").get_data(as_text=True) and "Trial ended" not in alex.get("/home").get_data(as_text=True), "a verified member keeps the normal card after the trial date has passed")
day = "2026-12-06"
eli.post("/practices", data=dict(csrf=csrf(eli, "/practices"), action="add", date=day, start="19:00", end="20:30", location="Sort Pool"))
spid = D.execute("SELECT id FROM practices WHERE date=? AND location='Sort Pool'", (day,)).fetchone()[0]
def sorter(first, last, email, pref=None, going=False):
    c = A.app.test_client(); data = dict(csrf=csrf(c, "/join"), first=first, last=last, email=email, phone="1")
    if pref: data["preferred_first"] = pref
    c.post("/join", data=data, follow_redirects=True)
    if going: c.post("/practices", data=dict(csrf=csrf(c, "/practices"), pid=spid, action="going"))
    return D.execute("SELECT id FROM members WHERE email=?", (email,)).fetchone()[0]
sorter("Mia", "Barnes", "mia.sort@example.com", going=True)
sorter("Liam", "Carter", "liam.sort@example.com", going=True)
sorter("Zoe", "Able", "amy.sort@example.com", pref="Amy")
sorter("Noah", "Diaz", "noah.sort@example.com")
ava = sorter("Ava", "Evans", "ava.sort@example.com", going=True)
ben = sorter("Ben", "Foster", "ben.sort@example.com")
sorter("Aaron", "Quinn", "zack.sort@example.com", pref="Zack")
eli.post("/admin", data=dict(csrf=csrf(eli, "/admin"), member_id=ava, date=day))
eli.post("/admin", data=dict(csrf=csrf(eli, "/admin"), member_id=ben, date=day))
page = eli.get("/admin?date=%s" % day).get_data(as_text=True)
g0, e0 = page.index(">Going <"), page.index(">Everyone else <")
going_html, rest_html = page[g0:e0], page[e0:]
ok(">Going <span class=t3>3</span>" in page and going_html.index("Ava Evans") < going_html.index("Liam Carter") < going_html.index("Mia Barnes") and "Amy Able" not in going_html and 'class="psub ell st-bad"' in going_html and '>Not cleared</span>' in going_html and ">✓ Checked in</button>" in going_html and "Checked in (" in page and rest_html.index("Amy Able") < rest_html.index("Ben Foster") < rest_html.index("Noah Diaz") < rest_html.index("Zack Quinn") and "Aaron Quinn" not in rest_html.split("Zack Quinn")[0] and "Liam Carter" not in rest_html and "Going (3)" in page and "Not Going (0)" in page and "No Response" not in page and 'class="chip chip-active on"' in page and 'aria-disabled=true>Not Going (0)' in page, "check-in sections sort A-Z by display name and keep clearance badges")
found = eli.get("/admin?date=%s&q=Liam" % day).get_data(as_text=True)
eli.post("/admin", data=dict(csrf=csrf(eli, "/admin"), member_id=ava, date=day, action="undo"))
back = eli.get("/admin?date=%s" % day).get_data(as_text=True)
ok(">Going <span class=t3>1</span>" in found and "Liam Carter" in found and "Mia Barnes" not in found and ">Everyone else <span class=t3>0</span>" in found and back.index(">Going <") < back.index("Ava Evans") < back.index("Mia Barnes") < back.index(">Everyone else <") and ">Check in</button>" in back[back.index("Ava Evans"):back.index("Mia Barnes")], "search stays inside the sections and undo returns a going member to Going")
noah = D.execute("SELECT id FROM members WHERE email='noah.sort@example.com'").fetchone()[0]
D.execute("INSERT INTO rsvps(practice_id,member_id,going) VALUES(?,?,0)", (spid, noah)); D.commit()
listed = eli.get("/admin?date=%s" % day).get_data(as_text=True)
lg, le = listed.index(">Going <"), listed.index(">Everyone else <")
ok("Noah Diaz" not in listed[lg:le] and "Noah Diaz" not in listed[le:] and "Not Going (1)" in listed and "aria-disabled=true>Not Going" not in listed and ">Check in</button>" in listed[lg:le] and ">Check in</button>" in listed[le:], "going view lists RSVPs and everyone else, and leaves not-going off both")
only_not = eli.get("/admin?date=%s&filt=not" % day).get_data(as_text=True)
ok("Noah Diaz" in only_not and ">Not Going <span class=t3>1</span>" in only_not and ">Everyone else" not in only_not and ">Going <span" not in only_not and "Mia Barnes" not in only_not and ">Check in</button>" in only_not and ('class="chip chip-active on" href="/admin?date=%s&amp;filt=not' % day) in only_not, "not going view is only the not-going list")
only_in = eli.get("/admin?date=%s&filt=in" % day).get_data(as_text=True)
ok("Ben Foster" in only_in and "Ava Evans" not in only_in and "Mia Barnes" not in only_in and "Noah Diaz" not in only_in and ">Everyone else" not in only_in and ">Going <span" not in only_in and ">Checked in <span class=t3>1</span>" in only_in, "checked-in view is only checked-in people")
fell = eli.get("/admin?date=2026-12-05&filt=in").get_data(as_text=True)
ok(">Going <span" in fell and ">Everyone else" in fell and 'class="chip chip-active on"' in fell.split("Not Going")[0] and 'aria-disabled=true>Checked in (0)' in fell and 'aria-disabled=true>Not Going (0)' in fell, "an empty checked-in filter falls back to Going")
tok_in = csrf(eli, "/admin")
kept = eli.post("/admin", data=dict(csrf=tok_in, member_id=ava, date=day, filt="in"), follow_redirects=False)
undone = eli.post("/admin", data=dict(csrf=tok_in, member_id=ben, date=day, action="undo", filt="in"), follow_redirects=False)
still = eli.post("/admin", data=dict(csrf=tok_in, member_id=ava, date=day, action="undo", filt="in"), follow_redirects=False)
ok("filt=in" in kept.headers["Location"] and "filt=in" in undone.headers["Location"] and "filt=in" not in still.headers["Location"], "undoing the last check-in leaves Checked in and returns to Going")
yesterday = (A.today_pt() - dt.timedelta(days=1)).isoformat()
ren = A.app.test_client(); join(ren, "Ren", "Ew", "ren@example.com")
rid = D.execute("SELECT id FROM members WHERE email='ren@example.com'").fetchone()[0]
D.execute("UPDATE members SET usawp_status='verified', usawp_number='659226', usawp_valid_until=?, usawp_verified_by='Eli Joern', usawp_verified_at='2026-01-01T00:00' WHERE id=?", (yesterday, rid))
D.execute("INSERT INTO member_reqs(member_id,req_id,completed_on,expires_on,source,by,at) VALUES(?,?,NULL,?, 'test','test','2026-01-01T00:00')", (rid, ssid, yesterday)); D.commit()
rh = ren.get("/profile").get_data(as_text=True)
rhome = ren.get("/home").get_data(as_text=True)
ok('<span class=rowtitle><span class="dot bad" aria-hidden=true></span>USAWP #659226</span><span class=v>expires ' + yesterday + '</span>' in rh and '<span class=rowtitle><span class="dot bad" aria-hidden=true></span>SafeSport training</span><span class=v>expired</span>' in rh and 'class="dot bad"' in rhome and ("Membership expired %s" % yesterday) in rh and ("SafeSport expired %s" % yesterday) in rh and ">Reverify membership<" in rh and 'id=reverifyForm hidden' in rh and 'value="659226"' in rh and ">Send<" in rh and "Cleared for water polo" not in rhome and "Needs:" not in rh and D.execute("SELECT usawp_status FROM members WHERE id=?", (rid,)).fetchone()[0] == "expired", "a passed membership date returns to Not cleared with Reverify, and an expired SafeSport date is listed")
sent = ren.post("/home", data=dict(csrf=csrf(ren, "/home"), usawp_number="424242"), follow_redirects=True).get_data(as_text=True)
ok("Sent to Grunions for verification" in sent and ">Status<" not in ren.get("/profile").get_data(as_text=True) and 'class="dot warn"' in sent and "USAWP #424242" in sent and ">Reverify membership<" not in sent and ("Membership expired %s" % yesterday) not in sent and tuple(D.execute("SELECT member_number, status FROM verify_requests WHERE member_id=? ORDER BY id DESC LIMIT 1", (rid,)).fetchone()) == ("424242", "pending"), "Reverify sends a new request, shows the toast, and the card goes to Pending")
sue = A.app.test_client(); join(sue, "Sue", "Park", "sue@example.com")
uid = D.execute("SELECT id FROM members WHERE email='sue@example.com'").fetchone()[0]
D.execute("UPDATE members SET usawp_status='verified', usawp_number='1112223', usawp_valid_until='2027-08-31' WHERE id=?", (uid,))
D.execute("INSERT INTO member_reqs(member_id,req_id,completed_on,expires_on,source,by,at) VALUES(?,?,NULL,?, 'test','test','2026-01-01T00:00')", (uid, ssid, yesterday)); D.commit()
shome = sue.get("/home").get_data(as_text=True)
sprof = sue.get("/profile").get_data(as_text=True)
ok(("SafeSport expired %s" % yesterday) in sprof and '<span class=rowtitle><span class="dot bad" aria-hidden=true></span>SafeSport training</span><span class=v>expired</span>' in sprof and ">Reverify membership<" not in sprof and "name=usawp_number" not in shome and "name=usawp_number" not in sprof and "USAWP #1112223" in shome and "Membership expired" not in sprof and ("SafeSport expired " + A.fmt_long(yesterday)) in eli.get("/admin/member/%d" % uid).get_data(as_text=True), "expired SafeSport stays Not cleared without a membership reverify button")

# notifications: web push + email
sw = jane.get("/sw.js").get_data(as_text=True)
home_note = jane.get("/home").get_data(as_text=True)
nh = jane.get("/notifications").get_data(as_text=True)
eh = eli.get("/notifications").get_data(as_text=True)
ok("showNotification" in sw and "notificationclick" in sw and "openWindow" in sw and "Allow notifications" in home_note and "Add to Home Screen" in home_note and "iOS 16.4" in home_note and "id=allowPush" in home_note and A.VAPID_PUBLIC and A.VAPID_PUBLIC in home_note and os.path.isfile(A.VAPID_PATH), "service worker opens the notification URL, and the home card can allow notifications")
ok('value="team_chat" checked' in nh and "Practice reminder (~3 hours before)" in nh and "Verification result" in nh and "Practice cancelled" in nh and "Trial, membership, SafeSport, and background screening expiring or expired" in nh and "Coaches chat" not in nh and "New verification requests" not in nh and "Practice cancellation emails always send" in nh and "Coaches chat" in eh and "New verification requests" in eh, "notification toggles default on; coaches and admin types stay on those roles")
keep = ["practice_reminder", "verification_result", "practice_cancelled", "expiry"]
jane.post("/notifications", data={"csrf": csrf(jane, "/notifications"), "push": keep})
saved = jane.get("/notifications").get_data(as_text=True)
ok('value="team_chat" checked' not in saved and 'value="expiry" checked' in saved and "name=email_reminders value=1 checked" not in saved, "a member can turn off team chat pushes and reminder emails")
ok(jane.post("/api/push/subscribe", json={"endpoint": "https://push.example/jane", "keys": {"p256dh": "pk", "auth": "ak"}}).status_code == 400, "push subscribe requires CSRF")
ok(jane.post("/api/push/subscribe", json={"endpoint": "https://push.example/jane", "keys": {"p256dh": "pk", "auth": "ak"}}, headers={"X-CSRF": csrf(jane, "/home")}).status_code == 200 and tuple(D.execute("SELECT member_id, p256dh FROM push_subscriptions WHERE endpoint='https://push.example/jane'").fetchone())[1] == "pk", "a browser subscription is stored for the member")
def pushsub(c, endpoint):
    c.post("/api/push/subscribe", json={"endpoint": endpoint, "keys": {"p256dh": "k", "auth": "a"}}, headers={"X-CSRF": csrf(c, "/home")})
pushsub(eli, "https://push.example/eli"); pushsub(john, "https://push.example/john")
pushes = []; emails = []
A.send_push = lambda sub, payload: pushes.append((sub["member_id"], payload))
A.smtp_ready = lambda: True
A.send_email = lambda to, subj, text: emails.append((to, subj, text))
D.execute("UPDATE members SET role='coach', is_admin=0 WHERE email='john@example.com'"); D.commit()
jane.post("/notifications", data={"csrf": csrf(jane, "/notifications"), "email_reminders": "1", "push": keep + ["team_chat"]})
eli.post("/api/messages", json={"body": "See you at the pool"}, headers={"X-CSRF": csrf(eli, "/chat")})
mine = [p for p in pushes if p[0] == D.execute("SELECT id FROM members WHERE email='jane@example.com'").fetchone()[0]]
ok(mine and mine[-1][1]["title"] == "Team chat" and mine[-1][1]["url"] == "/chat" and "See you at the pool" in mine[-1][1]["body"] and not any(p[0] == D.execute("SELECT id FROM members WHERE email='eli@example.com'").fetchone()[0] and p[1]["url"] == "/chat" and "See you at the pool" in p[1]["body"] for p in pushes), "team chat push goes to other members and skips the sender")
pushes.clear()
eli.post("/api/messages?c=coaches", json={"body": "Lineup is set"}, headers={"X-CSRF": csrf(eli, "/chat?c=coaches")})
jid = D.execute("SELECT id FROM members WHERE email='john@example.com'").fetchone()[0]
janie = D.execute("SELECT id FROM members WHERE email='jane@example.com'").fetchone()[0]
jh = john.get("/notifications").get_data(as_text=True)
ok(any(p[0] == jid and p[1]["url"] == "/chat?c=coaches" and p[1]["title"] == "Coaches chat" for p in pushes) and not any(p[0] == janie for p in pushes) and "Coaches chat" in jh and "New verification requests" not in jh, "coaches chat push stays with coaches and admins")
pushes.clear()
jane.post("/notifications", data={"csrf": csrf(jane, "/notifications"), "push": keep})
eli.post("/api/messages", json={"body": "Another note"}, headers={"X-CSRF": csrf(eli, "/chat")})
ok(not any(p[0] == janie for p in pushes), "team chat push respects the member toggle")
emails.clear(); pushes.clear()
day = (A.today_pt() + dt.timedelta(days=1)).isoformat()
eli.post("/practices", data=dict(csrf=csrf(eli, "/practices"), action="add", date=day, start="03:00", end="04:00", location="Notify Pool"))
npid = D.execute("SELECT id FROM practices WHERE location='Notify Pool'").fetchone()[0]
n_members = D.execute("SELECT COUNT(*) FROM members WHERE COALESCE(role,'')!='system'").fetchone()[0]
eli.post("/practices", data=dict(csrf=csrf(eli, "/practices"), pid=npid, action="cancel"))
cancel_mail = [e for e in emails if "Notify Pool" in e[2]]
ok(len(cancel_mail) == n_members and all(A.fmt_d(day) in e[2] and "3:00am" in e[2] and "4:00" in e[2] and "Notify Pool" in e[2] for e in cancel_mail) and any(e[0] == "jane@example.com" for e in cancel_mail) and any(p[0] == jid and p[1]["url"] == "/practices/%s" % npid and p[1]["title"] == "Practice cancelled" for p in pushes), "cancelling a practice emails every member and pushes subscribers")
n_mail = len(emails)
eli.post("/practices", data=dict(csrf=csrf(eli, "/practices"), pid=npid, action="cancel"))
ok(len(emails) == n_mail, "cancelling the same practice again does not send another email")
eli.post("/practices", data=dict(csrf=csrf(eli, "/practices"), pid=npid, action="restore"))
eli.post("/practices", data=dict(csrf=csrf(eli, "/practices"), pid=npid, action="cancel"))
ok(len([e for e in emails if "Notify Pool" in e[2]]) == n_members * 2, "restoring a practice lets a later cancel notify again")
pushes.clear()
start = dt.datetime.combine(A.today_pt() + dt.timedelta(days=1), dt.time(3, 15))
eli.post("/practices", data=dict(csrf=csrf(eli, "/practices"), action="add", date=start.date().isoformat(), start="03:15", end="04:15", location="Reminder Pool"))
rpid = D.execute("SELECT id FROM practices WHERE location='Reminder Pool'").fetchone()[0]
jane.post("/practices", data=dict(csrf=csrf(jane, "/practices"), pid=rpid, action="going"))
eli.post("/practices", data=dict(csrf=csrf(eli, "/practices"), pid=rpid, action="notgoing"))
nd = A.open_db()
try:
    A.run_practice_reminders(nd, start - dt.timedelta(hours=2)); A.run_practice_reminders(nd, start - dt.timedelta(hours=2))
finally:
    nd.close()
ok(sum(1 for p in pushes if p[0] == janie and p[1]["title"] == "Practice reminder" and p[1]["url"] == "/practices/%s" % rpid and "about 2 hours" in p[1]["body"]) == 1 and not any(p[0] == D.execute("SELECT id FROM members WHERE email='eli@example.com'").fetchone()[0] and "Reminder Pool" in p[1]["body"] for p in pushes), "a practice reminder goes once to members who RSVP'd going, about 3 hours before")
pushes.clear(); emails.clear()
soon = (A.today_pt() + dt.timedelta(days=7)).isoformat()
tomorrow = (A.today_pt() + dt.timedelta(days=1)).isoformat()
D.execute("UPDATE members SET usawp_valid_until=?, email_reminders=1, usawp_status='verified' WHERE email='jane@example.com'", (soon,))
D.execute("UPDATE members SET usawp_valid_until=?, email_reminders=0, usawp_status='verified' WHERE email='sue@example.com'", (soon,))
D.execute("UPDATE members SET usawp_valid_until=? WHERE email='ren@example.com'", ((A.today_pt() + dt.timedelta(days=8)).isoformat(),))
D.execute("UPDATE member_reqs SET expires_on=? WHERE member_id=? AND req_id=?", (tomorrow, D.execute("SELECT id FROM members WHERE email='casey@example.com'").fetchone()[0], ssid))
D.commit()
tmember = A.app.test_client(); join(tmember, "Tess", "Trial", "tess.trial@example.com")
D.execute("UPDATE members SET trial_acknowledged_at=?, usawp_status='unknown', usawp_valid_until=NULL WHERE email='tess.trial@example.com'", ((A.today_pt() - dt.timedelta(days=14)).isoformat() + "T08:00:00",))
D.commit()
pushsub(tmember, "https://push.example/tess")
sue_id = D.execute("SELECT id FROM members WHERE email='sue@example.com'").fetchone()[0]
D.commit()
pushsub(sue, "https://push.example/sue")
pushsub(casey, "https://push.example/casey")
nd = A.open_db()
try:
    A.run_expiry_notices(nd); A.run_expiry_notices(nd)
finally:
    nd.close()
jane_mail = [e for e in emails if e[0] == "jane@example.com" and "membership" in e[1].lower()]
sue_mail = [e for e in emails if e[0] == "sue@example.com"]
ss_mail = [e for e in emails if "SafeSport" in e[1]]
trial_mail = [e for e in emails if e[0] == "tess.trial@example.com"]
ok(len(jane_mail) == 1 and "in 7 days" in jane_mail[0][2] and "/home" in jane_mail[0][2] and A.TRIAL_JOIN_URL in jane_mail[0][2] and sue_mail == [] and not any(e[0] == "ren@example.com" and "in 8 days" in e[2] for e in emails) and len(ss_mail) == 1 and "tomorrow" in ss_mail[0][2] and len(trial_mail) == 1 and "today" in trial_mail[0][2] and A.TRIAL_JOIN_URL in trial_mail[0][2] and any(p[0] == sue_id and p[1]["url"] == "/home" and "membership" in p[1]["body"].lower() for p in pushes) and any(p[1]["url"] == "/home" and "SafeSport" in p[1]["body"] for p in pushes) and any(p[1]["url"] == "/home" and "trial" in p[1]["body"].lower() for p in pushes), "expiry emails and pushes go out 7 days, 1 day, and the day it expires, once, and reminder emails can be turned off")
pushes.clear()
vera = A.app.test_client(); join(vera, "Vera", "Fy", "vera@example.com")
vid = D.execute("SELECT id FROM members WHERE email='vera@example.com'").fetchone()[0]
D.commit()
pushsub(vera, "https://push.example/vera")
vera.post("/home", data=dict(csrf=csrf(vera, "/home"), usawp_number="515151"), follow_redirects=True)
eli_id = D.execute("SELECT id FROM members WHERE email='eli@example.com'").fetchone()[0]
ok(any(p[0] == eli_id and p[1]["title"] == "New verification request" and p[1]["url"] == "/admin" and "515151" in p[1]["body"] for p in pushes) and not any(p[0] == vid and p[1]["title"] == "New verification request" for p in pushes), "a new verification request pushes admins")
vr = D.execute("SELECT id FROM verify_requests WHERE member_id=? AND status='pending'", (vid,)).fetchone()[0]
c0.post("/api/verify-requests/%d/result" % vr, headers=H, json={"verified": True, "member_number": "515151", "membership_expires_on": "2027-08-31"})
ok(any(p[0] == vid and p[1]["title"] == "Verification result" and p[1]["url"] == "/home" and "verified" in p[1]["body"].lower() for p in pushes), "the verification result pushes the member")

# unread badges: app icon, chat tabs, schedule changes and cancellations
swb = jane.get("/sw.js").get_data(as_text=True)
hb = jane.get("/home").get_data(as_text=True)
ok("setAppBadge" in swb and "clearAppBadge" in swb and "data.badge" in swb and "navigator.setAppBadge" in hb and "clearAppBadge" in hb and "data-badge=chat" in hb and "data-badge=schedule" in hb and "background:var(--bad)" in hb, "app icon badge and red nav bubbles")
ju, jnu, eu = jane.get("/api/unread").get_json(), john.get("/api/unread").get_json(), eli.get("/api/unread").get_json()
pushes.clear()
eli.post("/api/messages", json={"body": "Badge ping"}, headers={"X-CSRF": csrf(eli, "/chat")})
ja, jo, el = jane.get("/api/unread").get_json(), john.get("/api/unread").get_json(), eli.get("/api/unread").get_json()
jp = [p for p in pushes if p[0] == jid]
ok(ja["team"] == ju["team"] + 1 and ja["chat"] == ju["chat"] + 1 and ja["coaches"] == 0 and ja["total"] == ja["chat"] + ja["schedule"] and jo["team"] == jnu["team"] + 1 and jo["chat"] == jnu["chat"] + 1 and el["team"] == eu["team"] and jp and jp[-1][1]["badge"] == jo["total"], "a team message badges other people, not the sender, and the push carries the total")
jane.get("/chat")
mx = D.execute("SELECT COALESCE(MAX(id),0) FROM messages WHERE channel='team'").fetchone()[0]
ok(jane.get("/api/unread").get_json()["team"] == 0 and D.execute("SELECT last_read FROM chat_reads WHERE member_id=? AND channel='team'", (janie,)).fetchone()[0] == mx, "opening team chat stores last_read and clears it")
jb, jane_now = john.get("/api/unread").get_json(), jane.get("/api/unread").get_json()
eli.post("/api/messages?c=coaches", json={"body": "Badge coaches"}, headers={"X-CSRF": csrf(eli, "/chat?c=coaches")})
ja, jo = jane.get("/api/unread").get_json(), john.get("/api/unread").get_json()
cht = john.get("/chat").get_data(as_text=True)
ok(jo["coaches"] == jb["coaches"] + 1 and ja["coaches"] == 0 and ja["total"] == jane_now["total"] and re.search(r'data-badge=coaches[^>]*>Coaches<span class=badge>\d+</span>', cht) and not re.search(r'data-badge=team[^>]*>Team<span class=badge>', cht), "coaches unread stays on the Coaches tab and off member totals")
ok(john.get("/chat?c=coaches").status_code == 200 and john.get("/api/unread").get_json()["coaches"] == 0, "opening coaches chat clears it")
def _audience(channel):
    rows = D.execute("SELECT id, role, is_admin FROM members WHERE COALESCE(role,'')!='system'").fetchall()
    if channel == "coaches": return {r[0] for r in rows if r[1] == "coach" or r[2]}
    return {r[0] for r in rows}
def _seen(c, channel):
    rows = c.get("/api/messages?c=%s&sync=1" % channel).get_json()
    hit = [m for m in rows if m.get("seen")]
    return hit[-1]["seen"] if hit else None
eli.post("/api/messages", json={"body": "Seen check"}, headers={"X-CSRF": csrf(eli, "/chat")})
eli_id_seen = D.execute("SELECT id FROM members WHERE email='eli@example.com'").fetchone()[0]
team_seen = _seen(eli, "team")
team_ids = {p["id"] for p in team_seen["seen"]}
ok(team_seen and team_seen["label"].startswith("Seen by") and "not_yet" not in team_seen and eli_id_seen not in team_ids and team_seen["total"] == len(_audience("team") - {eli_id_seen}) and janie not in team_ids and sum(1 for m in eli.get("/api/messages?sync=1").get_json() if m.get("seen")) == 1, "the latest team message counts everyone except the sender")
D.execute("UPDATE members SET preferred_first='Jay' WHERE id=?", (janie,)); D.commit()
jane.get("/api/messages")
team_seen = _seen(eli, "team")
ok(any(p["id"] == janie and p["name"].startswith("Jay ") and p["initials"] == "JD" for p in team_seen["seen"]), "opening the channel marks it seen and uses the preferred name")
D.execute("UPDATE members SET preferred_first=NULL WHERE id=?", (janie,)); D.commit()
for pid in _audience("team"):
    if pid != eli_id_seen:
        D.execute("INSERT INTO chat_reads(member_id, channel, last_read) VALUES(?,?,?) ON CONFLICT(member_id, channel) DO UPDATE SET last_read=MAX(chat_reads.last_read, excluded.last_read)", (pid, "team", team_seen["id"]))
D.commit()
everyone = _seen(jane, "team")
ok(everyone["label"] == "Seen by everyone" and len(everyone["seen"]) == everyone["total"], "Seen by everyone once the rest of the channel has read it")
eli.post("/api/messages?c=coaches", json={"body": "Seen coaches"}, headers={"X-CSRF": csrf(eli, "/chat?c=coaches")})
coach_seen = _seen(eli, "coaches")
coach_page = eli.get("/chat?c=coaches").get_data(as_text=True)
ok(janie not in {p["id"] for p in coach_seen["seen"]} and coach_seen["total"] == len(_audience("coaches") - {eli_id_seen}) and "seenline" in eli.get("/chat").get_data(as_text=True) and "id=seenSheet" in coach_page and "class=botsheet" in coach_page and ">Not yet</h3>" not in coach_page and "grunionsOpenSheet" in coach_page, "coaches read receipts count coaches and admins, not players")
dayb = (A.today_pt() + dt.timedelta(days=9)).isoformat()
eli.post("/practices", data=dict(csrf=csrf(eli, "/practices"), action="add", date=dayb, start="19:00", end="20:30", location="Badge Pool", note=""))
bpid = D.execute("SELECT id FROM practices WHERE location='Badge Pool'").fetchone()[0]
es, js = eli.get("/api/unread").get_json()["schedule"], jane.get("/api/unread").get_json()["schedule"]
eli.post("/practices", data=dict(csrf=csrf(eli, "/practices"), pid=bpid, action="edit", start="18:00", end="20:30", location="Badge Pool", note="moved"))
ok(jane.get("/api/unread").get_json()["schedule"] == js + 1 and eli.get("/api/unread").get_json()["schedule"] == es, "a practice change badges members and not the editor")
eli.post("/practices", data=dict(csrf=csrf(eli, "/practices"), pid=bpid, action="edit", start="18:00", end="20:30", location="Badge Pool", note="moved"))
pg = jane.get("/practices").get_data(as_text=True)
chunk = pg.split("id=p%d data-pid=%d" % (bpid, bpid))[1].split("id=p")[0]
ok(jane.get("/api/unread").get_json()["schedule"] == js + 1 and ("data-seen=%d" % bpid) in chunk and "Cancelled" not in chunk, "the same edit does not badge again, and the list keeps the bubble")
ok(jane.post("/api/practices/%d/seen" % bpid).status_code == 400 and jane.post("/api/practices/%d/seen" % bpid, headers={"X-CSRF": csrf(jane, "/home")}).status_code == 200, "marking a practice seen requires CSRF")
D.commit()
seen_at = D.execute("SELECT seen_at FROM practice_notices WHERE practice_id=? AND member_id=? AND kind='change'", (bpid, janie)).fetchone()[0]
ok(bool(seen_at) and jane.get("/api/unread").get_json()["schedule"] == js, "seen_at clears the schedule count")
eli.post("/practices", data=dict(csrf=csrf(eli, "/practices"), pid=bpid, action="cancel"))
pg = jane.get("/practices").get_data(as_text=True)
chunk = pg.split("id=p%d data-pid=%d" % (bpid, bpid))[1].split("id=p")[0]
ok(("data-seen=%d" % bpid) in chunk and "Cancelled" in chunk and jane.get("/api/unread").get_json()["schedule"] == js + 1, "a cancellation puts a red bubble on that practice")
jane.post("/api/practices/%d/seen" % bpid, headers={"X-CSRF": csrf(jane, "/practices")})
pg = jane.get("/practices").get_data(as_text=True)
chunk = pg.split("id=p%d data-pid=%d" % (bpid, bpid))[1].split("id=p")[0]
ok(("data-seen=%d" % bpid) not in chunk and "Cancelled" in chunk and jane.get("/api/unread").get_json()["schedule"] == js, "opening the cancellation clears its bubble")

# Pacific time. 5pm PDT is midnight UTC, which used to hide the same evening's practice.
from zoneinfo import ZoneInfo as _ZoneInfo
try:
    _ZoneInfo("America/Los_Angeles"); _tz_ok = True
except Exception:
    _tz_ok = False
ok(_tz_ok and A.today_pt().isoformat() == dt.datetime.now(A.PT).date().isoformat(), "Pacific timezone data loads so tonight's practice is not judged on UTC")
fri = "2026-10-23"
D.execute("INSERT OR IGNORE INTO practices(date,start,end,location) VALUES(?,?,?,?)", (fri, "19:00", "20:30", "Westminster High School")); D.commit()
row = D.execute("SELECT id, cancelled, end FROM practices WHERE date=? AND location='Westminster High School'", (fri,)).fetchone()
ok(row is not None and row[1] == 0 and row[2] == "20:30", "Friday Oct 23 practice is stored and was not deleted")
real_now = A.now_pt
try:
    A.now_pt = lambda: dt.datetime(2026, 10, 24, 0, 30, tzinfo=dt.timezone.utc)  # 5:30pm PDT
    sched = jane.get("/practices").get_data(as_text=True)
    home = jane.get("/home").get_data(as_text=True)
    nxt = home[home.find('class="card tap nextcard"'):]
    nxt = nxt[:nxt.find("I'm going")]
    adm = eli.get("/admin").get_data(as_text=True)
    ok("class=dn>23<" in sched and "class=mo>OCT<" in sched and "7:00 – 8:30 PM" in sched and "Westminster High School" in sched and "class=nxtitle>Water Polo Practice</div>" in nxt and "Fri, Oct 23 · 7:00 PM" in nxt and "7:00 PM" in nxt and "Westminster HS" in nxt and "class=datetile" not in nxt and 'value="2026-10-23"' in adm, "at 5:30pm Pacific, Friday's practice is on the schedule and check-in uses that date")
    ok(D.execute("SELECT COUNT(*) FROM practices WHERE date=? AND location='Westminster High School'", (fri,)).fetchone()[0] == 1, "opening the schedule does not delete Friday's practice")
    A.now_pt = lambda: dt.datetime(2026, 10, 24, 3, 30, tzinfo=dt.timezone.utc)  # 8:30pm PDT
    ok("class=dn>23<" in jane.get("/practices").get_data(as_text=True), "the practice stays up through 8:30pm Pacific")
    A.now_pt = lambda: dt.datetime(2026, 10, 24, 3, 31, tzinfo=dt.timezone.utc)  # 8:31pm PDT
    late = jane.get("/practices").get_data(as_text=True)
    late_home = jane.get("/home").get_data(as_text=True)
    late_i = late_home.find('class="card tap nextcard"')
    late_j = late_home.find("I'm going", late_i) if late_i >= 0 else -1
    late_next = late_home[late_i:late_j] if late_j >= 0 else (late_home[late_i:late_i + 500] if late_i >= 0 else "")
    ok("class=dn>23<" not in late and "Westminster HS" not in late_next and 'value="2026-10-23"' in eli.get("/admin").get_data(as_text=True) and D.execute("SELECT COUNT(*) FROM practices WHERE date=? AND location='Westminster High School'", (fri,)).fetchone()[0] == 1, "after 8:30pm Pacific the practice leaves the schedule and the row is still there")
    eli.post("/practices", data=dict(csrf=csrf(eli, "/practices"), action="add", date=fri, start="19:00", end="20:30", location="Pacific Pool"))
    pp = D.execute("SELECT id FROM practices WHERE location='Pacific Pool'").fetchone()[0]
    jane.post("/practices", data=dict(csrf=csrf(jane, "/practices"), pid=pp, action="going"))
    pushes.clear()
    A.now_pt = lambda: dt.datetime(2026, 10, 24, 0, 0, tzinfo=dt.timezone.utc)  # 5:00pm PDT, two hours before 7:00pm
    nd = A.open_db()
    try:
        A.run_practice_reminders(nd); A.run_practice_reminders(nd)
    finally:
        nd.close()
    ok(sum(1 for p in pushes if p[0] == janie and p[1]["title"] == "Practice reminder" and "Pacific Pool" in p[1]["body"] and "about 2 hours" in p[1]["body"]) == 1, "a 7pm Pacific practice reminds about two hours before, not on the UTC clock")
    D.execute("UPDATE members SET usawp_status='verified', usawp_valid_until='2026-10-23' WHERE email='john@example.com'"); D.commit()
    A.now_pt = lambda: dt.datetime(2026, 10, 24, 0, 30, tzinfo=dt.timezone.utc)
    eli.get("/members")
    ok(D.execute("SELECT usawp_status FROM members WHERE email='john@example.com'").fetchone()[0] == "verified", "a membership dated today is still current at 5:30pm Pacific")
    A.now_pt = lambda: dt.datetime(2026, 10, 24, 8, 0, tzinfo=dt.timezone.utc)  # 1:00am PDT
    eli.get("/members")
    ok(D.execute("SELECT usawp_status FROM members WHERE email='john@example.com'").fetchone()[0] == "expired", "that membership expires after midnight Pacific")
finally:
    A.now_pt = real_now

# admin CSV exports
import csv as csvmod, io as io_mod
gone = eli.get("/export"); old_import = eli.get("/import")
exp = eli.get("/transfer").get_data(as_text=True)
ok(gone.status_code == 302 and "/transfer" in gone.headers["Location"] and old_import.status_code == 302 and "/transfer" in old_import.headers["Location"] and ">Transfer<" in eli.get("/members").get_data(as_text=True) and ">Import<" not in eli.get("/members").get_data(as_text=True) and exp.find(">Import<") < exp.find(">Export<") and "Download members CSV" in exp and "Download practices CSV" in exp and "Download detailed attendance CSV" in exp and 'name=start' in exp and 'name=end' in exp and ('value="%s"' % (A.today_pt() - dt.timedelta(days=28)).isoformat()) in exp and ('value="%s"' % (A.today_pt() + dt.timedelta(days=28)).isoformat()) in exp, "Transfer puts import above export, and the old tabs redirect there")
ok("Bring in a Sport:80 export" in exp and "No file imported yet." in exp and 'class="btn btn-primary full"' in exp, "Transfer has one import action and an empty state")
rules = eli.get("/requirements").get_data(as_text=True)
ok("<h1>Rules</h1>" in rules and "Cleared to play means a current USAWP membership" in rules and "value=add>Add</button>" in rules and ("No rules yet." in rules or "<details class=card>" in rules), "Rules has a title, a one-line helper, and an add action")
ok(jane.get("/export").status_code == 403 and jane.get("/members.csv").status_code == 403 and jane.get("/export/practices.csv").status_code == 403 and john.get("/export").status_code == 403 and A.app.test_client().get("/export").status_code == 302, "member, coach, and signed-out visitors cannot export")
exa = A.app.test_client(); join(exa, "Exa", "Export", "exa.export@example.com")
eid = D.execute("SELECT id FROM members WHERE email='exa.export@example.com'").fetchone()[0]
bgid = D.execute("SELECT id FROM requirements WHERE lower(keywords) LIKE '%background%'").fetchone()[0]
D.execute("UPDATE members SET preferred_first='Ex', phone='', role='coach', is_admin=0, usawp_status='verified', usawp_number='4242421', usawp_valid_until='2027-12-01', usawp_verified_at='2026-10-01T09:00', trial_acknowledged_at='2026-09-01T08:00:00' WHERE id=?", (eid,))
D.execute("INSERT INTO member_reqs(member_id,req_id,completed_on,expires_on,source,by,at) VALUES(?,?,?,?,'test','test','2026-01-01')", (eid, ssid, "2026-01-01", "2027-06-01"))
D.execute("INSERT INTO member_reqs(member_id,req_id,completed_on,expires_on,source,by,at) VALUES(?,?,?,?,'test','test','2026-01-01')", (eid, bgid, "2026-01-01", "2028-01-15"))
D.execute("INSERT INTO checkins(member_id,practice_date,location,at) VALUES(?,?,?,?)", (eid, "2026-12-01", "Export Pool", "2026-12-02 03:15:00"))
D.commit()
tay = A.app.test_client(); join(tay, "Tay", "Trial", "tay.trial2@example.com")
tay.post("/home", data=dict(csrf=csrf(tay, "/home"), action="trial"), follow_redirects=True)
pen = A.app.test_client(); join(pen, "Pen", "Ding", "pen.ding@example.com")
pen.post("/home", data=dict(csrf=csrf(pen, "/home"), usawp_number="999111"), follow_redirects=True)
raw = eli.get("/members.csv")
text = raw.data.decode("utf-8-sig"); table = list(csvmod.reader(io_mod.StringIO(text)))
by_email = {r[3]: r for r in table[1:]}
exar, tayr, penr = by_email["exa.export@example.com"], by_email["tay.trial2@example.com"], by_email["pen.ding@example.com"]
ok(raw.data.startswith(b"\xef\xbb\xbf") and table[0] == A.MEMBERS_CSV_HEADER and ("grunions-members-%s.csv" % A.today_pt().isoformat()) in raw.headers["Content-Disposition"] and "bot@grunions.local" not in text, "members CSV is UTF-8 with a BOM, the column list, and today's filename")
ok(exar == ["Exa", "Export", "Ex", "exa.export@example.com", "", "coach", "no", "4242421", "cleared", "2027-12-01", "2027-06-01", "2028-01-15", "2026-09-01", "2026-09-15", "2026-10-01", A.today_pt().isoformat(), "1", "", "", "Background screening expires 2028-01-15"] and tayr[8] == "trial" and tayr[12] == A.today_pt().isoformat() and tayr[-1] == "" and penr[7] == "999111" and penr[8] == "pending" and penr[4] == "555-0100" and by_email["eli@example.com"][-1] == "Background screening missing" and by_email["john@example.com"][-1] == "Background screening expires 2027-03-01", "members CSV has clearance, trial, compliance dates, attendance, and the background screening line for coaches")
eli.post("/practices", data=dict(csrf=csrf(eli, "/practices"), action="add", date="2026-12-01", start="18:00", end="19:30", location="Export Pool"))
eli.post("/practices", data=dict(csrf=csrf(eli, "/practices"), action="add", date="2026-12-02", start="19:00", end="20:30", location="Export Pool"))
ppid = D.execute("SELECT id FROM practices WHERE date='2026-12-01' AND location='Export Pool'").fetchone()[0]
offid = D.execute("SELECT id FROM practices WHERE date='2026-12-02' AND location='Export Pool'").fetchone()[0]
exa.post("/practices", data=dict(csrf=csrf(exa, "/practices"), pid=ppid, action="going"))
jane.post("/practices", data=dict(csrf=csrf(jane, "/practices"), pid=ppid, action="notgoing"))
eli.post("/practices", data=dict(csrf=csrf(eli, "/practices"), pid=offid, action="cancel"))
psum = eli.get("/export/practices.csv?start=2026-12-02&end=2026-12-01")
stable = list(csvmod.reader(io_mod.StringIO(psum.data.decode("utf-8-sig"))))
smap = {r[0]: r for r in stable[1:]}
ok(psum.data.startswith(b"\xef\xbb\xbf") and stable[0] == A.PRACTICE_CSV_HEADER and "grunions-practices-2026-12-01-to-2026-12-02.csv" in psum.headers["Content-Disposition"] and smap["2026-12-01"] == ["2026-12-01", "18:00-19:30", "Export Pool", "no", "1", "1", "", "0", "0", ""] and smap["2026-12-02"] == ["2026-12-02", "19:00-20:30", "Export Pool", "yes", "0", "0", "", "0", "0", ""], "practices CSV is one row per practice and the filename uses the date range")
pdet = eli.get("/export/practices.csv?start=2026-12-01&end=2026-12-01&detail=1")
dtable = list(csvmod.reader(io_mod.StringIO(pdet.data.decode("utf-8-sig"))))
dmap = {r[4]: r for r in dtable[1:]}
ok(dtable[0] == A.ATTENDANCE_CSV_HEADER and "grunions-attendance-2026-12-01-to-2026-12-01.csv" in pdet.headers["Content-Disposition"] and dmap["Ex Export"] == ["2026-12-01", "18:00-19:30", "Export Pool", "no", "Ex Export", "4242421", "going", "yes", "2026-12-01 19:15"] and dmap["Jane Doe"][6:9] == ["not going", "no", ""] and dmap["Eli Joern"][6:9] == ["", "no", ""] and len(dtable) == 1 + D.execute("SELECT COUNT(*) FROM members WHERE COALESCE(role,'')!='system'").fetchone()[0], "detailed attendance is one row per member with RSVP and check-in time")
ok("Choose a start and end date." in eli.get("/export/practices.csv?start=nope&end=2026-12-01", follow_redirects=True).get_data(as_text=True), "a practice export without real dates asks for the range")

# chat edit, delete, reactions
chui = jane.get("/chat").get_data(as_text=True)
ok("contextmenu" in chui and "Message deleted" in chui and "(edited)" in chui and "Delete this message?" in chui and "Message actions" in chui and "😮" in chui and "🎉" in chui and "🙏" in chui and "👎" in chui and "👀" in chui and "🥲" in chui and "💯" in chui and "class=grab" in chui and "class=botsheet" in chui and ">Reply</button>" in chui and ">Copy</button>" in chui and "navigator.vibrate" in chui and "pointerdown" in chui and "(hover:hover) and (pointer:fine)" in chui and "translateY(110%)" in chui and ".25s ease-out" in chui and "grunionsOpenSheet" in chui and "z-index:30" in chui and "inset:auto 0 0 0" in chui and "<h1>Team</h1>" in chui.split("<main>",1)[0] and "<h1>Hi," not in chui.split("<main>",1)[0] and "Log out" not in chui.split("<main>",1)[0] and "/sw.js?v=70" in chui and "function linkify" in chui and "noopener noreferrer" in chui and "geo:0,0?q=" in chui and "a.msglink{color:var(--accent);text-decoration:none" in chui and "writeText(m.body)" in chui and ".rx:not(:empty){margin-top:6px}" in chui and ".m{position:relative;-webkit-touch-callout:none;margin-top:14px;display:flex;flex-direction:column;align-items:flex-start}" in chui and "5*60*1000" in chui and "new Date(prev.at)" in chui and "sameGroup(prev" in chui and "prev=msgs[+rows[j].id.slice(3)]" in chui and "new Date(first.at)" not in chui and "g-mid" in chui and ".m.g-mid,.m.g-last{margin-top:2px}" in chui and "id='seenLine'" in chui and "el!==line" in chui and "document.querySelectorAll('.seenline').forEach(el=>el.remove())" not in chui, "chat page has the press-and-hold action sheet")
import subprocess
_seen_src = chui[chui.find("function seenKey"):chui.find("function openSeen")]
_seen_proc = subprocess.run(["node", "-e", r'''
function El(){ this.children=[]; this.parentNode=null; this._id=""; this.className=""; this._text=""; this.dataset={}; this.type=""; this.textSets=0; }
var byId={};
Object.defineProperty(El.prototype,"id",{get:function(){return this._id},set:function(v){ if(this._id) delete byId[this._id]; this._id=v||""; if(v) byId[v]=this; }});
Object.defineProperty(El.prototype,"textContent",{get:function(){return this._text},set:function(v){ this.textSets++; this._text=String(v); }});
El.prototype.appendChild=function(el){ if(el.parentNode) el.parentNode.removeChild(el); el.parentNode=this; this.children.push(el); return el; };
El.prototype.removeChild=function(el){ this.children=this.children.filter(function(c){return c!==el}); el.parentNode=null; };
El.prototype.remove=function(){ if(this._id) delete byId[this._id]; if(this.parentNode) this.parentNode.removeChild(this); };
El.prototype.querySelectorAll=function(sel){
 var out=[];
 if(sel===".seenline" && (this.className||"").split(/\s+/).indexOf("seenline")>=0) out.push(this);
 if(sel==="#seenLine" && this.id==="seenLine") out.push(this);
 this.children.forEach(function(c){ out=out.concat(c.querySelectorAll(sel)); });
 return out;
};
El.prototype.querySelector=function(sel){ return this.querySelectorAll(sel)[0]||null; };
var root=new El();
var document={
 createElement:function(){return new El()},
 getElementById:function(id){return byId[id]||null},
 querySelectorAll:function(sel){return root.querySelectorAll(sel)}
};
function row(id){ var el=new El(); el.id="msg"+id; root.appendChild(el); return el; }
var seenInfo=null, msgs={};
''' + _seen_src + r'''
row(5); row(9);
var info={id:5,n:6,total:8,label:"Seen by 6",seen:[]};
msgs[5]={id:5,seen:info};
var node=null, writes=0;
for(var i=0;i<5;i++){
 paintSeen([msgs[5]]);
 var cur=document.getElementById("seenLine");
 if(!node){ node=cur; writes=cur.textSets; }
}
for(var n=0;n<3;n++){ var extra=document.createElement("button"); extra.className="seenline"; extra.textContent="Seen by 6"; document.getElementById("msg5").appendChild(extra); }
paintSeen([msgs[5]]);
var afterDup=document.querySelectorAll(".seenline").length;
var same=document.getElementById("seenLine")===node;
var quiet=node.textSets===writes;
msgs[9]={id:9,seen:{id:9,n:1,total:8,label:"Seen by 1",seen:[]}};
delete msgs[5].seen;
paintSeen([msgs[9]]);
var moved=node.parentNode&&node.parentNode.id==="msg9" && document.getElementById("msg5").querySelectorAll(".seenline").length===0;
console.log(JSON.stringify({count:document.querySelectorAll(".seenline").length, afterDup:afterDup, same:same, quiet:quiet, moved:moved, label:node.textContent, node:!!node}));
'''], capture_output=True, text=True)
_seen_out = {}
try: _seen_out = json.loads(_seen_proc.stdout or "{}")
except ValueError: _seen_out = {}
ok(_seen_proc.returncode == 0 and _seen_out.get("afterDup") == 1 and _seen_out.get("count") == 1 and _seen_out.get("same") and _seen_out.get("quiet") and _seen_out.get("moved") and _seen_out.get("label") == "Seen by 1", "several seen polls leave one stable line and do not rewrite it")
_grp_src = chui[chui.find("function sameGroup"):chui.find("function placeWho")]
_grp_proc = subprocess.run(["node", "-e", _grp_src + r'''
function chain(times, uids){
 var prev={uid:uids[0], at:times[0], ann:0, deleted:0}, n=1, i;
 for(i=1;i<times.length;i++){
  var cur={uid:uids[i], at:times[i], ann:0, deleted:0};
  if(!sameGroup(prev, cur)) break;
  prev=cur; n++;
 }
 return n;
}
var t0=Date.parse("2020-06-01T12:00:00Z");
function mins(m){return new Date(t0+m*60000).toISOString()}
console.log(JSON.stringify({
 long:chain([mins(0),mins(4),mins(8),mins(12)],[1,1,1,1]),
 exact:chain([mins(0),mins(5)],[1,1]),
 gap:chain([mins(0),mins(4),mins(10)],[1,1,1]),
 other:chain([mins(0),mins(4),mins(5)],[1,1,2])
}));
'''], capture_output=True, text=True)
_grp_out = {}
try: _grp_out = json.loads(_grp_proc.stdout or "{}")
except ValueError: _grp_out = {}
ok(_grp_proc.returncode == 0 and _grp_out.get("long") == 4 and _grp_out.get("exact") == 2 and _grp_out.get("gap") == 2 and _grp_out.get("other") == 2, "a rolling five-minute gap keeps a chain together until someone else speaks or the gap is longer")
_link_src = chui[chui.find("function safeHttp"):chui.find("function bodyHtml")]
_link_proc = subprocess.run(["node", "-e", r'''
const esc=s=>String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
''' + _link_src + r'''
function has(html, needle){ return html.indexOf(needle)>=0; }
var https=linkify('see https://example.com/a?b=1&c=2.');
var www=linkify('www.example.com/path');
var bare=linkify('go to example.com/path today');
var js=linkify('javascript:alert(1)');
var xss=linkify('<script>alert(1)</script>');
var addr=linkify('pool is 15192 Goldenwest St, Westminster, CA 92683 thanks');
var street=linkify('10 Main Street');
var email=linkify('email me at pat@example.com please');
var court=linkify('meet at 3 pm at the Court');
console.log(JSON.stringify({
 https: has(https,'href="https://example.com/a?b=1&amp;c=2"') && has(https,'target=_blank') && has(https,'rel="noopener noreferrer"') && https.endsWith('.</a>')===false && has(https,'</a>.'),
 www: has(www,'href="https://www.example.com/path"'),
 bare: has(bare,'href="https://example.com/path"'),
 js: js.indexOf('<a')<0 && has(js,'javascript:alert(1)'),
 xss: xss.indexOf('<script>')<0 && has(xss,'&lt;script&gt;'),
 addr: has(addr,'class="msglink maplink"') && has(addr,'maps/search/?api=1&amp;query=15192%20Goldenwest%20St') && has(addr,'data-map="15192 Goldenwest St, Westminster, CA 92683"'),
 street: has(street,'maplink') && has(street,'10%20Main%20Street'),
 email: email.indexOf('<a')<0,
 court: court.indexOf('<a')<0
}));
'''], capture_output=True, text=True)
_link_out = {}
try: _link_out = json.loads(_link_proc.stdout or "{}")
except ValueError: _link_out = {}
ok(_link_proc.returncode == 0 and all(_link_out.get(k) for k in ("https","www","bare","js","xss","addr","street","email","court")), "chat links http addresses and street addresses, and leaves scripts and emails as text")
tj = csrf(jane, "/chat"); te = csrf(eli, "/chat"); tjohn = csrf(john, "/chat")
ok(jane.post("/api/messages", json={"body": "Edit me please"}, headers={"X-CSRF": tj}).status_code == 200, "author can post a message to edit")
mid = [m for m in jane.get("/api/messages").get_json() if m["body"] == "Edit me please"][-1]["id"]
edited = jane.post("/api/messages/%d" % mid, json={"body": "Edited line"}, headers={"X-CSRF": tj})
em = edited.get_json()["message"]
ok(edited.status_code == 200 and em["body"] == "Edited line" and em["edited"] and not em["deleted"], "author edit saves and marks the message edited")
stamp = D.execute("SELECT edited_at FROM messages WHERE id=?", (mid,)).fetchone()[0]; D.commit()
again = jane.post("/api/messages/%d" % mid, json={"body": "Edited line"}, headers={"X-CSRF": tj}).get_json()["message"]
ok(again["edited"] and D.execute("SELECT edited_at FROM messages WHERE id=?", (mid,)).fetchone()[0] == stamp, "saving the same text does not change the edited time")
D.commit()
ok(jane.post("/api/messages/%d" % mid, json={"body": "   "}, headers={"X-CSRF": tj}).status_code == 400 and D.execute("SELECT body FROM messages WHERE id=?", (mid,)).fetchone()[0] == "Edited line", "an edit cannot be empty unless a photo remains")
D.commit()
ok(john.post("/api/messages/%d" % mid, json={"body": "nope"}, headers={"X-CSRF": tjohn}).status_code == 403 and eli.post("/api/messages/%d" % mid, json={"body": "nope"}, headers={"X-CSRF": te}).status_code == 403, "a coach and an admin cannot edit someone else's message")
seen = {m["id"]: m for m in jane.get("/api/messages").get_json()}
eli_seen = {m["id"]: m for m in eli.get("/api/messages").get_json()}
john_seen = {m["id"]: m for m in john.get("/api/messages").get_json()}
ok(seen[mid]["can_delete"] and eli_seen[mid]["can_delete"] and not john_seen[mid]["can_delete"], "delete is offered to the author and an admin")
ok(jane.post("/api/messages/%d/react" % mid, json={"emoji": "👍"}, headers={"X-CSRF": tj}).status_code == 200, "reaction lands before delete")
ok(jane.delete("/api/messages/%d" % mid).status_code == 400, "delete without CSRF is rejected")
ok(john.delete("/api/messages/%d" % mid, headers={"X-CSRF": tjohn}).status_code == 403, "a coach cannot delete someone else's team message")
gone = jane.delete("/api/messages/%d" % mid, headers={"X-CSRF": tj})
gm = gone.get_json()["message"]
ok(gone.status_code == 200 and gm["deleted"] and gm["body"] == "" and not gm["edited"] and not gm["can_delete"] and gm["image"] is None, "author delete leaves a placeholder and clears the body")
after = jane.get("/api/messages").get_json()
ok(not any(m["body"] == "Edited line" for m in after) and any(m["id"] == mid and m["deleted"] and m["body"] == "" for m in after) and str(mid) not in jane.get("/api/reactions?c=team").get_json() and jane.post("/api/messages/%d/react" % mid, json={"emoji": "👍"}, headers={"X-CSRF": tj}).status_code == 400 and jane.delete("/api/messages/%d" % mid, headers={"X-CSRF": tj}).status_code == 200, "deleted message stays in the list, drops reactions, and cannot be reacted to")
ok(jane.post("/api/messages", json={"body": "admin please remove this"}, headers={"X-CSRF": tj}).status_code == 200, "member posts a message an admin will remove")
amid = [m for m in jane.get("/api/messages").get_json() if m["body"] == "admin please remove this"][-1]["id"]
adm = eli.delete("/api/messages/%d" % amid, headers={"X-CSRF": te}).get_json()["message"]
ok(adm["deleted"] and adm["body"] == "" and not any(m["body"] == "admin please remove this" for m in eli.get("/api/messages").get_json()), "an admin can delete another person's team message")
own = [m for m in john.get("/api/messages?c=coaches").get_json() if m["body"].startswith("Coaches only")][-1]
ok(john.delete("/api/messages/%d" % own["id"], headers={"X-CSRF": tjohn}).status_code == 200, "a coach can delete their own coaches-chat message")
line = [m for m in eli.get("/api/messages?c=coaches").get_json() if m["body"] == "lineup"][-1]
ok(john.delete("/api/messages/%d" % line["id"], headers={"X-CSRF": tjohn}).status_code == 403, "a coach cannot delete someone else's coaches-chat message")
ok(john.post("/api/messages?c=coaches", json={"body": "secret coach note"}, headers={"X-CSRF": tjohn}).status_code == 200, "coach posts a note an admin will remove")
cid = [m for m in john.get("/api/messages?c=coaches").get_json() if m["body"] == "secret coach note"][-1]["id"]
ok(jane.delete("/api/messages/%d" % cid, headers={"X-CSRF": tj}).status_code == 403, "a member cannot delete a coaches-chat message")
cd = eli.delete("/api/messages/%d" % cid, headers={"X-CSRF": te}).get_json()["message"]
ok(cd["deleted"] and cd["body"] == "" and any(m["id"] == cid and m["deleted"] for m in eli.get("/api/messages?c=coaches&sync=1").get_json()), "an admin can delete someone else's coaches-chat message")
ok(jane.post("/api/messages", json={"body": "react here"}, headers={"X-CSRF": tj}).status_code == 200, "member posts a message to react to")
rid = [m for m in jane.get("/api/messages").get_json() if m["body"] == "react here"][-1]["id"]
first = jane.post("/api/messages/%d/react" % rid, json={"emoji": "😮"}, headers={"X-CSRF": tj}).get_json()
second = jane.post("/api/messages/%d/react" % rid, json={"emoji": "💩"}, headers={"X-CSRF": tj})
swapped = second.get_json()
who = jane.get("/api/messages/%d/reactors?emoji=%s" % (rid, "💩")).get_json()
ok(first["😮"] == {"n": 1, "mine": True} and second.status_code == 200 and swapped.get("💩") == {"n": 1, "mine": True} and "😮" not in swapped and jane.post("/api/messages/%d/react" % rid, json={"emoji": "nope"}, headers={"X-CSRF": tj}).status_code == 400 and who["people"] and who["people"][0]["name"].startswith("Jane"), "a new reaction replaces the previous one, and a pill can list who reacted")
quoted = jane.post("/api/messages", json={"body": "quoting that", "reply_to": rid}, headers={"X-CSRF": tj}).get_json()
qmsg = [m for m in jane.get("/api/messages?sync=1").get_json() if m["body"] == "quoting that"][-1]
ok(quoted.get("ok") and qmsg["reply"] and qmsg["reply"]["body"] == "react here" and qmsg["reply"]["who"].startswith("Jane") and jane.post("/api/messages", json={"body": "no quote", "reply_to": 999999}, headers={"X-CSRF": tj}).status_code == 200 and [m for m in jane.get("/api/messages?sync=1").get_json() if m["body"] == "no quote"][-1]["reply"] is None, "reply quotes the message above the composer and ignores a missing one")
photos = [m for m in jane.get("/api/messages").get_json() if m.get("body") == "Pool photo" and m.get("image")]
ph = photos[-1]; img = ph["image"]["full"]
cleared = jane.post("/api/messages/%d" % ph["id"], json={"body": "  "}, headers={"X-CSRF": tj}).get_json()["message"]
ok(cleared["body"] == "" and cleared["edited"] and cleared["image"] and jane.get(img).status_code == 200, "a photo message can be saved with no caption")
ok(jane.delete("/api/messages/%d" % ph["id"], headers={"X-CSRF": tj}).get_json()["message"]["image"] is None and jane.get(img).status_code == 404, "deleting a photo message removes the picture")
ok(eli.post("/api/messages", json={"body": "Temp announce xyz", "announcement": True}, headers={"X-CSRF": te}).status_code == 200, "admin posts an announcement to delete")
ann_id = [m for m in eli.get("/api/messages").get_json() if m["body"] == "Temp announce xyz"][-1]["id"]
eli.delete("/api/messages/%d" % ann_id, headers={"X-CSRF": te})
home = jane.get("/home").get_data(as_text=True)
ok("Temp announce xyz" not in home and "$45/mo" in home, "a deleted announcement is not the home card")
ok(jane.get("/api/messages?after=999999").get_json() == [] and any(m["id"] == mid and m["deleted"] for m in jane.get("/api/messages?after=999999&sync=1").get_json()), "sync=1 refreshes older messages and after= stays new-only")
oldp = tempfile.mktemp(suffix=".db")
od = sqlite3.connect(oldp)
od.execute("CREATE TABLE messages(id INTEGER PRIMARY KEY, member_id INTEGER, body TEXT NOT NULL, announcement INTEGER DEFAULT 0, at TEXT)")
od.execute("INSERT INTO messages(member_id, body) VALUES(1, 'kept')")
od.commit()
A.migrate_messages(od)
cols = [r[1] for r in od.execute("PRAGMA table_info(messages)")]
A.migrate_messages(od)
cols2 = [r[1] for r in od.execute("PRAGMA table_info(messages)")]
kept = od.execute("SELECT body, deleted FROM messages").fetchone()
od.close(); os.remove(oldp)
ok(cols == cols2 and set(("channel", "image", "edited_at", "deleted")) <= set(cols) and kept[0] == "kept" and kept[1] == 0, "migrate_messages adds chat columns once and keeps existing rows")

# coaching list: practice checkboxes, separate from coach access
ok(A.is_coach_membership("Coach") and A.is_coach_membership("Individual Membership, Coach") and A.is_coach_membership("Head Coach") and not A.is_coach_membership("coaches") and not A.is_coach_membership("coaching") and not A.is_coach_membership("Masters") and not A.is_coach_membership(""), "coach membership matches the word coach only")
D.execute("UPDATE members SET preferred_first='Sam' WHERE email='john@example.com'"); D.commit()
eli_id = D.execute("SELECT id FROM members WHERE email='eli@example.com'").fetchone()[0]
john_id = D.execute("SELECT id FROM members WHERE email='john@example.com'").fetchone()[0]
jane_id = D.execute("SELECT id FROM members WHERE email='jane@example.com'").fetchone()[0]
prow = D.execute("SELECT id, start, end, location, COALESCE(note,'') FROM practices WHERE cancelled=0 AND " + A.upcoming_where() + " ORDER BY date, start LIMIT 1", A.upcoming_bounds()).fetchone()
pid, pstart, pend, ploc, pnote = prow
base = dict(csrf=csrf(eli, "/practices"), pid=pid, action="edit", start=pstart, end=pend, location=ploc, note=pnote)
staff0 = eli.get("/practices/%d" % pid).get_data(as_text=True)
ok(("name=coach value=\"%d\"" % eli_id) not in staff0 and ("name=coach value=\"%d\"" % john_id) not in staff0 and "No coaches yet." in staff0 and john.get("/admin").status_code == 200 and john.get("/chat?c=coaches").status_code == 200 and eli.get("/admin").status_code == 200, "only people on the coaching list can be assigned, and active coaches can check in")
ok("Coaches:" not in jane.get("/practices").get_data(as_text=True) and "name=coach" not in jane.get("/practices").get_data(as_text=True), "a practice with no coaches has no coaches line, and members have no picker")
def list_act(mid, action):
    return eli.post("/admins", data=dict(csrf=csrf(eli, "/members"), member_id=mid, action=action), follow_redirects=True)
list_act(eli_id, "add_coaching"); list_act(john_id, "add_coaching")
roles = eli.get("/members?view=admins").get_data(as_text=True)
coaches_page = eli.get("/members?view=coaches").get_data(as_text=True)
ok(">People<" in roles and ">Roles<" not in roles and "Remove admin" in roles and "Remove active coach" in coaches_page and "Remove from coaches" in coaches_page and "Add to coaching list" not in coaches_page, "People replaces Roles, and active coach is separate from the coaching list")
eli.post("/practices", data=dict(base, coach=[str(eli_id), str(john_id), str(jane_id)]))
sched, home, staff, coachpg = jane.get("/practices").get_data(as_text=True), jane.get("/home").get_data(as_text=True), eli.get("/practices").get_data(as_text=True), john.get("/practices").get_data(as_text=True)
pdate = D.execute("SELECT date FROM practices WHERE id=?", (pid,)).fetchone()[0]
checkin = eli.get("/admin?date=%s" % pdate).get_data(as_text=True)
ok(" going · Coaches: Eli, Sam" in sched and " going · Coaches: Eli, Sam" in home and "Coaches: Eli, Sam" in coachpg and "Coaches: Eli, Sam" in staff and "Coaches: Eli, Sam" in checkin and 'class="st st-ok coach-elig"' not in sched and 'class="st st-ok coach-elig"' not in staff and "No assigned coach is coach-eligible" not in sched and "No assigned coach is coach-eligible" not in staff and "No assigned coach is coach-eligible" not in eli.get("/practices/%d" % pid).get_data(as_text=True) and 'coachmark" aria-hidden="true"' in eli.get("/practices/%d" % pid).get_data(as_text=True) and 'coachmark" aria-hidden="true"' not in jane.get("/practices/%d" % pid).get_data(as_text=True) and 'class="st st-warn coach-elig">Not eligible' not in eli.get("/practices/%d" % pid).get_data(as_text=True) and "No assigned coach is coach-eligible" not in checkin and "No assigned coach is coach-eligible" not in coachpg and "No assigned coach is coach-eligible" not in eli.get("/home").get_data(as_text=True), "assigned coaches show on every schedule card and on check-in, and each coach row carries its own status")
picker = eli.get("/practices/%d" % pid).get_data(as_text=True)
ok(('name=coach value="%d" checked' % eli_id) in picker and ('name=coach value="%d" checked' % john_id) in picker and ('name=coach value="%d"' % jane_id) not in picker and "<select name=coach" not in picker and "name=coach" not in sched and "name=coach" not in coachpg, "edit practice is a checkbox per coaching-list member, and only an admin gets that list")
ok(jane.post("/practices", data=dict(csrf=csrf(jane, "/practices"), pid=pid, action="edit", start=pstart, end=pend, location=ploc, note=pnote, coach=str(jane_id))).status_code == 403 and D.execute("SELECT member_id FROM practice_coaches WHERE practice_id=? ORDER BY member_id", (pid,)).fetchall() == [(eli_id,), (john_id,)], "a member cannot change practice coaches, and someone off the coaching list is not stored")
list_act(john_id, "remove_coaching")
hid = jane.get("/practices").get_data(as_text=True)
ok("Coaches: Eli" in hid and "Coaches: Eli, Sam" not in hid and D.execute("SELECT member_id FROM practice_coaches WHERE practice_id=? AND member_id=?", (pid, john_id)).fetchone() and john.get("/admin").status_code == 200, "leaving the coaching list hides a coach from the practice and keeps coach access")
list_act(john_id, "add_coaching")
ok("Coaches: Eli, Sam" in jane.get("/practices").get_data(as_text=True), "returning to the coaching list shows the assigned name again")
eli.post("/practices", data=dict(base, coach=[str(john_id)]))
ok("Coaches: Sam" in jane.get("/practices").get_data(as_text=True) and "Coaches: Eli, Sam" not in jane.get("/practices").get_data(as_text=True) and "Coaches: Sam" in jane.get("/home").get_data(as_text=True) and "Coaches: Eli, Sam" not in jane.get("/home").get_data(as_text=True), "unchecking a coach removes that name from the card")
eli.post("/practices", data=base)
ok("Coaches:" not in jane.get("/practices").get_data(as_text=True) and "Coaches:" not in jane.get("/home").get_data(as_text=True), "clearing every coach checkbox removes the line")
list_act(jane_id, "add_coaching")
eli.post("/practices", data=dict(base, coach=[str(jane_id)]))
ok("Coaches: Jane" in jane.get("/practices").get_data(as_text=True), "an athlete on the coaching list can be assigned")
list_act(jane_id, "remove_coaching")
ok("Coaches: Jane" not in jane.get("/practices").get_data(as_text=True) and D.execute("SELECT member_id FROM practice_coaches WHERE practice_id=? AND member_id=?", (pid, jane_id)).fetchone(), "leaving the coaching list hides an athlete who is not an admin or a coach")
eli.post("/practices", data=base)
list_act(jane_id, "add_coaching")
ok(jane.get("/admin").status_code == 403 and jane.get("/chat?c=coaches").status_code == 403, "the coaching list does not grant check-in or coaches chat")
list_act(jane_id, "make_coach")
ok(jane.get("/admin").status_code == 200 and jane.get("/chat?c=coaches").status_code == 200, "Make coach grants check-in and coaches chat")
list_act(jane_id, "remove_coach")
ok(jane.get("/admin").status_code == 403 and jane.get("/chat?c=coaches").status_code == 403 and D.execute("SELECT source FROM coaching_list WHERE member_id=?", (jane_id,)).fetchone()[0] == "manual", "Remove coach revokes access and leaves the coaching list")
kept = list_act(eli_id, "remove_coaching").get_data(as_text=True)
ok("Updated Eli Joern." in kept and not D.execute("SELECT 1 FROM coaching_list WHERE member_id=?", (eli_id,)).fetchone() and ("name=coach value=\"%d\"" % eli_id) not in eli.get("/practices/%d" % pid).get_data(as_text=True) and eli.get("/admin").status_code == 200 and eli.get("/chat?c=coaches").status_code == 200, "an admin can leave the coaching list and keep active coach access")
list_act(eli_id, "add_coaching")
oldp = tempfile.mktemp(suffix=".db")
od = sqlite3.connect(oldp)
od.execute("CREATE TABLE members(id INTEGER PRIMARY KEY, first TEXT)")
od.commit(); od.executescript(A.SCHEMA); od.executescript(A.SCHEMA)
A.migrate_members(od); A.migrate_members(od)
ccols = [r[1] for r in od.execute("PRAGMA table_info(practice_coaches)")]
mcols = [r[1] for r in od.execute("PRAGMA table_info(members)")]
clist = od.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='coaching_list'").fetchone()
od.close(); os.remove(oldp)
barep = tempfile.mktemp(suffix=".db")
bare = sqlite3.connect(barep)
bare.execute("CREATE TABLE members(id INTEGER PRIMARY KEY, first TEXT)")
bare.execute("INSERT INTO members(first) VALUES('Kept')")
A.migrate_practice_coaches(bare); A.migrate_practice_coaches(bare)
kept = bare.execute("SELECT first FROM members").fetchone()[0]
grew = [r[1] for r in bare.execute("PRAGMA table_info(practice_coaches)")]
bare.execute("INSERT INTO practice_coaches(practice_id, member_id) VALUES(1, 1)")
A.migrate_practice_coaches(bare)
still = bare.execute("SELECT member_id FROM practice_coaches").fetchone()[0]
bare.close(); os.remove(barep)
ok(ccols == ["practice_id", "member_id"] and "membership_type" in mcols and clist and kept == "Kept" and grew == ["practice_id", "member_id", "is_lead", "focus"] and still == 1, "an existing database gains the coaching list, membership type, practice coaches, and the lead and focus columns without dropping rows")

# USAWP coach membership fills the coaching list and can show the badge
riley = A.app.test_client(); join(riley, "Riley", "Quinn", "riley@example.com")
D.commit(); riley_id = D.execute("SELECT id FROM members WHERE email='riley@example.com'").fetchone()[0]
list_act(riley_id, "make_coach")
ok(riley.get("/admin").status_code == 200 and riley.get("/chat?c=coaches").status_code == 200 and not D.execute("SELECT 1 FROM coaching_list WHERE member_id=?", (riley_id,)).fetchone(), "Make coach does not add anyone to the coaching list")
list_act(riley_id, "remove_coach")
ok(riley.get("/admin").status_code == 403 and D.execute("SELECT role FROM members WHERE id=?", (riley_id,)).fetchone()[0] == "athlete", "Remove coach sets the role back to athlete")
eli.post("/admin", data=dict(csrf=csrf(eli, "/admin"), member_id=riley_id, date="2026-10-27", action="verify", number="1212121", valid_until="2027-08-31"))
ok(not D.execute("SELECT 1 FROM coaching_list WHERE member_id=?", (riley_id,)).fetchone(), "Mark membership verified does not add anyone to the coaching list")
today = A.today_pt().isoformat(); future = (A.today_pt() + dt.timedelta(days=40)).isoformat(); past = (A.today_pt() - dt.timedelta(days=1)).isoformat()
def answer(verified, **extra):
    D.execute("INSERT INTO verify_requests(member_id,name,email,status,created) VALUES(?,?,?,'pending',?)", (riley_id, "Riley Quinn", "riley@example.com", today))
    D.commit()
    vid = D.execute("SELECT id FROM verify_requests WHERE member_id=? AND status='pending' ORDER BY id DESC LIMIT 1", (riley_id,)).fetchone()[0]
    D.commit()
    body = {"verified": verified}; body.update(extra)
    return c0.post("/api/verify-requests/%d/result" % vid, headers=H, json=body)
answer(False, membership_type="Coach", note="not current")
ok(D.execute("SELECT membership_type FROM members WHERE id=?", (riley_id,)).fetchone()[0] == "Coach" and not D.execute("SELECT 1 FROM coaching_list WHERE member_id=?", (riley_id,)).fetchone() and 'class="st st-ok coach-elig"' not in riley.get("/home").get_data(as_text=True) and 'class="st st-bad coach-elig"' not in riley.get("/home").get_data(as_text=True), "a failed verification does not change the coaching list or show coach eligibility")
answer(True, membership_type="coaching staff")
ok(D.execute("SELECT membership_type FROM members WHERE id=?", (riley_id,)).fetchone()[0] == "coaching staff" and not D.execute("SELECT 1 FROM coaching_list WHERE member_id=?", (riley_id,)).fetchone(), "coaching is not a USAWP coach membership")
answer(True, membership_type="Head Coach", compliance={"SafeSport training": future, "Background screening": future})
ok(D.execute("SELECT role FROM members WHERE id=?", (riley_id,)).fetchone()[0] == "athlete" and D.execute("SELECT source FROM coaching_list WHERE member_id=?", (riley_id,)).fetchone()[0] == "usawp" and riley.get("/admin").status_code == 403 and riley.get("/chat?c=coaches").status_code == 403, "a USAWP coach membership joins the list and grants no coach access")
badge_pages = riley.get("/profile").get_data(as_text=True) + eli.get("/members").get_data(as_text=True) + eli.get("/admin").get_data(as_text=True) + eli.get("/admins").get_data(as_text=True)
members_html = eli.get("/members").get_data(as_text=True)
riley_row = people_row(members_html, "Riley Quinn")
eli_pick = eli.get("/practices/%d" % pid).get_data(as_text=True)
coaches_html = eli.get("/members?view=coaches").get_data(as_text=True)
riley_page = eli.get("/admin/member/%d" % riley_id).get_data(as_text=True)
riley_crow = people_row(coaches_html, "Riley Quinn")
ok('>Coaching</span><span class=v>Coach eligible</span>' in badge_pages and 'class="st st-ok coach-elig"' not in jane.get("/practices").get_data(as_text=True) and ('name=coach value="%d"' % riley_id) in eli_pick and 'class="st st-ok coach-elig">Coach eligible' in eli_pick and ('class="chip-info">Coach · expires ' + future) in riley_row and 'class="chip-info">Coach<' not in riley_row and "Active coach" not in riley_row and ('class="st st-ok">Background screening expires ' + future) not in riley_crow and ('class="chip-info">Coach · expires ' + future) in riley_crow and "Coach eligible" not in riley_crow and "Active coach" not in riley_crow and ('<span class=rowtitle><span class="dot ok" aria-hidden=true></span>Background screening</span><span class=v>' + A.fmt_long(future)) in riley_page and 'class=chip-info>Admin<' in eli.get("/members").get_data(as_text=True) and 'class=chip-info>Admin<' in coaches_html and 'class=chip-info>Admin<' in eli.get("/members?view=admins").get_data(as_text=True), "a current coach chip is grey, background screening stays in the details, and admins get an Admin chip")
filt = eli.get("/members?coach=eligible").get_data(as_text=True)
ok("Riley Quinn" in filt and ">Coach eligible <" in filt and ">Coaches</a>" in eli.get("/members").get_data(as_text=True) and 'class="chip-info">Coach · expires ' in filt, "People has Coaches and Coach eligible sections")
D.execute("UPDATE members SET usawp_valid_until=? WHERE id=?", (today, riley_id)); D.commit()
soon_chip = eli.get("/members").get_data(as_text=True)
ok('>Coaching</span><span class=v>Coach eligible</span>' in riley.get("/profile").get_data(as_text=True) and ('class="chip-info warn">Coach · expires ' + today) in soon_chip, "a coach membership is still eligible on the day it expires, and the chip turns yellow")
D.execute("UPDATE members SET usawp_valid_until='2027-08-31' WHERE id=?", (riley_id,)); D.commit()
pdate = D.execute("SELECT date FROM practices WHERE id=?", (pid,)).fetchone()[0]
eli.post("/practices", data=dict(base, coach=[str(riley_id)]))
card = eli.get("/practices").get_data(as_text=True).split("id=p%d " % pid, 1)[1].split("id=p")[0]
jane_card = jane.get("/practices").get_data(as_text=True).split("id=p%d " % pid, 1)[1].split("id=p")[0]
elig_page = eli.get("/practices/%d" % pid).get_data(as_text=True)
other_pid = D.execute("SELECT id FROM practices WHERE cancelled=0 AND id!=? ORDER BY date, start LIMIT 1", (pid,)).fetchone()[0]
ok("No assigned coach is coach-eligible" not in card and 'class="st st-ok coach-elig"' not in card and 'class="st st-ok coach-elig"' not in jane_card and "No assigned coach is coach-eligible" not in jane_card and "No assigned coach is coach-eligible" not in eli.get("/practices").get_data(as_text=True) and 'class="st st-ok coach-elig">Coach eligible' in elig_page and "No assigned coach is coach-eligible" not in elig_page and "No coaches assigned." in eli.get("/practices/%d" % other_pid).get_data(as_text=True) and "No assigned coach is coach-eligible" not in eli.get("/practices/%d" % other_pid).get_data(as_text=True), "an eligible assigned coach clears that practice's warning, and an empty coach list has no eligibility warning")
memcsv = {r[3]: r for r in list(csvmod.reader(io_mod.StringIO(eli.get("/members.csv").data.decode("utf-8-sig"))))[1:]}
prows = list(csvmod.reader(io_mod.StringIO(eli.get("/export/practices.csv?start=%s&end=%s" % (pdate, pdate)).data.decode("utf-8-sig"))))
prow = next(r for r in prows[1:] if r[0] == pdate and r[2] == ploc)
with A.app.app_context():
    detail = [r for r in A.practice_sheet_tabs(A.db())[A.SHEET_PRACTICE_COACHES][1:] if r[0] == pdate and r[2] == ploc]
ok(memcsv["riley@example.com"][-3] == "Coach eligible" and memcsv["riley@example.com"][-2] == "" and memcsv["riley@example.com"][-1].startswith("Background screening expires ") and memcsv["jane@example.com"][-3] == "" and memcsv["jane@example.com"][-2] == "" and memcsv["jane@example.com"][-1] == "" and prow[6] == "Riley" and prow[7] == "1" and prow[8] == "1" and detail == [[pdate, "%s-%s" % (pstart, pend), ploc, "Riley Quinn", "riley@example.com", "Coach eligible"]], "Coach eligible and background screening are on the members CSV, and coach eligibility is on the practices CSV and sheet")
D.execute("UPDATE member_reqs SET expires_on=? WHERE member_id=? AND req_id=(SELECT id FROM requirements WHERE keywords LIKE '%background%' LIMIT 1)", (past, riley_id)); D.commit()
expired_coaches = eli.get("/members?view=coaches").get_data(as_text=True)
expired_crow = people_row(expired_coaches, "Riley Quinn")
ok('coach-elig">Coach eligible' not in riley.get("/profile").get_data(as_text=True) and ("Coach eligibility expired " + past) in riley.get("/profile").get_data(as_text=True) and ('class="chip-info bad">Coach · expires ' + past) in eli.get("/members").get_data(as_text=True) and ('class="chip-info bad">Coach · expires ' + past) in expired_crow and "Coach eligible" not in expired_crow and "Background screening expires" not in expired_crow and D.execute("SELECT 1 FROM coaching_list WHERE member_id=?", (riley_id,)).fetchone(), "an expired background screening shows Coach eligibility expired and keeps the coaching list")
D.execute("UPDATE member_reqs SET expires_on=? WHERE member_id=? AND req_id IN (SELECT id FROM requirements WHERE keywords LIKE '%background%' OR keywords LIKE '%safesport%')", (today, riley_id)); D.commit()
ok('>Coaching</span><span class=v>Coach eligible</span>' in riley.get("/profile").get_data(as_text=True) and "Coach eligibility expired" not in riley.get("/home").get_data(as_text=True), "background and SafeSport are current on the expiry date itself")
D.execute("UPDATE member_reqs SET expires_on=? WHERE member_id=? AND req_id=(SELECT id FROM requirements WHERE keywords LIKE '%safesport%' LIMIT 1)", (past, riley_id)); D.commit()
ok('coach-elig">Coach eligible' not in riley.get("/home").get_data(as_text=True) and ("Coach eligibility expired " + past) in eli.get("/admin/member/%d" % riley_id).get_data(as_text=True), "an expired SafeSport date shows Coach eligibility expired on the member page")
D.execute("UPDATE member_reqs SET expires_on=? WHERE member_id=? AND req_id=(SELECT id FROM requirements WHERE keywords LIKE '%safesport%' LIMIT 1)", (future, riley_id)); D.commit()
answer(True, membership_type="Athlete")
ok(not D.execute("SELECT 1 FROM coaching_list WHERE member_id=?", (riley_id,)).fetchone() and 'class="st st-ok coach-elig"' not in riley.get("/home").get_data(as_text=True) and 'class="st st-bad coach-elig"' not in riley.get("/home").get_data(as_text=True) and ('name=coach value="%d"' % riley_id) not in eli.get("/practices/%d" % pid).get_data(as_text=True), "a verified athlete membership removes the USAWP coaching-list row")
list_act(riley_id, "add_coaching")
ok(('name=coach value="%d"' % riley_id) in eli.get("/practices/%d" % pid).get_data(as_text=True) and 'class="st st-ok coach-elig"' not in riley.get("/home").get_data(as_text=True) and 'class="st st-bad coach-elig"' not in riley.get("/home").get_data(as_text=True) and 'class="st st-ok coach-elig"' not in eli.get("/admins").get_data(as_text=True) and riley.get("/chat?c=coaches").status_code == 403, "a manual add is on the picker with no badge and no coach access")
answer(True, member_number="424242")
ok(D.execute("SELECT source FROM coaching_list WHERE member_id=?", (riley_id,)).fetchone()[0] == "manual", "a verification with no membership type leaves the coaching list alone")
import io
athlete = ("First Name,Last Name,Email,Status,Valid Until,Membership Type\nRiley,Quinn,riley@example.com,Current,2027-08-31,Athlete\n").encode()
eli.post("/import", data=dict(csrf=csrf(eli, "/transfer"), file=(io.BytesIO(athlete), "t.csv")), content_type="multipart/form-data")
ok(D.execute("SELECT source FROM coaching_list WHERE member_id=?", (riley_id,)).fetchone()[0] == "manual" and D.execute("SELECT membership_type FROM members WHERE id=?", (riley_id,)).fetchone()[0] == "Athlete", "an athlete import does not remove a manual coaching-list row")
coach_csv = ("First Name,Last Name,Email,Status,Valid Until,Member Type\nRiley,Quinn,riley@example.com,Current,2027-08-31,Head Coach\n").encode()
eli.post("/import", data=dict(csrf=csrf(eli, "/transfer"), file=(io.BytesIO(coach_csv), "t.csv")), content_type="multipart/form-data")
ok(D.execute("SELECT source FROM coaching_list WHERE member_id=?", (riley_id,)).fetchone()[0] == "usawp" and D.execute("SELECT membership_type FROM members WHERE id=?", (riley_id,)).fetchone()[0] == "Head Coach" and '>Coaching</span><span class=v>Coach eligible</span>' in riley.get("/profile").get_data(as_text=True), "a coach membership import adds the USAWP coaching-list row and the badge")
list_act(riley_id, "remove_coaching")
ok(not D.execute("SELECT 1 FROM coaching_list WHERE member_id=?", (riley_id,)).fetchone() and ('name=coach value="%d"' % riley_id) not in eli.get("/practices/%d" % pid).get_data(as_text=True), "an admin can remove a USAWP coach from the coaching list")
answer(True, membership_type="Individual Membership, Coach")
ok(D.execute("SELECT source FROM coaching_list WHERE member_id=?", (riley_id,)).fetchone()[0] == "usawp" and riley.get("/admin").status_code == 403, "the next coach verification puts them back on the list without coach access")
una = A.app.test_client(); join(una, "Una", "Noverified", "una.noverified@example.com")
D.commit(); una_id = D.execute("SELECT id FROM members WHERE email='una.noverified@example.com'").fetchone()[0]
chunk = people_row(eli.get("/members").get_data(as_text=True), "Una Noverified")
ok(D.execute("SELECT usawp_status FROM members WHERE id=?", (una_id,)).fetchone()[0] == "unknown" and "Add to coaches" in chunk and "Make admin" in chunk and "Add to referees" in chunk, "People offers coaches, referees, and admin actions before USAWP is verified")
list_act(una_id, "make_coach"); list_act(una_id, "make_admin")
ok(D.execute("SELECT role, is_admin, usawp_status FROM members WHERE id=?", (una_id,)).fetchone() == ("coach", 1, "unknown") and una.get("/admin").status_code == 200 and una.get("/chat?c=coaches").status_code == 200 and una.get("/members").status_code == 200, "Make coach and Make admin work for a member who is not USAWP verified")
list_act(una_id, "remove_admin"); list_act(una_id, "remove_coach")
ok(D.execute("SELECT role, is_admin, usawp_status FROM members WHERE id=?", (una_id,)).fetchone() == ("athlete", 0, "unknown") and una.get("/admin").status_code == 403 and una.get("/chat?c=coaches").status_code == 403, "Remove admin and Remove coach do not depend on USAWP status")
ned = A.app.test_client(); join(ned, "Ned", "List", "ned.list@example.com")
D.commit(); ned_id = D.execute("SELECT id FROM members WHERE email='ned.list@example.com'").fetchone()[0]
ok("Add to coaches" in eli.get("/members").get_data(as_text=True) and "Make active coach" in eli.get("/members?view=coaches").get_data(as_text=True) and ("name=coach value=\"%d\"" % ned_id) not in eli.get("/practices/%d" % pid).get_data(as_text=True) and ned.post("/members", data=dict(csrf=csrf(ned, "/home"), member_id=ned_id, action="make_coach")).status_code == 403, "People offers Add to coaches, and that person is not assignable yet")
made = eli.post("/members", data=dict(csrf=csrf(eli, "/members"), member_id=ned_id, action="make_coach"), follow_redirects=True).get_data(as_text=True)
ned_row = people_row(made, "Ned List")
ok('class="toast noprint" role=status>Ned List is now an active coach.' in made and D.execute("SELECT role FROM members WHERE id=?", (ned_id,)).fetchone()[0] == "coach" and not D.execute("SELECT 1 FROM coaching_list WHERE member_id=?", (ned_id,)).fetchone() and ("name=coach value=\"%d\"" % ned_id) not in eli.get("/practices/%d" % pid).get_data(as_text=True) and 'class="chip-info bad">Coach</span>' in ned_row and "Active coach" not in ned_row and "Remove active coach" in eli.get("/members?view=coaches").get_data(as_text=True) and ("name=coach value=\"%d\"" % eli_id) in eli.get("/practices/%d" % pid).get_data(as_text=True) and ned.get("/chat?c=coaches").status_code == 200 and ned.get("/admin").status_code == 200, "Make active coach grants access without the coaching list")

# assigned coaches in the practices CSV and the Google Sheet tabs
D.execute("INSERT INTO coaching_list(member_id, source, at) VALUES(?, 'manual', '2026-10-01') ON CONFLICT(member_id) DO UPDATE SET source='manual'", (eli_id,))
D.execute("INSERT INTO coaching_list(member_id, source, at) VALUES(?, 'manual', '2026-10-01') ON CONFLICT(member_id) DO UPDATE SET source='manual'", (john_id,))
D.execute("DELETE FROM coaching_list WHERE member_id=?", (jane_id,))
D.commit()
epid, estart, eend, eloc, enote = D.execute("SELECT id, start, end, location, COALESCE(note,'') FROM practices WHERE date='2026-12-01' AND location='Export Pool'").fetchone()
pushed = []
real_push = A.push_sheet_tabs
A.push_sheet_tabs = lambda tabs: pushed.append({k: [list(row) for row in rows] for k, rows in tabs.items()}) or True
def export_edit(ids):
    return eli.post("/practices", data=dict(csrf=csrf(eli, "/practices"), pid=epid, action="edit", start=estart, end=eend, location=eloc, note=enote, coach=ids))
export_edit([str(eli_id), str(john_id), str(jane_id)])
sheet = pushed[-1]
srow = next(r for r in sheet["Practices"][1:] if r[0] == "2026-12-01" and r[2] == "Export Pool")
detail = [r for r in sheet["Practice Coaches"][1:] if r[0] == "2026-12-01" and r[2] == "Export Pool"]
csv_row = {r[0]: r for r in list(csvmod.reader(io_mod.StringIO(eli.get("/export/practices.csv?start=2026-12-01&end=2026-12-01").data.decode("utf-8-sig"))))[1:]}["2026-12-01"]
ok(sheet["Practices"][0] == A.PRACTICE_CSV_HEADER and srow[6] == "Eli, Sam" and srow[7] == 2 and srow[8] == 0 and csv_row[6:8] == ["Eli, Sam", "2"] and csv_row[8] == "0" and "Jane" not in srow[6], "Practices tab and CSV list the assigned coaches and the count")
ok(sheet["Practice Coaches"][0] == A.PRACTICE_COACHES_HEADER and detail == [["2026-12-01", "18:00-19:30", "Export Pool", "Eli Joern", "eli@example.com", ""], ["2026-12-01", "18:00-19:30", "Export Pool", "Sam Smith", "john@example.com", ""]], "Practice Coaches is one row per coach with name and email")
mrow = next(r for r in sheet["Members"][1:] if r[3] == "exa.export@example.com")
eli_sheet = next(r for r in sheet["Members"][1:] if r[3] == "eli@example.com")
john_sheet = next(r for r in sheet["Members"][1:] if r[3] == "john@example.com")
ok(sheet["Members"][0] == A.MEMBERS_CSV_HEADER and mrow[11] == "2028-01-15" and mrow[-1] == "Background screening expires 2028-01-15" and eli_sheet[-1] == "Background screening missing" and john_sheet[-1] == "Background screening expires 2027-03-01", "Members sheet includes a coach's background screening line, and an active coach with no date shows missing")
att = next(r for r in sheet["Attendance"][1:] if r[0] == "2026-12-01" and r[2] == "Export Pool" and r[4] == "Ex Export")
ok(sheet["Attendance"][0] == A.ATTENDANCE_CSV_HEADER and att[6] == "going" and att[7] == "yes", "Attendance sheet is one row per member per practice")
export_edit([str(john_id)])
changed = next(r for r in pushed[-1]["Practices"][1:] if r[0] == "2026-12-01" and r[2] == "Export Pool")
changed_detail = [r for r in pushed[-1]["Practice Coaches"][1:] if r[0] == "2026-12-01" and r[2] == "Export Pool"]
ok(changed[6] == "Sam" and changed[7] == 1 and changed_detail == [["2026-12-01", "18:00-19:30", "Export Pool", "Sam Smith", "john@example.com", ""]], "changing the assigned coaches rewrites the sheet")
before = len(pushed)
D.execute("UPDATE members SET role='athlete' WHERE id=?", (john_id,)); D.commit()
list_act(john_id, "remove_coaching")
dropped = next(r for r in pushed[-1]["Practices"][1:] if r[0] == "2026-12-01" and r[2] == "Export Pool")
ok(len(pushed) > before and dropped[6] == "" and dropped[7] == 0 and not any(r[0] == "2026-12-01" and r[2] == "Export Pool" for r in pushed[-1]["Practice Coaches"][1:]) and D.execute("SELECT member_id FROM practice_coaches WHERE practice_id=? AND member_id=?", (epid, john_id)).fetchone(), "leaving the coaching list resyncs the sheet and drops that coach")
def boom(tabs):
    raise RuntimeError("sheet down")
A.push_sheet_tabs = boom
saved = export_edit([str(eli_id)])
ok(saved.status_code == 302 and D.execute("SELECT member_id FROM practice_coaches WHERE practice_id=?", (epid,)).fetchall() == [(eli_id,)], "a Google Sheet error still saves the coach assignment")
A.push_sheet_tabs = real_push
ok(A.push_sheet_tabs({A.SHEET_PRACTICES: [["Date"]]}) is False and "Sync to Google Sheet now" not in eli.get("/transfer").get_data(as_text=True), "sheet sync and the admin button stay hidden until GOOGLE_SA_JSON and GOOGLE_SHEET_ID are set")
class FakeSheet:
    def __init__(self, title):
        self.title = title; self.cleared = 0; self.values = None
    def clear(self): self.cleared += 1
    def update(self, values, range_name=None, value_input_option=None): self.values = values
class FakeBook:
    def __init__(self): self.by = {"Practices": FakeSheet("Practices")}
    def worksheet(self, title):
        if title not in self.by: raise A.gspread.WorksheetNotFound(title)
        return self.by[title]
    def add_worksheet(self, title, rows=1, cols=1):
        self.by[title] = FakeSheet(title); return self.by[title]
book = FakeBook()
os.environ["GOOGLE_SHEET_ID"] = "sheet123"
os.environ["GOOGLE_SA_JSON"] = A.json.dumps({"type": "service_account", "client_email": "sheet@test.iam.gserviceaccount.com", "private_key": "not-used", "token_uri": "https://oauth2.googleapis.com/token"})
real_open = A.open_spreadsheet
A.open_spreadsheet = lambda: book
try:
    wrote = A.push_sheet_tabs({A.SHEET_PRACTICES: [A.PRACTICE_CSV_HEADER, ["2026-12-01", "18:00-19:30", "Export Pool", "no", 1, 1, "Eli, Sam", 2]], A.SHEET_ATTENDANCE: [A.ATTENDANCE_CSV_HEADER, ["2026-12-01", "18:00-19:30", "Export Pool", "no", "Ex Export", "1", "going", "yes", ""]]})
    D.execute("DELETE FROM sheet_sync"); D.commit()
    page = eli.get("/transfer").get_data(as_text=True)
    ok(wrote is True and book.by["Practices"].cleared == 1 and book.by["Practices"].values[0] == A.PRACTICE_CSV_HEADER and book.by["Attendance"].title == "Attendance" and "Sync to Google Sheet now" in page and "Not synced yet" in page, "gspread creates a missing Attendance tab and the admin sync card appears")
    A.run_sheet_sync = lambda: A.save_sheet_status(True, "Synced")
    done = eli.post("/export/sheet", data=dict(csrf=csrf(eli, "/transfer")), follow_redirects=True).get_data(as_text=True)
    ok('class="toast noprint" role=status>Google Sheet synced.' in done and "Last sync" in done and "Synced" in done, "Sync to Google Sheet now records the time and status")
finally:
    A.open_spreadsheet = real_open
    os.environ.pop("GOOGLE_SHEET_ID", None); os.environ.pop("GOOGLE_SA_JSON", None)
hits = []
real_run = A.run_sheet_sync
A.run_sheet_sync = lambda: hits.append(1)
A.SHEET_DEBOUNCE_SEC = 0.05
os.environ["GRUNIONS_SHEET_SYNC"] = "debounce"
os.environ["GOOGLE_SHEET_ID"] = "sheet123"
os.environ["GOOGLE_SA_JSON"] = A.json.dumps({"client_email": "sheet@test.iam.gserviceaccount.com", "private_key": "x"})
try:
    A.schedule_sheet_sync(); A.schedule_sheet_sync()
    import time as time_mod; time_mod.sleep(0.25)
    ok(hits == [1] and any(j.id == "sheet_daily" for j in A._scheduler.get_jobs()), "sheet updates are debounced, and a daily resync is scheduled")
finally:
    A.run_sheet_sync = real_run
    A.SHEET_DEBOUNCE_SEC = 2.0
    os.environ["GRUNIONS_SHEET_SYNC"] = "inline"
    os.environ.pop("GOOGLE_SHEET_ID", None); os.environ.pop("GOOGLE_SA_JSON", None)
    if A._sheet_timer is not None: A._sheet_timer.cancel()

bea = A.app.test_client(); join(bea, "Bea", "Player", "bea.player@example.com")
bea_id = D.execute("SELECT id FROM members WHERE email='bea.player@example.com'").fetchone()[0]
D.execute("UPDATE members SET usawp_status='verified', usawp_valid_until=?, usawp_number='7771001' WHERE id=?", ((A.today_pt() + dt.timedelta(days=200)).isoformat(), bea_id))
D.execute("INSERT INTO member_reqs(member_id,req_id,completed_on,expires_on,source,by,at) VALUES(?,?,NULL,?,'test','test','2026-01-01')", (bea_id, ssid, (A.today_pt() + dt.timedelta(days=200)).isoformat()))
D.commit()
D.execute("UPDATE members SET require_background=1 WHERE id=?", (bea_id,)); D.commit()
bea_home = bea.get("/home").get_data(as_text=True)
members_html = eli.get("/members").get_data(as_text=True)
ok('class="dot ok"' in bea_home and '<span class=rowtitle><span class="dot ok" aria-hidden=true></span>SafeSport training</span><span class=v>expires ' in bea.get("/profile").get_data(as_text=True) and "Background screening" not in bea_home and "Not cleared to coach" not in bea_home and "Require background" not in members_html and "Don't require background" not in members_html, "a player is cleared without background screening, and the members menu has no Require background item")
denied = eli.post("/members", data=dict(csrf=csrf(eli, "/members"), member_id=bea_id, action="require_background"), follow_redirects=True)
ok(denied.status_code == 400 and 'class="dot ok"' in bea.get("/home").get_data(as_text=True) and D.execute("SELECT require_background FROM members WHERE id=?", (bea_id,)).fetchone()[0] == 1, "Require background is not an action and leaves the stored flag unused")
made_coach = eli.post("/members", data=dict(csrf=csrf(eli, "/members"), member_id=bea_id, action="make_coach"), follow_redirects=True).get_data(as_text=True)
bea_row = people_row(made_coach, "Bea Player")
bea_detail = eli.get("/admin/member/%d" % bea_id).get_data(as_text=True)
as_coach = bea.get("/profile").get_data(as_text=True)
coach_csv = {r[3]: r for r in list(csvmod.reader(io_mod.StringIO(eli.get("/members.csv").data.decode("utf-8-sig"))))[1:]}
eli.post("/members", data=dict(csrf=csrf(eli, "/members"), member_id=bea_id, action="remove_coach"), follow_redirects=True)
as_player = bea.get("/profile").get_data(as_text=True)
player_csv = {r[3]: r for r in list(csvmod.reader(io_mod.StringIO(eli.get("/members.csv").data.decode("utf-8-sig"))))[1:]}
ok('<span class=rowtitle><span class="dot ok" aria-hidden=true></span>SafeSport training</span><span class=v>expires ' in as_coach and "Not cleared to coach" in as_coach and '<span class=rowtitle><span class="dot bad" aria-hidden=true></span>Background screening</span><span class=v>missing</span>' in as_coach and "Background screening missing" not in bea_row and '<span class=rowtitle><span class="dot" aria-hidden=true></span>Background screening</span><span class=v>Not on file</span>' in bea_detail and coach_csv["bea.player@example.com"][-1] == "Background screening missing" and "Not cleared to coach" not in as_player and "Background screening" not in as_player and '<span class=rowtitle><span class="dot ok" aria-hidden=true></span>SafeSport training</span><span class=v>expires ' in as_player and player_csv["bea.player@example.com"][-1] == "", "Make coach requires background screening, and Remove coach drops that requirement")
week = (A.today_pt() + dt.timedelta(days=7)).isoformat()
bg_req = D.execute("SELECT id FROM requirements WHERE lower(keywords) LIKE '%background%'").fetchone()[0]
casey_mid = D.execute("SELECT id FROM members WHERE email='casey@example.com'").fetchone()[0]
D.execute("INSERT INTO member_reqs(member_id,req_id,completed_on,expires_on,source,by,at) VALUES(?,?,NULL,?,'test','test','2026-01-01')", (bea_id, bg_req, week))
D.execute("UPDATE member_reqs SET expires_on=? WHERE member_id=? AND req_id=?", (week, casey_mid, bg_req))
D.execute("UPDATE members SET email_reminders=1 WHERE id IN (?,?)", (bea_id, casey_mid)); D.commit()
pushsub(bea, "https://push.example/bea"); pushsub(casey, "https://push.example/casey")
emails.clear(); pushes.clear()
nd = A.open_db()
try: A.run_expiry_notices(nd)
finally: nd.close()
bg_player = [e for e in emails if e[0] == "bea.player@example.com" and "background" in e[1].lower()]
bg_coach = [e for e in emails if e[0] == "casey@example.com" and "background" in e[1].lower()]
casey_id_push = D.execute("SELECT id FROM members WHERE email='casey@example.com'").fetchone()[0]
ok(bg_player == [] and len(bg_coach) == 1 and "in 7 days" in bg_coach[0][2] and "/home" in bg_coach[0][2] and any(p[0] == casey_id_push and p[1]["url"] == "/home" and "background screening" in p[1]["body"].lower() for p in pushes) and not any(p[0] == bea_id and "background" in (p[1].get("body") or "").lower() for p in pushes), "background screening sends the 7-day email and push to a coach only")
past_day = (A.today_pt() - dt.timedelta(days=1)).isoformat()
D.execute("UPDATE member_reqs SET expires_on=? WHERE member_id=? AND req_id=?", (past_day, bea_id, bg_req))
D.execute("UPDATE member_reqs SET expires_on=? WHERE member_id=? AND req_id=?", (past_day, casey_mid, bg_req)); D.commit()
emails.clear(); pushes.clear()
nd = A.open_db()
try: A.run_expiry_notices(nd); A.run_expiry_notices(nd)
finally: nd.close()
expired_mail = [e for e in emails if e[0] == "casey@example.com" and e[1] == "Background screening expired"]
ok(len(expired_mail) == 1 and "expired on" in expired_mail[0][2] and not any(e[0] == "bea.player@example.com" and "background" in e[1].lower() for e in emails), "an expired background screening emails the coach once and does not email a player")
D.execute("UPDATE member_reqs SET expires_on=? WHERE member_id=? AND req_id=?", (far_bg, casey_mid, bg_req)); D.commit()

def nav_skeleton(html):
    nav = re.search(r'<nav class="tabs noprint".*?</nav>', html, re.S).group(0)
    nav = re.sub(r' class="on"', "", nav)
    nav = re.sub(r' aria-current=page', "", nav)
    nav = re.sub(r' class=""', "", nav)
    nav = re.sub(r'\sdata-total="[^"]*"', "", nav)
    return re.sub(r"<span class=badge>[^<]*</span>", "", nav)
eli_pages = [eli.get(p).get_data(as_text=True) for p in ("/home", "/practices", "/chat", "/admin", "/members")]
jane_pages = [jane.get(p).get_data(as_text=True) for p in ("/home", "/practices", "/chat")]
login_html = client().get("/login").get_data(as_text=True)
ok(len({nav_skeleton(h) for h in eli_pages}) == 1 and "href=/admin" in nav_skeleton(eli_pages[0]), "staff bottom nav markup matches on home, schedule, chat, and admin")
ok(len({nav_skeleton(h) for h in jane_pages}) == 1 and "href=/admin" not in nav_skeleton(jane_pages[0]) and "href=/home" in nav_skeleton(jane_pages[0]), "member bottom nav markup matches and has no admin tab")
ok("color-scheme:dark" in eli_pages[0][:600] and "content=dark" in eli_pages[0][:600] and "#090D0B" in eli_pages[0][:600] and '<body style="background:#090D0B' in eli_pages[0] and "color-scheme:dark" in login_html[:600] and "#090D0B" in login_html[:600], "dark background is in the first bytes, including the login page")
ok("input,select,textarea{" in eli_pages[0] and "color-scheme:dark" in eli_pages[0].split("input,select,textarea{", 1)[1][:400] and "input[type=date]::-webkit-calendar-picker-indicator" in eli_pages[0] and "input[type=time]::-webkit-calendar-picker-indicator" in eli_pages[0] and "%23F2F6F1" in eli_pages[0] and "font-display:swap" in eli_pages[0] and "Space Grotesk" in eli_pages[0] and "Plus Jakarta Sans" in eli_pages[0], "date and time icons use the input text color")
ok("@view-transition{navigation:auto}" in eli_pages[0] and "::view-transition-old(root)" in eli_pages[0] and "animation-duration:0s" in eli_pages[0] and "view-transition-name:grunions-nav" in eli_pages[0] and "contain:layout paint" not in eli_pages[0] and "replaceChildren" in eli_pages[0] and "bottom:calc(var(--nav-offset-bottom) + env(safe-area-inset-bottom))" in eli_pages[0] and "--nav-offset-bottom: 24px" in eli_pages[0] and "--nav-circle: 52px" in eli_pages[0] and "ico-fill" in eli_pages[0] and 'width="24" height="24"' in eli_pages[0] and "function grunionsGo(" in eli_pages[0] and "function grunionsApply(" in eli_pages[0] and "rel=stylesheet" not in eli_pages[0] and "rel=stylesheet" not in login_html and "--nav-glass-bg:" in eli_pages[0] and "-webkit-backdrop-filter:var(--nav-glass-blur)" in eli_pages[0] and "prefers-reduced-transparency:reduce" in eli_pages[0], "nav stays put across tab changes without a crossfade flicker")

dec = A.checkin_month("2026-12-04", ["2026-12-04"])
ok(A.default_checkin_date(["2026-10-20", "2026-10-23"], dt.date(2026, 10, 23)) == "2026-10-23" and A.default_checkin_date(["2026-10-20", "2026-10-23"], dt.date(2026, 10, 19)) == "2026-10-20" and A.default_checkin_date(["2026-10-16"], dt.date(2026, 10, 23)) == "2026-10-16" and A.default_checkin_date([], dt.date(2026, 10, 23)) == "2026-10-23" and A.neighbor_practice(["2026-10-20", "2026-10-23"], "2026-10-21", -1) == "2026-10-20" and A.neighbor_practice(["2026-10-20", "2026-10-23"], "2026-10-21", 1) == "2026-10-23" and A.neighbor_practice(["2026-10-20", "2026-10-23"], "2026-10-23", 1) is None and dec["label"] == "December 2026" and dec["cells"][0] is None and dec["cells"][2]["day"] == 1 and dec["cells"][5]["on"] and dec["cells"][5]["has"], "check-in picks today's practice, otherwise the next one, and lays the month out from Sunday")
real_now = A.now_pt
try:
    A.now_pt = lambda: dt.datetime(2026, 10, 19, 19, 0, tzinfo=dt.timezone.utc)  # Monday noon Pacific
    D.execute("INSERT INTO practices(date,start,end,location,cancelled) VALUES('2026-10-16','19:00','20:30','Past Pool',0)")
    D.execute("INSERT INTO practices(date,start,end,location,cancelled) VALUES('2026-10-21','19:00','20:30','Cancelled Only Pool',1)")
    D.commit()
    adm = eli.get("/admin").get_data(as_text=True)
    days = [r[0] for r in D.execute("SELECT DISTINCT date FROM practices WHERE cancelled=0 ORDER BY date").fetchall()]
    i = days.index("2026-10-20")
    prev_d = days[i - 1] if i else None
    next_d = days[i + 1] if i + 1 < len(days) else None
    grid = adm.split("id=calGrid", 1)[1].split("</div>", 1)[0]
    ok('value="2026-10-20"' in adm and "id=calPick" in adm and "id=calPop" in adm and "class=matpick" in adm and ">Select date<" in adm and ">Cancel</button>" in adm and ">OK</button>" in adm and "class=botsheet" not in adm.split("id=calPop",1)[0] and "calpop" not in adm and 'fill="currentColor"' in adm and "span.calday{color:var(--t3)" in adm and "border-radius:50%" in adm and not re.search(r"<input[^>]*type=date[^>]*name=date|<input[^>]*name=date[^>]*type=date", adm), "check-in opens a centered date dialog on the next practice when today has none")
    ok('aria-disabled=true>19</span>' in grid and 'aria-disabled=true>21</span>' in grid and 'class="calday on" href="/admin?date=2026-10-20"' in grid and 'href="/admin?date=2026-10-16"' in grid and "2026-10-21" not in grid and ('date=%s' % prev_d) in adm and 'aria-label="Previous event"' in adm and ('date=%s' % next_d) in adm and 'aria-label="Next event"' in adm, "only practice days are selectable, including past ones, and the arrows use those days")
    kept = eli.get("/admin?date=2026-10-23&q=Jane").get_data(as_text=True)
    odd = eli.get("/admin?date=2026-10-19").get_data(as_text=True)
    ok('value="2026-10-23"' in kept and 'value="Jane"' in kept and "date=2026-10-20" in kept and "q=Jane" in kept and 'value="2026-10-19"' in odd and "No events on this day" in odd and "id=calPop" in odd and ">Select date<" in odd and "Mon, Oct 19" in odd, "a chosen date stays put, and practice links keep the search")
finally:
    A.now_pt = real_now

# members list role menu
ada = A.app.test_client(); join(ada, "Ada", "Role", "ada.role@example.com")
ada_id = D.execute("SELECT id FROM members WHERE email='ada.role@example.com'").fetchone()[0]
menu_page = eli.get("/members").get_data(as_text=True)
ada_menu = people_row(menu_page, "Ada Role")
eli_menu = people_row(menu_page, "Eli Joern")
ok('class=morebtn' in ada_menu and "M140,128a12,12,0,1,1-12-12A12" in ada_menu and "Make admin" in ada_menu and "Add to coaches" in ada_menu and "Add to referees" in ada_menu and "Make active coach" not in ada_menu and "Remove admin" not in ada_menu and ">Remove admin</button>" in eli_menu and "disabled" in eli_menu, "each member has a three-dots menu with admin, coaches, and referees")
promoted = eli.post("/members", data=dict(csrf=csrf(eli, "/members"), member_id=ada_id, action="make_admin"), follow_redirects=True).get_data(as_text=True)
ok('class="toast noprint" role=status>Ada Role is now an admin.' in promoted and D.execute("SELECT is_admin FROM members WHERE id=?", (ada_id,)).fetchone()[0] == 1, "Make admin from the members menu confirms with a toast")
listed = eli.post("/members", data=dict(csrf=csrf(eli, "/members"), member_id=ada_id, action="add_coaching"), follow_redirects=True).get_data(as_text=True)
ok('class="toast noprint" role=status>Ada Role was added to coaches.' in listed and D.execute("SELECT source FROM coaching_list WHERE member_id=?", (ada_id,)).fetchone()[0] == "manual", "Add to coaches from the members menu confirms with a toast")
stays = eli.post("/members", data=dict(csrf=csrf(eli, "/members"), member_id=ada_id, action="remove_coaching"), follow_redirects=True).get_data(as_text=True)
ok('class="toast noprint" role=status>Ada Role was removed from coaches.' in stays and not D.execute("SELECT 1 FROM coaching_list WHERE member_id=?", (ada_id,)).fetchone(), "an admin can be removed from coaches")
demoted = eli.post("/members", data=dict(csrf=csrf(eli, "/members"), member_id=ada_id, action="remove_admin"), follow_redirects=True).get_data(as_text=True)
ok('class="toast noprint" role=status>Ada Role is no longer an admin.' in demoted and D.execute("SELECT is_admin FROM members WHERE id=?", (ada_id,)).fetchone()[0] == 0, "Remove admin works when another admin remains")
eli.post("/members", data=dict(csrf=csrf(eli, "/members"), member_id=ada_id, action="add_coaching"))
unlisted = eli.post("/members", data=dict(csrf=csrf(eli, "/members"), member_id=ada_id, action="remove_coaching"), follow_redirects=True).get_data(as_text=True)
ok('class="toast noprint" role=status>Ada Role was removed from coaches.' in unlisted and not D.execute("SELECT 1 FROM coaching_list WHERE member_id=?", (ada_id,)).fetchone(), "Remove from coaches from the members menu confirms with a toast")
others = [r[0] for r in D.execute("SELECT id FROM members WHERE is_admin=1 AND id!=?", (eli_id,)).fetchall()]
D.execute("UPDATE members SET is_admin=0 WHERE id!=?", (eli_id,)); D.commit()
blocked = eli.post("/members", data=dict(csrf=csrf(eli, "/members"), member_id=eli_id, action="remove_admin"), follow_redirects=True).get_data(as_text=True)
ok('class="toast noprint" role=status>The last admin cannot be removed.' in blocked and D.execute("SELECT is_admin FROM members WHERE id=?", (eli_id,)).fetchone()[0] == 1, "the last admin cannot remove their own admin role")
for oid in others: D.execute("UPDATE members SET is_admin=1 WHERE id=?", (oid,))
D.commit()

# Referee eligible follows Coach eligible: verification sets it, and it shows on Members, check-in, and the sheet.
ok(A.is_referee_membership("Referee") and A.is_referee_membership("Individual Membership, Referee") and A.is_referee_membership("Head Referee") and not A.is_referee_membership("referees") and not A.is_referee_membership("Coach") and not A.is_referee_membership(""), "referee membership matches the word referee only")
rae = A.app.test_client(); join(rae, "Rae", "Fern", "rae.fern@example.com")
rae_id = D.execute("SELECT id FROM members WHERE email='rae.fern@example.com'").fetchone()[0]
ref_future = (A.today_pt() + dt.timedelta(days=40)).isoformat()
ref_past = (A.today_pt() - dt.timedelta(days=1)).isoformat()
bgid = D.execute("SELECT id FROM requirements WHERE lower(keywords) LIKE '%background%'").fetchone()[0]
D.execute("INSERT INTO verify_requests(member_id,name,email,status,created) VALUES(?,?,?,'pending',?)", (rae_id, "Rae Fern", "rae.fern@example.com", A.today_pt().isoformat()))
D.commit()
ref_vid = D.execute("SELECT id FROM verify_requests WHERE member_id=? AND status='pending' ORDER BY id DESC LIMIT 1", (rae_id,)).fetchone()[0]
c0.post("/api/verify-requests/%d/result" % ref_vid, headers=H, json={"verified": True, "member_number": "9090909", "membership_type": "Referee", "membership_expires_on": ref_future, "compliance": {"SafeSport training": ref_future, "Background screening": ref_future}})
ref_members = eli.get("/members").get_data(as_text=True)
rae_row = people_row(ref_members, "Rae Fern")
ref_filt = eli.get("/members?referee=eligible").get_data(as_text=True)
ref_csv = {r[3]: r for r in list(csvmod.reader(io_mod.StringIO(eli.get("/members.csv").data.decode("utf-8-sig"))))[1:]}
checkin_ref = eli.get("/admin").get_data(as_text=True)
ok('class="st st-ok ref-elig">Referee eligible' in rae_row and "Coach eligible" not in rae_row and "Rae Fern" in ref_filt and "Jane Doe" not in ref_filt and "Riley Quinn" not in ref_filt and ">Referees</a>" in ref_members and 'class="st st-ok ref-elig">Referee eligible' in eli.get("/admin/member/%d" % rae_id).get_data(as_text=True) and ref_csv["rae.fern@example.com"][-2] == "Referee eligible" and ref_csv["jane@example.com"][-2] == "" and "Referee eligible" not in rae.get("/home").get_data(as_text=True), "a referee verification shows Referee eligible on Members, the filter, check-in, and the sheet")
D.execute("UPDATE member_reqs SET expires_on=? WHERE member_id=? AND req_id=?", (ref_past, rae_id, bgid)); D.commit()
expired_row = eli.get("/members").get_data(as_text=True)
rae_exp_row = people_row(expired_row, "Rae Fern")
lapsed = "Referee eligibility expired " + ref_past
lapsed_csv = {r[3]: r for r in list(csvmod.reader(io_mod.StringIO(eli.get("/members.csv").data.decode("utf-8-sig"))))[1:]}
ok(('class="st st-bad ref-elig">' + lapsed) in rae_exp_row and 'class="st st-ok ref-elig"' not in rae_exp_row and ("Referee eligibility expired " + A.fmt_long(ref_past)) in eli.get("/admin/member/%d" % rae_id).get_data(as_text=True) and lapsed_csv["rae.fern@example.com"][-2] == lapsed and "Rae Fern" not in eli.get("/members?referee=eligible").get_data(as_text=True), "a lapsed referee certification is marked on Members, check-in, and the sheet")
mem_panel = eli.get("/members").get_data(as_text=True)
adm_panel = eli.get("/admin").get_data(as_text=True)
jane_page = eli.get("/admin/member/%d" % jane_id).get_data(as_text=True)
coach_page = casey.get("/admin/member/%d" % jane_id)
jane_cred = '<span class=rowtitle><span class="dot warn" aria-hidden=true></span>USAWP # 1234567</span><span class=v>' + A.fmt_long(soon) + '</span>'
ok("Member # / expires" not in jane_page and jane_cred in jane_page and "Preferred first name" in jane_page and "name=preferred_first" in jane_page and "name=number" in jane_page and "<span>RSVP</span>" not in jane_page and "<span>Eligibility</span>" not in jane_page and "Save background screening" not in jane_page and "Save Sport:80 result" not in jane_page and ">Recheck</button>" in jane_page and ">Edit</button>" in jane_page and ">Ask Grunions to verify</button>" in jane_page and "class=panel" not in mem_panel and "class=panel" not in adm_panel and "nextElementSibling.toggleAttribute('hidden')" not in mem_panel and "nextElementSibling.toggleAttribute('hidden')" not in adm_panel and ('href="/admin/member/%d"' % jane_id) in mem_panel and ('href="/admin/member/%d"' % jane_id) in adm_panel and "bot answered" not in adm_panel and "verification requested" not in adm_panel and ">Cleared<" in adm_panel and jane.get("/admin/member/%d" % jane_id).status_code == 403 and coach_page.status_code == 200 and "id=profileEdit" not in coach_page.get_data(as_text=True), "a person opens a member page, check-in keeps its status on the row, and a member cannot open it")
ana_row = people_row(mem_panel, "Ana Lopez")
ok('class="avatar ciav"' in ana_row and ana_row.find(">Ana Lopez<") < ana_row.find('class="psub ell') and "thru " in ana_row and "ana@example.com" not in ana_row and "legal " not in ana_row and "practices" not in ana_row and 'class="psub ell' in ana_row and ana_row.find("class=morebtn") > ana_row.find('class="psub ell') and "<h3 class=alpha>" in mem_panel and mem_panel.find("<h3 class=alpha>") < mem_panel.find('class="list loose"') and ">Require background</button>" not in mem_panel and "Require background screening" not in mem_panel and "Don't require background" not in mem_panel, "People rows show one status line without email or legal name, and Require background is gone")
renamed = eli.post("/members", data=dict(csrf=csrf(eli, "/members"), member_id=jane_id, action="preferred", preferred_first="Jay"), follow_redirects=True).get_data(as_text=True)
jay_page = eli.get("/admin/member/%d" % jane_id).get_data(as_text=True)
ok("Jay" in renamed and "Legal name" in jay_page and D.execute("SELECT preferred_first FROM members WHERE id=?", (jane_id,)).fetchone()[0] == "Jay" and 'value="Jay"' in jay_page and "Jay Doe" in eli.get("/admin").get_data(as_text=True), "a preferred name saved on the members list shows on check-in")
nom = A.app.test_client(); join(nom, "Nora", "Name", "nora.name@example.com")
nid = D.execute("SELECT id FROM members WHERE email='nora.name@example.com'").fetchone()[0]
edit_page = eli.get("/admin/member/%d?edit=1" % nid).get_data(as_text=True)
coach_html = casey.get("/admin/member/%d" % nid).get_data(as_text=True)
prof = nom.get("/profile").get_data(as_text=True)
ok("Legal first name" in edit_page and "Legal last name" in edit_page and "name=first" in edit_page and "name=last" in edit_page and "profile-edit" in edit_page and "name=first" not in coach_html and "Legal first name" not in coach_html and "name=first" not in prof and "Legal first name" not in prof, "only an admin edit shows legal name fields")
nom.post("/profile", data=dict(csrf=csrf(nom, "/profile"), action="save", preferred_first="", phone="7205355925", first="Hacked", last="Person"), follow_redirects=True)
ok(D.execute("SELECT first, last FROM members WHERE id=?", (nid,)).fetchone() == ("Nora", "Name"), "a member cannot change their own legal name")
ok(casey.post("/admin/member/%d" % nid, data=dict(csrf=csrf(casey, "/admin/member/%d" % nid), action="edit", first="Hacked", last="Person", preferred_first="")).status_code == 403 and D.execute("SELECT first, last FROM members WHERE id=?", (nid,)).fetchone() == ("Nora", "Name"), "a coach cannot change a legal name")
blank = eli.post("/admin/member/%d" % nid, data=dict(csrf=csrf(eli, "/admin/member/%d" % nid), action="edit", first="  ", last="Name", preferred_first=""), follow_redirects=True).get_data(as_text=True)
ok("Enter a legal first and last name." in blank and D.execute("SELECT first, last FROM members WHERE id=?", (nid,)).fetchone() == ("Nora", "Name") and D.execute("SELECT COUNT(*) FROM name_audits WHERE member_id=?", (nid,)).fetchone()[0] == 0, "a blank legal name is refused")
saved = eli.post("/admin/member/%d" % nid, data=dict(csrf=csrf(eli, "/admin/member/%d" % nid), action="edit", first="  Norah ", last="Names", preferred_first=""), follow_redirects=True).get_data(as_text=True)
row = D.execute("SELECT actor_id, actor, old_name, new_name, at FROM name_audits WHERE member_id=?", (nid,)).fetchone()
ok(D.execute("SELECT first, last FROM members WHERE id=?", (nid,)).fetchone() == ("Norah", "Names") and "Norah Names" in saved and row[0] == eli_id and row[1] == "Eli Joern" and row[2] == "Nora Name" and row[3] == "Norah Names" and str(row[4]).startswith(A.today_pt().isoformat()) and "Eli Joern changed Nora Name → Norah Names" in saved, "an admin rename stores who, the old and new name, and when")
eli.post("/admin/member/%d" % nid, data=dict(csrf=csrf(eli, "/admin/member/%d" % nid), action="edit", first="Norah", last="Names", preferred_first=""))
ok(D.execute("SELECT COUNT(*) FROM name_audits WHERE member_id=?", (nid,)).fetchone()[0] == 1, "saving the same legal name does not add another audit row")
kay = A.app.test_client(); join(kay, "Kay", "Recheck", "kay.recheck@example.com")
kay_id = D.execute("SELECT id FROM members WHERE email='kay.recheck@example.com'").fetchone()[0]
D.execute("UPDATE members SET usawp_status='verified', usawp_number='303030', usawp_valid_until='2027-01-01', role='athlete', is_admin=0 WHERE id=?", (kay_id,))
D.commit()
shown = eli.get("/admin/member/%d" % kay_id).get_data(as_text=True)
ok(">Recheck</button>" in shown and "name=membership_type" in shown and "name=referee_expires" in shown and "name=safesport_expires" in shown and "name=background_expires" in shown and "Not on file · add date" in shown and kay.post("/members", data=dict(csrf=csrf(kay, "/home"), member_id=kay_id, action="recheck", verified="yes")).status_code == 403 and kay.get("/admin/member/%d" % kay_id).status_code == 403, "Recheck membership is on the member page for an admin, and a member cannot save it")
kay_panel = eli.get("/admin/member/%d" % kay_id).get_data(as_text=True)
ask_hits = []
class _AskResp:
    status = 204
    def __enter__(self): return self
    def __exit__(self, *a): return False
def _ask_spy(req, timeout=None, **k):
    ask_hits.append(json.loads(req.data.decode())); return _AskResp()
_ask_orig = __import__("urllib.request", fromlist=["urlopen"]).urlopen
_ask_url = A.VERIFY_WEBHOOK_URL
A.VERIFY_WEBHOOK_URL = "http://hooks.example/recheck"
__import__("urllib.request", fromlist=["urlopen"]).urlopen = _ask_spy
try:
    asked = eli.post("/members", data=dict(csrf=csrf(eli, "/members"), member_id=kay_id, action="ask_bot"), follow_redirects=True)
finally:
    __import__("urllib.request", fromlist=["urlopen"]).urlopen = _ask_orig
    A.VERIFY_WEBHOOK_URL = _ask_url
ok(">Ask Grunions to verify</button>" in kay_panel and "Look this member up on Sport:80" in kay_panel and ">Save</button>" in kay_panel and ">Cancel</button>" in kay_panel and asked.status_code == 200 and 'class="toast noprint"' in asked.get_data(as_text=True) and ask_hits and ask_hits[0]["requested_by"] == "Eli Joern" and ask_hits[0]["member_submitted"] is False and ask_hits[0]["member_id"] == kay_id and ask_hits[0]["name"] == "Kay Recheck" and D.execute("SELECT status, member_submitted, requested_by FROM verify_requests WHERE member_id=? ORDER BY id DESC LIMIT 1", (kay_id,)).fetchone() == ("pending", 0, "Eli Joern") and kay.post("/members", data=dict(csrf=csrf(kay, "/home"), member_id=kay_id, action="ask_bot")).status_code == 403, "Ask Grunions sits with Recheck and still asks the bot for a verified member")
D.execute("DELETE FROM verify_requests WHERE member_id=? AND status='pending'", (kay_id,)); D.commit()
ahead = (A.today_pt() + dt.timedelta(days=50)).isoformat()
eli.post("/members", data=dict(csrf=csrf(eli, "/members"), member_id=kay_id, action="recheck", verified="yes", membership_type="Individual Membership, Coach", valid_until=ahead, safesport_expires=ahead, background_expires=ahead))
who = D.execute("SELECT usawp_status, usawp_verified_by, usawp_verified_at, role, membership_type FROM members WHERE id=?", (kay_id,)).fetchone()
ok(who[0] == "verified" and who[1] == "Eli Joern" and who[2].startswith(A.today_pt().isoformat()) and who[3] == "athlete" and who[4] == "Individual Membership, Coach" and D.execute("SELECT source FROM coaching_list WHERE member_id=?", (kay_id,)).fetchone()[0] == "usawp" and kay.get("/admin").status_code == 403 and kay.get("/chat?c=coaches").status_code == 403 and '>Coaching</span><span class=v>Coach eligible</span>' in kay.get("/profile").get_data(as_text=True) and ('class="chip-info">Coach · expires ' + ahead) in eli.get("/members").get_data(as_text=True), "a Coach membership recorded from Sport:80 adds the coaching list and the expiry chip without coach access")
D.execute("INSERT INTO verify_requests(member_id,name,email,status,created) VALUES(?,?,?,'pending',?)", (kay_id, "Kay Recheck", "kay.recheck@example.com", A.today_pt().isoformat()))
D.commit()
pending_html = eli.get("/admin/member/%d" % kay_id).get_data(as_text=True)
eli.post("/members", data=dict(csrf=csrf(eli, "/members"), member_id=kay_id, action="recheck", verified="yes", membership_type="Athlete", valid_until=ahead, safesport_expires=ahead, background_expires=ahead, referee_expires=ahead))
ok("class=vrdetails" not in pending_html and "verification requested" not in pending_html and "bot answered" not in pending_html and D.execute("SELECT status FROM verify_requests WHERE member_id=? ORDER BY id DESC LIMIT 1", (kay_id,)).fetchone()[0] == "done" and not D.execute("SELECT 1 FROM coaching_list WHERE member_id=? AND source='usawp'", (kay_id,)).fetchone() and 'class="st st-ok ref-elig">Referee eligible' in eli.get("/members").get_data(as_text=True) and D.execute("SELECT role FROM members WHERE id=?", (kay_id,)).fetchone()[0] == "athlete", "the same form answers a pending request and a referee certification makes Referee eligible")
eli.post("/members", data=dict(csrf=csrf(eli, "/members"), member_id=kay_id, action="recheck", verified="yes", membership_type="Athlete", valid_until=ahead, safesport_expires=ahead, background_expires=ahead, referee_expires=(A.today_pt() - dt.timedelta(days=3)).isoformat()))
lapsed_ref = "Referee eligibility expired " + (A.today_pt() - dt.timedelta(days=3)).isoformat()
ok(lapsed_ref in eli.get("/members").get_data(as_text=True) and "Kay Recheck" not in eli.get("/members?referee=eligible").get_data(as_text=True), "a past referee certification is marked expired")
saved = eli.post("/members", data=dict(csrf=csrf(eli, "/members"), member_id=kay_id, action="edit", verified="yes", membership_type="Athlete", valid_until=ahead, safesport_expires=ahead, background_expires=ahead, preferred_first="Kaylee"), follow_redirects=True).get_data(as_text=True)
ok('class="toast noprint" role=status>Saved.' in saved and D.execute("SELECT preferred_first, membership_type FROM members WHERE id=?", (kay_id,)).fetchone() == ("Kaylee", "Athlete") and "Save background screening" not in saved and "Save preferred name" not in saved, "one Save stores the Sport:80 result and the preferred name")
eli.post("/members", data=dict(csrf=csrf(eli, "/members"), member_id=kay_id, action="recheck", verified="no", membership_type="Head Coach", valid_until=ahead))
ok(D.execute("SELECT usawp_status, role FROM members WHERE id=?", (kay_id,)).fetchone() == ("expired", "athlete") and not D.execute("SELECT 1 FROM coaching_list WHERE member_id=? AND source='usawp'", (kay_id,)).fetchone(), "a not-verified recheck does not add a coach membership to the coaching list")
D.execute("UPDATE members SET trial_acknowledged_at=?, usawp_status='unknown', usawp_valid_until=NULL WHERE id=?", (A.today_pt().isoformat(), jane_id))
D.commit()
trial_page = eli.get("/members").get_data(as_text=True)
jchunk = people_row(trial_page, "Jay Doe")
ok('class="psub ell st-warn"' in jchunk and '>Trial</span><span class=strest> · expires in 14 days' in jchunk and "jane@example.com" not in jchunk and "legal " not in jchunk and "practices" not in jchunk, "the members subline is status and detail, with no practice count")

# practice detail page
pday = (A.today_pt() + dt.timedelta(days=9)).isoformat()
eli.post("/practices", data=dict(csrf=csrf(eli, "/practices"), action="add", date=pday, start="19:00", end="20:30", location="Detail Pool", note="Bring caps"))
dpid = D.execute("SELECT id FROM practices WHERE location='Detail Pool'").fetchone()[0]
jane.post("/practices/%d" % dpid, data=dict(csrf=csrf(jane, "/practices"), pid=dpid, action="going", back="page"))
eli.post("/practices/%d" % dpid, data=dict(csrf=csrf(eli, "/practices"), pid=dpid, action="notgoing", back="page"))
D.execute("INSERT INTO checkins(member_id,practice_date,location) VALUES(?,?,?)", (D.execute("SELECT id FROM members WHERE email='jane@example.com'").fetchone()[0], pday, "Detail Pool")); D.commit()
sched_j = jane.get("/practices").get_data(as_text=True)
sched_e = eli.get("/practices").get_data(as_text=True)
card_e = sched_e.split("id=p%d " % dpid, 1)[1].split("id=p")[0]
ok(('href="/practices/%d"' % dpid) in sched_j and " going</span>" in card_e and "class=nxtitle>Water Polo Practice</div>" in card_e and "class=nxhead" not in card_e and "class=datetile" in card_e and "class=mo>" in card_e and "class=pills" in card_e and "I'm going" in card_e and "I'm not going" in card_e and "class=nxchev" not in card_e and "class=pimg" not in card_e and "class=nxicon" not in card_e and "class=morebtn" not in card_e and "Assign coaches" not in card_e and "Delete practice" not in card_e and "class=morebtn" not in sched_e and "class=morebtn" not in sched_j, "a schedule card shows the date tile and icon rows and has no More menu")
page_j = jane.get("/practices/%d" % dpid).get_data(as_text=True)
page_e = eli.get("/practices/%d" % dpid).get_data(as_text=True)
ok(jane.get("/practices/999999").status_code == 404 and "Detail Pool" in page_j and "Bring caps" in page_j and "Jay Doe" in page_j and "Eli Joern" in page_j and "Checked in" in page_j and "Can't make it" in page_j and "maps.google.com/maps?q=" not in page_j and "class=\"homemap cardmap banner\"" in page_j and "mode:'card'" in page_j and "google.com/maps/dir/" in page_j and "btn btn-secondary" in page_j and "loccard" in page_j and "practiceLoc" in page_j and "Scheduled" in page_j and ">Edit</a>" not in page_j and "Assign coaches" not in page_j and "class=morebtn" not in page_j and "No assigned coach is coach-eligible" not in page_j and "No coaches assigned." in page_e and "No assigned coach is coach-eligible" not in page_e and 'href="/admin/member/' in page_e and 'href="/admin/member/' not in page_j and ">Edit</a>" in page_e and "class=morebtn" not in page_e and "Assign coaches" in page_e and "Delete practice" in page_e, "the practice page shows who's coming, the map banner, and an admin edit action and coach warning")
editp = eli.get("/practices/%d?edit=1" % dpid).get_data(as_text=True)
ok('name=date' in editp and 'name=start' in editp and 'name=location' in editp and "name=note" in editp and ">Save</button>" in editp and ">Cancel</a>" in editp and editp.find(">Cancel</a>") < editp.find("<h1>Practice</h1>") < editp.find('class="profileact savebtn"') and 'aria-label="Back"' not in editp.split("<main>",1)[0] and 'class="btn btn-primary full" name=action value=edit>Save' not in editp and 'form=practiceForm name=action value=edit>Save' in editp and 'name=date' not in jane.get("/practices/%d?edit=1" % dpid).get_data(as_text=True), "admins edit the practice on the page, and members stay in read mode")
eli.post("/practices/%d" % dpid, data=dict(csrf=csrf(eli, "/practices/%d" % dpid), pid=dpid, action="edit", back="page", date=pday, start="18:30", end="20:00", location="Detail Pool", note="Caps and fins"))
saved = D.execute("SELECT start, note FROM practices WHERE id=?", (dpid,)).fetchone()
ok(saved == ("18:30", "Caps and fins") and "Caps and fins" in eli.get("/practices/%d" % dpid).get_data(as_text=True) and jane.post("/practices/%d" % dpid, data=dict(csrf=csrf(jane, "/home"), pid=dpid, action="edit", date=pday, start="18:30", end="20:00", location="Detail Pool", note="nope")).status_code == 403, "saving the practice page stores the new time and note")
dean = A.app.test_client(); join(dean, "Dean", "Lead", "dean.lead@example.com")
dean_id = D.execute("SELECT id FROM members WHERE email='dean.lead@example.com'").fetchone()[0]
D.execute("UPDATE members SET role='coach', is_admin=0 WHERE id=?", (dean_id,)); D.commit()
list_act(dean_id, "add_coaching"); list_act(eli_id, "add_coaching")
plan_day = (A.today_pt() + dt.timedelta(days=11)).isoformat()
eli.post("/practices", data=dict(csrf=csrf(eli, "/practices"), action="add", date=plan_day, start="19:00", end="20:30", location="Plan Pool"))
ppid = D.execute("SELECT id FROM practices WHERE location='Plan Pool'").fetchone()[0]
secret = "Secret drill\nfor goalies"
eli.post("/practices/%d" % ppid, data={"csrf": csrf(eli, "/practices/%d" % ppid), "pid": ppid, "action": "edit", "back": "page", "date": plan_day, "start": "19:00", "end": "20:30", "location": "Plan Pool", "note": "", "coach": [str(dean_id), str(eli_id)], "lead": str(dean_id), "plan_fields": "1", "coaching_plan": secret, "focus-%d" % dean_id: "Beginners", "focus-%d" % eli_id: "Goalies"})
plan_card = jane.get("/practices").get_data(as_text=True).split("id=p%d " % ppid, 1)[1].split("id=p")[0]
plan_home = jane.get("/home").get_data(as_text=True)
plan_mem = jane.get("/practices/%d" % ppid).get_data(as_text=True)
plan_adm = eli.get("/practices/%d" % ppid).get_data(as_text=True)
plan_coa = dean.get("/practices/%d" % ppid).get_data(as_text=True)
plan_edit = dean.get("/practices/%d?edit=1" % ppid).get_data(as_text=True)
ok("Coaches: Dean (lead), Eli" in plan_card and "Secret drill" not in plan_card and "Beginners" not in plan_card and "Secret drill" not in plan_home and "for goalies" not in plan_home and ">Lead</span>" in plan_mem and "Today's plan" not in plan_mem and "Coaches only" not in plan_mem and "Secret drill" not in plan_mem and "Beginners" not in plan_mem and "Goalies" not in plan_mem and "Today's plan" in plan_adm and "Coaches only" in plan_adm and "Secret drill" in plan_adm and "for goalies" in plan_adm and plan_adm.count("Beginners") >= 2 and "Goalies" in plan_adm and ">Lead</span>" in plan_coa and plan_coa.count("Beginners") >= 2 and "name=date" not in plan_edit and "Today's plan" in plan_edit and "name=coaching_plan" in plan_edit, "the lead shows for everyone, and the plan and focus groups stay with coaches")
ok(jane.post("/practices/%d" % ppid, data={"csrf": csrf(jane, "/home"), "pid": ppid, "action": "plan", "coaching_plan": "stolen", "lead": str(eli_id), "focus-%d" % dean_id: "Nope"}).status_code == 403 and D.execute("SELECT coaching_plan FROM practices WHERE id=?", (ppid,)).fetchone()[0] == secret and D.execute("SELECT member_id FROM practice_coaches WHERE practice_id=? AND is_lead=1", (ppid,)).fetchone()[0] == dean_id, "a member cannot save or read the coaching plan")
dean.post("/practices/%d" % ppid, data={"csrf": csrf(dean, "/practices/%d" % ppid), "pid": ppid, "action": "plan", "back": "page", "coaching_plan": "Updated drill\nline two", "lead": str(eli_id), "focus-%d" % eli_id: "Advanced", "focus-%d" % dean_id: "Goalies"})
moved = dean.get("/practices").get_data(as_text=True).split("id=p%d " % ppid, 1)[1].split("id=p")[0]
moved_mem = jane.get("/practices/%d" % ppid).get_data(as_text=True)
ok("Coaches: Eli (lead), Dean" in moved and "Updated drill" not in moved and D.execute("SELECT coaching_plan FROM practices WHERE id=?", (ppid,)).fetchone()[0] == "Updated drill\nline two" and D.execute("SELECT focus FROM practice_coaches WHERE practice_id=? AND member_id=?", (ppid, eli_id)).fetchone()[0] == "Advanced" and "Advanced" in eli.get("/practices/%d" % ppid).get_data(as_text=True) and "Updated drill" not in moved_mem and "Advanced" not in moved_mem and ">Lead</span>" in moved_mem, "a coach can change the lead, the plan, and a focus group")
eli.post("/practices/%d" % ppid, data=dict(csrf=csrf(eli, "/practices/%d" % ppid), pid=ppid, action="duplicate", back="page"))
copy_plan = (dt.date.fromisoformat(plan_day) + dt.timedelta(days=7)).isoformat()
copy_plan_id = D.execute("SELECT id FROM practices WHERE date=? AND location='Plan Pool'", (copy_plan,)).fetchone()[0]
ok(D.execute("SELECT coaching_plan FROM practices WHERE id=?", (copy_plan_id,)).fetchone()[0] == "Updated drill\nline two" and D.execute("SELECT member_id, focus FROM practice_coaches WHERE practice_id=? AND is_lead=1", (copy_plan_id,)).fetchone() == (eli_id, "Advanced"), "duplicating a practice copies the plan, the lead, and the focus group")
eli.post("/practices/%d" % copy_plan_id, data=dict(csrf=csrf(eli, "/practices/%d" % copy_plan_id), pid=copy_plan_id, action="delete"))
eli.post("/practices/%d" % ppid, data=dict(csrf=csrf(eli, "/practices/%d" % ppid), pid=ppid, action="delete"))
emails.clear(); pushes.clear()
eli.post("/practices/%d" % dpid, data=dict(csrf=csrf(eli, "/practices/%d" % dpid), pid=dpid, action="cancel", reason="Pool closed", back="page"))
cancelled = eli.get("/practices/%d" % dpid).get_data(as_text=True)
card_c = eli.get("/practices").get_data(as_text=True).split("id=p%d " % dpid, 1)[1].split("id=p")[0]
reason_mail = [e for e in emails if e[0] == "jane@example.com" and "Pool closed" in e[2]]
ok("Cancelled" in cancelled and "Pool closed" in cancelled and "Pool closed" in card_c and "Undo cancel" in cancelled and len(reason_mail) == 1 and "Detail Pool" in reason_mail[0][2] and any(p[1]["url"] == "/practices/%d" % dpid and "Pool closed" in p[1]["body"] for p in pushes), "sending a cancellation stores the reason, shows it, and emails and pushes it")
eli.post("/practices/%d" % dpid, data=dict(csrf=csrf(eli, "/practices/%d" % dpid), pid=dpid, action="restore", back="page"))
ok(D.execute("SELECT cancelled, COALESCE(cancel_reason,'') FROM practices WHERE id=?", (dpid,)).fetchone() == (0, "") and "Pool closed" not in eli.get("/practices/%d" % dpid).get_data(as_text=True), "undo cancel clears the cancellation and the reason")
eli.post("/practices/%d" % dpid, data=dict(csrf=csrf(eli, "/practices/%d" % dpid), pid=dpid, action="assign", back="page", coach=str(D.execute("SELECT id FROM members WHERE email='eli@example.com'").fetchone()[0])))
copied = eli.post("/practices/%d" % dpid, data=dict(csrf=csrf(eli, "/practices/%d" % dpid), pid=dpid, action="duplicate", back="page"), follow_redirects=True)
copy_day = (dt.date.fromisoformat(pday) + dt.timedelta(days=7)).isoformat()
copy_id = D.execute("SELECT id FROM practices WHERE date=? AND location='Detail Pool'", (copy_day,)).fetchone()[0]
ok(("Copied to %s." % A.fmt_d(copy_day)) in copied.get_data(as_text=True) and D.execute("SELECT COUNT(*) FROM practice_coaches WHERE practice_id=?", (copy_id,)).fetchone()[0] == 1 and jane.post("/practices/%d" % copy_id, data=dict(csrf=csrf(jane, "/home"), pid=copy_id, action="delete")).status_code == 403, "duplicate copies the practice a week later, and a member cannot delete it")
eli.post("/practices/%d" % copy_id, data=dict(csrf=csrf(eli, "/practices/%d" % copy_id), pid=copy_id, action="delete"))
eli.post("/practices/%d" % dpid, data=dict(csrf=csrf(eli, "/practices/%d" % dpid), pid=dpid, action="delete"))
ok(not D.execute("SELECT 1 FROM practices WHERE location='Detail Pool'").fetchone() and "Detail Pool" not in eli.get("/export/practices.csv?start=%s&end=%s" % (pday, copy_day)).get_data(as_text=True), "deleting a practice removes it from the schedule and the sheet export")
ref_added = eli.post("/members", data=dict(csrf=csrf(eli, "/members"), member_id=jane_id, action="add_referee", list_view="referees"), follow_redirects=True).get_data(as_text=True)
ok("was added to referees." in ref_added and "Jay Doe" in ref_added and "Remove from referees" in ref_added and ">Referees</a>" in ref_added and D.execute("SELECT 1 FROM referee_list WHERE member_id=?", (jane_id,)).fetchone() and jane.get("/members").status_code == 403, "Add to referees puts someone on the referee list, and only an admin can open People")

# after-practice social, coach message, and the home next-practice RSVP
pat = A.app.test_client(); join(pat, "Pat", "Host", "pat.host@example.com")
D.execute("UPDATE members SET role='coach', is_admin=0 WHERE email='pat.host@example.com'"); D.commit()
home0 = jane.get("/home").get_data(as_text=True)
card_at = home0.find('class="card tap nextcard"')
nchunk = home0[card_at:home0.find("</form>", card_at)]
nid = int(re.search(r'href="/practices/(\d+)"', nchunk).group(1))
nrow = D.execute("SELECT date, start, end, location, COALESCE(note,'') FROM practices WHERE id=?", (nid,)).fetchone()
ok("I'm going" in nchunk and "I'm not going" in nchunk and ('href="/practices/%d"' % nid) in nchunk and "card tap" in nchunk and "🍻" not in nchunk and "After-practice social" not in jane.get("/practices").get_data(as_text=True), "the next practice card links to the practice and offers I'm going and I'm not going")
ok(jane.post("/practices/%d" % nid, data=dict(csrf=csrf(jane, "/home"), pid=nid, action="social", social_kind="Drinks", social_place="The Harp")).status_code == 403 and jane.post("/practices/%d" % nid, data=dict(csrf=csrf(jane, "/home"), pid=nid, action="message", message="hi")).status_code == 403, "a member cannot set a social or a coach message")
missing = eli.post("/practices/%d" % nid, data=dict(csrf=csrf(eli, "/practices"), pid=nid, action="social", back="page", social_kind="Dinner", social_place=""), follow_redirects=True).get_data(as_text=True)
empty_host = pat.get("/practices/%d" % nid).get_data(as_text=True)
ok("Add a place for the social." in missing and "🍽️" not in jane.get("/practices/%d" % nid).get_data(as_text=True) and "<h2>After-practice social</h2>" not in jane.get("/practices/%d" % nid).get_data(as_text=True) and ">After-practice social<" in empty_host and ">Add<" in empty_host, "a social needs a place, and only a host sees Add when there is none")
pat.post("/practices/%d" % nid, data=dict(csrf=csrf(pat, "/practices"), pid=nid, action="social", back="schedule", social_kind="Drinks", social_place="The Harp", social_address="https://maps.example/harp", social_time="20:30", social_note="Cash bar"))
pat.post("/practices/%d" % nid, data=dict(csrf=csrf(pat, "/practices"), pid=nid, action="message", back="page", message="Bring dark caps"))
noted = D.execute("SELECT coach_note_by, coach_note_at FROM practices WHERE id=?", (nid,)).fetchone()
stamp = A.fmt_stamp(noted[1])
line = "Drinks after at The Harp"
page_s = jane.get("/practices/%d" % nid).get_data(as_text=True)
sched_s = jane.get("/practices").get_data(as_text=True)
card_s = sched_s.split("id=p%d " % nid, 1)[1].split("id=p")[0]
home_s = jane.get("/home").get_data(as_text=True)
pat_card = pat.get("/practices").get_data(as_text=True).split("id=p%d " % nid, 1)[1].split("id=p")[0]
eli_card = eli.get("/practices").get_data(as_text=True).split("id=p%d " % nid, 1)[1].split("id=p")[0]
pat_page = pat.get("/practices/%d" % nid).get_data(as_text=True)
eli_page = eli.get("/practices/%d" % nid).get_data(as_text=True)
ok((line + " · 8:30pm") in page_s and "Cash bar" in page_s and 'href="https://maps.example/harp"' in page_s and line not in card_s and "class=nxicon" not in card_s and "class=nxicon" in page_s and "class=nxicon" in home_s and "M237.66,45.66" in page_s and "M237.66,45.66" in home_s and 'fill="#FFFFFF"' not in home_s and "🍽️" not in home_s and "🍽️" not in page_s and "Cash bar" not in card_s and "Bring dark caps" in card_s and noted[0] == "Pat Host" and stamp in card_s and "Drinks after" in home_s and "The Harp" in home_s and "Bring dark caps" in home_s and stamp in home_s and "class=morebtn" not in pat_card and "class=morebtn" not in eli_card and "After-practice social" in pat_page and "Coach message" in pat_page and "Delete practice" not in pat_page and "After-practice social" in eli_page and "Delete practice" in eli_page and "name=date" not in pat.get("/practices/%d?edit=1" % nid).get_data(as_text=True), "a social shows on the practice page and home, not the schedule, and a coach message still shows on the schedule")
jane.post("/practices", data=dict(csrf=csrf(jane, "/home"), pid=nid, action="notgoing"))
ok(">I'm not going ✓<" in jane.get("/home").get_data(as_text=True) and ">I'm not going ✓<" in jane.get("/practices/%d" % nid).get_data(as_text=True) and ">I'm not going ✓<" in jane.get("/practices").get_data(as_text=True).split("id=p%d " % nid, 1)[1].split("id=p")[0], "I'm not going on home is the same RSVP as the practice page and the schedule")
jane.post("/practices/%d" % nid, data=dict(csrf=csrf(jane, "/practices/%d" % nid), pid=nid, action="going", back="page"))
ok(">I'm going ✓<" in jane.get("/home").get_data(as_text=True) and ">I'm going ✓<" in jane.get("/practices/%d" % nid).get_data(as_text=True) and ">I'm going ✓<" in jane.get("/practices").get_data(as_text=True).split("id=p%d " % nid, 1)[1].split("id=p")[0], "I'm going on the practice page shows on home and the schedule")
pat.post("/practices/%d" % nid, data=dict(csrf=csrf(pat, "/practices"), pid=nid, action="social", back="page", social_kind=["Dinner", "Drinks"], social_place="The Harp", social_address="https://maps.example/harp", social_time="20:30", social_note="Cash bar"))
combo = "Dinner &amp; drinks after at The Harp"
member_page = jane.get("/practices/%d" % nid).get_data(as_text=True)
host_page = pat.get("/practices/%d" % nid).get_data(as_text=True)
ok(D.execute("SELECT social_kind FROM practices WHERE id=?", (nid,)).fetchone()[0] == "Dinner,Drinks" and combo in member_page and "Dinner &amp; drinks after" in jane.get("/home").get_data(as_text=True) and "The Harp" in jane.get("/home").get_data(as_text=True) and combo not in jane.get("/practices").get_data(as_text=True).split("id=schedule",1)[-1] and member_page.find("seclabel>After-practice social") < member_page.find("seclabel>Coaches") < member_page.find("seclabel>Who") and ">Edit<" not in member_page and ">Add<" not in member_page and ">Edit<" in host_page and 'type=checkbox name=social_kind value="Dinner" checked' in host_page and 'type=checkbox name=social_kind value="Drinks" checked' in host_page and "None</option>" not in host_page, "types combine on the practice section and home, and a host edits them")
D.execute("UPDATE practices SET social_kind='Social,Dinner' WHERE id=?", (nid,)); D.commit()
A.migrate_social_kinds(D); D.commit()
ok(D.execute("SELECT social_kind FROM practices WHERE id=?", (nid,)).fetchone()[0] == "Dinner,Social" and "Dinner &amp; social after at The Harp" not in jane.get("/practices").get_data(as_text=True).split("id=schedule",1)[-1] and "Dinner &amp; social after" in jane.get("/home").get_data(as_text=True), "an older combination is stored as Dinner, then Drinks, then Social")
pat.post("/practices/%d" % nid, data=dict(csrf=csrf(pat, "/practices"), pid=nid, action="social", back="page", social_kind=["Dessert", "Coffee", "Other"], social_place="The Harp"))
kind_box = pat.get("/practices/%d" % nid).get_data(as_text=True)
kind_order = [kind_box.find('value="%s"' % k) for k in A.SOCIAL_KINDS]
ok(D.execute("SELECT social_kind FROM practices WHERE id=?", (nid,)).fetchone()[0] == "Coffee,Dessert,Other" and "Coffee &amp; dessert &amp; other after at The Harp" not in jane.get("/practices").get_data(as_text=True).split("id=schedule",1)[-1] and "Coffee &amp; dessert &amp; other after" in jane.get("/home").get_data(as_text=True) and kind_order == sorted(kind_order) and all(i > 0 for i in kind_order) and tuple(A.SOCIAL_KINDS) == ("Dinner", "Drinks", "Social", "Coffee", "Dessert", "Activities", "Potluck", "Other"), "social types include coffee, dessert, activities, potluck, and other, in that order")
eli.post("/practices/%d" % nid, data=dict(csrf=csrf(eli, "/practices/%d" % nid), pid=nid, action="edit", back="page", date=nrow[0], start=nrow[1], end=nrow[2], location=nrow[3], note=nrow[4], social_kind="Social", social_place="Clubhouse", social_address="", social_time="", social_note="", message="Warmup laps"))
ok("Social after" in jane.get("/home").get_data(as_text=True) and "Clubhouse" in jane.get("/home").get_data(as_text=True) and "Warmup laps" in jane.get("/practices/%d" % nid).get_data(as_text=True) and "Eli Joern" in jane.get("/practices/%d" % nid).get_data(as_text=True) and line not in jane.get("/home").get_data(as_text=True), "edit mode saves the social and the coach message")
jane.post("/practices/%d" % nid, data=dict(csrf=csrf(jane, "/home"), pid=nid, action="social_join"))
ok(">Joined ✓<" in jane.get("/home").get_data(as_text=True) and ">1 joining<" in jane.get("/practices/%d" % nid).get_data(as_text=True), "joining a social marks the Home pill and counts on the practice page")
jane.post("/practices/%d" % nid, data=dict(csrf=csrf(jane, "/home"), pid=nid, action="social_leave"))
ok(">Join<" in jane.get("/home").get_data(as_text=True) and ">Joined ✓<" not in jane.get("/home").get_data(as_text=True) and ">0 joining<" in jane.get("/practices/%d" % nid).get_data(as_text=True), "leaving a social clears the pill and the count")
eli.post("/practices/%d" % nid, data=dict(csrf=csrf(eli, "/practices"), pid=nid, action="social", social_kind=""))
eli.post("/practices/%d" % nid, data=dict(csrf=csrf(eli, "/practices"), pid=nid, action="message", message=""))
cleared = jane.get("/home").get_data(as_text=True) + jane.get("/practices/%d" % nid).get_data(as_text=True)
ok("Social after at" not in cleared and "Warmup laps" not in cleared and "Drinks after at" not in cleared and "<h2>After-practice social</h2>" not in jane.get("/practices/%d" % nid).get_data(as_text=True), "clearing the social and the coach message hides both")

# Home header, practice image, and map
home_h = jane.get("/home").get_data(as_text=True)
head, body = home_h.split("<main>", 1)
prof = jane.get("/profile").get_data(as_text=True)
sched_head = jane.get("/practices").get_data(as_text=True).split("<main>", 1)[0]
ok("Hi, Jay</h1>" in head and "class=hititle" in head and "class=schedtitle" in head and ">Schedule</h1>" in head and "--titlefade" in head and "Tue · Marina HS" not in head and ">JD<" in head and "Log out" not in head and 'href=/profile' in head and "<h1>Profile</h1>" in prof and "practices attended" in prof and 'href=/notifications' in prof and ">Log out</a>" in prof and ">Edit<" in prof and "tabs noprint" not in prof and "class=pick" in prof and "Change photo" not in prof and "class=avatarwrap" in prof and "id=camBadge" in prof and "header.profilebar button.editonly,header.profilebar a.editonly{display:none}" in prof and "body.profile-edit header.profilebar button.viewonly,body.profile-edit header.profilebar a.viewonly{display:none}" in prof and "id=profileBack" in prof and "id=profileEdit" in prof and "id=profileCancel" in prof and "id=profileSave" in prof and "Hi, Jay</h1>" in sched_head and "class=schedtitle" in sched_head and ">Schedule</h1>" in sched_head and "data-entry=\"schedule\"" in sched_head and "Tue · Marina HS" not in sched_head and "Log out" not in sched_head and 'href=/profile' in sched_head and "innerHeight-safe-offset-navH" in home_h, "Home greets by name with an initials avatar, and profile is its own page")
_today, _tom, _soon, _later = A.today_pt(), A.today_pt()+dt.timedelta(days=1), A.today_pt()+dt.timedelta(days=3), A.today_pt()+dt.timedelta(days=8)
_nxt = D.execute("SELECT date FROM practices WHERE date>=? AND cancelled=0 ORDER BY date, start LIMIT 1", (_today.isoformat(),)).fetchone()
_hero = body.split("id=schedule", 1)[0]
_later_cards = body.split("id=schedule", 1)[-1]
ok(A.relative_day(_today.isoformat()) == "TODAY" and A.relative_day(_tom.isoformat()) == "TOMORROW" and A.relative_day(_soon.isoformat()) == _soon.strftime("%A").upper() and A.relative_day(_later.isoformat()) == A.fmt_md(_later.isoformat()) and _nxt and ('class="chip-info daychip">%s<' % A.relative_day(_nxt[0])) in _hero and ".nextcard .daychip{height:32px;margin:-3px -8px -3px 0;padding:0 11px;font-size:16px}" in head and "nxsocial" not in _later_cards, "the next card shows today, tomorrow, a weekday, or a short date, and later cards have no social")
_prev_mem = D.execute("SELECT usawp_number, usawp_status, usawp_valid_until FROM members WHERE email='jane@example.com'").fetchone()
D.execute("UPDATE members SET usawp_number='4242421', usawp_status='verified', usawp_valid_until=? WHERE email='jane@example.com'", ((_today + dt.timedelta(days=40)).isoformat(),)); D.commit()
_hh, _bb = jane.get("/home").get_data(as_text=True).split("<main>", 1)
D.execute("UPDATE members SET usawp_number=?, usawp_status=?, usawp_valid_until=? WHERE email='jane@example.com'", _prev_mem); D.commit()
ok("USAWP #4242421" in _hh.split("Hi, Jay", 1)[-1] and "USAWP #4242421" not in _bb.split("id=schedule", 1)[0] and 'href="/profile#membership"' in _hh, "the membership chip sits under the greeting and not on the next card")
prev_phone, prev_pref = D.execute("SELECT phone, preferred_first FROM members WHERE id=?", (jane_id,)).fetchone()
short = jane.post("/profile", data=dict(csrf=csrf(jane, "/profile"), action="save", preferred_first=prev_pref or "", phone="555"), follow_redirects=True).get_data(as_text=True)
ok("10-digit" in short and D.execute("SELECT phone FROM members WHERE id=?", (jane_id,)).fetchone()[0] == prev_phone, "a short phone number is not saved")
saved_phone = jane.post("/profile", data=dict(csrf=csrf(jane, "/profile"), action="save", preferred_first=prev_pref or "", phone="1 (720) 535-5925"), follow_redirects=True).get_data(as_text=True)
ok(D.execute("SELECT phone FROM members WHERE id=?", (jane_id,)).fetchone()[0] == "7205355925" and "(720) 535-5925" in saved_phone and "name=phone" in saved_phone and "inputmode=numeric" in saved_phone and "name=email" not in saved_phone and "Remove photo" in saved_phone, "profile save stores a 10-digit phone and shows it formatted")
D.execute("UPDATE members SET phone=? WHERE id=?", (prev_phone, jane_id)); D.commit()
jane.post("/home", data={"csrf": csrf(jane, "/home"), "action": "avatar", "photo": (img_bytes("JPEG", (480, 480)), "me.jpg")}, content_type="multipart/form-data")
shown = jane.get("/home").get_data(as_text=True)
ok(('src="/avatar/%d' % jane_id) in shown and 'width="44" height="44"' in shown.split("<main>", 1)[0] and ">JD<" not in shown.split("<main>", 1)[0] and 'width="112" height="112"' in jane.get("/profile").get_data(as_text=True) and eli.get("/avatar/%d" % jane_id).status_code == 200 and client().get("/avatar/%d" % jane_id).status_code == 302, "a profile picture is stored for the member and stays inside the avatar circle")
jane.post("/home", data=dict(csrf=csrf(jane, "/home"), action="avatar_clear"))
ok(">JD<" in jane.get("/home").get_data(as_text=True).split("<main>", 1)[0] and not (D.execute("SELECT photo FROM members WHERE id=?", (jane_id,)).fetchone()[0] or ""), "removing the profile picture falls back to initials")
card_home = jane.get("/home").get_data(as_text=True)
pic_id = int(re.search(r'href="/practices/(\d+)"', card_home[card_home.find('class="card tap nextcard"'):]).group(1))
pic_date = D.execute("SELECT date FROM practices WHERE id=?", (pic_id,)).fetchone()[0]
badge = "TODAY" if pic_date == A.today_pt().isoformat() else A.fmt_d(pic_date)
ok(jane.post("/practices/%d" % pic_id, data={"csrf": csrf(jane, "/home"), "pid": pic_id, "action": "image", "image": (img_bytes(), "pool.png")}, content_type="multipart/form-data").status_code == 403 and "class=pimg" not in jane.get("/home").get_data(as_text=True), "a member cannot set the practice image, and Home omits the image area")
pat.post("/practices/%d" % pic_id, data={"csrf": csrf(pat, "/practices/%d" % pic_id), "pid": pic_id, "action": "image", "back": "page", "image": (img_bytes("PNG", (640, 400)), "pool.png")}, content_type="multipart/form-data")
pictured = jane.get("/home").get_data(as_text=True)
pcard = pictured[pictured.find('class="card tap nextcard"'):pictured.find("I'm going", pictured.find('class="card tap nextcard"'))]
sched_pic = jane.get("/practices").get_data(as_text=True)
ok("class=pimg" in pcard and ("/practice-image/%d" % pic_id) in pcard and (">%s<" % badge) in pcard and "class=pimg" not in sched_pic.split("id=schedule",1)[-1] and ("/practice-image/") not in sched_pic.split("id=schedule",1)[-1] and jane.get("/practice-image/%d" % pic_id).status_code == 200 and "Practice image" in pat.get("/practices/%d" % pic_id).get_data(as_text=True) and 'type=file name=image' in eli.get("/practices/%d?edit=1" % pic_id).get_data(as_text=True), "a coach image shows on the Home card with a monochrome date badge and stays off the schedule")
pat.post("/practices/%d" % pic_id, data=dict(csrf=csrf(pat, "/practices/%d" % pic_id), pid=pic_id, action="image", back="page", image_clear="1"))
ok("class=pimg" not in jane.get("/home").get_data(as_text=True) and not (D.execute("SELECT image FROM practices WHERE id=?", (pic_id,)).fetchone()[0] or ""), "removing the practice image drops the image area")
D.execute("UPDATE practices SET lat=?, lng=?, social_kind=?, social_place=?, social_address=?, social_lat=?, social_lng=? WHERE id=?", (33.5, -117.5, "Dinner", "The Harp", "123 Main St", 33.6, -117.6, pic_id)); D.commit()
mapped = jane.get("/home").get_data(as_text=True)
i_card, i_play, i_map = mapped.find('class="card tap nextcard"'), mapped.find('class="card playcard"'), mapped.find("id=homeMap")
pic_loc = D.execute("SELECT location FROM practices WHERE id=?", (pic_id,)).fetchone()[0]
pic_pool = A.pool_place(pic_loc)
pool_lat = str(pic_pool["lat"]) if pic_pool else "33.5"
ok("id=homeMap" in mapped and "class=homedock" in mapped and "padding:0 0 12px;min-height:" in mapped and "flex-end;gap:12px" in mapped and 'class="homefull"' in mapped and "var regional=12" in mapped and "cardTop*5/12" in mapped and "grunionsPlaceMap" in mapped and "zoomControl:false" in mapped and "dragging:false" in mapped and "touchZoom:false" in mapped and "doubleClickZoom:false" in mapped and "boxZoom:false" in mapped and "keyboard:false" in mapped and mapped.find("id=homeMap") < i_card and 'class="card playcard"' not in mapped and pool_lat in mapped and "33.6" in mapped and "tile.openstreetmap.org" in mapped and "maps.apple.com" in mapped and "google.com/maps/dir/" in mapped and "id=schedule" in jane.get("/practices").get_data(as_text=True) and "requestAnimationFrame" in mapped and "passive:true" in mapped and "prefers-reduced-motion" in mapped and "<summary>Attendance</summary>" not in mapped and "<summary>Profile</summary>" not in mapped and "name=preferred_first" in jane.get("/profile").get_data(as_text=True), "the map fills the home screen behind the cards at a regional zoom, with the pool and social pins")
import urllib.request as _ureq
class _GeoResp:
    def __enter__(self): return self
    def __exit__(self, *a): return False
    def read(self): return b'[{"lat":"33.5","lon":"-117.25"}]'
_orig_url = _ureq.urlopen
_ureq.urlopen = lambda req, timeout=None, **k: _GeoResp()
try:
    A._GEO_CACHE.pop("Unit Pool Address", None)
    hit = A.geocode_address("Unit Pool Address")
    again = A.geocode_address("Unit Pool Address")
finally:
    _ureq.urlopen = _orig_url
ok(hit == (33.5, -117.25) and again == hit and A.geocode_address("") is None and A.geocode_address("https://maps.example/x") is None, "nominatim results are cached and a map link is not geocoded")
west, marina = A.pool_place("Westminster High School"), A.pool_place("Marina High School")
wid = D.execute("SELECT id FROM practices WHERE location='Westminster High School' ORDER BY date LIMIT 1").fetchone()[0]
D.execute("UPDATE practices SET lat=39.836652, lng=-105.037205, address='' WHERE id=?", (wid,)); D.commit()
fixed = jane.get("/practices/%d" % wid).get_data(as_text=True)
wrow = D.execute("SELECT lat, lng, address FROM practices WHERE id=?", (wid,)).fetchone()
mid = D.execute("SELECT id FROM practices WHERE location='Marina High School' ORDER BY date LIMIT 1").fetchone()[0]
mrow = D.execute("SELECT lat, lng, address FROM practices WHERE id=?", (mid,)).fetchone()
ok(west["address"] == "14325 Goldenwest St, Westminster, CA 92683" and west["lng"] < -117 and A.geocode_address("Westminster High School") == (west["lat"], west["lng"]) and abs(wrow[0] - west["lat"]) < 1e-5 and abs(wrow[1] - west["lng"]) < 1e-5 and wrow[2] == west["address"] and "Goldenwest" in fixed and "39.836652" not in fixed and ("destination=%s" % west["lat"]) in fixed and marina["address"] == "15871 Springdale St, Huntington Beach, CA 92649" and abs(mrow[0] - marina["lat"]) < 1e-5 and abs(mrow[1] - marina["lng"]) < 1e-5 and mrow[2] == marina["address"] and A.geocode_address("Marina High School") == (marina["lat"], marina["lng"]), "Westminster and Marina pins and directions use the California schools")
prow = D.execute("SELECT date, start, end, COALESCE(note,'') FROM practices WHERE id=?", (pic_id,)).fetchone()
eli.post("/practices/%d" % pic_id, data=dict(csrf=csrf(eli, "/practices/%d" % pic_id), pid=pic_id, action="edit", back="page", date=prow[0], start=prow[1], end=prow[2], location="Moved Map Pool", note=prow[3]))
D.commit()
moved_row = D.execute("SELECT lat, lng, social_lat FROM practices WHERE id=?", (pic_id,)).fetchone()
eli.post("/practices/%d" % pic_id, data=dict(csrf=csrf(eli, "/practices/%d" % pic_id), pid=pic_id, action="social", back="page", social_kind="Dinner", social_place="Other Place", social_address="456 Side St"))
D.commit()
ok(moved_row[0] is None and moved_row[1] is None and moved_row[2] == 33.6 and D.execute("SELECT social_lat FROM practices WHERE id=?", (pic_id,)).fetchone()[0] is None, "changing the pool or social address clears the cached coordinates")
empty_line = jane.get("/lineup").get_data(as_text=True)
nav = empty_line.split("</main>", 1)[-1]
ok("Nothing on the Lineup yet." in empty_line and "No team trips yet." not in empty_line and "Add event" not in empty_line and ">Suggest an event</a>" not in empty_line and ">Create event</a>" not in empty_line and 'aria-label="Create event"' in empty_line and 'href="/events/new"' in empty_line and "btn-primary full" not in empty_line and "Water Polo Practice" not in empty_line and 'aria-label="Lineup"' in nav and ">Lineup</a>" not in nav and 'href="/practices#schedule"' not in nav and "data-badge=schedule" in nav and ">All</a>" in empty_line and ">Competitions</a>" in empty_line and ">Training</a>" in empty_line and ">Trips</a>" in empty_line and ">Community</a>" in empty_line and "<h2>My events</h2>" not in empty_line and "<h2>Interested</h2>" not in empty_line and jane.post("/lineup/new", data=dict(csrf=csrf(jane, "/lineup/new"), mode="create", category="social", title="Secret", location="Pool", description="Nope.", date=A.today_pt().isoformat(), start_time="09:00")).status_code == 403 and A.app.test_client().get("/lineup/new").status_code == 302 and jane.get("/lineup/new?mode=propose").status_code == 200, "Lineup replaces Schedule and members cannot publish events")
soon_day = (A.today_pt() + dt.timedelta(days=10)).isoformat()
soon_end = (A.today_pt() + dt.timedelta(days=13)).isoformat()
later_day = (A.today_pt() + dt.timedelta(days=40)).isoformat()
past_ev = (A.today_pt() - dt.timedelta(days=20)).isoformat()
def ev(**kw):
    base = dict(category="social", subtype="Happy hour", hosting="Hosting", title="Club Hour", location="Grunions Pool", city="Huntington Beach", description="Come by.", date=soon_day, start_time="18:00", end_time="20:00", official="1", mode="create")
    base.update(kw)
    return base
made = eli.post("/lineup/new", data=dict(csrf=csrf(eli, "/lineup/new"), **ev(title="Club Hour")), follow_redirects=True).get_data(as_text=True)
eid = D.execute("SELECT id, official, status, team_intent FROM lineup_events WHERE title='Club Hour'").fetchone()
ok("Club Hour" in made and eid[1] == 1 and eid[2] == "published" and eid[3] in ("", None) and "Official trip" in made and "Hosting · Social" in made and "class=chip-info>Hosting</span>" not in made and "Happy hour" not in made, "an organizer publishes an official club event directly")
eli.post("/lineup/new", data=dict(csrf=csrf(eli, "/lineup/new"), **ev(category="travel", subtype="Tournament", hosting="Away", title="Winter Cup", team_intent="official", city="Long Beach", location="Belmont Plaza", date=soon_day, end_date=soon_end, start_time="09:00", link="https://example.com/cup", description="Bring caps.")))
cup_id = D.execute("SELECT id FROM lineup_events WHERE title='Winter Cup'").fetchone()[0]
eli.post("/lineup/new", data=dict(csrf=csrf(eli, "/lineup/new"), **ev(category="service", subtype="Volunteering", title="Beach Cleanup", date=past_ev, end_date=past_ev, start_time="10:00", location="Leadbetter Beach", city="Santa Barbara", description="Already happened.")))
backwards = eli.post("/lineup/new", data=dict(csrf=csrf(eli, "/lineup/new"), **ev(title="Backwards", date=later_day, end_date=soon_day, location="Reno Pool")), follow_redirects=True).get_data(as_text=True)
rejected = eli.post("/lineup/new", data=dict(csrf=csrf(eli, "/lineup/new"), **ev(category="practice", title="Local Game", location="Marina High School")), follow_redirects=True).get_data(as_text=True)
listed = eli.get("/lineup").get_data(as_text=True)
cup_page = eli.get("/lineup/%d" % cup_id).get_data(as_text=True)
ok("End date must be on or after the start date." in backwards and "Practices and local games stay off the Lineup." in rejected and not D.execute("SELECT 1 FROM lineup_events WHERE title='Backwards' OR title='Local Game'").fetchone() and "Winter Cup" in listed and "Beach Cleanup" in listed.split("<details class=lineuppast>", 1)[-1] and "Beach Cleanup" not in listed.split("<details class=lineuppast>", 1)[0] and "Bring caps." not in listed and "maps/search/" not in listed and ">Edit</a>" not in listed.split("<h2>My events", 1)[0] and "class=datetile" in listed and "Bring caps." in cup_page and "maps/dir/?api=1&amp;destination=Belmont%20Plaza%2C%20Long%20Beach" in cup_page and ">Directions</span>" not in cup_page and "loccard" in cup_page and ">Who's in</h2>" not in cup_page and ">Edit</a>" in cup_page.split("<main>", 1)[0] and jane.get("/lineup/%d" % cup_id).status_code == 200 and "Water Polo Practice" not in listed, "Lineup cards stay light and the event page keeps the description, directions, and Edit")
eli.post("/lineup/new", data=dict(csrf=csrf(eli, "/lineup/new"), **ev(category="travel", subtype="Tournament", hosting="Away", title="Org Cup", team_intent="official", host_org="IGLA+", location="Harbor", description="Away cup.", date=soon_day, start_time="09:00")))
org_id = D.execute("SELECT id FROM lineup_events WHERE title='Org Cup'").fetchone()[0]
eli.post("/lineup/new", data=dict(csrf=csrf(eli, "/lineup/new"), **ev(category="social", subtype="Happy hour", hosting="Hosting", title="Home Social", host_org="Nope", location="Clubhouse", description="We host.", date=soon_day, start_time="18:00")))
home_id = D.execute("SELECT id, COALESCE(host_org,'') FROM lineup_events WHERE title='Home Social'").fetchone()
org_feed = eli.get("/lineup").get_data(as_text=True)
org_card = org_feed.split("Org Cup", 1)[1].split('class="card tap tripcard"', 1)[0]
jane.post("/lineup", data=dict(csrf=csrf(jane, "/lineup"), event_id=org_id, action="going"))
org_page = eli.get("/lineup/%d" % org_id).get_data(as_text=True)
home_edit = eli.get("/lineup/%d/edit" % home_id[0]).get_data(as_text=True)
ok(D.execute("SELECT host_org, hosting FROM lineup_events WHERE id=?", (org_id,)).fetchone() == ("IGLA+", "Attending") and "Hosted by IGLA+" in org_card and "Away cup." not in org_card and "Hosted by IGLA+" in org_page and "Who" in org_page and "going" in org_page and "Jay Doe" in org_page and home_id[1] == "" and "Hosted by Nope" not in org_feed and "id=lineOrg hidden" in home_edit and "Host organization" in eli.get("/lineup/new").get_data(as_text=True), "an Away event can name its host organization, and a Hosting event hides that field")
jane.post("/lineup", data=dict(csrf=csrf(jane, "/lineup"), event_id=cup_id, action="going"))
eli.post("/lineup", data=dict(csrf=csrf(jane, "/lineup"), event_id=cup_id, action="interested"))
cup = jane.get("/lineup").get_data(as_text=True).split("Winter Cup", 1)[1].split('class="card tap tripcard"', 1)[0]
jane_prof = jane.get("/profile").get_data(as_text=True)
jane_int = jane.get("/profile?tab=lineup").get_data(as_text=True)
jane_member = eli.get("/admin/member/%d" % D.execute("SELECT id FROM members WHERE email='jane@example.com'").fetchone()[0]).get_data(as_text=True)
ok("</svg>Going</button>" in cup and ">Interested</button>" in cup and ">Not going</button>" in cup and "I'm Going" not in cup and "I'm Interested" not in cup and D.execute("SELECT state FROM lineup_rsvps WHERE event_id=? AND member_id=(SELECT id FROM members WHERE email='jane@example.com')", (cup_id,)).fetchone()[0] == "going" and "<h2>Interested</h2>" not in jane.get("/lineup").get_data(as_text=True) and ">General</a>" in jane_prof and 'href="/profile?tab=lineup"' in jane_prof and ">My Lineup</a>" in jane_prof and ">Hosting</a>" not in jane_prof and "Winter Cup" in jane_int and "Nothing yet." not in jane_int and "class=\"card tap tripcard\"" in jane_int and "aria-label=\"Profile\"" not in jane_member, "Going and Interested are separate RSVPs, and Interested lives on the profile")
edit = eli.get("/lineup/%d/edit" % cup_id).get_data(as_text=True)
edit_head = edit.split("<main>", 1)[0]
ok(">Cancel</a>" in edit_head and ">Save</button>" in edit_head and "<h1>Event</h1>" in edit_head and "button.savebtn{color:var(--accent)" in edit and 'value="Winter Cup"' in edit and "name=event_type" in edit and "name=category" not in edit and ">Tournament</option>" in edit and "Banner image" in edit and ">Exact dates</span>" in edit and jane.get("/lineup/%d/edit" % cup_id).status_code == 403 and jane.post("/lineup/%d/edit" % cup_id, data=dict(csrf=csrf(jane, "/lineup"), mode="edit", category="social", title="Hijack", location="X", description="No.", date=soon_day, start_time="09:00")).status_code == 403, "admins edit an event with Cancel on the left and blue Save on the right")
detail = jane.get("/lineup/%d" % cup_id).get_data(as_text=True)
ok(">Event</h1>" in detail.split("<main>", 1)[0] and "Official trip" in detail and "class=chip-info>Official" not in detail and "Belmont Plaza" in detail and ">Registration</a>" in detail and "Attending · Tournament" in detail, "the event page reads like a practice profile")
sug = jane.post("/lineup/new", data=dict(csrf=csrf(jane, "/lineup/new?mode=suggest"), mode="suggest", category="social", subtype="Party", title="Birthday Party", location="Jane's place", description="Cake after practice.", date=soon_day, start_time="20:00", official="1", team_intent="official"), follow_redirects=True)
pid_party = D.execute("SELECT id, status, official, host_id, team_intent FROM lineup_events WHERE title='Birthday Party'").fetchone()
jane_id = D.execute("SELECT id FROM members WHERE email='jane@example.com'").fetchone()[0]
public = eli.get("/lineup").get_data(as_text=True)
jane_mine = jane.get("/profile?tab=hosting").get_data(as_text=True)
ok(sug.status_code == 200 and pid_party[1] == "pending" and pid_party[2] == 0 and pid_party[3] == jane_id and (pid_party[4] or "") == "" and "Birthday Party" not in public and "Birthday Party" not in jane.get("/lineup").get_data(as_text=True) and "Birthday Party" in jane_mine and "Pending approval" in jane_mine and ">Hosting</a>" in jane_mine and ">General</a>" in jane_mine, "a member suggestion stays pending, unofficial, and off the public Lineup")
ok(jane.post("/lineup/new", data=dict(csrf=csrf(jane, "/lineup/new?mode=suggest"), mode="suggest", category="travel", subtype="Tournament", title="Sneaky Cup", location="Pool", description="No.", date=soon_day, start_time="09:00"), follow_redirects=True).get_data(as_text=True).find("for organizers") >= 0 and not D.execute("SELECT 1 FROM lineup_events WHERE title='Sneaky Cup'").fetchone(), "members cannot suggest a tournament")
queue = eli.get("/admin/approvals").get_data(as_text=True)
ok(">Events</a>" in eli.get("/admin").get_data(as_text=True).split("<main>", 1)[0] and "Needs review" in queue and "Birthday Party" in queue and "Approve &amp; Publish" in queue and "<h1>Events</h1>" in queue and 'class="btn quiet pageact" href="/events/new">Create event</a>' in queue and 'class=pagehead' in queue and "<h1>Schedule</h1>" in eli.get("/admin").get_data(as_text=True) and 'class="btn quiet pageact" href=/members.csv>Export CSV</a>' in eli.get("/members").get_data(as_text=True) and "What are you planning?" not in queue and "Team schedule" not in queue and ">Scrimmage</a>" not in queue and "What are you planning?" in eli.get("/events/new").get_data(as_text=True) and ">Scrimmage</span>" in eli.get("/events/new").get_data(as_text=True) and "Team schedule" in eli.get("/events/new").get_data(as_text=True) and "Preview event" in eli.get("/events/new").get_data(as_text=True) and "Appears on Home by default" in eli.get("/events/new").get_data(as_text=True) and "Water Polo Practice" in eli.get("/events/new").get_data(as_text=True) and "Team schedule" not in jane.get("/events/new").get_data(as_text=True) and "Appears on Lineup by default" in jane.get("/events/new").get_data(as_text=True) and jane.get("/admin/approvals").status_code == 403, "admins review suggestions from the Events tab")
eli.post("/admin/approvals", data=dict(csrf=csrf(eli, "/admin/approvals"), event_id=pid_party[0], action="changes", note="Add a meeting point"))
ok(D.execute("SELECT status, review_note FROM lineup_events WHERE id=?", (pid_party[0],)).fetchone() == ("changes_requested", "Add a meeting point") and "Changes requested" in jane.get("/profile?tab=hosting").get_data(as_text=True) and "Birthday Party" not in jane.get("/lineup").get_data(as_text=True), "requesting changes tells the host and hides the event")
jane.post("/lineup/%d/edit" % pid_party[0], data=dict(csrf=csrf(jane, "/lineup/%d/edit" % pid_party[0]), mode="edit", category="social", subtype="Party", title="Birthday Party", location="Pier", description="Cake after practice.", date=soon_day, start_time="20:00", official="1"))
ok(D.execute("SELECT status, official, city, venue FROM lineup_events WHERE id=?", (pid_party[0],)).fetchone() == ("pending", 0, "Pier", ""), "resubmitting keeps the event unofficial")
eli.post("/admin/approvals", data=dict(csrf=csrf(eli, "/admin/approvals"), event_id=pid_party[0], action="approve"))
approved = jane.get("/lineup").get_data(as_text=True)
party_page = jane.get("/lineup/%d" % pid_party[0]).get_data(as_text=True)
ok(D.execute("SELECT status, official FROM lineup_events WHERE id=?", (pid_party[0],)).fetchone() == ("published", 0) and "Birthday Party" in approved and "Community" in party_page and "Member event" not in party_page and "Official trip" not in party_page, "approving publishes a member event without making it official")
note = D.execute("SELECT body FROM notices WHERE member_id=? ORDER BY id DESC LIMIT 1", (jane_id,)).fetchone()
ok(note and "Birthday Party" in note[0] and "on the Lineup" in note[0], "the host is told their event was approved")
prev_john = D.execute("SELECT role, is_admin FROM members WHERE email='john@example.com'").fetchone()
D.execute("UPDATE members SET role='coach', is_admin=0 WHERE email='john@example.com'"); D.commit()
prop = john.post("/lineup/new", data=dict(csrf=csrf(john, "/lineup/new?mode=propose"), mode="propose", category="social", title="IGLA", location="San Diego", description="Gauging a trip.", date=later_day, start_time="09:00", end_date=later_day, hosting="Away"), follow_redirects=True).get_data(as_text=True)
igla = D.execute("SELECT id, status, official, team_intent, category_id FROM lineup_events WHERE title='IGLA'").fetchone()
travel_id = D.execute("SELECT id FROM lineup_categories WHERE slug='travel'").fetchone()[0]
ok(igla[1] == "published" and igla[2] == 1 and igla[3] == "considering" and igla[4] == travel_id and ">Interested<" in prop and "Considering" in prop and "Make official" in prop and ">Create event</a>" not in john.get("/lineup").get_data(as_text=True) and 'aria-label="Create event"' in john.get("/lineup").get_data(as_text=True) and "href=\"/events/new\"" in john.get("/lineup").get_data(as_text=True), "a coach can propose a tournament that starts as Considering")
jane.post("/lineup", data=dict(csrf=csrf(jane, "/lineup"), event_id=igla[0], action="interested"))
home_before = jane.get("/home").get_data(as_text=True)
card_before = home_before[home_before.find('class="card tap nextcard"'):home_before.find("id=schedule")]
john.post("/lineup/%d" % igla[0], data=dict(csrf=csrf(john, "/lineup/%d" % igla[0]), action="official"))
ok(D.execute("SELECT team_intent FROM lineup_events WHERE id=?", (igla[0],)).fetchone()[0] == "official" and D.execute("SELECT state FROM lineup_rsvps WHERE event_id=? AND member_id=?", (igla[0], jane_id)).fetchone()[0] == "interested" and "official Grunions event" in D.execute("SELECT body FROM notices WHERE member_id=? ORDER BY id DESC LIMIT 1", (jane_id,)).fetchone()[0] and "IGLA" not in card_before, "promoting to Official keeps the Interested RSVP and does not put it on Home")
_now = A.wall_pt().replace(second=0, microsecond=0)
_estart = dt.datetime.combine(_now.date(), dt.time(0, 0))
_eend = dt.datetime.combine(_now.date(), dt.time(23, 30))
if _now >= _eend:
    _estart, _eend = dt.datetime.combine(_now.date(), dt.time(23, 0)), dt.datetime.combine(_now.date(), dt.time(23, 59))
early, early_end = _estart.date().isoformat(), _eend.date().isoformat()
eli.post("/lineup/new", data=dict(csrf=csrf(eli, "/lineup/new"), **ev(category="travel", subtype="Tournament", hosting="Away", title="Sunday Cup", team_intent="official", date=early, end_date=early_end, start_time="%02d:%02d" % (_estart.hour, _estart.minute), end_time="%02d:%02d" % (_eend.hour, _eend.minute), location="Early Pool", description="A multi-day trip.")))
sun_id = D.execute("SELECT id FROM lineup_events WHERE title='Sunday Cup'").fetchone()[0]
jane.post("/lineup", data=dict(csrf=csrf(jane, "/lineup"), event_id=sun_id, action="interested"))
still = jane.get("/home").get_data(as_text=True)
still_card = still[still.find('class="card tap nextcard"'):still.find("id=schedule")]
ok("Sunday Cup" not in still_card and "class=nxtitle>Water Polo Practice</div>" in still_card, "Interested does not replace the practice on Home")
jane.post("/lineup", data=dict(csrf=csrf(jane, "/lineup"), event_id=sun_id, action="going"))
bumped = jane.get("/home").get_data(as_text=True)
_b0 = bumped.find('class="card tap nextcard"')
bumped_card = bumped[_b0:bumped.find("id=schedule", _b0)]
ok("Sunday Cup" in bumped_card and "Official club event" in bumped_card and "I'm going ✓" in bumped_card and "HAPPENING NOW" in bumped_card and "nxsocial" not in bumped_card, "Going on an official trip can become the Home card")
eli.post("/lineup/%d/edit" % sun_id, data=dict(csrf=csrf(eli, "/lineup/%d/edit" % sun_id), mode="edit", category="travel", subtype="Tournament", hosting="Away", team_intent="official", official="1", title="Sunday Cup", location="Moved Pool", description="A multi-day trip.", date=early, end_date=early_end, start_time="%02d:%02d" % (_estart.hour, _estart.minute), end_time="%02d:%02d" % (_eend.hour, _eend.minute)))
moved_note = D.execute("SELECT body FROM notices WHERE member_id=? AND body LIKE '%Sunday Cup%' ORDER BY id DESC LIMIT 1", (jane_id,)).fetchone()
ok(moved_note and "new date or location" in moved_note[0], "moving a published event tells people who were going")
jane.post("/lineup", data=dict(csrf=csrf(jane, "/home"), event_id=sun_id, action="clear", back="/home"))
restored = jane.get("/home").get_data(as_text=True)
ok("Sunday Cup" not in restored[restored.find('class="card tap nextcard"'):restored.find("id=schedule")] and "class=nxtitle>Water Polo Practice</div>" in restored, "clearing Going puts the practice back on Home")
eli.post("/lineup/%d/edit" % sun_id, data=dict(csrf=csrf(eli, "/lineup/%d/edit" % sun_id), action="cancel", mode="edit", category="travel", title="Sunday Cup", location="Moved Pool", description="A multi-day trip.", date=early, start_time="%02d:%02d" % (_estart.hour, _estart.minute)))
ok(D.execute("SELECT status FROM lineup_events WHERE id=?", (sun_id,)).fetchone()[0] == "canceled" and "Sunday Cup" not in eli.get("/lineup").get_data(as_text=True).split("<h2>My events", 1)[0], "canceling removes the event from the public Lineup")
john.post("/lineup/%d/edit" % igla[0], data=dict(csrf=csrf(john, "/lineup/%d/edit" % igla[0]), action="delete"))
ok(not D.execute("SELECT 1 FROM lineup_events WHERE id=?", (igla[0],)).fetchone(), "a coach can delete a lineup event")
D.execute("UPDATE members SET role=?, is_admin=? WHERE email='john@example.com'", (prev_john[0], prev_john[1])); D.commit()
old = sqlite3.connect(":memory:")
old.execute("CREATE TABLE lineup_events(id INTEGER PRIMARY KEY, kind TEXT NOT NULL, title TEXT NOT NULL, date TEXT NOT NULL, start TEXT, location TEXT, description TEXT, link TEXT)")
old.execute("INSERT INTO lineup_events(kind, title, date, start, location) VALUES('Social','Old','2026-01-01','12:00','Park')")
old.execute("INSERT INTO lineup_events(kind, title, date, start, location) VALUES('Tournament','Cup','2026-02-01','09:00','Pool')")
old.execute("INSERT INTO lineup_events(kind, title, date, start, location) VALUES('Team trip/Social','Dinner','2026-03-01','18:00','Hall')")
A.migrate_lineup(old)
ok(old.execute("SELECT hosting, kind, stage FROM lineup_events ORDER BY id").fetchall() == [("Attending", "Clinic", "going"), ("Attending", "Tournament", "going"), ("Attending", "Clinic", "going")], "older lineup rows become Away clinics or tournaments")
ok(old.execute("SELECT status FROM lineup_events WHERE title='Cup'").fetchone()[0] == "published", "older lineup rows are published into the feed")
old.execute("INSERT INTO lineup_events(kind, title, date, city, venue, hosting, stage, status) VALUES('Tournament','Dup','2026-04-01','Toronto, Canada','Toronto, Canada','Away','going','published')")
A.migrate_lineup(old)
ok(old.execute("SELECT city, COALESCE(venue,'') FROM lineup_events WHERE title='Dup'").fetchone() == ("Toronto, Canada", "") and old.execute("SELECT city, COALESCE(venue,'') FROM lineup_events WHERE title='Old'").fetchone() == ("Park", ""), "a repeated city and venue collapse into City")
draft = eli.post("/lineup/new", data=dict(csrf=csrf(eli, "/lineup/new"), **ev(title="Quiet Draft", action="draft", mode="draft")), follow_redirects=True)
draft_id = D.execute("SELECT id, status FROM lineup_events WHERE title='Quiet Draft'").fetchone()
ok(draft_id[1] == "draft" and jane.get("/lineup/%d" % draft_id[0]).status_code == 404 and "Quiet Draft" not in jane.get("/lineup").get_data(as_text=True), "a draft stays off the Lineup for members")
date_form = eli.get("/lineup/new").get_data(as_text=True)
ok(">Exact dates</span>" in date_form and ">Month only</span>" in date_form and date_form.find(">Month only</span>") < date_form.find(">Starts<input") and date_form.find("name=date_precision") < date_form.find(">Starts<input") and "type=month name=month" in date_form and "name=date_part" in date_form and ">Early</option>" in date_form and ">Mid</option>" in date_form and ">Late</option>" in date_form and "id=exactDates" in date_form and "id=monthDates" in date_form and date_form.find("name=city") < date_form.find("name=venue") and "Toronto, Canada" in date_form, "the event form puts Exact dates and Month only directly above Starts")
ok(D.execute("SELECT date_precision FROM lineup_events WHERE title='Club Hour'").fetchone()[0] == "exact", "an event without a precision stays on exact dates")
_tba = A.today_pt().replace(day=1)
_tba_end = (dt.date(_tba.year + 1, 1, 1) if _tba.month == 12 else dt.date(_tba.year, _tba.month + 1, 1)) - dt.timedelta(days=1)
_tba_label = _tba.strftime("%B") + " " + str(_tba.year) + " · Dates TBA"
eli.post("/lineup/new", data=dict(csrf=csrf(eli, "/lineup/new"), **ev(title="March First Cup", category="travel", subtype="Tournament", hosting="Away", team_intent="official", date="2027-03-01", end_date="2027-03-01", start_time="09:00", location="First Pool", description="Opening day.")))
eli.post("/lineup/new", data=dict(csrf=csrf(eli, "/lineup/new"), **ev(title="Early Spring Cup", category="travel", subtype="Tournament", hosting="Away", team_intent="official", date_precision="month", month="2027-03", date_part="early", date="", start_time="", location="Spring Pool", description="Early in March.")))
eli.post("/lineup/new", data=dict(csrf=csrf(eli, "/lineup/new"), **ev(title="Late March Meet", category="travel", subtype="Tournament", hosting="Away", team_intent="official", date="2027-03-18", end_date="2027-03-18", start_time="09:00", location="Late Pool", description="Later in March.")))
eli.post("/lineup/new", data=dict(csrf=csrf(eli, "/lineup/new"), **ev(title="Dates Later Cup", category="travel", subtype="Tournament", hosting="Away", team_intent="official", date_precision="month", month=_tba.strftime("%Y-%m"), date="", start_time="", location="Somewhere", description="Dates later.")))
bad_month = eli.post("/lineup/new", data=dict(csrf=csrf(eli, "/lineup/new"), **ev(title="No Month", date_precision="month", month="2027-13", date="", start_time="")), follow_redirects=True).get_data(as_text=True)
spring = D.execute("SELECT date, end_date, date_precision, date_part, COALESCE(start_time,'') FROM lineup_events WHERE title='Early Spring Cup'").fetchone()
later_row = D.execute("SELECT id, date, end_date, date_precision, date_part, COALESCE(start_time,'') FROM lineup_events WHERE title='Dates Later Cup'").fetchone()
later_id = later_row[0]
feed = eli.get("/lineup").get_data(as_text=True)
feed_up = feed.split("<details class=lineuppast>", 1)[0]
early_card = feed_up.split("Early Spring Cup", 1)[1].split('class="card tap tripcard"', 1)[0]
later_card = feed_up.split("Dates Later Cup", 1)[1].split('class="card tap tripcard"', 1)[0]
first_card = feed_up.split("March First Cup", 1)[1].split('class="card tap tripcard"', 1)[0]
month_edit = eli.get("/lineup/%d/edit" % later_id).get_data(as_text=True)
ok("Choose a month." in bad_month and not D.execute("SELECT 1 FROM lineup_events WHERE title='No Month'").fetchone() and spring == ("2027-03-01", "2027-03-31", "month", "early", "") and later_row[1] == _tba.isoformat() and later_row[2] == _tba_end.isoformat() and later_row[3] == "month" and (later_row[4] or "") == "" and later_row[5] == "" and "Early March 2027 · Dates TBA" in early_card and _tba_label in later_card and "Early " + _tba_label not in later_card and "Dates TBA" not in first_card and "9:00 AM" in first_card and feed_up.find("Early Spring Cup") < feed_up.find("March First Cup") < feed_up.find("Late March Meet") and "name=date_precision value=month checked" in month_edit and ('value="%s"' % _tba.strftime("%Y-%m")) in month_edit, "month-only events say dates are TBA and sort at the start of that month")
jane.post("/lineup", data=dict(csrf=csrf(jane, "/lineup"), event_id=later_id, action="interested"))
home_interest = jane.get("/home").get_data(as_text=True)
hi = home_interest.find('class="card tap nextcard"')
interest_card = home_interest[hi:home_interest.find("id=schedule", hi)]
ok(D.execute("SELECT state FROM lineup_rsvps WHERE event_id=? AND member_id=?", (later_id, jane_id)).fetchone()[0] == "interested" and "Dates Later Cup" not in interest_card, "Interested is allowed on a month-only event and stays off Home")
jane.post("/lineup", data=dict(csrf=csrf(jane, "/lineup"), event_id=later_id, action="going"))
sam.post("/lineup", data=dict(csrf=csrf(sam, "/lineup"), event_id=later_id, action="interested"))
D.execute("UPDATE lineup_events SET capacity=1 WHERE id=?", (later_id,)); D.commit()
eli.post("/lineup", data=dict(csrf=csrf(eli, "/lineup"), event_id=later_id, action="going"))
home_going = jane.get("/home").get_data(as_text=True)
hg = home_going.find('class="card tap nextcard"')
going_card = home_going[hg:home_going.find("id=schedule", hg)]
_busy = {r[0] for r in D.execute("SELECT date FROM practices WHERE cancelled=0")}
for _start, _end in D.execute("SELECT date, COALESCE(NULLIF(end_date,''), date) FROM lineup_events WHERE status='published' AND COALESCE(date_precision,'exact')!='month'"):
    _a, _b = dt.date.fromisoformat(str(_start)[:10]), dt.date.fromisoformat(str(_end)[:10])
    if (_b - _a).days > 21: _b = _a + dt.timedelta(days=21)
    while _a <= _b:
        _busy.add(_a.isoformat()); _a += dt.timedelta(days=1)
_probe, _cursor = None, _tba
while _cursor <= _tba_end:
    if _cursor.isoformat() not in _busy:
        _probe = _cursor.isoformat(); break
    _cursor += dt.timedelta(days=1)
admin_mid = eli.get("/admin?date=" + _probe).get_data(as_text=True)
_sched = sqlite3.connect(os.environ["GRUNIONS_DB"]); _sched.row_factory = sqlite3.Row
ok(_probe and D.execute("SELECT state FROM lineup_rsvps WHERE event_id=? AND member_id=?", (later_id, jane_id)).fetchone()[0] == "going" and D.execute("SELECT state FROM lineup_rsvps WHERE event_id=? AND member_id=(SELECT id FROM members WHERE email='eli@example.com')", (later_id,)).fetchone()[0] == "waitlist" and "Dates Later Cup" not in going_card and "class=nxtitle>Water Polo Practice</div>" in going_card and "Dates Later Cup" not in admin_mid and _probe not in A.schedule_days(_sched), "a month-only event never becomes Next Up or a schedule day")
_now = A.wall_pt().replace(second=0, microsecond=0)
_estart = dt.datetime.combine(_now.date(), dt.time(0, 0))
_eend = dt.datetime.combine(_now.date(), dt.time(23, 30))
if _now >= _eend:
    _estart, _eend = dt.datetime.combine(_now.date(), dt.time(23, 0)), dt.datetime.combine(_now.date(), dt.time(23, 59))
_jane_prev = D.execute("SELECT COALESCE(MAX(id),0) FROM notices WHERE member_id=?", (jane_id,)).fetchone()[0]
_sam_id = D.execute("SELECT id FROM members WHERE email='sam@example.com'").fetchone()[0]
_eli_id = D.execute("SELECT id FROM members WHERE email='eli@example.com'").fetchone()[0]
_sam_prev = D.execute("SELECT COALESCE(MAX(id),0) FROM notices WHERE member_id=?", (_sam_id,)).fetchone()[0]
_eli_prev = D.execute("SELECT COALESCE(MAX(id),0) FROM notices WHERE member_id=?", (_eli_id,)).fetchone()[0]
eli.post("/lineup/%d/edit" % later_id, data=dict(csrf=csrf(eli, "/lineup/%d/edit" % later_id), mode="edit", category="travel", subtype="Tournament", hosting="Away", team_intent="official", official="1", title="Dates Later Cup", location="Somewhere", description="Dates later.", date_precision="exact", date=_estart.date().isoformat(), end_date=_eend.date().isoformat(), start_time="%02d:%02d" % (_estart.hour, _estart.minute), end_time="%02d:%02d" % (_eend.hour, _eend.minute)))
_when = A.lineup_when_label(_sched.execute("SELECT * FROM lineup_events WHERE id=?", (later_id,)).fetchone())
_jane_notes = [r[0] for r in D.execute("SELECT body FROM notices WHERE member_id=? AND id>?", (jane_id, _jane_prev))]
_sam_notes = [r[0] for r in D.execute("SELECT body FROM notices WHERE member_id=? AND id>?", (_sam_id, _sam_prev))]
_eli_notes = [r[0] for r in D.execute("SELECT body FROM notices WHERE member_id=? AND id>?", (_eli_id, _eli_prev))]
_dated = "Dates Later Cup now has dates: %s." % _when
home_dated = jane.get("/home").get_data(as_text=True)
hd = home_dated.find('class="card tap nextcard"')
dated_card = home_dated[hd:home_dated.find("id=schedule", hd)]
admin_exact = eli.get("/admin?date=" + _estart.date().isoformat()).get_data(as_text=True)
ok(_jane_notes == [_dated] and _sam_notes == [_dated] and _dated not in _eli_notes and "new date or location" not in " ".join(_jane_notes + _sam_notes + _eli_notes) and "Dates Later Cup" in dated_card and "Dates Later Cup" in admin_exact, "setting exact dates tells Interested and Going members and can then lead Home")
jane.post("/lineup", data=dict(csrf=csrf(jane, "/lineup"), event_id=later_id, action="clear"))
home_cleared = jane.get("/home").get_data(as_text=True)
hc = home_cleared.find('class="card tap nextcard"')
ok("Dates Later Cup" not in home_cleared[hc:home_cleared.find("id=schedule", hc)] and "class=nxtitle>Water Polo Practice</div>" in home_cleared, "clearing the dated event puts the practice back on Home")
for _title in ("Dates Later Cup", "Early Spring Cup", "Late March Meet", "March First Cup"):
    _rid = D.execute("SELECT id FROM lineup_events WHERE title=?", (_title,)).fetchone()[0]
    eli.post("/lineup/%d/edit" % _rid, data=dict(csrf=csrf(eli, "/lineup/%d/edit" % _rid), action="delete"))
cap_day = (A.today_pt() + dt.timedelta(days=12)).isoformat()
eli.post("/lineup/new", data=dict(csrf=csrf(eli, "/lineup/new"), **ev(title="Tiny Social", capacity="1", date=cap_day, location="Small Room", description="One spot.")))
tiny = D.execute("SELECT id FROM lineup_events WHERE title='Tiny Social'").fetchone()[0]
jane.post("/lineup", data=dict(csrf=csrf(jane, "/lineup"), event_id=tiny, action="going"))
eli.post("/lineup", data=dict(csrf=csrf(eli, "/lineup"), event_id=tiny, action="going"))
ok(D.execute("SELECT state FROM lineup_rsvps WHERE event_id=? AND member_id=(SELECT id FROM members WHERE email='eli@example.com')", (tiny,)).fetchone()[0] == "waitlist", "a full event waitlists the next Going reply")
sched = eli.get("/practices").get_data(as_text=True)
ok("Add a practice" not in sched and "Add a practice" not in eli.get("/home").get_data(as_text=True) and "name=repeat" not in sched.split("<main>", 1)[-1] and "Add a series" not in sched and jane.post("/practices", data=dict(csrf=csrf(jane, "/practices"), action="add", repeat="1", date=A.today_pt().isoformat(), location="Secret Pool")).status_code == 403, "practice creation stays off Home and Schedule, and members cannot add one")
s0 = A.today_pt()
wd_a, wd_b = s0.weekday(), (s0.weekday() + 2) % 7
s1 = s0 + dt.timedelta(days=13)
expect = []
day = s0
while day <= s1:
    if day.weekday() in (wd_a, wd_b): expect.append(day.isoformat())
    day += dt.timedelta(days=1)
eli_id = D.execute("SELECT id FROM members WHERE email='eli@example.com'").fetchone()[0]
D.execute("INSERT OR REPLACE INTO coaching_list(member_id, source) VALUES(?, 'manual')", (eli_id,)); D.commit()
eli.post("/practices", data=dict(csrf=csrf(eli, "/practices"), action="add", date=s0.isoformat(), start="18:00", end="19:15", location="One Off Pool", weekday=str(wd_a), end_date=s1.isoformat()))
one = D.execute("SELECT id, series_id FROM practices WHERE location='One Off Pool'").fetchone()
ok(one and one[1] is None and not D.execute("SELECT 1 FROM practice_series WHERE location='One Off Pool'").fetchone() and "Skip this date" not in eli.get("/practices/%d" % one[0]).get_data(as_text=True), "a practice without Repeat is a single date and cannot be skipped")
made_series = eli.post("/practices", data={"csrf": csrf(eli, "/practices"), "action": "add", "repeat": "1", "weekday": [str(wd_a), str(wd_b)], "start": "18:00", "end": "19:15", "location": "Series Pool", "date": s0.isoformat(), "end_date": s1.isoformat(), "coach": str(eli_id), "lead": str(eli_id)}, follow_redirects=True)
series_id = D.execute("SELECT id FROM practice_series WHERE location='Series Pool'").fetchone()[0]
rows = D.execute("SELECT id, date, start, series_detached FROM practices WHERE series_id=? ORDER BY date", (series_id,)).fetchall()
ok(made_series.status_code == 200 and [r[1] for r in rows] == expect and all(r[2] == "18:00" for r in rows) and D.execute("SELECT member_id, is_lead FROM practice_coaches WHERE practice_id=?", (rows[0][0],)).fetchone() == (eli_id, 1) and "Series Pool" in jane.get("/practices").get_data(as_text=True), "a series generates one practice per chosen weekday and copies its coaches")
skip_id = rows[1][0]
eli.post("/practices/%d" % skip_id, data=dict(csrf=csrf(eli, "/practices/%d" % skip_id), pid=skip_id, action="skip", back="page"))
ok(not D.execute("SELECT 1 FROM practices WHERE id=?", (skip_id,)).fetchone() and D.execute("SELECT 1 FROM series_skips WHERE series_id=? AND date=?", (series_id, rows[1][1])).fetchone() and jane.get("/practices/%d" % skip_id).status_code == 404, "skipping a date with no RSVPs removes it for members")
keep_id = rows[2][0]
jane.post("/practices/%d" % keep_id, data=dict(csrf=csrf(jane, "/practices/%d" % keep_id), pid=keep_id, action="going", back="page"))
eli.post("/practices/%d" % keep_id, data=dict(csrf=csrf(eli, "/practices/%d" % keep_id), pid=keep_id, action="skip", back="page"))
skipped_html = jane.get("/practices/%d" % keep_id).get_data(as_text=True)
ok(D.execute("SELECT cancelled, skipped FROM practices WHERE id=?", (keep_id,)).fetchone() == (1, 1) and "Cancelled" in skipped_html and "Skip this date" not in skipped_html, "skipping a date that already has RSVPs shows Cancelled")
first_id, first_day = rows[0][0], rows[0][1]
eli.post("/practices/%d" % first_id, data=dict(csrf=csrf(eli, "/practices/%d?edit=1" % first_id), pid=first_id, action="edit", back="page", series_scope="once", date=first_day, start="17:00", end="19:15", location="Series Pool", plan_fields="1", coach=str(eli_id), lead=str(eli_id)))
later_id, later_day = rows[3][0], rows[3][1]
ok(D.execute("SELECT start, location, series_detached FROM practices WHERE id=?", (first_id,)).fetchone() == ("17:00", "Series Pool", 1) and D.execute("SELECT start, series_detached FROM practices WHERE id=?", (later_id,)).fetchone() == ("18:00", 0), "editing one series date leaves the others alone")
eli.post("/practices/%d" % later_id, data=dict(csrf=csrf(eli, "/practices/%d?edit=1" % later_id), pid=later_id, action="edit", back="page", series_scope="following", date=later_day, start="18:30", end="19:45", location="Series East", plan_fields="1", coach=str(eli_id), lead=str(eli_id)))
ok(D.execute("SELECT location, start FROM practices WHERE id=?", (first_id,)).fetchone() == ("Series Pool", "17:00") and D.execute("SELECT location, start, series_detached FROM practices WHERE id=?", (later_id,)).fetchone() == ("Series East", "18:30", 0) and D.execute("SELECT location, start FROM practice_series WHERE id=?", (series_id,)).fetchone() == ("Series East", "18:30"), "this and following updates the series and later dates only")
import sports
ok(sports.pack_levels(["intermediate", "beginner", "nope"]) == "beginner,intermediate" and "developing" not in sports.pack_levels(["beginner", "intermediate"]) and sports.levels_label("beginner,developing,intermediate,experienced") == "All levels" and sports.levels_label("beginner,intermediate") == "Beginner · Intermediate" and sports.levels_label("") == "" and sports.divisions_label("open") == "Open to all" and sports.divisions_label("mens,coed,womens") == "Co-ed · Men's · Women's" and sports.activity_title("game", "Squid") == "Game vs. Squid" and sports.activity_title("hybrid", "", '[{"type":"practice","start":"19:00","end":"19:45"},{"type":"scrimmage","start":"19:45","end":"20:30"}]') == "Practice + Scrimmage", "skill levels are an exact set, not a range")
lv = D.execute("SELECT id, date, start, end, location FROM practices WHERE COALESCE(series_id,0)=0 AND cancelled=0 ORDER BY date LIMIT 1").fetchone()
eli.post("/practices/%d" % lv[0], data={"csrf": csrf(eli, "/practices/%d?edit=1" % lv[0]), "pid": lv[0], "action": "edit", "back": "page", "activity_type": "practice", "date": lv[1], "start": lv[2], "end": lv[3], "location": lv[4], "level": ["beginner", "intermediate"]})
lv_page = eli.get("/practices/%d" % lv[0]).get_data(as_text=True)
ok(D.execute("SELECT skill_levels FROM practices WHERE id=?", (lv[0],)).fetchone()[0] == "beginner,intermediate" and "class=\"t3 sm sportline\">Beginner · Intermediate</p>" in lv_page and "New to the sport or learning basic techniques" in lv_page and "developing" not in (D.execute("SELECT skill_levels FROM practices WHERE id=?", (lv[0],)).fetchone()[0]), "a practice stores Beginner and Intermediate without adding Developing")
eli.post("/practices/%d" % lv[0], data={"csrf": csrf(eli, "/practices/%d?edit=1" % lv[0]), "pid": lv[0], "action": "edit", "back": "page", "activity_type": "practice", "date": lv[1], "start": lv[2], "end": lv[3], "location": lv[4], "level": ["beginner", "developing", "intermediate", "experienced"], "division": ["open"]})
ok(D.execute("SELECT skill_levels, divisions FROM practices WHERE id=?", (lv[0],)).fetchone() == ("beginner,developing,intermediate,experienced", "open") and "All levels · Open to all" in eli.get("/practices/%d" % lv[0]).get_data(as_text=True), "all four levels render as All levels")
scr_day = (A.today_pt() + dt.timedelta(days=4)).isoformat()
eli.post("/practices", data=dict(csrf=csrf(eli, "/practices"), action="add", activity_type="scrimmage", date=scr_day, start="19:00", end="20:30", location="Scrimmage Pool", gameplay_notes="Work the press."))
scr = D.execute("SELECT id, activity_type FROM practices WHERE location='Scrimmage Pool'").fetchone()
eli.post("/practices", data=dict(csrf=csrf(eli, "/practices"), action="add", activity_type="game", date=scr_day, start="18:00", end="19:00", location="Game Pool", opponent="Squid", home_away="home"))
game = D.execute("SELECT id FROM practices WHERE location='Game Pool'").fetchone()[0]
hy_day = (A.today_pt() + dt.timedelta(days=5)).isoformat()
eli.post("/practices", data={"csrf": csrf(eli, "/practices"), "action": "add", "activity_type": "hybrid", "date": hy_day, "start": "19:00", "end": "20:30", "location": "Hybrid Pool", "segment_type": ["practice", "scrimmage"], "segment_start": ["19:00", "19:45"], "segment_end": ["19:45", "20:30"]})
hy = D.execute("SELECT id FROM practices WHERE location='Hybrid Pool'").fetchone()[0]
sched_types = jane.get("/home").get_data(as_text=True)
ok(scr[1] == "scrimmage" and "Scrimmage" in jane.get("/practices/%d" % scr[0]).get_data(as_text=True) and "Water Polo Game" in jane.get("/practices/%d" % game).get_data(as_text=True) and "vs. Squid" in jane.get("/practices/%d" % game).get_data(as_text=True) and "Practice + Scrimmage" in jane.get("/practices/%d" % hy).get_data(as_text=True) and "Work the press." in eli.get("/practices/%d?edit=1" % scr[0]).get_data(as_text=True) and jane.post("/practices/%d" % scr[0], data=dict(csrf=csrf(jane, "/practices/%d" % scr[0]), pid=scr[0], action="going")).status_code == 302, "scrimmage, game, and hybrid sessions keep one attendance list")
s2 = A.today_pt() + dt.timedelta(days=20)
s3 = s2 + dt.timedelta(days=14)
wd = s2.weekday()
eli.post("/practices", data={"csrf": csrf(eli, "/practices"), "action": "add", "repeat": "1", "weekday": [str(wd)], "start": "18:00", "end": "19:00", "location": "Repeat Pool", "date": s2.isoformat(), "end_date": s3.isoformat(), "activity_type": "practice"})
rep = D.execute("SELECT id, date FROM practices WHERE location='Repeat Pool' ORDER BY date").fetchall()
eli.post("/practices/%d" % rep[0][0], data=dict(csrf=csrf(eli, "/practices/%d?edit=1" % rep[0][0]), pid=rep[0][0], action="edit", back="page", series_scope="once", activity_type="scrimmage", date=rep[0][1], start="18:00", end="19:00", location="Repeat Pool"))
ok(D.execute("SELECT activity_type, series_detached FROM practices WHERE id=?", (rep[0][0],)).fetchone() == ("scrimmage", 1) and D.execute("SELECT activity_type FROM practices WHERE id=?", (rep[1][0],)).fetchone()[0] == "practice", "one series date can become a scrimmage without changing the series")
eli.post("/practices/%d" % rep[1][0], data=dict(csrf=csrf(eli, "/practices/%d?edit=1" % rep[1][0]), pid=rep[1][0], action="edit", back="page", series_scope="following", activity_type="scrimmage", date=rep[1][1], start="18:00", end="19:00", location="Repeat Pool"))
ok(D.execute("SELECT activity_type FROM practices WHERE id=?", (rep[0][0],)).fetchone()[0] == "scrimmage" and D.execute("SELECT activity_type FROM practices WHERE id=?", (rep[1][0],)).fetchone()[0] == "scrimmage" and D.execute("SELECT activity_type FROM practice_series WHERE location='Repeat Pool'").fetchone()[0] == "scrimmage", "this and following changes the later occurrences")
cup_sports = (A.today_pt() + dt.timedelta(days=15)).isoformat()
eli.post("/lineup/new", data={"csrf": csrf(eli, "/lineup/new"), "mode": "create", "category": "travel", "subtype": "Tournament", "hosting": "Away", "team_intent": "official", "official": "1", "title": "Level Cup", "location": "Belmont", "description": "Selected levels.", "date": cup_sports, "start_time": "09:00", "level": ["intermediate", "experienced"], "division": ["mens", "womens", "coed"], "comp_format": "per_team"})
level_id = D.execute("SELECT id FROM lineup_events WHERE title='Level Cup'").fetchone()[0]
level_cup = eli.get("/lineup").get_data(as_text=True)
cup_card = level_cup.split("Level Cup", 1)[1].split('class="card tap tripcard"', 1)[0]
cup_page = eli.get("/lineup/%d" % level_id).get_data(as_text=True)
ok("sportline" not in cup_card and "Intermediate · Experienced" in cup_page and "Co-ed" in cup_page and "Men&#39;s" in cup_page and "Women&#39;s" in cup_page and "per team" in cup_page and "Per Team" not in cup_page and "Beginner" not in cup_page and D.execute("SELECT skill_levels, divisions, comp_format FROM lineup_events WHERE title='Level Cup'").fetchone() == ("intermediate,experienced", "coed,mens,womens", "per_team") and jane.post("/lineup", data=dict(csrf=csrf(jane, "/lineup"), event_id=level_id, action="interested")).status_code == 302, "a tournament keeps levels, divisions, and registration separate from RSVP")
twin = (A.today_pt() + dt.timedelta(days=45)).isoformat()
eli.post("/practices", data=dict(csrf=csrf(eli, "/practices"), action="add", activity_type="practice", date=twin, start="18:00", end="19:00", location="Twin Practice Pool"))
eli.post("/practices", data=dict(csrf=csrf(eli, "/practices"), action="add", activity_type="scrimmage", date=twin, start="19:15", end="20:15", location="Twin Scrimmage Pool"))
eli.post("/lineup/new", data=dict(csrf=csrf(eli, "/lineup/new"), mode="create", category="social", subtype="Happy hour", hosting="Hosting", official="1", title="Twin Social", location="Twin Deck", description="After the session.", date=twin, start_time="20:30", end_time="21:30"))
prac_id = D.execute("SELECT id FROM practices WHERE location='Twin Practice Pool'").fetchone()[0]
scr_id = D.execute("SELECT id FROM practices WHERE location='Twin Scrimmage Pool'").fetchone()[0]
line_id = D.execute("SELECT id FROM lineup_events WHERE title='Twin Social'").fetchone()[0]
jane.post("/practices", data=dict(csrf=csrf(jane, "/practices"), pid=scr_id, action="going"))
both = eli.get("/admin?date=" + twin).get_data(as_text=True)
scr_admin = eli.get("/admin?date=%s&ev=p-%d" % (twin, scr_id)).get_data(as_text=True)
line_admin = eli.get("/admin?date=%s&ev=l-%d" % (twin, line_id)).get_data(as_text=True)
def _going(html):
    return html[html.find(">Going <"):html.find(">Everyone else <")]
_card = both.split('class="card evcard"', 1)[1].split("checkmeta", 1)[0]
_filt = both.split('aria-label="RSVP"', 1)[1].split("</div>", 1)[0]
_sched_bits = {
 "cards": both.count('class="card evcard"') == 1,
 "practice": "class=nxtitle>Water Polo Practice" in _card,
 "scrimmage": "Scrimmage" in both and "class=nxtitle>Scrimmage" not in _card,
 "social": "Twin Social" in both and "class=nxtitle>Twin Social" not in _card,
 "pool": "Twin Practice Pool" in _card,
 "details": ">Details</a>" not in both,
 "counter": ">1/3<" in both and ">2/3<" in scr_admin,
 "next": ("ev=p-%d" % scr_id) in both[max(0, both.find('aria-label="Next event"')-220):both.find('aria-label="Next event"')],
 "link": ('href="/practices/%d?from=admin"' % prac_id) in _card,
 "scr_title": "class=nxtitle>Water Polo Scrimmage" in scr_admin,
 "line_title": "class=nxtitle>Twin Social" in line_admin,
 "count": "checkprog" not in _filt and "Going (" in _filt and "Checked in (" in _filt,
 "search": both.find('aria-label="RSVP"') < both.find('placeholder="Search players..."') < both.find(">Going <"),
 "jane_scr": ('href="/admin/member/%d"' % jane_id) in _going(scr_admin),
 "jane_default": ('href="/admin/member/%d"' % jane_id) not in _going(both),
}
if not all(_sched_bits.values()):
    print("SCHED BITS", {k: v for k, v in _sched_bits.items() if not v})
ok(all(_sched_bits.values()), "each event that day is its own card, and the check-in count sits with the filters")
ds = eli.get("/design-system").get_data(as_text=True)
ok(jane.get("/design-system").status_code == 403 and "<h1>Regulars</h1>" in ds and "--color-bg: #090D0B" in ds and "--color-lime: #B2DE64" in ds and "--color-coral: #F48782" in ds and "--radius-card: 20px" in ds and "--radius-overlay: 24px" in ds and "--space-card: var(--space-3)" in ds and "btn-tertiary" in ds and "Expiring soon · expires in 3 days" in ds and "aria-label=\"Coach navigation\"" in ds and "aria-label=\"Member navigation\"" in ds and "aria-label=\"Admin\"" in ds and "aria-label=\"Home\"" in ds and "--nav-offset-bottom: 24px" in ds and "--nav-circle: 52px" in ds and "<h2>Segmented</h2>" in ds and "<h2>Field</h2>" in ds and "I'm going ✓" in ds and "--color-focus" in ds and "--color-map: var(--color-clubhouse)" in ds and "--color-sheet: var(--color-raised)" in ds and "<h2>Map, chat, and sheet</h2>" in ds and "data-theme=light" in ds, "admins can open the Regulars preview")
_wide = io.BytesIO(); Image.new("RGB", (4000, 2000), (12, 40, 80)).save(_wide, "PNG"); _wide.seek(0)
_bday = (A.today_pt() + dt.timedelta(days=16)).isoformat()
eli.post("/lineup/new", data=dict(csrf=csrf(eli, "/lineup/new"), mode="create", event_type="Tournament", hosting="Away", team_intent="official", title="Banner Cup", location="Banner Pool", description="A wide picture.", date=_bday, start_time="09:00", banner=(_wide, "wide.png")), follow_redirects=True)
_bid = D.execute("SELECT id, banner FROM lineup_events WHERE title='Banner Cup'").fetchone()
_bpage = eli.get("/lineup/%d" % _bid[0]).get_data(as_text=True)
_bim = Image.open(io.BytesIO(eli.get("/lineup-image/%d" % _bid[0]).data))
_bedit = eli.get("/lineup/%d/edit" % _bid[0]).get_data(as_text=True)
ok(_bid[1] and _bim.size[0] == 1600 and abs((_bim.size[0] / _bim.size[1]) - 1.5) < 0.02 and "evhero" in _bpage and "class=\"homemap cardmap still\"" in _bpage and "class=chip-info>Club" not in _bpage and "Attending · Tournament" in _bpage and "Replace" in _bedit and "banner_clear" in _bedit and "Banner image" in eli.get("/lineup/new").get_data(as_text=True).split(">Type<", 1)[0], "a banner is cropped to 3:2 and replaces the hero map")
eli.post("/lineup/%d/edit" % _bid[0], data=dict(csrf=csrf(eli, "/lineup/%d/edit" % _bid[0]), mode="edit", event_type="Tournament", hosting="Away", team_intent="official", title="Banner Cup", location="Banner Pool", description="A wide picture.", date=_bday, start_time="09:00", banner_clear="1"))
ok((D.execute("SELECT COALESCE(banner,'') FROM lineup_events WHERE id=?", (_bid[0],)).fetchone()[0] or "") == "" and eli.get("/lineup-image/%d" % _bid[0]).status_code == 404, "removing a banner clears the stored image")
_new = eli.get("/events/new").get_data(as_text=True)
_editp = eli.get("/practices/%d?edit=1" % D.execute("SELECT id FROM practices ORDER BY id LIMIT 1").fetchone()[0]).get_data(as_text=True)
ok("data-matfor=dateInput" in _new and "id=dateSheet" not in _new and "grunionsOpenDate" in _new and "Select time" in _new and "id=timeClock" in _new and "matDateOk" in _new and "type=date" in _editp and "type=time" in _editp and "grunionsBindPickers" in _editp, "form dates and times open the centered picker")
def _head(c, path):
    return c.get(path).get_data(as_text=True).split("<main>", 1)[0]
_jane_new = jane.get("/events/new").get_data(as_text=True)
_trip_day = (A.today_pt() + dt.timedelta(days=18)).isoformat()
_trip = jane.post("/events/new", data=dict(csrf=csrf(jane, "/events/new"), action="preview", lane="lineup", event_type="Trip", line_title="Member Trip", description="A weekend away.", location="San Diego", date=_trip_day, start="09:00"), follow_redirects=True)
_trip_row = D.execute("SELECT status, event_type FROM lineup_events WHERE title='Member Trip'").fetchone()
ok("class=headplus" in _head(eli, "/home") and "class=headplus" in _head(eli, "/chat") and "class=headplus" in _head(eli, "/admin") and "class=headplus" in _head(eli, "/lineup") and "class=headplus" not in _head(jane, "/home") and "class=headplus" not in _head(jane, "/chat") and "class=headplus" in _head(jane, "/lineup") and "margin-right:calc(12px - var(--space-3))" in _head(eli, "/home") and ">Trip</option>" in _jane_new and ">Social/Activity</option>" in _jane_new and ">Tournament</option>" not in _jane_new and "Team schedule" not in _jane_new and jane.post("/events/new", data=dict(csrf=csrf(jane, "/events/new"), action="preview", lane="schedule", location="Nope", date=_trip_day)).status_code == 403 and jane.post("/events/new", data=dict(csrf=csrf(jane, "/events/new"), action="preview", lane="lineup", event_type="Tournament", line_title="Sneaky Tournament", description="No.", location="Pool", date=_trip_day, start="09:00")).status_code == 403 and not D.execute("SELECT 1 FROM lineup_events WHERE title='Sneaky Tournament'").fetchone() and _trip.status_code == 200 and _trip_row == ("pending", "Trip"), "the plus follows the role, and members can only propose trips and community events")
