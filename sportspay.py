"""Sports, payment plans, and paid access.

USA Water Polo verification stays on the member row. Paid membership is a
separate entitlement. Nothing here rewrites RSVPs or sends mail.
"""
import datetime as dt
from markupsafe import escape

BODIES = (("usawp", "USA Water Polo"), ("usms", "US Masters Swimming"), ("none", "None"))
PLAN_KINDS = (("monthly", "Monthly membership"), ("drop_in", "Drop-in"), ("pass", "Session pass"), ("trial", "Introductory trial"), ("free", "Free sessions"))
PROVIDER_KINDS = (("external_link", "External payment link"), ("manual", "Manual payment"), ("free", "Free / trial access"), ("stripe", "Stripe"))
STATUSES = ("active", "pending", "expired", "inactive")
ACTIVITIES = (("practice", "Practice"), ("scrimmage", "Scrimmage"), ("game", "Game"))
CLUB_MONTHLY = "https://www.clubassistant.com/club/clinics/reserve.cfm?c=2180&cid=103002"
SWIM_DROPIN = "https://www.clubassistant.com/club/clinics/reserve.cfm?c=2180&cid=92340"


def ensure_schema(d):
    d.execute("""CREATE TABLE IF NOT EXISTS payment_settings(
        id INTEGER PRIMARY KEY CHECK (id=1), require_rsvp INTEGER NOT NULL DEFAULT 0)""")
    d.execute("INSERT OR IGNORE INTO payment_settings(id, require_rsvp) VALUES(1, 0)")
    d.execute("""CREATE TABLE IF NOT EXISTS org_sports(
        id INTEGER PRIMARY KEY, slug TEXT NOT NULL UNIQUE, name TEXT NOT NULL,
        active INTEGER NOT NULL DEFAULT 1, archived INTEGER NOT NULL DEFAULT 0,
        is_default INTEGER NOT NULL DEFAULT 0, governing_body TEXT NOT NULL DEFAULT 'none',
        activities TEXT NOT NULL DEFAULT 'practice')""")
    d.execute("""CREATE TABLE IF NOT EXISTS payment_providers(
        id INTEGER PRIMARY KEY, kind TEXT NOT NULL, name TEXT NOT NULL,
        active INTEGER NOT NULL DEFAULT 1, note TEXT NOT NULL DEFAULT '')""")
    d.execute("""CREATE TABLE IF NOT EXISTS payment_plans(
        id INTEGER PRIMARY KEY, name TEXT NOT NULL, kind TEXT NOT NULL,
        provider_id INTEGER, external_url TEXT NOT NULL DEFAULT '',
        sports TEXT NOT NULL DEFAULT '', activities TEXT NOT NULL DEFAULT 'practice',
        quantity INTEGER NOT NULL DEFAULT 0, active INTEGER NOT NULL DEFAULT 1,
        notes TEXT NOT NULL DEFAULT '')""")
    d.execute("""CREATE TABLE IF NOT EXISTS payment_prices(
        id INTEGER PRIMARY KEY, plan_id INTEGER NOT NULL, amount_cents INTEGER NOT NULL,
        effective_on TEXT NOT NULL)""")
    d.execute("""CREATE TABLE IF NOT EXISTS access_entitlements(
        id INTEGER PRIMARY KEY, member_id INTEGER NOT NULL, plan_id INTEGER,
        provider_id INTEGER, status TEXT NOT NULL DEFAULT 'inactive',
        valid_from TEXT NOT NULL DEFAULT '', paid_through TEXT NOT NULL DEFAULT '',
        last_verified TEXT NOT NULL DEFAULT '', verified_by TEXT NOT NULL DEFAULT '',
        notes TEXT NOT NULL DEFAULT '', practice_id INTEGER, created_at TEXT NOT NULL DEFAULT '')""")
    d.execute("""CREATE TABLE IF NOT EXISTS payment_records(
        id INTEGER PRIMARY KEY, member_id INTEGER NOT NULL, plan_id INTEGER,
        provider_id INTEGER, practice_id INTEGER, entitlement_id INTEGER,
        amount_cents INTEGER, status TEXT NOT NULL DEFAULT 'recorded',
        note TEXT NOT NULL DEFAULT '', at TEXT NOT NULL, actor TEXT NOT NULL DEFAULT '')""")
    d.execute("""CREATE TABLE IF NOT EXISTS external_memberships(
        member_id INTEGER NOT NULL, body TEXT NOT NULL, number TEXT NOT NULL DEFAULT '',
        membership_type TEXT NOT NULL DEFAULT '', status TEXT NOT NULL DEFAULT 'unknown',
        valid_from TEXT NOT NULL DEFAULT '', valid_until TEXT NOT NULL DEFAULT '',
        verified_by TEXT NOT NULL DEFAULT '', verified_at TEXT NOT NULL DEFAULT '',
        PRIMARY KEY(member_id, body))""")
    d.execute("""CREATE TABLE IF NOT EXISTS access_audits(
        id INTEGER PRIMARY KEY, member_id INTEGER NOT NULL, actor_id INTEGER,
        actor TEXT NOT NULL, action TEXT NOT NULL, detail TEXT NOT NULL DEFAULT '',
        at TEXT NOT NULL)""")
    d.execute("""CREATE TABLE IF NOT EXISTS payment_checks(
        id INTEGER PRIMARY KEY, member_id INTEGER NOT NULL, practice_id INTEGER,
        plan_id INTEGER, status TEXT NOT NULL DEFAULT 'pending', note TEXT NOT NULL DEFAULT '',
        at TEXT NOT NULL)""")
    _backfill_sports(d)
    _seed(d)
    import clubadmin
    clubadmin.ensure(d)


def _backfill_sports(d):
    """Empty sports are Water Polo. A note that is clearly swimming is Swimming. RSVPs stay."""
    cols = {row[1] for row in d.execute("PRAGMA table_info(practices)")}
    if "sport" not in cols:
        return
    d.execute("UPDATE practices SET sport='Water Polo' WHERE sport IS NULL OR trim(sport)=''")
    d.execute("""UPDATE practices SET sport='Swimming'
        WHERE lower(coalesce(title,'') || ' ' || coalesce(note,'')) LIKE '%swimming%'
          AND lower(coalesce(title,'') || ' ' || coalesce(note,'')) NOT LIKE '%water polo%'
          AND coalesce(sport,'Water Polo')='Water Polo'""")


def _seed(d):
    if d.execute("SELECT 1 FROM org_sports LIMIT 1").fetchone():
        return
    d.execute("""INSERT INTO org_sports(slug, name, active, is_default, governing_body, activities)
        VALUES('water-polo','Water Polo',1,1,'usawp','practice,scrimmage,game')""")
    d.execute("""INSERT INTO org_sports(slug, name, active, is_default, governing_body, activities)
        VALUES('swimming','Swimming',1,0,'usms','practice')""")
    external = d.execute("""INSERT INTO payment_providers(kind, name, active, note)
        VALUES('external_link','Club Assistant',1,'Opens the club payment page. Nothing is charged here.')""").lastrowid
    d.execute("""INSERT INTO payment_providers(kind, name, active, note)
        VALUES('manual','Manual payment',1,'An admin records a payment the club already received.')""")
    d.execute("""INSERT INTO payment_providers(kind, name, active, note)
        VALUES('free','Free / trial access',1,'Uses the existing free-trial offer when that offer is on.')""")
    d.execute("""INSERT INTO payment_providers(kind, name, active, note)
        VALUES('stripe','Stripe',0,'Coming later. This provider cannot be turned on.')""")
    monthly = d.execute("""INSERT INTO payment_plans(name, kind, provider_id, external_url, sports, activities, active, notes)
        VALUES(?,?,?,?,?,?,1,?)""", (
            "Grunions Water Polo + Swim Membership", "monthly", external, CLUB_MONTHLY,
            "water-polo,swimming", "practice,scrimmage,game",
            "Covers Water Polo and Swimming. Governing-body rules stay on each sport.")).lastrowid
    d.execute("INSERT INTO payment_prices(plan_id, amount_cents, effective_on) VALUES(?,?,?)", (monthly, 4500, "2026-12-01"))
    d.execute("INSERT INTO payment_prices(plan_id, amount_cents, effective_on) VALUES(?,?,?)", (monthly, 5000, "2027-01-01"))
    drop = d.execute("""INSERT INTO payment_plans(name, kind, provider_id, external_url, sports, activities, active, notes)
        VALUES(?,?,?,?,?,?,1,?)""", (
            "Swimming drop-in", "drop_in", external, SWIM_DROPIN, "swimming", "practice",
            "US Masters swimmers. Not a Water Polo drop-in.")).lastrowid
    d.execute("INSERT INTO payment_prices(plan_id, amount_cents, effective_on) VALUES(?,?,?)", (drop, 1000, "2026-01-01"))


def require_rsvp(d):
    row = d.execute("SELECT require_rsvp FROM payment_settings WHERE id=1").fetchone()
    return bool(row and row["require_rsvp"])


def set_require_rsvp(d, on):
    d.execute("UPDATE payment_settings SET require_rsvp=? WHERE id=1", (1 if on else 0,))


def sports(d, include_archived=False):
    sql = "SELECT * FROM org_sports"
    if not include_archived:
        sql += " WHERE archived=0"
    sql += " ORDER BY is_default DESC, name"
    return d.execute(sql).fetchall()


def providers(d):
    return d.execute("SELECT * FROM payment_providers ORDER BY id").fetchall()


def plans(d):
    return d.execute("SELECT * FROM payment_plans ORDER BY active DESC, name").fetchall()


def prices(d, plan_id):
    return d.execute("SELECT * FROM payment_prices WHERE plan_id=? ORDER BY effective_on", (plan_id,)).fetchall()


def price_on(rows, day):
    """Latest price whose effective date is on or before day. None when the first date is still ahead."""
    chosen = None
    for row in rows:
        if row["effective_on"] <= day:
            chosen = row
    return chosen


def money(cents):
    cents = int(cents or 0)
    sign = "-" if cents < 0 else ""
    cents = abs(cents)
    return "%s$%d" % (sign, cents // 100) if cents % 100 == 0 else "%s$%d.%02d" % (sign, cents // 100, cents % 100)


def _csv(value):
    return [part.strip() for part in str(value or "").split(",") if part.strip()]


def _stamp(now=None):
    return (now or dt.datetime.now()).isoformat(timespec="seconds")


def audit(d, member_id, actor, action, detail):
    actor_id = actor["id"] if actor is not None else None
    d.execute("""INSERT INTO access_audits(member_id, actor_id, actor, action, detail, at)
        VALUES(?,?,?,?,?,?)""", (member_id, actor_id, _actor_name(actor), action, detail[:500], _stamp()))


def _actor_name(actor):
    if not actor:
        return "Grunions"
    first = actor["preferred_first"] or actor["first"] or ""
    last = actor["last"] or ""
    return ("%s %s" % (first, last)).strip() or "Admin"


def save_entitlement(d, member_id, actor, plan_id, status, valid_from, paid_through, notes):
    """Write one paid-membership row and an audit line. Does not touch RSVPs or USAWP."""
    if status not in STATUSES:
        raise ValueError("Choose a status.")
    plan = d.execute("SELECT * FROM payment_plans WHERE id=?", (plan_id,)).fetchone() if plan_id else None
    if plan_id and not plan:
        raise ValueError("Choose a plan.")
    provider_id = plan["provider_id"] if plan else None
    if plan and provider_id:
        provider = d.execute("SELECT kind, active FROM payment_providers WHERE id=?", (provider_id,)).fetchone()
        if provider and provider["kind"] == "stripe":
            raise ValueError("Stripe is not available.")
    today = dt.date.today().isoformat()
    verified_by = ""
    last_verified = ""
    if status == "active":
        verified_by = _actor_name(actor)
        last_verified = today
    ent = d.execute("""INSERT INTO access_entitlements(
        member_id, plan_id, provider_id, status, valid_from, paid_through, last_verified, verified_by, notes, created_at)
        VALUES(?,?,?,?,?,?,?,?,?,?)""", (
            member_id, plan_id or None, provider_id, status, valid_from or "", paid_through or "",
            last_verified, verified_by, (notes or "")[:500], _stamp())).lastrowid
    if status == "active" and plan:
        amount = price_on(prices(d, plan["id"]), paid_through or today)
        d.execute("""INSERT INTO payment_records(member_id, plan_id, provider_id, entitlement_id, amount_cents, status, note, at, actor)
            VALUES(?,?,?,?,?,?,?,?,?)""", (
                member_id, plan["id"], provider_id, ent, amount["amount_cents"] if amount else None,
                "recorded", "Marked by an admin. No card was charged.", _stamp(), _actor_name(actor)))
    label = plan["name"] if plan else "No plan"
    audit(d, member_id, actor, "paid membership", "%s · %s · through %s" % (label, status, paid_through or "—"))
    return ent


def update_entitlement(d, ent_id, member_id, actor, plan_id, status, valid_from, paid_through, notes):
    """Edit one manual paid record. Does not touch RSVPs."""
    row = d.execute("SELECT id FROM access_entitlements WHERE id=? AND member_id=?", (ent_id, member_id)).fetchone()
    if not row:
        raise ValueError("Choose a paid record.")
    if status not in STATUSES:
        raise ValueError("Choose a status.")
    plan = d.execute("SELECT * FROM payment_plans WHERE id=?", (plan_id,)).fetchone() if plan_id else None
    if plan and plan_id:
        provider = d.execute("SELECT kind FROM payment_providers WHERE id=?", (plan["provider_id"],)).fetchone() if plan["provider_id"] else None
        if provider and provider["kind"] == "stripe":
            raise ValueError("Stripe is not available.")
    d.execute("""UPDATE access_entitlements SET plan_id=?, status=?, valid_from=?, paid_through=?, notes=? WHERE id=?""", (
        plan_id or None, status, valid_from or "", paid_through or "", (notes or "")[:500], ent_id))
    audit(d, member_id, actor, "paid membership", "Updated %s · %s · through %s" % (plan["name"] if plan else "No plan", status, paid_through or "—"))


def end_entitlement(d, ent_id, member_id, actor):
    """End a paid record. Does not touch RSVPs or clearance."""
    row = d.execute("SELECT id FROM access_entitlements WHERE id=? AND member_id=?", (ent_id, member_id)).fetchone()
    if not row:
        raise ValueError("Choose a paid record.")
    d.execute("UPDATE access_entitlements SET status='inactive' WHERE id=?", (ent_id,))
    audit(d, member_id, actor, "paid membership", "Ended paid record %s" % ent_id)


def entitlements(d, member_id):
    return d.execute("""SELECT e.*, p.name AS plan_name, p.kind AS plan_kind
        FROM access_entitlements e LEFT JOIN payment_plans p ON p.id=e.plan_id
        WHERE e.member_id=? ORDER BY e.id DESC""", (member_id,)).fetchall()


def audits(d, member_id, limit=12):
    return d.execute("SELECT * FROM access_audits WHERE member_id=? ORDER BY id DESC LIMIT ?", (member_id, limit)).fetchall()


def membership_rows(d):
    people = d.execute("""SELECT id, first, preferred_first, last FROM members
        WHERE COALESCE(role,'')!='system' ORDER BY last, first""").fetchall()
    out = []
    for person in people:
        ent = d.execute("""SELECT e.status, e.paid_through, p.name AS plan_name
            FROM access_entitlements e LEFT JOIN payment_plans p ON p.id=e.plan_id
            WHERE e.member_id=? ORDER BY e.id DESC LIMIT 1""", (person["id"],)).fetchone()
        out.append({"id": person["id"], "name": _actor_name(person), "ent": ent})
    return out


def _sport_for(d, name):
    needle = " ".join(str(name or "").split()).casefold()
    for row in sports(d, include_archived=True):
        if row["name"].casefold() == needle or row["slug"] == needle:
            return row
    return None


def _gov_ok(d, member, body, today):
    if body in ("", "none"):
        return True
    if body == "usawp":
        status = str(member["usawp_status"] or "")
        until = str(member["usawp_valid_until"] or "")[:10]
        return status == "verified" and bool(until) and until >= today
    row = d.execute("SELECT status, valid_until FROM external_memberships WHERE member_id=? AND body=?", (member["id"], body)).fetchone()
    if not row:
        return False
    until = str(row["valid_until"] or "")[:10]
    return row["status"] == "verified" and bool(until) and until >= today


def _covers(plan, sport_slug, activity):
    sports_ok = sport_slug in _csv(plan["sports"])
    acts = _csv(plan["activities"])
    return sports_ok and (not acts or activity in acts)


def _entitlement_state(d, member_id, sport_slug, activity, today):
    active = expired = None
    rows = d.execute("""SELECT e.*, p.sports, p.activities, p.kind, p.name AS plan_name
        FROM access_entitlements e JOIN payment_plans p ON p.id=e.plan_id
        WHERE e.member_id=? ORDER BY e.id DESC""", (member_id,)).fetchall()
    for row in rows:
        if not _covers(row, sport_slug, activity):
            continue
        through = str(row["paid_through"] or "")[:10]
        start = str(row["valid_from"] or "")[:10]
        dated_out = (through and through < today) or (start and start > today) or row["status"] in ("expired", "inactive")
        if row["status"] == "active" and not dated_out:
            active = row
            break
        if expired is None:
            expired = row
    return active, expired


def decide(d, member, practice, today):
    """Read-only. allow means the existing Going write may run."""
    if not require_rsvp(d):
        return {"allow": True, "scenario": "open", "plans": [], "body": "", "sport": ""}
    import publicfeed
    sport_name = practice["sport"] or "Water Polo"
    activity = (practice["activity_type"] or "practice").strip().lower()
    sport = _sport_for(d, sport_name)
    slug = sport["slug"] if sport else "water-polo"
    body = sport["governing_body"] if sport else "usawp"
    gov = _gov_ok(d, member, body, today)
    import clubadmin
    program = clubadmin.program_for_label(d, sport_name)
    if program is not None and not program["active"]:
        gov = True
    elif program is not None and program["active"]:
        cleared = clubadmin.eligibility(d, member, program, activity, "athlete", today)
        if cleared["applied"] and cleared["status"] != "Cleared":
            return dict({"plans": [], "body": body, "sport": sport_name, "activity": activity, "slug": slug}, allow=False, scenario="C")
    active, expired = _entitlement_state(d, member["id"], slug, activity, today)
    trial = publicfeed.normalize_trial((publicfeed.load(d).get("trial") or {}))
    trial_hit = None
    if trial.get("enabled") and publicfeed.activity_ok(trial, activity):
        pending = d.execute("SELECT 1 FROM verify_requests WHERE member_id=? AND status='pending' LIMIT 1", (member["id"],)).fetchone()
        trial_hit = publicfeed.eligibility(trial, publicfeed.member_facts(member, bool(pending)), today, practice["date"])
    options = [plan for plan in plans(d) if plan["active"] and _covers(plan, slug, activity)]
    base = {"plans": options, "body": body, "sport": sport_name, "activity": activity, "slug": slug}
    if gov and active:
        return dict(base, allow=True, scenario="A")
    if trial_hit and trial_hit["status"] == "active":
        return dict(base, allow=True, scenario="D")
    if expired and not active:
        return dict(base, allow=False, scenario="E")
    if gov:
        return dict(base, allow=False, scenario="B")
    return dict(base, allow=False, scenario="C")


def record_check(d, member_id, practice_id, plan_id, note):
    d.execute("""INSERT INTO payment_checks(member_id, practice_id, plan_id, status, note, at)
        VALUES(?,?,?,'pending',?,?)""", (member_id, practice_id, plan_id, (note or "")[:300], _stamp()))


def verify_check(d, check_id, actor, today):
    """Confirm a reported payment. Adds a Going RSVP only when one does not exist."""
    row = d.execute("SELECT * FROM payment_checks WHERE id=?", (check_id,)).fetchone()
    if not row or row["status"] != "pending":
        raise ValueError("That payment check is not pending.")
    plan = d.execute("SELECT * FROM payment_plans WHERE id=?", (row["plan_id"],)).fetchone()
    if not plan:
        raise ValueError("Choose a plan.")
    save_entitlement(d, row["member_id"], actor, plan["id"], "active", today, today, "Verified external payment")
    d.execute("UPDATE payment_checks SET status='verified' WHERE id=?", (check_id,))
    existing = d.execute("SELECT 1 FROM rsvps WHERE practice_id=? AND member_id=?", (row["practice_id"], row["member_id"])).fetchone()
    if row["practice_id"] and not existing:
        practice = d.execute("SELECT id, cancelled FROM practices WHERE id=?", (row["practice_id"],)).fetchone()
        if practice and not practice["cancelled"]:
            d.execute("INSERT INTO rsvps(practice_id, member_id, going) VALUES(?,?,1)", (row["practice_id"], row["member_id"]))
    audit(d, row["member_id"], actor, "payment verified", plan["name"])


def card_status(d, member, practice, mine, today):
    if mine == 1:
        return "Going"
    choice = decide(d, member, practice, today)
    if choice["scenario"] in ("open", "A", "D"):
        return "Eligible to register"
    if choice["scenario"] == "C":
        return "Verification required"
    return "Payment required"


def participate_page(decision, practice_title, when):
    scenario = decision["scenario"]
    if scenario == "C":
        body_name = dict(BODIES).get(decision["body"], "a governing-body membership")
        return """<h1>Verification required</h1>
<p>%s needs a verified %s before you can join.</p>
<p class="t3 sm">Submit your membership details from your profile. This page does not confirm a spot.</p>
<p><a class="btn btn-primary" href="/home">Open membership</a></p>""" % (escape(decision["sport"]), escape(body_name))
    bits = ["<h1>Choose How to Participate</h1>",
            "<p>Select a payment option to join this practice.</p>",
            "<p class=nxtitle>%s</p>" % escape(practice_title),
            "<p class=\"t3 sm\">%s</p>" % escape(when)]
    if scenario == "E":
        bits.append("<p>Your paid membership is not active. Renew it or use another option. Nothing is charged from this page.</p>")
    found_drop = False
    for plan in decision["plans"]:
        if plan["kind"] == "drop_in":
            found_drop = True
        blurb = "Get access to eligible Grunions practices with a monthly membership." if plan["kind"] == "monthly" else "Pay for this practice only."
        action = "Become a Member" if plan["kind"] == "monthly" else "Pay Drop-In"
        bits.append("""<div class=card><h2>%s</h2><p>%s</p><p class=t3>%s</p>%s
<form method=post><input type=hidden name=plan_id value="%d">{{ csrf_field() }}
<button class="btn btn-secondary" name=action value=paid>I've completed payment</button></form></div>""" % (
            escape(plan["name"]), blurb, escape(plan["external_url"]),
            ('<p><a class="btn btn-primary" href="%s" target=_blank rel=noopener>%s</a></p>' % (escape(plan["external_url"]), action)) if plan["external_url"] else "",
            plan["id"]))
    if decision["slug"] == "water-polo" and not found_drop:
        bits.append("<div class=card><h2>Single Practice</h2><p>A Water Polo drop-in is not configured. Contact the organizer.</p></div>")
    return "".join(bits)


def pending_checks(d):
    return d.execute("""SELECT c.*, m.first, m.last, m.preferred_first, p.name AS plan_name
        FROM payment_checks c JOIN members m ON m.id=c.member_id
        LEFT JOIN payment_plans p ON p.id=c.plan_id
        WHERE c.status='pending' ORDER BY c.id DESC""").fetchall()


def nav(active):
    items = (("schedule", "Schedule", "/manage/pricing"), ("sports", "Sports", "/manage/pricing/sports"),
             ("plans", "Pricing", "/manage/pricing/plans"), ("providers", "Providers", "/manage/pricing/providers"),
             ("membership", "Membership", "/manage/pricing/membership"))
    bits = ['<div class="rolechips chiprow" data-seg role=group aria-label="Sports and pricing">']
    for key, label, href in items:
        bits.append('<a class="chip%s" href="%s">%s</a>' % (" on" if key == active else "", href, label))
    bits.append("</div>")
    return "".join(bits)


def _acts(selected):
    chosen = set(_csv(selected))
    bits = []
    for slug, label in ACTIVITIES:
        bits.append('<label class=checkline><input type=checkbox name=activity value="%s"%s> %s</label>' % (
            slug, " checked" if slug in chosen else "", label))
    return "".join(bits)


def sports_page(rows):
    cards = []
    for row in rows:
        body = dict(BODIES).get(row["governing_body"], row["governing_body"])
        cards.append("""<form method=post class=card>
{{ csrf_field() }}
<input type=hidden name=sport_id value="%d">
<label>Name<input name=name value="%s"></label>
<label>Governing body<select name=governing_body>%s</select></label>
<div class=seclabel>Schedule activities</div>
%s
<label class=switchrow>Active<span class=switch><input type=checkbox name=active value=1 %s><span></span></span></label>
<label class=switchrow>Default sport<span class=switch><input type=checkbox name=is_default value=1 %s><span></span></span></label>
<button class="btn btn-primary" name=action value=save>Save</button>
<button class="btn btn-secondary" name=action value=archive>Archive</button>
</form>""" % (
            row["id"], escape(row["name"]),
            "".join('<option value="%s"%s>%s</option>' % (key, " selected" if key == row["governing_body"] else "", label) for key, label in BODIES),
            _acts(row["activities"]),
            "checked" if row["active"] else "",
            "checked" if row["is_default"] else ""))
    add = """<form method=post class=card>
{{ csrf_field() }}
<h2>Add a sport</h2>
<label>Name<input name=name autocomplete=off></label>
<label>Governing body<select name=governing_body>%s</select></label>
<div class=seclabel>Schedule activities</div>
%s
<button class="btn btn-primary" name=action value=add>Add sport</button>
</form>""" % ("".join('<option value="%s">%s</option>' % pair for pair in BODIES), _acts("practice"))
    return "".join(cards) + add


def plans_page(plan_rows, price_rows, provider_rows):
    cards = []
    for plan in plan_rows:
        own = [row for row in price_rows if row["plan_id"] == plan["id"]]
        lines = "".join("<p class=offerline>%s from %s</p>" % (money(row["amount_cents"]), escape(row["effective_on"])) for row in own)
        prov = "".join('<option value="%s"%s>%s</option>' % (
            row["id"], " selected" if row["id"] == plan["provider_id"] else "", escape(row["name"])) for row in provider_rows if row["kind"] != "stripe")
        cards.append("""<form method=post class=card>
{{ csrf_field() }}
<input type=hidden name=plan_id value="%d">
<p class=t3>%s · %s</p>
<label>Name<input name=name value="%s"></label>
<label>Type<select name=kind>%s</select></label>
<label>Provider<select name=provider_id>%s</select></label>
<label>External URL<input name=external_url value="%s"></label>
<label>Sports<input name=sports value="%s" placeholder="water-polo, swimming"></label>
<label>Activities<input name=activities value="%s"></label>
%s
<label class=switchrow>Active<span class=switch><input type=checkbox name=active value=1 %s><span></span></span></label>
<label>Next price<input name=amount placeholder="50" inputmode=decimal></label>
<label>Effective<input type=date name=effective_on></label>
<button class="btn btn-primary" name=action value=save>Save</button>
</form>""" % (
            plan["id"], escape(plan["kind"]), "one-time" if plan["kind"] != "monthly" else "subscription",
            escape(plan["name"]),
            "".join('<option value="%s"%s>%s</option>' % (key, " selected" if key == plan["kind"] else "", label) for key, label in PLAN_KINDS),
            prov, escape(plan["external_url"]), escape(plan["sports"]), escape(plan["activities"]),
            lines, "checked" if plan["active"] else ""))
    return "".join(cards)


def providers_page(rows, require):
    cards = []
    for row in rows:
        later = row["kind"] == "stripe"
        cards.append("""<form method=post class=card>
{{ csrf_field() }}
<input type=hidden name=provider_id value="%d">
<h2>%s</h2>
<p class="t3 sm">%s</p>
<p>%s</p>
%s
</form>""" % (
            row["id"], escape(row["name"]), escape(row["note"]),
            "Coming later" if later else "",
            '<p class="t3 sm">Stripe checkout, subscriptions, and refunds are not built. This switch stays off.</p>' if later else
            '<label class=switchrow>Active<span class=switch><input type=checkbox name=active value=1 %s><span></span></span></label><button class="btn btn-secondary" name=action value=save>Save</button>' % ("checked" if row["active"] else "")))
    gate = """<form method=post class=card>
{{ csrf_field() }}
<input type=hidden name=gate value=1>
<label class=switchrow>Require payment access to RSVP<span class=switch><input type=checkbox name=require_rsvp value=1 %s><span></span></span></label>
<p class="t3 sm">Off by default. While this is off, Going works exactly as it does today. Turning it on does not change RSVPs that are already saved.</p>
<button class="btn btn-primary" name=action value=gate>Save</button>
</form>""" % ("checked" if require else "")
    return gate + "".join(cards)


def membership_page(rows):
    lines = []
    for row in rows:
        ent = row["ent"]
        if ent and ent["plan_name"]:
            state = "%s · %s · through %s" % (ent["plan_name"], ent["status"], ent["paid_through"] or "—")
        else:
            state = "No paid membership"
        lines.append('<a class=mrow href="/admin/member/%d#paid"><span class=grow><span class=mtitle>%s</span><span class=mdesc>%s</span></span></a>' % (
            row["id"], escape(row["name"]), escape(state)))
    return '<div class=mlist>%s</div>' % "".join(lines)


def member_block(plans_rows, ents, audit_rows):
    options = "".join('<option value="%d">%s</option>' % (plan["id"], escape(plan["name"])) for plan in plans_rows if plan["active"])
    statuses = "".join('<option value="%s">%s</option>' % (name, name.capitalize()) for name in STATUSES)
    current = []
    for ent in ents:
        current.append("<p>%s · %s · %s through %s</p>" % (
            escape(ent["plan_name"] or "No plan"), escape(ent["status"]), escape(ent["valid_from"] or "—"), escape(ent["paid_through"] or "—")))
    history = "".join("<p class=\"t3 sm\">%s · %s · %s</p>" % (escape(row["at"][:16]), escape(row["actor"]), escape(row["detail"])) for row in audit_rows)
    return """<div class=seclabel id=paid>Paid membership</div>
<p class="t3 sm">This is separate from the team roster and from USA Water Polo. Saving it does not change an RSVP and does not charge a card.</p>
<div class=list>%s</div>
<form method=post class=card>
{{ csrf_field() }}
<input type=hidden name=action value=paid>
<label>Plan<select name=plan_id>%s</select></label>
<label>Status<select name=paid_status>%s</select></label>
<label>Valid from<input type=date name=valid_from></label>
<label>Paid through<input type=date name=paid_through></label>
<label>Notes<textarea class=planfield name=paid_notes rows=3></textarea></label>
<button class="btn btn-primary" name=paid_action value=save>Save</button>
<button class="btn btn-secondary" name=paid_action value=active>Mark active</button>
</form>
<div class=seclabel>Audit</div>
%s""" % ("".join(current) or "<p class=\"t3 sm\">No paid membership yet.</p>", options, statuses, history or "<p class=\"t3 sm\">No paid-membership changes yet.</p>")
