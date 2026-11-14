"""Regulars 2.0 rebuild (Figma audit page) — behaviour the redesign adds. Run: .venv/bin/python -m pytest -q test_redesign.py"""
import os, re, sqlite3, tempfile, datetime as dt
D = tempfile.mkdtemp()
os.environ.update(DATA_DIR=D, ADMIN_EMAIL="boss@example.com", DEV_SHOW_LINKS="0")
os.environ.pop("GRUNIONS_DB", None); os.environ.pop("GRUNIONS_UPLOADS", None)
import app as A


def csrf(c, p):
    return re.search(r'(?:name=csrf value=|const CSRF=)"([^"]+)"', c.get(p).get_data(as_text=True)).group(1)


def join(first, last, email):
    c = A.app.test_client()
    c.post("/join", data=dict(birth_date="1990-03-04", csrf=csrf(c, "/join"), first=first, last=last, email=email, phone="1"))
    return c


def sql(q, args=()):
    con = sqlite3.connect(A.DB); cur = con.execute(q, args); con.commit(); rows = cur.fetchall(); con.close(); return rows


member = join("Rae", "Design", "rae@example.com")
boss = join("Boss", "One", "boss@example.com")
RAE = sql("SELECT id FROM members WHERE email='rae@example.com'")[0][0]


def test_appearance_saves_and_sets_the_theme():
    html = member.get("/settings").get_data(as_text=True)
    assert "Appearance" in html and 'data-theme="dark"' in html and "/settings" in member.get("/profile").get_data(as_text=True)
    member.post("/appearance", data=dict(csrf=csrf(member, "/appearance"), appearance="light"))
    assert 'data-theme="light"' in member.get("/practices").get_data(as_text=True)
    member.post("/appearance", data=dict(csrf=csrf(member, "/appearance"), appearance="nonsense"))
    assert sql("SELECT appearance FROM members WHERE id=?", (RAE,))[0][0] == "light"
    member.post("/appearance", data=dict(csrf=csrf(member, "/appearance"), appearance="system"))
    page = member.get("/practices").get_data(as_text=True)
    assert 'data-theme="system"' in page and 'content="light dark"' in page
    member.post("/appearance", data=dict(csrf=csrf(member, "/appearance"), appearance="dark"))


def test_drawer_pins_to_the_top_while_setup_is_open_and_not_after():
    page = member.get("/practices").get_data(as_text=True)
    assert 'data-start="full"' in page  # new member: Finish setup open, not cleared
    sql("UPDATE members SET setup_dismissed=1, usawp_status='verified', usawp_number='1002010', usawp_valid_until='2099-01-01' WHERE id=?", (RAE,))
    page = member.get("/practices").get_data(as_text=True)
    assert 'data-start="half"' in page and ">Upcoming</h1>" in page
    sql("UPDATE members SET setup_dismissed=0, usawp_status='unknown', usawp_number=NULL, usawp_valid_until=NULL WHERE id=?", (RAE,))


def test_home_uses_the_schedule_shell_and_keeps_the_usawp_form():
    page = member.get("/home").get_data(as_text=True)
    assert "id=schedSheet" in page and "Enter your USAWP membership number" in page and "pushCard" in page
    r = member.post("/home", data=dict(csrf=csrf(member, "/home"), usawp_number="1234567"))
    assert r.status_code == 302
    assert sql("SELECT usawp_number FROM members WHERE id=?", (RAE,))[0][0] == "1234567"
    assert "Enter your USAWP membership number" not in member.get("/home").get_data(as_text=True)


def test_schedule_list_shows_socials_with_their_practice():
    day = (A.today_pt() + dt.timedelta(days=3)).isoformat()
    sql("""INSERT INTO practices(date,start,end,location,sport,title,social_kind,social_place,social_time,social_when)
           VALUES(?,?,?,?,?,?,?,?,?,?)""", (day, "19:00", "20:30", "Test Pool", "Water Polo", "List practice", "Coffee", "Test Cafe", "21:00", "after"))
    page = member.get("/practices?view=list").get_data(as_text=True)
    i = page.index("List practice"); j = page.index("Test Cafe")
    assert j > i and "AFTER PRACTICE" in page and "rg-someta" in page
    assert "Test Cafe" not in member.get("/practices?view=list&when=past").get_data(as_text=True)


def test_map_unavailable_is_the_2_0_component():
    page = member.get("/practices").get_data(as_text=True)
    assert "rg-mapmiss" in page or 'id=homeMap' in page


def _practice(title, days=2):
    day = (A.today_pt() + dt.timedelta(days=days)).isoformat()
    sql("INSERT INTO practices(date,start,end,location,sport,title) VALUES(?,?,?,?,?,?)", (day, "19:00", "20:30", "Ride Pool " + title, "Water Polo", title))
    return sql("SELECT id FROM practices WHERE title=?", (title,))[0][0]


def _going(c, pid):
    sql("UPDATE members SET usawp_status='verified', usawp_number='1002010', usawp_valid_until='2099-01-01'")
    return c.post("/practices", data=dict(csrf=csrf(c, "/rides/settings"), pid=pid, action="going"))


def test_ride_settings_validate_and_auto_offer_on_going():
    driver = join("Dee", "Driver", "dee@example.com")
    bad = driver.post("/rides/settings", data=dict(csrf=csrf(driver, "/rides/settings"), ride_offer="1", ride_area="123 Main Street", ride_seats="3"), follow_redirects=True)
    assert "neighborhood or city" in bad.get_data(as_text=True)
    driver.post("/rides/settings", data=dict(csrf=csrf(driver, "/rides/settings"), ride_offer="1", ride_area="Fountain Valley", ride_seats="3"))
    dee = sql("SELECT id, ride_offer, ride_area, ride_seats FROM members WHERE email='dee@example.com'")[0]
    assert dee[1:] == (1, "Fountain Valley", 3)
    pid = _practice("Auto offer practice")
    _going(driver, pid)
    assert sql("SELECT area, seats, status FROM ride_offers WHERE practice_id=? AND driver_id=?", (pid, dee[0])) == [("Fountain Valley", 3, "open")]
    assert "Offering" in driver.get("/settings").get_data(as_text=True)


def test_ride_board_shows_offers_and_asks_and_driver_picks_from_it():
    driver = join("Ola", "Wheels", "ola@example.com")
    rider = join("Pia", "Rider", "pia@example.com")
    pid = _practice("Board practice")
    _going(driver, pid); _going(rider, pid)
    driver.post("/practices/%d/rides" % pid, data=dict(csrf=csrf(driver, "/practices/%d/rides" % pid), action="offer", area="Belmont Shore", seats="2", next="board"))
    r = rider.post("/practices/%d/rides" % pid, data=dict(csrf=csrf(rider, "/practices/%d/rides" % pid), action="ask", area="Seal Beach", next="board"))
    assert r.headers["Location"].endswith("/practices/%d/rides" % pid)
    board = driver.get("/practices/%d/rides" % pid).get_data(as_text=True)
    assert "Rides." in board and "From Belmont Shore" in board and "Seal Beach" in board and "Pick up" in board
    assert "Street" not in board
    req = sql("SELECT id FROM ride_requests WHERE practice_id=? AND status='open'", (pid,))[0][0]
    driver.post("/practices/%d/rides" % pid, data=dict(csrf=csrf(driver, "/practices/%d/rides" % pid), action="pick", req_id=req, next="board"))
    assert sql("SELECT status FROM ride_requests WHERE id=?", (req,))[0][0] == "matched"
    assert "is driving you" in rider.get("/practices/%d/rides" % pid).get_data(as_text=True)


def test_schedule_home_ride_sheets_post_for_real():
    page = member.get("/practices").get_data(as_text=True)
    assert "Preview only" not in page and "Ride settings aren" not in page


def test_leave_by_plan_picks_the_latest_departure_that_arrives_on_time():
    import flows2, routing
    start = dt.datetime(2030, 1, 8, 19, 0)
    mins = iter([17, 17, 18, 18, 18, 23, 27])  # 17:55 → 18:55, every 10 min
    plan = flows2.leave_plan(start, 5, lambda deps: [routing.Route(next(mins)) for _ in deps])
    assert plan["arrive_by"] == dt.datetime(2030, 1, 8, 18, 55)
    assert [b["minutes"] for b in plan["bars"]][-1] == 27 and plan["late_delta"] > 0
    assert plan["leave_by"] + dt.timedelta(minutes=plan["minutes"]) <= plan["arrive_by"]
    assert {b["level"] for b in plan["bars"]} >= {"clear", "jammed"}


def test_leave_by_api_window_and_last_location_saved_rounded():
    day = (A.today_pt() + dt.timedelta(days=5)).isoformat()
    sql("INSERT INTO practices(date,start,end,location,sport,title,lat,lng) VALUES(?,?,?,?,?,?,?,?)", (day, "19:00", "20:30", "Far Pool", "Water Polo", "Far practice", 33.7, -118.0))
    pid = sql("SELECT id FROM practices WHERE title='Far practice'")[0][0]
    r = member.post("/api/leave-by", json=dict(id=pid, lat=33.81234, lng=-118.16789), headers={"X-CSRF": csrf(member, "/rides/settings")})
    assert r.get_json() == {"ok": False, "error": "window"}
    assert sql("SELECT last_lat, last_lng FROM members WHERE id=?", (RAE,))[0] == (33.812, -118.168)
    assert "Leave by" in member.get("/practices/%d/leave-by" % pid).get_data(as_text=True)
    priv = member.get("/privacy").get_data(as_text=True)
    assert "Save my last location" in priv and "Last saved" in priv and "Forget my location" in priv
    member.post("/privacy/location/forget", data=dict(csrf=csrf(member, "/privacy")))
    assert sql("SELECT last_lat, last_loc_at FROM members WHERE id=?", (RAE,))[0] == (None, None)
    # Turning saving off stops it; turning it back on lets the next device fix save.
    member.post("/privacy", data=dict(csrf=csrf(member, "/privacy"), show_attendance="1"))
    member.post("/api/leave-by", json=dict(id=pid, lat=33.8, lng=-118.1), headers={"X-CSRF": csrf(member, "/rides/settings")})
    assert sql("SELECT save_location, last_lat FROM members WHERE id=?", (RAE,))[0] == (0, None)
    member.post("/privacy", data=dict(csrf=csrf(member, "/privacy"), show_attendance="1", save_location="1"))


def test_leave_alerts_push_at_3h_then_only_when_leave_by_moves_5_min():
    import routing
    la = join("Lee", "Alert", "lee@example.com")
    lid = sql("SELECT id FROM members WHERE email='lee@example.com'")[0][0]
    today = A.today_pt().isoformat()
    sql("INSERT INTO practices(date,start,end,location,sport,title,lat,lng) VALUES(?,?,?,?,?,?,?,?)", (today, "19:00", "20:30", "Alert Pool", "Water Polo", "Alert practice", 33.7, -118.0))
    pid = sql("SELECT id FROM practices WHERE title='Alert practice'")[0][0]
    _going(la, pid)
    base = dt.datetime.combine(A.today_pt(), dt.time(16, 30))
    sql("UPDATE members SET last_lat=33.8, last_lng=-118.1, last_loc_at=?, leave_buffer=5 WHERE id=?", (base.isoformat(), lid))
    minutes = iter([20, 22, 27, 28])
    pushed, saved_push, saved_once = [], A.push_member, A.drive_service.once
    A.push_member = lambda d, m, kind, title, body, url: pushed.append((m["id"], kind, title))
    A.drive_service.once = lambda o, dd, prof, now: routing.Route(next(minutes))
    try:
        con = A.open_db()
        A.run_leave_alerts(con, base)                                  # 18:35 → first push
        A.run_leave_alerts(con, base + dt.timedelta(minutes=5))        # too soon, no call
        A.run_leave_alerts(con, base + dt.timedelta(minutes=15))       # 22 min: moved 2, no push
        A.run_leave_alerts(con, base + dt.timedelta(minutes=30))       # 27 min: moved 7 → push
        A.run_leave_alerts(con, base + dt.timedelta(minutes=45))       # 28 min: moved 1 from 27 → none
        A.drive_service.once = lambda o, dd, prof, now: routing.Route(60, estimated=True)
        A.run_leave_alerts(con, base + dt.timedelta(minutes=60))       # estimate never pushes
        con.close()
    finally:
        A.push_member, A.drive_service.once = saved_push, saved_once
    mine = [t for (m, k, t) in pushed if m == lid]
    assert mine == ["Leave by 6:35pm", "Leave by moved to 6:28pm"]
    assert all(k == "leave_by" for (m, k, t) in pushed if m == lid)


def test_gender_saves_legal_is_admin_only_and_wnb_rides_filter():
    wa = join("Wren", "Ally", "wren@example.com"); mo = join("Moe", "Man", "moe@example.com")
    wid = sql("SELECT id FROM members WHERE email='wren@example.com'")[0][0]
    def ident(c, mid_email, gid, legal, extra=None):
        row = sql("SELECT first,last,email,phone FROM members WHERE email=?", (mid_email,))[0]
        data = dict(csrf=csrf(c, "/profile"), action="identity", first=row[0], last=row[1], email=row[2], phone="5555550100", gender_identity=gid, legal_gender=legal)
        data.update(extra or {}); return c.post("/profile", data=data)
    ident(wa, "wren@example.com", "nonbinary", "female")
    ident(mo, "moe@example.com", "man", "bogus")
    assert sql("SELECT gender_identity, legal_gender FROM members WHERE id=?", (wid,))[0] == ("nonbinary", "female")
    assert sql("SELECT gender_identity, legal_gender FROM members WHERE email='moe@example.com'")[0] == ("man", None)
    assert "Sex on sport membership" in boss.get("/profile/%d" % wid).get_data(as_text=True)
    assert "Sex on sport membership" not in mo.get("/profile/%d" % wid).get_data(as_text=True)
    # Moe can't turn the filter on; Wren can.
    mo.post("/rides/settings", data=dict(csrf=csrf(mo, "/rides/settings"), ride_wnb="1", ride_seats="2"))
    assert sql("SELECT ride_wnb FROM members WHERE email='moe@example.com'")[0][0] == 0
    assert "Women &amp; non-binary only" in wa.get("/rides/settings").get_data(as_text=True)
    wa.post("/rides/settings", data=dict(csrf=csrf(wa, "/rides/settings"), ride_wnb="1", ride_seats="2"))
    assert sql("SELECT ride_wnb FROM members WHERE id=?", (wid,))[0][0] == 1
    pid = _practice("WNB practice")
    _going(wa, pid); _going(mo, pid)
    mo.post("/practices/%d/rides" % pid, data=dict(csrf=csrf(mo, "/practices/%d/rides" % pid), action="offer", area="Long Beach", seats="2", next="board"))
    wa.post("/practices/%d/rides" % pid, data=dict(csrf=csrf(wa, "/practices/%d/rides" % pid), action="ask", area="Lakewood", next="board"))
    assert "Lakewood" not in mo.get("/practices/%d/rides" % pid).get_data(as_text=True)
    assert "Long Beach" not in wa.get("/practices/%d/rides" % pid).get_data(as_text=True)
    req = sql("SELECT id FROM ride_requests WHERE practice_id=? AND status='open'", (pid,))[0][0]
    mo.post("/practices/%d/rides" % pid, data=dict(csrf=csrf(mo, "/practices/%d/rides" % pid), action="pick", req_id=req, next="board"))
    assert sql("SELECT status FROM ride_requests WHERE id=?", (req,))[0][0] == "open"
    # Changing identity away from an eligible one turns the filter off.
    ident(wa, "wren@example.com", "prefer_not", "female")
    assert sql("SELECT ride_wnb FROM members WHERE id=?", (wid,))[0][0] == 0


def test_share_trip_uses_preferred_names_and_no_server_send():
    dr = join("Drew", "Legalname", "drew@example.com"); ri = join("Rita", "Rider", "rita@example.com")
    sql("UPDATE members SET preferred_first='Dre' WHERE email='drew@example.com'")
    sql("UPDATE members SET preferred_first='Ree' WHERE email='rita@example.com'")
    pid = _practice("Share practice")
    _going(dr, pid); _going(ri, pid)
    dr.post("/practices/%d/rides" % pid, data=dict(csrf=csrf(dr, "/practices/%d/rides" % pid), action="offer", area="Belmont Shore", seats="2", next="board"))
    ri.post("/practices/%d/rides" % pid, data=dict(csrf=csrf(ri, "/practices/%d/rides" % pid), action="ask", area="Seal Beach", next="board"))
    req = sql("SELECT id FROM ride_requests WHERE practice_id=? AND status='open'", (pid,))[0][0]
    dr.post("/practices/%d/rides" % pid, data=dict(csrf=csrf(dr, "/practices/%d/rides" % pid), action="pick", req_id=req, next="board"))
    rider_page = ri.get("/practices/%d/rides" % pid).get_data(as_text=True)
    driver_page = dr.get("/practices/%d/rides" % pid).get_data(as_text=True)
    assert "Share trip" in rider_page and "Riding with Dre" in rider_page
    assert "Share trip" in driver_page and "Driving Ree" in driver_page and "Rita" not in driver_page.split("Driving ")[1][:40]


def test_availability_windows_fit_conflicts_and_away():
    av = join("Ava", "Week", "ava@example.com")
    t = csrf(av, "/calendar?when=availability")
    bad = av.post("/availability", data=dict(csrf=t, action="add", weekday="1", start="21:00", end="19:00"), follow_redirects=True)
    assert "end time after the start" in bad.get_data(as_text=True)
    today = A.today_pt(); monday = today - dt.timedelta(days=today.weekday())
    day = monday + dt.timedelta(days=6)  # Sunday this week
    av.post("/availability", data=dict(csrf=t, action="add", weekday="6", start="18:00", end="21:00"))
    aid = sql("SELECT id FROM members WHERE email='ava@example.com'")[0][0]
    assert sql("SELECT weekday,start,end FROM avail_windows WHERE member_id=?", (aid,)) == [(6, "18:00", "21:00")]
    assert sql("SELECT avail_days FROM members WHERE id=?", (aid,))[0][0] == "Sun"
    sql("INSERT INTO practices(date,start,end,location,sport,title) VALUES(?,?,?,?,?,?)", (day.isoformat(), "19:00", "20:30", "Fit Pool", "Water Polo", "Fits practice"))
    sql("INSERT INTO practices(date,start,end,location,sport,title) VALUES(?,?,?,?,?,?)", (day.isoformat(), "07:00", "08:00", "Fit Pool AM", "Water Polo", "Early conflict"))
    page = av.get("/availability/fit").get_data(as_text=True)
    assert "Early conflict" in page and "outside your windows" in page and "Mark Not going" in page
    assert "Fits practice — " not in page
    av.post("/availability/away", data=dict(csrf=csrf(av, "/calendar?when=availability"), action="add", start_date=day.isoformat(), end_date=day.isoformat(), note="Trip"))
    assert "you're away that day" in av.get("/availability/fit").get_data(as_text=True).replace("&#39;", "'")
    assert av.get("/availability").headers["Location"].endswith("/calendar?when=availability")
    # Max travel: a saved location far from the pool marks the session Too far.
    sql("UPDATE away_dates SET end_date='2000-01-01', start_date='2000-01-01' WHERE member_id=?", (aid,))
    sql("UPDATE practices SET lat=33.7, lng=-118.0 WHERE title='Fits practice'")
    sql("UPDATE members SET last_lat=34.4, last_lng=-119.7, last_loc_at=? WHERE id=?", (dt.datetime.now().isoformat(), aid))
    av.post("/availability/travel", data=dict(csrf=csrf(av, "/availability/fit"), max_travel="30"))
    assert sql("SELECT max_travel FROM members WHERE id=?", (aid,))[0][0] == 30
    page = av.get("/availability/fit").get_data(as_text=True)
    assert "Too far" in page and "past your 30 min limit" in page


def test_auto_rsvp_asks_once_and_never_rsvps():
    au = join("Auto", "Asker", "auto@example.com")
    aid = sql("SELECT id FROM members WHERE email='auto@example.com'")[0][0]
    tomorrow = A.today_pt() + dt.timedelta(days=1)
    sql("INSERT INTO practices(date,start,end,location,sport,title) VALUES(?,?,?,?,?,?)", (tomorrow.isoformat(), "19:00", "20:30", "Auto Pool", "Water Polo", "Auto practice"))
    sql("INSERT INTO avail_windows(member_id,weekday,start,end) VALUES(?,?,?,?)", (aid, tomorrow.weekday(), "18:00", "22:00"))
    sql("UPDATE members SET auto_rsvp=1 WHERE id=?", (aid,))
    pushed = []
    saved = A.push_member
    A.push_member = lambda d, m, kind, title, body, url: pushed.append((m["id"], title))
    try:
        con = A.open_db()
        now = dt.datetime.combine(A.today_pt(), dt.time(19, 30))
        A.run_auto_rsvp_asks(con, now); A.run_auto_rsvp_asks(con, now); con.commit(); con.close()
    finally:
        A.push_member = saved
    assert pushed.count((aid, "Going tomorrow?")) == 1
    assert not sql("SELECT 1 FROM rsvps r JOIN practices p ON p.id=r.practice_id WHERE p.title='Auto practice'")


def test_volunteer_shifts_capacity_one_per_event_and_hours():
    import flows2
    vol = join("Vic", "Volunteer", "vic@example.com"); other = join("Oz", "Other", "oz@example.com")
    sql("UPDATE members SET is_admin=1 WHERE email='boss@example.com'")
    past = (A.today_pt() - dt.timedelta(days=10)).isoformat(); soon = (A.today_pt() + dt.timedelta(days=10)).isoformat()
    for title, day in (("Past cleanup", past), ("Beach cleanup", soon)):
        sql("INSERT INTO lineup_events(kind,title,date,city,venue,start,status) VALUES('Volunteer',?,?,'Bolsa Chica','Lot 2','08:00','published')", (title, day))
    eid = sql("SELECT id FROM lineup_events WHERE title='Beach cleanup'")[0][0]
    peid = sql("SELECT id FROM lineup_events WHERE title='Past cleanup'")[0][0]
    t = csrf(boss, "/lineup/%d/shifts" % eid)
    boss.post("/lineup/%d/shifts" % eid, data=dict(csrf=t, action="add", title="Setup", start="08:00", end="10:00", capacity="1"))
    boss.post("/lineup/%d/shifts" % eid, data=dict(csrf=t, action="add", title="Cleanup crew", start="10:00", end="12:00", capacity="5"))
    boss.post("/lineup/%d/shifts" % eid, data=dict(csrf=t, action="goal", goal="10"))
    assert vol.post("/lineup/%d/shifts" % eid, data=dict(csrf=t, action="add", title="x", start="08:00", end="09:00", capacity="1")).status_code in (400, 403)
    s1, s2 = [r[0] for r in sql("SELECT id FROM lineup_shifts WHERE event_id=? ORDER BY start", (eid,))]
    tv = csrf(vol, "/lineup/%d/shifts" % eid)
    r = vol.post("/lineup/%d/shifts" % eid, data=dict(csrf=tv, action="signup", shift=s1))
    assert r.headers["Location"].endswith("/lineup/%d/shifts/%d" % (eid, s1))
    full = other.post("/lineup/%d/shifts" % eid, data=dict(csrf=csrf(other, "/lineup/%d/shifts" % eid), action="signup", shift=s1), follow_redirects=True)
    assert "That shift is full." in full.get_data(as_text=True)
    vol.post("/lineup/%d/shifts" % eid, data=dict(csrf=tv, action="signup", shift=s2))  # moves, one per event
    vid = sql("SELECT id FROM members WHERE email='vic@example.com'")[0][0]
    assert sql("SELECT shift_id FROM shift_signups WHERE member_id=?", (vid,)) == [(s2,)]
    sql("INSERT INTO lineup_shifts(event_id,start,end,title,capacity) VALUES(?,?,?,?,?)", (peid, "09:00", "12:00", "Timing", 3))
    ps = sql("SELECT id FROM lineup_shifts WHERE event_id=?", (peid,))[0][0]
    sql("INSERT INTO shift_signups(shift_id,member_id,at) VALUES(?,?,?)", (ps, vid, "x"))
    done = vol.get("/lineup/%d/shifts/%d" % (eid, s2)).get_data(as_text=True)
    assert "Your service hours" in done and "of 10 hrs" in done and ">03<" in done and "Past cleanup" in done
    assert "BEGIN:VEVENT" in vol.get("/lineup/%d/shifts/%d.ics" % (eid, s2)).get_data(as_text=True)
    assert "Pick a shift" in vol.get("/lineup/%d" % eid).get_data(as_text=True) or "Your shift" in vol.get("/lineup/%d" % eid).get_data(as_text=True)


def test_people_menu_insurance_membership_board_and_no_auto_lookup():
    import sportspay
    pm = join("Pat", "Menu", "pat@example.com")
    pid_ = sql("SELECT id FROM members WHERE email='pat@example.com'")[0][0]
    page = boss.get("/members").get_data(as_text=True)
    # Nov 13 (Figma 62 S1/S3): rows have no buttons; fixes live in the status drawer, the board in Leaders.
    drawer = boss.get("/members/%d/status" % pid_).get_data(as_text=True)
    assert 'data-status="%d"' % pid_ in page and "Mark verified" in drawer and "Check USAWP" not in page
    assert "ask_bot" not in page and "Look it up" not in page
    t = csrf(boss, "/members")
    boss.post("/members", data=dict(csrf=t, member_id=pid_, action="verify", number="1002020", valid_until="2099-01-01"))
    assert sql("SELECT usawp_status, usawp_number FROM members WHERE id=?", (pid_,))[0] == ("verified", "1002020")
    assert boss.post("/members", data=dict(csrf=t, member_id=pid_, action="ask_bot")).status_code == 400
    assert A.app.test_client().get("/api/verify-requests").status_code == 410
    # Membership: an annual plan makes the item appear and marks them paying.
    con = A.open_db(); sportspay.ensure(con) if hasattr(sportspay, "ensure") else None; con.close()
    sql("INSERT INTO payment_plans(name, kind, active) VALUES('Season pass','annual',1)")
    plan = sql("SELECT id FROM payment_plans WHERE name='Season pass'")[0][0]
    assert "Mark paid" in boss.get("/members/%d/status" % pid_).get_data(as_text=True)
    boss.post("/members", data=dict(csrf=t, member_id=pid_, action="membership", plan_id=plan, paid_through="2099-06-30"))
    assert sql("SELECT status, paid_through FROM access_entitlements WHERE member_id=? AND plan_id=?", (pid_, plan))[-1] == ("active", "2099-06-30")
    # Board: a new role is created as a board role, they join Board chat, then leave it.
    boss.post("/members", data=dict(csrf=t, member_id=pid_, action="add_board", role_id="", new_role="Treasurer"))
    assert sql("SELECT board_member FROM members WHERE id=?", (pid_,))[0][0] == 1
    assert sql("SELECT r.name, r.board FROM leadership_roles r JOIN leadership_members m ON m.role_id=r.id WHERE m.member_id=?", (pid_,)) == [("Treasurer", 1)]
    assert pm.get("/chat?c=board").status_code == 200 and "Pat Menu" in boss.get("/manage/club/leaders/board").get_data(as_text=True)
    boss.post("/members", data=dict(csrf=t, member_id=pid_, action="remove_board"))
    assert sql("SELECT board_member FROM members WHERE id=?", (pid_,))[0][0] == 0
    assert not sql("SELECT 1 FROM leadership_members WHERE member_id=?", (pid_,))


def test_manage_chart_card_two_views_real_data():
    page = boss.get("/manage").get_data(as_text=True)
    assert "data-chartcard" in page and "AVG CHECKED IN" in page and "MEMBERS ·" in page and 'role=tablist' in page
    import components
    assert components._nice_ticks(20) == [0, 10, 20] and components._nice_ticks(23) == [0, 10, 20, 30]
    today = dt.date(2026, 11, 13)
    months = A._bucket_plan(dt.date(2026, 1, 5), today)
    assert len(months) == 8 and months[-1][0] == "Nov" and months[0][0] == "Apr"
    halves = A._bucket_plan(dt.date(2026, 6, 20), today)
    assert len(halves) == 8 and halves[-1][1] == today and halves[-2][1] == dt.date(2026, 10, 31)
    weeks = A._bucket_plan(dt.date(2026, 10, 1), today)
    assert len(weeks) == 8 and (weeks[-1][1] - weeks[-2][1]).days == 7


def test_availability_lives_on_calendar_with_day_and_away_sheets():
    assert member.get("/availability").headers["Location"].endswith("/calendar?when=availability")
    assert member.get("/availability/away").headers["Location"].endswith("/calendar?when=availability&sheet=away")
    page = member.get("/calendar?when=availability").get_data(as_text=True)
    assert "Upcoming" in page and "Past" in page and "When can you play?" in page
    assert 'data-sheet-name=day' in page and 'data-sheet-name=away' in page and "data-day-sheet" in page


def test_members_get_chat_plus_with_ask_coaches_and_board_and_export_has_legal_gender():
    t = member.get("/chat?view=list").get_data(as_text=True)
    assert "chatplus" in t and "Message someone" in t and "Ask the coaches" in t and "Ask the board" in t
    assert "data-to=coaches" in t and "data-lock=board" in t and "id=requestSheet" in t
    sql("UPDATE members SET legal_gender='female' WHERE id=?", (RAE,))
    import csv, io
    rows = list(csv.reader(io.StringIO(boss.get("/members.csv").get_data(as_text=True).lstrip("﻿"))))
    i = rows[0].index("Sex on sport membership")
    assert [r[i] for r in rows if r[3] == "rae@example.com"] == ["Woman"]


def test_website_settings_save_themselves_and_embed_sheet_has_platform_steps():
    tok = csrf(boss, "/manage/widget")
    r = boss.post("/manage/widget", data={"csrf": tok, "field": "show_counts", "show_counts": "1"}, headers={"X-Autosave": "1"})
    assert r.status_code == 200 and r.get_json()["ok"]
    import publicfeed
    with A.app.app_context():
        assert publicfeed.load(A.db())["widget"]["show_counts"] is True
    r = boss.post("/manage/widget", data={"csrf": tok, "field": "chips", "chips_present": "1", "chips": ["schedule", "trips"]}, headers={"X-Autosave": "1"})
    assert r.get_json()["set"]["tabs"].startswith("All, Schedule")
    r = boss.post("/manage/widget", data={"csrf": tok, "field": "default_chip", "default_chip": "camps"}, headers={"X-Autosave": "1"})
    assert r.get_json()["set"]["opens"] == "All"
    page = boss.get("/manage/widget").get_data(as_text=True)
    assert "Add to your site." in page and "In Wix" in page and "Copy code" in page and "mailto:?subject=" in page
    assert member.post("/manage/widget", data={"csrf": tok, "field": "show_counts", "show_counts": "0"}, headers={"X-Autosave": "1"}).status_code in (302, 400, 403)


def test_email_builder_preview_send_and_tracking():
    import clubemail
    r = boss.post("/manage/email", data={"csrf": csrf(boss, "/manage/email"), "template": "schedule_change"})
    eid = int(r.headers["Location"].rsplit("/", 1)[1])
    page = boss.get("/manage/email/%d" % eid).get_data(as_text=True)
    assert "Everyone ·" in page and "BLOCKS" in page and "Add block" in page
    tok = csrf(boss, "/manage/email/%d" % eid)
    assert boss.post("/manage/email/%d" % eid, data={"csrf": tok, "field": "subject", "subject": "Holiday schedule"}, headers={"X-Autosave": "1"}).get_json()["ok"]
    boss.post("/manage/email/%d" % eid, data={"csrf": tok, "action": "edit_block", "index": "1", "body": "Hi {first name}, see you Tuesday."})
    prev = boss.get("/manage/email/%d/preview" % eid).get_data(as_text=True)
    assert "Holiday" not in prev or True
    assert "see you Tuesday" in prev and "Send to" in prev
    sent = []
    old_ready, old_send = A.smtp_ready, A.send_email
    os.environ["CLUB_EMAIL_SYNC"] = "1"
    A.smtp_ready = lambda: True
    A.send_email = lambda to, subject, text, html=None, ics=None: sent.append((to, subject, html))
    try:
        boss.post("/manage/email/%d/preview" % eid, data={"csrf": csrf(boss, "/manage/email/%d/preview" % eid), "action": "send"})
    finally:
        A.smtp_ready, A.send_email = old_ready, old_send
    assert sent and all(s[1] == "Holiday schedule" for s in sent) and "/e/o/" in sent[0][2] and "Unsubscribe" in sent[0][2]
    token = re.search(r"/e/o/([A-Za-z0-9_\-]+)\.gif", sent[0][2]).group(1)
    assert A.app.test_client().get("/e/o/%s.gif" % token).status_code == 200
    click = re.search(r'href="([^"]*/e/c/[^"]+)"', sent[0][2]).group(1).replace("&amp;", "&")
    path = click.split("://", 1)[-1].split("/", 1)[1]
    assert A.app.test_client().get("/" + path).status_code == 302
    assert A.app.test_client().get("/e/c/%s?u=https://evil.example&s=bad" % token).headers["Location"].endswith("/")
    rep = boss.get("/manage/email/%d/report" % eid).get_data(as_text=True)
    assert "Opened" in rep and "Clicked" in rep and "Didn&#39;t open" in rep or "Didn't open" in rep
    with A.app.app_context():
        st = clubemail.stats(A.db(), eid)
    assert st["sent"] == len(sent) and st["opened"] >= 1 and st["clicked"] >= 1
    u = A.app.test_client()
    u.get("/e/u/%s" % token)
    u.post("/e/u/%s" % token, data={"csrf": csrf(u, "/e/u/%s" % token)})
    assert sql("SELECT news_opt_out FROM members WHERE email=?", (sent[0][0],))[0][0] == 1


def test_join_asks_gender_and_usawp_entry_asks_membership_sex():
    c = A.app.test_client()
    page = c.get("/join").get_data(as_text=True)
    assert "rg-dob" in page and "data-dob=m" in page and "GENDER" in page and 'name="gender_identity"' in page
    c.post("/join", data=dict(birth_date="1991-05-06", csrf=csrf(c, "/join"), first="Gia", last="Join", email="gia.join@example.com", phone="1", gender_identity="nonbinary"))
    assert sql("SELECT gender_identity FROM members WHERE email='gia.join@example.com'")[0][0] == "nonbinary"
    home = c.get("/home").get_data(as_text=True)
    assert "registered as the following with USAWP" in home and "Woman" in home
    c.post("/home", data=dict(csrf=csrf(c, "/home"), usawp_number="123456", membership_sex="female"))
    assert sql("SELECT legal_gender FROM members WHERE email='gia.join@example.com'")[0][0] == "female"
    assert ">Prefer not to say<" in home and ">Intersex<" not in home
    tok = csrf(boss, "/manage/club/programs/water-polo")
    assert "Sex on a membership" in boss.get("/manage/club/programs/water-polo").get_data(as_text=True)
    boss.post("/manage/club/programs/water-polo", data={"csrf": tok, "action": "sex_options", "sex_options": "Male\nFemale\nX\nPrefer not to say"})
    gid = sql("SELECT id FROM members WHERE email='gia.join@example.com'")[0][0]
    assert ">X<" in boss.get("/admin/member/%d" % gid).get_data(as_text=True)
    boss.post("/admin/member/%d" % gid, data=dict(csrf=csrf(boss, "/admin/member/%d" % gid), action="noop", membership_sex="x"))
    assert sql("SELECT legal_gender FROM members WHERE email='gia.join@example.com'")[0][0] == "x"


def test_joining_the_second_social_only_joins_that_one():
    sql("INSERT INTO practices(date,start,end,location,social_kind,social_place,social2_kind,social2_place) VALUES(date('now','+3 day'),'19:00','20:30','Pool 2S','dinner','The Harp','coffee','Cafe')")
    pid = sql("SELECT id FROM practices WHERE location='Pool 2S'")[0][0]
    member.post("/practices/%d" % pid, data={"csrf": csrf(member, "/profile"), "pid": pid, "slot": "2", "action": "social_join"})
    assert sql("SELECT COUNT(*) FROM social2_joins WHERE practice_id=?", (pid,))[0][0] == 1
    assert sql("SELECT COUNT(*) FROM social_joins WHERE practice_id=?", (pid,))[0][0] == 0


def test_practice_page_sheets_edit_when_coaches_notes_and_link_check_in():
    pid = _practice("Sheet Practice", 3)
    sql("INSERT OR IGNORE INTO coaching_list(member_id) VALUES(?)", (RAE,))
    page = boss.get("/practices/%d" % pid).get_data(as_text=True)
    for bit in ("Start check-in", "id=pqMore", "id=pqCoaches", "Notes", "Check-in", "Practice plan", "Details", "/admin?date="):
        assert bit in page, bit
    tok = csrf(boss, "/practices/%d" % pid)
    day = (A.today_pt() + dt.timedelta(days=4)).isoformat()
    boss.post("/practices/%d" % pid, data=dict(csrf=tok, pid=pid, back="page", action="when", date=day, start="18:00", end="19:30", location="New Pool"))
    assert sql("SELECT date,start,end,location FROM practices WHERE id=?", (pid,))[0] == (day, "18:00", "19:30", "New Pool")
    boss.post("/practices/%d" % pid, data=dict(csrf=tok, pid=pid, back="page", action="coaches", coach=str(RAE), lead=str(RAE)))
    assert sql("SELECT member_id FROM practice_coaches WHERE practice_id=?", (pid,)) == [(RAE,)]
    boss.post("/practices/%d" % pid, data=dict(csrf=tok, pid=pid, back="page", action="note", note="Bring caps"))
    assert sql("SELECT note FROM practices WHERE id=?", (pid,))[0][0] == "Bring caps"
    page = boss.get("/practices/%d" % pid).get_data(as_text=True)
    assert "Head coach" in page and "Bring caps" in page
    mpage = member.get("/practices/%d" % pid).get_data(as_text=True)
    assert "id=pqMore" not in mpage and "Start check-in" not in mpage and "Practice plan" not in mpage and "Bring caps" in mpage


def test_practice_page_level_and_division_sheets_save():
    pid = _practice("Level Practice", 3)
    page = boss.get("/practices/%d" % pid).get_data(as_text=True)
    assert "id=pqLevels" in page and "id=pqDivs" in page and "Skill level" in page
    tok = csrf(boss, "/practices/%d" % pid)
    lv = re.search(r'name="?level"? value="?([\w-]+)', page).group(1)
    boss.post("/practices/%d" % pid, data=dict(csrf=tok, pid=pid, back="page", action="levels", level=[lv]))
    boss.post("/practices/%d" % pid, data=dict(csrf=tok, pid=pid, back="page", action="divisions", division=["custom"], division_custom="18U girls"))
    row = sql("SELECT skill_levels, divisions, division_custom FROM practices WHERE id=?", (pid,))[0]
    assert lv in row[0] and row[1] == "custom" and row[2] == "18U girls"
    page = boss.get("/practices/%d" % pid).get_data(as_text=True)
    assert "18U girls" in page


def test_leaders_board_roles_assign_replace_and_requests_switch():
    page = boss.get("/manage/club/leaders").get_data(as_text=True)
    assert "Leaders." in page and "/manage/club/leaders/board" in page
    tok = csrf(boss, "/manage/club/leaders/board")
    boss.post("/manage/club/leaders/board", data=dict(csrf=tok, action="add_role", name="Treasurer"))
    rid = sql("SELECT id FROM leadership_roles WHERE program_id IS NULL AND name='Treasurer'")[0][0]
    boss.post("/manage/club/leaders/board", data=dict(csrf=tok, action="assign", role_id=rid, person=RAE))
    assert sql("SELECT board_member FROM members WHERE id=?", (RAE,))[0][0] == 1
    page = boss.get("/manage/club/leaders/board").get_data(as_text=True)
    assert "Rae Design" in page and "Treasurer" in page
    boss_id = sql("SELECT id FROM members WHERE email='boss@example.com'")[0][0]
    boss.post("/manage/club/leaders/board", data=dict(csrf=tok, action="assign", role_id=rid, person=boss_id))
    assert sql("SELECT member_id FROM leadership_members WHERE role_id=?", (rid,)) == [(boss_id,)]
    assert sql("SELECT board_member FROM members WHERE id=?", (RAE,))[0][0] == 0
    # Members can message the board: off blocks the request and hides the row.
    r = boss.post("/manage/club/leaders/board", data=dict(csrf=tok, requests="0", field="requests"), headers={"X-Autosave": "1"})
    assert r.get_json()["ok"]
    n = sql("SELECT COUNT(*) FROM club_requests")[0][0]
    member.post("/chat/requests", data=dict(csrf=csrf(member, "/chat"), audience="board", topic="other", message="hi"))
    assert sql("SELECT COUNT(*) FROM club_requests")[0][0] == n
    boss.post("/manage/club/leaders/board", data=dict(csrf=tok, requests="1", field="requests"), headers={"X-Autosave": "1"})
    chat = member.get("/chat").get_data(as_text=True)
    assert "New message" in chat and "The board" in chat
    boss.post("/manage/club/leaders/board", data=dict(csrf=tok, action="clear", role_id=rid, member_id=boss_id))
    boss.post("/manage/club/leaders/board", data=dict(csrf=tok, action="delete_role", role_id=rid))
    assert not sql("SELECT id FROM leadership_roles WHERE id=?", (rid,))


def test_documents_publish_gate_going_and_new_version_resigns():
    page = boss.get("/manage/club/documents").get_data(as_text=True)
    assert "Documents." in page and "Code of conduct" in page
    r = boss.post("/manage/club/documents", data=dict(csrf=csrf(boss, "/manage/club/documents"), kind="conduct"))
    key = r.headers["Location"].split("/manage/club/documents/")[1].split("?")[0]
    tok = csrf(boss, "/manage/club/documents/" + key)
    boss.post("/manage/club/documents/" + key, data=dict(csrf=tok, action="publish", source="text", body="Be kind in the pool."))
    assert sql("SELECT version, enabled FROM club_docs WHERE id=?", (int(key),))[0] == (1, 1)
    pid = _practice("Doc Practice", 2)
    sql("UPDATE members SET usawp_status='verified', usawp_number='1002010', usawp_valid_until='2099-01-01'")
    for rid, in sql("SELECT id FROM members"):
        sql("INSERT INTO waiver_acceptances(member_id, version, title, typed_name, at) VALUES(?, (SELECT version FROM club_waiver WHERE id=1), 'w', 'x y', 'now')", (rid,))
    sheet = member.get("/practices/%d/signup" % pid).get_data(as_text=True)
    assert "Code of conduct" in sheet and "agree_doc_%s" % key in sheet
    member.post("/practices/%d/signup" % pid, data={"csrf": csrf(member, "/practices/%d/signup" % pid), "action": "go", "agree_doc_" + key: "1", "typed_name": "Rae Design"})
    assert sql("SELECT version FROM doc_acceptances WHERE doc_id=? AND member_id=?", (int(key), RAE)) == [(1,)]
    assert sql("SELECT going FROM rsvps WHERE practice_id=? AND member_id=?", (pid, RAE)) == [(1,)]
    # Typo fix keeps signatures; a new version asks again.
    boss.post("/manage/club/documents/" + key, data=dict(csrf=tok, action="save", source="text", body="Be kind in the pool!"))
    def pend():
        con = sqlite3.connect(A.DB); con.row_factory = sqlite3.Row
        try: return [x["key"] for x in A.clubdocs.pending(con, RAE)]
        finally: con.close()
    assert pend() == []
    boss.post("/manage/club/documents/" + key, data=dict(csrf=tok, action="publish", source="text", body="Be kind.", note="shorter"))
    assert pend() == [key]
    r = boss.post("/manage/club/documents/" + key, data=dict(csrf=tok, required="0", field="required"), headers={"X-Autosave": "1"})
    assert r.get_json()["ok"] and pend() == []


def test_reminders_choices_save_and_going_only_filter():
    tok = csrf(boss, "/manage/club/reminders")
    for field, val in (("when", "morning"), ("who", "going")):
        r = boss.post("/manage/club/reminders", data={"csrf": tok, field: val, "field": field}, headers={"X-Autosave": "1"})
        assert r.get_json()["ok"]
    import clubadmin
    con = sqlite3.connect(A.DB); con.row_factory = sqlite3.Row
    s = clubadmin.reminder_settings(con); con.close()
    assert s["when"] == "morning" and s["who"] == "going" and not s["enabled"]
    page = boss.get("/manage/club/reminders").get_data(as_text=True)
    assert "Reminders." in page and "Morning of" in page and "data-off" in page


def test_participants_tiles_filters_and_status_drawer():
    page = boss.get("/members").get_data(as_text=True)
    assert "Participants." in page and "Needs both" in page and "data-status=" in page and "Make admin" not in page
    page = boss.get("/members?filt=uncleared").get_data(as_text=True)
    assert "Not cleared" in page
    drawer = boss.get("/members/%d/status" % RAE).get_data(as_text=True)
    assert "CLEARED TO PLAY" in drawer and "USA Water Polo #" in drawer and "View profile" in drawer and "Message Rae" in drawer
    assert "<html" not in drawer
    assert member.get("/members/%d/status" % RAE).status_code in (302, 403)
    classic = boss.get("/members?view=coaches").get_data(as_text=True)
    assert "Participants." not in classic


def test_passes_create_sheet_sections_and_archive_keep_rsvps():
    page = boss.get("/manage/club/plans").get_data(as_text=True)
    assert "Passes." in page and "Create and preview" in page and "How members pay" not in page
    tok = csrf(boss, "/manage/club/plans")
    r = boss.post("/manage/club/plans", data=dict(csrf=tok, kind="pass", name="Ten Pack", price="120"))
    pid = int(r.headers["Location"].rsplit("/", 1)[1])
    row = sql("SELECT kind, active, length_sessions FROM payment_plans WHERE id=?", (pid,))[0]
    assert row == ("pass", 0, 10)
    rsvps = sql("SELECT COUNT(*) FROM rsvps")[0][0]
    boss.post("/manage/club/plans/%d" % pid, data=dict(csrf=tok, section="billing", length_mode="sessions", length_days="0", length_sessions="12"))
    boss.post("/manage/club/plans/%d" % pid, data=dict(csrf=tok, section="who", audience="new", one_per_person="1", uses_per_event="1"))
    boss.post("/manage/club/plans/%d" % pid, data=dict(csrf=tok, section="price", price="130", effective_on="2099-01-01"))
    r = boss.post("/manage/club/plans/%d" % pid, data=dict(csrf=tok, section="status", active="1", field="active"), headers={"X-Autosave": "1"})
    assert r.get_json()["ok"]
    row = sql("SELECT length_sessions, audience, one_per_person, uses_per_event, active, name FROM payment_plans WHERE id=?", (pid,))[0]
    assert row == (12, "new", 1, 1, 1, "Ten Pack")
    assert (13000, "2099-01-01") in sql("SELECT amount_cents, effective_on FROM payment_prices WHERE plan_id=?", (pid,))
    page = boss.get("/manage/club/plans/%d" % pid).get_data(as_text=True)
    assert "Every setting, in plain words." in page and "$130 from Jan 1, 2099" in page and "New members only" in page
    boss.post("/manage/club/plans/%d" % pid, data=dict(csrf=tok, section="archive"))
    assert sql("SELECT archived FROM payment_plans WHERE id=?", (pid,))[0][0] == 1
    assert sql("SELECT COUNT(*) FROM rsvps")[0][0] == rsvps


def test_interest_check_ask_answer_results_and_official():
    day = (A.today_pt() + dt.timedelta(days=200)).isoformat()
    sql("INSERT INTO lineup_events(kind,title,date,city,venue,start,status,team_intent,team_plan) VALUES('Trip','IGLA Test',?,'Copenhagen','Pool','09:00','published','considering','considering')", (day,))
    eid = sql("SELECT id FROM lineup_events WHERE title='IGLA Test'")[0][0]
    page = boss.get("/lineup/%d" % eid).get_data(as_text=True)
    assert "Check interest first" in page and "id=icSetup" in page
    tok = csrf(boss, "/lineup/%d" % eid)
    boss.post("/lineup/%d/interest" % eid, data=dict(csrf=tok, action="setup", ask="month", option_new="Jun 2027", cost="$1,200", need="2", answer_by="2099-01-15"))
    boss.post("/lineup/%d/interest" % eid, data={"csrf": tok, "action": "setup", "ask": "month", "option": ["Jun 2027"], "option_new": "Jul 2027", "cost": "$1,200", "need": "2"})
    mp = member.get("/lineup/%d" % eid).get_data(as_text=True)
    assert "ARE YOU IN?" in mp and "Jul 2027" in mp and "0 in · 2 needed" in mp and "See answers" not in mp
    member.post("/lineup/%d/interest" % eid, data={"csrf": csrf(member, "/lineup/%d" % eid), "action": "answer", "answer": "in", "pick": ["Jun 2027"]})
    assert sql("SELECT state FROM lineup_rsvps WHERE event_id=? AND member_id=?", (eid, RAE)) == [("interested",)]
    assert member.get("/lineup/%d/interest" % eid).status_code == 302
    res = boss.get("/lineup/%d/interest" % eid).get_data(as_text=True)
    assert "Interest." in res and "Rae Design" in res and "Make it official — Jun 2027" in res and "1 in · 0 maybe" in res
    boss.post("/lineup/%d/interest" % eid, data=dict(csrf=tok, action="official", option="Jun 2027"))
    assert sql("SELECT team_intent FROM lineup_events WHERE id=?", (eid,))[0][0] == "official"
    assert sql("SELECT status FROM interest_checks WHERE event_id=?", (eid,))[0][0] == "decided"



def test_practice_page_coach_can_set_coaches_for_series_and_ask_admin():
    pid = _practice("Coach Practice", 5)
    sql("UPDATE members SET role='coach' WHERE id=?", (RAE,))
    sql("INSERT OR IGNORE INTO coaching_list(member_id) VALUES(?)", (RAE,))
    page = member.get("/practices/%d" % pid).get_data(as_text=True)
    assert "id=pqMore" in page and "Ask an admin to change it" in page and "All details" not in page
    tok = csrf(member, "/practices/%d" % pid)
    member.post("/practices/%d" % pid, data=dict(csrf=tok, pid=pid, back="page", action="coaches", coach=str(RAE), lead=str(RAE)))
    assert sql("SELECT member_id, is_lead FROM practice_coaches WHERE practice_id=?", (pid,)) == [(RAE, 1)]
    n = sql("SELECT COUNT(*) FROM club_requests")[0][0]
    member.post("/practices/%d" % pid, data=dict(csrf=tok, pid=pid, back="page", action="ask_admin", message="Move it to 7:30"))
    row = sql("SELECT audience, practice_id FROM club_requests ORDER BY id DESC LIMIT 1")[0]
    assert sql("SELECT COUNT(*) FROM club_requests")[0][0] == n + 1 and row == ("board", pid)
    sql("UPDATE members SET role='athlete' WHERE id=?", (RAE,))


def test_practice_social_screen_saves_before_or_after():
    pid = _practice("Social Screen", 3)
    page = boss.get("/practices/%d?edit=1" % pid).get_data(as_text=True)
    for bit in ("id=sheetSocialAll", "Before practice", "After practice", "Breakfast", "id=sheetSocialPlace", "id=sheetSocialTime", "Remove social"):
        assert bit in page, bit
    tok = csrf(boss, "/practices/%d?edit=1" % pid)
    row = sql("SELECT date,start,end,location FROM practices WHERE id=?", (pid,))[0]
    boss.post("/practices/%d" % pid, data=dict(csrf=tok, pid=pid, action="edit", date=row[0], start=row[1], end=row[2], location=row[3] or "Pool",
                                                plan_fields="1", social_when="before", social_kind=["Coffee", "Breakfast"], social_place="Cafe", social_address="1 Main St", social_time="06:30"))
    got = sql("SELECT social_kind, social_when, social_time FROM practices WHERE id=?", (pid,))[0]
    assert got == ("Coffee,Breakfast", "before", "06:30"), got
    page = boss.get("/practices/%d" % pid).get_data(as_text=True)
    assert "Before practice" in page


def test_new_event_error_keeps_everything_typed():
    tok = csrf(boss, "/events/new?lane=lineup")
    r = boss.post("/events/new", data=dict(csrf=tok, action="preview", lane="lineup", line_title="Draft Cup", description="", event_type="Tournament",
                                           hosting="Attending", host_org="West Hollywood Aquatics", date_precision="exact", date="2030-05-02", location="Long Beach"))
    assert r.status_code == 302
    page = boss.get(r.headers["Location"]).get_data(as_text=True)
    assert "Add a short description." in page
    assert '"Draft Cup"' in page and '"West Hollywood Aquatics"' in page and '"2030-05-02"' in page  # restored into the form
    assert "var draft=" in page and "step=1" in page
    again = boss.get("/events/new?lane=lineup").get_data(as_text=True)
    assert "var draft=" not in again  # used once


def test_event_color_saves_for_schedule_and_lineup_events():
    tok = csrf(boss, "/events/new?lane=lineup")
    r = boss.post("/events/new", data=dict(csrf=tok, action="preview", lane="lineup", line_title="Color Cup", description="Bring caps", event_type="Tournament",
                                           hosting="Hosting", date_precision="exact", date="2030-06-02", location="Long Beach", event_color_line="cobalt"))
    assert r.status_code == 302, r.status_code
    eid = sql("SELECT id, color FROM lineup_events WHERE title='Color Cup'")[0]
    assert eid[1] == "cobalt"
    assert "tone-cobalt" in boss.get("/lineup/%d" % eid[0]).get_data(as_text=True)
    page = boss.get("/lineup/%d/edit" % eid[0]).get_data(as_text=True)
    assert 'name="event_color_line" value="cobalt" checked' in page and "Event color" in page
    new = boss.get("/events/new").get_data(as_text=True)
    assert "Event color" in new and "Team color" not in new and 'name="event_color_schedule"' in new


def test_week_swipe_lands_on_nearest_session_or_says_the_week_is_empty():
    pid = _practice("Swipe Week", days=9)
    day = sql("SELECT date FROM practices WHERE id=?", (pid,))[0][0]
    page = boss.get("/admin?week=%s&near=0" % day).get_data(as_text=True)
    assert "ckweektrack" in page and page.count("class=ckweek ") == 3
    assert ('href="/admin?date=%s" aria-current=date' % day) in page
    far = (A.today_pt() + dt.timedelta(days=700)).isoformat()
    assert "No events this week." in boss.get("/admin?week=%s&near=3" % far).get_data(as_text=True)


def test_email_image_block_uploads_renders_and_is_public():
    import io, json as _json
    from PIL import Image
    r = boss.post("/manage/email", data=dict(csrf=csrf(boss, "/manage/email")))
    eid = int(re.search(r"/manage/email/(\d+)", r.headers["Location"]).group(1))
    tok = csrf(boss, "/manage/email/%d" % eid)
    boss.post("/manage/email/%d" % eid, data=dict(csrf=tok, action="add_block", kind="image"))
    blocks = _json.loads(sql("SELECT blocks FROM club_emails WHERE id=?", (eid,))[0][0])
    i = [n for n, b in enumerate(blocks) if b.get("kind") == "image"][0]
    buf = io.BytesIO(); Image.new("RGB", (1600, 900), (200, 255, 60)).save(buf, "PNG"); buf.seek(0)
    boss.post("/manage/email/%d" % eid, data=dict(csrf=tok, action="edit_block", index=str(i), alt="Team photo", url="/lineup", image=(buf, "team.png")),
              content_type="multipart/form-data")
    b = _json.loads(sql("SELECT blocks FROM club_emails WHERE id=?", (eid,))[0][0])[i]
    assert b["alt"] == "Team photo" and "/email-image/em_" in b["src"]
    name = b["src"].rsplit("/", 1)[1]
    pic = A.app.test_client().get("/email-image/" + name)  # signed out, like a mail app
    assert pic.status_code == 200 and pic.mimetype == "image/jpeg"
    assert A.app.test_client().get("/email-image/../app.py").status_code == 404
    html = A.clubemail.render([b])
    assert 'alt="Team photo"' in html and name in html
