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
