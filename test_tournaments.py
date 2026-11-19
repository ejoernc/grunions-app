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
                                    "line_sport_on": "1", "line_sport": ["Water Polo", "Swimming"]})
    assert r.status_code == 302 and "/setup/basics" in r.headers["Location"], r.headers.get("Location")
    tid = int(r.headers["Location"].split("/")[2])
    with A.app.app_context():
        t = tourn.get(A.db(), tid)
        assert t["lineup_event_id"] and t["name"] == "Grunion Open" and t["multi"] == 1
        assert [s["key"] for s in tourn.sports_of(A.db(), tid)] == ["water-polo", "swimming"]
    # The Lineup event links back to its setup.
    assert "/tournaments/%d" % tid in c.get("/lineup/%d" % t["lineup_event_id"]).get_data(as_text=True)
