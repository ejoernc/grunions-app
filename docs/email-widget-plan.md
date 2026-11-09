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

A first-time trial cannot be claimed again after `trial_acknowledged_at` is set. That is the same acknowledgment the membership card already stores.

## Phase 3

`/manage/widget` is the next Club settings row. It is admin-only. The public page `/widget` and `/api/public/feed` answer 404 until Publish is on. Preview uses the admin’s login and does not publish the embed.

The feed is practices and published Lineup events only. Cards have a title, time, place, public note, and a price or trial line when one was entered. Names, photos, coach plans, and draft events are left out. A going count is a number, and only when that switch is on. The response is cached for about 30 seconds and capped at 40 cards.

The iframe uses the app fonts, Night or Day, and the chips All, Schedule, Competitions, Camps, Trips, and Community. Prices are shown as currency. The trial message is one callout, not a line on every card. Host CSS cannot style the frame. The embed snippet points at https://grunions.regulars.team/widget and does not change when settings change.

## Later phases

- Phase 4 reuses the existing login and RSVP. Going in the widget opens that flow and does not mark anyone as registered until it finishes.
