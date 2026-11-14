"""Merge safety, wider: main's lineup events and signups, USAWP numbers and verification, requirements,
series, past practices and check-ins all come through, and the main pages load for those members."""
import os, sys, json, subprocess, tempfile, shutil
HERE=os.path.dirname(os.path.abspath(__file__)); PY=sys.executable
sys.path.insert(0, HERE)
import test_upgrade as T
SEED = r'''
c.execute("UPDATE members SET usawp_status='verified', usawp_valid_until='2031-08-31', usawp_verified_by='Ada Old', usawp_verified_at='2026-10-01T10:00', sport80_contact_id='S80-1', membership_type='Individual', usawp_updated='2026-10-01' WHERE email='ada@example.com'")
c.execute("UPDATE members SET trial_acknowledged_at='2026-11-10T09:00:00' WHERE email='cy@example.com'")
c.execute("INSERT INTO requirements(name,applies_to,keywords,expires) VALUES('SafeSport','coach','safesport',1)")
rq = c.lastrowid
c.execute("INSERT INTO member_reqs(member_id,req_id,completed_on,expires_on,source,by,at) VALUES(1,?,'2026-01-05','2027-01-05','manual','Ada Old','2026-01-05')", (rq,))
c.execute("INSERT INTO verify_requests(member_id,name,email,member_number,requested_by,member_submitted,status,created) VALUES(2,'Ben Old','ben@example.com','7654321','Ben Old',1,'pending','2026-11-01')")
c.execute("INSERT INTO usawp_submits(member_id,at) VALUES(2,'2026-11-01')")
c.execute("""INSERT INTO lineup_events(kind,title,date,end_date,city,venue,start,description,stage,hosting,status,official,team_intent,event_type,created_by,capacity,cost,host_org,date_precision)
  VALUES('Tournament','IGLA 2031','2031-06-10','2031-06-14','Long Beach','Belmont Plaza','09:00','Big one','going','Attending','published',1,'official','Tournament',1,20,'$80','IGLA','exact')""")
e1 = c.lastrowid
c.execute("""INSERT INTO lineup_events(kind,title,date,city,venue,start,description,stage,hosting,status,official,event_type,created_by,date_precision)
  VALUES('Social','Holiday party','2031-12-12','Long Beach','Harp','19:00','Party','attending','Hosting','published',1,'Social',1,'exact')""")
e2 = c.lastrowid
c.execute("INSERT INTO lineup_rsvps(event_id,member_id,going,state) VALUES(?,1,1,'going')", (e1,))
c.execute("INSERT INTO lineup_rsvps(event_id,member_id,going,state) VALUES(?,2,0,'interested')", (e1,))
c.execute("INSERT INTO lineup_rsvps(event_id,member_id,going,state) VALUES(?,2,1,'going')", (e2,))
c.execute("INSERT INTO practice_series(weekdays,start,end,location,start_date,end_date,interval_weeks,activity_type,sport) VALUES('1','19:00','20:30','Series Pool','2031-01-06','2031-03-31',1,'practice','Water Polo')")
sid = c.lastrowid
c.execute("INSERT INTO series_coaches(series_id,member_id,is_lead) VALUES(?,1,1)", (sid,))
c.execute("INSERT INTO practices(date,start,end,location,series_id,activity_type,sport) VALUES('2031-01-07','19:00','20:30','Series Pool',?,'practice','Water Polo')", (sid,))
sp = c.lastrowid
c.execute("INSERT INTO practice_coaches(practice_id,member_id) VALUES(?,1)", (sp,))
c.execute("INSERT INTO rsvps(practice_id,member_id,going) VALUES(?,2,1)", (sp,))
c.execute("INSERT INTO practices(date,start,end,location,activity_type,sport) VALUES('2025-06-01','19:00','20:30','Past Pool','practice','Water Polo')")
pp = c.lastrowid
c.execute("INSERT INTO rsvps(practice_id,member_id,going) VALUES(?,2,1)", (pp,))
c.execute("INSERT INTO checkins(member_id,practice_date,location) VALUES(2,'2025-06-01','Past Pool')")
'''
main_side = T.MAIN_SIDE.replace("d.commit()\nout = {}", SEED + "d.commit()\nout = {}", 1)
assert SEED in main_side
CHECK = r'''
# pages render with the old data
def as_(mid):
    cl = A.app.test_client()
    with cl.session_transaction() as s: s["mid"] = mid
    return cl
ada, ben = as_(1), as_(2)
for pth in ("/lineup","/lineup/1","/profile","/members","/practices","/home","/chat","/admin"):
    r = (ada if pth in ("/profile","/members","/admin") else ben).get(pth)
    if r.status_code >= 400: problems.append("%s returned %s" % (pth, r.status_code))
lu = ben.get("/lineup").get_data(as_text=True)
for t in ("IGLA 2031", "Holiday party"):
    if t not in lu: problems.append("lineup missing " + t)
ev = ada.get("/lineup/1").get_data(as_text=True)
if "IGLA 2031" not in ev: problems.append("lineup event page")
prof = ada.get("/profile").get_data(as_text=True)
if "1234567" not in prof: problems.append("Ada USAWP number not on profile")
ppl = ada.get("/members").get_data(as_text=True)
if "Ben" not in ppl: problems.append("people list")
sp = ada.get("/practices/%d" % d.execute("SELECT id FROM practices WHERE location='Series Pool'").fetchone()[0]).get_data(as_text=True)
if "Series Pool" not in sp: problems.append("series practice page")
ck = ada.get("/admin?date=2025-06-01").get_data(as_text=True)
if "Ben Old" not in ck: problems.append("past check-in: Ben not listed")
if ("In · 1" not in ck) and ("1 of 1" not in ck): problems.append("past check-in count missing: " + str([x for x in ["In · ", "of 1"] if x in ck]))
past = ben.get("/practices?view=list&when=past").get_data(as_text=True)
if "Past Pool" not in past: problems.append("Ben's past list missing Past Pool")
evp = ada.get("/lineup/1").get_data(as_text=True)
if "Ada Old" not in evp and "01" not in evp: problems.append("lineup going count/people")
csv = ada.get("/export/practices.csv?start=2025-01-01&end=2031-12-31")
if csv.status_code != 200 or "Past Pool" not in csv.get_data(as_text=True): problems.append("practices CSV lost Past Pool")
if d.execute("SELECT stage, hosting FROM lineup_events ORDER BY id").fetchall() != [("going", "Attending"), ("attending", "Hosting")]: problems.append("lineup stage/hosting changed")
print(json.dumps(problems))
'''
branch_side = T.BRANCH_SIDE.replace("print(json.dumps(problems))", CHECK, 1)


def test_main_data_shows_up_on_branch_pages():
    main_dir, data = tempfile.mkdtemp(), tempfile.mkdtemp()
    arch = subprocess.run(["git", "-C", HERE, "archive", "origin/main"], capture_output=True)
    subprocess.run(["tar", "-x", "-C", main_dir], input=arch.stdout, check=True)
    env = dict(os.environ, DATA_DIR=data, DEV_SHOW_LINKS="0", ADMIN_EMAIL="ada@example.com"); env.pop("GRUNIONS_DB", None)
    snap = os.path.join(data, "snap.json")
    p = subprocess.run([PY, "-c", main_side], cwd=main_dir, env=env, capture_output=True, text=True)
    assert p.returncode == 0, p.stderr[-2000:]
    open(snap, "w").write(p.stdout.strip().splitlines()[-1])
    p = subprocess.run([PY, "-c", branch_side], cwd=HERE, env=dict(env, BRANCH_DIR=HERE, SNAP=snap), capture_output=True, text=True)
    assert p.returncode == 0, p.stderr[-3000:]
    problems = json.loads(p.stdout.strip().splitlines()[-1])
    shutil.rmtree(main_dir, ignore_errors=True); shutil.rmtree(data, ignore_errors=True)
    assert problems == [], "\n".join(problems)

