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
ok("verified" in h and "1234567" in h and "2027-08-31" in h and "Marina HS" in h and "Westminster HS" in h, "member home: status, number, valid-until, attendance")
ok("1 checked in" in eli.get("/admin?date=2026-10-27").get_data(as_text=True), "check-in count per practice")
ok(eli.get("/qr.svg").data.startswith(b"<?xml"), "QR svg")
# manual verify
t = eli.get("/admin?date=2026-10-27").get_data(as_text=True)
ok("Verify John on Sport:80" in t and "usawp.sport80.com" in t, "Verify shown only for non-verified")
ok(jane.post("/admin", data=dict(csrf=tok, member_id=3, action="verify")).status_code == 403, "member cannot mark verified")
eli.post("/admin", data=dict(csrf=tok_e, member_id=3, date="2026-10-27", action="verify", number="7654321", valid_until="2027-08-31"))
t = eli.get("/members").get_data(as_text=True); raw = eli.get("/members.csv").data; r = raw.decode("utf-8-sig")
ok(raw.startswith(b"\xef\xbb\xbf") and "John,Smith," in r and "7654321" in r and "2027-08-31" in r, "manual verify records number, date, admin, time")
eli.post("/admin", data=dict(csrf=tok_e, member_id=1, date="2026-10-27", action="verify", valid_until="2020-01-01"))
ok("Eli,Joern," in eli.get("/members.csv").data.decode("utf-8-sig") and "2020-01-01" not in eli.get("/members.csv").data.decode("utf-8-sig"), "past valid-until rejected")
# expiry
import datetime as dt, sqlite3
join(A.app.test_client(), "Ana", "Lopez", "ana@example.com")
D = sqlite3.connect(os.environ["GRUNIONS_DB"]); soon = (A.today_pt()+dt.timedelta(days=5)).isoformat()
eli.post("/admin", data=dict(csrf=tok_e, member_id=4, date="2026-10-27", action="verify", valid_until=soon))
ok("Please enter the expiration" in eli.post("/admin", data=dict(csrf=tok_e, member_id=1, date="2026-10-27", action="verify"), follow_redirects=True).get_data(as_text=True), "Mark verified asks for expiration date")
D.execute("UPDATE members SET usawp_status='verified', usawp_valid_until=? WHERE id=2", ((A.today_pt()-dt.timedelta(days=1)).isoformat(),)); D.commit()
t = eli.get("/admin?date=2026-10-27").get_data(as_text=True)
ok("5d left" in t and "USAWP: <b>" in t, "check-in badge + admin banner")
ok(D.execute("SELECT usawp_status FROM members WHERE id=2").fetchone()[0] == "expired", "auto-flip to expired after expires_on")
j = eli.get("/api/expiring").get_json()
ok(len(j["expired"]) >= 1 and any(r["first"]=="Ana" for r in j["within_7"]), "expiry report endpoint")
ok(jane.get("/api/expiring").status_code == 403, "report endpoint admin-only")
eli.post("/expiring", data=dict(csrf=tok_e, member_id=4))
ana = A.app.test_client(); rr = ana.post("/login", data=dict(csrf=csrf(ana,"/login"), email="ana@example.com"), follow_redirects=True).get_data(as_text=True)
h = ana.get(re.search(r'href="http://localhost(/auth/[^"]+)"', rr).group(1), follow_redirects=True).get_data(as_text=True)
ok("expires in <b>5 days" in h and "notice" in h, "member home expiry warning + in-app reminder")

# roles, channels, practices
D.execute("UPDATE members SET role='coach' WHERE id=3"); D.commit()
john = A.app.test_client(); rr = john.post("/login", data=dict(csrf=csrf(john,"/login"), email="john@example.com"), follow_redirects=True).get_data(as_text=True)
john.get(re.search(r'href="http://localhost(/auth/[^"]+)"', rr).group(1))
tj = csrf(john, "/chat")
ok(john.post("/api/messages?c=coaches", json={"body":"Coaches only: lineup for Friday"}, headers={"X-CSRF": tj}).status_code == 200, "coach posts to #coaches")
ok(jane.get("/api/messages?c=coaches").status_code == 403 and jane.get("/chat?c=coaches").status_code == 403, "#coaches private from members")
ok(len(eli.get("/api/messages?c=coaches").get_json()) == 1 and all("Coaches only" not in m["body"] for m in jane.get("/api/messages").get_json()), "channels separated")
ok(john.get("/admin").status_code == 200 and john.get("/import").status_code == 403 and john.post("/admin", data=dict(csrf=tj, member_id=2, action="verify")).status_code == 403, "coach can check in but not use admin tools")
p = jane.get("/practices").get_data(as_text=True); ok("Marina HS" in p and "Westminster HS" in p and "class=datetile" in p and "I'm going" in p and "I'm not going" in p, "recurring Tue/Fri practices generated")
pid = D.execute("SELECT id, date FROM practices WHERE location='Marina High School' ORDER BY date LIMIT 1").fetchone()
tj2 = csrf(jane, "/practices"); jane.post("/practices", data=dict(csrf=tj2, pid=pid[0], action="going"))
john.post("/practices", data=dict(csrf=tj, pid=pid[0], action="notgoing"))
ok("1 going" in jane.get("/practices").get_data(as_text=True), "RSVP headcount")
ok(jane.post("/practices", data=dict(csrf=tj2, pid=pid[0], action="cancel")).status_code == 403, "members cannot cancel practices")
eli.post("/admin", data=dict(csrf=tok_e, member_id=2, date=pid[1]))
c = eli.get("/admin?date=%s" % pid[1]).get_data(as_text=True)
ok("1 RSVP'd" in c and c.find(">Going <") < c.find(">Everyone else <") < c.find(">Checked in <") and c.find("Eli Joern") < c.find(">Checked in <") < c.find("Jane Doe") and "RSVP ✓" in c and "Not cleared" in c, "check-in groups going, then everyone else, then checked in")
eli.post("/practices", data=dict(csrf=tok_e, pid=pid[0], action="edit", start="19:30", end="21:00", location="Marina High School", note="Pool B"))
eli.post("/practices", data=dict(csrf=tok_e, pid=pid[0], action="cancel"))
ok(tuple(D.execute("SELECT cancelled, start, note FROM practices WHERE id=?", (pid[0],)).fetchone()) == (1, "19:30", "Pool B"), "admin edit + cancel practice")
eli.post("/practices", data=dict(csrf=tok_e, action="add", date="2026-12-05", start="09:00", end="11:00", location="Huntington Beach", note="Holiday scrimmage"))
ok(D.execute("SELECT COUNT(*) FROM practices WHERE date='2026-12-05'").fetchone()[0] == 1, "admin add practice")
ok("Not cleared for water polo" in x.get("/home").get_data(as_text=True), "member home shows Not cleared (membership ok, compliance missing)")
D.execute("UPDATE members SET usawp_status='verified', usawp_valid_until='2027-08-31' WHERE id=2"); D.commit()
eli.post("/admin", data=dict(csrf=tok_e, member_id=2, date="2026-10-27", action="req", req_id=1, completed_on="2026-01-10", expires_on="2027-01-10"))
eli.post("/admin", data=dict(csrf=tok_e, member_id=2, date="2026-10-27", action="req", req_id=3, completed_on="2026-10-01"))
h = x.get("/home").get_data(as_text=True); ok("Cleared for water polo" in h and "Not cleared for water polo" not in h, "manual compliance entry -> Cleared")
D.execute("UPDATE member_reqs SET expires_on=? WHERE member_id=2 AND req_id=1", ((A.today_pt()+dt.timedelta(days=10)).isoformat(),)); D.commit()
ok(any(r.get("item")=="SafeSport training" for r in eli.get("/api/expiring").get_json()["within_30"]), "compliance item in expiring report")
D.execute("UPDATE member_reqs SET expires_on='2026-01-01' WHERE member_id=2 AND req_id=1"); D.commit()
ok("SafeSport training expired" in eli.get("/admin?date=2026-10-27").get_data(as_text=True), "expired compliance -> Not cleared with reason")

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
ok("verification requested" in eli.get("/admin?date=2026-10-27").get_data(as_text=True), "pending state on member row")
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
ok("Verification for Ana Lopez" in a and "bot answered" in a, "admin notification + answered state")
members_now = eli.get("/members").get_data(as_text=True)
ok("bot@grunions.local" not in members_now and "Grunions bot" not in members_now.split(">Verified<")[0], "bot account hidden from member list")
ahome = ana.get("/home").get_data(as_text=True)
ok((">Verified</span><span>%s<" % A.today_pt().isoformat()) in ahome and "Grunions bot" not in ahome, "member verified row shows only the date")
ok("Grunions bot" in a and ">Verified</span><span>Grunions bot" in eli.get("/members").get_data(as_text=True), "admin views still show who verified")
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
ok(jane.post(f"/api/messages/{mid0}/react", json={"emoji": "💩"}, headers={"X-CSRF": tj3}).status_code == 400, "only quick-set emoji")
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
ok('href="/practices/' in pg and " going</span>" in pg and "class=datetile" in pg and "I'm going" in pg and "Edit practice" not in pg and "Assign coaches" not in pg and 'class=morebtn' not in pg, "a practice card links to its page, and a member has no More menu")
ch = jane.get("/chat").get_data(as_text=True)
ca = eli.get("/chat").get_data(as_text=True)
cc = eli.get("/chat?c=coaches").get_data(as_text=True)
ok("rows=1" in ch and "scrollbar-width:none" in ch and "shiftKey" in ch and 'id=attach' in ch and 'id=ann' not in ca and '>Announce<' not in ca and 'id=ann' not in cc and '>Announce<' not in cc and 'aria-label=Send' in ch and 'aria-label=Send' in ca and 'aria-label=Send' in cc and 'class="iconbtn send"' in ch and 'class="iconbtn send"' in cc, "composer: icon send on team and coaches, no announce checkbox")

# member USAWP number on the Not cleared card
jh = jane.get("/home").get_data(as_text=True)
jp = jane.post("/home", data=dict(csrf=csrf(jane, "/home"), usawp_number="99998888"), follow_redirects=True).get_data(as_text=True)
ok("Not cleared for water polo" in jh and "USAWP # 1234567" in jh and "name=usawp_number" not in jh and ">Edit<" not in jh and "id=trialOpen" not in jh and "Reverify membership" not in jh and "SafeSport expired 2026-01-01" in jh and "already verified" in jp and D.execute("SELECT usawp_number FROM members WHERE email='jane@example.com'").fetchone()[0] == "1234567", "verified member sees read-only USAWP number; Edit is hidden and the number cannot be changed")
ok("Membership & requirements" not in jh and "Membership &amp; requirements" not in jh and 'class="card playcard"' in jh and "Not cleared for water polo" in jh and 'class="dot bad"' in jh and "Cleared to coach" not in jh and jh.index("Not cleared for water polo") < jh.index("USAWP # 1234567") < jh.index(">USA Water Polo<"), "home merges clearance and membership into one card")
D.execute("UPDATE member_reqs SET expires_on='2027-06-01' WHERE member_id=2 AND req_id=1"); D.commit()
ok("USAWP Membership #" not in jane.get("/home").get_data(as_text=True) and "USAWP # 1234567" in jane.get("/home").get_data(as_text=True) and "Cleared for water polo" in jane.get("/home").get_data(as_text=True) and "Club waiver" not in jane.get("/home").get_data(as_text=True), "form hidden once verified and cleared; number stays read-only")
casey = A.app.test_client(); join(casey, "Casey", "Ng", "casey@example.com")
cid = D.execute("SELECT id FROM members WHERE email='casey@example.com'").fetchone()[0]
ssid = D.execute("SELECT id FROM requirements WHERE lower(keywords) LIKE '%safesport%'").fetchone()[0]
D.execute("UPDATE members SET role='coach', usawp_status='verified', usawp_valid_until='2027-06-07', usawp_number='659226' WHERE id=?", (cid,))
D.execute("INSERT INTO member_reqs(member_id,req_id,completed_on,expires_on,source,by,at) VALUES(?,?,NULL,'2027-05-11','test','test','2026-10-23T00:00')", (cid, ssid)); D.commit()
chome = casey.get("/home").get_data(as_text=True)
plain_home = jane.get("/home").get_data(as_text=True)
ok("Cleared for water polo" in chome and "Needs:" not in chome and "Club waiver" not in chome and "Concussion" not in chome and "SafeSport training" in chome and "Not cleared to coach" in chome and 'class="st st-bad">Background screening missing' in chome and "Not cleared to coach" not in plain_home and "Cleared to coach" not in plain_home and "Background screening missing" not in plain_home and "Club waiver" not in eli.get("/requirements").get_data(as_text=True) and "Club waiver" not in eli.get("/admin").get_data(as_text=True), "an active coach needs background screening, and a member who is not an active coach does not")
bgid_casey = D.execute("SELECT id FROM requirements WHERE lower(keywords) LIKE '%background%'").fetchone()[0]
far_bg = (A.today_pt() + dt.timedelta(days=400)).isoformat()
soon_bg = (A.today_pt() + dt.timedelta(days=5)).isoformat()
past_bg = (A.today_pt() - dt.timedelta(days=2)).isoformat()
D.execute("INSERT INTO member_reqs(member_id,req_id,completed_on,expires_on,source,by,at) VALUES(?,?,NULL,?,'test','test','2026-01-01')", (cid, bgid_casey, far_bg)); D.commit()
ok("Cleared to coach" in casey.get("/home").get_data(as_text=True) and ('class="st st-ok">Background screening expires ' + far_bg) in casey.get("/home").get_data(as_text=True) and ('class="st st-ok">Background screening expires ' + far_bg) in eli.get("/members").get_data(as_text=True) and ('class="st st-ok">Background screening expires ' + far_bg) in eli.get("/admin").get_data(as_text=True), "a current background screening is green for a coach on home, the roster, and check-in")
D.execute("UPDATE member_reqs SET expires_on=? WHERE member_id=? AND req_id=?", (soon_bg, cid, bgid_casey)); D.commit()
ok(('class="st st-warn">Background screening expires ' + soon_bg) in casey.get("/home").get_data(as_text=True), "background screening is amber inside the expiring window")
D.execute("UPDATE member_reqs SET expires_on=? WHERE member_id=? AND req_id=?", (past_bg, cid, bgid_casey)); D.commit()
expired_home = casey.get("/home").get_data(as_text=True)
ok("Cleared for water polo" in expired_home and "Not cleared to coach" in expired_home and ('class="st st-bad">Background screening expires ' + past_bg) in expired_home and ">Reverify background screening<" in expired_home, "an expired background screening is red, blocks coach clearance, and offers reverify")
casey.post("/home", data=dict(csrf=csrf(casey, "/home"), action="reverify_background"), follow_redirects=True)
ok(D.execute("SELECT status FROM verify_requests WHERE member_id=? ORDER BY id DESC LIMIT 1", (cid,)).fetchone()[0] == "pending" and "Verification pending" in casey.get("/home").get_data(as_text=True), "reverify background screening asks Grunions to verify")
D.execute("DELETE FROM verify_requests WHERE member_id=?", (cid,))
D.execute("UPDATE member_reqs SET expires_on=? WHERE member_id=? AND req_id=?", (far_bg, cid, bgid_casey)); D.commit()
cur = D.execute("INSERT INTO requirements(name,applies_to,keywords,expires,active) VALUES('Club waiver','all','waiver',0,1)")
wid = cur.lastrowid
D.execute("INSERT INTO member_reqs(member_id,req_id,completed_on,expires_on,source,by,at) VALUES(?,?, '2026-01-01', NULL, 'test','test','2026-01-01T00:00')", (cid, wid))
kept = D.execute("SELECT COUNT(*) FROM member_reqs WHERE req_id=?", (ssid,)).fetchone()[0]
nmembers = D.execute("SELECT COUNT(*) FROM members").fetchone()[0]
D.commit(); A.drop_club_waiver(D); A.drop_club_waiver(D)
ok(D.execute("SELECT COUNT(*) FROM requirements WHERE lower(name)='club waiver' OR lower(ifnull(keywords,'')) LIKE '%waiver%'").fetchone()[0] == 0 and D.execute("SELECT COUNT(*) FROM member_reqs WHERE req_id=?", (wid,)).fetchone()[0] == 0 and D.execute("SELECT COUNT(*) FROM member_reqs WHERE req_id=?", (ssid,)).fetchone()[0] == kept and D.execute("SELECT COUNT(*) FROM members").fetchone()[0] == nmembers and "Cleared for water polo" in casey.get("/home").get_data(as_text=True) and "Club waiver" not in casey.get("/home").get_data(as_text=True), "migration removes Club waiver only and the member stays cleared")
sam = A.app.test_client(); join(sam, "Sam", "River", "sam@example.com")
sh = sam.get("/home").get_data(as_text=True)
ok('name=usawp_number inputmode=numeric value=""' in sh and "USAWP Membership #" in sh and "Not cleared for water polo" in sh and 'class="dot bad"' in sh and "Verification pending" not in sh and "id=trialOpen" in sh and ">2-week USAWP trial<" in sh, "empty membership form for a new member")
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
ok(page.status_code == 200 and 'class="toast noprint" role=status>Sent to Grunions for verification' in sp and "setTimeout" in sp and "3000" in sp and "Verification pending" in sp and 'class="dot warn"' in sp and 'class="st st-bad">Not cleared' not in sp and "USAWP # 4321" in sp and ">Edit<" in sp and "id=usawpForm hidden" in sp and "id=trialOpen" not in sp and "name=usawp_number" not in sp.split("id=usawpForm")[0] and D.execute("SELECT usawp_number FROM members WHERE id=?", (sid,)).fetchone()[0] == "4321" and vr[1] == "4321" and vr[2] == "pending", "submit saves number, hides the input, toasts, and shows Pending")
ok(_spy.timeout == 5 and len(hits) == before + 1 and body == {"request_id": vr[0], "member_id": sid, "name": "Sam River", "preferred_first": None, "email": "sam@example.com", "member_number": "4321", "requested_by": "Sam River", "member_submitted": True, "app_url": "https://grunions.example"}, "member submit POSTs the webhook payload with a 5s timeout")
ok("verification requested" in eli.get("/admin").get_data(as_text=True) and any(x["id"] == vr[0] and x["member_number"] == "4321" and x["status"] == "pending" for x in c0.get("/api/verify-requests?status=pending", headers=H).get_json()), "request shows in admin and on the bot API")
quiet = sam.get("/home").get_data(as_text=True)
ok("class=\"toast" not in quiet and "Sent to Grunions for verification" not in quiet and "Verification pending" in quiet and 'class="dot warn"' in quiet and "USAWP # 4321" in quiet and ">Edit<" in quiet, "reload keeps the pending card without repeating the toast")
edit = sam_post("55555")
ok(tuple(D.execute("SELECT COUNT(*), MAX(member_number) FROM verify_requests WHERE member_id=? AND status='pending'", (sid,)).fetchone()) == (1, "55555") and len(hits) == before + 2 and hits[-1]["json"]["request_id"] == vr[0] and hits[-1]["json"]["member_number"] == "55555" and hits[-1]["json"]["member_submitted"] is True and hits[-1]["json"]["requested_by"] == "Sam River" and 'class="toast noprint" role=status>Sent to Grunions for verification' in edit.get_data(as_text=True) and "USAWP # 55555" in edit.get_data(as_text=True) and D.execute("SELECT requested_by FROM verify_requests WHERE id=?", (vr[0],)).fetchone()[0] == "Sam River", "edit save updates the pending number, re-sends the webhook, and toasts again")
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
ok(res["ok"] and D.execute("SELECT status FROM verify_requests WHERE id=?", (vr[0],)).fetchone()[0] == "done" and tuple(D.execute("SELECT usawp_status, usawp_number FROM members WHERE id=?", (sid,)).fetchone()) == ("verified", "666666") and "Cleared for water polo" in shome and 'class="dot ok"' in shome and "Verification pending" not in shome and "USAWP Membership #" not in shome and "USAWP # 666666" in shome and ">Edit<" not in shome, "bot result answers the member request and shows Cleared with a read-only number")
kr = D.execute("SELECT id FROM verify_requests WHERE member_id=? AND status='pending'", (kid,)).fetchone()
c0.post("/api/verify-requests/%d/result" % kr[0], headers=H, json={"verified": False, "note": "no matching membership"})
kh = kim.get("/home").get_data(as_text=True)
ok("Not cleared for water polo" in kh and 'class="dot bad"' in kh and "Verification pending" not in kh and "USAWP # 10003" in kh and ">Edit<" in kh and "id=trialOpen" not in kh, "bot not-verified result restores the red Not cleared card")
ACK = "I will complete the USA Water Polo 2-week trial membership before I get in the pool. I understand I need to get a full USAWP membership soon, otherwise I will not be able to practice."
alex = A.app.test_client(); join(alex, "Alex", "Trial", "alex@example.com")
ah = alex.get("/home").get_data(as_text=True)
ok("id=trialOpen" in ah and ">2-week USAWP trial<" in ah and ACK in ah and A.TRIAL_JOIN_URL in ah and "target=_blank" in ah and "rel=noopener" in ah and ">I confirm<" in ah and ">Get USAWP trial membership<" in ah and 'class="dot bad"' in ah and "Not cleared for water polo" in ah, "empty card offers the 2-week trial acknowledgment")
ok(alex.post("/home", data=dict(action="trial")).status_code == 400, "trial confirm requires CSRF")
jane.post("/home", data=dict(csrf=csrf(jane, "/home"), action="trial"), follow_redirects=True)
ok(D.execute("SELECT trial_acknowledged_at FROM members WHERE email='jane@example.com'").fetchone()[0] in (None, ""), "a verified membership cannot start a trial")
kim.post("/home", data=dict(csrf=tk, action="trial"), follow_redirects=True)
ok(D.execute("SELECT trial_acknowledged_at FROM members WHERE email='kim@example.com'").fetchone()[0] in (None, ""), "a saved USAWP number cannot start a trial")
def md(d): return d.strftime("%b ") + str(d.day)
today = A.today_pt(); end = today + dt.timedelta(days=14); start = today.isoformat()
ap = alex.post("/home", data=dict(csrf=csrf(alex, "/home"), action="trial"), follow_redirects=True).get_data(as_text=True)
stamp = D.execute("SELECT trial_acknowledged_at FROM members WHERE email='alex@example.com'").fetchone()[0]
ok(stamp and stamp[:10] == start and 'class="toast noprint" role=status>2-week USAWP trial started' in ap and 'class="st st-trial">Trial · 14 days left' in ap and (">Ends %s<" % md(end)) in ap and ".st-trial::before{background:var(--ok)}" in ap and "id=trialOpen" not in ap and 'name=usawp_number inputmode=numeric value=""' in ap and "Cleared for water polo" in ap and "Not cleared for water polo" not in ap and 'class="st st-bad">Not cleared' not in ap and "Needs:" not in ap, "confirm records the trial and shows a green Trial badge with days left")
again = alex.post("/home", data=dict(csrf=csrf(alex, "/home"), action="trial"), follow_redirects=True).get_data(as_text=True)
ok(D.execute("SELECT trial_acknowledged_at FROM members WHERE email='alex@example.com'").fetchone()[0] == stamp and "2-week USAWP trial started" not in again, "a second confirm does not reset the trial")
adm = eli.get("/admin").get_data(as_text=True); mem = eli.get("/members").get_data(as_text=True); csv = eli.get("/members.csv").get_data(as_text=True)
ok("Trial · 14 days left" in adm and ("Ends %s" % md(end)) in adm and "Trial · 14 days left" in mem and ("Ends %s" % md(end)) in mem and stamp[:10] in csv and end.isoformat() in csv, "admin check-in and roster show trial days left and the end date")
added = alex.post("/home", data=dict(csrf=csrf(alex, "/home"), usawp_number="88821"), follow_redirects=True).get_data(as_text=True)
ok('class="toast noprint" role=status>Sent to Grunions for verification' in added and "Verification pending" in added and 'class="dot warn"' in added and "USAWP # 88821" in added and ">Edit<" in added and "Trial · 14 days left" not in added and "Ends %s" % md(end) not in added and D.execute("SELECT trial_acknowledged_at FROM members WHERE email='alex@example.com'").fetchone()[0] == stamp and D.execute("SELECT member_number, status FROM verify_requests WHERE member_id=(SELECT id FROM members WHERE email='alex@example.com')").fetchone() == ("88821", "pending"), "a trial member can submit a USAWP number and the card shows Pending")
aid = D.execute("SELECT id FROM members WHERE email='alex@example.com'").fetchone()[0]
avr = D.execute("SELECT id FROM verify_requests WHERE member_id=? AND status='pending'", (aid,)).fetchone()[0]
c0.post("/api/verify-requests/%d/result" % avr, headers=H, json={"verified": True, "member_number": "88821", "membership_expires_on": "2027-08-31", "compliance": {"SafeSport training": "2027-05-01"}})
vh = alex.get("/home").get_data(as_text=True)
ok("Cleared for water polo" in vh and 'class="dot ok"' in vh and "USAWP # 88821" in vh and "Trial ·" not in vh and "Last day of trial" not in vh and ("Ends %s" % md(end)) not in vh and "Verification pending" not in vh and ">Edit<" not in vh, "a verified membership replaces the trial display")
drew = A.app.test_client(); join(drew, "Drew", "Lane", "drew@example.com")
drew.post("/home", data=dict(csrf=csrf(drew, "/home"), action="trial"), follow_redirects=True)
D.execute("UPDATE members SET trial_acknowledged_at=? WHERE email='drew@example.com'", ((today - dt.timedelta(days=13)).isoformat() + "T08:00:00",)); D.commit()
one = drew.get("/home").get_data(as_text=True)
ok('class="st st-trial">Trial · 1 day left' in one and (">Ends %s<" % md(today + dt.timedelta(days=1))) in one and "Cleared for water polo" in one and "Not cleared for water polo" not in one, "one day left uses the singular trial label")
D.execute("UPDATE members SET trial_acknowledged_at=? WHERE email='drew@example.com'", ((today - dt.timedelta(days=14)).isoformat() + "T08:00:00",)); D.commit()
last = drew.get("/home").get_data(as_text=True)
ok('class="st st-trial">Last day of trial' in last and (">Ends %s<" % md(today)) in last and "Cleared for water polo" in last and 'class="st st-bad">Not cleared' not in last, "the end date is the last day of the trial")
ended_on = today - dt.timedelta(days=1)
D.execute("UPDATE members SET trial_acknowledged_at=? WHERE email='drew@example.com'", ((today - dt.timedelta(days=15)).isoformat() + "T08:00:00",)); D.commit()
eh = drew.get("/home").get_data(as_text=True)
ok("Not cleared for water polo" in eh and 'class="dot bad"' in eh and ("Trial ended %s" % md(ended_on)) in eh and "id=trialOpen" not in eh and "Last day of trial" not in eh and 'name=usawp_number inputmode=numeric value=""' in eh and "Cleared for water polo" not in eh, "an ended trial returns to Not cleared and keeps the membership form")
ok(("Trial ended %s" % md(ended_on)) in eli.get("/admin").get_data(as_text=True) and ("Trial ended %s" % md(ended_on)) in eli.get("/members").get_data(as_text=True), "admin marks an ended trial on check-in and the roster")
D.execute("UPDATE members SET trial_acknowledged_at=? WHERE email='alex@example.com'", ((today - dt.timedelta(days=15)).isoformat() + "T08:00:00",)); D.commit()
ok("Cleared for water polo" in alex.get("/home").get_data(as_text=True) and "Trial ended" not in alex.get("/home").get_data(as_text=True), "a verified member keeps the normal card after the trial date has passed")
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
g0, e0, k0 = page.index(">Going <"), page.index(">Everyone else <"), page.index(">Checked in <")
going_html, rest_html, done_html = page[g0:e0], page[e0:k0], page[k0:]
ok(">Going <span class=t3>2</span>" in page and going_html.index("Liam Carter") < going_html.index("Mia Barnes") and "Ava Evans" not in going_html and "Amy Able" not in going_html and 'class="st st-bad">Not cleared' in going_html and rest_html.index("Amy Able") < rest_html.index("Noah Diaz") < rest_html.index("Zack Quinn") and "Aaron Quinn" not in rest_html.split("Zack Quinn")[0] and "Liam Carter" not in rest_html and done_html.index("Ava Evans") < done_html.index("Ben Foster") and "Mia Barnes" not in done_html and 'class="st st-bad">Not cleared' in done_html and "<details class=checkin>" in page and "<details class=checkin open" not in page, "check-in sections sort A-Z by display name and keep clearance badges")
found = eli.get("/admin?date=%s&q=Liam" % day).get_data(as_text=True)
eli.post("/admin", data=dict(csrf=csrf(eli, "/admin"), member_id=ava, date=day, action="undo"))
back = eli.get("/admin?date=%s" % day).get_data(as_text=True)
ok(">Going <span class=t3>1</span>" in found and "Liam Carter" in found and "Mia Barnes" not in found and ">Everyone else <span class=t3>0</span>" in found and ">Checked in <span class=t3>0</span>" in found and back.index(">Going <") < back.index("Ava Evans") < back.index("Mia Barnes") < back.index(">Everyone else <") and "Ava Evans" not in back[back.index(">Checked in <"):], "search stays inside the sections and undo returns a going member to Going")
yesterday = (A.today_pt() - dt.timedelta(days=1)).isoformat()
ren = A.app.test_client(); join(ren, "Ren", "Ew", "ren@example.com")
rid = D.execute("SELECT id FROM members WHERE email='ren@example.com'").fetchone()[0]
D.execute("UPDATE members SET usawp_status='verified', usawp_number='659226', usawp_valid_until=?, usawp_verified_by='Eli Joern', usawp_verified_at='2026-01-01T00:00' WHERE id=?", (yesterday, rid))
D.execute("INSERT INTO member_reqs(member_id,req_id,completed_on,expires_on,source,by,at) VALUES(?,?,NULL,?, 'test','test','2026-01-01T00:00')", (rid, ssid, yesterday)); D.commit()
rh = ren.get("/home").get_data(as_text=True)
ok("Not cleared for water polo" in rh and 'class="dot bad"' in rh and ("Membership expired %s" % yesterday) in rh and ("SafeSport expired %s" % yesterday) in rh and ">Reverify membership<" in rh and 'id=reverifyForm hidden' in rh and 'value="659226"' in rh and ">Send<" in rh and "Cleared for water polo" not in rh and "Needs:" not in rh and D.execute("SELECT usawp_status FROM members WHERE id=?", (rid,)).fetchone()[0] == "expired", "a passed membership date returns to Not cleared with Reverify, and an expired SafeSport date is listed")
sent = ren.post("/home", data=dict(csrf=csrf(ren, "/home"), usawp_number="424242"), follow_redirects=True).get_data(as_text=True)
ok("Sent to Grunions for verification" in sent and "Verification pending" in sent and 'class="dot warn"' in sent and "USAWP # 424242" in sent and ">Reverify membership<" not in sent and ("Membership expired %s" % yesterday) not in sent and tuple(D.execute("SELECT member_number, status FROM verify_requests WHERE member_id=? ORDER BY id DESC LIMIT 1", (rid,)).fetchone()) == ("424242", "pending"), "Reverify sends a new request, shows the toast, and the card goes to Pending")
sue = A.app.test_client(); join(sue, "Sue", "Park", "sue@example.com")
uid = D.execute("SELECT id FROM members WHERE email='sue@example.com'").fetchone()[0]
D.execute("UPDATE members SET usawp_status='verified', usawp_number='1112223', usawp_valid_until='2027-08-31' WHERE id=?", (uid,))
D.execute("INSERT INTO member_reqs(member_id,req_id,completed_on,expires_on,source,by,at) VALUES(?,?,NULL,?, 'test','test','2026-01-01T00:00')", (uid, ssid, yesterday)); D.commit()
shome = sue.get("/home").get_data(as_text=True)
ok(("SafeSport expired %s" % yesterday) in shome and "Not cleared for water polo" in shome and ">Reverify membership<" not in shome and "name=usawp_number" not in shome and "USAWP # 1112223" in shome and "Membership expired" not in shome and "SafeSport training expired" in eli.get("/admin?date=2026-10-27").get_data(as_text=True), "expired SafeSport stays Not cleared without a membership reverify button")

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
    nxt = home[home.find("NEXT PRACTICE"):]
    nxt = nxt[:nxt.find("I'm going")]
    adm = eli.get("/admin").get_data(as_text=True)
    ok("class=dn>23<" in sched and "7:00 PM" in sched and "Westminster HS" in sched and "FRI" in nxt and ">23<" in nxt and "7:00 PM" in nxt and "Westminster HS" in nxt and 'value="2026-10-23"' in adm, "at 5:30pm Pacific, Friday's practice is on the schedule and check-in uses that date")
    ok(D.execute("SELECT COUNT(*) FROM practices WHERE date=? AND location='Westminster High School'", (fri,)).fetchone()[0] == 1, "opening the schedule does not delete Friday's practice")
    A.now_pt = lambda: dt.datetime(2026, 10, 24, 3, 30, tzinfo=dt.timezone.utc)  # 8:30pm PDT
    ok("class=dn>23<" in jane.get("/practices").get_data(as_text=True), "the practice stays up through 8:30pm Pacific")
    A.now_pt = lambda: dt.datetime(2026, 10, 24, 3, 31, tzinfo=dt.timezone.utc)  # 8:31pm PDT
    late = jane.get("/practices").get_data(as_text=True)
    late_home = jane.get("/home").get_data(as_text=True)
    late_next = late_home[late_home.find("NEXT PRACTICE"):]
    late_next = late_next[:late_next.find("I'm going")] if "I'm going" in late_next else late_next[:500]
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
ok("contextmenu" in chui and "Message deleted" in chui and "(edited)" in chui and "Delete this message?" in chui and "Message actions" in chui and "😮" in chui and "🎉" in chui and "🙏" in chui and "pointerdown" in chui and "(hover:hover) and (pointer:fine)" in chui, "chat page has the press-and-hold action sheet")
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
ok(jane.post("/api/messages/%d/react" % rid, json={"emoji": "😮"}, headers={"X-CSRF": tj}).get_json()["😮"] == {"n": 1, "mine": True} and jane.post("/api/messages/%d/react" % rid, json={"emoji": "💩"}, headers={"X-CSRF": tj}).status_code == 400, "the extra reaction set toggles and anything outside it is rejected")
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
ok("Coaches: Eli, Sam" in sched and "Coaches: Eli, Sam" in home and "Coaches: Eli, Sam" in coachpg and "Coaches: Eli, Sam" in staff and "Coaches: Eli, Sam" in checkin and 'class="st st-ok coach-elig"' not in sched and 'class="st st-ok coach-elig"' not in staff and "No assigned coach is coach-eligible" not in sched and "No assigned coach is coach-eligible" not in staff and "No assigned coach is coach-eligible" in eli.get("/practices/%d" % pid).get_data(as_text=True) and "No assigned coach is coach-eligible" not in coachpg and "No assigned coach is coach-eligible" not in eli.get("/home").get_data(as_text=True), "assigned coaches show on every schedule card and on check-in, and the eligibility warning stays on the practice page")
picker = eli.get("/practices/%d" % pid).get_data(as_text=True)
ok(('name=coach value="%d" checked' % eli_id) in picker and ('name=coach value="%d" checked' % john_id) in picker and ('name=coach value="%d"' % jane_id) not in picker and "<select name=coach" not in picker and "name=coach" not in sched and "name=coach" not in coachpg, "edit practice is a checkbox per coaching-list member, and only an admin gets that list")
ok(jane.post("/practices", data=dict(csrf=csrf(jane, "/practices"), pid=pid, action="edit", start=pstart, end=pend, location=ploc, note=pnote, coach=str(jane_id))).status_code == 403 and D.execute("SELECT member_id FROM practice_coaches WHERE practice_id=? ORDER BY member_id", (pid,)).fetchall() == [(eli_id,), (john_id,)], "a member cannot change practice coaches, and someone off the coaching list is not stored")
list_act(john_id, "remove_coaching")
hid = jane.get("/practices").get_data(as_text=True)
ok("Coaches: Eli" in hid and "Coaches: Eli, Sam" not in hid and D.execute("SELECT member_id FROM practice_coaches WHERE practice_id=? AND member_id=?", (pid, john_id)).fetchone() and john.get("/admin").status_code == 200, "leaving the coaching list hides a coach from the practice and keeps coach access")
list_act(john_id, "add_coaching")
ok("Coaches: Eli, Sam" in jane.get("/practices").get_data(as_text=True), "returning to the coaching list shows the assigned name again")
eli.post("/practices", data=dict(base, coach=[str(john_id)]))
ok("Coaches: Sam" in jane.get("/practices").get_data(as_text=True) and "Coaches: Eli, Sam" not in jane.get("/practices").get_data(as_text=True) and "Coaches: Sam" in jane.get("/home").get_data(as_text=True), "unchecking a coach removes that name from the card")
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
ok(ccols == ["practice_id", "member_id"] and "membership_type" in mcols and clist and kept == "Kept" and grew == ["practice_id", "member_id"] and still == 1, "an existing database gains the coaching list, membership type, and practice coaches without dropping rows")

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
badge_pages = riley.get("/home").get_data(as_text=True) + eli.get("/members").get_data(as_text=True) + eli.get("/admin").get_data(as_text=True) + eli.get("/admins").get_data(as_text=True)
members_html = eli.get("/members").get_data(as_text=True)
riley_at = members_html.find("riley@example.com")
riley_row = members_html[members_html.rfind("<div class=li", 0, riley_at):members_html.find("<div class=li", riley_at)]
eli_pick = eli.get("/practices/%d" % pid).get_data(as_text=True)
ok(badge_pages.count('class="st st-ok coach-elig">Coach eligible') >= 3 and 'class="st st-ok coach-elig"' not in jane.get("/practices").get_data(as_text=True) and ('name=coach value="%d"' % riley_id) in eli_pick and 'class="st st-ok coach-elig">Coach eligible' in eli_pick and 'class="st st-ok coach-elig">Coach eligible' in riley_row and "class=coach-tag>Coach<" in riley_row and "Active coach" not in riley_row, "Coach eligible shows on home, check-in, and People, and the coaching list shows a Coach tag")
filt = eli.get("/members?coach=eligible").get_data(as_text=True)
ok("Riley Quinn" in filt and ">Coach eligible<" in filt and 'class="st st-ok coach-elig">Coach eligible' in filt and ">Coaches</a>" in eli.get("/members").get_data(as_text=True), "People has Coaches and Coach eligible sections")
D.execute("UPDATE members SET usawp_valid_until=? WHERE id=?", (today, riley_id)); D.commit()
ok('coach-elig">Coach eligible' in riley.get("/home").get_data(as_text=True), "a coach membership is still eligible on the day it expires")
D.execute("UPDATE members SET usawp_valid_until='2027-08-31' WHERE id=?", (riley_id,)); D.commit()
pdate = D.execute("SELECT date FROM practices WHERE id=?", (pid,)).fetchone()[0]
eli.post("/practices", data=dict(base, coach=[str(riley_id)]))
card = eli.get("/practices").get_data(as_text=True).split("id=p%d " % pid, 1)[1].split("id=p")[0]
jane_card = jane.get("/practices").get_data(as_text=True).split("id=p%d " % pid, 1)[1].split("id=p")[0]
elig_page = eli.get("/practices/%d" % pid).get_data(as_text=True)
other_pid = D.execute("SELECT id FROM practices WHERE cancelled=0 AND id!=? ORDER BY date, start LIMIT 1", (pid,)).fetchone()[0]
ok("No assigned coach is coach-eligible" not in card and 'class="st st-ok coach-elig"' not in card and 'class="st st-ok coach-elig"' not in jane_card and "No assigned coach is coach-eligible" not in jane_card and "No assigned coach is coach-eligible" not in eli.get("/practices").get_data(as_text=True) and 'class="st st-ok coach-elig">Coach eligible' in elig_page and "No assigned coach is coach-eligible" not in elig_page and "No assigned coach is coach-eligible" in eli.get("/practices/%d" % other_pid).get_data(as_text=True), "an eligible assigned coach clears that practice's warning, and schedule cards omit Coach eligible")
memcsv = {r[3]: r for r in list(csvmod.reader(io_mod.StringIO(eli.get("/members.csv").data.decode("utf-8-sig"))))[1:]}
prows = list(csvmod.reader(io_mod.StringIO(eli.get("/export/practices.csv?start=%s&end=%s" % (pdate, pdate)).data.decode("utf-8-sig"))))
prow = next(r for r in prows[1:] if r[0] == pdate and r[2] == ploc)
with A.app.app_context():
    detail = [r for r in A.practice_sheet_tabs(A.db())[A.SHEET_PRACTICE_COACHES][1:] if r[0] == pdate and r[2] == ploc]
ok(memcsv["riley@example.com"][-3] == "Coach eligible" and memcsv["riley@example.com"][-2] == "" and memcsv["riley@example.com"][-1].startswith("Background screening expires ") and memcsv["jane@example.com"][-3] == "" and memcsv["jane@example.com"][-2] == "" and memcsv["jane@example.com"][-1] == "" and prow[6] == "Riley" and prow[7] == "1" and prow[8] == "1" and detail == [[pdate, "%s-%s" % (pstart, pend), ploc, "Riley Quinn", "riley@example.com", "Coach eligible"]], "Coach eligible and background screening are on the members CSV, and coach eligibility is on the practices CSV and sheet")
D.execute("UPDATE member_reqs SET expires_on=? WHERE member_id=? AND req_id=(SELECT id FROM requirements WHERE keywords LIKE '%background%' LIMIT 1)", (past, riley_id)); D.commit()
ok('coach-elig">Coach eligible' not in riley.get("/home").get_data(as_text=True) and ("Coach eligibility expired " + past) in riley.get("/home").get_data(as_text=True) and ("Coach eligibility expired " + past) in eli.get("/members").get_data(as_text=True) and D.execute("SELECT 1 FROM coaching_list WHERE member_id=?", (riley_id,)).fetchone(), "an expired background screening shows Coach eligibility expired and keeps the coaching list")
D.execute("UPDATE member_reqs SET expires_on=? WHERE member_id=? AND req_id IN (SELECT id FROM requirements WHERE keywords LIKE '%background%' OR keywords LIKE '%safesport%')", (today, riley_id)); D.commit()
ok('coach-elig">Coach eligible' in riley.get("/home").get_data(as_text=True) and "Coach eligibility expired" not in riley.get("/home").get_data(as_text=True), "background and SafeSport are current on the expiry date itself")
D.execute("UPDATE member_reqs SET expires_on=? WHERE member_id=? AND req_id=(SELECT id FROM requirements WHERE keywords LIKE '%safesport%' LIMIT 1)", (past, riley_id)); D.commit()
ok('coach-elig">Coach eligible' not in riley.get("/home").get_data(as_text=True) and ("Coach eligibility expired " + past) in eli.get("/admin").get_data(as_text=True), "an expired SafeSport date shows Coach eligibility expired on check-in")
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
ok(D.execute("SELECT source FROM coaching_list WHERE member_id=?", (riley_id,)).fetchone()[0] == "usawp" and D.execute("SELECT membership_type FROM members WHERE id=?", (riley_id,)).fetchone()[0] == "Head Coach" and 'coach-elig">Coach eligible' in riley.get("/home").get_data(as_text=True), "a coach membership import adds the USAWP coaching-list row and the badge")
list_act(riley_id, "remove_coaching")
ok(not D.execute("SELECT 1 FROM coaching_list WHERE member_id=?", (riley_id,)).fetchone() and ('name=coach value="%d"' % riley_id) not in eli.get("/practices/%d" % pid).get_data(as_text=True), "an admin can remove a USAWP coach from the coaching list")
answer(True, membership_type="Individual Membership, Coach")
ok(D.execute("SELECT source FROM coaching_list WHERE member_id=?", (riley_id,)).fetchone()[0] == "usawp" and riley.get("/admin").status_code == 403, "the next coach verification puts them back on the list without coach access")
una = A.app.test_client(); join(una, "Una", "Noverified", "una.noverified@example.com")
D.commit(); una_id = D.execute("SELECT id FROM members WHERE email='una.noverified@example.com'").fetchone()[0]
chunk = eli.get("/members").get_data(as_text=True).split("una.noverified@example.com", 1)[1].split("<div class=li", 1)[0]
ok(D.execute("SELECT usawp_status FROM members WHERE id=?", (una_id,)).fetchone()[0] == "unknown" and "Add to coaches" in chunk and "Make admin" in chunk and "Add to referees" in chunk, "People offers coaches, referees, and admin actions before USAWP is verified")
list_act(una_id, "make_coach"); list_act(una_id, "make_admin")
ok(D.execute("SELECT role, is_admin, usawp_status FROM members WHERE id=?", (una_id,)).fetchone() == ("coach", 1, "unknown") and una.get("/admin").status_code == 200 and una.get("/chat?c=coaches").status_code == 200 and una.get("/members").status_code == 200, "Make coach and Make admin work for a member who is not USAWP verified")
list_act(una_id, "remove_admin"); list_act(una_id, "remove_coach")
ok(D.execute("SELECT role, is_admin, usawp_status FROM members WHERE id=?", (una_id,)).fetchone() == ("athlete", 0, "unknown") and una.get("/admin").status_code == 403 and una.get("/chat?c=coaches").status_code == 403, "Remove admin and Remove coach do not depend on USAWP status")
ned = A.app.test_client(); join(ned, "Ned", "List", "ned.list@example.com")
D.commit(); ned_id = D.execute("SELECT id FROM members WHERE email='ned.list@example.com'").fetchone()[0]
ok("Add to coaches" in eli.get("/members").get_data(as_text=True) and "Make active coach" in eli.get("/members?view=coaches").get_data(as_text=True) and ("name=coach value=\"%d\"" % ned_id) not in eli.get("/practices/%d" % pid).get_data(as_text=True) and ned.post("/members", data=dict(csrf=csrf(ned, "/home"), member_id=ned_id, action="make_coach")).status_code == 403, "People offers Add to coaches, and that person is not assignable yet")
made = eli.post("/members", data=dict(csrf=csrf(eli, "/members"), member_id=ned_id, action="make_coach"), follow_redirects=True).get_data(as_text=True)
ned_at = made.find("ned.list@example.com")
ned_li = made.rfind("<div class=li", 0, ned_at)
ned_row = made[ned_li:made.find("<div class=li", ned_at)]
ned_menu = made[ned_li:ned_at]
eli_at = made.find("eli@example.com")
eli_row = made[made.rfind("<div class=li", 0, eli_at):made.find("<div class=li", eli_at)]
ok('class="toast noprint" role=status>Ned List is now an active coach.' in made and D.execute("SELECT role FROM members WHERE id=?", (ned_id,)).fetchone()[0] == "coach" and not D.execute("SELECT 1 FROM coaching_list WHERE member_id=?", (ned_id,)).fetchone() and ("name=coach value=\"%d\"" % ned_id) not in eli.get("/practices/%d" % pid).get_data(as_text=True) and "Active coach" in ned_row and "Remove active coach" in eli.get("/members?view=coaches").get_data(as_text=True) and ("name=coach value=\"%d\"" % eli_id) in eli.get("/practices/%d" % pid).get_data(as_text=True) and ned.get("/chat?c=coaches").status_code == 200 and ned.get("/admin").status_code == 200, "Make active coach grants access without the coaching list")

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
ok("Cleared for water polo" in bea_home and "Background screening" not in bea_home and "Not cleared to coach" not in bea_home and "Require background" not in members_html and "Don't require background" not in members_html, "a player is cleared without background screening, and the members menu has no Require background item")
denied = eli.post("/members", data=dict(csrf=csrf(eli, "/members"), member_id=bea_id, action="require_background"), follow_redirects=True)
ok(denied.status_code == 400 and "Cleared for water polo" in bea.get("/home").get_data(as_text=True) and D.execute("SELECT require_background FROM members WHERE id=?", (bea_id,)).fetchone()[0] == 1, "Require background is not an action and leaves the stored flag unused")
made_coach = eli.post("/members", data=dict(csrf=csrf(eli, "/members"), member_id=bea_id, action="make_coach"), follow_redirects=True).get_data(as_text=True)
bea_at = made_coach.find("bea.player@example.com")
bea_row = made_coach[made_coach.rfind("<div class=li", 0, bea_at):made_coach.find("<div class=panel", bea_at)]
as_coach = bea.get("/home").get_data(as_text=True)
coach_csv = {r[3]: r for r in list(csvmod.reader(io_mod.StringIO(eli.get("/members.csv").data.decode("utf-8-sig"))))[1:]}
eli.post("/members", data=dict(csrf=csrf(eli, "/members"), member_id=bea_id, action="remove_coach"), follow_redirects=True)
as_player = bea.get("/home").get_data(as_text=True)
player_csv = {r[3]: r for r in list(csvmod.reader(io_mod.StringIO(eli.get("/members.csv").data.decode("utf-8-sig"))))[1:]}
ok("Cleared for water polo" in as_coach and "Not cleared to coach" in as_coach and "Background screening missing" in as_coach and "Background screening missing" in bea_row and coach_csv["bea.player@example.com"][-1] == "Background screening missing" and "Not cleared to coach" not in as_player and "Background screening" not in as_player and "Cleared for water polo" in as_player and player_csv["bea.player@example.com"][-1] == "", "Make coach requires background screening, and Remove coach drops that requirement")
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
    nav = re.sub(r' class=""', "", nav)
    nav = re.sub(r'\sdata-total="[^"]*"', "", nav)
    return re.sub(r"<span class=badge>[^<]*</span>", "", nav)
eli_pages = [eli.get(p).get_data(as_text=True) for p in ("/home", "/practices", "/chat", "/admin", "/members")]
jane_pages = [jane.get(p).get_data(as_text=True) for p in ("/home", "/practices", "/chat")]
login_html = client().get("/login").get_data(as_text=True)
ok(len({nav_skeleton(h) for h in eli_pages}) == 1 and "href=/admin" in nav_skeleton(eli_pages[0]), "staff bottom nav markup matches on home, schedule, chat, and admin")
ok(len({nav_skeleton(h) for h in jane_pages}) == 1 and "href=/admin" not in nav_skeleton(jane_pages[0]) and "href=/home" in nav_skeleton(jane_pages[0]), "member bottom nav markup matches and has no admin tab")
ok("color-scheme:dark" in eli_pages[0][:600] and "content=dark" in eli_pages[0][:600] and "#0a0a0b" in eli_pages[0][:600] and '<body style="background:#0a0a0b' in eli_pages[0] and "color-scheme:dark" in login_html[:600] and "#0a0a0b" in login_html[:600], "dark background is in the first bytes, including the login page")
ok("input,select,textarea{" in eli_pages[0] and "color-scheme:dark" in eli_pages[0].split("input,select,textarea{", 1)[1][:400] and "input[type=date]::-webkit-calendar-picker-indicator" in eli_pages[0] and "input[type=time]::-webkit-calendar-picker-indicator" in eli_pages[0] and "stroke='%23ececee'" in eli_pages[0], "date and time icons use the input text color")
ok("@view-transition{navigation:auto}" in eli_pages[0] and "::view-transition-old(root)" in eli_pages[0] and "animation-duration:0s" in eli_pages[0] and "view-transition-name:grunions-nav" in eli_pages[0] and "contain:layout paint" not in eli_pages[0] and "replaceChildren" in eli_pages[0] and "height:calc(64px + env(safe-area-inset-bottom))" in eli_pages[0] and 'width="24" height="24"' in eli_pages[0] and "function grunionsGo(" in eli_pages[0] and "function grunionsApply(" in eli_pages[0] and "rel=stylesheet" not in eli_pages[0] and "rel=stylesheet" not in login_html and "backdrop-filter" not in eli_pages[0], "nav stays put across tab changes without a crossfade flicker")

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
    ok('value="2026-10-20"' in adm and "id=calPick" in adm and "id=calPop hidden" in adm and 'stroke="currentColor"' in adm and ".calpop{position:absolute" in adm and "span.calday{color:var(--t3)" in adm and not re.search(r"<input[^>]*type=date[^>]*name=date|<input[^>]*name=date[^>]*type=date", adm), "check-in opens a dark practice calendar on the next practice when today has none")
    ok('aria-disabled=true>19</span>' in grid and 'aria-disabled=true>21</span>' in grid and 'class="calday on" href="/admin?date=2026-10-20"' in grid and 'href="/admin?date=2026-10-16"' in grid and "2026-10-21" not in grid and ('href="/admin?date=%s" aria-label="Previous practice"' % prev_d) in adm and ('href="/admin?date=%s" aria-label="Next practice"' % next_d) in adm, "only practice days are selectable, including past ones, and the arrows use those days")
    kept = eli.get("/admin?date=2026-10-23&q=Jane").get_data(as_text=True)
    odd = eli.get("/admin?date=2026-10-19").get_data(as_text=True)
    ok('value="2026-10-23"' in kept and 'value="Jane"' in kept and "date=2026-10-20&amp;q=Jane" in kept and 'value="2026-10-19"' in odd and "no practice scheduled" in odd and "grunionsCalDoc" in odd, "a chosen date stays put, and practice links keep the search")
finally:
    A.now_pt = real_now

# members list role menu
ada = A.app.test_client(); join(ada, "Ada", "Role", "ada.role@example.com")
ada_id = D.execute("SELECT id FROM members WHERE email='ada.role@example.com'").fetchone()[0]
menu_page = eli.get("/members").get_data(as_text=True)
ada_at = menu_page.find("ada.role@example.com")
ada_menu = menu_page[menu_page.rfind("<div class=li", 0, ada_at):menu_page.find("<div class=li", ada_at)]
eli_at = menu_page.find("eli@example.com")
eli_menu = menu_page[menu_page.rfind("<div class=li", 0, eli_at):menu_page.find("<div class=li", eli_at)]
ok('class=morebtn' in ada_menu and ">⋯</button>" in ada_menu and "Make admin" in ada_menu and "Add to coaches" in ada_menu and "Add to referees" in ada_menu and "Make active coach" not in ada_menu and "Remove admin" not in ada_menu and ">Remove admin</button>" in eli_menu and "disabled" in eli_menu, "each member has a three-dots menu with admin, coaches, and referees")
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
rae_at = ref_members.find("rae.fern@example.com")
rae_row = ref_members[ref_members.rfind("<div class=li", 0, rae_at):ref_members.find("<div class=li", rae_at)]
ref_filt = eli.get("/members?referee=eligible").get_data(as_text=True)
ref_csv = {r[3]: r for r in list(csvmod.reader(io_mod.StringIO(eli.get("/members.csv").data.decode("utf-8-sig"))))[1:]}
checkin_ref = eli.get("/admin").get_data(as_text=True)
ok('class="st st-ok ref-elig">Referee eligible' in rae_row and "Coach eligible" not in rae_row and "Rae Fern" in ref_filt and "Jane Doe" not in ref_filt and "Riley Quinn" not in ref_filt and ">Referees</a>" in ref_members and 'class="st st-ok ref-elig">Referee eligible' in checkin_ref and ref_csv["rae.fern@example.com"][-2] == "Referee eligible" and ref_csv["jane@example.com"][-2] == "" and "Referee eligible" not in rae.get("/home").get_data(as_text=True), "a referee verification shows Referee eligible on Members, the filter, check-in, and the sheet")
D.execute("UPDATE member_reqs SET expires_on=? WHERE member_id=? AND req_id=?", (ref_past, rae_id, bgid)); D.commit()
expired_row = eli.get("/members").get_data(as_text=True)
rae_exp = expired_row.find("rae.fern@example.com")
rae_exp_row = expired_row[expired_row.rfind("<div class=li", 0, rae_exp):expired_row.find("<div class=li", rae_exp)]
lapsed = "Referee eligibility expired " + ref_past
lapsed_csv = {r[3]: r for r in list(csvmod.reader(io_mod.StringIO(eli.get("/members.csv").data.decode("utf-8-sig"))))[1:]}
ok(('class="st st-bad ref-elig">' + lapsed) in rae_exp_row and 'class="st st-ok ref-elig"' not in rae_exp_row and lapsed in eli.get("/admin").get_data(as_text=True) and lapsed_csv["rae.fern@example.com"][-2] == lapsed and "Rae Fern" not in eli.get("/members?referee=eligible").get_data(as_text=True), "a lapsed referee certification is marked on Members, check-in, and the sheet")
mem_panel = eli.get("/members").get_data(as_text=True)
adm_panel = eli.get("/admin").get_data(as_text=True)
ok("Member # / expires" in mem_panel and "Member # / expires" in adm_panel and "Preferred first name (optional)" in mem_panel and "Preferred first name (optional)" in adm_panel and mem_panel.count('class=panel id=m') == adm_panel.count('class=panel id=m') and "nextElementSibling.toggleAttribute('hidden')" in mem_panel and "bot answered" in adm_panel and ">Cleared<" in adm_panel, "the members list opens the same detail panel as check-in")
ana_at = mem_panel.find("ana@example.com")
ana_li = mem_panel.rfind("<div class=li", 0, ana_at)
ana_row = mem_panel[ana_li:mem_panel.find("<div class=panel", ana_at)]
ok(ana_row.find('class="dot ok"') < ana_row.find(">Ana Lopez<") and "thru " in ana_row and ana_row.find("class=morebtn") > ana_row.find("ana@example.com") and ">Require background</button>" not in mem_panel and "Require background screening" not in mem_panel and "Don't require background" not in mem_panel, "the status dot sits in front of the name, the menu is at the right of the row, and Require background is gone")
renamed = eli.post("/members", data=dict(csrf=csrf(eli, "/members"), member_id=jane_id, action="preferred", preferred_first="Jay"), follow_redirects=True).get_data(as_text=True)
ok("Jay" in renamed and "Legal name" in renamed and D.execute("SELECT preferred_first FROM members WHERE id=?", (jane_id,)).fetchone()[0] == "Jay" and 'value="Jay"' in eli.get("/admin").get_data(as_text=True), "a preferred name saved on the members list shows on check-in")
kay = A.app.test_client(); join(kay, "Kay", "Recheck", "kay.recheck@example.com")
kay_id = D.execute("SELECT id FROM members WHERE email='kay.recheck@example.com'").fetchone()[0]
D.execute("UPDATE members SET usawp_status='verified', usawp_number='303030', usawp_valid_until='2027-01-01', role='athlete', is_admin=0 WHERE id=?", (kay_id,))
D.commit()
shown = eli.get("/members").get_data(as_text=True) + eli.get("/admin").get_data(as_text=True)
ok(shown.count(">Recheck membership<") >= 2 and "name=membership_type" in shown and "name=referee_expires" in shown and "name=safesport_expires" in shown and "name=background_expires" in shown and kay.post("/members", data=dict(csrf=csrf(kay, "/home"), member_id=kay_id, action="recheck", verified="yes")).status_code == 403, "Recheck membership is on the member panel for an admin, and a member cannot save it")
kay_page = eli.get("/members").get_data(as_text=True)
kay_panel = kay_page[kay_page.find('<div class=panel id=m%d' % kay_id):]
kay_next = kay_panel.find("<div class=li")
if kay_next >= 0: kay_panel = kay_panel[:kay_next]
kay_form = kay_panel[kay_panel.find("Recheck membership"):kay_panel.find("</details>")]
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
ok(">Ask Grunions to verify</button>" in kay_form and "Save Sport:80 result" in kay_form and asked.status_code == 200 and ask_hits and ask_hits[0]["requested_by"] == "Eli Joern" and ask_hits[0]["member_submitted"] is False and ask_hits[0]["member_id"] == kay_id and ask_hits[0]["name"] == "Kay Recheck" and D.execute("SELECT status, member_submitted, requested_by FROM verify_requests WHERE member_id=? ORDER BY id DESC LIMIT 1", (kay_id,)).fetchone() == ("pending", 0, "Eli Joern") and kay.post("/members", data=dict(csrf=csrf(kay, "/home"), member_id=kay_id, action="ask_bot")).status_code == 403, "Ask Grunions sits with Recheck membership and still asks the bot for a verified member")
D.execute("DELETE FROM verify_requests WHERE member_id=? AND status='pending'", (kay_id,)); D.commit()
ahead = (A.today_pt() + dt.timedelta(days=50)).isoformat()
eli.post("/members", data=dict(csrf=csrf(eli, "/members"), member_id=kay_id, action="recheck", verified="yes", membership_type="Individual Membership, Coach", valid_until=ahead, safesport_expires=ahead, background_expires=ahead))
who = D.execute("SELECT usawp_status, usawp_verified_by, usawp_verified_at, role, membership_type FROM members WHERE id=?", (kay_id,)).fetchone()
ok(who[0] == "verified" and who[1] == "Eli Joern" and who[2].startswith(A.today_pt().isoformat()) and who[3] == "athlete" and who[4] == "Individual Membership, Coach" and D.execute("SELECT source FROM coaching_list WHERE member_id=?", (kay_id,)).fetchone()[0] == "usawp" and kay.get("/admin").status_code == 403 and kay.get("/chat?c=coaches").status_code == 403 and 'class="st st-ok coach-elig">Coach eligible' in kay.get("/home").get_data(as_text=True) and 'class="st st-ok coach-elig">Coach eligible' in eli.get("/members").get_data(as_text=True) and "class=coach-tag>Coach<" in eli.get("/members").get_data(as_text=True), "a Coach membership recorded from Sport:80 adds the coaching list and the badge without coach access")
D.execute("INSERT INTO verify_requests(member_id,name,email,status,created) VALUES(?,?,?,'pending',?)", (kay_id, "Kay Recheck", "kay.recheck@example.com", A.today_pt().isoformat()))
D.commit()
pending_html = eli.get("/members").get_data(as_text=True)
eli.post("/members", data=dict(csrf=csrf(eli, "/members"), member_id=kay_id, action="recheck", verified="yes", membership_type="Athlete", valid_until=ahead, safesport_expires=ahead, background_expires=ahead, referee_expires=ahead))
ok("class=recheck open" in pending_html and D.execute("SELECT status FROM verify_requests WHERE member_id=? ORDER BY id DESC LIMIT 1", (kay_id,)).fetchone()[0] == "done" and not D.execute("SELECT 1 FROM coaching_list WHERE member_id=? AND source='usawp'", (kay_id,)).fetchone() and 'class="st st-ok ref-elig">Referee eligible' in eli.get("/members").get_data(as_text=True) and D.execute("SELECT role FROM members WHERE id=?", (kay_id,)).fetchone()[0] == "athlete", "the same form answers a pending request and a referee certification makes Referee eligible")
eli.post("/members", data=dict(csrf=csrf(eli, "/members"), member_id=kay_id, action="recheck", verified="yes", membership_type="Athlete", valid_until=ahead, safesport_expires=ahead, background_expires=ahead, referee_expires=(A.today_pt() - dt.timedelta(days=3)).isoformat()))
lapsed_ref = "Referee eligibility expired " + (A.today_pt() - dt.timedelta(days=3)).isoformat()
ok(lapsed_ref in eli.get("/members").get_data(as_text=True) and "Kay Recheck" not in eli.get("/members?referee=eligible").get_data(as_text=True), "a past referee certification is marked expired")
eli.post("/members", data=dict(csrf=csrf(eli, "/members"), member_id=kay_id, action="recheck", verified="no", membership_type="Head Coach", valid_until=ahead))
ok(D.execute("SELECT usawp_status, role FROM members WHERE id=?", (kay_id,)).fetchone() == ("expired", "athlete") and not D.execute("SELECT 1 FROM coaching_list WHERE member_id=? AND source='usawp'", (kay_id,)).fetchone(), "a not-verified recheck does not add a coach membership to the coaching list")
D.execute("UPDATE members SET trial_acknowledged_at=?, usawp_status='unknown', usawp_valid_until=NULL WHERE id=?", (A.today_pt().isoformat(), jane_id))
D.commit()
trial_page = eli.get("/members").get_data(as_text=True)
jat = trial_page.find("jane@example.com")
jchunk = trial_page[trial_page.rfind("<div class=li", 0, jat):trial_page.find("<div class=panel", jat)]
jpre = jchunk[:jchunk.find("jane@example.com")]
ok(jpre.rstrip().endswith("Ends " + A.fmt_md((A.today_pt() + dt.timedelta(days=14)).isoformat()) + " ·") and jchunk.count("Ends ") == 1 and "practices" in jchunk[jchunk.find("jane@example.com"):], "the members second line leads with the trial end date, then email and practice count")

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
ok(('href="/practices/%d"' % dpid) in sched_j and " going</span>" in card_e and "class=datetile" in card_e and "class=pills" in card_e and "I'm going" in card_e and "I'm not going" in card_e and "class=nxchev" in card_e and "class=morebtn" not in card_e and "Assign coaches" not in card_e and "Delete practice" not in card_e and "class=morebtn" not in sched_e and "class=morebtn" not in sched_j, "a schedule card matches the next-practice layout and has no More menu")
page_j = jane.get("/practices/%d" % dpid).get_data(as_text=True)
page_e = eli.get("/practices/%d" % dpid).get_data(as_text=True)
ok(jane.get("/practices/999999").status_code == 404 and "Detail Pool" in page_j and "Bring caps" in page_j and "Jay Doe" in page_j and "Eli Joern" in page_j and "Checked in" in page_j and "Can't make it" in page_j and "maps.google.com/maps?q=" in page_j and "Detail" in page_j and ">Directions</a>" in page_j and "Scheduled" in page_j and ">Edit</a>" not in page_j and "Assign coaches" not in page_j and "class=morebtn" not in page_j and "No assigned coach is coach-eligible" not in page_j and "No assigned coach is coach-eligible" in page_e and ">Edit</a>" in page_e and "class=morebtn" in page_e and "Assign coaches" in page_e and "Delete practice" in page_e, "the practice page shows who's coming, the map, and an admin-only edit button, More menu, and coach warning")
editp = eli.get("/practices/%d?edit=1" % dpid).get_data(as_text=True)
ok('name=date' in editp and 'name=start' in editp and 'name=location' in editp and "name=note" in editp and ">Save</button>" in editp and ">Cancel</a>" in editp and 'name=date' not in jane.get("/practices/%d?edit=1" % dpid).get_data(as_text=True), "admins edit the practice on the page, and members stay in read mode")
eli.post("/practices/%d" % dpid, data=dict(csrf=csrf(eli, "/practices/%d" % dpid), pid=dpid, action="edit", back="page", date=pday, start="18:30", end="20:00", location="Detail Pool", note="Caps and fins"))
saved = D.execute("SELECT start, note FROM practices WHERE id=?", (dpid,)).fetchone()
ok(saved == ("18:30", "Caps and fins") and "Caps and fins" in eli.get("/practices/%d" % dpid).get_data(as_text=True) and jane.post("/practices/%d" % dpid, data=dict(csrf=csrf(jane, "/home"), pid=dpid, action="edit", date=pday, start="18:30", end="20:00", location="Detail Pool", note="nope")).status_code == 403, "saving the practice page stores the new time and note")
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
nstart = home0.find("NEXT PRACTICE")
card_at = home0.rfind('class="card tap nextcard"', 0, nstart)
nchunk = home0[card_at:home0.find("</form>", nstart)]
nid = int(re.search(r'href="/practices/(\d+)"', nchunk).group(1))
nrow = D.execute("SELECT date, start, end, location, COALESCE(note,'') FROM practices WHERE id=?", (nid,)).fetchone()
ok("I'm going" in nchunk and "I'm not going" in nchunk and ('href="/practices/%d"' % nid) in nchunk and "card tap" in nchunk and "🍻" not in nchunk and "After-practice social" not in jane.get("/practices").get_data(as_text=True), "the next practice card links to the practice and offers I'm going and I'm not going")
ok(jane.post("/practices/%d" % nid, data=dict(csrf=csrf(jane, "/home"), pid=nid, action="social", social_kind="Drinks", social_place="The Harp")).status_code == 403 and jane.post("/practices/%d" % nid, data=dict(csrf=csrf(jane, "/home"), pid=nid, action="message", message="hi")).status_code == 403, "a member cannot set a social or a coach message")
missing = eli.post("/practices/%d" % nid, data=dict(csrf=csrf(eli, "/practices"), pid=nid, action="social", back="page", social_kind="Dinner", social_place=""), follow_redirects=True).get_data(as_text=True)
empty_host = pat.get("/practices/%d" % nid).get_data(as_text=True)
ok("Add a place for the social." in missing and "🍽️" not in jane.get("/practices/%d" % nid).get_data(as_text=True) and "<h2>After-practice social</h2>" not in jane.get("/practices/%d" % nid).get_data(as_text=True) and "<h2>After-practice social</h2>" in empty_host and ">Add<" in empty_host, "a social needs a place, and only a host sees Add when there is none")
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
ok((line + " · 8:30pm") in page_s and "Cash bar" in page_s and 'href="https://maps.example/harp"' in page_s and line not in card_s and "class=nxicon" not in card_s and "class=nxicon" in page_s and "class=nxicon" in home_s and "🍽️" not in home_s and "🍽️" not in page_s and "Cash bar" not in card_s and "Bring dark caps" in card_s and noted[0] == "Pat Host" and stamp in card_s and "Drinks after" in home_s and "The Harp" in home_s and "Bring dark caps" in home_s and stamp in home_s and "class=morebtn" not in pat_card and "class=morebtn" not in eli_card and "After-practice social" in pat_page and "Coach message" in pat_page and "Delete practice" not in pat_page and "After-practice social" in eli_page and "Delete practice" in eli_page and "name=date" not in pat.get("/practices/%d?edit=1" % nid).get_data(as_text=True), "a social shows on the practice page and home, not the schedule, and a coach message still shows on the schedule")
jane.post("/practices", data=dict(csrf=csrf(jane, "/home"), pid=nid, action="notgoing"))
ok(">I'm not going ✓<" in jane.get("/home").get_data(as_text=True) and ">Can't make it ✓<" in jane.get("/practices/%d" % nid).get_data(as_text=True) and ">I'm not going ✓<" in jane.get("/practices").get_data(as_text=True).split("id=p%d " % nid, 1)[1].split("id=p")[0], "I'm not going on home is the same RSVP as the practice page and the schedule")
jane.post("/practices/%d" % nid, data=dict(csrf=csrf(jane, "/practices/%d" % nid), pid=nid, action="going", back="page"))
ok(">I'm going ✓<" in jane.get("/home").get_data(as_text=True) and ">Going ✓<" in jane.get("/practices/%d" % nid).get_data(as_text=True) and ">I'm going ✓<" in jane.get("/practices").get_data(as_text=True).split("id=p%d " % nid, 1)[1].split("id=p")[0], "I'm going on the practice page shows on home and the schedule")
pat.post("/practices/%d" % nid, data=dict(csrf=csrf(pat, "/practices"), pid=nid, action="social", back="page", social_kind=["Dinner", "Drinks"], social_place="The Harp", social_address="https://maps.example/harp", social_time="20:30", social_note="Cash bar"))
combo = "Dinner &amp; drinks after at The Harp"
member_page = jane.get("/practices/%d" % nid).get_data(as_text=True)
host_page = pat.get("/practices/%d" % nid).get_data(as_text=True)
ok(D.execute("SELECT social_kind FROM practices WHERE id=?", (nid,)).fetchone()[0] == "Dinner,Drinks" and combo in member_page and "Dinner &amp; drinks after" in jane.get("/home").get_data(as_text=True) and "The Harp" in jane.get("/home").get_data(as_text=True) and combo not in jane.get("/practices").get_data(as_text=True) and member_page.find("<h2>After-practice social</h2>") < member_page.find("<h2>Coaches</h2>") < member_page.find("<h2>Going") and ">Edit<" not in member_page and ">Add<" not in member_page and ">Edit<" in host_page and 'type=checkbox name=social_kind value="Dinner" checked' in host_page and 'type=checkbox name=social_kind value="Drinks" checked' in host_page and "None</option>" not in host_page, "types combine on the practice section and home, and a host edits them")
D.execute("UPDATE practices SET social_kind='Social,Dinner' WHERE id=?", (nid,)); D.commit()
A.migrate_social_kinds(D); D.commit()
ok(D.execute("SELECT social_kind FROM practices WHERE id=?", (nid,)).fetchone()[0] == "Dinner,Social" and "Dinner &amp; social after at The Harp" not in jane.get("/practices").get_data(as_text=True) and "Dinner &amp; social after" in jane.get("/home").get_data(as_text=True), "an older combination is stored as Dinner, then Drinks, then Social")
pat.post("/practices/%d" % nid, data=dict(csrf=csrf(pat, "/practices"), pid=nid, action="social", back="page", social_kind=["Dessert", "Coffee", "Other"], social_place="The Harp"))
kind_box = pat.get("/practices/%d" % nid).get_data(as_text=True)
kind_order = [kind_box.find('value="%s"' % k) for k in A.SOCIAL_KINDS]
ok(D.execute("SELECT social_kind FROM practices WHERE id=?", (nid,)).fetchone()[0] == "Coffee,Dessert,Other" and "Coffee &amp; dessert &amp; other after at The Harp" not in jane.get("/practices").get_data(as_text=True) and "Coffee &amp; dessert &amp; other after" in jane.get("/home").get_data(as_text=True) and kind_order == sorted(kind_order) and all(i > 0 for i in kind_order) and tuple(A.SOCIAL_KINDS) == ("Dinner", "Drinks", "Social", "Coffee", "Dessert", "Activities", "Potluck", "Other"), "social types include coffee, dessert, activities, potluck, and other, in that order")
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
