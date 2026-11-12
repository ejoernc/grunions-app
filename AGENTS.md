# Grunions

Before building anything, read `docs/regulars-2.0-flows.md`. Build from the Figma workflow pages (12 Member, 13 Coach, 14 Admin), not one frame at a time. A screen whose action is fake (hardcoded data, "Preview only", a sheet that sends nothing) is not done. Never delete or rewrite rows on boot: live data is on the Render disk.

UI is built from components. Every repeated piece (event card, event row, event line, list row, chip, callout, metric, info block, section header, segmented control, filters, empty state, checklist, manage tile) is a function in `components.py`, named after its Figma component (page 02 · Components). Templates call them as `rg_*` Jinja globals; Python that builds HTML calls `components.*`. Change a component there and every screen updates. If a screen needs something that isn't there, add a component first. Don't hand-write card or row markup on a page.

Colors: only the Figma 01 Foundations palette in `regulars/foundation.css` (`--ink --carbon --graphite --smoke --paper --lime --tide --team-*`, plus `--fixed-ink/--fixed-paper` for text on colored fills). No other hex anywhere. Event color comes from `components.event_tone(kind)`.

Icons: the 20×20 stroke set in `ui._NAV3_GLYPHS` (Figma 02 G), shown at 16 / 20 / 24 via `rg_icon`.

The app is Flask and Jinja. Read `.cursor/skills/regulars-design-system/SKILL.md` too, but where it disagrees with this file, this file wins.
