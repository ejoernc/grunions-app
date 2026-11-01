---
name: regulars-design-system
description: Use when changing Grunions UI. Tokens, shared classes, light and dark, and what not to restyle.
---

# Regulars

Flask, Jinja, and vanilla CSS. Do not add React, Tailwind, or shadcn code.

The product paints dark. `[data-theme=light]` is the light theme for the preview. Colors are Forest Ink `#171C19`, Clubhouse `#303A33`, Chalk `#F7F8F3`, Electric Lime `#C7F464`, Clear Cyan `#5DDDE5`, Golden Yellow `#F4C95D`, Social Orange `#FF875D`, and Cloud Gray `#C3CACB`. Lime is the brand, not success. Cyan is cleared. Icons are Phosphor (Regular, Fill on the selected nav circle, Bold for emphasis) at 16, 20, or 24px. Headings use Space Grotesk. Everything else uses Plus Jakarta Sans.

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
| Card, button, chip, field, sheet roundness | `--radius-card`, `--radius-button`, `--radius-chip`, `--radius-input`, `--radius-overlay` |
| Button height, chip height, nav icon | `--size-button`, `--size-chip`, `--icon-nav` |
| Nav offset, circle, and content clearance | `--nav-offset-bottom` (24px), `--nav-pad`, `--nav-gap`, `--nav-circle`, `--nav-clear` |
| Selected chip or Schedule card | `--color-selected`, `--color-on-selected` |
| Focus ring | `--color-focus` |

Do not paste a new hex into a screen. Use a token or an existing class.

Leave these as literals: the first-paint `background:#171C19` on `html` and `body`, the date and time SVG icons (a variable cannot live inside the image; they use Chalk `#F7F8F3`), the Google mark, and the printed page.

## Classes

- Buttons: `btn btn-primary`, `btn btn-secondary`, `btn btn-danger`, `btn quiet`, `iconbtn`
- Chips: `chip`, `chip chip-active on`, `chip-info`
- Segmented: `actseg` (Exact dates / Month only, Away / Hosting, Considering / Official)
- Status line: `roster_status` (dot plus one line)
- Cards: `card`. Event pages share the hero, stat tiles, and location card.
- Chat: `.m .txt`, `.m.mine .txt`
- Sheets: `dialog.botsheet .sheet`, `dialog.modal .sheet`
- Map: `.homemap` with `.mpin`
- Nav: `nav.tabs` — a floating pill of 52px circles, 8px gaps, 8px padding, 24px above the safe area. Members get Home, Lineup, Chat. Coaches and admins also get Admin. No text labels. Unselected circles are Clubhouse with Chalk Phosphor Regular icons. The selected circle is Electric Lime with a Forest Ink Phosphor Fill icon. Built by `_nav_anchor`.
- Icons: `ICONS` in `ui.py`

Figma roles: Button `72:2719`, Badge `72:2718`, Avatar `72:2717`, Card `72:2721`, Input `73:1977`, Tabs `73:2899`, Toggle group `73:2902`, Dialog `73:227`, Sheet `73:1988`.

Preview: `/design-system` (admins). Human notes: `docs/design-system.md`.

Do not restyle the map pin position, the 12px Home card gap, the greeting crossfade, day chips, or People rows unless that is the task. Bump `/sw.js?v=` when shared CSS changes.
