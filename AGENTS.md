# Grunions

Before building anything, read `docs/regulars-2.0-flows.md`. Build from the Figma workflow pages (12 Member, 13 Coach, 14 Admin), not one frame at a time. A screen whose action is fake (hardcoded data, "Preview only", a sheet that sends nothing) is not done. Never delete or rewrite rows on boot: live data is on the Render disk.

UI changes go through Regulars. Read `.cursor/skills/regulars-design-system/SKILL.md` before editing screens or CSS.

Tokens live in `regulars/foundation.css`. Shared classes live in `ui.py`. The app is Flask and Jinja. Keep the Streamline Plump line icons.
