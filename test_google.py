"""Sign in with Google tests (Google is mocked). Run: .venv/bin/python -m pytest -q test_google.py"""
import os, re, tempfile, sqlite3
from urllib.parse import urlparse, parse_qs
os.environ.update(DATA_DIR=tempfile.mkdtemp(), ADMIN_EMAIL="boss@example.com", DEV_SHOW_LINKS="0", PUBLIC_URL="https://grunions.example.org",
                  GOOGLE_CLIENT_ID="cid.apps.googleusercontent.com", GOOGLE_CLIENT_SECRET="sec", SECURE_COOKIES="0")
for k in ("GRUNIONS_DB", "GRUNIONS_UPLOADS"): os.environ.pop(k, None)
import app as A
INFO = {}
A.google_userinfo = lambda: dict(INFO)
def csrf(c, p): return re.search(r'name=csrf value="([^"]+)"', c.get(p).get_data(as_text=True)).group(1)
c0 = A.app.test_client(); c0.post("/join", data=dict(csrf=csrf(c0, "/join"), first="Jane", last="Doe", email="Jane@Example.com", phone="1"))
def q(sql, *a): return sqlite3.connect(A.DB).execute(sql, a).fetchall()
def cb(info):
    INFO.clear(); INFO.update(info); c = A.app.test_client(); return c, c.get("/auth/google/callback?code=x&state=y", follow_redirects=True).get_data(as_text=True)

def test_button_shown_above_email_option():
    t = A.app.test_client().get("/login").get_data(as_text=True)
    assert "Sign in with Google" in t and t.index("Sign in with Google") < t.index("Send login link") and 'href=/auth/google' in t
def test_button_hidden_without_config():
    saved = A.GOOGLE_CLIENT_SECRET; A.GOOGLE_CLIENT_SECRET = None
    try:
        c = A.app.test_client(); assert "Sign in with Google" not in c.get("/login").get_data(as_text=True)
        assert c.get("/auth/google").status_code == 404 and c.get("/auth/google/callback").status_code == 404
    finally: A.GOOGLE_CLIENT_SECRET = saved
def test_authorize_redirect_has_state_nonce_and_callback():
    g = A.google_client(); g.server_metadata.update(authorization_endpoint="https://accounts.google.com/o/oauth2/v2/auth", _loaded_at=1)
    r = A.app.test_client().get("/auth/google"); assert r.status_code == 302
    u = urlparse(r.headers["Location"]); p = parse_qs(u.query)
    assert u.netloc == "accounts.google.com" and p["redirect_uri"] == ["https://grunions.example.org/auth/google/callback"]
    assert p["state"][0] and p["nonce"][0] and "openid" in p["scope"][0] and p["client_id"] == ["cid.apps.googleusercontent.com"]
def test_existing_member_case_insensitive():
    c, t = cb({"email": "JANE@example.COM", "email_verified": True, "given_name": "X"})
    assert "Hi, Jane" in t and q("SELECT COUNT(*) FROM members")[0][0] == 1
def test_unverified_email_rejected():
    c, t = cb({"email": "jane@example.com", "email_verified": False}); assert "isn't verified" in t and c.get("/home").status_code == 302
def test_new_member_created_not_admin():
    c, t = cb({"email": "new@gmail.com", "email_verified": True, "given_name": "Nina", "family_name": "New"})
    assert "Welcome to the Grunions, Nina" in t and q("SELECT first,last,is_admin FROM members WHERE email='new@gmail.com'") == [("Nina", "New", 0)]
    assert c.get("/admins").status_code == 403
def test_admin_only_via_admin_email():
    c, t = cb({"email": "Boss@Example.com", "email_verified": True, "name": "Big Boss"})
    assert q("SELECT first,last,is_admin FROM members WHERE email='boss@example.com'") == [("Big", "Boss", 1)]
def test_oauth_error_handled():
    def boom(): raise ValueError("mismatching_state")
    saved = A.google_userinfo; A.google_userinfo = boom
    try: c, t = cb({}); assert "didn't work" in t
    finally: A.google_userinfo = saved
