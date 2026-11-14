"""Leaders (Figma 62 · L1–L6, N1): the board and each sport's leads, one person per role.

Data stays in the existing tables: leadership_roles (program_id NULL + board=1 for the board,
program_id for a sport), leadership_members, members.board_member (board chat + Manage).
New here, additive only: club_flags for the two "members can ask" switches.
"""
from markupsafe import escape


def ensure(d):
    d.execute("CREATE TABLE IF NOT EXISTS club_flags(key TEXT PRIMARY KEY, value TEXT NOT NULL DEFAULT '')")


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
        rs = d.execute("SELECT * FROM leadership_roles WHERE program_id IS NULL AND board=1 ORDER BY sort, id").fetchall()
    out = []
    for r in rs:
        people = d.execute("""SELECT m.id, m.first, m.preferred_first, m.last, m.is_admin FROM leadership_members lm
            JOIN members m ON m.id=lm.member_id WHERE lm.role_id=? AND COALESCE(m.role,'')!='system' ORDER BY m.last, m.first""", (r["id"],)).fetchall()
        if program_id:
            access = SPORT_ACCESS.get(r["permission"], "")
        else:
            access = "Admin"  # board members open Manage (is_club_admin); the chip says what they can actually do
        if not people:
            out.append({"role_id": r["id"], "role": r["name"], "member_id": None, "name": "Open", "initials": "+", "access": "Assign", "open": True, "permission": r["permission"]})
        for p in people:
            name = _name(p)
            out.append({"role_id": r["id"], "role": r["name"], "member_id": p["id"], "name": name, "initials": _initials(name),
                        "access": access or "—", "open": False, "permission": r["permission"]})
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
                     "chat": bool(board_people(d)), "requests": board_requests_on(d) and bool(board_people(d)), "count": len({r["role_id"] for r in board if r["role_id"]})},
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
        WHERE lm.member_id=? AND r.program_id IS NULL AND r.board=1 LIMIT 1""", (member_id,)).fetchone()
    if holds:
        d.execute("UPDATE members SET board_member=1 WHERE id=?", (member_id,))
    elif _board_last_guard(d, member_id):
        d.execute("UPDATE members SET board_member=0 WHERE id=?", (member_id,))


def add_role(d, name, program_id=None, permission="none"):
    name = " ".join((name or "").split())[:80]
    if len(name) < 2:
        raise ValueError("Add a role name.")
    if program_id:
        if permission not in SPORT_ACCESS: permission = "none"
        hit = d.execute("SELECT id FROM leadership_roles WHERE program_id=? AND lower(name)=lower(?)", (program_id, name)).fetchone()
    else:
        permission = "none"
        hit = d.execute("SELECT id FROM leadership_roles WHERE program_id IS NULL AND lower(name)=lower(?)", (name,)).fetchone()
    if hit:
        if not program_id: d.execute("UPDATE leadership_roles SET board=1 WHERE id=?", (hit["id"],))
        return hit["id"]
    sort = d.execute("SELECT COALESCE(MAX(sort),0)+1 FROM leadership_roles WHERE COALESCE(program_id,0)=COALESCE(?,0)", (program_id,)).fetchone()[0]
    return d.execute("INSERT INTO leadership_roles(program_id, name, permission, sort, board) VALUES(?,?,?,?,?)",
                     (program_id, name, permission, sort, 0 if program_id else 1)).lastrowid


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
        for mid in set(before + [member_id]):
            _sync_board_flag(d, mid)
    return role


def clear(d, role_id, member_id):
    role = d.execute("SELECT * FROM leadership_roles WHERE id=?", (role_id,)).fetchone()
    if not role:
        raise ValueError("Choose a role.")
    if not role["program_id"]:
        still = d.execute("""SELECT 1 FROM leadership_members lm JOIN leadership_roles r ON r.id=lm.role_id
            WHERE lm.member_id=? AND r.program_id IS NULL AND r.board=1 AND r.id!=? LIMIT 1""", (member_id, role_id)).fetchone()
        if not still and not _board_last_guard(d, member_id):
            raise ValueError("The last admin can't be removed.")
    d.execute("DELETE FROM leadership_members WHERE role_id=? AND member_id=?", (role_id, member_id))
    if not role["program_id"]:
        _sync_board_flag(d, member_id)
    return role


def delete_role(d, role_id):
    if d.execute("SELECT 1 FROM leadership_members WHERE role_id=? LIMIT 1", (role_id,)).fetchone():
        raise ValueError("Clear the role first.")
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
