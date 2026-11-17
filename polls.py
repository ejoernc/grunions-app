"""Polls in chat. A poll has one or more questions; each is single or multiple choice.
Anonymous polls show counts only; open polls can show who voted for what.
Voting happens on the poll's own page; results show in the chat as a card.

Additive tables only. Turned on for coaches chats first (see enabled())."""
import datetime as dt

MAX_QUESTIONS = 10
MAX_OPTIONS = 12


def enabled(ch):
    """Where polls are available. Coaches chats first, to test; widen this to open them up."""
    return ch == "coaches" or (ch or "").startswith("coach:")


def ensure(d):
    d.execute("""CREATE TABLE IF NOT EXISTS polls(id INTEGER PRIMARY KEY, channel TEXT NOT NULL, creator_id INTEGER NOT NULL,
        title TEXT NOT NULL, anonymous INTEGER NOT NULL DEFAULT 0, ends_at TEXT NOT NULL DEFAULT '', closed_at TEXT NOT NULL DEFAULT '',
        message_id INTEGER, created_at TEXT NOT NULL)""")
    d.execute("""CREATE TABLE IF NOT EXISTS poll_questions(id INTEGER PRIMARY KEY, poll_id INTEGER NOT NULL, ord INTEGER NOT NULL,
        text TEXT NOT NULL, multi INTEGER NOT NULL DEFAULT 0)""")
    d.execute("""CREATE TABLE IF NOT EXISTS poll_options(id INTEGER PRIMARY KEY, question_id INTEGER NOT NULL, ord INTEGER NOT NULL, text TEXT NOT NULL)""")
    d.execute("""CREATE TABLE IF NOT EXISTS poll_votes(question_id INTEGER NOT NULL, option_id INTEGER NOT NULL, member_id INTEGER NOT NULL,
        at TEXT NOT NULL, PRIMARY KEY(question_id, option_id, member_id))""")
    cols = {r[1] for r in d.execute("PRAGMA table_info(messages)")}
    if "poll_id" not in cols:
        d.execute("ALTER TABLE messages ADD COLUMN poll_id INTEGER")
    pcols = {r[1] for r in d.execute("PRAGMA table_info(polls)")}
    if "allow_add" not in pcols:
        d.execute("ALTER TABLE polls ADD COLUMN allow_add INTEGER NOT NULL DEFAULT 0")
    if "post_results" not in pcols:
        d.execute("ALTER TABLE polls ADD COLUMN post_results INTEGER NOT NULL DEFAULT 0")
    if "results_posted_at" not in pcols:
        d.execute("ALTER TABLE polls ADD COLUMN results_posted_at TEXT NOT NULL DEFAULT ''")
    mcols = {r[1] for r in d.execute("PRAGMA table_info(members)")}
    if "poll_email" not in mcols:
        d.execute("ALTER TABLE members ADD COLUMN poll_email INTEGER NOT NULL DEFAULT 1")


def _clean(text, n):
    return " ".join((text or "").split())[:n]


def parse_form(form):
    """Builder form -> (title, anonymous, ends_at, questions[]) or raises ValueError with a readable message.
    Fields: title, anonymous, ends_at (YYYY-MM-DDTHH:MM, optional), q<i>_text, q<i>_multi, q<i>_opt (repeated)."""
    title = _clean(form.get("title"), 140)
    questions = []
    for i in range(MAX_QUESTIONS):
        text = _clean(form.get("q%d_text" % i), 200)
        opts = [o for o in (_clean(x, 120) for x in form.getlist("q%d_opt" % i)) if o]
        if not text and not opts:
            continue
        if not text:
            raise ValueError("Question %d needs a question." % (len(questions) + 1))
        seen, uniq = set(), []
        for o in opts:
            if o.lower() not in seen:
                seen.add(o.lower()); uniq.append(o)
        if len(uniq) < 2:
            raise ValueError("“%s” needs at least two options." % text)
        questions.append({"text": text, "multi": form.get("q%d_multi" % i) == "1", "options": uniq[:MAX_OPTIONS]})
    if not questions:
        raise ValueError("Add a question with at least two options.")
    if not title:
        title = questions[0]["text"]
    ends_at = (form.get("ends_at") or "").strip()[:16]
    if ends_at:
        try:
            dt.datetime.fromisoformat(ends_at)
        except ValueError:
            raise ValueError("Pick a valid end time.")
    return title, form.get("anonymous") == "1", ends_at, questions, form.get("allow_add") == "1", form.get("post_results") == "1"


def create(d, ch, creator_id, title, anonymous, ends_at, questions, now_iso, allow_add=False, post_results=False):
    pid = d.execute("INSERT INTO polls(channel, creator_id, title, anonymous, ends_at, created_at, allow_add, post_results) VALUES(?,?,?,?,?,?,?,?)",
                    (ch, creator_id, title, 1 if anonymous else 0, ends_at or "", now_iso, 1 if allow_add else 0, 1 if post_results else 0)).lastrowid
    for qi, q in enumerate(questions):
        qid = d.execute("INSERT INTO poll_questions(poll_id, ord, text, multi) VALUES(?,?,?,?)", (pid, qi, q["text"], 1 if q["multi"] else 0)).lastrowid
        for oi, o in enumerate(q["options"]):
            d.execute("INSERT INTO poll_options(question_id, ord, text) VALUES(?,?,?)", (qid, oi, o))
    return pid


def get(d, pid):
    return d.execute("SELECT * FROM polls WHERE id=?", (pid,)).fetchone()


def is_closed(p, now):
    if (p["closed_at"] or ""):
        return True
    if (p["ends_at"] or ""):
        try:
            return now >= dt.datetime.fromisoformat(p["ends_at"])
        except ValueError:
            return False
    return False


def questions(d, pid):
    out = []
    for q in d.execute("SELECT * FROM poll_questions WHERE poll_id=? ORDER BY ord, id", (pid,)):
        opts = d.execute("SELECT * FROM poll_options WHERE question_id=? ORDER BY ord, id", (q["id"],)).fetchall()
        out.append({"id": q["id"], "text": q["text"], "multi": bool(q["multi"]), "options": opts})
    return out


def my_votes(d, pid, member_id):
    return {(r["question_id"], r["option_id"]) for r in d.execute(
        """SELECT v.question_id, v.option_id FROM poll_votes v JOIN poll_questions q ON q.id=v.question_id
        WHERE q.poll_id=? AND v.member_id=?""", (pid, member_id))}


def voted(d, pid, member_id):
    return bool(d.execute("""SELECT 1 FROM poll_votes v JOIN poll_questions q ON q.id=v.question_id
        WHERE q.poll_id=? AND v.member_id=? LIMIT 1""", (pid, member_id)).fetchone())


def add_option(d, question_id, text):
    """Add an option to a question (by the creator while editing, or by a voter when the poll allows it).
    Same text as an existing option returns that option instead of a duplicate."""
    text = _clean(text, 120)
    if not text:
        return None
    for o in d.execute("SELECT id, text FROM poll_options WHERE question_id=?", (question_id,)):
        if (o["text"] or "").strip().lower() == text.lower():
            return o["id"]
    n = d.execute("SELECT COUNT(*) FROM poll_options WHERE question_id=?", (question_id,)).fetchone()[0]
    if n >= MAX_OPTIONS * 3:
        raise ValueError("That question has as many options as it can hold.")
    ord_ = d.execute("SELECT COALESCE(MAX(ord),0)+1 FROM poll_options WHERE question_id=?", (question_id,)).fetchone()[0]
    return d.execute("INSERT INTO poll_options(question_id, ord, text) VALUES(?,?,?)", (question_id, ord_, text)).lastrowid


def edit_texts(d, pid, form):
    """Rename the title, questions, and options, and add options. Nothing is removed, so every vote stays."""
    p = get(d, pid)
    title = _clean(form.get("title"), 140) or p["title"]
    d.execute("UPDATE polls SET title=?, allow_add=?, post_results=? WHERE id=?",
              (title, 1 if form.get("allow_add") == "1" else 0, 1 if form.get("post_results") == "1" else 0, pid))
    for q in questions(d, pid):
        qt = _clean(form.get("qt%d" % q["id"]), 200)
        if qt:
            d.execute("UPDATE poll_questions SET text=? WHERE id=?", (qt, q["id"]))
        for o in q["options"]:
            ot = _clean(form.get("ot%d" % o["id"]), 120)
            if ot:
                d.execute("UPDATE poll_options SET text=? WHERE id=?", (ot, o["id"]))
        for extra in form.getlist("new%d" % q["id"]):
            add_option(d, q["id"], extra)


def vote(d, pid, member_id, form, now_iso, allow_add=False):
    """Replace this person's answers. Every question needs an answer; single choice takes one.
    When the poll allows it, an option typed in (add<qid>) is added and counts as their pick."""
    qs = questions(d, pid)
    added = {}
    if allow_add:
        for q in qs:
            new = _clean(form.get("add%d" % q["id"]), 120)
            if new:
                added[q["id"]] = add_option(d, q["id"], new)
        if added:
            qs = questions(d, pid)
    picks = {}
    for q in qs:
        valid = {o["id"] for o in q["options"]}
        chosen = [int(x) for x in form.getlist("q%d" % q["id"]) if str(x).isdigit() and int(x) in valid]
        if q["id"] in added and added[q["id"]]:
            chosen = ([added[q["id"]]] + [c for c in chosen if c != added[q["id"]]]) if q["multi"] else [added[q["id"]]]
        if not chosen:
            raise ValueError("Answer “%s”." % q["text"])
        if not q["multi"]:
            chosen = chosen[:1]
        picks[q["id"]] = chosen
    for q in qs:
        d.execute("DELETE FROM poll_votes WHERE question_id=? AND member_id=?", (q["id"], member_id))
        for oid in picks[q["id"]]:
            d.execute("INSERT INTO poll_votes(question_id, option_id, member_id, at) VALUES(?,?,?,?)", (q["id"], oid, member_id, now_iso))


def summary(d, p, viewer_id, now, name_of, can_end=False):
    """What the chat card, the sticky bar, and the list show."""
    qs = questions(d, p["id"])
    voters = d.execute("""SELECT COUNT(DISTINCT v.member_id) FROM poll_votes v JOIN poll_questions q ON q.id=v.question_id
        WHERE q.poll_id=?""", (p["id"],)).fetchone()[0]
    mine = my_votes(d, p["id"], viewer_id)
    out_q = []
    for q in qs:
        rows = d.execute("SELECT option_id, member_id FROM poll_votes WHERE question_id=? ORDER BY at", (q["id"],)).fetchall()
        by_opt = {}
        for r in rows:
            by_opt.setdefault(r["option_id"], []).append(r["member_id"])
        answered = len({r["member_id"] for r in rows}) or 0
        opts = []
        top = max((len(v) for v in by_opt.values()), default=0)
        for o in q["options"]:
            ids = by_opt.get(o["id"], [])
            opts.append({"id": o["id"], "text": o["text"], "n": len(ids), "pct": round(100 * len(ids) / answered) if answered else 0,
                         "mine": (q["id"], o["id"]) in mine, "top": bool(ids) and len(ids) == top,
                         "who": [] if p["anonymous"] else [name_of(i) for i in ids]})
        out_q.append({"id": q["id"], "text": q["text"], "multi": q["multi"], "options": opts})
    closed = is_closed(p, now)
    ends = ""
    if p["ends_at"] and not closed:
        try:
            e = dt.datetime.fromisoformat(p["ends_at"])
            hour = e.hour % 12 or 12
            clock = ("%d %s" % (hour, "AM" if e.hour < 12 else "PM")) if e.minute == 0 else ("%d:%02d %s" % (hour, e.minute, "AM" if e.hour < 12 else "PM"))
            ends = "Ends %s %d, %s" % (e.strftime("%b"), e.day, clock)
        except ValueError:
            ends = ""
    return {"id": p["id"], "title": p["title"], "anonymous": bool(p["anonymous"]), "closed": closed, "ends": ends,
            "voters": voters, "voted": bool(mine), "questions": out_q, "can_end": bool(can_end and not closed), "can_edit": bool(can_end),
            "allow_add": bool(p["allow_add"]) if "allow_add" in p.keys() else False,
            "href": "/polls/%d" % p["id"]}


def for_channel(d, ch):
    return d.execute("SELECT * FROM polls WHERE channel=? ORDER BY id DESC", (ch,)).fetchall()


def due_results(d, now):
    """Closed polls that should post their results and haven't yet."""
    out = []
    for p in d.execute("SELECT * FROM polls WHERE post_results=1 AND results_posted_at=''"):
        if is_closed(p, now):
            out.append(p)
    return out
