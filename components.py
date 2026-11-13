"""Regulars 2.0 components — the single source for every repeated piece of UI.

Built from Figma file X1hA7Tpq3qoRN9fKMPEw3R, page 02 · Components. Each function names its Figma component.
Templates call these as Jinja globals (rg_*), and Python that builds HTML calls them directly, so changing a
component here changes it on every screen. Styles live in regulars/foundation.css under "Regulars 2.0 components".

Rules
- Colors only from the Figma palette (foundation.css). Pick a tone by name, never a hex.
- Icons come from ui.nav_icon at three sizes: sm 16 · md 20 · lg 24.
- A screen that needs something not listed here gets a new component here first, not one-off markup.
"""
from markupsafe import Markup, escape

TONES = ("sun", "sky", "tangerine", "lime", "aqua", "cobalt", "bubblegum", "grape", "cherry", "mango",
         "lavender", "sage", "blush", "stone", "graphite", "carbon")
CHIP_STATUS = ("going", "paid", "expiring", "notcleared", "cleared", "interested", "sport", "neutral")

# What color an event is (Figma 01 Foundations: sun = team, sky = swim/coach, lavender = Lineup,
# aqua = rides/trips, bubblegum = volunteer, mango = community, tangerine = admin / not cleared).
EVENT_TONE = {"practice": "sun", "scrimmage": "aqua", "game": "tangerine", "lineup": "lavender", "tournament": "lavender",
              "competition": "lavender", "trip": "aqua", "clinic": "aqua", "volunteer": "bubblegum",
              "fundraiser": "bubblegum", "social": "mango", "community": "mango", "cancelled": "graphite", "coaching": "sky"}


def _tone(t, default="graphite"):
    t = (t or "").lower()
    return t if t in TONES else default


def event_tone(kind, cancelled=False):
    if cancelled:
        return "graphite"
    return EVENT_TONE.get((kind or "practice").lower(), "sun")


def _e(v):
    return escape(v if v is not None else "")


def _tag(href, klass, inner, extra=""):
    if href:
        return Markup('<a class="%s" href="%s"%s>%s</a>' % (klass, _e(href), extra, inner))
    return Markup('<div class="%s"%s>%s</div>' % (klass, extra, inner))


def icon(name, size="md"):
    """Icon / * (02 G). 20×20 stroke glyphs, rendered at sm 16, md 20 or lg 24."""
    import ui
    return Markup('<span class="rg-ic rg-ic-%s" aria-hidden=true>%s</span>' % (size if size in ("sm", "md", "lg") else "md", ui.nav_icon(name)))


def chip(label, status="neutral"):
    """2.0 / Chip. going · paid · expiring · notcleared · cleared · interested · sport · neutral."""
    st = (status or "neutral").replace(" ", "").lower()
    st = st if st in CHIP_STATUS else "neutral"
    return Markup('<span class="rg-chip st-%s"><i></i>%s</span>' % (st, _e(label)))


def head(title, who="", sub=""):
    """Page header (Nav / Phone / Me · *): who + display title with a period."""
    t = str(title or "")
    t = t if t.endswith(".") else t + "."
    w = ('<div class=rg-who><b>%s</b>%s</div>' % (_e(who), ('<small>%s</small>' % _e(sub)) if sub else "")) if who else ""
    return Markup('<header class=rg-head>%s<h1 class=rg-title>%s</h1></header>' % (w, _e(t)))


def section(title, action_label="", action_href=""):
    """2.0 / Section header."""
    act = ('<a class=rg-secact href="%s">%s</a>' % (_e(action_href), _e(action_label))) if action_label else ""
    return Markup('<div class=rg-sec><h2>%s</h2>%s</div>' % (_e(title), act))


def seg(items, current):
    """2.0 / Segmented control. items = [(key, label, href)]; selected is paper."""
    return Markup('<nav class=rg-seg aria-label=View>%s</nav>' % "".join(
        '<a href="%s"%s>%s</a>' % (_e(h), ' class=on aria-current=page' if k == current else "", _e(l)) for k, l, h in items))


def filters(items, current):
    """Type filters. items = [(key, label, href)]; selected is lime."""
    return Markup('<nav class=rg-filters aria-label=Filter>%s</nav>' % "".join(
        '<a href="%s"%s>%s</a>' % (_e(h), ' class=on aria-current=true' if k == current else "", _e(l)) for k, l, h in items))


def day(label):
    """Day label above event rows (TUE 17)."""
    return Markup('<h3 class=rg-day>%s</h3>' % _e(label))


def label(text):
    """Caps section label (CLEARANCE, ACCOUNT, TUE 17)."""
    return Markup('<h3 class=rg-day>%s</h3>' % _e(text))


def event_line(href, title, sub="", tone="sun", badge="", cta=""):
    """Compact event line (Me · Calendar 09.03, Manage › Schedule 08.01). Team-colored, title + one line,
    ink pill on the right: an arrow, or a short action like Edit / Check in / Post."""
    b = ('<span class=rg-badge>%s</span>' % _e(badge)) if badge else ""
    pill = '<span class="rg-go%s"%s>%s</span>' % (" txt" if cta else "", "" if cta else " aria-hidden=true", _e(cta) if cta else "→")
    inner = '<span class=rg-txt><b>%s</b>%s</span>%s%s' % (_e(title), ('<small>%s</small>' % _e(sub)) if sub else "", b, pill)
    return _tag(href, "rg-event tone-%s" % _tone(tone, "sun"), inner)


def event_row(href, sport, title, meta="", count=None, count_label="GOING", tone="sun", chip_label=""):
    """2.0 / Event row (02 D, 350:741). Sport caps, two-line display title, meta, big count + chevron."""
    cnt = ('<span class=rg-ercount><i aria-hidden=true>›</i><b>%s</b><small>%s</small></span>' % (_e(count), _e(count_label))) if count is not None \
        else '<span class=rg-ercount><i aria-hidden=true>›</i></span>'
    top = '<span class=rg-ek>%s</span>%s' % (_e(sport), str(chip(chip_label, "neutral")) if chip_label else "")
    inner = '<span class=rg-txt>%s<b class=rg-ertitle>%s</b>%s</span>%s' % (
        '<span class=rg-ertop>%s</span>' % top, _e(title), ('<small>%s</small>' % _e(meta)) if meta else "", cnt)
    return _tag(href, "rg-erow tone-%s" % _tone(tone, "sun"), inner)


_CHECK = '<svg width="14" height="14" viewBox="0 0 20 20" fill="none" aria-hidden="true"><path d="M4.5 10.5L8.25 14.25L15.5 6.5" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>'


def event_card(href, sport, title, clock, meridiem="", duration="", venue="", people=(), going_n=0, going=False,
               tone="sun", chip_label="", went=False):
    """2.0 / Event card (02 D, 350:696). Sport + status, title, 104px time, going stack, venue, round action."""
    if going:
        status = '<span class=rg-ecstatus>%s<span>%s</span></span>' % (_CHECK, "You went" if went else "You're going")
    elif chip_label:
        status = '<span class=rg-ecstatus><span>%s</span></span>' % _e(chip_label)
    else:
        status = ""
    stack = "".join('<i>%s</i>' % _e(p) for p in list(people)[:3])
    who = ('<span class=rg-ecwho>%s<em>%s %s</em></span>' % (stack, ("+%d" % (going_n - len(list(people)[:3]))) if going_n > 3 else going_n, "went" if went else "going")) if going_n else ""
    inner = ('<span class=rg-ectop><span class=rg-ek>%s</span>%s</span><b class=rg-ectitle>%s</b>'
             '<span class=rg-ectime><b>%s</b><span><i>%s</i><i>%s</i></span></span>'
             '<span class=rg-ecfoot><span class=rg-ecleft>%s<small>%s</small></span><span class=rg-ecgo aria-hidden=true>›</span></span>') % (
        _e(sport), status, _e(title), _e(clock), _e(meridiem), _e(duration), who, _e(venue))
    return _tag(href, "rg-ecard tone-%s%s" % (_tone(tone, "sun"), " going" if going else ""), inner)


def row(title, sub="", href="", lead="", lead_tone="", trail="", chip_label="", chip_status="neutral",
        chevron=True, kind="settings", badge="", muted=False, extra=""):
    """2.0 / List row (02 D). kind = settings (label/value/chevron) · person (52 avatar) · chat (avatar + time/badge)."""
    lead_html = ""
    if lead:
        lt = _tone(lead_tone, "") if lead_tone else ""
        lead_html = '<span class="rg-lead%s">%s</span>' % (" tone-%s" % lt if lt else "", lead if isinstance(lead, Markup) else _e(lead))
    side = ""
    if chip_label:
        side += str(chip(chip_label, chip_status))
    if trail or badge:
        side += '<span class=rg-side>%s%s</span>' % (('<span class=rg-trail>%s</span>' % _e(trail)) if trail else "",
                                                    ('<span class=rg-count>%s</span>' % _e(badge)) if badge else "")
    if href and chevron and kind == "settings":
        side += '<span class=rg-chev aria-hidden=true>→</span>'
    inner = '%s<span class=rg-txt><b>%s</b>%s</span>%s' % (lead_html, _e(title), ('<small>%s</small>' % _e(sub)) if sub else "", side)
    return _tag(href, "rg-row rg-%s%s" % (kind, " muted" if muted else ""), inner, extra)


CHEVRON = '<svg width="18" height="18" viewBox="0 0 20 20" fill="none" aria-hidden="true"><path d="M8 5L13 10L8 15" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round"/></svg>'


def manage_tile(href, title, desc="", icon_html="", count=0, tone="info", tile="carbon", num=False):
    """Manage tile row (08 · Manage): colored icon tile, title, one line, count or chevron."""
    n = int(count or 0)
    right = ""
    if num or n:
        right += '<b class=tnum>%02d</b>' % (n if n < 100 else 99)
    if n:
        right += '<span class="mbadge %s">%s</span>' % (_e(tone), n if n < 100 else "99+")
    if not num and not n:
        right += '<span class=mchev aria-hidden=true>%s</span>' % CHEVRON
    return Markup('<a class="mrow mtile %s" href="%s"><span class=mico aria-hidden=true>%s</span><span class=grow><span class=mtitle>%s</span>%s</span>%s</a>' % (
        _e(tile or "carbon"), _e(href), Markup(icon_html or ""), _e(title), ('<span class=mdesc>%s</span>' % _e(desc)) if desc else "", right))


def _social_icon(title):
    t = (title or "").lower()
    if "coffee" in t:
        return "☕"
    if any(k in t for k in ("dinner", "drink", "beer", "bar")):
        return "🍻"
    if any(k in t for k in ("dessert", "ice cream")):
        return "🍦"
    if "potluck" in t or "food" in t:
        return "🍲"
    return "🎉"


def _social_title(title):
    t = str(title or "").strip().rstrip(".")
    for tail in (" before", " after"):
        if t.lower().endswith(tail):
            t = t[: -len(tail)]
    return t


def social_card(card, csrf_html, back="home", clock_label=""):
    """2.0 / Social card (02 H, 2072:3771). Condensed until you join (slim row: icon · when · place · going · Join);
    joining expands it (who's there, Joined, Directions). Condensed cards attach right above/below their practice."""
    when = "BEFORE PRACTICE" if card.get("when") == "before" else "AFTER PRACTICE"
    title = _social_title(card.get("title"))
    place = card.get("place") or ""
    pid = int(card.get("practice_id") or 0)
    form = ('<form method=post action="/practices/%d">%s<input type=hidden name=pid value="%d"><input type=hidden name=back value="%s">'
            % (pid, csrf_html, pid, _e(back)))
    if not card.get("joined"):
        n = len(card.get("people") or [])
        kicker = when + ((" · " + clock_label.upper()) if clock_label else "")
        return Markup('<div class="rg-social cond" data-when="%s"><span class=rg-socicon aria-hidden=true>%s</span>'
                      '<span class=rg-txt><span class=rg-sk>%s</span><b>%s</b><small>%d going</small></span>%s'
                      '<button class=rg-outline name=action value=social_join>Join</button></form></div>'
                      % (_e(card.get("when")), _social_icon(title), _e(kicker), _e(title + (" · " + place if place else "")), n, form))
    live = card.get("live")
    kicker = when + (" · HAPPENING NOW" if live else ((" · " + clock_label.upper()) if clock_label else ""))
    till = ('<span class=rg-live><i></i>Till %s</span>' % _e(clock_label)) if (live and clock_label) else ""
    faces = "".join('<i>%s</i>' % _e(p.get("initials")) for p in (card.get("people") or [])[:3])
    extra = len(card.get("people") or []) - 3
    if extra > 0:
        faces += '<i class=more>+%d</i>' % extra
    addr = card.get("address") or ""
    q = __import__("urllib.parse").parse.quote(addr or place)
    return Markup('<div class="rg-social open" data-when="%s"><div class=rg-sotop><span class=rg-sk>%s</span>%s</div>'
                  '<b class=rg-sotitle>%s.</b><div class=rg-sowhere><b>%s</b><small>%s %s</small></div>'
                  '<div class=rg-sowho><span class=rg-faces>%s</span><span>%s</span></div>'
                  '<div class=rg-soacts>%s<button class=rg-joined name=action value=social_leave>✓ Joined</button></form>'
                  '<a class=rg-outline href="https://www.google.com/maps/search/?api=1&amp;query=%s" target=_blank rel=noopener>↗ Directions</a></div></div>'
                  % (_e(card.get("when")), _e(kicker), till, _e(title), _e(place + (" · " + addr if addr else "")),
                     "Then" if card.get("when") == "before" else "After", _e(card.get("practice") or "practice"),
                     faces, _e(card.get("going_line") or ""), form, q))


def event_cancelled(href, kicker, title, reason=""):
    """Event card · Cancelled (04.01): carbon card, Cancelled chip, struck title, the reason."""
    return Markup('<a class="rg-ecard rg-cancelled tone-carbon" href="%s"><span class=rg-ectop><span class=rg-ek>%s</span>%s</span>'
                  '<b class=rg-ectitle>%s</b>%s</a>' % (_e(href), _e(kicker), chip("Cancelled", "notcleared"), _e(title),
                                                       ('<small class=rg-reason>%s</small>' % _e(reason)) if reason else ""))


def practice_actions(href, label="Chat", count=0, more_href=""):
    """2.0 / Practice actions (02 H, 2143:155580): split Chat button under Going / Not going.
    Main part opens this practice's chat with a lime count; the ▾ part opens the menu (practice chat, ask the coaches)."""
    badge = ('<span class=rg-pabadge>%s</span>' % _e(count)) if count else ""
    more = more_href or href
    return Markup('<div class=rg-pactions><a class=rg-pamain href="%s">%s<span>%s</span>%s</a>'
                  '<a class=rg-pamore href="%s" aria-label="More">%s</a></div>' % (
                      _e(href), icon("chat"), _e(label), badge, _e(more),
                      '<svg width="20" height="20" viewBox="0 0 20 20" fill="none" aria-hidden="true"><path d="M5 8L10 13L15 8" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round"/></svg>'))


def callout(title, sub="", cta="", href="", tone="graphite", onclick=""):
    """Tinted one-line action card ("Need a ride?  Ask →", "Requires USA Water Polo + club waiver  Once")."""
    inner = '<span class=rg-txt><b>%s</b>%s</span>%s' % (_e(title), ('<small>%s</small>' % _e(sub)) if sub else "",
                                                        ('<span class=rg-pill>%s</span>' % _e(cta)) if cta else "")
    klass = "rg-callout tone-%s" % _tone(tone)
    if href:
        return Markup('<a class="%s" href="%s">%s</a>' % (klass, _e(href), inner))
    return Markup('<button type=button class="%s"%s>%s</button>' % (klass, (' onclick="%s"' % _e(onclick)) if onclick else "", inner))


def metric(value, label, tone="carbon"):
    """2.0 / Metric."""
    return Markup('<div class="rg-metric tone-%s"><b>%s</b><span>%s</span></div>' % (_tone(tone, "carbon"), _e(value), _e(label)))


def info(kicker, body):
    """2.0 / Info block."""
    return Markup('<div class=rg-info><span>%s</span><b>%s</b></div>' % (_e(kicker), _e(body)))


def empty(title, body="", cta="", href="", big="00"):
    """2.0 / Empty state."""
    btn = ('<a class="btn btn-primary" href="%s">%s</a>' % (_e(href), _e(cta))) if cta else ""
    return Markup('<div class=rg-empty><b class=rg-big>%s</b><h2>%s</h2>%s%s</div>' % (
        _e(big), _e(title), ('<p>%s</p>' % _e(body)) if body else "", btn))


def checklist(title, steps, done_label=""):
    """Finish-setup style checklist card: [(label, done, href)]."""
    done = sum(1 for s in steps if s[1])
    rows = "".join('<a class="rg-step%s" href="%s"><span class=rg-tick>%s</span><b>%s</b>%s</a>' % (
        " ok" if ok else "", _e(href or "#"), "✓" if ok else "", _e(label), "" if ok else '<span class=rg-chev aria-hidden=true>›</span>')
        for label, ok, href in steps)
    return Markup('<div class=rg-check><div class=rg-checkhead><b>%s</b>%s</div>%s</div>' % (
        _e(title), chip("%d of %d" % (done, len(steps)), "neutral"), rows))


def jinja_globals():
    return dict(rg_icon=icon, rg_chip=chip, rg_head=head, rg_section=section, rg_seg=seg, rg_filters=filters, rg_day=day, rg_label=label,
                rg_event=event_line, rg_event_line=event_line, rg_event_row=event_row, rg_event_card=event_card, rg_row=row, rg_callout=callout, rg_metric=metric,
                rg_info=info, rg_empty=empty, rg_manage_tile=manage_tile, rg_social_card=social_card, rg_practice_actions=practice_actions, rg_event_cancelled=event_cancelled, rg_checklist=checklist, event_tone=event_tone)
