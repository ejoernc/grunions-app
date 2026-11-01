"""Grunions Water Polo team app prototype: member login, team chat, admin check-in tools. Flask + SQLite."""
import csv, io, os, re, sqlite3, secrets, hashlib, datetime as dt, functools, base64, threading
import json, urllib.request, urllib.parse, urllib.error
import gspread
from google.oauth2.service_account import Credentials
from zoneinfo import ZoneInfo
import qrcode, qrcode.image.svg
from markupsafe import Markup, escape
import lineupfeed
import sports
import ui
from ui import T
from flask import (Flask, request, redirect, url_for, session, g, render_template_string, Response, abort, flash, jsonify, send_from_directory)

DATA_DIR = os.environ.get("DATA_DIR") or os.path.dirname(os.path.abspath(__file__))  # persistent disk in production
os.makedirs(DATA_DIR, exist_ok=True)
DB = os.environ.get("GRUNIONS_DB", os.path.join(DATA_DIR, "grunions.db"))
PUBLIC_URL = os.environ.get("PUBLIC_URL")
ADMIN_EMAILS = {e.strip().lower() for e in os.environ.get("ADMIN_EMAIL", "").split(",") if e.strip()}  # bootstrap admins (comma-separated)
ADMIN_EMAIL = next(iter(sorted(ADMIN_EMAILS)), "")
LINK_MINUTES = int(os.environ.get("LINK_MINUTES", 15))
SMTP = {k: os.environ.get(k) for k in ("SMTP_HOST", "SMTP_PORT", "SMTP_USER", "SMTP_PASSWORD", "MAIL_FROM")}
EXPIRING_DAYS = int(os.environ.get("EXPIRING_DAYS", 30))
VERIFY_WEBHOOK_URL = os.environ.get("VERIFY_WEBHOOK_URL")  # outbound: new verification requests are POSTed here
VERIFY_WEBHOOK_KEY = os.environ.get("VERIFY_WEBHOOK_KEY")  # if set, Authorization: Bearer <key> (unless HEADER overrides)
VERIFY_WEBHOOK_HEADER = os.environ.get("VERIFY_WEBHOOK_HEADER")  # if set, this header carries the raw key
BOT_API_KEY = os.environ.get("BOT_API_KEY")  # inbound: bearer token for /api/verify-requests
CRON_KEY = os.environ.get("CRON_KEY")  # lets a scheduler call /api/expiring without a session
DEV_SHOW_LINKS = os.environ.get("DEV_SHOW_LINKS", "0") == "1"  # local testing only: show magic link on screen
UPLOADS = os.environ.get("GRUNIONS_UPLOADS", os.path.join(DATA_DIR, "uploads"))
MAX_UPLOAD = 8 * 1024 * 1024
REACTIONS = ["👍", "👎", "❤️", "😂", "🎉", "😮", "🔥", "👀", "🙏", "🥲", "💯"]
app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = MAX_UPLOAD + 64 * 1024
app.secret_key = os.environ.get("SECRET_KEY") or secrets.token_hex(32)
app.config.update(SESSION_COOKIE_HTTPONLY=True, SESSION_COOKIE_SAMESITE="Lax",
                  SESSION_COOKIE_SECURE=os.environ.get("SECURE_COOKIES", "1" if (PUBLIC_URL or "").startswith("https://") else "0") == "1",
                  PERMANENT_SESSION_LIFETIME=dt.timedelta(days=60))
if os.environ.get("BEHIND_PROXY", "1" if PUBLIC_URL else "0") == "1":  # Render etc. terminate HTTPS in front of us
    from werkzeug.middleware.proxy_fix import ProxyFix
    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1)

# The team is in California. Render's clock is UTC, so date.today() flips at 5pm PDT / 4pm PST
# and hides that evening's practice. All calendar dates and practice times are Pacific wall time.
# tzdata (the package) supplies America/Los_Angeles when the slim image has no system zoneinfo.
try:
    PT = ZoneInfo("America/Los_Angeles")
except Exception:
    import tzdata  # noqa: F401  registers the PyPI fallback
    PT = ZoneInfo("America/Los_Angeles")
def now_pt():
    return dt.datetime.now(PT)
def as_pt(when=None):
    """Pacific time. A naive input is a Pacific wall time; an aware input is converted."""
    if when is None: when = now_pt()
    if when.tzinfo is None: return when.replace(tzinfo=PT)
    return when.astimezone(PT)
def today_pt():
    return as_pt().date()
def wall_pt(when=None):
    return as_pt(when).replace(tzinfo=None)
def stamp_pt(timespec="seconds"):
    return wall_pt().isoformat(timespec=timespec)
def upcoming_bounds(now=None):
    """A practice stays on the schedule through its end minute (7:00–8:30 stays up at 8:30)."""
    n = wall_pt(now)
    day = n.date().isoformat()
    return (day, day, "%02d:%02d" % (n.hour, n.minute))
def upcoming_where(alias=""):
    p = (alias + ".") if alias else ""
    return "(%sdate > ? OR (%sdate = ? AND COALESCE(%send, '20:30') >= ?))" % (p, p, p)

SCHEMA = """
CREATE TABLE IF NOT EXISTS members(id INTEGER PRIMARY KEY, first TEXT NOT NULL, last TEXT NOT NULL,
  email TEXT NOT NULL UNIQUE, phone TEXT, created TEXT DEFAULT CURRENT_TIMESTAMP, is_admin INTEGER DEFAULT 0,
  usawp_status TEXT DEFAULT 'unknown', usawp_raw TEXT, usawp_number TEXT, usawp_valid_until TEXT, usawp_updated TEXT,
  preferred_first TEXT, trial_acknowledged_at TEXT, joined INTEGER DEFAULT 0, require_background INTEGER DEFAULT 0, photo TEXT);
CREATE TABLE IF NOT EXISTS checkins(id INTEGER PRIMARY KEY, member_id INTEGER REFERENCES members(id),
  practice_date TEXT NOT NULL, location TEXT, at TEXT DEFAULT CURRENT_TIMESTAMP, UNIQUE(member_id, practice_date));
CREATE TABLE IF NOT EXISTS login_tokens(token_hash TEXT PRIMARY KEY, member_id INTEGER, expires TEXT, used INTEGER DEFAULT 0);
CREATE TABLE IF NOT EXISTS requirements(id INTEGER PRIMARY KEY, name TEXT NOT NULL, applies_to TEXT DEFAULT 'all',
  keywords TEXT, expires INTEGER DEFAULT 1, active INTEGER DEFAULT 1);
CREATE TABLE IF NOT EXISTS member_reqs(member_id INTEGER, req_id INTEGER, completed_on TEXT, expires_on TEXT, source TEXT, by TEXT, at TEXT,
  PRIMARY KEY(member_id, req_id));
CREATE TABLE IF NOT EXISTS practices(id INTEGER PRIMARY KEY, date TEXT NOT NULL, start TEXT DEFAULT '19:00', end TEXT DEFAULT '20:30',
  location TEXT, address TEXT, note TEXT, cancelled INTEGER DEFAULT 0, cancel_reason TEXT, image TEXT,
  lat REAL, lng REAL, social_lat REAL, social_lng REAL, series_id INTEGER, series_detached INTEGER DEFAULT 0, skipped INTEGER DEFAULT 0, UNIQUE(date, location));
CREATE TABLE IF NOT EXISTS practice_series(id INTEGER PRIMARY KEY, weekdays TEXT NOT NULL, start TEXT NOT NULL, end TEXT NOT NULL,
  location TEXT NOT NULL, start_date TEXT NOT NULL, end_date TEXT);
CREATE TABLE IF NOT EXISTS series_coaches(series_id INTEGER NOT NULL, member_id INTEGER NOT NULL, is_lead INTEGER NOT NULL DEFAULT 0, PRIMARY KEY(series_id, member_id));
CREATE TABLE IF NOT EXISTS series_skips(series_id INTEGER NOT NULL, date TEXT NOT NULL, PRIMARY KEY(series_id, date));
CREATE TABLE IF NOT EXISTS rsvps(practice_id INTEGER, member_id INTEGER, going INTEGER, at TEXT DEFAULT CURRENT_TIMESTAMP, PRIMARY KEY(practice_id, member_id));
CREATE TABLE IF NOT EXISTS practice_coaches(practice_id INTEGER NOT NULL, member_id INTEGER NOT NULL, PRIMARY KEY(practice_id, member_id));
CREATE TABLE IF NOT EXISTS social_joins(practice_id INTEGER NOT NULL, member_id INTEGER NOT NULL, PRIMARY KEY(practice_id, member_id));
CREATE TABLE IF NOT EXISTS coaching_list(member_id INTEGER PRIMARY KEY, source TEXT NOT NULL DEFAULT 'manual', at TEXT);
CREATE TABLE IF NOT EXISTS referee_list(member_id INTEGER PRIMARY KEY, source TEXT NOT NULL DEFAULT 'manual', at TEXT);
CREATE TABLE IF NOT EXISTS verify_requests(id INTEGER PRIMARY KEY, member_id INTEGER REFERENCES members(id), name TEXT, email TEXT,
  member_number TEXT, requested_by TEXT, member_submitted INTEGER DEFAULT 0, status TEXT DEFAULT 'pending', created TEXT, answered TEXT, result TEXT, note TEXT, webhook TEXT);
CREATE TABLE IF NOT EXISTS reactions(message_id INTEGER, member_id INTEGER, emoji TEXT, PRIMARY KEY(message_id, member_id, emoji));
CREATE TABLE IF NOT EXISTS notices(id INTEGER PRIMARY KEY, member_id INTEGER REFERENCES members(id), body TEXT, at TEXT DEFAULT CURRENT_TIMESTAMP, seen INTEGER DEFAULT 0);
CREATE TABLE IF NOT EXISTS name_audits(id INTEGER PRIMARY KEY, member_id INTEGER NOT NULL, actor_id INTEGER, actor TEXT NOT NULL, old_name TEXT NOT NULL, new_name TEXT NOT NULL, at TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS usawp_submits(id INTEGER PRIMARY KEY, member_id INTEGER, at TEXT);
CREATE TABLE IF NOT EXISTS messages(id INTEGER PRIMARY KEY, member_id INTEGER REFERENCES members(id), body TEXT NOT NULL,
  announcement INTEGER DEFAULT 0, at TEXT DEFAULT CURRENT_TIMESTAMP, channel TEXT DEFAULT 'team', image TEXT,
  edited_at TEXT, deleted INTEGER DEFAULT 0, reply_to INTEGER);
CREATE TABLE IF NOT EXISTS push_subscriptions(id INTEGER PRIMARY KEY, member_id INTEGER REFERENCES members(id),
  endpoint TEXT NOT NULL UNIQUE, p256dh TEXT NOT NULL, auth TEXT NOT NULL, created TEXT);
CREATE TABLE IF NOT EXISTS sent_notices(member_id INTEGER, kind TEXT, sent_at TEXT, PRIMARY KEY(member_id, kind));
CREATE TABLE IF NOT EXISTS job_locks(name TEXT PRIMARY KEY, locked_at TEXT);
CREATE TABLE IF NOT EXISTS sheet_sync(id INTEGER PRIMARY KEY, at TEXT, ok INTEGER, detail TEXT);
CREATE TABLE IF NOT EXISTS chat_reads(member_id INTEGER NOT NULL, channel TEXT NOT NULL, last_read INTEGER NOT NULL DEFAULT 0, PRIMARY KEY(member_id, channel));
CREATE TABLE IF NOT EXISTS practice_notices(practice_id INTEGER NOT NULL, member_id INTEGER NOT NULL, kind TEXT NOT NULL, seen_at TEXT, PRIMARY KEY(practice_id, member_id, kind));
CREATE TABLE IF NOT EXISTS lineup_events(id INTEGER PRIMARY KEY, kind TEXT NOT NULL, title TEXT NOT NULL, date TEXT NOT NULL,
  end_date TEXT, city TEXT, venue TEXT, start TEXT, location TEXT, description TEXT, link TEXT, stage TEXT, hosting TEXT);
CREATE TABLE IF NOT EXISTS lineup_rsvps(event_id INTEGER NOT NULL, member_id INTEGER NOT NULL, going INTEGER NOT NULL,
  at TEXT DEFAULT CURRENT_TIMESTAMP, PRIMARY KEY(event_id, member_id));
"""
def db():
    if "db" not in g:
        g.db = sqlite3.connect(DB); g.db.row_factory = sqlite3.Row; g.db.executescript(SCHEMA)
        migrate_members(g.db)
        migrate_practice_coaches(g.db)
        migrate_practices(g.db)
        migrate_social_joins(g.db)
        migrate_referee_list(g.db)
        migrate_verify_requests(g.db)
        if not g.db.execute("SELECT 1 FROM requirements").fetchone():
            g.db.executemany("INSERT INTO requirements(name,applies_to,keywords,expires) VALUES(?,?,?,?)", DEFAULT_REQS); g.db.commit()
        drop_club_waiver(g.db)
        ensure_referee_req(g.db)
        migrate_messages(g.db)
        migrate_lineup(g.db)
        migrate_series(g.db)
        drop_bot_verify_messages(g.db)
        seed_chat_reads(g.db)
        expire_sweep(g.db)
        for e in ADMIN_EMAILS: g.db.execute("UPDATE members SET is_admin=1 WHERE email=?", (e,))
        g.db.commit()
    return g.db
def migrate_verify_requests(d):
    """Remember whether the member submitted the request. Existing rows stay admin-requested."""
    cols = [r[1] for r in d.execute("PRAGMA table_info(verify_requests)")]
    if "member_submitted" not in cols:
        d.execute("ALTER TABLE verify_requests ADD COLUMN member_submitted INTEGER DEFAULT 0")
def migrate_referee_list(d):
    """Referee list mirrors the coaching list. Existing members are not added."""
    d.execute("""CREATE TABLE IF NOT EXISTS referee_list(
        member_id INTEGER PRIMARY KEY, source TEXT NOT NULL DEFAULT 'manual', at TEXT)""")
def migrate_practices(d):
    """Store a cancellation reason, an optional social, and a coach message. Existing practices stay unchanged."""
    cols = [r[1] for r in d.execute("PRAGMA table_info(practices)")]
    for c, t in (("cancel_reason", "TEXT"), ("social_kind", "TEXT"), ("social_place", "TEXT"),
                 ("social_address", "TEXT"), ("social_time", "TEXT"), ("social_note", "TEXT"),
                 ("coach_note", "TEXT"), ("coach_note_by", "TEXT"), ("coach_note_at", "TEXT"),
                 ("image", "TEXT"), ("lat", "REAL"), ("lng", "REAL"), ("social_lat", "REAL"), ("social_lng", "REAL"),
                 ("address", "TEXT"), ("coaching_plan", "TEXT"),
                 ("series_id", "INTEGER"), ("series_detached", "INTEGER DEFAULT 0"), ("skipped", "INTEGER DEFAULT 0"),
                 ("activity_type", "TEXT"), ("sport", "TEXT"), ("title", "TEXT"), ("skill_levels", "TEXT"),
                 ("divisions", "TEXT"), ("division_custom", "TEXT"), ("opponent", "TEXT"), ("home_away", "TEXT"),
                 ("gameplay_notes", "TEXT"), ("segments", "TEXT"), ("comp_format", "TEXT")):
        if c not in cols:
            d.execute("ALTER TABLE practices ADD COLUMN %s %s" % (c, t))
    d.execute("UPDATE practices SET activity_type='practice' WHERE activity_type IS NULL OR trim(activity_type)=''")
    d.execute("UPDATE practices SET sport='Water Polo' WHERE sport IS NULL OR trim(sport)=''")
    migrate_social_kinds(d)
    pin_known_pools(d)
def migrate_social_joins(d):
    """Who is joining the after-practice social. Existing practices start with nobody."""
    d.execute("""CREATE TABLE IF NOT EXISTS social_joins(
        practice_id INTEGER NOT NULL, member_id INTEGER NOT NULL, PRIMARY KEY(practice_id, member_id))""")
def migrate_practice_coaches(d):
    """Create practice coach assignments on an older database under DATA_DIR. Existing rows stay."""
    d.execute("""CREATE TABLE IF NOT EXISTS practice_coaches(
        practice_id INTEGER NOT NULL, member_id INTEGER NOT NULL, PRIMARY KEY(practice_id, member_id))""")
    cols = [r[1] for r in d.execute("PRAGMA table_info(practice_coaches)")]
    if "is_lead" not in cols:
        d.execute("ALTER TABLE practice_coaches ADD COLUMN is_lead INTEGER NOT NULL DEFAULT 0")
    if "focus" not in cols:
        d.execute("ALTER TABLE practice_coaches ADD COLUMN focus TEXT")
def migrate_members(d):
    """Add columns missing from a database created by an older version (production SQLite on /data)."""
    cols = [r[1] for r in d.execute("PRAGMA table_info(members)")]
    for c, t in (("is_admin", "INTEGER DEFAULT 0"), ("role", "TEXT DEFAULT 'athlete'"), ("usawp_verified_by", "TEXT"),
                 ("usawp_verified_at", "TEXT"), ("sport80_contact_id", "TEXT"), ("preferred_first", "TEXT"),
                 ("trial_acknowledged_at", "TEXT"), ("notify_prefs", "TEXT"),
                 ("email_reminders", "INTEGER DEFAULT 1"), ("membership_type", "TEXT"), ("joined", "INTEGER DEFAULT 0"),
                 ("require_background", "INTEGER DEFAULT 0"), ("photo", "TEXT")):
        if c not in cols: d.execute(f"ALTER TABLE members ADD COLUMN {c} {t}")
    # /join always stores a phone. Existing registrations keep Google sign-in; a blank phone is not one.
    cols = [r[1] for r in d.execute("PRAGMA table_info(members)")]
    if "phone" in cols and "joined" in cols:
        d.execute("""UPDATE members SET joined=1 WHERE COALESCE(joined,0)=0 AND COALESCE(role,'')!='system'
                     AND trim(COALESCE(phone,''))!=''""")
def migrate_lineup(d):
    """Away and hosted lineup events. Existing databases gain the tables and columns without touching practices."""
    d.execute("""CREATE TABLE IF NOT EXISTS lineup_events(id INTEGER PRIMARY KEY, kind TEXT NOT NULL, title TEXT NOT NULL,
        date TEXT NOT NULL, end_date TEXT, city TEXT, venue TEXT, start TEXT, location TEXT, description TEXT, link TEXT)""")
    d.execute("""CREATE TABLE IF NOT EXISTS lineup_rsvps(event_id INTEGER NOT NULL, member_id INTEGER NOT NULL,
        going INTEGER NOT NULL, at TEXT DEFAULT CURRENT_TIMESTAMP, PRIMARY KEY(event_id, member_id))""")
    cols = [r[1] for r in d.execute("PRAGMA table_info(lineup_events)")]
    for c, t in (("end_date", "TEXT"), ("city", "TEXT"), ("venue", "TEXT")):
        if c not in cols:
            d.execute("ALTER TABLE lineup_events ADD COLUMN %s %s" % (c, t))
    d.execute("UPDATE lineup_events SET end_date=date WHERE end_date IS NULL OR trim(end_date)=''")
    d.execute("UPDATE lineup_events SET venue=location WHERE (venue IS NULL OR trim(venue)='') AND trim(COALESCE(location,''))!=''")
    cols = [r[1] for r in d.execute("PRAGMA table_info(lineup_events)")]
    if "stage" not in cols:
        d.execute("ALTER TABLE lineup_events ADD COLUMN stage TEXT")
    if "hosting" not in cols:
        d.execute("ALTER TABLE lineup_events ADD COLUMN hosting TEXT")
    # Legacy single-field kinds, only before hosting is filled in. New rows already store Tournament, Clinic, or Social.
    d.execute("UPDATE lineup_events SET kind='Away tournament' WHERE kind='Tournament' AND (hosting IS NULL OR trim(hosting)='')")
    d.execute("UPDATE lineup_events SET kind='Team trip' WHERE kind IN ('Social', 'Team trip/Social') AND (hosting IS NULL OR trim(hosting)='')")
    d.execute("UPDATE lineup_events SET stage='going' WHERE (stage IS NULL OR stage='') AND kind='Away tournament' AND (hosting IS NULL OR trim(hosting)='')")
    d.execute("UPDATE lineup_events SET stage='attending' WHERE (hosting IS NULL OR trim(hosting)='') AND (kind IN ('Hosted tournament', 'Hosted social', 'Team trip') OR stage IS NULL OR stage='')")
    legacy = {
        "Away tournament": ("Away", "Tournament"),
        "Hosted tournament": ("Hosting", "Tournament"),
        "Hosted social": ("Hosting", "Social"),
        "Team trip": ("Away", "Clinic"),
    }
    for row in d.execute("SELECT id, kind FROM lineup_events"):
        pair = legacy.get(row[1])
        if pair:
            d.execute("UPDATE lineup_events SET hosting=?, kind=? WHERE id=?", (pair[0], pair[1], row[0]))
    d.execute("UPDATE lineup_events SET hosting='Away' WHERE hosting IS NULL OR trim(hosting)=''")
    d.execute("UPDATE lineup_events SET stage='going' WHERE stage='attending' AND kind IN ('Tournament', 'Clinic')")
    d.execute("UPDATE lineup_events SET stage='attending' WHERE kind IN ('Social', 'Volunteering')")
    d.execute("UPDATE lineup_events SET stage='interest' WHERE (stage IS NULL OR trim(stage)='') AND kind IN ('Tournament', 'Clinic')")
    d.execute("UPDATE lineup_events SET stage='attending' WHERE stage IS NULL OR trim(stage)=''")
    lineupfeed.ensure_schema(d)
    for row in d.execute("SELECT id, city, venue FROM lineup_events"):
        city = " ".join(str((row["city"] if hasattr(row, "keys") else row[1]) or "").split())
        venue = " ".join(str((row["venue"] if hasattr(row, "keys") else row[2]) or "").split())
        eid = row["id"] if hasattr(row, "keys") else row[0]
        if city and venue and city.casefold() == venue.casefold():
            d.execute("UPDATE lineup_events SET city=?, venue='', lat=NULL, lng=NULL WHERE id=?", (city, eid))
        elif venue and not city:
            d.execute("UPDATE lineup_events SET city=?, venue='', lat=NULL, lng=NULL WHERE id=?", (venue, eid))
def migrate_series(d):
    """Practice series, their coaches, and skipped dates. Existing one-off practices stay unattached."""
    d.execute("""CREATE TABLE IF NOT EXISTS practice_series(id INTEGER PRIMARY KEY, weekdays TEXT NOT NULL, start TEXT NOT NULL, end TEXT NOT NULL,
        location TEXT NOT NULL, start_date TEXT NOT NULL, end_date TEXT)""")
    d.execute("""CREATE TABLE IF NOT EXISTS series_coaches(series_id INTEGER NOT NULL, member_id INTEGER NOT NULL,
        is_lead INTEGER NOT NULL DEFAULT 0, PRIMARY KEY(series_id, member_id))""")
    d.execute("CREATE TABLE IF NOT EXISTS series_skips(series_id INTEGER NOT NULL, date TEXT NOT NULL, PRIMARY KEY(series_id, date))")
    cols = [r[1] for r in d.execute("PRAGMA table_info(practices)")]
    for c, t in (("series_id", "INTEGER"), ("series_detached", "INTEGER DEFAULT 0"), ("skipped", "INTEGER DEFAULT 0")):
        if c not in cols:
            d.execute("ALTER TABLE practices ADD COLUMN %s %s" % (c, t))
    scols = [r[1] for r in d.execute("PRAGMA table_info(practice_series)")]
    for c, t in (("activity_type", "TEXT"), ("sport", "TEXT"), ("title", "TEXT"), ("skill_levels", "TEXT"),
                 ("divisions", "TEXT"), ("division_custom", "TEXT"), ("opponent", "TEXT"), ("home_away", "TEXT"),
                 ("gameplay_notes", "TEXT"), ("segments", "TEXT"), ("comp_format", "TEXT")):
        if c not in scols:
            d.execute("ALTER TABLE practice_series ADD COLUMN %s %s" % (c, t))
    d.execute("UPDATE practice_series SET activity_type='practice' WHERE activity_type IS NULL OR trim(activity_type)=''")
    d.execute("UPDATE practice_series SET sport='Water Polo' WHERE sport IS NULL OR trim(sport)=''")
def migrate_messages(d):
    """Add chat columns missing from a database created by an older version (production SQLite on DATA_DIR)."""
    cols = [r[1] for r in d.execute("PRAGMA table_info(messages)")]
    for c, t in (("channel", "TEXT DEFAULT 'team'"), ("image", "TEXT"), ("edited_at", "TEXT"), ("deleted", "INTEGER DEFAULT 0"), ("reply_to", "INTEGER")):
        if c not in cols: d.execute("ALTER TABLE messages ADD COLUMN %s %s" % (c, t))
def clean_preferred(v):
    v = str(v or "").strip()[:40]
    return v or None
def clean_legal(v):
    """Collapse whitespace. Empty means the field was left blank."""
    return " ".join(str(v or "").split())[:80]
def display_first(m):
    """Name shown in the app. Blank preferred_first falls back to the legal first name."""
    if not m: return ""
    if "preferred_first" in m.keys():
        pref = (m["preferred_first"] or "").strip()
        if pref: return pref
    return m["first"]
def initials(m):
    """First initial plus last initial, for a profile picture that has not been set."""
    if not m: return ""
    first = (display_first(m) or "").strip()
    last = ""
    try:
        if "last" in m.keys(): last = (m["last"] or "").strip()
    except (AttributeError, TypeError):
        last = ""
    letters = (first[:1] + last[:1]).upper()
    return letters or "?"
def normalize_phone(raw):
    """10 US digits, or None. A leading 1 is dropped. Stored without punctuation."""
    digits = re.sub(r"\D", "", str(raw or ""))
    if len(digits) == 11 and digits.startswith("1"): digits = digits[1:]
    return digits if len(digits) == 10 else None
def fmt_phone(raw):
    """(720) 535-5925 when the number has 10 digits. Anything else is shown as stored."""
    digits = normalize_phone(raw)
    if digits: return "(%s) %s-%s" % (digits[:3], digits[3:6], digits[6:])
    text = " ".join(str(raw or "").split())
    return text or "—"
app.jinja_env.globals.update(display_first=display_first, initials=initials, fmt_phone=fmt_phone)
# applies_to: all | athlete | coach. keywords: normalized substrings to find this item's columns in a Sport:80 export.
DEFAULT_REQS = [("SafeSport training", "all", "safesport", 1), ("Background screening", "coach", "background", 1),
                ("Concussion training", "coach", "concussion", 1)]
def drop_club_waiver(d):
    """Remove the Club waiver requirement from an existing database. Other rows stay put."""
    ids = []
    for rid, name, keywords in d.execute("SELECT id, name, keywords FROM requirements"):
        label = (name or "").strip().lower()
        kws = [k.strip().lower() for k in (keywords or "").split(",") if k.strip()]
        if label == "club waiver" or "waiver" in kws: ids.append(rid)
    if not ids: return
    marks = ",".join("?" * len(ids))
    d.execute("DELETE FROM member_reqs WHERE req_id IN (%s)" % marks, ids)
    d.execute("DELETE FROM requirements WHERE id IN (%s)" % marks, ids)
    d.commit()
def req_keywords(d):
    kws = [k for r in d.execute("SELECT keywords FROM requirements") for k in (r[0] or "").split(",") if k]
    if "waiver" not in kws: kws.append("waiver")  # leftover Sport:80 waiver columns are not membership dates
    return kws
def safesport_req(d):
    for q in d.execute("SELECT * FROM requirements WHERE active=1 ORDER BY id"):
        name = (q["name"] or "").lower()
        kws = [k.strip().lower() for k in (q["keywords"] or "").split(",") if k.strip()]
        if "safesport" in kws or "safesport" in name: return q
    return None
def background_req(d):
    for q in d.execute("SELECT * FROM requirements WHERE active=1 ORDER BY id"):
        name = (q["name"] or "").lower()
        kws = [k.strip().lower() for k in (q["keywords"] or "").split(",") if k.strip()]
        if "background" in kws or "background" in name: return q
    return None
def referee_req(d):
    for q in d.execute("SELECT * FROM requirements WHERE active=1 ORDER BY id"):
        blob = ((q["name"] or "") + " " + (q["keywords"] or "")).lower()
        if "referee certification" in blob or "refereecert" in blob: return q
    return None
def ensure_referee_req(d):
    """Older databases gain a place to store a referee certification expiry."""
    if referee_req(d): return
    d.execute("INSERT INTO requirements(name,applies_to,keywords,expires) VALUES(?,?,?,?)",
              ("Referee certification", "all", "refereecert", 1))
    d.commit()
def _member_flag(member, key):
    if not member: return None
    try:
        if key in member.keys(): return member[key]
    except (AttributeError, TypeError):
        return None
    return None
def is_role_coach(member):
    """True after Make coach. An admin who was not made a coach stays false."""
    return bool(member) and (_member_flag(member, "role") or "") == "coach"
def background_required(member):
    """Background screening is required only for members promoted with Make coach."""
    return is_role_coach(member)
def background_view(d, member):
    """Dated background screening line. Missing only when a coach has no date. None when someone else has no date."""
    if not member: return None
    q = background_req(d)
    if not q: return None
    mr = d.execute("SELECT * FROM member_reqs WHERE member_id=? AND req_id=?", (member["id"], q["id"])).fetchone()
    date = str(mr["expires_on"])[:10] if mr and mr["expires_on"] else ""
    required = background_required(member)
    if not date and not required: return None
    if not date:
        return dict(date="", kind="bad", text="Background screening missing", required=required, req_id=q["id"])
    left = days_left(date)
    if left is None or left < 0: kind = "bad"
    elif left <= EXPIRING_DAYS: kind = "warn"
    else: kind = "ok"
    return dict(date=date, kind=kind, text="Background screening expires " + date, required=required, req_id=q["id"])
def coach_clearance(d, member):
    """Cleared to coach requires a current background screening. Only Make coach members get this status."""
    if not is_role_coach(member): return None
    bg = background_view(d, member)
    ok = bool(bg and bg["date"] and bg["kind"] != "bad")
    return dict(ok=ok, text="Cleared to coach" if ok else "Not cleared to coach")
def save_background_expiry(d, mid, exp, by):
    q = background_req(d)
    if not q or not exp: return
    now = stamp_pt("minutes")
    d.execute("""INSERT INTO member_reqs(member_id,req_id,completed_on,expires_on,source,by,at) VALUES(?,?,?,?,'manual',?,?)
        ON CONFLICT(member_id,req_id) DO UPDATE SET expires_on=excluded.expires_on,
        completed_on=COALESCE(member_reqs.completed_on, excluded.completed_on), source='manual', by=excluded.by, at=excluded.at""",
        (mid, q["id"], today_pt().isoformat(), exp.isoformat() if hasattr(exp, "isoformat") else str(exp)[:10], by, now))
def clearance(d, member):
    """Cleared to play = USAWP membership verified and current, and SafeSport current.
    An active 2-week trial counts as cleared until it ends or the membership is verified.
    Background screening never blocks play."""
    today = today_pt().isoformat(); reasons = []; items = []
    until = member["usawp_valid_until"] if member and "usawp_valid_until" in member.keys() else None
    membership_expired = bool(until and until < today)
    if membership_expired: reasons.append("Membership expired")
    elif member["usawp_status"] != "verified": reasons.append(f"Membership {member['usawp_status']}")
    q = safesport_req(d)
    reqs = [q] if q else []
    if not q: reasons.append("SafeSport training missing")
    for q in reqs:
        mr = d.execute("SELECT * FROM member_reqs WHERE member_id=? AND req_id=?", (member["id"], q["id"])).fetchone()
        if not mr or not (mr["completed_on"] or mr["expires_on"]): st = "missing"
        elif mr["expires_on"] and mr["expires_on"] < today: st = "expired"
        elif q["expires"] and not mr["expires_on"]: st = "no date"
        else: st = "ok"
        items.append(dict(req=q, mr=mr, status=st, days_left=days_left(mr["expires_on"]) if mr else None))
        if st in ("missing", "expired"): reasons.append(f"{q['name']} {st}")
    tw = trial_window(member)
    if tw and tw["active"] and (member["usawp_status"] or "") != "verified" and not membership_expired:
        return dict(ok=True, reasons=[], checks=items)
    return dict(ok=not reasons, reasons=reasons, checks=items)
def expiry_notes(member, cl=None):
    """Lines for the home card once a membership or SafeSport date has passed."""
    today = today_pt().isoformat()
    until = None
    if member:
        try: keys = member.keys()
        except AttributeError: keys = member
        if "usawp_valid_until" in keys: until = member["usawp_valid_until"]
    membership = bool(until and until < today)
    safesport = None
    for it in (cl or {}).get("checks") or []:
        q = it["req"]; name = (q["name"] or "").lower(); kws = (q["keywords"] or "").lower()
        if it["status"] == "expired" and ("safesport" in kws or "safesport" in name) and it.get("mr") and it["mr"]["expires_on"]:
            safesport = it["mr"]["expires_on"]
    lines = []
    if membership: lines.append(f"Membership expired {until}")
    if safesport: lines.append(f"SafeSport expired {safesport}")
    skip = set()
    if membership: skip.add("Membership expired")
    if safesport: skip.add("SafeSport training expired")
    rest = [r for r in (cl or {}).get("reasons") or [] if r not in skip]
    return {"membership": membership, "safesport": safesport, "lines": lines, "rest": rest}
app.jinja_env.globals.update(clearance=lambda m: clearance(db(), m), expiry_notes=expiry_notes,
    background_view=lambda m: background_view(db(), m), coach_clearance=lambda m: coach_clearance(db(), m))
def expire_sweep(d):
    """Auto-flip: anyone whose expires_on (usawp_valid_until) has passed becomes expired."""
    d.execute("UPDATE members SET usawp_status='expired', usawp_raw='Expired '||usawp_valid_until WHERE usawp_status IN ('verified','pending') AND usawp_valid_until IS NOT NULL AND usawp_valid_until < ?", (today_pt().isoformat(),)); d.commit()
def expiry_report(d, days=None):
    days = days or EXPIRING_DAYS; today = today_pt()
    rows = d.execute("SELECT id, first, last, preferred_first, email, phone, usawp_status, usawp_valid_until FROM members WHERE usawp_valid_until IS NOT NULL ORDER BY usawp_valid_until").fetchall()
    rq = d.execute("""SELECT m.id, m.first, m.last, m.preferred_first, m.email, m.phone, 'verified' AS usawp_status, x.expires_on AS usawp_valid_until, q.name AS item
      FROM member_reqs x JOIN members m ON m.id=x.member_id JOIN requirements q ON q.id=x.req_id
      WHERE q.active=1 AND x.expires_on IS NOT NULL AND (q.applies_to='all' OR q.applies_to=m.role
        OR lower(q.name) LIKE '%background%' OR lower(ifnull(q.keywords,'')) LIKE '%background%')""").fetchall()
    out = {"expired": [], "within_7": [], "within_%d" % days: []}
    for r in sorted([dict(r, item="USAWP membership") for r in rows] + [dict(r) for r in rq], key=lambda x: x["usawp_valid_until"]):
        left = (dt.date.fromisoformat(r["usawp_valid_until"]) - today).days
        item = dict(r, days_left=left)
        if left < 0 or r["usawp_status"] == "expired": out["expired"].append(item)
        elif left <= 7: out["within_7"].append(item)
        elif left <= days: out["within_%d" % days].append(item)
    return out
def days_left(v):
    return (dt.date.fromisoformat(v) - today_pt()).days if v else None
TRIAL_DAYS = 14
TRIAL_JOIN_URL = "https://usawp.sport80.com/public/widget/1"  # official registration widget linked from usawaterpolo.org; trial is a membership type in that flow
def fmt_md(iso):
    d = dt.date.fromisoformat(str(iso)[:10]); return d.strftime("%b ") + str(d.day)
def trial_window(m):
    """2-week USAWP trial. The end date is the acknowledgment date plus 14 days, and that end date still counts."""
    if not m: return None
    try: keys = m.keys()
    except AttributeError: keys = m
    if "trial_acknowledged_at" not in keys: return None
    raw = m["trial_acknowledged_at"]
    if not raw: return None
    try: start = dt.date.fromisoformat(str(raw)[:10])
    except ValueError: return None
    end = start + dt.timedelta(days=TRIAL_DAYS)
    today = today_pt()
    left = (end - today).days
    return {"start": start.isoformat(), "end": end.isoformat(), "ends": fmt_md(end.isoformat()), "active": today <= end, "expired": today > end, "days_left": left}
def trial_left_phrase(tw):
    """Countdown from the trial end date: expires today, expires in 1 day, or expires in N days."""
    if not tw or not tw.get("active"): return ""
    left = tw.get("days_left")
    if left is None or left <= 0: return "expires today"
    if left == 1: return "expires in 1 day"
    return "expires in %d days" % left
def trial_badge(tw):
    """Status label for an active trial, counted from the trial end date."""
    phrase = trial_left_phrase(tw)
    return ("Trial · " + phrase) if phrase else ""
def relative_day(iso):
    """TODAY, TOMORROW, a weekday within the next week, otherwise a short date."""
    if not iso: return ""
    try: day = dt.date.fromisoformat(str(iso)[:10])
    except ValueError: return ""
    left = (day - today_pt()).days
    if left == 0: return "TODAY"
    if left == 1: return "TOMORROW"
    if 2 <= left <= 6: return day.strftime("%A").upper()
    return day.strftime("%b ") + str(day.day)
def remind(d, mid, by="Grunions"):
    r = d.execute("SELECT first, preferred_first, usawp_valid_until FROM members WHERE id=?", (mid,)).fetchone()
    if not r: return
    n = days_left(r["usawp_valid_until"])
    when = "has expired" if n is not None and n < 0 else (f"expires in {n} days ({r['usawp_valid_until']})" if n is not None else "needs to be confirmed")
    d.execute("INSERT INTO notices(member_id, body) VALUES(?,?)", (mid, f"Hi {display_first(r)}, your USA Water Polo membership {when}. Renew at usawp.sport80.com with Grunions as your club so you can keep playing. ({by})"))
app.jinja_env.globals.update(days_left=days_left, EXPIRING_DAYS=EXPIRING_DAYS, trial_window=trial_window, trial_badge=trial_badge, trial_left_phrase=trial_left_phrase, TRIAL_JOIN_URL=TRIAL_JOIN_URL, relative_day=relative_day)
@app.teardown_appcontext
def _close(e):
    d = g.pop("db", None)
    if d: d.close()

def norm(s): return re.sub(r"[^a-z]", "", (s or "").lower())
def location_for(d):
    wd = dt.date.fromisoformat(d).weekday()
    return {1: "Marina HS · Tue", 4: "Westminster HS · Fri"}.get(wd, "Other")
def me():
    if "me" not in g:
        mid = session.get("mid")
        g.me = db().execute("SELECT * FROM members WHERE id=?", (mid,)).fetchone() if mid else None
    return g.me
def login_required(f):
    @functools.wraps(f)
    def w(*a, **k):
        if not me(): return redirect(url_for("login", next=request.path))
        return f(*a, **k)
    return w
def admin_required(f):
    @functools.wraps(f)
    def w(*a, **k):
        if not me(): return redirect(url_for("login", next=request.path))
        if not me()["is_admin"]: abort(403)
        return f(*a, **k)
    return w
def is_active_coach(m=None):
    """Coach access from Make active coach. Being an admin does not count."""
    m = m or me()
    return bool(m and (m["role"] or "") == "coach")
def is_staff(m=None):
    """Check-in and coaches chat. Only active coaches."""
    return is_active_coach(m)
def can_host_practice(m=None):
    """Admins and active coaches can set a social and a coach message."""
    m = m or me()
    return bool(m and (m["is_admin"] or is_active_coach(m)))
def lineup_organizer_required(f):
    """Create, edit, and delete Lineup events. Members can still view and RSVP."""
    @functools.wraps(f)
    def w(*a, **k):
        if not me(): return redirect(url_for("login", next=request.path))
        if not can_host_practice(): abort(403)
        return f(*a, **k)
    return w
def role_label(m): return "admin" if m["is_admin"] else ("coach" if m["role"] == "coach" else "member")
_COACH_WORD = re.compile(r"\bcoach\b", re.IGNORECASE)
_REFEREE_WORD = re.compile(r"\breferee\b", re.IGNORECASE)
def is_coach_membership(text):
    """USAWP Coach membership. The word coach counts; coaches and coaching do not."""
    return bool(text and _COACH_WORD.search(str(text)))
def is_referee_membership(text):
    """USAWP Referee membership. The word referee counts; referees does not."""
    return bool(text and _REFEREE_WORD.search(str(text)))
def screening_dates(d, mid):
    """Latest SafeSport and background expiry on file for one member."""
    found = {}
    for name, keywords, exp in d.execute("""SELECT q.name, q.keywords, x.expires_on FROM member_reqs x
            JOIN requirements q ON q.id=x.req_id WHERE x.member_id=?""", (mid,)):
        if not exp: continue
        blob = ((name or "") + " " + (keywords or "")).lower()
        for key in ("safesport", "background", "referee"):
            day = str(exp)[:10]
            hit = ("referee certification" in blob or "refereecert" in blob) if key == "referee" else key in blob
            if hit and (key not in found or day > found[key]): found[key] = day
    return found
def screenings_current(d, mid):
    """Background screening and SafeSport are current when each expiry date is today or later."""
    today = today_pt().isoformat(); found = screening_dates(d, mid)
    return bool(found.get("safesport") and found["safesport"] >= today and found.get("background") and found["background"] >= today)
def coach_eligibility(d, member):
    """Verified current USAWP coach membership, plus current background and SafeSport.
    Make admin and Make coach do not depend on this. A past date on a verified coach membership
    is reported as Coach eligibility expired <date>."""
    empty = {"eligible": False, "expired": None, "text": ""}
    if not member: return empty
    try: mid = member["id"]; keys = member.keys()
    except (TypeError, KeyError, IndexError): return empty
    if not is_coach_membership(member["membership_type"] if "membership_type" in keys else None): return empty
    status = (member["usawp_status"] if "usawp_status" in keys else "") or ""
    until = str(member["usawp_valid_until"])[:10] if ("usawp_valid_until" in keys and member["usawp_valid_until"]) else ""
    today = today_pt().isoformat(); dates = screening_dates(d, mid)
    ss, bg = dates.get("safesport") or "", dates.get("background") or ""
    membership_ok = status == "verified" and (not until or until >= today)
    if membership_ok and ss and ss >= today and bg and bg >= today:
        return {"eligible": True, "expired": None, "text": "Coach eligible"}
    past = [day for day in (until, ss, bg) if day and day < today]
    if (status == "verified" or (status == "expired" and until)) and past:
        day = min(past)
        return {"eligible": False, "expired": day, "text": "Coach eligibility expired " + day}
    return empty
def referee_eligibility(d, member):
    """Verified current USAWP referee membership, plus current background and SafeSport.
    A past date on a verified referee membership is Referee eligibility expired <date>."""
    empty = {"eligible": False, "expired": None, "text": ""}
    if not member: return empty
    try: mid = member["id"]; keys = member.keys()
    except (TypeError, KeyError, IndexError): return empty
    today = today_pt().isoformat(); dates = screening_dates(d, mid)
    cert = dates.get("referee") or ""
    if not is_referee_membership(member["membership_type"] if "membership_type" in keys else None) and not cert: return empty
    status = (member["usawp_status"] if "usawp_status" in keys else "") or ""
    until = str(member["usawp_valid_until"])[:10] if ("usawp_valid_until" in keys and member["usawp_valid_until"]) else ""
    ss, bg = dates.get("safesport") or "", dates.get("background") or ""
    membership_ok = status == "verified" and (not until or until >= today)
    cert_ok = not cert or cert >= today
    if membership_ok and ss and ss >= today and bg and bg >= today and cert_ok:
        return {"eligible": True, "expired": None, "text": "Referee eligible"}
    past = [day for day in (until, ss, bg, cert) if day and day < today]
    if (status == "verified" or (status == "expired" and until)) and past:
        day = min(past)
        return {"eligible": False, "expired": day, "text": "Referee eligibility expired " + day}
    return empty
def usawp_coach_badge(m):
    return coach_eligibility(db(), m)["eligible"]
def coach_row_expiry(d, member):
    """Earliest membership, SafeSport, or background date for the Coaches list chip."""
    until = ""
    try:
        keys = member.keys()
        if "usawp_valid_until" in keys and member["usawp_valid_until"]:
            until = str(member["usawp_valid_until"])[:10]
        mid = member["id"]
    except (TypeError, KeyError, IndexError):
        return {"eligible": False, "date": ""}
    dates = screening_dates(d, mid)
    days = [day for day in (until, dates.get("safesport") or "", dates.get("background") or "") if day]
    date = min(days) if days else ""
    eligible = coach_eligibility(d, member)["eligible"]
    tone = "bad"
    if eligible:
        left = days_left(date) if date else None
        tone = "warn" if left is not None and left <= EXPIRING_DAYS else ""
    return {"eligible": eligible, "date": date, "tone": tone}
def credential_dates(m):
    """SafeSport, background, and referee certification expiries for the recheck form."""
    if not m: return {}
    try: mid = m["id"]
    except (TypeError, KeyError, IndexError): return {}
    return screening_dates(db(), mid)
def fmt_long(iso):
    """Nov 3, 2026."""
    if not iso: return ""
    try: d = dt.date.fromisoformat(str(iso)[:10])
    except ValueError: return ""
    return d.strftime("%b ") + str(d.day) + ", " + str(d.year)
def fmt_when(s):
    """Oct 23, 6:57 PM from a Pacific stamp."""
    if not s or "T" not in str(s): return ""
    day, clock = str(s).split("T", 1)
    try:
        d = dt.date.fromisoformat(day[:10])
        h, m = map(int, clock[:5].split(":"))
    except (ValueError, IndexError):
        return ""
    am = "AM" if h < 12 else "PM"
    h12 = (h - 1) % 12 + 1
    return d.strftime("%b ") + str(d.day) + ", %d:%02d %s" % (h12, m, am)
def date_dot(iso):
    """Green, amber, or red for an expiry date. Empty when there is no date."""
    if not iso: return ""
    left = days_left(str(iso)[:10])
    if left is None or left < 0: return "bad"
    if left <= EXPIRING_DAYS: return "warn"
    return "ok"
def _expiring_label(n):
    if n <= 0: return "Expiring soon today"
    if n == 1: return "Expiring soon in 1 day"
    return "Expiring soon in %d days" % n
def panel_status(member):
    """Headline for the expanded member row: a status, a dot, and one reason."""
    cl = clearance(db(), member)
    tw = trial_window(member)
    ex = expiry_notes(member, cl)
    status, until = "", ""
    try:
        status = (member["usawp_status"] or "") if member else ""
        if member and member["usawp_valid_until"]: until = str(member["usawp_valid_until"])[:10]
    except (TypeError, KeyError, IndexError):
        pass
    dl = days_left(until) if until else None
    if tw and tw["active"] and status != "verified" and not ex["membership"]:
        return {"label": trial_badge(tw), "dot": "warn", "reason": trial_badge(tw)}
    if tw and tw["expired"] and status != "verified":
        return {"label": "Expired", "dot": "bad", "reason": "Trial membership ended " + fmt_long(tw["end"])}
    if ex["membership"] or status == "expired":
        return {"label": "Expired", "dot": "bad", "reason": ("Membership expired " + fmt_long(until)) if until else "Membership expired"}
    if status != "verified":
        reason = "Membership not verified"
        return {"label": "Not verified", "dot": "bad", "reason": reason}
    if ex.get("safesport"):
        return {"label": "Expired", "dot": "bad", "reason": "SafeSport expired " + fmt_long(ex["safesport"])}
    if not cl["ok"]:
        reason = (cl.get("reasons") or ["Not cleared"])[0]
        if reason == "SafeSport training missing": reason = "SafeSport not on file"
        elif reason.startswith("Membership "): reason = "Membership not verified"
        return {"label": "Not cleared", "dot": "bad", "reason": reason}
    if dl is not None and dl <= EXPIRING_DAYS:
        return {"label": _expiring_label(dl), "dot": "warn", "reason": "Membership expires " + fmt_long(until)}
    ss = credential_dates(member).get("safesport") or ""
    left = days_left(ss) if ss else None
    if left is not None and left <= EXPIRING_DAYS:
        return {"label": _expiring_label(left), "dot": "warn", "reason": "SafeSport expires " + fmt_long(ss)}
    return {"label": "Cleared", "dot": "ok", "reason": ""}
def approval_count():
    m = me()
    if not m or not can_host_practice(m): return 0
    try: return db().execute("SELECT COUNT(*) FROM lineup_events WHERE status='pending'").fetchone()[0]
    except sqlite3.OperationalError: return 0
def on_coaching_list(member):
    try: mid = member["id"]
    except (TypeError, KeyError, IndexError): return False
    return db().execute("SELECT 1 FROM coaching_list WHERE member_id=?", (mid,)).fetchone() is not None
app.jinja_env.globals.update(is_staff=is_staff, can_host_practice=can_host_practice, approval_count=approval_count, role_label=role_label, usawp_coach_badge=usawp_coach_badge, coach_eligibility=lambda m: coach_eligibility(db(), m), referee_eligibility=lambda m: referee_eligibility(db(), m), credential_dates=credential_dates, coach_row_expiry=lambda m: coach_row_expiry(db(), m), fmt_long=fmt_long, fmt_when=fmt_when, date_dot=date_dot, panel_status=panel_status, on_coaching_list=on_coaching_list)
def staff_required(f):
    @functools.wraps(f)
    def w(*a, **k):
        if not me(): return redirect(url_for("login", next=request.path))
        if not is_staff(): abort(403)
        return f(*a, **k)
    return w
# CSRF: per-session token on every POST form/fetch
def csrf_token():
    if "csrf" not in session: session["csrf"] = secrets.token_urlsafe(16)
    return session["csrf"]
@app.before_request
def _csrf():
    if request.method in ("POST", "DELETE") and not request.path.startswith("/api/verify-requests/"):  # bot API uses bearer auth, no cookies
        t = request.form.get("csrf") or request.headers.get("X-CSRF")
        if not t or t != session.get("csrf"): abort(400, "Bad CSRF token, reload the page.")
def csrf_field(): return Markup('<input type=hidden name=csrf value="%s">' % csrf_token())
def admin_notices():
    if not (me() and me()["is_admin"]): return []
    d = db(); rows = d.execute("SELECT * FROM notices WHERE member_id=? AND seen=0 ORDER BY id DESC", (me()["id"],)).fetchall()
    d.execute("UPDATE notices SET seen=1 WHERE member_id=? AND seen=0", (me()["id"],)); d.commit(); return rows
def leaflet_css():
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static", "leaflet", "leaflet.css")
    with open(path, encoding="utf-8") as f: return f.read()
app.jinja_env.globals.update(REACTIONS=REACTIONS, csrf_token=csrf_token, csrf_field=csrf_field, admin_notices=admin_notices, me=me, leaflet_css=leaflet_css(), foundation_css=ui.FOUNDATION)
def start_session(mid):
    session.clear(); session.permanent = True; session["mid"] = mid; csrf_token()

def page(body, tab="", **kw):
    html = render_template_string(ui.BASE + body + ui.TABS, tab=tab, **kw)
    resp = Response(html, mimetype="text/html; charset=utf-8")
    resp.headers["Cache-Control"] = "no-store"
    return resp

# ---------- public: signup + login ----------
@app.route("/manifest.webmanifest")
def webmanifest():
    return Response(json.dumps({
        "name": "Grunions Water Polo", "short_name": "Grunions", "start_url": "/", "scope": "/", "display": "standalone",
        "background_color": "#090D0B", "theme_color": "#090D0B",
        "icons": [
            {"src": "/static/icons/icon-192.png", "sizes": "192x192", "type": "image/png", "purpose": "any"},
            {"src": "/static/icons/icon-512.png", "sizes": "512x512", "type": "image/png", "purpose": "any"},
            {"src": "/static/icons/maskable-512.png", "sizes": "512x512", "type": "image/png", "purpose": "maskable"},
        ],
    }), mimetype="application/manifest+json")
@app.route("/")
def index(): return redirect("/home" if me() else "/join")

@app.route("/join", methods=["GET", "POST"])
def join():
    if request.method == "POST":
        f = {k: (request.form.get(k) or "").strip() for k in ("first", "last", "email", "phone")}
        if not all(f.values()) or not re.match(r"[^@\s]+@[^@\s]+\.[^@\s]+$", f["email"]):
            flash("Please fill in every field with a valid email."); return redirect("/join")
        email = f["email"].lower(); d = db(); pref = clean_preferred(request.form.get("preferred_first"))
        if d.execute("SELECT 1 FROM members WHERE email=?", (email,)).fetchone():
            flash("You already have an account. We sent you a login link instead.")
            return send_link(email)
        cur = d.execute("INSERT INTO members(first,last,email,phone,is_admin,preferred_first,joined) VALUES(?,?,?,?,?,?,1)",
                        (f["first"], f["last"], email, f["phone"], int(email in ADMIN_EMAILS), pref))
        d.commit(); sync_practice_sheets(d); start_session(cur.lastrowid)
        flash(f"Welcome to the Grunions, {pref or f['first']}! Find a coach on deck to get checked in.")
        return redirect("/home")
    return page(T["join"])

def smtp_ready(): return all(SMTP.values())
def send_email(to, subject, text):
    """Send via SMTP (Gmail app password, Resend, Brevo...). Port 465 = SSL, otherwise STARTTLS."""
    import smtplib, ssl
    from email.message import EmailMessage
    msg = EmailMessage(); msg["From"] = SMTP["MAIL_FROM"]; msg["To"] = to; msg["Subject"] = subject; msg.set_content(text)
    port = int(SMTP["SMTP_PORT"]); ctx = ssl.create_default_context()
    if port == 465: srv = smtplib.SMTP_SSL(SMTP["SMTP_HOST"], port, context=ctx, timeout=15)
    else: srv = smtplib.SMTP(SMTP["SMTP_HOST"], port, timeout=15); srv.starttls(context=ctx)
    with srv: srv.login(SMTP["SMTP_USER"], SMTP["SMTP_PASSWORD"]); srv.send_message(msg)
def send_link(email):
    m = db().execute("SELECT id, first, preferred_first FROM members WHERE email=? AND COALESCE(role,'')!='system'", (email,)).fetchone()
    link = None
    if m:
        tok = secrets.token_urlsafe(32)
        db().execute("INSERT INTO login_tokens VALUES(?,?,?,0)", (hashlib.sha256(tok.encode()).hexdigest(), m["id"],
                     (dt.datetime.utcnow() + dt.timedelta(minutes=LINK_MINUTES)).isoformat())); db().commit()
        link = (PUBLIC_URL.rstrip("/") if PUBLIC_URL else request.host_url.rstrip("/")) + "/auth/" + tok
        if smtp_ready():
            try: send_email(email, "Your Grunions login link", f"Hi {display_first(m)},\n\nTap to sign in to the Grunions team app:\n{link}\n\n"
                            f"This link works once and expires in {LINK_MINUTES} minutes. If you didn't ask for it, ignore this email.\n\nGrunions Water Polo")
            except Exception as e: app.logger.error("login email to %s failed: %s", email, e)
        elif DEV_SHOW_LINKS: app.logger.warning("MAGIC LINK for %s: %s", email, link)
        else: app.logger.error("No SMTP configured; login link for %s not sent", email)
    msg = f"If that email is on the team, a login link is on its way (valid {LINK_MINUTES} minutes)."
    if DEV_SHOW_LINKS and link: msg += f'<br><b>Dev mode:</b> <a href="{link}">open your login link</a>'
    flash(msg); return redirect("/login")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST": return send_link((request.form.get("email") or "").strip().lower())
    return page(T["login"])

@app.route("/auth/<tok>")
def auth(tok):
    d = db(); h = hashlib.sha256(tok.encode()).hexdigest()
    r = d.execute("SELECT * FROM login_tokens WHERE token_hash=?", (h,)).fetchone()
    if not r or r["used"] or r["expires"] < dt.datetime.utcnow().isoformat():
        flash("That login link is invalid or expired. Request a new one."); return redirect("/login")
    d.execute("UPDATE login_tokens SET used=1 WHERE token_hash=?", (h,)); d.commit()
    start_session(r["member_id"]); return redirect("/home")
# ---------- Sign in with Google (OpenID Connect) ----------
GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID"); GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET")
oauth = None
def google_enabled(): return bool(GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET)
def google_client():
    global oauth
    if oauth is None:
        from authlib.integrations.flask_client import OAuth
        oauth = OAuth(app)
        oauth.register("google", client_id=GOOGLE_CLIENT_ID, client_secret=GOOGLE_CLIENT_SECRET,
                       server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
                       client_kwargs={"scope": "openid email profile"})
    return oauth.google
def google_redirect_uri(): return (PUBLIC_URL.rstrip("/") if PUBLIC_URL else request.host_url.rstrip("/")) + "/auth/google/callback"
def google_authorize_redirect():  # Authlib stores state + nonce in the session and checks them on return
    return google_client().authorize_redirect(google_redirect_uri(), nonce=secrets.token_urlsafe(16), prompt="select_account")
def google_userinfo():  # exchanges the code, verifies state, ID-token signature, audience and nonce
    return google_client().authorize_access_token().get("userinfo") or {}
app.jinja_env.globals.update(google_enabled=google_enabled)

@app.route("/auth/google")
def auth_google():
    if not google_enabled(): abort(404)
    return google_authorize_redirect()

@app.route("/auth/google/callback")
def auth_google_callback():
    if not google_enabled(): abort(404)
    try: info = google_userinfo()
    except Exception as e:
        app.logger.warning("Google sign-in failed: %s", e); session.clear(); flash("Google sign-in didn't work. Try again or use an email link."); return redirect("/login")
    email = (info.get("email") or "").strip().lower()
    if not email or info.get("email_verified") not in (True, "true"):
        session.clear(); flash("Your Google email isn't verified. Use an email login link instead."); return redirect("/login")
    d = db(); m = d.execute("SELECT * FROM members WHERE lower(email)=?", (email,)).fetchone()
    # Google never creates an account. /join sets joined. An existing admin can still sign in.
    if m and (m["role"] or "") != "system" and (m["joined"] or m["is_admin"]):
        start_session(m["id"]); return redirect("/home")
    session.clear()
    flash(Markup("We couldn't find a Grunions registration for ") + escape(email) + Markup(
        '. Sign up first at /join using this email, or sign in with the email you registered with.'
        '<a class="btn primary full" href="/join" style="margin-top:12px">Sign up</a>'))
    return redirect("/login")

@app.route("/logout")
def logout(): session.clear(); return redirect("/login")

# ---------- member ----------
@app.route("/home", methods=["GET", "POST"])
@login_required
def home():
    m = me(); d = db()
    if request.method == "POST" and request.form.get("action") == "reverify_background":
        flash(create_verify_request(d, m["id"], update_pending=True)); return redirect("/home")
    if request.method == "POST" and request.form.get("action") == "preferred":
        d.execute("UPDATE members SET preferred_first=? WHERE id=?", (clean_preferred(request.form.get("preferred_first")), m["id"]))
        d.commit(); sync_practice_sheets(d); flash("Preferred name saved."); return redirect("/home")
    if request.method == "POST" and request.form.get("action") == "avatar":
        f = request.files.get("photo")
        if not f or not f.filename:
            flash("Choose a picture."); return redirect("/home")
        try: stored = save_image(f)
        except ValueError as e:
            flash(str(e)); return redirect("/home")
        d.execute("UPDATE members SET photo=? WHERE id=?", (stored, m["id"]))
        d.commit(); flash("Profile picture saved.", "toast"); return redirect("/home")
    if request.method == "POST" and request.form.get("action") == "avatar_clear":
        d.execute("UPDATE members SET photo='' WHERE id=?", (m["id"],))
        d.commit(); return redirect("/home")
    if request.method == "POST" and request.form.get("action") == "trial":
        row = d.execute("SELECT usawp_number, usawp_status, trial_acknowledged_at FROM members WHERE id=?", (m["id"],)).fetchone()
        if (row["usawp_status"] or "") == "verified" or (row["usawp_number"] or "").strip() or (row["trial_acknowledged_at"] or "").strip():
            return redirect("/home")
        now = stamp_pt()
        d.execute("""UPDATE members SET trial_acknowledged_at=? WHERE id=?
            AND (trial_acknowledged_at IS NULL OR trial_acknowledged_at='')
            AND (usawp_number IS NULL OR trim(usawp_number)='')
            AND COALESCE(usawp_status,'')!='verified'""", (now, m["id"]))
        if d.execute("SELECT changes()").fetchone()[0]: flash("2-week USAWP trial started", "toast")
        d.commit(); sync_practice_sheets(d); return redirect("/home")
    if request.method == "POST":
        until = m["usawp_valid_until"] or ""
        if (m["usawp_status"] or "") == "verified" and not (until and until < today_pt().isoformat()):
            flash("Your USAWP number is already verified."); return redirect("/home")
        num = (request.form.get("usawp_number") or "").strip()
        if not re.fullmatch(r"[0-9]{4,10}", num):
            flash("Membership number must be 4-10 digits."); return redirect("/home")
        since = (dt.datetime.now() - dt.timedelta(hours=1)).isoformat(timespec="seconds")
        if d.execute("SELECT COUNT(*) FROM usawp_submits WHERE member_id=? AND at>=?", (m["id"], since)).fetchone()[0] >= 3:
            flash("You can only submit a membership number 3 times per hour."); return redirect("/home")
        d.execute("UPDATE members SET usawp_number=? WHERE id=?", (num, m["id"]))
        d.execute("INSERT INTO usawp_submits(member_id, at) VALUES(?,?)", (m["id"], dt.datetime.now().isoformat(timespec="seconds")))
        bg_exp = parse_date(request.form.get("background_expires"))
        if bg_exp: save_background_expiry(d, m["id"], bg_exp, display_first(m) + " " + (m["last"] or ""))
        create_verify_request(d, m["id"], update_pending=True)
        sync_practice_sheets(d)
        flash("Sent to Grunions for verification", "toast")
        return redirect("/home")
    return combined_view("home")

@app.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    m = me(); d = db()
    if request.method == "POST" and request.form.get("action") == "save":
        phone = normalize_phone(request.form.get("phone"))
        if not phone:
            flash("Enter a 10-digit US phone number.", "toast"); return redirect("/profile")
        new_num = None
        if "usawp_number" in request.form:
            num = (request.form.get("usawp_number") or "").strip()
            current = (m["usawp_number"] or "").strip()
            if num != current:
                until = m["usawp_valid_until"] or ""
                if (m["usawp_status"] or "") == "verified" and not (until and until < today_pt().isoformat()):
                    flash("Your USAWP number is already verified."); return redirect("/profile")
                if not re.fullmatch(r"[0-9]{4,10}", num):
                    flash("Membership number must be 4-10 digits."); return redirect("/profile")
                since = (dt.datetime.now() - dt.timedelta(hours=1)).isoformat(timespec="seconds")
                if d.execute("SELECT COUNT(*) FROM usawp_submits WHERE member_id=? AND at>=?", (m["id"], since)).fetchone()[0] >= 3:
                    flash("You can only submit a membership number 3 times per hour."); return redirect("/profile")
                new_num = num
        try:
            photo = None
            f = request.files.get("photo")
            if f and f.filename: photo = save_image(f)
            d.execute("UPDATE members SET preferred_first=?, phone=? WHERE id=?", (clean_preferred(request.form.get("preferred_first")), phone, m["id"]))
            if photo: d.execute("UPDATE members SET photo=? WHERE id=?", (photo, m["id"]))
            elif request.form.get("photo_clear") == "1": d.execute("UPDATE members SET photo='' WHERE id=?", (m["id"],))
            if new_num:
                d.execute("UPDATE members SET usawp_number=? WHERE id=?", (new_num, m["id"]))
                d.execute("INSERT INTO usawp_submits(member_id, at) VALUES(?,?)", (m["id"], dt.datetime.now().isoformat(timespec="seconds")))
            d.commit(); sync_practice_sheets(d)
            if new_num:
                create_verify_request(d, m["id"], update_pending=True)
                flash("Sent to Grunions for verification", "toast")
            else:
                flash("Saved", "toast")
        except ValueError as e:
            d.rollback(); flash(str(e))
        return redirect("/profile")
    hist = d.execute("SELECT practice_date FROM checkins WHERE member_id=?", (m["id"],)).fetchall()
    month = today_pt().strftime("%Y-%m")
    vr_pending = d.execute("SELECT 1 FROM verify_requests WHERE member_id=? AND status='pending'", (m["id"],)).fetchone() is not None
    ptab = (request.args.get("tab") or "general").strip()
    if ptab not in ("general", "interested", "mine"): ptab = "general"
    hosts = d.execute("SELECT 1 FROM lineup_events WHERE created_by=? OR host_id=? LIMIT 1", (m["id"], m["id"])).fetchone() is not None
    if ptab == "mine" and not hosts: ptab = "general"
    prof_upcoming, prof_past, prof_past_n = ([], [], 0)
    if ptab in ("interested", "mine"):
        prof_upcoming, prof_past, prof_past_n = profile_lineup(d, m["id"], ptab)
    return page(T["profile"], tab="profile", m=m, hist=hist, nmonth=sum(1 for h in hist if h["practice_date"].startswith(month)), vr_pending=vr_pending,
        ptab=ptab, hosts=hosts, prof_upcoming=prof_upcoming, prof_past=prof_past, prof_past_n=prof_past_n, prof_back="/profile?tab=" + ptab)

# ---------- unread badges ----------
def empty_unread():
    return {"team": 0, "coaches": 0, "chat": 0, "schedule": 0, "total": 0, "practices": {}}
def seed_chat_reads(d):
    """Baseline every member at the latest message so existing history is not a badge storm."""
    for ch in ("team", "coaches"):
        mx = d.execute("SELECT COALESCE(MAX(id),0) FROM messages WHERE channel=?", (ch,)).fetchone()[0]
        d.execute("""INSERT OR IGNORE INTO chat_reads(member_id, channel, last_read)
            SELECT id, ?, ? FROM members WHERE COALESCE(role,'')!='system'""", (ch, mx))
def mark_chat_read(d, mid, channel):
    mx = d.execute("SELECT COALESCE(MAX(id),0) FROM messages WHERE channel=?", (channel,)).fetchone()[0]
    d.execute("""INSERT INTO chat_reads(member_id, channel, last_read) VALUES(?,?,?)
        ON CONFLICT(member_id, channel) DO UPDATE SET last_read=MAX(chat_reads.last_read, excluded.last_read)""",
        (mid, channel, mx))
    d.commit()
def chat_unread_n(d, mid, channel):
    row = d.execute("SELECT last_read FROM chat_reads WHERE member_id=? AND channel=?", (mid, channel)).fetchone()
    if not row: return 0
    return d.execute("SELECT COUNT(*) FROM messages WHERE channel=? AND id>? AND member_id!=?", (channel, row["last_read"], mid)).fetchone()[0]
def ensure_cancel_notices(d, mid):
    """One unseen cancel row per practice still on the schedule. Existing seen_at values stay put."""
    d.execute("""INSERT OR IGNORE INTO practice_notices(practice_id, member_id, kind, seen_at)
        SELECT id, ?, 'cancel', NULL FROM practices WHERE cancelled=1 AND """ + upcoming_where(), (mid, *upcoming_bounds()))
    if d.execute("SELECT changes()").fetchone()[0]: d.commit()
def flag_practice(d, pid, kind, actor_id):
    """Record a cancellation or edit. The person who made it has already seen it."""
    now = dt.datetime.now().isoformat(timespec="seconds")
    for r in d.execute("SELECT id FROM members WHERE COALESCE(role,'')!='system'"):
        seen = now if r["id"] == actor_id else None
        d.execute("""INSERT INTO practice_notices(practice_id, member_id, kind, seen_at) VALUES(?,?,?,?)
            ON CONFLICT(practice_id, member_id, kind) DO UPDATE SET seen_at=excluded.seen_at""",
            (pid, r["id"], kind, seen))
def mark_practice_seen(d, mid, pid):
    now = dt.datetime.now().isoformat(timespec="seconds")
    d.execute("UPDATE practice_notices SET seen_at=? WHERE member_id=? AND practice_id=? AND seen_at IS NULL", (now, mid, pid))
def compute_unread(d, member):
    mid = member["id"]
    staff = bool(member["is_admin"] or member["role"] == "coach")
    ensure_cancel_notices(d, mid)
    team = chat_unread_n(d, mid, "team")
    coaches = chat_unread_n(d, mid, "coaches") if staff else 0
    rows = d.execute("""SELECT n.practice_id AS practice_id, COUNT(*) AS cnt FROM practice_notices n
        JOIN practices p ON p.id=n.practice_id
        WHERE n.member_id=? AND n.seen_at IS NULL AND """ + upcoming_where("p") + " GROUP BY n.practice_id", (mid, *upcoming_bounds())).fetchall()
    practices = {str(r["practice_id"]): r["cnt"] for r in rows}
    schedule = sum(practices.values())
    chat = team + coaches
    return {"team": team, "coaches": coaches, "chat": chat, "schedule": schedule, "total": chat + schedule, "practices": practices}
def unread_for_me():
    m = me()
    if not m: return empty_unread()
    if getattr(g, "_unread_mid", None) == m["id"]: return g._unread
    g._unread = compute_unread(db(), m)
    g._unread_mid = m["id"]
    return g._unread
app.jinja_env.globals.update(badges=unread_for_me)

# ---------- chat ----------
MSG_FROM = """FROM messages m JOIN members p ON p.id=m.member_id
  LEFT JOIN messages rm ON rm.id=m.reply_to LEFT JOIN members rp ON rp.id=rm.member_id"""
def msg_dict(r):
    deleted = bool(r["deleted"]) if "deleted" in r.keys() and r["deleted"] else False
    edited = bool(r["edited_at"]) if "edited_at" in r.keys() and r["edited_at"] else False
    mine = r["member_id"] == me()["id"]
    reply = None
    if "reply_to" in r.keys() and r["reply_to"] and "rfirst" in r.keys() and r["rfirst"]:
        who = display_first({"first": r["rfirst"], "last": r["rlast"], "preferred_first": r["rpref"]})
        if r["reply_deleted"]: text = "Message deleted"
        elif (r["reply_body"] or "").strip(): text = (r["reply_body"] or "").strip()[:140]
        elif r["reply_image"]: text = "Photo"
        else: text = ""
        reply = {"id": r["reply_to"], "who": "%s %s." % (who, (r["rlast"] or "")[:1]), "body": text}
    return {"id": r["id"], "uid": r["member_id"], "body": "" if deleted else (r["body"] or ""), "ann": bool(r["announcement"]), "at": (r["at"] or "") + "Z",
            "who": f'{display_first(r)} {r["last"][:1]}.', "mine": mine, "admin": bool(r["is_admin"]),
            "edited": edited and not deleted, "deleted": deleted, "can_delete": (mine or bool(me()["is_admin"])) and not deleted,
            "reply": reply,
            "image": None if deleted or not r["image"] else {"thumb": f"/media/{r['id']}/thumb", "full": f"/media/{r['id']}/full"}}
def load_message(d, mid):
    return d.execute("""SELECT m.*, p.first, p.last, p.is_admin, p.preferred_first,
        rm.body AS reply_body, rm.deleted AS reply_deleted, rm.image AS reply_image,
        rp.first AS rfirst, rp.last AS rlast, rp.preferred_first AS rpref """ + MSG_FROM + " WHERE m.id=?", (mid,)).fetchone()
def valid_emoji(e):
    """One emoji, including a picker choice. Words and empty strings are not."""
    if not isinstance(e, str): return False
    e = e.strip()
    if not e or len(e) > 32: return False
    if re.search(r"[A-Za-z0-9]", e): return False
    return any(ord(c) > 127 for c in e)
def reply_target(d, ch, raw):
    try: rid = int(raw)
    except (TypeError, ValueError): return None
    src = d.execute("SELECT id, channel, deleted FROM messages WHERE id=?", (rid,)).fetchone()
    if not src or src["deleted"] or (src["channel"] or "team") != ch: return None
    return src["id"]
def can_read(ch): return ch == "team" or (ch == "coaches" and is_staff())
def channel_members(d, channel):
    """Who a read receipt counts. Team is everyone. Coaches is coaches and admins."""
    rows = d.execute("""SELECT id, first, last, preferred_first, photo, role, is_admin FROM members
        WHERE COALESCE(role,'')!='system'""").fetchall()
    if channel == "coaches":
        return [r for r in rows if (r["role"] or "") == "coach" or r["is_admin"]]
    return list(rows)
def member_brief(m):
    photo = ""
    try:
        if "photo" in m.keys(): photo = m["photo"] or ""
    except (AttributeError, TypeError):
        photo = ""
    return {"id": m["id"], "name": ("%s %s" % (display_first(m), m["last"] or "")).strip(),
            "initials": initials(m), "photo": ("/avatar/%d?v=%s" % (m["id"], photo)) if photo else ""}
def seen_summary(d, channel, message_id, sender_id):
    """Who else in the channel has a last-read at or past this message. The sender is never counted."""
    others = [m for m in channel_members(d, channel) if m["id"] != sender_id]
    others.sort(key=lambda m: (display_first(m).casefold(), (m["last"] or "").casefold(), m["id"]))
    if not others or not message_id: return None
    reads = {r["member_id"]: r["last_read"] for r in d.execute(
        "SELECT member_id, last_read FROM chat_reads WHERE channel=?", (channel,))}
    seen = [member_brief(m) for m in others if reads.get(m["id"], 0) >= message_id]
    n = len(seen)
    label = "Seen by everyone" if n == len(others) else "Seen by %d" % n
    return {"id": message_id, "n": n, "total": len(others), "label": label, "seen": seen}
def with_seen(d, channel, rows):
    latest = d.execute("""SELECT id, member_id FROM messages WHERE channel=? AND COALESCE(deleted,0)=0
        ORDER BY id DESC LIMIT 1""", (channel,)).fetchone()
    info = seen_summary(d, channel, latest["id"], latest["member_id"]) if latest else None
    out = []
    for r in rows:
        item = msg_dict(r)
        if info and item["id"] == info["id"]: item["seen"] = info
        out.append(item)
    return out
def save_image(f):
    """Validate + re-encode an upload. Returns stored base name. Strips metadata, fixes rotation, resizes (max 1600px, thumb 480px)."""
    from PIL import Image, ImageOps
    try:
        import pillow_heif; pillow_heif.register_heif_opener()
    except ImportError: pass
    data = f.read(MAX_UPLOAD + 1)
    if len(data) > MAX_UPLOAD: raise ValueError("Image is larger than 8 MB.")
    try:
        im = Image.open(io.BytesIO(data)); fmt = (im.format or "").upper(); im.load()
    except Exception: raise ValueError("That file isn't a supported image.")
    if fmt not in ("JPEG", "PNG", "GIF", "WEBP", "HEIF", "HEIC"): raise ValueError("Use JPG, PNG, GIF, WEBP or HEIC.")
    os.makedirs(UPLOADS, exist_ok=True); name = secrets.token_hex(12)
    if fmt == "GIF" and getattr(im, "is_animated", False) and len(data) <= MAX_UPLOAD:
        open(os.path.join(UPLOADS, name + ".gif"), "wb").write(data); ext = "gif"   # keep animation
    else:
        im = ImageOps.exif_transpose(im); im = im.convert("RGBA" if im.mode in ("RGBA", "LA", "P") and fmt in ("PNG", "WEBP", "GIF") else "RGB")
        im.thumbnail((1600, 1600)); im.save(os.path.join(UPLOADS, name + ".webp"), "WEBP", quality=85); ext = "webp"
    th = Image.open(os.path.join(UPLOADS, f"{name}.{ext}")); th = th.convert("RGBA" if th.mode in ("RGBA", "P") else "RGB"); th.thumbnail((480, 480))
    th.save(os.path.join(UPLOADS, name + "_t.webp"), "WEBP", quality=80)
    return f"{name}.{ext}"
def save_banner(f):
    """Event banner: center-crop to 3:2, longest edge 1600, stored on the uploads disk."""
    from PIL import Image, ImageOps
    try:
        import pillow_heif; pillow_heif.register_heif_opener()
    except ImportError: pass
    data = f.read(MAX_UPLOAD + 1)
    if len(data) > MAX_UPLOAD: raise ValueError("Image is larger than 8 MB.")
    try:
        im = Image.open(io.BytesIO(data)); fmt = (im.format or "").upper(); im.load()
    except Exception: raise ValueError("That file isn't a supported image.")
    if fmt not in ("JPEG", "PNG", "GIF", "WEBP", "HEIF", "HEIC"): raise ValueError("Use JPG, PNG, GIF, WEBP or HEIC.")
    im = ImageOps.exif_transpose(im)
    im = im.convert("RGB")
    w, h = im.size
    if w < 1 or h < 1: raise ValueError("That file isn't a supported image.")
    if w / h > 1.5:
        nw = int(round(h * 1.5)); left = max(0, (w - nw) // 2); im = im.crop((left, 0, left + nw, h))
    elif h / w > (2 / 3):
        nh = int(round(w / 1.5)); top = max(0, (h - nh) // 2); im = im.crop((0, top, w, top + nh))
    im.thumbnail((1600, 1600))
    os.makedirs(UPLOADS, exist_ok=True); name = secrets.token_hex(12)
    im.save(os.path.join(UPLOADS, name + ".webp"), "WEBP", quality=82)
    return name + ".webp"
@app.route("/media/<int:mid>/<kind>")
@login_required
def media(mid, kind):
    r = db().execute("SELECT channel, image, deleted FROM messages WHERE id=?", (mid,)).fetchone()
    if not r or not r["image"] or r["deleted"] or kind not in ("thumb", "full"): abort(404)
    if not can_read(r["channel"]): abort(403)
    from flask import send_from_directory
    fn = r["image"].rsplit(".", 1)[0] + "_t.webp" if kind == "thumb" else r["image"]
    resp = send_from_directory(UPLOADS, fn, max_age=86400); resp.headers["Cache-Control"] = "private, max-age=86400"; return resp
def _stored_file(name):
    base = os.path.basename(str(name or ""))
    if not base or base != name or not os.path.isfile(os.path.join(UPLOADS, base)): return None
    return base
@app.route("/avatar/<int:mid>")
@login_required
def avatar(mid):
    r = db().execute("SELECT photo FROM members WHERE id=?", (mid,)).fetchone()
    fn = _stored_file(r["photo"] if r else "")
    if not fn: abort(404)
    resp = send_from_directory(UPLOADS, fn, max_age=86400)
    resp.headers["Cache-Control"] = "private, max-age=86400"
    return resp
@app.route("/practice-image/<int:pid>")
@login_required
def practice_image(pid):
    r = db().execute("SELECT image FROM practices WHERE id=?", (pid,)).fetchone()
    fn = _stored_file(r["image"] if r else "")
    if not fn: abort(404)
    resp = send_from_directory(UPLOADS, fn, max_age=86400)
    resp.headers["Cache-Control"] = "private, max-age=86400"
    return resp
def apply_practice_image(d, pid):
    """Replace or remove the Home-card image. An empty upload leaves the current picture."""
    f = request.files.get("image")
    if f and f.filename:
        d.execute("UPDATE practices SET image=? WHERE id=?", (save_image(f), pid))
        return True
    if request.form.get("image_clear"):
        d.execute("UPDATE practices SET image='' WHERE id=?", (pid,))
        return True
    return False
@app.errorhandler(413)
def too_big(e): return jsonify(error="Image is larger than 8 MB."), 413
@app.route("/api/messages/<int:mid>/react", methods=["POST"])
@login_required
def react(mid):
    d = db(); r = d.execute("SELECT channel, deleted FROM messages WHERE id=?", (mid,)).fetchone()
    if not r: abort(404)
    ch = r["channel"] or "team"
    if not can_read(ch): abort(403)
    if r["deleted"]: return jsonify(error="This message was deleted"), 400
    e = (request.get_json(silent=True) or {}).get("emoji")
    if not valid_emoji(e): return jsonify(error="unsupported emoji"), 400
    have = [row["emoji"] for row in d.execute("SELECT emoji FROM reactions WHERE message_id=? AND member_id=?", (mid, me()["id"]))]
    d.execute("DELETE FROM reactions WHERE message_id=? AND member_id=?", (mid, me()["id"]))
    if have != [e]:
        d.execute("INSERT INTO reactions VALUES(?,?,?)", (mid, me()["id"], e))
    d.commit(); return jsonify(reactions_for(d, ch).get(str(mid), {}))
@app.route("/api/messages/<int:mid>/reactors")
@login_required
def reactors(mid):
    d = db(); r = d.execute("SELECT channel FROM messages WHERE id=?", (mid,)).fetchone()
    if not r: abort(404)
    ch = r["channel"] or "team"
    if not can_read(ch): abort(403)
    e = request.args.get("emoji") or ""
    people = [member_brief(m) for m in d.execute("""SELECT p.id, p.first, p.last, p.preferred_first, p.photo
        FROM reactions x JOIN members p ON p.id=x.member_id
        WHERE x.message_id=? AND x.emoji=? ORDER BY p.last, p.first""", (mid, e))]
    return jsonify(emoji=e, people=people)
@app.route("/api/messages/<int:mid>", methods=["POST", "DELETE"])
@login_required
def api_message_one(mid):
    """Edit (author only) or soft-delete (author, or an admin in team and coaches chat)."""
    d = db()
    r = load_message(d, mid)
    if not r: abort(404)
    ch = r["channel"] or "team"
    if not can_read(ch): abort(403)
    if request.method == "DELETE":
        if r["member_id"] != me()["id"] and not me()["is_admin"]: abort(403)
        if not r["deleted"]:
            d.execute("UPDATE messages SET deleted=1, body='' WHERE id=?", (mid,))
            d.execute("DELETE FROM reactions WHERE message_id=?", (mid,))
            d.commit()
        return jsonify(ok=True, message=msg_dict(load_message(d, mid)))
    if r["member_id"] != me()["id"]: abort(403)
    if r["deleted"]: return jsonify(error="This message was deleted"), 400
    body = ((request.get_json(silent=True) or {}).get("body") or "").strip()[:2000]
    if not body and not r["image"]: return jsonify(error="empty"), 400
    if body != (r["body"] or ""):
        d.execute("UPDATE messages SET body=?, edited_at=? WHERE id=?", (body, stamp_pt(), mid))
        d.commit()
    return jsonify(ok=True, message=msg_dict(load_message(d, mid)))
def reactions_for(d, ch):
    out = {}
    for x in d.execute("""SELECT x.message_id, x.emoji, COUNT(*) n, SUM(x.member_id=?) mine FROM reactions x JOIN messages m ON m.id=x.message_id
        WHERE m.channel=? AND COALESCE(m.deleted,0)=0 AND m.id > (SELECT COALESCE(MAX(id),0)-300 FROM messages WHERE channel=?) GROUP BY x.message_id, x.emoji""", (me()["id"], ch, ch)):
        out.setdefault(str(x["message_id"]), {})[x["emoji"]] = {"n": x["n"], "mine": bool(x["mine"])}
    return out
@app.route("/api/reactions")
@login_required
def api_reactions():
    ch = request.args.get("c", "team")
    if ch not in ("team", "coaches") or not can_read(ch): abort(403)
    return jsonify(reactions_for(db(), ch))
@app.route("/chat")
@login_required
def chat():
    ch = request.args.get("c", "team")
    if ch == "coaches" and not is_staff(): abort(403)
    if ch not in ("team", "coaches"): ch = "team"
    mark_chat_read(db(), me()["id"], ch)
    return page(T["chat"], tab="chat", ch=ch)
@app.route("/api/messages", methods=["GET", "POST"])
@login_required
def api_messages():
    d = db(); ch = request.args.get("c", "team")
    if ch not in ("team", "coaches") or (ch == "coaches" and not is_staff()): abort(403)
    if request.method == "POST":
        image = None
        if request.files.get("image"):
            j = request.form
            try: image = save_image(request.files["image"])
            except ValueError as e: return jsonify(error=str(e)), 400
        else: j = request.get_json(silent=True) or {}
        body = (j.get("body") or "").strip()[:2000]
        if not body and not image: abort(400)
        ann = 1 if (j.get("announcement") in (True, "true", "1") and me()["is_admin"] and ch == "team") else 0
        d.execute("INSERT INTO messages(member_id,body,announcement,channel,image,reply_to) VALUES(?,?,?,?,?,?)", (me()["id"], body, ann, ch, image, reply_target(d, ch, j.get("reply_to")))); d.commit()
        mark_chat_read(d, me()["id"], ch)
        try: notify_chat(d, ch, me(), body, bool(image))
        except Exception as e: app.logger.warning("chat push failed: %s", e)
        return jsonify(ok=True)
    mark_chat_read(d, me()["id"], ch)
    if request.args.get("sync") == "1":
        rows = d.execute("""SELECT m.*, p.first, p.last, p.is_admin, p.preferred_first,
          rm.body AS reply_body, rm.deleted AS reply_deleted, rm.image AS reply_image,
          rp.first AS rfirst, rp.last AS rlast, rp.preferred_first AS rpref """ + MSG_FROM + """
          WHERE m.channel=? ORDER BY m.id DESC LIMIT 80""", (ch,)).fetchall()
        return jsonify(with_seen(d, ch, list(reversed(rows))))
    after = request.args.get("after", 0, type=int)
    rows = d.execute("""SELECT m.*, p.first, p.last, p.is_admin, p.preferred_first,
      rm.body AS reply_body, rm.deleted AS reply_deleted, rm.image AS reply_image,
      rp.first AS rfirst, rp.last AS rlast, rp.preferred_first AS rpref """ + MSG_FROM + """
      WHERE m.id>? AND m.channel=? ORDER BY m.id DESC LIMIT 200""", (after, ch)).fetchall()
    return jsonify(with_seen(d, ch, list(reversed(rows))))

# ---------- practices ----------
RECURRING = {1: ("Marina High School", "19:00", "20:30"), 4: ("Westminster High School", "19:00", "20:30")}  # Tue, Fri
def ensure_schedule(d, weeks=4):
    today = today_pt()
    for i in range(weeks * 7):
        day = today + dt.timedelta(days=i)
        if day.weekday() in RECURRING:
            loc, a, b = RECURRING[day.weekday()]
            d.execute("INSERT OR IGNORE INTO practices(date,start,end,location) VALUES(?,?,?,?)", (day.isoformat(), a, b, loc))
    sync_all_series(d)
    d.commit()
    pin_known_pools(d)
    d.commit()
SERIES_HORIZON_DAYS = 56
WEEKDAYS = ("Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun")
def series_weekday_set(raw):
    return {int(x) for x in str(raw or "").split(",") if str(x).strip().isdigit()}
def series_horizon(row, today):
    start = dt.date.fromisoformat(row["start_date"])
    cap = today + dt.timedelta(days=180)
    if row["end_date"]:
        end = min(dt.date.fromisoformat(row["end_date"]), cap)
    else:
        end = min(today + dt.timedelta(days=SERIES_HORIZON_DAYS), cap)
    return max(start, today), end
def series_dates(row, today=None):
    today = today or today_pt()
    begin, end = series_horizon(row, today)
    if end < begin: return []
    wanted = series_weekday_set(row["weekdays"])
    days, day = [], begin
    while day <= end:
        if day.weekday() in wanted: days.append(day)
        day += dt.timedelta(days=1)
    return days
def delete_practice_row(d, pid):
    d.execute("DELETE FROM practice_coaches WHERE practice_id=?", (pid,))
    d.execute("DELETE FROM rsvps WHERE practice_id=?", (pid,))
    d.execute("DELETE FROM social_joins WHERE practice_id=?", (pid,))
    d.execute("DELETE FROM practice_notices WHERE practice_id=?", (pid,))
    d.execute("DELETE FROM practices WHERE id=?", (pid,))
def replace_series_coaches(d, sid, raw, lead=None):
    allowed = {r["id"] for r in coach_candidates(d)}
    chosen = []
    for x in raw or []:
        try: i = int(x)
        except (TypeError, ValueError): continue
        if i in allowed and i not in chosen: chosen.append(i)
    try: lead_id = int(lead) if lead else None
    except (TypeError, ValueError): lead_id = None
    if lead_id not in chosen: lead_id = None
    d.execute("DELETE FROM series_coaches WHERE series_id=?", (sid,))
    if chosen:
        d.executemany("INSERT INTO series_coaches(series_id, member_id, is_lead) VALUES(?,?,?)",
                      [(sid, i, 1 if i == lead_id else 0) for i in chosen])
def copy_series_coaches(d, sid, pid):
    rows = d.execute("SELECT member_id, is_lead FROM series_coaches WHERE series_id=?", (sid,)).fetchall()
    save_practice_coaches(d, pid, [r["member_id"] for r in rows], lead=next((r["member_id"] for r in rows if r["is_lead"]), None),
                          focuses={r["member_id"]: "" for r in rows})
def practice_has_rsvps(d, pid):
    return d.execute("SELECT COUNT(*) FROM rsvps WHERE practice_id=?", (pid,)).fetchone()[0] > 0
def sync_series(d, sid, today=None):
    """Create missing occurrences and drop dates the series no longer includes. A skipped date with RSVPs stays, marked Cancelled."""
    row = d.execute("SELECT * FROM practice_series WHERE id=?", (sid,)).fetchone()
    if not row: return
    today = today or today_pt()
    wanted = series_weekday_set(row["weekdays"])
    start_d = dt.date.fromisoformat(row["start_date"])
    end_d = dt.date.fromisoformat(row["end_date"]) if row["end_date"] else None
    skips = {r["date"] for r in d.execute("SELECT date FROM series_skips WHERE series_id=?", (sid,))}
    for p in d.execute("SELECT * FROM practices WHERE series_id=?", (sid,)):
        day = dt.date.fromisoformat(p["date"])
        if p["date"] in skips:
            if practice_has_rsvps(d, p["id"]):
                if not p["cancelled"]: d.execute("UPDATE practices SET cancelled=1, skipped=1 WHERE id=?", (p["id"],))
            elif not p["skipped"]:
                delete_practice_row(d, p["id"])
            continue
        if p["series_detached"]: continue
        outside = day.weekday() not in wanted or day < start_d or (end_d is not None and day > end_d)
        if outside:
            if practice_has_rsvps(d, p["id"]):
                d.execute("UPDATE practices SET cancelled=1, skipped=1 WHERE id=?", (p["id"],))
                d.execute("INSERT OR IGNORE INTO series_skips(series_id, date) VALUES(?,?)", (sid, p["date"]))
            else:
                delete_practice_row(d, p["id"])
            continue
        if p["cancelled"]: continue
        try:
            sp = sports.sports_from_row(row)
            d.execute("""UPDATE practices SET start=?, end=?, location=?, activity_type=?, sport=?, title=?, skill_levels=?,
                divisions=?, division_custom=?, opponent=?, home_away=?, gameplay_notes=?, segments=?, comp_format=? WHERE id=?""",
                (row["start"], row["end"], row["location"], *sports.sports_tuple(sp), p["id"]))
        except sqlite3.IntegrityError:
            pass
    for day in series_dates(row, today):
        iso = day.isoformat()
        if iso in skips: continue
        if d.execute("SELECT 1 FROM practices WHERE series_id=? AND date=?", (sid, iso)).fetchone(): continue
        if d.execute("SELECT 1 FROM practices WHERE date=? AND location=?", (iso, row["location"])).fetchone(): continue
        try:
            sp = sports.sports_from_row(row)
            cur = d.execute("""INSERT INTO practices(date,start,end,location,series_id,activity_type,sport,title,skill_levels,divisions,division_custom,opponent,home_away,gameplay_notes,segments,comp_format)
                VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""", (iso, row["start"], row["end"], row["location"], sid, *sports.sports_tuple(sp)))
        except sqlite3.IntegrityError:
            continue
        copy_series_coaches(d, sid, cur.lastrowid)
def sync_all_series(d):
    for sid in [r["id"] for r in d.execute("SELECT id FROM practice_series")]:
        sync_series(d, sid)
def series_form_values(row=None, form=None, coaches=None):
    labels = [(str(i), WEEKDAYS[i]) for i in range(7)]
    if form is not None:
        return {"weekdays": form.getlist("weekday"), "start": form.get("start") or "19:00", "end": form.get("end") or "20:30",
                "location": form.get("location") or "", "start_date": form.get("start_date") or "", "end_date": form.get("end_date") or "",
                "coaches": [int(x) for x in form.getlist("coach") if str(x).isdigit()], "lead": form.get("lead") or "", "labels": labels}
    if row:
        chosen = [r["member_id"] for r in (coaches or [])]
        lead = next((str(r["member_id"]) for r in (coaches or []) if r["is_lead"]), "")
        return {"weekdays": [x for x in str(row["weekdays"]).split(",") if x], "start": row["start"], "end": row["end"],
                "location": row["location"], "start_date": row["start_date"], "end_date": row["end_date"] or "",
                "coaches": chosen, "lead": lead, "labels": labels}
    return {"weekdays": [], "start": "19:00", "end": "20:30", "location": "", "start_date": "", "end_date": "", "coaches": [], "lead": "", "labels": labels}
def save_series(d, sid=None):
    picked = []
    for x in request.form.getlist("weekday"):
        if str(x).isdigit() and 0 <= int(x) <= 6 and int(x) not in picked: picked.append(int(x))
    if not picked: raise ValueError("Choose at least one weekday.")
    start_t = (request.form.get("start") or "").strip()
    end_t = (request.form.get("end") or "").strip()
    if not re.fullmatch(r"\d{2}:\d{2}", start_t) or not re.fullmatch(r"\d{2}:\d{2}", end_t): raise ValueError("Add a start and end time.")
    loc = " ".join((request.form.get("location") or "").split())[:200]
    if not loc: raise ValueError("Add a location.")
    start = parse_date(request.form.get("start_date") or request.form.get("date"))
    if not start: raise ValueError("Add a start date.")
    end_raw = (request.form.get("end_date") or "").strip()
    end = parse_date(end_raw) if end_raw else None
    if end_raw and not end: raise ValueError("Add an end date.")
    if end and end < start: raise ValueError("End date must be on or after the start date.")
    weekdays = ",".join(str(n) for n in sorted(picked))
    end_iso = end.isoformat() if end else None
    sp = sports.sports_from_form(request.form)
    tup = sports.sports_tuple(sp)
    if sid:
        d.execute("""UPDATE practice_series SET weekdays=?, start=?, end=?, location=?, start_date=?, end_date=?,
            activity_type=?, sport=?, title=?, skill_levels=?, divisions=?, division_custom=?, opponent=?, home_away=?, gameplay_notes=?, segments=?, comp_format=? WHERE id=?""",
                  (weekdays, start_t, end_t, loc, start.isoformat(), end_iso, *tup, sid))
    else:
        sid = d.execute("""INSERT INTO practice_series(weekdays, start, end, location, start_date, end_date,
            activity_type, sport, title, skill_levels, divisions, division_custom, opponent, home_away, gameplay_notes, segments, comp_format)
            VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                        (weekdays, start_t, end_t, loc, start.isoformat(), end_iso, *tup)).lastrowid
    replace_series_coaches(d, sid, request.form.getlist("coach"), request.form.get("lead"))
    sync_series(d, sid)
    return sid
def apply_series_following(d, sid, from_date, start, end, loc, coach_ids, lead, sp=None):
    """Change this date and later occurrences. Earlier dates stay as they are."""
    if sp:
        d.execute("""UPDATE practice_series SET start=?, end=?, location=?, activity_type=?, sport=?, title=?, skill_levels=?,
            divisions=?, division_custom=?, opponent=?, home_away=?, gameplay_notes=?, segments=?, comp_format=? WHERE id=?""",
            (start, end, loc, *sports.sports_tuple(sp), sid))
    else:
        d.execute("UPDATE practice_series SET start=?, end=?, location=? WHERE id=?", (start, end, loc, sid))
    d.execute("UPDATE practices SET series_detached=1 WHERE series_id=? AND date<? AND COALESCE(series_detached,0)=0", (sid, from_date))
    replace_series_coaches(d, sid, coach_ids, lead)
    for p in d.execute("SELECT id FROM practices WHERE series_id=? AND date>=? AND COALESCE(cancelled,0)=0 AND COALESCE(skipped,0)=0", (sid, from_date)):
        try:
            if sp:
                d.execute("""UPDATE practices SET start=?, end=?, location=?, series_detached=0, activity_type=?, sport=?, title=?, skill_levels=?,
                    divisions=?, division_custom=?, opponent=?, home_away=?, gameplay_notes=?, segments=?, comp_format=? WHERE id=?""",
                    (start, end, loc, *sports.sports_tuple(sp), p["id"]))
            else:
                d.execute("UPDATE practices SET start=?, end=?, location=?, series_detached=0 WHERE id=?", (start, end, loc, p["id"]))
        except sqlite3.IntegrityError:
            continue
        prev = {r["member_id"]: (r["focus"] or "") for r in d.execute("SELECT member_id, focus FROM practice_coaches WHERE practice_id=?", (p["id"],))}
        save_practice_coaches(d, p["id"], coach_ids, lead=lead, focuses={i: prev.get(int(i), "") for i in coach_ids if str(i).isdigit()})
def fmt_t(t): h, m = map(int, t.split(":")); return f"{(h-1)%12+1}:{m:02d}{'pm' if h>=12 else 'am'}"
def fmt_clock(t):
    """7:00 PM, for the Home next-practice title."""
    h, m = map(int, str(t).split(":")[:2])
    return f"{(h-1)%12+1}:{m:02d} {'PM' if h >= 12 else 'AM'}"
def fmt_span(start, end):
    """7:00 – 8:30 PM. The first meridiem shows only when the two times differ."""
    def parts(t):
        h, m = map(int, str(t).split(":")[:2])
        return (h - 1) % 12 + 1, m, "PM" if h >= 12 else "AM"
    sh, sm, sa = parts(start)
    eh, em, ea = parts(end)
    left = "%d:%02d" % (sh, sm)
    if sa != ea: left += " " + sa
    return "%s – %d:%02d %s" % (left, eh, em, ea)
def weekday_abbr(s):
    return dt.date.fromisoformat(str(s)[:10]).strftime("%a").upper()
def month_abbr(s):
    return dt.date.fromisoformat(str(s)[:10]).strftime("%b").upper()
def day_num(s):
    return dt.date.fromisoformat(str(s)[:10]).day
def short_place(name):
    """Westminster High School becomes Westminster HS."""
    name = " ".join(str(name or "").split())
    for long, short in (("High School", "HS"), ("Middle School", "MS"), ("Elementary School", "ES")):
        if name.endswith(long): return (name[:-len(long)].strip() + " " + short).strip()
    return name
def fmt_d(s):
    d = dt.date.fromisoformat(s); return d.strftime("%a %b ") + str(d.day)
def fmt_card_date(s):
    """Tue, Nov 3. The comma sits on the Home time row."""
    d = dt.date.fromisoformat(str(s)[:10]); return d.strftime("%a, %b ") + str(d.day)
def practice_title(p):
    """Label from the activity type. A custom title wins. Unset rows are Practice."""
    if not p: return "Practice"
    data = sports.sports_from_row(p)
    return sports.activity_title(data["activity_type"], data["opponent"], data["segments"], data["title"])
def practice_sports_line(p):
    if not p: return ""
    data = sports.sports_from_row(p)
    return sports.sports_line(data["skill_levels"], data["divisions"], data["division_custom"], data["comp_format"])
def sports_editor(row=None, show_activity=True, show_format=False):
    """Shared activity, level, and division fields. Levels are an exact set."""
    data = sports.sports_from_row(row) if row is not None else {
        "activity_type": "practice", "sport": "Water Polo", "title": "", "skill_levels": "", "divisions": "",
        "division_custom": "", "opponent": "", "home_away": "", "gameplay_notes": "", "segments": "", "comp_format": ""}
    levels = set(data["skill_levels"].split(",")) if data["skill_levels"] else set()
    divs = set(data["divisions"].split(",")) if data["divisions"] else set()
    segs = sports.parse_segments(data["segments"])
    while len(segs) < 3: segs.append({"type": "", "start": "", "end": ""})
    parts = []
    if show_activity:
        parts.append('<div class=actseg role=group aria-label="Activity type">')
        for pid, name in sports.ACTIVITIES:
            checked = " checked" if data["activity_type"] == pid else ""
            parts.append('<label><input type=radio name=activity_type value="%s"%s><span>%s</span></label>' % (pid, checked, name))
        parts.append("</div>")
        parts.append('<label>Title<input name=title id=actTitle value="%s" placeholder="%s" autocomplete=off></label>' % (escape(data["title"]), escape(sports.activity_title(data["activity_type"], data["opponent"], data["segments"], ""))))
        parts.append('<label>Sport<input name=sport value="%s" autocomplete=off></label>' % escape(data["sport"] or "Water Polo"))
    parts.append('<div class=checks role=group aria-label="Skill levels"><div class="t3 xs">Skill levels</div>')
    parts.append('<label><input type=checkbox id=allLevels> All levels</label>')
    for pid, name, short, _full in sports.LEVELS:
        checked = " checked" if pid in levels else ""
        parts.append('<label><input type=checkbox name=level value="%s"%s> %s <span class="t3 sm">%s</span></label>' % (pid, checked, name, escape(short)))
    parts.append("</div>")
    parts.append('<div class=checks role=group aria-label="Division"><div class="t3 xs">Division <span class=t3>(optional)</span></div>')
    for pid, name in sports.DIVISIONS:
        checked = " checked" if pid in divs else ""
        parts.append('<label><input type=checkbox name=division value="%s"%s> %s</label>' % (pid, checked, name))
    parts.append('<label data-actcustom>Custom label<input name=division_custom value="%s" autocomplete=off></label></div>' % escape(data["division_custom"]))
    if show_activity:
        parts.append('<div data-act=game><label>Opponent<input name=opponent value="%s" autocomplete=off placeholder="Squid"></label>' % escape(data["opponent"]))
        parts.append('<label>Home / away<select name=home_away><option value="">Not set</option><option value=home%s>Home</option><option value=away%s>Away</option></select></label></div>' % (
            " selected" if data["home_away"] == "home" else "", " selected" if data["home_away"] == "away" else ""))
        parts.append('<div data-act=scrimmage><label>Gameplay notes<textarea name=gameplay_notes rows=2>%s</textarea></label></div>' % escape(data["gameplay_notes"]))
        parts.append('<div data-act=hybrid><div class="t3 xs">Segments</div>')
        for seg in segs[:3]:
            opts = "".join('<option value="%s"%s>%s</option>' % (pid, " selected" if seg["type"] == pid else "", name) for pid, name in sports.ACTIVITIES if pid != "hybrid")
            parts.append('<div class=row><label>Type<select name=segment_type><option value="">—</option>%s</select></label><label>Start<input type=time name=segment_start value="%s"></label><label>End<input type=time name=segment_end value="%s"></label></div>' % (opts, escape(seg["start"]), escape(seg["end"])))
        parts.append("</div>")
    if show_format:
        parts.append('<label>Registration<select name=comp_format><option value="">Not set</option>')
        for pid, name, blurb in sports.FORMATS:
            parts.append('<option value="%s"%s>%s</option>' % (pid, " selected" if data["comp_format"] == pid else "", name))
        parts.append("</select></label>")
        for _pid, name, blurb in sports.FORMATS:
            parts.append('<p class="t3 sm" style="margin:0 0 4px">%s — %s</p>' % (name, escape(blurb)))
    parts.append("""<script>(function(){
 var boxes=[].slice.call(document.querySelectorAll('input[name=level]'));
 var all=document.getElementById('allLevels');
 function syncAll(){ if(all) all.checked=boxes.length&&boxes.every(function(b){return b.checked}); }
 if(all) all.addEventListener('change', function(){ boxes.forEach(function(b){b.checked=all.checked}); });
 boxes.forEach(function(b){ b.addEventListener('change', syncAll); });
 syncAll();
 function kind(){ var r=document.querySelector('input[name=activity_type]:checked'); return r?r.value:'practice'; }
 function suggest(k, opp){ if(k==='scrimmage') return 'Scrimmage'; if(k==='game') return opp?('Game vs. '+opp):'Game'; if(k==='hybrid') return 'Practice + Scrimmage'; return 'Practice'; }
 document.querySelectorAll('[data-act]').forEach(function(el){ el.hidden=(el.getAttribute('data-act')||'').split(' ').indexOf(kind())<0; });
 document.querySelectorAll('input[name=activity_type]').forEach(function(r){ r.addEventListener('change', function(){
  document.querySelectorAll('[data-act]').forEach(function(el){ el.hidden=(el.getAttribute('data-act')||'').split(' ').indexOf(kind())<0; });
  var title=document.getElementById('actTitle'); if(title && title.dataset.auto!=='0'){ title.value=''; title.placeholder=suggest(kind(), (document.querySelector('[name=opponent]')||{}).value||''); }
 }); });
 var title=document.getElementById('actTitle'); if(title) title.addEventListener('input', function(){ title.dataset.auto=title.value?'0':'1'; });
})();</script>""")
    return Markup("".join(parts))
def fmt_stamp(s):
    """Pacific stamp from stamp_pt, shown as Fri Oct 30, 1:19pm."""
    if not s or "T" not in str(s): return ""
    day, clock = str(s).split("T", 1)
    try: return "%s, %s" % (fmt_d(day[:10]), fmt_t(clock[:5]))
    except (ValueError, IndexError): return ""
SOCIAL_KINDS = ("Dinner", "Drinks", "Social", "Coffee", "Dessert", "Activities", "Potluck", "Other")
def _field(row, key):
    try:
        if hasattr(row, "keys") and key in row.keys(): return row[key]
    except (AttributeError, TypeError):
        pass
    return None
def social_kinds_of(raw):
    """Canonical type order. A stored single value stays valid."""
    parts = [p.strip().lower() for p in str(raw or "").split(",") if p.strip()]
    return [kind for kind in SOCIAL_KINDS if kind.lower() in parts]
def migrate_social_kinds(d):
    """Rewrite stored types into Dinner, Drinks, Social, Coffee, Dessert, Activities, Potluck, Other."""
    cols = [r[1] for r in d.execute("PRAGMA table_info(practices)")]
    if "social_kind" not in cols: return
    for row in d.execute("SELECT id, social_kind FROM practices WHERE social_kind IS NOT NULL AND social_kind != ''"):
        pid, raw = (row["id"], row["social_kind"]) if hasattr(row, "keys") else (row[0], row[1])
        canon = ",".join(social_kinds_of(raw))
        if canon != (raw or ""):
            d.execute("UPDATE practices SET social_kind=? WHERE id=?", (canon, pid))
def social_line(p):
    """Short card line, or blank when the practice has no social."""
    kinds = social_kinds_of(_field(p, "social_kind"))
    place = " ".join(str(_field(p, "social_place") or "").split())
    if not kinds or not place: return ""
    names = [kinds[0]] + [k.lower() for k in kinds[1:]]
    return "%s after at %s" % (" & ".join(names), place)
def social_home(p):
    """Home card social row: 'Dinner & drinks after' and the place. None when unset."""
    kinds = social_kinds_of(_field(p, "social_kind"))
    place = " ".join(str(_field(p, "social_place") or "").split())
    if not kinds or not place: return None
    names = [kinds[0]] + [k.lower() for k in kinds[1:]]
    return {"title": " & ".join(names) + " after", "place": place}
def clean_social(form):
    raw = form.getlist("social_kind") if hasattr(form, "getlist") else [form.get("social_kind") or ""]
    kind = ",".join(k for k in SOCIAL_KINDS if k in raw)
    place = " ".join((form.get("social_place") or "").split())[:80]
    address = " ".join((form.get("social_address") or "").split())[:300]
    note = " ".join((form.get("social_note") or "").split())[:200]
    raw = (form.get("social_time") or "").strip()
    social_time = ""
    if raw:
        try:
            hh, mm = raw.split(":", 1)
            h, mnt = int(hh), int(mm[:2])
            if 0 <= h <= 23 and 0 <= mnt <= 59: social_time = "%02d:%02d" % (h, mnt)
        except ValueError:
            social_time = ""
    if not kind: return "", "", "", "", ""
    return kind, place, address, social_time, note
def save_social(d, pid, form):
    kind, place, address, social_time, note = clean_social(form)
    if kind and not place: return False
    old = d.execute("SELECT social_place, social_address, social_kind FROM practices WHERE id=?", (pid,)).fetchone()
    d.execute("""UPDATE practices SET social_kind=?, social_place=?, social_address=?, social_time=?, social_note=? WHERE id=?""",
              (kind, place, address, social_time, note, pid))
    moved = not old or (old["social_place"] or "") != (place or "") or (old["social_address"] or "") != (address or "") or not kind
    if moved: d.execute("UPDATE practices SET social_lat=NULL, social_lng=NULL WHERE id=?", (pid,))
    return True
# Bare "Westminster High School" geocodes to Westminster, Colorado. These two pools are the California schools.
POOLS = (
    {"name": "Marina High School", "address": "15871 Springdale St, Huntington Beach, CA 92649", "lat": 33.731441, "lng": -118.027846},
    {"name": "Westminster High School", "address": "14325 Goldenwest St, Westminster, CA 92683", "lat": 33.753752, "lng": -118.011052},
)
def pool_place(text):
    """The known California pool for a school name or its street address."""
    key = " ".join(str(text or "").split()).casefold()
    if not key: return None
    for place in POOLS:
        if key in (place["name"].casefold(), place["address"].casefold()): return place
    return None
def pin_known_pools(d):
    """Write the California street address and coordinates. A stored Colorado pin is replaced."""
    cols = [r[1] for r in d.execute("PRAGMA table_info(practices)")]
    if "address" not in cols or "lat" not in cols: return
    for place in POOLS:
        d.execute("""UPDATE practices SET lat=?, lng=?, address=?
            WHERE lower(trim(location))=?
              AND (lat IS NULL OR lng IS NULL OR abs(lat - ?) > 0.02 OR abs(lng - ?) > 0.02 OR COALESCE(address,'') != ?)""",
            (place["lat"], place["lng"], place["address"], place["name"].casefold(), place["lat"], place["lng"], place["address"]))
_GEO_CACHE = {}
def geocode_address(query):
    """Nominatim lookup. Results are cached in memory; the practice row stores the ones we keep.
    The two home pools never go to Nominatim: the bare school name would resolve to Colorado."""
    q = " ".join(str(query or "").split())
    if not q or q.lower().startswith(("http://", "https://")): return None
    place = pool_place(q)
    if place: return (place["lat"], place["lng"])
    if q in _GEO_CACHE: return _GEO_CACHE[q]
    url = "https://nominatim.openstreetmap.org/search?" + urllib.parse.urlencode({"q": q, "format": "jsonv2", "limit": "1"})
    req = urllib.request.Request(url, headers={"User-Agent": "GrunionsWaterPolo/1.0 (team practice map)", "Accept": "application/json"})
    hit = None
    try:
        with urllib.request.urlopen(req, timeout=3) as resp:
            data = json.loads(resp.read().decode() or "[]")
        if data and data[0].get("lat") and data[0].get("lon"):
            hit = (round(float(data[0]["lat"]), 6), round(float(data[0]["lon"]), 6))
    except Exception as e:
        app.logger.info("geocode failed: %s", e)
        hit = None
    _GEO_CACHE[q] = hit
    return hit
def social_geocode_query(p):
    """Address to geocode for the social pin. A map link is not an address, so the place name is used."""
    if not social_home(p): return ""
    addr = " ".join(str(_field(p, "social_address") or "").split())
    if addr and not addr.lower().startswith(("http://", "https://")): return addr
    return " ".join(str(_field(p, "social_place") or "").split())
def ensure_map_coords(d, p):
    """Fill missing pool and social coordinates. A failed lookup is not written, so a later try can succeed.
    Marina and Westminster always use their California coordinates, never a fresh text search."""
    if not p or "lat" not in p.keys(): return p
    changed = False
    place = pool_place(p["location"])
    if place and (p["lat"] is None or p["lng"] is None or abs(p["lat"] - place["lat"]) > 0.02 or abs(p["lng"] - place["lng"]) > 0.02 or (p["address"] or "") != place["address"]):
        d.execute("UPDATE practices SET lat=?, lng=?, address=? WHERE id=?", (place["lat"], place["lng"], place["address"], p["id"]))
        changed = True
    elif p["lat"] is None or p["lng"] is None:
        hit = geocode_address(p["location"])
        if hit:
            d.execute("UPDATE practices SET lat=?, lng=? WHERE id=?", (hit[0], hit[1], p["id"]))
            changed = True
    sq = social_geocode_query(p)
    if sq and (p["social_lat"] is None or p["social_lng"] is None):
        hit = geocode_address(sq)
        if hit:
            d.execute("UPDATE practices SET social_lat=?, social_lng=? WHERE id=?", (hit[0], hit[1], p["id"]))
            changed = True
    if changed:
        d.commit()
        p = d.execute("SELECT * FROM practices WHERE id=?", (p["id"],)).fetchone()
    return p
def map_pins(p):
    """Pool pin, plus the social pin when that place has coordinates. No pool pin means no map."""
    if not p or p["lat"] is None or p["lng"] is None: return []
    pins = [{"lat": p["lat"], "lng": p["lng"], "kind": "pool", "label": short_place(p["location"] or "")}]
    sh = social_home(p)
    if sh and p["social_lat"] is not None and p["social_lng"] is not None:
        pins.append({"lat": p["social_lat"], "lng": p["social_lng"], "kind": "social", "label": sh["place"]})
    return pins
def save_coach_note(d, pid, text):
    text = " ".join((text or "").split())[:280]
    old = d.execute("SELECT coach_note FROM practices WHERE id=?", (pid,)).fetchone()
    if not text:
        d.execute("UPDATE practices SET coach_note='', coach_note_by='', coach_note_at='' WHERE id=?", (pid,))
    elif not old or (old["coach_note"] or "") != text:
        who = (display_first(me()) + " " + (me()["last"] or "")).strip()
        d.execute("UPDATE practices SET coach_note=?, coach_note_by=?, coach_note_at=? WHERE id=?", (text, who, stamp_pt("minutes"), pid))
_MONTHS = ("January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December")
def practice_days(d):
    return [r["date"] for r in d.execute("SELECT DISTINCT date FROM practices WHERE cancelled=0 ORDER BY date").fetchall()]
def schedule_days(d):
    """Practice days plus published Lineup days, so Schedule can open either."""
    days = set(practice_days(d))
    for start, end, precision in d.execute("SELECT date, end_date, COALESCE(date_precision,'exact') FROM lineup_events WHERE status='published'"):
        if precision == "month": continue
        try: a = dt.date.fromisoformat(str(start)[:10])
        except ValueError: continue
        try: b = dt.date.fromisoformat(str(end or start)[:10])
        except ValueError: b = a
        if b < a: b = a
        if (b - a).days > 21: b = a + dt.timedelta(days=21)
        cur = a
        while cur <= b:
            days.add(cur.isoformat())
            cur += dt.timedelta(days=1)
    return sorted(days)
def admin_day_events(d, date):
    """Practices and published Lineup events that fall on this calendar day, earliest first."""
    events = []
    practices = d.execute("SELECT * FROM practices WHERE date=? AND cancelled=0 ORDER BY start, id", (date,)).fetchall()
    coach_map = practice_coach_rows(d, [p["id"] for p in practices])
    for p in practices:
        labels = coach_labels(coach_map.get(p["id"], []))
        kind = (p["activity_type"] or "practice") if "activity_type" in p.keys() else "practice"
        if kind not in sports.ACTIVITY_IDS: kind = "practice"
        start = p["start"] or "19:00"
        end = p["end"] or "20:30"
        events.append({"key": "p-%d" % p["id"], "kind": "practice", "id": p["id"], "title": practice_title(p),
            "start": start, "when": fmt_span(start, end), "pill": fmt_clock(start),
            "type_label": sports.ACTIVITY_NAME.get(kind, "Practice"), "place": p["location"] or "",
            "map_href": lineup_map_href("", p["location"] or ""),
            "who": ("Coaches: " + ", ".join(labels)) if labels else "",
            "detail": "/practices/%d?from=admin" % p["id"]})
    for e in d.execute("""SELECT e.*, c.chip AS cat_chip, h.first AS host_first, h.last AS host_last, h.preferred_first AS host_preferred
        FROM lineup_events e LEFT JOIN lineup_categories c ON c.id=e.category_id
        LEFT JOIN members h ON h.id=e.host_id
        WHERE e.status='published' AND COALESCE(e.date_precision,'exact')!='month' AND e.date<=? AND COALESCE(NULLIF(e.end_date,''), e.date)>=?""", (date, date)):
        start = (e["start_time"] or "09:00")[:5]
        end = (e["end_time"] or "")[:5]
        when = fmt_span(start, end) if len(end) == 5 else fmt_clock(start)
        who = ""
        events.append({"key": "l-%d" % e["id"], "kind": "lineup", "id": e["id"], "title": e["title"],
            "start": start, "when": when, "pill": fmt_clock(start), "type_label": e["cat_chip"] or "Event",
            "place": lineup_where(e["city"] or "", e["venue"] or ""),
            "map_href": lineup_map_href(e["city"] or "", e["venue"] or ""), "who": who,
            "detail": "/lineup/%d?from=admin&date=%s" % (e["id"], date)})
    events.sort(key=lambda ev: (ev["start"], 0 if ev["kind"] == "practice" else 1, ev["id"]))
    return events
def admin_people(d, date, event, q):
    """RSVP rows for one event. Check-in stays by calendar day, the way the list already works."""
    q = q or ""
    if event and event["kind"] == "lineup":
        rows = d.execute("""SELECT m.*, c.id AS cid,
          CASE rv.state WHEN 'going' THEN 1 WHEN 'notgoing' THEN 0 ELSE NULL END AS going,
          (SELECT COUNT(*) FROM checkins WHERE member_id=m.id) AS visits,
          (SELECT status FROM verify_requests WHERE member_id=m.id ORDER BY id DESC LIMIT 1) AS vr_status,
          (SELECT note FROM verify_requests WHERE member_id=m.id ORDER BY id DESC LIMIT 1) AS vr_note
          FROM members m LEFT JOIN checkins c ON c.member_id=m.id AND c.practice_date=?
          LEFT JOIN lineup_rsvps rv ON rv.member_id=m.id AND rv.event_id=?
          WHERE COALESCE(m.role,'')!='system' AND (?='' OR m.first||' '||COALESCE(m.preferred_first,'')||' '||m.last||' '||m.email LIKE '%'||?||'%')""",
          (date, event["id"], q, q)).fetchall()
    else:
        pid = event["id"] if event else -1
        rows = d.execute("""SELECT m.*, c.id AS cid, rv.going AS going,
          (SELECT COUNT(*) FROM checkins WHERE member_id=m.id) AS visits,
          (SELECT status FROM verify_requests WHERE member_id=m.id ORDER BY id DESC LIMIT 1) AS vr_status,
          (SELECT note FROM verify_requests WHERE member_id=m.id ORDER BY id DESC LIMIT 1) AS vr_note
          FROM members m LEFT JOIN checkins c ON c.member_id=m.id AND c.practice_date=?
          LEFT JOIN rsvps rv ON rv.member_id=m.id AND rv.practice_id=?
          WHERE COALESCE(m.role,'')!='system' AND (?='' OR m.first||' '||COALESCE(m.preferred_first,'')||' '||m.last||' '||m.email LIKE '%'||?||'%')""",
          (date, pid, q, q)).fetchall()
    def by_name(r): return (display_first(r).casefold(), (r["last"] or "").casefold(), r["id"])
    going = sorted((r for r in rows if r["going"] == 1), key=by_name)
    not_going = sorted((r for r in rows if r["going"] == 0), key=by_name)
    rest = sorted((r for r in rows if r["going"] is None), key=by_name)
    checked = sorted((r for r in rows if r["cid"]), key=by_name)
    return going, not_going, rest, checked
def default_checkin_date(days, today=None):
    """Today's practice if there is one, otherwise the next one, otherwise the most recent."""
    today = (today or today_pt()).isoformat()
    if today in days: return today
    for day in days:
        if day > today: return day
    return days[-1] if days else today
def admin_href(date, ev="", filt="going", q=""):
    """Schedule URL that keeps the selected date and event."""
    parts = [("date", date)]
    if ev: parts.append(("ev", ev))
    if filt and filt != "going": parts.append(("filt", filt))
    if q: parts.append(("q", q))
    return "/admin?" + urllib.parse.urlencode(parts)
def admin_step(d, days, date, events, selected_key, step):
    """Move to the next or previous event, then to the neighboring date.
    Forward lands on the first event of a new date. Back lands on the last."""
    keys = [e["key"] for e in events]
    if keys and selected_key in keys:
        idx = keys.index(selected_key)
        if step > 0 and idx < len(keys) - 1:
            return date, keys[idx + 1]
        if step < 0 and idx > 0:
            return date, keys[idx - 1]
    nxt = neighbor_practice(days, date, step)
    if not nxt:
        return None
    nxt_events = admin_day_events(d, nxt)
    if not nxt_events:
        return nxt, ""
    return nxt, nxt_events[0 if step > 0 else -1]["key"]
def admin_catalog(d, days):
    """Short event lists for the date picker, keyed by day."""
    out = {}
    for day in days or []:
        out[day] = [{"key": e["key"], "title": e["title"], "when": e["when"]} for e in admin_day_events(d, day)]
    return out
def neighbor_practice(days, date, step):
    if date in days:
        i = days.index(date) + step
        return days[i] if 0 <= i < len(days) else None
    earlier = [x for x in days if x < date]
    later = [x for x in days if x > date]
    if step < 0: return earlier[-1] if earlier else None
    return later[0] if later else None
def checkin_month(date_iso, days, today=None):
    """Sunday-first month grid. Cells are None (leading blank) or day dicts."""
    try: cur = dt.date.fromisoformat(date_iso)
    except ValueError: cur = today_pt()
    today = today or today_pt().isoformat()
    first = cur.replace(day=1)
    nxt = dt.date(first.year + 1, 1, 1) if first.month == 12 else dt.date(first.year, first.month + 1, 1)
    have = set(days or [])
    cells, day = [None] * ((first.weekday() + 1) % 7), first
    while day < nxt:
        iso = day.isoformat()
        cells.append({"iso": iso, "day": day.day, "has": iso in have, "on": iso == date_iso, "today": iso == today})
        day += dt.timedelta(days=1)
    return {"label": _MONTHS[first.month - 1] + " " + str(first.year), "ym": "%04d-%02d" % (first.year, first.month), "cells": cells}
def add_coaching(d, mid, source):
    d.execute("""INSERT INTO coaching_list(member_id, source, at) VALUES(?,?,?)
        ON CONFLICT(member_id) DO UPDATE SET source=excluded.source, at=excluded.at""", (mid, source, stamp_pt("minutes")))
def add_referee(d, mid, source="manual"):
    d.execute("""INSERT INTO referee_list(member_id, source, at) VALUES(?,?,?)
        ON CONFLICT(member_id) DO UPDATE SET source=excluded.source, at=excluded.at""", (mid, source, stamp_pt("minutes")))
def drop_usawp_coaching(d, mid):
    d.execute("DELETE FROM coaching_list WHERE member_id=? AND source='usawp'", (mid,))
def apply_membership_type(d, mid, membership_type, update_list):
    """Store the USAWP membership type. Change the coaching list only when update_list is set."""
    text = str(membership_type or "").strip()[:120]
    if not text: return
    d.execute("UPDATE members SET membership_type=? WHERE id=?", (text, mid))
    if not update_list: return
    if is_coach_membership(text): add_coaching(d, mid, "usawp")
    else: drop_usawp_coaching(d, mid)
def coach_candidates(d):
    """Assignable to a practice: the coaching list. Active coach access is separate."""
    return d.execute("""SELECT m.id, m.first, m.last, m.preferred_first, m.role, m.is_admin, m.membership_type, m.usawp_status, m.usawp_valid_until
        FROM members m
        WHERE COALESCE(m.role,'')!='system'
          AND m.id IN (SELECT member_id FROM coaching_list)
        ORDER BY lower(CASE WHEN trim(COALESCE(m.preferred_first,''))!='' THEN m.preferred_first ELSE m.first END), lower(m.last), m.id""").fetchall()
def row_lead(r):
    try: return 1 if int(r["is_lead"] or 0) else 0
    except (KeyError, IndexError, TypeError, ValueError): return 0
def coach_labels(rows):
    """First names for the schedule. The lead coach is first, then A–Z. A shared first name keeps the last initial."""
    rows = sorted(rows, key=lambda r: (0 if row_lead(r) else 1, display_first(r).casefold(), (r["last"] or "").casefold(), r["id"]))
    folded = [display_first(r).casefold() for r in rows]
    out = []
    for r, fold in zip(rows, folded):
        name = display_first(r)
        if folded.count(fold) > 1 and r["last"]: name = "%s %s." % (name, r["last"][:1])
        if row_lead(r): name += " (lead)"
        out.append(name)
    return out
def practice_coach_rows(d, pids):
    out = {pid: [] for pid in pids}
    if not pids: return out
    marks = ",".join("?" * len(pids))
    for r in d.execute("""SELECT pc.practice_id AS pid, pc.is_lead, pc.focus, m.id, m.first, m.last, m.preferred_first, m.email,
        m.membership_type, m.usawp_status, m.usawp_valid_until
        FROM practice_coaches pc JOIN members m ON m.id=pc.member_id
        WHERE pc.practice_id IN (%s) AND COALESCE(m.role,'')!='system'
          AND m.id IN (SELECT member_id FROM coaching_list)""" % marks, tuple(pids)):
        out[r["pid"]].append(r)
    return out
def clean_focus(text):
    return " ".join((text or "").split())[:80]
def clean_plan(text):
    return (text or "").replace("\r\n", "\n").replace("\r", "\n").strip()[:2000]
def focus_map_from_form():
    out = {}
    for key in request.form:
        if not str(key).startswith("focus-"): continue
        try: out[int(str(key).split("-", 1)[1])] = clean_focus(request.form.get(key))
        except ValueError: continue
    return out
def save_coaching_plan(d, pid, text):
    d.execute("UPDATE practices SET coaching_plan=? WHERE id=?", (clean_plan(text), pid))
def save_practice_coaches(d, pid, raw, lead=None, focuses=None):
    """Replace the assigned coaches. Ids outside the coach list are ignored.
    When focuses is omitted, a coach who stays keeps their lead flag and focus group."""
    allowed = {r["id"] for r in coach_candidates(d)}
    chosen = []
    for x in raw or []:
        try: i = int(x)
        except (TypeError, ValueError): continue
        if i in allowed and i not in chosen: chosen.append(i)
    prev = {}
    for r in d.execute("SELECT member_id, is_lead, focus FROM practice_coaches WHERE practice_id=?", (pid,)):
        prev[r["member_id"]] = (1 if r["is_lead"] else 0, r["focus"] or "")
    explicit = focuses is not None
    lead_id = None
    if explicit and lead:
        try: lead_id = int(lead)
        except (TypeError, ValueError): lead_id = None
        if lead_id not in chosen: lead_id = None
    d.execute("DELETE FROM practice_coaches WHERE practice_id=?", (pid,))
    rows = []
    for i in chosen:
        if explicit:
            flag, text = (1 if i == lead_id else 0), clean_focus((focuses or {}).get(i, ""))
        else:
            flag, text = prev.get(i, (0, ""))
        rows.append((pid, i, flag, text))
    if rows:
        d.executemany("INSERT INTO practice_coaches(practice_id, member_id, is_lead, focus) VALUES(?,?,?,?)", rows)
def save_assigned_plan(d, pid, lead, focuses):
    """Update the lead and focus groups without changing who is assigned."""
    ids = [r["member_id"] for r in d.execute("SELECT member_id FROM practice_coaches WHERE practice_id=?", (pid,))]
    try: lead_id = int(lead) if lead else None
    except (TypeError, ValueError): lead_id = None
    if lead_id not in ids: lead_id = None
    for i in ids:
        d.execute("UPDATE practice_coaches SET is_lead=?, focus=? WHERE practice_id=? AND member_id=?",
                  (1 if i == lead_id else 0, clean_focus((focuses or {}).get(i, "")), pid, i))
def hide_coaching_plan(p):
    """Members do not receive the coaches-only plan, even as an empty field on the row."""
    if not p or can_host_practice(): return p
    data = dict(p)
    data["coaching_plan"] = ""
    return data
app.jinja_env.globals.update(fmt_t=fmt_t, fmt_d=fmt_d, fmt_card_date=fmt_card_date, practice_title=practice_title, practice_sports_line=practice_sports_line, sports_editor=sports_editor, fmt_clock=fmt_clock, fmt_span=fmt_span, fmt_stamp=fmt_stamp, weekday_abbr=weekday_abbr, month_abbr=month_abbr, day_num=day_num, short_place=short_place, social_line=social_line, social_home=social_home, SOCIAL_KINDS=SOCIAL_KINDS, SPORTS=sports)
def practice_people(rows):
    return sorted(rows, key=lambda r: (display_first(r).casefold(), (r["last"] or "").casefold(), r["id"]))
def redirect_practice(pid, action):
    ref = request.referrer or ""
    if action in ("going", "notgoing", "clear", "social_join", "social_leave") and "/home" in ref: return redirect("/home")
    if action == "delete" or not pid: return redirect("/practices")
    if request.form.get("back") == "page": return redirect("/practices/%s" % pid)
    return redirect("/practices#p%s" % pid)
def handle_practice_post(d):
    """RSVP and admin actions for a practice. Returns the redirect."""
    a = request.form.get("action"); pid = request.form.get("pid", type=int)
    if pid and not d.execute("SELECT 1 FROM practices WHERE id=?", (pid,)).fetchone() and a != "add": abort(404)
    new_id = None
    if a in ("going", "notgoing", "clear"):
        if a == "clear": d.execute("DELETE FROM rsvps WHERE practice_id=? AND member_id=?", (pid, me()["id"]))
        else: d.execute("INSERT INTO rsvps(practice_id,member_id,going) VALUES(?,?,?) ON CONFLICT DO UPDATE SET going=excluded.going, at=CURRENT_TIMESTAMP", (pid, me()["id"], int(a == "going")))
    elif a in ("social_join", "social_leave") and pid:
        if a == "social_leave": d.execute("DELETE FROM social_joins WHERE practice_id=? AND member_id=?", (pid, me()["id"]))
        else: d.execute("INSERT OR IGNORE INTO social_joins(practice_id, member_id) VALUES(?,?)", (pid, me()["id"]))
    elif a == "social" and pid:
        if not can_host_practice(): abort(403)
        if not save_social(d, pid, request.form): flash("Add a place for the social.")
    elif a == "message" and pid:
        if not can_host_practice(): abort(403)
        save_coach_note(d, pid, request.form.get("message"))
    elif a == "plan" and pid:
        if not can_host_practice(): abort(403)
        save_assigned_plan(d, pid, request.form.get("lead"), focus_map_from_form())
        save_coaching_plan(d, pid, request.form.get("coaching_plan"))
    elif a == "image" and pid:
        if not can_host_practice(): abort(403)
        try:
            if not apply_practice_image(d, pid): flash("Choose a picture.")
        except ValueError as e:
            flash(str(e))
    elif not me()["is_admin"]: abort(403)
    elif a == "add":
        if request.form.get("repeat"):
            try: save_series(d)
            except ValueError as e: flash(str(e))
            except sqlite3.IntegrityError: flash("A practice already exists at that place on that date.")
        else:
            try:
                sp = sports.sports_from_form(request.form)
                d.execute("""INSERT INTO practices(date,start,end,location,note,activity_type,sport,title,skill_levels,divisions,division_custom,opponent,home_away,gameplay_notes,segments,comp_format)
                    VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                    (request.form["date"], request.form.get("start") or "19:00", request.form.get("end") or "20:30", request.form.get("location") or "TBD", request.form.get("note"), *sports.sports_tuple(sp)))
            except sqlite3.IntegrityError: flash("A practice already exists at that place on that date.")
    elif a == "edit" and pid:
        old = d.execute("SELECT date, start, end, location, note, series_id FROM practices WHERE id=?", (pid,)).fetchone()
        raw_date = request.form.get("date")
        date = old["date"] if raw_date is None else (parse_date(raw_date).isoformat() if parse_date(raw_date) else "")
        if old and old["series_id"] and request.form.get("series_scope") == "following": date = old["date"]
        start, end, loc, note = request.form.get("start") or old["start"], request.form.get("end") or old["end"], request.form.get("location") or old["location"], request.form.get("note")
        if note is None: note = old["note"]
        if "social_kind" in request.form and clean_social(request.form)[0] and not clean_social(request.form)[1]:
            flash("Add a place for the social.")
            return redirect("/practices/%s?edit=1" % pid if request.form.get("back") == "page" else "/practices#p%s" % pid)
        if not date: flash("Enter the practice date.")
        else:
            try:
                moved = (loc or "") != (old["location"] or "")
                d.execute("UPDATE practices SET date=?, start=?, end=?, location=?, note=?" + (", lat=NULL, lng=NULL" if moved else "") + " WHERE id=?", (date, start, end, loc, note, pid))
                if request.form.get("plan_fields"):
                    save_practice_coaches(d, pid, request.form.getlist("coach"), lead=request.form.get("lead"), focuses=focus_map_from_form())
                    save_coaching_plan(d, pid, request.form.get("coaching_plan"))
                else:
                    save_practice_coaches(d, pid, request.form.getlist("coach"))
                if "social_kind" in request.form: save_social(d, pid, request.form)
                if "message" in request.form: save_coach_note(d, pid, request.form.get("message"))
                try: apply_practice_image(d, pid)
                except ValueError as e: flash(str(e))
                sp = sports.sports_from_form(request.form) if "activity_type" in request.form else None
                if sp:
                    d.execute("""UPDATE practices SET activity_type=?, sport=?, title=?, skill_levels=?, divisions=?, division_custom=?,
                        opponent=?, home_away=?, gameplay_notes=?, segments=?, comp_format=? WHERE id=?""", (*sports.sports_tuple(sp), pid))
                if old and (old["date"], old["start"], old["end"], old["location"], old["note"] or "") != (date, start, end, loc, note or ""):
                    flag_practice(d, pid, "change", me()["id"])
                if old and old["series_id"]:
                    if request.form.get("series_scope") == "following":
                        apply_series_following(d, old["series_id"], old["date"], start, end, loc, request.form.getlist("coach"), request.form.get("lead"), sp)
                    else:
                        d.execute("UPDATE practices SET series_detached=1 WHERE id=?", (pid,))
            except sqlite3.IntegrityError:
                flash("A practice already exists at that place on that date.")
                d.rollback()
                return redirect("/practices/%s?edit=1" % pid if request.form.get("back") == "page" else "/practices#p%s" % pid)
    elif a == "assign" and pid:
        save_practice_coaches(d, pid, request.form.getlist("coach"))
    elif a in ("cancel", "restore") and pid:
        was = d.execute("SELECT cancelled FROM practices WHERE id=?", (pid,)).fetchone()
        reason = " ".join((request.form.get("reason") or "").split())[:300]
        if a == "cancel": d.execute("UPDATE practices SET cancelled=1, cancel_reason=? WHERE id=?", (reason, pid))
        else: d.execute("UPDATE practices SET cancelled=0, cancel_reason='' WHERE id=?", (pid,))
        if a == "restore":
            d.execute("DELETE FROM sent_notices WHERE kind IN (?,?)", ("email:practice_cancelled:%s" % pid, "push:practice_cancelled:%s" % pid))
            d.execute("DELETE FROM practice_notices WHERE practice_id=? AND kind='cancel'", (pid,))
            if was and was["cancelled"]: flag_practice(d, pid, "change", me()["id"])
        elif not was or not was["cancelled"]:
            flag_practice(d, pid, "cancel", me()["id"])
    elif a == "duplicate" and pid:
        src = d.execute("SELECT * FROM practices WHERE id=?", (pid,)).fetchone()
        new_date = (dt.date.fromisoformat(src["date"]) + dt.timedelta(days=7)).isoformat()
        try:
            cur = d.execute("""INSERT INTO practices(date,start,end,location,address,note,cancelled,social_kind,social_place,social_address,social_time,social_note,image,lat,lng,social_lat,social_lng,coaching_plan)
                VALUES(?,?,?,?,?,?,0,?,?,?,?,?,?,?,?,?,?,?)""", (new_date, src["start"], src["end"], src["location"], src["address"], src["note"],
                src["social_kind"], src["social_place"], src["social_address"], src["social_time"], src["social_note"],
                src["image"], src["lat"], src["lng"], src["social_lat"], src["social_lng"], src["coaching_plan"] if "coaching_plan" in src.keys() else ""))
            new_id = cur.lastrowid
            copied = d.execute("SELECT member_id, is_lead, focus FROM practice_coaches WHERE practice_id=?", (pid,)).fetchall()
            lead = next((r["member_id"] for r in copied if r["is_lead"]), None)
            save_practice_coaches(d, new_id, [r["member_id"] for r in copied], lead=lead, focuses={r["member_id"]: (r["focus"] or "") for r in copied})
            flash("Copied to %s." % fmt_d(new_date))
        except sqlite3.IntegrityError:
            flash("A practice is already on the schedule a week later at that place.")
    elif a == "skip" and pid:
        prow = d.execute("SELECT series_id, date FROM practices WHERE id=?", (pid,)).fetchone()
        if not prow or not prow["series_id"]: flash("Only a series date can be skipped.")
        else:
            d.execute("INSERT OR IGNORE INTO series_skips(series_id, date) VALUES(?,?)", (prow["series_id"], prow["date"]))
            if practice_has_rsvps(d, pid):
                d.execute("UPDATE practices SET cancelled=1, skipped=1 WHERE id=?", (pid,))
            else:
                delete_practice_row(d, pid); pid = None
    elif a == "unskip" and pid:
        prow = d.execute("SELECT series_id, date, skipped FROM practices WHERE id=?", (pid,)).fetchone()
        if prow and prow["series_id"]:
            d.execute("DELETE FROM series_skips WHERE series_id=? AND date=?", (prow["series_id"], prow["date"]))
            if prow["skipped"]: d.execute("UPDATE practices SET cancelled=0, skipped=0, cancel_reason='' WHERE id=?", (pid,))
            sync_series(d, prow["series_id"])
    elif a == "delete" and pid:
        d.execute("DELETE FROM practice_coaches WHERE practice_id=?", (pid,))
        d.execute("DELETE FROM rsvps WHERE practice_id=?", (pid,))
        d.execute("DELETE FROM social_joins WHERE practice_id=?", (pid,))
        d.execute("DELETE FROM practice_notices WHERE practice_id=?", (pid,))
        d.execute("DELETE FROM practices WHERE id=?", (pid,))
        pid = None
    if pid and a in ("going", "notgoing", "clear"): mark_practice_seen(d, me()["id"], pid)
    d.commit()
    if a in ("going", "notgoing", "clear", "edit", "add", "cancel", "restore", "assign", "duplicate", "delete", "skip", "unskip"): sync_practice_sheets(d)
    if a == "cancel" and pid:
        p = d.execute("SELECT * FROM practices WHERE id=?", (pid,)).fetchone()
        if p and p["cancelled"]:
            try: notify_practice_cancelled(d, p)
            except Exception as e: app.logger.warning("cancel notify failed: %s", e)
    if a == "duplicate" and new_id: return redirect("/practices/%s" % new_id)
    return redirect_practice(pid, a)
def practice_bundle(d, p):
    """RSVP lists, check-ins, and assigned coaches for one practice page or card."""
    rv = d.execute("SELECT r.going, m.first, m.last, m.preferred_first, m.id, COALESCE(m.photo,'') AS photo FROM rsvps r JOIN members m ON m.id=r.member_id WHERE practice_id=?", (p["id"],)).fetchall()
    mine = next((r["going"] for r in rv if r["id"] == me()["id"]), None)
    raw_coaches = practice_coach_rows(d, [p["id"]]).get(p["id"], [])
    host = can_host_practice()
    coaches = []
    for c in practice_people(raw_coaches):
        item = dict(c)
        if not host: item["focus"] = ""
        coaches.append(item)
    shown = hide_coaching_plan(p)
    checked = d.execute("""SELECT m.id, m.first, m.last, m.preferred_first, COALESCE(m.photo,'') AS photo FROM checkins c JOIN members m ON m.id=c.member_id
        WHERE c.practice_date=? AND COALESCE(m.role,'')!='system'""", (p["date"],)).fetchall()
    social_n = d.execute("SELECT COUNT(*) FROM social_joins WHERE practice_id=?", (p["id"],)).fetchone()[0]
    return dict(p=shown, going=practice_people([r for r in rv if r["going"]]), notgoing=practice_people([r for r in rv if not r["going"]]),
                checked=practice_people(checked), mine=mine, coach_ids={c["id"] for c in coaches}, coach_names=coach_labels(raw_coaches),
                coaches=coaches, social_n=social_n, lead_id=next((c["id"] for c in raw_coaches if row_lead(c)), None),
                focuses={c["id"]: (c["focus"] or "") for c in coaches})
def upcoming_schedule(d, skip_id=None):
    """Schedule cards after the featured next practice. The featured one stays in the home card."""
    ps = d.execute("SELECT * FROM practices WHERE " + upcoming_where() + " ORDER BY date, start LIMIT 16", upcoming_bounds()).fetchall()
    unseen = unread_for_me()["practices"]
    data = []
    for p in ps:
        if skip_id and p["id"] == skip_id: continue
        row = practice_bundle(d, p)
        row["unseen"] = unseen.get(str(p["id"]), 0)
        data.append(row)
    return data
def combined_view(entry):
    """Home and Schedule are one scrolling page. Schedule opens it already scrolled."""
    m = me(); d = db()
    hist = d.execute("SELECT practice_date, location FROM checkins WHERE member_id=? ORDER BY practice_date DESC", (m["id"],)).fetchall()
    month = today_pt().strftime("%Y-%m")
    ensure_schedule(d)
    picked = next_commitment(d, m["id"])
    next_kind, nextev = "practice", None
    practice_row = d.execute("SELECT * FROM practices WHERE cancelled=0 AND " + upcoming_where() + " ORDER BY date, start LIMIT 1", upcoming_bounds()).fetchone()
    if picked and picked[0] == "event":
        next_kind = "event"
        full = lineup_event_row(d, picked[1]["id"])
        nextev = lineup_pack(d, [full])[0] if full else None
        if not nextev: next_kind = "practice"
    if picked and picked[0] == "practice":
        practice_row = picked[1]
    nextp = practice_row
    if nextp: nextp = ensure_map_coords(d, nextp)
    nextp_n = d.execute("SELECT COUNT(*) FROM rsvps WHERE practice_id=? AND going=1", (nextp["id"],)).fetchone()[0] if nextp else 0
    nextp_mine = d.execute("SELECT going FROM rsvps WHERE practice_id=? AND member_id=?", (nextp["id"], m["id"])).fetchone() if nextp else None
    nextp_mine = nextp_mine[0] if nextp_mine else None
    next_rows = practice_coach_rows(d, [nextp["id"]]).get(nextp["id"], []) if nextp else []
    next_coaches = ", ".join(coach_labels(next_rows))
    nextp = hide_coaching_plan(nextp)
    next_joined = bool(nextp and d.execute("SELECT 1 FROM social_joins WHERE practice_id=? AND member_id=?", (nextp["id"], m["id"])).fetchone())
    notices = d.execute("SELECT * FROM notices WHERE member_id=? AND seen=0 ORDER BY id DESC", (m["id"],)).fetchall()
    d.execute("UPDATE notices SET seen=1 WHERE member_id=? AND seen=0", (m["id"],)); d.commit()
    ann = d.execute("SELECT m.*, p.first, p.preferred_first FROM messages m JOIN members p ON p.id=m.member_id WHERE announcement=1 AND channel='team' AND COALESCE(m.deleted,0)=0 ORDER BY m.id DESC LIMIT 1").fetchone()
    vr_pending = d.execute("SELECT 1 FROM verify_requests WHERE member_id=? AND status='pending'", (m["id"],)).fetchone() is not None
    pins = map_pins(nextp)
    data = upcoming_schedule(d)
    return page(T["home"], tab="practices" if entry == "practices" else "home",
        m=m, hist=hist, nmonth=sum(1 for h in hist if h['practice_date'].startswith(month)), ann=ann, notices=notices,
        nextp=nextp, next_kind=next_kind, nextev=nextev, nextp_n=nextp_n, nextp_mine=nextp_mine, next_coaches=next_coaches, next_joined=next_joined,
        vr_pending=vr_pending, today=today_pt().isoformat(), pins=pins, data=data, coach_choices=coach_candidates(d) if m["is_admin"] else [])
@app.route("/practices", methods=["GET", "POST"])
@login_required
def practices():
    d = db(); ensure_schedule(d)
    if request.method == "POST": return handle_practice_post(d)
    return combined_view("practices")
@app.route("/practices/<int:pid>", methods=["GET", "POST"])
@login_required
def practice_page(pid):
    d = db(); ensure_schedule(d)
    if request.method == "POST":
        if request.form.get("pid", type=int) != pid: abort(400)
        return handle_practice_post(d)
    p = d.execute("SELECT * FROM practices WHERE id=?", (pid,)).fetchone()
    if not p: abort(404)
    p = ensure_map_coords(d, p)
    mark_practice_seen(d, me()["id"], pid); d.commit()
    g._unread_mid = None
    host = can_host_practice()
    editing = request.args.get("edit") == "1" and bool(me()["is_admin"])
    plan_editing = request.args.get("edit") == "1" and host and not me()["is_admin"]
    return page(T["practice"], tab="practice", x=practice_bundle(d, p), editing=editing, plan_editing=plan_editing, pins=map_pins(p), coach_choices=coach_candidates(d) if host else [], from_admin=request.args.get("from") == "admin")
@app.route("/practices/series/new", methods=["GET", "POST"])
@admin_required
def series_new():
    d = db()
    values = series_form_values()
    if request.method == "POST":
        try:
            save_series(d); d.commit(); flash("Saved", "toast"); return redirect("/practices")
        except ValueError as e:
            flash(str(e)); values = series_form_values(form=request.form)
    return page(T["series_edit"], tab="series_edit", action="/practices/series/new", values=values, series_id=None, skips=[], coach_choices=coach_candidates(d), series=None)
@app.route("/practices/series/<int:sid>", methods=["GET", "POST"])
@admin_required
def series_page(sid):
    d = db()
    row = d.execute("SELECT * FROM practice_series WHERE id=?", (sid,)).fetchone()
    if not row: abort(404)
    if request.method == "POST" and request.form.get("action") == "unskip":
        day = (request.form.get("date") or "")[:10]
        d.execute("DELETE FROM series_skips WHERE series_id=? AND date=?", (sid, day))
        d.execute("UPDATE practices SET cancelled=0, skipped=0, cancel_reason='' WHERE series_id=? AND date=? AND skipped=1", (sid, day))
        sync_series(d, sid); d.commit(); return redirect("/practices/series/%d" % sid)
    coaches = d.execute("SELECT member_id, is_lead FROM series_coaches WHERE series_id=?", (sid,)).fetchall()
    values = series_form_values(row, coaches=coaches)
    if request.method == "POST":
        try:
            save_series(d, sid); d.commit(); flash("Saved", "toast"); return redirect("/practices/series/%d" % sid)
        except ValueError as e:
            flash(str(e)); values = series_form_values(form=request.form)
    skips = [r["date"] for r in d.execute("SELECT date FROM series_skips WHERE series_id=? ORDER BY date", (sid,))]
    return page(T["series_edit"], tab="series_edit", action="/practices/series/%d" % sid, values=values, series_id=sid, skips=skips, coach_choices=coach_candidates(d), series=row)
def lineup_where(city, venue):
    """Cards show the city. A venue-only legacy row falls back to that name."""
    city = " ".join(str(city or "").split())
    venue = " ".join(str(venue or "").split())
    if venue.lower().startswith(("http://", "https://")): return city or venue
    return city or venue
def lineup_map_href(city, venue):
    city = " ".join(str(city or "").split())
    venue = " ".join(str(venue or "").split())
    if venue.lower().startswith(("http://", "https://")): return venue
    query = ", ".join(part for part in (venue, city) if part)
    if not query: return ""
    return "https://www.google.com/maps/search/?api=1&query=" + urllib.parse.quote(query)
def lineup_range(start, end):
    start = str(start)[:10]
    end = str(end or start)[:10]
    if end <= start: return fmt_d(start)
    return "%s – %s" % (fmt_d(start), fmt_d(end))
def lineup_month(iso):
    day = dt.date.fromisoformat(str(iso)[:10])
    return day.strftime("%B ") + str(day.year)
def _form_last():
    """Last value wins, so a checkbox after a hidden 0 is the one that counts."""
    return {k: request.form.getlist(k)[-1] for k in request.form}
def ensure_lineup_coords(d, row):
    """Cache a pin for the venue so the event map can draw without another lookup."""
    if not row or "lat" not in row.keys(): return row
    if row["lat"] is not None and row["lng"] is not None: return row
    venue = " ".join(str(row["venue"] or "").split())
    city = " ".join(str(row["city"] or "").split())
    if venue.lower().startswith(("http://", "https://")): venue = ""
    query = venue or city
    if not query: return row
    hit = geocode_address(query)
    if not hit: return row
    d.execute("UPDATE lineup_events SET lat=?, lng=? WHERE id=?", (hit[0], hit[1], row["id"]))
    d.commit()
    return lineup_event_row(d, row["id"])
def lineup_event_row(d, eid):
    return d.execute("""SELECT e.*, c.slug AS cat_slug, c.name AS cat_name, c.chip AS cat_chip,
        c.member_ok, c.intent_ok, c.hosting_ok, c.active AS cat_active,
        h.first AS host_first, h.last AS host_last, h.preferred_first AS host_preferred
        FROM lineup_events e
        LEFT JOIN lineup_categories c ON c.id=e.category_id
        LEFT JOIN members h ON h.id=e.host_id WHERE e.id=?""", (eid,)).fetchone()
def lineup_query(d):
    return d.execute("""SELECT e.*, c.slug AS cat_slug, c.name AS cat_name, c.chip AS cat_chip,
        c.member_ok, c.intent_ok, c.hosting_ok, c.active AS cat_active,
        h.first AS host_first, h.last AS host_last, h.preferred_first AS host_preferred
        FROM lineup_events e
        LEFT JOIN lineup_categories c ON c.id=e.category_id
        LEFT JOIN members h ON h.id=e.host_id""").fetchall()
def event_window(e):
    day = dt.date.fromisoformat(str(e["date"])[:10])
    end_day = dt.date.fromisoformat(str(e["end_date"] or e["date"])[:10])
    def hm(v, default):
        raw = (v or default).strip() or default
        parts = raw.split(":")
        return int(parts[0]), int(parts[1] if len(parts) > 1 else 0)
    sh, sm = hm(e["start_time"] if "start_time" in e.keys() else "", "00:00")
    eh, em = hm(e["end_time"] if "end_time" in e.keys() else "", "23:59")
    start = dt.datetime.combine(day, dt.time(sh, sm))
    end = dt.datetime.combine(end_day, dt.time(eh, em))
    if end < start: end = dt.datetime.combine(end_day, dt.time(23, 59))
    return start, end
def event_chip_label(start, end, now=None):
    """Day chip for a committed event: happening now, day N of M, or the usual relative day."""
    now = wall_pt(now)
    if start <= now <= end:
        span = (end.date() - start.date()).days + 1
        if span <= 1: return "HAPPENING NOW"
        if now.date() >= end.date(): return "FINAL DAY"
        return "DAY %d OF %d" % ((now.date() - start.date()).days + 1, span)
    left = (start.date() - now.date()).days
    if left <= 6: return relative_day(start.date().isoformat())
    return "UP NEXT"
def lineup_public(row):
    return (row["status"] or "") == "published"
def lineup_seen(row, actor):
    if not row: return False
    if lineup_public(row): return True
    if not actor: return False
    if can_host_practice(actor): return True
    return actor["id"] in ((row["created_by"] or 0), (row["host_id"] or 0))
def lineup_tile(row):
    """Date tile for a Lineup card. Month-only events show the month, not a day."""
    precision = row["date_precision"] if "date_precision" in row.keys() and row["date_precision"] else "exact"
    day = dt.date.fromisoformat(str(row["date"])[:10])
    if precision == "month":
        part = (row["date_part"] or "").strip().lower() if "date_part" in row.keys() else ""
        top = {"early": "EARLY", "mid": "MID", "late": "LATE"}.get(part, "")
        return {"wd": top, "dn": day.strftime("%b").upper(), "mo": str(day.year)}
    return {"wd": weekday_abbr(day.isoformat()), "dn": str(day.day), "mo": month_abbr(day.isoformat())}
def lineup_dir_href(city, venue):
    """Directions link. A pasted map URL is used as-is."""
    venue = " ".join(str(venue or "").split())
    city = " ".join(str(city or "").split())
    if venue.lower().startswith(("http://", "https://")): return venue
    query = ", ".join(part for part in (venue, city) if part)
    if not query: return ""
    return "https://www.google.com/maps/dir/?api=1&destination=" + urllib.parse.quote(query)
def lineup_when_label(row):
    precision = row["date_precision"] if "date_precision" in row.keys() and row["date_precision"] else "exact"
    if precision == "month":
        day = dt.date.fromisoformat(str(row["date"])[:10])
        label = day.strftime("%B") + " " + str(day.year)
        part = (row["date_part"] or "").strip().lower() if "date_part" in row.keys() else ""
        if part in ("early", "mid", "late"): label = part[:1].upper() + part[1:] + " " + label
        return label + " · Dates TBA"
    start, end = str(row["date"])[:10], str(row["end_date"] or row["date"])[:10]
    if end > start: base = lineup_range(start, end)
    else: base = fmt_d(start)
    st, et = row["start_time"] or "", row["end_time"] or ""
    if st and et: return "%s · %s" % (base, fmt_span(st, et))
    if st: return "%s · %s" % (base, fmt_clock(st))
    return base
def lineup_status_text(row):
    """Dotted status on the event page. Chips do not repeat it."""
    status = row["status"] or "published"
    if status == "pending": return "warn", "Pending approval"
    if status == "canceled": return "bad", "Canceled"
    if status == "declined": return "bad", "Declined"
    if status == "changes_requested": return "warn", "Changes requested"
    if status == "draft": return "warn", "Draft"
    if not row["official"]: return "ok", "Community"
    if (row["team_intent"] or "") == "considering": return "warn", "Considering"
    return "ok", "Official trip"
def lineup_event_type(row):
    stored = row["event_type"] if "event_type" in row.keys() else ""
    return lineupfeed.event_type_from_parts(row["cat_slug"] or "", row["subtype"] or "", row["kind"] or "", stored or "")
def lineup_tag(row):
    hosting = row["hosting"] if (row["hosting"] or "") in ("Away", "Hosting") else ""
    return " · ".join(part for part in (hosting, lineup_event_type(row)) if part)
def lineup_host_line(row):
    if row["official"]: return "Official club event"
    who = display_first({"first": row["host_first"] or "", "last": row["host_last"] or "", "preferred_first": row["host_preferred"] or ""}) if row["host_first"] else ""
    return "Hosted by %s" % who if who else "Hosted by a member"
def lineup_status_label(row, now=None):
    status = row["status"] or "published"
    if status == "published":
        _start, end = event_window(row)
        if end < wall_pt(now): return "Completed"
    return lineupfeed.STATUS_LABEL.get(status, status)
def lineup_pack(d, rows):
    mid = me()["id"] if me() else 0
    organizer = can_host_practice() if me() else False
    ids = [r["id"] for r in rows]
    counts, mine, going_names = {}, {}, {}
    if ids:
        marks = ",".join("?" * len(ids))
        for eid, state, n in d.execute("SELECT event_id, state, COUNT(*) FROM lineup_rsvps WHERE event_id IN (%s) GROUP BY event_id, state" % marks, ids):
            counts.setdefault(eid, {})[state or "going"] = n
        for eid, state in d.execute("SELECT event_id, state FROM lineup_rsvps WHERE member_id=? AND event_id IN (%s)" % marks, (mid, *ids)):
            mine[eid] = state
        for eid, first, last, preferred, mid_row, photo in d.execute("""SELECT r.event_id, m.first, m.last, m.preferred_first, m.id, COALESCE(m.photo,'')
            FROM lineup_rsvps r JOIN members m ON m.id=r.member_id
            WHERE r.state='going' AND r.event_id IN (%s)""" % marks, ids):
            going_names.setdefault(eid, []).append({"id": mid_row, "first": first, "last": last, "preferred_first": preferred, "photo": photo})
    out = []
    for r in rows:
        c = counts.get(r["id"], {})
        going_n, interested_n = c.get("going", 0), c.get("interested", 0)
        wait_n = c.get("waitlist", 0)
        intent = r["team_intent"] or ""
        people = practice_people(going_names.get(r["id"], []))
        names = [("%s %s" % (display_first(p), p["last"] or "")).strip() for p in people]
        try:
            span = (dt.date.fromisoformat(str(r["end_date"] or r["date"])[:10]) - dt.date.fromisoformat(str(r["date"])[:10])).days + 1
        except ValueError:
            span = 1
        if span < 1: span = 1
        status_kind, status_text = lineup_status_text(r)
        etype = lineup_event_type(r)
        pins = []
        if "lat" in r.keys() and r["lat"] is not None and r["lng"] is not None:
            pins = [{"lat": r["lat"], "lng": r["lng"], "kind": "pool", "label": r["venue"] or r["city"] or ""}]
        if intent == "considering":
            count_line = "%d interested" % interested_n
            if going_n: count_line += " · %d going" % going_n
        elif interested_n:
            count_line = "%d going · %d interested" % (going_n, interested_n)
        else:
            count_line = "%d going" % going_n
        if wait_n: count_line += " · %d waitlisted" % wait_n
        cap = r["capacity"]
        full = bool(cap and going_n >= cap)
        start, end = event_window(r)
        out.append({"id": r["id"], "title": r["title"], "slug": r["cat_slug"] or "", "category": r["cat_name"] or r["kind"] or "Event",
            "event_type": etype, "tag": lineup_tag(r), "days": span, "pins": pins,
            "status_kind": status_kind, "status_text": status_text, "people": people,
            "chip": r["cat_chip"] or "", "subtype": r["subtype"] or "", "hosting": r["hosting"] if r["hosting"] in ("Away", "Hosting") else "",
            "official": bool(r["official"]), "intent": intent, "status": r["status"] or "published", "status_label": lineup_status_label(r),
            "host_line": lineup_host_line(r), "member_event": not r["official"], "featured": bool(r["featured"]),
            "where": lineup_where(r["city"] or "", r["venue"] or ""), "map_href": lineup_map_href(r["city"] or "", r["venue"] or ""),
            "dir_href": lineup_dir_href(r["city"] or "", r["venue"] or ""),
            "when": lineup_when_label(r), "date": r["date"], "end_date": r["end_date"] or r["date"],
            "precision": r["date_precision"] if "date_precision" in r.keys() and r["date_precision"] else "exact",
            "tile": lineup_tile(r),
            "venue": r["venue"] or "", "city": r["city"] or "",
            "host_org": (r["host_org"] or "") if "host_org" in r.keys() and r["hosting"] == "Away" else "",
            "description": r["description"] or "", "details": r["details"] or "", "link": r["link"] or "",
            "cost": r["cost"] or "", "capacity": cap, "full": full, "reg_deadline": r["reg_deadline"] or "",
            "review_note": r["review_note"] or "", "banner": r["banner"] or "",
            "going_n": going_n, "interested_n": interested_n, "wait_n": wait_n, "count_line": count_line,
            "roster": names, "mine": mine.get(r["id"]), "created_by": r["created_by"], "host_id": r["host_id"],
            "can_edit": lineupfeed.can_edit_event(me(), r, organizer) if me() else False,
            "can_review": organizer, "chip_label": event_chip_label(start, end),
            "submitted": (r["submitted_at"] or "")[:10],
            "sports_line": sports.sports_line(r["skill_levels"] if "skill_levels" in r.keys() else "", r["divisions"] if "divisions" in r.keys() else "", r["division_custom"] if "division_custom" in r.keys() else "", r["comp_format"] if "comp_format" in r.keys() else ""),
            "levels_raw": r["skill_levels"] if "skill_levels" in r.keys() else ""})
    return out
def lineup_groups(rows):
    groups = []
    for e in rows:
        label = lineup_month(e["date"])
        if not groups or groups[-1]["label"] != label: groups.append({"label": label, "events": []})
        groups[-1]["events"].append(e)
    return groups
def profile_lineup(d, member_id, kind):
    """Events for the profile chips. Interested is Going or Interested. Mine is created or hosted."""
    rows = lineup_query(d)
    if kind == "mine":
        raw = [r for r in rows if r["created_by"] == member_id or r["host_id"] == member_id]
    else:
        wanted = {r[0] for r in d.execute(
            "SELECT event_id FROM lineup_rsvps WHERE member_id=? AND state IN ('interested','going','waitlist')", (member_id,))}
        raw = [r for r in rows if r["id"] in wanted and (r["status"] or "") == "published"]
    packed = lineup_pack(d, raw)
    today = today_pt().isoformat()
    def ends(e):
        return str(e.get("end_date") or e.get("date") or "")[:10]
    upcoming = sorted((e for e in packed if ends(e) >= today), key=lambda e: (e["date"] or "", e["id"]))
    past = sorted((e for e in packed if ends(e) < today), key=lambda e: (e["date"] or "", e["id"]), reverse=True)
    return lineup_groups(upcoming), lineup_groups(past), len(past)
def _lineup_back(raw):
    raw = (raw or "").strip()
    if raw in ("/lineup", "/home", "/profile") or raw.startswith("/lineup/"): return raw
    if raw in ("/profile?tab=general", "/profile?tab=interested", "/profile?tab=mine"): return raw
    return "/lineup"
def notify_lineup_people(d, members, title, body, url="/lineup"):
    for m in members:
        if not m or (m["role"] or "") == "system": continue
        d.execute("INSERT INTO notices(member_id, body) VALUES(?,?)", (m["id"], body))
        try: push_member(d, m, "lineup", title, body, url)
        except Exception as e: app.logger.warning("lineup notify failed: %s", e)
def lineup_rsvp_members(d, eid, states):
    marks = ",".join("?" * len(states))
    return d.execute("""SELECT m.* FROM lineup_rsvps r JOIN members m ON m.id=r.member_id
        WHERE r.event_id=? AND r.state IN (%s) AND COALESCE(m.role,'')!='system'""" % marks, (eid, *states)).fetchall()
def notify_lineup_review(d, event, kind):
    creator = d.execute("SELECT * FROM members WHERE id=?", (event["created_by"],)).fetchone() if event["created_by"] else None
    title = event["title"]
    if kind == "approved":
        body = "Your event %s is on the Lineup." % title
    elif kind == "changes":
        body = "Changes requested for %s. %s" % (title, event["review_note"] or "")
    elif kind == "declined":
        body = "%s was declined. %s" % (title, event["review_note"] or "")
    elif kind == "submitted":
        who = display_first(me()) if me() else "A member"
        body = "%s suggested %s." % (who, title)
        admins = d.execute("SELECT * FROM members WHERE is_admin=1 AND COALESCE(role,'')!='system'").fetchall()
        notify_lineup_people(d, admins, "Lineup suggestion", body.strip(), "/admin/approvals")
        return
    elif kind == "official":
        body = "%s is an official Grunions event. Your interest is saved." % title
        notify_lineup_people(d, lineup_rsvp_members(d, event["id"], ("interested",)), "We're official", body, "/lineup/%d" % event["id"])
        return
    elif kind == "dated":
        body = "%s now has dates: %s." % (title, lineup_when_label(event))
        notify_lineup_people(d, lineup_rsvp_members(d, event["id"], ("going", "interested")), "Dates are set", body, "/lineup/%d" % event["id"])
        return
    elif kind == "changed":
        body = "%s has a new date or location." % title
        notify_lineup_people(d, lineup_rsvp_members(d, event["id"], ("going", "interested", "waitlist")), "Event updated", body, "/lineup/%d" % event["id"])
        if creator and (not me() or creator["id"] != me()["id"]):
            notify_lineup_people(d, [creator], "Event updated", body, "/lineup/%d" % event["id"])
        return
    elif kind == "canceled":
        body = "%s was canceled." % title
        people = list(lineup_rsvp_members(d, event["id"], ("going", "interested", "waitlist")))
        if creator and (not me() or creator["id"] != me()["id"]): people.append(creator)
        notify_lineup_people(d, people, "Event canceled", body, "/lineup/%d" % event["id"])
        return
    else:
        return
    if creator: notify_lineup_people(d, [creator], "Lineup", body.strip(), "/lineup/%d" % event["id"])
def apply_lineup_side_effects(d, info, before):
    row = lineup_event_row(d, info["id"])
    if info.get("submitted"): notify_lineup_review(d, row, "submitted")
    if info.get("promoted"): notify_lineup_review(d, row, "official")
    if info.get("dates_set"): notify_lineup_review(d, row, "dated")
    elif info.get("date_changed"): notify_lineup_review(d, row, "changed")
    if info.get("canceled"): notify_lineup_review(d, row, "canceled")
    return row
def set_lineup_rsvp(d, row, action):
    if (row["status"] or "") != "published": abort(400)
    eid, mid = row["id"], me()["id"]
    if action == "clear":
        prev = d.execute("SELECT state FROM lineup_rsvps WHERE event_id=? AND member_id=?", (eid, mid)).fetchone()
        d.execute("DELETE FROM lineup_rsvps WHERE event_id=? AND member_id=?", (eid, mid))
        if prev and prev["state"] == "going": _promote_waitlist(d, row)
        return
    if action not in ("interested", "going", "notgoing"): abort(400)
    state = action
    if action == "going":
        deadline = (row["reg_deadline"] or "")[:10]
        if deadline and deadline < today_pt().isoformat():
            raise ValueError("Registration is closed.")
        cap = row["capacity"]
        already = d.execute("SELECT state FROM lineup_rsvps WHERE event_id=? AND member_id=?", (eid, mid)).fetchone()
        going_now = d.execute("SELECT COUNT(*) FROM lineup_rsvps WHERE event_id=? AND state='going' AND member_id!=?", (eid, mid)).fetchone()[0]
        if cap and going_now >= cap and not (already and already["state"] == "going"):
            state = "waitlist"
    going_col = 1 if state == "going" else 0
    prev = d.execute("SELECT state FROM lineup_rsvps WHERE event_id=? AND member_id=?", (eid, mid)).fetchone()
    d.execute("""INSERT INTO lineup_rsvps(event_id, member_id, going, state) VALUES(?,?,?,?)
        ON CONFLICT(event_id, member_id) DO UPDATE SET going=excluded.going, state=excluded.state, at=CURRENT_TIMESTAMP""",
        (eid, mid, going_col, state))
    if prev and prev["state"] == "going" and state != "going": _promote_waitlist(d, row)
def _promote_waitlist(d, row):
    cap = row["capacity"]
    if not cap: return
    going_now = d.execute("SELECT COUNT(*) FROM lineup_rsvps WHERE event_id=? AND state='going'", (row["id"],)).fetchone()[0]
    if going_now >= cap: return
    nxt = d.execute("""SELECT member_id FROM lineup_rsvps WHERE event_id=? AND state='waitlist' ORDER BY at, member_id LIMIT 1""", (row["id"],)).fetchone()
    if not nxt: return
    d.execute("UPDATE lineup_rsvps SET state='going', going=1 WHERE event_id=? AND member_id=?", (row["id"], nxt["member_id"]))
    member = d.execute("SELECT * FROM members WHERE id=?", (nxt["member_id"],)).fetchone()
    notify_lineup_people(d, [member], "You're in", "A spot opened for %s. You're going." % row["title"], "/lineup/%d" % row["id"])
def lineup_template_ctx(d, mode, values, event_id=None, banner=""):
    types = list(lineupfeed.MEMBER_TYPES if not can_host_practice() else lineupfeed.EVENT_TYPES)
    cities = [r[0] for r in d.execute("SELECT DISTINCT trim(city) FROM lineup_events WHERE trim(COALESCE(city,''))!='' ORDER BY 1")]
    return dict(event_types=types, values=values, mode=mode, event_id=event_id, banner=banner or "",
        organizer=can_host_practice(), save_label=("Submit" if mode == "suggest" else "Save"), sports_row=None, cities=cities)
def suggest_places(q):
    """Place names for the city field. A map link is not a place."""
    q = " ".join(str(q or "").split())
    if len(q) < 3 or q.lower().startswith(("http://", "https://")): return []
    key = "suggest:" + q.casefold()
    if key in _GEO_CACHE: return _GEO_CACHE[key]
    url = "https://nominatim.openstreetmap.org/search?" + urllib.parse.urlencode({"q": q, "format": "jsonv2", "limit": "5"})
    req = urllib.request.Request(url, headers={"User-Agent": "GrunionsWaterPolo/1.0 (team practice map)", "Accept": "application/json"})
    names = []
    try:
        with urllib.request.urlopen(req, timeout=3) as resp:
            data = json.loads(resp.read().decode() or "[]")
        for item in data:
            name = " ".join(str(item.get("display_name") or "").split())
            if name and name not in names: names.append(name)
    except Exception as e:
        app.logger.info("place suggest failed: %s", e)
    _GEO_CACHE[key] = names[:5]
    return names[:5]
def _save_lineup(d, existing=None):
    form = _form_last()
    banner = None
    f = request.files.get("banner") if request.files else None
    if f and f.filename: banner = save_banner(f)
    try:
        info = lineupfeed.save_event(d, form, me(), can_host_practice(), existing=existing, banner=banner,
            banner_clear=form.get("banner_clear") == "1", parse_date=parse_date)
    except PermissionError:
        abort(403)
    apply_lineup_side_effects(d, info, existing)
    cat = d.execute("SELECT slug FROM lineup_categories c JOIN lineup_events e ON e.category_id=c.id WHERE e.id=?", (info["id"],)).fetchone()
    slug = cat["slug"] if cat else ""
    levels = sports.pack_levels(request.form.getlist("level"))
    divs, custom = sports.pack_divisions(request.form.getlist("division"), request.form.get("division_custom"))
    comp = sports.pack_format(request.form.get("comp_format")) if slug == "travel" else ""
    sport = " ".join((request.form.get("sport") or "").split())[:40]
    d.execute("UPDATE lineup_events SET skill_levels=?, divisions=?, division_custom=?, comp_format=?, sport=? WHERE id=?",
              (levels, divs, custom, comp, sport or "Water Polo", info["id"]))
    d.commit()
    return info
@app.route("/api/places")
@login_required
def api_places():
    return jsonify(suggest_places(request.args.get("q")))
@app.route("/lineup", methods=["GET", "POST"])
@login_required
def lineup():
    d = db()
    if request.method == "POST":
        action = (request.form.get("action") or "").strip()
        eid = request.form.get("event_id", type=int)
        row = lineup_event_row(d, eid) if eid else None
        if not row: abort(404)
        back = _lineup_back(request.form.get("back"))
        if action == "official":
            if not can_host_practice(): abort(403)
            if (row["team_intent"] or "") == "considering":
                d.execute("UPDATE lineup_events SET team_intent='official', stage='going' WHERE id=?", (eid,))
                d.commit(); notify_lineup_review(d, lineup_event_row(d, eid), "official"); d.commit()
            return redirect(back if back.startswith("/lineup/") else "/lineup/%d" % eid)
        try: set_lineup_rsvp(d, row, action)
        except ValueError as e:
            flash(str(e)); return redirect(back)
        d.commit()
        return redirect(back)
    cat = lineupfeed.filter_type((request.args.get("cat") or "").strip())
    raw = lineup_query(d)
    now = wall_pt()
    rows = lineup_pack(d, raw)
    by_id = {r["id"]: r for r in raw}
    def still_on(e):
        return event_window(by_id[e["id"]])[1] >= now
    public = [e for e in rows if e["status"] == "published" and (not cat or e["event_type"] == cat)]
    def feed_key(e): return (e["date"], 0 if e.get("precision") == "month" else 1, e["id"])
    upcoming = sorted((e for e in public if still_on(e)), key=feed_key)
    past = sorted((e for e in public if not still_on(e)), key=feed_key, reverse=True)
    featured = [e for e in upcoming if e["featured"]]
    rest = [e for e in upcoming if not e["featured"]]
    return page(T["lineup"], tab="lineup", featured=featured, upcoming=lineup_groups(rest), past=lineup_groups(past), past_n=len(past),
        cat=cat, filter_types=list(lineupfeed.EVENT_TYPES), empty_public=not upcoming and not past)
@app.route("/lineup/new", methods=["GET", "POST"])
@login_required
def lineup_new():
    d = db()
    mode = (request.args.get("mode") or request.form.get("mode") or ("create" if can_host_practice() else "suggest")).strip()
    if not can_host_practice() and mode not in ("suggest", "propose"): abort(403)
    if not can_host_practice() and mode == "propose": mode = "suggest"
    values = lineupfeed.form_values(mode=mode)
    asked = (request.args.get("event_type") or "").strip()
    if request.method == "GET" and asked in lineupfeed.EVENT_TYPES:
        values["event_type"] = asked
    if request.method == "POST":
        try:
            info = _save_lineup(d)
            flash("Submitted" if info["status"] == "pending" else "Saved", "toast")
            return redirect("/lineup/%d" % info["id"] if info["status"] == "published" else "/lineup")
        except ValueError as e:
            flash(str(e)); values = lineupfeed.form_values(_form_last(), mode=mode)
    ctx = lineup_template_ctx(d, mode, values)
    return page(T["lineup_edit"], tab="lineup_edit", action="/lineup/new", **ctx)
@app.route("/lineup/<int:eid>", methods=["GET", "POST"])
@login_required
def lineup_detail(eid):
    d = db()
    row = lineup_event_row(d, eid)
    if not row or not lineup_seen(row, me()): abort(404)
    if request.method == "POST":
        action = (request.form.get("action") or "").strip()
        if action == "official":
            if not can_host_practice(): abort(403)
            if (row["team_intent"] or "") == "considering":
                d.execute("UPDATE lineup_events SET team_intent='official', stage='going' WHERE id=?", (eid,))
                d.commit(); notify_lineup_review(d, lineup_event_row(d, eid), "official"); d.commit()
            return redirect("/lineup/%d" % eid)
        try: set_lineup_rsvp(d, row, action)
        except ValueError as e:
            flash(str(e)); return redirect("/lineup/%d" % eid)
        d.commit(); return redirect("/lineup/%d" % eid)
    row = ensure_lineup_coords(d, row)
    packed = lineup_pack(d, [row])[0]
    return page(T["lineup_event"], tab="lineup_event", e=packed, from_admin=request.args.get("from") == "admin", admin_date=(request.args.get("date") or row["date"] or "")[:10])
@app.route("/lineup/<int:eid>/edit", methods=["GET", "POST"])
@login_required
def lineup_edit(eid):
    d = db()
    row = lineup_event_row(d, eid)
    if not row: abort(404)
    if not lineupfeed.can_edit_event(me(), row, can_host_practice()): abort(403)
    if request.method == "POST" and request.form.get("action") == "delete":
        if not can_host_practice() and (row["status"] or "") not in ("draft", "declined", "changes_requested"): abort(403)
        d.execute("DELETE FROM lineup_rsvps WHERE event_id=?", (eid,))
        d.execute("DELETE FROM lineup_events WHERE id=?", (eid,))
        d.commit(); flash("Deleted", "toast"); return redirect("/lineup")
    values = lineupfeed.form_values(row=row, cat_slug=row["cat_slug"] or "", mode="edit")
    if request.method == "POST":
        try:
            info = _save_lineup(d, row)
            flash("Submitted" if info["status"] == "pending" else "Saved", "toast")
            return redirect("/lineup/%d" % eid if info["status"] == "published" else "/lineup")
        except ValueError as e:
            flash(str(e)); values = lineupfeed.form_values(_form_last(), mode="edit")
    ctx = lineup_template_ctx(d, "edit", values, event_id=eid, banner=row["banner"] or "")
    ctx["sports_row"] = row
    ctx["show_cancel"] = can_host_practice() and (row["status"] or "") == "published"
    ctx["show_delete"] = can_host_practice() or (row["created_by"] == me()["id"] and (row["status"] or "") in ("draft", "declined", "changes_requested"))
    return page(T["lineup_edit"], tab="lineup_edit", action="/lineup/%d/edit" % eid, **ctx)
@app.route("/lineup-image/<int:eid>")
@login_required
def lineup_image(eid):
    row = lineup_event_row(db(), eid)
    if not row or not lineup_seen(row, me()): abort(404)
    fn = _stored_file(row["banner"] or "")
    if not fn: abort(404)
    resp = send_from_directory(UPLOADS, fn, max_age=86400)
    resp.headers["Cache-Control"] = "private, max-age=86400"
    return resp
def events_hub_groups(d):
    """Upcoming practices and Lineup events, one group per type."""
    now = wall_pt()
    buckets = {}
    def add(label, item):
        buckets.setdefault(label, []).append(item)
    today = today_pt().isoformat()
    for p in d.execute("SELECT * FROM practices WHERE cancelled=0 AND date>=? ORDER BY date, start, id", (today,)):
        kind = (p["activity_type"] or "practice") if "activity_type" in p.keys() else "practice"
        if kind not in sports.ACTIVITY_IDS: kind = "practice"
        add(sports.ACTIVITY_NAME.get(kind, "Practice"), {
            "title": practice_title(p),
            "when": "%s · %s" % (fmt_d(p["date"]), fmt_span(p["start"] or "19:00", p["end"] or "20:30")),
            "place": p["location"] or "",
            "href": "/practices/%d?from=admin" % p["id"],
            "sort": (p["date"] or "", p["start"] or "", p["id"]),
        })
    raw = []
    for r in lineup_query(d):
        if (r["status"] or "") != "published": continue
        try:
            if event_window(r)[1] < now: continue
        except (TypeError, ValueError):
            continue
        raw.append(r)
    for e in lineup_pack(d, raw):
        add(e.get("event_type") or "Event", {
            "title": e["title"],
            "when": e["when"],
            "place": e["where"],
            "href": "/lineup/%d?from=admin" % e["id"],
            "sort": (e["date"] or "", e["id"]),
        })
    order = ["Practice", "Scrimmage", "Game", "Hybrid", "Clinic", "Tournament", "Trip", "Social", "Volunteer"]
    groups = []
    for label in order:
        if label in buckets:
            groups.append({"label": label, "items": sorted(buckets.pop(label), key=lambda item: item["sort"])})
    for label in sorted(buckets):
        groups.append({"label": label, "items": sorted(buckets[label], key=lambda item: item["sort"])})
    return groups
@app.route("/admin/approvals", methods=["GET", "POST"])
@login_required
def approvals():
    if not can_host_practice(): abort(403)
    d = db()
    if request.method == "POST":
        action = (request.form.get("action") or "").strip()
        if action == "category_add":
            name = " ".join((request.form.get("name") or "").split())[:80]
            chip = " ".join((request.form.get("chip") or "").split())[:40]
            if not name or not chip: flash("Add a name and a short filter label."); return redirect("/admin/approvals")
            slug = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")[:40] or "category"
            base, n = slug, 2
            while d.execute("SELECT 1 FROM lineup_categories WHERE slug=?", (slug,)).fetchone():
                slug = "%s-%d" % (base, n); n += 1
            sort = (d.execute("SELECT COALESCE(MAX(sort),0) FROM lineup_categories").fetchone()[0] or 0) + 1
            d.execute("""INSERT INTO lineup_categories(slug, name, chip, member_ok, intent_ok, hosting_ok, sort, active)
                VALUES(?,?,?,?,?,?,?,1)""", (slug, name, chip, 1 if request.form.get("member_ok") else 0,
                1 if request.form.get("intent_ok") else 0, 1 if request.form.get("hosting_ok") else 0, sort))
            d.commit(); flash("Category added", "toast"); return redirect("/admin/approvals")
        if action == "category_toggle":
            cid = request.form.get("category_id", type=int)
            if cid: d.execute("UPDATE lineup_categories SET active=CASE WHEN active=1 THEN 0 ELSE 1 END WHERE id=?", (cid,)); d.commit()
            return redirect("/admin/approvals")
        if action == "create_session":
            activity = (request.form.get("activity_type") or "practice").strip().lower()
            if activity not in ("practice", "scrimmage"): activity = "practice"
            day = parse_date(request.form.get("date"))
            loc = " ".join((request.form.get("location") or "").split())[:300]
            if not day: flash("Add a date."); return redirect("/admin/approvals")
            if not loc: flash("Add a location."); return redirect("/admin/approvals")
            start = (request.form.get("start") or "19:00").strip() or "19:00"
            end = (request.form.get("end") or "20:30").strip() or "20:30"
            try:
                sp = sports.sports_from_form(request.form)
                sp["activity_type"] = activity
                d.execute("""INSERT INTO practices(date,start,end,location,note,activity_type,sport,title,skill_levels,divisions,division_custom,opponent,home_away,gameplay_notes,segments,comp_format)
                    VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                    (day.isoformat(), start, end, loc, "", *sports.sports_tuple(sp)))
                d.commit(); flash("Created", "toast")
            except sqlite3.IntegrityError:
                flash("A practice already exists at that place on that date.")
            return redirect("/admin/approvals")
        eid = request.form.get("event_id", type=int)
        row = lineup_event_row(d, eid) if eid else None
        if not row: abort(404)
        if action == "approve":
            d.execute("UPDATE lineup_events SET status='published', official=0, review_note='' WHERE id=?", (eid,))
            d.commit(); notify_lineup_review(d, lineup_event_row(d, eid), "approved"); d.commit()
            flash("Published", "toast")
        elif action == "changes":
            note = (request.form.get("note") or "").strip()[:500]
            if not note: flash("Add a note for the host."); return redirect("/admin/approvals")
            d.execute("UPDATE lineup_events SET status='changes_requested', review_note=? WHERE id=?", (note, eid))
            d.commit(); notify_lineup_review(d, lineup_event_row(d, eid), "changes"); d.commit()
            flash("Sent back", "toast")
        elif action == "decline":
            note = (request.form.get("note") or "").strip()[:500]
            if not note: flash("Add a reason."); return redirect("/admin/approvals")
            d.execute("UPDATE lineup_events SET status='declined', review_note=? WHERE id=?", (note, eid))
            d.commit(); notify_lineup_review(d, lineup_event_row(d, eid), "declined"); d.commit()
            flash("Declined", "toast")
        else: abort(400)
        return redirect("/admin/approvals")
    queue = lineup_pack(d, [r for r in lineup_query(d) if (r["status"] or "") in ("pending", "changes_requested")])
    queue.sort(key=lambda e: (0 if e["status"] == "pending" else 1, e["submitted"], e["id"]))
    return page(T["approvals"], tab="admin", queue=queue, groups=events_hub_groups(d))
def next_commitment(d, mid):
    """Earliest committed thing: an in-progress item beats a later one. Interested and Considering stay off Home."""
    now = wall_pt()
    cands = []
    for p in d.execute("SELECT * FROM practices WHERE cancelled=0 AND " + upcoming_where(), upcoming_bounds()):
        day = dt.date.fromisoformat(p["date"])
        sh, sm = [int(x) for x in (p["start"] or "19:00").split(":")[:2]]
        eh, em = [int(x) for x in (p["end"] or "20:30").split(":")[:2]]
        start = dt.datetime.combine(day, dt.time(sh, sm))
        end = dt.datetime.combine(day, dt.time(eh, em))
        cands.append((0 if start <= now <= end else 1, start, 0, "practice", p))
    for e in d.execute("""SELECT e.*, c.intent_ok, r.state FROM lineup_events e
        JOIN lineup_categories c ON c.id=e.category_id
        JOIN lineup_rsvps r ON r.event_id=e.id AND r.member_id=? AND r.state='going'
        WHERE e.status='published'""", (mid,)):
        if e["intent_ok"] and (e["team_intent"] or "") != "official": continue
        if (e["date_precision"] or "") == "month": continue
        start, end = event_window(e)
        if end < now: continue
        cands.append((0 if start <= now <= end else 1, start, 1, "event", e))
    if not cands: return None
    cands.sort(key=lambda c: (c[0], c[1], c[2]))
    return cands[0][3], cands[0][4]
@app.route("/api/unread")
@login_required
def api_unread():
    return jsonify(compute_unread(db(), me()))
@app.route("/api/practices/<int:pid>/seen", methods=["POST"])
@login_required
def api_practice_seen(pid):
    d = db()
    if not d.execute("SELECT 1 FROM practices WHERE id=?", (pid,)).fetchone(): abort(404)
    mark_practice_seen(d, me()["id"], pid); d.commit()
    g._unread_mid = None
    return jsonify(ok=True, unread=compute_unread(d, me()))

# ---------- verification requests (bot) ----------
BOT_EMAIL = "bot@grunions.local"
def bot_member_id(d):
    r = d.execute("SELECT id FROM members WHERE email=?", (BOT_EMAIL,)).fetchone()
    if r: return r["id"]
    return d.execute("INSERT INTO members(first,last,email,phone,role) VALUES('Grunions','bot',?,'','system')", (BOT_EMAIL,)).lastrowid
def drop_bot_verify_messages(d):
    """Verification results are not chat. Remove any the bot already posted, on any channel."""
    row = d.execute("SELECT id FROM members WHERE email=?", (BOT_EMAIL,)).fetchone()
    if not row: return
    ids = [r[0] for r in d.execute("SELECT id FROM messages WHERE member_id=? AND body LIKE 'Verification for %'", (row["id"],))]
    if not ids: return
    marks = ",".join("?" * len(ids))
    d.execute("DELETE FROM reactions WHERE message_id IN (%s)" % marks, ids)
    d.execute("DELETE FROM messages WHERE id IN (%s)" % marks, ids)
    d.commit()
def vr_dict(r):
    return {k: r[k] for k in ("id", "member_id", "name", "email", "member_number", "requested_by", "status", "created", "answered", "note")} | {"member_submitted": bool(r["member_submitted"]), "result": json.loads(r["result"]) if r["result"] else None}
def webhook_headers():
    h = {"Content-Type": "application/json"}
    if VERIFY_WEBHOOK_KEY:
        h[VERIFY_WEBHOOK_HEADER or "Authorization"] = VERIFY_WEBHOOK_KEY if VERIFY_WEBHOOK_HEADER else "Bearer " + VERIFY_WEBHOOK_KEY
    return h
def post_verify_webhook(row, preferred_first=None):
    """POST a verify request. Failures are logged and never raised."""
    if not VERIFY_WEBHOOK_URL: return "skipped (no VERIFY_WEBHOOK_URL)"
    payload = {"request_id": row["id"], "member_id": row["member_id"], "name": row["name"], "preferred_first": clean_preferred(preferred_first),
               "email": row["email"], "member_number": row["member_number"], "requested_by": row["requested_by"],
               "member_submitted": bool(row["member_submitted"]), "app_url": PUBLIC_URL}
    try:
        req = urllib.request.Request(VERIFY_WEBHOOK_URL, data=json.dumps(payload).encode(), headers=webhook_headers(), method="POST")
        with urllib.request.urlopen(req, timeout=5) as resp: return f"sent ({resp.status})"
    except Exception as e:
        app.logger.warning("verify webhook failed: %s", e)
        return f"failed: {e.__class__.__name__}"
def create_verify_request(d, mid, update_pending=False):
    m = d.execute("SELECT * FROM members WHERE id=?", (mid,)).fetchone()
    pending = d.execute("SELECT id FROM verify_requests WHERE member_id=? AND status='pending' ORDER BY id DESC LIMIT 1", (mid,)).fetchone()
    if pending:
        if not update_pending: return "A verification request is already pending."
        d.execute("UPDATE verify_requests SET member_number=? WHERE id=?", (m["usawp_number"], pending["id"])); d.commit()
        r = d.execute("SELECT * FROM verify_requests WHERE id=?", (pending["id"],)).fetchone()
        wh = post_verify_webhook(r, m["preferred_first"])
        d.execute("UPDATE verify_requests SET webhook=? WHERE id=?", (wh, pending["id"])); d.commit()
        return f"Updated the pending verification request for {m['first']} {m['last']}. Webhook {wh}."
    now = dt.datetime.now().isoformat(timespec="seconds")
    submitted = 1 if me()["id"] == mid else 0
    rid = d.execute("INSERT INTO verify_requests(member_id,name,email,member_number,requested_by,member_submitted,created) VALUES(?,?,?,?,?,?,?)",
                    (mid, f"{m['first']} {m['last']}", m["email"], m["usawp_number"], f"{me()['first']} {me()['last']}", submitted, now)).lastrowid
    d.commit(); r = d.execute("SELECT * FROM verify_requests WHERE id=?", (rid,)).fetchone(); wh = post_verify_webhook(r, m["preferred_first"])
    d.execute("UPDATE verify_requests SET webhook=? WHERE id=?", (wh, rid)); d.commit()
    try: notify_new_verify_request(d, m)
    except Exception as e: app.logger.warning("verify-request push failed: %s", e)
    return f"Asked Grunions to verify {m['first']} {m['last']}. Webhook {wh}."
def bot_auth():
    h = request.headers.get("Authorization", "")
    if not BOT_API_KEY or not h.startswith("Bearer ") or not secrets.compare_digest(h[7:], BOT_API_KEY): abort(401)
@app.route("/api/verify-requests")
def api_verify_list():
    bot_auth(); st = request.args.get("status")
    rows = db().execute("SELECT * FROM verify_requests WHERE (? IS NULL OR status=?) ORDER BY id", (st, st)).fetchall()
    return jsonify([vr_dict(r) for r in rows])
@app.route("/api/verify-requests/<int:rid>/result", methods=["POST"])
def api_verify_result(rid):
    bot_auth(); d = db(); j = request.get_json(silent=True)
    if not isinstance(j, dict) or not isinstance(j.get("verified"), bool): return jsonify(error="JSON body with boolean 'verified' required"), 400
    r = d.execute("SELECT * FROM verify_requests WHERE id=?", (rid,)).fetchone()
    if not r: return jsonify(error="not found"), 404
    if r["status"] != "pending": return jsonify(error="already answered"), 409
    now = stamp_pt("minutes"); mid = r["member_id"]
    exp = parse_date(j.get("membership_expires_on")); num = (str(j.get("member_number") or "").strip() or None)
    if j["verified"]:
        st = "expired" if exp and exp < today_pt() else "verified"
        d.execute("""UPDATE members SET usawp_status=?, usawp_raw='Verified by Grunions bot', usawp_number=COALESCE(?,usawp_number),
          usawp_valid_until=COALESCE(?,usawp_valid_until), usawp_updated=?, usawp_verified_by='Grunions bot', usawp_verified_at=? WHERE id=?""",
          (st, num, exp and exp.isoformat(), now, now, mid))
    else:
        d.execute("UPDATE members SET usawp_status='expired', usawp_raw='Bot: not verified', usawp_number=COALESCE(?,usawp_number), usawp_updated=? WHERE id=?", (num, now, mid))
    applied, unknown = [], []
    for item, val in (j.get("compliance") or {}).items():
        q = next((q for q in d.execute("SELECT * FROM requirements") if norm(q["name"]) == norm(item) or any(k and k in norm(item) for k in (q["keywords"] or "").split(","))), None)
        e = parse_date(val)
        if not q or not e: unknown.append(item); continue
        d.execute("""INSERT INTO member_reqs VALUES(?,?,?,?,'bot','Grunions bot',?) ON CONFLICT(member_id,req_id) DO UPDATE SET
          expires_on=excluded.expires_on, completed_on=COALESCE(completed_on,excluded.completed_on), source='bot', by='Grunions bot', at=excluded.at""",
          (mid, q["id"], today_pt().isoformat(), e.isoformat(), now)); applied.append(q["name"])
    mtype = j.get("membership_type")
    if isinstance(mtype, str) and mtype.strip(): apply_membership_type(d, mid, mtype, bool(j["verified"]))
    note = (str(j.get("note") or "")[:500]) or None
    d.execute("UPDATE verify_requests SET status='done', answered=?, result=?, note=? WHERE id=?", (now, json.dumps(j), note, rid))
    expire_sweep(d)
    shown = d.execute("SELECT first, last, preferred_first FROM members WHERE id=?", (mid,)).fetchone()
    who = f"{display_first(shown)} {shown['last']}" if shown else r["name"]
    text = f"Verification for {who}: {'verified' if j['verified'] else 'NOT verified'}"
    if exp: text += f", membership expires {exp.isoformat()}"
    if applied: text += f"; updated {', '.join(applied)}"
    if note: text += f". Note: {note}"
    for a in d.execute("SELECT id FROM members WHERE is_admin=1").fetchall(): d.execute("INSERT INTO notices(member_id, body) VALUES(?,?)", (a["id"], text))
    d.commit()
    sync_practice_sheets(d)
    try: notify_verification_result(d, mid, bool(j["verified"]), exp)
    except Exception as e: app.logger.warning("verification push failed: %s", e)
    return jsonify(ok=True, request_id=rid, member_id=mid, applied_compliance=applied, ignored_compliance=unknown)

# ---------- admin ----------
def signup_url(): return (PUBLIC_URL or request.host_url.rstrip("/")) + "/join"
@app.route("/qr.svg")
@admin_required
def qr_svg():
    img = qrcode.make(signup_url(), image_factory=qrcode.image.svg.SvgPathImage, box_size=20)
    buf = io.BytesIO(); img.save(buf); return Response(buf.getvalue(), mimetype="image/svg+xml")
@app.route("/qr")
@admin_required
def qr_page():
    return page(T["qr_page"], tab="admin", u=signup_url())

DETAIL_ACTIONS = ("verify", "req", "role", "ask_bot", "preferred", "background", "recheck", "edit")
def save_req_expiry(d, mid, req, exp, by):
    if not req or not exp: return
    now = stamp_pt("minutes")
    day = exp.isoformat() if hasattr(exp, "isoformat") else str(exp)[:10]
    d.execute("""INSERT INTO member_reqs(member_id,req_id,completed_on,expires_on,source,by,at) VALUES(?,?,?,?,'manual',?,?)
        ON CONFLICT(member_id,req_id) DO UPDATE SET expires_on=excluded.expires_on,
        completed_on=COALESCE(member_reqs.completed_on, excluded.completed_on), source='manual', by=excluded.by, at=excluded.at""",
        (mid, req["id"], today_pt().isoformat(), day, by, now))
def save_sport80_recheck(d, mid, announce=True):
    """Manual Sport:80 result. Coach membership joins the coaching list and does not grant coach access."""
    verified = request.form.get("verified") == "yes"
    now = stamp_pt("minutes")
    who = "%s %s" % (me()["first"], me()["last"])
    vu = parse_date(request.form.get("valid_until"))
    mtype = (request.form.get("membership_type") or "").strip()[:120]
    status = "expired" if (verified and vu and vu < today_pt()) or not verified else "verified"
    num = (request.form.get("number") or "").strip()[:20]
    note = (request.form.get("note") or "").strip()[:500]
    raw = note or "Recorded from Sport:80"
    if num:
        d.execute("""UPDATE members SET usawp_status=?, usawp_raw=?, usawp_number=?, usawp_valid_until=COALESCE(?, usawp_valid_until),
            usawp_updated=?, usawp_verified_by=?, usawp_verified_at=? WHERE id=?""",
            (status, raw, num, vu.isoformat() if vu else None, now, who, now, mid))
    else:
        d.execute("""UPDATE members SET usawp_status=?, usawp_raw=?, usawp_valid_until=COALESCE(?, usawp_valid_until),
            usawp_updated=?, usawp_verified_by=?, usawp_verified_at=? WHERE id=?""",
            (status, raw, vu.isoformat() if vu else None, now, who, now, mid))
    if mtype: apply_membership_type(d, mid, mtype, verified)
    if not verified: drop_usawp_coaching(d, mid)
    for field, req in (("safesport_expires", safesport_req(d)), ("background_expires", background_req(d)), ("referee_expires", referee_req(d))):
        save_req_expiry(d, mid, req, parse_date(request.form.get(field)), who)
    pending = d.execute("SELECT id FROM verify_requests WHERE member_id=? AND status='pending' ORDER BY id DESC LIMIT 1", (mid,)).fetchone()
    if pending:
        d.execute("UPDATE verify_requests SET status='done', answered=?, result=?, note=? WHERE id=?",
                  (now, json.dumps({"verified": verified, "membership_type": mtype, "membership_expires_on": vu.isoformat() if vu else ""}),
                   note or "Recorded by hand from Sport:80", pending["id"]))
    if announce: flash("Saved the Sport:80 result.")
def handle_member_detail(d, mid):
    """Check-in and the members list share these edits. 'ok' saves, 'halt' leaves the row unchanged."""
    act = request.form.get("action")
    if act not in DETAIL_ACTIONS: return None
    if not me()["is_admin"]: abort(403)
    if act == "verify":
        num = (request.form.get("number") or "").strip()[:20] or None
        vu = parse_date(request.form.get("valid_until")); now = stamp_pt("minutes")
        if vu and vu < today_pt(): flash("That expiration date is in the past, so not marked verified.")
        elif not vu and not request.form.get("no_date"): flash("Please enter the expiration date from Sport:80 (or tick 'no date').")
        else:
            d.execute("""UPDATE members SET usawp_status='verified', usawp_raw='Manually verified', usawp_number=COALESCE(?,usawp_number),
              usawp_valid_until=COALESCE(?,usawp_valid_until), usawp_updated=?, usawp_verified_by=?, usawp_verified_at=? WHERE id=?""",
              (num, vu.isoformat() if vu else None, now, f"{me()['first']} {me()['last']}", now, mid))
    elif act == "ask_bot":
        flash(create_verify_request(d, mid), "toast")
    elif act == "req":
        rid = int(request.form["req_id"]); done = parse_date(request.form.get("completed_on")); exp = parse_date(request.form.get("expires_on"))
        q = d.execute("SELECT * FROM requirements WHERE id=?", (rid,)).fetchone()
        if q and q["expires"] and not exp: flash(f"Please enter the expiration date for {q['name']}.")
        elif not (done or exp): flash("Enter a completed or expiration date.")
        else:
            d.execute("""INSERT INTO member_reqs VALUES(?,?,?,?,'manual',?,?) ON CONFLICT(member_id,req_id) DO UPDATE SET completed_on=excluded.completed_on,
              expires_on=excluded.expires_on, source='manual', by=excluded.by, at=excluded.at""", (mid, rid, done and done.isoformat(), exp and exp.isoformat(),
              f"{me()['first']} {me()['last']}", dt.datetime.now().isoformat(timespec="minutes")))
    elif act == "role":
        role = request.form.get("role")
        if role != "admin" and is_last_admin(d, mid):
            flash("Can't remove the last admin.")
            return "halt"
        if role == "admin":
            d.execute("UPDATE members SET is_admin=1 WHERE id=?", (mid,))
        elif role == "coach":
            d.execute("UPDATE members SET role='coach' WHERE id=?", (mid,))
        else:
            d.execute("UPDATE members SET role='athlete', is_admin=0 WHERE id=?", (mid,))
    elif act == "preferred":
        d.execute("UPDATE members SET preferred_first=? WHERE id=?", (clean_preferred(request.form.get("preferred_first")), mid))
    elif act == "background":
        exp = parse_date(request.form.get("expires_on"))
        if not exp: flash("Enter the background screening expiration date.")
        else: save_background_expiry(d, mid, exp, f"{me()['first']} {me()['last']}")
    elif act == "recheck":
        save_sport80_recheck(d, mid)
    elif act == "edit":
        save_sport80_recheck(d, mid, announce=False)
        d.execute("UPDATE members SET preferred_first=? WHERE id=?", (clean_preferred(request.form.get("preferred_first")), mid))
        if save_legal_name(d, mid): flash("Saved.", "toast")
        else: flash("Enter a legal first and last name.", "toast")
    return "ok"
def save_legal_name(d, mid):
    """Admins may rename someone from the member page. A blank name is refused. Unchanged names are not audited."""
    if not me()["is_admin"]: abort(403)
    if "first" not in request.form and "last" not in request.form: return True
    first, last = clean_legal(request.form.get("first")), clean_legal(request.form.get("last"))
    if not first or not last: return False
    row = d.execute("SELECT first, last FROM members WHERE id=?", (mid,)).fetchone()
    if not row: return False
    old_name, new_name = "%s %s" % (row["first"], row["last"]), "%s %s" % (first, last)
    if old_name == new_name: return True
    actor = "%s %s" % (me()["first"], me()["last"])
    d.execute("UPDATE members SET first=?, last=? WHERE id=?", (first, last, mid))
    d.execute("INSERT INTO name_audits(member_id, actor_id, actor, old_name, new_name, at) VALUES(?,?,?,?,?,?)",
              (mid, me()["id"], actor, old_name, new_name, stamp_pt("minutes")))
    return True
@app.route("/admin/member/<int:mid>", methods=["GET", "POST"])
@login_required
def member_page(mid):
    """Full-page member view for an admin or a coach. Manual edits stay admin-only."""
    if not (me()["is_admin"] or is_staff()): abort(403)
    d = db()
    exists = d.execute("SELECT id FROM members WHERE id=? AND COALESCE(role,'')!='system'", (mid,)).fetchone()
    if not exists: abort(404)
    if request.method == "POST":
        detail = handle_member_detail(d, mid)
        if detail == "ok":
            d.commit()
            if request.form.get("action") in ("verify", "req", "background", "preferred", "role", "recheck", "edit"): sync_practice_sheets(d)
        return redirect(url_for("member_page", mid=mid))
    m = d.execute("""SELECT m.*,
      (SELECT status FROM verify_requests WHERE member_id=m.id ORDER BY id DESC LIMIT 1) AS vr_status,
      (SELECT note FROM verify_requests WHERE member_id=m.id ORDER BY id DESC LIMIT 1) AS vr_note
      FROM members m WHERE m.id=?""", (mid,)).fetchone()
    hist = d.execute("SELECT practice_date FROM checkins WHERE member_id=?", (mid,)).fetchall()
    month = today_pt().strftime("%Y-%m")
    editing = request.args.get("edit") == "1" and bool(me()["is_admin"])
    audits = d.execute("SELECT actor, old_name, new_name, at FROM name_audits WHERE member_id=? ORDER BY id DESC LIMIT 8", (mid,)).fetchall()
    return page(T["member"], tab="member", m=m, hist=hist, nmonth=sum(1 for h in hist if (h["practice_date"] or "").startswith(month)), editing=editing, audits=audits)
def members_back():
    view = request.form.get("list_view") or ""
    if request.form.get("list_coach") == "eligible": view = view or "coaches"
    if request.form.get("list_referee") == "eligible": view = view or "referees"
    q = (request.form.get("q") or "").strip()
    kwargs = {}
    if view in ("coaches", "admins", "referees", "expiring", "uncleared"): kwargs["view"] = view
    if q: kwargs["q"] = q
    return redirect(url_for("members", **kwargs))
def checkin_filter(raw, n_not, n_in):
    """Going is the default. A Not Going or Checked in view with nobody in it falls back."""
    filt = raw if raw in ("not", "in") else "going"
    if filt == "not" and n_not <= 0: return "going"
    if filt == "in" and n_in <= 0: return "going"
    return filt
@app.route("/admin", methods=["GET", "POST"])
@staff_required
def admin():
    d = db(); posted = request.values.get("date")
    if request.method == "POST" and request.form.get("action") == "walkin":
        abort(400)
    if request.method == "POST":
        date = posted or today_pt().isoformat()
        mid = int(request.form["member_id"])
        detail = handle_member_detail(d, mid)
        if detail == "halt": return redirect(request.full_path)
        who = d.execute("SELECT first, last, preferred_first FROM members WHERE id=?", (mid,)).fetchone()
        if detail is None:
            if request.form.get("action") == "undo":
                d.execute("DELETE FROM checkins WHERE member_id=? AND practice_date=?", (mid, date))
                if who: flash("Undid check-in for %s." % display_first(who), "toast")
            else:
                d.execute("INSERT OR IGNORE INTO checkins(member_id,practice_date,location) VALUES(?,?,?)", (mid, date, location_for(date)))
                if who: flash("Checked in %s." % display_first(who), "toast")
        d.commit()
        if request.form.get("action") in ("verify", "req", "background", "preferred", "role", "recheck", "edit", "undo") or not request.form.get("action"): sync_practice_sheets(d)
        q = request.form.get("q", "")
        events = admin_day_events(d, date)
        ev = (request.form.get("ev") or "").strip()
        selected = next((e for e in events if e["key"] == ev), events[0] if events else None)
        going, not_going, rest, checked = admin_people(d, date, selected, q)
        filt = checkin_filter(request.form.get("filt"), len(not_going), len(checked))
        kwargs = {"date": date, "q": q}
        if filt != "going": kwargs["filt"] = filt
        if selected: kwargs["ev"] = selected["key"]
        return redirect(url_for("admin", **kwargs))
    ensure_schedule(d)
    days = schedule_days(d)
    date = posted or default_checkin_date(days)
    q = request.args.get("q", "").strip()
    events = admin_day_events(d, date)
    ev = (request.args.get("ev") or "").strip()
    selected = next((e for e in events if e["key"] == ev), events[0] if events else None)
    going, not_going, rest, checked = admin_people(d, date, selected, q)
    n_not, n = len(not_going), len(checked)
    filt = checkin_filter(request.args.get("filt"), n_not, n)
    pr = d.execute("SELECT * FROM practices WHERE id=?", (selected["id"],)).fetchone() if selected and selected["kind"] == "practice" else None
    evkey = selected["key"] if selected else ""
    ev_i = ([e["key"] for e in events].index(evkey) + 1) if evkey and events else 0
    prev_step = admin_step(d, days, date, events, evkey, -1)
    next_step = admin_step(d, days, date, events, evkey, 1)
    return page(T["admin"],
        tab="admin", date=date, q=q, going=going, rest=rest, not_going=not_going, checked=checked, n=n, n_not=n_not, filt=filt,
        loc=(selected["place"] if selected else ""), pr=pr, sel=selected, events=events, evkey=evkey,
        ev_i=ev_i, ev_n=len(events),
        prev_href=admin_href(prev_step[0], prev_step[1], filt, q) if prev_step else "",
        next_href=admin_href(next_step[0], next_step[1], filt, q) if next_step else "",
        days=days, catalog=admin_catalog(d, days), month=checkin_month(date, days), today=today_pt().isoformat())

def expiring_roster(d, rep):
    ids = []
    seen = set()
    for bucket in rep.values():
        for item in bucket:
            if item["id"] not in seen:
                seen.add(item["id"]); ids.append(item["id"])
    if not ids: return []
    qmarks = ",".join("?" * len(ids))
    rows = d.execute("""SELECT m.*,
      (SELECT status FROM verify_requests WHERE member_id=m.id ORDER BY id DESC LIMIT 1) AS vr_status,
      (SELECT note FROM verify_requests WHERE member_id=m.id ORDER BY id DESC LIMIT 1) AS vr_note
      FROM members m WHERE m.id IN (%s)""" % qmarks, ids).fetchall()
    by_id = {r["id"]: r for r in rows}
    return [by_id[i] for i in ids if i in by_id]
@app.route("/expiring", methods=["GET", "POST"])
@admin_required
def expiring():
    d = db(); days = request.values.get("days", EXPIRING_DAYS, type=int) or EXPIRING_DAYS
    if request.method == "POST" and request.form.get("action") == "ask_all":
        rep = expiry_report(d, days)
        ids = [r["id"] for r in expiring_roster(d, rep)]
        asked = sum(1 for mid in ids if create_verify_request(d, mid).startswith("Asked"))
        if not ids: flash("No one to recheck.", "toast")
        else: flash("Asked Grunions to recheck %d %s." % (asked, "person" if asked == 1 else "people"), "toast")
        return redirect(url_for("expiring", days=days))
    if request.method == "POST" and request.form.get("member_id") and request.form.get("action") in DETAIL_ACTIONS:
        mid = int(request.form["member_id"])
        detail = handle_member_detail(d, mid)
        if detail == "ok":
            d.commit()
            if request.form.get("action") in ("verify", "req", "background", "preferred", "role", "recheck", "edit"): sync_practice_sheets(d)
        return redirect(url_for("expiring", days=days))
    if request.method == "POST":
        ids = [int(request.form["member_id"])] if request.form.get("member_id") else [x["id"] for k, v in expiry_report(d, days).items() for x in v]
        for mid in ids: remind(d, mid, by=f"{me()['first']} {me()['last']}")
        d.commit(); flash(f"In-app reminder posted to {len(ids)} member(s)."); return redirect(url_for("expiring", days=days))
    rep = expiry_report(d, days)
    return page(T["expiring"], tab="admin", rep=rep, days=days, roster=expiring_roster(d, rep), date="", q="")
@app.route("/requirements", methods=["GET", "POST"])
@admin_required
def requirements_page():
    d = db()
    if request.method == "POST":
        a = request.form.get("action")
        if a == "add" and request.form.get("name", "").strip():
            d.execute("INSERT INTO requirements(name,applies_to,keywords,expires) VALUES(?,?,?,?)", (request.form["name"].strip(), request.form.get("applies_to", "all"),
                      norm(request.form.get("keywords") or request.form["name"].split()[0]), 1 if request.form.get("expires") else 0))
        elif a == "save":
            d.execute("UPDATE requirements SET applies_to=?, expires=?, active=?, keywords=? WHERE id=?", (request.form.get("applies_to", "all"), 1 if request.form.get("expires") else 0,
                      1 if request.form.get("active") else 0, ",".join(norm(k) for k in request.form.get("keywords", "").split(",") if norm(k)), int(request.form["id"])))
        d.commit(); return redirect("/requirements")
    reqs = d.execute("SELECT * FROM requirements ORDER BY id").fetchall()
    return page(T["requirements_page"], tab="admin", reqs=reqs)

@app.route("/api/expiring")
def api_expiring():
    ok = (me() and me()["is_admin"]) or (CRON_KEY and secrets.compare_digest(request.args.get("key", ""), CRON_KEY))
    if not ok: abort(403)
    return jsonify(date=today_pt().isoformat(), window_days=request.args.get("days", EXPIRING_DAYS, type=int), **expiry_report(db(), request.args.get("days", EXPIRING_DAYS, type=int)))

def is_last_admin(d, mid):
    r = d.execute("SELECT is_admin FROM members WHERE id=?", (mid,)).fetchone()
    return bool(r and r["is_admin"]) and d.execute("SELECT COUNT(*) FROM members WHERE is_admin=1").fetchone()[0] <= 1
@app.route("/admins", methods=["GET", "POST"])
@admin_required
def admins():
    if request.method == "GET": return redirect("/members?view=admins")
    d = db()
    if request.method == "POST":
        mid = int(request.form.get("member_id") or 0); act = request.form.get("action")
        m = d.execute("SELECT * FROM members WHERE id=? AND COALESCE(role,'')!='system'", (mid,)).fetchone()
        if not m: abort(404)
        if act == "make_admin": d.execute("UPDATE members SET is_admin=1 WHERE id=?", (mid,))
        elif act == "remove_admin":
            if is_last_admin(d, mid): flash("Can't remove the last admin."); return redirect("/admins")
            if m["email"] in ADMIN_EMAILS: flash(f"{display_first(m)} is set as admin by the ADMIN_EMAIL setting; change it there."); return redirect("/admins")
            d.execute("UPDATE members SET is_admin=0 WHERE id=?", (mid,))
        elif act == "make_coach": d.execute("UPDATE members SET role='coach' WHERE id=?", (mid,))
        elif act == "remove_coach": d.execute("UPDATE members SET role='athlete' WHERE id=?", (mid,))
        elif act == "add_coaching": add_coaching(d, mid, "manual")
        elif act == "remove_coaching":
            d.execute("DELETE FROM coaching_list WHERE member_id=?", (mid,))
        elif act == "add_referee": add_referee(d, mid)
        elif act == "remove_referee": d.execute("DELETE FROM referee_list WHERE member_id=?", (mid,))
        else: abort(400)
        d.commit()
        if act in ("add_coaching", "remove_coaching", "add_referee", "remove_referee", "make_coach", "remove_coach", "make_admin", "remove_admin"): sync_practice_sheets(d)
        flash(f"Updated {display_first(m)} {m['last']}."); return redirect("/members?view=admins")

def _stamp_day(raw, utc=False):
    """Calendar day in Pacific. SQLite created values are UTC; verified_at is already Pacific."""
    if not raw: return None
    if not utc:
        try: return dt.date.fromisoformat(str(raw)[:10])
        except ValueError: return None
    iso = utc_to_pt(raw)
    if not iso: return None
    try: return dt.date.fromisoformat(iso[:10])
    except ValueError: return None
def _growth_kind(span):
    """Daily under about 3 weeks, weekly under about 4 months, monthly under about 2 years."""
    if span < 21: return "day"
    if span < 122: return "week"
    if span < 730: return "month"
    return "quarter"
def _period_end(day, kind, today):
    """Last calendar day of the day, week, month, or quarter that contains day."""
    if kind == "day": end = day
    elif kind == "week": end = day + dt.timedelta(days=(6 - day.weekday()))
    elif kind == "month":
        nxt = dt.date(day.year + 1, 1, 1) if day.month == 12 else dt.date(day.year, day.month + 1, 1)
        end = nxt - dt.timedelta(days=1)
    else:
        q_end = ((day.month - 1) // 3 + 1) * 3
        nxt = dt.date(day.year + 1, 1, 1) if q_end == 12 else dt.date(day.year, q_end + 1, 1)
        end = nxt - dt.timedelta(days=1)
    return min(end, today)
def _bucket_ends(start, today, kind):
    """Last day of each bucket from start through today, always including both ends."""
    ends = [start]
    if kind == "day":
        d = start + dt.timedelta(days=1)
        while d <= today:
            ends.append(d)
            d += dt.timedelta(days=1)
        return ends
    cursor = start
    while True:
        end = _period_end(cursor, kind, today)
        if end > ends[-1]: ends.append(end)
        if end >= today: return ends
        cursor = end + dt.timedelta(days=1)
def _growth_when(kind, start, today):
    if start >= today: return "today"
    if kind == "week" and (today - start).days < 7: return "this week"
    if kind == "month" and start.year == today.year and start.month == today.month: return "this month"
    if kind == "quarter" and start.year == today.year and (start.month - 1) // 3 == (today.month - 1) // 3: return "this quarter"
    if kind in ("day", "week"): return "since %s %d" % (start.strftime("%b"), start.day)
    return "since %s %d" % (start.strftime("%b"), start.year)
def growth_chart(joined, verified, today=None):
    """Cumulative membership from real signup days. Straight segments only, no invented points."""
    today = today or today_pt()
    joined = sorted(d for d in joined if d and d <= today)
    verified = sorted(d for d in verified if d and d <= today)
    if not joined:
        return {"html": Markup('<div class="card growthcard" id=growthCard data-kind=""><div class=growthhead>0 members</div><p class="t3 sm" style="margin:0">No signups yet.</p></div>'),
                "kind": "", "total": 0, "delta": 0}
    start, total = joined[0], len(joined)
    kind = _growth_kind((today - start).days)
    ends = _bucket_ends(start, today, kind)
    before = sum(1 for d in joined if d < start)
    def cum(days, end): return sum(1 for d in days if d <= end)
    points = [(end, cum(joined, end), cum(verified, end)) for end in ends]
    delta = points[-1][1] - before
    noun = "member" if total == 1 else "members"
    head = "%d %s · %+d %s" % (total, noun, delta, _growth_when(kind, start, today))
    W, H, L, R, T, B = 320, 132, 8, 312, 16, 104
    span = max((today - start).days, 0)
    vmax = max(p[1] for p in points) or 1
    def xy(day, value):
        x = (L + R) / 2 if span == 0 else L + (R - L) * ((day - start).days / span)
        y = B - (B - T) * (value / vmax)
        return round(x, 1), round(y, 1)
    total_pts = " ".join("%s,%s" % xy(day, n) for day, n, _v in points)
    ver_pts = " ".join("%s,%s" % xy(day, v) for day, _n, v in points)
    labels = []
    show = [points[0][0], points[-1][0]]
    if len(points) >= 3:
        show.insert(1, points[len(points) // 2][0])
    seen_x = []
    for day in show:
        x, _y = xy(day, 0)
        if any(abs(x - prev) < 46 for prev in seen_x): continue
        seen_x.append(x)
        text = "%s %d" % (day.strftime("%b"), day.day) if kind in ("day", "week") or day.year == today.year else "%s %s" % (day.strftime("%b"), str(day.year)[2:])
        anchor = "start" if x < 40 else ("end" if x > W - 40 else "middle")
        labels.append('<text x="%s" y="124" text-anchor="%s" fill="#BEC9C1" font-size="12">%s</text>' % (x, anchor, escape(text)))
    parts = ['<svg viewBox="0 0 %d %d" role="img" aria-label="%s">' % (W, H, escape(head))]
    for frac in (0, 0.5, 1):
        y = round(B - (B - T) * frac, 1)
        parts.append('<line x1="%d" y1="%s" x2="%d" y2="%s" stroke="#1B221E" stroke-width="1"/>' % (L, y, R, y))
    if any(v for _d, _n, v in points):
        if len(points) == 1:
            x, y = xy(points[0][0], points[0][2])
            parts.append('<circle cx="%s" cy="%s" r="2.5" fill="#BEC9C1"/>' % (x, y))
        else:
            parts.append('<polyline points="%s" fill="none" stroke="#BEC9C1" stroke-width="1.5" stroke-linejoin="round" stroke-linecap="round"/>' % ver_pts)
    if len(points) == 1:
        x, y = xy(points[0][0], points[0][1])
        parts.append('<circle cx="%s" cy="%s" r="3.5" fill="#F2F6F1"/>' % (x, y))
    else:
        parts.append('<polyline points="%s" fill="none" stroke="#F2F6F1" stroke-width="2" stroke-linejoin="round" stroke-linecap="round"/>' % total_pts)
    parts.append('<line id=growthMark x1="0" y1="%d" x2="0" y2="%d" stroke="#F2F6F1" stroke-width="1" opacity="0" pointer-events="none"/>' % (T, B))
    parts.extend(labels)
    parts.append("</svg>")
    payload = [{"x": xy(day, n)[0], "label": "%s %d" % (day.strftime("%b"), day.day), "total": n, "verified": v} for day, n, v in points]
    script = """<script>(function(){
var card=document.getElementById('growthCard'); if(!card||card.dataset.bound) return; card.dataset.bound='1';
var svg=card.querySelector('svg'), tip=card.querySelector('.growthtip'), mark=card.querySelector('#growthMark');
var pts=[]; try{pts=JSON.parse(card.getAttribute('data-pts')||'[]')}catch(e){}
if(!svg||!tip||!pts.length) return;
var drag=false, timer=0;
function show(clientX){
 var box=svg.getBoundingClientRect(), x=(clientX-box.left)/box.width*320, best=pts[0], dist=1e9, i;
 for(i=0;i<pts.length;i++){var d=Math.abs(pts[i].x-x); if(d<dist){dist=d; best=pts[i]}}
 tip.hidden=false; tip.textContent=best.label+' · '+best.total+' member'+(best.total==1?'':'s')+(best.verified?' · '+best.verified+' verified':'');
 var left=(best.x/320)*box.width, half=tip.offsetWidth/2;
 tip.style.left=Math.max(half+8, Math.min(card.clientWidth-half-8, left))+'px';
 if(mark){mark.setAttribute('x1', best.x); mark.setAttribute('x2', best.x); mark.setAttribute('opacity','0.45')}
}
svg.addEventListener('pointerdown', function(e){drag=true; try{svg.setPointerCapture(e.pointerId)}catch(err){} clearTimeout(timer); show(e.clientX)});
svg.addEventListener('pointermove', function(e){if(drag) show(e.clientX)});
function end(){drag=false; clearTimeout(timer); timer=setTimeout(function(){tip.hidden=true; if(mark) mark.setAttribute('opacity','0')}, 1400)}
svg.addEventListener('pointerup', end); svg.addEventListener('pointercancel', end);
})();</script>"""
    html = Markup('<div class="card growthcard" id=growthCard data-kind="%s" data-pts="%s"><div class=growthhead>%s</div>%s<div class=growthtip hidden></div></div>%s' % (
        kind, escape(json.dumps(payload)), escape(head), "".join(parts), script))
    return {"html": html, "kind": kind, "total": total, "delta": delta}
@app.route("/members", methods=["GET", "POST"])
@admin_required
def members():
    d = db()
    if request.method == "POST":
        mid = int(request.form.get("member_id") or 0)
        m = d.execute("SELECT * FROM members WHERE id=? AND COALESCE(role,'')!='system'", (mid,)).fetchone()
        if not m: abort(404)
        act = request.form.get("action")
        name = "%s %s" % (display_first(m), m["last"])
        detail = handle_member_detail(d, mid)
        if detail == "halt": return members_back()
        if detail == "ok":
            d.commit()
            if act in ("verify", "req", "background", "preferred", "role", "recheck", "edit"): sync_practice_sheets(d)
            return members_back()
        if act == "make_admin":
            d.execute("UPDATE members SET is_admin=1 WHERE id=?", (mid,))
            d.commit(); sync_practice_sheets(d)
            flash("%s is now an admin." % name, "toast")
        elif act == "remove_admin":
            if is_last_admin(d, mid): flash("The last admin cannot be removed.", "toast")
            elif m["email"] in ADMIN_EMAILS: flash("%s is set as admin by ADMIN_EMAIL." % display_first(m), "toast")
            else:
                d.execute("UPDATE members SET is_admin=0 WHERE id=?", (mid,))
                d.commit(); sync_practice_sheets(d)
                flash("%s is no longer an admin." % name, "toast")
        elif act == "make_coach":
            if (m["role"] or "") != "coach":
                d.execute("UPDATE members SET role='coach' WHERE id=?", (mid,))
                d.commit(); sync_practice_sheets(d)
            flash("%s is now an active coach." % name, "toast")
        elif act == "remove_coach":
            if (m["role"] or "") == "coach":
                d.execute("UPDATE members SET role='athlete' WHERE id=?", (mid,))
                d.commit(); sync_practice_sheets(d)
            flash("%s is no longer an active coach." % name, "toast")
        elif act == "add_coaching":
            add_coaching(d, mid, "manual")
            d.commit(); sync_practice_sheets(d)
            flash("%s was added to coaches." % name, "toast")
        elif act == "remove_coaching":
            d.execute("DELETE FROM coaching_list WHERE member_id=?", (mid,))
            d.commit(); sync_practice_sheets(d)
            flash("%s was removed from coaches." % name, "toast")
        elif act == "add_referee":
            add_referee(d, mid)
            d.commit(); sync_practice_sheets(d)
            flash("%s was added to referees." % name, "toast")
        elif act == "remove_referee":
            d.execute("DELETE FROM referee_list WHERE member_id=?", (mid,))
            d.commit(); sync_practice_sheets(d)
            flash("%s was removed from referees." % name, "toast")
        else: abort(400)
        return members_back()
    days = practice_days(d)
    focus = default_checkin_date(days)
    pr = d.execute("SELECT id FROM practices WHERE date=? AND cancelled=0 ORDER BY start LIMIT 1", (focus,)).fetchone()
    rows = d.execute("""SELECT m.*, (SELECT COUNT(*) FROM checkins WHERE member_id=m.id) AS visits,
      (SELECT MAX(practice_date) FROM checkins WHERE member_id=m.id) AS lastp,
      (SELECT status FROM verify_requests WHERE member_id=m.id ORDER BY id DESC LIMIT 1) AS vr_status,
      (SELECT note FROM verify_requests WHERE member_id=m.id ORDER BY id DESC LIMIT 1) AS vr_note,
      (SELECT going FROM rsvps WHERE member_id=m.id AND practice_id=?) AS going
      FROM members m WHERE COALESCE(role,'')!='system' ORDER BY last, first""", (pr["id"] if pr else -1,)).fetchall()
    q = (request.args.get("q") or "").strip()
    view = request.args.get("view") or "members"
    if request.args.get("coach") == "eligible": view = "coaches"
    if request.args.get("referee") == "eligible": view = "referees"
    if view not in ("members", "coaches", "admins", "referees", "expiring", "uncleared"): view = "members"
    if q:
        needle = q.casefold()
        rows = [r for r in rows if needle in " ".join(x for x in (r["first"], r["preferred_first"], r["last"], r["email"]) if x).casefold()]
    if view == "expiring":
        rep = expiry_report(d)
        ids = {item["id"] for bucket in rep.values() for item in bucket}
        rows = [r for r in rows if r["id"] in ids]
    elif view == "uncleared":
        rows = [r for r in rows if not clearance(d, r)["ok"]]
    elif view == "admins":
        rows = [r for r in rows if r["is_admin"]]
    c = {s: sum(1 for r in rows if r["usawp_status"] == s) for s in ("verified", "pending", "expired", "unknown")}
    coach_ids = {r["id"] for r in rows if coach_eligibility(d, r)["eligible"]}
    ref_ids = {r["id"] for r in rows if referee_eligibility(d, r)["eligible"]}
    listed = {r[0] for r in d.execute("SELECT member_id FROM coaching_list")}
    referees = {r[0] for r in d.execute("SELECT member_id FROM referee_list")}
    joined, verified = [], []
    for r in d.execute("SELECT created, usawp_verified_at FROM members WHERE COALESCE(role,'')!='system'"):
        day = _stamp_day(r["created"], utc=True)
        if day: joined.append(day)
        vday = _stamp_day(r["usawp_verified_at"], utc=False)
        if vday: verified.append(vday)
    return page(T["members"],
        tab="admin", rows=rows, c=c, view=view, date=focus, q=q,
        listed=listed, referees=referees, coach_ids=coach_ids, ref_ids=ref_ids,
        n_admins=sum(1 for r in rows if r["is_admin"]), boot=ADMIN_EMAILS, growth=growth_chart(joined, verified)["html"])
def csv_attachment(filename, header, rows):
    """UTF-8 with a BOM so Excel opens names and punctuation correctly."""
    buf = io.StringIO(); buf.write("\ufeff"); w = csv.writer(buf); w.writerow(header)
    for row in rows: w.writerow(["" if v is None else v for v in row])
    return Response(buf.getvalue().encode("utf-8"), mimetype="text/csv; charset=utf-8",
                    headers={"Content-Disposition": 'attachment; filename="%s"' % filename})
def utc_to_pt(raw, with_time=False):
    """SQLite CURRENT_TIMESTAMP is UTC. Return the Pacific date, or date and time."""
    if not raw: return ""
    s = str(raw).strip().replace(" ", "T")
    if len(s) <= 10: return s[:10]
    try: naive = dt.datetime.fromisoformat(s[:19])
    except ValueError: return s[:10]
    pt = naive.replace(tzinfo=dt.timezone.utc).astimezone(PT)
    if not with_time: return pt.date().isoformat()
    return "%04d-%02d-%02d %02d:%02d" % (pt.year, pt.month, pt.day, pt.hour, pt.minute)
def export_status(d, member, pending_ids):
    """Same words as the member card: pending, then trial, then cleared, otherwise not cleared."""
    if member["id"] in pending_ids: return "pending"
    tw = trial_window(member); cl = clearance(d, member)
    if cl["ok"] and tw and tw["active"] and (member["usawp_status"] or "") != "verified": return "trial"
    if cl["ok"]: return "cleared"
    return "not cleared"
def trial_dates(member):
    raw = member["trial_acknowledged_at"] if member and "trial_acknowledged_at" in member.keys() else None
    if not raw: return "", ""
    try: start = dt.date.fromisoformat(str(raw)[:10])
    except ValueError: return "", ""
    return start.isoformat(), (start + dt.timedelta(days=TRIAL_DAYS)).isoformat()
def requirement_expiries(d):
    """Latest SafeSport and background dates on file, keyed by member id."""
    out = {}
    for mid, name, keywords, exp in d.execute("SELECT x.member_id, q.name, q.keywords, x.expires_on FROM member_reqs x JOIN requirements q ON q.id=x.req_id"):
        if not exp: continue
        blob = ((name or "") + " " + (keywords or "")).lower()
        for key in ("safesport", "background"):
            if key in blob:
                prev = out.get((mid, key))
                if not prev or str(exp) > prev: out[(mid, key)] = str(exp)[:10]
    return out
MEMBERS_CSV_HEADER = ["Legal first", "Legal last", "Preferred first", "Email", "Phone", "Role", "Admin", "USAWP #", "Status",
                      "Membership expires", "SafeSport expires", "Background screening expires", "Trial start", "Trial end",
                      "Verified date", "Joined date", "Total attendance", "Coach eligible", "Referee eligible", "Background screening"]
@app.route("/members.csv")
@admin_required
def members_csv():
    rows = member_sheet_rows(db())
    return csv_attachment("grunions-members-%s.csv" % today_pt().isoformat(), rows[0], rows[1:])
def export_default_range():
    today = today_pt(); return today - dt.timedelta(days=28), today + dt.timedelta(days=28)
def export_range():
    """Start and end from the query string. A backwards range is swapped. Missing dates use the default window."""
    if not request.args.get("start") and not request.args.get("end"): return export_default_range()
    start, end = parse_date(request.args.get("start")), parse_date(request.args.get("end"))
    if not start or not end: return None
    if end < start: start, end = end, start
    return start, end
PRACTICE_CSV_HEADER = ["Date", "Time", "Location", "Cancelled", "RSVP going", "Checked in", "Coaches", "Coach count", "Eligible coaches", "Cancel reason"]
ATTENDANCE_CSV_HEADER = ["Date", "Time", "Location", "Cancelled", "Name", "USAWP #", "RSVP", "Checked in", "Check-in time"]
PRACTICE_COACHES_HEADER = ["Date", "Time", "Location", "Coach name", "Coach email", "Coach eligible"]
SHEET_PRACTICES = "Practices"
SHEET_PRACTICE_COACHES = "Practice Coaches"
SHEET_MEMBERS = "Members"
SHEET_ATTENDANCE = "Attendance"
SHEET_SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
SHEET_DEBOUNCE_SEC = 2.0
def practice_time(p):
    return "%s-%s" % (p["start"] or "", p["end"] or "")
def practice_export_bundle(d, practices):
    """RSVPs, check-ins, and assigned coaches for these practices. Coaches off the coaching list are left out."""
    ids = [p["id"] for p in practices]
    rsvps = {}
    if ids:
        marks = ",".join("?" * len(ids))
        for pid, mid, going in d.execute("SELECT practice_id, member_id, going FROM rsvps WHERE practice_id IN (%s)" % marks, ids):
            rsvps[(pid, mid)] = going
    dates = sorted({p["date"] for p in practices})
    checkins = {}
    if dates:
        qmarks = ",".join("?" * len(dates))
        for mid, day, at in d.execute("SELECT member_id, practice_date, at FROM checkins WHERE practice_date IN (%s)" % qmarks, dates):
            checkins[(mid, day)] = at
    return rsvps, checkins, practice_coach_rows(d, ids)
def practice_summary_row(d, p, rsvps, checkins, coaches):
    going_n = sum(1 for (pid, _), g in rsvps.items() if pid == p["id"] and g == 1)
    checked_n = sum(1 for (_, day) in checkins if day == p["date"])
    names = coach_labels(coaches)
    eligible_n = sum(1 for c in coaches if coach_eligibility(d, c)["eligible"])
    reason = (p["cancel_reason"] or "") if p["cancelled"] else ""
    return [p["date"], practice_time(p), p["location"] or "", "yes" if p["cancelled"] else "no", going_n, checked_n, ", ".join(names), len(names), eligible_n, reason]
def practice_coach_name(c):
    return ("%s %s" % (display_first(c), c["last"] or "")).strip()
def practice_coach_detail_rows(d, practices, assigned):
    rows = []
    for p in practices:
        coaches = sorted(assigned.get(p["id"], []), key=lambda r: (display_first(r).casefold(), (r["last"] or "").casefold(), r["id"]))
        for c in coaches:
            rows.append([p["date"], practice_time(p), p["location"] or "", practice_coach_name(c), c["email"] or "", coach_eligibility(d, c)["text"]])
    return rows
def attendance_rows(d, practices):
    """One row per member per practice: RSVP and check-in. Header is not included."""
    rsvps, checkins, _assigned = practice_export_bundle(d, practices)
    members = d.execute("SELECT * FROM members WHERE COALESCE(role,'')!='system' ORDER BY last, first, id").fetchall()
    rows = []
    for p in practices:
        when = practice_time(p); cancelled = "yes" if p["cancelled"] else "no"
        for m in members:
            going = rsvps.get((p["id"], m["id"]))
            rsvp = "going" if going == 1 else ("not going" if going == 0 else "")
            at = checkins.get((m["id"], p["date"]))
            rows.append([p["date"], when, p["location"] or "", cancelled, "%s %s" % (display_first(m), m["last"]),
                         m["usawp_number"] or "", rsvp, "yes" if (m["id"], p["date"]) in checkins else "no",
                         utc_to_pt(at, with_time=True) if at else ""])
    return rows
def member_sheet_rows(d):
    """Same columns as the members CSV, including the background screening line."""
    pending = {r[0] for r in d.execute("SELECT DISTINCT member_id FROM verify_requests WHERE status='pending'")}
    expiries = requirement_expiries(d)
    rows = [MEMBERS_CSV_HEADER]
    for m in d.execute("""SELECT m.*, (SELECT COUNT(*) FROM checkins WHERE member_id=m.id) AS visits FROM members m
            WHERE COALESCE(role,'')!='system' ORDER BY last, first, id"""):
        trial_start, trial_end = trial_dates(m)
        verified = str(m["usawp_verified_at"] or "")[:10]
        rows.append([m["first"], m["last"], m["preferred_first"] or "", m["email"], (m["phone"] or "").strip(),
                     role_label(m), "yes" if m["is_admin"] else "no", m["usawp_number"] or "", export_status(d, m, pending),
                     m["usawp_valid_until"] or "", expiries.get((m["id"], "safesport"), ""), expiries.get((m["id"], "background"), ""),
                     trial_start, trial_end, verified, utc_to_pt(m["created"]), m["visits"], coach_eligibility(d, m)["text"],
                     referee_eligibility(d, m)["text"], (background_view(d, m) or {}).get("text", "")])
    return rows
def practice_sheet_tabs(d, practices=None):
    """Members, Practices, Attendance, and Practice Coaches."""
    if practices is None:
        practices = d.execute("SELECT * FROM practices ORDER BY date, start, id").fetchall()
    rsvps, checkins, assigned = practice_export_bundle(d, practices)
    summary = [PRACTICE_CSV_HEADER]
    for p in practices: summary.append(practice_summary_row(d, p, rsvps, checkins, assigned.get(p["id"], [])))
    detail = [PRACTICE_COACHES_HEADER] + practice_coach_detail_rows(d, practices, assigned)
    return {SHEET_MEMBERS: member_sheet_rows(d), SHEET_PRACTICES: summary,
            SHEET_ATTENDANCE: [ATTENDANCE_CSV_HEADER] + attendance_rows(d, practices),
            SHEET_PRACTICE_COACHES: detail}
def sheet_id():
    return (os.environ.get("GOOGLE_SHEET_ID") or "").strip()
def service_account_info():
    """GOOGLE_SA_JSON is the full service-account JSON. Missing or unreadable JSON disables the sheet."""
    raw = (os.environ.get("GOOGLE_SA_JSON") or "").strip()
    if not raw.startswith("{"): return None
    try: info = json.loads(raw)
    except ValueError:
        app.logger.warning("GOOGLE_SA_JSON is not valid JSON")
        return None
    if not info.get("client_email") or not info.get("private_key"): return None
    return info
def sheet_configured():
    return bool(sheet_id() and service_account_info())
def open_spreadsheet():
    info = service_account_info()
    creds = Credentials.from_service_account_info(info, scopes=SHEET_SCOPES)
    return gspread.authorize(creds).open_by_key(sheet_id())
def push_sheet_tabs(tabs):
    """Replace Members, Practices, Attendance, and Practice Coaches. False when the sheet is not configured."""
    if not sheet_configured() or not tabs: return False
    sh = open_spreadsheet()
    for title, rows in tabs.items():
        try: ws = sh.worksheet(title)
        except gspread.WorksheetNotFound:
            cols = max((len(r) for r in rows), default=1)
            ws = sh.add_worksheet(title=title, rows=max(len(rows), 1), cols=max(cols, 1))
        ws.clear()
        if rows: ws.update(rows, range_name="A1", value_input_option="RAW")
    return True
def _sheet_conn():
    """Use the request connection when a page is saving. A background sync opens its own."""
    try:
        if "db" in g: return g.db, False
    except RuntimeError:
        pass
    d = sqlite3.connect(DB, timeout=5); d.row_factory = sqlite3.Row
    return d, True
def save_sheet_status(ok, detail):
    d, owned = _sheet_conn()
    try:
        d.execute("""INSERT INTO sheet_sync(id, at, ok, detail) VALUES(1,?,?,?)
            ON CONFLICT(id) DO UPDATE SET at=excluded.at, ok=excluded.ok, detail=excluded.detail""",
            (stamp_pt("minutes"), 1 if ok else 0, (detail or "")[:300]))
        d.commit()
    finally:
        if owned: d.close()
def sheet_status():
    """Last sync for the admin page. None when the sheet is not configured."""
    if not sheet_configured(): return None
    d = db()
    row = d.execute("SELECT at, ok, detail FROM sheet_sync WHERE id=1").fetchone()
    if not row: return {"at": "", "ok": None, "label": "Not synced yet", "detail": ""}
    return {"at": row["at"] or "", "ok": row["ok"], "label": "Synced" if row["ok"] else "Failed", "detail": row["detail"] or ""}
def run_sheet_sync():
    """Full rewrite of the sheet. Logs errors and never raises."""
    try:
        d, owned = _sheet_conn()
        try: tabs = practice_sheet_tabs(d)
        finally:
            if owned: d.close()
        ok = push_sheet_tabs(tabs)
        if ok: save_sheet_status(True, "Synced")
        elif sheet_configured(): save_sheet_status(False, "Google Sheet did not update")
    except Exception as e:
        app.logger.exception("Google Sheet sync failed")
        try: save_sheet_status(False, str(e).split("\n")[0][:160])
        except Exception: app.logger.exception("could not store Google Sheet status")
_sheet_lock = threading.Lock()
_sheet_timer = None
def schedule_sheet_sync():
    """Debounce a full sync onto a background thread. Inline mode runs it before returning."""
    global _sheet_timer
    try:
        if os.environ.get("GRUNIONS_SHEET_SYNC") == "inline":
            run_sheet_sync(); return
        if not sheet_configured(): return
        with _sheet_lock:
            if _sheet_timer is not None: _sheet_timer.cancel()
            _sheet_timer = threading.Timer(SHEET_DEBOUNCE_SEC, run_sheet_sync)
            _sheet_timer.daemon = True
            _sheet_timer.start()
    except Exception:
        app.logger.exception("could not schedule Google Sheet sync")
def sync_practice_sheets(d=None):
    """Queue a sheet rewrite. A failure is logged and does not affect the request."""
    schedule_sheet_sync()
def run_daily_sheet_sync():
    if not sheet_configured(): return
    d = open_db()
    try:
        if not claim_job(d, "sheet_daily", 20 * 3600): return
    except Exception:
        app.logger.exception("Google Sheet daily lock failed")
        return
    finally:
        d.close()
    run_sheet_sync()
def render_transfer(stats=None):
    start, end = export_default_range()
    return page(T["transfer"], tab="admin", start=start.isoformat(), end=end.isoformat(), sheet_on=sheet_configured(), sheet_status=sheet_status(), stats=stats)
def take_import():
    """Read an uploaded Sport:80 file. None when nothing was saved."""
    f = request.files.get("file")
    if not f or not f.filename:
        flash("Choose a file.")
        return None
    stats = import_roster(f.filename, f.read())
    if stats is None: flash("Couldn't find name/email and status columns in that file.")
    return stats
@app.route("/transfer", methods=["GET", "POST"])
@admin_required
def transfer_page():
    stats = take_import() if request.method == "POST" else None
    return render_transfer(stats)
@app.route("/export")
@admin_required
def export_page():
    return redirect("/transfer")
@app.route("/export/sheet", methods=["POST"])
@admin_required
def export_sheet_now():
    if not sheet_configured(): abort(404)
    run_sheet_sync()
    st = sheet_status()
    if st and st.get("ok"): flash("Google Sheet synced.", "toast")
    else: flash("Google Sheet sync failed. The error was logged.", "toast")
    return redirect("/transfer")
@app.route("/export/practices.csv")
@admin_required
def practices_csv():
    bounds = export_range()
    if not bounds:
        flash("Choose a start and end date."); return redirect("/transfer")
    start, end = bounds
    d = db()
    practices = d.execute("SELECT * FROM practices WHERE date>=? AND date<=? ORDER BY date, start, id", (start.isoformat(), end.isoformat())).fetchall()
    rsvps, checkins, assigned = practice_export_bundle(d, practices)
    span = "%s-to-%s" % (start.isoformat(), end.isoformat())
    if request.args.get("detail") in ("1", "true", "yes"):
        return csv_attachment("grunions-attendance-%s.csv" % span, ATTENDANCE_CSV_HEADER, attendance_rows(d, practices))
    rows = [practice_summary_row(d, p, rsvps, checkins, assigned.get(p["id"], [])) for p in practices]
    return csv_attachment("grunions-practices-%s.csv" % span, PRACTICE_CSV_HEADER, rows)

# ---- USAWP (Sport:80 Smart List export) import ----
ALIASES = {  # normalized header -> field. Sport:80 Smart List columns vary by chosen columns, so match loosely.
    "preferred": ["preferredfirstname", "preferredname", "nickname", "knownas"],
    "first": ["firstname", "forename", "givenname", "legalfirstname"],
    "last": ["lastname", "surname", "familyname", "legallastname"],
    "name": ["name", "fullname", "membername", "profilename"],
    "email": ["email", "emailaddress", "primaryemail", "profileemail"],
    "status": ["status", "membershipstatus", "individualmembershipstatus", "addonstatus"],
    "number": ["idnumber", "usawpnumber", "membernumber", "membershipnumber", "membershipid", "memberid", "usawpid", "individualmembershipmembernumber"],
    "contact": ["contactid", "sportcontactid", "profileid"],
    "valid": ["validuntil", "membershipexpirydate", "membershipexpirationdate", "membershipvaliduntil", "expiry", "validthrough", "expirydate", "expirationdate", "expires", "enddate", "individualmembershipvaliduntil", "individualmembershipexpirydate"],
    "mtype": ["membertype", "membershiptype", "individualmembershiptype", "membershiptypename"],
}
EXCLUDE_KW = [k for r in DEFAULT_REQS for k in r[2].split(",")]
def map_headers(headers):
    m = {}
    for i, h in enumerate(headers):
        n = norm(h)
        if any(k in n for k in EXCLUDE_KW): continue  # e.g. "Background Screening Expiration Date" is not membership expiry
        for field, al in ALIASES.items():
            if field == "first" and "preferred" in n: continue  # "Preferred First Name" is not the legal first name
            if field not in m and (n in al or any(n.endswith(a) for a in al if len(a) > 5)): m[field] = i
    return m
def parse_date(v):
    if isinstance(v, (dt.date, dt.datetime)): return v.date() if isinstance(v, dt.datetime) else v
    v = (str(v or "")).strip()[:10]
    for f in ("%Y-%m-%d", "%m/%d/%Y", "%d/%m/%Y", "%m/%d/%y"):
        try: return dt.datetime.strptime(v, f).date()
        except ValueError: pass
def classify(raw, valid):
    s = norm(raw)
    if valid and valid < today_pt(): return "expired"
    if s in ("current", "active", "valid", "approved", "paid"): return "verified"
    if s in ("expired", "lapsed", "cancelled", "canceled", "inactive", "suspended", "revoked"): return "expired"
    if s in ("pendingapproval", "actionrequired", "pending"): return "pending"
    return "unknown"
def read_rows(fname, data):
    if fname.lower().endswith((".xlsx", ".xlsm")):
        import openpyxl
        ws = openpyxl.load_workbook(io.BytesIO(data), read_only=True, data_only=True).active
        rows = [list(r) for r in ws.iter_rows(values_only=True)]
    else:
        rows = list(csv.reader(io.StringIO(data.decode("utf-8-sig", errors="replace"))))
    # header row = first row containing a name-ish column (skips title rows in exports)
    for i, r in enumerate(rows[:10]):
        hm = map_headers([str(c or "") for c in r])
        if ("email" in hm or "name" in hm or "last" in hm) and ("status" in hm or "number" in hm or "valid" in hm): return hm, rows[i + 1:], [str(c or "") for c in r]
    return None, rows, []
def import_roster(fname, data):
    hm, rows, hdr = read_rows(fname, data)
    if not hm: return None
    d = db()
    global EXCLUDE_KW; EXCLUDE_KW = req_keywords(d)
    reqcols = {}  # req_id -> {"exp": col, "done": col, "status": col}
    for q in d.execute("SELECT * FROM requirements WHERE active=1"):
        for i, h in enumerate(hdr):
            n = norm(h)
            if not any(k and k in n for k in (q["keywords"] or "").split(",")): continue
            kind = "exp" if any(x in n for x in ("expir", "validthrough", "validuntil", "validto", "enddate")) else "done" if any(x in n for x in ("complet", "date", "signed")) else "status" if "status" in n else None
            if kind: reqcols.setdefault(q["id"], {}).setdefault(kind, i)
    now = stamp_pt("minutes")
    members = d.execute("SELECT id, first, last, email FROM members").fetchall()
    by_email = {m["email"]: m["id"] for m in members}
    by_name = {}
    for m in members: by_name.setdefault(norm(m["first"]) + "|" + norm(m["last"]), []).append(m["id"])
    stats = {"rows": 0, "matched": 0, "unmatched": []}; best = {}
    cell = lambda r, k: (r[hm[k]] if k in hm and hm[k] < len(r) else None)
    for r in rows:
        if not any(r): continue
        stats["rows"] += 1
        first, last = str(cell(r, "first") or "").strip(), str(cell(r, "last") or "").strip()
        if not (first and last) and cell(r, "name"):
            parts = str(cell(r, "name")).strip().split()
            first, last = parts[0], parts[-1] if len(parts) > 1 else ""
        email = str(cell(r, "email") or "").strip().lower()
        raw = str(cell(r, "status") or "").strip(); valid = parse_date(cell(r, "valid"))
        mtype = str(cell(r, "mtype") or "").strip() if "mtype" in hm else ""
        mid = by_email.get(email) if email else None
        if not mid:
            ids = by_name.get(norm(first) + "|" + norm(last), [])
            mid = ids[0] if len(ids) == 1 else None
        if not mid: stats["unmatched"].append(f"{first} {last} <{email}> {raw}"); continue
        for rid, cols in reqcols.items():
            g_ = lambda k: r[cols[k]] if k in cols and cols[k] < len(r) else None
            exp, done, sraw = parse_date(g_("exp")), parse_date(g_("done")), norm(str(g_("status") or ""))
            if not done and sraw in ("current", "complete", "completed", "valid", "passed", "approved", "yes", "signed"): done = today_pt()
            if exp or done:
                d.execute("""INSERT INTO member_reqs VALUES(?,?,?,?,'Sport:80 import','import',?) ON CONFLICT(member_id,req_id) DO UPDATE SET
                  completed_on=COALESCE(excluded.completed_on,completed_on), expires_on=COALESCE(excluded.expires_on,expires_on), source=excluded.source, at=excluded.at""",
                  (mid, rid, done.isoformat() if done else None, exp.isoformat() if exp else None, now))
                stats["req_updates"] = stats.get("req_updates", 0) + 1
        if cell(r, "contact"): d.execute("UPDATE members SET sport80_contact_id=? WHERE id=?", (str(cell(r, "contact")).strip(), mid))
        if "preferred" in hm and clean_preferred(cell(r, "preferred")): d.execute("UPDATE members SET preferred_first=? WHERE id=?", (clean_preferred(cell(r, "preferred")), mid))
        st = classify(raw, valid)
        if st == "unknown" and not raw and valid and valid >= today_pt(): st = "verified"  # no status column: future expiry = current
        rank = {"verified": 3, "pending": 2, "expired": 1, "unknown": 0}[st]
        if mid not in best or rank > best[mid][0]:  # keep best status if someone appears twice
            best[mid] = (rank, st, raw, str(cell(r, "number") or ""), valid.isoformat() if valid else None, mtype)
    for mid, (_, st, raw, num, valid, mtype) in best.items():
        d.execute("UPDATE members SET usawp_status=?,usawp_raw=?,usawp_number=?,usawp_valid_until=COALESCE(?,usawp_valid_until),usawp_updated=? WHERE id=?", (st, raw, num, valid, now, mid))
        if st == "verified": d.execute("UPDATE members SET usawp_verified_by='Sport:80 import', usawp_verified_at=? WHERE id=?", (now, mid))
        if mtype: apply_membership_type(d, mid, mtype, True)
    expire_sweep(d)
    d.commit(); stats["matched"] = len(best)
    sync_practice_sheets(d)
    return stats

@app.route("/import", methods=["GET", "POST"])
@admin_required
def import_page():
    if request.method == "POST": return render_transfer(take_import())
    return redirect("/transfer")

# ---------- notifications (web push + email) ----------
import base64, threading
NOTIFY_PUSH = (
    ("team_chat", "Team chat messages", "all"),
    ("coaches_chat", "Coaches chat", "staff"),
    ("practice_reminder", "Practice reminder (~3 hours before)", "all"),
    ("verification_result", "Verification result", "all"),
    ("practice_cancelled", "Practice cancelled", "all"),
    ("expiry", "Trial, membership, SafeSport, and background screening expiring or expired", "all"),
    ("verify_request", "New verification requests", "admin"),
)
VAPID = None
VAPID_PUBLIC = ""
VAPID_PATH = os.path.join(DATA_DIR, "vapid_private.pem")
_vapid_lock = threading.Lock()
_scheduler = None

def public_b64(v):
    from cryptography.hazmat.primitives import serialization
    raw = v.public_key.public_bytes(serialization.Encoding.X962, serialization.PublicFormat.UncompressedPoint)
    return base64.urlsafe_b64encode(raw).decode().rstrip("=")
def vapid_from_private(raw):
    from py_vapid import Vapid
    s = (raw or "").strip()
    if "\\n" in s: s = s.replace("\\n", "\n")
    if "BEGIN" in s: return Vapid.from_pem(s.encode())
    return Vapid.from_string(s)
def ensure_vapid():
    """Use VAPID_PUBLIC_KEY / VAPID_PRIVATE_KEY when set. Otherwise generate once and keep the key under DATA_DIR."""
    global VAPID, VAPID_PUBLIC
    if VAPID is not None: return
    with _vapid_lock:
        if VAPID is not None: return
        from py_vapid import Vapid
        env = os.environ.get("VAPID_PRIVATE_KEY")
        if env: v = vapid_from_private(env)
        elif os.path.isfile(VAPID_PATH): v = Vapid.from_file(VAPID_PATH)
        else:
            v = Vapid(); v.generate_keys()
        os.makedirs(DATA_DIR, exist_ok=True)
        v.save_key(VAPID_PATH)
        try: os.chmod(VAPID_PATH, 0o600)
        except OSError: pass
        pub = public_b64(v)
        open(os.path.join(DATA_DIR, "vapid_public.txt"), "w").write(pub)
        given = (os.environ.get("VAPID_PUBLIC_KEY") or "").strip().rstrip("=")
        if given and given != pub: app.logger.warning("VAPID_PUBLIC_KEY does not match the private key; using the public key derived from the private key")
        VAPID, VAPID_PUBLIC = v, pub
def vapid_public_key():
    ensure_vapid(); return VAPID_PUBLIC
def vapid_subject():
    src = "%s %s" % (SMTP.get("MAIL_FROM") or "", ADMIN_EMAIL or "")
    m = re.search(r"[\w.+-]+@[\w.-]+", src)
    return "mailto:" + (m.group(0) if m else "grunions@localhost")
app.jinja_env.globals.update(vapid_public_key=vapid_public_key)
def notify_prefs(m):
    raw = None
    try:
        if m and "notify_prefs" in m.keys() and m["notify_prefs"]: raw = json.loads(m["notify_prefs"])
    except (TypeError, ValueError, AttributeError): raw = None
    return raw if isinstance(raw, dict) else {}
def wants_push(m, kind):
    prefs = notify_prefs(m)
    return True if kind not in prefs else bool(prefs[kind])
def wants_email_reminders(m):
    try:
        if m and "email_reminders" in m.keys() and m["email_reminders"] is not None: return int(m["email_reminders"]) != 0
    except (TypeError, ValueError, AttributeError): pass
    return True
def notify_types_for(m):
    out = []
    staff = is_active_coach(m); admin = bool(m and m["is_admin"])
    for key, label, who in NOTIFY_PUSH:
        if who == "staff" and not staff: continue
        if who == "admin" and not admin: continue
        out.append((key, label))
    return out
def app_base():
    if PUBLIC_URL: return PUBLIC_URL.rstrip("/")
    try:
        if request: return request.host_url.rstrip("/")
    except RuntimeError: pass
    return "http://localhost:%s" % os.environ.get("PORT", "5055")
app.jinja_env.globals.update(app_base=app_base)
def open_db():
    d = sqlite3.connect(DB, timeout=30); d.row_factory = sqlite3.Row
    d.executescript(SCHEMA); migrate_members(d); migrate_messages(d); migrate_practices(d); migrate_lineup(d); migrate_series(d)
    seed_chat_reads(d); d.commit(); return d
def claim_notice(d, member_id, kind):
    cur = d.execute("INSERT OR IGNORE INTO sent_notices(member_id, kind, sent_at) VALUES(?,?,?)", (member_id, kind, dt.datetime.now().isoformat(timespec="seconds")))
    d.commit(); return cur.rowcount == 1
def release_notice(d, member_id, kind):
    d.execute("DELETE FROM sent_notices WHERE member_id=? AND kind=?", (member_id, kind)); d.commit()
def claim_job(d, name, ttl):
    now = dt.datetime.now()
    try: d.execute("BEGIN IMMEDIATE")
    except sqlite3.OperationalError: return False
    row = d.execute("SELECT locked_at FROM job_locks WHERE name=?", (name,)).fetchone()
    if row:
        try: locked = dt.datetime.fromisoformat(row["locked_at"])
        except ValueError: locked = now - dt.timedelta(days=1)
        if (now - locked).total_seconds() < ttl:
            d.rollback(); return False
        d.execute("UPDATE job_locks SET locked_at=? WHERE name=?", (now.isoformat(timespec="seconds"), name))
    else:
        d.execute("INSERT INTO job_locks(name, locked_at) VALUES(?,?)", (name, now.isoformat(timespec="seconds")))
    d.commit(); return True
def send_push(sub, payload):
    ensure_vapid()
    from pywebpush import webpush
    webpush(subscription_info={"endpoint": sub["endpoint"], "keys": {"p256dh": sub["p256dh"], "auth": sub["auth"]}},
            data=json.dumps(payload), vapid_private_key=VAPID, vapid_claims={"sub": vapid_subject()}, ttl=12 * 60 * 60, timeout=10)
def push_member(d, member, kind, title, body, url):
    """Push to every subscription for this member. member is a row or an id. Returns how many landed."""
    if isinstance(member, int):
        member = d.execute("SELECT * FROM members WHERE id=?", (member,)).fetchone()
    if not member or not wants_push(member, kind): return 0
    from pywebpush import WebPushException
    try: badge = compute_unread(d, member)["total"]
    except Exception as e:
        app.logger.warning("unread badge failed: %s", e); badge = 0
    payload = {"title": title, "body": body, "url": url, "badge": badge}
    n = 0
    for s in d.execute("SELECT * FROM push_subscriptions WHERE member_id=?", (member["id"],)):
        try:
            send_push(s, payload); n += 1
        except WebPushException as e:
            if getattr(e, "status_code", None) in (404, 410):
                d.execute("DELETE FROM push_subscriptions WHERE id=?", (s["id"],)); d.commit()
            else: app.logger.warning("push to member %s failed: %s", member["id"], e)
        except Exception as e:
            app.logger.warning("push to member %s failed: %s", member["id"], e)
    return n
def notify_chat(d, channel, sender, body, has_image):
    kind = "coaches_chat" if channel == "coaches" else "team_chat"
    text = (body or "").strip()
    if not text and has_image: text = "Sent a photo"
    if not text: return
    text = text[:140]
    title = "Coaches chat" if channel == "coaches" else "Team chat"
    url = "/chat?c=coaches" if channel == "coaches" else "/chat"
    line = "%s %s.: %s" % (display_first(sender), (sender["last"] or "")[:1], text)
    for m in d.execute("SELECT * FROM members WHERE COALESCE(role,'')!='system' AND id!=?", (sender["id"],)):
        if channel == "coaches" and not is_active_coach(m): continue
        push_member(d, m, kind, title, line, url)
def notify_practice_cancelled(d, p):
    when = "%s, %s-%s" % (fmt_d(p["date"]), fmt_t(p["start"]), fmt_t(p["end"]))
    loc = p["location"] or ""
    reason = " ".join(str(p["cancel_reason"] or "").split())
    url = "/practices/%s" % p["id"]
    subject = "Practice cancelled: %s" % fmt_d(p["date"])
    title = "Practice cancelled"
    body = ("%s at %s" % (when, loc)) if loc else when
    if reason: body = "%s. %s" % (body, reason)
    for m in d.execute("SELECT * FROM members WHERE COALESCE(role,'')!='system'"):
        ek, pk = "email:practice_cancelled:%s" % p["id"], "push:practice_cancelled:%s" % p["id"]
        if m["email"] and claim_notice(d, m["id"], ek):
            if not smtp_ready(): release_notice(d, m["id"], ek)
            else:
                text = "Hi %s,\n\nPractice is cancelled.\n\n%s\n%s\n" % (display_first(m), when, loc)
                if reason: text += "\n%s\n" % reason
                text += "\nGrunions Water Polo\n"
                try: send_email(m["email"], subject, text)
                except Exception as e:
                    app.logger.error("cancel email to %s failed: %s", m["email"], e); release_notice(d, m["id"], ek)
        if wants_push(m, "practice_cancelled") and claim_notice(d, m["id"], pk):
            if not push_member(d, m, "practice_cancelled", title, body, url): release_notice(d, m["id"], pk)
def notify_new_verify_request(d, member):
    who = "%s %s" % (member["first"], member["last"])
    if member["usawp_number"]: who += " #%s" % member["usawp_number"]
    for a in d.execute("SELECT * FROM members WHERE is_admin=1 AND COALESCE(role,'')!='system'"):
        push_member(d, a, "verify_request", "New verification request", who, "/admin")
def notify_verification_result(d, mid, verified, exp):
    if verified:
        body = "Your USAWP membership was verified."
        if exp: body += " Expires %s." % exp.isoformat()
    else:
        body = "Your USAWP membership was not verified."
    push_member(d, mid, "verification_result", "Verification result", body, "/home")
def expiry_when(date_iso, left):
    if left == 0: return "today (%s)" % date_iso
    if left == 1: return "tomorrow (%s)" % date_iso
    return "in %d days (%s)" % (left, date_iso)
def expiry_text(kind, date_iso, left):
    when = expiry_when(date_iso, left)
    if kind == "membership":
        sentence = "Your USA Water Polo membership expires %s." % when
        title = "Membership expires today" if left == 0 else "Membership expiring"
    elif kind == "safesport":
        sentence = "Your SafeSport training expires %s." % when
        title = "SafeSport expires today" if left == 0 else "SafeSport expiring"
    elif kind == "background":
        if left < 0:
            sentence = "Your background screening expired on %s." % date_iso
            title = "Background screening expired"
        else:
            sentence = "Your background screening expires %s." % when
            title = "Background screening expires today" if left == 0 else "Background screening expiring"
    else:
        sentence = "Your 2-week USAWP trial ends %s." % when
        title = "Trial ends today" if left == 0 else "Trial ending"
    return title, sentence, "/home"
def deliver_expiry(d, m, kind, date_iso, left):
    title, sentence, url = expiry_text(kind, date_iso, left)
    base_key = "expiry:%s:%s:%s" % (kind, date_iso, left)
    if wants_email_reminders(m) and m["email"]:
        ek = "email:" + base_key
        if claim_notice(d, m["id"], ek):
            if not smtp_ready(): release_notice(d, m["id"], ek)
            else:
                text = ("Hi %s,\n\n%s\n\nReverify in the app: %s/home\nGet a USAWP membership: %s\n\n"
                        "You can turn off these reminder emails in Notification settings. Practice cancellation emails still send.\n\nGrunions Water Polo\n") % (
                        display_first(m), sentence, app_base(), TRIAL_JOIN_URL)
                try: send_email(m["email"], title, text)
                except Exception as e:
                    app.logger.error("expiry email to %s failed: %s", m["email"], e); release_notice(d, m["id"], ek)
    if wants_push(m, "expiry"):
        pk = "push:" + base_key
        if claim_notice(d, m["id"], pk) and not push_member(d, m, "expiry", title, sentence, url):
            release_notice(d, m["id"], pk)
def trial_end_date(m):
    raw = None
    try:
        if m and "trial_acknowledged_at" in m.keys(): raw = m["trial_acknowledged_at"]
    except AttributeError: raw = None
    if not raw: return None
    try: return dt.date.fromisoformat(str(raw)[:10]) + dt.timedelta(days=TRIAL_DAYS)
    except ValueError: return None
def run_expiry_notices(d, today=None):
    today = today or today_pt()
    for m in d.execute("SELECT * FROM members WHERE COALESCE(role,'')!='system'"):
        if m["usawp_valid_until"]:
            try: left = (dt.date.fromisoformat(str(m["usawp_valid_until"])[:10]) - today).days
            except ValueError: left = None
            if left in (7, 1, 0): deliver_expiry(d, m, "membership", str(m["usawp_valid_until"])[:10], left)
        end = trial_end_date(m)
        if end and (m["usawp_status"] or "") != "verified":
            left = (end - today).days
            if left in (7, 1, 0): deliver_expiry(d, m, "trial", end.isoformat(), left)
    for kind, finder in (("safesport", safesport_req), ("background", background_req)):
        q = finder(d)
        if not q: continue
        for m in d.execute("""SELECT m.*, x.expires_on AS item_expires FROM member_reqs x JOIN members m ON m.id=x.member_id
                WHERE x.req_id=? AND x.expires_on IS NOT NULL AND COALESCE(m.role,'')!='system'""", (q["id"],)):
            if kind == "background" and (m["role"] or "") != "coach": continue
            try: left = (dt.date.fromisoformat(str(m["item_expires"])[:10]) - today).days
            except ValueError: continue
            due = left in (7, 1, 0) or (kind == "background" and left == -1)
            if due: deliver_expiry(d, m, kind, str(m["item_expires"])[:10], left)
def run_practice_reminders(d, now=None):
    now = wall_pt(now)
    lo = (now.date() - dt.timedelta(days=1)).isoformat(); hi = (now.date() + dt.timedelta(days=1)).isoformat()
    for p in d.execute("SELECT * FROM practices WHERE cancelled=0 AND date>=? AND date<=?", (lo, hi)):
        try: start = dt.datetime.fromisoformat(p["date"] + "T" + (p["start"] or "19:00"))
        except ValueError: continue
        delta = start - now
        if not (dt.timedelta(0) < delta <= dt.timedelta(hours=3)): continue
        rounded = int(round(delta.total_seconds() / 3600))
        if rounded <= 0: soon = "in less than an hour"
        elif rounded == 1: soon = "in about 1 hour"
        else: soon = "in about %d hours" % rounded
        body = "%s, %s at %s is %s." % (fmt_d(p["date"]), fmt_t(p["start"]), p["location"] or "practice", soon)
        url = "/practices/%s" % p["id"]
        going = d.execute("""SELECT m.* FROM rsvps r JOIN members m ON m.id=r.member_id
            WHERE r.practice_id=? AND r.going=1 AND COALESCE(m.role,'')!='system'""", (p["id"],))
        for m in going:
            if not wants_push(m, "practice_reminder"): continue
            key = "push:practice_reminder:%s" % p["id"]
            if claim_notice(d, m["id"], key) and not push_member(d, m, "practice_reminder", "Practice reminder", body, url):
                release_notice(d, m["id"], key)
def run_notify_jobs():
    d = open_db()
    try:
        if not claim_job(d, "notify_scan", 90): return
        run_practice_reminders(d); run_expiry_notices(d)
    except Exception:
        app.logger.exception("notification job failed")
    finally:
        d.close()
def start_scheduler():
    """One background scheduler per process. A DB lock keeps a second worker from sending the same notice."""
    global _scheduler
    if _scheduler is not None or os.environ.get("GRUNIONS_SCHEDULER", "1") != "1": return
    from apscheduler.schedulers.background import BackgroundScheduler
    _scheduler = BackgroundScheduler(daemon=True)
    _scheduler.add_job(run_notify_jobs, "interval", minutes=15, start_date=dt.datetime.now() + dt.timedelta(minutes=15),
                       id="notify", max_instances=1, coalesce=True, misfire_grace_time=120)
    _scheduler.add_job(run_daily_sheet_sync, "cron", hour=3, minute=15, timezone=PT,
                       id="sheet_daily", max_instances=1, coalesce=True, misfire_grace_time=3600)
    _scheduler.start()

SW_JS = """/* grunions-sw-64 */
self.addEventListener('push', function(event) {
  var data = {title: 'Grunions', body: '', url: '/'};
  try { if (event.data) data = Object.assign(data, event.data.json()); } catch (e) {}
  var tasks = [self.registration.showNotification(data.title || 'Grunions', {
    body: data.body || '', icon: '/static/icons/icon-192.png', badge: '/static/icons/icon-192.png', data: {url: data.url || '/'}
  })];
  if (typeof data.badge === 'number' && navigator.setAppBadge) {
    try {
      var badge = data.badge > 0 ? navigator.setAppBadge(data.badge) : (navigator.clearAppBadge && navigator.clearAppBadge());
      if (badge && badge.then) tasks.push(badge.catch(function(){}));
    } catch (e) {}
  }
  event.waitUntil(Promise.all(tasks));
});
self.addEventListener('notificationclick', function(event) {
  event.notification.close();
  var path = (event.notification.data && event.notification.data.url) || '/';
  var url = new URL(path, self.location.origin).href;
  event.waitUntil(clients.matchAll({type: 'window', includeUncontrolled: true}).then(function(list) {
    for (var i = 0; i < list.length; i++) {
      if (list[i].url.indexOf(self.location.origin) === 0 && 'focus' in list[i]) {
        if (list[i].navigate) return list[i].navigate(url).then(function(win) { return (win || list[i]).focus(); });
        return list[i].focus();
      }
    }
    if (clients.openWindow) return clients.openWindow(url);
  }));
});
"""
@app.route("/design-system")
@admin_required
def design_system_page():
    return page(T["design_system"], tab="admin")
@app.route("/sw.js")
def service_worker():
    resp = Response(SW_JS, mimetype="application/javascript")
    resp.headers["Cache-Control"] = "no-cache"
    resp.headers["Service-Worker-Allowed"] = "/"
    return resp
@app.route("/api/push/subscribe", methods=["POST"])
@login_required
def push_subscribe():
    j = request.get_json(silent=True) or {}
    endpoint = (j.get("endpoint") or "").strip()
    keys = j.get("keys") or {}
    p256dh, authk = (keys.get("p256dh") or "").strip(), (keys.get("auth") or "").strip()
    if not endpoint or not p256dh or not authk: return jsonify(error="bad subscription"), 400
    d = db()
    now = dt.datetime.now().isoformat(timespec="seconds")
    d.execute("""INSERT INTO push_subscriptions(member_id, endpoint, p256dh, auth, created) VALUES(?,?,?,?,?)
        ON CONFLICT(endpoint) DO UPDATE SET member_id=excluded.member_id, p256dh=excluded.p256dh, auth=excluded.auth, created=excluded.created""",
        (me()["id"], endpoint, p256dh, authk, now))
    d.commit(); return jsonify(ok=True)
@app.route("/notifications", methods=["GET", "POST"])
@login_required
def notifications():
    d = db(); m = d.execute("SELECT * FROM members WHERE id=?", (me()["id"],)).fetchone()
    if request.method == "POST":
        chosen = set(request.form.getlist("push"))
        prefs = notify_prefs(m)
        for key, _label in notify_types_for(m): prefs[key] = key in chosen
        d.execute("UPDATE members SET notify_prefs=?, email_reminders=? WHERE id=?", (json.dumps(prefs), 1 if request.form.get("email_reminders") else 0, m["id"]))
        d.commit(); flash("Notification settings saved."); return redirect("/notifications")
    return page(T["notifications"], tab="notifications", types=notify_types_for(m), prefs=notify_prefs(m), email_on=wants_email_reminders(m))

ensure_vapid()
start_scheduler()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5055)))
