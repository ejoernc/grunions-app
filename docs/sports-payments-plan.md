# Sports & Payments

One Club destination: **Sports & pricing** (`/manage/pricing`). It keeps the regular schedule, the prices the widget shows, and the free-trial offer. Sports, payment plans, providers, and paid memberships are sections of that same page. There is no second settings destination.

Paid access is not team membership, not a USA Water Polo record, and not an RSVP. Existing RSVPs are never rewritten. Going stays open until an admin turns on **Require payment access to RSVP**. That switch defaults to off. Stripe is listed as coming later and cannot be turned on. No card fields. No mail to members.

## Data model

`org_sports` — name, slug, active, archived, default, governing body (`usawp`, `usms`, or `none`), and the Schedule activity types that sport uses. Grunions seeds Water Polo (practice, scrimmage, game, USA Water Polo, default) and Swimming (practice, US Masters Swimming).

Practices already store `sport` and `activity_type`. Empty sports are Water Polo. A row whose title or note says swimming, and does not say water polo, is Swimming. RSVPs are not part of that backfill.

`payment_providers` — `external_link`, `manual`, `free`, and `stripe`. Stripe stays inactive. Every provider writes the same entitlement. Eligibility does not branch on the provider.

`payment_plans` — monthly, drop-in, pass, trial, or free. Each plan names eligible sports and activities, a provider, and an optional external URL. Introductory trial plans point at the existing trial offer. They do not start a second clock.

`payment_prices` — amount in cents and an effective date. The price on a day is the latest row whose date is on or before that day. Later rows are the next price, not a second plan.

`access_entitlements` — plan, provider, status (`active`, `pending`, `expired`, `inactive`), valid from, paid-through, last verified, verified by, notes, and an optional practice. Expiry is the date. There is no permanent paid flag.

`payment_records` — a manual or external record attached to a person, a plan, and optionally a practice. No card data.

`external_memberships` — governing-body rows for bodies other than USA Water Polo. USA Water Polo stays on `members.usawp_status`, `usawp_number`, `usawp_valid_until`, and `membership_type`. A claim is not verified.

`payment_settings` — one row. `require_rsvp` defaults to 0.

`access_audits` — who changed a paid membership, what changed, and when.

`payment_checks` — Phase 2. An athlete can say they paid. That inserts a pending check. It does not create an RSVP and it does not mark them paid.

## Grunions seed

Editable after it is created. Seeding runs only when `org_sports` is empty, so a later save is not overwritten.

- Monthly plan “Grunions Water Polo + Swim Membership”, Club Assistant, `https://www.clubassistant.com/club/clinics/reserve.cfm?c=2180&cid=103002`. $45 from 2026-12-01. $50 from 2027-01-01. Covers Water Polo and Swimming practices (and Water Polo scrimmages and games).
- Swimming drop-in $10, `https://www.clubassistant.com/club/clinics/reserve.cfm?c=2180&cid=92340`. Swimming practice only.
- No Water Polo drop-in. The Going flow says that option is not configured.

## Phases

Phase 1 stores the model, the Sports & pricing sections, and the paid-membership editor on each person. Going is unchanged.

Phase 2 reads the gate. When it is off, Going is the current RSVP. When it is on:

- A. Verified governing-body coverage and an active plan that includes the sport and activity: RSVP, no prompt.
- B. Verified governing body, no entitlement: show the configured options and open the external URL. No team join.
- C. Governing body missing or not verified: explain it and do not RSVP.
- D. The existing trial offer covers the activity and the athlete is eligible: RSVP with no payment prompt.
- E. Expired entitlement: show renewal and drop-in. Do not charge.

“I’ve completed payment” stores a pending check. An admin verifies it, which writes the entitlement and the audit. The RSVP is added only if the gate still passes and the practice still exists. A previous RSVP is left as it was.

Phase 3 adds Schedule chips for All, Swimming, and Water Polo only when more than one sport is active. Each card shows the sport and Going, Eligible to register, Payment required, or Verification required. A person who already has access does not see a payment prompt.
