"""Sample practices and one tournament for a local preview database.

Refuses to run unless GRUNIONS_DEMO_SEED=1. A deploy never loads these rows.

    GRUNIONS_DEMO_SEED=1 GRUNIONS_DB=/tmp/grunions-sports-demo.db \\
        .venv/bin/python seed_sports_demo.py
"""
import os, sys, datetime as dt

if os.environ.get("GRUNIONS_DEMO_SEED") != "1":
    sys.exit("Refusing to seed. Set GRUNIONS_DEMO_SEED=1 and point GRUNIONS_DB at a local or preview database.")

os.environ.setdefault("GRUNIONS_SHEET_SYNC", "0")
os.environ.setdefault("ADMIN_EMAIL", "eli@example.com")
import app as A
import sports

def put(d, **kw):
    sp = {
        "activity_type": kw.get("activity_type") or "practice",
        "sport": "Water Polo",
        "title": kw.get("title") or "",
        "skill_levels": kw.get("skill_levels") or "",
        "divisions": kw.get("divisions") or "",
        "division_custom": kw.get("division_custom") or "",
        "opponent": kw.get("opponent") or "",
        "home_away": kw.get("home_away") or "",
        "gameplay_notes": kw.get("gameplay_notes") or "",
        "segments": kw.get("segments") or "",
        "comp_format": kw.get("comp_format") or "",
    }
    d.execute("""INSERT INTO practices(date,start,end,location,note,activity_type,sport,title,skill_levels,divisions,division_custom,opponent,home_away,gameplay_notes,segments,comp_format)
        VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
        (kw["date"], kw.get("start") or "19:00", kw.get("end") or "20:30", kw["location"], kw.get("note") or "", *sports.sports_tuple(sp)))

def main():
    d = A.open_db()
    today = A.today_pt()
    def day(n): return (today + dt.timedelta(days=n)).isoformat()
    put(d, date=day(2), location="All Levels Pool", skill_levels="beginner,developing,intermediate,experienced", divisions="open", note="Everyone is welcome.")
    put(d, date=day(3), start="18:00", end="19:15", location="Learn the Eggbeater Pool", skill_levels="beginner,intermediate")
    put(d, date=day(4), start="20:00", end="21:00", location="Experienced Training Pool", skill_levels="experienced", activity_type="practice")
    put(d, date=day(6), location="Internal Scrimmage Pool", activity_type="scrimmage", gameplay_notes="Even teams. Work the counterattack.")
    put(d, date=day(8), start="18:00", end="19:30", location="Home Game Pool", activity_type="game", opponent="Squid", home_away="home")
    put(d, date=day(9), location="Hybrid Pool", activity_type="hybrid",
        segments='[{"type":"practice","start":"19:00","end":"19:45"},{"type":"scrimmage","start":"19:45","end":"20:30"}]')
    # Recurring practice, then one date becomes a scrimmage.
    start = today + dt.timedelta(days=14)
    end = start + dt.timedelta(days=14)
    sid = d.execute("""INSERT INTO practice_series(weekdays,start,end,location,start_date,end_date,activity_type,sport)
        VALUES(?,?,?,?,?,?,?,?)""", (str(start.weekday()), "18:00", "19:00", "Tuesday Series Pool", start.isoformat(), end.isoformat(), "practice", "Water Polo")).lastrowid
    A.sync_series(d, sid)
    one = d.execute("SELECT id FROM practices WHERE series_id=? ORDER BY date LIMIT 1", (sid,)).fetchone()
    if one:
        d.execute("UPDATE practices SET activity_type='scrimmage', series_detached=1 WHERE id=?", (one["id"],))
    cat = d.execute("SELECT id FROM lineup_categories WHERE slug='learn'").fetchone()
    travel = d.execute("SELECT id FROM lineup_categories WHERE slug='travel'").fetchone()
    eli = d.execute("SELECT id FROM members WHERE email='eli@example.com'").fetchone()
    if cat and eli:
        d.execute("""INSERT INTO lineup_events(category_id, subtype, title, date, end_date, start_time, end_time, city, venue, description, hosting, kind, stage, official, status, created_by, sport, skill_levels, divisions)
            VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
            (cat["id"], "Clinic", "Developing clinic", day(11), day(11), "10:00", "12:00", "Huntington Beach", "Clinic Pool",
             "A clinic for players who know the fundamentals.", "Hosting", "Clinic", "attending", 1, "published", eli["id"], "Water Polo", "developing", ""))
    if travel and eli:
        d.execute("""INSERT INTO lineup_events(category_id, subtype, title, date, end_date, start_time, end_time, city, venue, description, hosting, kind, stage, official, team_intent, status, created_by, sport, skill_levels, divisions, comp_format)
            VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
            (travel["id"], "Tournament", "Coastal Cup", day(20), day(22), "08:00", "17:00", "Long Beach", "Belmont Plaza",
             "Official tournament. Registration is per team.", "Away", "Tournament", "going", 1, "official", "published", eli["id"],
             "Water Polo", "intermediate,experienced", "mens,womens,coed", "per_team"))
    d.commit()
    print("Seeded sports samples into", os.environ.get("GRUNIONS_DB"))

if __name__ == "__main__":
    main()
