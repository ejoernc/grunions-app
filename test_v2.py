"""Tests for roles page, login emails, reset_real, import tolerance, deploy config. Run: .venv/bin/python -m pytest -q test_v2.py"""
import os, re, sys, tempfile, sqlite3, subprocess, datetime as dt
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
           f"Mem,Three,MEM@example.com,659999,C-42,{(dt.date.today()+dt.timedelta(days=200)).isoformat()},2027-05-11\n").encode()
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
    assert db.execute("SELECT COUNT(*) FROM requirements").fetchone()[0] >= 4
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
    assert "gunicorn" in open(os.path.join(HERE, "Dockerfile"), encoding="utf-8").read()
    ry = open(os.path.join(HERE, "render.yaml"), encoding="utf-8").read(); assert "DATA_DIR" in ry and "disk" in ry and "SECRET_KEY" in ry
    assert "elliott.joern@gmail.com" in open(os.path.join(HERE, ".env.local"), encoding="utf-8").read()
def test_utf8_and_no_dash_strftime():
    for f in os.listdir(HERE):
        if f.endswith((".py", ".md", ".txt", ".yaml")) or f in ("Dockerfile",):
            s = open(os.path.join(HERE, f), "rb").read().decode("utf-8")
            if f.endswith(".py") and f != "test_v2.py": assert not re.search(r"%-[a-zA-Z]", s), f
