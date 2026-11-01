"""Sample Lineup events for a local preview database.

Refuses to run unless GRUNIONS_DEMO_SEED=1. It does not run on deploy and it
does not touch a database unless you point GRUNIONS_DB at one and opt in.

    GRUNIONS_DEMO_SEED=1 GRUNIONS_DB=/tmp/grunions-lineup-demo.db \\
        .venv/bin/python seed_lineup_demo.py
"""
import os, sys, datetime as dt

if os.environ.get("GRUNIONS_DEMO_SEED") != "1":
    sys.exit("Refusing to seed. Set GRUNIONS_DEMO_SEED=1 and point GRUNIONS_DB at a local or preview database.")

os.environ.setdefault("GRUNIONS_SHEET_SYNC", "0")
os.environ.setdefault("ADMIN_EMAIL", "eli@example.com")
import app as A

def main():
    d = A.open_db()
    today = A.today_pt()
    def add(email, **kw):
        who = d.execute("SELECT id FROM members WHERE email=?", (email,)).fetchone()
        if not who: raise SystemExit("missing member " + email)
        cat = d.execute("SELECT id FROM lineup_categories WHERE slug=?", (kw.pop("slug"),)).fetchone()
        d.execute("""INSERT INTO lineup_events(category_id, subtype, title, date, end_date, start_time, end_time,
            city, venue, description, link, hosting, kind, stage, official, team_intent, status, host_id, created_by,
            capacity, cost, details, submitted_at, featured)
            VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
            (cat["id"], kw.get("subtype") or "", kw["title"], kw["date"], kw.get("end_date") or kw["date"],
             kw.get("start_time") or "09:00", kw.get("end_time") or "", kw.get("city") or "", kw["location"],
             kw["description"], kw.get("link") or "", kw.get("hosting") or "Away", kw.get("kind") or kw.get("subtype") or "Event",
             "interest" if kw.get("team_intent") == "considering" else ("going" if kw.get("team_intent") == "official" else "attending"),
             kw.get("official") or 0, kw.get("team_intent") or "", kw.get("status") or "published",
             None if kw.get("official") else who["id"], who["id"], kw.get("capacity"), kw.get("cost") or "",
             kw.get("details") or "", A.stamp_pt() if kw.get("status") == "pending" else None, kw.get("featured") or 0))
        return d.execute("SELECT last_insert_rowid()").fetchone()[0]
    friday = today + dt.timedelta(days=(4 - today.weekday()) % 7 or 7)
    sunday = friday + dt.timedelta(days=2)
    # Member birthday, waiting on an admin. Not on the public Lineup.
    add("jane@example.com", slug="social", subtype="Party", title="Jane's birthday", status="pending", official=0,
        date=(today + dt.timedelta(days=9)).isoformat(), start_time="20:00", end_time="22:00",
        city="Huntington Beach", location="Jane's place", description="Cake after Friday practice. Not a club commitment.")
    # Approved member-hosted run. Going here is optional and is not an official trip.
    run = add("sam@example.com", slug="activities", subtype="Run", title="Friday morning run", official=0,
        date=friday.isoformat(), start_time="07:00", end_time="08:00", city="Huntington Beach",
        location="Pier parking lot", description="Easy 4 miles. Meet at the pier. Hosted by a member, not a club practice.")
    add("casey@example.com", slug="service", subtype="Volunteering", title="Harbor cleanup", official=0,
        date=(today + dt.timedelta(days=16)).isoformat(), start_time="09:00", end_time="12:00",
        city="Long Beach", location="Alamitos Bay", description="Gloves and bags provided. Member-hosted volunteer morning.")
    add("eli@example.com", slug="social", subtype="Happy hour", title="Club happy hour", official=1, hosting="Hosting", featured=1,
        date=(today + dt.timedelta(days=6)).isoformat(), start_time="18:30", end_time="20:30",
        city="Huntington Beach", location="Grunions pool deck", description="Official club social after the week.")
    igla = add("eli@example.com", slug="travel", subtype="Tournament", title="IGLA", official=1, hosting="Away",
        team_intent="considering", date=(today + dt.timedelta(days=40)).isoformat(), end_date=(today + dt.timedelta(days=44)).isoformat(),
        start_time="09:00", city="San Diego", location="San Diego", description="Gauging interest for the trip. Not a commitment yet.",
        link="https://example.com/igla")
    add("eli@example.com", slug="travel", subtype="Tournament", title="Coastal Cup", official=1, hosting="Away",
        team_intent="official", date=friday.isoformat(), end_date=sunday.isoformat(), start_time="08:00", end_time="17:00",
        city="Long Beach", location="Belmont Plaza", description="Official Fri–Sun tournament. Only Going puts it on Home.",
        link="https://example.com/coastal")
    jane = d.execute("SELECT id FROM members WHERE email='jane@example.com'").fetchone()["id"]
    # Jane is only Interested in IGLA, so the next practice stays on her Home card.
    d.execute("INSERT INTO lineup_rsvps(event_id, member_id, going, state) VALUES(?,?,0,'interested')", (igla, jane))
    d.commit()
    print("Seeded Lineup samples into", os.environ.get("GRUNIONS_DB"))
    print("Friday run", run, friday.isoformat(), "· Jane is Interested in IGLA only, so Home stays on practice.")

if __name__ == "__main__":
    main()
