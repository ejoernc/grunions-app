# Regulars 2.0: flows to build, and where the branch stood (Nov 12)

Source of truth: Figma file `X1hA7Tpq3qoRN9fKMPEw3R` (Regulars 2.0). Build from the **workflow pages**:
12 Member (`2003:63187`), 13 Coach (`2003:63188`), 14 Admin (`2003:63189`), plus 15 Map (`429:3387`).
Each step names a screen number (for example 05.15). Build that screen from its area page, then wire it to the next step.
Visual polish on one frame doesn't count as done until the step it belongs to works end to end with real data.

**Rule for agents:** if a screen exists but the action behind it is fake ("Preview only", hardcoded names or places, a sheet that sends nothing), that step is NOT done. Build the backend first.

## Decided (Nov 11). Don't contradict these.
- Waiver = checkbox + typed full name, stored with time and waiver version. Re-sign when the version changes.
- Insurance (USAWP / USMS number) is manual in v1: the member enters it, and a coach or admin verifies or rejects it with an expiry date. No API.
- No Stripe. Plans have a payment LINK (Membership, Drop-in, Practice pass). "Paying member" is an on/off flag the board sets by hand. Paying members tap Going with no payment step. Everyone else gets "Before you go": free trial if unused, drop-in, pass, membership. Drop-in and pass only record the pick, which shows at check-in.
- Trial is per club: N days OR N practices ("5 days left" / "2 practices left").
- Adults only. Date of birth is checked at join. Under 18 can't join.
- Team chat is members-only. Visitors see "Join to chat with the team" at most.
- Only coaches and admins create practices, scrimmages and games. Members suggest Lineup events, and a coach or admin approves them.
- Location privacy: exact location only for a driver who agreed to pick someone up, only to their riders, only during the pickup window. Everyone else is an approximate area. Never show home addresses.
- Roles are per team.

## Gap list (ranked) and what was done on Nov 12

| # | Flow step | Branch on Nov 12 | Status |
|---|---|---|---|
| 1 | Member 07–09 · Going → one-sheet gate (05.15): insurance # + waiver, trial link, then "You're going" | Going just RSVPs. `drop_club_waiver()` deleted the waiver requirement on every boot (on `main` too). No waiver acceptance was stored. | **Done.** `club_waiver` (versioned, URL or text) + `waiver_acceptances` (typed name, time, version, practice). Going → `/practices/<id>/signup` when a number or waiver is missing. The RSVP JS now follows that redirect instead of faking Going. Admin: Manage › Club › Waiver. |
| 2 | Member · "Before you go" for non-paying members | `sportspay.decide` + `/participate` exist, behind the "require payment on Going" toggle. The JS RSVP swallowed that redirect too. | **Fixed:** the redirect is followed now. Copy and design still need to match 05.x "Before you go". |
| 3 | Member 10–11 · Ask for a ride → matched driver | Hardcoded mock ("Home · Belmont Shore", "Preview only"). Offer said "not in this pass". | **Done.** `ride_requests` / `ride_offers`. Areas only (street addresses refused). Driver picks a rider, seats are capped, and the driver adds a pickup spot that only that rider sees, only from 3h before to 1h after. Pushes for new request, pickup, cancel. Not going cancels or reopens rides. Practice page only for now; the Schedule-home sheet is still the old mock. |
| 4 | Member 01–06 · Join: DOB 18+, teams, week, notifications, Finish setup | No DOB, no steps | **Done:** DOB required, under 18 refused and nothing stored; join → Your week (10.31) → Schedule; Finish setup card (Teams · Account · Your week · Notifications) on Schedule home. **Not done:** team picker (10.30), notification pre-ask screen (06.17). |
| 5 | Coach 03 · Check-in Hold + walk-in | No Hold | **Done:** reason line (Not cleared · USAWP missing / Waiver not signed yet) + Hold button with confirm; Walk-in QR + Wrap up buttons on check-in. |
| 6 | Coach 05 · Wrap up | Missing | **Done:** `/practices/<id>/wrap` with attended / no-show / walk-in, private admin note, recap to practice chat, Close. |
| 7 | Admin 10–11 · Mark paid, per-team role | Entitlements exist in sportspay | Check the Person page against 08.06 |
| 8 | Admin 01–05 · Bring your club wizard | Pieces exist separately | Next |
| 9 | Member 12–13 · Leave-by push, Go now | Traffic chip only | Next |
| 10 | Coach 01 · Coach home (08.08) with going / not cleared / first-timers | Missing | Next |
| 11 | Admin 07–08 · Suggestion → Approve & post | `/manage/requests` exists | Verify end to end |

## Data that must survive
Production is SQLite on the Render disk (`/data/grunions.db`). Schema changes must be additive (`CREATE TABLE IF NOT EXISTS`, `ADD COLUMN`). Never delete rows on boot. `drop_club_waiver()` was removed for this reason.
