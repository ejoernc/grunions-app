# Regulars

Grunions keeps its own look. The [shadcn/ui library](https://www.figma.com/design/9ZhrS5v7hQGSY7eGJwG19Y) supplied the structure: semantic tokens, light and dark, and component roles. The app stays Flask and Jinja.

Admins open `/design-system` to see type, color, buttons, chips, the status line, and both navs.

## One place to change

`regulars/foundation.css`

| You want | Token |
| --- | --- |
| A different font | `--font-sans` |
| A different blue | `--color-primary` |
| A different background | `--color-bg` |
| Different text | `--color-text`, `--color-text-secondary`, `--color-text-tertiary` |
| Status colors | `--color-status-cleared`, `--color-status-attention`, `--color-status-not-cleared` |
| The map | `--color-map`, `--color-scrim` |
| Chat bubbles | `--color-surface` and `--color-surface-2` |
| Sheets | `--color-sheet`, `--color-sheet-border`, `--color-sheet-handle`, `--color-sheet-row` |
| Light theme | the same names under `[data-theme=light]` |
| More space between Home cards | `--space-card` (12px today). The Home dock gap stays the literal `12px`. |
| Rounder cards | `--radius-card` |
| Rounder buttons, chips, or sheets | `--radius-button`, `--radius-chip`, `--radius-overlay` |

Older names still work: `--bg`, `--surface`, `--accent`, `--ok`, `--warn`, `--bad`, `--r`.

## What screens already use

Buttons, chips, cards, inputs, sheets, avatars, the bottom nav, and Plump icons. Clearance rows use `roster_status`: one dot and one line, such as `Expiring soon · expires in 3 days`.

## Screen audit

`:root` is the dark theme the app paints. `[data-theme=light]` is the light theme. The preview shows both. The product does not switch the whole app to light.

| Screen | What it uses |
| --- | --- |
| Home | The map canvas, attribution, and pin read `--color-map` and the selected colors. Pin position, the 12px dock gap, the greeting crossfade, and the day chip stay as they are. |
| Practice list | Schedule cards (`card`, date tile, RSVP pills). |
| Practice page | Shared event layout: hero map, stat tiles, status dot, details list, who's going, location card. |
| Lineup feed | Event cards, one gray type line, RSVP pills, filter chips. |
| Lineup event | Same event layout as Practice. Status is Official trip, Considering, Community, or Pending approval. |
| Lineup form | Segmented controls (`actseg`) for Where, Status, and Exact dates / Month only. Inputs use the shared field. |
| Chat | Bubbles use `--color-surface` and `--color-surface-2`. The message sheet uses the sheet tokens. Links use the primary blue. |
| People | Rows, letter headers, and status dots. Sticky bars keep the page background. |
| Member and profile | Shared lists, avatars, and the profile bar. |
| Admin Schedule | One card per event, selected with `--color-selected`. Filters and the check-in count stay in the filter row. |
| Approvals, Expiring, Transfer, Rules, QR | Admin chips and the shared buttons, lists, and fields. |
| Design preview | `/design-system`, admins only. |

Reused: `btn`, `chip`, `card`, `actseg`, `list`, `st`, avatars, and the bottom nav.

Adapted: semantic names, the type and spacing scale, radius roles, focus and disabled states, and a light theme. Map, chat, sheets, buttons, chips, and fields read the tokens.

Kept custom: the map pin position, the greeting crossfade, day chips, Lineup cards, People rows, the Google mark, and every workflow. The first paint on `html` and `body` stays `#0a0a0b`. SVG icons in date and time fields stay encoded hex, because a CSS variable cannot live inside those images.

Not copied: React, Tailwind, and `npx shadcn`. The Figma skill page (`2688:3905`) installs a React theme. Grunions keeps Flask and Jinja. Component pages in file `9ZhrS5v7hQGSY7eGJwG19Y` are the structure: Button `72:2719`, Badge `72:2718`, Avatar `72:2717`, Card `72:2721`, Input `73:1977`, Tabs `73:2899`, Toggle group `73:2902`, Dialog `73:227`, Sheet `73:1988`. Event types stay gray. They do not get a separate hue.
