"""Passes (Figma 62 · P1–P5, H1–H4): read-first pass pages with one sheet per section.

Every section sheet saves through clubadmin.save_pass, so the same validation and the
"never touches RSVPs" guard apply. A sheet only sends its own fields; the rest come from
the pass as it is (form_from_plan).
"""
import datetime as dt
from werkzeug.datastructures import MultiDict

import clubadmin as ca

FREQ_LABEL = {"week": "week", "month": "month", "year": "year"}
NEW_KINDS = (("monthly", "Membership", "Recurring access — monthly, yearly"),
             ("pass", "Practice pass", "A set number of practices"),
             ("drop_in", "Drop-in", "One practice"),
             ("trial", "Free trial", "Free for some days or practices, once per person"))


def _k(plan, key, default=""):
    return plan[key] if plan is not None and key in plan.keys() and plan[key] is not None else default


def pay_mode(d, plan):
    mode = "none"
    if _k(plan, "provider_id"):
        row = d.execute("SELECT kind FROM payment_providers WHERE id=?", (plan["provider_id"],)).fetchone()
        mode = {"external_link": "external", "manual": "manual", "free": "none"}.get(row["kind"] if row else "", "none")
    if _k(plan, "external_url") and mode == "none":
        mode = "external"
    return mode


def form_from_plan(d, plan):
    f = MultiDict()
    for key in ("name", "description", "kind", "renewal", "frequency", "length_mode", "audience", "external_url", "terms", "active_from", "active_until"):
        f[key] = str(_k(plan, key))
    for key in ("renewal_count", "length_days", "length_sessions", "uses_per_event"):
        f[key] = str(_k(plan, key, 0) or 0)
    if _k(plan, "one_per_person"): f["one_per_person"] = "1"
    if _k(plan, "offer_code") == "usawp_trial": f["offer_code"] = "usawp_trial"
    if _k(plan, "active"): f["active"] = "1"
    f["pay"] = pay_mode(d, plan)
    for a in ca._csv(_k(plan, "activities")):
        f["activity_" + a] = "1"
    for c in ca._csv(_k(plan, "lineup_categories")):
        f["lineup_" + c] = "1"
    for row in d.execute("SELECT program_id FROM plan_programs WHERE plan_id=?", (plan["id"],)):
        f.add("program", str(row["program_id"]))
    for row in d.execute("SELECT member_id FROM plan_people WHERE plan_id=?", (plan["id"],)):
        f.add("person", str(row["member_id"]))
    return f


SECTION_FIELDS = {
    "basics": ("name", "description", "kind"),
    "billing": ("frequency", "renewal", "renewal_count", "length_mode", "length_days", "length_sessions"),
    "dates": ("active_from", "active_until"),
    "covers": ("program", "activity_*", "lineup_*"),
    "who": ("audience", "person", "one_per_person", "uses_per_event", "offer_code"),
    "pay": ("pay", "external_url", "terms"),
    "status": ("active",),
}


def save_section(d, plan, section, form):
    fields = SECTION_FIELDS.get(section)
    if not fields:
        raise ValueError("Pick a section.")
    merged = form_from_plan(d, plan)
    for name in fields:
        if name.endswith("_*"):
            prefix = name[:-1]
            for key in [k for k in merged.keys() if k.startswith(prefix)]:
                merged.pop(key)
            for key in form.keys():
                if key.startswith(prefix): merged[key] = form.get(key)
        else:
            merged.pop(name, None)
            vals = [v for v in form.getlist(name)]
            for v in vals:
                if v not in ("", None) or name not in ("one_per_person", "offer_code", "active"):
                    merged.add(name, v)
            if name in ("one_per_person", "offer_code", "active") and form.get(name) in ("0", ""):
                merged.pop(name, None)
    if section == "billing" and form.get("renewal") == "once":
        merged["renewal"] = "fixed"; merged["renewal_count"] = "1"
    return ca.save_pass(d, plan["id"], merged)


def add_price(d, plan_id, raw, effective_on):
    cents = ca._dollars(raw)
    if cents is None:
        raise ValueError("Enter a price.")
    day = ca._pass_date(effective_on, "the start date") or dt.date.today().isoformat()
    hit = d.execute("SELECT id FROM payment_prices WHERE plan_id=? AND effective_on=?", (plan_id, day)).fetchone()
    if hit:
        d.execute("UPDATE payment_prices SET amount_cents=? WHERE id=?", (cents, hit["id"]))
    else:
        d.execute("INSERT INTO payment_prices(plan_id, amount_cents, effective_on) VALUES(?,?,?)", (plan_id, cents, day))


def create(d, form):
    kind = form.get("kind") if form.get("kind") in dict((k, l) for k, l, _s in NEW_KINDS) else "monthly"
    progs = ca.programs(d)
    first = [p for p in progs if p["active"]] or progs
    f = MultiDict({"name": form.get("name") or "", "kind": kind, "price": form.get("price") or "",
                   "renewal": "indefinite", "frequency": "month", "audience": "everyone", "activity_practice": "1",
                   "pay": "none" if kind == "trial" else "manual", "active": "0"})
    if kind == "trial":
        f["length_mode"] = "duration"; f["length_days"] = "14"; f["one_per_person"] = "1"
    if kind == "pass":
        f["length_mode"] = "sessions"; f["length_sessions"] = form.get("sessions") or "10"
    if first:
        f.add("program", str(first[0]["id"]))
    return ca.save_pass(d, None, f)


def _date(iso):
    try:
        return ca._pretty_date(iso)
    except Exception:
        return iso or ""


def card(d, plan, today=None):
    today = today or dt.date.today().isoformat()
    rows = ca._price_rows(d, plan["id"])
    cents, starts = ca._shown_price(rows, today)
    free = plan["kind"] in ("trial", "free")
    price = "$0" if free else ("—" if cents is None else ca._money(cents))
    per = {"monthly": "/ " + (FREQ_LABEL.get(_k(plan, "frequency") or "month", "month")), "drop_in": "/ practice",
           "pass": "/ %d practices" % (_k(plan, "length_sessions", 0) or 0) if _k(plan, "length_sessions", 0) else "/ pack",
           "trial": "/ %d days" % (_k(plan, "length_days", 0) or 14) if _k(plan, "length_days", 0) else "", "free": ""}.get(plan["kind"], "")
    if plan["kind"] == "trial" and _k(plan, "length_days", 0) == 14: per = "/ 2 weeks"
    acts = [l for a, l in ca.ACTIVITIES if a in ca._csv(_k(plan, "activities"))]
    covers = "%s · %s" % (", ".join(ca.plan_program_names(d, plan["id"]) or ["No sport yet"]), ", ".join(acts).capitalize() if acts else "No activities")
    return {"id": plan["id"], "name": plan["name"], "on": bool(plan["active"]), "price": price, "per": per,
            "covers": covers, "line": renew_line(plan) + " · " + window_line(plan), "starts": starts}


def renew_line(plan):
    k = plan["kind"]
    if k == "monthly":
        freq = FREQ_LABEL.get(_k(plan, "frequency") or "month", "month")
        if _k(plan, "renewal") == "fixed" and _k(plan, "renewal_count", 0):
            n = plan["renewal_count"]
            return "Renews every %s, %d time%s" % (freq, n, "" if n == 1 else "s")
        return "Renews every %s, until cancelled" % freq
    if k == "drop_in":
        return "One practice"
    if k == "pass":
        return "%d practices" % (_k(plan, "length_sessions", 0) or 0)
    if k == "trial":
        bits = []
        if _k(plan, "length_days", 0): bits.append("%d days" % plan["length_days"])
        if _k(plan, "length_sessions", 0): bits.append("%d practices" % plan["length_sessions"])
        return "Once per person · ends after " + (" or ".join(bits) or "the trial")
    return "Free"


def window_line(plan):
    start, end = str(_k(plan, "active_from"))[:10], str(_k(plan, "active_until"))[:10]
    if start and end: return "%s to %s" % (_date(start), _date(end))
    if start: return "starts %s · no end date" % _date(start)
    if end: return "ends %s" % _date(end)
    return "no end date"


def detail(d, plan):
    today = dt.date.today().isoformat()
    rows = ca._price_rows(d, plan["id"])
    now = [r for r in rows if r["effective_on"] <= today]
    later = [r for r in rows if r["effective_on"] > today]
    price_rows = []
    if plan["kind"] in ("trial", "free"):
        price_rows.append(("Now", "Free"))
    else:
        if now: price_rows.append(("Now", "%s USD from %s" % (ca._money(now[-1]["amount_cents"]), _date(now[-1]["effective_on"]))))
        for r in later: price_rows.append(("Next", "%s from %s" % (ca._money(r["amount_cents"]), _date(r["effective_on"]))))
        if not price_rows: price_rows.append(("Now", "Not set"))
    progs = ca.plan_program_names(d, plan["id"])
    acts = [l for a, l in ca.ACTIVITIES if a in ca._csv(_k(plan, "activities"))]
    cats = [l for a, l in ca.LINEUP_CATS if a in ca._csv(_k(plan, "lineup_categories"))]
    aud = {"everyone": "Everyone", "new": "New members only", "specific": "Specific people"}.get(_k(plan, "audience") or "everyone", "Everyone")
    pay = {"external": "Club Assistant link", "manual": "Manual — the board records it", "none": "Free"}[pay_mode(d, plan)]
    sections = [
        ("basics", "Basics", [("Name", plan["name"]), ("Type", dict(ca.PASS_KINDS).get(plan["kind"], plan["kind"])), ("Description", _k(plan, "description") or "—")]),
        ("price", "Price", price_rows),
        ("billing", "Billing & renewal" if plan["kind"] == "monthly" else "Length", [("Renews" if plan["kind"] == "monthly" else "Length", renew_line(plan))]),
        ("dates", "Active dates", [("Covers events", window_line(plan).capitalize())]),
        ("covers", "Covers", [("Sports", ", ".join(progs) or "None"), ("Schedule", ", ".join(acts).capitalize() if acts else "None"), ("Lineup", ", ".join(cats) or "None")]),
        ("who", "Who & limits", [("Who can get it", aud), ("Per person", "One" if _k(plan, "one_per_person") else "No limit"),
                                 ("Per event", ("%d" % plan["uses_per_event"]) if _k(plan, "uses_per_event", 0) else "No limit")]),
        ("pay", "Where to pay", [("Method", pay), ("Terms", "Added" if _k(plan, "terms") else "None")]),
    ]
    return sections
