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
        assert amy in got and bo in got and host not in got
        assert len([p for p in PUSHED if p[0] == amy]) == 1
        assert all(p[1] == "lineup" and p[4] == "/lineup/%d" % eid and p[5].endswith("/public-image/e/%d" % eid) for p in PUSHED)
        to = [s[0] for s in SENT]
        assert to.count("amy@example.com") == 1 and "bo@example.com" not in to and "hana@example.com" not in to
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
