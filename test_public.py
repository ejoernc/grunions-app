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
    club = eli.get("/manage/area/club").get_data(as_text=True)
    assert "Sports &amp; pricing" in club
    assert 'href="/manage/pricing"' in club
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
    assert "Get 2 Free Practices" in body
    assert "2 free practices" in body
    assert "Try Water Polo Free" not in body.split("<h2>On the website</h2>", 1)[1]
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
    assert "Website widget" in html and "Visitors can switch" not in html
    assert ">All<" in html and ">Schedule<" in html and ">Competitions<" in html and ">Camps<" in html and ">Trips<" in html and ">Community<" in html
    assert 'src="/widget?preview=1"' in html and "https://grunions.regulars.team/widget" in html and "<iframe" in html
    preview = admin.get("/widget?preview=1")
    assert preview.status_code == 200 and "prefers-color-scheme" in preview.get_data(as_text=True) and "id=theme" not in preview.get_data(as_text=True)
    assert "id=theme" not in admin.get("/widget?preview=1&theme=day").get_data(as_text=True)
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
    assert "Space Grotesk" in frame and "datetile" in frame and "class=callout" in frame and "id=theme" not in frame and "prefers-color-scheme" in frame
    assert frame.count("<h2>Try Water Polo Free for 2 Weeks</h2>") == 1 and "Get 2 Free Practices" not in frame
    assert "A valid USA Water Polo trial membership is required" in frame
    assert "https://usawp.sport80.com/public/widget/1" in frame
    assert '"/register?event=p-' in frame and "Harbor Cup" in frame and 'id=sheetSignup' in frame and "Sign up" in frame
    assert "Loading the schedule" in frame and "Nothing coming up" in frame and "Couldn't load the schedule" in frame
    assert "Drop-in $15" in frame and "grid-template-columns:repeat(auto-fill,minmax(320px,1fr))" in frame
    assert "Mia" not in frame and "secret drill" not in frame
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
    admin_page = admin.get("/manage/widget").get_data(as_text=True)
    assert "Events in preview" in admin_page and "live widget shows every upcoming event" in admin_page
    assert "scrolling=no" in admin_page and "id=prevMobile" not in admin_page and "id=prevDesk" not in admin_page
    assert "embedrow" in admin_page and "https://grunions.regulars.team/widget" in admin_page
    assert "height:1px" in admin_page and "width:100%" in admin_page
    with A.app.app_context():
        d = A.db()
        for offset, place in enumerate(("Pool A", "Pool B", "Pool C", "Pool D"), start=7):
            when = (A.today_pt() + __import__("datetime").timedelta(days=offset)).isoformat()
            d.execute("""INSERT INTO practices(date,start,end,location,activity_type,sport,note)
                VALUES(?,?,?,?,?,?,?)""", (when, "19:00", "20:30", place, "practice", "Water Polo", "Extra session"))
        d.commit()
    admin.post("/manage/widget", data={
        "csrf": csrf(admin, "/manage/widget"),
        "widget_on": "1",
        "chip_all": "1", "chip_schedule": "1", "chip_competitions": "1", "chip_camps": "1", "chip_trips": "1", "chip_community": "1",
        "default_chip": "all", "include_schedule": "1", "show_pricing": "1", "show_trial": "1",
        "hide_past": "1", "limit": "2",
    })
    public_frame = member.get("/widget").get_data(as_text=True)
    preview_frame = admin.get("/widget?preview=1").get_data(as_text=True)
    public_feed = member.get("/api/public/feed").get_json()
    assert public_frame.count("<article") > 4 and public_frame.count("<article") == len(public_feed["events"])
    assert "Extra session" in public_frame and preview_frame.count("Extra session") == 0
    assert preview_frame.count("<article") == 2 and "id=sheet" in preview_frame and "Back" in preview_frame
    assert public_frame.count("<h2>Try Water Polo Free for 2 Weeks</h2>") == preview_frame.count("<h2>Try Water Polo Free for 2 Weeks</h2>") == 1
    assert "Fridays" in public_frame and "Fridays" in preview_frame
    admin.post("/manage/widget", data={
        "csrf": csrf(admin, "/manage/widget"),
        "widget_on": "1",
        "chip_all": "1", "chip_schedule": "1", "chip_competitions": "1",
        "default_chip": "all", "include_schedule": "1", "show_pricing": "1",
        "hide_past": "1", "limit": "2",
    })
    quiet_public = member.get("/widget").get_data(as_text=True)
    quiet_preview = admin.get("/widget?preview=1").get_data(as_text=True)
    assert "class=callout" not in quiet_public and "class=callout" not in quiet_preview
    assert "Fridays" in quiet_public and "Fridays" in quiet_preview
    assert quiet_preview.count("<article") == 2 and quiet_public.count("<article") > 2


def test_manage_home_groups_destinations_and_keeps_the_chart():
    admin, member = client(), client()
    join(admin, "Nia", "Admin", "nia.manage@example.com")
    join(member, "Sam", "Athlete", "sam.manage@example.com")
    with A.app.app_context():
        A.db().execute("UPDATE members SET is_admin=1 WHERE email='nia.manage@example.com'")
        A.db().commit()
    assert member.get("/manage").status_code == 403
    page = admin.get("/manage").get_data(as_text=True)
    assert "id=growthCard" in page and "Search settings, people, tools..." in page
    assert ">Practice</a>" not in page and ">Bulletin</a>" not in page and "class=qactions" not in page
    assert 'aria-label="Create event"' in page
    assert ">Activities</b>" in page and ">People</b>" in page and ">Club</b>" in page and ">Tools</b>" in page
    club = admin.get("/manage/area/club").get_data(as_text=True)
    assert "Sports &amp; pricing" in club and 'href="/manage/pricing"' in club and "Website widget" in club and ">Rules<" in club
    assert "Schedule &amp; pricing" not in club
    people = admin.get("/manage/area/people").get_data(as_text=True)
    assert "Members and roles" in people and ">Compliance<" in people
    tools = admin.get("/manage/area/tools").get_data(as_text=True)
    assert "QR codes" in tools and "Data transfer" in tools and ">Usage<" in tools
    roster = admin.get("/members").get_data(as_text=True)
    assert 'data-seg role=group aria-label="Role"' in roster and ">All</a>" in roster and ">Members</a>" in roster and ">Coaches</a>" in roster
    coaches = admin.get("/members?view=coaches").get_data(as_text=True)
    admins = admin.get("/members?view=admins").get_data(as_text=True)
    assert "<h1>Coaches</h1>" in coaches and 'href="/members?view=coaches"' in coaches
    assert "<h1>Admins</h1>" in admins and 'href="/members?view=admins"' in admins
    assert "<h1>Members</h1>" in roster


def test_registration_checks_eligibility_and_does_not_charge_or_email():
    sent = []
    real = A.send_email
    A.send_email = lambda *args, **kwargs: sent.append(args)
    try:
        admin, guest = client(), client()
        join(admin, "Nia", "Admin", "nia.reg@example.com")
        with A.app.app_context():
            d = A.db()
            d.execute("UPDATE members SET is_admin=1 WHERE email='nia.reg@example.com'")
            before = [tuple(row) for row in d.execute("SELECT id, usawp_status, usawp_valid_until, trial_acknowledged_at FROM members")]
            day = (A.today_pt() + __import__("datetime").timedelta(days=4)).isoformat()
            later = (A.today_pt() + __import__("datetime").timedelta(days=20)).isoformat()
            pid = d.execute("""INSERT INTO practices(date,start,end,location,activity_type,sport)
                VALUES(?,?,?,?,?,?)""", (day, "19:00", "20:30", "Westminster HS", "practice", "Water Polo")).lastrowid
            sid = d.execute("""INSERT INTO practices(date,start,end,location,activity_type,sport)
                VALUES(?,?,?,?,?,?)""", (day, "18:00", "19:00", "Side pool", "scrimmage", "Water Polo")).lastrowid
            d.commit()
        admin.post("/manage/pricing", data={
            "csrf": csrf(admin, "/manage/pricing"),
            "program_name": "Water Polo", "timezone": "America/Los_Angeles", "schedule_public": "1",
            "trial_on": "1", "trial_mode": "duration", "trial_duration": "14", "trial_first": "1",
            "trial_activity": "practice", "trial_external": "usawp_trial",
        })
        event = "p-%d" % pid
        with A.app.app_context():
            snapshot = A.db().execute("SELECT usawp_status, trial_acknowledged_at, usawp_valid_until FROM members WHERE email='nia.reg@example.com'").fetchone()
        opened = guest.get("/register?event=%s" % event)
        page = opened.get_data(as_text=True)
        assert opened.status_code == 200 and "<h2>Sign in</h2>" in page and "Create an account" in page
        with A.app.app_context():
            again = A.db().execute("SELECT usawp_status, trial_acknowledged_at, usawp_valid_until FROM members WHERE email='nia.reg@example.com'").fetchone()
            assert tuple(again) == tuple(snapshot)
        created = guest.post("/join", data=dict(csrf=csrf(guest, "/join"), first="Rio", last="Visitor", email="rio.reg@example.com", phone="555-0199"))
        assert created.status_code == 302 and created.headers["Location"].endswith("/register?event=%s" % event)
        claim = guest.get("/register?event=%s" % event).get_data(as_text=True)
        assert "<h2>USA Water Polo trial</h2>" in claim and "Submit for verification" in claim
        guest.post("/register?event=%s" % event, data={
            "csrf": csrf(guest, "/register?event=%s" % event),
            "action": "claim", "event": event, "usawp_number": "445566",
            "claim_start": A.today_pt().isoformat(), "claim_until": later,
        })
        pending = guest.get("/register?event=%s" % event).get_data(as_text=True)
        assert "<h2>Pending USAWP verification</h2>" in pending
        with A.app.app_context():
            row = A.db().execute("SELECT usawp_status, usawp_valid_until, usawp_number, trial_acknowledged_at, trial_claim_until FROM members WHERE email='rio.reg@example.com'").fetchone()
            assert (row["usawp_status"] or "unknown") in ("unknown", "") and not row["usawp_valid_until"]
            assert row["usawp_number"] == "445566" and row["trial_acknowledged_at"] == A.today_pt().isoformat()
            assert row["trial_claim_until"] == later
            assert A.db().execute("SELECT COUNT(*) FROM rsvps WHERE member_id=(SELECT id FROM members WHERE email='rio.reg@example.com')").fetchone()[0] == 0
        blocked = guest.post("/register?event=%s" % event, data={
            "csrf": csrf(guest, "/register?event=%s" % event), "action": "confirm", "event": event,
        })
        assert blocked.status_code == 302
        with A.app.app_context():
            assert A.db().execute("SELECT COUNT(*) FROM rsvps WHERE member_id=(SELECT id FROM members WHERE email='rio.reg@example.com')").fetchone()[0] == 0
            A.db().execute("""UPDATE members SET usawp_status='verified', membership_type='Trial', usawp_valid_until=?
                WHERE email='rio.reg@example.com'""", (later,))
            A.db().commit()
        eligible = guest.get("/register?event=%s" % event).get_data(as_text=True)
        assert "<h2>Eligible trial applied</h2>" in eligible and "Coverage" in eligible and A.today_pt().isoformat() in eligible and "Confirm registration" in eligible
        guest.post("/register?event=%s" % event, data={
            "csrf": csrf(guest, "/register?event=%s" % event), "action": "confirm", "event": event,
        })
        done = guest.get("/register?event=%s&done=1" % event).get_data(as_text=True)
        assert "<h2>You're registered</h2>" in done and "Nothing was charged" in done
        with A.app.app_context():
            rio = A.db().execute("SELECT id FROM members WHERE email='rio.reg@example.com'").fetchone()[0]
            assert A.db().execute("SELECT going FROM rsvps WHERE practice_id=? AND member_id=?", (pid, rio)).fetchone()["going"] == 1
            assert A.db().execute("SELECT COUNT(*) FROM trial_holds WHERE member_id=?", (rio,)).fetchone()[0] == 0
            others = [tuple(row) for row in A.db().execute("SELECT id, usawp_status, usawp_valid_until, trial_acknowledged_at FROM members WHERE id!=?", (rio,))]
            assert others == [row for row in before if row[0] != rio]
        scrimmage = guest.get("/register?event=p-%d" % sid).get_data(as_text=True)
        assert "not covered" in scrimmage and "Confirm registration" not in scrimmage
        admin.post("/manage/pricing", data={
            "csrf": csrf(admin, "/manage/pricing"),
            "program_name": "Water Polo", "timezone": "America/Los_Angeles",
            "trial_on": "1", "trial_mode": "sessions", "trial_sessions": "2", "trial_first": "1",
            "trial_activity": "practice", "trial_external": "usawp_trial",
        })
        second = (A.today_pt() + __import__("datetime").timedelta(days=5)).isoformat()
        with A.app.app_context():
            d = A.db()
            extra = d.execute("""INSERT INTO practices(date,start,end,location,activity_type,sport)
                VALUES(?,?,?,?,?,?)""", (second, "19:00", "20:30", "Marina HS", "practice", "Water Polo")).lastrowid
            d.commit()
        guest.post("/register?event=p-%d" % extra, data={
            "csrf": csrf(guest, "/register?event=p-%d" % extra), "action": "confirm", "event": "p-%d" % extra,
        })
        with A.app.app_context():
            hold = A.db().execute("SELECT state FROM trial_holds WHERE member_id=? AND practice_id=?", (rio, extra)).fetchone()
            assert hold["state"] == "held"
        guest.post("/practices", data={"csrf": csrf(guest, "/practices"), "action": "notgoing", "pid": extra})
        with A.app.app_context():
            assert A.db().execute("SELECT COUNT(*) FROM trial_holds WHERE member_id=? AND practice_id=?", (rio, extra)).fetchone()[0] == 0
        assert sent == []
        assert publicfeed.banner({"enabled": True, "mode": "sessions", "session_count": 2, "activities": ["practice"], "external": "none"})["title"] == "Get 2 Free Practices"
        duration = publicfeed.banner({"enabled": True, "mode": "duration", "duration_days": 14, "activities": ["practice"], "external": "usawp_trial"})
        assert duration["title"] == "Try Water Polo Free for 2 Weeks" and "free practices" not in duration["body"].lower()
    finally:
        A.send_email = real


def test_paid_membership_is_separate_and_does_not_touch_rsvps():
    import sportspay
    admin, member = client(), client()
    join(admin, "Pat", "Admin", "pat.pay@example.com")
    join(member, "Ada", "Athlete", "ada.pay@example.com")
    with A.app.app_context():
        d = A.db()
        d.execute("UPDATE members SET is_admin=1 WHERE email='pat.pay@example.com'")
        d.execute("UPDATE practices SET title='Morning swimming', note='USMS set' WHERE location='Side pool'")
        d.commit()
        sportspay.ensure_schema(d)
        assert sportspay.require_rsvp(d) is False
        names = [row["name"] for row in sportspay.sports(d)]
        assert names[:2] == ["Water Polo", "Swimming"]
        stripe = d.execute("SELECT active FROM payment_providers WHERE kind='stripe'").fetchone()
        assert stripe["active"] == 0
        monthly = d.execute("SELECT id FROM payment_plans WHERE name LIKE 'Grunions Water Polo%'").fetchone()
        assert [row["amount_cents"] for row in sportspay.prices(d, monthly["id"])] == [4500, 5000]
        assert sportspay.price_on(sportspay.prices(d, monthly["id"]), "2026-11-09") is None
        assert sportspay.price_on(sportspay.prices(d, monthly["id"]), "2026-12-15")["amount_cents"] == 4500
        assert sportspay.price_on(sportspay.prices(d, monthly["id"]), "2027-02-01")["amount_cents"] == 5000
        swim = d.execute("SELECT sport FROM practices WHERE location='Side pool'").fetchone()
        if swim:
            assert swim["sport"] == "Swimming"
        ada = d.execute("SELECT id FROM members WHERE email='ada.pay@example.com'").fetchone()["id"]
        d.execute("INSERT INTO rsvps(practice_id, member_id, going) VALUES(1, ?, 1)", (ada,))
        d.commit()
        before = d.execute("SELECT going FROM rsvps WHERE member_id=?", (ada,)).fetchone()["going"]
        usawp = d.execute("SELECT usawp_status FROM members WHERE id=?", (ada,)).fetchone()["usawp_status"]
    assert member.get("/manage/pricing/sports").status_code == 403
    page = admin.get("/manage/pricing/sports").get_data(as_text=True)
    assert "Water Polo" in page and "USA Water Polo" in page and "Coming later" not in page
    providers = admin.get("/manage/pricing/providers").get_data(as_text=True)
    assert "Coming later" in providers and "Require payment access to RSVP" in providers
    plans = admin.get("/manage/pricing/plans").get_data(as_text=True)
    assert "Grunions Water Polo + Swim Membership" in plans and "$45" in plans and "$50" in plans
    assert SWIM_OK(plans)
    person = admin.get("/admin/member/%d" % ada).get_data(as_text=True)
    assert "Paid membership" in person and "does not change an RSVP" in person
    admin.post("/admin/member/%d" % ada, data={
        "csrf": csrf(admin, "/admin/member/%d" % ada),
        "action": "paid", "paid_action": "active", "plan_id": str(monthly["id"]),
        "paid_status": "inactive", "valid_from": "2026-12-01", "paid_through": "2027-01-31", "paid_notes": "Check received",
    })
    with A.app.app_context():
        d = A.db()
        ent = d.execute("SELECT status, paid_through FROM access_entitlements WHERE member_id=?", (ada,)).fetchone()
        assert ent["status"] == "active" and ent["paid_through"] == "2027-01-31"
        assert d.execute("SELECT going FROM rsvps WHERE member_id=?", (ada,)).fetchone()["going"] == before
        assert (d.execute("SELECT usawp_status FROM members WHERE id=?", (ada,)).fetchone()["usawp_status"] or "") == (usawp or "")
        assert d.execute("SELECT COUNT(*) FROM access_audits WHERE member_id=?", (ada,)).fetchone()[0] == 1
        stripe_id = d.execute("SELECT id FROM payment_providers WHERE kind='stripe'").fetchone()["id"]
    turned = admin.post("/manage/pricing/providers", data={"csrf": csrf(admin, "/manage/pricing/providers"), "provider_id": str(stripe_id), "active": "1", "action": "save"}, follow_redirects=True)
    assert "Stripe is not available" in turned.get_data(as_text=True)
    with A.app.app_context():
        assert A.db().execute("SELECT active FROM payment_providers WHERE kind='stripe'").fetchone()["active"] == 0


def SWIM_OK(plans):
    return "Swimming drop-in" in plans and "cid=92340" in plans and "cid=103002" in plans


def test_payment_gate_stays_off_and_does_not_rewrite_rsvps():
    import sportspay
    sent = []
    real = A.send_email
    A.send_email = lambda *a, **k: sent.append(a)
    try:
        admin, athlete = client(), client()
        join(admin, "Gate", "Admin", "gate.admin@example.com")
        join(athlete, "Gale", "Athlete", "gale.pay@example.com")
        with A.app.app_context():
            d = A.db()
            d.execute("UPDATE members SET is_admin=1 WHERE email='gate.admin@example.com'")
            day = (A.today_pt() + __import__("datetime").timedelta(days=8)).isoformat()
            pid = d.execute("""INSERT INTO practices(date,start,end,location,activity_type,sport)
                VALUES(?,?,?,?,?,?)""", (day, "19:00", "20:30", "Gate Pool", "practice", "Water Polo")).lastrowid
            d.commit()
            gid = d.execute("SELECT id FROM members WHERE email='gale.pay@example.com'").fetchone()["id"]
        athlete.post("/practices", data={"csrf": csrf(athlete, "/practices"), "action": "going", "pid": pid})
        with A.app.app_context():
            assert A.db().execute("SELECT going FROM rsvps WHERE practice_id=? AND member_id=?", (pid, gid)).fetchone()["going"] == 1
            sportspay.set_require_rsvp(A.db(), True)
            A.db().commit()
        blocked = athlete.post("/practices", data={"csrf": csrf(athlete, "/practices"), "action": "going", "pid": pid})
        assert blocked.status_code == 302 and "/participate" in blocked.headers["Location"]
        page = athlete.get("/practices/%d/participate" % pid).get_data(as_text=True)
        assert "Verification required" in page
        with A.app.app_context():
            A.db().execute("""UPDATE members SET usawp_status='verified', usawp_valid_until='2027-06-01', membership_type='Individual'
                WHERE id=?""", (gid,))
            A.db().commit()
        choose = athlete.get("/practices/%d/participate" % pid).get_data(as_text=True)
        assert "Choose How to Participate" in choose and "Become a Member" in choose and "not configured" in choose
        with A.app.app_context():
            assert A.db().execute("SELECT going FROM rsvps WHERE practice_id=? AND member_id=?", (pid, gid)).fetchone()["going"] == 1
        plan = None
        with A.app.app_context():
            plan = A.db().execute("SELECT id FROM payment_plans WHERE kind='monthly'").fetchone()["id"]
        athlete.post("/practices/%d/participate" % pid, data={
            "csrf": csrf(athlete, "/practices/%d/participate" % pid), "action": "paid", "plan_id": str(plan),
        })
        with A.app.app_context():
            d = A.db()
            assert d.execute("SELECT status FROM payment_checks WHERE member_id=? AND practice_id=?", (gid, pid)).fetchone()["status"] == "pending"
            assert d.execute("SELECT going FROM rsvps WHERE practice_id=? AND member_id=?", (pid, gid)).fetchone()["going"] == 1
            check_id = d.execute("SELECT id FROM payment_checks WHERE member_id=?", (gid,)).fetchone()["id"]
        admin.post("/manage/pricing/membership", data={
            "csrf": csrf(admin, "/manage/pricing/membership"), "action": "verify_check", "check_id": str(check_id),
        })
        with A.app.app_context():
            d = A.db()
            assert d.execute("SELECT status FROM access_entitlements WHERE member_id=? ORDER BY id DESC LIMIT 1", (gid,)).fetchone()["status"] == "active"
            assert d.execute("SELECT going FROM rsvps WHERE practice_id=? AND member_id=?", (pid, gid)).fetchone()["going"] == 1
            sportspay.set_require_rsvp(d, False)
            d.commit()
        assert sent == []
    finally:
        A.send_email = real
        with A.app.app_context():
            sportspay.set_require_rsvp(A.db(), False)
            A.db().commit()


def test_home_hides_sport_chips_and_keeps_card_status():
    member = client()
    join(member, "Sky", "Athlete", "sky.sport@example.com")
    home = member.get("/home").get_data(as_text=True)
    assert "id=sportFilters" not in home and 'aria-label="Sport"' not in home
    assert "Eligible to register" in home or "Going" in home
    assert "Water Polo" in home
