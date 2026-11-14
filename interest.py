"""Interest check (Figma 62 · I1–I3): ask the team before dates and cost are set.

Hangs off a Lineup event that is still "Gauging interest" (team_intent='considering').
New tables only. An answer of "I'm in" also marks the member Interested on the event,
so every existing count, list and "We're official" notice keeps working.
"""
import datetime as dt
import json

ANSWERS = ("in", "maybe", "no")


def ensure(d):
    d.execute("""CREATE TABLE IF NOT EXISTS interest_checks(
        event_id INTEGER PRIMARY KEY, ask TEXT NOT NULL DEFAULT 'month', options TEXT NOT NULL DEFAULT '[]',
        cost TEXT NOT NULL DEFAULT '', need INTEGER NOT NULL DEFAULT 0, answer_by TEXT NOT NULL DEFAULT '',
        status TEXT NOT NULL DEFAULT 'open', nudged_at TEXT, created_by INTEGER, created_at TEXT)""")
    d.execute("""CREATE TABLE IF NOT EXISTS interest_answers(
        event_id INTEGER NOT NULL, member_id INTEGER NOT NULL, answer TEXT NOT NULL, picks TEXT NOT NULL DEFAULT '[]',
        at TEXT NOT NULL, PRIMARY KEY(event_id, member_id))""")


def get(d, eid):
    ensure(d)
    row = d.execute("SELECT * FROM interest_checks WHERE event_id=?", (eid,)).fetchone()
    if not row:
        return None
    out = dict(row)
    try:
        out["options"] = [str(o)[:40] for o in json.loads(row["options"] or "[]") if str(o).strip()][:8]
    except ValueError:
        out["options"] = []
    return out


def save(d, eid, form, mid):
    ensure(d)
    ask = form.get("ask") if form.get("ask") in ("month", "date", "none") else "month"
    options = []
    for raw in form.getlist("option") + [form.get("option_new") or ""]:
        o = " ".join(str(raw or "").split())[:40]
        if o and o not in options:
            options.append(o)
    if ask != "none" and not options:
        raise ValueError("Add at least one option for people to pick.")
    try:
        need = max(0, min(999, int(form.get("need") or 0)))
    except ValueError:
        raise ValueError("Use a whole number of people.")
    by = (form.get("answer_by") or "").strip()[:10]
    if by:
        try:
            dt.date.fromisoformat(by)
        except ValueError:
            raise ValueError("Pick an answer-by date.")
    cost = " ".join((form.get("cost") or "").split())[:40]
    d.execute("""INSERT INTO interest_checks(event_id, ask, options, cost, need, answer_by, status, created_by, created_at)
        VALUES(?,?,?,?,?,?,'open',?,?) ON CONFLICT(event_id) DO UPDATE SET ask=excluded.ask, options=excluded.options,
        cost=excluded.cost, need=excluded.need, answer_by=excluded.answer_by""",
              (eid, ask, json.dumps(options[:8]), cost, need, by, mid, dt.datetime.now().isoformat(timespec="seconds")))
    return get(d, eid)


def mine(d, eid, mid):
    ensure(d)
    row = d.execute("SELECT * FROM interest_answers WHERE event_id=? AND member_id=?", (eid, mid)).fetchone()
    if not row:
        return {"answer": "", "picks": []}
    try:
        picks = json.loads(row["picks"] or "[]")
    except ValueError:
        picks = []
    return {"answer": row["answer"], "picks": picks}


def answer(d, eid, mid, value, picks):
    check = get(d, eid)
    if not check or check["status"] != "open":
        raise ValueError("This question is closed.")
    if value not in ANSWERS:
        raise ValueError("Pick I'm in, Maybe, or Not this time.")
    picks = [p for p in picks if p in check["options"]] if value != "no" else []
    d.execute("""INSERT INTO interest_answers(event_id, member_id, answer, picks, at) VALUES(?,?,?,?,?)
        ON CONFLICT(event_id, member_id) DO UPDATE SET answer=excluded.answer, picks=excluded.picks, at=excluded.at""",
              (eid, mid, value, json.dumps(picks), dt.datetime.now().isoformat(timespec="seconds")))


def results(d, eid):
    check = get(d, eid)
    rows = d.execute("""SELECT a.*, m.first, m.preferred_first, m.last FROM interest_answers a JOIN members m ON m.id=a.member_id
        WHERE a.event_id=? AND COALESCE(m.role,'')!='system' ORDER BY a.at""", (eid,)).fetchall()
    people, counts = [], {"in": 0, "maybe": 0, "no": 0}
    per = {o: {"in": 0, "maybe": 0} for o in (check["options"] if check else [])}
    for r in rows:
        try:
            picks = json.loads(r["picks"] or "[]")
        except ValueError:
            picks = []
        counts[r["answer"]] = counts.get(r["answer"], 0) + 1
        for p in picks:
            if p in per and r["answer"] in ("in", "maybe"):
                per[p][r["answer"]] += 1
        name = ("%s %s" % ((r["preferred_first"] or "").strip() or r["first"], r["last"] or "")).strip()
        people.append({"id": r["member_id"], "name": name, "answer": r["answer"], "picks": picks})
    best = max(per.items(), key=lambda kv: (kv[1]["in"], kv[1]["maybe"]))[0] if per and any(v["in"] for v in per.values()) else ""
    return {"check": check, "counts": counts, "per": per, "people": people, "best": best}


def short_pick(p):
    return p.split(" ")[0][:3] if p else p
