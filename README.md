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
Tests: `.venv/bin/python test_app.py` (84 checks) and `.venv/bin/python -m pytest -q test_v2.py` (14 tests), `.venv/bin/python -m pytest -q test_google.py` (8 tests). Run each in its own process, or just `./run_tests.sh`. Daily job: `.venv/bin/python daily_expiry.py [--days 30] [--remind]`.

## Roles
member (athlete), coach (check-in + #coaches), admin (everything). Manage on Admin → **Roles** (/admins): every member with Make/Remove admin and Make/Remove coach. The last admin can't be removed.
ADMIN_EMAIL (comma-separated) bootstraps admins and keeps them admin on every start; remove an address there to demote it.

## Pages
- /join: QR target, creates the account and logs in. /login: one-time magic link (LINK_MINUTES, default 15; single use, stored hashed), emailed via SMTP.
- /home: Cleared to play card (membership + each required item), USAWP status, expiry warning, reminders, next practice, attendance, profile.
  Until a member is verified and cleared, the Not cleared card includes an inline USAWP Membership # form (digits, 4-10, prefilled when stored). Add saves the number and opens a pending verification request, or updates the number on the one already pending. The card then shows "Sent to Grunions for verification" with status pending. Three submissions per member per hour.
- /practices: recurring Tue 7–8:30 Marina HS / Fri 7–8:30 Westminster HS (next 4 weeks auto-created); Going / Not going, headcount, who's coming. Admin add/edit/cancel/restore.
- /chat: #team (everyone; admins can post 📣 announcements) and 🔒 #coaches (coaches + admins). Polls every 3 s.
- /admin (staff): check-in by date; RSVP'd first; badges for RSVP, USAWP, Cleared/Not cleared with reason, days left.
  Admin "Verify" panel: open Sport:80 (name copied to clipboard), Mark membership verified (member #, expires on; records admin + time),
  enter compliance items (completed / expires), set role.
- /members (admin, +CSV), /import (Sport:80 .xlsx/.csv incl. SafeSport/Background columns), /qr, /expiring (expired / 7 days / N days, incl. compliance items; in-app reminders), /requirements (configure items, who they apply to, import keywords).
Status auto-flips to expired once expires_on passes. Cleared = membership verified AND all required items present and unexpired.
Security: CSRF on every POST, HttpOnly SameSite cookies, chat escaped, role checks server-side.
Before production: SMTP configured, DEV_SHOW_LINKS=0, HTTPS, DB backups (copy $DATA_DIR/grunions.db). v1 kept as app_v1_checkin.py.

## UI
Templates live in ui.py (restrained dark theme: one surface, gray text, blue only for primary actions and the active tab, status shown as a small dot + label).
Tabs: Home, Schedule, Chat, plus Admin for coaches/admins (Check-in · Members · Expiring · Import · Rules · QR). Tap a name on check-in to open its details panel.

## Verification bot API
- Home form or admin "Ask Grunions to verify" creates a verify_requests row (pending). The Home form, if one is already pending, updates that row's member_number instead of inserting another. Admin "Ask Grunions to verify" does not create a duplicate while one is pending.
- Whenever a verify request is created, if VERIFY_WEBHOOK_URL is set, POSTs this JSON (5 s timeout). Failures are logged only and never break the page:
  `{"request_id": 12, "member_id": 4, "name": "Ana Lopez", "email": "ana@example.com", "member_number": "5555555", "requested_by": "Eli Joern", "app_url": "https://grunions.example"}`
  `app_url` is PUBLIC_URL. `member_number` and `requested_by` are stored on the request. If VERIFY_WEBHOOK_KEY is set, the POST sends `Authorization: Bearer <key>`. If VERIFY_WEBHOOK_HEADER is set, that name is used instead and the value is the raw key (no Bearer prefix).
- Auth: `Authorization: Bearer $BOT_API_KEY` (401 otherwise; API disabled if unset).
- GET /api/verify-requests?status=pending|done → list.
- POST /api/verify-requests/<id>/result  {"verified":true,"member_number":"123","membership_expires_on":"2027-08-31",
  "compliance":{"SafeSport training":"2027-05-01"},"note":"..."} → updates member + compliance (matched by requirement name or keyword),
  marks done (409 if already answered), posts summary to #coaches as "Grunions bot", and an in-app notice to every admin.

## Environment variables
| Var | Needed | Purpose |
|---|---|---|
| SECRET_KEY | prod | session signing (random 64 hex). |
| ADMIN_EMAIL | yes | bootstrap admin(s), comma-separated, e.g. `elliott.joern@gmail.com`. |
| PUBLIC_URL | prod | e.g. `https://grunions.onrender.com`; used in login links + QR. If it starts with https, secure cookies and proxy headers are on. |
| DATA_DIR | prod | folder for `grunions.db` and `uploads/` (Render disk: `/data`). Defaults to the app folder. GRUNIONS_DB / GRUNIONS_UPLOADS override individually. |
| SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASSWORD, MAIL_FROM | prod | login emails. All five must be set. Port 465 = SSL, other ports = STARTTLS. |
| DEV_SHOW_LINKS | local | `1` shows the login link on screen. Never in production. |
| GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET | no | enable Sign in with Google (button appears only when both are set). |
| LINK_MINUTES | no | login link lifetime (default 15). |
| SECURE_COOKIES / BEHIND_PROXY | no | force `1`/`0`; default on when PUBLIC_URL is https. |
| VERIFY_WEBHOOK_URL | no | POST target when a verify request is created. JSON keys: request_id, member_id, name, email, member_number, requested_by, app_url (PUBLIC_URL). 5 s timeout. |
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
and re-creates Elliott Joern (elliott.joern@gmail.com, USAWP #659226, membership thru 2027-06-07, SafeSport thru 2027-05-11, background thru 2028-08-28) as verified admin + coach.
Back up grunions.db first. It acts on whatever DATA_DIR/GRUNIONS_DB points at.

## Sport:80 roster import columns
/import takes .csv or .xlsx (title rows above the header are skipped; headers matched case/space/punctuation-insensitively):
- **First Name / Last Name** (or Name / Full Name), **Email / Email Address** — matching (email first, then unique first+last).
- **ID Number / Member Number / Membership Number** — stored as USAWP #. **Contact ID** — stored as sport80_contact_id.
- **Status / Membership Status** and **Valid Until / Expiry Date / Membership Expiry Date** — status. If there's no status column, a future expiry counts as current.
- Any column containing a requirement keyword (safesport, background, waiver, concussion; editable in Rules) plus expiry/valid through/completed/status updates that item.
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
