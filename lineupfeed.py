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
EVENT_TYPES = ("Tournament", "Competition", "Clinic", "Trip", "Social", "Volunteer", "Fundraiser", "Meeting", "Other")
EVENT_TYPE_LABELS = (
    ("Tournament", "Tournament"), ("Competition", "Competition"), ("Clinic", "Clinic/Camp"),
    ("Trip", "Trip"), ("Social", "Social/Activity"), ("Volunteer", "Volunteer"),
    ("Fundraiser", "Fundraiser"), ("Meeting", "Meeting/Workshop"), ("Other", "Other"),
)
MEMBER_TYPES = ("Clinic", "Trip", "Social", "Volunteer", "Fundraiser", "Meeting", "Other")
MEMBER_TYPE_LABELS = tuple(pair for pair in EVENT_TYPE_LABELS if pair[0] in MEMBER_TYPES)
TEAM_PLAN_TYPES = ("Tournament", "Competition", "Trip", "Clinic")
TEAM_PLANS = ("considering", "planning", "committed")
FILTER_GROUPS = (
    ("competitions", "Competitions", ("Tournament", "Competition")),
    ("camps", "Camps", ("Clinic",)),
    ("trips", "Trips", ("Trip",)),
    ("community", "Community", ("Social", "Volunteer", "Fundraiser", "Meeting", "Other")),
)
_FILTER_ALIAS = {"training": "camps"}
# Canonical storage: category slug, subtype column, legacy kind.
TYPE_STORE = {
    "Tournament": ("travel", "Tournament", "Tournament"),
    "Competition": ("travel", "Competition", "Competition"),
    "Clinic": ("learn", "Clinic", "Clinic"),
    "Trip": ("travel", "Trip", "Trip"),
    "Social": ("social", "", "Social"),
    "Volunteer": ("service", "Volunteering", "Volunteering"),
    "Fundraiser": ("service", "Fundraiser", "Fundraiser"),
    "Meeting": ("club", "Meeting", "Meeting"),
    "Other": ("social", "Other", "Other"),
}
_SUBTYPE_TYPE = {
    "Tournament": "Tournament", "Invitational": "Tournament", "Festival": "Tournament",
    "Clinic": "Clinic", "Workshop": "Clinic", "Speaker": "Clinic", "Rules seminar": "Clinic", "Safety": "Clinic",
    "Trip": "Trip", "Team trip": "Trip",
    "Volunteering": "Volunteer", "Charity": "Volunteer", "Partnership": "Volunteer",
    "Fundraiser": "Fundraiser",
    "Competition": "Competition", "Meet": "Competition", "Race": "Competition", "League": "Competition", "Championship": "Competition",
    "Meeting": "Meeting", "Workshop": "Meeting",
    "Other": "Other",
    "Happy hour": "Social", "Party": "Social", "Dinner": "Social", "Community": "Social",
    "Run": "Social", "Hike": "Social", "Ride": "Social", "Beach volleyball": "Social",
    "Open-water swim": "Social", "Coffee": "Social",
    "Orientation": "Social", "Meeting": "Social", "Recruitment": "Social", "Kickoff": "Social", "Election": "Social",
}
_SLUG_TYPE = {
    "travel": "Tournament", "learn": "Clinic", "service": "Volunteer",
    "social": "Social", "activities": "Social", "club": "Social",
}
_KIND_TYPE = {
    "Tournament": "Tournament", "Away tournament": "Tournament", "Clinic": "Clinic",
    "Trip": "Trip", "Team trip": "Trip", "Social": "Social", "Team trip/Social": "Social",
    "Volunteering": "Volunteer",
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
                 ("date_precision", "TEXT"), ("date_part", "TEXT"), ("host_org", "TEXT"),
                 ("event_type", "TEXT"), ("lat", "REAL"), ("lng", "REAL"), ("team_plan", "TEXT")):
        if c not in cols:
            d.execute("ALTER TABLE lineup_events ADD COLUMN %s %s" % (c, t))
    d.execute("UPDATE lineup_events SET date_precision='exact' WHERE date_precision IS NULL OR trim(date_precision)=''")
    d.execute("""UPDATE lineup_events SET date_part='all'
        WHERE date_precision='month' AND (date_part IS NULL OR trim(date_part)='' OR lower(trim(date_part))='tba')""")
    for eid, subtype, kind, slug, stored in d.execute("""SELECT e.id, COALESCE(e.subtype,''), COALESCE(e.kind,''),
            COALESCE(c.slug,''), COALESCE(e.event_type,'')
            FROM lineup_events e LEFT JOIN lineup_categories c ON c.id=e.category_id"""):
        if stored in EVENT_TYPES: continue
        d.execute("UPDATE lineup_events SET event_type=? WHERE id=?",
                  (event_type_from_parts(slug, subtype, kind, stored), eid))
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
    d.execute("""UPDATE lineup_events SET team_plan='committed',
        status=CASE WHEN status IS NULL OR trim(status)='' OR status='draft' THEN 'published' ELSE status END
        WHERE team_intent='official' AND (team_plan IS NULL OR trim(team_plan)='')""")
    d.execute("""UPDATE lineup_events SET team_plan='considering'
        WHERE team_intent='considering' AND (team_plan IS NULL OR trim(team_plan)='')""")
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


def filter_type(cat):
    """Feed filter accepts a type name or an older category slug."""
    if cat in EVENT_TYPES: return cat
    return _SLUG_TYPE.get(cat, "")


def filter_group(name):
    """Discovery chips: Competitions, Camps, Trips, Community. training is the old Camps slug."""
    name = _FILTER_ALIAS.get((name or "").strip(), (name or "").strip())
    for slug, _label, types in FILTER_GROUPS:
        if name == slug: return slug, types
    return "", ()


def type_groups(pairs):
    """Group create-form types under Competitions, Camps, Trips, and Community."""
    allowed = dict(pairs or ())
    groups = []
    for _slug, label, types in FILTER_GROUPS:
        opts = [(name, allowed[name]) for name in types if name in allowed]
        if opts: groups.append((label, opts))
    return groups


def hosting_label(value):
    """Attending replaced Away. Hosting is unchanged."""
    v = (value or "").strip()
    if v in ("Away", "Attending"): return "Attending"
    if v == "Hosting": return "Hosting"
    return ""


def normalize_hosting(value, default="Attending"):
    label = hosting_label(value)
    return label or default


def team_plan_for(event_type, team_intent, form, existing=None):
    """Team plan is separate from publication. Only competitions, trips, and clinics have one."""
    if event_type not in TEAM_PLAN_TYPES:
        return ""
    posted = ""
    if form is not None:
        posted = (form.get("team_plan") or "").strip()
    if posted in TEAM_PLANS:
        return posted
    if team_intent == "official":
        return "committed"
    if team_intent == "considering":
        return "considering"
    if existing is not None and "team_plan" in existing.keys():
        prev = (existing["team_plan"] or "").strip()
        if prev in TEAM_PLANS: return prev
    return ""


def event_type_from_parts(slug="", subtype="", kind="", stored=""):
    """Map an older category, subtype, or kind onto Tournament, Clinic, Trip, Social, or Volunteer."""
    if stored in EVENT_TYPES: return stored
    if subtype in _SUBTYPE_TYPE: return _SUBTYPE_TYPE[subtype]
    if slug in _SLUG_TYPE: return _SLUG_TYPE[slug]
    if kind in _KIND_TYPE: return _KIND_TYPE[kind]
    return "Social"


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
    if not existing and not organizer and mode == "propose":
        mode = "suggest"
    if not existing and not organizer and mode in ("create", "draft"):
        raise PermissionError()
    if not existing and organizer and mode not in ("create", "propose", "draft", "suggest"):
        mode = "create"
    if existing and not can_edit_event(actor, existing, organizer):
        raise PermissionError()
    raw_cat = (form.get("category") or form.get("kind") or "").strip()
    if raw_cat.lower() in _OFF_LINEUP:
        raise ValueError("Practices and local games stay off the Lineup.")
    posted_type = (form.get("event_type") or "").strip()
    explicit_type = posted_type in EVENT_TYPES
    if mode == "propose" and not explicit_type:
        event_type = "Tournament"
    elif explicit_type:
        event_type = posted_type
    else:
        cat_guess = category_by_slug(d, raw_cat) if raw_cat else None
        if not cat_guess and raw_cat:
            cat_guess = d.execute("SELECT * FROM lineup_categories WHERE lower(name)=lower(?) OR lower(chip)=lower(?)", (raw_cat, raw_cat)).fetchone()
        event_type = event_type_from_parts(cat_guess["slug"] if cat_guess else raw_cat, _words(form.get("subtype"), 80), raw_cat, "")
    if event_type not in EVENT_TYPES:
        event_type = "Social"
    slug, subtype, _kind_name = TYPE_STORE[event_type]
    cat = category_by_slug(d, slug)
    if not cat or not cat["active"]:
        raise ValueError("Choose a type.")
    if not organizer and event_type not in MEMBER_TYPES:
        raise ValueError("That type is for organizers. Suggest a clinic, a trip, or a community event instead.")
    title = _words(form.get("title"), 120)
    if not title: raise ValueError("Add a title.")
    precision = (form.get("date_precision") or "exact").strip().lower()
    if precision not in ("exact", "month"): precision = "exact"
    if not organizer and precision == "month":
        raise ValueError("Add a specific date.")
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
        if part not in ("early", "mid", "late", "all"): part = "all"
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
    city = _words(form.get("city"), 120)
    venue = _words(form.get("venue"), 300)
    legacy = _words(form.get("location"), 300)
    if not venue and legacy: venue = legacy
    if not city and venue:
        city, venue = venue, ""
    if city and venue and city.casefold() == venue.casefold(): venue = ""
    if not city: raise ValueError("Add a city.")
    location = venue
    description = (form.get("description") or "").strip()[:2000]
    if not description: raise ValueError("Add a short description.")
    link = (form.get("link") or "").strip()[:500]
    if link and not link.lower().startswith(("http://", "https://")):
        raise ValueError("Link must start with http:// or https://.")
    if explicit_type or cat["hosting_ok"]:
        hosting = normalize_hosting(form.get("hosting"), normalize_hosting(existing["hosting"]) if existing else "Attending")
    else:
        hosting = normalize_hosting(existing["hosting"]) if existing else "Attending"
    host_org = _words(form.get("host_org"), 80) if hosting == "Attending" and (explicit_type or cat["hosting_ok"]) else ""
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
    featured = 1 if existing and existing["featured"] else 0
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
    if explicit_type and organizer and mode != "suggest":
        official, host_id = 1, None
        posted = (form.get("team_intent") or "").strip()
        if posted in ("considering", "official"): team_intent = posted
        elif mode == "propose": team_intent = "considering"
        else: team_intent = "official"
    if form.get("pin_present") == "1":
        featured = 1 if organizer and status == "published" and form.get("featured") == "1" else 0
    elif organizer and form.get("featured") == "1" and status == "published":
        featured = 1
    if existing and organizer and action not in ("draft", "cancel") and (existing["status"] or "") == "published" and status == "published":
        pass
    if organizer:
        plan = team_plan_for(event_type, team_intent, form, existing)
        if plan == "committed":
            team_intent = "official"
        elif plan in ("considering", "planning"):
            team_intent = "considering"
    else:
        plan = ""
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
            banner_name, capacity, cost, details, deadline, review_note or "", submitted, featured, precision, part, host_org, event_type, plan)
    if existing:
        d.execute("""UPDATE lineup_events SET category_id=?, subtype=?, title=?, date=?, end_date=?, start_time=?, end_time=?,
            city=?, venue=?, description=?, link=?, hosting=?, kind=?, stage=?, official=?, team_intent=?, status=?, host_id=?,
            created_by=?, banner=?, capacity=?, cost=?, details=?, reg_deadline=?, review_note=?, submitted_at=?, featured=?,
            date_precision=?, date_part=?, host_org=?, event_type=?, team_plan=? WHERE id=?""",
            (*vals, existing["id"]))
        eid = existing["id"]
        if (existing["venue"] or "") != location or (existing["city"] or "") != city:
            d.execute("UPDATE lineup_events SET lat=NULL, lng=NULL WHERE id=?", (eid,))
    else:
        eid = d.execute("""INSERT INTO lineup_events(category_id, subtype, title, date, end_date, start_time, end_time,
            city, venue, description, link, hosting, kind, stage, official, team_intent, status, host_id, created_by,
            banner, capacity, cost, details, reg_deadline, review_note, submitted_at, featured, date_precision, date_part, host_org, event_type, team_plan)
            VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""", vals).lastrowid
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
        if precision == "month":
            if part not in ("early", "mid", "late", "all"): part = "all"
        elif part not in ("early", "mid", "late", "all"):
            part = ""
        month = (form.get("month") or "").strip()
        if not re.fullmatch(r"\d{4}-\d{2}", month):
            month = str(form.get("date") or "")[:7]
        return precision, month if re.fullmatch(r"\d{4}-\d{2}", month) else "", part
    if row is not None:
        precision = row["date_precision"] if "date_precision" in row.keys() and row["date_precision"] in ("exact", "month") else "exact"
        stored = (row["date_part"] or "").strip().lower() if "date_part" in row.keys() else ""
        if stored in ("early", "mid", "late", "all"): part = stored
        elif precision == "month": part = "all"
        else: part = ""
        month = str(row["date"] or "")[:7]
        return precision, month if re.fullmatch(r"\d{4}-\d{2}", month) else "", part
    return "exact", "", ""

def _form_type(form=None, row=None, cat_slug="", mode="create"):
    if form is not None:
        posted = (form.get("event_type") or "").strip()
        if posted in EVENT_TYPES: return posted
        if mode == "propose": return "Tournament"
        return event_type_from_parts(form.get("category") or cat_slug, form.get("subtype") or "", form.get("kind") or "", "")
    if row is not None:
        stored = row["event_type"] if "event_type" in row.keys() else ""
        return event_type_from_parts(cat_slug, row["subtype"] or "", row["kind"] or "", stored or "")
    if mode == "propose": return "Tournament"
    if mode == "suggest": return "Social"
    return "Tournament"


def form_values(form=None, row=None, cat_slug="", mode="create"):
    precision, month, part = _date_fields(form, row)
    event_type = _form_type(form, row, cat_slug, mode)
    if form is not None:
        return {"mode": mode, "category": form.get("category") or cat_slug, "subtype": form.get("subtype") or "",
            "event_type": event_type,
            "hosting": normalize_hosting(form.get("hosting")), "title": form.get("title") or "", "date": form.get("date") or "",
            "end_date": form.get("end_date") or "", "start_time": form.get("start_time") or "", "end_time": form.get("end_time") or "",
            "date_precision": precision, "month": month, "date_part": part,
            "host_org": form.get("host_org") or "",
            "location": form.get("location") or form.get("venue") or "", "city": form.get("city") or "",
            "description": form.get("description") or "", "link": form.get("link") or "", "details": form.get("details") or "",
            "cost": form.get("cost") or "", "capacity": form.get("capacity") or "", "reg_deadline": form.get("reg_deadline") or "",
            "team_intent": form.get("team_intent") or ("considering" if mode == "propose" else ""), "official": form.get("official") or "", "featured": form.get("featured") or ""}
    if row:
        return {"mode": mode, "category": cat_slug, "subtype": row["subtype"] or "", "event_type": event_type,
            "hosting": normalize_hosting(row["hosting"]),
            "title": row["title"] or "", "date": row["date"] or "", "end_date": row["end_date"] or "",
            "start_time": row["start_time"] or "", "end_time": row["end_time"] or "",
            "date_precision": precision, "month": month, "date_part": part,
            "host_org": row["host_org"] if "host_org" in row.keys() and row["host_org"] else "",
            "location": row["venue"] or "", "city": row["city"] or "", "description": row["description"] or "",
            "link": row["link"] or "", "details": row["details"] or "", "cost": row["cost"] or "",
            "capacity": "" if row["capacity"] is None else str(row["capacity"]), "reg_deadline": row["reg_deadline"] or "",
            "team_intent": row["team_intent"] or "", "official": "1" if row["official"] else "", "featured": "1" if row["featured"] else ""}
    intent = "considering" if mode == "propose" else ""
    return {"mode": mode, "category": "travel" if mode == "propose" else cat_slug, "subtype": "Tournament" if mode == "propose" else "",
        "event_type": event_type,
        "hosting": "Attending", "title": "", "date": "", "end_date": "", "start_time": "", "end_time": "",
        "date_precision": "exact", "month": "", "date_part": "", "host_org": "", "location": "", "city": "",
        "description": "", "link": "", "details": "", "cost": "", "capacity": "", "reg_deadline": "",
        "team_intent": intent, "official": "1" if mode in ("create", "propose") else "", "featured": ""}
