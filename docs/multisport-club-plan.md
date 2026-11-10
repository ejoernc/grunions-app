# Multi-sport Club administration

Admin-only, under Manage → Club and Manage → People. Member home, the public widget, and existing RSVPs stay as they are. Schedule and Lineup stay one combined feed.

## Model

One club. A sport family can have several programs.

- `sport_families` — Water Polo; Swimming.
- `programs` — Water Polo (active), Pool Swimming (inactive), Open Water Swimming (inactive). `public_name` is the label already stored on sessions (`Water Polo`, `Swimming`). Turning a program off does not rewrite those rows.
- `program_schedules` — the regular-schedule template (weekdays, times, venue, notes, Pacific time). Saving it does not create sessions.
- `program_coaches` — who coaches that program. Tags also read coaches already assigned on sessions, without editing those sessions.
- `requirement_scopes` plus `requirement_programs` — a requirement applies only to the programs an admin checked. Activities and roles are optional. `review_status` is `active` or `needs_review`.
- `scope_reviews` — ambiguous legacy rules (anything that is not clearly SafeSport for Water Polo). They are not enforced.
- `plan_programs` — which programs a paid plan covers. Existing `payment_plans.sports` and Club Assistant URLs stay. Entitlements stay in `access_entitlements`.

Inactive programs do not contribute requirements to clearance, registration, Schedule, Lineup, or the widget. A valid USMS membership can still show a Swimming tag.

## Clearance vs payment

Clearance is per active program, activity, and role. SafeSport is scoped to Water Polo. USAWP stays on the member row. USMS stays on `external_memberships`. An unverified document does not clear someone. Paying does not satisfy USAWP or USMS.

Payment status comes from the latest manual entitlement: Paid (plan name), Trial, Drop-in, Expired, or Unpaid. The Paying / Not paying chip uses `replaceState`.

## Migration

Existing Water Polo and Swimming sports, prices, and Club Assistant links are kept. Swimming is the Pool Swimming program and starts inactive. Open Water Swimming is added inactive, with no enforced requirements until an admin turns it on. Practices and RSVPs are not updated. Sessions whose sport is Swimming stay on the combined Schedule.

## What this pass does not do

No per-program Schedule or Lineup pages. No Stripe. No member email. The widget stays unpublished and its layout is unchanged. Home sport chips stay hidden.
