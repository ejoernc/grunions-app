"""Schedule, pricing, and free-trial settings. Saving them creates no practices."""
import os
import re
import tempfile

os.environ["GRUNIONS_DB"] = tempfile.mktemp(suffix=".db")
os.environ["ADMIN_EMAIL"] = "eli@example.com"
os.environ["GRUNIONS_SCHEDULER"] = "0"
os.environ["GRUNIONS_SHEET_SYNC"] = "0"
os.environ["DEV_SHOW_LINKS"] = "1"

import app as A
import publicfeed


def client():
    return A.app.test_client()


def csrf(browser, path):
    html = browser.get(path).get_data(as_text=True)
    return re.search(r'name=csrf value="([^"]+)"', html).group(1)


def join(browser, first, last, email):
    return browser.post("/join", data=dict(csrf=csrf(browser, "/join"), first=first, last=last, email=email, phone="555-0100"))


def counts():
    with A.app.app_context():
        d = A.db()
        return (d.execute("SELECT COUNT(*) FROM practices").fetchone()[0],
                d.execute("SELECT COUNT(*) FROM practice_series").fetchone()[0])


def test_settings_are_admin_only_and_create_no_practices():
    eli, jane, coach = client(), client(), client()
    join(eli, "Eli", "Joern", "eli@example.com")
    join(jane, "Jane", "Doe", "jane@example.com")
    join(coach, "Sam", "Coach", "sam.coach@example.com")
    with A.app.app_context():
        A.db().execute("UPDATE members SET role='coach', is_admin=0 WHERE email='sam.coach@example.com'")
        A.db().commit()
    assert jane.get("/manage/pricing").status_code == 403
    assert coach.get("/manage/pricing").status_code == 403
    assert "Schedule & pricing" not in jane.get("/manage").get_data(as_text=True)
    page = eli.get("/manage/pricing")
    html = page.get_data(as_text=True)
    assert page.status_code == 200
    assert "Schedule &amp; pricing" in eli.get("/manage").get_data(as_text=True)
    assert 'href="/manage/pricing"' in eli.get("/manage").get_data(as_text=True)
    assert "does not add sessions" in html
    form = html.split("<form", 1)[1].split("<h2>On the website</h2>", 1)[0]
    assert "Westminster" not in form and "Marina" not in form and "$" not in form
    assert "No prices to show." in html and "No free-trial offer." in html
    before, series = counts()
    saved = eli.post("/manage/pricing", data={
        "csrf": csrf(eli, "/manage/pricing"),
        "program_name": "Water Polo",
        "program_desc": "Evening practice",
        "timezone": "America/Los_Angeles",
        "venue": "Westminster High School",
        "address": "14325 Goldenwest St",
        "schedule_public": "1",
        "slot0_day": "4",
        "slot0_start": "19:00",
        "slot0_end": "20:30",
        "price_dropin": "15",
        "trial_on": "1",
        "trial_first": "1",
        "trial_visits": "2",
        "trial_message": "New to water polo? Your first two practices are on us.",
    }, follow_redirects=True)
    body = saved.get_data(as_text=True)
    assert saved.status_code == 200
    assert "Fridays: 7:00 PM–8:30 PM · Westminster High School" in body
    assert "Drop-in · 15" in body
    assert "Member" not in body.split("<h2>On the website</h2>", 1)[1]
    assert "Your first two practices are on us." in body
    assert "2 free practices" in body
    assert counts() == (before, series)
    with A.app.app_context():
        stored = publicfeed.load(A.db())
        eli_row = A.db().execute("SELECT trial_acknowledged_at FROM members WHERE email='eli@example.com'").fetchone()
    offer = publicfeed.public_view(stored)
    assert [row["label"] for row in offer["prices"]] == ["Drop-in"]
    assert offer["prices"][0]["price"] == "15"
    assert publicfeed.trial_claim_open(stored, eli_row)
    with A.app.app_context():
        A.db().execute("UPDATE members SET trial_acknowledged_at='2026-11-01' WHERE email='eli@example.com'")
        A.db().commit()
        claimed = A.db().execute("SELECT * FROM members WHERE email='eli@example.com'").fetchone()
        stored = publicfeed.load(A.db())
    assert not publicfeed.trial_claim_open(stored, claimed)
    hidden = eli.post("/manage/pricing", data={
        "csrf": csrf(eli, "/manage/pricing"),
        "program_name": "Water Polo",
        "timezone": "America/Los_Angeles",
        "slot0_day": "4",
        "slot0_start": "19:00",
        "slot0_end": "20:30",
        "venue": "Westminster High School",
    }, follow_redirects=True).get_data(as_text=True)
    website = hidden.split("<h2>On the website</h2>", 1)[1]
    assert "The regular schedule is hidden" in website
    assert "Fridays" not in website
    assert "No prices to show." in website
    assert "No free-trial offer." in website
    assert counts()[0] == before


def test_a_blank_weekly_row_is_skipped_and_a_half_row_is_refused():
    data = publicfeed.parse_form({
        "program_name": "Water Polo",
        "timezone": "America/Los_Angeles",
        "slot0_day": ["1", "4"],
        "slot0_start": "19:00",
        "slot0_end": "20:30",
        "slot0_venue": "Marina HS",
        "slot1_start": "",
    })
    assert len(data["schedule"]["slots"]) == 1
    assert data["schedule"]["slots"][0]["days"] == [1, 4]
    try:
        publicfeed.parse_form({"slot0_day": "4", "timezone": "America/Los_Angeles"})
    except ValueError as exc:
        assert "start time" in str(exc)
    else:
        raise AssertionError("a day without a start time should be refused")
