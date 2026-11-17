"""Leaders (Figma 62 · L1–L6, N1): the board and each sport's leads, one person per role.

Data stays in the existing tables: leadership_roles (program_id NULL + board=1 for the board,
program_id for a sport), leadership_members, members.board_member (board chat + Manage).
New here, additive only: club_flags for the two "members can ask" switches.
"""
from markupsafe import escape


def ensure(d):
    d.execute("CREATE TABLE IF NOT EXISTS club_flags(key TEXT PRIMARY KEY, value TEXT NOT NULL DEFAULT '')")
    # Referees per sport. New, additive. The club-wide referee_list stays the source for "is a referee".
    d.execute("CREATE TABLE IF NOT EXISTS program_referees(program_id INTEGER NOT NULL, member_id INTEGER NOT NULL, PRIMARY KEY(program_id, member_id))")


def flag(d, key, default="1"):
    ensure(d)
    row = d.execute("SELECT value FROM club_flags WHERE key=?", (key,)).fetchone()
    return (row["value"] if row else default) == "1"


def set_flag(d, key, on):
    ensure(d)
    d.execute("INSERT INTO club_flags(key, value) VALUES(?,?) ON CONFLICT(key) DO UPDATE SET value=excluded.value", (key, "1" if on else "0"))


def board_requests_on(d):
    return flag(d, "board_requests")


def leads_requests_on(d, slug):
    return flag(d, "leads_requests:" + slug)


def chat_on(d, key):
    """Board chat ('board') and each sport's coaches chat ('coach:<slug>') can be turned off.
    Off hides the chat; its messages are kept and come back when it's turned on."""
    return flag(d, "chat:" + key)


def _name(m):
    return ("%s %s" % ((m["preferred_first"] or "").strip() or m["first"], m["last"] or "")).strip()


def _initials(name):
    return ("".join(part[:1] for part in name.split()[:2]) or "?").upper()


SPORT_ACCESS = {"sport_admin": "Sport admin", "none": ""}


def roles(d, program_id=None):
    """Rows for a group page: one row per held seat, an Open row for an empty role."""
    if program_id:
        rs = d.execute("SELECT * FROM leadership_roles WHERE program_id=? ORDER BY sort, id", (program_id,)).fetchall()
    else:
        rs = d.execute("""SELECT r.*, COALESCE(NULLIF(p.public_name,''), p.name) AS sport FROM leadership_roles r
            LEFT JOIN programs p ON p.id=r.program_id WHERE r.board=1 ORDER BY (r.program_id IS NOT NULL), r.sort, r.id""").fetchall()
    out = []
    for r in rs:
        people = d.execute("""SELECT m.id, m.first, m.preferred_first, m.last, m.is_admin FROM leadership_members lm
            JOIN members m ON m.id=lm.member_id WHERE lm.role_id=? AND COALESCE(m.role,'')!='system' ORDER BY m.last, m.first""", (r["id"],)).fetchall()
        board = bool(r["board"])
        if board:
            access = "Board"  # board members open Manage (is_club_admin); the chip says what they can actually do
        else:
            access = SPORT_ACCESS.get(r["permission"], "")
        label = r["name"] if (program_id or not r["program_id"]) else "%s · %s" % (r["name"], r["sport"] or "")
        if not people:
            out.append({"role_id": r["id"], "role": label, "member_id": None, "name": "Open", "initials": "+", "access": "", "open": True, "permission": r["permission"], "board": board})
        for p in people:
            name = _name(p)
            out.append({"role_id": r["id"], "role": label, "member_id": p["id"], "name": name, "initials": _initials(name),
                        "access": access or "—", "open": False, "permission": r["permission"], "board": board})
    if not program_id:
        # Board members from before titles existed: on the board, no role yet. Shown, never rewritten.
        seated = {r["member_id"] for r in out if r["member_id"]}
        for p in d.execute("""SELECT id, first, preferred_first, last FROM members WHERE COALESCE(board_member,0)=1
                AND COALESCE(role,'')!='system' ORDER BY last, first""").fetchall():
            if p["id"] in seated: continue
            name = _name(p)
            out.append({"role_id": None, "role": "Board · no title yet", "member_id": p["id"], "name": name, "initials": _initials(name),
                        "access": "Admin", "open": False, "permission": "none", "legacy": True})
    return out


def board_people(d):
    return d.execute("""SELECT id FROM members WHERE COALESCE(board_member,0)=1 AND COALESCE(role,'')!='system'""").fetchall()


def sport_coaches(d, program_id):
    return d.execute("""SELECT DISTINCT c.member_id FROM program_coaches c JOIN members m ON m.id=c.member_id
        WHERE c.program_id=? AND COALESCE(m.role,'')!='system'""", (program_id,)).fetchall()


def overview(d, programs):
    board = roles(d)
    held = [r for r in board if not r["open"]]
    names = [r["role"] for r in board if r["role_id"]]
    out = {"board": {"sub": ("%s · %d of %d filled" % (", ".join(dict.fromkeys(names)), len({r["role_id"] for r in held if r["role_id"]}), len({r["role_id"] for r in board if r["role_id"]})))
                     if names else ("%d on the board · no titles yet" % len(held) if held else "No roles yet"),
                     "chat": bool(board_people(d)) and chat_on(d, "board"), "requests": board_requests_on(d) and bool(board_people(d)), "count": len({r["role_id"] for r in board if r["role_id"]})},
           "sports": []}
    for p in programs:
        rs = roles(d, p["id"])
        filled = len({r["role_id"] for r in rs if not r["open"]})
        total = len({r["role_id"] for r in rs})
        coaches = sport_coaches(d, p["id"])
        out["sports"].append({"slug": p["slug"], "name": p["public_name"] or p["name"],
                              "sub": ("%s · %d of %d filled" % (", ".join(dict.fromkeys(r["role"] for r in rs)), filled, total)) if rs else "No one yet",
                              "chat": bool(coaches), "requests": leads_requests_on(d, p["slug"]) and bool(coaches)})
    return out


def access_counts(d):
    admins = d.execute("SELECT COUNT(*) FROM members WHERE is_admin=1 AND COALESCE(role,'')!='system'").fetchone()[0]

    def held(perm):
        return d.execute("""SELECT COUNT(DISTINCT lm.member_id) FROM leadership_members lm JOIN leadership_roles r ON r.id=lm.role_id
            JOIN members m ON m.id=lm.member_id WHERE r.permission=? AND COALESCE(m.role,'')!='system'""", (perm,)).fetchone()[0]
    return [("Admin", admins), ("Admin lite", held("admin_lite")), ("Sport admin", held("sport_admin"))]


def people_for_pick(d):
    """Everyone who can hold a role, with one line of context."""
    out = []
    for m in d.execute("""SELECT id, first, preferred_first, last, role, is_admin FROM members
            WHERE COALESCE(role,'')!='system' AND COALESCE(joined,1)=1 ORDER BY lower(COALESCE(NULLIF(preferred_first,''), first)), lower(last)""").fetchall():
        name = _name(m)
        out.append({"id": m["id"], "name": name, "line": "Coach" if (m["role"] or "") == "coach" else "Member"})
    return out


def _board_last_guard(d, member_id):
    """True when taking this person off the board still leaves someone who can open Manage."""
    if d.execute("SELECT 1 FROM members WHERE id=? AND is_admin=1", (member_id,)).fetchone():
        return True
    others = d.execute("""SELECT COUNT(*) FROM members WHERE id!=? AND COALESCE(role,'')!='system'
        AND (is_admin=1 OR COALESCE(board_member,0)=1)""", (member_id,)).fetchone()[0]
    return others > 0


def _sync_board_flag(d, member_id):
    """On the board while they hold any board role. Never strips the last person who can open Manage."""
    holds = d.execute("""SELECT 1 FROM leadership_members lm JOIN leadership_roles r ON r.id=lm.role_id
        WHERE lm.member_id=? AND r.board=1 LIMIT 1""", (member_id,)).fetchone()
    if holds:
        d.execute("UPDATE members SET board_member=1 WHERE id=?", (member_id,))
    elif _board_last_guard(d, member_id):
        d.execute("UPDATE members SET board_member=0 WHERE id=?", (member_id,))


def add_role(d, name, program_id=None, permission="none", board=False):
    """Add a role. A name that's already used in the same group gets numbered: the first becomes
    'Co-Captain (1)' and the new one 'Co-Captain (2)', then (3) and so on."""
    import re
    name = " ".join((name or "").split())[:80]
    if len(name) < 2:
        raise ValueError("Add a role name.")
    base = re.sub(r"\s*\(\d+\)$", "", name).strip() or name
    if program_id:
        if permission not in SPORT_ACCESS: permission = "none"
        same = d.execute("SELECT id, name FROM leadership_roles WHERE program_id=?", (program_id,)).fetchall()
    else:
        permission = "none"
        same = d.execute("SELECT id, name FROM leadership_roles WHERE program_id IS NULL", ()).fetchall()
    taken = []
    plain = None
    for r in same:
        nm = (r["name"] or "").strip()
        if nm.lower() == base.lower():
            plain = r; taken.append(1)
        else:
            m = re.match(r"^(.*?)\s*\((\d+)\)$", nm)
            if m and m.group(1).strip().lower() == base.lower():
                taken.append(int(m.group(2)))
    if taken:
        if plain is not None:
            base = (plain["name"] or base).strip()  # keep how the existing role is written
            d.execute("UPDATE leadership_roles SET name=? WHERE id=?", ("%s (1)" % base, plain["id"]))
        name = "%s (%d)" % (base, max(taken) + 1)
    sort = d.execute("SELECT COALESCE(MAX(sort),0)+1 FROM leadership_roles WHERE COALESCE(program_id,0)=COALESCE(?,0)", (program_id,)).fetchone()[0]
    return d.execute("INSERT INTO leadership_roles(program_id, name, permission, sort, board) VALUES(?,?,?,?,?)",
                     (program_id, name[:80], permission, sort, (1 if board else 0) if program_id else 1)).lastrowid


def set_board(d, role_id, on):
    """A sport role can also be a board role: its holder joins the board (#board, Manage)."""
    role = d.execute("SELECT * FROM leadership_roles WHERE id=? AND program_id IS NOT NULL", (role_id,)).fetchone()
    if not role:
        raise ValueError("Choose a sport role.")
    holders = [r["member_id"] for r in d.execute("SELECT member_id FROM leadership_members WHERE role_id=?", (role_id,))]
    if not on:
        for mid in holders:
            still = d.execute("""SELECT 1 FROM leadership_members lm JOIN leadership_roles r ON r.id=lm.role_id
                WHERE lm.member_id=? AND r.board=1 AND r.id!=? LIMIT 1""", (mid, role_id)).fetchone()
            if not still and not _board_last_guard(d, mid):
                raise ValueError("The last admin can't be removed.")
    d.execute("UPDATE leadership_roles SET board=? WHERE id=?", (1 if on else 0, role_id))
    for mid in holders:
        _sync_board_flag(d, mid)
    return role


def assign(d, role_id, member_id, permission=None):
    """One person per role (Figma L5). The person this replaces keeps any other roles they hold."""
    role = d.execute("SELECT * FROM leadership_roles WHERE id=?", (role_id,)).fetchone()
    if not role:
        raise ValueError("Choose a role.")
    person = d.execute("SELECT id FROM members WHERE id=? AND COALESCE(role,'')!='system'", (member_id or 0,)).fetchone()
    if not person:
        raise ValueError("Choose a person.")
    before = [r["member_id"] for r in d.execute("SELECT member_id FROM leadership_members WHERE role_id=?", (role_id,))]
    d.execute("DELETE FROM leadership_members WHERE role_id=?", (role_id,))
    d.execute("INSERT OR IGNORE INTO leadership_members(role_id, member_id) VALUES(?,?)", (role_id, member_id))
    if role["program_id"] and permission in SPORT_ACCESS:
        d.execute("UPDATE leadership_roles SET permission=? WHERE id=?", (permission, role_id))
    if not role["program_id"]:
        d.execute("UPDATE leadership_roles SET board=1 WHERE id=?", (role_id,))
    if not role["program_id"] or role["board"]:
        for mid in set(before + [member_id]):
            _sync_board_flag(d, mid)
    return role


def clear(d, role_id, member_id):
    role = d.execute("SELECT * FROM leadership_roles WHERE id=?", (role_id,)).fetchone()
    if not role:
        raise ValueError("Choose a role.")
    if role["board"]:
        still = d.execute("""SELECT 1 FROM leadership_members lm JOIN leadership_roles r ON r.id=lm.role_id
            WHERE lm.member_id=? AND r.board=1 AND r.id!=? LIMIT 1""", (member_id, role_id)).fetchone()
        if not still and not _board_last_guard(d, member_id):
            raise ValueError("The last admin can't be removed.")
    d.execute("DELETE FROM leadership_members WHERE role_id=? AND member_id=?", (role_id, member_id))
    if role["board"]:
        _sync_board_flag(d, member_id)
    return role


def delete_role(d, role_id):
    """Remove a role, held or open. Whoever holds it comes off it first (the last admin stays protected);
    any other roles they hold, and their chat messages, are untouched."""
    for row in d.execute("SELECT member_id FROM leadership_members WHERE role_id=?", (role_id,)).fetchall():
        clear(d, role_id, row["member_id"])
    d.execute("DELETE FROM leadership_roles WHERE id=?", (role_id,))


def member_line(d, member_id, fallback):
    """N1 people rows: 'Board · Secretary', 'Head coach · Water Polo'."""
    row = d.execute("""SELECT r.name, r.program_id, p.public_name, p.name AS pname FROM leadership_members lm
        JOIN leadership_roles r ON r.id=lm.role_id LEFT JOIN programs p ON p.id=r.program_id
        WHERE lm.member_id=? ORDER BY (r.program_id IS NOT NULL), r.sort LIMIT 1""", (member_id,)).fetchone()
    if not row:
        return fallback
    if row["program_id"]:
        return "%s · %s" % (row["name"], row["public_name"] or row["pname"])
    return "Board · %s" % row["name"]


def esc(s):
    return escape(s)
