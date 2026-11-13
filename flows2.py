"""Regulars 2.0 flows that need real data behind them.

Member: one-sheet sign-up gate (insurance number + club waiver) on Going, rides, 18+ date of birth,
usual week, Finish setup. Coach: check-in hold reasons, wrap-up and close. Admin: club waiver settings.

Every schema change here is additive. Nothing on boot deletes or rewrites existing rows.
"""
import datetime as dt
import re

ADULT_AGE = 18
DAYS = ("Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun")


def _cols(d, table):
    return {r[1] for r in d.execute("PRAGMA table_info(%s)" % table)}


def ensure_schema(d):
    d.execute("""CREATE TABLE IF NOT EXISTS club_waiver(
        id INTEGER PRIMARY KEY CHECK (id = 1), enabled INTEGER NOT NULL DEFAULT 0, title TEXT,
        version INTEGER NOT NULL DEFAULT 1, body TEXT, url TEXT, updated_at TEXT, updated_by TEXT)""")
    d.execute("INSERT OR IGNORE INTO club_waiver(id, enabled, title, version) VALUES(1, 0, 'Club liability waiver', 1)")
    d.execute("""CREATE TABLE IF NOT EXISTS waiver_acceptances(
        id INTEGER PRIMARY KEY, member_id INTEGER NOT NULL, version INTEGER NOT NULL, title TEXT,
        typed_name TEXT NOT NULL, practice_id INTEGER, at TEXT NOT NULL)""")
    d.execute("CREATE INDEX IF NOT EXISTS waiver_acc_member ON waiver_acceptances(member_id, version)")
    d.execute("""CREATE TABLE IF NOT EXISTS ride_requests(
        id INTEGER PRIMARY KEY, practice_id INTEGER NOT NULL, rider_id INTEGER NOT NULL, area TEXT NOT NULL,
        back INTEGER NOT NULL DEFAULT 0, note TEXT, status TEXT NOT NULL DEFAULT 'open', driver_id INTEGER,
        pickup_note TEXT, created TEXT NOT NULL, matched_at TEXT)""")
    d.execute("""CREATE TABLE IF NOT EXISTS ride_offers(
        id INTEGER PRIMARY KEY, practice_id INTEGER NOT NULL, driver_id INTEGER NOT NULL, area TEXT NOT NULL,
        seats INTEGER NOT NULL DEFAULT 1, back INTEGER NOT NULL DEFAULT 0, status TEXT NOT NULL DEFAULT 'open',
        created TEXT NOT NULL, UNIQUE(practice_id, driver_id))""")
    d.execute("""CREATE TABLE IF NOT EXISTS practice_wraps(
        practice_id INTEGER PRIMARY KEY, admin_note TEXT, recap TEXT, closed_by INTEGER, closed_at TEXT)""")
    d.execute("""CREATE TABLE IF NOT EXISTS avail_windows(
        id INTEGER PRIMARY KEY, member_id INTEGER NOT NULL, weekday INTEGER NOT NULL, start TEXT NOT NULL, end TEXT NOT NULL)""")
    d.execute("CREATE INDEX IF NOT EXISTS avail_windows_member ON avail_windows(member_id, weekday)")
    d.execute("""CREATE TABLE IF NOT EXISTS away_dates(
        id INTEGER PRIMARY KEY, member_id INTEGER NOT NULL, start_date TEXT NOT NULL, end_date TEXT NOT NULL, note TEXT)""")
    d.execute("""CREATE TABLE IF NOT EXISTS lineup_shifts(
        id INTEGER PRIMARY KEY, event_id INTEGER NOT NULL, start TEXT NOT NULL, end TEXT NOT NULL, title TEXT NOT NULL,
        capacity INTEGER NOT NULL DEFAULT 1, created TEXT)""")
    d.execute("CREATE INDEX IF NOT EXISTS lineup_shifts_event ON lineup_shifts(event_id, start)")
    d.execute("""CREATE TABLE IF NOT EXISTS shift_signups(
        shift_id INTEGER NOT NULL, member_id INTEGER NOT NULL, at TEXT NOT NULL, PRIMARY KEY(shift_id, member_id))""")
    d.execute("CREATE TABLE IF NOT EXISTS club_prefs(key TEXT PRIMARY KEY, value TEXT)")
    # Tools › Usage: map/traffic calls per day by what used them (counts only, no places or people).
    d.execute("CREATE TABLE IF NOT EXISTS route_usage(day TEXT NOT NULL, purpose TEXT NOT NULL, calls INTEGER NOT NULL DEFAULT 0, PRIMARY KEY(day, purpose))")
    # 04.09 leave-by alert per member per practice: the last leave-by we told them, and when we last checked traffic.
    d.execute("""CREATE TABLE IF NOT EXISTS leave_alerts(
        member_id INTEGER NOT NULL, practice_id INTEGER NOT NULL, leave_by TEXT, checked TEXT, PRIMARY KEY(member_id, practice_id))""")
    have = _cols(d, "members")
    for col, ddl in (("birth_date", "TEXT"), ("avail_days", "TEXT"), ("setup_dismissed", "INTEGER DEFAULT 0"),
                     ("ride_offer", "INTEGER DEFAULT 0"), ("ride_area", "TEXT"), ("ride_seats", "INTEGER DEFAULT 2"),
                     ("leave_buffer", "INTEGER DEFAULT 5"), ("auto_rsvp", "INTEGER DEFAULT 0"),
                     # Last location: rounded to ~100 m, saved only when the member's own device shares it, never shown to anyone.
                     ("save_location", "INTEGER DEFAULT 1"), ("last_lat", "REAL"), ("last_lng", "REAL"), ("last_loc_at", "TEXT"),
                     ("max_travel", "INTEGER DEFAULT 0"),
                     # Legal gender is for governing bodies / insurance rosters (admins only). Identity is the member's own words.
                     ("legal_gender", "TEXT"), ("gender_identity", "TEXT"), ("gender_self", "TEXT"), ("ride_wnb", "INTEGER DEFAULT 0")):
        if col not in have:
            d.execute("ALTER TABLE members ADD COLUMN %s %s" % (col, ddl))


LEGAL_GENDERS = (("female", "Female"), ("male", "Male"), ("x", "X"))
GENDER_IDENTITIES = (("woman", "Woman"), ("man", "Man"), ("nonbinary", "Non-binary"), ("self", "Self-describe"), ("prefer_not", "Prefer not to say"))
TRAVEL_CHOICES = (0, 15, 30, 45, 60)


def clean_choice(value, choices):
    v = (value or "").strip().lower()
    return v if v in dict(choices) else None


def wnb_eligible(member):
    """Women & non-binary rides (04.19): open to members who identify as a woman, non-binary, or self-describe."""
    keys = member.keys() if hasattr(member, "keys") else []
    return ("gender_identity" in keys) and (member["gender_identity"] or "") in ("woman", "nonbinary", "self")


def wnb_on(member):
    keys = member.keys() if hasattr(member, "keys") else []
    return bool("ride_wnb" in keys and member["ride_wnb"]) and wnb_eligible(member)


def ride_visible(viewer, owner):
    """Either side's women & non-binary setting hides the pair unless the other side is eligible."""
    return (not wnb_on(owner) or wnb_eligible(viewer)) and (not wnb_on(viewer) or wnb_eligible(owner))


def round_loc(lat, lng):
    return round(float(lat), 3), round(float(lng), 3)


def last_location(member, now, max_age_h=12):
    """(lat, lng) if the member saved one recently enough to plan a drive from, else None."""
    keys = member.keys() if hasattr(member, "keys") else []
    if "last_lat" not in keys or member["last_lat"] is None or member["last_lng"] is None or not member["last_loc_at"]:
        return None
    if "save_location" in keys and not member["save_location"]:
        return None
    try:
        at = dt.datetime.fromisoformat(member["last_loc_at"])
    except ValueError:
        return None
    if max_age_h is not None and now - at > dt.timedelta(hours=max_age_h):
        return None
    return (member["last_lat"], member["last_lng"])


def _now():
    return dt.datetime.now().isoformat(timespec="seconds")


# ---------- age ----------
def parse_birth(raw):
    raw = (raw or "").strip()
    try:
        b = dt.date.fromisoformat(raw)
    except ValueError:
        return None
    if b.year < 1900 or b > dt.date.today():
        return None
    return b


def age_on(birth, today):
    return today.year - birth.year - ((today.month, today.day) < (birth.month, birth.day))


def is_adult(birth, today):
    return age_on(birth, today) >= ADULT_AGE


# ---------- waiver ----------
def waiver(d):
    return d.execute("SELECT * FROM club_waiver WHERE id=1").fetchone()


def save_waiver(d, enabled, title, body, url, bump, actor):
    w = waiver(d)
    version = (w["version"] or 1) + (1 if bump else 0)
    d.execute("UPDATE club_waiver SET enabled=?, title=?, body=?, url=?, version=?, updated_at=?, updated_by=? WHERE id=1",
              (1 if enabled else 0, (title or "Club liability waiver").strip()[:120], (body or "").strip()[:20000],
               (url or "").strip()[:500], version, _now(), actor))


def accepted_waiver(d, member_id):
    """The acceptance for the current version, or None. A disabled waiver counts as nothing to sign."""
    w = waiver(d)
    if not w or not w["enabled"]:
        return {"version": 0, "at": "", "typed_name": ""}
    return d.execute("SELECT * FROM waiver_acceptances WHERE member_id=? AND version=? ORDER BY id DESC LIMIT 1",
                     (member_id, w["version"])).fetchone()


def accept_waiver(d, member_id, typed_name, practice_id=None):
    w = waiver(d)
    d.execute("INSERT INTO waiver_acceptances(member_id, version, title, typed_name, practice_id, at) VALUES(?,?,?,?,?,?)",
              (member_id, w["version"], w["title"], typed_name.strip()[:120], practice_id, _now()))


def typed_name_ok(typed, member):
    """Full name typed: at least two words, and it has to include the last name on file when there is one."""
    t = " ".join((typed or "").split()).lower()
    if len(t.split(" ")) < 2:
        return False
    last = " ".join(((member["last"] or "") if member else "").split()).lower()
    return not last or last in t


# ---------- sign-up gate ----------
def gate_needs(d, member, today, trial_active):
    """What the one sheet must collect before Going. Empty list = one tap."""
    needs = []
    verified = (member["usawp_status"] or "") == "verified" and not (member["usawp_valid_until"] and member["usawp_valid_until"] < today)
    has_number = bool((member["usawp_number"] or "").strip())
    if not verified and not has_number and not trial_active:
        needs.append("number")
    if not accepted_waiver(d, member["id"]):
        needs.append("waiver")
    return needs


# ---------- rides ----------
def ride_window(practice, now):
    """Pickup window: 3 hours before start until 1 hour after the end, on the practice date."""
    try:
        start = dt.datetime.fromisoformat("%s %s" % (practice["date"], practice["start"] or "00:00"))
        end = dt.datetime.fromisoformat("%s %s" % (practice["date"], practice["end"] or practice["start"] or "23:59"))
    except ValueError:
        return False
    return start - dt.timedelta(hours=3) <= now <= end + dt.timedelta(hours=1)


def clean_area(raw):
    """An area is a neighborhood or city, never a street address."""
    a = " ".join((raw or "").split())[:60]
    if re.search(r"\d{2,}\s+\w+", a):
        return ""
    return a


def rides_for(d, practice_id, member_id):
    my_req = d.execute("SELECT r.*, m.first AS dfirst, m.preferred_first AS dpref, m.last AS dlast FROM ride_requests r "
                       "LEFT JOIN members m ON m.id=r.driver_id WHERE r.practice_id=? AND r.rider_id=? AND r.status!='cancelled' "
                       "ORDER BY r.id DESC LIMIT 1", (practice_id, member_id)).fetchone()
    my_offer = d.execute("SELECT * FROM ride_offers WHERE practice_id=? AND driver_id=? AND status='open'",
                         (practice_id, member_id)).fetchone()
    open_reqs = d.execute("SELECT r.*, m.first, m.preferred_first, m.last, m.gender_identity, m.ride_wnb FROM ride_requests r JOIN members m ON m.id=r.rider_id "
                          "WHERE r.practice_id=? AND r.status='open' AND r.rider_id!=? ORDER BY r.id", (practice_id, member_id)).fetchall()
    viewer = d.execute("SELECT * FROM members WHERE id=?", (member_id,)).fetchone()
    if viewer is not None:
        open_reqs = [r for r in open_reqs if ride_visible(viewer, r)]
    my_riders = d.execute("SELECT r.*, m.first, m.preferred_first, m.last FROM ride_requests r JOIN members m ON m.id=r.rider_id "
                          "WHERE r.practice_id=? AND r.driver_id=? AND r.status='matched' ORDER BY r.id", (practice_id, member_id)).fetchall()
    drivers = sum(1 for o in d.execute("SELECT m.gender_identity, m.ride_wnb FROM ride_offers o JOIN members m ON m.id=o.driver_id "
                                       "WHERE o.practice_id=? AND o.status='open' AND o.driver_id!=?", (practice_id, member_id)).fetchall()
                  if viewer is None or ride_visible(viewer, o))
    return {"mine": my_req, "offer": my_offer, "open": open_reqs, "riders": my_riders, "drivers": drivers}


def seats_left(d, offer):
    if not offer:
        return 0
    used = d.execute("SELECT COUNT(*) FROM ride_requests WHERE practice_id=? AND driver_id=? AND status='matched'",
                     (offer["practice_id"], offer["driver_id"])).fetchone()[0]
    return max(0, (offer["seats"] or 1) - used)


def ride_board(d, practice_id, viewer=None):
    """04.18 practice ride board: who's offering (area, seats left) and who's asking (area). Areas only, never addresses.
    With a viewer, rows hidden by either side's women & non-binary setting are left out."""
    who = "m.first, m.preferred_first, m.last, m.gender_identity, m.ride_wnb"
    offers = d.execute("SELECT o.*, %s FROM ride_offers o JOIN members m ON m.id=o.driver_id "
                       "WHERE o.practice_id=? AND o.status='open' ORDER BY o.id" % who, (practice_id,)).fetchall()
    asking = d.execute("SELECT r.*, %s FROM ride_requests r JOIN members m ON m.id=r.rider_id "
                       "WHERE r.practice_id=? AND r.status='open' ORDER BY r.id" % who, (practice_id,)).fetchall()
    if viewer is not None:
        offers = [o for o in offers if o["driver_id"] == viewer["id"] or ride_visible(viewer, o)]
        asking = [r for r in asking if r["rider_id"] == viewer["id"] or ride_visible(viewer, r)]
    rows = [dict(o, seats_left=seats_left(d, o)) for o in offers]
    return {"offers": rows, "asking": asking, "seats_open": sum(r["seats_left"] for r in rows),
            "need": len(asking), "cars": len(rows)}


def ride_defaults(member):
    keys = member.keys() if hasattr(member, "keys") else []
    return {"offer": bool(member["ride_offer"]) if "ride_offer" in keys else False,
            "area": (member["ride_area"] or "") if "ride_area" in keys else "",
            "seats": int(member["ride_seats"] or 2) if "ride_seats" in keys else 2,
            "wnb": bool(member["ride_wnb"]) if "ride_wnb" in keys else False, "wnb_ok": wnb_eligible(member)}


def auto_offer(d, practice_id, member):
    """Ride settings · Offer rides (04.19): tapping Going opens an offer from your saved area. Never overwrites one you changed."""
    rd = ride_defaults(member)
    if not (rd["offer"] and rd["area"]):
        return False
    cur = d.execute("""INSERT INTO ride_offers(practice_id, driver_id, area, seats, back, created) VALUES(?,?,?,?,1,?)
        ON CONFLICT(practice_id, driver_id) DO NOTHING""", (practice_id, member["id"], rd["area"], rd["seats"], _now()))
    return cur.rowcount == 1


def traffic_level(minutes, best):
    """Clear / Slow / Jammed for one forecast bar, against the best departure in the same window."""
    if not best or minutes <= best * 1.15:
        return "clear"
    return "slow" if minutes <= best * 1.4 else "jammed"


def leave_plan(start, buffer_min, forecast_fn, step=10, span=60):
    """04.10 Leave-by planner. `start` is the practice start (naive local). Departures run every `step` minutes from
    `span` before the arrive-by time to the arrive-by time; forecast_fn(departures) returns [Route]. Returns the latest
    departure that still arrives by start - buffer, the bars, and what leaving at the last slot costs."""
    arrive_by = start - dt.timedelta(minutes=int(buffer_min or 0))
    first = arrive_by - dt.timedelta(minutes=span)
    first = first.replace(minute=(first.minute // step) * step, second=0, microsecond=0)
    departures = []
    t = first
    while t <= arrive_by:
        departures.append(t); t += dt.timedelta(minutes=step)
    routes = forecast_fn(departures)
    best = min((r.minutes for r in routes), default=0)
    bars = [{"at": d, "minutes": r.minutes, "level": traffic_level(r.minutes, best), "estimated": r.estimated}
            for d, r in zip(departures, routes)]
    ok = [b for b in bars if b["at"] + dt.timedelta(minutes=b["minutes"]) <= arrive_by]
    pick = ok[-1] if ok else bars[0]
    # Exact leave-by inside the chosen slot: arrive_by minus that slot's drive time, never later than arriving on time.
    leave_by = min(arrive_by - dt.timedelta(minutes=pick["minutes"]), pick["at"] + dt.timedelta(minutes=step - 1))
    for b in bars:
        b["pick"] = b is pick
    last = bars[-1]
    return {"leave_by": leave_by, "arrive_by": arrive_by, "minutes": pick["minutes"], "bars": bars,
            "late_delta": max(0, last["minutes"] - pick["minutes"]), "late_at": last["at"],
            "estimated": any(b["estimated"] for b in bars)}


# ---------- availability (09.06–09.09, 09.16) ----------
def _hm(raw):
    try:
        h, m = str(raw or "").split(":")[:2]
        h, m = int(h), int(m)
        return h * 60 + m if 0 <= h <= 23 and 0 <= m <= 59 else None
    except (ValueError, TypeError):
        return None


def clean_window(weekday, start, end):
    """(weekday 0–6, 'HH:MM', 'HH:MM') or None. End after start, same day."""
    try:
        wd = int(weekday)
    except (TypeError, ValueError):
        return None
    a, b = _hm(start), _hm(end)
    if not (0 <= wd <= 6) or a is None or b is None or b <= a:
        return None
    return wd, "%02d:%02d" % divmod(a, 60), "%02d:%02d" % divmod(b, 60)


def windows(d, member_id):
    return d.execute("SELECT * FROM avail_windows WHERE member_id=? ORDER BY weekday, start", (member_id,)).fetchall()


def sync_days(d, member_id):
    """Keep members.avail_days (Finish setup, Your week) in step with the windows."""
    days = sorted({w["weekday"] for w in windows(d, member_id)})
    if days:
        d.execute("UPDATE members SET avail_days=? WHERE id=?", (",".join(DAYS[i] for i in days), member_id))


def away(d, member_id, today=None):
    q = "SELECT * FROM away_dates WHERE member_id=?" + (" AND end_date>=?" if today else "") + " ORDER BY start_date"
    return d.execute(q, (member_id, today) if today else (member_id,)).fetchall()


def is_away(aways, day):
    return any(a["start_date"] <= day <= a["end_date"] for a in aways)


def fits(practice, wins):
    """A session fits when one window on its weekday covers its whole start–end."""
    try:
        day = dt.date.fromisoformat(str(practice["date"])[:10])
    except ValueError:
        return False
    a, b = _hm(practice["start"] or "19:00"), _hm(practice["end"] or practice["start"] or "20:30")
    if a is None or b is None:
        return False
    return any(w["weekday"] == day.weekday() and _hm(w["start"]) <= a and b <= _hm(w["end"]) for w in wins)


def week_fit(d, member_id, practices, travel=None, max_travel=0):
    """09.07: which of this week's sessions fit your windows, away dates and max travel. Conflicts carry the fix to offer.
    travel(p) returns estimated drive minutes from the member's saved location, or None when unknown."""
    wins = windows(d, member_id); aways = away(d, member_id)
    rows, fit = [], 0
    for p in practices:
        day = str(p["date"])[:10]
        if p["cancelled"]:
            continue
        gone = is_away(aways, day)
        mins = travel(p) if travel else None
        far = bool(max_travel and mins is not None and mins > max_travel)
        ok = (not gone) and (not far) and fits(p, wins)
        fit += 1 if ok else 0
        rows.append({"p": p, "fits": ok, "away": gone, "far": far, "minutes": mins})
    return {"rows": rows, "fit": fit, "total": len(rows), "conflicts": [r for r in rows if not r["fits"]]}


def grid_blocks(items, first=6 * 60, last=23 * 60):
    """Week-grid geometry (top/height in %) for windows or sessions: [{'col':0-6,'top':..,'h':..}]."""
    span = last - first
    out = []
    for wd, a, b, extra in items:
        a, b = max(first, a), min(last, b)
        if b <= a:
            continue
        out.append(dict(extra, col=wd, top=round((a - first) / span * 100, 2), h=round((b - a) / span * 100, 2)))
    return out


def clock_range(start, end):
    def f(v, keep_ampm):
        m = _hm(v); h, mi = divmod(m, 60)
        s = "%d%s" % ((h - 1) % 12 + 1, (":%02d" % mi) if mi else "")
        return s + ((" AM" if h < 12 else " PM") if keep_ampm else "")
    same = (_hm(start) < 720) == (_hm(end) < 720)
    return "%s – %s" % (f(start, not same), f(end, True))


# ---------- Lineup volunteer shifts (07.15–07.17) ----------
def pref(d, key, default=""):
    row = d.execute("SELECT value FROM club_prefs WHERE key=?", (key,)).fetchone()
    return row["value"] if row and row["value"] is not None else default


def set_pref(d, key, value):
    d.execute("INSERT INTO club_prefs(key, value) VALUES(?,?) ON CONFLICT(key) DO UPDATE SET value=excluded.value", (key, str(value)))


def shift_hours(shift):
    a, b = _hm(shift["start"]), _hm(shift["end"])
    return round(max(0, (b or 0) - (a or 0)) / 60, 1)


def shifts_for(d, event_id, member_id):
    rows = d.execute("""SELECT s.*, (SELECT COUNT(*) FROM shift_signups x WHERE x.shift_id=s.id) AS taken,
        EXISTS(SELECT 1 FROM shift_signups x WHERE x.shift_id=s.id AND x.member_id=?) AS mine
        FROM lineup_shifts s WHERE s.event_id=? ORDER BY s.start""", (member_id, event_id)).fetchall()
    out = []
    for r in rows:
        x = dict(r); x["open"] = max(0, (r["capacity"] or 0) - (r["taken"] or 0)); x["hours"] = shift_hours(r)
        x["pct"] = int(round(100 * (r["taken"] or 0) / max(1, r["capacity"] or 1)))
        out.append(x)
    return out


def sign_up_shift(d, shift_id, member_id):
    """One shift per event per member; never over capacity. Returns '' or the reason it can't."""
    s = d.execute("SELECT * FROM lineup_shifts WHERE id=?", (shift_id,)).fetchone()
    if not s:
        return "That shift is gone."
    taken = d.execute("SELECT COUNT(*) FROM shift_signups WHERE shift_id=?", (shift_id,)).fetchone()[0]
    if d.execute("SELECT 1 FROM shift_signups WHERE shift_id=? AND member_id=?", (shift_id, member_id)).fetchone():
        return ""
    if taken >= (s["capacity"] or 0):
        return "That shift is full."
    d.execute("DELETE FROM shift_signups WHERE member_id=? AND shift_id IN (SELECT id FROM lineup_shifts WHERE event_id=?)", (member_id, s["event_id"]))
    d.execute("INSERT INTO shift_signups(shift_id, member_id, at) VALUES(?,?,?)", (shift_id, member_id, _now()))
    return ""


def service_hours(d, member_id, today):
    """Hours from shifts on events that have happened, newest first. Season = since Sep 1."""
    season = dt.date(today.year if today.month >= 9 else today.year - 1, 9, 1).isoformat()
    rows = d.execute("""SELECT s.*, e.title AS etitle, e.date AS edate, COALESCE(e.venue, e.city, '') AS where_
        FROM shift_signups x JOIN lineup_shifts s ON s.id=x.shift_id JOIN lineup_events e ON e.id=s.event_id
        WHERE x.member_id=? AND e.date>=? ORDER BY e.date DESC""", (member_id, season)).fetchall()
    done = [dict(r, hours=shift_hours(r)) for r in rows if (r["edate"] or "") < today.isoformat()]
    ahead = [dict(r, hours=shift_hours(r)) for r in rows if (r["edate"] or "") >= today.isoformat()]
    return {"done": done, "hours": round(sum(r["hours"] for r in done), 1), "ahead": round(sum(r["hours"] for r in ahead), 1)}


# ---------- usual week + finish setup ----------
def parse_days(values):
    return ",".join(x for x in DAYS if x in set(values or []))


def setup_steps(member, notif_on):
    days = (member["avail_days"] or "") if "avail_days" in member.keys() else ""
    steps = [("Teams", True, "/practices"), ("Account", True, "/profile"),
             ("Your week", bool(days), "/setup/week"),
             ("Notifications", bool(notif_on), "/notifications")]
    return steps


# ---------- wrap-up ----------
def wrap(d, pid):
    return d.execute("SELECT * FROM practice_wraps WHERE practice_id=?", (pid,)).fetchone()


def wrap_counts(d, pid):
    going = {r[0] for r in d.execute("SELECT member_id FROM rsvps WHERE practice_id=? AND going=1", (pid,))}
    checked = {r[0] for r in d.execute("SELECT member_id FROM checkins WHERE practice_id=?", (pid,))}
    return {"attended": len(checked), "no_show": len(going - checked), "walk_in": len(checked - going)}


# ---------- templates (rendered inside ui.BASE, so the shared macros and classes apply) ----------
PRACTICE_PANEL = """
{% if fx and not p.cancelled %}
{% if fx.gate_hint %}{{ rg_callout(fx.gate_hint, 'First time only', 'Once', '/practices/' ~ p.id ~ '/signup', 'graphite') }}{% endif %}
{% if fx.going %}
<div class=fxrides>
{% set rd = fx.rides %}
{% if rd.mine and rd.mine.status == 'matched' %}
<div class="fxcard tone-aqua"><span class=fxk>RIDE CONFIRMED</span><b>{{ rd.mine.dpref or rd.mine.dfirst }} is driving.</b>
<small>Pickup area · {{ rd.mine.area }}{% if rd.mine.back %} · ride back too{% endif %}</small>
{% if fx.in_window and rd.mine.pickup_note %}<p class=fxspot>Pickup spot: {{ rd.mine.pickup_note }}</p>{% elif rd.mine.pickup_note %}<p class=fxspot>Pickup spot shows 3 hours before practice.</p>{% endif %}
<div class=fxrow><a class="rg-btn secondary" href="/chat?c=dm:{{ [me().id, rd.mine.driver_id]|min }}:{{ [me().id, rd.mine.driver_id]|max }}&place=me">Message {{ rd.mine.dpref or rd.mine.dfirst }}</a>
<form method=post action="/practices/{{ p.id }}/rides">{{ csrf_field() }}<button class="rg-btn ghost" name=action value=cancel>Cancel ride</button></form></div></div>
{% elif rd.mine %}
<div class=fxcard><span class=fxk>RIDE REQUESTED</span><b>Asking drivers near {{ rd.mine.area }}.</b>
<small>{{ rd.drivers }} driver{{ '' if rd.drivers == 1 else 's' }} offering for this practice · we'll notify you when one picks you up</small>
<form method=post action="/practices/{{ p.id }}/rides">{{ csrf_field() }}<button class="rg-btn ghost" name=action value=cancel>Cancel request</button></form></div>
{% elif not rd.offer %}
{{ rg_callout('Need a ride?', ((rd.drivers ~ ' teammate' ~ ('' if rd.drivers == 1 else 's') ~ ' driving') if rd.drivers else 'Ask teammates who are going'), 'Ask →', '', 'aqua', "document.getElementById('fxAsk').showModal()") }}
{% endif %}
{% if rd.offer %}
<div class=fxcard><span class=fxk>YOU'RE DRIVING · {{ fx.seats_left }} SEAT{{ '' if fx.seats_left == 1 else 'S' }} LEFT</span><b>From {{ rd.offer.area }}.</b>
{% for r in rd.riders %}<form method=post action="/practices/{{ p.id }}/rides" class=fxrider>{{ csrf_field() }}<input type=hidden name=req_id value="{{ r.id }}"><span class=grow><b>{{ r.preferred_first or r.first }} {{ r.last[:1] }}.</b><small>{{ r.area }}{% if r.back %} · back too{% endif %}</small></span><input name=pickup_note value="{{ r.pickup_note or '' }}" placeholder="Pickup spot (only they see it)" maxlength=120><button class="rg-btn secondary" name=action value=spot>Save</button></form>{% endfor %}
{% for r in rd.open %}<form method=post action="/practices/{{ p.id }}/rides" class=fxrider>{{ csrf_field() }}<input type=hidden name=req_id value="{{ r.id }}"><span class=grow><b>{{ r.preferred_first or r.first }} {{ r.last[:1] }}.</b><small>Needs a ride · {{ r.area }}{% if r.back %} · back too{% endif %}</small></span>{% if fx.seats_left %}<button class="rg-btn primary" name=action value=pick>Pick up</button>{% endif %}</form>{% endfor %}
<form method=post action="/practices/{{ p.id }}/rides">{{ csrf_field() }}<button class="rg-btn ghost" name=action value=unoffer>Stop offering</button></form></div>
{% elif not rd.mine %}
{{ rg_callout('Driving?', ((rd.open|length ~ ' teammate' ~ ('' if rd.open|length == 1 else 's') ~ ' need a ride') if rd.open else 'Offer seats to teammates who are going'), 'Offer →', '', 'graphite', "document.getElementById('fxOffer').showModal()") }}
{% endif %}
</div>
<dialog id=fxAsk class=botsheet><form method=post action="/practices/{{ p.id }}/rides" class=sheet>{{ csrf_field() }}<div class=grab aria-hidden=true></div>
<h2>Ask for a ride.</h2>
<label class=rg-field><span>PICKUP AREA</span><input name=area required maxlength=60 placeholder="Neighborhood or city, e.g. Belmont Shore" value="{{ fx.last_area }}"></label>
<p class='ty-muted ty-sm'>Drivers see this area, never your address. You can share an exact spot with your driver after they pick you up.</p>
<label class=checkline><input type=checkbox name=back value=1 checked> Ride back too · practice ends {{ fmt_clock(p.end) if p.end else '' }}</label>
<button class="rg-btn primary full" name=action value=ask>Ask {% if rd.drivers %}{{ rd.drivers }} driver{{ '' if rd.drivers == 1 else 's' }}{% else %}teammates{% endif %}</button>
</form></dialog>
<dialog id=fxOffer class=botsheet><form method=post action="/practices/{{ p.id }}/rides" class=sheet>{{ csrf_field() }}<div class=grab aria-hidden=true></div>
<h2>Offer a ride.</h2>
<label class=rg-field><span>LEAVING FROM (AREA)</span><input name=area required maxlength=60 placeholder="Neighborhood or city" value="{{ fx.last_area }}"></label>
<label class=rg-field><span>SEATS</span><select name=seats>{% for n in range(1,7) %}<option{% if n == fx.seats_default %} selected{% endif %}>{{ n }}</option>{% endfor %}</select></label>
<label class=checkline><input type=checkbox name=back value=1 checked> I can drive people back</label>
<button class="rg-btn primary full" name=action value=offer>Offer seats</button>
<p class='ty-muted ty-sm'>Riders only see your area. Your exact location is never shared.</p>
</form></dialog>
{% endif %}
{% if fx.going %}<a class=rg-calink href="/practices/{{ p.id }}/rides">Ride board →</a>{% endif %}
{% if fx.can_wrap %}{{ rg_callout('Wrap up' if not fx.closed else 'Wrap-up · closed', 'Attendance, private note, recap', 'Open →', '/practices/' ~ p.id ~ '/wrap', 'tangerine' if not fx.closed else 'graphite') }}{% endif %}
{% endif %}
"""

RIDE_BOARD = """<div class="rg-page rg-rides">
<h1 class=ty-display-l>Rides.</h1>
<div class=rg-metrics>{{ rg_metric('%02d'|format(board.seats_open), 'Seats open', 'lime') }}{{ rg_metric('%02d'|format(board.need), 'Need a ride', 'sun') }}{{ rg_metric('%02d'|format(board.cars), 'Cars', 'carbon') }}</div>
{% if rd.mine and rd.mine.status == 'matched' %}{{ rg_callout(((rd.mine.dpref or rd.mine.dfirst) ~ ' is driving you'), 'Pickup area · ' ~ rd.mine.area, 'Practice →', '/practices/' ~ p.id, 'aqua') }}
<div class=rg-sharetrip><button type=button class="rg-btn secondary" data-share-text="{{ 'Riding with %s to %s, %s at %s. Pickup area: %s. Shared from Regulars.'|format(rd.mine.dpref or rd.mine.dfirst, practice_title(p), when, p.location or 'the pool', rd.mine.area) }}">Share trip</button><small class=ty-muted data-share-note hidden></small></div>
{% elif rd.mine %}{{ rg_callout('You asked for a ride', "From " ~ rd.mine.area ~ " · we'll tell you when a driver picks you up", 'Practice →', '/practices/' ~ p.id, 'graphite') }}{% endif %}
{% if rd.riders %}{% set ns = namespace(names=[]) %}{% for r in rd.riders %}{% set ns.names = ns.names + [r.preferred_first or r.first] %}{% endfor %}<div class=rg-sharetrip><button type=button class="rg-btn secondary" data-share-text="{{ 'Driving %s to %s, %s at %s. Shared from Regulars.'|format(ns.names|join(', '), practice_title(p), when, p.location or 'the pool') }}">Share trip</button><small class=ty-muted data-share-note hidden></small></div>{% endif %}
{{ rg_label('Offering') }}
{% for o in board.offers %}{{ rg_ride_row((o.preferred_first or o.first) ~ ' ' ~ (o.last or '')[:1] ~ '.', 'From ' ~ o.area ~ (' · back too' if o.back else ''), ((o.preferred_first or o.first)[:1] ~ (o.last or '')[:1])|upper, 'sky', '<span class=rg-seats><b>' ~ o.seats_left ~ '</b><small>seat' ~ ('' if o.seats_left == 1 else 's') ~ '</small></span>') }}
{% else %}<p class=ty-muted>No one is offering yet.</p>{% endfor %}
{{ rg_label('Asking') }}
{% for r in board.asking %}{% set btn = rg_ride_pick(p.id, r.id, csrf_field()) if (rd.offer and seats_left and r.rider_id != me().id) else '' %}
{{ rg_ride_row((r.preferred_first or r.first) ~ ' ' ~ (r.last or '')[:1] ~ '.', r.area ~ (' · back too' if r.back else ''), ((r.preferred_first or r.first)[:1] ~ (r.last or '')[:1])|upper, 'sun', btn) }}
{% else %}<p class=ty-muted>No one needs a ride.</p>{% endfor %}
{% if going %}
<div class=rg-ridebtns>
{% if not rd.offer %}<button type=button class="rg-btn primary" data-open-dialog=rbOffer>Offer seats</button>{% else %}<form method=post action="/practices/{{ p.id }}/rides">{{ csrf_field() }}<input type=hidden name=next value=board><button class="rg-btn secondary" name=action value=unoffer>Stop offering</button></form>{% endif %}
{% if not rd.mine %}<button type=button class="rg-btn secondary" data-open-dialog=rbAsk>Need a ride</button>{% else %}<form method=post action="/practices/{{ p.id }}/rides">{{ csrf_field() }}<input type=hidden name=next value=board><button class="rg-btn secondary" name=action value=cancel>Cancel my request</button></form>{% endif %}
</div>
<a class=rg-calink href=/rides/settings>Ride settings</a>
<dialog id=rbAsk class="botsheet modal"><form method=post action="/practices/{{ p.id }}/rides" class=sheet>{{ csrf_field() }}<input type=hidden name=next value=board><div class=grab aria-hidden=true></div>
<h2>Ask for a ride.</h2>
<label class=rg-field><span>PICKUP AREA</span><input name=area required maxlength=60 placeholder="Neighborhood or city" value="{{ last_area }}"></label>
<p class=ty-muted>Drivers see this area, never your address.</p>
<label class=checkline><input type=checkbox name=back value=1 checked> Ride back too</label>
<button class="rg-btn primary" name=action value=ask>Ask {{ board.cars }} driver{{ '' if board.cars == 1 else 's' }}</button>
</form></dialog>
<dialog id=rbOffer class="botsheet modal"><form method=post action="/practices/{{ p.id }}/rides" class=sheet>{{ csrf_field() }}<input type=hidden name=next value=board><div class=grab aria-hidden=true></div>
<h2>Offer a ride.</h2>
<label class=rg-field><span>LEAVING FROM (AREA)</span><input name=area required maxlength=60 placeholder="Neighborhood or city" value="{{ last_area }}"></label>
<label class=rg-field><span>SEATS</span><select name=seats>{% for n in range(1,7) %}<option{% if n == defaults.seats %} selected{% endif %}>{{ n }}</option>{% endfor %}</select></label>
<label class=checkline><input type=checkbox name=back value=1 checked> I can drive people back</label>
<button class="rg-btn primary" name=action value=offer>Offer seats</button>
</form></dialog>
{% else %}{{ rg_callout('Tap Going to ride together', 'Rides are for teammates going to this practice', 'Practice →', '/practices/' ~ p.id, 'graphite') }}{% endif %}
</div>"""

LEAVE_BY = """<div class="rg-page rg-rides rg-leaveby" data-practice="{{ p.id }}">
<div class="rg-lbhero" id=lbHero><span class=ty-caps>Leave by</span><b class=ty-display-xl id=lbTime>–:––</b>
<small id=lbSub>Arrive {{ arrive_label }} · {{ buffer }} min deck buffer</small></div>
<p class=ty-muted id=lbStatus role=status>Finding your location to plan the drive. We keep your last spot (to about 100 m) so we can tell you if leave-by moves. Only you see it; turn it off in <a href=/privacy>Privacy</a>.</p>
<section id=lbForecast hidden>
<h2 class=ty-title>Traffic forecast</h2><p class=ty-muted>Drive time if you leave at…</p>
<figure class=rg-bars id=lbBars role=img aria-label="Drive minutes by departure time"></figure>
<div class=rg-chartlegend><span><i class=clear></i>Clear</span><span><i class=slow></i>Slow</span><span><i class=jammed></i>Jammed</span></div>
<details class=rg-tableview><summary>Show as a table</summary><table id=lbTable><thead><tr><th>Leave at</th><th>Minutes</th><th>Traffic</th></tr></thead><tbody></tbody></table></details>
<div class="rg-latecard" id=lbLate hidden><b id=lbLateN></b><span id=lbLateText></span></div>
</section>
{{ rg_label('Getting there') }}
<div class=rg-modes role=tablist><button type=button class=on data-mode=drive>Drive</button><a href="/practices/{{ p.id }}/rides">Carpool</a><button type=button data-mode=bike>Bike</button></div>
<p class=ty-muted id=lbBike hidden></p>
<form method=post action=/leave-by/settings class=fxsheet>{{ csrf_field() }}<input type=hidden name=next value="/practices/{{ p.id }}/leave-by">
<label class=rg-toggle><span><b>Arrive {{ buffer or 5 }} min early for the deck</b><small>Leave-by counts back from {{ arrive_label }}</small></span><input type=checkbox name=buffer value=1 {% if buffer %}checked{% endif %} onchange="this.form.requestSubmit()"><i aria-hidden=true></i></label>
</form>
<a class="rg-btn secondary" href="https://www.google.com/maps/dir/?api=1&amp;destination={{ dest|urlencode }}" target=_blank rel=noopener>Open in Maps</a>
<script>
(function(){
 var pid={{ p.id }}, st=document.getElementById('lbStatus');
 function fail(t){ st.textContent=t; }
 if(!navigator.geolocation){ fail('Location is off, so we can\u2019t plan the drive. Open the venue in Maps.'); return; }
 navigator.geolocation.getCurrentPosition(function(pos){
  fetch('/api/leave-by',{method:'POST',headers:{'Content-Type':'application/json','X-CSRF':window.PUSH_CSRF||''},
   body:JSON.stringify({id:pid,lat:pos.coords.latitude,lng:pos.coords.longitude})}).then(function(r){return r.json()}).then(function(j){
   if(!j.ok){ fail(j.error==='window'?'The planner opens on the day of practice.':'Couldn\u2019t plan this drive. Open the venue in Maps.'); return; }
   document.getElementById('lbTime').textContent=j.leave_by;
   document.getElementById('lbSub').textContent='Arrive '+j.arrive_by+' · '+j.buffer+' min deck buffer · '+j.miles+' mi';
   st.textContent=j.estimated?'Estimated without live traffic.':'Predicted traffic for each departure.';
   var bars=document.getElementById('lbBars'), tb=document.querySelector('#lbTable tbody'), max=Math.max.apply(null,j.bars.map(function(b){return b.minutes}));
   bars.innerHTML=''; tb.innerHTML='';
   j.bars.forEach(function(b){
    var c=document.createElement('div'); c.className='rg-bar '+b.level+(b.pick?' pick':''); c.tabIndex=0;
    c.title='Leave '+b.at+' · '+b.minutes+' min · '+b.level; c.setAttribute('aria-label',c.title);
    c.innerHTML='<span class=v>'+b.minutes+'</span><i style="height:'+Math.max(8,Math.round(b.minutes/max*100))+'%"></i><span class=t>'+b.at+'</span>';
    bars.appendChild(c);
    var tr=document.createElement('tr'); tr.innerHTML='<td>'+b.at+'</td><td>'+b.minutes+'</td><td>'+b.level+'</td>'; tb.appendChild(tr);
   });
   document.getElementById('lbForecast').hidden=false;
   if(j.late_delta>0){ var l=document.getElementById('lbLate'); l.hidden=false; document.getElementById('lbLateN').textContent='+'+j.late_delta;
    document.getElementById('lbLateText').textContent='min if you leave at '+j.late_at+'.'; }
   var bk=document.getElementById('lbBike'); if(j.bike_minutes){ bk.textContent='About '+j.bike_minutes+' min by bike'+(j.bike_estimated?' (estimate)':'')+'.'; }
   document.querySelector('[data-mode=bike]').onclick=function(){ bk.hidden=!bk.hidden; this.classList.toggle('on',!bk.hidden); };
  }).catch(function(){ fail('Couldn\u2019t plan this drive. Open the venue in Maps.'); });
 }, function(){ fail('Location is off, so we can\u2019t plan the drive. Open the venue in Maps.'); }, {timeout:8000, maximumAge:300000});
})();
</script>
</div>"""

AVAIL_WEEK = """<div class="rg-screen rg-avail">
{{ seg }}
<h2 class=ty-title>When can you play?</h2>
<p class=ty-muted>Your regular week. Teams you're on can see "available" without the details.</p>
{{ rg_week_grid(blocks, 'Your available windows') }}
{{ rg_label('Windows') }}
<div class=rg-srows>
{% for w in wins %}<button type=button class=rg-srow data-day-sheet data-id="{{ w.id }}" data-weekday="{{ w.weekday }}" data-start="{{ w.start }}" data-end="{{ w.end }}"><span class=rg-srlabel>{{ DAYS[w.weekday] }}</span><span class=rg-srvalue>{{ clock_range(w.start, w.end) }}</span>{{ rg_icon('chevron_right', 'sm') }}</button>
{% else %}<p class=ty-muted>No windows yet. Add the times you can usually play.</p>{% endfor %}
<button type=button class=rg-srow data-day-sheet data-id="" data-weekday="1" data-start="18:00" data-end="21:00"><span class=rg-srlabel>Add a window</span>{{ rg_icon('plus', 'sm') }}</button>
<button type=button class=rg-srow data-open-dialog=awaySheet><span class=rg-srlabel>Away dates</span><span class=rg-srvalue>{{ away_n or 'None' }}</span>{{ rg_icon('chevron_right', 'sm') }}</button>
</div>
{{ rg_button('How your teams fit', 'primary', '/availability/fit') }}
<dialog id=daySheet class="botsheet modal" data-sheet-name=day><form method=post action=/availability class=sheet>{{ csrf_field() }}<div class=grab aria-hidden=true></div>
<input type=hidden name=id id=dayId><input type=hidden name=next value="/calendar?when=availability">
<h2 id=dayTitle>Edit a day.</h2>
<label class=rg-field><span>DAY</span><select name=weekday id=dayWeekday>{% for x in DAYS %}<option value="{{ loop.index0 }}">{{ x }}</option>{% endfor %}</select></label>
<div class=rg-wingrid><label class=rg-field><span>FROM</span><input type=time name=start id=dayStart required></label><label class=rg-field><span>TO</span><input type=time name=end id=dayEnd required></label></div>
<button class="rg-btn primary" name=action value=save id=daySave>Save</button>
<button class="rg-btn secondary" name=action value=delete formnovalidate id=dayDelete>Remove this window</button>
</form></dialog>
<dialog id=awaySheet class="botsheet modal" data-sheet-name=away><div class=sheet><div class=grab aria-hidden=true></div>
<h2>Away dates.</h2>
<p class=ty-muted>Sessions on these days count as conflicts, and Auto-RSVP skips them.</p>
{% for a in aways %}<form method=post action=/availability/away class=rg-awayrow>{{ csrf_field() }}<input type=hidden name=id value="{{ a.id }}"><span><b>{{ fmt_d(a.start_date) }}{% if a.end_date != a.start_date %} – {{ fmt_d(a.end_date) }}{% endif %}</b>{% if a.note %}<small>{{ a.note }}</small>{% endif %}</span><button class="rg-btn secondary" name=action value=delete>Remove</button></form>
{% endfor %}
<form method=post action=/availability/away class=fxsheet>{{ csrf_field() }}
<div class=rg-wingrid><label class=rg-field><span>FROM</span><input type=date name=start_date required></label><label class=rg-field><span>TO</span><input type=date name=end_date></label></div>
<label class=rg-field><span>NOTE (OPTIONAL)</span><input name=note maxlength=60 placeholder="Trip, work, family"></label>
<button class="rg-btn primary" name=action value=add>Add away dates</button></form>
</div></dialog>
<script>
(function(){
 if(window.grunionsDaySheet) return; window.grunionsDaySheet=1;
 document.addEventListener('click',function(e){
  var b=e.target.closest&&e.target.closest('[data-day-sheet]'); if(!b) return;
  var d=document.getElementById('daySheet'); if(!d) return;
  var id=b.getAttribute('data-id');
  document.getElementById('dayId').value=id;
  document.getElementById('dayWeekday').value=b.getAttribute('data-weekday');
  document.getElementById('dayStart').value=b.getAttribute('data-start');
  document.getElementById('dayEnd').value=b.getAttribute('data-end');
  document.getElementById('dayTitle').textContent=id?'Edit a day.':'Add a window.';
  document.getElementById('daySave').value=id?'save':'add';
  document.getElementById('dayDelete').hidden=!id;
  if(window.grunionsOpenSheet) grunionsOpenSheet(d); else d.showModal();
 });
})();
</script>
</div>"""

AVAIL_FIT = """<div class="rg-page rg-rides rg-avail rg-avail-fit">
<h1 class=ty-display-l>How your teams fit.</h1>
<div class=rg-fithero><b class=ty-display-ml>{{ fit.fit }}/{{ fit.total }}</b><span><b>Sessions fit</b><small>this week{% if org %} · {{ org }}{% endif %}</small></span></div>
{{ rg_week_grid(blocks, "Your windows and this week's sessions") }}
<div class=rg-chartlegend><span><i class=free></i>You're free</span><span><i class=session></i>Session</span><span><i class=conflict></i>Conflict</span></div>
{% for r in fit.conflicts %}<section class="rg-calloutcard tone-tangerine"><span class=ty-caps>{{ 'Away' if r.away else ('Too far' if r.far else 'Conflict') }}</span>
<b>{{ weekday_name(r.p.date) }} {{ fmt_clock(r.p.start) }} · {{ practice_title(r.p) }} — {{ "you're away that day" if r.away else (("about %d min away, past your %d min limit"|format(r.minutes, max_travel)) if r.far else "outside your windows") }}.</b>
<div class=rg-fitacts><form method=post action=/practices>{{ csrf_field() }}<input type=hidden name=pid value="{{ r.p.id }}"><input type=hidden name=back value=/availability/fit><button class="rg-btn ink" name=action value=notgoing>Mark Not going</button></form>
{% if not r.away and not r.far %}<form method=post action=/availability>{{ csrf_field() }}<input type=hidden name=weekday value="{{ r.wd }}"><input type=hidden name=start value="{{ r.p.start }}"><input type=hidden name=end value="{{ r.p.end or r.p.start }}"><input type=hidden name=next value=/availability/fit><button class="rg-btn ink" name=action value=add>Add {{ DAYS[r.wd] }} {{ fmt_clock(r.p.start) }}</button></form>{% endif %}</div></section>
{% endfor %}
{% if not fit.total %}<p class=ty-muted>No sessions on the team schedule this week.</p>{% endif %}
<form method=post action=/availability/travel class=fxsheet>{{ csrf_field() }}
<label class=rg-field><span>MAX TRAVEL</span><select name=max_travel onchange="this.form.requestSubmit()">{% for n in travel_choices %}<option value="{{ n }}"{% if n == max_travel %} selected{% endif %}>{{ 'No limit' if not n else ('%d min drive'|format(n)) }}</option>{% endfor %}</select></label>
<p class=ty-muted>{% if has_loc %}From your last saved location, estimated without traffic.{% else %}Needs your location: open a practice's Leave-by once, or turn on saving in <a href=/privacy>Privacy</a>.{% endif %}</p>
<noscript><button class="rg-btn secondary">Save</button></noscript></form>
<form method=post action=/availability/auto>{{ csrf_field() }}
<label class=rg-toggle><span><b>Auto-RSVP</b><small>The night before a session that fits, we'll ask you to confirm Going.</small></span><input type=checkbox name=auto_rsvp value=1 {% if me().auto_rsvp %}checked{% endif %} onchange="this.form.requestSubmit()"><i aria-hidden=true></i></label>
<noscript><button class="rg-btn secondary">Save</button></noscript></form>
</div>"""

AVAIL_AWAY = """<div class="rg-page rg-rides rg-avail">
<h1 class=ty-display-l>Away dates.</h1>
<p class=ty-muted>Sessions on these days count as conflicts, and Auto-RSVP skips them.</p>
{% for a in aways %}<form method=post class=rg-awayrow>{{ csrf_field() }}<input type=hidden name=id value="{{ a.id }}"><span><b>{{ fmt_d(a.start_date) }}{% if a.end_date != a.start_date %} – {{ fmt_d(a.end_date) }}{% endif %}</b>{% if a.note %}<small>{{ a.note }}</small>{% endif %}</span><button class="rg-btn secondary" name=action value=delete>Remove</button></form>
{% else %}<p class=ty-muted>No away dates.</p>{% endfor %}
<form method=post class=fxsheet>{{ csrf_field() }}
<div class=rg-wingrid><label class=rg-field><span>FROM</span><input type=date name=start_date required></label><label class=rg-field><span>TO</span><input type=date name=end_date></label></div>
<label class=rg-field><span>NOTE (OPTIONAL)</span><input name=note maxlength=60 placeholder="Trip, work, family"></label>
<button class="rg-btn primary" name=action value=add>Add away dates</button></form>
</div>"""

SHIFTS = """<div class="rg-page rg-rides rg-shifts">
<section class="rg-shifthero tone-bubblegum"><div class=rg-fitacts><span class=rg-pillk>Volunteer</span>{% if goal %}<span class=rg-pillk>Counts as service hours</span>{% endif %}</div>
<b class=ty-heading>{{ e.title }}</b><div class=rg-shiftdate><b class=ty-hero>{{ day }}</b><small>{{ dow }} · {{ mon }}<br>{{ where }}</small></div></section>
<h2 class=ty-title>Pick a shift</h2>
{% for s in shifts %}<form method=post class="rg-shift{% if s.mine %} mine{% elif not s.open %} full{% endif %}">{{ csrf_field() }}<input type=hidden name=shift value="{{ s.id }}">
<div class=rg-shifttop><span class=rg-shifttime><b class=ty-display-s>{{ s.nums }}</b><small>{{ s.ampm }}</small></span><span class=rg-chipk>{% if s.mine %}You're on it{% elif s.open %}{{ s.open }} open{% else %}Full{% endif %}</span></div>
<span class=ty-body-strong>{{ s.title }}</span>
<div class=rg-progress role=progressbar aria-valuemin=0 aria-valuemax="{{ s.capacity }}" aria-valuenow="{{ s.taken }}"><i style="width:{{ s.pct }}%"></i></div><small class=rg-shiftn>{{ s.taken }}/{{ s.capacity }}</small>
{% if s.mine %}<button class="rg-btn secondary" name=action value=leave>Leave this shift</button>{% elif s.open %}<button class="rg-btn primary" name=action value=signup aria-label="Sign up for {{ s.range }} {{ s.title }}">Sign up</button>{% endif %}
</form>{% else %}<p class=ty-muted>No shifts posted yet.</p>{% endfor %}
{% if e.description %}{{ rg_info('WHAT TO BRING', e.description) }}{% endif %}
{% if can_edit %}<details class=rg-window><summary><b class=ty-label-l>Manage shifts</b></summary>
<form method=post class=rg-winform>{{ csrf_field() }}<label class=rg-field><span>WHAT</span><input name=title required maxlength=60 placeholder="Setup · tents + sign-in"></label>
<div class=rg-wingrid><label class=rg-field><span>FROM</span><input type=time name=start required value="08:00"></label><label class=rg-field><span>TO</span><input type=time name=end required value="10:00"></label></div>
<label class=rg-field><span>PEOPLE</span><input type=number name=capacity min=1 max=200 value=4 required></label>
<button class="rg-btn primary" name=action value=add>Add shift</button></form>
{% for s in shifts %}<form method=post class=rg-awayrow>{{ csrf_field() }}<input type=hidden name=shift value="{{ s.id }}"><span><b>{{ s.range }} · {{ s.title }}</b><small>{{ s.taken }}/{{ s.capacity }} signed up</small></span><button class="rg-btn secondary" name=action value=delete>Remove</button></form>{% endfor %}
<form method=post class=rg-winform>{{ csrf_field() }}<label class=rg-field><span>SERVICE HOURS GOAL PER SEASON (0 = OFF)</span><input type=number name=goal min=0 max=200 value="{{ goal }}"></label><button class="rg-btn secondary" name=action value=goal>Save goal</button></form>
</details>{% endif %}
</div>"""

SHIFT_DONE = """<div class="rg-page rg-rides rg-shifts">
<section class=rg-lbhero><span class=ty-caps>{{ e.title }} · {{ when }}</span><b class="ty-display-80 rg-donetime">{{ s.nums }}<small>{{ s.ampm }}</small></b><small>You're on {{ s.title|lower }}.</small></section>
<div class=rg-ridebtns><a class="rg-btn secondary" href="/lineup/{{ e.id }}/shifts/{{ s.id }}.ics">Add to calendar</a><button type=button class="rg-btn secondary" data-share="{{ share_url }}" onclick="var u=this.dataset.share;if(navigator.share){navigator.share({title:'{{ e.title|e }}',url:u}).catch(function(){})}else if(navigator.clipboard){navigator.clipboard.writeText(u);this.textContent='Link copied'}">Invite a friend</button></div>
{% if goal %}<h2 class=ty-title>Your service hours</h2>
<section class=rg-hours><div><b class=ty-display-88>{{ '%02d'|format(hours.hours|int) }}</b><span><b>of {{ goal }} hrs</b><small>{% if hours.ahead %}+{{ hours.ahead|round(1)|string|replace('.0','') }} after {{ e.title }}{% endif %}</small></span></div>
<div class=rg-progress><i style="width:{{ [100, (hours.hours / goal * 100)|int]|min }}%"></i></div>
<small class=ty-muted>{{ org }} asks members for {{ goal }} service hours a season.{% if hours.hours + hours.ahead >= goal %} You're there.{% endif %}</small></section>
{% for r in hours.done %}{{ rg_row(r.etitle, fmt_d(r.edate) ~ ((' · ' ~ r.where_) if r.where_ else ''), '', '', '', ((r.hours|string)[:-2] if (r.hours|string).endswith('.0') else (r.hours|string)) ~ 'h') }}{% endfor %}{% endif %}
</div>"""

RIDE_SETTINGS = """<div class="rg-page rg-rides">
<p class=ty-caps>Me · Rides</p>
<h1 class=ty-display-l>Ride settings.</h1>
<form method=post class=fxsheet>{{ csrf_field() }}
<label class="rg-toggle"><span><b>Offer rides</b><small>When you tap Going, teammates going to the same session can ask you</small></span><input type=checkbox name=ride_offer value=1 {% if rs.offer %}checked{% endif %}><i aria-hidden=true></i></label>
<label class=rg-field><span>I DRIVE FROM (AREA)</span><input name=ride_area maxlength=60 value="{{ rs.area }}" placeholder="Neighborhood or city, e.g. Fountain Valley"></label>
<label class=rg-field><span>SEATS IN MY CAR</span><select name=ride_seats>{% for n in range(1,7) %}<option{% if n == rs.seats %} selected{% endif %}>{{ n }}</option>{% endfor %}</select></label>
{% if rs.wnb_ok %}<label class="rg-toggle"><span><b>Women &amp; non-binary only</b><small>Your offers and asks are only seen by, and matched with, teammates who identify as a woman or non-binary</small></span><input type=checkbox name=ride_wnb value=1 {% if rs.wnb %}checked{% endif %}><i aria-hidden=true></i></label>
{% else %}<p class=ty-muted>Women &amp; non-binary rides: add your gender in <a href="/profile?edit=identity">Edit profile</a> to turn this on.</p>{% endif %}
<div class="rg-toggle locked"><span><b>Show my area, not my address</b><small>Always on. An exact pickup spot goes only to a matched rider, 3 hours before practice.</small></span><i aria-hidden=true class=on></i></div>
<button class="rg-btn primary">Save</button>
</form>
</div>"""

SIGNUP = """<div class="rg-page rg-task">
{{ rg_chip("First time with " ~ org, "neutral") }}
<h1>{% if needs|length > 1 %}Two things, then you're in.{% else %}One thing, then you're in.{% endif %}</h1>
<p class='ty-muted ty-sm'>{{ when }} · {{ p.location or '' }}</p>
<form method=post class=fxsheet>{{ csrf_field() }}
{% set n = namespace(i=0) %}
{% if 'number' in needs %}{% set n.i = n.i + 1 %}
<label class=rg-field><span>{{ n.i }} · USA WATER POLO MEMBER #</span><input name=usawp_number inputmode=numeric pattern="[0-9]{4,10}" maxlength=10 placeholder="1002004" autocomplete=off></label>
<p class='ty-muted ty-sm'>A coach or admin checks it by hand. You can still go while it's pending.</p>
{% endif %}
{% if 'waiver' in needs %}{% set n.i = n.i + 1 %}
<div class=fxwaiver>
<b>{{ n.i }} · I'm 18+ and agree to the {{ w.title }}</b>
<small>Version {{ w.version }}{% if w.url %} · <a href="{{ w.url }}" target=_blank rel=noopener>Read it →</a>{% endif %}</small>
{% if w.body %}<details><summary>Read it here</summary><div class=fxwaivertext>{{ w.body }}</div></details>{% endif %}
<label class=checkline><input type=checkbox name=agree value=1 required> I've read it and I agree</label>
<label class=rg-field><span>TYPE YOUR FULL NAME</span><input name=typed_name required maxlength=120 autocomplete=name placeholder="{{ me().first }} {{ me().last }}"></label>
</div>
{% endif %}
<button class="rg-btn primary full" name=action value=go>I'm going</button>
{% if 'number' in needs and trial_offer %}<button class="rg-btn ghost full" name=action value=trial formnovalidate>No number yet? Start a free trial instead →</button>{% endif %}
</form></div>"""

WAIVER_ADMIN = """{{ admin_page('Club waiver', 'Members accept it once, in the same sheet as their insurance number. Raise the version to make everyone sign again.') }}
<form method=post class=fxsheet>{{ csrf_field() }}
<label class=checkline><input type=checkbox name=enabled value=1 {% if w.enabled %}checked{% endif %}> Require the waiver before Going</label>
<label class=rg-field><span>TITLE</span><input name=title value="{{ w.title or '' }}" maxlength=120></label>
<label class=rg-field><span>LINK TO THE WAIVER (URL OR PDF)</span><input name=url value="{{ w.url or '' }}" placeholder="https://"></label>
<label class=rg-field><span>OR PASTE THE TEXT</span><textarea name=body rows=10>{{ w.body or '' }}</textarea></label>
<p class='ty-muted ty-sm'>Current version {{ w.version }} · {{ signed }} signed this version{% if w.updated_at %} · updated {{ w.updated_at[:10] }}{% if w.updated_by %} by {{ w.updated_by }}{% endif %}{% endif %}</p>
<label class=checkline><input type=checkbox name=bump value=1> This is a new version. Everyone signs again.</label>
<button class="rg-btn primary full">Save</button>
</form>"""

WRAP = """<div class=rg-page>
<a class=rg-tbdisc href="/practices/{{ p.id }}" aria-label="Close">{{ rg_icon('close') }}</a>
<h1>Wrap up.</h1>
<p class='ty-muted ty-sm'>{{ when }} · {{ p.location or '' }}{% if wr and wr.closed_at %} · closed {{ wr.closed_at[:16].replace('T', ' ') }}{% endif %}</p>
<div class=rg-metrics>{{ rg_metric('%02d'|format(c.attended), 'Attended', 'lime') }}{{ rg_metric('%02d'|format(c.no_show), 'No-show') }}{{ rg_metric('%02d'|format(c.walk_in), 'Walk-in') }}</div>
<form method=post class=fxsheet>{{ csrf_field() }}
<label class=rg-field><span>NOTE FOR ADMINS (PRIVATE)</span><textarea name=admin_note rows=3 maxlength=2000 placeholder="Lane 3 light out. Ana needs her USAWP renewed.">{{ wr.admin_note if wr else '' }}</textarea></label>
<label class=rg-field><span>RECAP TO PRACTICE CHAT (OPTIONAL)</span><input name=recap maxlength=280 placeholder="One line for everyone who came"></label>
<button class="rg-btn secondary full" name=action value=save>Save note</button>
<button class="rg-btn primary full" name=action value=close>{% if wr and wr.closed_at %}Save and keep closed{% else %}Close practice{% endif %}</button>
</form>
<p class='ty-muted ty-sm'><a href="/admin?date={{ p.date }}">Back to check-in</a></p>
</div>"""

WEEK = """<div class=rg-page>
{{ rg_chip("Optional", "neutral") }}
<h1>When can you usually play?</h1>
<form method=post class=fxsheet>{{ csrf_field() }}
<div class=fxdays>{% for d in days %}<label><input type=checkbox name=day value="{{ d }}" {% if d in picked %}checked{% endif %}><span>{{ d[:1] }}</span></label>{% endfor %}</div>
<p class='ty-muted ty-sm'>{{ fit }}</p>
<button class="rg-btn primary full" name=action value=save>Save my week</button>
<a class="rg-btn ghost full" href="{{ back }}">Later</a>
</form></div>"""

SETUP_CARD = """{% if setup and setup.show %}{{ rg_checklist('Finish setup', setup.steps) }}{% endif %}"""

CSS = """
.fxcard.fxgate{display:flex;align-items:center;gap:12px;text-decoration:none;color:inherit;margin:12px 0}
.fxgate .grow,.fxask .grow{display:grid;gap:2px}
.fxgate small,.fxcard small{color:var(--color-text-secondary)}
.fxdark{background:var(--color-forest);color:var(--color-chalk)}
.fxrides{display:grid;gap:12px;margin:12px 0}
.fxcard{display:grid;gap:6px;padding:16px;border-radius:var(--radius-card);background:var(--color-surface-2);color:var(--color-text);border:0;text-align:left;font:inherit}
.fxcard[class*=tone-]{background:var(--tone);color:var(--fixed-ink)}
.fxcard[class*=tone-] small{color:inherit;opacity:.8}
.fxcard.fxask{display:flex;align-items:center;gap:12px;cursor:pointer}
.fxcard .r2-chip{flex:none}
.fxcard .r2-chip.fxdark{background:var(--color-forest);color:var(--color-chalk);border:0}
.fxask .grow{display:grid;gap:2px}
.fxk{font-size:11px;letter-spacing:.08em;font-weight:700;opacity:.8}
.fxspot{margin:0;font-weight:600}
.fxrow{display:flex;gap:8px;flex-wrap:wrap}
.fxrider{display:flex;gap:8px;align-items:center;flex-wrap:wrap;padding:8px 0;border-top:1px solid var(--color-border)}
.fxrider .grow{display:grid;min-width:120px}
.fxrider input{flex:1 1 160px}
.fxwrap,.fxoffer{margin-top:8px}
.fxpage{display:grid;gap:12px;padding:8px 16px 120px;max-width:560px;margin:0 auto}
.fxpage h1{margin:0}
.fxback{color:var(--color-text-secondary);text-decoration:none}
.fxsheet{display:grid;gap:12px}
.fxfield{display:grid;gap:6px}
.fxfield span{font-size:11px;letter-spacing:.08em;font-weight:700;color:var(--color-text-secondary)}
.fxwaiver{display:grid;gap:8px;padding:16px;border-radius:var(--radius-card);background:var(--color-surface-2)}
.fxwaivertext{white-space:pre-wrap;max-height:240px;overflow:auto;font-size:14px;color:var(--color-text-secondary)}
.fxdays{display:grid;grid-template-columns:repeat(7,1fr);gap:6px}
.fxdays label{position:relative}
.fxdays input{position:absolute;opacity:0}
.fxdays span{display:grid;place-items:center;height:49px;border-radius:var(--radius-control);background:var(--color-surface-2);font-weight:700}
.fxdays input:checked+span{background:var(--color-selected);color:var(--color-on-selected)}
.fxsetup{display:grid;gap:8px;padding:16px 18px;border-radius:var(--radius-card);background:var(--color-surface-2);margin:0 0 12px}
.fxsetuphead{display:flex;align-items:center;justify-content:space-between}
.fxstep{display:flex;gap:10px;align-items:center}
.fxstep a{color:inherit}
.fxstep small{margin-left:auto;color:var(--color-text-secondary)}
.fxstep.ok{color:var(--color-text-secondary)}
.fxtick{width:18px;color:var(--color-cyan)}
.holdchip{color:var(--color-status-not-cleared)}
"""
