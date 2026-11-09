# Email and website widget

Reuse what the app already stores and sends. New mail stays behind `HTML_EMAILS_ENABLED`, which defaults to off. New public pages stay admin-only until a later phase turns them on.

## Already in the app

- `send_email` in `app.py` opens SMTP, uses implicit TLS on port 465 and STARTTLS otherwise, and sends one plain-text body. Certificate checks stay on.
- Three callers send mail today: the login link (`send_link`), a practice cancellation (`notify_practice_cancelled`), and expiry reminders (`deliver_expiry` for membership, SafeSport, background screening, and the trial).
- Practice reminders and RSVP changes are push notifications. There is no payment mail and no RSVP confirmation mail.
- People, practices, Lineup events, RSVPs, and login tokens already exist. A login link expires in 15 minutes and works once.
- Manage is `manage_home_groups`: Activities, People, and Club settings. Admins see Club settings. Coaches see Schedule, Lineup, and Requests.
- Visual tokens live in `regulars/foundation.css` (Space Grotesk, Plus Jakarta Sans, lime `#C4E65A`, 12px buttons, 16px and 20px corners). The corrected lockup is `static/regulars-lockup.svg`. Email uses `static/email-lockup.png`, the same mark with a dark wordmark so it reads on a white header.

## Phase 1

`mailhtml.py` builds one table layout: lockup, lime eyebrow, headline, black button, optional WHEN/WHERE/STATUS card, optional security note, fallback link, and the footer “Sent by Regulars for Grunions Water Polo.” plus the tagline. Plain text is unchanged. HTML is attached as `multipart/alternative` only when `HTML_EMAILS_ENABLED=1`. Admins preview samples at `/manage/emails`, a Club settings row. Previews are not delivered.

## Later phases

- Phase 2 stores the public schedule, prices, and free-trial rules. Nothing is invented when a price is unset.
- Phase 3 adds a read-only public feed and the embed, plus a Website Widget page under Club settings. Visitors do not see names, photos, or private notes.
- Phase 4 reuses the existing login and RSVP. Going in the widget opens that flow and does not mark anyone as registered until it finishes.
