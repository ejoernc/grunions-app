---
name: regulars-design-system
description: Use when changing Grunions UI. Tokens, shared classes, light and dark, and what not to restyle.
---

# Regulars

Flask, Jinja, and vanilla CSS. Do not add React, Tailwind, or shadcn code.

Figma file `9ZhrS5v7hQGSY7eGJwG19Y` is the structure. The product paints dark. `[data-theme=light]` is the light theme for the preview. Colors stay monochrome gray, blue `#3b82f6`, and the status dots. Icons stay Streamline Plump.

The Figma skill page (`2688:3905`) installs React, Tailwind, and `npx shadcn`. Do not run that. Map its roles onto the classes below.

## Where to change things

All of these are in `regulars/foundation.css`. `:root` is dark. `[data-theme=light]` overrides the same names.

| Change | Token |
| --- | --- |
| Font | `--font-sans` |
| Blue | `--color-primary` (alias `--accent`) |
| Background, surfaces, text, borders | `--color-bg`, `--color-surface`, `--color-surface-2`, `--color-text`, `--color-border` |
| Map canvas and pin | `--color-map`, `--color-selected`, `--color-bg` |
| Chat bubble | `--color-surface` for others, `--color-surface-2` for mine |
| Sheet, handle, row | `--color-sheet`, `--color-sheet-border`, `--color-sheet-handle`, `--color-sheet-row` |
| Cleared, attention, not cleared | `--color-status-cleared`, `--color-status-attention`, `--color-status-not-cleared` |
| Card gap (12px on Home) | `--space-card`. The Home dock gap stays the literal `12px`. |
| Card, button, chip, field, sheet roundness | `--radius-card`, `--radius-button`, `--radius-chip`, `--radius-input`, `--radius-overlay` |
| Button height, chip height, nav icon | `--size-button`, `--size-chip`, `--icon-nav` |
| Selected chip or Schedule card | `--color-selected`, `--color-on-selected` |
| Focus ring | `--color-focus` |

Do not paste a new hex into a screen. Use a token or an existing class.

Leave these as literals: the first-paint `background:#0a0a0b` on `html` and `body`, the date and time SVG icons (a variable cannot live inside the image), the Google mark, and the printed page.

## Classes

- Buttons: `btn btn-primary`, `btn btn-secondary`, `btn btn-danger`, `btn quiet`, `iconbtn`
- Chips: `chip`, `chip chip-active on`, `chip-info`
- Segmented: `actseg` (Exact dates / Month only, Away / Hosting, Considering / Official)
- Status line: `roster_status` (dot plus one line)
- Cards: `card`. Event pages share the hero, stat tiles, and location card.
- Chat: `.m .txt`, `.m.mine .txt`
- Sheets: `dialog.botsheet .sheet`, `dialog.modal .sheet`
- Map: `.homemap` with `.mpin`
- Nav: `nav.tabs` — Home, Lineup, Chat, and Admin for coaches and admins
- Icons: `ICONS` in `ui.py`

Figma roles: Button `72:2719`, Badge `72:2718`, Avatar `72:2717`, Card `72:2721`, Input `73:1977`, Tabs `73:2899`, Toggle group `73:2902`, Dialog `73:227`, Sheet `73:1988`.

Preview: `/design-system` (admins). Human notes: `docs/design-system.md`.

Do not restyle the map pin position, the 12px Home card gap, the greeting crossfade, day chips, or People rows unless that is the task. Bump `/sw.js?v=` when shared CSS changes.
