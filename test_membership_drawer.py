"""Going drawer: membership fees start Dec 1. Shown to people without a membership, once; never blocks Going."""
import os
import re
import tempfile

os.environ["GRUNIONS_DB"] = tempfile.mktemp(suffix=".db")
os.environ["ADMIN_EMAIL"] = "memadmin@example.com"
os.environ["GRUNIONS_SCHEDULER"] = "0"
os.environ["GRUNIONS_SHEET_SYNC"] = "0"
os.environ["DEV_SHOW_LINKS"] = "1"

import app as A
import sportspay


def _setup():
    with A.app.app_context():
        d = A.db()
        sportspay.ensure_schema(d)
        d.execute("INSERT INTO members(first, last, email, role, joined) VALUES('Pia','Player','pia@example.com','athlete',1)")
        d.execute("INSERT INTO members(first, last, email, role, joined) VALUES('Mo','Member','mo@example.com','athlete',1)")
        d.execute("INSERT INTO practices(date, start, sport, cancelled) VALUES('2099-01-05','19:00','Water Polo',0)")
        pid = d.execute("SELECT MAX(id) FROM practices").fetchone()[0]
        ids = {r["email"]: r["id"] for r in d.execute("SELECT id, email FROM members")}
        plan = A._membership_plan(d, d.execute("SELECT * FROM practices WHERE id=?", (pid,)).fetchone())
        assert plan is not None, "seeded monthly plan with a Club Assistant link"
        sportspay.save_entitlement(d, ids["mo@example.com"], None, plan["id"], "active", "2026-01-01", "", "test")
        d.commit()
        return pid, ids, plan


PID, IDS, PLAN = _setup()


def _as(mid):
    c = A.app.test_client()
    with c.session_transaction() as s:
        s["mid"] = mid
    return c


def _csrf(c):
    return re.search(r'name=csrf value="([^"]+)"', c.get("/notifications").get_data(as_text=True)).group(1)


def test_drawer_shows_monthly_link_only_for_people_without_membership_and_only_once():
    pia = _as(IDS["pia@example.com"])
    j = pia.get("/api/membership/prompt?pid=%d" % PID).get_json()
    assert j["show"] and j["url"] == PLAN["external_url"] and j["start"] == "December 1, 2026"
    assert "/mo" in j["price"]
    assert _as(IDS["mo@example.com"]).get("/api/membership/prompt?pid=%d" % PID).get_json()["show"] is False
    r = pia.post("/membership/ack", data={"csrf": _csrf(pia), "action": "registered", "pid": PID})
    assert r.status_code == 200
    assert pia.get("/api/membership/prompt?pid=%d" % PID).get_json()["show"] is False
    with A.app.app_context():
        d = A.db()
        row = d.execute("SELECT note, status FROM payment_checks WHERE member_id=?", (IDS["pia@example.com"],)).fetchone()
        assert row and row["status"] == "pending" and "already registered" in row["note"]


def test_going_is_never_blocked_by_the_drawer():
    """The drawer is a nudge in the page. The server never turns Going into a payment step for it."""
    pia = _as(IDS["pia@example.com"])
    r = pia.post("/practices/%d" % PID, data={"csrf": _csrf(pia), "pid": PID, "action": "going"})
    assert r.status_code in (200, 302)
    assert "/participate" not in (r.headers.get("Location") or "")
    with A.app.app_context():
        assert not sportspay.require_rsvp(A.db())  # the hard payment gate stays off


def test_coaches_pass_follows_the_coach_switch_and_isnt_a_mark_paid_choice():
    import clubadmin
    with A.app.app_context():
        d = A.db()
        clubadmin.ensure(d)
        prog = d.execute("SELECT id, slug FROM programs WHERE slug='water-polo'").fetchone()
        if not prog:
            d.execute("INSERT INTO programs(slug, name, active) VALUES('water-polo','Water Polo',1)")
            prog = d.execute("SELECT id, slug FROM programs WHERE slug='water-polo'").fetchone()
        pid = d.execute("""INSERT INTO payment_plans(name, kind, active, audience, sports, activities)
            VALUES('Coaches Pass','monthly',1,'coaches','water-polo','')""").lastrowid
        d.execute("INSERT OR IGNORE INTO plan_programs(plan_id, program_id) VALUES(?,?)", (pid, prog["id"]))
        d.execute("INSERT INTO members(first, last, email, role, joined) VALUES('Cy','Coach','cy@example.com','coach',1)")
        cy = d.execute("SELECT id FROM members WHERE email='cy@example.com'").fetchone()[0]
        # Even a coaches pass marked by hand stops counting when Coach is turned off.
        sportspay.save_entitlement(d, cy, None, pid, "active", "2026-01-01", "", "given by hand")
        d.commit()
        today = A.today_pt().isoformat()
        assert clubadmin.has_monthly_membership(d, cy, today)
        assert clubadmin.payment_view(d, cy, today)["label"] == "Paid"
        d.execute("UPDATE members SET role='athlete' WHERE id=?", (cy,)); d.commit()
        assert not clubadmin.has_monthly_membership(d, cy, today)
        assert clubadmin.payment_view(d, cy, today)["label"] == "Unpaid"
        d.execute("UPDATE members SET role='coach' WHERE id=?", (cy,)); d.commit()
        assert clubadmin.has_monthly_membership(d, cy, today)  # back on: the pass applies again, nothing to pick
        names = [p["name"] for p in A._people_sheets(d)["member_plans"]]
        assert "Coaches Pass" not in names
