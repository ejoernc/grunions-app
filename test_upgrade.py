"""Merge safety: a database written by `main` must boot on this branch with nothing lost,
and main's team chat must read as #everyone. Run: .venv/bin/python -m pytest -q test_upgrade.py

Builds main's code from git (origin/main), lets it create and fill a database, then boots this
branch on the same file and compares every table main created, row for row.
"""
import os, sys, json, sqlite3, subprocess, tempfile, shutil

HERE = os.path.dirname(os.path.abspath(__file__))
PY = sys.executable

MAIN_SIDE = r'''
import os, sys, json, sqlite3
sys.path.insert(0, os.getcwd())
import app as A  # main's code
A.open_db().close()  # main's full schema + migrations
d = sqlite3.connect(A.DB)
c = d.cursor()
c.execute("INSERT INTO members(first,last,email,phone,is_admin) VALUES('Ada','Old','ada@example.com','1',1)")
c.execute("INSERT INTO members(first,last,email,phone) VALUES('Ben','Old','ben@example.com','2')")
c.execute("UPDATE members SET usawp_number='1234567', usawp_status='verified', usawp_valid_until='2031-08-31' WHERE email='ada@example.com'")
c.execute("UPDATE members SET usawp_number='7654321' WHERE email='ben@example.com'")  # entered, not verified yet
c.execute("INSERT INTO members(first,last,email,phone) VALUES('Cy','New','cy@example.com','3')")  # never gave a number
c.execute("INSERT INTO practices(date,start,end,location) VALUES('2030-01-08','19:00','20:30','Old Pool')")
pid = c.lastrowid
c.execute("INSERT INTO rsvps(practice_id,member_id,going) VALUES(?,1,1)", (pid,))
c.execute("INSERT INTO rsvps(practice_id,member_id,going) VALUES(?,2,0)", (pid,))
c.execute("INSERT INTO checkins(member_id,practice_date,location) VALUES(1,'2030-01-01','Old Pool')")
c.execute("INSERT INTO messages(member_id,body) VALUES(1,'legacy default channel hello')")
c.execute("INSERT INTO messages(member_id,body,channel) VALUES(2,'legacy explicit team hello','team')")
c.execute("INSERT INTO messages(member_id,body,channel) VALUES(2,'legacy null channel hello',NULL)")
c.execute("INSERT INTO messages(member_id,body,channel) VALUES(1,'legacy empty channel hello','')")
c.execute("INSERT INTO messages(member_id,body,channel) VALUES(1,'coaches only note','coaches')")
c.execute("INSERT OR REPLACE INTO chat_reads(member_id,channel,last_read) VALUES(2,'team',1)")
d.commit()
out = {}
for (t,) in d.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'"):
    cols = [r[1] for r in d.execute("PRAGMA table_info(%s)" % t)]
    rows = d.execute("SELECT rowid,%s FROM %s ORDER BY rowid" % (",".join('"%s"' % x for x in cols), t)).fetchall()
    out[t] = {"cols": cols, "rows": [list(r) for r in rows]}
print(json.dumps(out, default=str))
'''

BRANCH_SIDE = r'''
import os, sys, json, sqlite3
sys.path.insert(0, os.environ["BRANCH_DIR"])
before = json.load(open(os.environ["SNAP"]))
import app as A  # this branch
A.open_db().close(); A.app.test_client().get('/join')  # this branch's additive migrations
d = sqlite3.connect(A.DB)
problems = []
for t, snap in before.items():
    have = {r[0] for r in d.execute("SELECT name FROM sqlite_master WHERE type='table'")}
    if t not in have: problems.append("table dropped: " + t); continue
    cols = [r[1] for r in d.execute("PRAGMA table_info(%s)" % t)]
    missing = [c for c in snap["cols"] if c not in cols]
    if missing: problems.append("%s lost columns %s" % (t, missing)); continue
    rows = d.execute("SELECT rowid,%s FROM %s ORDER BY rowid" % (",".join('"%s"' % x for x in snap["cols"]), t)).fetchall()
    newmap = {r[0]: r for r in rows}
    for r in snap["rows"]:
        n = newmap.get(r[0])
        if n is None: problems.append("%s row lost: %r" % (t, r)); continue
        # An empty field getting its default (or main's own joined backfill) is not loss. A changed value is.
        diff = ["%s: %r -> %r" % (c, a, b) for c, a, b in zip(["rowid"] + snap["cols"], r, n)
                if a != b and a not in (None, "") and not (c == "joined" and a == 0)]
        if diff: problems.append("%s row %r changed: %s" % (t, r[0], "; ".join(diff)))
c = A.app.test_client()
with c.session_transaction() as s:
    s["mid"] = 2
page = c.get("/chat?c=team").get_data(as_text=True)
for body in ("legacy default channel hello", "legacy explicit team hello", "legacy null channel hello", "legacy empty channel hello"):
    if body not in page: problems.append("missing from #everyone: " + body)
if "coaches only note" in page: problems.append("coaches message leaked into #everyone")
if "everyone" not in page: problems.append("team chat is not labelled #everyone")
# USAWP numbers survive, and only someone without one is asked, and only for water polo
import flows2
with A.app.app_context():
    db = A.open_db()
    polo = db.execute("SELECT * FROM practices WHERE location='Old Pool'").fetchone()
    for email, asked in (("ada@example.com", False), ("ben@example.com", False), ("cy@example.com", True)):
        m = db.execute("SELECT * FROM members WHERE email=?", (email,)).fetchone()
        if ("number" in flows2.gate_needs(db, m, "2030-01-01", False, polo)) != asked:
            problems.append("USAWP prompt wrong for %s (expected asked=%s)" % (email, asked))
    db.execute("INSERT INTO practices(date,start,end,location,sport) VALUES('2030-01-09','07:00','08:00','Swim Pool','Swimming')")
    swim = db.execute("SELECT * FROM practices WHERE location='Swim Pool'").fetchone()
    cy = db.execute("SELECT * FROM members WHERE email='cy@example.com'").fetchone()
    if "number" in flows2.gate_needs(db, cy, "2030-01-01", False, swim):
        problems.append("a swim practice asked for a USAWP number")
print(json.dumps(problems))
'''


def _run(code, cwd, env):
    p = subprocess.run([PY, "-c", code], cwd=cwd, env=env, capture_output=True, text=True, timeout=300)
    assert p.returncode == 0, p.stderr[-3000:]
    return p.stdout.strip().splitlines()[-1]


def test_main_database_boots_on_branch_without_loss():
    main_dir = tempfile.mkdtemp()
    data = tempfile.mkdtemp()
    try:
        arch = subprocess.run(["git", "-C", HERE, "archive", "origin/main"], capture_output=True)
        assert arch.returncode == 0, "fetch origin/main first: git fetch --depth=1 origin +refs/heads/main:refs/remotes/origin/main"
        subprocess.run(["tar", "-x", "-C", main_dir], input=arch.stdout, check=True)
        env = dict(os.environ, DATA_DIR=data, DEV_SHOW_LINKS="0", ADMIN_EMAIL="ada@example.com")
        env.pop("GRUNIONS_DB", None); env.pop("GRUNIONS_UPLOADS", None)
        snap = os.path.join(data, "snap.json")
        open(snap, "w").write(_run(MAIN_SIDE, main_dir, env))
        env2 = dict(env, BRANCH_DIR=HERE, SNAP=snap)
        problems = json.loads(_run(BRANCH_SIDE, HERE, env2))
        assert problems == [], "\n".join(problems)
    finally:
        shutil.rmtree(main_dir, ignore_errors=True)
        shutil.rmtree(data, ignore_errors=True)
