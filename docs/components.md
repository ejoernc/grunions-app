# Regulars 2.0 components

Source: Figma `X1hA7Tpq3qoRN9fKMPEw3R`, page 02 · Components. Code: `components.py` (Jinja `rg_*`), styles in `regulars/foundation.css` ("Regulars 2.0 components").

| Component | Function / Jinja | Figma | Used on |
|---|---|---|---|
| Event card | `event_card` / `rg_event_card` | 2.0 / Event card (350:696) | Schedule home week list, Schedule list (featured) — via `r2_event_card` |
| Event row | `event_row` / `rg_event_row` | 2.0 / Event row (350:741) | Schedule list rows, cancelled practices — via `r2_event_row` |
| Event line | `event_line` / `rg_event_line` | Me · Calendar rows (09.03) | Calendar, Manage › This week (with Edit pill) |
| List row | `row` / `rg_row` (settings · person · chat) | 2.0 / List row (350:849) | Chat lists, practice people, profile Account + clearances, club settings rows |
| Chip | `chip` / `rg_chip` | 2.0 / Chip (349:566) | Status everywhere |
| Callout | `callout` / `rg_callout` | flow cards ("Need a ride? Ask →") | Practice: sign-up gate, rides, wrap up; Calendar availability |
| Metric | `metric` / `rg_metric` | 2.0 / Metric | Practice page, wrap-up — via `r2_metric` |
| Info block | `info` / `rg_info` | 2.0 / Info block | Practice details — via `r2_info` |
| Section header | `section` / `rg_section` | 2.0 / Section header | Practice page — via `r2_section` |
| Caps label | `label` / `rg_label` | CLEARANCE / TUE 17 | Profile, Calendar |
| Segmented control | `seg` / `rg_seg` | 2.0 / Segmented control (349:602) | Calendar, Schedule list |
| Filters | `filters` / `rg_filters` | type filters | Calendar |
| Empty state | `empty` / `rg_empty` | 2.0 / Empty state (353:749) | Calendar |
| Checklist | `checklist` / `rg_checklist` | 10.33 Finish setup | Schedule home (new members only) |
| Manage tile | `manage_tile` / `rg_manage_tile` | 08 Manage rows | Manage — via `manage_row` |
| Icon | `icon` / `rg_icon` | 02 G Icons (20×20) | sizes sm 16 · md 20 · lg 24 |

Event colors: `event_tone(kind)` — practice sun, scrimmage sky, game tangerine, Lineup lavender, trip/clinic aqua, volunteer bubblegum, social mango, cancelled graphite, coaching sky.

Not migrated yet (still screen-specific markup): Lineup cards (`lineup_card`), Home "next practice" hero and week drawer chrome, practice hero (`p5hero`), check-in rows, chat thread bubbles and composer, Manage People rows, member detail panel, event create/edit forms, sheets. Move each onto a component (add one if needed) rather than restyling in place.
