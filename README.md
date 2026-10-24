# Grunions Water Polo team app
Flask + SQLite. Dark, mobile-first. Runs locally or on Render/any Docker host (see Deploy).

## Run
    ./run.sh    # reads .env.local (BOT_API_KEY, SECRET_KEY, ADMIN_EMAIL, optional VERIFY_WEBHOOK_URL); port 5055
or:
    python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
    ADMIN_EMAIL=you@yourmail.com SECRET_KEY=$(openssl rand -hex 32) .venv/bin/python app.py   # http://localhost:5055
Env: PUBLIC_URL (base URL for QR + login links), EXPIRING_DAYS (default 30), CRON_KEY (lets a scheduler call /api/expiring?key=...),
DEV_SHOW_LINKS=1 (local testing only: show magic link on screen; default 0), SECURE_COOKIES=1 (behind HTTPS), GRUNIONS_DB, PORT.
Demo data: `rm grunions.db && .venv/bin/python seed_demo.py` (admin eli@example.com, coach marcus@example.com).
Tests: `.venv/bin/python test_app.py` (215 checks) and `.venv/bin/python -m pytest -q test_v2.py` (16 tests), `.venv/bin/python -m pytest -q test_google.py` (8 tests). Run each in its own process, or just `./run_tests.sh`. Daily job: `.venv/bin/python daily_expiry.py [--days 30] [--remind]`.

## Roles
member (athlete), coach (check-in + #coaches), admin (everything). Manage on Admin → **Roles** (/admins): every member with Make/Remove admin and Make/Remove coach. The last admin can't be removed. Admins always have full access.
The coaching list is separate from coach access. A verified USAWP membership type with the word coach (for example Individual Membership, Coach) adds that person automatically. Admins can also use Add to coaching list and Remove from coaching list. Being on the list does not open check-in or coaches chat. Only Make coach does that, and Remove coach takes it away. Edit practice offers a checkbox for each person on the list. A USAWP coach badge shows when they are on the list because of that coach membership and both background screening and SafeSport are current.
ADMIN_EMAIL (comma-separated) bootstraps admins and keeps them admin on every start; remove an address there to demote it.

## Pages
- /join: QR target, creates the account and logs in. Optional preferred first name (blank uses the legal first name). /login: one-time magic link (LINK_MINUTES, default 15; single use, stored hashed), emailed via SMTP. The greeting uses the preferred first name when set.
- /home: Cleared to play card (membership + each required item), USAWP status, expiry warning, reminders, next practice, attendance, profile (legal name, and an editable preferred first name).
  Until a member is verified, the card includes an inline USAWP Membership # form (digits, 4-10). Add saves the number, opens a pending verification request, and shows a toast, "Sent to Grunions for verification", for about 3 seconds. The input is then replaced by the saved number (USAWP # 1234567) and an Edit button. Edit reveals the prefilled input; saving updates the number, re-sends that pending request's webhook, and shows the toast again. While a request is pending the card title is "Verification pending" with an amber Pending badge. After the bot answers, the card returns to Cleared (green) or Not cleared (red). Once verified, Edit is hidden and the number stays read-only. Three submissions per member per hour. When that membership date has passed, the card returns to Not cleared with "Membership expired 2026-10-22" and a primary Reverify membership button. It reveals the prefilled number; Send starts a new verification request, shows the toast, and the card goes to Pending. An expired SafeSport date shows "SafeSport expired 2026-01-01" and Not cleared.
  With no membership number saved, a secondary **2-week USAWP trial** button sits next to that entry. It opens an acknowledgment: "I will complete the USA Water Polo 2-week trial membership before I get in the pool. I understand I need to get a full USAWP membership soon, otherwise I will not be able to practice." **I confirm** stores `trial_acknowledged_at`. The card then counts as cleared: a green **Trial · 14 days left** badge (on the last day, **Last day of trial**) and **Ends Nov 6**. **Get USAWP trial membership** opens the official registration widget, https://usawp.sport80.com/public/widget/1, in a new tab. The button is hidden once a number is entered or the trial has been acknowledged. During the trial the same Membership # form still sends the number for verification and the card shows Pending. Once verified, the normal Cleared or Not cleared card replaces the trial. After the end date the badge returns to Not cleared and the card says **Trial ended Nov 6**.
- /practices: recurring Tue 7–8:30 Marina HS / Fri 7–8:30 Westminster HS (next 4 weeks auto-created); Going / Not going, headcount, who's coming. Admin add/edit/cancel/restore. Edit practice lists everyone on the coaching list as a checkbox, and several can be checked. The schedule card and the next-practice card show the assigned coaches to every member, for example Coaches: Eli, Sam. Someone who leaves the list disappears from that line. Dates, expiry, and practice times use Pacific time (America/Los_Angeles). A practice stays on the schedule until its end time, so Friday's 7–8:30 practice is still there after 5pm. A cancellation or a change to the time, place, or note shows a red count on the Schedule tab and a red bubble on that practice until the member opens it.
- /chat: #team (everyone) and 🔒 #coaches (coaches + admins). Polls every 3 s. Press and hold a message, or right-click it, to open actions (on a desktop with a mouse, the same menu is on the hover ⋯). The sheet offers 👍 ❤️ 😂 😮 🎉 🙏 and a few more; reactions already on a message show as small pills underneath, and tapping a pill toggles yours. Edit is only on your own message and saves inline, then the message shows (edited). Delete asks "Delete this message?" and then leaves the row as "Message deleted". You can delete your own messages. An admin can delete anyone's message in team chat and in coaches chat. A coach who is not an admin cannot. The composer has an image button and a send icon; announcements already stored still show on Home, and a deleted announcement does not. Unread messages show a red count on the Chat tab, and on the Team and Coaches tabs. Opening a channel marks it read.
- /admin (staff): check-in by date. Going lists who RSVP'd and is not checked in yet, A–Z by display name. Everyone else not checked in is the next list, also A–Z. Checked in is a collapsible section at the bottom with a count. Each row keeps its clearance badge. A current USAWP coach also shows a USAWP coach badge on check-in, on the member roster, on Roles, and on that member's home card. An active 2-week trial shows the days left and end date on check-in and on the member roster; a trial that has ended is marked Trial ended.
  Admin "Verify" panel: open Sport:80 (name copied to clipboard), Mark membership verified (member #, expires on; records admin + time),
  enter compliance items (completed / expires), set role.
- /members (admin, +CSV), /export (admin): members CSV, and practices/attendance CSV for a start and end date. Practices is one row per practice (RSVP going and checked-in counts). Detailed attendance is one row per member per practice (name, USAWP #, RSVP, checked in, check-in time). Files are UTF-8 with a BOM so Excel opens them, and the filename includes the date or date range. /import (Sport:80 .xlsx/.csv incl. SafeSport/Background columns), /qr, /expiring (expired / 7 days / N days, incl. compliance items; in-app reminders), /requirements (configure items, who they apply to, import keywords).
Status auto-flips to expired once expires_on passes. Cleared = USAWP membership verified and current, and SafeSport current, or an active 2-week USAWP trial that is not yet verified. Club waiver is not a requirement.
- /notifications: per-type push toggles, all on until changed. Team chat, coaches chat (coaches and admins), a practice reminder about 3 hours before for anyone who RSVP'd going, verification result, practice cancelled, trial / membership / SafeSport expiring or expired, and (admins) new verification requests. Home shows **Allow notifications**. On iPhone or iPad, add Grunions to the Home Screen first (iOS 16.4 or later), then open it from there. Reminder emails (7 days before, 1 day before, and the day it expires) can be turned off here. Practice cancellation emails always send, with the date, time, and location. Each notice is stored so it is not sent twice. An in-process scheduler runs the expiry and reminder checks about every 15 minutes (one scheduler per process, plus a database lock). No extra Render service.
Security: CSRF on every POST and DELETE, HttpOnly SameSite cookies, chat escaped, role checks server-side.
Before production: SMTP configured, DEV_SHOW_LINKS=0, HTTPS, DB backups (copy $DATA_DIR/grunions.db). v1 kept as app_v1_checkin.py.

## UI
Templates live in ui.py (restrained dark theme: one surface, gray text, blue only for primary actions and the active tab, status shown as a small dot + label).
Tabs: Home, Schedule, Chat, plus Admin for coaches/admins (Check-in · Members · Expiring · Import · Rules · QR). The bar is the same markup on every page, 64px tall, with inline icons. Switching tabs replaces the page content and leaves the bar mounted. The document background is #0a0a0b from the first bytes, and a full load keeps the bar still with a view transition. Chat and Schedule show a red unread count. The home-screen icon uses the Badging API (`setAppBadge` / `clearAppBadge`, including from the service worker when a push arrives) for the same total. Tap a name on check-in to open its details panel.

## Verification bot API
- Home form or admin "Ask Grunions to verify" creates a verify_requests row (pending). The Home form, if one is already pending, updates that row's member_number instead of inserting another. Admin "Ask Grunions to verify" does not create a duplicate while one is pending.
- Whenever a verify request is created, if VERIFY_WEBHOOK_URL is set, POSTs this JSON (5 s timeout). Failures are logged only and never break the page:
  `{"request_id": 12, "member_id": 4, "name": "Ana Lopez", "preferred_first": "Ana", "email": "ana@example.com", "member_number": "5555555", "requested_by": "Eli Joern", "app_url": "https://grunions.example"}`
  `app_url` is PUBLIC_URL. `member_number` and `requested_by` are stored on the request. If VERIFY_WEBHOOK_KEY is set, the POST sends `Authorization: Bearer <key>`. If VERIFY_WEBHOOK_HEADER is set, that name is used instead and the value is the raw key (no Bearer prefix).
- Auth: `Authorization: Bearer $BOT_API_KEY` (401 otherwise; API disabled if unset).
- GET /api/verify-requests?status=pending|done → list.
- POST /api/verify-requests/<id>/result  {"verified":true,"member_number":"123","membership_expires_on":"2027-08-31",
  "membership_type":"Individual Membership, Coach","compliance":{"SafeSport training":"2027-05-01"},"note":"..."} → updates member + compliance (matched by requirement name or keyword),
  marks done (409 if already answered) and posts an in-app notice to every admin. It does not post to chat. The member's card updates, and they get the verification-result push when that notification is on.
  When verified is true and membership_type contains the word coach, the member is added to the coaching list. That does not grant coach access. A verified result whose membership type is not a coach membership removes only a USAWP-sourced list row. A failed result, or a result with no membership_type, leaves the list unchanged. Mark membership verified does not set a membership type and does not change the list.

## Environment variables
| Var | Needed | Purpose |
|---|---|---|
| SECRET_KEY | prod | session signing (random 64 hex). |
| ADMIN_EMAIL | yes | bootstrap admin(s), comma-separated, e.g. `elliott.joern@gmail.com`. |
| PUBLIC_URL | prod | e.g. `https://grunions.onrender.com`; used in login links + QR. If it starts with https, secure cookies and proxy headers are on. |
| DATA_DIR | prod | folder for `grunions.db` and `uploads/` (Render disk: `/data`). Defaults to the app folder. GRUNIONS_DB / GRUNIONS_UPLOADS override individually. |
| SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASSWORD, MAIL_FROM | prod | login emails, practice-cancellation emails, and expiry reminder emails. All five must be set. Port 465 = SSL, other ports = STARTTLS. |
| VAPID_PUBLIC_KEY, VAPID_PRIVATE_KEY | no | Web Push keys. If either private key is missing, a key pair is generated at startup and saved in DATA_DIR (`vapid_private.pem`, `vapid_public.txt`). |
| GRUNIONS_SCHEDULER | no | `0` turns off the in-process reminder scheduler. Default on. |
| DEV_SHOW_LINKS | local | `1` shows the login link on screen. Never in production. |
| GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET | no | enable Sign in with Google (button appears only when both are set). |
| LINK_MINUTES | no | login link lifetime (default 15). |
| SECURE_COOKIES / BEHIND_PROXY | no | force `1`/`0`; default on when PUBLIC_URL is https. |
| VERIFY_WEBHOOK_URL | no | POST target when a verify request is created. JSON keys: request_id, member_id, name (legal), preferred_first, email, member_number, requested_by, app_url (PUBLIC_URL). 5 s timeout. |
| VERIFY_WEBHOOK_KEY | no | If set, sent as `Authorization: Bearer <key>` on that POST. |
| VERIFY_WEBHOOK_HEADER | no | Optional header name. When set, the raw key is that header's value (no Bearer prefix). |
| BOT_API_KEY, CRON_KEY, EXPIRING_DAYS, PORT | no | see below. |

SMTP examples: **Gmail** `smtp.gmail.com`, 587, your Gmail address, a 16-char App Password (needs 2-Step Verification), MAIL_FROM `Grunions Water Polo <you@gmail.com>`.
**Resend** `smtp.resend.com`, 465, user `resend`, password = API key, MAIL_FROM on a verified domain. **Brevo** `smtp-relay.brevo.com`, 587, SMTP login + SMTP key.

## Deploy (Render)
`render.yaml` defines a Docker web service (gunicorn, 1 worker x 8 threads since SQLite) with a 1 GB persistent disk at `/data` (`DATA_DIR=/data`).
New → Blueprint → point at the repo, then fill PUBLIC_URL and the SMTP_* values. Other hosts: `docker build -t grunions . && docker run -p 10000:10000 -v grunions-data:/data --env-file prod.env grunions`.
Without Docker: `gunicorn app:app --bind 0.0.0.0:$PORT --workers 1 --threads 8`.

## Start clean (real data)
`python reset_real.py` (type RESET, or `--yes`) wipes members, chat, reactions, check-ins, RSVPs, verify requests, notices, login tokens, membership-number submissions and uploads.
Keeps schema, requirements and the real practices (Tue 7–8:30 PM Marina High School, 15871 Springdale St, Huntington Beach; Fri 7–8:30 PM Westminster High School),
and re-creates Elliott Joern (elliott.joern@gmail.com, USAWP #659226, membership thru 2027-06-07, SafeSport thru 2027-05-11, background thru 2028-08-28) as verified admin + coach, on the coaching list because his USAWP membership type is Individual Membership, Coach.
Back up grunions.db first. It acts on whatever DATA_DIR/GRUNIONS_DB points at.

## Sport:80 roster import columns
/import takes .csv or .xlsx (title rows above the header are skipped; headers matched case/space/punctuation-insensitively):
- **First Name / Last Name** (or Name / Full Name), **Email / Email Address** — matching (email first, then unique legal first+last). Optional **Preferred First Name / Nickname** is stored as the name shown in the app and is not used to match.
- **ID Number / Member Number / Membership Number** — stored as USAWP #. **Contact ID** — stored as sport80_contact_id.
- **Status / Membership Status** and **Valid Until / Expiry Date / Membership Expiry Date** — status. If there's no status column, a future expiry counts as current.
- **Membership Type / Member Type** — stored on the member. A value with the word coach (not coaches or coaching) adds them to the coaching list. Any other value removes only a USAWP-sourced list row.
- Any column containing a requirement keyword (safesport, background, concussion; editable in Rules) plus expiry/valid through/completed/status updates that item. A Club waiver column is ignored.
A file needs a name or email column plus at least one of status, member number, or expiry.

## Sign in with Google
OpenID Connect via Authlib (state + nonce, ID token checked). Requires `email_verified`. Matches an existing member by email (case-insensitive);
otherwise creates the account just like /join (open signup; phone left blank). Admin is never granted by Google sign-in, only via ADMIN_EMAIL or the Roles page.
Redirect URI: `PUBLIC_URL + /auth/google/callback`, e.g. `https://grunions-team-app.onrender.com/auth/google/callback`
(locally without PUBLIC_URL: `http://localhost:5055/auth/google/callback`).

Google Cloud Console setup:
1. https://console.cloud.google.com → project picker → **New project** (e.g. "Grunions") → select it.
2. **APIs & Services → OAuth consent screen** (Google Auth Platform → Branding/Audience): User type **External** → app name "Grunions Water Polo", support email, developer contact email → Save.
   Scopes: add `openid`, `.../auth/userinfo.email`, `.../auth/userinfo.profile` (non-sensitive, no verification review needed).
3. **Audience → Publish app** (move from Testing to **In production**) so any Google account can sign in. In Testing, only listed test users can.
4. **APIs & Services → Credentials → Create credentials → OAuth client ID** → Application type **Web application**, name "Grunions web".
   - Authorized JavaScript origins: `https://YOUR-DOMAIN` (and `http://localhost:5055` for local testing).
   - Authorized redirect URIs: `https://YOUR-DOMAIN/auth/google/callback` (and `http://localhost:5055/auth/google/callback`). Must match exactly: scheme, host, no trailing slash.
5. Create → copy the **Client ID** and **Client secret** into GOOGLE_CLIENT_ID / GOOGLE_CLIENT_SECRET (Render dashboard → Environment, or .env.local). Set PUBLIC_URL to the same https origin. Restart.
