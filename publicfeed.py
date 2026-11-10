"""Public schedule, prices, and free-trial rules.

These describe what an organization usually offers. Saving them does not create
practices or Lineup events. Blank prices are omitted, never filled in.
"""
import datetime as dt
import json
import re
from decimal import Decimal, InvalidOperation
from zoneinfo import ZoneInfo

DAYS = ("Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday")
DAY_SHORT = ("Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun")
_TIME = re.compile(r"^(\d{2}):(\d{2})$")
_DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def ensure_schema(d):
    d.execute("""CREATE TABLE IF NOT EXISTS org_settings(
        id INTEGER PRIMARY KEY CHECK (id=1),
        body TEXT NOT NULL DEFAULT '{}',
        updated_at TEXT NOT NULL DEFAULT '')""")
    d.execute("""CREATE TABLE IF NOT EXISTS trial_holds(
        member_id INTEGER NOT NULL, practice_id INTEGER NOT NULL,
        state TEXT NOT NULL, at TEXT NOT NULL, PRIMARY KEY(member_id, practice_id))""")
    member_cols = {row[1] for row in d.execute("PRAGMA table_info(members)")}
    if member_cols and "trial_claim_until" not in member_cols:
        d.execute("ALTER TABLE members ADD COLUMN trial_claim_until TEXT")


def blank_slot():
    return {"days": [], "start": "", "end": "", "venue": "", "address": ""}


def blank():
    return {
        "schedule": {
            "name": "", "description": "", "timezone": "America/Los_Angeles",
            "season_start": "", "season_end": "", "public": False,
            "venue": "", "address": "", "slots": [],
        },
        "pricing": {
            "drop_in": "", "member": "", "nonmember": "",
            "monthly": "", "monthly_desc": "", "passes": [], "fees": [],
        },
        "trial": {
            "enabled": False, "mode": "duration", "duration_days": 14, "session_count": 2,
            "activities": ["practice"], "external": "usawp_trial", "first_time_only": True,
            "includes": "", "visits": "", "days": "", "conditions": "", "message": "",
        },
        "widget": widget_blank(),
    }


def _words(value, limit):
    return " ".join(str(value or "").split())[:limit]


def _time(value, label):
    raw = (value or "").strip()
    if not raw:
        return ""
    match = _TIME.fullmatch(raw)
    if not match:
        raise ValueError("Use a time like 19:00 for %s." % label)
    hour, minute = int(match.group(1)), int(match.group(2))
    if hour > 23 or minute > 59:
        raise ValueError("Use a time like 19:00 for %s." % label)
    return "%02d:%02d" % (hour, minute)


def _date(value, label):
    raw = (value or "").strip()
    if not raw:
        return ""
    if not _DATE.fullmatch(raw):
        raise ValueError("Use a date for %s." % label)
    try:
        dt.date.fromisoformat(raw)
    except ValueError as exc:
        raise ValueError("Use a date for %s." % label) from exc
    return raw


def _zone(value):
    raw = _words(value, 64) or "America/Los_Angeles"
    try:
        ZoneInfo(raw)
    except Exception as exc:
        raise ValueError("Use a time zone like America/Los_Angeles.") from exc
    return raw


def _count(value, label):
    raw = (value or "").strip()
    if not raw:
        return ""
    if not raw.isdigit() or int(raw) > 999:
        raise ValueError("Use a whole number for %s." % label)
    return str(int(raw))


def _get(form, key):
    if form is None:
        return ""
    value = form.get(key)
    if value is None:
        return ""
    return str(value)


def _listed(form, key):
    if form is None:
        return []
    if hasattr(form, "getlist"):
        return [str(item) for item in form.getlist(key)]
    value = form.get(key)
    if value is None:
        return []
    if isinstance(value, (list, tuple)):
        return [str(item) for item in value]
    return [str(value)]


def _days(form, key):
    found = []
    for raw in _listed(form, key):
        if raw.isdigit() and 0 <= int(raw) <= 6 and int(raw) not in found:
            found.append(int(raw))
    return found


def _slot(form, index):
    days = _days(form, "slot%d_day" % index)
    start = _time(_get(form, "slot%d_start" % index), "weekly time %d" % (index + 1))
    end = _time(_get(form, "slot%d_end" % index), "weekly time %d" % (index + 1))
    venue = _words(_get(form, "slot%d_venue" % index), 120)
    address = _words(_get(form, "slot%d_address" % index), 180)
    if not days and not start and not end and not venue and not address:
        return None
    if not days or not start:
        raise ValueError("Add the days and a start time for weekly time %d, or leave that row blank." % (index + 1))
    return {"days": days, "start": start, "end": end, "venue": venue, "address": address}


def _priced(name, price, extra):
    name, price = _words(name, 80), _words(price, 40)
    if not name and not price:
        return None
    row = {"name": name, "price": price}
    row.update(extra)
    return row


def parse_form(form):
    """Read the settings form. Raises ValueError and writes nothing."""
    data = blank()
    schedule = data["schedule"]
    schedule["name"] = _words(_get(form, "program_name"), 80)
    schedule["description"] = _words(_get(form, "program_desc"), 500)
    schedule["timezone"] = _zone(_get(form, "timezone"))
    schedule["season_start"] = _date(_get(form, "season_start"), "the season start")
    schedule["season_end"] = _date(_get(form, "season_end"), "the season end")
    schedule["public"] = _get(form, "schedule_public") == "1"
    schedule["venue"] = _words(_get(form, "venue"), 120)
    schedule["address"] = _words(_get(form, "address"), 180)
    slots = []
    for index in range(3):
        slot = _slot(form, index)
        if slot:
            slots.append(slot)
    schedule["slots"] = slots
    pricing = data["pricing"]
    for key, field in (("drop_in", "price_dropin"), ("member", "price_member"), ("nonmember", "price_nonmember"), ("monthly", "price_monthly")):
        pricing[key] = _words(_get(form, field), 40)
    pricing["monthly_desc"] = _words(_get(form, "price_monthly_desc"), 180)
    pas = _priced(_get(form, "pass_name"), _get(form, "pass_price"), {
        "visits": _count(_get(form, "pass_visits"), "practice-pass visits"),
        "description": _words(_get(form, "pass_desc"), 180),
    })
    if pas:
        pricing["passes"] = [pas]
    fee = _priced(_get(form, "fee_name"), _get(form, "fee_price"), {
        "description": _words(_get(form, "fee_desc"), 180),
    })
    if fee:
        pricing["fees"] = [fee]
    trial = data["trial"]
    trial["enabled"] = _get(form, "trial_on") == "1"
    posted = set(form.keys()) if hasattr(form, "keys") else set()
    trial["first_time_only"] = _get(form, "trial_first") == "1" if "trial_first" in posted else True
    mode = _get(form, "trial_mode")
    if mode not in ("duration", "sessions"):
        if _get(form, "trial_visits") and not _get(form, "trial_days"):
            mode = "sessions"
        else:
            mode = "duration"
    trial["mode"] = mode
    if mode == "sessions":
        choice = _get(form, "trial_sessions") or _get(form, "trial_visits")
        if choice == "custom":
            choice = _count(_get(form, "trial_sessions_custom"), "free practices")
        elif choice in ("1", "2", "3"):
            pass
        else:
            choice = _count(choice, "free practices") if choice else "2"
        trial["session_count"] = int(choice or "2")
        trial["visits"] = str(trial["session_count"])
        trial["duration_days"] = 14
    else:
        choice = _get(form, "trial_duration") or _get(form, "trial_days") or "14"
        if choice == "custom":
            choice = _count(_get(form, "trial_duration_custom"), "trial length") or "14"
        elif str(choice) not in ("7", "14", "30") and not str(choice).isdigit():
            raise ValueError("Use 7, 14, 30, or a custom number of days.")
        elif str(choice).isdigit():
            choice = _count(str(int(choice)), "trial length") or "14"
        trial["duration_days"] = int(choice or "14")
        trial["days"] = str(trial["duration_days"])
    activities = [item for item in _listed(form, "trial_activity") if item in ("practice", "scrimmage", "game")]
    if "trial_activity" not in posted and not activities:
        activities = ["practice"]
    if not activities:
        activities = ["practice"]
    trial["activities"] = activities
    external = _get(form, "trial_external")
    if external not in ("usawp_trial", "none"):
        external = "usawp_trial" if mode == "duration" else "none"
    trial["external"] = external
    trial["includes"] = _words(_get(form, "trial_includes"), 180)
    trial["conditions"] = _words(_get(form, "trial_conditions"), 500)
    trial["message"] = _words(_get(form, "trial_message"), 280)
    return data


def _merge(base, stored):
    if not isinstance(stored, dict):
        return base
    for key, value in base.items():
        if key not in stored:
            continue
        if isinstance(value, dict) and isinstance(stored[key], dict):
            base[key] = _merge(value, stored[key])
        else:
            base[key] = stored[key]
    return base


def load(d):
    ensure_schema(d)
    row = d.execute("SELECT body FROM org_settings WHERE id=1").fetchone()
    data = blank()
    if not row or not row["body"]:
        return data
    try:
        stored = json.loads(row["body"])
    except (TypeError, json.JSONDecodeError):
        return data
    stored = stored if isinstance(stored, dict) else {}
    data = _merge(data, stored)
    raw = stored.get("trial") if isinstance(stored.get("trial"), dict) else {}
    if raw.get("mode") not in ("duration", "sessions"):
        data["trial"]["mode"] = ""
    data["trial"] = normalize_trial(data["trial"])
    return data


def save_sections(d, **sections):
    """Replace named sections and leave every other saved section alone."""
    data = load(d)
    for key, value in sections.items():
        data[key] = value
    ensure_schema(d)
    now = dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")
    d.execute("""INSERT INTO org_settings(id, body, updated_at) VALUES(1, ?, ?)
        ON CONFLICT(id) DO UPDATE SET body=excluded.body, updated_at=excluded.updated_at""",
              (json.dumps(data, separators=(",", ":")), now))
    _CACHE.clear()
    return data


def save_form(d, form):
    parsed = parse_form(form)
    return save_sections(d, schedule=parsed["schedule"], pricing=parsed["pricing"], trial=parsed["trial"])


def form_slots(data):
    slots = [dict(slot) for slot in data["schedule"].get("slots") or []]
    while len(slots) < 3:
        slots.append(blank_slot())
    slots = slots[:3]
    for index, slot in enumerate(slots):
        slot["index"] = index
    return slots


def _first(rows):
    row = (rows or [{}])[0] if rows else {}
    return {
        "name": row.get("name") or "",
        "price": row.get("price") or "",
        "visits": row.get("visits") or "",
        "description": row.get("description") or "",
    }


def clock(value):
    if not value:
        return ""
    hour, minute = int(value[:2]), int(value[3:5])
    suffix = "AM" if hour < 12 else "PM"
    hour = hour % 12 or 12
    return "%d:%02d %s" % (hour, minute, suffix)


def money(raw):
    """Show a typed amount as currency. Words such as Free stay as typed."""
    text = (raw or "").strip()
    if not text:
        return ""
    body = text[1:].strip() if text[:1] == "$" else text
    try:
        amount = Decimal(body.replace(",", ""))
    except (InvalidOperation, ValueError):
        return text
    if amount == amount.to_integral_value():
        return "$%d" % int(amount)
    return "$%s" % format(amount.quantize(Decimal("0.01")), "f")


def price_line(label, amount):
    shown = money(amount)
    label = (label or "").strip()
    if label and shown:
        return "%s %s" % (label, shown)
    return shown or label


def _day_phrase(days):
    days = list(days or [])
    if len(days) == 1:
        return DAYS[days[0]] + "s"
    return ", ".join(DAY_SHORT[day] for day in days)


def _span(slot):
    start, end = clock(slot.get("start")), clock(slot.get("end"))
    if start and end:
        return "%s–%s" % (start, end)
    return start or end


def public_view(data):
    """Visitor-facing schedule, prices, and trial. Empty prices are left out."""
    schedule = data.get("schedule") or {}
    lines = []
    if schedule.get("public"):
        for slot in schedule.get("slots") or []:
            place = slot.get("venue") or schedule.get("venue") or ""
            lines.append({
                "program": schedule.get("name") or "",
                "when": "%s: %s" % (_day_phrase(slot.get("days")), _span(slot)),
                "place": place,
                "address": slot.get("address") or (schedule.get("address") if not slot.get("venue") else "") or "",
            })
    prices = []
    pricing = data.get("pricing") or {}
    for key, label in (("drop_in", "Drop-in"), ("member", "Member"), ("nonmember", "Nonmember"), ("monthly", "Monthly")):
        amount = (pricing.get(key) or "").strip()
        if not amount:
            continue
        item = {"label": label, "price": money(amount), "detail": "", "line": price_line(label, amount)}
        if key == "monthly":
            item["detail"] = pricing.get("monthly_desc") or ""
        prices.append(item)
    for pas in pricing.get("passes") or []:
        if not (pas.get("name") or pas.get("price")):
            continue
        detail = pas.get("description") or ""
        if pas.get("visits"):
            detail = ("%s visits" % pas["visits"] + (" · " + detail if detail else "")).strip()
        label = pas.get("name") or "Practice pass"
        prices.append({"label": label, "price": money(pas.get("price") or ""), "detail": detail, "line": price_line(label, pas.get("price") or "")})
    for fee in pricing.get("fees") or []:
        if not (fee.get("name") or fee.get("price")):
            continue
        label = fee.get("name") or "Fee"
        prices.append({"label": label, "price": money(fee.get("price") or ""), "detail": fee.get("description") or "", "line": price_line(label, fee.get("price") or "")})
    trial = None
    raw = normalize_trial(data.get("trial") or {})
    if raw.get("enabled"):
        trial = dict(raw)
        trial["banner"] = banner(raw)
    return {
        "name": schedule.get("name") or "" if schedule.get("public") else "",
        "description": schedule.get("description") or "" if schedule.get("public") else "",
        "timezone": schedule.get("timezone") or "" if schedule.get("public") else "",
        "season_start": schedule.get("season_start") or "" if schedule.get("public") else "",
        "season_end": schedule.get("season_end") or "" if schedule.get("public") else "",
        "lines": lines,
        "prices": prices,
        "trial": trial,
    }


def normalize_trial(trial):
    """Fill the Grunions duration offer without turning it on or rewriting a saved choice."""
    base = blank()["trial"]
    trial = dict(base, **(trial or {}))
    if trial.get("mode") not in ("duration", "sessions"):
        if trial.get("visits") and not trial.get("days") and not trial.get("duration_days"):
            trial["mode"] = "sessions"
        else:
            trial["mode"] = "duration"
    if trial["mode"] == "sessions":
        count = trial.get("session_count") or trial.get("visits") or 2
        try:
            trial["session_count"] = max(1, min(99, int(count)))
        except (TypeError, ValueError):
            trial["session_count"] = 2
    else:
        days = trial.get("duration_days") or trial.get("days") or 14
        try:
            trial["duration_days"] = max(1, min(365, int(days)))
        except (TypeError, ValueError):
            trial["duration_days"] = 14
    activities = [item for item in (trial.get("activities") or []) if item in ("practice", "scrimmage", "game")]
    trial["activities"] = activities or ["practice"]
    if trial.get("external") not in ("usawp_trial", "none"):
        trial["external"] = "usawp_trial"
    return trial


def banner(trial):
    """Public copy from the offer type. A duration trial never uses session wording."""
    trial = normalize_trial(trial)
    if not trial.get("enabled"):
        return None
    if trial["mode"] == "sessions":
        n = trial["session_count"]
        noun = "Practice" if n == 1 else "Practices"
        lower = "practice" if n == 1 else "practices"
        return {
            "title": "Get %d Free %s" % (n, noun),
            "body": "New here? Select a practice below and sign up to claim your %d free %s." % (n, lower),
            "link": "",
            "href": "",
        }
    days = trial["duration_days"]
    if days == 14:
        title = "Try Water Polo Free for 2 Weeks"
    elif days % 7 == 0:
        title = "Try Water Polo Free for %d Weeks" % (days // 7)
    else:
        title = "Try Water Polo Free for %d Days" % days
    body = "New to water polo? Select a practice below to sign up."
    link, href = "", ""
    if trial.get("external") == "usawp_trial":
        body = "New to water polo? Select a practice below to sign up. A valid USA Water Polo trial membership is required to participate."
        link = "Learn about USA Water Polo trial membership"
        href = "https://usawp.sport80.com/public/widget/1"
    return {"title": title, "body": body, "link": link, "href": href}


def _member_get(member, key):
    if not member:
        return ""
    try:
        value = member[key]
    except (KeyError, TypeError, IndexError):
        return ""
    return value or ""


def eligibility(trial, member, today, session_date=None):
    """Read-only. A self-claim is not USAWP verification, and nothing is written."""
    trial = normalize_trial(trial)
    if not trial.get("enabled"):
        return {"status": "ineligible", "label": "Ineligible", "reason": "No free-trial offer is on.", "start": "", "end": ""}
    if not member:
        return {"status": "not_started", "label": "Not started", "reason": "Sign in to check eligibility.", "start": "", "end": ""}
    status = str(_member_get(member, "usawp_status"))
    until = str(_member_get(member, "usawp_valid_until"))[:10]
    kind = str(_member_get(member, "membership_type"))
    claimed = str(_member_get(member, "trial_acknowledged_at"))[:10]
    pending = str(_member_get(member, "verify_pending") or "")
    today_s = today.isoformat() if hasattr(today, "isoformat") else str(today)[:10]
    external = trial.get("external") == "usawp_trial"
    trial_type = "trial" in kind.lower()
    verified_cover = status == "verified" and bool(until) and until >= today_s and (trial_type or not external)
    if external and status == "verified" and until and until >= today_s and kind and not trial_type:
        return {"status": "ineligible", "label": "Ineligible", "reason": "This offer is only for a USA Water Polo trial membership.", "start": "", "end": until}
    if trial.get("first_time_only") and claimed and not verified_cover:
        try:
            start = dt.date.fromisoformat(claimed)
            end = start + dt.timedelta(days=int(trial["duration_days"]))
            if str(end) < today_s and status != "pending" and not pending:
                return {"status": "ineligible", "label": "Ineligible", "reason": "The USA Water Polo trial can be used once.", "start": claimed, "end": end.isoformat()}
        except ValueError:
            pass
    if external and not verified_cover:
        if claimed or status == "pending" or pending:
            return {"status": "pending", "label": "Pending verification", "reason": "USA Water Polo has not verified this trial membership yet.", "start": "", "end": ""}
        return {"status": "not_started", "label": "Not started", "reason": "A verified USA Water Polo trial membership is required.", "start": "", "end": ""}
    if trial["mode"] == "duration":
        if external:
            end = until
            start = claimed or ""
            if start:
                try:
                    claim_end = (dt.date.fromisoformat(start) + dt.timedelta(days=int(trial["duration_days"]))).isoformat()
                    if claim_end < end:
                        end = claim_end
                except ValueError:
                    start = ""
            if session_date and str(session_date)[:10] > end:
                return {"status": "expired", "label": "Expired", "reason": "That session is after the USA Water Polo trial coverage.", "start": start, "end": end}
            if end < today_s:
                return {"status": "expired", "label": "Expired", "reason": "The trial coverage has ended.", "start": start, "end": end}
            return {"status": "active", "label": "Active", "reason": "Verified USA Water Polo trial coverage.", "start": start, "end": end}
        if not claimed:
            return {"status": "not_started", "label": "Not started", "reason": "The trial has not been started.", "start": "", "end": ""}
        start = claimed
        end = (dt.date.fromisoformat(start) + dt.timedelta(days=int(trial["duration_days"]))).isoformat()
        if end < today_s:
            return {"status": "expired", "label": "Expired", "reason": "The trial period has ended.", "start": start, "end": end}
        return {"status": "active", "label": "Active", "reason": "The trial period covers this session.", "start": start, "end": end}
    return {"status": "active", "label": "Active", "reason": "Session credits are available.", "start": claimed, "end": until}


def trial_claim_open(data, member):
    """True only when the person has not already started the one-time offer."""
    trial = normalize_trial((data or {}).get("trial") or data or {})
    if not trial.get("enabled") or str(_member_get(member, "trial_acknowledged_at"))[:10]:
        return False
    found = eligibility(trial, member, dt.date.today())
    return found["status"] in ("not_started", "active")


def activity_ok(trial, activity):
    trial = normalize_trial(trial)
    return (activity or "practice") in (trial.get("activities") or ["practice"])


def member_facts(member, pending=False):
    """A plain dict so eligibility can see a pending request without writing the member row."""
    if not member:
        return None
    try:
        data = {key: member[key] for key in member.keys()}
    except AttributeError:
        data = dict(member)
    data["verify_pending"] = "1" if pending else ""
    return data


def session_balance(d, member_id, trial):
    """Credits still available. A cancelled RSVP or a cancelled session is not counted."""
    trial = normalize_trial(trial)
    total = int(trial.get("session_count") or 0) if trial.get("mode") == "sessions" else 0
    used = held = 0
    if total and member_id:
        rows = d.execute("""SELECT h.state, p.cancelled, r.going
            FROM trial_holds h
            JOIN practices p ON p.id=h.practice_id
            LEFT JOIN rsvps r ON r.practice_id=h.practice_id AND r.member_id=h.member_id
            WHERE h.member_id=?""", (member_id,)).fetchall()
        for row in rows:
            if row["cancelled"] or not row["going"]:
                continue
            if row["state"] == "used":
                used += 1
            elif row["state"] == "held":
                held += 1
    return {"total": total, "used": used, "held": held, "remaining": max(0, total - used - held)}


def release_practice_holds(d, practice_id):
    """A cancelled session gives every held credit back."""
    if practice_id:
        d.execute("DELETE FROM trial_holds WHERE practice_id=?", (practice_id,))


def sync_trial_hold(d, member_id, practice_id, today):
    """Hold a credit while the athlete is Going, and use it only after check-in.
    An RSVP that is cancelled, or a session that is cancelled, releases the credit.
    People who are not eligible for the session offer are left alone."""
    if not member_id or not practice_id:
        return
    trial = normalize_trial((load(d).get("trial") or {}))

    def drop():
        d.execute("DELETE FROM trial_holds WHERE member_id=? AND practice_id=?", (member_id, practice_id))

    practice = d.execute("SELECT id, date, cancelled, activity_type FROM practices WHERE id=?", (practice_id,)).fetchone()
    going = d.execute("SELECT going FROM rsvps WHERE practice_id=? AND member_id=?", (practice_id, member_id)).fetchone()
    if (not trial.get("enabled") or trial.get("mode") != "sessions" or not practice or practice["cancelled"]
            or not going or not going["going"] or not activity_ok(trial, practice["activity_type"] or "practice")):
        drop()
        return
    member = d.execute("SELECT * FROM members WHERE id=?", (member_id,)).fetchone()
    pending = d.execute("SELECT 1 FROM verify_requests WHERE member_id=? AND status='pending' LIMIT 1", (member_id,)).fetchone()
    found = eligibility(trial, member_facts(member, bool(pending)), today, practice["date"])
    if found["status"] != "active":
        drop()
        return
    existing = d.execute("SELECT state FROM trial_holds WHERE member_id=? AND practice_id=?", (member_id, practice_id)).fetchone()
    checked = d.execute("SELECT 1 FROM checkins WHERE member_id=? AND practice_date=?", (member_id, practice["date"])).fetchone()
    if not existing and not checked and session_balance(d, member_id, trial)["remaining"] <= 0:
        return
    state = "used" if checked else "held"
    now = dt.datetime.now(ZoneInfo("America/Los_Angeles")).isoformat(timespec="seconds")
    d.execute("""INSERT INTO trial_holds(member_id, practice_id, state, at) VALUES(?,?,?,?)
        ON CONFLICT(member_id, practice_id) DO UPDATE SET state=excluded.state, at=excluded.at""",
               (member_id, practice_id, state, now))


def sync_holds_on_date(d, member_id, day, today):
    for row in d.execute("SELECT id FROM practices WHERE date=?", (str(day)[:10],)):
        sync_trial_hold(d, member_id, row["id"], today)


CHIPS = (
    ("all", "All"),
    ("schedule", "Schedule"),
    ("competitions", "Competitions"),
    ("camps", "Camps"),
    ("trips", "Trips"),
    ("community", "Community"),
)
_LINEUP_CHIP = {
    "Tournament": "competitions", "Competition": "competitions",
    "Clinic": "camps", "Trip": "trips",
    "Social": "community", "Volunteer": "community", "Fundraiser": "community",
    "Meeting": "community", "Other": "community",
}
_CACHE = {}


def widget_blank():
    return {
        "enabled": False, "theme": "night", "visitor_theme": True,
        "chips": [slug for slug, _label in CHIPS], "default_chip": "all",
        "show_pricing": True, "show_trial": True, "show_counts": False,
        "hide_past": True, "limit": 4, "include_schedule": True,
    }


def parse_widget(form):
    """Read the Website Widget form. Raises ValueError and writes nothing."""
    data = widget_blank()
    chosen = [slug for slug, _label in CHIPS if _get(form, "chip_%s" % slug) == "1"]
    if not chosen:
        chosen = ["all"]
    if "all" not in chosen:
        chosen.insert(0, "all")
    data["chips"] = chosen
    theme = _get(form, "theme")
    data["theme"] = theme if theme in ("night", "day") else "night"
    default = _get(form, "default_chip")
    data["default_chip"] = default if default in chosen else "all"
    data["enabled"] = _get(form, "widget_on") == "1"
    data["visitor_theme"] = _get(form, "visitor_theme") == "1"
    data["show_pricing"] = _get(form, "show_pricing") == "1"
    data["show_trial"] = _get(form, "show_trial") == "1"
    data["show_counts"] = _get(form, "show_counts") == "1"
    data["hide_past"] = _get(form, "hide_past") == "1"
    data["include_schedule"] = _get(form, "include_schedule") == "1"
    limit = _count(_get(form, "limit") or "4", "events in preview") or "4"
    data["limit"] = min(40, max(1, int(limit)))
    return data


def _stamp(day, clock):
    day = str(day or "")[:10]
    clock = (clock or "00:00")[:5]
    return "%sT%s" % (day, clock)


def _ended(day, clock, now):
    try:
        date = dt.date.fromisoformat(str(day)[:10])
        hour, minute = [int(part) for part in ((clock or "23:59")[:5].split(":") + ["0"])[:2]]
    except (TypeError, ValueError):
        return False
    return dt.datetime.combine(date, dt.time(hour, minute)) < now


def _cols(d, table):
    try:
        return {row[1] for row in d.execute("PRAGMA table_info(%s)" % table)}
    except Exception:
        return set()


def _short_day(iso):
    try:
        day = dt.date.fromisoformat(str(iso)[:10])
    except ValueError:
        return ""
    return day.strftime("%a, %b ") + str(day.day)


def _tile(iso):
    try:
        day = dt.date.fromisoformat(str(iso)[:10])
    except ValueError:
        return {"wd": "", "dn": "", "mo": ""}
    return {"wd": day.strftime("%a").upper(), "dn": str(day.day), "mo": day.strftime("%b").upper()}


_CHIP_LABEL = dict(CHIPS)


def build_feed(d, data, practice_title, now, org, event_limit=None):
    """Public cards only. No names, photos, plans, or private notes.
    event_limit trims the admin preview. The live widget and feed leave it unset."""
    widget = data.get("widget") or widget_blank()
    offer = public_view(data)
    hide_past = widget.get("hide_past", True)
    show_price = bool(widget.get("show_pricing"))
    show_trial = bool(widget.get("show_trial")) and bool((offer.get("trial") or {}).get("banner"))
    show_counts = bool(widget.get("show_counts"))
    drop_in = ""
    if show_price:
        for price in offer["prices"]:
            if price["label"] == "Drop-in" and price.get("price"):
                drop_in = price["price"]
                break
    events = []
    pcols = _cols(d, "practices")
    if "date" in pcols and widget.get("include_schedule", True):
        rows = d.execute("""SELECT id, date, start, end, location, note, cancelled, cancel_reason,
            activity_type, sport, title, opponent, segments FROM practices
            WHERE COALESCE(date_precision,'exact')!='month' ORDER BY date, start, id""").fetchall()
        ids = [row["id"] for row in rows]
        counts = {}
        if show_counts and ids:
            marks = ",".join("?" * len(ids))
            for pid, n in d.execute("SELECT practice_id, COUNT(*) FROM rsvps WHERE going=1 AND practice_id IN (%s) GROUP BY practice_id" % marks, ids):
                counts[pid] = n
        for row in rows:
            if hide_past and _ended(row["date"], row["end"] or row["start"], now):
                continue
            kind = (row["activity_type"] or "practice").strip().lower()
            covered = (not row["cancelled"]) and activity_ok(data.get("trial") or {}, kind) and bool((data.get("trial") or {}).get("enabled"))
            item = {
                "id": "p-%d" % row["id"],
                "chip": "schedule",
                "category": "Schedule",
                "sport": row["sport"] or "Water Polo",
                "activity": {"practice": "Practice", "scrimmage": "Scrimmage", "game": "Game", "hybrid": "Hybrid"}.get(kind, "Practice"),
                "date": _short_day(row["date"]),
                "title": practice_title(row),
                "tile": _tile(row["date"]),
                "time": _span({"start": row["start"], "end": row["end"]}),
                "when": "%s · %s" % (_short_day(row["date"]), _span({"start": row["start"], "end": row["end"]})),
                "place": row["location"] or "",
                "detail": _words(row["note"], 280),
                "cancelled": bool(row["cancelled"]),
                "reason": _words(row["cancel_reason"], 180) if row["cancelled"] else "",
                "price": price_line("Drop-in", drop_in) if drop_in else "",
                "signup": covered,
                "trial_line": ((offer.get("trial") or {}).get("banner") or {}).get("title") or "" if covered and show_trial else "",
                "count": counts.get(row["id"]) if show_counts else None,
                "sort": _stamp(row["date"], row["start"]),
            }
            events.append(item)
    lcols = _cols(d, "lineup_events")
    if "title" in lcols and "status" in lcols:
        for row in d.execute("""SELECT id, title, date, end_date, city, venue, start_time, end_time,
            description, event_type, status, capacity, cost FROM lineup_events WHERE status='published'"""):
            end_day = row["end_date"] or row["date"]
            if hide_past and _ended(end_day, row["end_time"] or "23:59", now):
                continue
            chip = _LINEUP_CHIP.get(row["event_type"] or "", "community")
            place = " · ".join(part for part in ((row["venue"] or "").strip(), (row["city"] or "").strip()) if part)
            cost = _words(row["cost"], 40) if show_price else ""
            events.append({
                "id": "e-%d" % row["id"],
                "chip": chip,
                "category": _CHIP_LABEL.get(chip, "Community"),
                "sport": "",
                "activity": row["event_type"] or _CHIP_LABEL.get(chip, "Event"),
                "date": _short_day(row["date"]),
                "title": _words(row["title"], 120),
                "trial_line": "",
                "tile": _tile(row["date"]),
                "time": _span({"start": row["start_time"], "end": row["end_time"]}),
                "when": "%s · %s" % (_short_day(row["date"]), _span({"start": row["start_time"], "end": row["end_time"]})),
                "place": place,
                "detail": _words(row["description"], 280),
                "cancelled": False,
                "reason": "",
                "price": price_line("", cost) if cost else "",
                "signup": False,
                "count": None,
                "capacity": row["capacity"] if row["capacity"] else None,
                "sort": _stamp(row["date"], row["start_time"]),
            })
    events.sort(key=lambda item: (item["sort"], item["id"]))
    if event_limit:
        events = events[:max(1, int(event_limit))]
    for item in events:
        item.pop("sort", None)
    overview = offer["lines"] if widget.get("include_schedule", True) else []
    chips = [slug for slug in widget.get("chips") or ["all"] if slug in dict(CHIPS)]
    if "all" not in chips:
        chips.insert(0, "all")
    return {
        "org": org,
        "theme": widget.get("theme") if widget.get("theme") in ("night", "day") else "night",
        "visitor_theme": bool(widget.get("visitor_theme")),
        "chips": chips,
        "default_chip": widget.get("default_chip") if widget.get("default_chip") in chips else "all",
        "overview": overview,
        "prices": offer["prices"] if show_price else [],
        "trial": offer["trial"] if show_trial else None,
        "events": events,
    }


def feed_body(d, data, practice_title, now, org):
    """Small cached JSON. At most a few dozen cards, refreshed about every 30 seconds."""
    import time
    stamp = ""
    try:
        row = d.execute("SELECT updated_at FROM org_settings WHERE id=1").fetchone()
        stamp = row["updated_at"] if row else ""
    except Exception:
        stamp = ""
    key = stamp or "none"
    now_s = time.monotonic()
    hit = _CACHE.get(key)
    if hit and now_s - hit[0] < 30:
        return hit[1]
    body = json.dumps(build_feed(d, data, practice_title, now, org), separators=(",", ":")).encode()
    if len(_CACHE) > 3:
        _CACHE.clear()
    _CACHE[key] = (now_s, body)
    return body


SETTINGS_PAGE = """<style>
.daypick{display:flex;flex-wrap:wrap;gap:8px 12px;margin:0 0 12px}
.daypick label{display:flex;align-items:center;gap:6px;margin:0;min-height:40px;color:var(--t1);font-size:15px}
.pill{height:36px;padding:0 14px;border-radius:999px;border:1px solid var(--color-control);background:transparent;color:var(--t1);font:500 14px/1 var(--font-sans);cursor:pointer}
.pill.on{background:var(--color-lime);border-color:var(--color-lime);color:#090D0B}
.callout{margin:12px 0 0;padding:12px 14px;border-radius:16px;background:color-mix(in srgb,var(--color-lime) 18%,transparent)}
.slotblock{margin:0 0 8px}
.offerline{margin:0}
</style>
{{ admin_page('Sports & pricing', 'The regular schedule is when you usually practice. Saving it does not add sessions. Create those in Schedule.') }}
{{ pay_nav|safe }}
<form method=post>
{{ csrf_field() }}
<h2>Regular schedule</h2>
<label>Program<input name=program_name value="{{ s.schedule.name }}" autocomplete=off placeholder="Water Polo"></label>
<label>Description<textarea class=planfield name=program_desc rows=3>{{ s.schedule.description }}</textarea></label>
<label>Time zone<input name=timezone value="{{ s.schedule.timezone }}" autocomplete=off></label>
<label>Primary venue<input name=venue value="{{ s.schedule.venue }}" autocomplete=off></label>
<label>Address<input name=address value="{{ s.schedule.address }}" autocomplete=off></label>
<div class=row>
<label>Season starts<input type=date name=season_start value="{{ s.schedule.season_start }}"></label>
<label>Season ends<input type=date name=season_end value="{{ s.schedule.season_end }}"></label>
</div>
<label class=switchrow>Show this schedule on the website<span class=switch><input type=checkbox name=schedule_public value=1 {% if s.schedule.public %}checked{% endif %}><span></span></span></label>
<h2>Weekly times</h2>
<p class="t3 sm">Each row can use different days and a different place. Leave a row blank to skip it.</p>
{% for slot in slots %}
<div class=slotblock>
<div class=seclabel>Time {{ slot.index + 1 }}</div>
<div class=daypick role=group aria-label="Days for time {{ slot.index + 1 }}">
{% for name in day_names %}<label><input type=checkbox name="slot{{ slot.index }}_day" value="{{ loop.index0 }}" {% if loop.index0 in slot.days %}checked{% endif %}>{{ name }}</label>{% endfor %}
</div>
<div class=row>
<label>Start<input type=time name="slot{{ slot.index }}_start" value="{{ slot.start }}"></label>
<label>End<input type=time name="slot{{ slot.index }}_end" value="{{ slot.end }}"></label>
</div>
<label>Place for these days<input name="slot{{ slot.index }}_venue" value="{{ slot.venue }}" autocomplete=off placeholder="Uses the primary venue if blank"></label>
<label>Address for these days<input name="slot{{ slot.index }}_address" value="{{ slot.address }}" autocomplete=off></label>
</div>
{% endfor %}
<h2>Pricing</h2>
<p class="t3 sm">Leave a price blank to hide it. Nothing is filled in for you.</p>
<label>Drop-in<input name=price_dropin value="{{ s.pricing.drop_in }}" autocomplete=off></label>
<label>Member<input name=price_member value="{{ s.pricing.member }}" autocomplete=off></label>
<label>Nonmember<input name=price_nonmember value="{{ s.pricing.nonmember }}" autocomplete=off></label>
<label>Monthly<input name=price_monthly value="{{ s.pricing.monthly }}" autocomplete=off></label>
<label>Monthly description<input name=price_monthly_desc value="{{ s.pricing.monthly_desc }}" autocomplete=off></label>
<div class=seclabel>Practice pass</div>
<label>Name<input name=pass_name value="{{ pass_row.name }}" autocomplete=off></label>
<div class=row>
<label>Price<input name=pass_price value="{{ pass_row.price }}" autocomplete=off></label>
<label>Visits<input name=pass_visits value="{{ pass_row.visits }}" inputmode=numeric autocomplete=off></label>
</div>
<label>Description<input name=pass_desc value="{{ pass_row.description }}" autocomplete=off></label>
<div class=seclabel>Additional fee</div>
<label>Name<input name=fee_name value="{{ fee_row.name }}" autocomplete=off></label>
<label>Price<input name=fee_price value="{{ fee_row.price }}" autocomplete=off></label>
<label>Description<input name=fee_desc value="{{ fee_row.description }}" autocomplete=off></label>
<h2>Free trial</h2>
<label class=switchrow>Offer a free trial<span class=switch><input type=checkbox name=trial_on value=1 {% if s.trial.enabled %}checked{% endif %}><span></span></span></label>
<div class=seclabel>Trial type</div>
<div class="daypick pillset" id=trialType role=radiogroup aria-label="Trial type">
<button type=button class="pill{% if s.trial.mode != 'sessions' %} on{% endif %}" data-mode=duration>Duration</button>
<button type=button class="pill{% if s.trial.mode == 'sessions' %} on{% endif %}" data-mode=sessions>Number of Sessions</button>
</div>
<input type=hidden name=trial_mode id=trialMode value="{{ s.trial.mode or 'duration' }}">
<div id=durationFields {% if s.trial.mode == 'sessions' %}hidden{% endif %}>
<label>Length<select name=trial_duration id=trialDuration>
<option value=7 {% if s.trial.duration_days|string == '7' %}selected{% endif %}>7 days</option>
<option value=14 {% if s.trial.duration_days|string == '14' %}selected{% endif %}>14 days</option>
<option value=30 {% if s.trial.duration_days|string == '30' %}selected{% endif %}>30 days</option>
<option value=custom {% if s.trial.duration_days|string not in ['7','14','30'] %}selected{% endif %}>Custom</option>
</select></label>
<label>Custom days<input name=trial_duration_custom value="{{ '' if s.trial.duration_days|string in ['7','14','30'] else s.trial.duration_days }}" inputmode=numeric></label>
<p class="t3 sm">During the period, eligible practices have no session fee. The window cannot run past verified USA Water Polo coverage.</p>
</div>
<div id=sessionFields {% if s.trial.mode != 'sessions' %}hidden{% endif %}>
<label>Free practices<select name=trial_sessions>
<option value=1 {% if s.trial.session_count|string == '1' %}selected{% endif %}>1</option>
<option value=2 {% if s.trial.session_count|string == '2' %}selected{% endif %}>2</option>
<option value=3 {% if s.trial.session_count|string == '3' %}selected{% endif %}>3</option>
<option value=custom {% if s.trial.session_count|string not in ['1','2','3'] %}selected{% endif %}>Custom</option>
</select></label>
<label>Custom count<input name=trial_sessions_custom value="{{ '' if s.trial.session_count|string in ['1','2','3'] else s.trial.session_count }}" inputmode=numeric></label>
<p class="t3 sm">A credit is used when the athlete attends. Cancelling the RSVP, or cancelling the session, gives it back.</p>
</div>
<div class=seclabel>Eligible schedule activities</div>
<div class="daypick pillset" id=activityPills>
{% for value, label in [('practice','Practices'),('scrimmage','Scrimmages'),('game','Games')] %}
<button type=button class="pill{% if value in s.trial.activities %} on{% endif %}" data-activity="{{ value }}">{{ label }}</button>
<input type=hidden name=trial_activity value="{{ value }}" {% if value not in s.trial.activities %}disabled{% endif %}>
{% endfor %}
</div>
<p class="t3 sm">Scrimmages, games, and Lineup events are not included unless you select them here.</p>
<label>External requirement<select name=trial_external>
<option value=usawp_trial {% if s.trial.external != 'none' %}selected{% endif %}>USA Water Polo trial membership</option>
<option value=none {% if s.trial.external == 'none' %}selected{% endif %}>None</option>
</select></label>
<label class=switchrow>One time only<span class=switch><input type=checkbox name=trial_first value=1 {% if s.trial.first_time_only %}checked{% endif %}><span></span></span></label>
<button class="btn btn-primary full" type=submit>Save</button>
</form>
<h2>On the website</h2>
<div class=card>
{% if offer.lines %}
{% if offer.name %}<div class=nxtitle>{{ offer.name }}</div>{% endif %}
{% if offer.description %}<p>{{ offer.description }}</p>{% endif %}
{% for line in offer.lines %}<p class=offerline>{{ line.when }}{% if line.place %} · {{ line.place }}{% endif %}</p>{% endfor %}
{% if offer.season_start or offer.season_end %}<p class="t3 sm">{{ offer.season_start }}{% if offer.season_end %} – {{ offer.season_end }}{% endif %}</p>{% endif %}
{% else %}<p class="t3 sm">The regular schedule is hidden until you turn it on.</p>{% endif %}
{% if offer.prices %}<div class=seclabel>Pricing</div>{% for price in offer.prices %}<p class=offerline>{{ price.line }}{% if price.detail %} · {{ price.detail }}{% endif %}</p>{% endfor %}
{% else %}<p class="t3 sm">No prices to show.</p>{% endif %}
{% if offer.trial and offer.trial.banner %}<div class=callout><b>{{ offer.trial.banner.title }}</b><p>{{ offer.trial.banner.body }}</p></div>
{% else %}<p class="t3 sm">No free-trial offer.</p>{% endif %}
</div>
<script>
(function(){
  var mode=document.getElementById("trialMode");
  document.querySelectorAll("#trialType .pill").forEach(function(btn){
    btn.addEventListener("click", function(){
      document.querySelectorAll("#trialType .pill").forEach(function(other){other.classList.remove("on");});
      btn.classList.add("on");
      mode.value=btn.getAttribute("data-mode");
      document.getElementById("durationFields").hidden=mode.value!=="duration";
      document.getElementById("sessionFields").hidden=mode.value!=="sessions";
    });
  });
  document.querySelectorAll("#activityPills .pill").forEach(function(btn){
    btn.addEventListener("click", function(){
      btn.classList.toggle("on");
      var input=btn.parentNode.querySelector('input[value="'+btn.getAttribute("data-activity")+'"]');
      if(input) input.disabled=!btn.classList.contains("on");
    });
  });
})();
</script>
"""


WIDGET_URL = "https://grunions.regulars.team/widget"


def embed_snippet(base=None):
    """The paste-once snippet. The custom domain stays the source when Render's hostname changes."""
    return (
        '<iframe id="regulars-schedule" src="%s" title="Schedule" '
        'style="width:100%%;border:0;min-height:640px" loading="lazy"></iframe>\n'
        '<script>\n'
        'window.addEventListener("message",function(e){\n'
        '  var f=document.getElementById("regulars-schedule");\n'
        '  if(!f||e.source!==f.contentWindow||!e.data||e.data.type!=="regulars-widget")return;\n'
        '  if(e.data.height)f.style.height=Math.max(320,e.data.height)+"px";\n'
        '});\n'
        '</script>'
    ) % WIDGET_URL


_CLOCK = '<svg class=nxglyph width="16" height="16" viewBox="0 0 256 256" fill="currentColor" aria-hidden="true"><path d="M128,24A104,104,0,1,0,232,128,104.11,104.11,0,0,0,128,24Zm0,192a88,88,0,1,1,88-88A88.1,88.1,0,0,1,128,216Zm64-88a8,8,0,0,1-8,8H128a8,8,0,0,1-8-8V72a8,8,0,0,1,16,0v48h48A8,8,0,0,1,192,128Z"/></svg>'
_PIN = '<svg class=nxglyph width="16" height="16" viewBox="0 0 256 256" fill="currentColor" aria-hidden="true"><path d="M128,64a40,40,0,1,0,40,40A40,40,0,0,0,128,64Zm0,64a24,24,0,1,1,24-24A24,24,0,0,1,128,128Zm0-112a88.1,88.1,0,0,0-88,88c0,31.4,14.51,64.68,42,96.25a254.19,254.19,0,0,0,41.45,38.3,8,8,0,0,0,9.18,0A254.19,254.19,0,0,0,174,200.25c27.45-31.57,42-64.85,42-96.25A88.1,88.1,0,0,0,128,16Zm0,206c-16.53-13-72-60.75-72-118a72,72,0,0,1,144,0C200,161.23,144.53,209,128,222Z"/></svg>'
_SUN = '<svg width="16" height="16" viewBox="0 0 256 256" fill="currentColor" aria-hidden="true"><path d="M120,40V16a8,8,0,0,1,16,0V40a8,8,0,0,1-16,0Zm72,88a64,64,0,1,1-64-64A64.07,64.07,0,0,1,192,128Zm-16,0a48,48,0,1,0-48,48A48.05,48.05,0,0,0,176,128ZM58.34,69.66A8,8,0,0,1,69.66,58.34l16,16a8,8,0,0,1-11.32,11.32Zm0,116.68,16-16a8,8,0,0,1,11.32,11.32l-16,16a8,8,0,0,1-11.32-11.32ZM192,72a8,8,0,0,1,5.66-2.34l16-16a8,8,0,0,1,11.32,11.32l-16,16A8,8,0,0,1,192,72Zm5.66,114.34a8,8,0,0,1,0-11.32,8,8,0,0,1,11.32,0l16,16a8,8,0,0,1-11.32,11.32ZM40,120H16a8,8,0,0,0,0,16H40a8,8,0,0,0,0-16Zm200,0H216a8,8,0,0,0,0,16h24a8,8,0,0,0,0-16ZM128,200a8,8,0,0,0-8,8v24a8,8,0,0,0,16,0V208A8,8,0,0,0,128,200Z"/></svg>'


def widget_document(payload, theme=None, preview=False):
    """Standalone iframe. It uses the app fonts and Lineup card structure. Host CSS cannot reach it."""
    import html as htmlmod
    theme = theme if theme in ("night", "day") else payload.get("theme") or "night"
    chips = [(slug, label) for slug, label in CHIPS if slug in (payload.get("chips") or ["all"])]
    if not chips:
        chips = [("all", "All")]
    active = payload.get("default_chip") if payload.get("default_chip") in dict(chips) else chips[0][0]
    e = htmlmod.escape
    org = payload.get("org") or "Schedule"

    def chip_buttons():
        parts = []
        for slug, label in chips:
            on = " chip on" if slug == active else ""
            pressed = "true" if slug == active else "false"
            parts.append('<button type=button class="chip%s" role=tab aria-pressed="%s" data-chip="%s">%s</button>' % (on, pressed, e(slug), e(label)))
        return "".join(parts)

    def public_event(item):
        href = "/register?event=%s" % item["id"] if item.get("signup") else ""
        return {
            "id": item.get("id") or "",
            "title": item.get("title") or "Event",
            "category": item.get("category") or "Event",
            "sport": item.get("sport") or "",
            "activity": item.get("activity") or "",
            "date": item.get("date") or "",
            "time": item.get("time") or "",
            "place": item.get("place") or "",
            "detail": item.get("detail") or "",
            "price": item.get("price") or "",
            "count": item.get("count"),
            "capacity": item.get("capacity"),
            "cancelled": bool(item.get("cancelled")),
            "reason": item.get("reason") or "",
            "signup": href,
            "trial": item.get("trial_line") or "",
        }

    def cards():
        rows = []
        for item in payload.get("events") or []:
            hidden = "" if active == "all" or item.get("chip") == active else " hidden"
            tile = item.get("tile") or {}
            title = e(item.get("title") or "Event")
            if item.get("cancelled"):
                title = "<s>%s</s>" % title
            signup = "/register?event=%s" % e(item["id"]) if item.get("signup") else ""
            bits = ['<article class="card tripcard" role=button tabindex=0 data-id="%s" data-chip="%s" data-signup="%s"%s>' % (
                e(item.get("id") or ""), e(item.get("chip") or "community"), signup, hidden)]
            bits.append('<div class=nxmain><div class=datetile><span class=wd>%s</span><span class=dn>%s</span><span class=mo>%s</span></div>' % (e(tile.get("wd") or ""), e(tile.get("dn") or ""), e(tile.get("mo") or "")))
            bits.append('<div class="grow schedrows"><h2 class=nxtitle>%s</h2>' % title)
            if item.get("time"):
                bits.append('<div class=nxrow>%s<span>%s</span></div>' % (_CLOCK, e(item["time"])))
            if item.get("place"):
                bits.append('<div class=nxrow>%s<span>%s</span></div>' % (_PIN, e(item["place"])))
            bits.append('<div class=tags><span class=chip-info>%s</span>' % e(item.get("category") or "Event"))
            if item.get("sport"):
                bits.append('<span class=chip-info>%s</span>' % e(item["sport"]))
            if item.get("price"):
                bits.append('<span class="chip-info cost">%s</span>' % e(item["price"]))
            if item.get("count") is not None:
                bits.append('<span class=chip-info>%s going</span>' % e(str(item["count"])))
            if item.get("capacity"):
                bits.append('<span class=chip-info>%s spots</span>' % e(str(item["capacity"])))
            bits.append("</div></div></div>")
            if item.get("cancelled"):
                bits.append('<p class=reason>Cancelled%s</p>' % ((" · " + e(item["reason"])) if item.get("reason") else ""))
            if item.get("detail"):
                bits.append('<p class=detail>%s</p>' % e(item["detail"]))
            bits.append("</article>")
            rows.append("".join(bits))
        return "".join(rows)

    event_blob = json.dumps([public_event(item) for item in (payload.get("events") or [])], ensure_ascii=True).replace("<", "\\u003c")

    banner_info = ((payload.get("trial") or {}).get("banner")) or {}
    offer_bits = []
    if payload.get("overview") or payload.get("prices") or banner_info:
        offer_bits.append('<section class="card offer">')
        if payload.get("overview"):
            for line in payload["overview"]:
                text = e(line.get("when") or "")
                if line.get("place"):
                    text += " · " + e(line["place"])
                offer_bits.append("<p class=usual>%s</p>" % text)
        if payload.get("prices"):
            offer_bits.append('<div class=tags>')
            for price in payload["prices"]:
                offer_bits.append('<span class=chip-info>%s</span>' % e(price.get("line") or price_line(price.get("label"), price.get("price"))))
            offer_bits.append("</div>")
        if banner_info:
            offer_bits.append('<div class=callout><h2>%s</h2><p>%s</p>' % (e(banner_info.get("title") or ""), e(banner_info.get("body") or "")))
            if banner_info.get("href"):
                offer_bits.append('<a href="%s" target=_blank rel=noopener>%s</a>' % (e(banner_info["href"]), e(banner_info.get("link") or "Learn more")))
            offer_bits.append("</div>")
        offer_bits.append("</section>")
    return """<!doctype html><html lang=en class="%s"><head><meta charset=utf-8>
<meta name=viewport content="width=device-width,initial-scale=1">
<title>%s</title>
<style>
@font-face{font-family:"Space Grotesk";font-style:normal;font-weight:600;font-display:swap;src:url("/static/fonts/space-grotesk-600.woff2") format("woff2")}
@font-face{font-family:"Space Grotesk";font-style:normal;font-weight:700;font-display:swap;src:url("/static/fonts/space-grotesk-700.woff2") format("woff2")}
@font-face{font-family:"Plus Jakarta Sans";font-style:normal;font-weight:400;font-display:swap;src:url("/static/fonts/plus-jakarta-sans-400.woff2") format("woff2")}
@font-face{font-family:"Plus Jakarta Sans";font-style:normal;font-weight:500;font-display:swap;src:url("/static/fonts/plus-jakarta-sans-500.woff2") format("woff2")}
@font-face{font-family:"Plus Jakarta Sans";font-style:normal;font-weight:600;font-display:swap;src:url("/static/fonts/plus-jakarta-sans-600.woff2") format("woff2")}
:root{color-scheme:dark;--font-display:"Space Grotesk","Plus Jakarta Sans",system-ui,sans-serif;--font-sans:"Plus Jakarta Sans",system-ui,sans-serif;--color-bg:#090D0B;--color-surface:#0F1512;--color-surface-2:#131A16;--color-border:#1B221E;--color-control:#5c665f;--color-text:#F2F6F1;--color-text-secondary:#BEC9C1;--color-lime:#C4E65A;--color-on-selected:#090D0B;--color-chip:#131A16;--radius-card:20px;--radius-control:16px;--radius-chip:999px;--size-chip:36px}
@media (prefers-color-scheme: light){:root{color-scheme:light;--color-bg:#F2F6F1;--color-surface:#FFFFFF;--color-surface-2:#E8EEE9;--color-border:#D9E0DB;--color-control:#5C665F;--color-text:#090D0B;--color-text-secondary:#3A4A40;--color-on-selected:#090D0B;--color-chip:#E8EEE9}}
*{box-sizing:border-box}html,body{margin:0;background:var(--color-bg);color:var(--color-text)}
html.preview,html.preview body{overflow:hidden}
body{font:400 16px/1.5 var(--font-sans);padding:0 0 16px}
header{display:flex;align-items:center;justify-content:space-between;gap:12px;padding:20px 20px 4px}
.brand{display:flex;align-items:center;gap:12px;min-width:0}
.brand img{width:36px;height:36px;border-radius:10px;flex:none}
.brand p{margin:0;color:var(--color-text-secondary);font-size:12px;font-weight:600;letter-spacing:.04em}
h1,.nxtitle,.datetile .dn{font-family:var(--font-display)}
h1{margin:0;font-size:20px;line-height:28px;font-weight:600;letter-spacing:-.02em}
button{font:inherit;color:inherit}
.theme{display:inline-flex;align-items:center;gap:6px;height:36px;padding:0 12px 0 10px;border-radius:999px;border:1px solid var(--color-control);background:var(--color-surface-2);cursor:pointer}
.chipbar{position:relative;margin-top:8px}
.chipbar:before,.chipbar:after{content:"";position:absolute;top:0;bottom:0;width:28px;z-index:1;pointer-events:none}
.chipbar:before{left:0;background:linear-gradient(90deg,var(--color-bg),transparent)}
.chipbar:after{right:0;background:linear-gradient(270deg,var(--color-bg),transparent)}
.chips{display:flex;gap:8px;overflow-x:auto;padding:4px 20px 12px;scrollbar-width:none}
.chips::-webkit-scrollbar{display:none}
.chip{position:relative;display:inline-flex;align-items:center;justify-content:center;height:var(--size-chip);padding:0 14px;border-radius:var(--radius-chip);border:1px solid var(--color-control);background:transparent;color:var(--color-text);font-size:14px;font-weight:500;line-height:1;white-space:nowrap;flex:none;cursor:pointer}
.chip.on{background:var(--color-lime);color:var(--color-on-selected);border-color:var(--color-lime)}
main{padding:4px 20px 0;width:100%%}
#cards{display:grid;grid-template-columns:repeat(auto-fill,minmax(320px,1fr));gap:12px;width:100%%}
#cards .card{margin:0}
.signup{display:inline-flex;align-items:center;height:36px;margin-top:16px;padding:0 14px;border-radius:999px;background:var(--color-lime);color:#090D0B;font-weight:600;text-decoration:none}
.card{background:var(--color-surface);border:1px solid var(--color-border);border-radius:var(--radius-card);padding:16px;margin:0 0 12px;text-align:left;font:inherit;color:inherit}
article.card{cursor:pointer;display:block;width:100%%}
.offer .usual{margin:0 0 8px;color:var(--color-text-secondary)}
.tags{display:flex;flex-wrap:wrap;gap:6px;margin-top:8px}
.chip-info{display:inline-flex;align-items:center;height:28px;padding:0 8px;border-radius:var(--radius-chip);border:1px solid var(--color-border);background:var(--color-chip);color:var(--color-text);font-size:12px;font-weight:500;line-height:1}
.chip-info.cost{background:color-mix(in srgb,var(--color-lime) 22%%,var(--color-surface));border-color:color-mix(in srgb,var(--color-lime) 55%%,var(--color-border))}
.callout{margin:12px 0 0;padding:12px 14px;border-radius:16px;background:color-mix(in srgb,var(--color-lime) 18%%,transparent);border:1px solid color-mix(in srgb,var(--color-lime) 50%%,transparent);font-weight:500}
.nxmain{display:flex;align-items:center;gap:12px}
.datetile{width:56px;height:56px;border-radius:var(--radius-control);background:var(--color-surface-2);display:flex;flex-direction:column;align-items:center;justify-content:center;flex:none}
.datetile .wd,.datetile .mo{font-size:10px;font-weight:700;letter-spacing:.6px;color:var(--color-text-secondary);line-height:1}
.datetile .dn{font-size:18px;font-weight:600;line-height:1.1;margin-top:2px}
.grow{min-width:0;flex:1}
.nxtitle{margin:0 0 2px;font-size:16px;line-height:24px;font-weight:600}
.nxrow{display:flex;align-items:flex-start;gap:8px;margin-top:2px;color:var(--color-text-secondary);font-size:14px;line-height:1.35}
.nxglyph{flex:none;margin-top:2px}
.detail,.reason{margin:12px 0 0;color:var(--color-text-secondary)}
.state{display:flex;flex-direction:column;align-items:flex-start;gap:8px;padding:8px 4px 20px;color:var(--color-text-secondary)}
.state[hidden],article[hidden],#browse[hidden],#sheet[hidden]{display:none}
#sheet{padding:8px 20px 20px}
#sheetBack{height:36px;padding:0 14px;border-radius:999px;border:1px solid var(--color-control);background:var(--color-surface-2);color:inherit;cursor:pointer}
#sheet h2{margin:16px 0 8px;font-size:22px;line-height:28px}
#sheet p{margin:8px 0}
#sheet a.place{color:inherit}
.state h2{margin:0;font-family:var(--font-display);font-size:20px;color:var(--color-text)}
.state p{margin:0}
.spin{width:22px;height:22px;border:2px solid var(--color-border);border-top-color:var(--color-lime);border-radius:50%%;animation:spin .7s linear infinite}
@keyframes spin{to{transform:rotate(360deg)}}
#retry{height:40px;padding:0 14px;border-radius:12px;border:1px solid var(--color-control);background:var(--color-surface-2);cursor:pointer}
:focus-visible{outline:2px solid var(--color-lime);outline-offset:2px}
</style></head><body>
<div id=browse>
<header><div class=brand><img src="/static/icons/icon-192.png?v=119" alt="" width="36" height="36"><div><p>Regulars</p><h1>%s</h1></div></div></header>
<div class=chipbar><div class=chips role=tablist aria-label="Categories">%s</div></div>
<main>%s
<div id=loading class=state role=status><span class=spin aria-hidden=true></span><p>Loading the schedule</p></div>
<div id=empty class=state hidden><h2>Nothing coming up</h2><p>Published practices and events will show here.</p></div>
<div id=error class=state hidden><h2>Couldn't load the schedule</h2><p>Check the connection and try again.</p><button type=button id=retry>Try again</button></div>
<div id=cards>%s</div>
</main>
</div>
<div id=sheet hidden>
<button type=button id=sheetBack>Back</button>
<h2 id=sheetTitle></h2>
<div class=tags id=sheetChips></div>
<p id=sheetDate></p>
<p id=sheetTime></p>
<p id=sheetPlace></p>
<p id=sheetDetail></p>
<p id=sheetCount></p>
<p id=sheetPrice></p>
<p id=sheetTrial></p>
<p id=sheetReason></p>
<a id=sheetSignup class=signup target=_top>Sign up</a>
</div>
<script type="application/json" id=eventData>%s</script>
<script>
(function(){
  var root=document.documentElement, cards=document.getElementById("cards"), chips=[].slice.call(document.querySelectorAll(".chips button"));
  var loading=document.getElementById("loading"), empty=document.getElementById("empty"), error=document.getElementById("error");
  var browse=document.getElementById("browse"), sheet=document.getElementById("sheet"), back=document.getElementById("sheetBack");
  var events={}; try{ JSON.parse(document.getElementById("eventData").textContent).forEach(function(ev){ events[ev.id]=ev; }); }catch(err){}
  var opener=null;
  function report(){var h=Math.ceil(document.documentElement.scrollHeight);try{parent.postMessage({type:"regulars-widget",height:h},"*");}catch(e){}}
  function text(id, value){ var el=document.getElementById(id); el.hidden=!value; el.textContent=value||""; }
  function chip(label){ var s=document.createElement("span"); s.className="chip-info"; s.textContent=label; return s; }
  function openDetail(id, from){
    var ev=events[id]; if(!ev) return;
    opener=from||null;
    document.getElementById("sheetTitle").textContent=ev.title||"Event";
    var box=document.getElementById("sheetChips"); box.textContent="";
    if(ev.sport) box.appendChild(chip(ev.sport));
    if(ev.activity) box.appendChild(chip(ev.activity));
    if(ev.category) box.appendChild(chip(ev.category));
    text("sheetDate", ev.date);
    text("sheetTime", ev.time);
    var place=document.getElementById("sheetPlace"); place.textContent="";
    if(ev.place){
      var link=document.createElement("a"); link.className="place"; link.target="_blank"; link.rel="noopener";
      link.href="https://www.google.com/maps/search/?api=1&query="+encodeURIComponent(ev.place);
      link.textContent=ev.place; place.appendChild(link); place.hidden=false;
    } else place.hidden=true;
    text("sheetDetail", ev.detail);
    text("sheetCount", ev.count==null?"":(ev.count+" going"));
    text("sheetPrice", ev.price||"");
    text("sheetTrial", ev.trial||"");
    text("sheetReason", ev.cancelled?(ev.reason?("Cancelled · "+ev.reason):"Cancelled"):"");
    var go=document.getElementById("sheetSignup");
    if(ev.signup){ go.href=ev.signup; go.hidden=false; } else { go.hidden=true; go.removeAttribute("href"); }
    browse.hidden=true; sheet.hidden=false; back.focus(); report();
  }
  function closeDetail(){ sheet.hidden=true; browse.hidden=false; if(opener) opener.focus(); report(); }
  function show(name){
    var n=0;
    chips.forEach(function(btn){var on=btn.getAttribute("data-chip")===name;btn.setAttribute("aria-pressed",on?"true":"false");btn.classList.toggle("on",on);});
    [].slice.call(cards.children).forEach(function(card){
      var chipName=card.getAttribute("data-chip");
      var hide=name!=="all"&&chipName!==name;
      card.hidden=hide; if(!hide) n++;
    });
    empty.hidden=n>0;
    report();
  }
  function ready(){loading.hidden=true; error.hidden=true; root.setAttribute("data-ready","1"); show(document.querySelector(".chips button.on") ? document.querySelector(".chips button.on").getAttribute("data-chip") : "all");}
  chips.forEach(function(btn){btn.addEventListener("click",function(){show(btn.getAttribute("data-chip"));});});
  cards.addEventListener("click", function(ev){ var card=ev.target.closest("article.card"); if(card) openDetail(card.getAttribute("data-id"), card); });
  cards.addEventListener("keydown", function(ev){
    if(ev.key!=="Enter" && ev.key!==" ") return;
    var card=ev.target.closest("article.card"); if(!card) return;
    ev.preventDefault(); openDetail(card.getAttribute("data-id"), card);
  });
  back.addEventListener("click", closeDetail);
  document.addEventListener("keydown", function(ev){ if(ev.key==="Escape" && !sheet.hidden) closeDetail(); });
  document.getElementById("retry").addEventListener("click", function(){
    loading.hidden=false; error.hidden=true; empty.hidden=true;
    fetch("/api/public/feed",{credentials:"same-origin"}).then(function(r){if(!r.ok) throw new Error("bad"); return r.json();}).then(function(){ready();}).catch(function(){loading.hidden=true; error.hidden=false; report();});
  });
  if(cards.children.length) ready();
  else { loading.hidden=true; empty.hidden=false; root.setAttribute("data-ready","1"); report(); }
  var scheme=window.matchMedia("(prefers-color-scheme: light)");
  function applyScheme(){root.setAttribute("data-scheme", scheme.matches ? "light" : "dark"); report();}
  applyScheme();
  if(scheme.addEventListener) scheme.addEventListener("change", applyScheme);
  window.addEventListener("resize", report);
})();
</script></body></html>""" % (
        "preview" if preview else "", e(org), e(org), chip_buttons(), "".join(offer_bits), cards(), event_blob,
    )


WIDGET_ADMIN = """<style>
.daypick{display:flex;flex-wrap:wrap;gap:8px 12px;margin:0 0 12px}
.pill{height:36px;padding:0 14px;border-radius:999px;border:1px solid var(--color-control);background:transparent;color:var(--t1);font:500 14px/1 var(--font-sans);cursor:pointer}
.pill.on{background:var(--color-lime);border-color:var(--color-lime);color:#090D0B}
#widgetPreview{width:100%;max-width:100%;height:1px;margin-top:12px;border:1px solid var(--line);border-radius:16px;overflow:hidden;display:block;background:#0A0D0A}
#embedCode{display:block;width:100%;box-sizing:border-box;margin:12px 0 0;padding:16px;line-height:1.5}
.embedrow{display:flex;flex-wrap:wrap;gap:12px;align-items:center;margin-top:16px}
.embedrow .btn{margin:0}
#copied{margin:12px 0 0}
</style>
{{ admin_page('Website widget', 'Visitors see this only after you publish it. The embed keeps working when you change these settings.') }}
<form method=post>
{{ csrf_field() }}
<label class=switchrow>Publish on the website<span class=switch><input type=checkbox name=widget_on value=1 {% if w.enabled %}checked{% endif %}><span></span></span></label>
<p class="t3 sm">The public widget follows the visitor's light or dark appearance. There is no separate theme switch.</p>
<div class=seclabel>Chips</div>
<div class="daypick pillset" role=group aria-label="Chips">
{% for slug, label in chip_choices %}<button type=button class="pill{% if slug in w.chips %} on{% endif %}" data-name="chip_{{ slug }}">{{ label }}</button><input type=hidden name="chip_{{ slug }}" value="{{ '1' if slug in w.chips else '0' }}">{% endfor %}
</div>
<label>Opens on<select name=default_chip>{% for slug, label in chip_choices %}<option value="{{ slug }}" {% if w.default_chip == slug %}selected{% endif %}>{{ label }}</option>{% endfor %}</select></label>
<label class=switchrow>Show the regular schedule<span class=switch><input type=checkbox name=include_schedule value=1 {% if w.include_schedule %}checked{% endif %}><span></span></span></label>
<label class=switchrow>Show prices that are filled in<span class=switch><input type=checkbox name=show_pricing value=1 {% if w.show_pricing %}checked{% endif %}><span></span></span></label>
<label class=switchrow>Show the free-trial message<span class=switch><input type=checkbox name=show_trial value=1 {% if w.show_trial %}checked{% endif %}><span></span></span></label>
<label class=switchrow>Show how many are going<span class=switch><input type=checkbox name=show_counts value=1 {% if w.show_counts %}checked{% endif %}><span></span></span></label>
<p class="t3 sm">Counts are numbers only. Names and photos stay off the widget.</p>
<label class=switchrow>Hide events that already ended<span class=switch><input type=checkbox name=hide_past value=1 {% if w.hide_past %}checked{% endif %}><span></span></span></label>
<label>Events in preview<input name=limit inputmode=numeric value="{{ w.limit }}"></label>
<p class="t3 sm">The live widget shows every upcoming event. This number is only for the preview on this page.</p>
<button class="btn btn-primary full" type=submit>Save</button>
</form>
<h2>Preview</h2>
<p class="t3 sm">Same schedule as the live widget, limited to the event count above. It is the full width of this page and does not scroll inside the frame. The public embed stays empty until you publish.</p>
<iframe id=widgetPreview title="Widget preview" src="/widget?preview=1" scrolling=no></iframe>
<h2>Embed code</h2>
<p class="t3 sm">Paste this once. Later changes show up without a new snippet.</p>
<textarea id=embedCode class=planfield rows=8 readonly>{{ embed }}</textarea>
<div class=embedrow>
<button type=button class="btn btn-secondary" id=copyEmbed>Copy embed code</button>
<a class="btn btn-secondary" href="/widget?preview=1">Open the preview</a>
</div>
<p class="t3 sm" id=copied hidden>Copied.</p>
<script>
(function(){
  document.querySelectorAll(".pillset .pill").forEach(function(btn){
    btn.addEventListener("click", function(){
      btn.classList.toggle("on");
      var input=btn.parentNode.querySelector('input[name="'+btn.getAttribute("data-name")+'"]');
      if(input) input.value=btn.classList.contains("on")?"1":"0";
    });
  });
  var frame=document.getElementById("widgetPreview");
  document.getElementById("copyEmbed").onclick=function(){
    var text=document.getElementById("embedCode").value;
    if(navigator.clipboard) navigator.clipboard.writeText(text);
    document.getElementById("copied").hidden=false;
  };
  window.addEventListener("message", function(e){
    if(!frame||e.source!==frame.contentWindow||!e.data||e.data.type!=="regulars-widget") return;
    if(e.data.height) frame.style.height=e.data.height+"px";
  });
})();
</script>
"""


REGISTER_PAGE = """
{{ csrf_field() }}
<h1>Register</h1>
<p class=nxtitle>{{ title }}</p>
<p class="t3 sm">{{ when }}{% if place %} · {{ place }}{% endif %}</p>
<ol class="t3 sm">
<li>Sign in or create an account</li>
<li>Check the free-trial offer and USA Water Polo coverage</li>
<li>Confirm only after every requirement is met</li>
</ol>
{% if state == 'signin' %}
<h2>Sign in</h2>
<p>Sign in or create an account to register for this session. Joining the club is not required.</p>
<p><a class="btn btn-primary" href="/login">Sign in</a></p>
<p><a class="btn btn-secondary" href="/join">Create an account</a></p>
{% elif state == 'claim' %}
<h2>USA Water Polo trial</h2>
<p>{{ reason }}</p>
<p class="t3 sm">Enter the trial details you have. Grunions verifies them. A claim is not verified coverage, and this does not start the trial by itself.</p>
<form method=post>
{{ csrf_field() }}
<input type=hidden name=action value=claim>
<input type=hidden name=event value="{{ event }}">
<label>USA Water Polo number<input name=usawp_number inputmode=numeric autocomplete=off></label>
<label>Trial starts<input type=date name=claim_start value="{{ today }}"></label>
<label>Valid through<input type=date name=claim_until></label>
<button class="btn btn-primary" type=submit>Submit for verification</button>
</form>
<p><a href="{{ trial_url }}" target=_blank rel=noopener>Learn about USA Water Polo trial membership</a></p>
{% elif state == 'pending' %}
<h2>Pending USAWP verification</h2>
<p>{{ reason }}</p>
<p class="t3 sm">Registration stays closed until the trial membership is verified. Nothing is charged.</p>
<p><a href="{{ trial_url }}" target=_blank rel=noopener>Learn about USA Water Polo trial membership</a></p>
{% elif state == 'eligible' %}
<h2>Eligible trial applied</h2>
<p>{{ reason }}</p>
{% if start or end %}<p>Coverage {{ start }}{% if end %} through {{ end }}{% endif %}.</p>{% endif %}
{% if balance and balance.total %}<p>{{ balance.remaining }} of {{ balance.total }} free practices left. {{ balance.used }} attended, {{ balance.held }} reserved.</p>{% endif %}
<form method=post>
{{ csrf_field() }}
<input type=hidden name=action value=confirm>
<input type=hidden name=event value="{{ event }}">
<button class="btn btn-primary" type=submit>Confirm registration</button>
</form>
<p class="t3 sm">Confirming uses the free trial for this session. It does not charge a card or start a subscription.</p>
{% elif state == 'confirmed' %}
<h2>You're registered</h2>
<p>Eligible trial applied. Nothing was charged.</p>
{% if start or end %}<p>Coverage {{ start }}{% if end %} through {{ end }}{% endif %}.</p>{% endif %}
{% else %}
<h2>{{ label or 'Not eligible' }}</h2>
<p>{{ reason }}</p>
<p class="t3 sm">The usual subscription, pass, or drop-in price applies after the trial. Nothing is charged from this page, and you are not enrolled automatically.</p>
{% endif %}
"""
