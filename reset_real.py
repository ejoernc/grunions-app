"""Wipe demo data and leave a clean, real Grunions database.

Deletes all members, chat messages, reactions, check-ins, RSVPs, verify requests, notices, login tokens and uploaded images.
Keeps the schema, the requirements (Cleared-to-play rules) and the real practices (Tue Marina HS / Fri Westminster HS).
Re-creates Elliott Joern as the verified admin.

Usage:  python reset_real.py          (asks you to type RESET)
        python reset_real.py --yes    (no prompt)
Uses the same DATA_DIR / GRUNIONS_DB / GRUNIONS_UPLOADS settings as the app. Make a backup of grunions.db first.
"""
import os, sys, shutil, datetime as dt
import app as A

REAL_LOCATIONS = {"Marina High School": "15871 Springdale St, Huntington Beach", "Westminster High School": "Westminster"}
ELLIOTT = dict(first="Elliott", last="Joern", email="elliott.joern@gmail.com", number="659226", membership="2027-06-07")
COMPLIANCE = {"safesport": "2027-05-11", "background": "2028-08-28"}

def main():
    if "--yes" not in sys.argv:
        print(f"This permanently deletes all members, chat, check-ins and uploads in {A.DB}.")
        if input("Type RESET to continue: ").strip() != "RESET": print("Cancelled."); sys.exit(1)
    with A.app.app_context():
        d = A.db()
        for t in ("reactions", "messages", "checkins", "rsvps", "verify_requests", "notices", "login_tokens", "member_reqs", "members"):
            d.execute(f"DELETE FROM {t}")
        d.execute("DELETE FROM practices WHERE location NOT IN (%s)" % ",".join("?" * len(REAL_LOCATIONS)), tuple(REAL_LOCATIONS))
        now = dt.datetime.now().isoformat(timespec="minutes")
        mid = d.execute("""INSERT INTO members(first,last,email,phone,is_admin,role,usawp_status,usawp_raw,usawp_number,usawp_valid_until,
            usawp_updated,usawp_verified_by,usawp_verified_at) VALUES(?,?,?,'',1,'coach','verified','Current (Individual Membership, Coach)',?,?,?,'Sport:80 lookup',?)""",
            (ELLIOTT["first"], ELLIOTT["last"], ELLIOTT["email"], ELLIOTT["number"], ELLIOTT["membership"], now, now)).lastrowid
        for q in d.execute("SELECT id, keywords FROM requirements").fetchall():
            for kw, exp in COMPLIANCE.items():
                if kw in (q["keywords"] or ""):
                    d.execute("INSERT OR REPLACE INTO member_reqs VALUES(?,?,NULL,?,'Sport:80 lookup','Grunions bot',?)", (mid, q["id"], exp, now))
        d.commit()
        A.ensure_schedule(d)
        d.execute("VACUUM")
    if os.path.isdir(A.UPLOADS):
        for f in os.listdir(A.UPLOADS):
            p = os.path.join(A.UPLOADS, f)
            shutil.rmtree(p) if os.path.isdir(p) else os.remove(p)
    print(f"Reset done: {A.DB}. Admin: {ELLIOTT['email']}. Practices kept: " + ", ".join(REAL_LOCATIONS))

if __name__ == "__main__":
    main()
