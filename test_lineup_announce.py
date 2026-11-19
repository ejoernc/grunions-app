"""A new Lineup event goes out once to the club: in-app notice, push (with banner), and an email with the banner."""
import os
import tempfile

os.environ["GRUNIONS_DB"] = tempfile.mktemp(suffix=".db")
os.environ["ADMIN_EMAIL"] = "lineupadmin@example.com"
os.environ["GRUNIONS_SCHEDULER"] = "0"
os.environ["GRUNIONS_SHEET_SYNC"] = "0"

import app as A

SENT = []
A.send_email = lambda to, subject, text, html=None, ics=None: SENT.append((to, subject, html))
PUSHED = []
A.push_member = lambda d, m, kind, title, body, url, image="": PUSHED.append((m["id"], kind, title, body, url, image)) or 1


def _member(d, first, email, **cols):
    d.execute("INSERT INTO members(first, last, email, role, joined) VALUES(?,?,?,?,1)", (first, "Tester", email, cols.get("role", "athlete")))
    mid = d.execute("SELECT id FROM members WHERE email=?", (email,)).fetchone()[0]
    for k, v in cols.items():
        if k != "role": d.execute("UPDATE members SET %s=? WHERE id=?" % k, (v, mid))
    return mid


def test_new_lineup_event_announced_once_with_banner():
    with A.app.test_request_context("/"):
        d = A.db()
        host = _member(d, "Hana", "hana@example.com")
        amy = _member(d, "Amy", "amy@example.com")
        bo = _member(d, "Bo", "bo@example.com", lineup_email=0)
        os.makedirs(A.UPLOADS, exist_ok=True)
        open(os.path.join(A.UPLOADS, "banner-test.jpg"), "wb").write(b"\xff\xd8\xff")
        eid = d.execute("""INSERT INTO lineup_events(kind, title, date, end_date, status, created_by, venue, banner, date_precision)
            VALUES('event','Charity 5K','2027-03-14','2027-03-14','published',?,'Back Bay','banner-test.jpg','exact')""", (host,)).lastrowid
        d.commit()
        A.announce_lineup_event(d, eid, host, "https://x.test")
        A.announce_lineup_event(d, eid, host, "https://x.test")
        got = {p[0] for p in PUSHED}
        assert amy in got and bo in got and host in got
        assert len([p for p in PUSHED if p[0] == amy]) == 1
        assert all(p[1] == "lineup" and p[4] == "/lineup/%d" % eid and p[5].endswith("/public-image/e/%d" % eid) for p in PUSHED)
        to = [s[0] for s in SENT]
        assert to.count("amy@example.com") == 1 and "bo@example.com" not in to and to.count("hana@example.com") == 1
        html = [s[2] for s in SENT if s[0] == "amy@example.com"][0]
        assert "Charity 5K" in html and "/public-image/e/%d" % eid in html and "View the event" in html and "Mar 14" in html
        assert d.execute("SELECT COUNT(*) FROM notices WHERE member_id=? AND body LIKE 'New on the Lineup%'", (amy,)).fetchone()[0] == 1


def test_draft_or_pending_is_not_announced():
    with A.app.test_request_context("/"):
        d = A.db()
        host = d.execute("SELECT id FROM members WHERE email='hana@example.com'").fetchone()[0]
        eid = d.execute("INSERT INTO lineup_events(kind, title, date, status, created_by) VALUES('event','Draft','2027-04-01','pending',?)", (host,)).lastrowid
        d.commit()
        n = len(PUSHED)
        assert A.announce_lineup_event(d, eid, host, "https://x.test") == 0 and len(PUSHED) == n


def test_preview_is_a_draft_and_save_posts_and_emails_everyone():
    import re, io
    with A.app.test_request_context("/"):
        d = A.db()
        admin = _member(d, "Ada", "lineupadmin@example.com", is_admin=1, role="admin")
        d.commit()
    c = A.app.test_client()
    with c.session_transaction() as s: s["mid"] = admin
    tok = re.search(r'name=csrf value="([^"]+)"', c.get("/events/new?lane=lineup").get_data(as_text=True)).group(1)
    from PIL import Image
    buf = io.BytesIO(); Image.new("RGB", (900, 600), (200, 80, 40)).save(buf, "JPEG"); buf.seek(0)
    r = c.post("/events/new", data={"csrf": tok, "action": "preview", "lane": "lineup", "line_title": "Bay 5K", "description": "Fun run.",
        "date": "2027-03-14", "date_precision": "exact", "location": "Back Bay", "event_type": "Social", "hosting": "Hosting",
        "line_sport_on": "1", "line_sport": ["Road running"], "image": (buf, "b.jpg")}, content_type="multipart/form-data")
    assert r.status_code == 302 and "/lineup/" in r.headers["Location"], r.get_data(as_text=True)[:300]
    eid = int(r.headers["Location"].rsplit("/", 1)[1])
    with A.app.app_context():
        row = A.db().execute("SELECT status, banner FROM lineup_events WHERE id=?", (eid,)).fetchone()
    assert row["status"] == "draft" and row["banner"]
    before = len(SENT)
    page = c.get("/lineup/%d" % eid).get_data(as_text=True)
    assert "value=publish" in page and len(SENT) == before
    c.post("/lineup/%d" % eid, data={"csrf": tok, "action": "publish"})
    with A.app.app_context():
        assert A.db().execute("SELECT status FROM lineup_events WHERE id=?", (eid,)).fetchone()[0] == "published"
    to = [s[0] for s in SENT[before:]]
    assert "lineupadmin@example.com" in to and "amy@example.com" in to


def test_manual_email_me_and_everyone():
    import re
    with A.app.app_context():
        d = A.db()
        admin = d.execute("SELECT id FROM members WHERE email='lineupadmin@example.com'").fetchone()[0]
        eid = d.execute("SELECT id FROM lineup_events WHERE title='Bay 5K'").fetchone()[0]
    c = A.app.test_client()
    with c.session_transaction() as s: s["mid"] = admin
    tok = re.search(r'name=csrf value="([^"]+)"', c.get("/lineup/%d" % eid).get_data(as_text=True)).group(1)
    assert "value=email_all" in c.get("/lineup/%d" % eid).get_data(as_text=True)
    n, p = len(SENT), len(PUSHED)
    c.post("/lineup/%d" % eid, data={"csrf": tok, "action": "email_me"})
    assert [s[0] for s in SENT[n:]] == ["lineupadmin@example.com"] and len(PUSHED) == p
    n = len(SENT)
    c.post("/lineup/%d" % eid, data={"csrf": tok, "action": "email_all"})
    to = [s[0] for s in SENT[n:]]
    assert "amy@example.com" in to and "lineupadmin@example.com" in to and "bo@example.com" not in to and len(PUSHED) == p
