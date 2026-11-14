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
    svg = ui.nav_icon(name).replace('class="nav3-glyph"', 'class="rg-glyph"')
    return Markup('<span class="rg-ic rg-ic-%s" aria-hidden=true>%s</span>' % (size if size in ("sm", "md", "lg") else "md", svg))


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


def section_count(title, count=None, action_label="", action_href="", action_attrs="", chevron=False):
    """2.0 / Section header with the small (04) count, Figma 62 style. Action is an Edit / + Add link or button."""
    sup = ('<sup>(%s)</sup>' % (("%02d" % count) if isinstance(count, int) and count < 10 and count >= 0 else _e(count))) if count is not None else ""
    act = ""
    if action_label:
        lab = _e(action_label) + (Markup(icon("chevron_right", "sm")) if chevron else "")
        act = ('<a class=rg-secact href="%s"%s>%s</a>' % (_e(action_href), (" " + action_attrs) if action_attrs else "", lab)) if action_href \
            else '<button type=button class=rg-secact%s>%s</button>' % ((" " + action_attrs) if action_attrs else "", lab)
    return Markup('<div class=rg-sec><h2>%s%s</h2>%s</div>' % (_e(title), sup, act))


def seg(items, current):
    """2.0 / Segmented control. items = [(key, label, href)]; selected is paper."""
    return Markup('<nav class=rg-seg data-seg aria-label=View>%s</nav>' % "".join(
        '<a href="%s"%s>%s</a>' % (_e(h), ' class=on aria-current=page' if k == current else "", _e(l)) for k, l, h in items))


def seg_choice(name, items, value, autosubmit=False):
    """2.0 / Segmented control as a form field. items = [(value, label)]. Radios, so it works without JS
    and is keyboard-accessible; autosubmit saves on change (settings rows)."""
    opts = "".join('<label><input type=radio name="%s" value="%s"%s%s><span>%s</span></label>' % (
        _e(name), _e(v), " checked" if v == value else "", " onchange=this.form.requestSubmit()" if autosubmit else "", _e(l))
        for v, l in items)
    return Markup('<div class="rg-seg rg-segform" role=radiogroup>%s</div>' % opts)


def map_unavailable(line="We can't show the map right now.", sub="Your week is below. Open a practice for directions.",
                    href="/practices?view=list", link="See the schedule"):
    """2.0 / Map unavailable (359:1185): big ghost "No map." over the map area, one line, one link."""
    return Markup('<section class=rg-mapmiss data-r2="map-unavailable" role=status>'
                  '<span class=rg-mapmiss-big aria-hidden=true>No<br>map.</span>'
                  '<b>%s</b><small>%s</small>%s</section>' % (
                      _e(line), _e(sub), ('<a href="%s">%s</a>' % (_e(href), _e(link))) if href else ""))


def filters(items, current):
    """Type filters. items = [(key, label, href)]; selected is lime."""
    return Markup('<nav class=rg-filters data-seg aria-label=Filter>%s</nav>' % "".join(
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


def social_card(card, csrf_html, back="home", clock_label="", expanded=False):
    """2.0 / Social card (02 H, 2072:3771). Condensed until you join (slim row: icon · when · place · going · Join);
    joining expands it (who's there, Joined, Directions). Condensed cards attach right above/below their practice."""
    when = "BEFORE PRACTICE" if card.get("when") == "before" else "AFTER PRACTICE"
    title = _social_title(card.get("title"))
    place = card.get("place") or ""
    pid = int(card.get("practice_id") or 0)
    form = ('<form method=post action="/practices/%d">%s<input type=hidden name=pid value="%d"><input type=hidden name=back value="%s"><input type=hidden name=slot value="%d">'
            % (pid, csrf_html, pid, _e(back), int(card.get("slot") or 1)))
    if not card.get("joined") and not expanded:
        n = len(card.get("people") or [])
        kicker = when + ((" · " + clock_label.upper()) if clock_label else "")
        # Condensed (Nov 13 redesign): the kicker gets the full width, the title wraps instead of truncating,
        # and "N going" + Join share their own row, so nothing collides at 320px.
        return Markup('<div class="rg-social cond" data-social="%d-%d" data-when="%s"><span class=rg-socicon aria-hidden=true>%s</span>'
                      '<span class=rg-txt><span class=rg-sk>%s</span><b>%s</b>'
                      '<span class=rg-someta><small>%d going</small>%s<button class=rg-outline name=action value=social_join>Join</button></form></span></span></div>'
                      % (pid, int(card.get("slot") or 1), _e(card.get("when")), _social_icon(title), _e(kicker), _e(title + (" · " + place if place else "")), n, form))
    live = card.get("live")
    kicker = when + (" · HAPPENING NOW" if live else ((" · " + clock_label.upper()) if clock_label else ""))
    till = ('<span class=rg-live><i></i>Till %s</span>' % _e(clock_label)) if (live and clock_label) else ""
    faces = "".join('<i>%s</i>' % _e(p.get("initials")) for p in (card.get("people") or [])[:3])
    extra = len(card.get("people") or []) - 3
    if extra > 0:
        faces += '<i class=more>+%d</i>' % extra
    addr = card.get("address") or ""
    q = __import__("urllib.parse").parse.quote(addr or place)
    return Markup('<div class="rg-social open" data-social="%d-%d" data-when="%s"><div class=rg-sotop><span class=rg-sk>%s</span>%s</div>'
                  '<b class=rg-sotitle>%s.</b><div class=rg-sowhere><b>%s</b><small>%s %s</small></div>'
                  '<div class=rg-sowho><span class=rg-faces>%s</span><span>%s</span></div>'
                  '<div class=rg-soacts>%s%s</form>'
                  '<a class=rg-outline href="https://www.google.com/maps/search/?api=1&amp;query=%s" target=_blank rel=noopener>↗ Directions</a></div></div>'
                  % (pid, int(card.get("slot") or 1), _e(card.get("when")), _e(kicker), till, _e(title), _e(place + (" · " + addr if addr else "")),
                     "Then" if card.get("when") == "before" else "After", _e(card.get("practice") or "practice"),
                     faces, _e(card.get("going_line") or ("%d going" % len(card.get("people") or []))), form,
                     ('<button class=rg-joined name=action value=social_leave><svg width=16 height=16 viewBox="0 0 20 20" fill=none aria-hidden=true><path d="M4.5 10.5L8.25 14.25L15.5 6.5" stroke=currentColor stroke-width=2 stroke-linecap=round stroke-linejoin=round/></svg><span>Joined</span></button>'
                      if card.get("joined") else '<button class=rg-outline name=action value=social_join>I\'m coming</button>'), q))


def event_cancelled(href, kicker, title, reason=""):
    """Event card · Cancelled (04.01): carbon card, Cancelled chip, struck title, the reason."""
    return Markup('<a class="rg-ecard rg-cancelled tone-carbon" href="%s"><span class=rg-ectop><span class=rg-ek>%s</span>%s</span>'
                  '<b class=rg-ectitle>%s</b>%s</a>' % (_e(href), _e(kicker), chip("Cancelled", "notcleared"), _e(title),
                                                       ('<small class=rg-reason>%s</small>' % _e(reason)) if reason else ""))


def practice_actions(href, label="Practice Chat", count=0, more_href=""):
    """2.0 / Practice actions (02 H, 2143:155580): full-width Practice Chat button under Going / Not going.
    The split menu (the down-arrow half) is parked until it has real options; more_href is kept for callers."""
    badge = ('<span class=rg-pabadge>%s</span>' % _e(count)) if count else ""
    return Markup('<div class=rg-pactions><a class=rg-pamain href="%s">%s<span>%s</span>%s</a></div>' % (
        _e(href), icon("chat"), _e(label), badge))


def search_field(input_id, placeholder, action_href="", action_icon="settings", clear_id=""):
    """2.0 / Search field (02 C, 349:617): graphite pill, search icon, input, lime round action."""
    clear = ('<button type=button class=rg-sclear id="%s" hidden aria-label="Clear search">×</button>' % _e(clear_id)) if clear_id else ""
    act = ('<a class=rg-sact href="%s" aria-label="Settings">%s</a>' % (_e(action_href), icon(action_icon, "sm"))) if action_href else ""
    return Markup('<label class=rg-search>%s<input id="%s" type=search enterkeyhint=search placeholder="%s" autocomplete=off autocapitalize=off>%s%s</label>'
                  % (icon("search"), _e(input_id), _e(placeholder), clear, act))


def stat_card(label, value, delta="", bars=()):
    """2.0 / Stat card (02 D, 350:825): label + delta, 128px value, 7 day bars (highest is lime)."""
    bars = list(bars)
    top = max([b[1] for b in bars] or [0])
    cols = "".join('<span class=rg-bar><i style="height:%dpx"%s></i><small>%s</small></span>' % (
        (max(8, int(120 * (v / top))) if v else 4) if top else 4, ' class=hi' if top and v == top else "", _e(lab)) for lab, v in bars)
    return Markup('<div class=rg-stat><div class=rg-stattop><span>%s</span>%s</div><b class=rg-statval>%s</b>%s</div>' % (
        _e(label), ('<em>%s</em>' % _e(delta)) if delta else "", _e(value), ('<div class=rg-bars>%s</div>' % cols) if bars else ""))


def _nice_ticks(vmax, n=3):
    """0..top in n steps of a 1/2/5 step, top >= vmax. Integer counts only."""
    vmax = max(1, int(vmax or 0))
    step = 1
    for base in (1, 2, 5, 10, 20, 25, 50, 100, 200, 250, 500, 1000):
        if base * n >= vmax:
            step = base; break
    else:
        step = -(-vmax // n)
    return [step * i for i in range(max(2, -(-vmax // step)) + 1)]


def chart_switch(views, card_id="mgrChart"):
    """2.0 / Chart card (02 Components · Membership): one card, dots top-right switch views.
    Each view: {key, kicker, value, title, sub, bars:[{label, segs:[n,...], tip}], series:[(name, count)], empty}.
    Bars stand on a 0 baseline with 3 gridlines labelled on the right; series colors come from --cc-1/--cc-2."""
    dots = "".join('<button type=button role=tab class=rg-ccdot aria-selected="%s" aria-controls="%s-%s" aria-label="%s" data-cc="%s"></button>' % (
        "true" if i == 0 else "false", _e(card_id), _e(v["key"]), _e(v["title"]), _e(v["key"])) for i, v in enumerate(views))
    panes = []
    for i, v in enumerate(views):
        bars = v.get("bars") or []
        totals = [sum(b["segs"]) for b in bars]
        ticks = _nice_ticks(max(totals or [0])) if any(totals) else [0]
        top = ticks[-1] or 1
        grid = "".join('<i style="bottom:%.2f%%"><small>%d</small></i>' % (100.0 * t / top, t) for t in ticks)
        cols = []
        for b, tot in zip(bars, totals):
            segs = "".join('<span class="rg-ccseg s%d" style="height:%.2f%%"></span>' % (k + 1, 100.0 * n / tot) for k, n in enumerate(b["segs"]) if n) if tot else ""
            cols.append('<button type=button class=rg-cccol data-tip="%s" aria-label="%s"><span class="rg-ccstack%s" style="height:%.2f%%">%s</span></button>' % (
                _e(b["tip"]), _e(b["tip"]), "" if tot else " zero", (100.0 * tot / top) if tot else 0, segs))
        xs = "".join("<span>%s</span>" % _e(b["label"]) for b in bars)
        series = v.get("series") or []
        legend = ('<ul class=rg-cclegend>%s</ul>' % "".join('<li><i class=s%d></i><span>%s</span><b>%s</b></li>' % (k + 1, _e(name), _e(n)) for k, (name, n) in enumerate(series))) if len(series) > 1 else ""
        rows = "".join("<tr><th scope=row>%s</th>%s</tr>" % (_e(b["label"]), "".join("<td>%d</td>" % n for n in b["segs"])) for b in bars)
        head = "".join("<th scope=col>%s</th>" % _e(name) for name, _n in series) or "<th scope=col>%s</th>" % _e(v["title"])
        table = '<table class=rg-srtable><caption>%s</caption><thead><tr><th></th>%s</tr></thead><tbody>%s</tbody></table>' % (_e(v["title"]), head, rows)
        plot = ('<div class=rg-ccplot><div class=rg-ccgrid aria-hidden=true>%s</div><div class=rg-cccols style="--n:%d">%s</div></div><div class=rg-ccx aria-hidden=true style="--n:%d">%s</div>' % (
            grid, max(1, len(bars)), "".join(cols), max(1, len(bars)), xs)) if bars else '<p class=ty-muted>%s</p>' % _e(v.get("empty") or "Nothing yet.")
        panes.append('<div class=rg-ccview id="%s-%s" role=tabpanel data-cc="%s"%s><p class=ty-caps>%s</p>'
                     '<div class=rg-cchero><b>%s</b><span><b>%s</b><small>%s</small></span></div>%s%s'
                     '<p class=rg-cctip aria-live=polite>%s</p>%s</div>' % (
            _e(card_id), _e(v["key"]), _e(v["key"]), "" if i == 0 else " hidden", _e(v["kicker"]), _e(v["value"]), _e(v["title"]), _e(v["sub"]),
            plot, legend, "Tap a bar for its numbers" if bars else "", table))
    dotbar = ('<div class=rg-ccdots role=tablist aria-label="Charts">%s</div>' % dots) if len(views) > 1 else ""
    return Markup('<section class=rg-chartcard id="%s" data-chartcard>%s%s</section>' % (_e(card_id), dotbar, "".join(panes)))


def hub_tile(href, count, title, desc, tone="sun"):
    """Manage hub tile (08.13): colored 200px tile, big count + arrow, title, one line."""
    return Markup('<a class="rg-hub tone-%s" href="%s"><span class=rg-hubtop><b>%02d</b><i aria-hidden=true>→</i></span>'
                  '<span class=rg-hubtxt><b>%s</b><small>%s</small></span></a>' % (_tone(tone, "sun"), _e(href), int(count or 0), _e(title), _e(desc)))


def stack_tile(href, title, sub, count, tone="sun"):
    """2.0 / People / List stack tile (08 · 2015:10275): colored tile, display title, one line, big two-digit count.
    Tiles in an .rg-tilestack overlap like a deck."""
    right = ('<b class=rg-tilen>%02d</b>' % int(count)) if count is not None else '<b class="rg-tilen arrow" aria-hidden=true>→</b>'
    return Markup('<a class="rg-tile tone-%s" href="%s"><span class=rg-txt><b>%s</b><small>%s</small></span>%s</a>'
                  % (_tone(tone, "sun"), _e(href), _e(title), _e(sub), right))


DECK_TONES = ("sun", "sky", "tangerine", "lavender", "lime", "aqua", "mango", "bubblegum", "cobalt", "grape")


def count_chips(items):
    """Count chips row (2.0 / Participants: TOTAL · VERIFIED · PENDING · EXPIRED · UNKNOWN). items = [(n, label, tone)]."""
    return Markup('<div class=rg-counts>%s</div>' % "".join(
        '<span class="rg-cnt tone-%s"><b>%02d</b><small>%s</small></span>' % (_tone(t, "graphite"), int(n or 0), _e(l)) for n, l, t in items))


def callout(title, sub="", cta="", href="", tone="graphite", onclick=""):
    """Tinted one-line action card ("Need a ride?  Ask →", "Requires USA Water Polo + club waiver  Once")."""
    inner = '<span class=rg-txt><b>%s</b>%s</span>%s' % (_e(title), ('<small>%s</small>' % _e(sub)) if sub else "",
                                                        ('<span class=rg-pill>%s</span>' % _e(cta)) if cta else "")
    klass = "rg-callout tone-%s" % _tone(tone)
    if href:
        return Markup('<a class="%s" href="%s">%s</a>' % (klass, _e(href), inner))
    return Markup('<button type=button class="%s"%s>%s</button>' % (klass, (' onclick="%s"' % _e(onclick)) if onclick else "", inner))


def callout_card(title, body="", cta="", cta_id="", link="", link_href="", tone="lavender", card_id="", extra="", hidden=False):
    """2.0 / Callout (Audit PROPOSED 2376:91): tinted block with a title, body, one ink CTA and an optional link.
    Tone lavender for an ask, graphite for a blocked / informational state. `extra` is trusted Markup (hints the JS toggles)."""
    return Markup('<section class="rg-calloutcard tone-%s"%s%s><b>%s</b>%s%s%s%s</section>' % (
        _tone(tone, "lavender"), (' id="%s"' % _e(card_id)) if card_id else "", " hidden" if hidden else "", _e(title),
        ('<p>%s</p>' % _e(body)) if body else "", extra or "",
        ('<button type=button class=rg-cta%s>%s</button>' % ((' id="%s"' % _e(cta_id)) if cta_id else "", _e(cta))) if cta else "",
        ('<a class=rg-calink href="%s">%s</a>' % (_e(link_href), _e(link))) if link else ""))


def usawp_card(csrf_html, show_trial=True, trial_url="", action="/home"):
    """/home USAWP card (Audit 03, AFTER): title, number field, Save, and the 2-week trial with its confirm sheet.
    Posts to /home exactly like the v1 card (usawp_number, action=trial)."""
    trial = ""
    if show_trial:
        trial = ('<button type=button class="rg-btn secondary" data-open-dialog=trialDialog>2-week USAWP trial</button>'
                 '<dialog id=trialDialog class=modal><div class=sheet>'
                 '<p>I will complete the USA Water Polo 2-week trial membership before I get in the pool. I understand I need to '
                 'get a full USAWP membership soon, otherwise I will not be able to practice.</p>'
                 '<form method=post action="%s">%s<input type=hidden name=action value=trial>'
                 '<button class="rg-btn primary">I confirm</button></form>'
                 '<a class="rg-btn secondary" href="%s" target=_blank rel=noopener>Get USAWP trial membership</a>'
                 '</div></dialog>') % (_e(action), csrf_html, _e(trial_url))
    return Markup('<section class="rg-usawp numcard"><b>Enter your USAWP membership number</b>'
                  '<form method=post action="%s">%s<label class=rg-field><span>USAWP Membership #</span>'
                  '<input name=usawp_number inputmode=numeric autocomplete=off pattern="[0-9]{4,10}" required></label>%s'
                  '<button class="rg-btn primary">Save</button></form>%s</section>' % (_e(action), csrf_html, membership_sex(), trial))


def ride_row(name, sub, initials, tone="sky", right=""):
    """04.18 ride board row: avatar, name, area line, and a right slot (seats count or an Offer / Pick up button).
    `right` is trusted Markup built by the caller."""
    return Markup('<div class="rg-row rg-person rg-ride tone-%s"><span class="rg-lead tone-%s">%s</span>'
                  '<span class=rg-txt><b>%s</b><small>%s</small></span>%s</div>' % (
                      _tone(tone, "sky"), _tone(tone, "sky"), _e(initials), _e(name), _e(sub), right or ""))


def ride_pick(pid, req_id, csrf_html, label="Pick up"):
    """Ride board: the driver's one-tap Pick up for an open request (posts action=pick, returns to the board)."""
    return Markup('<form method=post action="/practices/%d/rides">%s<input type=hidden name=next value=board>'
                  '<input type=hidden name=req_id value="%d"><button class="rg-btn ink" name=action value=pick>%s</button></form>'
                  % (int(pid), csrf_html, int(req_id), _e(label)))


def week_grid(blocks, label="Your week"):
    """09.06 / 09.07 week grid: Mon–Sun columns, 6a–11p rows. blocks = [{col, top, h, cls, title}] (percent geometry).
    Each block keeps a text title for screen readers and hover; the list beside the grid is the table view."""
    hours = "".join('<span style="top:%.2f%%">%s</span>' % ((h - 6) / 17 * 100, lab)
                    for h, lab in ((6, "6a"), (9, "9a"), (12, "12p"), (15, "3p"), (18, "6p"), (21, "9p")))
    cols = "".join('<b>%s</b>' % x for x in ("M", "T", "W", "T", "F", "S", "S"))
    marks = "".join('<i class="%s" style="--c:%d;top:%.2f%%;height:%.2f%%" title="%s"></i>' % (
        _e(b.get("cls", "free")), int(b["col"]), b["top"], b["h"], _e(b.get("title", ""))) for b in blocks)
    return Markup('<figure class=rg-week role=img aria-label="%s"><div class=rg-weekhead>%s</div>'
                  '<div class=rg-weekbody><div class=rg-weekhours>%s</div><div class=rg-weekcols>%s</div></div></figure>'
                  % (_e(label), cols, hours, marks))


def metric(value, label, tone="carbon", href="", on=False):
    """2.0 / Metric. With href it's a filter tile (Figma 62 S1 2×2): the picked one gets a ring."""
    inner = '<b>%s</b><span>%s</span>' % (_e(value), _e(label))
    if href:
        return Markup('<a class="rg-metric tone-%s%s" href="%s"%s>%s</a>' % (_tone(tone, "carbon"), " on" if on else "", _e(href), ' aria-current=true' if on else "", inner))
    return Markup('<div class="rg-metric tone-%s">%s</div>' % (_tone(tone, "carbon"), inner))


def info(kicker, body, href="", attrs=""):
    """2.0 / Info block. With href the whole block is the link (e.g. tap a location to open Maps)."""
    if href:
        return Markup('<a class="rg-info link" href="%s"%s><span>%s</span><b>%s</b>%s</a>' % (
            _e(href), (" " + attrs) if attrs else "", _e(kicker), _e(body), icon("chevron_right", "sm")))
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
        " ok" if ok else "", _e(href or "#"), _CHECK if ok else "", _e(label), "" if ok else '<span class=rg-chev aria-hidden=true>›</span>')
        for label, ok, href in steps)
    return Markup('<div class=rg-check><div class=rg-checkhead><b>%s</b>%s</div>%s</div>' % (
        _e(title), chip("%d of %d" % (done, len(steps)), "neutral"), rows))


def checkin_hero(n, total, title="", when="", tone="sun", href=""):
    """2.0 / R5 Check-in hero (08.09): event-tone card, big n/total, 'checked in', the event underneath."""
    tone = tone if tone in TONES else "sun"
    tag = "a" if href else "div"
    sub = " · ".join(x for x in (title, when) if x)
    return Markup('<%s class="rg-cihero tone-%s"%s><b class=rg-cinum>%s/%s</b><span class=rg-cilbl><b>checked in</b>%s</span></%s>' % (
        tag, tone, (' href="%s"' % _e(href)) if href else "", _e(n), _e(total),
        ('<small>%s</small>' % _e(sub)) if sub else "", tag))


def checkin_row(name, href, sub, fields, checked=False, hold="", pick=""):
    """2.0 / R5 Check-in row (08.09, 08.70). One row per athlete; the pill on the right is the action.
    checked: 'In' pill (tap to undo). hold: graphite row + 'Hold' pill that confirms first.
    pick: sun-outlined row + sun pill with what they picked (Drop-in, Pass, Trial). Otherwise a lime 'Check in' pill.
    fields: the hidden inputs (csrf, member id, date...) for the form."""
    if checked:
        cls, btn = "", '<button class="rg-cipill in" name=action value=undo title="Undo check-in" aria-label="Checked in. Tap to undo">%s<span>In</span></button>' % _CHECK
    elif hold:
        cls, btn = " hold", '<button class="rg-cipill hold" data-confirm="%s. Check in anyway?">Hold</button>' % _e(hold)
    elif pick:
        cls, btn = " pick", '<button class="rg-cipill pick" title="Check in">%s</button>' % _e(pick)
    else:
        cls, btn = "", '<button class="rg-cipill go">Check in</button>'
    nm = ('<a href="%s">%s</a>' % (_e(href), _e(name))) if href else _e(name)
    return Markup('<div class="rg-cirow%s"><div class=rg-citext><b>%s</b><small>%s</small></div><form method=post>%s%s</form></div>' % (
        cls, nm, _e(sub), fields, btn))


_BACK = '<svg width="24" height="24" viewBox="0 0 256 256" fill="currentColor" aria-hidden="true"><path d="M224,128a8,8,0,0,1-8,8H59.31l58.35,58.34a8,8,0,0,1-11.32,11.32l-72-72a8,8,0,0,1,0-11.32l72-72a8,8,0,0,1,11.32,11.32L59.31,120H216A8,8,0,0,1,224,128Z"/></svg>'


def back_button(href, label="Back"):
    """Back circle (graphite 44px, arrow) that sits above a sub-page title."""
    return Markup('<a class=rg-back href="%s" aria-label="%s">%s</a>' % (_e(href), _e(label), _BACK))


def event_hero(kind, title, line="", tone="lavender", status=""):
    """2.0 / Lineup event hero (07.18, 07.07): tone card, ink type chip, display title with a period, when · where."""
    t = str(title or "").strip()
    t = t if t.endswith((".", "!", "?")) else t + "."
    return Markup('<div class="rg-evhero tone-%s"><div class=rg-evtop><span class=rg-evkind>%s</span>%s</div><h1 class=rg-evtitle>%s</h1>%s</div>' % (
        _tone(tone, "lavender"), _e(kind or "Event"), ('<span class=rg-evstatus>%s</span>' % _e(status)) if status else "", _e(t),
        ('<p class=rg-evline>%s</p>' % _e(line)) if line else ""))


def plus_button(href, label="Add", dialog=""):
    """Header plus (06 Chat list): lime 52px circle, top right of a display title. Chat, Schedule, Lineup.
    dialog opens a slide-up instead (href stays as the no-JS fallback)."""
    extra = (' data-open-dialog="%s"' % _e(dialog)) if dialog else ""
    return Markup('<a class="chatplus rg-plus" href="%s"%s aria-label="%s" title="%s"><svg width="24" height="24" viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M12 5v14M5 12h14" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"/></svg></a>' % (_e(href), extra, _e(label), _e(label)))


def top_bar(type="compact", title="", eyebrow="", back_href="", back_label="", action_href="", action_icon="plus",
            action_label="", avatar_html="", action_html="", back_button=False):
    """2.0 / Top bar (02, 353:648). Props mirror Figma: Type (large | compact), Title, Eyebrow, Show back, Show action,
    Show avatar. Back is always a link to the canonical parent (nav.parent_url), never history.
    Compact: ‹ disc + the parent's title (the page's own large heading follows in the body).
    Large: actions row, then eyebrow + 56px title. Only roots show the avatar."""
    if back_button:
        back_href = ""
    back = ('<button type=button class=rg-tbdisc data-sheetdone aria-label="Back to %s">%s</button>' % (_e(back_label or title), icon("chevron_left"))) if back_button else ('<a class=rg-tbdisc href="%s" aria-label="Back to %s">%s</a>' % (_e(back_href), _e(back_label or title), icon("chevron_left"))) if back_href else ""
    act = action_html or (('<a class=rg-tbdisc href="%s" aria-label="%s">%s</a>' % (_e(action_href), _e(action_label or "Add"), icon(action_icon))) if action_href else "")
    avatar = ('<span class=rg-tbavatar>%s</span>' % avatar_html) if avatar_html else ""
    if type == "large":
        head = '<div class=rg-tbhead>%s<h1 class=rg-tbtitle>%s</h1></div>' % (('<p class=rg-tbeyebrow>%s</p>' % _e(eyebrow)) if eyebrow else "", _e(title))
        return Markup('<header class="rg-topbar large"><div class=rg-tbrow>%s<span class=rg-tbspace></span>%s%s</div>%s</header>' % (back, act, avatar, head))
    label = '<a class=rg-tbtitle href="%s">%s</a>' % (_e(back_href), _e(title)) if back_href else '<span class=rg-tbtitle>%s</span>' % _e(title)
    return Markup('<header class="rg-topbar compact"><div class=rg-tbrow>%s%s<span class=rg-tbspace></span>%s%s</div></header>' % (back, label, act, avatar))


def sheet_head(title, close_href):
    """Task header (Figma 60 rule 7): ✕ close (a link to the page the task sits on) + the task title. No back."""
    return Markup('<header class="rg-topbar compact rg-sheethead"><div class=rg-tbrow><a class=rg-tbdisc href="%s" aria-label="Close">%s</a>'
                  '<span class=rg-tbtitle>%s</span></div></header>' % (_e(close_href), icon("close"), _e(title)))


def button(label, type="primary", href="", name="", value="", icon_name="", disabled=False, submit=True, attrs=""):
    """2.0 / Button (02, 349:500). Types: primary (lime) | ink | secondary (graphite) | ghost | danger | sun."""
    ic = icon(icon_name) if icon_name else ""
    cls = "rg-btn %s" % type
    if href and not disabled:
        return Markup('<a class="%s" href="%s"%s>%s<span>%s</span></a>' % (cls, _e(href), (" " + attrs) if attrs else "", ic, _e(label)))
    nv = (' name="%s" value="%s"' % (_e(name), _e(value))) if name else ""
    return Markup('<button class="%s" type=%s%s%s%s>%s<span>%s</span></button>' % (
        cls, "submit" if submit else "button", nv, " disabled" if disabled else "", (" " + attrs) if attrs else "", ic, _e(label)))


def settings_row(label, value="", href="", attrs="", live=""):
    """2.0 / List row · Type=Settings (02, 350:849): carbon pill, bold label, smoke value, chevron.
    live names the value so an autosave can update it in place."""
    inner = '<span class=rg-srlabel>%s</span>%s%s' % (_e(label), ('<span class=rg-srvalue%s>%s</span>' % ((' data-live="%s"' % _e(live)) if live else "", _e(value))) if value else "",
                                                     icon("chevron_right", "sm") if href else "")
    return Markup(_tag(href, "rg-srow", inner, (" " + attrs) if attrs else "") if href else '<div class=rg-srow%s>%s</div>' % ((" " + attrs) if attrs else "", inner))


def page_title(title, sub="", actions=""):
    """The large heading under a compact Top bar (Figma 60: the large heading names the current page)."""
    t = _e(title)
    if t and not t.endswith((".", "?", "!")):
        t = t + "."
    return Markup('<div class=rg-pagetitle><h1 class=rg-pt>%s</h1>%s%s</div>' % (
        t, ('<p class=rg-ptsub>%s</p>' % _e(sub)) if sub else "", ('<div class=rg-ptacts>%s</div>' % actions) if actions else ""))


def qr_card(title, sub, img_src="", url="", filename="qr.svg", note=""):
    """Tools › QR codes (Figma 61 · M4.2): one code per card, Download + Share. note replaces the code when it isn't ready."""
    if not img_src:
        return Markup('<section class=rg-qrcard><b class=rg-qrtitle>%s</b><p class=ty-muted>%s</p><p class="ty-muted ty-sm">%s</p></section>' % (_e(title), _e(sub), note))
    return Markup('<section class=rg-qrcard><div class=rg-qrimg><img src="%s" alt="%s QR code" width=200 height=200></div>'
                  '<b class=rg-qrtitle>%s</b><p class=ty-muted>%s</p><p class="ty-muted ty-sm rg-qrurl">%s</p>'
                  '<div class=rg-qracts><a class="rg-btn secondary" href="%s" download="%s">Download</a>'
                  '<button type=button class="rg-btn secondary" data-share-text="%s">Share</button></div>'
                  '<small class=ty-muted data-share-note hidden></small></section>' % (
                      _e(img_src), _e(title), _e(title), _e(sub), _e(url), _e(img_src), _e(filename), _e(url)))


def toggle(name, label, sub="", checked=False, value="1", attrs="", plain=False):
    """2.0 / Toggle row (02): carbon row, bold label, caption, lime switch. plain = no row fill (Figma 63 sheets)."""
    return Markup(('<label class="rg-toggle plain">' if plain else '<label class=rg-toggle>') + '<span><b>%s</b>%s</span><input type=checkbox name="%s" value="%s"%s%s><i aria-hidden=true></i></label>' % (
        _e(label), ('<small>%s</small>' % _e(sub)) if sub else "", _e(name), _e(value), " checked" if checked else "", (" " + attrs) if attrs else ""))


def choice(name, value, title, sub="", checked=False, type="radio", attrs=""):
    """2.0 / Choice row (Figma M5.2 picker, M5.3 checkboxes): title + caption, lime ring when chosen."""
    return Markup('<label class="rg-choice %s"><input type=%s name="%s" value="%s"%s%s><span class=rg-txt><b>%s</b>%s</span><i aria-hidden=true></i></label>' % (
        _e(type), "checkbox" if type == "checkbox" else "radio", _e(name), _e(value), " checked" if checked else "", (" " + attrs) if attrs else "",
        _e(title), ('<small>%s</small>' % _e(sub)) if sub else ""))


def info_block(kicker, title, sub=""):
    """2.0 / Info block (Figma M5.4): caps kicker, bold line, caption, on carbon."""
    return Markup('<div class=rg-infoblock><span class=ty-caps>%s</span><b>%s</b>%s</div>' % (_e(kicker), _e(title), ('<small>%s</small>' % _e(sub)) if sub else ""))


def status_toggle(name, live, title, sub="", live_label="Live", off_label="Off", attrs=""):
    """2.0 / Status (Figma 62 W1): Live/Off chip over a bold line and caption, with the lime switch."""
    return Markup('<label class="rg-toggle rg-status"><span>%s<b>%s</b>%s</span><input type=checkbox name="%s" value=1%s%s><i aria-hidden=true></i></label>' % (
        str(chip(live_label if live else off_label, "going" if live else "neutral")), _e(title), ('<small>%s</small>' % _e(sub)) if sub else "",
        _e(name), " checked" if live else "", (" " + attrs) if attrs else ""))


def choice_chips(name, items, selected=(), multi=False, attrs=""):
    """Chip set as form inputs (Figma 62: platform, tabs, audience, timing). Lime when picked. items = [(value, label)]."""
    sel = set(selected if isinstance(selected, (list, tuple, set)) else [selected])
    kind = "checkbox" if multi else "radio"
    return Markup('<div class=rg-chipset role=%s%s>%s</div>' % ("group" if multi else "radiogroup", (" " + attrs) if attrs else "", "".join(
        '<label><input type=%s name="%s" value="%s"%s><span>%s</span></label>' % (kind, _e(name), _e(v), " checked" if v in sel else "", _e(l))
        for v, l in items)))


def code_block(text, block_id=""):
    """Short code preview (Figma 62 W2): ink box, lime mono text, a few lines."""
    return Markup('<pre class=rg-code%s><code>%s</code></pre>' % ((' id="%s"' % _e(block_id)) if block_id else "", _e(text)))


def steps(items):
    """Numbered steps (Figma 62 W2)."""
    return Markup('<ol class=rg-steps>%s</ol>' % "".join('<li>%s</li>' % _e(t) for t in items))


def block_row(title, sub="", action="Edit", attrs="", handle=True):
    """Builder block row (Figma 62 E3): grip, title + one line, lime action on the right. A button so the whole row opens the sheet."""
    return Markup('<button type=button class=rg-block%s>%s<span class=rg-txt><b>%s</b>%s</span><span class=rg-blockact>%s</span></button>' % (
        (" " + attrs) if attrs else "", '<span class=rg-grip aria-hidden=true>⠿</span>' if handle else "", _e(title),
        ('<small>%s</small>' % _e(sub)) if sub else "", _e(action)))


def brand_mark(label="regulars"):
    """Icon mark + wordmark set in type (Figma 10 · pre-auth): lime mark in dark, ink in light."""
    return Markup('<span class=rg-brand><i class=rg-brandmark aria-hidden=true></i><b>%s</b></span>' % _e(label))


def auth_head(title, sub="", big=False):
    """Pre-auth header (Figma 10.02 / 10.07): icon mark + wordmark, then the display title.
    big = the Log in treatment ("Log / in." over two lines)."""
    t = _e(title)
    if t and not t.endswith((".", "?", "!")):
        t = t + "."
    if big and " " in t:
        first, rest = t.split(" ", 1)
        t = Markup("%s<br>%s" % (first, rest))
    return Markup('<div class=rg-authhead>%s<h1 class="rg-authtitle%s">%s</h1>%s</div>' % (
        brand_mark(), " xl" if big else "", t, ('<p class=rg-authsub>%s</p>' % _e(sub)) if sub else ""))


def notice(title, body="", tone="lime", icon_name="check", dismiss=True):
    """2.0 / Notice (Figma 10.03 Link sent): colored banner, round ink icon, title + body, ✕ to dismiss. body may hold safe HTML."""
    return Markup('<div class="rg-notice tone-%s" role=status><span class=rg-noticeic>%s</span><span class=rg-txt><b>%s</b>%s</span>%s</div>' % (
        _tone(tone, "lime"), _CHECK if icon_name == "check" else icon(icon_name, "sm"), _e(title), ('<small>%s</small>' % body) if body else "",
        '<button type=button class=rg-noticex aria-label="Dismiss" onclick="this.parentNode.remove()">%s</button>' % icon("close", "sm") if dismiss else ""))


def divider(label="or"):
    return Markup('<div class=rg-divider><span>%s</span></div>' % _e(label))


def dob_field(name="birth_date", value="", club="", min_age=18):
    """2.0 / Field / Date of birth (02 H, 2328:139058): three typed boxes, no calendar. Age line when valid,
    cherry error under the age floor. A hidden input carries YYYY-MM-DD for the form."""
    y, m, d = (str(value or "")[:10].split("-") + ["", "", ""])[:3] if value else ("", "", "")
    box = lambda key, label, ph, val, n: ('<label class=rg-dobbox><span>%s</span><input data-dob=%s inputmode=numeric pattern="[0-9]*" maxlength=%d placeholder="%s" value="%s" autocomplete=%s></label>'
                                       % (label, key, n, ph, _e(val), {"m": "bday-month", "d": "bday-day", "y": "bday-year"}[key]))
    return Markup('<div class=rg-dob data-min-age="%d" data-club="%s"><div class=rg-dobrow>%s%s%s</div>'
                  '<input type=hidden name="%s" value="%s"><p class=rg-dobhelp>Type it — 2-digit month and day, 4-digit year.</p></div>' % (
                      int(min_age), _e(club), box("m", "MONTH", "MM", m, 2), box("d", "DAY", "DD", d, 2), box("y", "YEAR", "YYYY", y, 4),
                      _e(name), _e(value or "")))


def membership_sex(current="", body="USA Water Polo", name="membership_sex", options=None):
    """Asked next to the membership number: the sex on their governing-body membership (insurance rosters, admins only).
    The choices come from the sport (Club › Sports › Sex on a membership)."""
    opts = options or (("male", "Man"), ("female", "Woman"), ("prefer_not_to_say", "Prefer not to say"))
    short = {"USA Water Polo": "USAWP"}.get(body, body)
    return Markup('<div class="rg-field rg-sexq"><span>You\'re registered as the following with %s</span>%s<small class=rg-fieldnote>Only admins see this. It matches the insurance roster.</small></div>' % (
        _e(short), choice_chips(name, opts, current or "")))



def person_row(name, sub="", initials="", chip_label="", chip_status="neutral", href="", attrs="", tone="sun"):
    """2.0 / People row (Figma 62 L2, Q1, N1): 52 avatar, bold name, smoke line, chip on the right.
    href makes it a link; attrs (e.g. data-open-dialog) on a row without href makes it a button."""
    ini = initials or ("".join(p[:1] for p in str(name).split()[:2]) or "?").upper()
    inner = '<span class="rg-pav tone-%s" aria-hidden=true>%s</span><span class=rg-txt><b>%s</b>%s</span>%s' % (
        _tone(tone, "sun"), _e(ini), _e(name), ('<small>%s</small>' % _e(sub)) if sub else "", str(chip(chip_label, chip_status)) if chip_label else "")
    extra = (" " + attrs) if attrs else ""
    if href:
        return Markup('<a class=rg-person href="%s"%s>%s</a>' % (_e(href), extra, inner))
    if attrs:
        return Markup('<button type=button class=rg-person%s>%s</button>' % (extra, inner))
    return Markup('<div class=rg-person>%s</div>' % inner)


def group_card(title, sub="", chips=(), href=""):
    """2.0 / Group card (Figma 62 L1): title + one line, chevron, then on/off chips. chips = [(label, on)]."""
    row = "".join(str(chip(label, "going" if on else "neutral")) for label, on in chips)
    inner = '<span class=rg-gchead><span class=rg-txt><b>%s</b>%s</span>%s</span>%s' % (
        _e(title), ('<small>%s</small>' % _e(sub)) if sub else "", icon("chevron_right", "sm") if href else "",
        ('<span class=rg-gcchips>%s</span>' % row) if row else "")
    return Markup(_tag(href, "rg-gcard", inner) if href else '<div class=rg-gcard>%s</div>' % inner)


def detail_group(label, count=None, action="", action_href="", action_attrs="", body=""):
    """2.0 / Detail group (Figma 62 Q1): caps label (+count), lime Edit / + Add on the right, content below, on carbon."""
    act = ""
    if action:
        act = ('<a class=rg-dgact href="%s">%s</a>' % (_e(action_href), _e(action))) if action_href else \
              '<button type=button class=rg-dgact%s>%s</button>' % ((" " + action_attrs) if action_attrs else "", _e(action))
    return Markup('<section class=rg-dgroup><div class=rg-dghead><span>%s%s</span>%s</div>%s</section>' % (
        _e(label), (" %s" % _e(count)) if count is not None else "", act, body))


def doc_card(chips, title, excerpt="", button="", button_attrs=""):
    """2.0 / Document preview (Figma 62 D2): chips, bold title, three-line excerpt, a full-width secondary button."""
    btn = ('<button type=button class="rg-btn secondary"%s>%s</button>' % ((" " + button_attrs) if button_attrs else "", _e(button))) if button else ""
    return Markup('<section class=rg-doccard><span class=rg-gcchips>%s</span><b>%s</b>%s%s</section>' % (
        "".join(str(chip(c, "neutral")) for c in chips if c), _e(title), ('<p>%s</p>' % _e(excerpt)) if excerpt else "", btn))


def notif_preview(app, title, line):
    """2.0 / Notification preview (Figma 62 R1): what the reminder looks like on a phone."""
    return Markup('<div class=rg-notif>%s<b>%s</b><small>%s</small></div>' % (str(chip(app, "neutral")), _e(title), _e(line)))


def person_status(name, sub="", chips=(), note="", initials="", href="", attrs="", tone="sun"):
    """2.0 / People row with status (Figma 62 S1): avatar, name, role line, status chips, one 'missing' line.
    chips = [(label, status)]. No action buttons on the row; tap opens the status drawer or the profile."""
    ini = initials or ("".join(p[:1] for p in str(name).split()[:2]) or "?").upper()
    row = "".join(str(chip(l, st)) for l, st in chips if l)
    inner = '<span class="rg-pav tone-%s" aria-hidden=true>%s</span><span class=rg-txt><b>%s</b>%s%s%s</span>' % (
        _tone(tone, "sun"), _e(ini), _e(name), ('<small>%s</small>' % _e(sub)) if sub else "",
        ('<span class=rg-gcchips>%s</span>' % row) if row else "", ('<small class=rg-pnote>%s</small>' % _e(note)) if note else "")
    extra = (" " + attrs) if attrs else ""
    if href:
        return Markup('<a class="rg-person rg-pstat" href="%s"%s>%s</a>' % (_e(href), extra, inner))
    return Markup('<button type=button class="rg-person rg-pstat"%s>%s</button>' % (extra, inner))


def status_list(rows):
    """2.0 / Status list (Figma 62 S3): grouped rows, title + one line, a chip or a lime action on the right.
    rows = [dict(title, sub, chip=(label, status) | None, action=label, href='', attrs='')]."""
    out = []
    for r in rows:
        side = ""
        if r.get("chip"):
            side = str(chip(*r["chip"]))
        elif r.get("action"):
            side = ('<a class=rg-dgact href="%s">%s</a>' % (_e(r["href"]), _e(r["action"]))) if r.get("href") else \
                   '<button type=button class=rg-dgact%s>%s</button>' % ((" " + r["attrs"]) if r.get("attrs") else "", _e(r["action"]))
        out.append('<div class=rg-slrow><span class=rg-txt><b>%s</b>%s</span>%s</div>%s' % (
            _e(r["title"]), ('<small>%s</small>' % _e(r["sub"])) if r.get("sub") else "", side, r.get("extra", "")))
    return Markup('<div class=rg-slist>%s</div>' % "".join(out))


def pass_card(name, on, price, per="", covers="", line="", href="", hero=False, button="", button_href=""):
    """2.0 / Pass card (Figma 62 P1/H2): name + On/Off chip, big price, what it covers, renewal line.
    hero = the lime top card on the pass page, with the member-facing button."""
    btn = ('<a class=rg-passbtn href="%s" target=_blank rel=noopener>%s</a>' % (_e(button_href), _e(button))) if button and button_href else ""
    inner = ('<span class=rg-passtop><b>%s</b>%s</span><span class=rg-passprice><b>%s</b><small>%s</small></span>%s%s%s') % (
        _e(name), str(chip("On" if on else "Off", "going" if on else "neutral")), _e(price), _e(per),
        ('<span class=rg-passcov>%s</span>' % _e(covers)) if covers else "", ('<small class=rg-passline>%s</small>' % _e(line)) if line else "", btn)
    klass = "rg-pass" + (" hero" if hero else "")
    return Markup(_tag(href, klass, inner) if href else '<div class="%s">%s</div>' % (klass, inner))


def kv_rows(rows):
    """2.0 / Key–value rows inside a detail group (Figma 62 H2): smoke label, paper value."""
    return Markup('<dl class=rg-kv>%s</dl>' % "".join('<dt>%s</dt><dd>%s</dd>' % (_e(k), _e(v)) for k, v in rows))


def progress_card(title, done, total, sub=""):
    """2.0 / Progress card (Figma 62 I2): '9 in · 12 needed', a lime bar, one line under it."""
    pct = 0 if not total else max(0, min(100, int(100 * done / total)))
    return Markup('<div class=rg-progress><b>%s</b><span class=rg-pbar><i style="width:%d%%"></i></span>%s</div>' % (
        _e(title), pct, ('<small>%s</small>' % _e(sub)) if sub else ""))


def drive_card(minutes, note="", leave="", kicker="YOUR DRIVE", href=""):
    """2.0 / Drive card (Figma 359:1134): lime, r40. Caps kicker + ink 'Leave by' pill, 80px minutes, MIN + note, 60px ink disc."""
    pill = ('<span class=rg-drvleave>%s</span>' % _e(leave)) if leave else ""
    inner = ('<span class=rg-drvtop><span class=rg-drvk>%s</span>%s</span><span class=rg-drvmid><span class=rg-drvnum><b>%s</b>'
             '<span><i>MIN</i><small>%s</small></span></span><span class=rg-drvdisc aria-hidden=true>%s</span></span>') % (
        _e(kicker), pill, _e(minutes), _e(note), icon("chevron_right"))
    return Markup(_tag(href, "rg-drive", inner, ' aria-label="Plan when to leave"' if href else ""))

def jinja_globals():
    return dict(rg_icon=icon, rg_chip=chip, rg_head=head, rg_section=section, rg_seg=seg, rg_seg_choice=seg_choice, rg_map_unavailable=map_unavailable, rg_callout_card=callout_card, rg_usawp_card=usawp_card, rg_ride_row=ride_row, rg_ride_pick=ride_pick, rg_week_grid=week_grid, rg_filters=filters, rg_day=day, rg_label=label,
                rg_event=event_line, rg_event_line=event_line, rg_event_row=event_row, rg_event_card=event_card, rg_row=row, rg_callout=callout, rg_metric=metric,
                rg_info=info, rg_empty=empty, rg_manage_tile=manage_tile, rg_social_card=social_card, rg_practice_actions=practice_actions, rg_search=search_field, rg_stat=stat_card, rg_chart_switch=chart_switch, rg_top_bar=top_bar, rg_qr_card=qr_card, rg_sheet_head=sheet_head, rg_page_title=page_title, rg_button=button, rg_settings_row=settings_row, rg_hub=hub_tile, rg_stack_tile=stack_tile, rg_counts=count_chips, rg_event_cancelled=event_cancelled, rg_checklist=checklist, rg_checkin_hero=checkin_hero, rg_checkin_row=checkin_row, rg_plus=plus_button, rg_event_hero=event_hero, rg_back=back_button, rg_toggle=toggle, rg_choice=choice, rg_section_count=section_count, rg_status_toggle=status_toggle, rg_choice_chips=choice_chips, rg_code=code_block, rg_steps=steps, rg_block_row=block_row, rg_auth_head=auth_head, rg_brand=brand_mark, rg_notice=notice, rg_divider=divider, rg_dob=dob_field, rg_membership_sex=membership_sex, rg_info_block=info_block, rg_person=person_row, rg_group_card=group_card, rg_detail_group=detail_group, rg_doc_card=doc_card, rg_notif=notif_preview, rg_person_status=person_status, rg_status_list=status_list, rg_pass=pass_card, rg_kv=kv_rows, rg_progress=progress_card, rg_drive=drive_card, event_tone=event_tone)
