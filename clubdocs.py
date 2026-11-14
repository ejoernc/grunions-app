"""Club documents (Figma 62 · D1–D4): the liability waiver plus a code of conduct, a membership
agreement, or any other document members accept once, in the same sheet as their insurance number.

The waiver keeps living in club_waiver / waiver_acceptances (nothing moves). Other documents are new
rows in club_docs / doc_acceptances. Additive only.
"""
import datetime as dt

PRESETS = (("conduct", "Code of conduct"), ("membership", "Membership agreement"))
KIND_LABEL = dict(PRESETS + (("waiver", "Waiver"), ("custom", "Document")))
SOURCES = (("url", "Link (URL)"), ("pdf", "Upload PDF"), ("text", "Paste text"))


def _now():
    return dt.datetime.now().isoformat(timespec="seconds")


def ensure(d):
    d.execute("""CREATE TABLE IF NOT EXISTS club_docs(
        id INTEGER PRIMARY KEY, kind TEXT NOT NULL, title TEXT NOT NULL, body TEXT NOT NULL DEFAULT '', url TEXT NOT NULL DEFAULT '',
        pdf TEXT NOT NULL DEFAULT '', source TEXT NOT NULL DEFAULT 'text', version INTEGER NOT NULL DEFAULT 0,
        enabled INTEGER NOT NULL DEFAULT 0, note TEXT NOT NULL DEFAULT '', updated_at TEXT, updated_by TEXT)""")
    d.execute("""CREATE TABLE IF NOT EXISTS doc_acceptances(
        id INTEGER PRIMARY KEY, doc_id INTEGER NOT NULL, member_id INTEGER NOT NULL, version INTEGER NOT NULL,
        typed_name TEXT NOT NULL, practice_id INTEGER, at TEXT NOT NULL)""")
    d.execute("CREATE INDEX IF NOT EXISTS doc_acc_member ON doc_acceptances(member_id, doc_id, version)")
    have = {r[1] for r in d.execute("PRAGMA table_info(club_waiver)")}
    for col, ddl in (("pdf", "TEXT NOT NULL DEFAULT ''"), ("source", "TEXT NOT NULL DEFAULT ''"), ("note", "TEXT NOT NULL DEFAULT ''")):
        if col not in have:
            d.execute("ALTER TABLE club_waiver ADD COLUMN %s %s" % (col, ddl))


def _source(row):
    s = (row["source"] or "") if "source" in row.keys() else ""
    if s in ("url", "pdf", "text"):
        return s
    if (row["pdf"] if "pdf" in row.keys() else ""):
        return "pdf"
    return "url" if (row["url"] or "").strip() and not (row["body"] or "").strip() else "text"


def team_size(d):
    return d.execute("SELECT COUNT(*) FROM members WHERE COALESCE(role,'')!='system' AND COALESCE(joined,0)=1").fetchone()[0]


def _shape(d, row, key, kind):
    if key == "waiver":
        signed = d.execute("SELECT COUNT(DISTINCT member_id) FROM waiver_acceptances WHERE version=?", (row["version"],)).fetchone()[0]
        published = bool(row["enabled"]) or bool((row["body"] or "").strip() or (row["url"] or "").strip())
    else:
        signed = d.execute("SELECT COUNT(DISTINCT member_id) FROM doc_acceptances WHERE doc_id=? AND version=?", (row["id"], row["version"])).fetchone()[0]
        published = (row["version"] or 0) > 0
    return {"key": key, "kind": kind, "title": row["title"] or KIND_LABEL.get(kind, "Document"), "body": row["body"] or "",
            "url": row["url"] or "", "pdf": (row["pdf"] if "pdf" in row.keys() else "") or "", "source": _source(row),
            "version": row["version"] or 0, "enabled": bool(row["enabled"]), "published": published, "signed": signed,
            "note": (row["note"] if "note" in row.keys() else "") or "", "updated_at": row["updated_at"] or "",
            "updated_by": row["updated_by"] or ""}


def get(d, key):
    ensure(d)
    if key == "waiver":
        import flows2
        return _shape(d, flows2.waiver(d), "waiver", "waiver")
    if not str(key).isdigit():
        return None
    row = d.execute("SELECT * FROM club_docs WHERE id=?", (int(key),)).fetchone()
    return _shape(d, row, str(row["id"]), row["kind"]) if row else None


def all_docs(d):
    ensure(d)
    out = [get(d, "waiver")]
    for row in d.execute("SELECT * FROM club_docs ORDER BY id"):
        out.append(_shape(d, row, str(row["id"]), row["kind"]))
    return out


def overview(d):
    docs = all_docs(d)
    live = [x for x in docs if x["enabled"]]
    rest = [x for x in docs if not x["enabled"]]
    have_kinds = {x["kind"] for x in docs}
    missing = [(k, label) for k, label in PRESETS if k not in have_kinds]
    return live, rest, missing


def create(d, kind, actor):
    ensure(d)
    if kind not in ("conduct", "membership", "custom"):
        kind = "custom"
    title = KIND_LABEL.get(kind, "Document") if kind != "custom" else "New document"
    if kind != "custom":
        hit = d.execute("SELECT id FROM club_docs WHERE kind=?", (kind,)).fetchone()
        if hit:
            return hit["id"]
    return d.execute("INSERT INTO club_docs(kind, title, version, enabled, updated_at, updated_by) VALUES(?,?,0,0,?,?)",
                     (kind, title, _now(), actor)).lastrowid


def save(d, key, form, actor, pdf_name="", publish=False):
    """Typo fix (no re-sign) or publish a new version (everyone accepts again). Old signatures stay on record."""
    doc = get(d, key)
    if not doc:
        raise ValueError("That document is gone.")
    source = form.get("source") if form.get("source") in ("url", "pdf", "text") else doc["source"]
    body = (form.get("body") if form.get("body") is not None else doc["body"]).strip()[:20000]
    url = (form.get("url") if form.get("url") is not None else doc["url"]).strip()[:500]
    if url and not url.lower().startswith(("https://", "http://")):
        raise ValueError("Use a link that starts with https://")
    pdf = pdf_name or doc["pdf"]
    title = " ".join((form.get("title") or doc["title"]).split())[:120] or doc["title"]
    if source == "text" and not body: raise ValueError("Paste the text members will read.")
    if source == "url" and not url: raise ValueError("Add the link members will open.")
    if source == "pdf" and not pdf: raise ValueError("Upload the PDF members will read.")
    first = not doc["published"]
    if first:
        version = max(doc["version"], 1)  # the first publish is version 1 (the waiver row starts at 1)
    else:
        version = doc["version"] + 1 if publish else doc["version"]
    note = " ".join((form.get("note") or "").split())[:200] if publish else doc["note"]
    enabled = 1 if first else (1 if doc["enabled"] else 0)
    if key == "waiver":
        d.execute("UPDATE club_waiver SET title=?, body=?, url=?, pdf=?, source=?, version=?, note=?, enabled=?, updated_at=?, updated_by=? WHERE id=1",
                  (title, body, url, pdf, source, max(version, 1), note, enabled, _now(), actor))
    else:
        d.execute("UPDATE club_docs SET title=?, body=?, url=?, pdf=?, source=?, version=?, note=?, enabled=?, updated_at=?, updated_by=? WHERE id=?",
                  (title, body, url, pdf, source, version, note, enabled, _now(), actor, int(key)))
    return get(d, key)


def set_required(d, key, on):
    doc = get(d, key)
    if not doc:
        raise ValueError("That document is gone.")
    if on and not doc["published"]:
        raise ValueError("Publish it first.")
    if key == "waiver":
        d.execute("UPDATE club_waiver SET enabled=? WHERE id=1", (1 if on else 0,))
    else:
        d.execute("UPDATE club_docs SET enabled=? WHERE id=?", (1 if on else 0, int(key)))


def remove(d, key):
    """Only a document nobody has accepted can be removed; signed ones are switched off instead."""
    if key == "waiver" or not str(key).isdigit():
        raise ValueError("The waiver can be switched off, not removed.")
    if d.execute("SELECT 1 FROM doc_acceptances WHERE doc_id=? LIMIT 1", (int(key),)).fetchone():
        raise ValueError("People have accepted it. Switch it off instead.")
    d.execute("DELETE FROM club_docs WHERE id=?", (int(key),))


def pending(d, member_id):
    """Required documents (not the waiver) this person hasn't accepted at the current version."""
    ensure(d)
    out = []
    for row in d.execute("SELECT * FROM club_docs WHERE enabled=1 AND version>0 ORDER BY id"):
        if not d.execute("SELECT 1 FROM doc_acceptances WHERE doc_id=? AND member_id=? AND version=? LIMIT 1",
                         (row["id"], member_id, row["version"])).fetchone():
            out.append(_shape(d, row, str(row["id"]), row["kind"]))
    return out


def accept(d, doc, member_id, typed_name, practice_id=None):
    d.execute("INSERT INTO doc_acceptances(doc_id, member_id, version, typed_name, practice_id, at) VALUES(?,?,?,?,?,?)",
              (int(doc["key"]), member_id, doc["version"], typed_name.strip()[:120], practice_id, _now()))


def signers(d, key, accepted=True):
    doc = get(d, key)
    if key == "waiver":
        q = "SELECT DISTINCT member_id FROM waiver_acceptances WHERE version=?"
        args = (doc["version"],)
    else:
        q = "SELECT DISTINCT member_id FROM doc_acceptances WHERE doc_id=? AND version=?"
        args = (int(key), doc["version"])
    ids = {r[0] for r in d.execute(q, args)}
    rows = d.execute("""SELECT id, first, preferred_first, last FROM members WHERE COALESCE(role,'')!='system' AND COALESCE(joined,0)=1
        ORDER BY lower(COALESCE(NULLIF(preferred_first,''), first)), lower(last)""").fetchall()
    return [r for r in rows if (r["id"] in ids) == accepted]
