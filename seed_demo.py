"""Seed demo data into grunions.db (local prototype only)."""
import os; os.environ.setdefault("ADMIN_EMAIL", "eli@example.com"); os.environ.setdefault("DEV_SHOW_LINKS", "1")
import re, app as A
c = A.app.test_client()
def tok(cl, p): return re.search(r'(?:name=csrf value=|const CSRF=)"([^"]+)"', cl.get(p).get_data(as_text=True)).group(1)
people = [("Eli","Joern","eli@example.com"),("Jane","Doe","jane@example.com"),("John","Smith","john@example.com"),("Ana","Lopez","ana@example.com"),("Marcus","Lee","marcus@example.com")]
cl = {}
for f,l,e in people:
    x = A.app.test_client(); x.post("/join", data=dict(csrf=tok(x,"/join"), first=f, last=l, email=e, phone="714-555-0100")); cl[f]=x
E = cl["Eli"]; t = tok(E, "/admin")
with open("sample_sport80_export.csv","rb") as fh: E.post("/import", data=dict(csrf=t, file=(fh,"s.csv")), content_type="multipart/form-data")
for mid in (1,2,4,5): E.post("/admin", data=dict(csrf=t, member_id=mid, date="2026-10-20"))
for mid in (1,2,3): E.post("/admin", data=dict(csrf=t, member_id=mid, date="2026-10-16"))
def say(who, body, ann=False): cl[who].post("/api/messages", json={"body": body, "announcement": ann}, headers={"X-CSRF": tok(cl[who], "/chat")})
say("Jane","Anyone carpooling to Marina on Tuesday?"); say("Marcus","I can take 2 from Fountain Valley 🚗")
say("Eli","Starting in November, membership is $45/mo and covers all practices (Tue Marina HS + Fri Westminster HS). October is still free!", True)
say("John","Is the Friday practice still at Westminster?"); say("Eli","Yep, Fridays 7–8:30 at Westminster HS. Bring dark + white caps.")
print("seeded")
import sqlite3, datetime as dt
D = sqlite3.connect(A.DB); today = A.today_pt()
D.execute("UPDATE members SET role='coach' WHERE first='Marcus'")
D.execute("UPDATE members SET usawp_status='verified', usawp_valid_until=?, usawp_number='2223334' WHERE first='Eli'", ((today+dt.timedelta(days=12)).isoformat(),))
for mid, rid, done, exp in [(1,1,"2026-02-01","2027-02-01"),(1,3,"2026-09-01",None),(2,3,"2026-09-15",None),(5,1,"2026-03-01","2027-03-01"),(5,2,"2026-03-01","2028-03-01")]:
    D.execute("INSERT OR REPLACE INTO member_reqs VALUES(?,?,?,?,'manual','Eli Joern',?)", (mid, rid, done, exp, today.isoformat()))
D.commit()
cl["Marcus"].get("/practices")
pid = D.execute("SELECT id FROM practices WHERE date>=? AND location='Marina High School' ORDER BY date LIMIT 1", (today.isoformat(),)).fetchone()[0]
for who, a in [("Jane","going"),("Marcus","going"),("Ana","going"),("John","notgoing")]: cl[who].post("/practices", data=dict(csrf=tok(cl[who],"/practices"), pid=pid, action=a))
cl["Marcus"].post("/api/messages?c=coaches", json={"body": "Coaches: let's run 6-on-5 drills Tuesday. Ana still needs SafeSport before she can scrimmage."}, headers={"X-CSRF": tok(cl["Marcus"], "/chat")})
print("seeded extras, Marina practice id", pid)
