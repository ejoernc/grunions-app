# Grunions

Before building anything, read `docs/regulars-2.0-flows.md`. Build from the Figma workflow pages (12 Member, 13 Coach, 14 Admin), not one frame at a time. A screen whose action is fake (hardcoded data, "Preview only", a sheet that sends nothing) is not done. Never delete or rewrite rows on boot: live data is on the Render disk.

UI is built from components. Every repeated piece (event card, event row, event line, list row, chip, callout, metric, info block, section header, segmented control, filters, empty state, checklist, manage tile) is a function in `components.py`, named after its Figma component (page 02 · Components). Templates call them as `rg_*` Jinja globals; Python that builds HTML calls `components.*`. Change a component there and every screen updates. If a screen needs something that isn't there, add a component first. Don't hand-write card or row markup on a page.

Colors: only the Figma 01 Foundations palette in `regulars/foundation.css` (`--ink --carbon --graphite --smoke --paper --lime --tide --team-*`, plus `--fixed-ink/--fixed-paper` for text on colored fills). No other hex anywhere. Event color comes from `components.event_tone(kind)`.

Icons: the 20×20 stroke set in `ui._NAV3_GLYPHS` (Figma 02 G), shown at 16 / 20 / 24 via `rg_icon`.

The app is Flask and Jinja. Read `.cursor/skills/regulars-design-system/SKILL.md` too, but where it disagrees with this file, this file wins.

## Matching Figma

Never approximate. A screen is done only when it measures the same as its Figma frame.

1. For every frame, call `get_design_context` (with the figma-design-to-code skill) and read the exact values: sizes, padding, gaps, radius, font size / weight / line height / tracking, colors. Use `get_metadata` for positions and `get_variable_defs` for colors inside images (toggles, icons). A screenshot is for checking, not for reading values.
2. Read how the frame works, not only how it looks: is it a page, a pushed screen with its own top bar, or a bottom sheet? What does each row open? Which field does each control save? If a control has no data behind it, add the column (additive only) instead of faking it.
3. Build with components and palette tokens. If the Figma component changed (e.g. 2.0 / Toggle is 60×34), change the component in `components.py` / `foundation.css` so every screen updates.
4. Measure the rendered page with Playwright at 390×844: computed styles and bounding boxes for each element, compared with the Figma numbers. Restart the local server after CSS changes.
5. Before calling it done, list every remaining difference and its reason (font metrics ±1px, preview data, a deliberate product decision the user asked for). Nothing is left unexplained.
6. CSS is inlined into every page: never put user-visible words (e.g. "Practice plan") in CSS comments; tests search page text.
