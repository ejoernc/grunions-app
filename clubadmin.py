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
    _migrate(d)


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
        {"slug": "pool-swimming", "family": "swimming", "name": "Pool Swimming", "public_name": "Swimming",
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
    _scope(d, usms, "Current US Masters Swimming membership for pool swimming.", "US Masters Swimming",
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
    if body not in ("usawp", "usms", "none"):
        raise ValueError("Choose a governing body.")
    d.execute("""UPDATE programs SET governing_body=?, activities=?, venue=?, notes=? WHERE id=?""", (
        body, ",".join(activities), (form.get("venue") or "")[:200], (form.get("notes") or "")[:500], program["id"]))
    chosen = [int(v) for v in form.getlist("coach") if str(v).isdigit()]
    d.execute("DELETE FROM program_coaches WHERE program_id=?", (program["id"],))
    for mid in chosen:
        d.execute("INSERT OR IGNORE INTO program_coaches(program_id, member_id) VALUES(?,?)", (program["id"], mid))


def save_schedule(d, slug, form):
    """Store the template only. Does not insert practices."""
    program = program_by_slug(d, slug)
    if not program:
        raise ValueError("Choose a program.")
    days = [code for code, _label in WEEKDAYS if form.get("weekday_%s" % code)]
    start = (form.get("start") or "").strip()
    end = (form.get("end") or "").strip()
    if days and (not start or not end):
        raise ValueError("Add a start and end time.")
    if start and end and start >= end:
        raise ValueError("End time must be after the start time.")
    row = d.execute("SELECT id FROM program_schedules WHERE program_id=? ORDER BY id LIMIT 1", (program["id"],)).fetchone()
    fields = ((form.get("description") or "")[:200], ",".join(days), start, end, "America/Los_Angeles",
              (form.get("schedule_venue") or form.get("venue") or "")[:200], (form.get("schedule_notes") or "")[:500], program["id"])
    if row:
        d.execute("""UPDATE program_schedules SET description=?, weekdays=?, start=?, end=?, timezone=?, venue=?, notes=?
            WHERE id=?""", fields[:-1] + (row["id"],))
    else:
        d.execute("""INSERT INTO program_schedules(description, weekdays, start, end, timezone, venue, notes, program_id)
            VALUES(?,?,?,?,?,?,?,?)""", fields)


def schedule_for(d, program_id):
    return d.execute("SELECT * FROM program_schedules WHERE program_id=? ORDER BY id LIMIT 1", (program_id,)).fetchone()


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
    return sports + coach


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
        acts = _csv(scope["activities"])
        if acts and activity and activity not in acts:
            continue
        if not _role_ok(scope, role):
            continue
        if not _req_met(d, member, req, scope, today):
            missing.append(req["name"])
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
    return '<a class=mrow href="%s"><span class=grow><span class=mtitle>%s</span><span class=mdesc>%s</span></span><span class=mchev>%s</span></a>' % (
        escape(href), escape(title), escape(desc), CHEV)


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
    if body not in ("usawp", "usms", "none"):
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
<p class="t3 sm">A new sport starts off. Its requirements are not applied until you turn it on.</p>
<button class="btn btn-primary full" type=submit>Save</button>
</form>""" % (csrf, options)


def programs_html(d):
    bits = ['<div class=mlist>']
    for program in programs(d):
        state = "On" if program["active"] else "Off"
        body = {"usawp": "USA Water Polo", "usms": "US Masters Swimming", "none": "No governing body"}.get(program["governing_body"], program["governing_body"])
        count = requirement_count(d, program["id"])
        noun = "requirement" if count == 1 else "requirements"
        bits.append(_row("/manage/club/programs/%s" % program["slug"], program["name"], "%s · %s · %d %s" % (body, state, count, noun)))
    bits.append("</div>")
    open_reviews = reviews(d)
    if open_reviews:
        bits.append('<h2 class=mseclabel>Needs a sport</h2><div class=mlist>')
        for row in open_reviews:
            bits.append(_row("/manage/club/requirements/%d" % row["ref_id"], row["req_name"] or "Requirement", "Not enforced until a sport is chosen"))
        bits.append("</div>")
    return "".join(bits)


def program_detail_html(d, program, csrf):
    sched = schedule_for(d, program["id"]) or {}
    days = set(_csv(sched["weekdays"] if sched else ""))
    acts = set(_csv(program["activities"]))
    coaches = d.execute("""SELECT id, first, preferred_first, last, role, is_admin FROM members
        WHERE COALESCE(role,'')!='system' AND (role='coach' OR is_admin=1 OR id IN (SELECT member_id FROM coaching_list))
        ORDER BY last, first""").fetchall()
    assigned = {row["member_id"] for row in d.execute("SELECT member_id FROM program_coaches WHERE program_id=?", (program["id"],)).fetchall()}
    day_bits = []
    for code, label in WEEKDAYS:
        day_bits.append('<label class=checkline><input type=checkbox name="weekday_%s" value=1%s> %s</label>' % (
            code, " checked" if code in days else "", label))
    coach_bits = []
    for person in coaches:
        name = ("%s %s" % (person["preferred_first"] or person["first"], person["last"] or "")).strip()
        coach_bits.append('<label class=checkline><input type=checkbox name=coach value="%d"%s> %s</label>' % (
            person["id"], " checked" if person["id"] in assigned else "", escape(name)))
    req_bits = ""
    return """<form method=post class=clubform>
%s
<input type=hidden name=action value=save>
<h2>Overview</h2>
<p class="t3 sm">%s</p>
<label class=checkline><input type=checkbox name=active value=1%s> Program is on</label>
<p class="t3 sm">While this is off, its requirements are not applied and it stays out of registration, Schedule filters, Lineup filters, and the widget.</p>
<label>Governing body<select name=governing_body>
<option value=usawp%s>USA Water Polo</option>
<option value=usms%s>US Masters Swimming</option>
<option value=none%s>None</option></select></label>
<p>Activities</p>
<label class=checkline><input type=checkbox name=activity_practice value=1%s> Practice</label>
<label class=checkline><input type=checkbox name=activity_scrimmage value=1%s> Scrimmage</label>
<label class=checkline><input type=checkbox name=activity_game value=1%s> Game</label>
<h2>Venues</h2>
<label>Venue<input name=venue value="%s"></label>
<label>Notes<textarea class=planfield name=notes rows=3>%s</textarea></label>
<h2>Regular schedule</h2>
<p class="t3 sm">This is the usual pattern. Saving it does not add sessions. Real sessions stay on Schedule.</p>
<label>Description<input name=description value="%s"></label>
<p>Weekdays</p>%s
<div class=row><label>Start<input type=time name=start value="%s"></label><label>End<input type=time name=end value="%s"></label></div>
<label>Schedule venue<input name=schedule_venue value="%s"></label>
<label>Schedule notes<textarea class=planfield name=schedule_notes rows=2>%s</textarea></label>
<h2>Coaches</h2>
%s
<button class="btn btn-primary full" type=submit>Save</button>
</form>
%s""" % (
        csrf, escape(program["family_name"]), " checked" if program["active"] else "",
        " selected" if program["governing_body"] == "usawp" else "",
        " selected" if program["governing_body"] == "usms" else "",
        " selected" if program["governing_body"] == "none" else "",
        " checked" if "practice" in acts else "", " checked" if "scrimmage" in acts else "", " checked" if "game" in acts else "",
        escape(program["venue"] or ""), escape(program["notes"] or ""),
        escape((sched or {}).get("description") or "" if False else (sched["description"] if sched else "")),
        "".join(day_bits),
        escape(sched["start"] if sched else ""), escape(sched["end"] if sched else ""),
        escape(sched["venue"] if sched else ""), escape(sched["notes"] if sched else ""),
        "".join(coach_bits) or "<p class=t3>No coaches to assign yet.</p>", program_requirements_html(d, program))


def program_requirements_html(d, program):
    rows = d.execute("""SELECT q.id, q.name FROM requirement_programs rp
        JOIN requirements q ON q.id=rp.requirement_id
        WHERE rp.program_id=? ORDER BY q.name""", (program["id"],)).fetchall()
    bits = ['<h2>Requirements</h2><div class=mlist>']
    if not rows:
        bits.append('<p class="t3 sm" style="padding:12px 16px">No requirements yet.</p>')
    for row in rows:
        others = [item["name"] for item in d.execute("""SELECT p.name FROM requirement_programs rp
            JOIN programs p ON p.id=rp.program_id
            WHERE rp.requirement_id=? AND p.id!=? ORDER BY p.name""", (row["id"], program["id"]))]
        note = ("Also applies to: " + ", ".join(others)) if others else "This sport only"
        if not program["active"]:
            note += " · Not applied while this sport is off"
        bits.append(_row("/manage/club/requirements/%d?sport=%s" % (row["id"], program["slug"]), row["name"], note))
    bits.append(_row("/manage/club/programs/%s/requirements/new" % program["slug"], "Add requirement", "Starts checked for this sport"))
    bits.append("</div>")
    return "".join(bits)


def plans_html(d):
    bits = ['<div class=mlist>']
    for plan in d.execute("SELECT * FROM payment_plans ORDER BY active DESC, name").fetchall():
        names = plan_program_names(d, plan["id"]) or ["No program yet"]
        bits.append(_row("/manage/club/plans/%d" % plan["id"], plan["name"], ", ".join(names)))
    bits.append("</div>")
    return "".join(bits)


def plan_edit_html(d, plan, csrf):
    linked = {row["program_id"] for row in d.execute("SELECT program_id FROM plan_programs WHERE plan_id=?", (plan["id"],)).fetchall()}
    boxes = []
    for program in programs(d):
        boxes.append('<label class=checkline><input type=checkbox name=program value="%d"%s> %s%s</label>' % (
            program["id"], " checked" if program["id"] in linked else "", escape(program["name"]),
            "" if program["active"] else " (off)"))
    return """<form method=post class=clubform>%s
<p class="t3 sm">%s · %s</p>
<p class="t3 sm">%s</p>
<p>Programs this plan covers. A payment does not satisfy USA Water Polo or USMS.</p>
%s
<button class="btn btn-primary full" type=submit>Save</button>
</form>""" % (csrf, escape(plan["name"]), escape(plan["kind"]), escape(plan["external_url"] or "No external link"), "".join(boxes))


def requirement_edit_html(d, req, scope, csrf, preset_ids=None, sport=""):
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
<p class="t3 sm">External verification is recorded only. It does not call a governing body from this page.</p>
<label class=checkline><input type=checkbox name=expires value=1%s> Has an expiration date</label>
<label class=checkline><input type=checkbox name=affects_clearance value=1%s> Counts toward Cleared to Play</label>
<button class="btn btn-primary full" type=submit>Save</button>
</form>""" % (
        csrf, hidden_sport, escape(req["name"] if req else ""), escape(scope["description"] if scope else ""),
        escape(scope["category"] if scope else ""), escape(scope["issuer"] if scope else ""),
        "".join(boxes), act_bits, " checked" if scope and scope["everyone"] else "", role_bits,
        "".join('<option value="%s"%s>%s</option>' % (value, " selected" if value == effect else "", label) for value, label in EFFECTS),
        "".join('<option value="%s"%s>%s</option>' % (value, " selected" if value == verification else "", label) for value, label in VERIFICATIONS),
        " checked" if not req or req["expires"] else "",
        " checked" if scope and scope["affects_clearance"] else "")


def integrations_html(d):
    bits = ['<p class="t3 sm">Plans use these providers. Stripe cannot be turned on and no card is collected.</p><div class=mlist>']
    for row in d.execute("SELECT * FROM payment_providers ORDER BY id").fetchall():
        state = "On" if row["active"] else "Off"
        if row["kind"] == "stripe":
            state = "Off · coming later"
        bits.append(_row("/manage/club/plans", row["name"], "%s · %s" % (row["kind"], state)))
    bits.append("</div>")
    return "".join(bits)


def program_eligibility_html(d, member, today):
    bits = ['<div class=seclabel id=programs>Eligibility by program</div>',
            '<p class="t3 sm">Clearance is separate from payment. An off program does not apply its requirements.</p>']
    for program in programs(d):
        if not program["active"]:
            bits.append("<p><b>%s</b> · Off</p>" % escape(program["name"]))
            continue
        result = eligibility(d, member, program, "practice", "athlete", today)
        missing = (", ".join(result["missing"])) if result["missing"] else ""
        bits.append("<p><b>%s</b> · %s%s</p>" % (escape(program["name"]), escape(result["status"] or "Cleared"), (" · " + escape(missing)) if missing else ""))
    return "".join(bits)


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
