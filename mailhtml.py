"""Branded HTML mail. Outgoing messages include this HTML unless HTML_EMAILS_ENABLED=0."""
import html
import os

ORG_NAME = "Grunions Water Polo"
TAGLINE = "Built for the people who show up."
LIME = "#C4E65A"
INK = "#141614"
MUTED = "#5C6560"
PAGE = "#F3F4F0"
CARD = "#FFFFFF"
WASH = "#F4F8E8"
LINE = "#E4E7E0"
EYEBROW = "#5E6B24"
FONT = "'Space Grotesk','Plus Jakarta Sans',Arial,Helvetica,sans-serif"

def html_emails_enabled():
    return os.environ.get("HTML_EMAILS_ENABLED", "1") != "0"

def _e(value):
    return html.escape(str(value if value is not None else ""), quote=False)
def _a(value):
    return html.escape(str(value if value is not None else ""), quote=True)

def render_email(eyebrow, headline, paragraphs, logo_url, cta=None, rows=None, note=None, fallback=None, org=ORG_NAME):
    """Table layout, inline styles, light background. Dynamic text is escaped."""
    paras = "".join(
        '<p style="margin:0 0 14px;font-family:%s;font-size:16px;line-height:24px;color:%s;">%s</p>' % (FONT, INK, _e(p))
        for p in paragraphs)
    block = ""
    if rows:
        cells = []
        for i, (label, value) in enumerate(rows):
            border = "border-bottom:1px solid %s;" % LINE if i < len(rows) - 1 else ""
            cells.append(
                '<tr><td style="padding:10px 0;width:88px;%sfont-family:%s;font-size:12px;line-height:16px;letter-spacing:.06em;color:%s;vertical-align:top;">%s</td>'
                '<td style="padding:10px 0;%sfont-family:%s;font-size:16px;line-height:22px;font-weight:600;color:%s;">%s</td></tr>'
                % (border, FONT, MUTED, _e(label), border, FONT, INK, _e(value)))
        block += (
            '<table role="presentation" width="100%%" cellspacing="0" cellpadding="0" border="0" bgcolor="%s" '
            'style="margin:8px 0 22px;background:%s;border-radius:16px;border-left:4px solid %s;"><tr><td style="padding:8px 18px 8px;">'
            '<table role="presentation" width="100%%" cellspacing="0" cellpadding="0" border="0">%s</table>'
            '</td></tr></table>' % (WASH, WASH, LIME, "".join(cells)))
    if cta:
        label, url = cta
        block += (
            '<table role="presentation" cellspacing="0" cellpadding="0" border="0" style="margin:6px 0 18px;">'
            '<tr><td bgcolor="%s" style="border-radius:12px;background:%s;">'
            '<a href="%s" style="display:inline-block;padding:14px 22px;font-family:%s;font-size:16px;line-height:20px;font-weight:700;color:#ffffff;text-decoration:none;">%s</a>'
            '</td></tr></table>' % (INK, INK, _a(url), FONT, _e(label)))
    if note:
        title, body = note
        block += (
            '<table role="presentation" width="100%%" cellspacing="0" cellpadding="0" border="0" bgcolor="%s" '
            'style="margin:8px 0 18px;background:%s;border-radius:16px;"><tr><td style="padding:16px 18px;">'
            '<p style="margin:0 0 6px;font-family:%s;font-size:16px;line-height:22px;font-weight:700;color:%s;">%s</p>'
            '<p style="margin:0;font-family:%s;font-size:15px;line-height:22px;color:%s;">%s</p>'
            '</td></tr></table>' % (WASH, WASH, FONT, INK, _e(title), FONT, INK, _e(body)))
    if fallback:
        block += (
            '<p style="margin:8px 0 0;font-family:%s;font-size:14px;line-height:21px;color:%s;">Button not working? Copy this link into your browser:<br>'
            '<a href="%s" style="color:%s;word-break:break-all;">%s</a></p>'
            % (FONT, MUTED, _a(fallback), LIME, _e(fallback)))
    return (
        '<!doctype html><html lang="en"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width,initial-scale=1">'
        '<meta name="color-scheme" content="light"><meta name="supported-color-schemes" content="light">'
        '</head><body bgcolor="%s" style="margin:0;padding:0;background:%s;color:%s;">'
        '<table role="presentation" width="100%%" cellspacing="0" cellpadding="0" border="0" bgcolor="%s" style="background:%s;">'
        '<tr><td align="center" style="padding:28px 16px;">'
        '<table role="presentation" width="100%%" cellspacing="0" cellpadding="0" border="0" bgcolor="%s" '
        'style="max-width:560px;background:%s;border-radius:20px;border:1px solid %s;">'
        '<tr><td style="padding:28px 28px 18px;border-bottom:1px solid %s;">'
        '<img src="%s" alt="Regulars" width="220" height="43" style="display:block;border:0;outline:none;width:220px;height:auto;">'
        '</td></tr><tr><td style="padding:26px 28px 8px;">'
        '<p style="margin:0 0 10px;font-family:%s;font-size:12px;line-height:16px;font-weight:700;letter-spacing:.08em;color:%s;">%s</p>'
        '<h1 style="margin:0 0 16px;font-family:%s;font-size:32px;line-height:38px;font-weight:700;color:%s;">%s</h1>'
        '%s%s</td></tr>'
        '<tr><td bgcolor="#F7F8F5" style="padding:18px 28px 20px;background:#F7F8F5;border-top:1px solid %s;border-radius:0 0 20px 20px;">'
        '<p style="margin:0;font-family:%s;font-size:14px;line-height:21px;color:%s;">Sent by <strong>Regulars</strong> for %s.</p>'
        '</td></tr></table>'
        '<p style="margin:16px 0 0;font-family:%s;font-size:13px;line-height:18px;color:%s;">%s</p>'
        '</td></tr></table></body></html>'
        % (PAGE, PAGE, INK, PAGE, PAGE, CARD, CARD, LINE, LINE, _a(logo_url),
           FONT, EYEBROW, _e(eyebrow), FONT, INK, _e(headline), paras, block,
           LINE, FONT, MUTED, _e(org), FONT, MUTED, _e(TAGLINE)))

def logo_url(base):
    return base.rstrip("/") + "/static/email-lockup.png"

def sign_in_html(base, first, link, minutes, org=ORG_NAME):
    return render_email(
        "SECURE SIGN-IN", "Sign in",
        ["Hi %s," % first, "Use the button below to sign in to %s on Regulars." % org],
        logo_url(base), cta=("Sign in securely", link),
        note=("For your security", "This link works once and expires in %d minutes. Never share it with anyone." % minutes),
        fallback=link, org=org)

def practice_cancelled_html(base, first, when, place, reason, url, org=ORG_NAME):
    rows = [("WHEN", when)]
    if place: rows.append(("WHERE", place))
    rows.append(("STATUS", "Cancelled"))
    paras = ["Hi %s," % first, "This session has been cancelled."]
    if reason: paras.append(reason)
    return render_email("SCHEDULE CHANGE", "Practice cancelled", paras, logo_url(base),
                        cta=("View the schedule", url), rows=rows, org=org)

def expiry_eyebrow(kind):
    return {"membership": "MEMBERSHIP", "safesport": "SAFESPORT", "background": "BACKGROUND SCREENING", "trial": "FREE TRIAL"}.get(kind, "MEMBERSHIP")
def expiry_html(base, first, headline, sentence, url, org=ORG_NAME, eyebrow="MEMBERSHIP"):
    return render_email(
        eyebrow, headline,
        ["Hi %s," % first, sentence, "You can turn off these reminder emails in Notification settings."],
        logo_url(base), cta=("Open Regulars", url), org=org)

def preview_catalog(base, org=ORG_NAME):
    """Sample messages for a local render. None of these are delivered."""
    home = base.rstrip("/") + "/home"
    practice = base.rstrip("/") + "/practices/preview"
    link = "https://example.com/auth/preview-not-a-link"
    when = "Friday, November 13 · 7:00–8:30 PM"
    where = "Westminster High School"
    return [
        ("sign-in", "Sign in", sign_in_html(base, "Eli", link, 15, org)),
        ("practice-rsvp", "Practice confirmation", render_email(
            "PRACTICE CONFIRMATION", "You're on the roster.",
            ["Hi Eli,", "You're signed up for Water Polo Practice with %s." % org],
            logo_url(base), cta=("View your RSVP", practice),
            rows=[("WHEN", when), ("WHERE", where), ("STATUS", "You're going")], org=org)),
        ("rsvp-change", "RSVP change", render_email(
            "RSVP UPDATE", "You're marked not going.",
            ["Hi Eli,", "Your RSVP for Water Polo Practice was updated."],
            logo_url(base), cta=("Update your RSVP", practice),
            rows=[("WHEN", when), ("WHERE", where), ("STATUS", "Not going")], org=org)),
        ("practice-reminder", "Practice reminder", render_email(
            "PRACTICE REMINDER", "See you at the pool.",
            ["Hi Eli,", "Water Polo Practice is coming up."],
            logo_url(base), cta=("View practice", practice),
            rows=[("WHEN", when), ("WHERE", where), ("STATUS", "You're going")], org=org)),
        ("practice-cancelled", "Practice cancelled", practice_cancelled_html(
            base, "Eli", when, where, "The pool is closed.", practice, org)),
        ("schedule-change", "Schedule change", render_email(
            "SCHEDULE CHANGE", "The time has changed.",
            ["Hi Eli,", "Water Polo Practice has a new time."],
            logo_url(base), cta=("View practice", practice),
            rows=[("WHEN", "Friday, November 13 · 6:30–8:00 PM"), ("WHERE", where), ("STATUS", "Updated")], org=org)),
        ("lineup-confirm", "Lineup confirmation", render_email(
            "LINEUP", "You're registered.",
            ["Hi Eli,", "You're down for Sunday Cup."],
            logo_url(base), cta=("View the event", base.rstrip("/") + "/lineup/preview"),
            rows=[("WHEN", "Sunday, March 1 · 9:00 AM"), ("WHERE", "First Pool"), ("STATUS", "Registered")], org=org)),
        ("event-reminder", "Event reminder", render_email(
            "EVENT REMINDER", "Sunday Cup is coming up.",
            ["Hi Eli,", "Here's the event you're registered for."],
            logo_url(base), cta=("View the event", base.rstrip("/") + "/lineup/preview"),
            rows=[("WHEN", "Sunday, March 1 · 9:00 AM"), ("WHERE", "First Pool"), ("STATUS", "Registered")], org=org)),
        ("membership", "Membership", render_email(
            "MEMBERSHIP", "Your membership is confirmed.",
            ["Hi Eli,", "Your USA Water Polo membership is on file with %s." % org],
            logo_url(base), cta=("Open Regulars", home), org=org)),
        ("trial-start", "Free trial", render_email(
            "FREE TRIAL", "Your trial has started.",
            ["Hi Eli,", "Your first practices with %s are covered by the trial." % org],
            logo_url(base), cta=("See the schedule", home), org=org)),
        ("trial-end", "Trial ending", expiry_html(
            base, "Eli", "Your trial ends today", "Your 2-week USAWP trial ends today.", home, org)),
        ("expiry", "Expiry reminder", expiry_html(
            base, "Eli", "Membership expiring", "Your USA Water Polo membership expires in 7 days.", home, org)),
    ]
