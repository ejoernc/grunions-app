"""Lineup discovery feed: categories, publication, team intent, and RSVP states.

Practices stay on their own schedule. This module does not import the Flask app.
"""
import datetime as dt
import re

FEED_CATEGORIES = (
    ("social", "Social & Community", "Social", 1, 0, 1, 1),
    ("activities", "Activities & Meetups", "Activities", 1, 0, 0, 2),
    ("club", "Club Activities", "Club", 1, 0, 0, 3),
    ("learn", "Education & Development", "Learn", 1, 0, 1, 4),
    ("service", "Outreach & Service", "Service", 1, 0, 0, 5),
    ("travel", "Tournament & Travel", "Tournaments & Travel", 0, 1, 1, 6),
)
FEED_SUBTYPES = {
    "social": ("Happy hour", "Party", "Dinner", "Community"),
    "activities": ("Run", "Hike", "Ride", "Beach volleyball", "Open-water swim", "Coffee"),
    "club": ("Orientation", "Meeting", "Recruitment", "Kickoff", "Election"),
    "learn": ("Workshop", "Clinic", "Speaker", "Rules seminar", "Safety"),
    "service": ("Fundraiser", "Charity", "Volunteering", "Partnership"),
    "travel": ("Tournament", "Trip", "Invitational", "Festival"),
}
EVENT_STATUSES = ("draft", "pending", "changes_requested", "published", "declined", "canceled")
RSVP_STATES = ("interested", "going", "notgoing", "waitlist")
STATUS_LABEL = {
    "draft": "Draft",
    "pending": "Pending approval",
    "changes_requested": "Changes requested",
    "published": "Published",
    "declined": "Declined",
    "canceled": "Canceled",
    "completed": "Completed",
}
_OFF_LINEUP = ("practice", "practices", "game", "games", "scrimmage", "local game", "local games")


def _cols(d, table):
    return [r[1] for r in d.execute("PRAGMA table_info(%s)" % table)]


def ensure_schema(d):
    """Add feed tables and columns. Existing lineup rows are filled in once, when status is empty."""
    d.execute("""CREATE TABLE IF NOT EXISTS lineup_categories(
        id INTEGER PRIMARY KEY, slug TEXT NOT NULL UNIQUE, name TEXT NOT NULL, chip TEXT NOT NULL,
        member_ok INTEGER NOT NULL DEFAULT 1, intent_ok INTEGER NOT NULL DEFAULT 0,
        hosting_ok INTEGER NOT NULL DEFAULT 0, sort INTEGER NOT NULL DEFAULT 0, active INTEGER NOT NULL DEFAULT 1)""")
    d.execute("""CREATE TABLE IF NOT EXISTS lineup_subtypes(
        id INTEGER PRIMARY KEY, category_id INTEGER NOT NULL, name TEXT NOT NULL,
        sort INTEGER NOT NULL DEFAULT 0, UNIQUE(category_id, name))""")
    for slug, name, chip, member_ok, intent_ok, hosting_ok, sort in FEED_CATEGORIES:
        d.execute("""INSERT OR IGNORE INTO lineup_categories(slug, name, chip, member_ok, intent_ok, hosting_ok, sort, active)
            VALUES(?,?,?,?,?,?,?,1)""", (slug, name, chip, member_ok, intent_ok, hosting_ok, sort))
    ids = {row[1]: row[0] for row in d.execute("SELECT id, slug FROM lineup_categories")}
    for slug, names in FEED_SUBTYPES.items():
        cid = ids.get(slug)
        if not cid: continue
        for i, name in enumerate(names):
            d.execute("INSERT OR IGNORE INTO lineup_subtypes(category_id, name, sort) VALUES(?,?,?)", (cid, name, i))
    cols = _cols(d, "lineup_events")
    for c, t in (("category_id", "INTEGER"), ("subtype", "TEXT"), ("start_time", "TEXT"), ("end_time", "TEXT"),
                 ("host_id", "INTEGER"), ("official", "INTEGER DEFAULT 0"), ("team_intent", "TEXT"),
                 ("status", "TEXT"), ("banner", "TEXT"), ("capacity", "INTEGER"), ("cost", "TEXT"),
                 ("details", "TEXT"), ("reg_deadline", "TEXT"), ("review_note", "TEXT"),
                 ("created_by", "INTEGER"), ("submitted_at", "TEXT"), ("featured", "INTEGER DEFAULT 0"),
                 ("skill_levels", "TEXT"), ("divisions", "TEXT"), ("division_custom", "TEXT"),
                 ("comp_format", "TEXT"), ("sport", "TEXT"),
                 ("date_precision", "TEXT"), ("date_part", "TEXT")):
        if c not in cols:
            d.execute("ALTER TABLE lineup_events ADD COLUMN %s %s" % (c, t))
    d.execute("UPDATE lineup_events SET date_precision='exact' WHERE date_precision IS NULL OR trim(date_precision)=''")
    rcols = _cols(d, "lineup_rsvps")
    if "state" not in rcols:
        d.execute("ALTER TABLE lineup_rsvps ADD COLUMN state TEXT")
    kind_map = {"Tournament": ("travel", "Tournament"), "Clinic": ("learn", "Clinic"),
                "Social": ("social", ""), "Volunteering": ("service", "Volunteering")}
    cols = _cols(d, "lineup_events")
    for raw in d.execute("SELECT * FROM lineup_events WHERE status IS NULL OR trim(status)=''"):
        row = raw if hasattr(raw, "keys") else dict(zip(cols, raw))
        slug, sub = kind_map.get(row["kind"] or "", ("social", ""))
        intent = ""
        if slug == "travel":
            intent = "official" if (row["stage"] or "") == "going" else "considering"
        start = ""
        if "start" in row.keys() and row["start"] and str(row["start"]).strip():
            start = str(row["start"]).strip()[:5]
        d.execute("""UPDATE lineup_events SET category_id=?, subtype=?, official=1, status='published',
            team_intent=?, start_time=COALESCE(NULLIF(trim(start_time),''), ?) WHERE id=?""",
            (ids.get(slug), sub, intent, start or "09:00", row["id"]))
    d.execute("""UPDATE lineup_rsvps SET state=CASE
        WHEN going=1 AND event_id IN (SELECT id FROM lineup_events WHERE team_intent='considering' OR stage='interest') THEN 'interested'
        WHEN going=1 THEN 'going' ELSE 'notgoing' END
        WHERE state IS NULL OR trim(state)=''""")


def categories(d, active_only=False):
    sql = "SELECT * FROM lineup_categories"
    if active_only: sql += " WHERE active=1"
    return list(d.execute(sql + " ORDER BY sort, id"))


def subtypes_for(d):
    out = {}
    rows = d.execute("""SELECT c.slug, s.name FROM lineup_subtypes s
        JOIN lineup_categories c ON c.id=s.category_id ORDER BY s.sort, s.id""")
    for slug, name in rows:
        out.setdefault(slug, []).append(name)
    return out


def category_by_slug(d, slug):
    return d.execute("SELECT * FROM lineup_categories WHERE slug=?", (slug,)).fetchone()


def _time(v, label):
    v = (v or "").strip()
    if not v: return ""
    if not re.fullmatch(r"\d{2}:\d{2}", v):
        raise ValueError("Use a time like 09:00 for %s." % label)
    h, m = int(v[:2]), int(v[3:])
    if h > 23 or m > 59: raise ValueError("Use a time like 09:00 for %s." % label)
    return "%02d:%02d" % (h, m)


def _words(v, n):
    return " ".join(str(v or "").split())[:n]


def legacy_kind(cat, subtype, intent):
    """Keep the older kind/stage columns coherent for rows this feed writes."""
    slug = cat["slug"] if cat else ""
    if slug == "travel":
        return (subtype or "Tournament"), ("interest" if intent == "considering" else "going")
    if slug == "learn" and (subtype or "") == "Clinic":
        return "Clinic", "attending"
    if slug == "social":
        return "Social", "attending"
    if slug == "service":
        return "Volunteering", "attending"
    return (subtype or (cat["name"] if cat else "Event")), "attending"


def can_edit_event(actor, row, organizer):
    if not actor or not row: return False
    if organizer: return True
    owner = actor["id"] in ((row["created_by"] or 0), (row["host_id"] or 0))
    if not owner or row["official"]: return False
    return (row["status"] or "") in ("draft", "changes_requested", "published")


def save_event(d, form, actor, organizer, existing=None, banner=None, banner_clear=False, parse_date=None):
    """Insert or update one event. Does not commit. Members cannot publish an official event."""
    mode = (form.get("mode") or ("create" if organizer else "suggest")).strip()
    action = (form.get("action") or "save").strip()
    if not existing and not organizer and mode in ("create", "propose", "draft"):
        raise PermissionError()
    if not existing and organizer and mode not in ("create", "propose", "draft", "suggest"):
        mode = "create"
    if existing and not can_edit_event(actor, existing, organizer):
        raise PermissionError()
    raw_cat = (form.get("category") or form.get("kind") or "").strip()
    if raw_cat.lower() in _OFF_LINEUP:
        raise ValueError("Practices and local games stay off the Lineup.")
    if mode == "propose":
        cat = category_by_slug(d, "travel")
    else:
        cat = category_by_slug(d, raw_cat) if raw_cat else None
        if not cat and raw_cat:
            cat = d.execute("SELECT * FROM lineup_categories WHERE lower(name)=lower(?) OR lower(chip)=lower(?)", (raw_cat, raw_cat)).fetchone()
    if not cat or not cat["active"]:
        raise ValueError("Choose a category.")
    if not organizer and not cat["member_ok"]:
        raise ValueError("That category is for organizers. Suggest a community event instead.")
    title = _words(form.get("title"), 120)
    if not title: raise ValueError("Add a title.")
    precision = (form.get("date_precision") or "exact").strip().lower()
    if precision not in ("exact", "month"): precision = "exact"
    part = ""
    if precision == "month":
        month = (form.get("month") or "").strip()
        if not re.fullmatch(r"\d{4}-\d{2}", month): raise ValueError("Choose a month.")
        year, mon = int(month[:4]), int(month[5:7])
        if not 1 <= mon <= 12: raise ValueError("Choose a month.")
        try:
            day = dt.date(year, mon, 1)
            end = dt.date(year + 1, 1, 1) - dt.timedelta(days=1) if mon == 12 else dt.date(year, mon + 1, 1) - dt.timedelta(days=1)
        except ValueError:
            raise ValueError("Choose a month.")
        start_time, end_time = "", ""
        part = (form.get("date_part") or "").strip().lower()
        if part not in ("early", "mid", "late"): part = ""
    else:
        day = parse_date(form.get("date")) if parse_date else None
        if not day: raise ValueError("Add a start date.")
        start_time = _time(form.get("start_time") or form.get("start"), "the start")
        if not start_time: raise ValueError("Add a start time.")
        end_raw = (form.get("end_date") or "").strip()
        end = parse_date(end_raw) if end_raw else day
        if not end: raise ValueError("Add an end date.")
        if end < day: raise ValueError("End date must be on or after the start date.")
        end_time = _time(form.get("end_time"), "the end")
        if end_time and end == day and end_time < start_time:
            raise ValueError("End time must be at or after the start time.")
    location = _words(form.get("location") or form.get("venue"), 300)
    if not location: raise ValueError("Add a location.")
    city = _words(form.get("city"), 80)
    description = (form.get("description") or "").strip()[:2000]
    if not description: raise ValueError("Add a short description.")
    link = (form.get("link") or "").strip()[:500]
    if link and not link.lower().startswith(("http://", "https://")):
        raise ValueError("Link must start with http:// or https://.")
    subtype = _words(form.get("subtype"), 80)
    known = subtypes_for(d).get(cat["slug"], [])
    if subtype and known and subtype not in known:
        subtype = ""
    hosting = (form.get("hosting") or "").strip()
    if cat["hosting_ok"]:
        if hosting not in ("Away", "Hosting"): hosting = (existing["hosting"] if existing and existing["hosting"] in ("Away", "Hosting") else "Away")
    else:
        hosting = existing["hosting"] if existing and existing["hosting"] in ("Away", "Hosting") else "Away"
    details = (form.get("details") or "").strip()[:2000]
    cost = _words(form.get("cost"), 80)
    cap_raw = (form.get("capacity") or "").strip()
    capacity = None
    if cap_raw:
        if not cap_raw.isdigit() or int(cap_raw) < 1: raise ValueError("Capacity must be a number.")
        capacity = int(cap_raw)
    deadline = None
    if (form.get("reg_deadline") or "").strip():
        deadline = parse_date(form.get("reg_deadline"))
        if not deadline: raise ValueError("Registration deadline must be a date.")
        deadline = deadline.isoformat()
    review_note = existing["review_note"] if existing else ""
    featured = 0
    if not organizer:
        official, team_intent, host_id = 0, "", actor["id"]
        if existing and (existing["status"] or "") == "published":
            status = "published"
        else:
            status = "pending"
        if status == "pending":
            review_note = ""
    elif not existing and mode == "suggest":
        official, team_intent, host_id, status = 0, "", actor["id"], "pending"
    elif not existing and (mode == "propose" or mode == "draft" and cat["intent_ok"] and (form.get("team_intent") or "") == "considering"):
        official, team_intent, host_id = 1, "considering", None
        status = "draft" if (mode == "draft" or action == "draft") else "published"
    elif not existing:
        official, host_id = 1, None
        if cat["intent_ok"]:
            posted = (form.get("team_intent") or "").strip()
            team_intent = posted if posted in ("considering", "official") else "official"
        else:
            team_intent = ""
        status = "draft" if (mode == "draft" or action == "draft") else "published"
    else:
        official = 1 if form.get("official") == "1" else 0
        host_id = None if official else (existing["host_id"] or existing["created_by"] or actor["id"])
        if cat["intent_ok"] and official:
            posted = (form.get("team_intent") or existing["team_intent"] or "").strip()
            team_intent = posted if posted in ("considering", "official") else (existing["team_intent"] or "official")
        else:
            team_intent = ""
        if action == "cancel":
            status = "canceled"
        elif action == "draft":
            status = "draft"
        elif (existing["status"] or "") == "canceled":
            status = "canceled"
        elif (existing["status"] or "") == "published":
            status = "published"
        else:
            status = "published"
    if organizer and status == "published" and form.get("featured") == "1":
        featured = 1
    if existing and organizer and action not in ("draft", "cancel") and (existing["status"] or "") == "published" and status == "published":
        pass
    kind, stage = legacy_kind(cat, subtype, team_intent)
    submitted = None
    if status == "pending":
        submitted = existing["submitted_at"] if existing and existing["submitted_at"] and (existing["status"] or "") == "pending" else dt.datetime.now().isoformat(timespec="seconds")
    banner_name = existing["banner"] if existing else ""
    if banner: banner_name = banner
    elif banner_clear: banner_name = ""
    prev_precision, prev_part = "exact", ""
    if existing and "date_precision" in existing.keys() and existing["date_precision"]:
        prev_precision = existing["date_precision"]
    if existing and "date_part" in existing.keys() and existing["date_part"]:
        prev_part = existing["date_part"]
    published_edit = bool(existing and (existing["status"] or "") == "published" and status == "published")
    dates_set = published_edit and prev_precision == "month" and precision == "exact"
    date_changed = False
    if published_edit and not dates_set:
        date_changed = (existing["date"] != day.isoformat() or (existing["end_date"] or "") != end.isoformat()
            or (existing["start_time"] or "") != start_time or (existing["venue"] or "") != location or (existing["city"] or "") != city
            or prev_precision != precision or prev_part != part)
    vals = (cat["id"], subtype, title, day.isoformat(), end.isoformat(), start_time, end_time, city, location,
            description, link, hosting, kind, stage, official, team_intent, status, host_id, actor["id"] if not existing else existing["created_by"],
            banner_name, capacity, cost, details, deadline, review_note or "", submitted, featured, precision, part)
    if existing:
        d.execute("""UPDATE lineup_events SET category_id=?, subtype=?, title=?, date=?, end_date=?, start_time=?, end_time=?,
            city=?, venue=?, description=?, link=?, hosting=?, kind=?, stage=?, official=?, team_intent=?, status=?, host_id=?,
            created_by=?, banner=?, capacity=?, cost=?, details=?, reg_deadline=?, review_note=?, submitted_at=?, featured=?,
            date_precision=?, date_part=? WHERE id=?""",
            (*vals, existing["id"]))
        eid = existing["id"]
    else:
        eid = d.execute("""INSERT INTO lineup_events(category_id, subtype, title, date, end_date, start_time, end_time,
            city, venue, description, link, hosting, kind, stage, official, team_intent, status, host_id, created_by,
            banner, capacity, cost, details, reg_deadline, review_note, submitted_at, featured, date_precision, date_part)
            VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""", vals).lastrowid
    became_pending = status == "pending" and (not existing or (existing["status"] or "") != "pending")
    promoted = team_intent == "official" and existing and (existing["team_intent"] or "") == "considering"
    return {"id": eid, "status": status, "submitted": became_pending, "date_changed": bool(date_changed),
            "dates_set": bool(dates_set),
            "canceled": status == "canceled" and existing and (existing["status"] or "") != "canceled",
            "promoted": bool(promoted), "official": official}


def _date_fields(form=None, row=None):
    if form is not None:
        precision = (form.get("date_precision") or "exact").strip().lower()
        if precision not in ("exact", "month"): precision = "exact"
        part = (form.get("date_part") or "").strip().lower()
        if part not in ("early", "mid", "late"): part = ""
        month = (form.get("month") or "").strip()
        if not re.fullmatch(r"\d{4}-\d{2}", month):
            month = str(form.get("date") or "")[:7]
        return precision, month if re.fullmatch(r"\d{4}-\d{2}", month) else "", part
    if row is not None:
        precision = row["date_precision"] if "date_precision" in row.keys() and row["date_precision"] in ("exact", "month") else "exact"
        part = row["date_part"] if "date_part" in row.keys() and (row["date_part"] or "") in ("early", "mid", "late") else ""
        month = str(row["date"] or "")[:7]
        return precision, month if re.fullmatch(r"\d{4}-\d{2}", month) else "", part
    return "exact", "", ""

def form_values(form=None, row=None, cat_slug="", mode="create"):
    precision, month, part = _date_fields(form, row)
    if form is not None:
        return {"mode": mode, "category": form.get("category") or cat_slug, "subtype": form.get("subtype") or "",
            "hosting": form.get("hosting") or "Away", "title": form.get("title") or "", "date": form.get("date") or "",
            "end_date": form.get("end_date") or "", "start_time": form.get("start_time") or "", "end_time": form.get("end_time") or "",
            "date_precision": precision, "month": month, "date_part": part,
            "location": form.get("location") or form.get("venue") or "", "city": form.get("city") or "",
            "description": form.get("description") or "", "link": form.get("link") or "", "details": form.get("details") or "",
            "cost": form.get("cost") or "", "capacity": form.get("capacity") or "", "reg_deadline": form.get("reg_deadline") or "",
            "team_intent": form.get("team_intent") or "", "official": form.get("official") or "", "featured": form.get("featured") or ""}
    if row:
        return {"mode": mode, "category": cat_slug, "subtype": row["subtype"] or "", "hosting": row["hosting"] or "Away",
            "title": row["title"] or "", "date": row["date"] or "", "end_date": row["end_date"] or "",
            "start_time": row["start_time"] or "", "end_time": row["end_time"] or "",
            "date_precision": precision, "month": month, "date_part": part,
            "location": row["venue"] or "", "city": row["city"] or "", "description": row["description"] or "",
            "link": row["link"] or "", "details": row["details"] or "", "cost": row["cost"] or "",
            "capacity": "" if row["capacity"] is None else str(row["capacity"]), "reg_deadline": row["reg_deadline"] or "",
            "team_intent": row["team_intent"] or "", "official": "1" if row["official"] else "", "featured": "1" if row["featured"] else ""}
    intent = "considering" if mode == "propose" else ""
    return {"mode": mode, "category": "travel" if mode == "propose" else cat_slug, "subtype": "Tournament" if mode == "propose" else "",
        "hosting": "Away", "title": "", "date": "", "end_date": "", "start_time": "", "end_time": "",
        "date_precision": "exact", "month": "", "date_part": "", "location": "", "city": "",
        "description": "", "link": "", "details": "", "cost": "", "capacity": "", "reg_deadline": "",
        "team_intent": intent, "official": "1" if mode in ("create", "propose") else "", "featured": ""}
