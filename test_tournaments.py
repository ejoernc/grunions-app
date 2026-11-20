"""Tournaments: setup (basics, sports with format presets, interest, registration, review), the public interest page,
access, and that fees are a demo (nothing charged)."""
import os
import re
import tempfile

os.environ["GRUNIONS_DB"] = tempfile.mktemp(suffix=".db")
os.environ["ADMIN_EMAIL"] = "touradmin@example.com"
os.environ["GRUNIONS_SCHEDULER"] = "0"
os.environ["GRUNIONS_SHEET_SYNC"] = "0"

import app as A
import tournaments as tourn


def _member(first, email, role="athlete", admin=0):
    with A.app.app_context():
        d = A.db()
        d.execute("INSERT INTO members(first, last, email, role, is_admin, joined) VALUES(?,?,?,?,?,1)", (first, "Tester", email, role, admin))
        mid = d.execute("SELECT id FROM members WHERE email=?", (email,)).fetchone()[0]
        d.commit()
        return mid


def _as(mid=None):
    c = A.app.test_client()
    if mid:
        with c.session_transaction() as s:
            s["mid"] = mid
    return c


def _csrf(c, path):
    html = c.get(path).get_data(as_text=True)
    return re.search(r'name=csrf value="([^"]+)"', html).group(1)


ADMIN = _member("Ada", "touradmin@example.com", "athlete", 1)
PLAYER = _member("Pat", "tourplayer@example.com")


def test_catalog_has_formats_from_the_research():
    wp, sw = tourn.sport("water-polo"), tourn.sport("swimming")
    assert wp["default"] == "A" and wp["allowed"] == ["A"]
    assert sw["default"] == "B" and "E" in sw["allowed"]
    assert len(tourn.CATALOG) > 150
    assert tourn.search("polo")[0]["name"] in ("Polocrosse", "Water polo") and any(s["key"] == "water-polo" for s in tourn.search("polo"))


def test_full_setup_interest_and_publish():
    c = _as(ADMIN)
    r = c.post("/tournaments/new", data={"csrf": _csrf(c, "/tournaments/new"), "name": "Harbor Invitational", "starts": "2027-03-06", "term": "Meet",
                                          "ends": "2027-03-07", "hosting": "organization", "host_org": "Grunions", "venue": "Belmont", "city": "Long Beach"})
    assert r.status_code == 302 and r.headers["Location"].endswith("/setup/sports")
    tid = int(r.headers["Location"].split("/")[2])
    tok = _csrf(c, "/tournaments/%d/setup/sports" % tid)
    # One sport by default: a second pick replaces the first.
    c.post("/tournaments/%d/setup/sports" % tid, data={"csrf": tok, "action": "add", "key": "diving"})
    c.post("/tournaments/%d/setup/sports" % tid, data={"csrf": tok, "action": "add", "key": "soccer"})
    with A.app.app_context():
        assert [s["key"] for s in tourn.sports_of(A.db(), tid)] == ["soccer"]
    c.post("/tournaments/%d/setup/sports" % tid, data={"csrf": tok, "action": "mode", "multi": "1"})
    c.post("/tournaments/%d/setup/sports" % tid, data={"csrf": tok, "action": "remove", "key": "soccer"})
    for k in ("water-polo", "swimming"):
        assert c.post("/tournaments/%d/setup/sports" % tid, data={"csrf": tok, "action": "add", "key": k}).status_code == 302
    c.post("/tournaments/%d/setup/sports" % tid, data={"csrf": tok, "action": "preset", "key": "swimming", "preset": "E"})
    c.post("/tournaments/%d/setup/sports" % tid, data={"csrf": tok, "action": "preset", "key": "water-polo", "preset": "D"})  # not allowed: stays A
    with A.app.app_context():
        sp = {s["key"]: s["preset"] for s in tourn.sports_of(A.db(), tid)}
    assert sp == {"water-polo": "A", "swimming": "E"}
    # A sport that isn't listed: the host names it and picks how it's won.
    c.post("/tournaments/%d/setup/sports" % tid, data={"csrf": tok, "action": "custom", "custom_name": "Tube polo", "preset": "A"})
    with A.app.app_context():
        names = [(s["name"], s["preset"]) for s in tourn.sports_of(A.db(), tid)]
    assert ("Tube polo", "A") in names
    c.post("/tournaments/%d/setup/sports" % tid, data={"csrf": tok, "action": "remove", "key": "custom-tube-polo"})
    page = c.get("/tournaments/%d/setup/sports" % tid).get_data(as_text=True)
    assert "multi-sport" in page and "Water polo" in page
    # Interest: closed until opened; anyone with the link can answer once it's open.
    with A.app.app_context():
        token = tourn.get(A.db(), tid)["token"]
    anon = _as()
    assert "Not taking interest yet" in anon.get("/t/" + token).get_data(as_text=True)
    c.post("/tournaments/%d/setup/interest" % tid, data={"csrf": _csrf(c, "/tournaments/%d/setup/interest" % tid), "action": "open"})
    r = anon.post("/t/" + token, data={"csrf": _csrf(anon, "/t/" + token), "kind": "team", "name": "Kara", "email": "kara@example.com",
                                        "team": "Squid", "players": "12", "sports": ["water-polo", "nope"]})
    assert r.status_code == 302 and "sent=1" in r.headers["Location"]
    bad = anon.post("/t/" + token, data={"csrf": _csrf(anon, "/t/" + token), "kind": "athlete", "name": "No Email"})
    assert "Add an email" in bad.get_data(as_text=True)
    with A.app.app_context():
        iv = tourn.interest_summary(A.db(), tid)
    assert iv["teams"] == 1 and iv["athletes"] == 12 and iv["per_sport"] == {"water-polo": 12}
    assert "Squid" in c.get("/tournaments/%d/setup/interest" % tid).get_data(as_text=True)
    # Can't publish without a base fee.
    tok = _csrf(c, "/tournaments/%d/setup/review" % tid)
    assert "Finish Registration first" in c.post("/tournaments/%d/setup/review" % tid, data={"csrf": tok, "action": "publish"}).get_data(as_text=True)
    neg = c.post("/tournaments/%d/setup/registration" % tid, data={"csrf": tok, "base": "-5"})
    assert "below zero" in neg.get_data(as_text=True)
    c.post("/tournaments/%d/setup/registration" % tid, data={"csrf": tok, "base": "220", "early": "180", "early_until": "2099-01-01", "channels": ["app", "link"]})
    review = c.get("/tournaments/%d/setup/review" % tid).get_data(as_text=True)
    assert "$180.00" in review and "Nothing is charged" in review
    r = c.post("/tournaments/%d/setup/review" % tid, data={"csrf": tok, "action": "publish"})
    assert r.status_code == 302 and r.headers["Location"] == "/tournaments/%d" % tid
    ws = c.get("/tournaments/%d" % tid).get_data(as_text=True)
    assert "Published" in ws and "Harbor Invitational" in ws and "meets" in ws  # the host's word, everywhere


def test_only_hosts_can_create_and_only_the_owner_or_admin_can_open_it():
    p = _as(PLAYER)
    assert p.get("/tournaments/new").status_code == 403
    with A.app.app_context():
        d = A.db(); tourn.ensure(d)
        tid = tourn.save_basics(d, None, {"name": "Private", "starts": "2027-01-01", "hosting": "individual"}, ADMIN); d.commit()
    assert p.get("/tournaments/%d" % tid).status_code in (403, 404)
    assert _as(ADMIN).get("/tournaments/%d" % tid).status_code == 200


def test_fee_today_picks_the_window():
    t = {"base_cents": 22000, "early_cents": 18000, "early_until": "2026-09-30", "late_cents": 26000, "late_from": "2026-10-20"}
    assert tourn.fee_today(t, "2026-09-01") == 18000
    assert tourn.fee_today(t, "2026-10-01") == 22000
    assert tourn.fee_today(t, "2026-10-25") == 26000


def test_hosted_competition_in_lineup_opens_the_setup():
    c = _as(ADMIN)
    tok = _csrf(c, "/events/new?lane=lineup")
    r = c.post("/events/new", data={"csrf": tok, "action": "preview", "lane": "lineup", "event_type": "Competition", "hosting": "Hosting", "line_title": "Grunion Open",
                                    "description": "Our open.", "date": "2027-05-01", "date_precision": "exact", "start": "09:00", "location": "Belmont Pool",
                                    "line_sport_on": "1", "line_sport": ["Water Polo", "Swimming", "Pickleball", "Tube relay"]})
    assert r.status_code == 302 and "/setup/basics" in r.headers["Location"], r.headers.get("Location")
    tid = int(r.headers["Location"].split("/")[2])
    with A.app.app_context():
        t = tourn.get(A.db(), tid)
        assert t["lineup_event_id"] and t["name"] == "Grunion Open" and t["multi"] == 1
        # Club sports, a listed sport the club doesn't run yet, and one the host typed.
        assert [s["key"] for s in tourn.sports_of(A.db(), tid)] == ["water-polo", "swimming", "pickleball", "custom-tube-relay"]
    # The Lineup event links back to its setup.
    assert "/tournaments/%d" % tid in c.get("/lineup/%d" % t["lineup_event_id"]).get_data(as_text=True)


def _new_comp_for_details():
    c = _as(ADMIN)
    r = c.post("/tournaments/new", data={"csrf": _csrf(c, "/tournaments/new"), "name": "Bay Games", "starts": "2027-05-06", "term": "Competition",
                                          "ends": "2027-05-07", "hosting": "organization", "host_org": "Grunions", "venue": "Belmont", "city": "Long Beach"})
    tid = int(r.headers["Location"].split("/")[2])
    tok = _csrf(c, "/tournaments/%d/setup/sports" % tid)
    c.post("/tournaments/%d/setup/sports" % tid, data={"csrf": tok, "action": "mode", "multi": "1"})
    for k in ("water-polo", "swimming"):
        c.post("/tournaments/%d/setup/sports" % tid, data={"csrf": tok, "action": "add", "key": k})
    return c, tid


def test_browse_by_format_and_each_sport_details():
    c, tid = _new_comp_for_details()
    page = c.get("/tournaments/%d/setup/sports?fmt=B" % tid).get_data(as_text=True)
    assert "Browse by format" in page and "Open water swimming" in page.replace("Open Water Swimming", "Open water swimming")
    page = c.get("/tournaments/%d/setup/details" % tid).get_data(as_text=True)
    tok = re.search(r'name=csrf value="([^"]+)"', page).group(1)
    with A.app.app_context():
        sid = A.db().execute("SELECT id FROM tournament_sports WHERE tournament_id=? ORDER BY id LIMIT 1", (tid,)).fetchone()[0]
    p = "s%d_" % sid
    r = c.post("/tournaments/%d/setup/details" % tid, data={"csrf": tok, p + "fee": "25", p + "cap": "64", p + "venue": "Belmont Plaza",
        p + "schedule": "Sat 8 AM - 4 PM", p + "checkin": "7:15 AM", p + "rules": "FINA rules.", p + "rules_link": "example.com/rules"})
    assert r.status_code == 302 and r.headers["Location"].endswith("/setup/review")
    with A.app.app_context():
        row = A.db().execute("SELECT fee_cents, cap, venue, rules_link FROM tournament_sports WHERE id=?", (sid,)).fetchone()
    assert tuple(row) == (2500, 64, "Belmont Plaza", "https://example.com/rules")
    assert "1 of" in c.get("/tournaments/%d/setup/review" % tid).get_data(as_text=True)


def test_competition_started_from_lineup_makes_a_linked_draft_and_publishes_it():
    c = _as(ADMIN)
    page = c.get("/tournaments/new?from=lineup&name=Harbor%20Open&color=cherry").get_data(as_text=True)
    assert 'value="Harbor Open"' in page and 'value="cherry" checked' in page and "name=from value=lineup" in page
    r = c.post("/tournaments/new", data={"csrf": _csrf(c, "/tournaments/new?from=lineup"), "from": "lineup", "name": "Harbor Open", "term": "Meet",
        "starts": "2027-06-05", "ends": "2027-06-06", "hosting": "organization", "host_org": "Grunions", "venue": "Belmont", "city": "Long Beach",
        "color": "cherry", "color_seen": "1"})
    tid = int(r.headers["Location"].split("/")[2])
    with A.app.app_context():
        d = A.db()
        eid = d.execute("SELECT lineup_event_id FROM tournaments WHERE id=?", (tid,)).fetchone()[0]
        ev = d.execute("SELECT title, status, color, event_type, type_custom, end_date FROM lineup_events WHERE id=?", (eid,)).fetchone()
    assert tuple(ev) == ("Harbor Open", "draft", "cherry", "Competition", "Meet", "2027-06-06")
    tok = _csrf(c, "/tournaments/%d/setup/basics" % tid)
    c.post("/tournaments/%d/setup/basics" % tid, data={"csrf": tok, "name": "Harbor Open 2027", "term": "Meet", "starts": "2027-06-05", "ends": "2027-06-07",
        "hosting": "organization", "host_org": "Grunions", "color": "sky", "color_seen": "1"})
    c.post("/tournaments/%d/setup/sports" % tid, data={"csrf": tok, "action": "add", "key": "swimming"})
    c.post("/tournaments/%d/setup/registration" % tid, data={"csrf": tok, "base": "40", "channels": "app"})
    c.post("/tournaments/%d/setup/review" % tid, data={"csrf": tok, "action": "publish"})
    with A.app.app_context():
        ev = A.db().execute("SELECT title, status, color, end_date FROM lineup_events WHERE id=?", (eid,)).fetchone()
    assert tuple(ev) == ("Harbor Open 2027", "published", "sky", "2027-06-07")


def test_new_event_step_one_hands_over_to_competition_setup():
    import io
    from PIL import Image
    c = _as(ADMIN)
    tok = _csrf(c, "/events/new?lane=lineup")
    buf = io.BytesIO(); Image.new("RGB", (900, 600), (20, 120, 200)).save(buf, "JPEG"); buf.seek(0)
    r = c.post("/tournaments/new?from=lineup", data={"csrf": tok, "start": "1", "lane": "lineup", "line_title": "Bay Meet",
        "description": "Two days of racing.", "event_type": "competitions|Meet", "hosting": "Hosting", "cohosted": "1",
        "cohost_org": ["Long Beach Swim"], "event_color_line": "aqua", "line_sport_on": "1", "line_sport": ["Swimming", "Water Polo"],
        "image": (buf, "b.jpg")}, content_type="multipart/form-data")
    assert r.headers["Location"].endswith("/tournaments/new?from=lineup")
    page = c.get("/tournaments/new?from=lineup").get_data(as_text=True)
    assert 'value="Bay Meet"' in page and 'value="Long Beach Swim"' in page and 'value="aqua" checked' in page and 'value="Meet" checked' in page
    r = c.post("/tournaments/new", data={"csrf": tok, "from": "lineup", "name": "Bay Meet", "term": "Meet", "starts": "2027-07-10", "ends": "2027-07-11",
        "hosting": "several", "host_org": "Grunions", "cohosts": "Long Beach Swim", "color": "aqua", "color_seen": "1"})
    tid = int(r.headers["Location"].split("/")[2])
    with A.app.app_context():
        d = A.db()
        t = d.execute("SELECT multi, lineup_event_id FROM tournaments WHERE id=?", (tid,)).fetchone()
        keys = [x["sport_key"] for x in d.execute("SELECT sport_key FROM tournament_sports WHERE tournament_id=? ORDER BY sort", (tid,))]
        ev = d.execute("SELECT banner, type_custom, color, status FROM lineup_events WHERE id=?", (t["lineup_event_id"],)).fetchone()
    assert t["multi"] == 1 and keys == ["swimming", "water-polo"]
    assert ev["banner"] and ev["type_custom"] == "Meet" and ev["color"] == "aqua" and ev["status"] == "draft"
