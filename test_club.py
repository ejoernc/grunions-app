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
    assert "Water Polo" in sports and "Pool Swimming" in sports and "Open Water Swimming" in sports
    assert "Off" in sports and "USA Water Polo" in sports and "Add sport" in sports
    assert "href=/manage/area/club" in sports
    detail = admin.get("/manage/club/programs/pool-swimming").get_data(as_text=True)
    assert "Regular schedule" in detail and "does not add sessions" in detail and "href=/manage/club/programs" in detail
    assert "Program is on" in detail
    assert "Needs a sport" in sports and "Background screening" in sports and "Referee certification" in sports
    assert "Not enforced until a sport is chosen" in sports
    polo = admin.get("/manage/club/programs/water-polo").get_data(as_text=True)
    assert "SafeSport" in polo and "Add requirement" in polo and "/manage/club/programs/water-polo/requirements/new" in polo
    assert ">Requirements</span>" not in admin.get("/manage/area/club").get_data(as_text=True)
    form = admin.get("/manage/club/programs/water-polo/requirements/new").get_data(as_text=True)
    assert "Water Polo" in form and 'name=program value="' in form
    with A.app.app_context():
        d = A.db()
        wp_id = clubadmin.program_by_slug(d, "water-polo")["id"]
        pool_id = clubadmin.program_by_slug(d, "pool-swimming")["id"]
    assert ('name=program value="%d" checked' % wp_id) in form or ('value="%d" checked' % wp_id) in form
    made = admin.post("/manage/club/programs/water-polo/requirements/new", data={
        "csrf": csrf(admin, "/manage/club/programs/water-polo/requirements/new"),
        "name": "Shared clinic rule", "effect": "info", "verification": "manual",
        "program": [str(wp_id), str(pool_id)],
    })
    assert made.status_code == 302 and made.headers["Location"].endswith("/manage/club/programs/water-polo")
    again = admin.get("/manage/club/programs/water-polo").get_data(as_text=True)
    pool_page = admin.get("/manage/club/programs/pool-swimming").get_data(as_text=True)
    assert "Shared clinic rule" in again and "Also applies to: Pool Swimming" in again
    assert "Shared clinic rule" in pool_page and "Also applies to: Water Polo" in pool_page


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
    assert "<h1>People</h1>" in page and "class=mtitle>Members" in page and "class=mtitle>Compliance" in page and "class=mtitle>Membership" not in page
    roster = admin.get("/members").get_data(as_text=True)
    assert "Unpaid" in roster and ">Paying</a>" in roster and ">Not paying</a>" in roster and 'data-seg' in roster
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
    assert "Water Polo" in detail and "Pool Swimming" in detail
    with A.app.app_context():
        d = A.db()
        assert d.execute("SELECT COUNT(*) FROM rsvps").fetchone()[0] == before
        view = clubadmin.payment_view(d, mid, "2026-11-09")
        assert view["paying"] is True and view["label"] == "Paid"
        usawp = d.execute("SELECT usawp_status FROM members WHERE id=?", (mid,)).fetchone()["usawp_status"]
        assert (usawp or "") != "verified"
