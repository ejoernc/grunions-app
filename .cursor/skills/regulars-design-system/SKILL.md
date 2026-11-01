---
name: regulars-design-system
description: Use when changing Grunions UI. Tokens, shared classes, and what not to restyle.
---

# Regulars

Flask, Jinja, and vanilla CSS. Do not add React, Tailwind, or shadcn code.

Figma file `9ZhrS5v7hQGSY7eGJwG19Y` is a structural reference. The product look stays monochrome gray, blue `#3b82f6`, status dots, and Streamline Plump line icons.

## Where to change things

All of these are in `regulars/foundation.css`.

| Change | Token |
| --- | --- |
| Font | `--font-sans` |
| Blue | `--color-primary` (alias `--accent`) |
| Background, surfaces, text, borders | `--color-bg`, `--color-surface`, `--color-text`, `--color-border` |
| Cleared, attention, not cleared | `--color-status-cleared`, `--color-status-attention`, `--color-status-not-cleared` |
| Card gap (12px) | `--space-card` |
| Card roundness | `--radius-card` |
| Button, chip, field roundness | `--radius-button`, `--radius-chip`, `--radius-input` |
| Button height, chip height, nav icon | `--size-button`, `--size-chip`, `--icon-nav` |
| Selected chip or Schedule card | `--color-selected`, `--color-on-selected` |
| Focus ring | `--color-focus` |

Do not paste a new hex into a screen. Use a token or an existing class.

The Figma file's Claude skill page installs React, Tailwind, and `npx shadcn`. Do not do that. Map the library's roles onto the classes below. Event types stay gray (`--color-event`). They do not get their own hues.

## Classes

- Buttons: `btn btn-primary`, `btn btn-secondary`, `btn btn-danger`, `btn quiet`
- Chips: `chip`, `chip chip-active on`, `chip-info`
- Status line: `roster_status` (dot plus one line of text)
- Cards: `card`
- Nav: `nav.tabs` — Home, Lineup, Chat, and Admin for coaches and admins
- Icons: `ICONS` in `ui.py` (Streamline Plump)

Figma roles: Button `72:2719`, Badge `72:2718`, Avatar `72:2717`, Card `72:2721`, Input `73:1977`, Tabs `73:2899`, Dialog `73:227`, Sheet `73:1988`.

Preview: `/design-system` (admins). Human notes: `docs/design-system.md`.

Do not restyle Home, the map pin, the 12px card gap, the greeting crossfade, day chips, or People rows unless that is the task. Bump `/sw.js?v=` when shared CSS changes.
