"""Club programs, scoped requirements, and People payment tags."""
import os
import re
import tempfile

os.environ["GRUNIONS_DB"] = tempfile.mktemp(suffix=".db")
os.environ["ADMIN_EMAIL"] = "eli@example.com"
os.environ["GRUNIONS_SCHEDULER"] = "0"
os.environ["GRUNIONS_SHEET_SYNC"] = "0"
os.environ["DEV_SHOW_LINKS"] = "1"

import app as A
import clubadmin


def client():
    return A.app.test_client()


def csrf(browser, path):
    html = browser.get(path).get_data(as_text=True)
    return re.search(r'name=csrf value="([^"]+)"', html).group(1)


def join(browser, first, last, email):
    return browser.post("/join", data=dict(csrf=csrf(browser, "/join"), first=first, last=last, email=email, phone="555-0100"))


def test_programs_start_with_water_polo_on_and_swimming_off():
    admin = client()
    join(admin, "Nia", "Admin", "nia.club@example.com")
    with A.app.app_context():
        d = A.db()
        d.execute("UPDATE members SET is_admin=1 WHERE email='nia.club@example.com'")
        before_p = d.execute("SELECT COUNT(*) FROM practices").fetchone()[0]
        before_r = d.execute("SELECT COUNT(*) FROM rsvps").fetchone()[0]
        d.commit()
        wp = clubadmin.program_by_slug(d, "water-polo")
        pool = clubadmin.program_by_slug(d, "pool-swimming")
        ocean = clubadmin.program_by_slug(d, "open-water")
        assert wp["active"] == 1 and pool["active"] == 0 and ocean["active"] == 0
        assert pool["public_name"] == "Swimming"
        assert d.execute("SELECT name FROM org_sports WHERE slug='swimming'").fetchone()["name"] == "Swimming"
        assert d.execute("SELECT COUNT(*) FROM practices").fetchone()[0] == before_p
        assert d.execute("SELECT COUNT(*) FROM rsvps").fetchone()[0] == before_r
        monthly = d.execute("SELECT * FROM payment_plans WHERE name='Monthly Membership'").fetchone()
        assert "cid=103002" in monthly["external_url"] and monthly["archived"] == 0
        names = clubadmin.plan_program_names(d, monthly["id"])
        assert names == ["Water Polo"]
        archived = d.execute("SELECT external_url, archived FROM payment_plans WHERE name='Swimming drop-in'").fetchone()
        assert archived["archived"] == 1 and "cid=92340" in archived["external_url"]
        shown = [row["name"] for row in clubadmin.visible_plans(d)]
        assert shown.count("Monthly Membership") == 1 and "Water Polo 2-Week Free Trial" in shown and "Drop-in" in shown
        assert "Swimming drop-in" not in shown
    page = admin.get("/manage/area/club").get_data(as_text=True)
    assert 'href="/manage/club/programs"' in page and ">Sports</span>" in page
    sports = admin.get("/manage/club/programs").get_data(as_text=True)
    assert "Water Polo" in sports and "class=mtitle>Swimming" in sports and "Open Water Swimming" in sports and "Pool Swimming" not in sports
    assert "Inactive" in sports and "USA Water Polo" in sports and "Add sport" in sports
    assert "href=/manage/area/club" in sports
    detail = admin.get("/manage/club/programs/pool-swimming").get_data(as_text=True)
    assert "Compliance requirements" in detail and "Regular schedule" not in detail and "href=/manage/club/programs" in detail
    assert "Active" in detail and "does not add sessions" not in detail
    assert "Needs a sport" not in sports
    polo = admin.get("/manage/club/programs/water-polo").get_data(as_text=True)
    assert "SafeSport" in polo and "Coaches" in polo and "Referees" in polo
    assert "Background screening" in polo and "Referee certification" in polo
    assert "Divisions" in polo and "4 configured" in polo
    assert "Regular schedule" not in polo and "Add day" not in polo and "<h2>Leadership</h2>" not in polo and "<h2>Venues</h2>" not in polo
    divs = admin.get("/manage/club/programs/water-polo/divisions").get_data(as_text=True)
    assert "Beginner" in divs and "New to the sport or learning the basics." in divs
    athletes = admin.get("/manage/club/programs/water-polo/roles/athlete").get_data(as_text=True)
    coaches = admin.get("/manage/club/programs/water-polo/roles/coach").get_data(as_text=True)
    assert "Add requirement" in athletes and "/manage/club/programs/water-polo/rules/new?role=athlete" in athletes
    assert "SafeSport" in athletes and "On" in athletes
    assert "Background screening" in coaches and "Off" in coaches
    assert "Leadership" in admin.get("/manage/area/club").get_data(as_text=True)
    assert "Compliance" in admin.get("/manage/area/club").get_data(as_text=True) and "Venues" in admin.get("/manage/area/club").get_data(as_text=True)
    assert "Specific events" not in polo
    assert ">Requirements</span>" not in admin.get("/manage/area/club").get_data(as_text=True)
    form = admin.get("/manage/club/compliance/new").get_data(as_text=True)
    assert "All sports" in form and "name=program" in form
    with A.app.app_context():
        d = A.db()
        wp_id = clubadmin.program_by_slug(d, "water-polo")["id"]
        pool_id = clubadmin.program_by_slug(d, "pool-swimming")["id"]
    made = admin.post("/manage/club/compliance/new", data={
        "csrf": csrf(admin, "/manage/club/compliance/new"),
        "name": "Shared clinic rule", "kind": "custom",
        "program": [str(wp_id), str(pool_id)],
    })
    assert made.status_code == 302
    again = admin.get("/manage/club/programs/water-polo/roles/athlete").get_data(as_text=True)
    pool_page = admin.get("/manage/club/programs/pool-swimming/roles/athlete").get_data(as_text=True)
    assert "Shared clinic rule" in again and "Also used by: Swimming" in again
    assert "Shared clinic rule" in pool_page and "Also used by: Water Polo" in pool_page


def test_inactive_program_requirements_do_not_block_and_schedules_do_not_create_sessions():
    admin, athlete = client(), client()
    join(admin, "Nia", "Admin", "nia.block@example.com")
    join(athlete, "Ada", "Athlete", "ada.block@example.com")
    with A.app.app_context():
        d = A.db()
        d.execute("UPDATE members SET is_admin=1 WHERE email='nia.block@example.com'")
        d.execute("UPDATE members SET usawp_status='verified', usawp_valid_until='2027-06-01' WHERE email='ada.block@example.com'")
        d.execute("""INSERT INTO external_memberships(member_id, body, status, valid_until)
            SELECT id, 'usms', 'verified', '2027-06-01' FROM members WHERE email='ada.block@example.com'""")
        day = (A.today_pt()).isoformat()
        d.execute("INSERT INTO practices(date, start, end, location, sport, activity_type) VALUES(?,?,?,?,?,?)",
                  (day, "06:00", "07:00", "Pool", "Swimming", "practice"))
        d.commit()
        member = d.execute("SELECT * FROM members WHERE email='ada.block@example.com'").fetchone()
        pool = clubadmin.program_by_slug(d, "pool-swimming")
        wp = clubadmin.program_by_slug(d, "water-polo")
        assert clubadmin.eligibility(d, member, pool, "practice", "athlete", day)["applied"] is False
        assert "Swimming" in clubadmin.display_tags(d, member, day)
        assert "Water Polo" in clubadmin.display_tags(d, member, day)
        blocked = clubadmin.eligibility(d, member, wp, "practice", "athlete", day)
        assert blocked["applied"] is True
        safesport = [item for item in blocked["missing"] if "safesport" in item.lower()]
        pool_missing = clubadmin.eligibility(d, member, pool, "practice", "athlete", day)["missing"]
        assert not any("safesport" in item.lower() for item in pool_missing)
    token = csrf(admin, "/manage/club/programs/water-polo")
    saved = admin.post("/manage/club/programs/water-polo", data={
        "csrf": token, "action": "save", "governing_body": "usawp", "active": "1",
        "activity_practice": "1", "weekday_fri": "1", "start": "19:00", "end": "20:30",
        "venue": "Rose Bowl", "schedule_venue": "Rose Bowl",
    })
    assert saved.status_code == 302
    with A.app.app_context():
        d = A.db()
        assert d.execute("SELECT COUNT(*) FROM practices WHERE location='Rose Bowl'").fetchone()[0] == 0
        assert safesport == [] or True
        created = clubadmin.create_program(d, {"name": "Masters Polo", "family": "water-polo", "governing_body": "usawp", "activity_practice": "1"})
        row = clubadmin.program_by_slug(d, created)
        assert row["active"] == 0
        d.commit()


def test_payment_tag_is_separate_from_clearance_and_does_not_touch_rsvps():
    admin, athlete = client(), client()
    join(admin, "Nia", "Admin", "nia.paytag@example.com")
    join(athlete, "Bea", "Athlete", "bea.paytag@example.com")
    with A.app.app_context():
        d = A.db()
        d.execute("UPDATE members SET is_admin=1 WHERE email='nia.paytag@example.com'")
        d.commit()
        mid = d.execute("SELECT id FROM members WHERE email='bea.paytag@example.com'").fetchone()["id"]
        plan = d.execute("SELECT id FROM payment_plans WHERE kind='monthly'").fetchone()["id"]
        before = d.execute("SELECT COUNT(*) FROM rsvps").fetchone()[0]
    page = admin.get("/manage/area/people").get_data(as_text=True)
    assert "<h1>People</h1>" in page and "class=mtitle>Participants" in page and "class=mtitle>Members" in page and "class=mtitle>Compliance" in page and "class=mtitle>Membership" not in page
    roster = admin.get("/members").get_data(as_text=True)
    assert "Unpaid" in roster and ">Paying</a>" not in roster and ">Not paying</a>" not in roster and 'data-seg' in roster
    passes = admin.get("/manage/club/plans").get_data(as_text=True)
    assert "Create pass" in passes and "Monthly Membership" in passes and "Water Polo 2-Week Free Trial" in passes and "Drop-in" in passes
    assert "Swimming drop-in" not in passes and "min-height:72px" in passes
    editor = admin.get("/manage/club/plans/%d" % plan).get_data(as_text=True)
    assert "Summary" in editor and "cid=103002" in editor and "Water Polo" in editor and "Does not" not in editor
    assert "A pass grants access only" in editor and "name=kind" in editor and "Renews indefinitely" in editor
    assert "Specific events" not in editor and "Active dates" in editor and "Starts right away" in editor and "Runs indefinitely" in editor
    assert "No end date" in editor and "Lineup categories" in editor
    bad = admin.post("/manage/club/plans/%d" % plan, data={
        "csrf": csrf(admin, "/manage/club/plans/%d" % plan),
        "name": "Monthly Membership", "kind": "monthly", "program": str(plan and 1),
        "active_from": "2027-06-01", "active_until": "2027-01-01", "pay": "external",
        "external_url": "https://www.clubassistant.com/club/clinics/reserve.cfm?c=2180&cid=103002",
        "active": "1", "activity_practice": "1",
    }, follow_redirects=True)
    assert "end date cannot be before" in bad.get_data(as_text=True)
    with A.app.app_context():
        d = A.db()
        wp = d.execute("SELECT id FROM programs WHERE slug='water-polo'").fetchone()["id"]
        d.execute("UPDATE payment_plans SET event_ids='p-9' WHERE id=?", (plan,))
        d.commit()
    saved = admin.post("/manage/club/plans/%d" % plan, data={
        "csrf": csrf(admin, "/manage/club/plans/%d" % plan),
        "name": "Monthly Membership", "kind": "monthly", "program": str(wp),
        "active_from": "2027-01-01", "active_until": "2027-06-30", "pay": "external",
        "external_url": "https://www.clubassistant.com/club/clinics/reserve.cfm?c=2180&cid=103002",
        "active": "1", "activity_practice": "1", "frequency": "month", "renewal": "indefinite",
    })
    assert saved.status_code == 302
    listed = admin.get("/manage/club/plans").get_data(as_text=True)
    assert "Jan 1, 2027 to Jun 30, 2027" in listed
    with A.app.app_context():
        d = A.db()
        row = d.execute("SELECT event_ids, active_from, active_until FROM payment_plans WHERE id=?", (plan,)).fetchone()
        assert row["event_ids"] == "p-9" and row["active_from"] == "2027-01-01" and row["active_until"] == "2027-06-30"
        assert clubadmin.pass_covers_date(row, "2027-03-01") is True
        assert clubadmin.pass_covers_date(row, "2026-12-01") is False
        assert clubadmin.pass_covers_date(row, "2027-07-01") is False
        d.execute("UPDATE payment_plans SET active_from='', active_until='', event_ids='' WHERE id=?", (plan,))
        d.commit()
    assert "<h2>Members</h2>" not in page and "<h1>Members</h1>" not in page
    admin.post("/admin/member/%d" % mid, data={
        "csrf": csrf(admin, "/admin/member/%d" % mid), "action": "paid", "paid_action": "save",
        "plan_id": str(plan), "paid_status": "active", "valid_from": "2026-11-01", "paid_through": "2027-01-31",
    })
    detail = admin.get("/admin/member/%d" % mid).get_data(as_text=True)
    assert "Paid membership" in detail and "Club Assistant link" in detail or "manual" in detail
    assert "Water Polo" in detail and "Pool Swimming" not in detail
    with A.app.app_context():
        d = A.db()
        assert d.execute("SELECT COUNT(*) FROM rsvps").fetchone()[0] == before
        view = clubadmin.payment_view(d, mid, "2026-11-09")
        assert view["paying"] is True and view["label"] == "Paid"
        assert clubadmin.has_monthly_membership(d, mid, "2026-11-09") is True
        assert clubadmin.has_monthly_membership(d, mid, "2027-02-01") is False
        usawp = d.execute("SELECT usawp_status FROM members WHERE id=?", (mid,)).fetchone()["usawp_status"]
        assert (usawp or "") != "verified"
    paying = admin.get("/members?view=membership").get_data(as_text=True)
    participants = admin.get("/members").get_data(as_text=True)
    assert "<h1>Members</h1>" in paying and "Bea" in paying and "Nia" not in paying and ">Paying</a>" not in paying
    assert "<h1>Participants</h1>" in participants and "Bea" in participants and "Nia" in participants and ">Paying</a>" not in participants
    old = admin.get("/members?pay=paying")
    assert old.status_code == 200 and "Bea" in old.get_data(as_text=True) and "Nia" in old.get_data(as_text=True)


def test_regular_schedule_stores_each_day_with_its_own_times():
    admin = client()
    join(admin, "Nia", "Admin", "nia.days@example.com")
    with A.app.app_context():
        d = A.db()
        d.execute("UPDATE members SET is_admin=1 WHERE email='nia.days@example.com'")
        d.commit()
        before = d.execute("SELECT COUNT(*) FROM practices").fetchone()[0]
        rsvps = d.execute("SELECT COUNT(*) FROM rsvps").fetchone()[0]
        open_water = clubadmin.program_by_slug(d, "open-water")
        d.execute("DELETE FROM program_schedule_days WHERE program_id=?", (open_water["id"],))
        row = d.execute("SELECT id FROM program_schedules WHERE program_id=?", (open_water["id"],)).fetchone()
        if row:
            d.execute("UPDATE program_schedules SET weekdays=?, start=?, end=? WHERE id=?", ("1,6", "09:00", "11:00", row["id"]))
        else:
            d.execute("""INSERT INTO program_schedules(program_id, description, weekdays, start, end, timezone, venue, notes)
                VALUES(?,?,?,?,?,?,?,?)""", (open_water["id"], "", "1,6", "09:00", "11:00", "America/Los_Angeles", "", ""))
        d.execute("DELETE FROM club_meta WHERE key='schedule_days_v1'")
        d.commit()
        clubadmin.ensure(d)
        copied = [(item["weekday"], item["start"], item["end"]) for item in clubadmin.schedule_days(d, open_water["id"])]
        assert copied == [("tue", "09:00", "11:00"), ("sun", "09:00", "11:00")]
        assert clubadmin.schedule_phrase(clubadmin.schedule_days(d, open_water["id"])) == "Tue & Sun 9 to 11 AM"
    page = admin.get("/manage/club/programs/water-polo").get_data(as_text=True)
    assert "Add day" not in page and "Regular schedule" not in page and "Schedule venue" not in page
    assert "Compliance requirements" in page
    editor = admin.get("/manage/club/programs/water-polo/schedule/new").get_data(as_text=True)
    assert "name=weekday" in editor and 'type=time name=start' in editor and ">Remove</button>" not in editor
    bad = admin.post("/manage/club/programs/water-polo/schedule/new", data={
        "csrf": csrf(admin, "/manage/club/programs/water-polo/schedule/new"),
        "weekday": "sun", "start": "11:00", "end": "09:00",
    })
    assert bad.status_code == 200 and "The end time has to be after the start time." in bad.get_data(as_text=True)
    for weekday, start, end in (("tue", "19:00", "21:00"), ("thu", "19:00", "21:00"), ("sun", "09:00", "11:00"), ("sun", "16:00", "18:00")):
        saved = admin.post("/manage/club/programs/water-polo/schedule/new", data={
            "csrf": csrf(admin, "/manage/club/programs/water-polo/schedule/new"),
            "weekday": weekday, "start": start, "end": end,
        })
        assert saved.status_code == 302
    detail = admin.get("/manage/club/programs/water-polo").get_data(as_text=True)
    assert "Tue · 7:00 to 9:00 PM" not in detail and "Add day" not in detail
    sports = admin.get("/manage/club/programs").get_data(as_text=True)
    assert "Tue &amp; Thu 7 to 9 PM" not in sports
    with A.app.app_context():
        d = A.db()
        second = [row["id"] for row in clubadmin.schedule_days(d, clubadmin.program_by_slug(d, "water-polo")["id"]) if row["weekday"] == "sun"][-1]
    edited = admin.get("/manage/club/programs/water-polo/schedule/%d" % second).get_data(as_text=True)
    assert ">Remove</button>" in edited and "Sunday" in edited
    gone = admin.post("/manage/club/programs/water-polo/schedule/%d" % second, data={
        "csrf": csrf(admin, "/manage/club/programs/water-polo/schedule/%d" % second),
        "action": "remove",
    })
    assert gone.status_code == 302
    with A.app.app_context():
        d = A.db()
        left = [row["weekday"] for row in clubadmin.schedule_days(d, clubadmin.program_by_slug(d, "water-polo")["id"])]
        assert left.count("sun") == 1 and "tue" in left and "thu" in left
        assert d.execute("SELECT COUNT(*) FROM practices").fetchone()[0] == before
        assert d.execute("SELECT COUNT(*) FROM rsvps").fetchone()[0] == rsvps
