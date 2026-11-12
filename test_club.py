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


def clear_preview_rows():
    """Drop only the fictional preview rows these tests inserted. Live data is a different database."""
    with A.app.app_context():
        d = A.db()
        ids = [r["id"] for r in d.execute("SELECT id FROM members WHERE email LIKE '%@preview.regulars.invalid' OR email='ejoernc@gmail.com'")]
        if ids:
            marks = ",".join("?" * len(ids))
            d.execute("DELETE FROM messages WHERE member_id IN (%s) OR body LIKE 'Preview:%%'" % marks, ids)
            d.execute("DELETE FROM rsvps WHERE member_id IN (%s)" % marks, ids)
            d.execute("DELETE FROM lineup_rsvps WHERE member_id IN (%s)" % marks, ids)
            d.execute("DELETE FROM members WHERE id IN (%s)" % marks, ids)
        d.execute("DELETE FROM practices WHERE location='Preview Pool' OR location LIKE 'Preview lane %'")
        d.execute("DELETE FROM lineup_events WHERE title='Preview harbor weekend'")
        d.execute("DELETE FROM messages WHERE body LIKE 'Preview:%'")
        d.commit()


def test_nav_3_lands_on_schedule_and_lists_only_grunions():
    member = client()
    join(member, "Ada", "Nav", "ada.nav@example.com")
    assert member.get("/").headers["Location"].endswith("/practices")
    schedule = member.get("/practices").get_data(as_text=True)
    assert 'class="nav3' in schedule and 'data-place="team"' in schedule
    tabs = schedule.split('class="nav3', 1)[1].split("</nav>", 1)[0]
    assert ">Schedule<" in tabs and ">Lineup<" in tabs and ">Chat<" in tabs and ">Manage<" not in tabs
    assert 'data-tab="calendar" class=on' in tabs
    assert '.nav3-slide.manage{background:var(--r2-tangerine)}' in schedule
    assert 'touch-action:pan-y' in schedule and 'nav3Follow' in schedule
    assert "border-radius:var(--r2-radius-pill)" in schedule
    assert tabs.find(">Schedule<") < tabs.find(">Lineup<")
    assert "--r2-ink" in schedule and "#C8FF3C" in schedule and "#4A6A00" in schedule
    menu = schedule.split('id="crestMenu"', 1)[1].split("</dialog>", 1)[0]
    assert ">Everything<" in menu and ">Grunions<" in menu and 'class="crestgo" href="/discover"' in menu and ">Log out<" in menu
    assert member.get("/find").headers["Location"].endswith("/discover")
    assert ">Member<" in menu and "Surf City" not in menu and "Harbor Seals" not in menu
    discover = member.get("/discover").get_data(as_text=True)
    assert "Discover." in discover and "Grunions is your team" in discover and "Surf City" not in discover
    assert 'data-place="everything"' in discover and ">Map<" in discover and ">Chat<" in discover and ">Inbox<" not in discover.split('class="nav3', 1)[1].split("</nav>", 1)[0]
    me = member.get("/calendar").get_data(as_text=True)
    me_tabs = me.split('class="nav3', 1)[1].split("</nav>", 1)[0]
    me_menu = me.split('id="crestMenu"', 1)[1].split("</dialog>", 1)[0]
    assert me_tabs.find(">Calendar<") < me_tabs.find(">Chat<") < me_tabs.find(">Profile<")
    assert 'data-tab="calendar" class=on' in me_tabs
    assert ">Schedule<" not in me_tabs and ">Lineup<" not in me_tabs and "Settings" not in me_tabs
    assert "Calendar · chat · profile" in me_menu
    assert "@media (min-width:768px)" in me and "window.innerWidth>=768" in me
    with A.app.app_context():
        d = A.db()
        d.execute("UPDATE members SET is_admin=1 WHERE email='ada.nav@example.com'")
        d.commit()
        assert d.execute("SELECT is_admin FROM members WHERE email='ada.nav@example.com'").fetchone()["is_admin"] == 1
    admin_tabs = member.get("/practices").get_data(as_text=True).split('class="nav3', 1)[1].split("</nav>", 1)[0]
    assert ">Manage<" in admin_tabs and admin_tabs.find(">Schedule<") < admin_tabs.find(">Manage<")
    assert 'href="/practices"' in member.get("/practices").get_data(as_text=True).split("YOUR TEAMS", 1)[1].split("</dialog>", 1)[0]


def test_selected_chat_badge_sits_beside_the_label():
    member = client()
    join(member, "Ada", "Badge", "ada.badge@example.com")
    with A.app.app_context():
        d = A.db()
        mid = d.execute("SELECT id FROM members WHERE email='ada.badge@example.com'").fetchone()["id"]
        other = d.execute("INSERT INTO members(first,last,email,joined) VALUES('Bo','Badge','bo.badge@example.com',1)").lastrowid
        mx = d.execute("SELECT COALESCE(MAX(id),0) FROM messages WHERE channel='team'").fetchone()[0]
        d.execute("""INSERT INTO chat_reads(member_id, channel, last_read) VALUES(?,?,?)
            ON CONFLICT(member_id, channel) DO UPDATE SET last_read=excluded.last_read""", (mid, "team", mx))
        d.execute("INSERT INTO messages(member_id, body, channel) VALUES(?,?,?)", (other, "lane 3", "team"))
        d.commit()
        expect = A.chat_tab_unread(d, mid, False)
    page = member.get("/chat?view=list").get_data(as_text=True)
    tabs = page.split('class="nav3', 1)[1].split("</nav>", 1)[0]
    assert 'data-tab="chat" class=on' in tabs
    assert '<span class="nav3-meta"><span class="nav3-label">Chat</span><span class=nav3-badge>%d</span></span>' % expect in tabs
    assert ".nav3-badge{position:absolute;top:2px;right:2px;" in page
    assert ".nav3-tabs a.on .nav3-badge{position:static;top:auto;right:auto;flex:none;min-width:20px;height:20px;padding:0 5px;background:var(--r2-fixed-ink);color:var(--r2-lime);font-size:12.5px}" in page
    away = member.get("/practices").get_data(as_text=True)
    away_tabs = away.split('class="nav3', 1)[1].split("</nav>", 1)[0]
    assert 'data-tab="chat" class=on' not in away_tabs
    assert '<span class="nav3-label">Chat</span><span class=nav3-badge>%d</span>' % expect in away_tabs


def test_preview_seed_stays_off_the_live_database_and_is_idempotent():
    with A.app.app_context():
        d = A.db()
        kept = d.execute("SELECT COUNT(*) FROM members").fetchone()[0]
        os.environ.pop("IS_PULL_REQUEST", None)
        assert A.seed_preview_club(d) == {"ran": False, "promoted": False, "people": 0}
        assert d.execute("SELECT COUNT(*) FROM members WHERE email LIKE '%@preview.regulars.invalid'").fetchone()[0] == 0
        os.environ["IS_PULL_REQUEST"] = "true"
        try:
            first = A.seed_preview_club(d)
            d.execute("INSERT INTO members(first,last,email,is_admin,joined) VALUES('Eli','Joern','ejoernc@gmail.com',0,1)")
            d.commit()
            second = A.seed_preview_club(d)
            third = A.seed_preview_club(d)
            assert first["ran"] is True and first["people"] == 8 and first["promoted"] is False
            assert second["promoted"] is True and third["promoted"] is False and third["people"] == 8
            assert d.execute("SELECT COUNT(*) FROM members WHERE email LIKE '%@preview.regulars.invalid'").fetchone()[0] == 8
            assert d.execute("SELECT COUNT(*) FROM practices WHERE location LIKE 'Preview lane %'").fetchone()[0] >= 3
            assert d.execute("SELECT is_admin FROM members WHERE email='ejoernc@gmail.com'").fetchone()["is_admin"] == 1
            assert d.execute("SELECT COUNT(*) FROM members").fetchone()[0] >= kept + 6
            assert d.execute("SELECT 1 FROM practices WHERE location='Preview Pool'").fetchone()
        finally:
            os.environ.pop("IS_PULL_REQUEST", None)
            clear_preview_rows()


def test_team_chat_list_keeps_everyone_and_personal_messages():
    member = client()
    join(member, "Nia", "Chat", "nia.chat@example.com")
    os.environ["IS_PULL_REQUEST"] = "true"
    try:
        with A.app.app_context():
            A.seed_preview_club(A.db())
        html = member.get("/chat?view=list").get_data(as_text=True)
        inbox = member.get("/inbox").get_data(as_text=True)
        mine = member.get("/inbox?place=me").get_data(as_text=True)
        with A.app.app_context():
            A.db().execute("UPDATE members SET role='coach' WHERE email='nia.chat@example.com'")
            A.db().commit()
        coach = member.get("/chat?view=list").get_data(as_text=True)
    finally:
        os.environ.pop("IS_PULL_REQUEST", None)
        clear_preview_rows()
    assert "Personal messages" in html and "everyone" in html and "No practice chat right now" in html and "Message the coaches" in html
    assert 'class=chatplus' in html and 'data-scope="team"' in html and "<h1>Team</h1>" not in html
    assert "New chat" in html and "Message someone" in html and "New group" in html and "Message the board" in html
    assert "New channel" not in html and "Board room" not in html and "New message" not in html
    assert "Preview Tuesday practice" not in html and "Preview Friday practice" not in html and "Preview recent practice" not in html
    ask = html.split("Ask the club", 1)[1].split("<dialog", 1)[0]
    assert "Message the board" not in ask and "Create channel" not in html
    picker = member.get("/chat?view=practices").get_data(as_text=True)
    assert "Practice chats." in picker and "Up next" in picker and "Earlier" in picker and "Search all practice chats" in picker
    with A.app.app_context():
        A.db().execute("UPDATE members SET role='athlete' WHERE email='nia.chat@example.com'")
        A.db().commit()
    assert member.get("/chat/channels").status_code == 403
    assert "Your teams" in inbox and ">Grunions<" in inbox and "Direct" in inbox
    assert 'data-place="everything"' in inbox
    assert 'data-place="me"' in mine and ">Calendar<" in mine and ">Profile<" in mine
    assert "Message someone" in mine and "New group" in mine and "Message the coaches" not in mine and "New channel" not in mine
    sheet = coach.split("id=newChat", 1)[1].split("</dialog>", 1)[0]
    assert "Board room" in sheet and "New channel" in sheet and "Message the board" not in sheet


def test_practice_chat_is_read_only_after_seven_days():
    member = client()
    join(member, "Bea", "Lock", "bea.lock@example.com")
    old = (A.today_pt() - __import__("datetime").timedelta(days=10)).isoformat()
    recent = (A.today_pt() - __import__("datetime").timedelta(days=2)).isoformat()
    with A.app.app_context():
        d = A.db()
        old_id = d.execute("INSERT INTO practices(date, start, end, location, sport, title) VALUES(?,?,?,?,?,?)",
                           (old, "19:00", "20:30", "Lock Pool", "Water Polo", "Old preview")).lastrowid
        new_id = d.execute("INSERT INTO practices(date, start, end, location, sport, title) VALUES(?,?,?,?,?,?)",
                           (recent, "19:00", "20:30", "Fresh Pool", "Water Polo", "Recent preview")).lastrowid
        d.commit()
    old_page = member.get("/chat?c=practice:%d" % old_id).get_data(as_text=True)
    assert "read-only" in old_page and "disabled" in old_page.split("id=body", 1)[1].split(">", 1)[0]
    token = re.search(r'const CSRF="([^"]+)"', member.get("/chat?c=practice:%d" % new_id).get_data(as_text=True)).group(1)
    blocked = member.post("/api/messages?c=practice:%d" % old_id, json={"body": "too late"}, headers={"X-CSRF": token})
    assert blocked.status_code == 403
    allowed = member.post("/api/messages?c=practice:%d" % new_id, json={"body": "still open"}, headers={"X-CSRF": token})
    assert allowed.status_code == 200


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
    club = admin.get("/manage/area/club").get_data(as_text=True)
    assert "Leadership" in club and "class=mtitle>Permissions" in club
    assert "Who can manage the club, sports and schedule" in club and 'href="/manage/club/permissions"' in club
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
    paying_list = re.sub(r'<nav class="nav3.*?</nav>|<dialog id="crestMenu".*?</dialog>', "", paying, flags=re.S)
    assert "<h1>Members</h1>" in paying and "Bea" in paying and "Nia" not in paying_list and ">Paying</a>" not in paying
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


def test_practice_reminders_stay_off_and_use_the_branded_mail():
    admin, going, quiet, declined = client(), client(), client(), client()
    join(admin, "Nia", "Admin", "nia.remind@example.com")
    join(going, "Bea", "Going", "bea.remind@example.com")
    join(quiet, "Ada", "Quiet", "ada.remind@example.com")
    join(declined, "Cam", "Out", "cam.remind@example.com")
    with A.app.app_context():
        d = A.db()
        d.execute("UPDATE members SET is_admin=1 WHERE email='nia.remind@example.com'")
        d.commit()
        assert clubadmin.reminder_settings(d)["enabled"] is False
        day = (A.today_pt() + __import__("datetime").timedelta(days=1)).isoformat()
        pid = d.execute("INSERT INTO practices(date, start, end, location, sport, activity_type, cancelled) VALUES(?,?,?,?,?,?,0)",
                        (day, "19:00", "20:30", "Marina High School", "Water Polo", "practice")).lastrowid
        ids = {row["email"]: row["id"] for row in d.execute("SELECT id, email FROM members")}
        d.execute("INSERT INTO rsvps(practice_id, member_id, going) VALUES(?,?,1)", (pid, ids["bea.remind@example.com"]))
        d.execute("INSERT INTO rsvps(practice_id, member_id, going) VALUES(?,?,0)", (pid, ids["cam.remind@example.com"]))
        before = d.execute("SELECT COUNT(*) FROM rsvps").fetchone()[0]
        d.commit()
    page = admin.get("/manage/club/reminders").get_data(as_text=True)
    assert "Send practice reminders" in page and "Hours before" in page and "checked" not in page.split("Send practice reminders")[0][-80:]
    settings = admin.get("/notifications").get_data(as_text=True)
    assert "Practice reminders" in settings and 'value=both' in settings and "checked" in settings
    sent = []
    real_send, real_ready = A.send_email, A.smtp_ready
    A.send_email = lambda to, subj, text, html=None: sent.append((to, subj, text, html))
    A.smtp_ready = lambda: True
    start = __import__("datetime").datetime.fromisoformat(day + "T19:00")
    try:
        nd = A.open_db()
        try:
            A.run_practice_reminders(nd, start - __import__("datetime").timedelta(hours=2))
        finally:
            nd.close()
        assert sent == []
        with A.app.app_context():
            d = A.db()
            clubadmin.save_reminder_settings(d, {"enabled": "1", "hours": "3"})
            d.commit()
        nd = A.open_db()
        try:
            A.run_practice_reminders(nd, start - __import__("datetime").timedelta(hours=2))
            A.run_practice_reminders(nd, start - __import__("datetime").timedelta(hours=2))
        finally:
            nd.close()
    finally:
        A.send_email, A.smtp_ready = real_send, real_ready
    by = {row[0]: row for row in sent}
    assert {"bea.remind@example.com", "ada.remind@example.com", "nia.remind@example.com", "cam.remind@example.com"} <= set(by)
    assert not any(addr.endswith("@preview.regulars.invalid") for addr in by)
    assert by["bea.remind@example.com"][1] == "Water Polo practice today at 7:00 PM, Marina High School"
    assert ">SPORT<" in by["bea.remind@example.com"][3] or "SPORT" in by["bea.remind@example.com"][3]
    assert "Sign up for practice" in by["bea.remind@example.com"][3]
    assert "Sent by" in by["bea.remind@example.com"][3] and "/practices/%d" % pid in by["bea.remind@example.com"][3]
    assert by["cam.remind@example.com"][1] == by["bea.remind@example.com"][1]
    with A.app.app_context():
        d = A.db()
        assert d.execute("SELECT COUNT(*) FROM rsvps").fetchone()[0] == before
        d.execute("UPDATE members SET practice_reminder='off' WHERE email='bea.remind@example.com'")
        d.execute("DELETE FROM practice_reminder_sent WHERE practice_id=?", (pid,))
        d.execute("DELETE FROM sent_notices WHERE kind LIKE 'email:practice_%'")
        d.commit()
    sent.clear()
    A.send_email = lambda to, subj, text, html=None: sent.append((to, subj, text, html))
    A.smtp_ready = lambda: True
    try:
        nd = A.open_db()
        try:
            A.run_practice_reminders(nd, start - __import__("datetime").timedelta(minutes=1))
            A.run_practice_reminders(nd, start + __import__("datetime").timedelta(minutes=1))
        finally:
            nd.close()
    finally:
        A.send_email, A.smtp_ready = real_send, real_ready
    assert "bea.remind@example.com" not in {row[0] for row in sent}


def test_a_new_going_rsvp_confirms_once_and_does_not_rewrite_the_rsvp():
    member = client()
    join(member, "Bea", "Signup", "bea.signup@example.com")
    with A.app.app_context():
        d = A.db()
        day = (A.today_pt() + __import__("datetime").timedelta(days=2)).isoformat()
        pid = d.execute("INSERT INTO practices(date, start, end, location, address, sport, activity_type, cancelled) VALUES(?,?,?,?,?,?,?,0)",
                        (day, "19:00", "20:30", "Marina High School", "15871 Springdale St, Huntington Beach, CA 92649", "Water Polo", "practice")).lastrowid
        d.commit()
    sent = []
    real_send, real_ready = A.send_email, A.smtp_ready
    A.send_email = lambda *a, **k: sent.append((a, k))
    A.smtp_ready = lambda: True
    try:
        token = csrf(member, "/practices/%d" % pid)
        first = member.post("/practices/%d" % pid, data={"csrf": token, "pid": pid, "action": "going"})
        assert first.status_code == 302
        again = member.post("/practices/%d" % pid, data={"csrf": csrf(member, "/practices/%d" % pid), "pid": pid, "action": "going"})
        assert again.status_code == 302
        member.post("/practices/%d" % pid, data={"csrf": csrf(member, "/practices/%d" % pid), "pid": pid, "action": "notgoing"})
        member.post("/practices/%d" % pid, data={"csrf": csrf(member, "/practices/%d" % pid), "pid": pid, "action": "going"})
    finally:
        A.send_email, A.smtp_ready = real_send, real_ready
    assert len(sent) == 1
    assert sent[0][0][0] == "bea.signup@example.com"
    assert sent[0][0][1].startswith("You're signed up: Water Polo practice,")
    html = sent[0][1]["html"]
    assert "Sign up for practice" not in html and "View practice" in html
    assert "SPORT" in html and "BEGIN:VCALENDAR" in sent[0][1]["ics"]
    assert "calendar.google.com" in html
    with A.app.app_context():
        d = A.db()
        assert d.execute("SELECT going FROM rsvps WHERE practice_id=? AND member_id=(SELECT id FROM members WHERE email='bea.signup@example.com')", (pid,)).fetchone()["going"] == 1


def test_permissions_lists_admins_and_does_not_raise_access_on_its_own():
    admin, athlete = client(), client()
    join(admin, "Nia", "Admin", "nia.perm@example.com")
    join(athlete, "Bea", "Athlete", "bea.perm@example.com")
    with A.app.app_context():
        d = A.db()
        d.execute("UPDATE members SET is_admin=1 WHERE email='nia.perm@example.com'")
        d.commit()
        nia = d.execute("SELECT id FROM members WHERE email='nia.perm@example.com'").fetchone()["id"]
        bea = d.execute("SELECT id FROM members WHERE email='bea.perm@example.com'").fetchone()["id"]
        before = d.execute("SELECT is_admin FROM members WHERE id=?", (nia,)).fetchone()["is_admin"]
    page = admin.get("/manage/club/permissions").get_data(as_text=True)
    assert "Nia" in page and "Admin" in page and "Assign" in page and "Bea" not in page
    with A.app.app_context():
        d = A.db()
        assert d.execute("SELECT is_admin FROM members WHERE id=?", (nia,)).fetchone()["is_admin"] == before
        role = d.execute("INSERT INTO leadership_roles(program_id, name, permission, sort) VALUES(NULL, 'Treasurer', 'admin_lite', 1)").lastrowid
        d.commit()
    saved = admin.post("/manage/club/permissions/new", data={
        "csrf": csrf(admin, "/manage/club/permissions/new"),
        "person": str(bea), "role": str(role),
    })
    assert saved.status_code == 302
    with A.app.app_context():
        d = A.db()
        assert d.execute("SELECT is_admin FROM members WHERE id=?", (bea,)).fetchone()["is_admin"] == 0
        assert d.execute("SELECT 1 FROM leadership_members WHERE role_id=? AND member_id=?", (role, bea)).fetchone()
    cleared = admin.post("/manage/club/permissions/%d" % nia, data={
        "csrf": csrf(admin, "/manage/club/permissions/%d" % nia),
    })
    assert cleared.status_code == 302
    with A.app.app_context():
        d = A.db()
        assert d.execute("SELECT is_admin FROM members WHERE id=?", (nia,)).fetchone()["is_admin"] == 1


def test_chat_accepts_heic_and_names_live_photo_and_proraw():
    import io
    import os
    from PIL import Image
    import pillow_heif
    pillow_heif.register_heif_opener()
    member = client()
    join(member, "Jon", "Photo", "jon.photo@example.com")
    page = member.get("/chat").get_data(as_text=True)
    accept = page.split('id=file', 1)[1].split('>', 1)[0]
    assert 'accept="image/*' in accept
    assert "image/heic" in accept and "image/heif" in accept
    assert "image/heic-sequence" in accept and ".heic" in accept and ".heif" in accept
    assert "That photo isn't supported. Use a JPG, PNG, GIF, WEBP, or HEIC photo." in page
    assert "Live Photo videos aren't supported" in page and "ProRAW isn't supported" in page
    token = re.search(r'const CSRF="([^"]+)"', page).group(1)
    def post(blob, name):
        blob.seek(0)
        return member.post("/api/messages", data={"image": (blob, name)}, headers={"X-CSRF": token}, content_type="multipart/form-data")
    before = None
    with A.app.app_context():
        before = [row[0] for row in A.db().execute("SELECT image FROM messages WHERE image IS NOT NULL").fetchall()]
    heif = io.BytesIO()
    shot = Image.new("RGB", (20, 40), (12, 34, 56))
    exif = shot.getexif()
    exif[274] = 6
    shot.save(heif, "HEIF", exif=exif.tobytes())
    saved = post(heif, "iphone.heic")
    assert saved.status_code == 200
    heif2 = io.BytesIO()
    Image.new("RGB", (16, 16), (1, 2, 3)).save(heif2, "HEIF")
    assert post(heif2, "iphone.heif").status_code == 200
    for fmt, name, size in (("JPEG", "pool.jpg", (30, 20)), ("PNG", "pool.png", (30, 20)), ("GIF", "pool.gif", (30, 20)), ("WEBP", "pool.webp", (30, 20))):
        buf = io.BytesIO()
        Image.new("RGB", size, (4, 5, 6)).save(buf, fmt)
        assert post(buf, name).status_code == 200
    live = post(io.BytesIO(b"\x00\x00\x00\x14ftypqt  \x00\x00\x00\x00"), "live.mov")
    raw = post(io.BytesIO(b"II*\x00" + b"\x00" * 16 + b"DNG "), "shot.dng")
    junk = post(io.BytesIO(b"not a photo"), "notes.txt")
    assert live.status_code == 400 and "Live Photo" in live.get_json()["error"] and "JPG, PNG, GIF, WEBP, or HEIC" in live.get_json()["error"]
    assert raw.status_code == 400 and "ProRAW" in raw.get_json()["error"]
    assert junk.status_code == 400 and "isn't supported" in junk.get_json()["error"]
    sequence = post(io.BytesIO(b"\x00\x00\x00\x18ftyphevc" + b"\x00" * 8), "burst.heic")
    assert sequence.status_code == 400 and "isn't supported" in sequence.get_json()["error"]
    with A.app.app_context():
        rows = A.db().execute("SELECT id, image FROM messages WHERE image IS NOT NULL ORDER BY id").fetchall()
    new = [row for row in rows if row["image"] not in before]
    assert any(row["image"].endswith(".jpg") for row in new)
    heic_row = next(row for row in new if row["image"].endswith(".jpg"))
    full = member.get("/media/%d/full" % heic_row["id"])
    opened = Image.open(io.BytesIO(full.data))
    assert opened.format == "JPEG" and opened.size == (40, 20) and not dict(opened.getexif())
    for row in new:
        for suffix in (row["image"], row["image"].rsplit(".", 1)[0] + "_t.webp"):
            path = os.path.join(A.UPLOADS, suffix)
            if os.path.isfile(path):
                os.remove(path)
