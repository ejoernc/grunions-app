# Regulars

Grunions keeps its own look. The [shadcn/ui library](https://www.figma.com/design/9ZhrS5v7hQGSY7eGJwG19Y) supplied the structure: semantic tokens, light and dark, and component roles. The app stays Flask and Jinja.

Admins open `/design-system` to see type, color, buttons, chips, the status line, and both navs.

## One place to change

`regulars/foundation.css`

| You want | Token |
| --- | --- |
| A different font | `--font-sans` |
| A different lime | `--color-lime` (`--color-primary`) |
| A different background | `--color-bg` |
| Different text | `--color-text`, `--color-text-secondary`, `--color-text-tertiary` |
| Status colors | `--color-status-cleared`, `--color-status-attention`, `--color-status-not-cleared` |
| The map | `--color-map`, `--color-scrim` |
| Chat bubbles | `--color-surface` and `--color-surface-2` |
| Sheets | `--color-sheet`, `--color-sheet-border`, `--color-sheet-handle`, `--color-sheet-row` |
| Light theme | the same names under `[data-theme=light]` |
| More space between Home cards | `--space-card` (12px today). The Home dock gap stays the literal `12px`. |
| Rounder cards | `--radius-card` (20px) |
| Rounder buttons, fields, or sheets | `--radius-button` (12px), `--radius-input` (12px), `--radius-overlay` (24px) |
| Space | `--space-1` through `--space-6`, then `--space-8`, `--space-10`, `--space-12` (4, 8, 12, 16, 20, 24, 32, 40, 48) |
| How high the nav floats | `--nav-offset-bottom` (24px). Content clearance follows `--nav-clear`. |

Older names still work: `--bg`, `--surface`, `--accent`, `--ok`, `--warn`, `--bad`, `--r`.

## What screens already use

Buttons, chips, cards, inputs, sheets, avatars, the bottom nav, and Phosphor icons. The nav is one floating pill (`nav.tabs`, built by `_nav_anchor`). Members get three circles: Home, Lineup, Chat. Coaches and admins get a fourth, Admin. There are no text labels. Circles are 52px with 8px gaps, so four circles are about two-thirds of a phone and three are narrower. The selected circle is Electric Lime with a Forest Ink icon. Clearance rows use `roster_status`: one dot and one line, such as `Expiring soon · expires in 3 days`.

## Screen audit

`:root` is the dark theme the app paints. `[data-theme=light]` is the light theme. The preview shows both. The product does not switch the whole app to light.

| Screen | What it uses |
| --- | --- |
| Home | The map canvas, attribution, and pin read `--color-map` and the selected colors. Pin position, the 12px dock gap, the greeting crossfade, and the day chip stay as they are. Page padding uses `--nav-clear` so the pill does not cover the dock. |
| Practice list | Schedule cards (`card`, date tile, RSVP pills). |
| Practice page | Shared event layout: hero map, stat tiles, status dot, details list, who's going, location card. |
| Lineup feed | Event cards, RSVP pills, and one scrolling row of filter chips. Hosting and My Lineup live on the profile. |
| Lineup event | Same event layout as Practice. Status is Official trip, Considering, Community, or Pending approval. |
| Lineup form | Segmented controls (`actseg`) for Where, Status, and Exact dates / Month only. Inputs use the shared field. |
| Chat | Team and Coaches are the same pill chips as the Lineup filters. The composer sits above the nav. Bubbles use `--color-surface` and `--color-surface-2`. |
| People | Rows, letter headers, and status dots. Sticky bars keep the page background. |
| Member and profile | Shared lists, avatars, and the profile bar. Your profile switches General, My Lineup, and Hosting with the same pill chips. Hosting shows only after you have hosted. Another member's page stays on General. |
| Admin tabs | One page header (`admin_page`): chip row, then Title 1, an optional ghost action (`btn quiet pageact`), then an optional Body 2 subtitle. Schedule, People, Events, Expiring, Transfer, Rules, and Join QR use it. The gap from the chips to the title is `--space-5`. The gap from the header block to the first content is `--space-4`. |
| Admin Schedule | The header title is Schedule, then the date bar. One card per event, selected with `--color-selected`. Filters and the check-in count stay in the filter row. |
| Events, People, Expiring, Transfer, Rules, QR | Same page header. People puts Export CSV in the action slot. Events puts Create event there. Each page has one H1. |
| Design preview | `/design-system`, admins only. |

Reused: `btn`, `chip`, `card`, `actseg`, `list`, `st`, avatars, and the bottom nav.

Adapted: semantic names, the type and spacing scale, radius roles, focus and disabled states, and a light theme. Map, chat, sheets, buttons, chips, and fields read the tokens.

Kept custom: the map pin position, the greeting crossfade, day chips, Lineup cards, People rows, the Google mark, and every workflow. The first paint on `html` and `body` stays `#090D0B`. SVG icons in date and time fields stay encoded hex (`#F2F6F1`), because a CSS variable cannot live inside those images.

Not copied: React, Tailwind, and `npx shadcn`. The Figma skill page (`2688:3905`) installs a React theme. Grunions keeps Flask and Jinja. Component pages in file `9ZhrS5v7hQGSY7eGJwG19Y` are the structure: Button `72:2719`, Badge `72:2718`, Avatar `72:2717`, Card `72:2721`, Input `73:1977`, Tabs `73:2899`, Toggle group `73:2902`, Dialog `73:227`, Sheet `73:1988`. Event types stay gray. They do not get a separate hue.
