"""Regulars 2.0 navigation model (Figma "Audit — 2026-11-12" · 60 NAV MODEL / 61 MANAGE).

One route tree, declared once. Back goes UP one layer to the canonical parent, never back in history.
Every template gets nav_back_href / nav_back_title / nav_area / nav_kind from one context processor
(app.nav_context_processor); no template computes its own back.

ROUTES[endpoint] = {title, parent, area, kind}
  title   str, or callable(args) -> str   (args = view args + query args)
  parent  endpoint name, or callable(args) -> (endpoint, {state}) | None
  area    schedule | lineup | chat | calendar | profile | manage | public   (which nav tab lights)
  kind    root | page | sheet | thread | asset | redirect
State the parent should restore (segment / filter) is carried as query args on the parent href.
"""

ROOTS = ("practices", "home", "lineup", "chat", "manage_home", "calendar", "profile", "discover")

MANAGE_AREAS = {"activities": "Activities", "people": "People", "club": "Club", "tools": "Tools"}
PEOPLE_VIEWS = {"members": "Participants", "paying": "Members", "coaches": "Coaches", "admins": "Admins",
                "referees": "Referees", "compliance": "Needs attention"}


def _a(args, key, default=""):
    v = args.get(key)
    return default if v in (None, "") else str(v)


def _chat_title(args):
    c = _a(args, "c")
    if not c:
        return "Chat"
    if c in ("team", "everyone"):
        return "#everyone"
    return "Chat"


def _chat_kind(args):
    return "thread" if _a(args, "c") else "root"


def _chat_parent(args):
    # Threads go up to the inbox they belong to. Practice chat also goes to Chat (decision, Nov 13).
    return ("chat", {"view": "list"}) if _a(args, "c") else None


def _member_parent(args):
    view = _a(args, "view", "members")
    return ("members", {"view": view} if view != "members" else {})


def _members_title(args):
    return PEOPLE_VIEWS.get(_a(args, "view", "members"), "People")


def _area_title(args):
    return MANAGE_AREAS.get(_a(args, "area"), "Manage")


def _sport_title(args):
    return (args.get("_sport_name") or _a(args, "slug").replace("-", " ").title() or "Sport")


def _role_title(args):
    return _a(args, "role").replace("-", " ").title() or "Role"


R = {}


def route(endpoint, title, parent, area, kind="page"):
    R[endpoint] = {"title": title, "parent": parent, "area": area, "kind": kind}


# Schedule
route("practices", "Schedule", None, "schedule", "root")
route("home", "Schedule", None, "schedule", "root")
route("index", "Schedule", "practices", "schedule", "redirect")
route("practice_page", "Practice", "practices", "schedule")
route("practice_signup", "Sign up", "practice_page", "schedule", "sheet")
route("participate", "Sign up", "practice_page", "schedule", "sheet")
route("practice_rides", "Rides", "practice_page", "schedule")
route("leave_by_page", "Leave by", "practice_page", "schedule")
route("practice_wrap", "Wrap-up", "practice_page", "schedule")
route("event_new", "Create", "practices", "schedule", "sheet")
route("series_new", "New series", "manage_schedule", "manage", "sheet")
route("series_page", "Series", "manage_schedule", "manage")
# Lineup
route("lineup", "Lineup", None, "lineup", "root")
route("lineup_detail", "Event", "lineup", "lineup")
route("lineup_edit", "Edit event", "lineup_detail", "lineup", "sheet")
route("lineup_new", "Suggest an event", "lineup", "lineup", "sheet")
route("lineup_shifts", "Volunteer shifts", "lineup_detail", "lineup")
route("lineup_shift_done", "Your shift", "lineup_shifts", "lineup")
route("register_for_event", "Register", "lineup", "lineup")
# Chat
route("chat", _chat_title, _chat_parent, "chat", _chat_kind)
route("chat_channels", "Channels", "chat", "chat")
route("chat_info", "Channel info", "chat", "chat", "sheet")
route("chat_person", "Person", "chat", "chat")
route("person_profile", "Person", "chat", "chat")
route("inbox", "Chat", "chat", "chat", "redirect")
# Calendar (Me)
route("calendar", "Calendar", None, "calendar", "root")
route("availability", "Availability", ("calendar", {"when": "availability"}), "calendar", "redirect")
route("availability_fit", "How your teams fit", ("calendar", {"when": "availability"}), "calendar")
route("availability_away", "Away dates", ("calendar", {"when": "availability"}), "calendar", "redirect")
route("setup_week", "Your week", ("calendar", {"when": "availability"}), "calendar", "sheet")
# Profile (Me)
route("profile", "Profile", None, "profile", "root")
route("settings", "Settings", "profile", "profile")
route("notifications", "Notifications", "settings", "profile")
route("privacy", "Privacy", "settings", "profile")
route("appearance", "Appearance", "settings", "profile")
route("ride_settings", "Rides", "settings", "profile")
# Manage
route("manage_home", "Manage", None, "manage", "root")
route("manage_search", "Search", "manage_home", "manage")
route("manage_area", _area_title, "manage_home", "manage")
route("manage_schedule", "Schedule", ("manage_area", {"area": "activities"}), "manage")
route("manage_lineup", "Lineup", ("manage_area", {"area": "activities"}), "manage")
route("manage_requests", "Requests", ("manage_area", {"area": "activities"}), "manage")
route("manage_request", "Reply", "manage_requests", "manage", "sheet")
route("admin", "Check-in", ("manage_area", {"area": "activities"}), "manage")
route("approvals", "Requests", "manage_requests", "manage", "redirect")
route("members", _members_title, ("manage_area", {"area": "people"}), "manage")
route("admins", "Admins", "members", "manage", "redirect")
route("expiring", "Expiring", ("manage_area", {"area": "people"}), "manage")
route("member_page", "Member", _member_parent, "manage")
route("requirements_page", "Sports", "club_programs", "manage", "redirect")
route("club_programs", "Sports", ("manage_area", {"area": "club"}), "manage")
route("club_program_new", "New sport", "club_programs", "manage", "sheet")
route("club_program", _sport_title, "club_programs", "manage")
route("sport_role_rules", _role_title, "club_program", "manage")
route("sport_rule_new", "Add requirement", "club_program", "manage", "sheet")
route("sport_rule_edit", "Edit requirement", "club_program", "manage", "sheet")
route("club_program_requirement_new", "Add requirement", "club_program", "manage", "sheet")
route("sport_divisions", "Divisions", "club_program", "manage")
route("sport_division_new", "New division", "club_program", "manage", "sheet")
route("sport_division_edit", "Edit division", "club_program", "manage", "sheet")
route("sport_leadership_new", "New role", "club_program", "manage", "sheet")
route("sport_leadership_edit", "Edit role", "club_program", "manage", "sheet")
route("sport_schedule_day_new", "Add a day", "club_program", "manage", "sheet")
route("sport_schedule_day_edit", "Edit day", "club_program", "manage", "sheet")
route("club_compliance", "Sports", "club_programs", "manage", "redirect")
route("club_compliance_new", "New requirement", "club_programs", "manage", "sheet")
route("club_compliance_edit", "Edit requirement", "club_programs", "manage", "sheet")
route("club_requirements", "Sports", "club_programs", "manage", "redirect")
route("club_requirement", "Requirement", "club_programs", "manage", "sheet")
route("club_requirement_new", "New requirement", "club_programs", "manage", "sheet")
route("club_plans", "Plans & payments", ("manage_area", {"area": "club"}), "manage")
route("club_plan", "Edit plan", "club_plans", "manage", "sheet")
route("club_plan_new", "New plan", "club_plans", "manage", "sheet")
route("club_integrations", "Plans & payments", "club_plans", "manage", "redirect")
route("manage_pricing", "Pricing", "club_plans", "manage")
route("manage_pay_membership", "Membership", "manage_pricing", "manage")
route("manage_pay_plans", "Plans", "manage_pricing", "manage")
route("manage_pay_providers", "Providers", "manage_pricing", "manage")
route("manage_pay_sports", "Sports", "manage_pricing", "manage")
route("club_venues", "Venues", ("manage_area", {"area": "club"}), "manage")
route("club_venue_new", "New venue", "club_venues", "manage", "sheet")
route("club_venue_edit", "Edit venue", "club_venues", "manage", "sheet")
route("manage_waiver", "Documents", ("manage_area", {"area": "club"}), "manage")
route("club_permissions", "Roles & permissions", ("manage_area", {"area": "club"}), "manage")
route("club_permission_new", "Add person", "club_permissions", "manage", "sheet")
route("club_permission_edit", "Edit access", "club_permissions", "manage", "sheet")
route("club_leadership", "Roles & permissions", "club_permissions", "manage", "redirect")
route("club_leadership_new", "New role", "club_permissions", "manage", "sheet")
route("club_leadership_edit", "Edit role", "club_permissions", "manage", "sheet")
route("club_reminders", "Reminders", ("manage_area", {"area": "club"}), "manage")
route("manage_widget", "Website & sharing", ("manage_area", {"area": "club"}), "manage")
# Tools pages keep their current URLs until the Figma 61 · M4 rebuild moves them under /manage/tools/.
route("qr_page", "QR codes", "tools_qr", "manage", "redirect")
route("email_home", "Email", ("manage_area", {"area": "activities"}), "manage")
route("email_builder", "New email", "email_home", "manage", "sheet")
route("email_preview", "Preview", "email_builder", "manage")
route("email_report", "Sent", "email_home", "manage")
route("email_open", "Email", None, "public", "asset")
route("email_click", "Email", None, "public", "asset")
route("email_unsub", "Unsubscribe", None, "public", "root")
route("tools_qr", "QR codes", ("manage_area", {"area": "tools"}), "manage")
route("transfer_page", "Data transfer", "tools_transfer", "manage", "redirect")
route("tools_transfer", "Data transfer", ("manage_area", {"area": "tools"}), "manage")
route("export_page", "Data transfer", "tools_transfer", "manage", "redirect")
route("import_page", "Data transfer", "tools_transfer", "manage", "redirect")
route("usage_page", "Usage", "tools_usage", "manage", "redirect")
route("tools_usage", "Usage", ("manage_area", {"area": "tools"}), "manage")
route("design_system_page", "Design system", ("manage_area", {"area": "tools"}), "manage")
# Public / visitor
route("discover", "Discover", None, "public", "root")
route("find_team", "Discover", "discover", "public", "redirect")
route("join", "Join", "discover", "public")
route("login", "Log in", "discover", "public")
# Files, feeds and endpoints that aren't screens
for ep in ("avatar", "media", "practice_image", "lineup_image", "practice_ics", "lineup_shift_ics", "practices_csv",
           "members_csv", "payments_csv", "export_all_zip", "qr_svg", "service_worker", "webmanifest", "widget_frame", "auth", "auth_google",
           "auth_google_callback", "logout", "practice_reminder_off", "static"):
    route(ep, "", None, "public", "asset")

ROUTES = R


def entry(endpoint):
    return ROUTES.get(endpoint)


def _resolve(value, args):
    return value(args) if callable(value) else value


def kind(endpoint, args):
    e = ROUTES.get(endpoint)
    return _resolve(e["kind"], args) if e else None


def title(endpoint, args):
    e = ROUTES.get(endpoint)
    return _resolve(e["title"], args) if e else ""


def parent(endpoint, args):
    """(parent_endpoint, state) or None for roots."""
    e = ROUTES.get(endpoint)
    if not e or kind(endpoint, args) == "root":
        return None
    p = _resolve(e["parent"], args)
    if p is None:
        return None
    if isinstance(p, tuple):
        return p
    return (p, {})


# View args a parent inherits from its child (e.g. /practices/<pid>/rides → /practices/<pid>).
CARRY = ("pid", "eid", "slug", "mid", "area")


def parent_url(endpoint, args, url_for):
    """Back href for this route, with the parent's restore state. None for roots."""
    p = parent(endpoint, args)
    if not p:
        return None
    pe, state = p
    from werkzeug.routing import BuildError
    params = dict(state)
    try:
        from flask import current_app
        needed = set()
        for rule in current_app.url_map.iter_rules(pe):
            needed |= set(rule.arguments)
    except Exception:
        needed = set(CARRY)
    for k in CARRY:
        if k in args and k in needed and k not in params:
            params[k] = args[k]
    try:
        return url_for(pe, **params)
    except BuildError:
        try:
            return url_for(pe, **state)
        except BuildError:
            return None


def parent_title(endpoint, args):
    p = parent(endpoint, args)
    if not p:
        return ""
    pe, state = p
    merged = dict(args)
    merged.update(state)
    return title(pe, merged)


def area(endpoint, args):
    e = ROUTES.get(endpoint)
    return e["area"] if e else ""


def depth(endpoint, args, limit=8):
    """Hops to a root. Raises on a cycle or a dangling parent."""
    seen, ep, a, n = set(), endpoint, dict(args), 0
    while True:
        p = parent(ep, a)
        if not p:
            return n
        pe, state = p
        if pe not in ROUTES:
            raise KeyError("%s has unknown parent %s" % (ep, pe))
        key = (pe, tuple(sorted(state.items())))
        if key in seen or n > limit:
            raise RuntimeError("cycle at %s" % ep)
        seen.add(key)
        a = {k: v for k, v in a.items() if k in CARRY}
        a.update(state)
        ep, n = pe, n + 1
