"""Templates (Jinja strings) for the Grunions app. Restrained dark UI: one surface, gray text, one blue accent."""

BASE = """<!doctype html><html lang=en style="background:#0a0a0b;color-scheme:dark"><head>
<meta charset=utf-8><meta name=color-scheme content=dark><meta name=theme-color content="#0a0a0b">
<meta name=viewport content="width=device-width,initial-scale=1,viewport-fit=cover">
<meta name=apple-mobile-web-app-capable content=yes><link rel=manifest href=/manifest.webmanifest>
<link rel=icon href=/static/icons/favicon-32.png sizes=32x32 type=image/png><link rel=apple-touch-icon href=/static/icons/apple-touch-icon-180.png>
<title>Grunions</title>
<style>html,body{background:#0a0a0b;color:#ececee}html{color-scheme:dark}
@view-transition{navigation:auto}
::view-transition-old(root),::view-transition-new(root){animation-duration:0s;mix-blend-mode:normal}
::view-transition-group(grunions-nav),::view-transition-old(grunions-nav),::view-transition-new(grunions-nav){animation:none;mix-blend-mode:normal}
[hidden]{display:none!important}
:root{--bg:#0a0a0b;--surface:#151517;--surface2:#1d1d20;--line:#26262a;--t1:#ececee;--t2:#a0a0a8;--t3:#6c6c74;--accent:#3b82f6;
--ok:#3fb950;--bad:#f0524a;--warn:#e3a008;--r:14px}
*{box-sizing:border-box}html{-webkit-text-size-adjust:100%}
body{margin:0;background:#0a0a0b;color:var(--t1);font:16px/1.5 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,system-ui,sans-serif}
a{color:var(--t1)}main{max-width:640px;margin:0 auto;padding:20px 20px calc(120px + env(safe-area-inset-bottom))}
header{display:flex;align-items:center;justify-content:space-between;padding:16px 20px;max-width:640px;margin:0 auto}
.brand{font-weight:600;letter-spacing:.2px;color:var(--t1);text-decoration:none}header a.sub{color:var(--t3);font-size:14px;text-decoration:none}
h1{font-size:28px;font-weight:650;letter-spacing:-.3px;margin:4px 0 20px}h2{font-size:17px;font-weight:600;margin:28px 0 10px}
p{margin:0 0 12px}.t2{color:var(--t2)}.t3{color:var(--t3)}.sm{font-size:14px}.xs{font-size:13px}
.card{background:var(--surface);border-radius:var(--r);padding:18px;margin:0 0 12px}
.usawp-line{display:flex;align-items:center;justify-content:space-between;gap:12px;margin-top:12px}
.list{background:var(--surface);border-radius:var(--r);margin:0 0 12px;overflow:hidden}
.list.loose{overflow:visible}
.more{position:relative;flex:0 0 auto;margin-left:2px}
button.morebtn{width:32px;height:32px;padding:0;background:transparent;color:var(--t3);font-size:22px;line-height:1;border-radius:8px}
button.morebtn[aria-expanded=true]{background:var(--surface2);color:var(--t1)}
.menu{position:absolute;left:0;top:36px;z-index:20;min-width:232px;padding:6px;background:#151517;border:1px solid var(--line);border-radius:12px;box-shadow:0 10px 28px rgba(0,0,0,.45)}
.menu form{margin:0}
.menu button{width:100%;height:40px;padding:0 12px;justify-content:flex-start;background:transparent;color:var(--t1);font-weight:500;font-size:15px;border-radius:8px}
.menu button:disabled{color:var(--t3)}
.li{display:flex;align-items:center;gap:12px;padding:14px 18px;min-height:60px;border-top:1px solid var(--line)}.li:first-child{border-top:0}
.grow{flex:1;min-width:0}.ell{white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
label{display:block;font-size:13px;color:var(--t2);margin:0 0 14px}
.checks{margin:0 0 14px}.checks label{display:flex;align-items:center;min-height:40px;margin:0;color:var(--t1);font-size:16px}
input,select,textarea{display:block;width:100%;margin-top:6px;background:var(--surface2);border:1px solid var(--line);color:var(--t1);border-radius:10px;
padding:0 14px;height:48px;font:inherit;color-scheme:dark}textarea{padding:12px 14px}input[type=hidden]{display:none}input[type=checkbox]{display:inline-block;width:20px;height:20px;margin:0 8px 0 0;vertical-align:-4px;accent-color:var(--accent)}
input[type=date]::-webkit-calendar-picker-indicator,input[type=datetime-local]::-webkit-calendar-picker-indicator{cursor:pointer;background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Crect x='3' y='5' width='18' height='16' rx='2' fill='none' stroke='%23ececee' stroke-width='1.8'/%3E%3Cpath d='M3 10h18M8 3v4M16 3v4' fill='none' stroke='%23ececee' stroke-width='1.8' stroke-linecap='round'/%3E%3C/svg%3E");background-repeat:no-repeat;background-size:18px 18px;background-position:center}
input[type=time]::-webkit-calendar-picker-indicator{cursor:pointer;background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Ccircle cx='12' cy='12' r='8' fill='none' stroke='%23ececee' stroke-width='1.8'/%3E%3Cpath d='M12 8v5l3 2' fill='none' stroke='%23ececee' stroke-width='1.8' stroke-linecap='round'/%3E%3C/svg%3E");background-repeat:no-repeat;background-size:18px 18px;background-position:center}
input:focus,select:focus,textarea:focus{outline:none;border-color:var(--accent)}
.btn,button{display:inline-flex;align-items:center;justify-content:center;gap:6px;height:48px;padding:0 18px;border-radius:10px;border:0;font:inherit;font-weight:600;
cursor:pointer;text-decoration:none;background:var(--surface2);color:var(--t1)}.btn.primary,button.primary{background:var(--accent);color:#fff}
.btn.quiet,button.quiet{background:none;color:var(--t2);padding:0 8px}.btn.danger,button.danger{background:none;color:var(--bad)}
.btn.compact,button.compact{height:40px;padding:0 14px;font-size:15px}.full{width:100%}.row{display:flex;gap:10px}.row>*{flex:1}
.coach-tag{display:inline-block;margin-left:6px;padding:0 7px;border-radius:999px;border:1px solid var(--line);color:var(--t2);font-size:12px;font-weight:600;line-height:20px;vertical-align:1px;white-space:nowrap}
.coach-elig,.ref-elig{margin-left:8px;font-weight:650;font-size:15px}
.eligs{display:flex;flex-wrap:wrap;gap:4px 10px;margin-top:4px}.eligs .coach-elig,.eligs .ref-elig,.eligs .coach-tag{margin-left:0}.eligs .st{white-space:normal}
.memline{display:flex;flex-wrap:wrap;align-items:center;gap:2px 0;margin-top:2px;color:var(--t3);font-size:13px;line-height:1.4}
.st{display:inline-flex;align-items:center;gap:7px;font-size:14px;color:var(--t2);white-space:nowrap}
.st::before{content:"";width:8px;height:8px;border-radius:50%;background:var(--t3)}.st-ok::before{background:var(--ok)}.st-bad::before{background:var(--bad)}.st-warn::before{background:var(--warn)}.st-trial::before{background:var(--ok)}
.row.wrap{flex-wrap:wrap}
dialog.modal{border:0;padding:0;background:transparent;color:var(--t1);width:min(440px,calc(100vw - 32px))}
dialog.modal::backdrop{background:rgba(0,0,0,.72)}
dialog.modal .sheet{background:var(--surface);border:1px solid var(--line);border-radius:var(--r);padding:20px}
.note{background:var(--surface);border-radius:var(--r);padding:14px 18px;margin:0 0 12px;color:var(--t2);font-size:15px}.note b{color:var(--t1)}
.toast{position:fixed;left:50%;bottom:calc(76px + env(safe-area-inset-bottom));transform:translateX(-50%);z-index:30;background:var(--surface);color:var(--t1);border:1px solid var(--line);border-radius:12px;padding:12px 16px;font-size:15px;line-height:1.4;text-align:center;box-shadow:0 8px 28px rgba(0,0,0,.5);max-width:min(440px,calc(100% - 32px))}
details>summary{list-style:none;cursor:pointer;display:flex;align-items:center;justify-content:space-between;min-height:56px;padding:0 18px;color:var(--t1)}
details>summary::-webkit-details-marker{display:none}details>summary::after{content:"›";color:var(--t3);font-size:22px;transition:transform .15s}
details[open]>summary::after{transform:rotate(90deg)}details.card{padding:0}details.card>.body{padding:0 18px 16px}
details.checkin{margin:4px 0 20px}details.checkin>summary{min-height:0;padding:18px 0 8px;font-size:17px;font-weight:600;justify-content:flex-start;gap:8px}
.kv{display:flex;justify-content:space-between;gap:12px;padding:10px 0;border-top:1px solid var(--line);font-size:15px}.kv:first-child{border-top:0}.kv span:first-child{color:var(--t2)}
.seg{display:flex;gap:4px;background:var(--surface);border-radius:12px;padding:4px;margin:0 0 20px;overflow-x:auto}
.seg a{flex:1;text-align:center;padding:9px 12px;border-radius:9px;color:var(--t2);text-decoration:none;font-size:14px;font-weight:500;white-space:nowrap}.seg a.on{background:var(--surface2);color:var(--t1)}
nav.tabs{position:fixed;left:0;right:0;bottom:0;z-index:9;box-sizing:border-box;
height:calc(64px + env(safe-area-inset-bottom));padding:0 0 env(safe-area-inset-bottom);background:#0a0a0b;
border-top:1px solid var(--line);display:flex;justify-content:center;view-transition-name:grunions-nav}
nav.tabs a{position:relative;flex:1;max-width:140px;height:64px;min-height:64px;box-sizing:border-box;
display:flex;flex-direction:column;align-items:center;justify-content:center;gap:4px;padding:0;margin:0;
color:var(--t3);text-decoration:none;font:500 12px/14px -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,system-ui,sans-serif}
.badge{display:inline-flex;align-items:center;justify-content:center;min-width:16px;height:16px;padding:0 4px;border-radius:8px;background:var(--bad);color:#fff;font-size:10px;font-weight:700;line-height:1}
nav.tabs a .badge{position:absolute;top:4px;left:50%;margin-left:8px}.pdate .badge{margin-left:8px}
nav.tabs a.on{color:var(--accent)}nav.tabs svg{width:24px;height:24px;flex:none;display:block;fill:none;stroke:currentColor;stroke-width:1.8;stroke-linecap:round;stroke-linejoin:round}
.chat{display:flex;flex-direction:column;gap:14px}.m{position:relative;-webkit-touch-callout:none}.m .who{font-size:13px;color:var(--t3);margin-bottom:3px}.m .txt{background:var(--surface);border-radius:14px;padding:10px 14px;display:inline-block;max-width:85%;white-space:pre-wrap;word-wrap:break-word}
.m.mine{text-align:right}.m.mine .txt{background:var(--surface2);text-align:left}.m.ann .txt{display:block;max-width:none;border:1px solid var(--line);background:var(--surface)}
.m .txt.deleted{font-style:italic;color:var(--t3);background:transparent}.m .edited{font-size:12px;color:var(--t3);font-weight:400}
.m .more{display:none;position:absolute;top:-4px;right:0;width:32px;height:32px;padding:0;background:none;color:var(--t3);font-size:18px}
.m.mine .more{left:0;right:auto}
@media (hover:hover) and (pointer:fine){.m:hover .more{display:inline-flex}}
.m .editbox textarea{min-height:72px;height:auto;margin:0}
.composer{position:fixed;left:0;right:0;bottom:calc(64px + env(safe-area-inset-bottom));background:var(--bg);padding:10px 20px;border-top:1px solid var(--line);z-index:8}
.composer form{max-width:600px;margin:auto;display:flex;gap:8px;align-items:flex-end}
.composer textarea{margin:0;height:48px;min-height:48px;max-height:136px;resize:none;line-height:22px;padding:12px 14px;overflow-y:auto;scrollbar-width:none;-ms-overflow-style:none}
.composer textarea::-webkit-scrollbar{display:none}.iconbtn{width:48px;padding:0;flex:none;color:var(--t2)}.iconbtn svg{width:22px;height:22px;fill:none;stroke:currentColor;stroke-width:1.8;stroke-linecap:round;stroke-linejoin:round}
.iconbtn.send{color:var(--accent)}
.preview{max-width:600px;margin:0 auto 8px;display:flex;align-items:center;gap:10px;color:var(--t2);font-size:14px}.preview img{height:48px;border-radius:8px}
.m .img{display:block;margin-top:4px}.m.mine .img{margin-left:auto}.m .img img{max-width:min(70vw,280px);max-height:280px;border-radius:12px;display:block;background:var(--surface)}.m.mine .img{width:fit-content}
.rx{display:flex;flex-wrap:wrap;gap:6px;margin-top:6px}.m.mine .rx{justify-content:flex-end}
.rx button{height:30px;padding:0 10px;border-radius:15px;font-size:14px;font-weight:500;background:var(--surface);color:var(--t2);border:1px solid var(--line)}
.rx button.on{border-color:var(--accent);color:var(--t1)}
.sheet .emojirow{display:flex;flex-wrap:wrap;gap:6px;margin:0 0 14px}
.sheet .emojirow button{height:36px;width:36px;padding:0;border-radius:18px;background:var(--surface2);font-size:18px}
#actConfirm{margin:0 0 12px;font-weight:600}
.lightbox{position:fixed;inset:0;background:rgba(0,0,0,.92);display:flex;align-items:center;justify-content:center;z-index:20}.lightbox img{max-width:96vw;max-height:92vh;border-radius:8px}
.gobtn{background:none;height:auto;padding:4px 0;color:var(--t2);font-weight:500;font-size:14px}.gobtn::after{content:" ›";color:var(--t3)}
.ci-name{flex:1;min-width:0;height:auto;padding:0;background:none;display:block;text-align:left;font-weight:400}
.calpick{position:relative;flex:1.6;min-width:0;display:flex;align-items:center;gap:4px}
.calnav,.calmonth{flex:none;width:36px;height:36px;padding:0;display:inline-flex;align-items:center;justify-content:center;background:none;color:var(--t1);text-decoration:none;border-radius:10px}
.calnav{height:48px;width:40px}
.calnav[aria-disabled=true]{color:var(--t3);opacity:.35;pointer-events:none}
.calnav svg,.calmonth svg,.calbtn svg{fill:none;stroke:currentColor;stroke-width:1.8;stroke-linecap:round;stroke-linejoin:round;display:block}
.calbtn{flex:1;min-width:0;height:48px;margin:0;padding:0 10px;background:var(--surface2);border:1px solid var(--line);color:var(--t1);border-radius:10px;font:inherit;font-weight:600;display:flex;align-items:center;justify-content:center;gap:8px;cursor:pointer}
.calbtn span{overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.calpop{position:absolute;z-index:12;top:calc(100% + 6px);left:0;width:min(300px,calc(100vw - 40px));background:var(--surface);border:1px solid var(--line);border-radius:14px;padding:12px;box-shadow:0 12px 32px rgba(0,0,0,.55);color:var(--t1)}
.calhead{display:flex;align-items:center;justify-content:space-between;gap:8px;margin-bottom:8px}
.calhead .lbl{font-weight:600;color:var(--t1)}
.calwd,.calgrid{display:grid;grid-template-columns:repeat(7,1fr);gap:2px;text-align:center}
.calwd{color:var(--t3);font-size:12px;margin-bottom:4px}
.calday{display:flex;align-items:center;justify-content:center;height:36px;border-radius:8px;font-size:14px;font-weight:600;text-decoration:none;color:var(--t1)}
a.calday:hover{background:var(--surface2)}
a.calday.on{background:var(--accent);color:#fff}
span.calday{color:var(--t3);opacity:.4;font-weight:500}
.panel{padding:4px 18px 18px;border-top:1px solid var(--line);background:var(--surface)}.panel h3{font-size:15px;font-weight:600;margin:18px 0 10px}
@media print{header,nav,.noprint{display:none!important}body{background:#fff;color:#000}.card{background:#fff}}
</style></head><body style="background:#0a0a0b;color:#ececee;margin:0">
{% macro st(kind, label) %}<span class="st st-{{kind}}">{{label}}</span>{% endmacro %}
{% macro bubble(n) %}{% if n %}<span class=badge>{{ n if n < 100 else '99+' }}</span>{% endif %}{% endmacro %}
{% macro usawp(s) %}{{ st({'verified':'ok','expired':'bad','pending':'warn'}.get(s,'none'), 'USAWP ' ~ s) }}{% endmacro %}
{% macro coach_tag(m) %}{% set ce = coach_eligibility(m) %}{% if ce.eligible %}<span class="st st-ok coach-elig">Coach eligible</span>{% elif ce.text %}<span class="st st-bad coach-elig">{{ce.text}}</span>{% endif %}{% endmacro %}
{% macro referee_tag(m) %}{% set rf = referee_eligibility(m) %}{% if rf.eligible %}<span class="st st-ok ref-elig">Referee eligible</span>{% elif rf.text %}<span class="st st-bad ref-elig">{{rf.text}}</span>{% endif %}{% endmacro %}
{% macro bg_line(m) %}{% set bg = background_view(m) %}{% if bg %}{{ st(bg.kind, bg.text) }}{% endif %}{% endmacro %}
{% macro member_status(r) %}{% set cl = clearance(r) %}{% set dl = days_left(r.usawp_valid_until) %}{% set tw = trial_window(r) %}{% set ex = expiry_notes(r, cl) %}
{% if tw and tw.active and r.usawp_status != 'verified' and not ex.membership %}{{ st('trial', trial_badge(tw)) }}<div class="t3 xs">Ends {{tw.ends}}</div>{% elif not cl.ok %}{{ st('bad','Not cleared') }}{% elif dl is not none and dl <= EXPIRING_DAYS %}{{ st('warn','Expires in %dd' % dl) }}{% else %}{{ st('ok','Cleared') }}{% endif %}
{% if tw and tw.expired and r.usawp_status != 'verified' %}<div class="xs">Trial ended {{tw.ends}}</div>{% endif %}
{% if r.vr_status == 'pending' %}<span class="t3 xs"> · verification requested</span>{% elif r.vr_status == 'done' %}<span class="t3 xs"> · bot answered</span>{% endif %}{% endmacro %}
{% macro member_panel(r) %}{% set cl = clearance(r) %}{% set dl = days_left(r.usawp_valid_until) %}{% set tw = trial_window(r) %}{% set ex = expiry_notes(r, cl) %}
<div class=panel id=m{{r.id}} hidden>
<div class=kv><span>RSVP</span><span>{% if r.going==1 %}RSVP ✓{% elif r.going==0 %}Not going{% else %}—{% endif %}</span></div>
<div class=kv><span>Membership</span><span>{{ usawp(r.usawp_status) }}{% if r.usawp_status=='verified' and dl is not none and dl <= EXPIRING_DAYS %} · {{dl}}d left{% endif %}</span></div>
{% if r.usawp_number or r.usawp_valid_until %}<div class=kv><span>Member # / expires</span><span>{{r.usawp_number or '—'}} / {{r.usawp_valid_until or '—'}}</span></div>{% endif %}
{% if tw and r.usawp_status != 'verified' %}<div class=kv><span>USAWP trial</span><span>{% if tw.active %}{{ trial_badge(tw) }} · Ends {{tw.ends}}{% else %}Trial ended {{tw.ends}}{% endif %}</span></div>{% endif %}
{% if not cl.ok %}<div class=kv><span>Not cleared</span><span style="text-align:right">{{cl.reasons|join(', ')}}</span></div>{% endif %}
{% if background_view(r) %}<div class=kv>{{ bg_line(r) }}</div>{% endif %}
{% if me().is_admin %}<form method=post>{{csrf_field()}}<input type=hidden name=member_id value={{r.id}}><input type=hidden name=date value="{{date}}"><input type=hidden name=q value="{{q}}">{% if coach_filter is defined %}<input type=hidden name=list_coach value="{{'eligible' if coach_filter else ''}}"><input type=hidden name=list_referee value="{{'eligible' if referee_filter else ''}}">{% endif %}
<label>Background screening expires<input name=expires_on type=date value="{{ background_view(r).date if background_view(r) else '' }}"></label>
<button class=full name=action value=background>Save background screening</button></form>
{% if not r.is_admin and r.role != 'coach' %}<form method=post>{{csrf_field()}}<input type=hidden name=member_id value={{r.id}}><input type=hidden name=date value="{{date}}"><input type=hidden name=q value="{{q}}">{% if coach_filter is defined %}<input type=hidden name=list_coach value="{{'eligible' if coach_filter else ''}}"><input type=hidden name=list_referee value="{{'eligible' if referee_filter else ''}}">{% endif %}
<button class=full name=action value=require_background>{% if r.require_background %}Don't require background{% else %}Require background{% endif %}</button></form>{% endif %}{% endif %}
{% if r.usawp_verified_by %}<div class=kv><span>Verified</span><span>{{r.usawp_verified_by}}, {{r.usawp_verified_at.replace('T',' ')}}</span></div>{% endif %}
{% if r.vr_status %}<div class=kv><span>Bot request</span><span>{{r.vr_status}}{% if r.vr_note %} · {{r.vr_note}}{% endif %}</span></div>{% endif %}
{% if me().is_admin %}{% set cred = credential_dates(r) %}<details class=recheck {% if r.vr_status == 'pending' %}open{% endif %}><summary>Recheck membership</summary>
<form method=post class=body>{{csrf_field()}}<input type=hidden name=member_id value={{r.id}}><input type=hidden name=date value="{{date}}"><input type=hidden name=q value="{{q}}">{% if coach_filter is defined %}<input type=hidden name=list_coach value="{{'eligible' if coach_filter else ''}}"><input type=hidden name=list_referee value="{{'eligible' if referee_filter else ''}}">{% endif %}
<p class="t3 sm">Look this member up on Sport:80 and enter what you find. Grunions does not contact Sport:80.{% if r.vr_status == 'pending' %} Saving answers the pending verification request.{% endif %}</p>
<label>Verified<select name=verified><option value=yes {{'selected' if r.usawp_status=='verified'}}>Yes</option><option value=no {{'selected' if r.usawp_status!='verified'}}>No</option></select></label>
<label>Membership type<input name=membership_type value="{{r.membership_type or ''}}" placeholder="Individual Membership, Coach"></label>
<label>Membership expires<input type=date name=valid_until value="{{r.usawp_valid_until or ''}}"></label>
<label>SafeSport expires<input type=date name=safesport_expires value="{{cred.safesport or ''}}"></label>
<label>Background screening expires<input type=date name=background_expires value="{{cred.background or ''}}"></label>
<label>Referee certification expires<input type=date name=referee_expires value="{{cred.referee or ''}}"></label>
<button class="primary full" name=action value=recheck>Save Sport:80 result</button></form></details>{% endif %}
{% if r.preferred_first and r.preferred_first.strip() %}<div class=kv><span>Legal name</span><span>{{r.first}} {{r.last}}</span></div>{% endif %}
{% if me().is_admin %}<form method=post>{{csrf_field()}}<input type=hidden name=member_id value={{r.id}}><input type=hidden name=date value="{{date}}"><input type=hidden name=q value="{{q}}">{% if coach_filter is defined %}<input type=hidden name=list_coach value="{{'eligible' if coach_filter else ''}}"><input type=hidden name=list_referee value="{{'eligible' if referee_filter else ''}}">{% endif %}
<label>Preferred first name (optional)<input name=preferred_first value="{{r.preferred_first or ''}}" placeholder="Leave blank to use legal first name"></label>
<button class=full name=action value=preferred>Save preferred name</button></form>{% endif %}
{% if me().is_admin and (not cl.ok or r.usawp_status != 'verified') %}
<h3>Verify {{r.first}} on Sport:80</h3>
<div class=row><a class="btn" target=_blank rel=noopener href="https://usawp.sport80.com/" onclick="navigator.clipboard&&navigator.clipboard.writeText('{{r.first}} {{r.last}}')">Open Sport:80</a>
<form method=post style="flex:1">{{csrf_field()}}<input type=hidden name=member_id value={{r.id}}><input type=hidden name=date value="{{date}}">{% if coach_filter is defined %}<input type=hidden name=list_coach value="{{'eligible' if coach_filter else ''}}"><input type=hidden name=list_referee value="{{'eligible' if referee_filter else ''}}">{% endif %}
<button class=full name=action value=ask_bot {% if r.vr_status=='pending' %}disabled{% endif %}>{{'Requested' if r.vr_status=='pending' else 'Ask Grunions to verify'}}</button></form></div>
<p class="t3 xs" style="margin-top:6px">Opening Sport:80 copies the name. Search the Grunions club members list and confirm membership is Current. Enter what you find with Recheck membership.</p>
<h3>Compliance item</h3><form method=post>{{csrf_field()}}<input type=hidden name=member_id value={{r.id}}><input type=hidden name=date value="{{date}}"><input type=hidden name=q value="{{q}}">{% if coach_filter is defined %}<input type=hidden name=list_coach value="{{'eligible' if coach_filter else ''}}"><input type=hidden name=list_referee value="{{'eligible' if referee_filter else ''}}">{% endif %}
<label>Item<select name=req_id>{% for it in cl.checks|sort(attribute='status') %}<option value={{it.req.id}}>{{it.req.name}} ({{it.status}})</option>{% endfor %}</select></label>
<div class=row><label>Completed<input name=completed_on type=date></label><label>Expires on<input name=expires_on type=date></label></div>
<button class=full name=action value=req>Save item</button></form>
<h3>Role</h3><form method=post class=row>{{csrf_field()}}<input type=hidden name=member_id value={{r.id}}><input type=hidden name=date value="{{date}}">{% if coach_filter is defined %}<input type=hidden name=list_coach value="{{'eligible' if coach_filter else ''}}"><input type=hidden name=list_referee value="{{'eligible' if referee_filter else ''}}">{% endif %}
<select name=role style="margin:0">{% for o in ['member','coach','admin'] %}<option {{'selected' if role_label(r)==o}}>{{o}}</option>{% endfor %}</select><button name=action value=role style="flex:0 0 auto">Save</button></form>
{% endif %}</div>{% endmacro %}
<header><a class=brand href=/>Grunions</a>{% if me() %}<a class=sub href=/logout>Log out</a>{% endif %}</header><main>
{% for cat, msg in get_flashed_messages(with_categories=true) %}{% if cat == 'toast' %}<div class="toast noprint" role=status>{{msg}}</div>{% else %}<div class=note>{{msg|safe}}</div>{% endif %}{% endfor %}
<script>document.querySelectorAll('.toast').forEach(function(t){setTimeout(function(){t.remove()},3000)})</script>
{% macro push_card() %}<div class=card id=pushCard hidden>
<div style="font-weight:600">Notifications</div>
<p class="t2 sm" id=iosPushHint hidden>On iPhone or iPad, add Grunions to your Home Screen to get notifications. Tap Share, then Add to Home Screen, and open the app from there (iOS 16.4 or later).</p>
<p class="t2 sm">Allow notifications for chat, practice reminders, and membership expiry. This works on Android, and on iPhone once Grunions is on your Home Screen (iOS 16.4 or later).</p>
<p class="t2 sm" id=pushDenied hidden>Notifications are blocked in this browser. Allow them in the site settings, then come back.</p>
<button type=button class="primary full" id=allowPush>Allow notifications</button>
<p class="t3 sm" style="margin:10px 0 0"><a href=/notifications>Notification settings</a></p>
</div>{% endmacro %}"""

ICONS = {
 "home": '<svg width="24" height="24" viewBox="0 0 24 24" aria-hidden="true"><path d="M3 10.5 12 3l9 7.5V20a1 1 0 0 1-1 1h-5v-6H9v6H4a1 1 0 0 1-1-1z"/></svg>',
 "cal": '<svg width="24" height="24" viewBox="0 0 24 24" aria-hidden="true"><rect x="3" y="5" width="18" height="16" rx="2"/><path d="M3 10h18M8 3v4M16 3v4"/></svg>',
 "chat": '<svg width="24" height="24" viewBox="0 0 24 24" aria-hidden="true"><path d="M21 12a8 8 0 0 1-11.6 7.1L4 20l1-4.4A8 8 0 1 1 21 12z"/></svg>',
 "admin": '<svg width="24" height="24" viewBox="0 0 24 24" aria-hidden="true"><path d="M9 11l3 3 8-8"/><path d="M20 12v7a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h9"/></svg>',
}
TABS = ("""</main>{% if me() %}<nav class="tabs noprint" data-total="{{ badges().total }}">
<a href=/home class="{{'on' if tab=='home'}}">""" + ICONS["home"] + """Home</a>
<a href=/practices class="{{'on' if tab=='practices'}}" data-badge=schedule>""" + ICONS["cal"] + """Schedule{{ bubble(badges().schedule) }}</a>
<a href=/chat class="{{'on' if tab=='chat'}}" data-badge=chat>""" + ICONS["chat"] + """Chat{{ bubble(badges().chat) }}</a>
{% if is_staff() %}<a href=/admin class="{{'on' if tab=='admin'}}">""" + ICONS["admin"] + """Admin</a>{% endif %}
</nav>{% endif %}
<script>
if('serviceWorker' in navigator) navigator.serviceWorker.register('/sw.js');
function grunionsPushCard(){
var card=document.getElementById('pushCard'); if(!card) return;
var ios=/iPad|iPhone|iPod/.test(navigator.userAgent)||(navigator.platform==='MacIntel'&&navigator.maxTouchPoints>1);
var standalone=window.matchMedia('(display-mode: standalone)').matches||window.navigator.standalone===true;
var hint=document.getElementById('iosPushHint'), btn=document.getElementById('allowPush'), denied=document.getElementById('pushDenied');
if(ios&&!standalone){card.hidden=false; if(hint) hint.hidden=false; if(btn) btn.hidden=true; return;}
if(!('serviceWorker' in navigator)||!('PushManager' in window)||!('Notification' in window)) return;
if(Notification.permission==='granted') return;
card.hidden=false;
if(Notification.permission==='denied'){ if(denied) denied.hidden=false; if(btn) btn.hidden=true; return;}
function b64(s){var pad='='.repeat((4-s.length%4)%4);var b=atob((s+pad).replace(/-/g,'+').replace(/_/g,'/'));var a=new Uint8Array(b.length);for(var i=0;i<b.length;i++)a[i]=b.charCodeAt(i);return a;}
if(btn) btn.onclick=function(){btn.disabled=true;
Notification.requestPermission().then(function(perm){if(perm!=='granted'){btn.disabled=false;return;}
return navigator.serviceWorker.ready.then(function(reg){return reg.pushManager.subscribe({userVisibleOnly:true,applicationServerKey:b64(VAPID_PUBLIC)});}).then(function(sub){
return fetch('/api/push/subscribe',{method:'POST',headers:{'Content-Type':'application/json','X-CSRF':PUSH_CSRF},body:JSON.stringify(sub)});
}).then(function(){card.hidden=true;});}).catch(function(){btn.disabled=false;});};
}
grunionsPushCard();
function grunionsAppBadge(n){try{if(!navigator.setAppBadge)return;if((n|0)>0)navigator.setAppBadge(n|0);else if(navigator.clearAppBadge)navigator.clearAppBadge();}catch(e){}}
function grunionsBadges(u){if(!u)return;grunionsAppBadge(u.total);
 document.querySelectorAll('[data-badge]').forEach(function(el){var n=u[el.getAttribute('data-badge')]|0;var b=el.querySelector('.badge');
  if(!n){if(b)b.remove();return;}if(!b){b=document.createElement('span');b.className='badge';el.appendChild(b);}b.textContent=n>99?'99+':String(n);});
 document.querySelectorAll('[data-pid]').forEach(function(card){var n=(u.practices&&u.practices[card.getAttribute('data-pid')])|0;var slot=card.querySelector('.pdate');if(!slot)return;
  var b=slot.querySelector('.badge');if(!n){if(b)b.remove();return;}if(!b){b=document.createElement('span');b.className='badge';b.setAttribute('data-seen',card.getAttribute('data-pid'));slot.appendChild(b);}b.textContent=n>99?'99+':String(n);});}
function grunionsRefresh(){fetch('/api/unread').then(function(r){return r.ok?r.json():null;}).then(grunionsBadges).catch(function(){});}
var navBadges=document.querySelector('nav.tabs');if(navBadges){grunionsAppBadge(navBadges.getAttribute('data-total'));setInterval(grunionsRefresh,15000);
 document.addEventListener('visibilitychange',function(){if(!document.hidden)grunionsRefresh();});}
function grunionsSeen(id){return fetch('/api/practices/'+id+'/seen',{method:'POST',headers:{'X-CSRF':window.PUSH_CSRF},keepalive:true}).then(function(){grunionsRefresh();}).catch(function(){});}
document.addEventListener('click',function(e){var card=e.target.closest&&e.target.closest('[data-pid]');if(card)grunionsSeen(card.getAttribute('data-pid'));});
setTimeout(function(){var m=/^#p(\\d+)$/.exec(location.hash);if(m&&location.pathname==='/practices')grunionsSeen(m[1]);},0);
var grunionsPageTimers=[];
function grunionsClearPage(){grunionsPageTimers.forEach(clearInterval);grunionsPageTimers=[];window.grunionsNavEpoch=(window.grunionsNavEpoch|0)+1;}
function grunionsRunScripts(scripts){
 var orig=window.setInterval;
 window.setInterval=function(fn,t){var id=orig.call(window,fn,t);grunionsPageTimers.push(id);return id;};
 try{scripts.forEach(function(old){
  var code=old.textContent||''; if(!code.trim())return;
  var s=document.createElement('script'); s.textContent='(function(){\\n'+code+'\\n})();';
  document.body.appendChild(s); if(s.parentNode) s.parentNode.removeChild(s);
 });} finally {window.setInterval=orig;}
}
function grunionsSyncNav(next){
 var nav=document.querySelector('nav.tabs'); if(!nav||!next) return false;
 var oldA=[].slice.call(nav.querySelectorAll('a')), newA=[].slice.call(next.querySelectorAll('a'));
 var same=oldA.length===newA.length;
 if(same) for(var i=0;i<oldA.length;i++) if(oldA[i].getAttribute('href')!==newA[i].getAttribute('href')) same=false;
 nav.setAttribute('data-total', next.getAttribute('data-total')||'0');
 if(!same){nav.innerHTML=next.innerHTML; return true;}
 for(var j=0;j<oldA.length;j++){
  oldA[j].className=newA[j].className;
  var nb=newA[j].querySelector('.badge'), ob=oldA[j].querySelector('.badge');
  if(!nb&&ob) ob.remove();
  else if(nb&&!ob) oldA[j].appendChild(nb.cloneNode(true));
  else if(nb&&ob) ob.textContent=nb.textContent;
 }
 return true;
}
var grunionsNavGen=0;
function grunionsApply(html,url,pop){
 var doc=new DOMParser().parseFromString(html,'text/html');
 var newMain=doc.querySelector('main'), newNav=doc.querySelector('nav.tabs');
 if(!newMain||!newNav){location.href=url; return;}
 grunionsClearPage();
 var scripts=[].slice.call(newMain.querySelectorAll('script'));
 scripts.forEach(function(s){if(s.parentNode) s.parentNode.removeChild(s);});
 var main=document.querySelector('main');
 main.replaceChildren.apply(main, [].slice.call(newMain.childNodes));
 grunionsSyncNav(newNav);
 document.title=doc.title||document.title;
 if(!pop) history.pushState({grunions:1},'',url);
 grunionsRunScripts(scripts);
 grunionsPushCard();
 if(window.grunionsRefresh) grunionsRefresh();
 var hash=url.split('#')[1]||'';
 if(hash){var el=document.getElementById(hash); if(el) el.scrollIntoView(); else scrollTo(0,0);} else scrollTo(0,0);
 var seen=/^#p(\\d+)$/.exec(location.hash);
 if(seen&&location.pathname==='/practices') grunionsSeen(seen[1]);
}
function grunionsGo(url,pop){
 var abs; try{abs=new URL(url,location.href);}catch(e){location.href=url; return;}
 if(abs.origin!==location.origin){location.href=abs.href; return;}
 var gen=++grunionsNavGen;
 fetch(abs.href,{credentials:'same-origin',cache:'no-store',headers:{Accept:'text/html'}}).then(function(res){
  if(gen!==grunionsNavGen) return;
  var ct=res.headers.get('content-type')||'';
  if(ct.indexOf('text/html')===-1){location.href=abs.href; return;}
  return res.text().then(function(html){
   if(gen!==grunionsNavGen) return;
   var dest=res.url||abs.href; if(abs.hash&&dest.indexOf('#')<0) dest+=abs.hash;
   grunionsApply(html,dest,pop);
  });
 }).catch(function(){if(gen===grunionsNavGen) location.href=abs.href;});
}
if(document.querySelector('nav.tabs')){
 history.scrollRestoration='manual';
 history.replaceState({grunions:1},'',location.href);
 document.addEventListener('click',function(e){
  if(e.defaultPrevented||e.button||e.metaKey||e.ctrlKey||e.shiftKey||e.altKey) return;
  var a=e.target.closest&&e.target.closest('a'); if(!a||!a.href||a.hasAttribute('download')) return;
  if(a.target&&a.target!=='_self') return;
  var abs; try{abs=new URL(a.href,location.href);}catch(err){return;}
  if(abs.origin!==location.origin) return;
  if(/^\\/(logout|login|join|auth\\/|static\\/|api\\/)/.test(abs.pathname)) return;
  if(/\\.(csv|svg|png|webp|jpe?g|gif)$/i.test(abs.pathname)) return;
  if(abs.pathname===location.pathname&&abs.search===location.search){
   e.preventDefault();
   if(abs.hash&&abs.hash!==location.hash){
    history.pushState({grunions:1},'',abs.pathname+abs.search+abs.hash);
    var el=document.getElementById(abs.hash.slice(1)); if(el) el.scrollIntoView();
    var seen=/^#p(\\d+)$/.exec(abs.hash); if(seen&&abs.pathname==='/practices') grunionsSeen(seen[1]);
   }
   return;
  }
  e.preventDefault();
  var nav=a.closest('nav.tabs');
  if(nav){nav.querySelectorAll('a').forEach(function(x){x.classList.remove('on');}); a.classList.add('on');}
  grunionsGo(abs.href,false);
 });
 window.addEventListener('popstate',function(){if(document.querySelector('nav.tabs')) grunionsGo(location.href,true);});
}
</script>
<script>var PUSH_CSRF="{{csrf_token()}}",VAPID_PUBLIC="{{vapid_public_key()}}";</script>
</body></html>""")

ADMIN_NAV = """<div class="seg noprint">{% set ep = request.endpoint %}<a href=/admin class="{{'on' if ep=='admin'}}">Check-in</a>
{% if me().is_admin %}<a href=/members class="{{'on' if ep=='members'}}">Members</a><a href=/export class="{{'on' if ep=='export_page'}}">Export</a><a href=/admins class="{{'on' if ep=='admins'}}">Roles</a><a href=/expiring class="{{'on' if ep=='expiring'}}">Expiring</a>
<a href=/import class="{{'on' if ep=='import_page'}}">Import</a><a href=/requirements class="{{'on' if ep=='requirements_page'}}">Rules</a><a href=/qr class="{{'on' if ep=='qr_page'}}">QR</a>{% endif %}</div>
{% set al = admin_alert() %}{% if al %}<a href=/expiring class="note noprint" style="display:block;text-decoration:none"><span class="st st-warn"></span> USAWP: <b>{{al[0]}}</b> expired · <b>{{al[1]}}</b> expiring within {{EXPIRING_DAYS}} days</a>{% endif %}
{% for n in admin_notices() %}<div class=note>{{n.body}}</div>{% endfor %}"""

T = {}
T["join"] = """<h1>Join the Grunions</h1>
<p class=t2>Tuesdays at Marina High School and Fridays at Westminster High School, 7–8:30 PM. Membership is $45/mo starting in November; a current USA Water Polo membership is required.</p>
<form method=post>{{csrf_field()}}
<label>Legal first name<input name=first required autocomplete=given-name></label>
<label>Preferred first name (optional)<input name=preferred_first autocomplete=off placeholder="Leave blank to use your legal first name"></label>
<label>Legal last name<input name=last required autocomplete=family-name></label>
<label>Email<input name=email type=email required autocomplete=email placeholder="The one on your USA Water Polo account"></label>
<label>Phone<input name=phone type=tel required autocomplete=tel></label>
<button class="primary full">Create account</button></form>
<p class="t3 sm" style="text-align:center;margin-top:20px">Already a member? <a href=/login>Log in</a></p>"""

T["login"] = """<h1>Log in</h1>
{% if google_enabled() %}<a class="btn full" href=/auth/google style="background:var(--surface2);color:var(--t1);border:1px solid var(--line)"><svg width=18 height=18 viewBox="0 0 48 48" aria-hidden=true><path fill="#EA4335" d="M24 9.5c3.5 0 6.6 1.2 9.1 3.6l6.8-6.8C35.8 2.4 30.3 0 24 0 14.6 0 6.6 5.4 2.7 13.3l7.9 6.1C12.5 13.6 17.8 9.5 24 9.5z"/><path fill="#4285F4" d="M46.1 24.5c0-1.6-.1-3.1-.4-4.5H24v9h12.4c-.5 2.9-2.2 5.3-4.6 6.9l7.4 5.7c4.3-4 6.9-9.9 6.9-17.1z"/><path fill="#FBBC05" d="M10.6 28.6c-.5-1.4-.8-3-.8-4.6s.3-3.2.8-4.6l-7.9-6.1C1 16.6 0 20.2 0 24s1 7.4 2.7 10.7l7.9-6.1z"/><path fill="#34A853" d="M24 48c6.5 0 11.9-2.1 15.9-5.8l-7.4-5.7c-2.1 1.4-4.8 2.3-8.5 2.3-6.2 0-11.5-4.1-13.4-9.9l-7.9 6.1C6.6 42.6 14.6 48 24 48z"/></svg>Sign in with Google</a>
<p class="t3 sm" style="text-align:center;margin:16px 0 4px">or</p>{% endif %}<p class=t2>We'll email you a one-time login link.</p>
<form method=post>{{csrf_field()}}<label>Email<input name=email type=email required autocomplete=email></label>
<button class="primary full">Send login link</button></form>
<p class="t3 sm" style="text-align:center;margin-top:20px">New here? <a href=/join>Join the team</a></p>"""

T["home"] = """<h1>Hi, {{display_first(m)}}</h1>
{{ push_card() }}
{% for n in notices %}<div class="note notice">{{n.body}}</div>{% endfor %}
{% set cl = clearance(m) %}{% set dl = days_left(m.usawp_valid_until) %}{% set tw = trial_window(m) %}{% set ex = expiry_notes(m, cl) %}
<div class=card><div style="display:flex;align-items:center;justify-content:space-between">
{% if vr_pending %}<div style="font-size:19px;font-weight:600">Verification pending</div>{{ st('warn','Pending') }}
{% elif cl.ok and tw and tw.active and m.usawp_status != 'verified' %}<div style="font-size:19px;font-weight:600">Cleared to play</div>{{ st('trial', trial_badge(tw)) }}
{% elif cl.ok %}<div style="font-size:19px;font-weight:600">Cleared to play</div>{{ st('ok','Cleared') }}
{% else %}<div style="font-size:19px;font-weight:600">Not cleared to play</div>{{ st('bad','Not cleared') }}{% endif %}</div>
{% set cc = coach_clearance(m) %}{% if cc %}<div style="margin-top:8px">{{ st('ok' if cc.ok else 'bad', cc.text) }}</div>{% endif %}
{% if coach_eligibility(m).text %}<div style="margin-top:8px">{{ coach_tag(m) }}</div>{% endif %}
{% if not cl.ok %}{% if not vr_pending %}{% for line in ex.lines %}<p class="sm" style="margin:8px 0 0">{{line}}</p>{% endfor %}{% elif ex.safesport %}<p class="sm" style="margin:8px 0 0">SafeSport expired {{ex.safesport}}</p>{% endif %}
{% if ex.rest %}<p class="t2 sm" style="margin:8px 0 0">Needs: {{ex.rest|join(', ')}}</p>{% endif %}{% endif %}
{% if tw and tw.active and not ex.membership and m.usawp_status != 'verified' and not vr_pending %}<p class="sm" style="margin:8px 0 0">Ends {{tw.ends}}</p>{% elif tw and tw.expired and not ex.membership and m.usawp_status != 'verified' and not vr_pending %}<p class="sm" style="margin:8px 0 0">Trial ended {{tw.ends}}</p>{% endif %}
{% if m.usawp_status=='verified' and dl is not none and dl <= EXPIRING_DAYS %}<p class="sm" style="margin:8px 0 0"><span class="st st-warn"></span> Your membership expires in <b>{{dl}} days</b> ({{m.usawp_valid_until}}). <a href=https://usawp.sport80.com>Renew</a></p>{% endif %}
{% if m.usawp_status != 'verified' %}<p class="t2 sm" style="margin:8px 0 0">Register or renew at <a href=https://usawp.sport80.com>usawp.sport80.com</a> with {{m.email}} and choose Grunions as your club.</p>{% endif %}
{% if ex.membership and not vr_pending %}
<button type=button class="primary full" id=reverifyOpen style="margin-top:14px">Reverify membership</button>
<form id=reverifyForm hidden method=post action=/home style="margin-top:14px">{{csrf_field()}}
<div class=row style="align-items:flex-end"><label style="margin:0">USAWP Membership #<input name=usawp_number inputmode=numeric value="{{m.usawp_number or ''}}" autocomplete=off></label>
<label style="margin:0">Background screening expires<input name=background_expires type=date value="{{ (background_view(m).date if background_view(m) else '') }}"></label>
<button class=primary style="flex:0 0 auto">Send</button></div></form>
<script>document.getElementById('reverifyOpen').onclick=function(){var f=document.getElementById('reverifyForm');f.hidden=false;this.hidden=true;f.querySelector('input[name=usawp_number]').focus()};</script>
{% elif m.usawp_status == 'verified' %}
{% if m.usawp_number %}<p class="sm" style="margin:12px 0 0">USAWP # {{m.usawp_number}}</p>{% endif %}
{% set bg = background_view(m) %}{% if bg and bg.kind == 'bad' and not vr_pending %}
<form method=post action=/home style="margin-top:14px">{{csrf_field()}}<input type=hidden name=action value=reverify_background>
<button class="primary full">Reverify background screening</button></form>{% endif %}
{% elif m.usawp_number %}
<div class=usawp-line><span>USAWP # {{m.usawp_number}}</span><button type=button class=compact id=usawpEdit>Edit</button></div>
<form id=usawpForm hidden method=post action=/home>{{csrf_field()}}
<div class=row style="align-items:flex-end"><label style="margin:0">USAWP Membership #<input name=usawp_number inputmode=numeric value="{{m.usawp_number}}" autocomplete=off></label>
<button class=primary style="flex:0 0 auto">Save</button></div></form>
<script>document.getElementById('usawpEdit').onclick=function(){var f=document.getElementById('usawpForm');f.hidden=!f.hidden;if(!f.hidden)f.querySelector('input[name=usawp_number]').focus()};</script>
{% else %}<form method=post action=/home style="margin-top:14px">{{csrf_field()}}
<div class="row wrap" style="align-items:flex-end"><label style="margin:0;flex:1 1 180px">USAWP Membership #<input name=usawp_number inputmode=numeric value="" autocomplete=off></label>
<button class=primary style="flex:0 0 auto">Add</button>
{% if not tw %}<button type=button class=compact id=trialOpen style="flex:0 0 auto">2-week USAWP trial</button>{% endif %}</div></form>
{% if not tw %}<dialog id=trialDialog class=modal><div class=sheet>
<p>I will complete the USA Water Polo 2-week trial membership before I get in the pool. I understand I need to get a full USAWP membership soon, otherwise I will not be able to practice.</p>
<form method=post action=/home>{{csrf_field()}}<input type=hidden name=action value=trial>
<button class="primary full">I confirm</button></form>
<a class="btn full" style="margin-top:10px" href="{{TRIAL_JOIN_URL}}" target=_blank rel=noopener>Get USAWP trial membership</a>
</div></dialog>
<script>document.getElementById('trialOpen').onclick=function(){document.getElementById('trialDialog').showModal()};
document.getElementById('trialDialog').addEventListener('click',function(e){if(e.target===this)this.close()});</script>{% endif %}
{% endif %}</div>
{% if nextp %}<div class=card><div class="t3 xs">NEXT PRACTICE</div><div style="font-size:18px;font-weight:600;margin-top:2px">{{fmt_d(nextp.date)}}, {{fmt_t(nextp.start)}}</div>
<div class=t2>{{nextp.location}} · {{nextp_n}} going</div>
{% if next_coaches %}<div class=t2>Coaches: {{next_coaches}}</div>{% endif %}
{% if me().is_admin %}{% if not next_any %}<div class="sm" style="margin-top:6px">{{ st('warn', 'No assigned coach is coach-eligible') }}</div>{% endif %}
{% for c in next_rows %}{% if coach_eligibility(c).text %}<div class="sm" style="margin-top:4px">{{ coach_tag(c) }}</div>{% endif %}{% endfor %}{% endif %}
<form method=post action=/practices style="margin-top:14px">{{csrf_field()}}<input type=hidden name=pid value={{nextp.id}}>
{% if nextp_mine == 1 %}<button class=full name=action value=clear>Going ✓</button>{% else %}<button class="primary full" name=action value=going>I'm going</button>{% endif %}</form></div>{% endif %}
{% if ann %}<div class=card><div class="t3 xs">ANNOUNCEMENT · {{display_first(ann)|upper}}</div><p style="margin:6px 0 0">{{ann.body}}</p></div>{% endif %}
<details class=card><summary>Membership &amp; requirements</summary><div class=body>
<div class=kv><span>USA Water Polo</span>{{ usawp(m.usawp_status) }}</div>
<div class=kv><span>Member #</span><span>{{m.usawp_number or '—'}}</span></div><div class=kv><span>Expires</span><span>{{m.usawp_valid_until or '—'}}</span></div>
{% if m.usawp_verified_at %}<div class=kv><span>Verified</span><span>{{m.usawp_verified_at[:10]}}</span></div>{% endif %}
{% for it in cl.checks %}<div class=kv><span>{{it.req.name}}</span>{{ st({'ok':'ok','no date':'warn'}.get(it.status,'bad'),
 (('expires ' ~ it.mr.expires_on) if it.mr and it.mr.expires_on else ('done ' ~ it.mr.completed_on) if it.mr and it.mr.completed_on else 'missing') if it.status!='expired' else 'expired') }}</div>{% endfor %}
{% if background_view(m) %}<div class=kv>{{ bg_line(m) }}</div>{% endif %}
</div></details>
<details class=card><summary>Attendance <span class="t3 sm" style="margin-left:auto;margin-right:10px">{{hist|length}} total · {{nmonth}} this month</span></summary><div class=body>
{% for h in hist[:20] %}<div class=kv><span>{{fmt_d(h.practice_date)}}</span><span class=t2>{{h.location}}</span></div>{% else %}<p class=t3>No practices yet.</p>{% endfor %}</div></details>
<details class=card><summary>Profile</summary><div class=body>
<div class=kv><span>Legal name</span><span>{{m.first}} {{m.last}}</span></div>
<form method=post action=/home>{{csrf_field()}}<input type=hidden name=action value=preferred>
<label>Preferred first name (optional)<input name=preferred_first value="{{m.preferred_first or ''}}" placeholder="Leave blank to use your legal first name" autocomplete=off></label>
<button class=full>Save</button></form>
<div class=kv><span>Email</span><span>{{m.email}}</span></div>
<div class=kv><span>Phone</span><span>{{m.phone}}</span></div><div class=kv><span>Role</span><span>{{role_label(m)|capitalize}}</span></div>
<p class="sm" style="margin:8px 0 0"><a href=/notifications>Notification settings</a></p></div></details>"""

T["notifications"] = """<h1>Notifications</h1>
{{ push_card() }}
<form method=post action=/notifications>{{csrf_field()}}
<div class=list>{% for key, label in types %}
<label class=li><input type=checkbox name=push value="{{key}}" {% if prefs.get(key, True) %}checked{% endif %}>{{label}}</label>
{% endfor %}</div>
<label style="margin-top:16px"><input type=checkbox name=email_reminders value=1 {% if email_on %}checked{% endif %}>Email reminders for membership, SafeSport, and the 2-week trial</label>
<p class="t3 sm">These emails go out 7 days before, 1 day before, and on the day it expires. Practice cancellation emails always send.</p>
<button class="primary full">Save</button></form>"""

T["chat"] = """{% if is_staff() %}<div class=seg><a href=/chat class="{{'on' if ch=='team'}}" data-badge=team>Team{{ bubble(badges().team) }}</a><a href="/chat?c=coaches" class="{{'on' if ch=='coaches'}}" data-badge=coaches>Coaches{{ bubble(badges().coaches) }}</a></div>{% else %}<h1>Team</h1>{% endif %}
<div class=chat id=chat></div><div style=height:90px></div>
<div class="composer noprint"><div class=preview id=prev hidden><img id=prevImg alt=""><span id=prevName></span><button type=button class="quiet compact" id=prevX>Remove</button></div>
<form id=f><input type=file id=file accept="image/jpeg,image/png,image/gif,image/webp,image/heic,image/heif,.heic" hidden>
<button type=button class="iconbtn" id=attach title="Attach image" aria-label="Attach image"><svg viewBox="0 0 24 24"><rect x="3" y="4" width="18" height="16" rx="2"/><circle cx="9" cy="10" r="2"/><path d="m21 16-5-5-9 9"/></svg></button>
<textarea id=body rows=1 maxlength=2000 placeholder="Message {{'coaches' if ch=='coaches' else 'the team'}}"></textarea>
<button class="iconbtn send" type=submit aria-label=Send><svg viewBox="0 0 24 24" aria-hidden=true><path d="m22 2-7 20-4-9-9-4Z"/><path d="M22 2 11 13"/></svg></button></form></div>
<dialog id=actSheet class=modal><div class=sheet>
<div class=emojirow id=actEmoji>{% for e in REACTIONS %}<button type=button>{{e}}</button>{% endfor %}</div>
<p id=actConfirm hidden>Delete this message?</p>
<button type=button class=full id=actEdit>Edit</button>
<button type=button class="full danger" id=actDelete>Delete</button>
<button type=button class="quiet full" id=actCancel>Cancel</button>
</div></dialog>
<script>
const CSRF="{{csrf_token()}}",CH="{{ch}}",EMO={{REACTIONS|tojson}};let last=0;const box=document.getElementById('chat'),msgs={};
const esc=s=>s.replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const t=iso=>new Date(iso).toLocaleString([], {weekday:'short',hour:'numeric',minute:'2-digit'});
function rxHtml(id,r){r=r||{};return EMO.filter(e=>r[e]).map(e=>`<button type=button class="${r[e].mine?'on':''}" data-m=${id} data-e="${e}">${e} ${r[e].n}</button>`).join('')}
function bodyHtml(m){
 if(m.deleted) return '<div class="txt deleted">Message deleted</div>';
 let h=m.body?`<div class=txt>${esc(m.body)}${m.edited?' <span class=edited>(edited)</span>':''}</div>`:'';
 if(m.image) h+=`<a class=img href="${m.image.full}" data-full="${m.image.full}"><img src="${m.image.thumb}" alt="Photo from ${esc(m.who)}" loading=lazy></a>`;
 return h}
function fill(d,m){
 d.className='m'+(m.mine?' mine':'')+(m.ann&&!m.deleted?' ann':'');
 d.innerHTML=(m.deleted?'':`<button type=button class=more data-act=${m.id} aria-label="Message actions">⋯</button>`)+
  `<div class=who>${m.ann&&!m.deleted?'Announcement · ':''}${esc(m.who)} · ${t(m.at)}</div>`+bodyHtml(m)+`<div class=rx>${rxHtml(m.id)}</div>`}
function add(m){msgs[m.id]=m;last=Math.max(last,m.id);if(document.getElementById('msg'+m.id))return;const d=document.createElement('div');d.id='msg'+m.id;fill(d,m);box.appendChild(d)}
function upsert(m,force){msgs[m.id]=m;const d=document.getElementById('msg'+m.id);if(!d){add(m);return}last=Math.max(last,m.id);if(!force&&d.querySelector('.editbox'))return;fill(d,m)}
function paintRx(map){document.querySelectorAll('.m').forEach(el=>{const id=el.id.slice(3),rx=el.querySelector('.rx');if(!rx)return;const h=rxHtml(id,map[id]);if(rx.dataset.h!==h){rx.innerHTML=h;rx.dataset.h=h}})}
let pollGen=0;
async function poll(){const gen=++pollGen,epoch=window.grunionsNavEpoch|0;try{const r=await fetch('/api/messages?c='+CH+'&after='+last);const j=await r.json();if(gen!==pollGen||(window.grunionsNavEpoch|0)!==epoch)return;const end=innerHeight+scrollY>=document.body.scrollHeight-120;
 j.forEach(add);const sync=await (await fetch('/api/messages?c='+CH+'&sync=1')).json();if(gen!==pollGen||(window.grunionsNavEpoch|0)!==epoch)return;sync.forEach(m=>{if(gen===pollGen)upsert(m)});
 const rx=await (await fetch('/api/reactions?c='+CH)).json();if(gen!==pollGen||(window.grunionsNavEpoch|0)!==epoch)return;paintRx(rx);if(window.grunionsRefresh)grunionsRefresh();if(j.length&&end)scrollTo(0,document.body.scrollHeight)}catch(e){}}
const sheet=document.getElementById('actSheet'),actEmoji=document.getElementById('actEmoji'),actEdit=document.getElementById('actEdit'),actDelete=document.getElementById('actDelete'),actConfirm=document.getElementById('actConfirm');
let actId=null,confirming=false;
function closeSheet(){if(sheet.open)sheet.close();actId=null;confirming=false;actConfirm.hidden=true;actDelete.textContent='Delete'}
function openSheet(id){const m=msgs[id];if(!m||m.deleted)return;actId=id;confirming=false;actConfirm.hidden=true;actDelete.textContent='Delete';
 actEmoji.innerHTML=EMO.map(e=>`<button type=button data-e="${e}" data-m=${id}>${e}</button>`).join('');
 actEdit.hidden=!(m.mine&&!m.deleted);actDelete.hidden=!m.can_delete;sheet.showModal()}
function startEdit(id){const m=msgs[id],d=document.getElementById('msg'+id);if(!d||!m||m.deleted||d.querySelector('.editbox'))return;
 const boxe=document.createElement('div');boxe.className='editbox';
 boxe.innerHTML='<textarea maxlength=2000></textarea><div class=row style="margin-top:8px"><button type=button class=primary data-save>Save</button><button type=button class=quiet data-cancel>Cancel</button></div>';
 boxe.querySelector('textarea').value=m.body||'';const txt=d.querySelector('.txt');if(txt)txt.replaceWith(boxe);else d.querySelector('.who').after(boxe);
 boxe.querySelector('[data-save]').onclick=async()=>{pollGen++;const r=await fetch('/api/messages/'+id,{method:'POST',headers:{'Content-Type':'application/json','X-CSRF':CSRF},body:JSON.stringify({body:boxe.querySelector('textarea').value})});const j=await r.json().catch(()=>({}));if(!r.ok){alert(j.error||'Could not save.');return}if(j.message)upsert(j.message,true)};
 boxe.querySelector('[data-cancel]').onclick=()=>upsert(msgs[id],true);
 d.scrollIntoView({block:'center'});boxe.querySelector('textarea').focus()}
actEdit.onclick=(e)=>{e.preventDefault();e.stopPropagation();const id=actId;closeSheet();setTimeout(()=>startEdit(id),0)};
actDelete.onclick=async()=>{if(!confirming){confirming=true;actConfirm.hidden=false;return}
 const id=actId;pollGen++;const r=await fetch('/api/messages/'+id,{method:'DELETE',headers:{'X-CSRF':CSRF}}),j=await r.json().catch(()=>({}));closeSheet();if(r.ok&&j.message)upsert(j.message,true)};
document.getElementById('actCancel').onclick=closeSheet;
sheet.addEventListener('click',e=>{if(e.target===sheet)closeSheet()});
sheet.addEventListener('close',()=>{confirming=false;actConfirm.hidden=true;actDelete.textContent='Delete'});
actEmoji.addEventListener('click',async e=>{const b=e.target.closest('button');if(!b)return;pollGen++;
 await fetch('/api/messages/'+b.dataset.m+'/react',{method:'POST',headers:{'Content-Type':'application/json','X-CSRF':CSRF},body:JSON.stringify({emoji:b.dataset.e})});closeSheet();poll()});
box.addEventListener('pointerdown',e=>{if(e.button)return;if(e.target.closest('button,a,textarea,.editbox'))return;const row=e.target.closest('.m');if(!row)return;
 const id=+row.id.slice(3),x=e.clientX,y=e.clientY,timer=setTimeout(()=>openSheet(id),500);
 const cancel=ev=>{if(ev.type==='pointermove'&&Math.hypot(ev.clientX-x,ev.clientY-y)<10)return;clearTimeout(timer);row.removeEventListener('pointerup',cancel);row.removeEventListener('pointercancel',cancel);row.removeEventListener('pointermove',cancel)};
 row.addEventListener('pointerup',cancel);row.addEventListener('pointercancel',cancel);row.addEventListener('pointermove',cancel)});
box.addEventListener('contextmenu',e=>{const row=e.target.closest('.m');if(!row||e.target.closest('textarea'))return;e.preventDefault();openSheet(+row.id.slice(3))});
box.addEventListener('click',async e=>{
 const b=e.target.closest('button,a.img');if(!b||b.dataset.save!=null||b.hasAttribute('data-cancel'))return;
 if(b.matches('a.img')){e.preventDefault();const lb=document.createElement('div');lb.className='lightbox';lb.innerHTML=`<img src="${b.dataset.full}" alt="">`;lb.onclick=()=>lb.remove();document.body.appendChild(lb);return}
 if(b.dataset.act){openSheet(+b.dataset.act);return}
 if(b.dataset.e){pollGen++;await fetch('/api/messages/'+b.dataset.m+'/react',{method:'POST',headers:{'Content-Type':'application/json','X-CSRF':CSRF},body:JSON.stringify({emoji:b.dataset.e})});poll()}});
const ta=document.getElementById('body'),file=document.getElementById('file'),prev=document.getElementById('prev');
function grow(){ta.style.height='auto';ta.style.height=Math.min(ta.scrollHeight,136)+'px'}ta.addEventListener('input',grow);
document.getElementById('attach').onclick=()=>file.click();
file.onchange=()=>{const f=file.files[0];if(!f)return;if(f.size>8*1024*1024){alert('Image is larger than 8 MB.');file.value='';return}
 prev.hidden=false;document.getElementById('prevName').textContent=f.name;document.getElementById('prevImg').src=URL.createObjectURL(f)};
document.getElementById('prevX').onclick=()=>{file.value='';prev.hidden=true};
document.getElementById('f').onsubmit=async e=>{e.preventDefault();const f=file.files[0];if(!ta.value.trim()&&!f)return;
 let r;if(f){const fd=new FormData();fd.append('body',ta.value);fd.append('image',f);
  r=await fetch('/api/messages?c='+CH,{method:'POST',headers:{'X-CSRF':CSRF},body:fd})}
 else r=await fetch('/api/messages?c='+CH,{method:'POST',headers:{'Content-Type':'application/json','X-CSRF':CSRF},body:JSON.stringify({body:ta.value})});
 if(!r.ok){const j=await r.json().catch(()=>({}));alert(j.error||'Could not send.');return}
 const epoch=window.grunionsNavEpoch|0;ta.value='';grow();file.value='';prev.hidden=true;await poll();if((window.grunionsNavEpoch|0)!==epoch)return;scrollTo(0,document.body.scrollHeight)};
ta.addEventListener('keydown',e=>{if(e.key==='Enter'&&!e.shiftKey&&!e.isComposing){e.preventDefault();document.getElementById('f').requestSubmit()}});
poll().then(()=>scrollTo(0,document.body.scrollHeight));setInterval(poll,3000);
</script>"""

T["practices"] = """<h1>Schedule</h1><p class="t2 sm" style="margin-top:-12px">Tue · Marina HS &nbsp;·&nbsp; Fri · Westminster HS &nbsp;·&nbsp; 7–8:30 PM</p>
{% for x in data %}{% set p = x.p %}<div class=card id=p{{p.id}} data-pid={{p.id}} {% if p.cancelled %}style="opacity:.55"{% endif %}>
<div style="display:flex;justify-content:space-between;align-items:baseline;gap:12px"><div><div class=pdate style="font-size:18px;font-weight:600">{{fmt_d(p.date)}}{% if x.unseen %}<span class=badge data-seen={{p.id}}>{{ x.unseen if x.unseen < 100 else '99+' }}</span>{% endif %}</div>
<div class="t2 sm">{{fmt_t(p.start)}}–{{fmt_t(p.end)}} · {{p.location}}</div>
{% if x.coach_names %}<div class="t2 sm">Coaches: {{ x.coach_names|join(', ') }}</div>{% endif %}
{% if me().is_admin and not p.cancelled %}{% if not x.any_eligible %}<div class="sm" style="margin-top:6px">{{ st('warn', 'No assigned coach is coach-eligible') }}</div>{% endif %}
{% for c in x.coaches %}{% if coach_eligibility(c).text %}<div class="sm" style="margin-top:4px">{{ coach_tag(c) }}</div>{% endif %}{% endfor %}{% endif %}
{% if p.note %}<div class="t3 sm">{{p.note}}</div>{% endif %}</div>
<div>{% if p.cancelled %}{{ st('bad','Cancelled') }}{% else %}<button type=button class=gobtn aria-expanded=false aria-controls=who{{p.id}}
 onclick="const w=document.getElementById('who{{p.id}}');w.hidden=!w.hidden;this.setAttribute('aria-expanded',!w.hidden)">{{x.going|length}} going</button>{% endif %}</div></div>
{% if not p.cancelled %}<div id=who{{p.id}} class="t2 sm" hidden style="margin-top:10px;padding-top:10px;border-top:1px solid var(--line)">
{% for r in x.going %}{{display_first(r)}} {{r.last[:1]}}.{{', ' if not loop.last}}{% else %}<span class=t3>No one yet.</span>{% endfor %}
{% if x.notgoing %}<div class=t3>Can't make it: {% for r in x.notgoing %}{{display_first(r)}} {{r.last[:1]}}.{{', ' if not loop.last}}{% endfor %}</div>{% endif %}</div>{% endif %}
{% if not p.cancelled %}<form method=post class=row style="margin-top:14px">{{csrf_field()}}<input type=hidden name=pid value={{p.id}}>
{% if x.mine == 1 %}<button name=action value=clear>Going ✓</button>{% else %}<button class=primary name=action value=going>Going</button>{% endif %}
{% if x.mine == 0 %}<button name=action value=clear>Not going ✓</button>{% else %}<button class=quiet name=action value=notgoing style="flex:0 0 auto">Can't make it</button>{% endif %}</form>
{% endif %}
{% if me().is_admin %}<details style="margin:4px -18px -18px"><summary class="t3 sm">Edit practice</summary><form method=post style="padding:0 18px 18px">{{csrf_field()}}<input type=hidden name=pid value={{p.id}}>
<div class=row><label>Start<input type=time name=start value={{p.start}}></label><label>End<input type=time name=end value={{p.end}}></label></div>
<label>Location<input name=location value="{{p.location}}"></label><label>Note<input name=note value="{{p.note or ''}}"></label>
<div class=checks role=group aria-label="Coaches"><div class="t3 xs">Coaches</div>
{% for c in coach_choices %}<label><input type=checkbox name=coach value="{{c.id}}" {% if c.id in x.coach_ids %}checked{% endif %}>{{display_first(c)}} {{c.last}} {{ coach_tag(c) }}</label>
{% else %}<p class="t3 sm">No coaches yet. Mark a member as a coach on Members.</p>{% endfor %}</div>
<div class=row><button name=action value=edit>Save</button>{% if p.cancelled %}<button name=action value=restore>Restore</button>{% else %}<button class=danger name=action value=cancel>Cancel practice</button>{% endif %}</div>
<a class="btn quiet full" href="/admin?date={{p.date}}" style="margin-top:6px">Open check-in</a></form></details>{% endif %}</div>{% endfor %}
{% if me().is_admin %}<details class=card><summary>Add a practice</summary><form method=post class=body>{{csrf_field()}}<label>Date<input type=date name=date required></label>
<div class=row><label>Start<input type=time name=start value=19:00></label><label>End<input type=time name=end value=20:30></label></div>
<label>Location<input name=location required></label><label>Note<input name=note></label><button class="primary full" name=action value=add>Add practice</button></form></details>{% endif %}"""

_CHEV_L = '<svg width="20" height="20" viewBox="0 0 24 24" aria-hidden="true"><path d="M15 6 9 12l6 6" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>'
_CHEV_R = '<svg width="20" height="20" viewBox="0 0 24 24" aria-hidden="true"><path d="M9 6l6 6-6 6" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>'
_CAL_I = '<svg width="18" height="18" viewBox="0 0 24 24" aria-hidden="true"><rect x="3" y="5" width="18" height="16" rx="2" fill="none" stroke="currentColor" stroke-width="1.8"/><path d="M3 10h18M8 3v4M16 3v4" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/></svg>'
T["admin"] = ADMIN_NAV + """
<form class="row noprint" method=get action=/admin style="margin-bottom:8px"><div class=calpick id=calPick data-date="{{date}}" data-q="{{q}}" data-dates='{{ days|tojson }}'>
{% if prev_d %}<a class=calnav href="/admin?date={{prev_d}}{% if q %}&amp;q={{q|urlencode}}{% endif %}" aria-label="Previous practice">""" + _CHEV_L + """</a>{% else %}<span class=calnav aria-disabled=true aria-label="Previous practice">""" + _CHEV_L + """</span>{% endif %}
<button type=button class=calbtn id=calOpen aria-haspopup=dialog aria-expanded=false aria-controls=calPop>""" + _CAL_I + """<span>{{fmt_d(date)}}</span></button>
{% if next_d %}<a class=calnav href="/admin?date={{next_d}}{% if q %}&amp;q={{q|urlencode}}{% endif %}" aria-label="Next practice">""" + _CHEV_R + """</a>{% else %}<span class=calnav aria-disabled=true aria-label="Next practice">""" + _CHEV_R + """</span>{% endif %}
<div class=calpop id=calPop hidden role=dialog aria-label="Choose a practice"><div class=calhead>
<button type=button class=calmonth id=calPrevM aria-label="Previous month">""" + _CHEV_L + """</button><div class=lbl id=calLabel>{{month.label}}</div>
<button type=button class=calmonth id=calNextM aria-label="Next month">""" + _CHEV_R + """</button></div>
<div class=calwd><span>S</span><span>M</span><span>T</span><span>W</span><span>T</span><span>F</span><span>S</span></div>
<div class=calgrid id=calGrid>{% for c in month.cells %}{% if c is none %}<span class=calday></span>{% elif c.has %}<a class="calday{{' on' if c.on}}" href="/admin?date={{c.iso}}{% if q %}&amp;q={{q|urlencode}}{% endif %}">{{c.day}}</a>{% else %}<span class=calday aria-disabled=true>{{c.day}}</span>{% endif %}{% endfor %}</div></div></div>
<input type=hidden name=date value="{{date}}"><input name=q value="{{q}}" placeholder="Search" style="margin:0"></form>
<h1 style="margin:20px 0 4px">{{loc}}</h1><p class="t2 sm">{{fmt_d(date)}} · {{n}} checked in{% if pr %} · {{rsvp_n}} RSVP'd{% else %} · no practice scheduled{% endif %}</p>
{% if coach_names %}<p class="t2 sm" style="margin-top:0">Coaches: {{ coach_names|join(', ') }}</p>{% endif %}
{% if coach_warn %}<p class="sm" style="margin-top:0">{{ st('warn', 'No assigned coach is coach-eligible') }}</p>{% endif %}
{% macro ci(r) %}
<div class=li><button type=button class=ci-name onclick="this.closest('.li').nextElementSibling.toggleAttribute('hidden')">
<div style="display:flex;align-items:center;min-width:0;font-weight:500"><span class=ell>{{display_first(r)}} {{r.last}}</span>{{ coach_tag(r) }}{{ referee_tag(r) }}</div>
{% if background_view(r) %}<div class="xs" style="margin-top:4px">{{ bg_line(r) }}</div>{% endif %}
{{ member_status(r) }}</button>
<form method=post>{{csrf_field()}}<input type=hidden name=member_id value={{r.id}}><input type=hidden name=date value={{date}}><input type=hidden name=q value="{{q}}">
{% if r.cid %}<button class=compact name=action value=undo title="Undo check-in">Checked in</button>{% else %}<button class="primary compact">Check in</button>{% endif %}</form></div>
{{ member_panel(r) }}{% endmacro %}
<h2>Going <span class=t3>{{going|length}}</span></h2>
<div class=list>{% for r in going %}{{ ci(r) }}{% else %}<div class=li><span class=t3>No one yet.</span></div>{% endfor %}</div>
<h2>Everyone else <span class=t3>{{rest|length}}</span></h2>
<div class=list>{% for r in rest %}{{ ci(r) }}{% else %}<div class=li><span class=t3>No one yet.</span></div>{% endfor %}</div>
<details class=checkin><summary>Checked in <span class=t3>{{checked|length}}</span></summary>
<div class=list>{% for r in checked %}{{ ci(r) }}{% else %}<div class=li><span class=t3>No one yet.</span></div>{% endfor %}</div></details>
<script>if(/^#m\\d+$/.test(location.hash)){const p=document.querySelector(location.hash);if(p){const d=p.closest('details');if(d)d.open=true;p.removeAttribute('hidden')}}
(function(){
var root=document.getElementById('calPick'); if(!root) return;
var pop=document.getElementById('calPop'), openBtn=document.getElementById('calOpen'), grid=document.getElementById('calGrid'), label=document.getElementById('calLabel');
var dates=[]; try{dates=JSON.parse(root.getAttribute('data-dates')||'[]')}catch(err){dates=[]}
var set={}; dates.forEach(function(d){set[d]=1});
var q=root.getAttribute('data-q')||'', selected=root.getAttribute('data-date')||'', shown=selected.slice(0,7);
function pad(n){return (n<10?'0':'')+n}
function href(iso){return '/admin?date='+iso+(q?'&q='+encodeURIComponent(q):'')}
var months=['January','February','March','April','May','June','July','August','September','October','November','December'];
function render(ym){
 shown=ym; var parts=ym.split('-'), y=+parts[0], m=+parts[1];
 label.textContent=months[m-1]+' '+y;
 var blanks=new Date(y, m-1, 1).getDay(), last=new Date(y, m, 0).getDate(), html='', day, iso;
 for(var i=0;i<blanks;i++) html+='<span class=calday></span>';
 for(day=1; day<=last; day++){
  iso=y+'-'+pad(m)+'-'+pad(day);
  if(set[iso]) html+='<a class="calday'+(iso===selected?' on':'')+'" href="'+href(iso)+'">'+day+'</a>';
  else html+='<span class=calday aria-disabled=true>'+day+'</span>';
 }
 grid.innerHTML=html;
}
function shift(delta){
 var parts=shown.split('-'), y=+parts[0], m=+parts[1]+delta;
 if(m<1){m=12;y--} if(m>12){m=1;y++}
 render(y+'-'+pad(m));
}
document.getElementById('calPrevM').onclick=function(){shift(-1)};
document.getElementById('calNextM').onclick=function(){shift(1)};
openBtn.onclick=function(){
 var show=pop.hidden; pop.hidden=!show; openBtn.setAttribute('aria-expanded', show?'true':'false');
 if(show) render(selected.slice(0,7)||shown);
};
if(!window.grunionsCalDoc){
 window.grunionsCalDoc=1;
 document.addEventListener('click', function(e){
  var box=document.getElementById('calPick'), panel=document.getElementById('calPop'), btn=document.getElementById('calOpen');
  if(!box||!panel||panel.hidden) return;
  if(!box.contains(e.target)){panel.hidden=true; if(btn) btn.setAttribute('aria-expanded','false')}
 });
 document.addEventListener('keydown', function(e){
  if(e.key!=='Escape') return;
  var panel=document.getElementById('calPop'), btn=document.getElementById('calOpen');
  if(!panel||panel.hidden) return;
  panel.hidden=true; if(btn){btn.setAttribute('aria-expanded','false'); btn.focus()}
 });
}
})();
</script>"""

T["export_page"] = ADMIN_NAV + """<h1>Export</h1>
<div class=card><h2 style="margin:0 0 8px">Members</h2>
<p class="t2 sm">Legal name, preferred name, phone, role, clearance, USAWP number, membership, SafeSport, background screening, trial dates, and attendance.</p>
<a class="btn primary" href=/members.csv>Download members CSV</a></div>
<div class=card><h2 style="margin:0 0 8px">Practices and attendance</h2>
<form method=get action=/export/practices.csv>
<div class=row><label>Start<input type=date name=start value="{{start}}" required></label><label>End<input type=date name=end value="{{end}}" required></label></div>
<button class="primary full" name=detail value=0>Download practices CSV</button>
<button class=full style="margin-top:10px" name=detail value=1>Download detailed attendance CSV</button></form>
<p class="t3 sm" style="margin:12px 0 0">Practices is one row per practice, with the assigned coaches, a coach count, and how many of those coaches are coach-eligible. Detailed attendance is one row per member per practice, with RSVP and check-in.</p></div>
{% if sheet_on %}<div class=card><h2 style="margin:0 0 8px">Google Sheet</h2>
<p class="t2 sm">{% if sheet_status.at %}Last sync {{sheet_status.at}} PT · {{sheet_status.label}}{% else %}Not synced yet{% endif %}{% if sheet_status.detail and not sheet_status.ok %} · {{sheet_status.detail}}{% endif %}</p>
<p class="t3 sm">Members, Practices, and Attendance stay in sync after changes. A full rewrite also runs daily.</p>
<form method=post action=/export/sheet>{{csrf_field()}}<button class="primary full">Sync to Google Sheet now</button></form></div>{% endif %}"""

T["members"] = ADMIN_NAV + """<div style="display:flex;justify-content:space-between;align-items:baseline"><h1>Members</h1><a class="t2 sm" href=/members.csv>Export CSV</a></div>
<div class=seg><a href=/members {% if not coach_filter and not referee_filter %}class=on{% endif %}>All</a><a href="/members?coach=eligible" {% if coach_filter %}class=on{% endif %}>Coach eligible</a><a href="/members?referee=eligible" {% if referee_filter %}class=on{% endif %}>Referee eligible</a></div>
<p class="t2 sm">{% if referee_filter %}{{rows|length}} referee eligible{% elif coach_filter %}{{rows|length}} coach eligible{% else %}{{rows|length}} total · {% for s,v in c.items() %}{{v}} {{s}}{{' · ' if not loop.last}}{% endfor %}{% endif %}</p>
<div class="list loose">{% for r in rows %}{% set tw = trial_window(r) %}{% set ex = expiry_notes(r) %}<div class=li style="flex-wrap:wrap;align-items:flex-start"><div class=grow onclick="if(event.target.closest('.more,button,a,form,input,select'))return;this.closest('.li').nextElementSibling.toggleAttribute('hidden')" style="cursor:pointer;flex:1 1 100%"><div style="display:flex;align-items:center;justify-content:space-between;gap:8px;min-width:0"><span class=ell style="font-weight:500">{{display_first(r)}} {{r.last}}</span>
<span class=more><button type=button class=morebtn aria-label="Actions for {{display_first(r)}} {{r.last}}" aria-haspopup=menu aria-expanded=false>⋯</button>
<div class=menu hidden role=menu>
{% if r.is_admin %}{% if n_admins<=1 or r.email in boot %}<button type=button disabled title="{% if n_admins<=1 %}Last admin{% else %}Set by ADMIN_EMAIL{% endif %}">Remove admin</button>{% else %}<form method=post>{{csrf_field()}}<input type=hidden name=member_id value={{r.id}}><button name=action value=remove_admin>Remove admin</button></form>{% endif %}{% else %}<form method=post>{{csrf_field()}}<input type=hidden name=member_id value={{r.id}}><button name=action value=make_admin>Make admin</button></form>{% endif %}
{% if r.role=='coach' %}<form method=post>{{csrf_field()}}<input type=hidden name=member_id value={{r.id}}><button name=action value=remove_coach>Remove coach</button></form>{% else %}<form method=post>{{csrf_field()}}<input type=hidden name=member_id value={{r.id}}><button name=action value=make_coach>Make coach</button></form>{% endif %}
{% if not r.is_admin %}{% if r.id in listed %}<form method=post>{{csrf_field()}}<input type=hidden name=member_id value={{r.id}}><button name=action value=remove_coaching>Remove from coaching list</button></form>{% else %}<form method=post>{{csrf_field()}}<input type=hidden name=member_id value={{r.id}}><button name=action value=add_coaching>Add to coaching list</button></form>{% endif %}{% endif %}
</div></span></div>
<div class=memline>{{ usawp(r.usawp_status) }}<span>{% if r.usawp_valid_until %} · thru {{r.usawp_valid_until}}{% endif %} · {{r.email}}{% if r.preferred_first and r.preferred_first.strip() %} · legal {{r.first}}{% endif %} · {{r.visits}} practices</span></div>
{% if r.is_admin or r.id in listed or r.role=='coach' or coach_eligibility(r).text or referee_eligibility(r).text %}<div class=eligs>{% if r.is_admin or r.id in listed %}<span class=coach-tag>Coaching list</span>{% endif %}{% if r.is_admin or r.role=='coach' %}<span class=coach-tag>Coach</span>{% endif %}{% if usawp_coach_badge(r) %}<span class=coach-tag>USAWP coach</span>{% else %}{{ coach_tag(r) }}{% endif %}{{ referee_tag(r) }}</div>{% endif %}
{% if background_view(r) %}<div class="xs" style="margin-top:4px">{{ bg_line(r) }}</div>{% endif %}
{% if tw and tw.active and r.usawp_status != 'verified' and not ex.membership %}<div class="xs">{{ st('trial', trial_badge(tw)) }}<span class="t3 xs"> · Ends {{tw.ends}}</span></div>{% elif tw and tw.expired and r.usawp_status != 'verified' and not ex.membership %}<div class="xs">Trial ended {{tw.ends}}</div>{% endif %}
{% if not r.is_admin and r.role != 'coach' %}<form method=post style="margin-top:8px">{{csrf_field()}}<input type=hidden name=member_id value={{r.id}}><input type=hidden name=list_coach value="{{'eligible' if coach_filter else ''}}"><input type=hidden name=list_referee value="{{'eligible' if referee_filter else ''}}"><button class=compact name=action value=require_background>{% if r.require_background %}Don't require background{% else %}Require background{% endif %}</button></form>{% endif %}
</div></div>{{ member_panel(r) }}{% endfor %}</div>
<script>
(function(){
 function closeAll(){document.querySelectorAll('.menu').forEach(function(m){m.hidden=true; var b=m.parentNode.querySelector('.morebtn'); if(b) b.setAttribute('aria-expanded','false')})}
 document.querySelectorAll('.morebtn').forEach(function(btn){
  btn.onclick=function(e){e.stopPropagation(); var menu=btn.parentNode.querySelector('.menu'); var open=menu.hidden; closeAll(); if(open){menu.hidden=false; btn.setAttribute('aria-expanded','true')}};
 });
 if(!window.grunionsMore){window.grunionsMore=1;
  document.addEventListener('click', closeAll);
  document.addEventListener('keydown', function(e){if(e.key==='Escape') closeAll()});
 }
})();
</script>"""

T["expiring"] = ADMIN_NAV + """<h1>Expiring</h1>
<form class="row noprint" style="align-items:center;margin-bottom:8px"><span class="t2 sm" style="flex:0 0 auto">Window (days)</span><input name=days type=number value={{days}} onchange=this.form.submit() style="margin:0"></form>
{% for key, label in [('expired','Already expired'),('within_7','Next 7 days'),('within_%d'%days,'Next %d days'%days)] %}<h2>{{label}} <span class=t3>{{rep[key]|length}}</span></h2>
<div class=list>{% for r in rep[key] %}<div class=li><div class=grow><div style="font-weight:500">{{display_first(r)}} {{r.last}}</div>
<div class="t3 xs">{{r.item}} · {{r.usawp_valid_until}} · {% if r.days_left < 0 %}{{-r.days_left}}d ago{% else %}{{r.days_left}}d left{% endif %}</div></div>
<form method=post>{{csrf_field()}}<input type=hidden name=member_id value={{r.id}}><button class=compact>Remind</button></form></div>{% else %}<div class=li><span class=t3>None</span></div>{% endfor %}</div>{% endfor %}
<form method=post style="margin-top:20px">{{csrf_field()}}<button class="primary full">Remind everyone listed</button></form>
<p class="t3 xs" style="margin-top:10px">Reminders appear on each member's home screen. Daily report: <a href=/api/expiring>/api/expiring</a> or daily_expiry.py.</p>"""

T["requirements_page"] = ADMIN_NAV + """<h1>Requirements</h1><p class="t2 sm">Cleared to play means a verified, current USAWP membership and current SafeSport. Other items can stay on file for import; they do not block clearance. Keywords match Sport:80 export columns.</p>
{% for q in reqs %}<details class=card><summary><span>{{q.name}}</span><span class="t3 sm" style="margin-left:auto;margin-right:10px">{{q.applies_to}}{{'' if q.active else ' · off'}}</span></summary>
<form method=post class=body>{{csrf_field()}}<input type=hidden name=id value={{q.id}}>
<div class=row><label>Applies to<select name=applies_to>{% for o in ['all','athlete','coach'] %}<option {{'selected' if q.applies_to==o}}>{{o}}</option>{% endfor %}</select></label>
<label>Import keywords<input name=keywords value="{{q.keywords or ''}}"></label></div>
<label><input type=checkbox name=expires {{'checked' if q.expires}}>Has an expiration date</label><label><input type=checkbox name=active {{'checked' if q.active}}>Active</label>
<button class=full name=action value=save>Save</button></form></details>{% endfor %}
<details class=card><summary>Add requirement</summary><form method=post class=body>{{csrf_field()}}<label>Name<input name=name placeholder="CPR / First Aid"></label>
<div class=row><label>Applies to<select name=applies_to><option>all</option><option>athlete</option><option>coach</option></select></label><label>Keywords<input name=keywords placeholder="cpr,firstaid"></label></div>
<label><input type=checkbox name=expires checked>Has an expiration date</label><button class="primary full" name=action value=add>Add</button></form></details>"""

T["import_page"] = ADMIN_NAV + """<h1>Sport:80 import</h1>
<div class=card><ol class="t2 sm" style="margin:0;padding-left:18px;line-height:1.7">
<li>Log in at <a href=https://usawp.sport80.com>usawp.sport80.com</a> and switch to the Grunions club profile.</li>
<li>Members → Smart Lists → Edit Columns: name, email, membership status, member number, valid until, plus SafeSport / background columns.</li>
<li>Actions → Export Report, then upload the emailed file here.</li></ol></div>
<form method=post enctype=multipart/form-data>{{csrf_field()}}<input type=file name=file accept=".csv,.xlsx" style="padding:11px 14px"><button class="primary full" style="margin-top:12px">Import</button></form>
{% if stats %}<div class=note style="margin-top:16px">Read {{stats.rows}} rows · updated {{stats.matched}} members · {{stats.req_updates or 0}} compliance items · {{stats.unmatched|length}} roster rows not in the app</div>
{% if stats.unmatched %}<details class=card><summary>Not signed up in the app</summary><div class=body>{% for u in stats.unmatched %}<div class="kv t2">{{u}}</div>{% endfor %}</div></details>{% endif %}{% endif %}
<p class="t3 xs" style="margin-top:16px">Matching uses email first, then exact legal first and last name. An optional Preferred First Name column is stored as the name shown in the app and is not used for matching. A Membership Type or Member Type column adds USAWP coaches to the coaching list.</p>"""

T["qr_page"] = ADMIN_NAV + """<div style="text-align:center"><h1>New to Grunions? Scan to join.</h1>
<div style="background:#fff;border-radius:16px;padding:18px;display:inline-block"><img src=/qr.svg alt="Sign-up QR code" style="width:min(70vw,380px);display:block"></div>
<p class="t3 sm" style="margin-top:12px">{{u}}</p><button class="primary noprint" onclick=print()>Print</button></div>"""

T["admins"] = ADMIN_NAV + """<h1>Roles</h1><p class="t2 sm">{{n_admins}} admin{{'s' if n_admins!=1}} · admins manage everything. Make admin and Make coach work for any member, whether or not USA Water Polo has verified them. Remove admin and Remove coach take that access away. Make coach opens check-in and coaches chat. It does not add someone to the coaching list. The coaching list is who can be assigned to a practice, besides admins, who are always on it. There must always be at least one admin.</p>
<div class=list>{% for r in rows %}<div class=li style="flex-wrap:wrap;align-items:flex-start"><div class=grow><div style="font-weight:500">{{display_first(r)}} {{r.last}}{% if r.id==me().id %} <span class="t3 xs">(you)</span>{% endif %}{{ coach_tag(r) }}</div>
<div class="t3 xs ell">{{r.email}} · {{role_label(r)}}{% if r.email in boot %} · set by ADMIN_EMAIL{% endif %}{% if r.is_admin or r.id in listed %} · coaching list{% endif %}</div></div>
<div style="display:flex;flex-direction:column;align-items:flex-end;gap:6px">
<form method=post class=row style="flex:0 0 auto;gap:6px;margin:0">{{csrf_field()}}<input type=hidden name=member_id value={{r.id}}>
{% if r.role=='coach' %}<button class=compact name=action value=remove_coach>Remove coach</button>{% else %}<button class=compact name=action value=make_coach>Make coach</button>{% endif %}
{% if r.is_admin %}<button class=compact name=action value=remove_admin {{'disabled title="Last admin"' if n_admins<=1 else ('disabled title="Set by ADMIN_EMAIL"' if r.email in boot else '')}}>Remove admin</button>{% else %}<button class="compact primary" name=action value=make_admin>Make admin</button>{% endif %}
</form>
{% if not r.is_admin %}<form method=post style="margin:0">{{csrf_field()}}<input type=hidden name=member_id value={{r.id}}>
{% if r.id in listed %}<button class=compact name=action value=remove_coaching>Remove from coaching list</button>{% else %}<button class=compact name=action value=add_coaching>Add to coaching list</button>{% endif %}
</form>{% endif %}</div></div>{% endfor %}</div>"""
