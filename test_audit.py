"""Pre-merge audit: privacy, permissions, notifications and deletes still hold in 2.0. Run: .venv/bin/python -m pytest -q test_audit.py"""
import os, re, sqlite3, tempfile, datetime as dt
D = tempfile.mkdtemp()
os.environ.update(DATA_DIR=D, ADMIN_EMAIL="boss@example.com", DEV_SHOW_LINKS="0")
os.environ.pop("GRUNIONS_DB", None); os.environ.pop("GRUNIONS_UPLOADS", None)
import app as A

TOKEN = re.compile(r'(?:name=csrf value=|const CSRF=)"([^"]+)"')
def csrf(c, p="/profile"):
    m = TOKEN.search(c.get(p).get_data(as_text=True)) or TOKEN.search(c.get("/profile").get_data(as_text=True))
    return m.group(1)
def join(first, last, email):
    c = A.app.test_client()
    c.post("/join", data=dict(birth_date="1990-03-04", csrf=csrf(c, "/join"), first=first, last=last, email=email, phone="1"))
    return c
def sql(q, args=()):
    con = sqlite3.connect(A.DB); cur = con.execute(q, args); con.commit(); rows = cur.fetchall(); con.close(); return rows

boss = join("Boss", "One", "boss@example.com")
jane = join("Jane", "Doe", "jane@example.com")
coach = join("Cora", "Coach", "cora@example.com")
anon = A.app.test_client()
JANE = sql("SELECT id FROM members WHERE email='jane@example.com'")[0][0]
CORA = sql("SELECT id FROM members WHERE email='cora@example.com'")[0][0]
BOSS = sql("SELECT id FROM members WHERE email='boss@example.com'")[0][0]
sql("UPDATE members SET role='coach' WHERE id=?", (CORA,))
sql("UPDATE members SET usawp_status='verified', usawp_number='1002010', usawp_valid_until='2099-01-01'")

def practice(title, days=2):
    day = (A.today_pt() + dt.timedelta(days=days)).isoformat()
    sql("INSERT INTO practices(date,start,end,location,sport,title) VALUES(?,?,?,?,?,?)", (day, "19:00", "20:30", "Audit Pool " + title, "Water Polo", title))
    return sql("SELECT id FROM practices WHERE title=?", (title,))[0][0]


def test_signed_out_sees_nothing_private():
    for path in ("/practices", "/members", "/members.csv", "/export", "/export/practices.csv", "/api/expiring", "/chat", "/manage", "/profile/%d" % JANE):
        r = anon.get(path)
        assert r.status_code in (302, 401, 403), (path, r.status_code)


def test_member_cannot_open_admin_data():
    for path in ("/admin/member/%d" % BOSS, "/members", "/members.csv", "/api/expiring", "/export", "/export/practices.csv", "/manage/search?q=boss"):
        r = jane.get(path)
        assert r.status_code in (302, 403, 404), (path, r.status_code)
        assert "boss@example.com" not in r.get_data(as_text=True), path


def test_member_profile_of_someone_else_hides_contact_details():
    page = jane.get("/profile/%d" % BOSS).get_data(as_text=True)
    assert "boss@example.com" not in page


def test_member_cannot_change_a_practice():
    pid = practice("Member Locked")
    t = csrf(jane, "/practices/%d" % pid)
    for data in (dict(action="social", social_kind="Drinks", social_place="Harp"), dict(action="message", message="hi"),
                 dict(action="cancel"), dict(action="delete"), dict(action="edit", date="2030-01-01", start="07:00", end="08:00", location="X"),
                 dict(action="coaches", coach=str(JANE), lead=str(JANE)), dict(action="plan", coaching_plan="x")):
        jane.post("/practices/%d" % pid, data=dict(csrf=t, pid=pid, **data))
    row = sql("SELECT cancelled, social_kind, date, coaching_plan, location FROM practices WHERE id=?", (pid,))[0]
    assert row[0] in (0, None) and not row[1] and row[2] != "2030-01-01" and not row[3] and row[4].startswith("Audit Pool"), row
    assert not sql("SELECT 1 FROM practice_coaches WHERE practice_id=?", (pid,))


def test_member_cannot_reach_coaches_or_board_chat():
    for ch in ("coaches", "board"):
        page = jane.get("/chat?c=%s" % ch)
        body = page.get_data(as_text=True)
        assert page.status_code in (302, 403, 404) or "composer" not in body, ch
    t = csrf(jane)
    jane.post("/chat", data=dict(csrf=t, c="coaches", body="sneaky"))
    assert not sql("SELECT 1 FROM messages WHERE body='sneaky'")


def test_cancel_emails_members_and_pushes_and_delete_cleans_up():
    emails, pushes = [], []
    old_e, old_p, old_r = A.send_email, A.send_push, A.smtp_ready
    A.smtp_ready = lambda: True
    A.send_email = lambda to, subj, text, html=None, ics=None: emails.append((to, subj, text))
    A.send_push = lambda sub, payload: pushes.append((sub.get("member_id"), payload))
    try:
        pid = practice("Cancel Me", days=3)
        sql("INSERT INTO rsvps(practice_id, member_id, going) VALUES(?,?,1)", (pid, JANE))
        t = csrf(boss, "/practices/%d" % pid)
        boss.post("/practices/%d" % pid, data=dict(csrf=t, pid=pid, action="cancel", reason="Pool closed"))
        assert sql("SELECT cancelled FROM practices WHERE id=?", (pid,))[0][0] == 1
        assert any(e[0] == "jane@example.com" for e in emails), emails
        boss.post("/practices/%d" % pid, data=dict(csrf=t, pid=pid, action="delete"))
        assert not sql("SELECT 1 FROM practices WHERE id=?", (pid,))
        assert not sql("SELECT 1 FROM rsvps WHERE practice_id=?", (pid,))
    finally:
        A.send_email, A.send_push, A.smtp_ready = old_e, old_p, old_r


def test_coach_can_check_in_but_member_cannot():
    pid = practice("Check Gate", days=0)
    day = sql("SELECT date FROM practices WHERE id=?", (pid,))[0][0]
    assert jane.get("/admin?date=%s&ev=p-%d" % (day, pid)).status_code in (302, 403)
    jane.post("/admin", data=dict(csrf=csrf(jane), member_id=JANE, date=day, ev="p-%d" % pid))
    assert not sql("SELECT 1 FROM checkins WHERE member_id=? AND practice_date=?", (JANE, day))
    assert coach.get("/admin?date=%s&ev=p-%d" % (day, pid)).status_code == 200


def test_csrf_is_required():
    pid = practice("Csrf Gate")
    r = jane.post("/practices", data=dict(pid=pid, action="going"))
    assert r.status_code in (400, 403)
    assert not sql("SELECT 1 FROM rsvps WHERE practice_id=? AND member_id=?", (pid, JANE))


def test_every_simple_page_renders_for_every_role():
    pid = practice("Crawl Practice")
    bad = []
    rules = [r for r in A.app.url_map.iter_rules() if "GET" in r.methods and not r.rule.startswith("/static")]
    for who, c in (("anon", anon), ("member", jane), ("coach", coach), ("admin", boss)):
        for r in rules:
            path = r.rule
            if "<" in path:
                if path.count("<") > 1: continue
                arg = list(r.arguments)[0]
                if arg in ("pid", "practice_id"): path = re.sub(r"<[^>]+>", str(pid), path)
                elif arg in ("mid", "member_id", "uid"): path = re.sub(r"<[^>]+>", str(JANE), path)
                else: continue
            if any(x in path for x in ("/logout", "/api/", "/auth/", "/login/google", "/oauth", ".ics", "/avatar", "/qr", "/sw.js", "/reset")): continue
            try:
                code = c.get(path).status_code
            except Exception as e:
                bad.append((who, path, repr(e)[:80])); continue
            if code >= 500: bad.append((who, path, code))
    assert not bad, bad


def test_chat_pushes_go_only_to_people_in_that_chat():
    pushes = []
    old = A.push_member
    A.push_member = lambda d, m, kind, title, body, url: pushes.append((m["id"], title, url))
    try:
        lo, hi = sorted([JANE, CORA])
        jane.post("/api/messages?c=dm:%d:%d" % (lo, hi), json={"body": "private hi"}, headers={"X-CSRF": csrf(jane)})
        assert pushes and {p[0] for p in pushes} == {CORA}, pushes
        assert all(p[2] == "/chat?c=dm:%d:%d" % (lo, hi) for p in pushes)
        pushes.clear()
        jane.post("/api/messages?c=team", json={"body": "all hands"}, headers={"X-CSRF": csrf(jane)})
        assert BOSS in {p[0] for p in pushes} and CORA in {p[0] for p in pushes} and JANE not in {p[0] for p in pushes}
        pushes.clear()
        # a group: only the people picked get it; outsiders can't read or post
        r = jane.post("/chat/dm", data={"csrf": csrf(jane), "with": [str(CORA), str(BOSS)], "name": "Trio"})
        ch = r.headers["Location"].split("c=", 1)[1].split("&", 1)[0]
        outsider = join("Otto", "Side", "otto@example.com")
        jane.post("/api/messages?c=" + ch, json={"body": "group start"}, headers={"X-CSRF": csrf(jane)})
        assert {p[0] for p in pushes} == {CORA, BOSS}, pushes
        assert outsider.get("/api/messages?c=" + ch).status_code == 403
        assert outsider.post("/api/messages?c=" + ch, json={"body": "x"}, headers={"X-CSRF": csrf(outsider)}).status_code == 403
        pushes.clear()
        jane.post("/api/messages?c=grp:nobody-here", json={"body": "x"}, headers={"X-CSRF": csrf(jane)})
        assert not pushes
    finally:
        A.push_member = old
