"""Daily job: print USAWP expiry report (expired / next 7 / next N days). Wire the output to email later.
Usage: .venv/bin/python daily_expiry.py [--days 30] [--remind]   (--remind posts in-app reminders to those members)
cron: 0 8 * * * cd /workspace/grunions-checkin && .venv/bin/python daily_expiry.py --remind >> expiry.log"""
import sys, sqlite3, app as A
days = int(sys.argv[sys.argv.index("--days") + 1]) if "--days" in sys.argv else A.EXPIRING_DAYS
d = sqlite3.connect(A.DB); d.row_factory = sqlite3.Row; d.executescript(A.SCHEMA); A.expire_sweep(d)
rep = A.expiry_report(d, days)
print(f"Grunions USAWP expiry report {A.today_pt()} (window {days}d)")
for k, v in rep.items():
    print(f"\n{k}: {len(v)}")
    for r in v: print(f"  [{r['item']}] {A.display_first(r)} {r['last']} <{r['email']}> {r['usawp_valid_until']} ({r['days_left']}d)")
if "--remind" in sys.argv:
    n = 0
    for v in rep.values():
        for r in v: A.remind(d, r["id"], by="automatic reminder"); n += 1
    d.commit(); print(f"\nPosted {n} in-app reminders")
