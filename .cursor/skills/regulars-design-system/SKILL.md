---
name: regulars-design-system
description: Use when changing Grunions UI. Tokens, shared classes, light and dark, and what not to restyle.
---

# Regulars

Flask, Jinja, and vanilla CSS. Do not add React, Tailwind, or shadcn code.

The product paints dark. `[data-theme=light]` is the light theme for the preview. Colors are Deep Forest `#090D0B`, Dark Clubhouse `#0F1512`, Raised `#131A16`, Chalk text `#F2F6F1`, Muted Lime `#B2DE64`, Deep Cyan `#50C6CF`, Golden Yellow `#E4C84D`, Coral `#F48782`, and Cloud Gray `#ADB5B1`. Lime is the brand, not success. Cyan is cleared. Icons are Phosphor (Regular, Fill on the selected nav circle, Bold for emphasis) at 16, 20, or 24px. Headings use Space Grotesk. Everything else uses Plus Jakarta Sans.

The Figma skill page (`2688:3905`) installs React, Tailwind, and `npx shadcn`. Do not run that. Map its roles onto the classes below.

## Where to change things

All of these are in `regulars/foundation.css`. `:root` is dark. `[data-theme=light]` overrides the same names.

| Change | Token |
| --- | --- |
| Font | `--font-sans` |
| Lime brand | `--color-lime` (alias `--color-primary`, `--accent`) |
| Background, surfaces, text, borders | `--color-bg`, `--color-surface`, `--color-surface-2`, `--color-text`, `--color-border` |
| Map canvas and pin | `--color-map`, `--color-selected`, `--color-bg` |
| Chat bubble | `--color-surface` for others, `--color-surface-2` for mine |
| Sheet, handle, row | `--color-sheet`, `--color-sheet-border`, `--color-sheet-handle`, `--color-sheet-row` |
| Cleared, attention, not cleared | `--color-status-cleared`, `--color-status-attention`, `--color-status-not-cleared` |
| Card gap (12px on Home) | `--space-card`. The Home dock gap stays the literal `12px`. |
| Card, button, field, sheet, pill roundness | `--radius-card` 20, `--radius-button` 12, `--radius-input` 12, `--radius-control` 16, `--radius-overlay` 24, `--radius-chip` 999 |
| Button height, chip height, nav icon | `--size-button`, `--size-chip`, `--icon-nav` |
| Nav offset, circle, and content clearance | `--nav-offset-bottom` (24px), `--nav-pad`, `--nav-gap`, `--nav-circle`, `--nav-clear` |
| Selected chip or Schedule card | `--color-selected`, `--color-on-selected` |
| Focus ring | `--color-focus` |

Do not paste a new hex into a screen. Use a token or an existing class.

Leave these as literals: the first-paint `background:#090D0B` on `html` and `body`, the date and time SVG icons (a variable cannot live inside the image; they use `#F2F6F1`), the Google mark, and the printed page.

## Classes

- Buttons: `btn btn-primary`, `btn btn-secondary`, `btn btn-danger`, `btn quiet`, `iconbtn`. RSVP uses one macro, `rsvp_btn`: selected is lime `btn-primary` with a leading Phosphor check (`svg.rsvpcheck`); unselected is outlined `btn-secondary`. Labels are Going and Not going (Lineup also has Interested).
- Upload field: `upload_field(name, mode, hint, accept, src, clear_name)`. One 140px zone for images and files. Dashed 1.5px `--color-border`, radius `--radius-overlay`. Image mode uses a Phosphor image icon, lime “Upload an image”, and “PNG or JPG”, then a thumbnail. File mode uses a Phosphor file icon, lime “Upload a file”, and the accepted types (such as “CSV or Excel”), then the filename and size. The whole area opens the hidden input. A desktop drag highlights the border. Replace and Remove sit on the chosen file.

- Chips: `chip`, `chip chip-active on`, `chip-info`. Sibling views (Chat, Admin, Profile) use these pills. There is no underline tab.
- Admin page header: `admin_page(title, subtitle)`. One Title 1 H1 with an optional `btn quiet pageact` on the right, then an optional Body 2 subtitle (`pagesub`). Gap from the header block to content is `--space-4` (`.pagehead` margin-bottom). Management pages use a back control to Manage. One H1 per page.
- Manage rows: `manage_row` inside `.mlist` on `.mgroup`. Raised surface, 32px rounded icon, title, one description line, a lime count (`.mbadge`) only when it is above zero, and a trailing chevron. Groups are Activities, Members, and Club settings.
- Segmented: `actseg` (Exact dates / Month only, Away / Hosting, Considering / Official)
- Status line: `roster_status` (dot plus one line)
- Cards: `card`. Event pages share the hero, stat tiles, and location card. Icon rows on Schedule, Lineup, and the Home next card use `.nxrow`. The gap between those rows is `--space-meta` (2px). The icon-to-text gap stays `--space-2`, and the sports subtext (`.sportline`) stays 6px. Location fields use `data-places`: a custom dropdown from `/api/places`, not a native datalist. Club pools come first. Picking a suggestion shows the verified check.
- Chat: `.m .txt`, `.m.mine .txt`
- Sheets: `dialog.botsheet .sheet`, `dialog.modal .sheet`. Chat and settings sheets stay bottom sheets with a grab handle. Date and time pickers are a centered dialog (`dialog.matpick`) with Cancel and OK. Schedule ghosts days with no events, shows a dot on event days, and mutes past days. Form calendars leave every day selectable. Time is a clock. `grunionsOpenDate` and `grunionsOpenTime` open them for every `input[type=date]`, `input[type=time]`, and `input[type=month]`. Create event When starts with Exact dates | Month only for coaches and admins, on Team schedule and Lineup. Members only get a specific date, and they do not see Team plan. Month only hides the start and end. The month dialog includes All month, Early, Mid, and Late under the month grid. All month is the default and sorts after Late.
- Map: `.homemap` with `.mpin`
- Top bar: one `app_header` (`header.homehead.apphead`) on Home, Schedule, Lineup, Chat, and Manage. It is 76px plus the safe area. The title, Chat pills, plus circle, and avatar share that 44px row. The plus opens Create event for the same roles as before, including on Manage. Home’s membership chip sits under the title and does not change the row. The bar has no border, shadow, or edge sliver.
- Nav: `nav.tabs` — a floating pill of 52px circles, 8px gaps, 8px padding, 24px above the safe area. Members get Home, Lineup, Chat. Coaches and admins also get Manage (SquaresFour). No text labels. Unselected circles are Clubhouse with Chalk Phosphor Regular icons. The selected circle is Electric Lime with a Forest Ink Phosphor Fill icon. Built by `_nav_anchor`.
- Icons: `ICONS` in `ui.py`

Figma roles: Button `72:2719`, Badge `72:2718`, Avatar `72:2717`, Card `72:2721`, Input `73:1977`, Tabs `73:2899`, Toggle group `73:2902`, Dialog `73:227`, Sheet `73:1988`.

Preview: `/design-system` (admins). Human notes: `docs/design-system.md`.

Do not restyle the map pin position, the 12px Home card gap, the greeting crossfade, day chips, or People rows unless that is the task. Bump `/sw.js?v=` when shared CSS changes.
