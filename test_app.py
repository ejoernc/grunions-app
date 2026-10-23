import os, re, tempfile
os.environ["GRUNIONS_DB"] = tempfile.mktemp(suffix=".db"); os.environ["ADMIN_EMAIL"] = "eli@example.com"; os.environ["DEV_SHOW_LINKS"] = "1"
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
    t = eli.post("/import", data=dict(csrf=csrf(eli, "/import"), file=(f, "x.csv")), content_type="multipart/form-data").get_data(as_text=True)
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
t = eli.get("/members").get_data(as_text=True); r = eli.get("/members.csv").get_data(as_text=True)
ok("John,Smith,john@example.com,555-0100,verified,Manually verified,7654321,2027-08-31,Eli Joern," in r, "manual verify records number, date, admin, time")
eli.post("/admin", data=dict(csrf=tok_e, member_id=1, date="2026-10-27", action="verify", valid_until="2020-01-01"))
ok("Eli,Joern,eli@example.com,555-0100,unknown" in eli.get("/members.csv").get_data(as_text=True), "past valid-until rejected")
# expiry
import datetime as dt, sqlite3
join(A.app.test_client(), "Ana", "Lopez", "ana@example.com")
D = sqlite3.connect(os.environ["GRUNIONS_DB"]); soon = (dt.date.today()+dt.timedelta(days=5)).isoformat()
eli.post("/admin", data=dict(csrf=tok_e, member_id=4, date="2026-10-27", action="verify", valid_until=soon))
ok("Please enter the expiration" in eli.post("/admin", data=dict(csrf=tok_e, member_id=1, date="2026-10-27", action="verify"), follow_redirects=True).get_data(as_text=True), "Mark verified asks for expiration date")
D.execute("UPDATE members SET usawp_status='verified', usawp_valid_until=? WHERE id=2", ((dt.date.today()-dt.timedelta(days=1)).isoformat(),)); D.commit()
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
p = jane.get("/practices").get_data(as_text=True); ok("Marina High School" in p and "Westminster High School" in p, "recurring Tue/Fri practices generated")
pid = D.execute("SELECT id, date FROM practices WHERE location='Marina High School' ORDER BY date LIMIT 1").fetchone()
tj2 = csrf(jane, "/practices"); jane.post("/practices", data=dict(csrf=tj2, pid=pid[0], action="going"))
john.post("/practices", data=dict(csrf=tj, pid=pid[0], action="notgoing"))
ok("1 going" in jane.get("/practices").get_data(as_text=True), "RSVP headcount")
ok(jane.post("/practices", data=dict(csrf=tj2, pid=pid[0], action="cancel")).status_code == 403, "members cannot cancel practices")
c = eli.get("/admin?date=%s" % pid[1]).get_data(as_text=True)
ok("1 RSVP'd" in c and c.index("Jane Doe") < c.index("Eli Joern") and "RSVP ✓" in c and "Not cleared" in c, "check-in lists RSVPs first, flags not-cleared")
eli.post("/practices", data=dict(csrf=tok_e, pid=pid[0], action="edit", start="19:30", end="21:00", location="Marina High School", note="Pool B"))
eli.post("/practices", data=dict(csrf=tok_e, pid=pid[0], action="cancel"))
ok(tuple(D.execute("SELECT cancelled, start, note FROM practices WHERE id=?", (pid[0],)).fetchone()) == (1, "19:30", "Pool B"), "admin edit + cancel practice")
eli.post("/practices", data=dict(csrf=tok_e, action="add", date="2026-12-05", start="09:00", end="11:00", location="Huntington Beach", note="Holiday scrimmage"))
ok(D.execute("SELECT COUNT(*) FROM practices WHERE date='2026-12-05'").fetchone()[0] == 1, "admin add practice")
ok("Not cleared to play" in x.get("/home").get_data(as_text=True), "member home shows Not cleared (membership ok, compliance missing)")
D.execute("UPDATE members SET usawp_status='verified', usawp_valid_until='2027-08-31' WHERE id=2"); D.commit()
eli.post("/admin", data=dict(csrf=tok_e, member_id=2, date="2026-10-27", action="req", req_id=1, completed_on="2026-01-10", expires_on="2027-01-10"))
eli.post("/admin", data=dict(csrf=tok_e, member_id=2, date="2026-10-27", action="req", req_id=3, completed_on="2026-10-01"))
h = x.get("/home").get_data(as_text=True); ok("Cleared to play" in h and "Not cleared to play" not in h, "manual compliance entry -> Cleared")
D.execute("UPDATE member_reqs SET expires_on=? WHERE member_id=2 AND req_id=1", ((dt.date.today()+dt.timedelta(days=10)).isoformat(),)); D.commit()
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
ok("Webhook sent" in r and body == {"request_id": body.get("request_id"), "member_id": 4, "name": "Ana Lopez", "preferred_first": None, "email": "ana@example.com", "member_number": None, "requested_by": "Eli Joern", "app_url": "https://grunions.example"} and hits[0]["authorization"] is None and hits[0]["content_type"] == "application/json", "Ask Grunions creates request + POSTs webhook")
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
ok(cm[-1]["who"].startswith("Grunions") and "Ana Lopez" in cm[-1]["body"], "bot posts result in #coaches")
a = eli.get("/admin?date=2026-10-27").get_data(as_text=True)
ok("Verification for Ana Lopez" in a and "bot answered" in a, "admin notification + answered state")
ok("Grunions bot" not in eli.get("/members").get_data(as_text=True).split("verified by")[0] and "bot@grunions.local" not in eli.get("/members").get_data(as_text=True), "bot account hidden from member list")
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
ok('class=gobtn aria-expanded=false' in pg and re.search(r'id=who\d+ class="t2 sm" hidden', pg), "schedule 'N going' toggles hidden list")
ch = jane.get("/chat").get_data(as_text=True)
ca = eli.get("/chat").get_data(as_text=True)
cc = eli.get("/chat?c=coaches").get_data(as_text=True)
ok("rows=1" in ch and "scrollbar-width:none" in ch and "shiftKey" in ch and 'id=attach' in ch and 'id=ann' not in ca and '>Announce<' not in ca and 'id=ann' not in cc and '>Announce<' not in cc and 'aria-label=Send' in ch and 'aria-label=Send' in ca and 'aria-label=Send' in cc and 'class="iconbtn send"' in ch and 'class="iconbtn send"' in cc, "composer: icon send on team and coaches, no announce checkbox")

# member USAWP number on the Not cleared card
jh = jane.get("/home").get_data(as_text=True)
jp = jane.post("/home", data=dict(csrf=csrf(jane, "/home"), usawp_number="99998888"), follow_redirects=True).get_data(as_text=True)
ok("Not cleared to play" in jh and "USAWP # 1234567" in jh and "name=usawp_number" not in jh and ">Edit<" not in jh and "already verified" in jp and D.execute("SELECT usawp_number FROM members WHERE email='jane@example.com'").fetchone()[0] == "1234567", "verified member sees read-only USAWP number; Edit is hidden and the number cannot be changed")
D.execute("UPDATE member_reqs SET expires_on='2027-06-01' WHERE member_id=2 AND req_id=1"); D.commit()
ok("USAWP Membership #" not in jane.get("/home").get_data(as_text=True) and "USAWP # 1234567" in jane.get("/home").get_data(as_text=True) and "Cleared to play" in jane.get("/home").get_data(as_text=True), "form hidden once verified and cleared; number stays read-only")
sam = A.app.test_client(); join(sam, "Sam", "River", "sam@example.com")
sh = sam.get("/home").get_data(as_text=True)
ok('name=usawp_number inputmode=numeric value=""' in sh and "USAWP Membership #" in sh and "Not cleared to play" in sh and 'class="st st-bad">Not cleared' in sh and "Verification pending" not in sh, "empty membership form for a new member")
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
ok(page.status_code == 200 and 'class="toast noprint" role=status>Sent to Grunions for verification' in sp and "setTimeout" in sp and "3000" in sp and "Verification pending" in sp and 'class="st st-warn">Pending' in sp and 'class="st st-bad">Not cleared' not in sp and "USAWP # 4321" in sp and ">Edit<" in sp and "id=usawpForm hidden" in sp and "name=usawp_number" not in sp.split("id=usawpForm")[0] and D.execute("SELECT usawp_number FROM members WHERE id=?", (sid,)).fetchone()[0] == "4321" and vr[1] == "4321" and vr[2] == "pending", "submit saves number, hides the input, toasts, and shows Pending")
ok(_spy.timeout == 5 and len(hits) == before + 1 and body == {"request_id": vr[0], "member_id": sid, "name": "Sam River", "preferred_first": None, "email": "sam@example.com", "member_number": "4321", "requested_by": "Sam River", "app_url": "https://grunions.example"}, "member submit POSTs the webhook payload with a 5s timeout")
ok("verification requested" in eli.get("/admin").get_data(as_text=True) and any(x["id"] == vr[0] and x["member_number"] == "4321" and x["status"] == "pending" for x in c0.get("/api/verify-requests?status=pending", headers=H).get_json()), "request shows in admin and on the bot API")
quiet = sam.get("/home").get_data(as_text=True)
ok("class=\"toast" not in quiet and "Sent to Grunions for verification" not in quiet and "Verification pending" in quiet and 'class="st st-warn">Pending' in quiet and "USAWP # 4321" in quiet and ">Edit<" in quiet, "reload keeps the pending card without repeating the toast")
edit = sam_post("55555")
ok(tuple(D.execute("SELECT COUNT(*), MAX(member_number) FROM verify_requests WHERE member_id=? AND status='pending'", (sid,)).fetchone()) == (1, "55555") and len(hits) == before + 2 and hits[-1]["json"]["request_id"] == vr[0] and hits[-1]["json"]["member_number"] == "55555" and 'class="toast noprint" role=status>Sent to Grunions for verification' in edit.get_data(as_text=True) and "USAWP # 55555" in edit.get_data(as_text=True) and D.execute("SELECT requested_by FROM verify_requests WHERE id=?", (vr[0],)).fetchone()[0] == "Sam River", "edit save updates the pending number, re-sends the webhook, and toasts again")
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
ok(res["ok"] and D.execute("SELECT status FROM verify_requests WHERE id=?", (vr[0],)).fetchone()[0] == "done" and tuple(D.execute("SELECT usawp_status, usawp_number FROM members WHERE id=?", (sid,)).fetchone()) == ("verified", "666666") and "Cleared to play" in shome and 'class="st st-ok">Cleared' in shome and "Verification pending" not in shome and "USAWP Membership #" not in shome and "USAWP # 666666" in shome and ">Edit<" not in shome, "bot result answers the member request and shows Cleared with a read-only number")
kr = D.execute("SELECT id FROM verify_requests WHERE member_id=? AND status='pending'", (kid,)).fetchone()
c0.post("/api/verify-requests/%d/result" % kr[0], headers=H, json={"verified": False, "note": "no matching membership"})
kh = kim.get("/home").get_data(as_text=True)
ok("Not cleared to play" in kh and 'class="st st-bad">Not cleared' in kh and "Verification pending" not in kh and "USAWP # 10003" in kh and ">Edit<" in kh, "bot not-verified result restores the red Not cleared card")
