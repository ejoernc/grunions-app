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
    assert "Drop-in $15" in body
    assert "Member" not in body.split("<h2>On the website</h2>", 1)[1]
    assert "Your first two practices are on us." in body
    assert "2 free practices" in body
    assert counts() == (before, series)
    with A.app.app_context():
        stored = publicfeed.load(A.db())
        eli_row = A.db().execute("SELECT trial_acknowledged_at FROM members WHERE email='eli@example.com'").fetchone()
    offer = publicfeed.public_view(stored)
    assert [row["label"] for row in offer["prices"]] == ["Drop-in"]
    assert offer["prices"][0]["price"] == "$15" and offer["prices"][0]["line"] == "Drop-in $15"
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


def test_widget_is_off_until_an_admin_publishes_it():
    admin, member = client(), client()
    join(admin, "Ada", "Widget", "ada.widget@example.com")
    join(member, "Mia", "Member", "mia.widget@example.com")
    with A.app.app_context():
        A.db().execute("UPDATE members SET is_admin=1, role='athlete' WHERE email='ada.widget@example.com'")
        A.db().commit()
        before = A.db().execute("SELECT COUNT(*) FROM practices").fetchone()[0]
    assert member.get("/manage/widget").status_code == 403
    assert admin.get("/api/public/feed").status_code == 404
    assert admin.get("/widget").status_code == 404
    assert member.get("/widget?preview=1").status_code == 404
    page = admin.get("/manage/widget")
    html = page.get_data(as_text=True)
    assert page.status_code == 200
    assert "Website widget" in html and "Night" in html and "Day" in html
    assert ">All<" in html and ">Schedule<" in html and ">Competitions<" in html and ">Camps<" in html and ">Trips<" in html and ">Community<" in html
    assert 'src="/widget?preview=1"' in html and "https://grunions.regulars.team/widget" in html and "<iframe" in html
    preview = admin.get("/widget?preview=1")
    assert preview.status_code == 200 and 'data-theme="night"' in preview.get_data(as_text=True)
    assert 'data-theme="day"' in admin.get("/widget?preview=1&theme=day").get_data(as_text=True)
    day = (A.today_pt() + __import__("datetime").timedelta(days=3)).isoformat()
    with A.app.app_context():
        d = A.db()
        mia = d.execute("SELECT id FROM members WHERE email='mia.widget@example.com'").fetchone()[0]
        pid = d.execute("""INSERT INTO practices(date,start,end,location,note,coaching_plan,activity_type,sport)
            VALUES(?,?,?,?,?,?,?,?)""", (day, "19:00", "20:30", "Westminster HS", "Bring a dark cap", "secret drill", "practice", "Water Polo")).lastrowid
        d.execute("INSERT INTO rsvps(practice_id, member_id, going) VALUES(?,?,1)", (pid, mia))
        d.execute("""INSERT INTO lineup_events(kind,title,date,status,event_type,venue,city,description,start_time,end_time)
            VALUES('Tournament','Harbor Cup',?,'published','Tournament','Harbor Pool','Long Beach','Open water polo tournament','09:00','17:00')""", (day,))
        d.execute("""INSERT INTO lineup_events(kind,title,date,status,event_type,description)
            VALUES('Social','Secret draft',?,'draft','Social','not public')""", (day,))
        d.commit()
    admin.post("/manage/pricing", data={
        "csrf": csrf(admin, "/manage/pricing"),
        "program_name": "Water Polo", "timezone": "America/Los_Angeles", "schedule_public": "1",
        "slot0_day": "4", "slot0_start": "19:00", "slot0_end": "20:30", "venue": "Westminster High School",
        "price_dropin": "15", "trial_on": "1", "trial_first": "1",
        "trial_message": "New to water polo? Your first two practices are on us.",
    })
    published = admin.post("/manage/widget", data={
        "csrf": csrf(admin, "/manage/widget"),
        "widget_on": "1", "theme": "night", "visitor_theme": "1",
        "chip_all": "1", "chip_schedule": "1", "chip_competitions": "1", "chip_camps": "1", "chip_trips": "1", "chip_community": "1",
        "default_chip": "all", "include_schedule": "1", "show_pricing": "1", "show_trial": "1",
        "hide_past": "1", "limit": "12",
    }, follow_redirects=True)
    assert published.status_code == 200
    feed = member.get("/api/public/feed")
    body = feed.get_data(as_text=True)
    assert feed.status_code == 200 and feed.mimetype.startswith("application/json")
    assert "Mia" not in body and "secret drill" not in body and "photo" not in body and "Secret draft" not in body and "not public" not in body
    assert "Bring a dark cap" in body and "Harbor Cup" in body and '"count":null' in body
    frame = member.get("/widget").get_data(as_text=True)
    assert "All" in frame and "Schedule" in frame and "Competitions" in frame and "Camps" in frame and "Trips" in frame and "Community" in frame
    assert "Space Grotesk" in frame and "datetile" in frame and "class=callout" in frame and frame.count("Your first two practices are on us.") == 1
    assert "Loading the schedule" in frame and "Nothing coming up" in frame and "Couldn't load the schedule" in frame
    assert "Drop-in $15" in frame and "Mia" not in frame and "secret drill" not in frame
    admin.post("/manage/widget", data={
        "csrf": csrf(admin, "/manage/widget"),
        "widget_on": "1", "theme": "day", "visitor_theme": "1",
        "chip_all": "1", "chip_schedule": "1", "chip_competitions": "1",
        "default_chip": "schedule", "include_schedule": "1", "show_counts": "1",
        "hide_past": "1", "limit": "12",
    })
    counted = member.get("/api/public/feed").get_json()
    practice = next(item for item in counted["events"] if item["id"].startswith("p-"))
    assert practice["count"] == 1 and "Mia" not in str(counted) and practice["chip"] == "schedule"
    assert counted["theme"] == "day" and counted["default_chip"] == "schedule"
    with A.app.app_context():
        assert A.db().execute("SELECT COUNT(*) FROM practices").fetchone()[0] == before + 1
