"""Branded HTML mail. Outgoing messages include this HTML unless HTML_EMAILS_ENABLED=0."""
import html
import os

ORG_NAME = "Grunions Water Polo"
TAGLINE = "Good things happen when we show up."
# Figma 11 · Emails (2.0). Light is the default; dark comes from the stylesheet below.
FIXED_INK = "#0B0B0C"
LIME = "#C8FF3C"
PAGE = "#F3F1EB"        # color/ink (light)
CARD = "#FFFFFF"        # color/carbon (light)
TEXT = "#0B0B0C"        # color/paper (light)
BOX = "#E6E2D9"         # color/graphite (light)
MUTED = "#6A6E73"       # color/smoke (light)
ACCENT = "#4A6A00"      # accent/text (light)
DARK = {"page": "#0B0B0C", "card": "#17181A", "text": "#F6F4EF", "box": "#24262A", "muted": "#8B8F93", "accent": "#C8FF3C"}
HERO = {"lime": "#C8FF3C", "tangerine": "#FF5A1F", "lavender": "#A89CFF", "sky": "#7CC8F4", "aqua": "#2EE6C8",
        "sun": "#FFC61A", "mango": "#FF9F1C", "cherry": "#FF3D57", "cobalt": "#4F7BFF", "bubblegum": "#FF5FB8"}
DISPLAY = "'Space Grotesk',Arial,Helvetica,sans-serif"
SANS = "'Plus Jakarta Sans',Arial,Helvetica,sans-serif"
# Kept for callers that still import them.
INK = TEXT
WASH = BOX
LINE = BOX
EYEBROW = ACCENT
FONT = SANS

def html_emails_enabled():
    return os.environ.get("HTML_EMAILS_ENABLED", "1") != "0"

def _e(value):
    return html.escape(str(value if value is not None else ""), quote=False)
def _a(value):
    return html.escape(str(value if value is not None else ""), quote=True)

def _style(base):
    b = base.rstrip("/")
    faces = "".join(
        "@font-face{font-family:'%s';font-style:normal;font-weight:%d;src:url('%s/static/fonts/%s-%d.woff2') format('woff2')}" % (fam, w, b, slug, w)
        for fam, slug, weights in (("Space Grotesk", "space-grotesk", (700,)), ("Plus Jakarta Sans", "plus-jakarta-sans", (500, 600, 700)))
        for w in weights)
    dark = ("{.r-page{background:%(page)s!important}.r-card{background:%(card)s!important}.r-text{color:%(text)s!important}"
            ".r-box{background:%(box)s!important}.r-muted{color:%(muted)s!important}.r-accent{color:%(accent)s!important}"
            ".r-text a{color:%(text)s!important}.r-muted a{color:%(muted)s!important}}") % DARK
    ogsc = dark[1:-1].replace(".r-", "[data-ogsc] .r-").replace("[data-ogsc] .r-page", "[data-ogsb] .r-page")
    return ("<style>%s:root{color-scheme:light dark;supported-color-schemes:light dark}"
            "body{margin:0;padding:0;-webkit-text-size-adjust:100%%}a{text-decoration:none}"
            "@media (prefers-color-scheme:dark)%s%s"
            "</style>") % (faces, dark, ogsc)

def _gap(px):
    return '<tr><td style="height:%dpx;line-height:%dpx;font-size:0;">&nbsp;</td></tr>' % (px, px)

def _detail(label, value):
    return ('<table role="presentation" width="100%%" cellspacing="0" cellpadding="0" border="0" class="r-box" bgcolor="%s" style="background:%s;border-radius:22px;">'
            '<tr><td style="padding:14px 18px;">'
            '<div class="r-muted" style="font-family:%s;font-size:9px;line-height:12px;font-weight:700;letter-spacing:.72px;color:%s;">%s</div>'
            '<div style="height:4px;line-height:4px;font-size:0;">&nbsp;</div>'
            '<div class="r-text" style="font-family:%s;font-size:16px;line-height:20px;font-weight:700;color:%s;">%s</div>'
            '</td></tr></table>' % (BOX, BOX, SANS, MUTED, _e(label), SANS, TEXT, _e(value)))

def _note(label, value):
    return ('<table role="presentation" width="100%%" cellspacing="0" cellpadding="0" border="0" class="r-box" bgcolor="%s" style="background:%s;border-radius:22px;">'
            '<tr><td style="padding:14px 18px;">'
            '<div class="r-accent" style="font-family:%s;font-size:9px;line-height:12px;font-weight:700;letter-spacing:.72px;color:%s;">%s</div>'
            '<div style="height:4px;line-height:4px;font-size:0;">&nbsp;</div>'
            '<div class="r-text" style="font-family:%s;font-size:13px;line-height:17px;font-weight:600;color:%s;">%s</div>'
            '</td></tr></table>' % (BOX, BOX, SANS, ACCENT, _e(label.upper()), SANS, TEXT, _e(value)))

def _cta(label, url):
    return ('<table role="presentation" width="100%%" cellspacing="0" cellpadding="0" border="0"><tr>'
            '<td align="center" bgcolor="%s" style="background:%s;border-radius:999px;">'
            '<a href="%s" style="display:block;padding:18px 16px;font-family:%s;font-size:16px;line-height:20px;font-weight:700;color:%s;text-decoration:none;text-align:center;">%s</a>'
            '</td></tr></table>' % (LIME, LIME, _a(url), SANS, FIXED_INK, _e(label)))

def _pills(links):
    cells = []
    for i, (label, url) in enumerate(links):
        if i: cells.append('<td style="width:8px;font-size:0;">&nbsp;</td>')
        cells.append('<td align="center" class="r-box" bgcolor="%s" style="background:%s;border-radius:999px;">'
                     '<a href="%s" class="r-text" style="display:block;padding:14px 8px;font-family:%s;font-size:13px;line-height:17px;font-weight:700;color:%s;text-decoration:none;text-align:center;">%s</a></td>'
                     % (BOX, BOX, _a(url), SANS, TEXT, _e(label)))
    return '<table role="presentation" width="100%%" cellspacing="0" cellpadding="0" border="0" style="table-layout:fixed;"><tr>%s</tr></table>' % "".join(cells)

def render_v2(base, hero, eyebrow, big, headline, first, paragraphs, org=ORG_NAME, rows=None, note=None, cta=None,
              calendar=None, fallback=None, footer_link=None, footer_note=None, big_size=112, preheader="", image=""):
    """Figma 11 · Emails 2.0: colored hero (logo, eyebrow, big figure, headline), body, footer.
    Table layout with inline styles; dark mode comes from prefers-color-scheme. Dynamic text is escaped."""
    hero_bg = HERO.get(hero, hero)
    track = -0.05 * big_size
    big_html = "<br>".join(_e(part) for part in str(big).split("\n"))
    blocks = ['<div class="r-text" style="font-family:%s;font-size:17px;line-height:22px;font-weight:700;color:%s;">Hi %s,</div>' % (SANS, TEXT, _e(first))]
    if image:
        blocks.insert(0, '<img src="%s" alt="" width="552" style="display:block;width:100%%;max-width:552px;height:auto;border:0;outline:none;border-radius:22px;">' % _a(image))
    for p in paragraphs:
        blocks.append('<div class="r-text" style="font-family:%s;font-size:15px;line-height:22.5px;font-weight:500;color:%s;">%s</div>' % (SANS, TEXT, _e(p)))
    if note:
        blocks.append(_note(*note))
    if rows:
        blocks.append('<table role="presentation" width="100%%" cellspacing="0" cellpadding="0" border="0">%s</table>'
                      % "".join(('<tr><td>%s</td></tr>' % _detail(l, v)) + (_gap(10) if i < len(rows) - 1 else "") for i, (l, v) in enumerate(rows)))
    if cta:
        blocks.append(_cta(*cta))
    if calendar:
        blocks.append(_pills(calendar))
    if fallback:
        blocks.append('<div class="r-muted" style="font-family:%s;font-size:11px;line-height:14px;font-weight:600;color:%s;overflow-wrap:anywhere;word-break:break-word;">'
                      'Button not working? Copy this link into your browser: <a href="%s" style="color:%s;text-decoration:underline;">%s</a></div>'
                      % (SANS, MUTED, _a(fallback), MUTED, _e(fallback)))
    body = "".join(('<tr><td>%s</td></tr>' % b) + (_gap(16) if i < len(blocks) - 1 else "") for i, b in enumerate(blocks))
    foot = []
    if footer_link:
        label, url = footer_link
        foot.append('<div class="r-text" style="font-family:%s;font-size:12px;line-height:16px;font-weight:600;color:%s;"><a href="%s" style="color:%s;text-decoration:underline;">%s</a></div>'
                    % (SANS, TEXT, _a(url), TEXT, _e(label)))
    if footer_note:
        foot.append('<div class="r-text" style="font-family:%s;font-size:12px;line-height:16px;font-weight:600;color:%s;">%s</div>' % (SANS, TEXT, _e(footer_note)))
    foot.append('<div class="r-muted" style="font-family:%s;font-size:11px;line-height:14px;font-weight:600;color:%s;">Sent by Regulars for %s.</div>' % (SANS, MUTED, _e(org)))
    foot.append('<div class="r-text" style="font-family:%s;font-size:14px;line-height:14px;font-weight:700;letter-spacing:-0.42px;color:%s;">%s</div>' % (DISPLAY, TEXT, _e(TAGLINE)))
    footer = '<div style="height:6px;line-height:6px;font-size:0;">&nbsp;</div>'.join(foot)
    pre = ('<div style="display:none;max-height:0;overflow:hidden;mso-hide:all;font-size:1px;line-height:1px;color:%s;opacity:0;">%s&#8203;&nbsp;&#8203;&nbsp;&#8203;&nbsp;</div>'
           % (PAGE, _e(preheader))) if preheader else ""
    mark = base.rstrip("/") + "/static/email-mark.png"
    return (
        '<!doctype html><html lang="en"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width,initial-scale=1">'
        '<meta name="color-scheme" content="light dark"><meta name="supported-color-schemes" content="light dark">'
        '%s</head><body class="r-page" bgcolor="%s" style="margin:0;padding:0;background:%s;">%s'
        '<table role="presentation" width="100%%" cellspacing="0" cellpadding="0" border="0" class="r-page" bgcolor="%s" style="background:%s;">'
        '<tr><td align="center" style="padding:24px 16px;">'
        '<table role="presentation" width="100%%" cellspacing="0" cellpadding="0" border="0" class="r-card" bgcolor="%s" style="max-width:600px;background:%s;border-radius:36px;overflow:hidden;">'
        # Hero
        '<tr><td bgcolor="%s" style="background:%s;padding:22px 24px 26px;border-radius:36px 36px 0 0;">'
        '<table role="presentation" width="100%%" cellspacing="0" cellpadding="0" border="0"><tr>'
        '<td style="vertical-align:middle;"><table role="presentation" cellspacing="0" cellpadding="0" border="0"><tr>'
        '<td style="vertical-align:top;padding-top:2px;"><img src="%s" alt="" width="33" height="13" style="display:block;border:0;outline:none;width:33px;height:13px;"></td>'
        '<td style="padding-left:4px;font-family:%s;font-size:18px;line-height:18px;font-weight:700;letter-spacing:-0.54px;color:%s;white-space:nowrap;">regulars</td>'
        '</tr></table></td>'
        '<td align="right" style="vertical-align:middle;font-family:%s;font-size:10px;line-height:13px;font-weight:700;letter-spacing:.8px;color:%s;padding-left:12px;">%s</td>'
        '</tr></table>'
        '<div style="height:18px;line-height:18px;font-size:0;">&nbsp;</div>'
        '<div class="r-big" style="font-family:%s;font-size:%dpx;line-height:%.2fpx;font-weight:700;letter-spacing:%.2fpx;color:%s;">%s</div>'
        '<div style="height:18px;line-height:18px;font-size:0;">&nbsp;</div>'
        '<div style="font-family:%s;font-size:28px;line-height:27.44px;font-weight:700;letter-spacing:-0.84px;color:%s;">%s</div>'
        '</td></tr>'
        # Body
        '<tr><td style="padding:24px 24px 28px;"><table role="presentation" width="100%%" cellspacing="0" cellpadding="0" border="0">%s</table></td></tr>'
        # Footer
        '<tr><td class="r-box" bgcolor="%s" style="background:%s;padding:18px 24px 22px;border-radius:0 0 36px 36px;">%s</td></tr>'
        '</table></td></tr></table></body></html>'
        % (_style(base), PAGE, PAGE, pre, PAGE, PAGE, CARD, CARD,
           hero_bg, hero_bg, _a(mark), DISPLAY, FIXED_INK, SANS, FIXED_INK, "<br>".join(_e(x) for x in str(eyebrow).split("\n")),
           DISPLAY, big_size, big_size * 0.86, track, FIXED_INK, big_html,
           DISPLAY, FIXED_INK, _e(headline), body, BOX, BOX, footer))

def render_email(eyebrow, headline, paragraphs, logo_url, cta=None, rows=None, note=None, fallback=None, org=ORG_NAME, footer_link=None, extra_links=None):
    """Older call shape (no hero figure). Renders in the 2.0 layout with a lime hero."""
    base = logo_url.split("/static/")[0] if "/static/" in logo_url else logo_url
    paras = list(paragraphs)
    first = "there"
    if paras and paras[0].startswith("Hi ") and paras[0].endswith(","):
        first = paras.pop(0)[3:-1]
    return render_v2(base, "lime", eyebrow, headline, headline, first, paras, org=org, rows=rows, note=note, cta=cta,
                     calendar=extra_links, fallback=fallback, footer_link=footer_link, big_size=56)

def logo_url(base):
    return base.rstrip("/") + "/static/email-lockup.png"

def sign_in_html(base, first, link, minutes, org=ORG_NAME):
    """11.01 Login Link."""
    return render_v2(base, "lime", "SECURE SIGN-IN", "%d min" % minutes, "Sign in.", first,
                     ["Use the button below to sign in to %s on Regulars." % org], org=org,
                     note=("For your security", "This link works once and expires in %d minutes. Never share it with anyone." % minutes),
                     cta=("Sign in securely", link), fallback=link, preheader="Your sign-in link works once and expires in %d minutes." % minutes)

def _day_figure(date_iso):
    """'2026-11-13' -> 'Fri 13'."""
    import datetime as dt
    try:
        d = dt.date.fromisoformat(str(date_iso)[:10])
        return "%s %d" % (d.strftime("%a"), d.day)
    except ValueError:
        return str(date_iso or "")

def _clock_figure(clock):
    """'7:00 PM' -> '7:00'."""
    return str(clock or "").replace(" AM", "").replace(" PM", "").replace("AM", "").replace("PM", "").strip()

def practice_cancelled_html(base, first, when, place, reason, url, org=ORG_NAME, date_iso=""):
    """11.02 Practice Cancelled."""
    rows = [("WHEN", when)]
    if place: rows.append(("WHERE", place))
    rows.append(("STATUS", "Cancelled"))
    line = "This session has been cancelled."
    if reason:
        line += " " + reason.rstrip(".") + "."
    return render_v2(base, "tangerine", "SCHEDULE CHANGE", _day_figure(date_iso) or "Off", "Practice cancelled.", first, [line],
                     org=org, rows=rows, cta=("View the schedule", url), preheader=line)

def practice_rows(sport, when, place):
    rows = [("SPORT", sport), ("WHEN", when)]
    if place:
        rows.append(("WHERE", place))
    return rows

def _sentence_case(sport):
    sport = str(sport or "Water Polo")
    return sport[:1].upper() + sport[1:].lower()

def practice_reminder_html(base, first, headline, sentence, sport, when, place, url, button, unsub, org=ORG_NAME, clock=""):
    """11.08 Practice Reminder. The button opens the session."""
    return render_v2(base, "sun", "PRACTICE · TODAY", _clock_figure(clock) or "Today", "%s practice today." % _sentence_case(sport), first,
                     [sentence], org=org, rows=practice_rows(sport, when, place), cta=(button, url), fallback=url,
                     footer_link=("Turn off practice reminder emails", unsub), preheader=sentence)

def practice_signup_html(base, first, headline, sentence, sport, when, place, url, google, ics_url, org=ORG_NAME, clock="", weekday=""):
    """11.09 Signup Confirmation, with calendar buttons."""
    return render_v2(base, "lime", "YOU'RE SIGNED UP", _clock_figure(clock) or "In", ("See you %s." % weekday) if weekday else "See you there.", first,
                     [sentence], org=org, rows=practice_rows(sport, when, place), cta=("View practice", url),
                     calendar=(("Google Calendar", google), ("Apple / Outlook", ics_url)), fallback=url, preheader=sentence)

def expiry_eyebrow(kind):
    return {"membership": "MEMBERSHIP", "safesport": "SAFESPORT", "background": "BACKGROUND SCREENING", "trial": "FREE TRIAL"}.get(kind, "MEMBERSHIP")

def _expiry_hero(left):
    """11.12–11.24: 7 days sun, tomorrow mango, today tangerine, expired cherry."""
    if left is None:
        return "sun", "Soon", 112
    if left < 0:
        return "cherry", "Expired", 84
    if left == 0:
        return "tangerine", "Today", 112
    if left == 1:
        return "mango", "Tomor-\nrow", 84
    return "sun", "%d days" % left, 112

def expiry_html(base, first, headline, sentence, url, org=ORG_NAME, eyebrow="MEMBERSHIP", left=None):
    hero, big, size = _expiry_hero(left)
    return render_v2(base, hero, eyebrow, big, headline, first, [sentence], org=org, cta=("Open Regulars", url),
                     footer_note="You can turn off these reminder emails in Notification settings.", big_size=size, preheader=sentence)

def _event_html(base, hero, eyebrow, big, headline, first, line, rows, cta, org, big_size=112):
    return render_v2(base, hero, eyebrow, big, headline, first, [line], org=org, rows=rows, cta=cta, big_size=big_size, preheader=line)

def schedule_change_html(base, first, sport_title, when, place, url, clock, org=ORG_NAME):
    """11.03 Schedule Change / Time."""
    rows = [("WHEN", when)] + ([("WHERE", place)] if place else []) + [("STATUS", "Updated")]
    return _event_html(base, "tangerine", "SCHEDULE CHANGE", _clock_figure(clock), "The time has changed.", first,
                       "%s has a new time." % sport_title, rows, ("View practice", url), org)

def lineup_registered_html(base, first, event, when, place, url, date_iso, org=ORG_NAME):
    """11.04 Lineup / Registered."""
    rows = [("WHEN", when)] + ([("WHERE", place)] if place else []) + [("STATUS", "Registered")]
    return _event_html(base, "lavender", "LINEUP", _month_figure(date_iso), "You're registered.", first,
                       "You're down for %s." % event, rows, ("View the event", url), org)

def event_reminder_html(base, first, event, when, place, url, date_iso, org=ORG_NAME):
    """11.05 Event Reminder / Upcoming."""
    rows = [("WHEN", when)] + ([("WHERE", place)] if place else []) + [("STATUS", "Registered")]
    return _event_html(base, "lavender", "EVENT REMINDER", _month_figure(date_iso), "%s is coming up." % event, first,
                       "Here's the event you're registered for.", rows, ("View the event", url), org)

def membership_confirmed_html(base, first, url, org=ORG_NAME):
    """11.06 Membership / Confirmed."""
    return render_v2(base, "sky", "MEMBERSHIP", "On file", "Your membership is confirmed.", first,
                     ["Your USA Water Polo membership is on file with %s." % org], org=org, cta=("Open Regulars", url), big_size=84)

def trial_started_html(base, first, url, days=14, org=ORG_NAME):
    """11.07 Trial / Started."""
    return render_v2(base, "aqua", "FREE TRIAL", "%d days" % days, "Your trial has started.", first,
                     ["Your first practices with %s are covered by the trial." % org], org=org, cta=("See the schedule", url), big_size=84)

def rsvp_not_going_html(base, first, sport_title, when, place, url, org=ORG_NAME):
    """11.10 RSVP / Not Going."""
    rows = [("WHEN", when)] + ([("WHERE", place)] if place else []) + [("STATUS", "Not going")]
    return _event_html(base, "cherry", "RSVP UPDATE", "Out", "You're marked not going.", first,
                       "Your RSVP for %s was updated." % sport_title, rows, ("Update your RSVP", url), org)

def rsvp_roster_html(base, first, sport_title, when, place, url, org=ORG_NAME):
    """11.11 Older RSVP / Roster."""
    rows = [("WHEN", when)] + ([("WHERE", place)] if place else []) + [("STATUS", "You're going")]
    return _event_html(base, "lime", "PRACTICE CONFIRMATION", "In", "You're on the roster.", first,
                       "You're signed up for %s with %s." % (sport_title, org), rows, ("View your RSVP", url), org)

def _month_figure(date_iso):
    import datetime as dt
    try:
        d = dt.date.fromisoformat(str(date_iso)[:10])
        return "%s %d" % (d.strftime("%b"), d.day)
    except ValueError:
        return str(date_iso or "")

def preview_catalog(base, org=ORG_NAME):
    """Sample of every 11 · Emails frame for a local render. None of these are delivered."""
    b = base.rstrip("/")
    home, practice, lineup = b + "/home", b + "/practices/6", b + "/lineup/1"
    link = b + "/practices/6"
    fri = "Friday, November 13 · 7:00–8:30 PM"
    west = "Westminster High School"
    out = [
        ("11.01", "Login Link", sign_in_html(base, "Eli", link, 15, org)),
        ("11.02", "Practice Cancelled", practice_cancelled_html(base, "Eli", fri, west, "The pool is closed.", practice, org, "2026-11-13")),
        ("11.03", "Schedule Change", schedule_change_html(base, "Eli", "Water Polo Practice", "Friday, November 13 · 6:30–8:00 PM", west, practice, "6:30 PM", org)),
        ("11.04", "Lineup Registered", lineup_registered_html(base, "Eli", "Sunday Cup", "Sunday, March 1 · 9:00 AM", "First Pool", lineup, "2027-03-01", org)),
        ("11.05", "Event Reminder", event_reminder_html(base, "Eli", "Sunday Cup", "Sunday, March 1 · 9:00 AM", "First Pool", lineup, "2027-03-01", org)),
        ("11.06", "Membership Confirmed", membership_confirmed_html(base, "Eli", home, org)),
        ("11.07", "Trial Started", trial_started_html(base, "Eli", home, 14, org)),
        ("11.08", "Practice Reminder", practice_reminder_html(base, "Eli", "", "Water Polo practice today at 7:00 PM, Marina High School.", "Water Polo", "7:00 – 8:30 PM", "Marina High School", practice, "Sign up for practice", b + "/practice-reminders/off/x", org, "7:00 PM")),
        ("11.09", "Signup Confirmation", practice_signup_html(base, "Eli", "", "You're signed up: Water Polo practice, Tue Nov 10 at 7:00 PM, Marina High School.", "Water Polo", "7:00 – 8:30 PM", "Marina High School", practice, "https://calendar.google.com", practice + "/event.ics", org, "7:00 PM", "Tuesday")),
        ("11.10", "RSVP Not Going", rsvp_not_going_html(base, "Eli", "Water Polo Practice", fri, west, practice, org)),
        ("11.11", "RSVP Roster", rsvp_roster_html(base, "Eli", "Water Polo Practice", fri, west, practice, org)),
    ]
    n = 12
    for kind, noun, verb in (("membership", "USA Water Polo membership", "expires"), ("safesport", "SafeSport training", "expires"), ("background", "background screening", "expires"), ("trial", "2-week USAWP trial", "ends")):
        lefts = (7, 1, 0, -1) if kind == "background" else (7, 1, 0)
        for left in lefts:
            title = {"membership": "Membership", "safesport": "SafeSport", "background": "Background screening", "trial": "Trial"}[kind]
            if left < 0:
                head, line = "%s expired" % title, "Your %s expired on 2026-11-01." % noun
            elif left == 0:
                head = ("%s ends today" if kind == "trial" else "%s expires today") % title
                line = "Your %s %s today (2026-11-10)." % (noun, verb)
            else:
                head = ("%s ending" if kind == "trial" else "%s expiring") % title
                line = "Your %s %s %s (2026-11-%d)." % (noun, verb, "tomorrow" if left == 1 else "in %d days" % left, 10 + left)
            out.append(("11.%02d" % n, head, expiry_html(base, "Eli", head, line, home, org, expiry_eyebrow(kind), left)))
            n += 1
    return out


def new_event_label(event_type):
    """'New social event', 'New tournament': a type that already names an event stands alone."""
    t = " ".join(str(event_type or "").split())
    if not t: return "New event"
    if t.lower() in ("tournament", "competition", "meet", "clinic", "trip", "camp", "fundraiser", "race", "regatta", "match", "game", "scrimmage", "party"):
        return "New " + t.lower()
    return "New %s event" % t.lower()

def lineup_new_html(base, first, title, figure, rows, image, url, unsub, org=ORG_NAME, note="", note_by="Note", hero="lavender", kind="New event", volunteer=""):
    """A new Lineup event. Emails 2.0 layout in the event's own color, the club named in the eyebrow, the event's
    banner on top of the body, and one-tap Going / Interested (the event page records the choice)."""
    sep = "&" if "?" in url else "?"
    return render_v2(base, hero if hero in HERO else "lavender", "%s\n%s" % (org.upper(), kind.upper()), figure, title, first,
                     ["%s is on the %s Lineup. Are you in?" % (title, org)], org=org, rows=rows,
                     note=(note_by, note) if note else None,
                     cta=("I'm going", url + sep + "rsvp=going"), calendar=[("Interested", url + sep + "rsvp=interested")] + ([("Volunteer", volunteer)] if volunteer else []) + [("View the event", url)],
                     fallback=url, footer_link=("Turn off Lineup emails", unsub),
                     preheader="%s · %s: %s" % (org, kind, title), image=image)

def poll_html(base, first, who, where, title, rows, url, unsub, org=ORG_NAME):
    """New poll in a chat. Emails 2.0 layout; the button opens the poll's vote page."""
    return render_v2(base, "lime", "NEW POLL", "Poll", title, first,
                     ["%s posted a poll in %s." % (who, where)], org=org, rows=rows, cta=("Answer the poll", url),
                     fallback=url, footer_link=("Turn off poll emails", unsub), preheader="%s posted a poll: %s" % (who, title))
