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
| More space between Home cards | `--space-card` (12px today) |
| Rounder cards | `--radius-card` |
| Rounder buttons or chips | `--radius-button`, `--radius-chip` |

Older names still work: `--bg`, `--surface`, `--accent`, `--ok`, `--warn`, `--bad`, `--r`.

## What screens already use

Buttons, chips, cards, inputs, sheets, avatars, the bottom nav, and Plump icons. Clearance rows use `roster_status`: one dot and one line, such as `Expiring soon · expires in 3 days`.

## Audit

Reused: the existing classes, now fed by tokens where the foundation is included.

Adapted: semantic token names, a type and spacing scale, radius roles, and a light theme that the product does not turn on.

Kept custom: Home, the map pin, greeting crossfade, day chips, Lineup cards, People rows, the Google mark, and every workflow.

Not copied: React, Tailwind, and the shadcn default palette. The library’s install notes ask for `npx shadcn` and a theme URL that was not available, and Figma variable values did not load without a selected layer. The numbers in the foundation are the colors already shipping in the app.
