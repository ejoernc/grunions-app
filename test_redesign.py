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
    html = member.get("/profile").get_data(as_text=True)
    assert "Appearance" in html and 'data-theme="dark"' in html
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
    assert "Offering from Fountain Valley" in driver.get("/profile").get_data(as_text=True)


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
