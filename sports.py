"""Skill levels, divisions, activity types, and competition format.

These are independent. A set of levels is never a range: Beginner and Intermediate
do not include Developing. Nothing here decides who may RSVP.
"""
import json

LEVELS = (
    ("beginner", "Beginner",
     "New to the sport or learning the basics.",
     "New to the sport or learning basic techniques, rules, and movements. May have little or no previous experience."),
    ("developing", "Developing",
     "Knows the fundamentals and is building consistency.",
     "Understands the fundamentals and has some practical experience, but is still building confidence, consistency, and coordination."),
    ("intermediate", "Intermediate",
     "Comfortable playing and using core skills.",
     "Comfortable participating independently, understands gameplay and strategy, and consistently demonstrates core skills."),
    ("experienced", "Experienced",
     "Proficient in advanced or competitive play.",
     "Highly proficient, with strong technical ability, game awareness, and experience in advanced or competitive environments."),
)
LEVEL_IDS = tuple(row[0] for row in LEVELS)
LEVEL_NAME = {row[0]: row[1] for row in LEVELS}

DIVISIONS = (
    ("open", "Open to all"),
    ("coed", "Co-ed"),
    ("mens", "Men's"),
    ("womens", "Women's"),
    ("custom", "Custom"),
)
DIVISION_IDS = tuple(row[0] for row in DIVISIONS)
DIVISION_NAME = {row[0]: row[1] for row in DIVISIONS}

FORMATS = (
    ("scramble", "Scramble", "Players are placed on teams at the event."),
    ("per_team", "per team", "Clubs enter as a team."),
    ("both", "Both", "Teams and individual players can enter."),
    ("tba", "TBA", "The registration format is not set yet."),
)
FORMAT_IDS = tuple(row[0] for row in FORMATS)
FORMAT_NAME = {row[0]: row[1] for row in FORMATS}

ACTIVITIES = (
    ("practice", "Practice"),
    ("scrimmage", "Scrimmage"),
    ("game", "Game"),
    ("hybrid", "Hybrid"),
)
ACTIVITY_IDS = tuple(row[0] for row in ACTIVITIES)
ACTIVITY_NAME = {row[0]: row[1] for row in ACTIVITIES}

SPORTS_COLUMNS = (
    "activity_type", "sport", "title", "skill_levels", "divisions", "division_custom",
    "opponent", "home_away", "gameplay_notes", "segments", "comp_format",
)


def _ids(raw, allowed):
    if raw is None: return []
    if isinstance(raw, str):
        parts = [p.strip().lower() for p in raw.split(",") if p.strip()]
    else:
        parts = []
        for item in raw:
            parts.extend(p.strip().lower() for p in str(item or "").split(",") if p.strip())
    chosen = []
    for pid in allowed:
        if pid in parts and pid not in chosen: chosen.append(pid)
    return chosen


def pack_levels(raw):
    """Canonical comma-separated ids. Unknown ids are dropped. Order is fixed."""
    return ",".join(_ids(raw, LEVEL_IDS))


def levels_label(raw):
    ids = _ids(raw, LEVEL_IDS)
    if not ids: return ""
    if len(ids) == len(LEVEL_IDS): return "All levels"
    return " · ".join(LEVEL_NAME[i] for i in ids)


def pack_divisions(raw, custom=""):
    ids = _ids(raw, DIVISION_IDS)
    text = " ".join(str(custom or "").split())[:80]
    if "custom" not in ids: text = ""
    return ",".join(ids), text


def divisions_label(raw, custom=""):
    ids = _ids(raw, DIVISION_IDS)
    labels = []
    for pid in ids:
        if pid == "custom":
            text = " ".join(str(custom or "").split())
            labels.append(text or "Custom")
        else:
            labels.append(DIVISION_NAME[pid])
    return " · ".join(labels)


def pack_format(raw):
    pid = str(raw or "").strip().lower()
    return pid if pid in FORMAT_IDS else ""


def format_label(raw):
    return FORMAT_NAME.get(pack_format(raw), "")


def parse_segments(raw):
    if not raw: return []
    if isinstance(raw, list): data = raw
    else:
        try: data = json.loads(raw)
        except (TypeError, ValueError): return []
    out = []
    if not isinstance(data, list): return []
    for item in data:
        if not isinstance(item, dict): continue
        kind = str(item.get("type") or "").strip().lower()
        if kind not in ("practice", "scrimmage", "game"): continue
        start = str(item.get("start") or "")[:5]
        end = str(item.get("end") or "")[:5]
        if len(start) != 5 or len(end) != 5: continue
        out.append({"type": kind, "start": start, "end": end})
    return out[:6]


def pack_segments(types, starts, ends):
    rows = []
    for kind, start, end in zip(types or [], starts or [], ends or []):
        kind = str(kind or "").strip().lower()
        start = str(start or "")[:5]
        end = str(end or "")[:5]
        if kind not in ("practice", "scrimmage", "game"): continue
        if len(start) != 5 or len(end) != 5: continue
        rows.append({"type": kind, "start": start, "end": end})
    return json.dumps(rows[:6]) if rows else ""


def activity_title(activity, opponent="", segments="", custom=""):
    custom = " ".join(str(custom or "").split())[:120]
    if custom: return custom
    kind = str(activity or "practice").strip().lower()
    if kind not in ACTIVITY_IDS: kind = "practice"
    if kind == "game":
        opp = " ".join(str(opponent or "").split())
        return ("Game vs. " + opp) if opp else "Game"
    if kind == "scrimmage": return "Scrimmage"
    if kind == "hybrid":
        labels = []
        for seg in parse_segments(segments):
            lab = ACTIVITY_NAME.get(seg["type"], "")
            if lab and lab not in labels: labels.append(lab)
        if len(labels) >= 2: return " + ".join(labels)
        if labels: return labels[0]
        return "Hybrid"
    return "Practice"


def session_title(sport, activity, opponent="", segments="", custom=""):
    """Live team-schedule title. A custom title wins. Empty falls back to Sport + type."""
    custom = " ".join(str(custom or "").split())[:120]
    if custom: return custom
    kind = str(activity or "practice").strip().lower()
    if kind not in ACTIVITY_IDS: kind = "practice"
    if kind == "hybrid":
        return activity_title(kind, opponent, segments, "")
    name = " ".join(str(sport or "").split()) or "Water Polo"
    return "%s %s" % (name, ACTIVITY_NAME.get(kind, "Practice"))


def sports_line(levels, divisions, custom="", comp=""):
    """One subtle line. Empty when nothing is set."""
    parts = [levels_label(levels), divisions_label(divisions, custom), format_label(comp)]
    return " · ".join(p for p in parts if p)


def _get(form, key):
    if form is None: return None
    if hasattr(form, "get"): return form.get(key)
    return None


def _getlist(form, key):
    if form is None: return []
    if hasattr(form, "getlist"): return form.getlist(key)
    val = form.get(key) if hasattr(form, "get") else None
    if val is None: return []
    return val if isinstance(val, (list, tuple)) else [val]


def sports_from_form(form):
    activity = str(_get(form, "activity_type") or "practice").strip().lower()
    if activity not in ACTIVITY_IDS: activity = "practice"
    opponent = " ".join(str(_get(form, "opponent") or "").split())[:80]
    side = str(_get(form, "home_away") or "").strip().lower()
    if side not in ("home", "away"): side = ""
    segments = pack_segments(_getlist(form, "segment_type"), _getlist(form, "segment_start"), _getlist(form, "segment_end"))
    comp = pack_format(_get(form, "comp_format"))
    if activity != "game": comp = ""
    divs, custom = pack_divisions(_getlist(form, "division"), _get(form, "division_custom"))
    sport = " ".join(str(_get(form, "sport") or "").split())[:40] or "Water Polo"
    title = " ".join(str(_get(form, "title") or "").split())[:120]
    derived = session_title(sport, activity, opponent, segments, "")
    if title == derived or title == activity_title(activity, opponent, segments, ""): title = ""
    return {
        "activity_type": activity,
        "sport": sport,
        "title": title,
        "skill_levels": pack_levels(_getlist(form, "level")),
        "divisions": divs,
        "division_custom": custom,
        "opponent": opponent if activity == "game" else "",
        "home_away": side if activity == "game" else "",
        "gameplay_notes": (" ".join(str(_get(form, "gameplay_notes") or "").split())[:500] if activity == "scrimmage" else ""),
        "segments": segments if activity == "hybrid" else "",
        "comp_format": comp,
    }


def sports_from_row(row):
    def val(key, default=""):
        try:
            if hasattr(row, "keys") and key in row.keys() and row[key] is not None: return row[key]
        except (AttributeError, TypeError):
            pass
        return default
    activity = str(val("activity_type") or "practice").strip().lower()
    if activity not in ACTIVITY_IDS: activity = "practice"
    return {
        "activity_type": activity,
        "sport": val("sport") or "Water Polo",
        "title": val("title") or "",
        "skill_levels": pack_levels(val("skill_levels")),
        "divisions": pack_divisions(val("divisions"), val("division_custom"))[0],
        "division_custom": pack_divisions(val("divisions"), val("division_custom"))[1],
        "opponent": val("opponent") or "",
        "home_away": val("home_away") or "",
        "gameplay_notes": val("gameplay_notes") or "",
        "segments": val("segments") or "",
        "comp_format": pack_format(val("comp_format")),
    }


def sports_tuple(data):
    return tuple(data[k] for k in SPORTS_COLUMNS)
