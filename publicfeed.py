"""Public schedule, prices, and free-trial rules.

These describe what an organization usually offers. Saving them does not create
practices or Lineup events. Blank prices are omitted, never filled in.
"""
import datetime as dt
import json
import re
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
            "enabled": False, "includes": "", "visits": "", "first_time_only": True,
            "days": "", "conditions": "", "message": "",
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
    trial["includes"] = _words(_get(form, "trial_includes"), 180)
    trial["visits"] = _count(_get(form, "trial_visits"), "free practices")
    trial["first_time_only"] = _get(form, "trial_first") == "1"
    trial["days"] = _count(_get(form, "trial_days"), "how long the trial lasts")
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
    return _merge(data, stored if isinstance(stored, dict) else {})


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
        item = {"label": label, "price": amount, "detail": ""}
        if key == "monthly":
            item["detail"] = pricing.get("monthly_desc") or ""
        prices.append(item)
    for pas in pricing.get("passes") or []:
        if not (pas.get("name") or pas.get("price")):
            continue
        detail = pas.get("description") or ""
        if pas.get("visits"):
            detail = ("%s visits" % pas["visits"] + (" · " + detail if detail else "")).strip()
        prices.append({"label": pas.get("name") or "Practice pass", "price": pas.get("price") or "", "detail": detail})
    for fee in pricing.get("fees") or []:
        if not (fee.get("name") or fee.get("price")):
            continue
        prices.append({"label": fee.get("name") or "Fee", "price": fee.get("price") or "", "detail": fee.get("description") or ""})
    trial = None
    raw = data.get("trial") or {}
    if raw.get("enabled"):
        trial = {
            "enabled": True,
            "includes": raw.get("includes") or "",
            "visits": raw.get("visits") or "",
            "first_time_only": bool(raw.get("first_time_only")),
            "days": raw.get("days") or "",
            "conditions": raw.get("conditions") or "",
            "message": raw.get("message") or "",
        }
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


def trial_claim_open(data, member):
    """A first-time offer cannot be claimed again after the existing trial acknowledgment."""
    trial = (data.get("trial") or {})
    if not trial.get("enabled"):
        return False
    if not trial.get("first_time_only"):
        return True
    if not member:
        return True
    try:
        claimed = member["trial_acknowledged_at"]
    except (KeyError, TypeError, IndexError):
        claimed = None
    return not claimed


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
        "hide_past": True, "limit": 12, "include_schedule": True,
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
    limit = _count(_get(form, "limit") or "12", "how many events to show") or "12"
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


def build_feed(d, data, practice_title, now, org):
    """Public cards only. No names, photos, plans, or private notes."""
    widget = data.get("widget") or widget_blank()
    offer = public_view(data)
    hide_past = widget.get("hide_past", True)
    show_price = bool(widget.get("show_pricing"))
    show_trial = bool(widget.get("show_trial")) and offer.get("trial")
    show_counts = bool(widget.get("show_counts"))
    drop_in = ""
    if show_price:
        for price in offer["prices"]:
            if price["label"] == "Drop-in" and price.get("price"):
                drop_in = price["price"]
                break
    trial_line = ""
    if show_trial and offer["trial"].get("message"):
        trial_line = offer["trial"]["message"]
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
            item = {
                "id": "p-%d" % row["id"],
                "chip": "schedule",
                "title": practice_title(row),
                "when": "%s · %s" % (_short_day(row["date"]), _span({"start": row["start"], "end": row["end"]})),
                "place": row["location"] or "",
                "detail": _words(row["note"], 280),
                "cancelled": bool(row["cancelled"]),
                "reason": _words(row["cancel_reason"], 180) if row["cancelled"] else "",
                "price": drop_in,
                "trial": trial_line,
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
                "title": _words(row["title"], 120),
                "when": "%s · %s" % (_short_day(row["date"]), _span({"start": row["start_time"], "end": row["end_time"]})),
                "place": place,
                "detail": _words(row["description"], 280),
                "cancelled": False,
                "reason": "",
                "price": cost,
                "trial": "",
                "count": None,
                "capacity": row["capacity"] if row["capacity"] else None,
                "sort": _stamp(row["date"], row["start_time"]),
            })
    events.sort(key=lambda item: (item["sort"], item["id"]))
    limit = min(40, max(1, int(widget.get("limit") or 12)))
    events = events[:limit]
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
.slotblock{margin:0 0 8px}
.offerline{margin:0}
</style>
{{ admin_page('Schedule & pricing', 'The regular schedule is when you usually practice. Saving it does not add sessions. Create those in Schedule.') }}
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
<label>What it includes<input name=trial_includes value="{{ s.trial.includes }}" autocomplete=off></label>
<label>Free practices<input name=trial_visits value="{{ s.trial.visits }}" inputmode=numeric autocomplete=off></label>
<label class=switchrow>First time only<span class=switch><input type=checkbox name=trial_first value=1 {% if s.trial.first_time_only %}checked{% endif %}><span></span></span></label>
<p class="t3 sm">Someone who already started the trial on their membership card cannot claim a first-time offer again.</p>
<label>Expires after (days)<input name=trial_days value="{{ s.trial.days }}" inputmode=numeric autocomplete=off></label>
<label>Conditions<textarea class=planfield name=trial_conditions rows=3>{{ s.trial.conditions }}</textarea></label>
<label>Public message<textarea class=planfield name=trial_message rows=3 placeholder="Shown only when the trial is on">{{ s.trial.message }}</textarea></label>
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
{% if offer.prices %}<div class=seclabel>Pricing</div>{% for price in offer.prices %}<p class=offerline>{{ price.label }}{% if price.price %} · {{ price.price }}{% endif %}{% if price.detail %} · {{ price.detail }}{% endif %}</p>{% endfor %}
{% else %}<p class="t3 sm">No prices to show.</p>{% endif %}
{% if offer.trial %}{% if offer.trial.message %}<p>{{ offer.trial.message }}</p>{% endif %}{% if offer.trial.includes %}<p class="t3 sm">{{ offer.trial.includes }}</p>{% endif %}{% if offer.trial.visits %}<p class="t3 sm">{{ offer.trial.visits }} free practices</p>{% endif %}
{% else %}<p class="t3 sm">No free-trial offer.</p>{% endif %}
</div>
"""


def embed_snippet(base):
    src = base.rstrip("/") + "/widget"
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
    ) % src


def widget_document(payload, theme=None):
    """Standalone iframe document. Host styles cannot reach it."""
    import html as htmlmod
    theme = theme if theme in ("night", "day") else payload.get("theme") or "night"
    chips = [(slug, label) for slug, label in CHIPS if slug in (payload.get("chips") or ["all"])]
    if not chips:
        chips = [("all", "All")]
    active = payload.get("default_chip") if payload.get("default_chip") in dict(chips) else chips[0][0]
    e = htmlmod.escape

    def chip_buttons():
        parts = []
        for slug, label in chips:
            pressed = "true" if slug == active else "false"
            parts.append('<button type=button role=tab aria-pressed="%s" data-chip="%s">%s</button>' % (pressed, e(slug), e(label)))
        return "".join(parts)

    def cards():
        rows = []
        for item in payload.get("events") or []:
            bits = ['<article class=card data-chip="%s"' % e(item.get("chip") or "community")]
            if item.get("chip") != active and active != "all":
                bits[0] += " hidden"
            bits[0] += ">"
            title = e(item.get("title") or "Event")
            if item.get("cancelled"):
                title = '<s>%s</s>' % title
            bits.append("<h2>%s</h2>" % title)
            if item.get("cancelled"):
                bits.append('<p class=meta>Cancelled%s</p>' % ((" · " + e(item["reason"])) if item.get("reason") else ""))
            if item.get("when"):
                bits.append("<p>%s</p>" % e(item["when"]))
            if item.get("place"):
                bits.append('<p class=meta>%s</p>' % e(item["place"]))
            if item.get("detail"):
                bits.append("<p>%s</p>" % e(item["detail"]))
            if item.get("price"):
                bits.append('<p class=meta>%s</p>' % e(item["price"]))
            if item.get("trial"):
                bits.append('<p class=trial>%s</p>' % e(item["trial"]))
            if item.get("capacity"):
                bits.append('<p class=meta>%s spots</p>' % e(str(item["capacity"])))
            if item.get("count") is not None:
                bits.append('<p class=meta>%s going</p>' % e(str(item["count"])))
            bits.append("</article>")
            rows.append("".join(bits))
        return "".join(rows) or '<p class=empty data-empty>Nothing coming up.</p>'

    overview = []
    for line in payload.get("overview") or []:
        text = e(line.get("when") or "")
        if line.get("place"):
            text += " · " + e(line["place"])
        overview.append("<p class=usual>%s</p>" % text)
    prices = []
    for price in payload.get("prices") or []:
        text = e(price.get("label") or "")
        if price.get("price"):
            text += " · " + e(price["price"])
        prices.append("<p class=meta>%s</p>" % text)
    trial = ""
    if payload.get("trial") and payload["trial"].get("message"):
        trial = '<p class=trial>%s</p>' % e(payload["trial"]["message"])
    toggle = ""
    if payload.get("visitor_theme"):
        other = "Day" if theme == "night" else "Night"
        toggle = '<button type=button id=theme>%s</button>' % other
    return """<!doctype html><html lang=en data-theme="%s"><head><meta charset=utf-8>
<meta name=viewport content="width=device-width,initial-scale=1">
<title>%s</title>
<style>
:root{color-scheme:dark;--bg:#0A0D0A;--card:#171C18;--text:#F4F7F2;--muted:#9AA59C;--line:#2C342F;--lime:#C4E65A;--ink:#141614}
html[data-theme=day]{color-scheme:light;--bg:#F3F4F0;--card:#FFFFFF;--text:#141614;--muted:#5C6560;--line:#E1E4DC}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--text);font:16px/1.4 "Plus Jakarta Sans",Segoe UI,sans-serif}
header{display:flex;align-items:center;justify-content:space-between;gap:12px;padding:16px 16px 0}
h1{font:600 22px/1.2 "Space Grotesk",Segoe UI,sans-serif;margin:0}
button,article{font:inherit}
#theme, .chips button{border:1px solid var(--line);background:transparent;color:var(--text);border-radius:999px;min-height:36px;padding:0 12px}
.chips{display:flex;gap:8px;overflow-x:auto;padding:12px 16px 4px}
.chips button[aria-pressed=true]{background:var(--lime);color:var(--ink);border-color:var(--lime);font-weight:650}
main{padding:8px 16px 24px}
.usual,.meta{color:var(--muted);margin:0 0 8px}
.trial{margin:0 0 12px}
.card{background:var(--card);border:1px solid var(--line);border-radius:16px;padding:16px;margin:0 0 12px}
.card h2{font:600 18px/1.25 "Space Grotesk",Segoe UI,sans-serif;margin:0 0 6px}
.card p{margin:0 0 6px}.empty{color:var(--muted)}
:focus-visible{outline:2px solid var(--lime);outline-offset:2px}
</style></head><body>
<header><h1>%s</h1>%s</header>
<div class=chips role=tablist aria-label="Categories">%s</div>
<main>%s%s%s<div id=list>%s</div></main>
<script>
(function(){
  var root=document.documentElement, list=document.getElementById("list"), chips=[].slice.call(document.querySelectorAll(".chips button"));
  function show(name){
    chips.forEach(function(btn){btn.setAttribute("aria-pressed", btn.getAttribute("data-chip")===name ? "true" : "false");});
    [].slice.call(list.children).forEach(function(card){
      if(!card.getAttribute) return;
      var chip=card.getAttribute("data-chip");
      if(!chip){card.hidden = name!=="all" && !list.querySelector('[data-chip="'+name+'"]'); return;}
      card.hidden = name!=="all" && chip!==name;
    });
    report();
  }
  chips.forEach(function(btn){btn.addEventListener("click", function(){show(btn.getAttribute("data-chip"));});});
  var themeBtn=document.getElementById("theme");
  if(themeBtn) themeBtn.addEventListener("click", function(){
    var next=root.getAttribute("data-theme")==="night"?"day":"night";
    root.setAttribute("data-theme", next);
    themeBtn.textContent = next==="night" ? "Day" : "Night";
    report();
  });
  function report(){
    var h=Math.ceil(document.documentElement.scrollHeight);
    try{parent.postMessage({type:"regulars-widget", height:h}, "*");}catch(e){}
  }
  report();
  window.addEventListener("resize", report);
})();
</script></body></html>""" % (
        e(theme), e(payload.get("org") or "Schedule"), e(payload.get("org") or "Schedule"),
        toggle, chip_buttons(), trial, "".join(prices), "".join(overview), cards(),
    )


WIDGET_ADMIN = """<style>
.daypick{display:flex;flex-wrap:wrap;gap:8px 12px;margin:0 0 12px}
.daypick label{display:flex;align-items:center;gap:6px;margin:0;min-height:40px;color:var(--t1);font-size:15px}
</style>
{{ admin_page('Website widget', 'Visitors see this only after you publish it. The embed keeps working when you change these settings.') }}
<form method=post>
{{ csrf_field() }}
<label class=switchrow>Publish on the website<span class=switch><input type=checkbox name=widget_on value=1 {% if w.enabled %}checked{% endif %}><span></span></span></label>
<div class=seclabel>Default appearance</div>
<div class=daypick role=radiogroup aria-label="Theme">
<label><input type=radio name=theme value=night {% if w.theme != 'day' %}checked{% endif %}> Night</label>
<label><input type=radio name=theme value=day {% if w.theme == 'day' %}checked{% endif %}> Day</label>
</div>
<label class=switchrow>Visitors can switch Night and Day<span class=switch><input type=checkbox name=visitor_theme value=1 {% if w.visitor_theme %}checked{% endif %}><span></span></span></label>
<div class=seclabel>Chips</div>
<div class=daypick role=group aria-label="Chips">
{% for slug, label in chip_choices %}<label><input type=checkbox name="chip_{{ slug }}" value=1 {% if slug in w.chips %}checked{% endif %}> {{ label }}</label>{% endfor %}
</div>
<label>Opens on<select name=default_chip>{% for slug, label in chip_choices %}<option value="{{ slug }}" {% if w.default_chip == slug %}selected{% endif %}>{{ label }}</option>{% endfor %}</select></label>
<label class=switchrow>Show the regular schedule<span class=switch><input type=checkbox name=include_schedule value=1 {% if w.include_schedule %}checked{% endif %}><span></span></span></label>
<label class=switchrow>Show prices that are filled in<span class=switch><input type=checkbox name=show_pricing value=1 {% if w.show_pricing %}checked{% endif %}><span></span></span></label>
<label class=switchrow>Show the free-trial message<span class=switch><input type=checkbox name=show_trial value=1 {% if w.show_trial %}checked{% endif %}><span></span></span></label>
<label class=switchrow>Show how many are going<span class=switch><input type=checkbox name=show_counts value=1 {% if w.show_counts %}checked{% endif %}><span></span></span></label>
<p class="t3 sm">Counts are numbers only. Names and photos stay off the widget.</p>
<label class=switchrow>Hide events that already ended<span class=switch><input type=checkbox name=hide_past value=1 {% if w.hide_past %}checked{% endif %}><span></span></span></label>
<label>Upcoming events to show<input name=limit inputmode=numeric value="{{ w.limit }}"></label>
<button class="btn btn-primary full" type=submit>Save</button>
</form>
<h2>Preview</h2>
<p class="t3 sm">This preview uses your admin login. The public embed stays empty until you publish.</p>
<div class=daypick>
<button type=button class="btn btn-secondary" id=prevMobile>390</button>
<button type=button class="btn btn-secondary" id=prevDesk>1280</button>
</div>
<iframe id=widgetPreview title="Widget preview" src="/widget?preview=1" style="width:min(100%,390px);height:640px;border:1px solid var(--line);border-radius:16px;background:#0A0D0A"></iframe>
<h2>Embed code</h2>
<p class="t3 sm">Paste this once. Later changes show up without a new snippet.</p>
<textarea id=embedCode class=planfield rows=8 readonly>{{ embed }}</textarea>
<button type=button class="btn btn-secondary" id=copyEmbed>Copy embed code</button>
<p class="t3 sm" id=copied hidden>Copied.</p>
<p><a href="/widget?preview=1">Open the preview</a></p>
<script>
(function(){
  var frame=document.getElementById("widgetPreview");
  document.getElementById("prevMobile").onclick=function(){frame.style.width="min(100%,390px)";};
  document.getElementById("prevDesk").onclick=function(){frame.style.width="min(100%,1280px)";};
  document.getElementById("copyEmbed").onclick=function(){
    var text=document.getElementById("embedCode").value;
    if(navigator.clipboard) navigator.clipboard.writeText(text);
    document.getElementById("copied").hidden=false;
  };
  window.addEventListener("message", function(e){
    if(!frame||e.source!==frame.contentWindow||!e.data||e.data.type!=="regulars-widget") return;
    if(e.data.height) frame.style.height=Math.max(320, e.data.height)+"px";
  });
})();
</script>
"""
