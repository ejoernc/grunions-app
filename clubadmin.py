"""Club programs, scoped requirements, and payment labels for Manage.

Inactive programs do not enforce requirements. Practices and RSVPs are never written here.
"""
import datetime as dt
from markupsafe import Markup, escape

WEEKDAYS = (("mon", "Mon"), ("tue", "Tue"), ("wed", "Wed"), ("thu", "Thu"), ("fri", "Fri"), ("sat", "Sat"), ("sun", "Sun"))
ROLES = (("athlete", "Athlete"), ("coach", "Coach"), ("referee", "Referee"), ("admin", "Administrator"))
EFFECTS = (("register", "Required for registration"), ("checkin", "Required for check-in"), ("info", "Informational only"))
VERIFICATIONS = (("manual", "Manual"), ("document", "Document upload"), ("external", "External verification"))
CHEV = '<svg width="18" height="18" viewBox="0 0 256 256" fill="currentColor"><path d="M181.66,133.66l-80,80a8,8,0,0,1-11.32-11.32L164.69,128,90.34,53.66a8,8,0,0,1,11.32-11.32l80,80A8,8,0,0,1,181.66,133.66Z"/></svg>'


def _csv(value):
    return [part.strip() for part in str(value or "").split(",") if part.strip()]


def ensure(d):
    d.execute("""CREATE TABLE IF NOT EXISTS sport_families(
        id INTEGER PRIMARY KEY, slug TEXT NOT NULL UNIQUE, name TEXT NOT NULL)""")
    d.execute("""CREATE TABLE IF NOT EXISTS programs(
        id INTEGER PRIMARY KEY, family_id INTEGER NOT NULL, slug TEXT NOT NULL UNIQUE, name TEXT NOT NULL,
        public_name TEXT NOT NULL, governing_body TEXT NOT NULL DEFAULT 'none',
        activities TEXT NOT NULL DEFAULT 'practice', active INTEGER NOT NULL DEFAULT 0,
        public_feed INTEGER NOT NULL DEFAULT 0, venue TEXT NOT NULL DEFAULT '', notes TEXT NOT NULL DEFAULT '',
        legacy_slug TEXT NOT NULL DEFAULT '')""")
    d.execute("""CREATE TABLE IF NOT EXISTS program_schedules(
        id INTEGER PRIMARY KEY, program_id INTEGER NOT NULL, description TEXT NOT NULL DEFAULT '',
        weekdays TEXT NOT NULL DEFAULT '', start TEXT NOT NULL DEFAULT '', end TEXT NOT NULL DEFAULT '',
        timezone TEXT NOT NULL DEFAULT 'America/Los_Angeles', venue TEXT NOT NULL DEFAULT '',
        notes TEXT NOT NULL DEFAULT '')""")
    d.execute("""CREATE TABLE IF NOT EXISTS program_coaches(
        program_id INTEGER NOT NULL, member_id INTEGER NOT NULL, PRIMARY KEY(program_id, member_id))""")
    d.execute("""CREATE TABLE IF NOT EXISTS requirement_scopes(
        requirement_id INTEGER PRIMARY KEY, description TEXT NOT NULL DEFAULT '', category TEXT NOT NULL DEFAULT '',
        issuer TEXT NOT NULL DEFAULT '', activities TEXT NOT NULL DEFAULT '', roles TEXT NOT NULL DEFAULT '',
        everyone INTEGER NOT NULL DEFAULT 0, effect TEXT NOT NULL DEFAULT 'info',
        affects_clearance INTEGER NOT NULL DEFAULT 0, verification TEXT NOT NULL DEFAULT 'manual',
        review_status TEXT NOT NULL DEFAULT 'needs_review')""")
    d.execute("""CREATE TABLE IF NOT EXISTS requirement_programs(
        requirement_id INTEGER NOT NULL, program_id INTEGER NOT NULL,
        PRIMARY KEY(requirement_id, program_id))""")
    d.execute("""CREATE TABLE IF NOT EXISTS plan_programs(
        plan_id INTEGER NOT NULL, program_id INTEGER NOT NULL, PRIMARY KEY(plan_id, program_id))""")
    d.execute("""CREATE TABLE IF NOT EXISTS scope_reviews(
        id INTEGER PRIMARY KEY, kind TEXT NOT NULL, ref_id INTEGER NOT NULL, reason TEXT NOT NULL,
        resolved INTEGER NOT NULL DEFAULT 0)""")
    d.execute("""CREATE TABLE IF NOT EXISTS club_meta(key TEXT PRIMARY KEY, value TEXT NOT NULL)""")
    d.execute("""CREATE TABLE IF NOT EXISTS governing_bodies(
        id INTEGER PRIMARY KEY, name TEXT NOT NULL, short TEXT NOT NULL DEFAULT '', url TEXT NOT NULL DEFAULT '',
        gives_number INTEGER NOT NULL DEFAULT 0, gives_insurance INTEGER NOT NULL DEFAULT 0, gives_expiry INTEGER NOT NULL DEFAULT 0,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP)""")
    d.execute("""CREATE TABLE IF NOT EXISTS program_divisions(
        id INTEGER PRIMARY KEY, program_id INTEGER NOT NULL, slug TEXT NOT NULL,
        name TEXT NOT NULL, description TEXT NOT NULL DEFAULT '',
        sort INTEGER NOT NULL DEFAULT 0, archived INTEGER NOT NULL DEFAULT 0,
        UNIQUE(program_id, slug))""")
    d.execute("""CREATE TABLE IF NOT EXISTS leadership_roles(
        id INTEGER PRIMARY KEY, program_id INTEGER, name TEXT NOT NULL,
        permission TEXT NOT NULL DEFAULT 'none', sort INTEGER NOT NULL DEFAULT 0)""")
    d.execute("""CREATE TABLE IF NOT EXISTS leadership_members(
        role_id INTEGER NOT NULL, member_id INTEGER NOT NULL, PRIMARY KEY(role_id, member_id))""")
    if "board" not in [r[1] for r in d.execute("PRAGMA table_info(leadership_roles)")]:
        d.execute("ALTER TABLE leadership_roles ADD COLUMN board INTEGER NOT NULL DEFAULT 0")  # role held by a board member
    _migrate(d)
    _ensure_pass_columns(d)
    _seed_passes(d)
    _seed_org_structure(d)
    _ensure_schedule_days(d)
    _migrate_compliance_venues(d)
    _rename_pool_swimming(d)


def reminder_settings(d):
    """Club switch for automatic practice reminders. Off until an admin turns it on."""
    raw = _meta(d, "practice_reminders_hours") or "3"
    try:
        hours = int(raw)
    except ValueError:
        hours = 3
    if hours < 1:
        hours = 1
    if hours > 24:
        hours = 24
    return {"enabled": _meta(d, "practice_reminders") == "1", "hours": hours}


def save_reminder_settings(d, form):
    try:
        hours = int((form.get("hours") or "3").strip())
    except ValueError:
        raise ValueError("Use a whole number of hours.")
    if hours < 1 or hours > 24:
        raise ValueError("Use 1 to 24 hours.")
    _set_meta(d, "practice_reminders", "1" if form.get("enabled") else "0")
    _set_meta(d, "practice_reminders_hours", str(hours))


def reminders_html(d, csrf):
    settings = reminder_settings(d)
    return """<form method=post class=clubform style="padding-bottom:120px">%s
<label class=checkline><input type=checkbox name=enabled value=1%s> Send practice reminders</label>
<label>Hours before<input name=hours type=number min=1 max=24 value="%d"></label>
<p class="ty-muted ty-sm sm">Off until you turn this on. Nothing goes out automatically while it is off. A reminder is sent once for each session and skips cancelled or started sessions. RSVPs are not changed.</p>
<button class="rg-btn primary full" type=submit>Save</button>
</form>""" % (csrf, " checked" if settings["enabled"] else "", settings["hours"])


def _meta(d, key):
    row = d.execute("SELECT value FROM club_meta WHERE key=?", (key,)).fetchone()
    return row["value"] if row else ""


def _set_meta(d, key, value):
    d.execute("INSERT INTO club_meta(key, value) VALUES(?,?) ON CONFLICT(key) DO UPDATE SET value=excluded.value", (key, value))


def _family_id(d, slug, name):
    row = d.execute("SELECT id FROM sport_families WHERE slug=?", (slug,)).fetchone()
    if row:
        return row["id"]
    return d.execute("INSERT INTO sport_families(slug, name) VALUES(?,?)", (slug, name)).lastrowid


def _program_id(d, spec, family_id):
    row = d.execute("SELECT id FROM programs WHERE slug=?", (spec["slug"],)).fetchone()
    if row:
        return row["id"]
    return d.execute("""INSERT INTO programs(family_id, slug, name, public_name, governing_body, activities, active, public_feed, legacy_slug)
        VALUES(?,?,?,?,?,?,?,?,?)""", (
            family_id, spec["slug"], spec["name"], spec["public_name"], spec["body"], spec["activities"],
            spec["active"], spec["public"], spec["legacy"])).lastrowid


def _migrate(d):
    if _meta(d, "programs_seeded") == "1":
        return
    families = {
        "water-polo": _family_id(d, "water-polo", "Water Polo"),
        "swimming": _family_id(d, "swimming", "Swimming"),
    }
    specs = (
        {"slug": "water-polo", "family": "water-polo", "name": "Water Polo", "public_name": "Water Polo",
         "body": "usawp", "activities": "practice,scrimmage,game", "active": 1, "public": 1, "legacy": "water-polo"},
        {"slug": "pool-swimming", "family": "swimming", "name": "Swimming", "public_name": "Swimming",
         "body": "usms", "activities": "practice", "active": 0, "public": 0, "legacy": "swimming"},
        {"slug": "open-water", "family": "swimming", "name": "Open Water Swimming", "public_name": "Open Water Swimming",
         "body": "none", "activities": "practice", "active": 0, "public": 0, "legacy": ""},
    )
    ids = {}
    for spec in specs:
        ids[spec["slug"]] = _program_id(d, spec, families[spec["family"]])
    _map_plans(d, ids)
    _map_requirements(d, ids)
    _copy_series(d, ids)
    _set_meta(d, "programs_seeded", "1")


def _rename_pool_swimming(d):
    """The pool program is named Swimming. The id and slug stay so links do not move."""
    row = d.execute("SELECT id, name FROM programs WHERE slug='pool-swimming'").fetchone()
    if row and row["name"] != "Swimming":
        d.execute("UPDATE programs SET name='Swimming', public_name='Swimming' WHERE id=?", (row["id"],))
    d.execute("""UPDATE requirement_scopes SET description='Current US Masters Swimming membership for swimming.'
        WHERE description='Current US Masters Swimming membership for pool swimming.'""")


def _map_plans(d, ids):
    try:
        plans = d.execute("SELECT id, sports FROM payment_plans").fetchall()
    except Exception:
        return
    for plan in plans:
        slugs = set(_csv(plan["sports"]))
        if "water-polo" in slugs:
            d.execute("INSERT OR IGNORE INTO plan_programs(plan_id, program_id) VALUES(?,?)", (plan["id"], ids["water-polo"]))
        if "swimming" in slugs:
            d.execute("INSERT OR IGNORE INTO plan_programs(plan_id, program_id) VALUES(?,?)", (plan["id"], ids["pool-swimming"]))


def _ensure_requirement(d, name, keywords, applies_to="athlete"):
    row = d.execute("SELECT id FROM requirements WHERE lower(name)=?", (name.lower(),)).fetchone()
    if row:
        return row["id"]
    return d.execute("INSERT INTO requirements(name, applies_to, keywords, expires, active) VALUES(?,?,?,1,1)",
                      (name, applies_to, keywords)).lastrowid


def _scope(d, req_id, description, issuer, activities, roles, everyone, effect, affects, verification, review):
    d.execute("""INSERT INTO requirement_scopes(requirement_id, description, category, issuer, activities, roles, everyone, effect, affects_clearance, verification, review_status)
        VALUES(?,?,?,?,?,?,?,?,?,?,?)
        ON CONFLICT(requirement_id) DO NOTHING""", (
            req_id, description, "", issuer, activities, roles, everyone, effect, affects, verification, review))


def _link(d, req_id, program_id):
    d.execute("INSERT OR IGNORE INTO requirement_programs(requirement_id, program_id) VALUES(?,?)", (req_id, program_id))


def _map_requirements(d, ids):
    usms = _ensure_requirement(d, "USMS membership", "usms")
    _scope(d, usms, "Current US Masters Swimming membership for swimming.", "US Masters Swimming",
           "practice", "athlete", 0, "register", 1, "manual", "active")
    _link(d, usms, ids["pool-swimming"])
    insurance = _ensure_requirement(d, "Open-water insurance", "openwater,insurance")
    _scope(d, insurance, "Insurance for open-water swimming. Not applied while the program is off.", "Club",
           "practice", "athlete", 0, "register", 1, "manual", "active")
    _link(d, insurance, ids["open-water"])
    for req in d.execute("SELECT * FROM requirements").fetchall():
        blob = ((req["name"] or "") + " " + (req["keywords"] or "")).lower()
        if d.execute("SELECT 1 FROM requirement_scopes WHERE requirement_id=?", (req["id"],)).fetchone():
            continue
        if "safesport" in blob:
            _scope(d, req["id"], "SafeSport for Water Polo only.", "USA Water Polo", "", "athlete,coach", 0, "checkin", 1, "manual", "active")
            _link(d, req["id"], ids["water-polo"])
            continue
        _scope(d, req["id"], "", "", "", "", 0, "info", 0, "manual", "needs_review")
        d.execute("""INSERT INTO scope_reviews(kind, ref_id, reason, resolved)
            SELECT 'requirement', ?, ?, 0 WHERE NOT EXISTS(
                SELECT 1 FROM scope_reviews WHERE kind='requirement' AND ref_id=? AND resolved=0)""",
                  (req["id"], "Legacy rule has no explicit program. It is not enforced until an admin chooses programs.", req["id"]))


def _copy_series(d, ids):
    cols = {row[1] for row in d.execute("PRAGMA table_info(practice_series)")}
    if "weekdays" not in cols:
        return
    sport_col = "sport" in cols
    for series in d.execute("SELECT * FROM practice_series").fetchall():
        label = (series["sport"] if sport_col else "") or "Water Polo"
        program = program_for_label(d, label)
        if not program:
            continue
        exists = d.execute("""SELECT 1 FROM program_schedules WHERE program_id=? AND weekdays=? AND start=? AND venue=?""",
                           (program["id"], series["weekdays"] or "", series["start"] or "", series["location"] or "")).fetchone()
        if exists:
            continue
        d.execute("""INSERT INTO program_schedules(program_id, description, weekdays, start, end, timezone, venue, notes)
            VALUES(?,?,?,?,?,?,?,?)""", (
                program["id"], "Copied from the existing series. Saving this template does not add sessions.",
                series["weekdays"] or "", series["start"] or "", series["end"] or "", "America/Los_Angeles",
                series["location"] or "", ""))


def programs(d, active_only=False):
    sql = """SELECT p.*, f.name AS family_name, f.slug AS family_slug
        FROM programs p JOIN sport_families f ON f.id=p.family_id"""
    if active_only:
        sql += " WHERE p.active=1"
    sql += " ORDER BY p.active DESC, p.name"
    return d.execute(sql).fetchall()


def program_by_slug(d, slug):
    return d.execute("""SELECT p.*, f.name AS family_name FROM programs p
        JOIN sport_families f ON f.id=p.family_id WHERE p.slug=?""", (slug,)).fetchone()


def program_for_label(d, label):
    needle = " ".join(str(label or "").split()).casefold()
    if not needle:
        return None
    for row in programs(d):
        if needle in (row["name"].casefold(), row["public_name"].casefold(), row["slug"], (row["legacy_slug"] or "").casefold()):
            return row
    if needle == "swimming":
        return program_by_slug(d, "pool-swimming")
    return None


def reviews(d):
    return d.execute("""SELECT r.*, q.name AS req_name FROM scope_reviews r
        LEFT JOIN requirements q ON q.id=r.ref_id
        WHERE r.resolved=0 ORDER BY r.id""").fetchall()


def requirement_rows(d):
    rows = []
    for req in d.execute("SELECT * FROM requirements ORDER BY name").fetchall():
        scope = d.execute("SELECT * FROM requirement_scopes WHERE requirement_id=?", (req["id"],)).fetchone()
        linked = [r["name"] for r in d.execute("""SELECT p.name FROM requirement_programs rp
            JOIN programs p ON p.id=rp.program_id WHERE rp.requirement_id=? ORDER BY p.name""", (req["id"],)).fetchall()]
        rows.append({"req": req, "scope": scope, "programs": linked})
    return rows


def set_active(d, slug, on):
    program = program_by_slug(d, slug)
    if not program:
        raise ValueError("Choose a program.")
    flag = 1 if on else 0
    d.execute("UPDATE programs SET active=?, public_feed=? WHERE id=?", (flag, flag, program["id"]))


def save_overview(d, slug, form):
    program = program_by_slug(d, slug)
    if not program:
        raise ValueError("Choose a program.")
    activities = [a for a in ("practice", "scrimmage", "game") if form.get("activity_%s" % a)]
    if not activities:
        raise ValueError("Choose at least one activity.")
    body = (form.get("governing_body") or "none").strip()
    if not valid_body(d, body):
        raise ValueError("Choose a governing body.")
    d.execute("""UPDATE programs SET governing_body=?, activities=?, venue=?, notes=? WHERE id=?""", (
        body, ",".join(activities), (form.get("venue") or "")[:200], (form.get("notes") or "")[:500], program["id"]))
    chosen = [int(v) for v in form.getlist("coach") if str(v).isdigit()]
    d.execute("DELETE FROM program_coaches WHERE program_id=?", (program["id"],))
    for mid in chosen:
        d.execute("INSERT OR IGNORE INTO program_coaches(program_id, member_id) VALUES(?,?)", (program["id"], mid))


def _hm(value):
    text = (value or "").strip()
    if len(text) >= 5 and text[2] == ":":
        text = text[:5]
    if len(text) != 5 or not (text[:2].isdigit() and text[3:].isdigit()):
        return ""
    hour, minute = int(text[:2]), int(text[3:])
    if hour > 23 or minute > 59:
        return ""
    return "%02d:%02d" % (hour, minute)


def _clock_bits(value):
    hour, minute = int(value[:2]), int(value[3:])
    meridiem = "AM" if hour < 12 else "PM"
    return hour % 12 or 12, minute, meridiem


def slot_span(start, end, keep_minutes=True):
    """7:00 to 9:00 PM on a row. 7 to 9 PM in a summary, keeping minutes that are not :00."""
    sh, sm, sa = _clock_bits(start)
    eh, em, ea = _clock_bits(end)

    def piece(hour, minute):
        if keep_minutes or minute:
            return "%d:%02d" % (hour, minute)
        return "%d" % hour

    left, right = piece(sh, sm), piece(eh, em)
    if sa != ea:
        return "%s %s to %s %s" % (left, sa, right, ea)
    return "%s to %s %s" % (left, right, ea)


def _day_label(code):
    return dict(WEEKDAYS).get(code, code)


def _join_days(labels):
    if len(labels) <= 1:
        return labels[0] if labels else ""
    if len(labels) == 2:
        return "%s & %s" % (labels[0], labels[1])
    return "%s & %s" % (", ".join(labels[:-1]), labels[-1])


def schedule_days(d, program_id):
    order = {code: index for index, (code, _label) in enumerate(WEEKDAYS)}
    rows = d.execute("SELECT * FROM program_schedule_days WHERE program_id=?", (program_id,)).fetchall()
    return sorted(rows, key=lambda row: (order.get(row["weekday"], 9), row["start"] or "", row["id"]))


def schedule_phrase(rows):
    """Tue & Thu 7 to 9 PM · Sun 9 to 11 AM. Days that share a time stay together."""
    order = {code: index for index, (code, _label) in enumerate(WEEKDAYS)}

    def ident(row):
        try:
            return row["id"] or 0
        except Exception:
            return 0

    groups = []
    for row in sorted(rows, key=lambda row: (order.get(row["weekday"], 9), row["start"] or "", ident(row))):
        label = _day_label(row["weekday"])
        if groups and groups[-1][0] == row["start"] and groups[-1][1] == row["end"] and label not in groups[-1][2]:
            groups[-1][2].append(label)
        else:
            groups.append([row["start"], row["end"], [label]])
    return " · ".join("%s %s" % (_join_days(labels), slot_span(start, end, False)) for start, end, labels in groups)


def slot_line(row):
    return "%s · %s" % (_day_label(row["weekday"]), slot_span(row["start"], row["end"], True))


def save_schedule(d, slug, form):
    """Store the description only. Day slots are saved on their own and this does not insert practices."""
    program = program_by_slug(d, slug)
    if not program:
        raise ValueError("Choose a program.")
    row = d.execute("SELECT * FROM program_schedules WHERE program_id=? ORDER BY id LIMIT 1", (program["id"],)).fetchone()
    description = (form.get("description") or "")[:200]
    if row and "schedule_notes" not in form:
        notes = row["notes"] or ""
    else:
        notes = (form.get("schedule_notes") or "")[:500]
    if "schedule_venue" in form:
        venue = (form.get("schedule_venue") or "")[:200]
    elif row:
        venue = row["venue"] or ""
    else:
        venue = ""
    if row:
        d.execute("UPDATE program_schedules SET description=?, venue=?, notes=? WHERE id=?", (description, venue, notes, row["id"]))
    else:
        d.execute("""INSERT INTO program_schedules(program_id, description, weekdays, start, end, timezone, venue, notes)
            VALUES(?,?,?,?,?,?,?,?)""", (program["id"], description, "", "", "", "America/Los_Angeles", venue, notes))


def save_schedule_day(d, program, day_id, form):
    """One weekday and its own times. The same weekday can be saved more than once. Does not insert practices."""
    code = (form.get("weekday") or "").strip().lower()
    if code not in dict(WEEKDAYS):
        raise ValueError("Choose a day.")
    start, end = _hm(form.get("start")), _hm(form.get("end"))
    if not start or not end:
        raise ValueError("Add a start and end time.")
    if start >= end:
        raise ValueError("The end time has to be after the start time.")
    if day_id:
        row = d.execute("SELECT id FROM program_schedule_days WHERE id=? AND program_id=?", (day_id, program["id"])).fetchone()
        if not row:
            raise ValueError("That day is no longer on this schedule.")
        d.execute("UPDATE program_schedule_days SET weekday=?, start=?, end=? WHERE id=?", (code, start, end, day_id))
        return day_id
    return d.execute("INSERT INTO program_schedule_days(program_id, weekday, start, end) VALUES(?,?,?,?)",
                     (program["id"], code, start, end)).lastrowid


def remove_schedule_day(d, program, day_id):
    d.execute("DELETE FROM program_schedule_days WHERE id=? AND program_id=?", (day_id, program["id"]))


def _ensure_schedule_days(d):
    d.execute("""CREATE TABLE IF NOT EXISTS program_schedule_days(
        id INTEGER PRIMARY KEY, program_id INTEGER NOT NULL,
        weekday TEXT NOT NULL, start TEXT NOT NULL, end TEXT NOT NULL)""")
    if _meta(d, "schedule_days_v1") == "1":
        return
    order = ("mon", "tue", "wed", "thu", "fri", "sat", "sun")
    known = dict(WEEKDAYS)
    for sched in d.execute("SELECT * FROM program_schedules").fetchall():
        start, end = _hm(sched["start"]), _hm(sched["end"])
        if not start or not end or start >= end:
            continue
        if d.execute("SELECT 1 FROM program_schedule_days WHERE program_id=?", (sched["program_id"],)).fetchone():
            continue
        seen = []
        for part in _csv(sched["weekdays"]):
            key = part.strip().lower()
            if key in known:
                code = key
            elif key.isdigit() and 0 <= int(key) <= 6:
                code = order[int(key)]
            else:
                continue
            if code in seen:
                continue
            seen.append(code)
            d.execute("INSERT INTO program_schedule_days(program_id, weekday, start, end) VALUES(?,?,?,?)",
                      (sched["program_id"], code, start, end))
    _set_meta(d, "schedule_days_v1", "1")


def schedule_for(d, program_id):
    return d.execute("SELECT * FROM program_schedules WHERE program_id=? ORDER BY id LIMIT 1", (program_id,)).fetchone()


def _kind_for(name, keywords):
    blob = "%s %s" % (name or "", keywords or "")
    blob = blob.lower()
    if "safesport" in blob:
        return "safesport"
    if "background" in blob:
        return "background"
    if "referee" in blob:
        return "referee"
    if "insurance" in blob or "open water" in blob or "open-water" in blob:
        return "insurance"
    if "usawp" in blob or "usa water polo" in blob or "usms" in blob or "masters swimming" in blob:
        return "membership"
    if "waiver" in blob:
        return "waiver"
    if "coach" in blob and "cert" in blob:
        return "coaching"
    return "custom"


def _default_roles(kind):
    if kind == "safesport":
        return "athlete,coach"
    if kind in ("background", "coaching"):
        return "coach"
    if kind == "referee":
        return "referee"
    return "athlete"


def _verify_from_scope(value):
    if value == "external":
        return "auto"
    return "review"


def _sync_rules(d, req_id, program_ids, roles, everyone, enforced, verification, tracks):
    """Keep one per-sport rule for each linked sport. Does not touch member records."""
    kind = ""
    row = d.execute("SELECT kind, expires FROM requirements WHERE id=?", (req_id,)).fetchone()
    if row:
        kind = row["kind"] or ""
        if tracks is None:
            tracks = row["expires"] or 0
    verify = _verify_from_scope(verification)
    role_csv = ",".join(roles) if isinstance(roles, (list, tuple)) else (roles or "")
    if not role_csv and not everyone:
        role_csv = _default_roles(kind)
    keep = set(program_ids)
    for pid in keep:
        found = d.execute("SELECT id FROM program_rules WHERE program_id=? AND requirement_id=?", (pid, req_id)).fetchone()
        if found:
            d.execute("""UPDATE program_rules SET roles=?, everyone=?, enforced=?, verification=?, tracks_expiration=?
                WHERE id=?""", (role_csv, 1 if everyone else 0, 1 if enforced else 0, verify, 1 if tracks else 0, found["id"]))
        else:
            d.execute("""INSERT INTO program_rules(program_id, requirement_id, roles, everyone, enforced, timing, within_days, verification, tracks_expiration)
                VALUES(?,?,?,?,?,'before_first',0,?,?)""", (pid, req_id, role_csv, 1 if everyone else 0, 1 if enforced else 0, verify, 1 if tracks else 0))
    for old in d.execute("SELECT id, program_id FROM program_rules WHERE requirement_id=?", (req_id,)).fetchall():
        if old["program_id"] not in keep:
            d.execute("DELETE FROM program_rules WHERE id=?", (old["id"],))


def _migrate_compliance_venues(d):
    """One definition per requirement name, one rule per sport link, and venues from saved places."""
    cols = {row[1] for row in d.execute("PRAGMA table_info(requirements)")}
    if not cols:
        return
    if "kind" not in cols:
        d.execute("ALTER TABLE requirements ADD COLUMN kind TEXT NOT NULL DEFAULT 'custom'")
    d.execute("""CREATE TABLE IF NOT EXISTS program_rules(
        id INTEGER PRIMARY KEY, program_id INTEGER NOT NULL, requirement_id INTEGER NOT NULL,
        roles TEXT NOT NULL DEFAULT '', everyone INTEGER NOT NULL DEFAULT 0,
        enforced INTEGER NOT NULL DEFAULT 0, timing TEXT NOT NULL DEFAULT 'before_first',
        within_days INTEGER NOT NULL DEFAULT 0, verification TEXT NOT NULL DEFAULT 'review',
        tracks_expiration INTEGER NOT NULL DEFAULT 0, UNIQUE(program_id, requirement_id))""")
    d.execute("""CREATE TABLE IF NOT EXISTS venues(
        id INTEGER PRIMARY KEY, name TEXT NOT NULL, address TEXT NOT NULL DEFAULT '',
        instructions TEXT NOT NULL DEFAULT '')""")
    d.execute("""CREATE TABLE IF NOT EXISTS venue_programs(
        venue_id INTEGER NOT NULL, program_id INTEGER NOT NULL, PRIMARY KEY(venue_id, program_id))""")
    if _meta(d, "compliance_venues_v1") == "1":
        return
    groups = {}
    for req in d.execute("SELECT * FROM requirements ORDER BY id").fetchall():
        key = " ".join((req["name"] or "").casefold().split())
        groups.setdefault(key, []).append(req)
    for rows in groups.values():
        keep = rows[0]["id"]
        for extra in rows[1:]:
            d.execute("""DELETE FROM member_reqs WHERE req_id=? AND member_id IN (
                SELECT member_id FROM member_reqs WHERE req_id=?)""", (extra["id"], keep))
            d.execute("UPDATE member_reqs SET req_id=? WHERE req_id=?", (keep, extra["id"]))
            for link in d.execute("SELECT program_id FROM requirement_programs WHERE requirement_id=?", (extra["id"],)).fetchall():
                d.execute("INSERT OR IGNORE INTO requirement_programs(requirement_id, program_id) VALUES(?,?)", (keep, link["program_id"]))
            d.execute("DELETE FROM requirement_programs WHERE requirement_id=?", (extra["id"],))
            d.execute("DELETE FROM requirement_scopes WHERE requirement_id=?", (extra["id"],))
            d.execute("DELETE FROM requirements WHERE id=?", (extra["id"],))
    for req in d.execute("SELECT * FROM requirements").fetchall():
        kind = _kind_for(req["name"], req["keywords"] if "keywords" in req.keys() else "")
        d.execute("UPDATE requirements SET kind=? WHERE id=?", (kind, req["id"]))
        scope = d.execute("SELECT * FROM requirement_scopes WHERE requirement_id=?", (req["id"],)).fetchone()
        enforced = 1 if scope and scope["review_status"] == "active" and scope["affects_clearance"] else 0
        roles = scope["roles"] if scope else _default_roles(kind)
        everyone = scope["everyone"] if scope else 0
        verify = _verify_from_scope(scope["verification"] if scope else "manual")
        tracks = 1 if req["expires"] else 0
        linked = [row["program_id"] for row in d.execute("SELECT program_id FROM requirement_programs WHERE requirement_id=?", (req["id"],)).fetchall()]
        for pid in linked:
            d.execute("""INSERT OR IGNORE INTO program_rules(program_id, requirement_id, roles, everyone, enforced, timing, within_days, verification, tracks_expiration)
                VALUES(?,?,?,?,?,'before_first',0,?,?)""", (pid, req["id"], roles or _default_roles(kind), everyone, enforced, verify, tracks))
    if not d.execute("""SELECT 1 FROM requirements WHERE kind='membership' AND (
            lower(name) LIKE '%usa water polo%' OR lower(coalesce(keywords,'')) LIKE '%usawp%')""").fetchone():
        req_id = d.execute("INSERT INTO requirements(name, applies_to, keywords, expires, active, kind) VALUES(?,?,?,?,1,?)",
                           ("USA Water Polo membership", "athlete", "usawp", 1, "membership")).lastrowid
        d.execute("""INSERT INTO requirement_scopes(requirement_id, description, category, issuer, activities, roles, everyone, effect, affects_clearance, verification, review_status)
            VALUES(?,?,?,?,?,?,?,?,?,?,?)""", (
                req_id, "Current USA Water Polo membership.", "", "USA Water Polo", "", "athlete", 0, "checkin", 1, "external", "active"))
        polo = d.execute("SELECT id FROM programs WHERE slug='water-polo'").fetchone()
        if polo:
            d.execute("INSERT OR IGNORE INTO requirement_programs(requirement_id, program_id) VALUES(?,?)", (req_id, polo["id"]))
            d.execute("""INSERT OR IGNORE INTO program_rules(program_id, requirement_id, roles, everyone, enforced, timing, within_days, verification, tracks_expiration)
                VALUES(?,?, 'athlete', 0, 1, 'before_first', 0, 'auto', 1)""", (polo["id"], req_id))
    _seed_venues(d)
    _set_meta(d, "compliance_venues_v1", "1")


def _seed_venues(d):
    def ensure_venue(name, address):
        found = d.execute("SELECT id FROM venues WHERE lower(name)=?", (name.casefold(),)).fetchone()
        if found:
            if address and not (d.execute("SELECT address FROM venues WHERE id=?", (found["id"],)).fetchone()["address"] or ""):
                d.execute("UPDATE venues SET address=? WHERE id=?", (address, found["id"]))
            return found["id"]
        return d.execute("INSERT INTO venues(name, address, instructions) VALUES(?,?,?)", (name, address or "", "")).lastrowid

    def link(venue_id, program_id):
        if venue_id and program_id:
            d.execute("INSERT OR IGNORE INTO venue_programs(venue_id, program_id) VALUES(?,?)", (venue_id, program_id))

    known = (
        ("Marina High School", "15871 Springdale St, Huntington Beach, CA 92649"),
        ("Westminster High School", "14325 Goldenwest St, Westminster, CA 92683"),
    )
    ids = {}
    for name, address in known:
        ids[name.casefold()] = ensure_venue(name, address)
    for program in d.execute("SELECT id, venue FROM programs").fetchall():
        name = " ".join((program["venue"] or "").split())
        if name:
            link(ensure_venue(name, ""), program["id"])
    for sched in d.execute("SELECT program_id, venue FROM program_schedules").fetchall():
        name = " ".join((sched["venue"] or "").split())
        if name:
            link(ensure_venue(name, ""), sched["program_id"])
    try:
        practices = d.execute("SELECT location, sport FROM practices WHERE trim(COALESCE(location,''))!=''").fetchall()
    except Exception:
        practices = []
    for practice in practices:
        name = " ".join((practice["location"] or "").split())
        venue_id = ids.get(name.casefold())
        if not venue_id:
            found = d.execute("SELECT id FROM venues WHERE lower(name)=?", (name.casefold(),)).fetchone()
            venue_id = found["id"] if found else None
        if not venue_id:
            continue
        program = program_for_label(d, practice["sport"] or "")
        if program:
            link(venue_id, program["id"])


def save_sport_identity(d, slug, form):
    """Name stays put. Active and governing body only. Choosing a body does not add requirements."""
    program = program_by_slug(d, slug)
    if not program:
        raise ValueError("Choose a program.")
    body = (form.get("governing_body") or program["governing_body"] or "none").strip()
    if not valid_body(d, body):
        raise ValueError("Choose a governing body.")
    d.execute("UPDATE programs SET governing_body=? WHERE id=?", (body, program["id"]))


def rules_for(d, program_id, role=None):
    rows = d.execute("""SELECT r.*, q.name, q.kind FROM program_rules r
        JOIN requirements q ON q.id=r.requirement_id
        WHERE r.program_id=? ORDER BY q.name, r.id""", (program_id,)).fetchall()
    if not role:
        return rows
    out = []
    for row in rows:
        if row["everyone"] or not _csv(row["roles"]) or role in _csv(row["roles"]):
            out.append(row)
    return out


def _rule_note(d, program, rule):
    note = "On" if rule["enforced"] else "Off"
    others = [item["name"] for item in d.execute("""SELECT p.name FROM program_rules r
        JOIN programs p ON p.id=r.program_id
        WHERE r.requirement_id=? AND p.id!=? ORDER BY p.name""", (rule["requirement_id"], program["id"]))]
    if others:
        note += " · Also used by: " + ", ".join(others)
    if not program["active"]:
        note += " · Not applied while this sport is off"
    return note


def save_requirement(d, req_id, form):
    name = (form.get("name") or "").strip()
    if not name:
        raise ValueError("Add a name.")
    program_ids = [int(v) for v in form.getlist("program") if str(v).isdigit()]
    if not program_ids:
        raise ValueError("Choose at least one program.")
    effect = form.get("effect") or "info"
    if effect not in dict(EFFECTS):
        raise ValueError("Choose how this requirement is used.")
    verification = form.get("verification") or "manual"
    if verification not in dict(VERIFICATIONS):
        raise ValueError("Choose how this requirement is checked.")
    roles = [code for code, _label in ROLES if form.get("role_%s" % code)]
    activities = [a for a in ("practice", "scrimmage", "game") if form.get("activity_%s" % a)]
    everyone = 1 if form.get("everyone") or not roles else 0
    affects = 1 if form.get("affects_clearance") and effect != "info" else 0
    if req_id:
        d.execute("UPDATE requirements SET name=?, applies_to=?, keywords=?, expires=?, active=1 WHERE id=?", (
            name, "all" if everyone else (roles[0] if roles else "athlete"),
            (form.get("keywords") or name.split()[0]).lower(), 1 if form.get("expires") else 0, req_id))
    else:
        req_id = d.execute("INSERT INTO requirements(name, applies_to, keywords, expires, active) VALUES(?,?,?,?,1)", (
            name, "all" if everyone else (roles[0] if roles else "athlete"),
            (form.get("keywords") or name.split()[0]).lower(), 1 if form.get("expires") else 0)).lastrowid
    d.execute("""INSERT INTO requirement_scopes(requirement_id, description, category, issuer, activities, roles, everyone, effect, affects_clearance, verification, review_status)
        VALUES(?,?,?,?,?,?,?,?,?,?, 'active')
        ON CONFLICT(requirement_id) DO UPDATE SET description=excluded.description, category=excluded.category, issuer=excluded.issuer,
            activities=excluded.activities, roles=excluded.roles, everyone=excluded.everyone, effect=excluded.effect,
            affects_clearance=excluded.affects_clearance, verification=excluded.verification, review_status='active'""", (
                req_id, (form.get("description") or "")[:500], (form.get("category") or "")[:80],
                (form.get("issuer") or "")[:120], ",".join(activities), ",".join(roles), everyone, effect, affects, verification))
    d.execute("DELETE FROM requirement_programs WHERE requirement_id=?", (req_id,))
    for pid in program_ids:
        d.execute("INSERT INTO requirement_programs(requirement_id, program_id) VALUES(?,?)", (req_id, pid))
    d.execute("UPDATE scope_reviews SET resolved=1 WHERE kind='requirement' AND ref_id=?", (req_id,))
    _sync_rules(d, req_id, program_ids, roles, everyone, 1 if affects else 0, verification, 1 if form.get("expires") else 0)
    return req_id


def save_plan_programs(d, plan_id, form):
    plan = d.execute("SELECT id FROM payment_plans WHERE id=?", (plan_id,)).fetchone()
    if not plan:
        raise ValueError("Choose a plan.")
    d.execute("DELETE FROM plan_programs WHERE plan_id=?", (plan_id,))
    for pid in [int(v) for v in form.getlist("program") if str(v).isdigit()]:
        d.execute("INSERT INTO plan_programs(plan_id, program_id) VALUES(?,?)", (plan_id, pid))


def plan_program_names(d, plan_id):
    return [row["name"] for row in d.execute("""SELECT p.name FROM plan_programs pp
        JOIN programs p ON p.id=pp.program_id WHERE pp.plan_id=? ORDER BY p.name""", (plan_id,)).fetchall()]


def coached_slugs(d, member_id):
    slugs = {row["slug"] for row in d.execute("""SELECT p.slug FROM program_coaches c
        JOIN programs p ON p.id=c.program_id WHERE c.member_id=?""", (member_id,)).fetchall()}
    for table, col in (("practice_coaches", "practices"),):
        try:
            for row in d.execute("""SELECT sport FROM practices p JOIN practice_coaches c ON c.practice_id=p.id
                WHERE c.member_id=?""", (member_id,)).fetchall():
                program = program_for_label(d, row["sport"] or "")
                if program:
                    slugs.add(program["slug"])
        except Exception:
            pass
    try:
        cols = {row[1] for row in d.execute("PRAGMA table_info(practice_series)")}
        if "sport" in cols:
            for row in d.execute("""SELECT sport FROM practice_series s JOIN series_coaches c ON c.series_id=s.id
                WHERE c.member_id=?""", (member_id,)).fetchall():
                program = program_for_label(d, row["sport"] or "")
                if program:
                    slugs.add(program["slug"])
    except Exception:
        pass
    return slugs


def _valid_until(status, until, today):
    day = str(until or "")[:10]
    return status == "verified" and bool(day) and day >= today


def membership_tags(d, member, today):
    tags = []
    until = member["usawp_valid_until"] if "usawp_valid_until" in member.keys() else ""
    status = member["usawp_status"] if "usawp_status" in member.keys() else ""
    if _valid_until(status or "", until, today):
        tags.append("Water Polo")
    row = d.execute("SELECT status, valid_until FROM external_memberships WHERE member_id=? AND body='usms'", (member["id"],)).fetchone()
    if row and _valid_until(row["status"] or "", row["valid_until"], today):
        tags.append("Swimming")
    return tags


def coach_tags(d, member_id):
    labels = []
    slugs = coached_slugs(d, member_id)
    if "water-polo" in slugs:
        labels.append("Water Polo coach")
    if "pool-swimming" in slugs or "open-water" in slugs:
        labels.append("Swim coach")
    return labels


def display_tags(d, member, today):
    """Membership tags, with a coach label replacing the matching sport tag."""
    sports = membership_tags(d, member, today)
    coach = coach_tags(d, member["id"])
    if "Water Polo coach" in coach:
        sports = [tag for tag in sports if tag != "Water Polo"]
    if "Swim coach" in coach:
        sports = [tag for tag in sports if tag != "Swimming"]
    names = leadership_tags(d, member["id"])
    have = {tag.casefold() for tag in sports + coach}
    extra = [tag for tag in names if tag.casefold() not in have]
    return sports + coach + extra


def _provider_kind(d, provider_id):
    if not provider_id:
        return ""
    row = d.execute("SELECT kind FROM payment_providers WHERE id=?", (provider_id,)).fetchone()
    return row["kind"] if row else ""


def payment_source(kind, provider_kind):
    if kind == "trial" or provider_kind == "free":
        return "trial"
    if provider_kind == "external_link":
        return "Club Assistant link"
    return "manual"


def has_monthly_membership(d, member_id, today):
    """An active monthly membership. Trials, drop-ins, and expired or unpaid passes do not count."""
    try:
        rows = d.execute("""SELECT e.status, e.paid_through, e.valid_from, p.kind AS plan_kind
            FROM access_entitlements e LEFT JOIN payment_plans p ON p.id=e.plan_id
            WHERE e.member_id=?""", (member_id,)).fetchall()
    except Exception:
        return False
    today = str(today or "")[:10]
    for row in rows:
        if (row["plan_kind"] or "") != "monthly":
            continue
        through = str(row["paid_through"] or "")[:10]
        start = str(row["valid_from"] or "")[:10]
        if row["status"] == "active" and not (through and through < today) and not (start and start > today):
            return True
    return False


def payment_view(d, member_id, today):
    """Latest entitlement as a People-list label. Paying is not clearance."""
    try:
        rows = d.execute("""SELECT e.*, p.name AS plan_name, p.kind AS plan_kind, p.provider_id
            FROM access_entitlements e LEFT JOIN payment_plans p ON p.id=e.plan_id
            WHERE e.member_id=? ORDER BY e.id DESC""", (member_id,)).fetchall()
    except Exception:
        rows = []
    chosen = None
    for row in rows:
        through = str(row["paid_through"] or "")[:10]
        start = str(row["valid_from"] or "")[:10]
        current = row["status"] == "active" and not (through and through < today) and not (start and start > today)
        if current:
            chosen = row
            break
    if chosen is None:
        for row in rows:
            if row["status"] in ("expired", "inactive") or (str(row["paid_through"] or "")[:10] and str(row["paid_through"] or "")[:10] < today):
                return {"label": "Expired", "plan": row["plan_name"] or "", "paying": False, "source": payment_source(row["plan_kind"], _provider_kind(d, row["provider_id"])),
                        "start": row["valid_from"] or "", "end": row["paid_through"] or "", "id": row["id"]}
        return {"label": "Unpaid", "plan": "", "paying": False, "source": "", "start": "", "end": "", "id": None}
    kind = chosen["plan_kind"] or ""
    source = payment_source(kind, _provider_kind(d, chosen["provider_id"]))
    if kind == "trial":
        label, plan = "Trial", ""
    elif kind == "drop_in":
        label, plan = "Drop-in", ""
    else:
        label, plan = "Paid", chosen["plan_name"] or ""
    return {"label": label, "plan": plan, "paying": True, "source": source, "start": chosen["valid_from"] or "",
            "end": chosen["paid_through"] or "", "id": chosen["id"], "programs": plan_program_names(d, chosen["plan_id"]) if chosen["plan_id"] else []}


def entitlement_details(d, member_id):
    out = []
    for row in d.execute("""SELECT e.*, p.name AS plan_name, p.kind AS plan_kind, p.provider_id, p.external_url
        FROM access_entitlements e LEFT JOIN payment_plans p ON p.id=e.plan_id
        WHERE e.member_id=? ORDER BY e.id DESC""", (member_id,)).fetchall():
        out.append({
            "id": row["id"], "plan_id": row["plan_id"], "plan": row["plan_name"] or "No plan",
            "kind": row["plan_kind"] or "", "status": row["status"],
            "start": row["valid_from"] or "", "end": row["paid_through"] or "",
            "source": payment_source(row["plan_kind"], _provider_kind(d, row["provider_id"])),
            "programs": plan_program_names(d, row["plan_id"]) if row["plan_id"] else [],
            "url": row["external_url"] or "", "notes": row["notes"] or "",
        })
    return out


def _req_met(d, member, req, scope, today):
    mr = d.execute("SELECT * FROM member_reqs WHERE member_id=? AND req_id=?", (member["id"], req["id"])).fetchone()
    if scope and scope["verification"] == "document":
        if not mr or (mr["source"] or "") not in ("verified", "manual"):
            return False
    if not mr or not (mr["completed_on"] or mr["expires_on"]):
        return False
    if mr["expires_on"] and str(mr["expires_on"])[:10] < today:
        return False
    if req["expires"] and not mr["expires_on"]:
        return False
    return True


def _role_ok(scope, role):
    if not scope or scope["everyone"] or not _csv(scope["roles"]):
        return True
    return role in _csv(scope["roles"])


def eligibility(d, member, program, activity, role, today):
    """Clearance for one active program. Inactive programs apply nothing."""
    if not program or not program["active"]:
        return {"applied": False, "status": "", "missing": []}
    missing = []
    pending = False
    body = program["governing_body"]
    if body == "usawp":
        until = str(member["usawp_valid_until"] or "")[:10]
        status = member["usawp_status"] or ""
        if status == "pending":
            pending = True
        elif not _valid_until(status, until, today):
            missing.append("USA Water Polo membership")
    elif body == "usms":
        row = d.execute("SELECT status, valid_until FROM external_memberships WHERE member_id=? AND body='usms'", (member["id"],)).fetchone()
        if not row or not _valid_until(row["status"] or "", row["valid_until"], today):
            if row and (row["status"] or "") == "pending":
                pending = True
            else:
                missing.append("USMS membership")
    for req in d.execute("SELECT * FROM requirements WHERE active=1").fetchall():
        scope = d.execute("SELECT * FROM requirement_scopes WHERE requirement_id=?", (req["id"],)).fetchone()
        if not scope or scope["review_status"] != "active" or not scope["affects_clearance"]:
            continue
        linked = d.execute("SELECT 1 FROM requirement_programs WHERE requirement_id=? AND program_id=?", (req["id"], program["id"])).fetchone()
        if not linked:
            continue
        rule = d.execute("SELECT * FROM program_rules WHERE program_id=? AND requirement_id=?", (program["id"], req["id"])).fetchone()
        if rule is not None:
            continue
        acts = _csv(scope["activities"])
        if acts and activity and activity not in acts:
            continue
        if not _role_ok(scope, role):
            continue
        if not _req_met(d, member, req, scope, today):
            missing.append(req["name"])
    for rule in d.execute("""SELECT r.*, q.name, q.expires, q.kind FROM program_rules r
            JOIN requirements q ON q.id=r.requirement_id
            WHERE r.program_id=? AND q.active=1 AND r.enforced=1""", (program["id"],)).fetchall():
        if (rule["kind"] or "") == "membership":
            continue
        if not _role_ok(rule, role):
            continue
        req = {"id": rule["requirement_id"], "name": rule["name"], "expires": 1 if rule["tracks_expiration"] else 0}
        scope = {"verification": "manual", "roles": rule["roles"], "everyone": rule["everyone"]}
        if not _req_met(d, member, req, scope, today):
            missing.append(rule["name"])
    if missing:
        return {"applied": True, "status": "Action needed", "missing": missing}
    if pending:
        return {"applied": True, "status": "Pending verification", "missing": []}
    return {"applied": True, "status": "Cleared", "missing": []}


def swimming_sessions(d):
    """Existing swimming sessions. Read only."""
    cols = {row[1] for row in d.execute("PRAGMA table_info(practices)")}
    if "sport" not in cols:
        return []
    return d.execute("""SELECT id, date, title, sport, location FROM practices
        WHERE lower(coalesce(sport,'')) LIKE '%swim%' OR lower(coalesce(title,'')) LIKE '%swim%'
        ORDER BY date, id""").fetchall()


def _checks(selected, options, name):
    chosen = set(_csv(selected))
    bits = []
    for value, label in options:
        bits.append('<label class=checkline><input type=checkbox name="%s" value="%s"%s> %s</label>' % (
            name, value, " checked" if value in chosen else "", escape(label)))
    return "".join(bits)


def _row(href, title, desc):
    import components
    return str(components.row(title, desc, href))


def requirement_count(d, program_id):
    return d.execute("SELECT COUNT(*) FROM requirement_programs WHERE program_id=?", (program_id,)).fetchone()[0]


def _slug(name):
    raw = "".join(ch.lower() if ch.isalnum() else "-" for ch in name).strip("-")
    while "--" in raw:
        raw = raw.replace("--", "-")
    return raw or "program"


def create_program(d, form):
    name = " ".join((form.get("name") or "").split())
    if not name:
        raise ValueError("Add a name.")
    family_name = " ".join((form.get("family_name") or "").split())
    family_slug = (form.get("family") or "").strip()
    if family_name:
        family_slug = _slug(family_name)
        family_id = _family_id(d, family_slug, family_name)
    else:
        row = d.execute("SELECT id FROM sport_families WHERE slug=?", (family_slug,)).fetchone()
        if not row:
            raise ValueError("Choose a sport family.")
        family_id = row["id"]
    body = (form.get("governing_body") or "none").strip()
    if not valid_body(d, body):
        raise ValueError("Choose a governing body.")
    activities = [a for a in ("practice", "scrimmage", "game") if form.get("activity_%s" % a)]
    if not activities:
        raise ValueError("Choose at least one activity.")
    slug = _slug(name)
    base, n = slug, 2
    while d.execute("SELECT 1 FROM programs WHERE slug=?", (slug,)).fetchone():
        slug = "%s-%d" % (base, n)
        n += 1
    d.execute("""INSERT INTO programs(family_id, slug, name, public_name, governing_body, activities, active, public_feed, venue, notes, legacy_slug)
        VALUES(?,?,?,?,?,?,0,0,'','','')""", (family_id, slug, name, name, body, ",".join(activities)))
    return slug


def add_program_html(d, csrf):
    families = d.execute("SELECT slug, name FROM sport_families ORDER BY name").fetchall()
    options = "".join('<option value="%s">%s</option>' % (escape(row["slug"]), escape(row["name"])) for row in families)
    return """<form method=post class=clubform>%s
<label>Name<input name=name required placeholder="Open Water Swimming"></label>
<label>Sport family<select name=family>%s</select></label>
<label>Or a new family<input name=family_name placeholder="Leave blank to use the family above"></label>
<label>Governing body<select name=governing_body>
<option value=usawp>USA Water Polo</option>
<option value=usms>US Masters Swimming</option>
<option value=none selected>None</option></select></label>
<p>Activities</p>
<label class=checkline><input type=checkbox name=activity_practice value=1 checked> Practice</label>
<label class=checkline><input type=checkbox name=activity_scrimmage value=1> Scrimmage</label>
<label class=checkline><input type=checkbox name=activity_game value=1> Game</label>
<p class="ty-muted ty-sm sm">A new sport starts off. Its requirements are not applied until you turn it on.</p>
<button class="rg-btn primary full" type=submit>Save</button>
</form>""" % (csrf, options)


DEFAULT_DIVISIONS = (
    ("beginner", "Beginner", "New to the sport or learning the basics."),
    ("developing", "Developing", "Knows the fundamentals and is building consistency."),
    ("intermediate", "Intermediate", "Comfortable playing and using core skills."),
    ("experienced", "Experienced", "Proficient in advanced or competitive play."),
)
PERM_CLUB = (("none", "No admin access"), ("admin_lite", "Admin lite"), ("admin", "Admin"))
PERM_SPORT = (("none", "No admin access"), ("sport_admin", "Sport admin"))
REQ_GROUPS = (("athlete", "Athletes"), ("coach", "Coaches"), ("referee", "Referees"))
KIND_LABELS = (
    ("membership", "Governing-body membership"),
    ("safesport", "SafeSport"),
    ("background", "Background screening"),
    ("insurance", "Insurance"),
    ("coaching", "Coaching certification"),
    ("referee", "Referee certification"),
    ("waiver", "Waiver"),
    ("custom", "Custom"),
)
VERIFY_RULE = (("auto", "Automatic check"), ("review", "Admin review"), ("attest", "Self-attestation"))
TIMING_RULE = (("before_first", "Before the first session"), ("within_days", "Within a number of days"))


def _seed_org_structure(d):
    """Divisions and role homes for unassigned requirements. Does not enforce them or touch RSVPs."""
    if _meta(d, "org_structure") == "1":
        return
    for program in d.execute("SELECT id FROM programs").fetchall():
        for i, (slug, name, desc) in enumerate(DEFAULT_DIVISIONS):
            d.execute("""INSERT OR IGNORE INTO program_divisions(program_id, slug, name, description, sort, archived)
                VALUES(?,?,?,?,?,0)""", (program["id"], slug, name, desc, i))
    for req in d.execute("SELECT id, name, keywords FROM requirements").fetchall():
        blob = ((req["name"] or "") + " " + (req["keywords"] or "")).lower()
        role = "coach" if "background" in blob else ("referee" if "referee" in blob else "")
        if not role:
            continue
        scope = d.execute("SELECT review_status, affects_clearance FROM requirement_scopes WHERE requirement_id=?", (req["id"],)).fetchone()
        if scope and scope["review_status"] == "active" and scope["affects_clearance"]:
            continue
        d.execute("""UPDATE requirement_scopes SET roles=?, everyone=0, affects_clearance=0, review_status='needs_review'
            WHERE requirement_id=?""", (role, req["id"]))
        for program in d.execute("SELECT id FROM programs").fetchall():
            d.execute("INSERT OR IGNORE INTO requirement_programs(requirement_id, program_id) VALUES(?,?)", (req["id"], program["id"]))
        d.execute("UPDATE scope_reviews SET resolved=1 WHERE kind='requirement' AND ref_id=?", (req["id"],))
    _set_meta(d, "org_structure", "1")


def level_rows(d, sport_name, selected=""):
    """Active divisions for a sport, plus archived ones still saved on this event."""
    program = program_for_label(d, sport_name or "")
    chosen = {part.strip().lower() for part in str(selected or "").split(",") if part.strip()}
    if not program:
        import sports as sportsmod
        return list(sportsmod.LEVELS)
    rows = d.execute("""SELECT slug, name, description, archived FROM program_divisions
        WHERE program_id=? ORDER BY sort, id""", (program["id"],)).fetchall()
    if not rows:
        import sports as sportsmod
        return list(sportsmod.LEVELS)
    out = []
    for row in rows:
        if row["archived"] and row["slug"] not in chosen:
            continue
        out.append((row["slug"], row["name"], row["description"], row["description"]))
    return out or []


def level_slugs(d, sport_name, include_archived=False):
    program = program_for_label(d, sport_name or "")
    if not program:
        import sports as sportsmod
        return list(sportsmod.LEVEL_IDS)
    sql = "SELECT slug FROM program_divisions WHERE program_id=?"
    if not include_archived:
        sql += " AND archived=0"
    sql += " ORDER BY sort, id"
    return [row["slug"] for row in d.execute(sql, (program["id"],)).fetchall()]


def member_has_permission(d, member_id, permission):
    row = d.execute("""SELECT 1 FROM leadership_members m JOIN leadership_roles r ON r.id=m.role_id
        WHERE m.member_id=? AND r.permission=? LIMIT 1""", (member_id, permission)).fetchone()
    return bool(row)


def leadership_tags(d, member_id):
    return [row["name"] for row in d.execute("""SELECT r.name FROM leadership_roles r
        JOIN leadership_members m ON m.role_id=r.id WHERE m.member_id=? ORDER BY r.name""", (member_id,)).fetchall()]


def save_leadership_role(d, role_id, form, program_id):
    name = " ".join((form.get("name") or "").split())
    if len(name) < 2:
        raise ValueError("Add a role name.")
    allowed = dict(PERM_SPORT if program_id else PERM_CLUB)
    permission = form.get("permission") or "none"
    if permission not in allowed:
        raise ValueError("Choose a permission level.")
    if role_id:
        row = d.execute("SELECT id, program_id FROM leadership_roles WHERE id=?", (role_id,)).fetchone()
        if not row or (row["program_id"] or None) != (program_id or None):
            raise ValueError("Choose a role.")
        d.execute("UPDATE leadership_roles SET name=?, permission=? WHERE id=?", (name[:80], permission, role_id))
    else:
        sort = d.execute("SELECT COALESCE(MAX(sort),0)+1 FROM leadership_roles WHERE COALESCE(program_id,0)=COALESCE(?,0)", (program_id,)).fetchone()[0]
        role_id = d.execute("INSERT INTO leadership_roles(program_id, name, permission, sort) VALUES(?,?,?,?)",
                            (program_id, name[:80], permission, sort)).lastrowid
    d.execute("DELETE FROM leadership_members WHERE role_id=?", (role_id,))
    for mid in form.getlist("person"):
        if str(mid).isdigit():
            d.execute("INSERT OR IGNORE INTO leadership_members(role_id, member_id) VALUES(?,?)", (role_id, int(mid)))
            if permission == "admin":
                d.execute("UPDATE members SET is_admin=1 WHERE id=? AND COALESCE(role,'')!='system'", (int(mid),))
    return role_id


def save_division(d, program, div_id, form):
    name = " ".join((form.get("name") or "").split())
    if len(name) < 2:
        raise ValueError("Add a division name.")
    desc = " ".join((form.get("description") or "").split())[:180]
    if div_id:
        row = d.execute("SELECT id, slug FROM program_divisions WHERE id=? AND program_id=?", (div_id, program["id"])).fetchone()
        if not row:
            raise ValueError("Choose a division.")
        d.execute("UPDATE program_divisions SET name=?, description=? WHERE id=?", (name[:80], desc, div_id))
        return div_id
    slug = _slug(name)
    base, n = slug, 2
    while d.execute("SELECT 1 FROM program_divisions WHERE program_id=? AND slug=?", (program["id"], slug)).fetchone():
        slug = "%s-%d" % (base, n)
        n += 1
    sort = d.execute("SELECT COALESCE(MAX(sort),-1)+1 FROM program_divisions WHERE program_id=?", (program["id"],)).fetchone()[0]
    return d.execute("""INSERT INTO program_divisions(program_id, slug, name, description, sort, archived)
        VALUES(?,?,?,?,?,0)""", (program["id"], slug, name[:80], desc, sort)).lastrowid


def move_division(d, program, div_id, direction):
    rows = d.execute("SELECT id FROM program_divisions WHERE program_id=? AND archived=0 ORDER BY sort, id", (program["id"],)).fetchall()
    ids = [row["id"] for row in rows]
    if div_id not in ids:
        return
    i = ids.index(div_id)
    j = i - 1 if direction == "up" else i + 1
    if j < 0 or j >= len(ids):
        return
    ids[i], ids[j] = ids[j], ids[i]
    for n, item in enumerate(ids):
        d.execute("UPDATE program_divisions SET sort=? WHERE id=?", (n, item))


def programs_html(d):
    bits = ['<div class=mlist>']
    for program in programs(d):
        state = "Active" if program["active"] else "Inactive"
        body = body_label(d, program["governing_body"], "No governing body")
        count = d.execute("SELECT COUNT(*) FROM program_rules WHERE program_id=?", (program["id"],)).fetchone()[0]
        noun = "requirement" if count == 1 else "requirements"
        bits.append(_row("/manage/club/programs/%s" % program["slug"], program["name"], "%s · %s · %d %s" % (body, state, count, noun)))
    bits.append("</div>")
    return "".join(bits)


# Governing bodies (Figma M5): known bodies first, then Self-insured / None, then the club's own.
BUILTIN_BODIES = (("usawp", "USA Water Polo", "Membership + insurance"),
                  ("usms", "US Masters Swimming", "Membership + insurance"),
                  ("usas", "USA Swimming", "Membership"))
SPECIAL_BODIES = (("self", "Self-insured", "Club covers insurance"), ("none", "None", "Club requirements only"))


def custom_bodies(d):
    try:
        return d.execute("SELECT * FROM governing_bodies ORDER BY name").fetchall()
    except Exception:
        return []


def valid_body(d, code):
    code = (code or "").strip()
    if code in [c for c, _n, _s in BUILTIN_BODIES] or code in [c for c, _n, _s in SPECIAL_BODIES]:
        return True
    if code.startswith("gb") and code[2:].isdigit():
        return bool(d.execute("SELECT 1 FROM governing_bodies WHERE id=?", (int(code[2:]),)).fetchone())
    return False


def body_label(d, code, none_label="None"):
    for c, name, _s in BUILTIN_BODIES + SPECIAL_BODIES:
        if c == code:
            return none_label if c == "none" else name
    if code and code.startswith("gb") and code[2:].isdigit():
        row = d.execute("SELECT name FROM governing_bodies WHERE id=?", (int(code[2:]),)).fetchone()
        if row:
            return row["name"]
    return none_label


def _body_gives(row):
    bits = [w for w, on in (("Membership", row["gives_number"]), ("insurance", row["gives_insurance"])) if on]
    return " + ".join(bits) if bits else "Club-defined"


def save_body(d, slug, form):
    program = program_by_slug(d, slug)
    if not program:
        raise ValueError("Choose a program.")
    body = (form.get("governing_body") or "").strip()
    if not valid_body(d, body):
        raise ValueError("Choose a governing body.")
    d.execute("UPDATE programs SET governing_body=? WHERE id=?", (body, program["id"]))


def add_body(d, slug, form):
    """Add a governing body for the whole club and use it for this sport. What members get from it becomes
    requirement templates (not yet assigned to a role), so the next step picks who needs them."""
    program = program_by_slug(d, slug)
    if not program:
        raise ValueError("Choose a program.")
    name = (form.get("name") or "").strip()[:120]
    short = (form.get("short") or "").strip()[:24]
    url = (form.get("url") or "").strip()[:200]
    if not name:
        raise ValueError("Give the governing body a name.")
    found = d.execute("SELECT id FROM governing_bodies WHERE lower(name)=?", (name.casefold(),)).fetchone()
    flags = tuple(1 if form.get(k) else 0 for k in ("gives_number", "gives_insurance", "gives_expiry"))
    if found:
        bid = found["id"]
    else:
        bid = d.execute("""INSERT INTO governing_bodies(name, short, url, gives_number, gives_insurance, gives_expiry)
            VALUES(?,?,?,?,?,?)""", (name, short, url) + flags).lastrowid
    label = short or name
    made = []
    for key, req in (("gives_number", "%s membership number"), ("gives_insurance", "%s insurance")):
        if not form.get(key):
            continue
        rname = req % label
        row = d.execute("SELECT id FROM requirements WHERE lower(name)=?", (rname.casefold(),)).fetchone()
        if not row:
            d.execute("INSERT INTO requirements(name, applies_to, keywords, expires, active) VALUES(?,?,?,?,1)",
                      (rname, "all", label.lower(), 1 if form.get("gives_expiry") else 0))
        made.append(rname)
    d.execute("UPDATE programs SET governing_body=? WHERE id=?", ("gb%d" % bid, program["id"]))
    return made


def _divisions_line(d, program):
    rows = d.execute("SELECT name FROM program_divisions WHERE program_id=? AND archived=0 ORDER BY sort, id", (program["id"],)).fetchall()
    return ", ".join(r["name"] for r in rows) if rows else "None yet"


def program_detail_html(d, program, csrf):
    """Figma M5.1 / M5.4 / M5.5: one control per setting, each change saves with a toast."""
    import components as C
    slug = program["slug"]
    code = program["governing_body"] or "none"
    name = program["name"]
    blurbs = {"athlete": "Insurance, training, and waivers", "coach": "Screening and certifications", "referee": "Officiating credentials"}
    tones = {"athlete": "sun", "coach": "sky", "referee": "lavender"}
    tiles = []
    for role, label in REQ_GROUPS:
        rows = rules_for(d, program["id"], role)
        sub = ", ".join(r["name"] for r in rows[:4]) if rows else blurbs[role]
        tiles.append(str(C.stack_tile("/manage/club/programs/%s/roles/%s" % (slug, role), label, sub, None, tones[role])))
    if code == "self":
        note = "Your club covers insurance. No outside membership is checked."
        block = str(C.info_block("Insurance", "Club covers it", "Add a waiver or proof under Athletes."))
    elif code == "none":
        note = "No governing body. Only your club's own requirements apply."
        block = str(C.info_block("Insurance", "Not set", "Nothing checked unless you add it."))
    else:
        note = "Decides which memberships and insurance count. Picking one doesn't add requirements."
        block = ""
    # Picker sheet (M5.2)
    known = "".join(str(C.choice("governing_body", c, n, sub, code == c)) for c, n, sub in BUILTIN_BODIES)
    known += "".join(str(C.choice("governing_body", "gb%d" % r["id"], r["name"], _body_gives(r), code == "gb%d" % r["id"])) for r in custom_bodies(d))
    special = "".join(str(C.choice("governing_body", c, n, sub, code == c)) for c, n, sub in SPECIAL_BODIES)
    picker = """<dialog id=bodySheet class="botsheet modal" data-sheet-name=body><form method=post class=sheet>%s<div class=grab aria-hidden=true></div>
<input type=hidden name=action value=body>
<h2>Governing body.</h2><p class=ty-muted>Who sets %s's memberships and insurance.</p>
%s<div class=rg-orlabel>OR</div>%s
<button type=button class="rg-choice add" data-swap-sheet=bodyAdd><span class=rg-txt><b>+ Add a governing body</b><small>Not listed? Define it once for the club.</small></span></button>
<button class="rg-btn primary" type=submit>Done</button>
</form></dialog>""" % (csrf, escape(name), known, special)
    adder = """<dialog id=bodyAdd class="botsheet modal" data-sheet-name=add-body><form method=post class=sheet>%s<div class=grab aria-hidden=true></div>
<input type=hidden name=action value=add_body>
<h2>Add a governing body.</h2><p class=ty-muted>Saved for the whole club. Use it on any sport.</p>
<label class=rg-field><span>NAME</span><input name=name required maxlength=120 placeholder="International Gay &amp; Lesbian Aquatics" autocomplete=off></label>
<label class=rg-field><span>SHORT NAME</span><input name=short maxlength=24 placeholder="IGLA" autocomplete=off></label>
<label class=rg-field><span>WEBSITE (OPTIONAL)</span><input name=url maxlength=200 placeholder="igla.org" autocomplete=off inputmode=url></label>
<div class=rg-orlabel>WHAT MEMBERS GET FROM THEM</div>
%s%s%s
<p class="ty-muted ty-sm">Next: pick which roles need it (Athletes, Coaches, Referees).</p>
<button class="rg-btn primary" type=submit>Add and use for %s</button>
</form></dialog>""" % (csrf, C.choice("gives_number", "1", "Membership number", "Members enter an ID you can check", True, "checkbox"),
                        C.choice("gives_insurance", "1", "Insurance", "Their membership includes insurance", True, "checkbox"),
                        C.choice("gives_expiry", "1", "Expiration date", "Remind members before it lapses", True, "checkbox"), escape(name))
    return """<div class=rg-sport>
<form method=post data-autosave>%s<input type=hidden name=action value=active><input type=hidden name=active value=0>
%s</form>
%s
<p class=rg-note>%s</p>
%s
<h2 class=rg-h2>Who needs what</h2>
<div class=rg-tilelist>%s</div>
<h2 class=rg-h2>Skill levels</h2>
<div class=rg-tilelist>%s</div>
<p class=rg-note>Changes save as you make them.</p>
</div>
%s%s
<script>
(function(){
 document.querySelectorAll('form[data-autosave] input[type=checkbox]').forEach(function(i){ i.addEventListener('change', function(){ i.form.requestSubmit ? i.form.requestSubmit() : i.form.submit(); }); });
 document.querySelectorAll('[data-swap-sheet]').forEach(function(b){ b.addEventListener('click', function(){
  var cur=b.closest('dialog'), next=document.getElementById(b.getAttribute('data-swap-sheet'));
  if(cur) cur.close(); if(next){ if(window.grunionsOpenSheet) grunionsOpenSheet(next); else next.showModal(); var f=next.querySelector('input[name=name]'); if(f) setTimeout(function(){f.focus()},250); }
 }); });
})();
</script>""" % (
        csrf, C.toggle("active", "Active", "Requirements apply to everyone in %s." % name, bool(program["active"])),
        C.settings_row("Governing body", body_label(d, code), "#", 'data-open-dialog=bodySheet'),
        escape(note), block, "".join(tiles),
        C.stack_tile("/manage/club/programs/%s/divisions" % slug, "Divisions", _divisions_line(d, program), None, "lime"),
        picker, adder)


def _req_role(scope):
    if not scope or scope["everyone"] or not _csv(scope["roles"]):
        return "athlete"
    roles = _csv(scope["roles"])
    for code, _label in REQ_GROUPS:
        if code in roles:
            return code
    return "athlete"


def _enforced(scope):
    return bool(scope and scope["review_status"] == "active" and scope["affects_clearance"])


def program_requirements_html(d, program):
    rows = d.execute("""SELECT q.id, q.name, s.roles, s.everyone, s.review_status, s.affects_clearance
        FROM requirement_programs rp JOIN requirements q ON q.id=rp.requirement_id
        LEFT JOIN requirement_scopes s ON s.requirement_id=q.id
        WHERE rp.program_id=? ORDER BY q.name""", (program["id"],)).fetchall()
    grouped = {code: [] for code, _label in REQ_GROUPS}
    for row in rows:
        grouped.setdefault(_req_role(row), []).append(row)
    bits = ['<h2>Requirements</h2><p class="ty-muted ty-sm sm">A requirement applies only to that role, and only while this sport is on. Off means it is not enforced.</p>']
    for code, label in REQ_GROUPS:
        bits.append("<h2>%s</h2><div class=mlist>" % label)
        items = grouped.get(code) or []
        if not items:
            bits.append('<p class="ty-muted ty-sm sm" style="padding:12px 16px">No requirements yet.</p>')
        for row in items:
            others = [item["name"] for item in d.execute("""SELECT p.name FROM requirement_programs rp
                JOIN programs p ON p.id=rp.program_id
                WHERE rp.requirement_id=? AND p.id!=? ORDER BY p.name""", (row["id"], program["id"]))]
            note = "On" if _enforced(row) else "Off"
            if others:
                note += " · Also applies to: " + ", ".join(others)
            if not program["active"]:
                note += " · Not applied while this sport is off"
            bits.append(_row("/manage/club/requirements/%d?sport=%s" % (row["id"], program["slug"]), row["name"], note))
        bits.append(_row("/manage/club/programs/%s/requirements/new?role=%s" % (program["slug"], code), "Add requirement", "For %s" % label.lower()))
        bits.append("</div>")
    return "".join(bits)


def divisions_html(d, program):
    rows = d.execute("""SELECT * FROM program_divisions WHERE program_id=? AND archived=0 ORDER BY sort, id""", (program["id"],)).fetchall()
    bits = ['<h2>Divisions</h2><p class="ty-muted ty-sm sm">These are the skill levels for this sport. All levels stays available on each session and is not stored here.</p><div class=mlist>']
    if not rows:
        bits.append('<p class="ty-muted ty-sm sm" style="padding:12px 16px">No divisions yet.</p>')
    for i, row in enumerate(rows):
        bits.append(_row("/manage/club/programs/%s/divisions/%d" % (program["slug"], row["id"]), row["name"], row["description"] or "No description"))
    bits.append(_row("/manage/club/programs/%s/divisions/new" % program["slug"], "Add division", "Name and a one-line description"))
    bits.append("</div>")
    return "".join(bits)


def role_rules_html(d, program, role):
    label = dict(REQ_GROUPS).get(role, role)
    bits = ['<div class=mlist>']
    rows = rules_for(d, program["id"], role)
    if not rows:
        bits.append('<p class="ty-muted ty-sm sm" style="padding:12px 16px">No requirements yet.</p>')
    for row in rows:
        bits.append(_row("/manage/club/programs/%s/rules/%d" % (program["slug"], row["id"]), row["name"], _rule_note(d, program, row)))
    bits.append(_row("/manage/club/programs/%s/rules/new?role=%s" % (program["slug"], role), "Add requirement", "For %s" % label.lower()))
    bits.append("</div>")
    return "".join(bits)


def _select(options, current):
    return "".join('<option value="%s"%s>%s</option>' % (value, " selected" if value == current else "", label) for value, label in options)


def rule_edit_html(d, program, rule, csrf, preset_role=""):
    req_id = rule["requirement_id"] if rule else None
    roles = set(_csv(rule["roles"])) if rule else set()
    if preset_role and not rule:
        roles.add(preset_role)
    defs = d.execute("SELECT id, name FROM requirements WHERE active=1 ORDER BY name").fetchall()
    options = ['<option value="">Choose a requirement</option>']
    for item in defs:
        options.append('<option value="%d"%s>%s</option>' % (item["id"], " selected" if item["id"] == req_id else "", escape(item["name"])))
    role_bits = "".join('<label class=checkline><input type=checkbox name="role_%s" value=1%s> %s</label>' % (
        code, " checked" if code in roles else "", label) for code, label in REQ_GROUPS)
    timing = rule["timing"] if rule else "before_first"
    verify = rule["verification"] if rule else "review"
    kind = "custom"
    if rule:
        current = d.execute("SELECT kind FROM requirements WHERE id=?", (rule["requirement_id"],)).fetchone()
        kind = (current["kind"] if current and current["kind"] else "custom")
    within = rule["within_days"] if rule else 0
    remove = ""
    if rule:
        remove = """<form method=post style="margin-top:12px">%s<input type=hidden name=action value=remove><button class="rg-btn danger full" type=submit>Remove from this sport</button></form>""" % csrf
    return """<form method=post class=clubform style="padding-bottom:120px">%s
<label>Requirement<select name=requirement>%s</select></label>
<p class="ty-muted ty-sm sm">Or create one. An existing name is reused, not copied.</p>
<label>New name<input name=new_name placeholder="Leave blank to use the requirement above"></label>
<label>Kind<select name=kind>%s</select></label>
<p>Who</p>
%s
<label class=checkline><input type=checkbox name=enforced value=1%s> Enforced</label>
<label>When<select name=timing>%s</select></label>
<label>Days<input name=within_days inputmode=numeric value="%s"></label>
<label>Verification<select name=verification>%s</select></label>
<label class=checkline><input type=checkbox name=tracks_expiration value=1%s> Track expiration</label>
<button class="rg-btn primary full" type=submit>Save</button>
</form>%s""" % (
        csrf, "".join(options), _select(KIND_LABELS, kind), role_bits,
        " checked" if rule and rule["enforced"] else "",
        _select(TIMING_RULE, timing), escape(str(within or "")),
        _select(VERIFY_RULE, verify),
        " checked" if rule and rule["tracks_expiration"] else "",
        remove)


def save_program_rule(d, program, rule_id, form):
    """Attach a definition to this sport. Does not change other sports or member records."""
    name = " ".join((form.get("new_name") or "").split())
    req_raw = (form.get("requirement") or "").strip()
    if name:
        kind = form.get("kind") if form.get("kind") in dict(KIND_LABELS) else "custom"
        found = d.execute("SELECT id FROM requirements WHERE lower(name)=?", (name.casefold(),)).fetchone()
        if found:
            req_id = found["id"]
        else:
            req_id = d.execute("INSERT INTO requirements(name, applies_to, keywords, expires, active, kind) VALUES(?,?,?,?,1,?)",
                               (name[:80], "athlete", _slug(name)[:40], 1 if form.get("tracks_expiration") else 0, kind)).lastrowid
            d.execute("""INSERT INTO requirement_scopes(requirement_id, description, category, issuer, activities, roles, everyone, effect, affects_clearance, verification, review_status)
                VALUES(?,?,?,?,?,?,?,?,?,?,?)""", (req_id, "", "", "", "", "", 0, "info", 0, "manual", "needs_review"))
    elif req_raw.isdigit():
        req_id = int(req_raw)
        if not d.execute("SELECT 1 FROM requirements WHERE id=?", (req_id,)).fetchone():
            raise ValueError("Choose a requirement.")
    else:
        raise ValueError("Choose a requirement.")
    roles = [code for code, _label in REQ_GROUPS if form.get("role_%s" % code)]
    if not roles:
        raise ValueError("Choose who this applies to.")
    timing = form.get("timing") if form.get("timing") in dict(TIMING_RULE) else "before_first"
    try:
        within = int(form.get("within_days") or 0)
    except ValueError:
        within = 0
    if timing == "within_days" and within < 1:
        raise ValueError("Add how many days.")
    if timing != "within_days":
        within = 0
    verification = form.get("verification") if form.get("verification") in dict(VERIFY_RULE) else "review"
    enforced = 1 if form.get("enforced") else 0
    tracks = 1 if form.get("tracks_expiration") else 0
    if rule_id:
        row = d.execute("SELECT id FROM program_rules WHERE id=? AND program_id=?", (rule_id, program["id"])).fetchone()
        if not row:
            raise ValueError("That requirement is no longer on this sport.")
        d.execute("""UPDATE program_rules SET requirement_id=?, roles=?, everyone=0, enforced=?, timing=?, within_days=?, verification=?, tracks_expiration=?
            WHERE id=?""", (req_id, ",".join(roles), enforced, timing, within, verification, tracks, rule_id))
    else:
        found = d.execute("SELECT id FROM program_rules WHERE program_id=? AND requirement_id=?", (program["id"], req_id)).fetchone()
        if found:
            rule_id = found["id"]
            d.execute("""UPDATE program_rules SET roles=?, everyone=0, enforced=?, timing=?, within_days=?, verification=?, tracks_expiration=?
                WHERE id=?""", (",".join(roles), enforced, timing, within, verification, tracks, rule_id))
        else:
            rule_id = d.execute("""INSERT INTO program_rules(program_id, requirement_id, roles, everyone, enforced, timing, within_days, verification, tracks_expiration)
                VALUES(?,?,?,0,?,?,?,?,?)""", (program["id"], req_id, ",".join(roles), enforced, timing, within, verification, tracks)).lastrowid
    d.execute("INSERT OR IGNORE INTO requirement_programs(requirement_id, program_id) VALUES(?,?)", (req_id, program["id"]))
    return rule_id


def remove_program_rule(d, program, rule_id):
    row = d.execute("SELECT requirement_id FROM program_rules WHERE id=? AND program_id=?", (rule_id, program["id"])).fetchone()
    if not row:
        return
    d.execute("DELETE FROM program_rules WHERE id=?", (rule_id,))
    d.execute("DELETE FROM requirement_programs WHERE requirement_id=? AND program_id=?", (row["requirement_id"], program["id"]))


def compliance_html(d):
    bits = ['<p class="ty-muted ty-sm sm">Each requirement is defined once and can apply to one sport, several, or all of them.</p><div class=mlist>']
    rows = d.execute("SELECT * FROM requirements WHERE active=1 ORDER BY name").fetchall()
    if not rows:
        bits.append('<p class="ty-muted ty-sm sm" style="padding:12px 16px">No requirements yet.</p>')
    labels = dict(KIND_LABELS)
    for row in rows:
        n = d.execute("SELECT COUNT(*) FROM program_rules WHERE requirement_id=?", (row["id"],)).fetchone()[0]
        sport = "all sports" if n and n == d.execute("SELECT COUNT(*) FROM programs").fetchone()[0] else ("%d sports" % n if n != 1 else "1 sport")
        bits.append(_row("/manage/club/compliance/%d" % row["id"], row["name"], "%s · %s" % (labels.get(row["kind"] or "custom", "Custom"), sport)))
    bits.append("</div>")
    bits.append('<p style="margin-top:16px"><a class="rg-btn primary full" href="/manage/club/compliance/new">Add requirement</a></p>')
    return "".join(bits)


def definition_edit_html(d, req, csrf):
    kind = req["kind"] if req and "kind" in req.keys() else "custom"
    scope = None
    linked = set()
    if req:
        scope = d.execute("SELECT description FROM requirement_scopes WHERE requirement_id=?", (req["id"],)).fetchone()
        linked = {row["program_id"] for row in d.execute("SELECT program_id FROM program_rules WHERE requirement_id=?", (req["id"],)).fetchall()}
    boxes = []
    programs_all = programs(d)
    for program in programs_all:
        boxes.append('<label class=checkline><input type=checkbox name=program value="%d"%s> %s</label>' % (
            program["id"], " checked" if program["id"] in linked else "", escape(program["name"])))
    return """<form method=post class=clubform style="padding-bottom:120px">%s
<label>Name<input name=name required value="%s"></label>
<label>Kind<select name=kind>%s</select></label>
<label>Description<textarea class=planfield name=description rows=3>%s</textarea></label>
<p>Sports</p>
<label class=checkline><input type=checkbox name=all_sports value=1%s> All sports</label>
%s
<p class="ty-muted ty-sm sm">Unchecking a sport removes the rule from that sport. It does not delete the definition or anyone's record.</p>
<button class="rg-btn primary full" type=submit>Save</button>
</form>""" % (
        csrf, escape(req["name"] if req else ""), _select(KIND_LABELS, kind or "custom"),
        escape(scope["description"] if scope else ""),
        " checked" if programs_all and linked and linked >= {row["id"] for row in programs_all} else "",
        "".join(boxes))


def save_definition(d, req_id, form):
    name = " ".join((form.get("name") or "").split())
    if len(name) < 2:
        raise ValueError("Add a name.")
    kind = form.get("kind") if form.get("kind") in dict(KIND_LABELS) else "custom"
    other = d.execute("SELECT id FROM requirements WHERE lower(name)=? AND id!=?", (name.casefold(), req_id or 0)).fetchone()
    if other:
        raise ValueError("That requirement already exists.")
    description = (form.get("description") or "")[:500]
    if req_id:
        d.execute("UPDATE requirements SET name=?, kind=?, active=1 WHERE id=?", (name[:80], kind, req_id))
    else:
        req_id = d.execute("INSERT INTO requirements(name, applies_to, keywords, expires, active, kind) VALUES(?,?,?,?,1,?)",
                           (name[:80], "athlete", _slug(name)[:40], 0, kind)).lastrowid
    if d.execute("SELECT 1 FROM requirement_scopes WHERE requirement_id=?", (req_id,)).fetchone():
        d.execute("UPDATE requirement_scopes SET description=? WHERE requirement_id=?", (description, req_id))
    else:
        d.execute("""INSERT INTO requirement_scopes(requirement_id, description, category, issuer, activities, roles, everyone, effect, affects_clearance, verification, review_status)
            VALUES(?,?,?,?,?,?,?,?,?,?,?)""", (req_id, description, "", "", "", "", 0, "info", 0, "manual", "needs_review"))
    if form.get("all_sports"):
        chosen = [row["id"] for row in programs(d)]
    else:
        chosen = [int(v) for v in form.getlist("program") if str(v).isdigit()]
    have = {row["program_id"]: row["id"] for row in d.execute("SELECT id, program_id FROM program_rules WHERE requirement_id=?", (req_id,)).fetchall()}
    for pid in chosen:
        if pid in have:
            continue
        d.execute("""INSERT INTO program_rules(program_id, requirement_id, roles, everyone, enforced, timing, within_days, verification, tracks_expiration)
            VALUES(?,?,?,0,0,'before_first',0,'review',0)""", (pid, req_id, _default_roles(kind)))
        d.execute("INSERT OR IGNORE INTO requirement_programs(requirement_id, program_id) VALUES(?,?)", (req_id, pid))
    for pid, rule_id in have.items():
        if pid not in chosen:
            d.execute("DELETE FROM program_rules WHERE id=?", (rule_id,))
            d.execute("DELETE FROM requirement_programs WHERE requirement_id=? AND program_id=?", (req_id, pid))
    return req_id


def venues_html(d):
    bits = ['<p class="ty-muted ty-sm sm">A venue is a place. Days, times, and coaches stay on Schedule and People.</p><div class=mlist>']
    rows = d.execute("SELECT * FROM venues ORDER BY name").fetchall()
    if not rows:
        bits.append('<p class="ty-muted ty-sm sm" style="padding:12px 16px">No venues yet.</p>')
    for row in rows:
        names = [item["name"] for item in d.execute("""SELECT p.name FROM venue_programs vp
            JOIN programs p ON p.id=vp.program_id WHERE vp.venue_id=? ORDER BY p.name""", (row["id"],)).fetchall()]
        desc = row["address"] or "No address"
        if names:
            desc = "%s · %s" % (", ".join(names), desc)
        bits.append(_row("/manage/club/venues/%d" % row["id"], row["name"], desc))
    bits.append("</div>")
    bits.append('<p style="margin-top:16px"><a class="rg-btn primary full" href="/manage/club/venues/new">Add venue</a></p>')
    return "".join(bits)


def venue_edit_html(d, venue, csrf):
    linked = set()
    if venue:
        linked = {row["program_id"] for row in d.execute("SELECT program_id FROM venue_programs WHERE venue_id=?", (venue["id"],)).fetchall()}
    boxes = []
    for program in programs(d):
        boxes.append('<label class=checkline><input type=checkbox name=program value="%d"%s> %s</label>' % (
            program["id"], " checked" if program["id"] in linked else "", escape(program["name"])))
    remove = ""
    if venue:
        remove = """<form method=post style="margin-top:12px">%s<input type=hidden name=action value=remove><button class="rg-btn danger full" type=submit>Remove venue</button></form>""" % csrf
    return """<form method=post class=clubform style="padding-bottom:120px">%s
<label>Name<input name=name required value="%s"></label>
<label>Address<input name=address value="%s"></label>
<label>Instructions<textarea class=planfield name=instructions rows=3>%s</textarea></label>
<p>Sports</p>
%s
<p class="ty-muted ty-sm sm">Unchecking a sport removes the link. Sessions that already use this place are left as they are.</p>
<button class="rg-btn primary full" type=submit>Save</button>
</form>%s""" % (
        csrf, escape(venue["name"] if venue else ""), escape(venue["address"] if venue else ""),
        escape(venue["instructions"] if venue else ""), "".join(boxes) or "<p class='ty-muted ty-sm'>No sports yet.</p>", remove)


def save_venue(d, venue_id, form):
    name = " ".join((form.get("name") or "").split())
    if len(name) < 2:
        raise ValueError("Add a name.")
    address = " ".join((form.get("address") or "").split())[:200]
    instructions = (form.get("instructions") or "")[:500]
    if venue_id:
        row = d.execute("SELECT id FROM venues WHERE id=?", (venue_id,)).fetchone()
        if not row:
            raise ValueError("That venue is gone.")
        d.execute("UPDATE venues SET name=?, address=?, instructions=? WHERE id=?", (name[:120], address, instructions, venue_id))
    else:
        venue_id = d.execute("INSERT INTO venues(name, address, instructions) VALUES(?,?,?)", (name[:120], address, instructions)).lastrowid
    chosen = [int(v) for v in form.getlist("program") if str(v).isdigit()]
    d.execute("DELETE FROM venue_programs WHERE venue_id=?", (venue_id,))
    for pid in chosen:
        d.execute("INSERT OR IGNORE INTO venue_programs(venue_id, program_id) VALUES(?,?)", (venue_id, pid))
    return venue_id


def remove_venue(d, venue_id):
    d.execute("DELETE FROM venue_programs WHERE venue_id=?", (venue_id,))
    d.execute("DELETE FROM venues WHERE id=?", (venue_id,))


def venue_suggestions(d, q, sport=""):
    """Club venues, with the session's sport first."""
    rows = d.execute("SELECT * FROM venues ORDER BY name").fetchall()
    wanted = None
    if sport:
        program = program_for_label(d, sport)
        wanted = program["id"] if program else None
    ranked = []
    for row in rows:
        linked = [item["program_id"] for item in d.execute("SELECT program_id FROM venue_programs WHERE venue_id=?", (row["id"],)).fetchall()]
        if wanted and wanted not in linked and linked:
            continue
        if q and not _place_hit_local(q, row["name"], row["address"]):
            continue
        ranked.append(row)
    if wanted:
        ranked.sort(key=lambda row: 0 if d.execute("SELECT 1 FROM venue_programs WHERE venue_id=? AND program_id=?", (row["id"], wanted)).fetchone() else 1)
    return ranked


def _place_hit_local(q, name, detail=""):
    needle = " ".join(str(q or "").casefold().split())
    blob = " ".join(str(name or "").casefold().split()) + " " + " ".join(str(detail or "").casefold().split())
    if not needle:
        return True
    if needle in blob:
        return True
    return all(part in blob for part in needle.split())


def sport_leadership_html(d, program):
    rows = d.execute("SELECT * FROM leadership_roles WHERE program_id=? ORDER BY sort, id", (program["id"],)).fetchall()
    bits = ['<h2>Leadership</h2><p class="ty-muted ty-sm sm">Roles for this sport. Sport admin is a title. It does not open club settings.</p><div class=mlist>']
    if not rows:
        bits.append('<p class="ty-muted ty-sm sm" style="padding:12px 16px">No roles yet.</p>')
    for row in rows:
        n = d.execute("SELECT COUNT(*) FROM leadership_members WHERE role_id=?", (row["id"],)).fetchone()[0]
        bits.append(_row("/manage/club/programs/%s/leadership/%d" % (program["slug"], row["id"]), row["name"], "%s · %d %s" % (dict(PERM_SPORT).get(row["permission"], row["permission"]), n, "person" if n == 1 else "people")))
    bits.append(_row("/manage/club/programs/%s/leadership/new" % program["slug"], "Add role", "Name, permission, and people"))
    bits.append("</div>")
    return "".join(bits)


ADMIN_LEVELS = (("admin", "Admin"), ("admin_lite", "Admin lite"), ("sport_admin", "Sport admin"))


def _person_name(person):
    return ("%s %s" % (person["preferred_first"] or person["first"], person["last"] or "")).strip()


def admin_level_roles(d):
    return d.execute("""SELECT r.*, p.name AS program_name, p.slug AS program_slug
        FROM leadership_roles r LEFT JOIN programs p ON p.id=r.program_id
        WHERE r.permission IN ('admin', 'admin_lite', 'sport_admin')
        ORDER BY CASE r.permission WHEN 'admin' THEN 0 WHEN 'admin_lite' THEN 1 ELSE 2 END, p.name, r.name""").fetchall()


def permission_holders(d):
    """People who already have Admin, Admin lite, or Sport admin. Read only."""
    levels = dict(ADMIN_LEVELS)
    grants = d.execute("""SELECT m.id AS member_id, m.first, m.preferred_first, m.last, m.is_admin,
            r.id AS role_id, r.name AS role_name, r.permission, p.name AS program_name
        FROM leadership_members lm
        JOIN leadership_roles r ON r.id=lm.role_id
        JOIN members m ON m.id=lm.member_id
        LEFT JOIN programs p ON p.id=r.program_id
        WHERE r.permission IN ('admin', 'admin_lite', 'sport_admin')
          AND COALESCE(m.role,'')!='system'
        ORDER BY m.last, m.first, r.name""").fetchall()
    covered = {row["member_id"] for row in grants if row["permission"] == "admin"}
    rows = []
    for row in grants:
        label = levels.get(row["permission"], row["permission"])
        if row["program_name"]:
            desc = "%s · %s · %s" % (row["role_name"], row["program_name"], label)
        else:
            desc = "%s · %s" % (row["role_name"], label)
        rows.append({"id": row["member_id"], "name": _person_name(row), "desc": desc})
    for person in d.execute("""SELECT id, first, preferred_first, last FROM members
            WHERE is_admin=1 AND COALESCE(role,'')!='system' ORDER BY last, first""").fetchall():
        if person["id"] in covered:
            continue
        rows.append({"id": person["id"], "name": _person_name(person), "desc": "Admin"})
    rows.sort(key=lambda row: (row["name"].casefold(), row["desc"].casefold()))
    return rows


def permissions_html(d):
    bits = ['<p class="ty-muted ty-sm sm">Admin, Admin lite, and Sport admin. Opening this list does not change anyone.</p><div class=mlist>']
    rows = permission_holders(d)
    if not rows:
        bits.append('<p class="ty-muted ty-sm sm" style="padding:12px 16px">No admin-level access yet.</p>')
    for row in rows:
        bits.append(_row("/manage/club/permissions/%d" % row["id"], row["name"], row["desc"]))
    bits.append(_row("/manage/club/permissions/new", "Assign", "Add someone to an existing admin-level role"))
    bits.append("</div>")
    return "".join(bits)


def permission_edit_html(d, member, csrf):
    roles = admin_level_roles(d)
    held = set()
    if member:
        held = {row["role_id"] for row in d.execute("""SELECT lm.role_id FROM leadership_members lm
            JOIN leadership_roles r ON r.id=lm.role_id
            WHERE lm.member_id=? AND r.permission IN ('admin', 'admin_lite', 'sport_admin')""", (member["id"],)).fetchall()}
    people = d.execute("""SELECT id, first, preferred_first, last FROM members
        WHERE COALESCE(role,'')!='system' ORDER BY last, first""").fetchall()
    if member:
        who = '<p class="ty-muted ty-sm sm">%s</p>' % escape(_person_name(member))
    else:
        options = ['<option value="">Choose a person</option>']
        for person in people:
            options.append('<option value="%d">%s</option>' % (person["id"], escape(_person_name(person))))
        who = '<label>Person<select name=person required>%s</select></label>' % "".join(options)
    boxes = []
    for role in roles:
        label = dict(ADMIN_LEVELS).get(role["permission"], role["permission"])
        title = role["name"]
        if role["program_name"]:
            title = "%s · %s" % (role["name"], role["program_name"])
        boxes.append('<label class=checkline><input type=checkbox name=role value="%d"%s> %s · %s</label>' % (
            role["id"], " checked" if role["id"] in held else "", escape(title), escape(label)))
    locked = ""
    if member and member["is_admin"]:
        locked = '<p class="ty-muted ty-sm sm">Account admin stays on this person. Removing a role does not take it away.</p>'
    empty = ""
    if not roles:
        empty = '<p class="ty-muted ty-sm sm">No admin-level role exists yet. Club Leadership is where those roles are defined.</p><p><a class="rg-btn secondary" href="/manage/club/leadership">Leadership</a></p>'
    return """<form method=post class=clubform style="padding-bottom:120px">%s
%s
<p>Roles</p>
%s
%s
%s
<button class="rg-btn primary full" type=submit>Save</button>
</form>""" % (csrf, who, "".join(boxes) or empty, locked,
              '<p class="ty-muted ty-sm sm">Saving adds or removes only these roles. It never removes an existing admin.</p>' if roles else "")


def save_permission_assignment(d, member_id, form):
    """Add or remove admin-level role membership. Never clears is_admin."""
    if member_id is None:
        raw = form.get("person") or ""
        if not str(raw).isdigit():
            raise ValueError("Choose a person.")
        member_id = int(raw)
    member = d.execute("SELECT id FROM members WHERE id=? AND COALESCE(role,'')!='system'", (member_id,)).fetchone()
    if not member:
        raise ValueError("Choose a person.")
    roles = {row["id"]: row["permission"] for row in admin_level_roles(d)}
    wanted = {int(v) for v in form.getlist("role") if str(v).isdigit() and int(v) in roles}
    current = {row["role_id"] for row in d.execute("""SELECT lm.role_id FROM leadership_members lm
        JOIN leadership_roles r ON r.id=lm.role_id
        WHERE lm.member_id=? AND r.permission IN ('admin', 'admin_lite', 'sport_admin')""", (member_id,)).fetchall()}
    for role_id in wanted - current:
        d.execute("INSERT OR IGNORE INTO leadership_members(role_id, member_id) VALUES(?,?)", (role_id, member_id))
        if roles[role_id] == "admin":
            d.execute("UPDATE members SET is_admin=1 WHERE id=? AND COALESCE(role,'')!='system'", (member_id,))
    for role_id in current - wanted:
        d.execute("DELETE FROM leadership_members WHERE role_id=? AND member_id=?", (role_id, member_id))
    return member_id


def leadership_list_html(d):
    rows = d.execute("SELECT * FROM leadership_roles WHERE program_id IS NULL ORDER BY sort, id").fetchall()
    bits = ['<div class=mlist>']
    if not rows:
        bits.append('<p class="ty-muted ty-sm sm" style="padding:12px 16px">No club roles yet.</p>')
    for row in rows:
        n = d.execute("SELECT COUNT(*) FROM leadership_members WHERE role_id=?", (row["id"],)).fetchone()[0]
        bits.append(_row("/manage/club/leadership/%d" % row["id"], row["name"], "%s · %d %s" % (dict(PERM_CLUB).get(row["permission"], row["permission"]), n, "person" if n == 1 else "people")))
    bits.append("</div>")
    bits.append('<p style="margin-top:16px"><a class="rg-btn primary full" href="/manage/club/leadership/new">Add role</a></p>')
    return "".join(bits)


def leadership_edit_html(d, role, csrf, program=None):
    perms = PERM_SPORT if program else PERM_CLUB
    current = role["permission"] if role else "none"
    chosen = set()
    if role:
        chosen = {row["member_id"] for row in d.execute("SELECT member_id FROM leadership_members WHERE role_id=?", (role["id"],)).fetchall()}
    people = d.execute("""SELECT id, first, preferred_first, last FROM members
        WHERE COALESCE(role,'')!='system' ORDER BY last, first""").fetchall()
    boxes = []
    for person in people:
        name = ("%s %s" % (person["preferred_first"] or person["first"], person["last"] or "")).strip()
        boxes.append('<label class=checkline><input type=checkbox name=person value="%d"%s> %s</label>' % (
            person["id"], " checked" if person["id"] in chosen else "", escape(name)))
    options = "".join('<option value="%s"%s>%s</option>' % (value, " selected" if value == current else "", escape(label)) for value, label in perms)
    note = "Admin opens the whole club. Admin lite can run schedule and lineup the way an active coach can, and cannot open Club, plans, or People. Removing a role never removes an existing admin." if not program else "Sport admin is a title for this sport. It does not grant club admin or schedule access by itself."
    return """<form method=post class=clubform>%s
<label>Name<input name=name required value="%s"></label>
<label>Permission<select name=permission>%s</select></label>
<p class="ty-muted ty-sm sm">%s</p>
<p>People</p>
%s
<button class="rg-btn primary full" type=submit>Save</button>
</form>""" % (csrf, escape(role["name"] if role else ""), options, escape(note), "".join(boxes) or "<p class='ty-muted ty-sm'>No people yet.</p>")


def schedule_day_edit_html(program, row, csrf, attempt=None):
    chosen = ""
    start = end = ""
    if attempt is not None:
        chosen = (attempt.get("weekday") or "").strip().lower()
        start = attempt.get("start") or ""
        end = attempt.get("end") or ""
    elif row:
        chosen = row["weekday"]
        start, end = row["start"], row["end"]
    options = []
    for code, label in WEEKDAYS:
        full = {"mon": "Monday", "tue": "Tuesday", "wed": "Wednesday", "thu": "Thursday", "fri": "Friday", "sat": "Saturday", "sun": "Sunday"}[code]
        options.append('<option value="%s"%s>%s</option>' % (code, " selected" if code == chosen else "", full))
    remove = ""
    if row:
        remove = """<form method=post style="margin-top:12px">%s<input type=hidden name=action value=remove><button class="rg-btn danger full" type=submit>Remove</button></form>""" % csrf
    return """<form method=post class=clubform style="padding-bottom:120px">%s
<label>Day<select name=weekday>%s</select></label>
<div class=row><label>Start<input type=time name=start required value="%s"></label><label>End<input type=time name=end required value="%s"></label></div>
<button class="rg-btn primary full" type=submit>Save</button>
</form>%s""" % (csrf, "".join(options), escape(start), escape(end), remove)


def division_edit_html(d, program, row, csrf):
    extra = ""
    if row:
        extra = """<form method=post>%s<input type=hidden name=action value=up><button class="rg-btn secondary full" type=submit>Move up</button></form>
<form method=post>%s<input type=hidden name=action value=down><button class="rg-btn secondary full" type=submit>Move down</button></form>
<form method=post>%s<input type=hidden name=action value=remove><button class="rg-btn danger full" type=submit>Remove</button></form>""" % (csrf, csrf, csrf)
    return """<form method=post class=clubform>%s
<label>Name<input name=name required value="%s"></label>
<label>Description<input name=description value="%s"></label>
<button class="rg-btn primary full" type=submit>Save</button>
</form>%s""" % (csrf, escape(row["name"] if row else ""), escape(row["description"] if row else ""), extra)


PASS_COLUMNS = (
    ("description", "TEXT NOT NULL DEFAULT ''"),
    ("currency", "TEXT NOT NULL DEFAULT 'USD'"),
    ("renewal", "TEXT NOT NULL DEFAULT 'indefinite'"),
    ("renewal_count", "INTEGER NOT NULL DEFAULT 0"),
    ("frequency", "TEXT NOT NULL DEFAULT 'month'"),
    ("length_mode", "TEXT NOT NULL DEFAULT ''"),
    ("length_days", "INTEGER NOT NULL DEFAULT 0"),
    ("length_sessions", "INTEGER NOT NULL DEFAULT 0"),
    ("audience", "TEXT NOT NULL DEFAULT 'everyone'"),
    ("one_per_person", "INTEGER NOT NULL DEFAULT 0"),
    ("uses_per_event", "INTEGER NOT NULL DEFAULT 0"),
    ("lineup_categories", "TEXT NOT NULL DEFAULT ''"),
    ("event_ids", "TEXT NOT NULL DEFAULT ''"),
    ("active_from", "TEXT NOT NULL DEFAULT ''"),
    ("active_until", "TEXT NOT NULL DEFAULT ''"),
    ("archived", "INTEGER NOT NULL DEFAULT 0"),
    ("terms", "TEXT NOT NULL DEFAULT ''"),
    ("offer_code", "TEXT NOT NULL DEFAULT ''"),
)
PASS_KINDS = (
    ("monthly", "Membership (recurring)"),
    ("drop_in", "Drop-in (single session)"),
    ("pass", "Multi-session pack"),
    ("trial", "Free trial"),
    ("free", "Free"),
)
KIND_WORD = {"monthly": "Membership", "drop_in": "Drop-in", "pass": "Multi-session pack", "trial": "Free trial", "free": "Free"}
FREQS = (("week", "week"), ("month", "month"), ("year", "year"))
LINEUP_CATS = (("competitions", "Competitions"), ("camps", "Camps"), ("trips", "Trips"), ("community", "Community"))
ACTIVITIES = (("practice", "Practice"), ("scrimmage", "Scrimmage"), ("game", "Game"))


def _ensure_pass_columns(d):
    cols = {row[1] for row in d.execute("PRAGMA table_info(payment_plans)")}
    if not cols:
        return
    for name, decl in PASS_COLUMNS:
        if name not in cols:
            d.execute("ALTER TABLE payment_plans ADD COLUMN %s %s" % (name, decl))
    d.execute("""CREATE TABLE IF NOT EXISTS plan_people(
        plan_id INTEGER NOT NULL, member_id INTEGER NOT NULL, PRIMARY KEY(plan_id, member_id))""")


def _provider_id(d, kind):
    row = d.execute("SELECT id FROM payment_providers WHERE kind=? ORDER BY id LIMIT 1", (kind,)).fetchone()
    return row["id"] if row else None


def _pass_date(raw, label):
    text = (raw or "").strip()
    if not text:
        return ""
    if not __import__("re").fullmatch(r"\d{4}-\d{2}-\d{2}", text):
        raise ValueError("Use a date for %s." % label)
    try:
        dt.date.fromisoformat(text)
    except ValueError as exc:
        raise ValueError("Use a date for %s." % label) from exc
    return text


def _dollars(raw):
    text = (raw or "").strip().replace("$", "").replace(",", "")
    if not text:
        return None
    if not __import__("re").fullmatch(r"\d+(\.\d{1,2})?", text):
        raise ValueError("Use a price like 45 or 45.00.")
    return int(round(float(text) * 100))


def _price_rows(d, plan_id):
    try:
        return d.execute("SELECT * FROM payment_prices WHERE plan_id=? ORDER BY effective_on", (plan_id,)).fetchall()
    except Exception:
        return []


def _shown_price(rows, today):
    current = None
    for row in rows:
        if row["effective_on"] <= today:
            current = row
    if current:
        return current["amount_cents"], ""
    future = [row for row in rows if row["effective_on"] > today]
    if future:
        return future[0]["amount_cents"], future[0]["effective_on"]
    return None, ""


def _money(cents):
    cents = int(cents or 0)
    return "$%d" % (cents // 100) if cents % 100 == 0 else "$%d.%02d" % (cents // 100, cents % 100)


def _period(plan):
    kind = plan["kind"] if plan else ""
    if kind == "monthly":
        freq = (plan["frequency"] or "month") if "frequency" in plan.keys() else "month"
        return "/ " + (freq if freq in ("week", "month", "year") else "month")
    if kind == "drop_in":
        return "/ session"
    if kind == "pass":
        count = plan["length_sessions"] if plan and "length_sessions" in plan.keys() else 0
        return "for %d sessions" % count if count else "/ pack"
    return ""


def _pretty_date(iso):
    day = dt.date.fromisoformat(str(iso)[:10])
    return "%s %d, %d" % (day.strftime("%b"), day.day, day.year)


def window_phrase(plan):
    """How long the pass covers events. Empty dates mean right away and indefinitely."""
    keys = plan.keys() if plan is not None and hasattr(plan, "keys") else []
    start = str(plan["active_from"] or "")[:10] if plan is not None and "active_from" in keys else ""
    end = str(plan["active_until"] or "")[:10] if plan is not None and "active_until" in keys else ""
    if start and end:
        return "%s to %s" % (_pretty_date(start), _pretty_date(end))
    if start:
        return "%s · No end date" % _pretty_date(start)
    if end:
        return "No start date to %s" % _pretty_date(end)
    return "No end date"


def pass_covers_date(plan, day):
    """True when an event date falls in the pass window. Blank dates do not limit it."""
    if not plan:
        return False
    keys = plan.keys() if hasattr(plan, "keys") else []
    start = str(plan["active_from"] or "")[:10] if "active_from" in keys else ""
    end = str(plan["active_until"] or "")[:10] if "active_until" in keys else ""
    day = str(day or "")[:10]
    if not day:
        return True
    if start and day < start:
        return False
    if end and day > end:
        return False
    return True


def pass_summary(plan, program_names, cents, starts):
    """One line such as '$45 / month · Water Polo practices'."""
    kind = plan["kind"] if plan else "monthly"
    if kind in ("trial", "free") or cents is None:
        price = "Free" if kind in ("trial", "free") else "Price not set"
    else:
        price = _money(cents) + " " + _period(plan)
        if starts:
            price += " from " + starts
    acts = _csv(plan["activities"] if plan and "activities" in plan.keys() else "")
    act = ""
    if acts == ["practice"]:
        act = " practices"
    elif acts:
        act = " " + ", ".join(acts)
    names = program_names or ["No sport yet"]
    return "%s · %s%s" % (price.strip(), ", ".join(names), act)


def visible_plans(d):
    _ensure_pass_columns(d)
    return d.execute("SELECT * FROM payment_plans WHERE COALESCE(archived,0)=0 ORDER BY active DESC, name").fetchall()


def _seed_passes(d):
    """Map the existing monthly plan and archive the rest. Does not delete rows or RSVPs."""
    if _meta(d, "passes_v1") == "1":
        return
    _ensure_pass_columns(d)
    if not d.execute("SELECT 1 FROM payment_plans LIMIT 1").fetchone():
        _set_meta(d, "passes_v1", "1")
        return
    wp = program_by_slug(d, "water-polo")
    wp_id = wp["id"] if wp else None
    keep = []
    monthly = d.execute("SELECT * FROM payment_plans WHERE kind='monthly' ORDER BY id LIMIT 1").fetchone()
    if monthly:
        d.execute("""UPDATE payment_plans SET name='Monthly Membership', sports='water-polo', frequency='month',
            renewal='indefinite', audience='everyone', archived=0, currency='USD' WHERE id=?""", (monthly["id"],))
        if wp_id:
            d.execute("DELETE FROM plan_programs WHERE plan_id=?", (monthly["id"],))
            d.execute("INSERT INTO plan_programs(plan_id, program_id) VALUES(?,?)", (monthly["id"], wp_id))
        keep.append(monthly["id"])
    drop = d.execute("""SELECT * FROM payment_plans WHERE kind='drop_in' AND COALESCE(archived,0)=0
        AND (sports LIKE '%water-polo%' OR lower(name) LIKE '%water polo%') ORDER BY id LIMIT 1""").fetchone()
    if drop:
        priced = _price_rows(d, drop["id"]) or (drop["external_url"] or "").strip()
        d.execute("""UPDATE payment_plans SET name='Drop-in', sports='water-polo', activities='practice', frequency='',
            length_mode='sessions', length_sessions=1, audience='everyone', archived=0, active=? WHERE id=?""",
                  (1 if priced else 0, drop["id"]))
        if wp_id:
            d.execute("DELETE FROM plan_programs WHERE plan_id=?", (drop["id"],))
            d.execute("INSERT INTO plan_programs(plan_id, program_id) VALUES(?,?)", (drop["id"], wp_id))
        keep.append(drop["id"])
    else:
        free_id = _provider_id(d, "free")
        new_id = d.execute("""INSERT INTO payment_plans(name, kind, provider_id, external_url, sports, activities, active, notes, description, currency, length_mode, length_sessions, audience, archived)
            VALUES('Drop-in','drop_in',?,'','water-polo','practice',0,'','','USD','sessions',1,'everyone',0)""", (free_id,)).lastrowid
        if wp_id:
            d.execute("INSERT INTO plan_programs(plan_id, program_id) VALUES(?,?)", (new_id, wp_id))
        keep.append(new_id)
    trial = {}
    try:
        import publicfeed
        trial = publicfeed.normalize_trial((publicfeed.load(d).get("trial") or {}))
        enabled = 1 if (publicfeed.load(d).get("trial") or {}).get("enabled") else 0
    except Exception:
        trial = {"mode": "duration", "duration_days": 14, "session_count": 2, "activities": ["practice"], "external": "usawp_trial", "first_time_only": True}
        enabled = 0
    mode = trial.get("mode") or "duration"
    days = (trial.get("duration_days") or 14) if mode == "duration" else 0
    sessions = (trial.get("session_count") or 2) if mode == "sessions" else 0
    audience = "new" if trial.get("first_time_only", True) else "everyone"
    tid = d.execute("""INSERT INTO payment_plans(name, kind, provider_id, external_url, sports, activities, quantity, active, notes,
        description, currency, renewal, frequency, length_mode, length_days, length_sessions, audience, one_per_person, offer_code, archived)
        VALUES('Water Polo 2-Week Free Trial','trial',?,'','water-polo',?,0,?,?,'','USD','','',?,?,?,?,1,?,0)""", (
            _provider_id(d, "free"), ",".join(trial.get("activities") or ["practice"]), enabled,
            "Uses the existing free-trial offer. It does not satisfy USA Water Polo.",
            mode, days, sessions, audience, trial.get("external") or "usawp_trial")).lastrowid
    if wp_id:
        d.execute("INSERT INTO plan_programs(plan_id, program_id) VALUES(?,?)", (tid, wp_id))
    keep.append(tid)
    marks = ",".join("?" * len(keep))
    d.execute("UPDATE payment_plans SET archived=1, active=0 WHERE id NOT IN (%s)" % marks, keep)
    _set_meta(d, "passes_v1", "1")


def trial_dict(d):
    """The active free-trial pass, or an inactive one so the widget can stay quiet."""
    _ensure_pass_columns(d)
    row = d.execute("""SELECT * FROM payment_plans WHERE kind='trial' AND COALESCE(archived,0)=0 ORDER BY active DESC, id LIMIT 1""").fetchone()
    if not row:
        return None
    mode = row["length_mode"] if row["length_mode"] in ("duration", "sessions") else "duration"
    return {
        "enabled": bool(row["active"]),
        "mode": mode,
        "duration_days": row["length_days"] or 14,
        "session_count": row["length_sessions"] or 2,
        "activities": _csv(row["activities"]) or ["practice"],
        "external": row["offer_code"] if row["offer_code"] in ("usawp_trial", "none") else "usawp_trial",
        "first_time_only": row["audience"] == "new" or bool(row["one_per_person"]),
        "includes": row["description"] or "",
        "visits": str(row["length_sessions"] or ""),
        "days": str(row["length_days"] or ""),
        "conditions": row["terms"] or "",
        "message": row["description"] or "",
    }


def sync_trial_from_settings(d, trial):
    """Keep the seeded trial pass aligned when the older trial form is saved."""
    _seed_passes(d)
    row = d.execute("SELECT id FROM payment_plans WHERE kind='trial' AND COALESCE(archived,0)=0 ORDER BY id LIMIT 1").fetchone()
    if not row:
        return
    try:
        import publicfeed
        trial = publicfeed.normalize_trial(trial)
    except Exception:
        return
    mode = trial.get("mode") or "duration"
    d.execute("""UPDATE payment_plans SET active=?, length_mode=?, length_days=?, length_sessions=?, activities=?, audience=?, one_per_person=?, offer_code=?
        WHERE id=?""", (
            1 if trial.get("enabled") else 0, mode,
            (trial.get("duration_days") or 14) if mode == "duration" else 0,
            (trial.get("session_count") or 2) if mode == "sessions" else 0,
            ",".join(trial.get("activities") or ["practice"]),
            "new" if trial.get("first_time_only") else "everyone",
            1 if trial.get("first_time_only") else 0,
            trial.get("external") or "none", row["id"]))


def _push_trial_settings(d, plan):
    if plan["kind"] != "trial":
        return
    try:
        import publicfeed
    except Exception:
        return
    data = publicfeed.load(d)
    trial = dict(data.get("trial") or {})
    trial.update(trial_dict(d) or {})
    publicfeed.save_sections(d, trial=publicfeed.normalize_trial(trial))


def save_pass(d, plan_id, form):
    """Write one pass. Does not touch RSVPs, cards, or governing-body clearance."""
    _ensure_pass_columns(d)
    name = " ".join((form.get("name") or "").split())
    if len(name) < 3:
        raise ValueError("Name needs at least 3 characters.")
    kinds = dict(PASS_KINDS)
    kind = form.get("kind") or ""
    if kind not in kinds:
        raise ValueError("Choose a pass type.")
    programs = [int(v) for v in form.getlist("program") if str(v).isdigit()]
    if not programs:
        raise ValueError("Choose at least one sport.")
    activities = [a for a, _label in ACTIVITIES if form.get("activity_%s" % a)]
    cats = [a for a, _label in LINEUP_CATS if form.get("lineup_%s" % a)]
    audience = form.get("audience") or "everyone"
    if audience not in ("everyone", "new", "specific"):
        raise ValueError("Choose who can get this pass.")
    renewal = form.get("renewal") or "indefinite"
    if renewal not in ("indefinite", "fixed"):
        renewal = "indefinite"
    try:
        renewal_count = int(form.get("renewal_count") or 0)
    except ValueError:
        renewal_count = 0
    frequency = form.get("frequency") or "month"
    if frequency not in ("week", "month", "year"):
        frequency = "month"
    length_mode = form.get("length_mode") or ""
    if length_mode not in ("duration", "sessions", ""):
        length_mode = ""
    try:
        length_days = max(0, min(365, int(form.get("length_days") or 0)))
        length_sessions = max(0, min(999, int(form.get("length_sessions") or 0)))
        uses = max(0, min(99, int(form.get("uses_per_event") or 0)))
    except ValueError as exc:
        raise ValueError("Use whole numbers for the length and limits.") from exc
    pay = form.get("pay") or "none"
    if pay not in ("external", "manual", "none"):
        pay = "none"
    if kind in ("trial", "free"):
        pay = "none"
    url = (form.get("external_url") or "").strip()[:300]
    if pay != "external":
        url = url if pay == "manual" else ""
    if url and not (url.startswith("https://") or url.startswith("http://")):
        raise ValueError("The registration link has to start with https://.")
    provider_kind = {"external": "external_link", "manual": "manual", "none": "free"}[pay]
    provider = _provider_id(d, provider_kind)
    if provider:
        prow = d.execute("SELECT kind FROM payment_providers WHERE id=?", (provider,)).fetchone()
        if prow and prow["kind"] == "stripe":
            raise ValueError("Stripe is not available.")
    if kind == "trial":
        offer = "usawp_trial" if form.get("offer_code") == "usawp_trial" else "none"
    else:
        offer = ""
    active = 1 if form.get("active") == "1" else 0
    active_from = _pass_date(form.get("active_from"), "the start date")
    active_until = _pass_date(form.get("active_until"), "the end date")
    if active_from and active_until and active_until < active_from:
        raise ValueError("The end date cannot be before the start date.")
    fields = (name, kind, provider, url, ",".join(activities), (form.get("description") or "")[:500],
              "USD", renewal, renewal_count, frequency if kind == "monthly" else "",
              length_mode, length_days, length_sessions, audience, 1 if form.get("one_per_person") else 0, uses,
              ",".join(cats), active_from, active_until, (form.get("terms") or "")[:2000], offer, active)
    if plan_id:
        row = d.execute("SELECT id FROM payment_plans WHERE id=?", (plan_id,)).fetchone()
        if not row:
            raise ValueError("Choose a pass.")
        d.execute("""UPDATE payment_plans SET name=?, kind=?, provider_id=?, external_url=?, activities=?, description=?, currency=?,
            renewal=?, renewal_count=?, frequency=?, length_mode=?, length_days=?, length_sessions=?, audience=?, one_per_person=?,
            uses_per_event=?, lineup_categories=?, active_from=?, active_until=?, terms=?, offer_code=?, active=?, archived=0 WHERE id=?""", fields + (plan_id,))
    else:
        plan_id = d.execute("""INSERT INTO payment_plans(name, kind, provider_id, external_url, activities, description, currency,
            renewal, renewal_count, frequency, length_mode, length_days, length_sessions, audience, one_per_person,
            uses_per_event, lineup_categories, active_from, active_until, terms, offer_code, active, archived, sports, notes)
            VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,0,'','')""", fields).lastrowid
    cents = _dollars(form.get("price"))
    if cents is not None:
        today = dt.date.today().isoformat()
        existing = d.execute("SELECT id FROM payment_prices WHERE plan_id=? AND effective_on=?", (plan_id, today)).fetchone()
        if existing:
            d.execute("UPDATE payment_prices SET amount_cents=? WHERE id=?", (cents, existing["id"]))
        else:
            d.execute("INSERT INTO payment_prices(plan_id, amount_cents, effective_on) VALUES(?,?,?)", (plan_id, cents, today))
    d.execute("DELETE FROM plan_programs WHERE plan_id=?", (plan_id,))
    for pid in programs:
        d.execute("INSERT INTO plan_programs(plan_id, program_id) VALUES(?,?)", (plan_id, pid))
    d.execute("DELETE FROM plan_people WHERE plan_id=?", (plan_id,))
    if audience == "specific":
        for mid in form.getlist("person"):
            if str(mid).isdigit():
                d.execute("INSERT OR IGNORE INTO plan_people(plan_id, member_id) VALUES(?,?)", (plan_id, int(mid)))
    plan = d.execute("SELECT * FROM payment_plans WHERE id=?", (plan_id,)).fetchone()
    _push_trial_settings(d, plan)
    return plan_id


def plans_html(d):
    today = dt.date.today().isoformat()
    bits = ['<div class=mlist>']
    rows = visible_plans(d)
    if not rows:
        bits.append('<p class="ty-muted ty-sm sm" style="padding:12px 16px">No passes yet.</p>')
    for plan in rows:
        names = plan_program_names(d, plan["id"]) or ["No sport yet"]
        cents, starts = _shown_price(_price_rows(d, plan["id"]), today)
        price = "Free" if plan["kind"] in ("trial", "free") else ("Price not set" if cents is None else _money(cents) + " " + _period(plan))
        if starts and cents is not None and plan["kind"] not in ("trial", "free"):
            price += " from " + starts
        state = "On" if plan["active"] else "Off"
        desc = "%s · %s · %s · %s · %s" % (KIND_WORD.get(plan["kind"], plan["kind"]), price.strip(), ", ".join(names), window_phrase(plan), state)
        bits.append(_row("/manage/club/plans/%d" % plan["id"], plan["name"], desc))
    bits.append('</div><p style="margin-top:16px"><a class="rg-btn primary full" href="/manage/club/plans/new">Create pass</a></p>')
    return "".join(bits)


def _check_boxes(name, options, selected):
    chosen = set(selected)
    return "".join('<label class=checkline><input type=checkbox name="%s" value="%s"%s> %s</label>' % (
        name, escape(value), " checked" if value in chosen else "", escape(label)) for value, label in options)


def plan_edit_html(d, plan, csrf):
    plan = plan or {}
    pid = plan["id"] if plan and "id" in plan.keys() else None
    linked = set()
    people_on = set()
    if pid:
        linked = {row["program_id"] for row in d.execute("SELECT program_id FROM plan_programs WHERE plan_id=?", (pid,)).fetchall()}
        people_on = {row["member_id"] for row in d.execute("SELECT member_id FROM plan_people WHERE plan_id=?", (pid,)).fetchall()}
    today = dt.date.today().isoformat()
    prices = _price_rows(d, pid) if pid else []
    cents, starts = _shown_price(prices, today) if prices else (None, "")
    kind = plan["kind"] if plan and "kind" in plan.keys() else "monthly"
    program_boxes = []
    for program in programs(d):
        program_boxes.append('<label class=checkline><input type=checkbox name=program value="%d"%s> %s%s</label>' % (
            program["id"], " checked" if program["id"] in linked else "", escape(program["name"]),
            "" if program["active"] else " (off)"))
    acts = set(_csv(plan["activities"] if plan and "activities" in plan.keys() else "practice"))
    cats = set(_csv(plan["lineup_categories"] if plan and "lineup_categories" in plan.keys() else ""))
    people = []
    try:
        people = d.execute("""SELECT id, first, preferred_first, last FROM members
            WHERE COALESCE(role,'')!='system' ORDER BY last, first LIMIT 80""").fetchall()
    except Exception:
        people = []
    person_boxes = []
    for person in people:
        person_boxes.append((str(person["id"]), ("%s %s" % (person["preferred_first"] or person["first"], person["last"] or "")).strip()))
    pay = "none"
    if plan and plan["provider_id"]:
        prow = d.execute("SELECT kind FROM payment_providers WHERE id=?", (plan["provider_id"],)).fetchone()
        pay = {"external_link": "external", "manual": "manual", "free": "none"}.get(prow["kind"] if prow else "", "none")
    if plan and (plan["external_url"] or "") and pay == "none":
        pay = "external"
    price_lines = "".join("<p class='ty-muted ty-sm'>%s from %s</p>" % (_money(row["amount_cents"]), escape(row["effective_on"])) for row in prices)
    names = plan_program_names(d, pid) if pid else []
    blank_plan = {"kind": "monthly", "frequency": "month", "activities": "practice", "length_sessions": 0}
    core = pass_summary(plan if plan else blank_plan, names, cents, starts)
    summary = "%s · %s" % (core, window_phrase(plan if plan else None))
    active_from = str(plan["active_from"] or "")[:10] if plan and "active_from" in plan.keys() else ""
    active_until = str(plan["active_until"] or "")[:10] if plan and "active_until" in plan.keys() else ""
    freq = plan["frequency"] if plan and "frequency" in plan.keys() and plan["frequency"] else "month"
    renewal = plan["renewal"] if plan and "renewal" in plan.keys() and plan["renewal"] else "indefinite"
    length_mode = plan["length_mode"] if plan and "length_mode" in plan.keys() else ""
    audience = plan["audience"] if plan and "audience" in plan.keys() and plan["audience"] else "everyone"
    offer = plan["offer_code"] if plan and "offer_code" in plan.keys() else ""
    def sel(options, current):
        return "".join('<option value="%s"%s>%s</option>' % (value, " selected" if value == current else "", escape(label)) for value, label in options)
    return """<form method=post class="clubform passform" id=passForm>%s
<p class="ty-muted ty-sm sm">A pass grants access only. It does not satisfy USA Water Polo, USMS, or any other sport requirement, and it does not change an RSVP.</p>
<label>Name<input name=name required minlength=3 value="%s"></label>
<label>Description<textarea class=planfield name=description rows=4>%s</textarea></label>
<label>Type<select name=kind id=passKind>%s</select></label>
<label>Price<input name=price id=passPrice inputmode=decimal placeholder="45" autocomplete=off></label>
<label>Currency<select name=currency><option value=USD selected>USD</option></select></label>
<p class="ty-muted ty-sm sm">No fees are added here. A free trial or a free pass stays at no charge. Saving a price adds it from today and leaves later prices in place.</p>
%s
<div id=passRenew>
<h2>Billing and renewal</h2>
<label>Renewal<select name=renewal>%s</select></label>
<label>Number of renewals<input name=renewal_count inputmode=numeric value="%s"></label>
<label>Frequency<select name=frequency id=passFreq>%s</select></label>
</div>
<div id=passLength>
<h2>Trial or pass length</h2>
<label>Length<select name=length_mode id=passLengthMode>%s</select></label>
<label>Days<input name=length_days id=passDays inputmode=numeric value="%s"></label>
<label>Sessions<input name=length_sessions id=passSessions inputmode=numeric value="%s"></label>
</div>
<h2>Active dates</h2>
<p class="ty-muted ty-sm sm">These dates decide which events the pass covers. They are separate from renewal and from a person's paid start and end.</p>
<label class="datefield%s">Start date<input type=date name=active_from value="%s"><span class=dateph>Starts right away</span></label>
<button type=button class=textlink data-cleardate=active_from>Clear start date</button>
<label class="datefield%s">End date<input type=date name=active_until value="%s"><span class=dateph>Runs indefinitely</span></label>
<button type=button class=textlink data-cleardate=active_until>Clear end date</button>
<h2>Applies to</h2>
<p class="ty-muted ty-sm sm">Check the sports, activities, and Lineup categories this pass covers.</p>
%s
<p>Schedule activities</p>
%s
<p>Lineup categories</p>
%s
<h2>Who can get it</h2>
<label>Audience<select name=audience id=passAudience>%s</select></label>
<div id=passPeople>%s</div>
<h2>Limits</h2>
<label class=checkline><input type=checkbox name=one_per_person value=1%s> One per person</label>
<label>Uses per event<input name=uses_per_event inputmode=numeric value="%s" placeholder="0 for no limit"></label>
<h2>Where to pay</h2>
<label>Payment<select name=pay>%s</select></label>
<label>Registration URL<input name=external_url value="%s" placeholder="https://" autocomplete=off></label>
<p class="ty-muted ty-sm sm">External opens Club Assistant or another registration page. Manual is recorded by an admin. None is for a free pass or a trial. Stripe is not available.</p>
<label class=checkline id=passUsawp><input type=checkbox name=offer_code value=usawp_trial%s> Requires a USA Water Polo trial membership</label>
<label>Terms<textarea class=planfield name=terms rows=4>%s</textarea></label>
<label class=switchrow>Pass is on<span class=switch><input type=checkbox name=active value=1%s><span></span></span></label>
<div class=card id=passSummaryCard><h2>Summary</h2><p id=passSummary data-base="%s">%s</p></div>
<button class="rg-btn primary full" type=submit>Save</button>
</form>
<script>
(function(){
  var form=document.getElementById("passForm"); if(!form) return;
  var kind=document.getElementById("passKind"), freq=document.getElementById("passFreq"), mode=document.getElementById("passLengthMode");
  var summary=document.getElementById("passSummary");
  function show(id, on){ var el=document.getElementById(id); if(el) el.hidden=!on; }
  function selected(name){
    return [].slice.call(form.querySelectorAll('input[name="'+name+'"]:checked')).map(function(el){ return el.parentNode.textContent.trim(); });
  }
  function paint(){
    var k=kind.value;
    show("passRenew", k==="monthly");
    show("passLength", k==="trial"||k==="pass"||k==="drop_in");
    show("passPeople", form.querySelector('[name=audience]').value==="specific");
    show("passUsawp", k==="trial");
    var price=(form.querySelector('[name=price]').value||'').trim().replace(/^\\$/, "");
    var sports=selected("program");
    var acts=selected("activity_practice").concat(selected("activity_scrimmage"), selected("activity_game"));
    var months=["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"];
    function pretty(iso){ if(!iso) return ""; var p=iso.split("-"); return months[(+p[1]||1)-1]+" "+(+p[2])+", "+p[0]; }
    function windowLabel(){
      var s=(form.querySelector('[name=active_from]')||{}).value||"";
      var e=(form.querySelector('[name=active_until]')||{}).value||"";
      if(s && e) return pretty(s)+" to "+pretty(e);
      if(s) return pretty(s)+" · No end date";
      if(e) return "No start date to "+pretty(e);
      return "No end date";
    }
    var body;
    if(!price && summary.getAttribute("data-base")) body=summary.getAttribute("data-base");
    else {
      var money = k==="trial"||k==="free" ? "Free" : (price ? "$"+price : "Price not set");
      var period = k==="monthly" ? " / "+freq.value : (k==="drop_in" ? " / session" : (k==="pass" ? " pack" : ""));
      body = money+period+" · "+(sports.join(", ")||"No sport yet")+(acts.length?" "+acts.join(", ").toLowerCase():"");
    }
    summary.textContent = body+" · "+windowLabel();
  }
  form.querySelectorAll("[data-cleardate]").forEach(function(btn){
    btn.addEventListener("click", function(){
      var input=form.querySelector('[name="'+btn.getAttribute("data-cleardate")+'"]');
      if(!input) return;
      input.value="";
      var lab=input.closest(".datefield");
      if(lab) lab.classList.add("empty");
      input.dispatchEvent(new Event("change",{bubbles:true}));
    });
  });
  form.addEventListener("input", paint); form.addEventListener("change", paint); paint();
})();
</script>""" % (
        csrf, escape(plan["name"] if plan and "name" in plan.keys() else ""),
        escape(plan["description"] if plan and "description" in plan.keys() else ""),
        sel(PASS_KINDS, kind), price_lines,
        sel((("indefinite", "Renews indefinitely"), ("fixed", "Fixed number of renewals")), renewal),
        escape(str(plan["renewal_count"] if plan and "renewal_count" in plan.keys() else 0)),
        sel(FREQS, freq),
        sel((("", "Not set"), ("duration", "A length of time"), ("sessions", "A number of sessions")), length_mode),
        escape(str(plan["length_days"] if plan and "length_days" in plan.keys() else (14 if kind == "trial" else 0))),
        escape(str(plan["length_sessions"] if plan and "length_sessions" in plan.keys() else (1 if kind == "drop_in" else 0))),
        "" if active_from else " empty", escape(active_from),
        "" if active_until else " empty", escape(active_until),
        "".join(program_boxes),
        "".join('<label class=checkline><input type=checkbox name="activity_%s" value=1%s> %s</label>' % (value, " checked" if value in acts else "", label) for value, label in ACTIVITIES),
        "".join('<label class=checkline><input type=checkbox name="lineup_%s" value=1%s> %s</label>' % (value, " checked" if value in cats else "", label) for value, label in LINEUP_CATS),
        sel((("everyone", "Everyone"), ("new", "New members only"), ("specific", "Specific people")), audience),
        "".join('<label class=checkline><input type=checkbox name=person value="%s"%s> %s</label>' % (value, " checked" if int(value) in people_on else "", escape(label)) for value, label in person_boxes) or "<p class='ty-muted ty-sm'>No people yet.</p>",
        " checked" if plan and "one_per_person" in plan.keys() and plan["one_per_person"] else "",
        escape(str(plan["uses_per_event"] if plan and "uses_per_event" in plan.keys() else 0)),
        sel((("external", "External registration link"), ("manual", "Manual"), ("none", "None")), pay),
        escape(plan["external_url"] if plan and "external_url" in plan.keys() else ""),
        " checked" if offer == "usawp_trial" or (kind == "trial" and offer != "none") else "",
        escape(plan["terms"] if plan and "terms" in plan.keys() else ""),
        " checked" if plan and plan["active"] else "",
        escape(core), escape(summary))


def requirement_edit_html(d, req, scope, csrf, preset_ids=None, sport="", preset_role=""):
    linked = set()
    if req:
        linked = {row["program_id"] for row in d.execute("SELECT program_id FROM requirement_programs WHERE requirement_id=?", (req["id"],)).fetchall()}
    elif preset_ids:
        linked = set(preset_ids)
    scope = scope or {}
    boxes = []
    for program in programs(d):
        boxes.append('<label class=checkline><input type=checkbox name=program value="%d"%s> %s</label>' % (
            program["id"], " checked" if program["id"] in linked else "", escape(program["name"])))
    roles = set(_csv(scope["roles"] if scope else ""))
    if preset_role and not req:
        roles.add(preset_role)
    acts = set(_csv(scope["activities"] if scope else ""))
    role_bits = "".join('<label class=checkline><input type=checkbox name="role_%s" value=1%s> %s</label>' % (
        code, " checked" if code in roles else "", label) for code, label in ROLES)
    act_bits = "".join('<label class=checkline><input type=checkbox name="activity_%s" value=1%s> %s</label>' % (
        code, " checked" if code in acts else "", code.title()) for code in ("practice", "scrimmage", "game"))
    effect = scope["effect"] if scope else "info"
    verification = scope["verification"] if scope else "manual"
    hidden_sport = '<input type=hidden name=sport value="%s">' % escape(sport) if sport else ""
    return """<form method=post class=clubform>%s%s
<label>Name<input name=name value="%s" required></label>
<label>Description<textarea class=planfield name=description rows=3>%s</textarea></label>
<label>Category<input name=category value="%s"></label>
<label>Issuing organization<input name=issuer value="%s"></label>
<p>Programs. This does not apply to every program unless you check each one.</p>
%s
<p>Activities. Leave blank to cover every activity in the checked programs.</p>
%s
<p>Roles</p>
<label class=checkline><input type=checkbox name=everyone value=1%s> Everyone in the checked programs</label>
%s
<label>Use<select name=effect>%s</select></label>
<label>Verification<select name=verification>%s</select></label>
<p class="ty-muted ty-sm sm">External verification is recorded only. It does not call a governing body from this page.</p>
<label class=checkline><input type=checkbox name=expires value=1%s> Has an expiration date</label>
<label class=checkline><input type=checkbox name=affects_clearance value=1%s> Counts toward Cleared to Play</label>
<button class="rg-btn primary full" type=submit>Save</button>
</form>""" % (
        csrf, hidden_sport, escape(req["name"] if req else ""), escape(scope["description"] if scope else ""),
        escape(scope["category"] if scope else ""), escape(scope["issuer"] if scope else ""),
        "".join(boxes), act_bits, " checked" if scope and scope["everyone"] else "", role_bits,
        "".join('<option value="%s"%s>%s</option>' % (value, " selected" if value == effect else "", label) for value, label in EFFECTS),
        "".join('<option value="%s"%s>%s</option>' % (value, " selected" if value == verification else "", label) for value, label in VERIFICATIONS),
        " checked" if not req or req["expires"] else "",
        " checked" if scope and scope["affects_clearance"] else "")


def integrations_html(d):
    bits = ['<p class="ty-muted ty-sm sm">Plans use these providers. Stripe cannot be turned on and no card is collected.</p><div class=mlist>']
    for row in d.execute("SELECT * FROM payment_providers ORDER BY id").fetchall():
        state = "On" if row["active"] else "Off"
        if row["kind"] == "stripe":
            state = "Off · coming later"
        bits.append(_row("/manage/club/plans", row["name"], "%s · %s" % (row["kind"], state)))
    bits.append("</div>")
    return "".join(bits)


def program_eligibility_html(d, member, today):
    """Sports on the admin member page: one list row per sport with its clearance chip (2.0 / List row)."""
    import components as C
    rows = []
    for program in programs(d):
        if not program["active"]:
            rows.append(C.row(program["name"], "Off for the club", chip_label="Off", chip_status="neutral", chevron=False, muted=True))
            continue
        result = eligibility(d, member, program, "practice", "athlete", today)
        status = result["status"] or "Cleared"
        st = {"Cleared": "cleared", "Pending verification": "expiring"}.get(status, "notcleared")
        sub = ("Needs " + ", ".join(result["missing"])) if result["missing"] else ""
        rows.append(C.row(program["name"], sub, chip_label=status, chip_status=st, chevron=False))
    return Markup('<h3 class=rg-day id=programs>Sports</h3><div class="rg-list memlist">%s</div>' % "".join(str(r) for r in rows))


def attention(d, member, view="members"):
    try:
        import app as A
        tone = A.list_status(d, member, view if view in ("members", "coaches", "admins", "referees") else "members")["tone"]
    except Exception:
        return ""
    if tone == "bad":
        return "Not cleared"
    if tone == "warn":
        return "Expiring"
    return ""
