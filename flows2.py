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
    for col, ddl in (("birth_date", "TEXT"), ("avail_days", "TEXT"), ("setup_dismissed", "INTEGER DEFAULT 0")):
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


# ---------- usual week + finish setup ----------
def parse_days(values):
    return ",".join(x for x in DAYS if x in set(values or []))


def setup_steps(member, notif_on):
    days = (member["avail_days"] or "") if "avail_days" in member.keys() else ""
    steps = [("Teams", True, ""), ("Account", True, ""),
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
{% if fx.gate_hint %}<a class="fxcard fxgate" href="/practices/{{ p.id }}/signup"><span class=grow><b>{{ fx.gate_hint }}</b><small>First time only</small></span><span class=r2-chip>Once</span></a>{% endif %}
{% if fx.going %}
<div class=fxrides>
{% set rd = fx.rides %}
{% if rd.mine and rd.mine.status == 'matched' %}
<div class="fxcard cyan"><span class=fxk>RIDE CONFIRMED</span><b>{{ rd.mine.dpref or rd.mine.dfirst }} is driving.</b>
<small>Pickup area · {{ rd.mine.area }}{% if rd.mine.back %} · ride back too{% endif %}</small>
{% if fx.in_window and rd.mine.pickup_note %}<p class=fxspot>Pickup spot: {{ rd.mine.pickup_note }}</p>{% elif rd.mine.pickup_note %}<p class=fxspot>Pickup spot shows 3 hours before practice.</p>{% endif %}
<div class=fxrow><a class="btn btn-secondary" href="/chat?c=dm:{{ [me().id, rd.mine.driver_id]|min }}:{{ [me().id, rd.mine.driver_id]|max }}&place=me">Message {{ rd.mine.dpref or rd.mine.dfirst }}</a>
<form method=post action="/practices/{{ p.id }}/rides">{{ csrf_field() }}<button class="btn quiet" name=action value=cancel>Cancel ride</button></form></div></div>
{% elif rd.mine %}
<div class=fxcard><span class=fxk>RIDE REQUESTED</span><b>Asking drivers near {{ rd.mine.area }}.</b>
<small>{{ rd.drivers }} driver{{ '' if rd.drivers == 1 else 's' }} offering for this practice · we'll notify you when one picks you up</small>
<form method=post action="/practices/{{ p.id }}/rides">{{ csrf_field() }}<button class="btn quiet" name=action value=cancel>Cancel request</button></form></div>
{% elif not rd.offer %}
<button type=button class="fxcard cyan fxask" onclick="document.getElementById('fxAsk').showModal()"><span class=grow><b>Need a ride?</b><small>{% if rd.drivers %}{{ rd.drivers }} teammate{{ '' if rd.drivers == 1 else 's' }} driving{% else %}Ask teammates who are going{% endif %}</small></span><span class="r2-chip fxdark">Ask →</span></button>
{% endif %}
{% if rd.offer %}
<div class=fxcard><span class=fxk>YOU'RE DRIVING · {{ fx.seats_left }} SEAT{{ '' if fx.seats_left == 1 else 'S' }} LEFT</span><b>From {{ rd.offer.area }}.</b>
{% for r in rd.riders %}<form method=post action="/practices/{{ p.id }}/rides" class=fxrider>{{ csrf_field() }}<input type=hidden name=req_id value="{{ r.id }}"><span class=grow><b>{{ r.preferred_first or r.first }} {{ r.last[:1] }}.</b><small>{{ r.area }}{% if r.back %} · back too{% endif %}</small></span><input name=pickup_note value="{{ r.pickup_note or '' }}" placeholder="Pickup spot (only they see it)" maxlength=120><button class="btn btn-secondary" name=action value=spot>Save</button></form>{% endfor %}
{% for r in rd.open %}<form method=post action="/practices/{{ p.id }}/rides" class=fxrider>{{ csrf_field() }}<input type=hidden name=req_id value="{{ r.id }}"><span class=grow><b>{{ r.preferred_first or r.first }} {{ r.last[:1] }}.</b><small>Needs a ride · {{ r.area }}{% if r.back %} · back too{% endif %}</small></span>{% if fx.seats_left %}<button class="btn btn-primary" name=action value=pick>Pick up</button>{% endif %}</form>{% endfor %}
<form method=post action="/practices/{{ p.id }}/rides">{{ csrf_field() }}<button class="btn quiet" name=action value=unoffer>Stop offering</button></form></div>
{% elif not rd.mine %}
<button type=button class="btn btn-secondary full fxoffer" onclick="document.getElementById('fxOffer').showModal()">Offer a ride{% if rd.open %} · {{ rd.open|length }} asking{% endif %}</button>
{% endif %}
</div>
<dialog id=fxAsk class=botsheet><form method=post action="/practices/{{ p.id }}/rides" class=sheet>{{ csrf_field() }}<div class=grab aria-hidden=true></div>
<h2>Ask for a ride.</h2>
<label class=fxfield><span>PICKUP AREA</span><input name=area required maxlength=60 placeholder="Neighborhood or city, e.g. Belmont Shore" value="{{ fx.last_area }}"></label>
<p class=t3>Drivers see this area, never your address. You can share an exact spot with your driver after they pick you up.</p>
<label class=checkline><input type=checkbox name=back value=1 checked> Ride back too · practice ends {{ fmt_clock(p.end) if p.end else '' }}</label>
<button class="btn btn-primary full" name=action value=ask>Ask {% if rd.drivers %}{{ rd.drivers }} driver{{ '' if rd.drivers == 1 else 's' }}{% else %}teammates{% endif %}</button>
</form></dialog>
<dialog id=fxOffer class=botsheet><form method=post action="/practices/{{ p.id }}/rides" class=sheet>{{ csrf_field() }}<div class=grab aria-hidden=true></div>
<h2>Offer a ride.</h2>
<label class=fxfield><span>LEAVING FROM (AREA)</span><input name=area required maxlength=60 placeholder="Neighborhood or city" value="{{ fx.last_area }}"></label>
<label class=fxfield><span>SEATS</span><select name=seats>{% for n in range(1,7) %}<option{% if n == 2 %} selected{% endif %}>{{ n }}</option>{% endfor %}</select></label>
<label class=checkline><input type=checkbox name=back value=1 checked> I can drive people back</label>
<button class="btn btn-primary full" name=action value=offer>Offer seats</button>
<p class=t3>Riders only see your area. Your exact location is never shared.</p>
</form></dialog>
{% endif %}
{% if fx.can_wrap %}<a class="btn btn-secondary full fxwrap" href="/practices/{{ p.id }}/wrap">{% if fx.closed %}Wrap-up · closed{% else %}Wrap up practice{% endif %}</a>{% endif %}
{% endif %}
"""

SIGNUP = """<div class=fxpage>
<a class=fxback href="/practices/{{ p.id }}">← Practice</a>
<span class=r2-chip>FIRST TIME WITH {{ org|upper }}</span>
<h1>{% if needs|length > 1 %}Two things, then you're in.{% else %}One thing, then you're in.{% endif %}</h1>
<p class=t3>{{ when }} · {{ p.location or '' }}</p>
<form method=post class=fxsheet>{{ csrf_field() }}
{% set n = namespace(i=0) %}
{% if 'number' in needs %}{% set n.i = n.i + 1 %}
<label class=fxfield><span>{{ n.i }} · USA WATER POLO MEMBER #</span><input name=usawp_number inputmode=numeric pattern="[0-9]{4,10}" maxlength=10 placeholder="1002004" autocomplete=off></label>
<p class=t3>A coach or admin checks it by hand. You can still go while it's pending.</p>
{% endif %}
{% if 'waiver' in needs %}{% set n.i = n.i + 1 %}
<div class=fxwaiver>
<b>{{ n.i }} · I'm 18+ and agree to the {{ w.title }}</b>
<small>Version {{ w.version }}{% if w.url %} · <a href="{{ w.url }}" target=_blank rel=noopener>Read it →</a>{% endif %}</small>
{% if w.body %}<details><summary>Read it here</summary><div class=fxwaivertext>{{ w.body }}</div></details>{% endif %}
<label class=checkline><input type=checkbox name=agree value=1 required> I've read it and I agree</label>
<label class=fxfield><span>TYPE YOUR FULL NAME</span><input name=typed_name required maxlength=120 autocomplete=name placeholder="{{ me().first }} {{ me().last }}"></label>
</div>
{% endif %}
<button class="btn btn-primary full" name=action value=go>I'm going</button>
{% if 'number' in needs and trial_offer %}<button class="btn quiet full" name=action value=trial formnovalidate>No number yet? Start a free trial instead →</button>{% endif %}
</form></div>"""

WAIVER_ADMIN = """{{ admin_page('Club waiver', 'Members accept it once, in the same sheet as their insurance number. Raise the version to make everyone sign again.') }}
<form method=post class=fxsheet>{{ csrf_field() }}
<label class=checkline><input type=checkbox name=enabled value=1 {% if w.enabled %}checked{% endif %}> Require the waiver before Going</label>
<label class=fxfield><span>TITLE</span><input name=title value="{{ w.title or '' }}" maxlength=120></label>
<label class=fxfield><span>LINK TO THE WAIVER (URL OR PDF)</span><input name=url value="{{ w.url or '' }}" placeholder="https://"></label>
<label class=fxfield><span>OR PASTE THE TEXT</span><textarea name=body rows=10>{{ w.body or '' }}</textarea></label>
<p class=t3>Current version {{ w.version }} · {{ signed }} signed this version{% if w.updated_at %} · updated {{ w.updated_at[:10] }}{% if w.updated_by %} by {{ w.updated_by }}{% endif %}{% endif %}</p>
<label class=checkline><input type=checkbox name=bump value=1> This is a new version. Everyone signs again.</label>
<button class="btn btn-primary full">Save</button>
</form>"""

WRAP = """<div class=fxpage>
<a class=fxback href="/practices/{{ p.id }}">← Practice</a>
<h1>Wrap up.</h1>
<p class=t3>{{ when }} · {{ p.location or '' }}{% if wr and wr.closed_at %} · closed {{ wr.closed_at[:16].replace('T', ' ') }}{% endif %}</p>
<div class=p5metrics>
<div class="r2-metric lime"><b>{{ '%02d'|format(c.attended) }}</b><span>ATTENDED</span></div>
<div class="r2-metric"><b>{{ '%02d'|format(c.no_show) }}</b><span>NO-SHOW</span></div>
<div class="r2-metric"><b>{{ '%02d'|format(c.walk_in) }}</b><span>WALK-IN</span></div>
</div>
<form method=post class=fxsheet>{{ csrf_field() }}
<label class=fxfield><span>NOTE FOR ADMINS (PRIVATE)</span><textarea name=admin_note rows=3 maxlength=2000 placeholder="Lane 3 light out. Ana needs her USAWP renewed.">{{ wr.admin_note if wr else '' }}</textarea></label>
<label class=fxfield><span>RECAP TO PRACTICE CHAT (OPTIONAL)</span><input name=recap maxlength=280 placeholder="One line for everyone who came"></label>
<button class="btn btn-secondary full" name=action value=save>Save note</button>
<button class="btn btn-primary full" name=action value=close>{% if wr and wr.closed_at %}Save and keep closed{% else %}Close practice{% endif %}</button>
</form>
<p class=t3><a href="/admin?date={{ p.date }}">Back to check-in</a></p>
</div>"""

WEEK = """<div class=fxpage>
<span class=r2-chip>OPTIONAL</span>
<h1>When can you usually play?</h1>
<form method=post class=fxsheet>{{ csrf_field() }}
<div class=fxdays>{% for d in days %}<label><input type=checkbox name=day value="{{ d }}" {% if d in picked %}checked{% endif %}><span>{{ d[:1] }}</span></label>{% endfor %}</div>
<p class=t3>{{ fit }}</p>
<button class="btn btn-primary full" name=action value=save>Save my week</button>
<a class="btn quiet full" href="{{ back }}">Later</a>
</form></div>"""

SETUP_CARD = """{% if setup and setup.show %}<div class=fxsetup><div class=fxsetuphead><b>Finish setup</b><i class=r2-chip>{{ setup.done }} of {{ setup.steps|length }}</i></div>
{% for name, ok, href in setup.steps %}<div class="fxstep{% if ok %} ok{% endif %}">{% if ok %}<span class=fxtick>✓</span>{{ name }}{% else %}<span class=fxtick>○</span><a href="{{ href }}">{{ name }}</a><small>2 min →</small>{% endif %}</div>{% endfor %}
<form method=post action="/setup/dismiss">{{ csrf_field() }}<button class="btn quiet">Hide</button></form></div>{% endif %}"""

CSS = """
.fxcard.fxgate{display:flex;align-items:center;gap:12px;text-decoration:none;color:inherit;margin:12px 0}
.fxgate .grow,.fxask .grow{display:grid;gap:2px}
.fxgate small,.fxcard small{color:var(--color-text-secondary)}
.fxcard.cyan small{color:inherit}
.fxdark{background:var(--color-forest);color:var(--color-chalk)}
.fxrides{display:grid;gap:12px;margin:12px 0}
.fxcard{display:grid;gap:6px;padding:16px;border-radius:var(--radius-card);background:var(--color-surface-2);color:var(--color-text);border:0;text-align:left;font:inherit}
.fxcard.cyan{background:var(--color-cyan);color:var(--color-forest)}
.fxcard.cyan small{color:inherit;opacity:.8}
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
