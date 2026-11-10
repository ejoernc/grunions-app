# Email and website widget

Reuse what the app already stores and sends. HTML mail is on unless `HTML_EMAILS_ENABLED=0`. New public pages stay admin-only until a later phase turns them on.

## Already in the app

- `send_email` in `app.py` opens SMTP, uses implicit TLS on port 465 and STARTTLS otherwise, and sends one plain-text body. Certificate checks stay on.
- Three callers send mail today: the login link (`send_link`), a practice cancellation (`notify_practice_cancelled`), and expiry reminders (`deliver_expiry` for membership, SafeSport, background screening, and the trial).
- Practice reminders and RSVP changes are push notifications. There is no payment mail and no RSVP confirmation mail.
- People, practices, Lineup events, RSVPs, and login tokens already exist. A login link expires in 15 minutes and works once.
- Manage is `manage_home_groups`: Activities, People, and Club settings. Admins see Club settings. Coaches see Schedule, Lineup, and Requests.
- Visual tokens live in `regulars/foundation.css` (Space Grotesk, Plus Jakarta Sans, lime `#C4E65A`, 12px buttons, 16px and 20px corners). The corrected lockup is `static/regulars-lockup.svg`. Email uses `static/email-lockup.png`, the same mark with a dark wordmark so it reads on a white header.

## Phase 1

`mailhtml.py` is the generic design for every notification email, not a per-team settings screen. The layout is a lockup, lime eyebrow, headline, black button, optional WHEN/WHERE/STATUS card, optional security note, fallback link, and the footer “Sent by Regulars for [org].” plus the tagline. The org name is filled at send time (`ORG_NAME`, otherwise Grunions Water Polo).

HTML is on by default. Set `HTML_EMAILS_ENABLED=0` to send plain text only. Otherwise each existing send is `multipart/alternative`: the same plain text as before, plus the matching template.

- Login magic link uses the sign-in template.
- Practice cancellation uses the schedule-change template.
- Expiry reminders use the membership template, with the eyebrow set from the kind (membership, SafeSport, background screening, or free trial).

There is no Manage page and no `/admin/emails` page. `scripts/render_email_samples.py` writes samples locally and does not send them.

## Phase 2

`/manage/pricing` is under Club settings and is admin-only. It stores one program’s regular days, times, places, season dates, and public flag, plus any prices and the free-trial offer the admin actually enters.

Blank prices are not shown. The page does not invent a dollar amount, a venue, or a practice. Saving it writes `org_settings` only. Sessions are still created in Manage Schedule.

The free-trial block is one offer with two types. Duration is 7, 14, 30, or a custom number of days. Number of Sessions is 1, 2, 3, or a custom count. Grunions defaults to 14 days, water polo practices only, and a USA Water Polo trial membership. Scrimmages, games, and Lineup events stay off that offer unless an admin selects them. Saving still does not create practices or charge anyone.

A self-claim is `trial_acknowledged_at` plus an optional `trial_claim_until`. It is not verification. Coverage uses the existing `usawp_status`, `usawp_valid_until`, and `membership_type`, and it never runs past the verified USA Water Polo date. The public banner is generated from the type: a 14-day USAWP offer says “Try Water Polo Free for 2 Weeks”. A session offer says “Get N Free Practices”.

## Phase 3

`/manage/widget` is the next Club settings row. It is admin-only. The public page `/widget` and `/api/public/feed` answer 404 until Publish is on. Preview uses the admin’s login and does not publish the embed.

The feed is practices and published Lineup events only. Cards have a title, time, place, public note, and a price or trial line when one was entered. Names, photos, coach plans, and draft events are left out. A going count is a number, and only when that switch is on. The response is cached for about 30 seconds. The live widget lists every upcoming event. Events in preview is only the static preview on the admin page.

The iframe uses the app fonts and follows the visitor’s light or dark appearance with `prefers-color-scheme`. There is no Day/Night toggle. Chips are All, Schedule, Competitions, Camps, Trips, and Community. The schedule is a grid of `repeat(auto-fill, minmax(320px, 1fr))` and fills the container. Prices are shown as currency. The trial message is one callout above the grid, not a line on every card. Host CSS cannot style the frame. The embed snippet points at https://grunions.regulars.team/widget and does not change when settings change. Publish stays off until an admin turns it on.

## Phase 4

Sign up on a practice opens `/register?event=p-<id>` in the top window. The page asks the visitor to sign in or create an account, then checks the offer. A missing USA Water Polo trial stays on Pending verification. The athlete can submit a number and dates; that writes the claim and a verification request, and it does not mark `usawp_status` verified or change `usawp_valid_until`. Confirm adds a Going RSVP only when eligibility is Active and the activity is covered. A session offer holds a credit on that RSVP, uses it at check-in, and releases it if the RSVP or the session is cancelled. The page does not charge a card, start a trial on view, or send mail.
