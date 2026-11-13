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
    have = _cols(d, "members")
    for col, ddl in (("birth_date", "TEXT"), ("avail_days", "TEXT"), ("setup_dismissed", "INTEGER DEFAULT 0"),
                     ("ride_offer", "INTEGER DEFAULT 0"), ("ride_area", "TEXT"), ("ride_seats", "INTEGER DEFAULT 2"),
                     ("leave_buffer", "INTEGER DEFAULT 5")):
        if col not in have:
            d.execute("ALTER TABLE members ADD COLUMN %s %s" % (col, ddl))


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
    open_reqs = d.execute("SELECT r.*, m.first, m.preferred_first, m.last FROM ride_requests r JOIN members m ON m.id=r.rider_id "
                          "WHERE r.practice_id=? AND r.status='open' AND r.rider_id!=? ORDER BY r.id", (practice_id, member_id)).fetchall()
    my_riders = d.execute("SELECT r.*, m.first, m.preferred_first, m.last FROM ride_requests r JOIN members m ON m.id=r.rider_id "
                          "WHERE r.practice_id=? AND r.driver_id=? AND r.status='matched' ORDER BY r.id", (practice_id, member_id)).fetchall()
    drivers = d.execute("SELECT COUNT(*) FROM ride_offers WHERE practice_id=? AND status='open' AND driver_id!=?",
                        (practice_id, member_id)).fetchone()[0]
    return {"mine": my_req, "offer": my_offer, "open": open_reqs, "riders": my_riders, "drivers": drivers}


def seats_left(d, offer):
    if not offer:
        return 0
    used = d.execute("SELECT COUNT(*) FROM ride_requests WHERE practice_id=? AND driver_id=? AND status='matched'",
                     (offer["practice_id"], offer["driver_id"])).fetchone()[0]
    return max(0, (offer["seats"] or 1) - used)


def ride_board(d, practice_id):
    """04.18 practice ride board: who's offering (area, seats left) and who's asking (area). Areas only, never addresses."""
    offers = d.execute("SELECT o.*, m.first, m.preferred_first, m.last FROM ride_offers o JOIN members m ON m.id=o.driver_id "
                       "WHERE o.practice_id=? AND o.status='open' ORDER BY o.id", (practice_id,)).fetchall()
    asking = d.execute("SELECT r.*, m.first, m.preferred_first, m.last FROM ride_requests r JOIN members m ON m.id=r.rider_id "
                       "WHERE r.practice_id=? AND r.status='open' ORDER BY r.id", (practice_id,)).fetchall()
    rows = [dict(o, seats_left=seats_left(d, o)) for o in offers]
    return {"offers": rows, "asking": asking, "seats_open": sum(r["seats_left"] for r in rows),
            "need": len(asking), "cars": len(rows)}


def ride_defaults(member):
    keys = member.keys() if hasattr(member, "keys") else []
    return {"offer": bool(member["ride_offer"]) if "ride_offer" in keys else False,
            "area": (member["ride_area"] or "") if "ride_area" in keys else "",
            "seats": int(member["ride_seats"] or 2) if "ride_seats" in keys else 2}


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
<div class=fxrow><a class="btn btn-secondary" href="/chat?c=dm:{{ [me().id, rd.mine.driver_id]|min }}:{{ [me().id, rd.mine.driver_id]|max }}&place=me">Message {{ rd.mine.dpref or rd.mine.dfirst }}</a>
<form method=post action="/practices/{{ p.id }}/rides">{{ csrf_field() }}<button class="btn quiet" name=action value=cancel>Cancel ride</button></form></div></div>
{% elif rd.mine %}
<div class=fxcard><span class=fxk>RIDE REQUESTED</span><b>Asking drivers near {{ rd.mine.area }}.</b>
<small>{{ rd.drivers }} driver{{ '' if rd.drivers == 1 else 's' }} offering for this practice · we'll notify you when one picks you up</small>
<form method=post action="/practices/{{ p.id }}/rides">{{ csrf_field() }}<button class="btn quiet" name=action value=cancel>Cancel request</button></form></div>
{% elif not rd.offer %}
{{ rg_callout('Need a ride?', ((rd.drivers ~ ' teammate' ~ ('' if rd.drivers == 1 else 's') ~ ' driving') if rd.drivers else 'Ask teammates who are going'), 'Ask →', '', 'aqua', "document.getElementById('fxAsk').showModal()") }}
{% endif %}
{% if rd.offer %}
<div class=fxcard><span class=fxk>YOU'RE DRIVING · {{ fx.seats_left }} SEAT{{ '' if fx.seats_left == 1 else 'S' }} LEFT</span><b>From {{ rd.offer.area }}.</b>
{% for r in rd.riders %}<form method=post action="/practices/{{ p.id }}/rides" class=fxrider>{{ csrf_field() }}<input type=hidden name=req_id value="{{ r.id }}"><span class=grow><b>{{ r.preferred_first or r.first }} {{ r.last[:1] }}.</b><small>{{ r.area }}{% if r.back %} · back too{% endif %}</small></span><input name=pickup_note value="{{ r.pickup_note or '' }}" placeholder="Pickup spot (only they see it)" maxlength=120><button class="btn btn-secondary" name=action value=spot>Save</button></form>{% endfor %}
{% for r in rd.open %}<form method=post action="/practices/{{ p.id }}/rides" class=fxrider>{{ csrf_field() }}<input type=hidden name=req_id value="{{ r.id }}"><span class=grow><b>{{ r.preferred_first or r.first }} {{ r.last[:1] }}.</b><small>Needs a ride · {{ r.area }}{% if r.back %} · back too{% endif %}</small></span>{% if fx.seats_left %}<button class="btn btn-primary" name=action value=pick>Pick up</button>{% endif %}</form>{% endfor %}
<form method=post action="/practices/{{ p.id }}/rides">{{ csrf_field() }}<button class="btn quiet" name=action value=unoffer>Stop offering</button></form></div>
{% elif not rd.mine %}
{{ rg_callout('Driving?', ((rd.open|length ~ ' teammate' ~ ('' if rd.open|length == 1 else 's') ~ ' need a ride') if rd.open else 'Offer seats to teammates who are going'), 'Offer →', '', 'graphite', "document.getElementById('fxOffer').showModal()") }}
{% endif %}
</div>
<dialog id=fxAsk class=botsheet><form method=post action="/practices/{{ p.id }}/rides" class=sheet>{{ csrf_field() }}<div class=grab aria-hidden=true></div>
<h2>Ask for a ride.</h2>
<label class=rg-field><span>PICKUP AREA</span><input name=area required maxlength=60 placeholder="Neighborhood or city, e.g. Belmont Shore" value="{{ fx.last_area }}"></label>
<p class=t3>Drivers see this area, never your address. You can share an exact spot with your driver after they pick you up.</p>
<label class=checkline><input type=checkbox name=back value=1 checked> Ride back too · practice ends {{ fmt_clock(p.end) if p.end else '' }}</label>
<button class="btn btn-primary full" name=action value=ask>Ask {% if rd.drivers %}{{ rd.drivers }} driver{{ '' if rd.drivers == 1 else 's' }}{% else %}teammates{% endif %}</button>
</form></dialog>
<dialog id=fxOffer class=botsheet><form method=post action="/practices/{{ p.id }}/rides" class=sheet>{{ csrf_field() }}<div class=grab aria-hidden=true></div>
<h2>Offer a ride.</h2>
<label class=rg-field><span>LEAVING FROM (AREA)</span><input name=area required maxlength=60 placeholder="Neighborhood or city" value="{{ fx.last_area }}"></label>
<label class=rg-field><span>SEATS</span><select name=seats>{% for n in range(1,7) %}<option{% if n == fx.seats_default %} selected{% endif %}>{{ n }}</option>{% endfor %}</select></label>
<label class=checkline><input type=checkbox name=back value=1 checked> I can drive people back</label>
<button class="btn btn-primary full" name=action value=offer>Offer seats</button>
<p class=t3>Riders only see your area. Your exact location is never shared.</p>
</form></dialog>
{% endif %}
{% if fx.going %}<a class=rg-calink href="/practices/{{ p.id }}/rides">Ride board →</a>{% endif %}
{% if fx.can_wrap %}{{ rg_callout('Wrap up' if not fx.closed else 'Wrap-up · closed', 'Attendance, private note, recap', 'Open →', '/practices/' ~ p.id ~ '/wrap', 'tangerine' if not fx.closed else 'graphite') }}{% endif %}
{% endif %}
"""

RIDE_BOARD = """<div class="rg-page rg-rides">
<a class=rg-backlink href="/practices/{{ p.id }}">← Practice · {{ when }}</a>
<h1 class=ty-display-l>Rides.</h1>
<div class=rg-metrics>{{ rg_metric('%02d'|format(board.seats_open), 'Seats open', 'lime') }}{{ rg_metric('%02d'|format(board.need), 'Need a ride', 'sun') }}{{ rg_metric('%02d'|format(board.cars), 'Cars', 'carbon') }}</div>
{% if rd.mine and rd.mine.status == 'matched' %}{{ rg_callout(((rd.mine.dpref or rd.mine.dfirst) ~ ' is driving you'), 'Pickup area · ' ~ rd.mine.area, 'Practice →', '/practices/' ~ p.id, 'aqua') }}
{% elif rd.mine %}{{ rg_callout('You asked for a ride', "From " ~ rd.mine.area ~ " · we'll tell you when a driver picks you up", 'Practice →', '/practices/' ~ p.id, 'graphite') }}{% endif %}
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
<a class=rg-backlink href="/practices/{{ p.id }}">← Practice · {{ when }}</a>
<div class="rg-lbhero" id=lbHero><span class=ty-caps>Leave by</span><b class=ty-display-xl id=lbTime>–:––</b>
<small id=lbSub>Arrive {{ arrive_label }} · {{ buffer }} min deck buffer</small></div>
<p class=ty-muted id=lbStatus role=status>Finding your location to plan the drive. It stays on your phone; it isn't saved.</p>
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

RIDE_SETTINGS = """<div class="rg-page rg-rides">
<a class=rg-backlink href=/profile>← Profile</a>
<p class=ty-caps>Me · Rides</p>
<h1 class=ty-display-l>Ride settings.</h1>
<form method=post class=fxsheet>{{ csrf_field() }}
<label class="rg-toggle"><span><b>Offer rides</b><small>When you tap Going, teammates going to the same session can ask you</small></span><input type=checkbox name=ride_offer value=1 {% if rs.offer %}checked{% endif %}><i aria-hidden=true></i></label>
<label class=rg-field><span>I DRIVE FROM (AREA)</span><input name=ride_area maxlength=60 value="{{ rs.area }}" placeholder="Neighborhood or city, e.g. Fountain Valley"></label>
<label class=rg-field><span>SEATS IN MY CAR</span><select name=ride_seats>{% for n in range(1,7) %}<option{% if n == rs.seats %} selected{% endif %}>{{ n }}</option>{% endfor %}</select></label>
<div class="rg-toggle locked"><span><b>Show my area, not my address</b><small>Always on. An exact pickup spot goes only to a matched rider, 3 hours before practice.</small></span><i aria-hidden=true class=on></i></div>
<button class="rg-btn primary">Save</button>
</form>
</div>"""

SIGNUP = """<div class=rg-page>
<a class=rg-back href="/practices/{{ p.id }}">← Practice</a>
{{ rg_chip("First time with " ~ org, "neutral") }}
<h1>{% if needs|length > 1 %}Two things, then you're in.{% else %}One thing, then you're in.{% endif %}</h1>
<p class=t3>{{ when }} · {{ p.location or '' }}</p>
<form method=post class=fxsheet>{{ csrf_field() }}
{% set n = namespace(i=0) %}
{% if 'number' in needs %}{% set n.i = n.i + 1 %}
<label class=rg-field><span>{{ n.i }} · USA WATER POLO MEMBER #</span><input name=usawp_number inputmode=numeric pattern="[0-9]{4,10}" maxlength=10 placeholder="1002004" autocomplete=off></label>
<p class=t3>A coach or admin checks it by hand. You can still go while it's pending.</p>
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
<button class="btn btn-primary full" name=action value=go>I'm going</button>
{% if 'number' in needs and trial_offer %}<button class="btn quiet full" name=action value=trial formnovalidate>No number yet? Start a free trial instead →</button>{% endif %}
</form></div>"""

WAIVER_ADMIN = """{{ admin_page('Club waiver', 'Members accept it once, in the same sheet as their insurance number. Raise the version to make everyone sign again.') }}
<form method=post class=fxsheet>{{ csrf_field() }}
<label class=checkline><input type=checkbox name=enabled value=1 {% if w.enabled %}checked{% endif %}> Require the waiver before Going</label>
<label class=rg-field><span>TITLE</span><input name=title value="{{ w.title or '' }}" maxlength=120></label>
<label class=rg-field><span>LINK TO THE WAIVER (URL OR PDF)</span><input name=url value="{{ w.url or '' }}" placeholder="https://"></label>
<label class=rg-field><span>OR PASTE THE TEXT</span><textarea name=body rows=10>{{ w.body or '' }}</textarea></label>
<p class=t3>Current version {{ w.version }} · {{ signed }} signed this version{% if w.updated_at %} · updated {{ w.updated_at[:10] }}{% if w.updated_by %} by {{ w.updated_by }}{% endif %}{% endif %}</p>
<label class=checkline><input type=checkbox name=bump value=1> This is a new version. Everyone signs again.</label>
<button class="btn btn-primary full">Save</button>
</form>"""

WRAP = """<div class=rg-page>
<a class=rg-back href="/practices/{{ p.id }}">← Practice</a>
<h1>Wrap up.</h1>
<p class=t3>{{ when }} · {{ p.location or '' }}{% if wr and wr.closed_at %} · closed {{ wr.closed_at[:16].replace('T', ' ') }}{% endif %}</p>
<div class=rg-metrics>{{ rg_metric('%02d'|format(c.attended), 'Attended', 'lime') }}{{ rg_metric('%02d'|format(c.no_show), 'No-show') }}{{ rg_metric('%02d'|format(c.walk_in), 'Walk-in') }}</div>
<form method=post class=fxsheet>{{ csrf_field() }}
<label class=rg-field><span>NOTE FOR ADMINS (PRIVATE)</span><textarea name=admin_note rows=3 maxlength=2000 placeholder="Lane 3 light out. Ana needs her USAWP renewed.">{{ wr.admin_note if wr else '' }}</textarea></label>
<label class=rg-field><span>RECAP TO PRACTICE CHAT (OPTIONAL)</span><input name=recap maxlength=280 placeholder="One line for everyone who came"></label>
<button class="btn btn-secondary full" name=action value=save>Save note</button>
<button class="btn btn-primary full" name=action value=close>{% if wr and wr.closed_at %}Save and keep closed{% else %}Close practice{% endif %}</button>
</form>
<p class=t3><a href="/admin?date={{ p.date }}">Back to check-in</a></p>
</div>"""

WEEK = """<div class=rg-page>
{{ rg_chip("Optional", "neutral") }}
<h1>When can you usually play?</h1>
<form method=post class=fxsheet>{{ csrf_field() }}
<div class=fxdays>{% for d in days %}<label><input type=checkbox name=day value="{{ d }}" {% if d in picked %}checked{% endif %}><span>{{ d[:1] }}</span></label>{% endfor %}</div>
<p class=t3>{{ fit }}</p>
<button class="btn btn-primary full" name=action value=save>Save my week</button>
<a class="btn quiet full" href="{{ back }}">Later</a>
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
