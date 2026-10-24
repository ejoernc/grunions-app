"""Tests for roles page, login emails, reset_real, import tolerance, deploy config. Run: .venv/bin/python -m pytest -q test_v2.py"""
import os, re, sys, json, tempfile, sqlite3, subprocess, datetime as dt
D = tempfile.mkdtemp()
os.environ.update(DATA_DIR=D, ADMIN_EMAIL="boss@example.com, second@example.com", DEV_SHOW_LINKS="0",
                  SMTP_HOST="smtp.test", SMTP_PORT="587", SMTP_USER="u", SMTP_PASSWORD="p", MAIL_FROM="Grunions <team@test>")
os.environ.pop("GRUNIONS_DB", None); os.environ.pop("GRUNIONS_UPLOADS", None)
import app as A
SENT = []
A.send_email = lambda to, subj, text: SENT.append((to, subj, text))
HERE = os.path.dirname(os.path.abspath(__file__))
def csrf(c, p): return re.search(r'(?:name=csrf value=|const CSRF=)"([^"]+)"', c.get(p).get_data(as_text=True)).group(1)
def join(first, last, email):
    c = A.app.test_client(); c.post("/join", data=dict(csrf=csrf(c, "/join"), first=first, last=last, email=email, phone="1")); return c
boss = join("Boss", "One", "boss@example.com"); sec = join("Sec", "Two", "second@example.com"); mem = join("Mem", "Three", "mem@example.com")
def ids(): return {r[0]: r[1] for r in sqlite3.connect(A.DB).execute("SELECT email,id FROM members")}
def is_admin(e): return sqlite3.connect(A.DB).execute("SELECT is_admin FROM members WHERE email=?", (e,)).fetchone()[0]
def act(c, mid, a): return c.post("/admins", data=dict(csrf=csrf(c, "/admins"), member_id=mid, action=a), follow_redirects=True)

def test_data_dir_used(): assert A.DB == os.path.join(D, "grunions.db") and A.UPLOADS == os.path.join(D, "uploads") and os.path.exists(A.DB)
def test_multi_admin_bootstrap(): assert is_admin("boss@example.com") and is_admin("second@example.com") and not is_admin("mem@example.com")
def test_roles_page_admin_only():
    assert mem.get("/admins").status_code == 403 and boss.get("/admins").status_code == 200
    assert "mem@example.com" in boss.get("/admins").get_data(as_text=True)
    assert mem.post("/admins", data=dict(csrf=csrf(mem, "/home"), member_id=1, action="make_admin")).status_code == 403
def test_promote_demote_and_coach():
    m = ids()["mem@example.com"]; act(boss, m, "make_admin"); assert is_admin("mem@example.com")
    act(boss, m, "remove_admin"); assert not is_admin("mem@example.com")
    act(boss, m, "make_coach"); assert sqlite3.connect(A.DB).execute("SELECT role FROM members WHERE id=?", (m,)).fetchone()[0] == "coach"
    assert mem.get("/admin").status_code == 200  # coach can open check-in
    act(boss, m, "remove_coach"); assert mem.get("/admin").status_code == 403
def test_bootstrap_admin_not_removable():
    act(boss, ids()["boss@example.com"], "remove_admin"); assert is_admin("boss@example.com")
def test_last_admin_guard():
    saved = A.ADMIN_EMAILS; A.ADMIN_EMAILS = set()
    try:
        db = sqlite3.connect(A.DB); db.execute("UPDATE members SET is_admin=0 WHERE email!='boss@example.com'"); db.commit()
        t = act(boss, ids()["boss@example.com"], "remove_admin").get_data(as_text=True)
        assert "last admin" in t and is_admin("boss@example.com")
        boss.post("/admin", data=dict(csrf=csrf(boss, "/admin"), member_id=ids()["boss@example.com"], action="role", role="member"))
        assert is_admin("boss@example.com")
        act(boss, ids()["mem@example.com"], "make_admin"); act(boss, ids()["boss@example.com"], "remove_admin")
        assert not is_admin("boss@example.com") and is_admin("mem@example.com")  # allowed once someone else is admin
        db.execute("UPDATE members SET is_admin=1 WHERE email IN ('boss@example.com','second@example.com')"); db.execute("UPDATE members SET is_admin=0 WHERE email='mem@example.com'"); db.commit()
    finally: A.ADMIN_EMAILS = saved
def test_login_email_sent_no_link_on_screen():
    SENT.clear(); c = A.app.test_client()
    t = c.post("/login", data=dict(csrf=csrf(c, "/login"), email="mem@example.com"), follow_redirects=True).get_data(as_text=True)
    assert "/auth/" not in t and "15 minutes" in t and len(SENT) == 1 and SENT[0][0] == "mem@example.com"
    link = re.search(r"(https?://\S+/auth/\S+)", SENT[0][2]).group(1); path = "/auth/" + link.split("/auth/")[1]
    assert "Hi, Mem" in c.get(path, follow_redirects=True).get_data(as_text=True)
    assert "invalid or expired" in A.app.test_client().get(path, follow_redirects=True).get_data(as_text=True)
def test_login_link_expires():
    SENT.clear(); c = A.app.test_client(); c.post("/login", data=dict(csrf=csrf(c, "/login"), email="mem@example.com"))
    path = "/auth/" + SENT[0][2].split("/auth/")[1].split()[0]
    db = sqlite3.connect(A.DB); db.execute("UPDATE login_tokens SET expires=? WHERE used=0", ((dt.datetime.utcnow() - dt.timedelta(minutes=1)).isoformat(),)); db.commit()
    assert "invalid or expired" in c.get(path, follow_redirects=True).get_data(as_text=True)
def test_unknown_email_no_send():
    SENT.clear(); c = A.app.test_client(); c.post("/login", data=dict(csrf=csrf(c, "/login"), email="nobody@x.com")); assert SENT == []
def test_import_tolerant_columns():
    csv = ("Report title\n" "First Name,Last Name,Email Address,ID Number,Contact ID,Membership Expiry Date,SafeSport Expiry Date\n"
           f"Mem,Three,MEM@example.com,659999,C-42,{(A.today_pt()+dt.timedelta(days=200)).isoformat()},2027-05-11\n").encode()
    import io
    t = boss.post("/import", data=dict(csrf=csrf(boss, "/import"), file=(io.BytesIO(csv), "x.csv")), content_type="multipart/form-data").get_data(as_text=True)
    r = sqlite3.connect(A.DB).execute("SELECT usawp_status, usawp_number, sport80_contact_id FROM members WHERE email='mem@example.com'").fetchone()
    assert r == ("verified", "659999", "C-42"), (r, t)
def test_reset_real():
    db_path = os.path.join(tempfile.mkdtemp(), "r.db")
    env = dict(os.environ, DATA_DIR=os.path.dirname(db_path), GRUNIONS_DB=db_path, ADMIN_EMAIL="eli@example.com", DEV_SHOW_LINKS="1")
    subprocess.run([sys.executable, "seed_demo.py"], cwd=HERE, env=env, check=True, capture_output=True)
    up = os.path.join(os.path.dirname(db_path), "uploads"); os.makedirs(up, exist_ok=True); open(os.path.join(up, "x.webp"), "w").close()
    p = subprocess.run([sys.executable, "reset_real.py", "--yes"], cwd=HERE, env=env, capture_output=True, text=True); assert p.returncode == 0, p.stderr
    db = sqlite3.connect(db_path)
    assert db.execute("SELECT first,last,email,is_admin,usawp_status,usawp_number,usawp_valid_until FROM members WHERE COALESCE(role,'')!='system'").fetchall() == \
        [("Elliott", "Joern", "elliott.joern@gmail.com", 1, "verified", "659226", "2027-06-07")]
    for t in ("messages", "reactions", "checkins", "verify_requests", "rsvps", "notices", "login_tokens"): assert db.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0] == 0, t
    assert db.execute("SELECT COUNT(*) FROM requirements").fetchone()[0] >= 3
    assert db.execute("SELECT COUNT(*) FROM requirements WHERE lower(name) LIKE '%waiver%' OR lower(ifnull(keywords,'')) LIKE '%waiver%'").fetchone()[0] == 0
    reqs = dict(db.execute("SELECT q.name, x.expires_on FROM member_reqs x JOIN requirements q ON q.id=x.req_id").fetchall())
    assert reqs["SafeSport training"] == "2027-05-11" and reqs["Background screening"] == "2028-08-28"
    locs = {r[0] for r in db.execute("SELECT location FROM practices")}; assert locs == {"Marina High School", "Westminster High School"}
    assert os.listdir(up) == []
def test_reset_requires_confirmation():
    p = subprocess.run([sys.executable, "reset_real.py"], cwd=HERE, env=dict(os.environ, GRUNIONS_DB=os.path.join(tempfile.mkdtemp(), "z.db")), input="no\n", capture_output=True, text=True)
    assert p.returncode != 0
def test_deploy_files():
    req = open(os.path.join(HERE, "requirements.txt"), encoding="utf-8").read()
    for pkg in ("flask", "gunicorn", "qrcode", "pillow", "openpyxl"): assert pkg in req.lower()
    docker = open(os.path.join(HERE, "Dockerfile"), encoding="utf-8").read()
    assert "gunicorn" in docker and "COPY static" in docker
    ry = open(os.path.join(HERE, "render.yaml"), encoding="utf-8").read(); assert "DATA_DIR" in ry and "disk" in ry and "SECRET_KEY" in ry
    assert "elliott.joern@gmail.com" in open(os.path.join(HERE, ".env.local"), encoding="utf-8").read()
    from PIL import Image
    for name, size in (("icon-192.png", 192), ("icon-512.png", 512), ("maskable-512.png", 512), ("apple-touch-icon-180.png", 180), ("favicon-32.png", 32)):
        assert Image.open(os.path.join(HERE, "static", "icons", name)).size == (size, size)
    c = A.app.test_client()
    m = c.get("/manifest.webmanifest"); body = json.loads(m.get_data(as_text=True))
    assert m.content_type.startswith("application/manifest+json") and body["name"] == "Grunions Water Polo" and body["short_name"] == "Grunions" and body["display"] == "standalone"
    assert body["theme_color"] == "#0a0a0b" and body["background_color"] == "#0a0a0b" and "maskable" in {i["purpose"] for i in body["icons"]}
    icon = c.get("/static/icons/icon-192.png"); assert icon.status_code == 200 and icon.data[:8] == b"\x89PNG\r\n\x1a\n"
    html = c.get("/join").get_data(as_text=True)
    assert "rel=manifest" in html and "rel=icon" in html and "rel=apple-touch-icon" in html and 'name=theme-color content="#0a0a0b"' in html
def test_utf8_and_no_dash_strftime():
    for f in os.listdir(HERE):
        if f.endswith((".py", ".md", ".txt", ".yaml")) or f in ("Dockerfile",):
            s = open(os.path.join(HERE, f), "rb").read().decode("utf-8")
            if f.endswith(".py") and f != "test_v2.py": assert not re.search(r"%-[a-zA-Z]", s), f
def test_preferred_first_migration():
    path = os.path.join(tempfile.mkdtemp(), "old.db")
    raw = sqlite3.connect(path)
    raw.execute("CREATE TABLE members(id INTEGER PRIMARY KEY, first TEXT NOT NULL, last TEXT NOT NULL, email TEXT NOT NULL UNIQUE, phone TEXT)")
    raw.execute("INSERT INTO members(first,last,email,phone) VALUES('Old','Member','old@example.com','1')")
    A.migrate_members(raw); A.migrate_members(raw); raw.commit()
    cols = [r[1] for r in raw.execute("PRAGMA table_info(members)")]
    assert "preferred_first" in cols and "trial_acknowledged_at" in cols
    assert raw.execute("SELECT preferred_first, trial_acknowledged_at FROM members").fetchone() == (None, None)
def test_preferred_first_display_and_legal_verify():
    join_page = A.app.test_client().get("/join").get_data(as_text=True)
    assert "Preferred first name (optional)" in join_page and "Leave blank to use your legal first name" in join_page
    blank = A.app.test_client()
    blank.post("/join", data=dict(csrf=csrf(blank, "/join"), first="Zoe", last="Blank", email="zoe@example.com", phone="1", preferred_first="   "))
    assert sqlite3.connect(A.DB).execute("SELECT preferred_first FROM members WHERE email='zoe@example.com'").fetchone()[0] is None
    assert "<h1>Hi, Zoe</h1>" in blank.get("/home").get_data(as_text=True)
    c = A.app.test_client()
    c.post("/join", data=dict(csrf=csrf(c, "/join"), first="Samuel", last="River", email="samuel@example.com", phone="1", preferred_first="  Sam  "), follow_redirects=True)
    assert sqlite3.connect(A.DB).execute("SELECT first, preferred_first FROM members WHERE email='samuel@example.com'").fetchone() == ("Samuel", "Sam")
    home = c.get("/home").get_data(as_text=True)
    assert "<h1>Hi, Sam</h1>" in home and "Samuel River" in home and 'value="Sam"' in home
    c.post("/api/messages", json={"body": "hey team"}, headers={"X-CSRF": csrf(c, "/chat")})
    assert c.get("/api/messages").get_json()[-1]["who"].startswith("Sam ")
    boss.post("/home", data=dict(csrf=csrf(boss, "/home"), action="preferred", preferred_first="Chief"))
    boss.post("/api/messages?c=coaches", json={"body": "coach note", "announcement": False}, headers={"X-CSRF": csrf(boss, "/chat")})
    assert boss.get("/api/messages?c=coaches").get_json()[-1]["who"].startswith("Chief ")
    boss.post("/api/messages", json={"body": "announcement from chief", "announcement": True}, headers={"X-CSRF": csrf(boss, "/chat")})
    assert "CHIEF" in c.get("/home").get_data(as_text=True)
    boss.post("/home", data=dict(csrf=csrf(boss, "/home"), action="preferred", preferred_first=""))
    pid = sqlite3.connect(A.DB).execute("SELECT id FROM practices WHERE date>? ORDER BY date LIMIT 1", (A.today_pt().isoformat(),)).fetchone()[0]
    c.post("/practices", data=dict(csrf=csrf(c, "/practices"), pid=pid, action="going"))
    assert "Sam R." in c.get("/practices").get_data(as_text=True)
    SENT.clear(); login = A.app.test_client(); login.post("/login", data=dict(csrf=csrf(login, "/login"), email="samuel@example.com"))
    assert SENT[-1][2].startswith("Hi Sam,")
    mid = ids()["samuel@example.com"]
    db = sqlite3.connect(A.DB); db.execute("UPDATE members SET usawp_valid_until=? WHERE id=?", ((A.today_pt() + dt.timedelta(days=3)).isoformat(), mid)); db.commit()
    with A.app.app_context():
        A.remind(A.db(), mid); A.db().commit()
    assert "Hi Sam," in c.get("/home").get_data(as_text=True)
    admin = boss.get("/admin").get_data(as_text=True)
    assert "Sam River" in admin and "writeText('Samuel River')" in admin and "Verify Samuel on Sport:80" in admin
    act(boss, ids()["mem@example.com"], "make_coach")
    assert mem.post("/admin", data=dict(csrf=csrf(mem, "/admin"), member_id=mid, action="preferred", preferred_first="Nope")).status_code == 403
    act(boss, ids()["mem@example.com"], "remove_coach")
    boss.post("/admin", data=dict(csrf=csrf(boss, "/admin"), member_id=mid, action="preferred", preferred_first="Sammy"))
    assert sqlite3.connect(A.DB).execute("SELECT preferred_first FROM members WHERE id=?", (mid,)).fetchone()[0] == "Sammy"
    assert "Sammy River" in boss.get("/members").get_data(as_text=True) and "legal Samuel" in boss.get("/members").get_data(as_text=True)
    assert "Sammy" in boss.get("/admin?q=Sammy").get_data(as_text=True)
    captured = []
    class R:
        status = 204
        def __enter__(self): return self
        def __exit__(self, *a): return False
    def spy(req, timeout=None, **k):
        captured.append(json.loads(req.data.decode())); return R()
    import urllib.request
    orig = urllib.request.urlopen; A.VERIFY_WEBHOOK_URL = "http://hooks.example/verify"; urllib.request.urlopen = spy
    try: boss.post("/admin", data=dict(csrf=csrf(boss, "/admin"), member_id=mid, action="ask_bot"))
    finally:
        urllib.request.urlopen = orig; A.VERIFY_WEBHOOK_URL = None
    assert captured[0]["name"] == "Samuel River" and captured[0]["preferred_first"] == "Sammy" and captured[0]["requested_by"] == "Boss One"
    assert sqlite3.connect(A.DB).execute("SELECT name FROM verify_requests WHERE member_id=?", (mid,)).fetchone()[0] == "Samuel River"
    import io
    csv_bytes = ("First Name,Last Name,Email Address,Preferred First Name,Membership Status\nSamuel,River,samuel@example.com,Samwell,Current\n").encode()
    boss.post("/import", data=dict(csrf=csrf(boss, "/import"), file=(io.BytesIO(csv_bytes), "x.csv")), content_type="multipart/form-data")
    assert sqlite3.connect(A.DB).execute("SELECT first, preferred_first FROM members WHERE email='samuel@example.com'").fetchone() == ("Samuel", "Samwell")
    c.post("/home", data=dict(csrf=csrf(c, "/home"), action="preferred", preferred_first="   "))
    assert sqlite3.connect(A.DB).execute("SELECT preferred_first FROM members WHERE id=?", (mid,)).fetchone()[0] is None
    assert "<h1>Hi, Samuel</h1>" in c.get("/home").get_data(as_text=True)
