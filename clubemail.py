"""Club email (Figma 62 · E): build from a template, preview, send, and see opens.

Schema is additive. Nothing here runs on import. Every send goes through app.send_email, so if
SMTP is not set up the send stops with a clear error instead of pretending it went out.
"""
import datetime as dt
import html
import json
import secrets

STATUSES = ("draft", "scheduled", "sending", "sent")
TONES = {"sun": "#FFC61A", "sky": "#7CC8F4", "tangerine": "#FF5A1F", "lime": "#C8FF3C", "lavender": "#A89CFF",
         "aqua": "#2EE6C8", "mango": "#FF9F1C", "bubblegum": "#FF5FB8"}
INK, CARBON, GRAPHITE, PAPER, SMOKE, LIME = "#0B0B0C", "#17181A", "#24262A", "#F6F4EF", "#8B8F93", "#C8FF3C"
FONT = "'Space Grotesk','Plus Jakarta Sans',Arial,Helvetica,sans-serif"

BLOCK_KINDS = (
    ("header", "Header", "Club logo + name"),
    ("text", "Text", "A paragraph. {first name} fills in."),
    ("practice", "Practice", "When and where, from the schedule"),
    ("button", "Button", "One link"),
    ("footer", "Footer", "Unsubscribe · club address"),
)

TEMPLATES = (
    ("schedule_change", "Schedule change", "sun", "SCHEDULE CHANGE", "The schedule has changed.",
     "Hi {first name}, practice is moving. Here are the new details.", "See the schedule", "/practices"),
    ("practice_cancelled", "Practice cancelled", "tangerine", "CANCELLED", "Practice is cancelled.",
     "Hi {first name}, we have to cancel this one. See you at the next practice.", "See the schedule", "/practices"),
    ("welcome", "Welcome a new member", "lime", "WELCOME", "Welcome to the club.",
     "Hi {first name}, we're glad you're here. Here's how to find practices and sign up.", "Open Regulars", "/practices"),
    ("dues", "Dues reminder", "lavender", "MEMBERSHIP", "Dues are due.",
     "Hi {first name}, a quick reminder that membership dues are due. Thank you for keeping the club going.", "See plans", "/profile"),
)


def ensure(d):
    d.execute("""CREATE TABLE IF NOT EXISTS club_emails(
        id INTEGER PRIMARY KEY, status TEXT NOT NULL DEFAULT 'draft', audience TEXT NOT NULL DEFAULT 'everyone',
        template TEXT NOT NULL DEFAULT '', subject TEXT NOT NULL DEFAULT '', blocks TEXT NOT NULL DEFAULT '[]',
        created_by INTEGER, created_at TEXT DEFAULT CURRENT_TIMESTAMP, updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
        scheduled_for TEXT, sent_at TEXT, sent_count INTEGER NOT NULL DEFAULT 0, error TEXT NOT NULL DEFAULT '')""")
    d.execute("""CREATE TABLE IF NOT EXISTS club_email_recipients(
        id INTEGER PRIMARY KEY, email_id INTEGER NOT NULL, member_id INTEGER, address TEXT NOT NULL,
        token TEXT NOT NULL UNIQUE, sent_at TEXT, opened_at TEXT, clicked_at TEXT, bounced TEXT NOT NULL DEFAULT '')""")
    cols = {r[1] for r in d.execute("PRAGMA table_info(members)")}
    if "news_opt_out" not in cols:
        d.execute("ALTER TABLE members ADD COLUMN news_opt_out INTEGER DEFAULT 0")


def _now():
    return dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")


def template_blocks(key):
    for k, name, tone, kicker, title, body, button, url in TEMPLATES:
        if k == key:
            return name, [
                {"kind": "header", "tone": tone, "kicker": kicker, "big": "", "title": title},
                {"kind": "text", "body": body},
                {"kind": "practice", "practice_id": None},
                {"kind": "button", "label": button, "url": url},
                {"kind": "footer"},
            ]
    return "", [{"kind": "header", "tone": "lime", "kicker": "NEWS", "big": "", "title": "News from the club."},
                {"kind": "text", "body": "Hi {first name},"}, {"kind": "footer"}]


def blocks_of(row):
    try:
        out = json.loads(row["blocks"] or "[]")
        return out if isinstance(out, list) else []
    except (TypeError, ValueError):
        return []


def create(d, member_id, template=""):
    name, blocks = template_blocks(template)
    subject = name if name else ""
    return d.execute("INSERT INTO club_emails(status, audience, template, subject, blocks, created_by) VALUES('draft','everyone',?,?,?,?)",
                     (template, subject, json.dumps(blocks), member_id)).lastrowid


def get(d, eid):
    return d.execute("SELECT * FROM club_emails WHERE id=?", (eid,)).fetchone()


def save(d, eid, **fields):
    allowed = {"audience", "subject", "blocks", "template", "scheduled_for", "status"}
    sets = [(k, v) for k, v in fields.items() if k in allowed]
    if not sets:
        return
    d.execute("UPDATE club_emails SET %s, updated_at=? WHERE id=?" % ", ".join("%s=?" % k for k, _v in sets),
              [v for _k, v in sets] + [_now(), eid])


def duplicate(d, eid, member_id):
    row = get(d, eid)
    return d.execute("INSERT INTO club_emails(status, audience, template, subject, blocks, created_by) VALUES('draft',?,?,?,?,?)",
                     (row["audience"], row["template"], row["subject"], row["blocks"], member_id)).lastrowid


# --- Audiences ---------------------------------------------------------------

def _people(d):
    return d.execute("""SELECT * FROM members WHERE COALESCE(role,'')!='system' AND email IS NOT NULL AND email!=''
        AND COALESCE(news_opt_out,0)=0 ORDER BY last, first""").fetchall()


def audiences(d, clearance_ok, sport_rows, next_practice, paying):
    """[(key, label, [member rows])]. clearance_ok(member)->bool, paying(member)->bool."""
    people = _people(d)
    out = [("everyone", "Everyone", people)]
    for sport in sport_rows:
        ids = {r[0] for r in d.execute("SELECT member_id FROM member_sports WHERE sport=?", (sport["slug"],))} if _has(d, "member_sports") else set()
        if ids:
            out.append(("sport:%s" % sport["slug"], sport["name"], [m for m in people if m["id"] in ids]))
    out.append(("members", "Members", [m for m in people if paying(m)]))
    out.append(("notcleared", "Not cleared", [m for m in people if not clearance_ok(m)]))
    if next_practice:
        going = {r[0] for r in d.execute("SELECT member_id FROM rsvps WHERE practice_id=? AND going=1", (next_practice["id"],))}
        out.append(("going:%d" % next_practice["id"], "Going %s" % next_practice["label"], [m for m in people if m["id"] in going]))
    return out


def _has(d, table):
    return bool(d.execute("SELECT 1 FROM sqlite_master WHERE type='table' AND name=?", (table,)).fetchone())


# --- Rendering (2.0 email: colored hero, dark body) ------------------------------

def _e(v):
    return html.escape(str(v if v is not None else ""), quote=False)


def _a(v):
    return html.escape(str(v if v is not None else ""), quote=True)


def fill(text, first):
    return (text or "").replace("{first name}", first or "there").replace("{first_name}", first or "there")


def render(blocks, first="Eli", practice_lookup=None, link=lambda url: url, pixel="", unsub="", club="", address="", dark=True, logo=""):
    """Table layout, inline styles. Dynamic text is escaped. link() wraps URLs for click tracking."""
    bg, body_bg, text, muted, box = (INK, CARBON, PAPER, SMOKE, GRAPHITE) if dark else ("#F3F1EB", "#FFFFFF", INK, "#6A6E73", "#F3F1EB")
    parts = []
    hero_done = False
    for b in blocks:
        kind = b.get("kind")
        if kind == "header" and not hero_done:
            hero_done = True
            tone = TONES.get(b.get("tone") or "lime", LIME)
            big = ('<div style="margin:18px 0 0;font-family:%s;font-size:72px;line-height:72px;font-weight:700;letter-spacing:-3px;color:%s;">%s</div>' % (FONT, INK, _e(b["big"]))) if b.get("big") else ""
            parts.append(
                '<tr><td bgcolor="%s" style="background:%s;padding:24px 24px 26px;border-radius:24px 24px 0 0;">'
                '<table role="presentation" width="100%%" cellspacing="0" cellpadding="0" border="0"><tr>'
                '<td style="font-family:%s;font-size:17px;font-weight:700;color:%s;">%s%s</td>'
                '<td align="right" style="font-family:%s;font-size:11px;font-weight:700;letter-spacing:1px;color:%s;">%s</td></tr></table>'
                '%s<div style="margin:%s 0 0;font-family:%s;font-size:26px;line-height:30px;font-weight:700;letter-spacing:-.5px;color:%s;">%s</div>'
                '</td></tr>' % (tone, tone, FONT, INK, ('<img src="%s" alt="" width="28" height="11" style="vertical-align:middle;margin-right:6px;border:0">' % _a(logo)) if logo else "",
                                _e(club or "regulars"), FONT, INK, _e(b.get("kicker") or ""), big, "10px" if big else "28px", FONT, INK, _e(b.get("title") or "")))
            parts.append('<tr><td bgcolor="%s" style="background:%s;padding:22px 24px 6px;">' % (body_bg, body_bg))
        elif kind == "text":
            for para in fill(b.get("body") or "", first).split("\n"):
                if para.strip():
                    parts.append('<p style="margin:0 0 14px;font-family:%s;font-size:16px;line-height:24px;color:%s;">%s</p>' % (FONT, text, _e(para)))
        elif kind == "practice":
            p = practice_lookup(b.get("practice_id")) if practice_lookup and b.get("practice_id") else None
            if p:
                for label, value in (("WHEN", p.get("when")), ("WHERE", p.get("where")), ("STATUS", p.get("status"))):
                    if value:
                        parts.append('<table role="presentation" width="100%%" cellspacing="0" cellpadding="0" border="0" style="margin:0 0 8px;"><tr>'
                                     '<td bgcolor="%s" style="background:%s;border-radius:16px;padding:12px 16px;">'
                                     '<div style="font-family:%s;font-size:10px;font-weight:700;letter-spacing:1px;color:%s;">%s</div>'
                                     '<div style="margin-top:4px;font-family:%s;font-size:16px;line-height:22px;font-weight:700;color:%s;">%s</div>'
                                     '</td></tr></table>' % (box, box, FONT, muted, label, FONT, text, _e(value)))
        elif kind == "button" and b.get("label") and b.get("url"):
            parts.append('<table role="presentation" width="100%%" cellspacing="0" cellpadding="0" border="0" style="margin:10px 0 16px;"><tr>'
                         '<td align="center" bgcolor="%s" style="background:%s;border-radius:999px;">'
                         '<a href="%s" style="display:block;padding:15px 22px;font-family:%s;font-size:16px;font-weight:700;color:%s;text-decoration:none;">%s</a>'
                         '</td></tr></table>' % (LIME, LIME, _a(link(b["url"])), FONT, INK, _e(b["label"])))
        elif kind == "footer":
            parts.append('</td></tr><tr><td bgcolor="%s" style="background:%s;padding:16px 24px 22px;border-radius:0 0 24px 24px;">'
                         '<p style="margin:0;font-family:%s;font-size:12px;line-height:18px;color:%s;">%s%s%s</p>' % (
                             body_bg, body_bg, FONT, muted, _e(club or "Your club"), (" · " + _e(address)) if address else "",
                             (' · <a href="%s" style="color:%s;text-decoration:underline;">Unsubscribe</a>' % (_a(unsub), muted)) if unsub else " · Unsubscribe"))
    if not hero_done:
        parts.insert(0, '<tr><td bgcolor="%s" style="background:%s;padding:22px 24px 6px;border-radius:24px 24px 0 0;">' % (body_bg, body_bg))
    parts.append('</td></tr>')
    if pixel:
        parts.append('<tr><td><img src="%s" width="1" height="1" alt="" style="display:block;border:0;width:1px;height:1px;"></td></tr>' % _a(pixel))
    return ('<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
            '<meta name="color-scheme" content="%s"></head><body bgcolor="%s" style="margin:0;padding:0;background:%s;">'
            '<table role="presentation" width="100%%" cellspacing="0" cellpadding="0" border="0" bgcolor="%s" style="background:%s;"><tr><td align="center" style="padding:20px 12px;">'
            '<table role="presentation" width="100%%" cellspacing="0" cellpadding="0" border="0" style="max-width:560px;">%s</table>'
            '</td></tr></table></body></html>') % ("dark" if dark else "light", bg, bg, bg, bg, "".join(parts))


def plain_text(blocks, first="", practice_lookup=None):
    lines = []
    for b in blocks:
        if b.get("kind") == "header" and b.get("title"):
            lines.append(b["title"])
        elif b.get("kind") == "text":
            lines.append(fill(b.get("body") or "", first))
        elif b.get("kind") == "practice":
            p = practice_lookup(b.get("practice_id")) if practice_lookup and b.get("practice_id") else None
            if p:
                lines.append("\n".join(x for x in (p.get("when"), p.get("where")) if x))
        elif b.get("kind") == "button" and b.get("url"):
            lines.append("%s: %s" % (b.get("label") or "Link", b["url"]))
    return "\n\n".join(x for x in lines if x)


def block_summary(b, practice_lookup=None):
    k = b.get("kind")
    if k == "header":
        return b.get("title") or "Club logo + name"
    if k == "text":
        return (b.get("body") or "Empty")[:80]
    if k == "practice":
        p = practice_lookup(b.get("practice_id")) if practice_lookup and b.get("practice_id") else None
        return " · ".join(x for x in ((p or {}).get("when"), (p or {}).get("where")) if x) or "Pick a practice"
    if k == "button":
        return b.get("label") or "Add a label"
    if k == "footer":
        return "Unsubscribe · club address"
    return ""


# --- Sending and tracking -------------------------------------------------------------

def stage_recipients(d, eid, members):
    """One row per address with its own token. Rerunning skips addresses already staged."""
    have = {r[0] for r in d.execute("SELECT address FROM club_email_recipients WHERE email_id=?", (eid,))}
    for m in members:
        addr = (m["email"] or "").strip().lower()
        if not addr or addr in have:
            continue
        have.add(addr)
        d.execute("INSERT INTO club_email_recipients(email_id, member_id, address, token) VALUES(?,?,?,?)",
                  (eid, m["id"], addr, secrets.token_urlsafe(18)))


def stats(d, eid):
    row = d.execute("""SELECT COUNT(*) AS n, SUM(CASE WHEN sent_at IS NOT NULL THEN 1 ELSE 0 END) AS sent,
        SUM(CASE WHEN opened_at IS NOT NULL THEN 1 ELSE 0 END) AS opened, SUM(CASE WHEN clicked_at IS NOT NULL THEN 1 ELSE 0 END) AS clicked,
        SUM(CASE WHEN bounced!='' THEN 1 ELSE 0 END) AS bounced FROM club_email_recipients WHERE email_id=?""", (eid,)).fetchone()
    sent = row["sent"] or 0
    return {"staged": row["n"] or 0, "sent": sent, "opened": row["opened"] or 0, "clicked": row["clicked"] or 0, "bounced": row["bounced"] or 0,
            "rate": int(round(100.0 * (row["opened"] or 0) / sent)) if sent else 0}


def mark(d, token, what):
    col = {"open": "opened_at", "click": "clicked_at"}[what]
    row = d.execute("SELECT * FROM club_email_recipients WHERE token=?", (token,)).fetchone()
    if not row:
        return None
    if not row[col]:
        d.execute("UPDATE club_email_recipients SET %s=? WHERE id=?" % col, (_now(), row["id"]))
    if what == "click" and not row["opened_at"]:
        d.execute("UPDATE club_email_recipients SET opened_at=? WHERE id=?", (_now(), row["id"]))
    return row
