"""Templates (Jinja strings) for the Grunions app. Restrained dark UI: one surface, gray text, one blue accent."""

BASE = """<!doctype html><html lang=en><meta charset=utf-8><meta name=viewport content="width=device-width,initial-scale=1,viewport-fit=cover">
<meta name=theme-color content="#0a0a0b"><link rel=manifest href=/manifest.webmanifest>
<link rel=icon href=/static/icons/favicon-32.png sizes=32x32 type=image/png><link rel=apple-touch-icon href=/static/icons/apple-touch-icon-180.png>
<title>Grunions</title>
<style>[hidden]{display:none!important}
:root{--bg:#0a0a0b;--surface:#151517;--surface2:#1d1d20;--line:#26262a;--t1:#ececee;--t2:#a0a0a8;--t3:#6c6c74;--accent:#3b82f6;
--ok:#3fb950;--bad:#f0524a;--warn:#e3a008;--r:14px}
*{box-sizing:border-box}html{-webkit-text-size-adjust:100%}
body{margin:0;background:var(--bg);color:var(--t1);font:16px/1.5 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,system-ui,sans-serif}
a{color:var(--t1)}main{max-width:640px;margin:0 auto;padding:20px 20px 120px}
header{display:flex;align-items:center;justify-content:space-between;padding:16px 20px;max-width:640px;margin:0 auto}
.brand{font-weight:600;letter-spacing:.2px;color:var(--t1);text-decoration:none}header a.sub{color:var(--t3);font-size:14px;text-decoration:none}
h1{font-size:28px;font-weight:650;letter-spacing:-.3px;margin:4px 0 20px}h2{font-size:17px;font-weight:600;margin:28px 0 10px}
p{margin:0 0 12px}.t2{color:var(--t2)}.t3{color:var(--t3)}.sm{font-size:14px}.xs{font-size:13px}
.card{background:var(--surface);border-radius:var(--r);padding:18px;margin:0 0 12px}
.usawp-line{display:flex;align-items:center;justify-content:space-between;gap:12px;margin-top:12px}
.list{background:var(--surface);border-radius:var(--r);margin:0 0 12px;overflow:hidden}
.li{display:flex;align-items:center;gap:12px;padding:14px 18px;min-height:60px;border-top:1px solid var(--line)}.li:first-child{border-top:0}
.grow{flex:1;min-width:0}.ell{white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
label{display:block;font-size:13px;color:var(--t2);margin:0 0 14px}
input,select,textarea{display:block;width:100%;margin-top:6px;background:var(--surface2);border:1px solid var(--line);color:var(--t1);border-radius:10px;
padding:0 14px;height:48px;font:inherit}textarea{padding:12px 14px}input[type=hidden]{display:none}input[type=checkbox]{display:inline-block;width:20px;height:20px;margin:0 8px 0 0;vertical-align:-4px;accent-color:var(--accent)}
input:focus,select:focus,textarea:focus{outline:none;border-color:var(--accent)}
.btn,button{display:inline-flex;align-items:center;justify-content:center;gap:6px;height:48px;padding:0 18px;border-radius:10px;border:0;font:inherit;font-weight:600;
cursor:pointer;text-decoration:none;background:var(--surface2);color:var(--t1)}.btn.primary,button.primary{background:var(--accent);color:#fff}
.btn.quiet,button.quiet{background:none;color:var(--t2);padding:0 8px}.btn.danger,button.danger{background:none;color:var(--bad)}
.btn.compact,button.compact{height:40px;padding:0 14px;font-size:15px}.full{width:100%}.row{display:flex;gap:10px}.row>*{flex:1}
.st{display:inline-flex;align-items:center;gap:7px;font-size:14px;color:var(--t2);white-space:nowrap}
.st::before{content:"";width:8px;height:8px;border-radius:50%;background:var(--t3)}.st-ok::before{background:var(--ok)}.st-bad::before{background:var(--bad)}.st-warn::before{background:var(--warn)}
.note{background:var(--surface);border-radius:var(--r);padding:14px 18px;margin:0 0 12px;color:var(--t2);font-size:15px}.note b{color:var(--t1)}
.toast{position:fixed;left:50%;bottom:calc(76px + env(safe-area-inset-bottom));transform:translateX(-50%);z-index:30;background:var(--surface);color:var(--t1);border:1px solid var(--line);border-radius:12px;padding:12px 16px;font-size:15px;line-height:1.4;text-align:center;box-shadow:0 8px 28px rgba(0,0,0,.5);max-width:min(440px,calc(100% - 32px))}
details>summary{list-style:none;cursor:pointer;display:flex;align-items:center;justify-content:space-between;min-height:56px;padding:0 18px;color:var(--t1)}
details>summary::-webkit-details-marker{display:none}details>summary::after{content:"›";color:var(--t3);font-size:22px;transition:transform .15s}
details[open]>summary::after{transform:rotate(90deg)}details.card{padding:0}details.card>.body{padding:0 18px 16px}
.kv{display:flex;justify-content:space-between;gap:12px;padding:10px 0;border-top:1px solid var(--line);font-size:15px}.kv:first-child{border-top:0}.kv span:first-child{color:var(--t2)}
.seg{display:flex;gap:4px;background:var(--surface);border-radius:12px;padding:4px;margin:0 0 20px;overflow-x:auto}
.seg a{flex:1;text-align:center;padding:9px 12px;border-radius:9px;color:var(--t2);text-decoration:none;font-size:14px;font-weight:500;white-space:nowrap}.seg a.on{background:var(--surface2);color:var(--t1)}
nav.tabs{position:fixed;left:0;right:0;bottom:0;background:rgba(10,10,11,.94);backdrop-filter:blur(12px);border-top:1px solid var(--line);
display:flex;justify-content:center;padding:6px 0 calc(6px + env(safe-area-inset-bottom));z-index:9}
nav.tabs a{flex:1;max-width:140px;display:flex;flex-direction:column;align-items:center;gap:3px;padding:6px 0;color:var(--t3);text-decoration:none;font-size:12px;font-weight:500}
nav.tabs a.on{color:var(--accent)}nav.tabs svg{width:24px;height:24px;fill:none;stroke:currentColor;stroke-width:1.8;stroke-linecap:round;stroke-linejoin:round}
.chat{display:flex;flex-direction:column;gap:14px}.m .who{font-size:13px;color:var(--t3);margin-bottom:3px}.m .txt{background:var(--surface);border-radius:14px;padding:10px 14px;display:inline-block;max-width:85%;white-space:pre-wrap;word-wrap:break-word}
.m.mine{text-align:right}.m.mine .txt{background:var(--surface2);text-align:left}.m.ann .txt{display:block;max-width:none;border:1px solid var(--line);background:var(--surface)}
.composer{position:fixed;left:0;right:0;bottom:64px;background:var(--bg);padding:10px 20px;border-top:1px solid var(--line);z-index:8}
.composer form{max-width:600px;margin:auto;display:flex;gap:8px;align-items:flex-end}
.composer textarea{margin:0;height:48px;min-height:48px;max-height:136px;resize:none;line-height:22px;padding:12px 14px;overflow-y:auto;scrollbar-width:none;-ms-overflow-style:none}
.composer textarea::-webkit-scrollbar{display:none}.iconbtn{width:48px;padding:0;flex:none;color:var(--t2)}.iconbtn svg{width:22px;height:22px;fill:none;stroke:currentColor;stroke-width:1.8;stroke-linecap:round;stroke-linejoin:round}
.iconbtn.send{color:var(--accent)}
.preview{max-width:600px;margin:0 auto 8px;display:flex;align-items:center;gap:10px;color:var(--t2);font-size:14px}.preview img{height:48px;border-radius:8px}
.m .img{display:block;margin-top:4px}.m.mine .img{margin-left:auto}.m .img img{max-width:min(70vw,280px);max-height:280px;border-radius:12px;display:block;background:var(--surface)}.m.mine .img{width:fit-content}
.rx{display:flex;flex-wrap:wrap;gap:6px;margin-top:6px}.m.mine .rx{justify-content:flex-end}
.rx button{height:30px;padding:0 10px;border-radius:15px;font-size:14px;font-weight:500;background:var(--surface);color:var(--t2);border:1px solid var(--line)}
.rx button.on{border-color:var(--accent);color:var(--t1)}.rx .add{color:var(--t3)}
.picker{display:flex;gap:4px;background:var(--surface2);border:1px solid var(--line);border-radius:20px;padding:4px;width:fit-content;margin-top:6px}.m.mine .picker{margin-left:auto}
.picker button{height:36px;width:40px;padding:0;background:none;font-size:20px}
.lightbox{position:fixed;inset:0;background:rgba(0,0,0,.92);display:flex;align-items:center;justify-content:center;z-index:20}.lightbox img{max-width:96vw;max-height:92vh;border-radius:8px}
.gobtn{background:none;height:auto;padding:4px 0;color:var(--t2);font-weight:500;font-size:14px}.gobtn::after{content:" ›";color:var(--t3)}
.ci-name{flex:1;min-width:0;height:auto;padding:0;background:none;display:block;text-align:left;font-weight:400}
.panel{padding:4px 18px 18px;border-top:1px solid var(--line);background:var(--surface)}.panel h3{font-size:15px;font-weight:600;margin:18px 0 10px}
@media print{header,nav,.noprint{display:none!important}body{background:#fff;color:#000}.card{background:#fff}}
</style>
{% macro st(kind, label) %}<span class="st st-{{kind}}">{{label}}</span>{% endmacro %}
{% macro usawp(s) %}{{ st({'verified':'ok','expired':'bad','pending':'warn'}.get(s,'none'), 'USAWP ' ~ s) }}{% endmacro %}
<header><a class=brand href=/>Grunions</a>{% if me() %}<a class=sub href=/logout>Log out</a>{% endif %}</header><main>
{% for cat, msg in get_flashed_messages(with_categories=true) %}{% if cat == 'toast' %}<div class="toast noprint" role=status>{{msg}}</div>{% else %}<div class=note>{{msg|safe}}</div>{% endif %}{% endfor %}
<script>document.querySelectorAll('.toast').forEach(function(t){setTimeout(function(){t.remove()},3000)})</script>"""

ICONS = {
 "home": '<svg viewBox="0 0 24 24"><path d="M3 10.5 12 3l9 7.5V20a1 1 0 0 1-1 1h-5v-6H9v6H4a1 1 0 0 1-1-1z"/></svg>',
 "cal": '<svg viewBox="0 0 24 24"><rect x="3" y="5" width="18" height="16" rx="2"/><path d="M3 10h18M8 3v4M16 3v4"/></svg>',
 "chat": '<svg viewBox="0 0 24 24"><path d="M21 12a8 8 0 0 1-11.6 7.1L4 20l1-4.4A8 8 0 1 1 21 12z"/></svg>',
 "admin": '<svg viewBox="0 0 24 24"><path d="M9 11l3 3 8-8"/><path d="M20 12v7a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h9"/></svg>',
}
TABS = ("""</main>{% if me() %}<nav class="tabs noprint">
<a href=/home class="{{'on' if tab=='home'}}">""" + ICONS["home"] + """Home</a>
<a href=/practices class="{{'on' if tab=='practices'}}">""" + ICONS["cal"] + """Schedule</a>
<a href=/chat class="{{'on' if tab=='chat'}}">""" + ICONS["chat"] + """Chat</a>
{% if is_staff() %}<a href=/admin class="{{'on' if tab=='admin'}}">""" + ICONS["admin"] + """Admin</a>{% endif %}
</nav>{% endif %}""")

ADMIN_NAV = """<div class="seg noprint">{% set ep = request.endpoint %}<a href=/admin class="{{'on' if ep=='admin'}}">Check-in</a>
{% if me().is_admin %}<a href=/members class="{{'on' if ep=='members'}}">Members</a><a href=/admins class="{{'on' if ep=='admins'}}">Roles</a><a href=/expiring class="{{'on' if ep=='expiring'}}">Expiring</a>
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
{% for n in notices %}<div class="note notice">{{n.body}}</div>{% endfor %}
{% set cl = clearance(m) %}{% set dl = days_left(m.usawp_valid_until) %}
<div class=card><div style="display:flex;align-items:center;justify-content:space-between">
{% if vr_pending %}<div style="font-size:19px;font-weight:600">Verification pending</div>{{ st('warn','Pending') }}
{% else %}<div style="font-size:19px;font-weight:600">{{'Cleared to play' if cl.ok else 'Not cleared to play'}}</div>{{ st('ok' if cl.ok else 'bad', 'Cleared' if cl.ok else 'Not cleared') }}{% endif %}</div>
{% if not cl.ok %}<p class="t2 sm" style="margin:8px 0 0">Needs: {{cl.reasons|join(', ')}}</p>{% endif %}
{% if m.usawp_status=='verified' and dl is not none and dl <= EXPIRING_DAYS %}<p class="sm" style="margin:8px 0 0"><span class="st st-warn"></span> Your membership expires in <b>{{dl}} days</b> ({{m.usawp_valid_until}}). <a href=https://usawp.sport80.com>Renew</a></p>{% endif %}
{% if m.usawp_status != 'verified' %}<p class="t2 sm" style="margin:8px 0 0">Register or renew at <a href=https://usawp.sport80.com>usawp.sport80.com</a> with {{m.email}} and choose Grunions as your club.</p>{% endif %}
{% if m.usawp_status == 'verified' %}
{% if m.usawp_number %}<p class="sm" style="margin:12px 0 0">USAWP # {{m.usawp_number}}</p>{% endif %}
{% elif m.usawp_number %}
<div class=usawp-line><span>USAWP # {{m.usawp_number}}</span><button type=button class=compact id=usawpEdit>Edit</button></div>
<form id=usawpForm hidden method=post action=/home>{{csrf_field()}}
<div class=row style="align-items:flex-end"><label style="margin:0">USAWP Membership #<input name=usawp_number inputmode=numeric value="{{m.usawp_number}}" autocomplete=off></label>
<button class=primary style="flex:0 0 auto">Save</button></div></form>
<script>document.getElementById('usawpEdit').onclick=function(){var f=document.getElementById('usawpForm');f.hidden=!f.hidden;if(!f.hidden)f.querySelector('input[name=usawp_number]').focus()};</script>
{% else %}<form method=post action=/home style="margin-top:14px">{{csrf_field()}}
<div class=row style="align-items:flex-end"><label style="margin:0">USAWP Membership #<input name=usawp_number inputmode=numeric value="" autocomplete=off></label>
<button class=primary style="flex:0 0 auto">Add</button></div></form>{% endif %}</div>
{% if nextp %}<div class=card><div class="t3 xs">NEXT PRACTICE</div><div style="font-size:18px;font-weight:600;margin-top:2px">{{fmt_d(nextp.date)}}, {{fmt_t(nextp.start)}}</div>
<div class=t2>{{nextp.location}} · {{nextp_n}} going</div>
<form method=post action=/practices style="margin-top:14px">{{csrf_field()}}<input type=hidden name=pid value={{nextp.id}}>
{% if nextp_mine == 1 %}<button class=full name=action value=clear>Going ✓</button>{% else %}<button class="primary full" name=action value=going>I'm going</button>{% endif %}</form></div>{% endif %}
{% if ann %}<div class=card><div class="t3 xs">ANNOUNCEMENT · {{display_first(ann)|upper}}</div><p style="margin:6px 0 0">{{ann.body}}</p></div>{% endif %}
<details class=card><summary>Membership &amp; requirements</summary><div class=body>
<div class=kv><span>USA Water Polo</span>{{ usawp(m.usawp_status) }}</div>
<div class=kv><span>Member #</span><span>{{m.usawp_number or '—'}}</span></div><div class=kv><span>Expires</span><span>{{m.usawp_valid_until or '—'}}</span></div>
{% if m.usawp_verified_by %}<div class=kv><span>Verified</span><span>{{m.usawp_verified_by}}, {{m.usawp_verified_at[:10]}}</span></div>{% endif %}
{% for it in cl.checks %}<div class=kv><span>{{it.req.name}}</span>{{ st({'ok':'ok','no date':'warn'}.get(it.status,'bad'),
 (('expires ' ~ it.mr.expires_on) if it.mr and it.mr.expires_on else ('done ' ~ it.mr.completed_on) if it.mr and it.mr.completed_on else 'missing') if it.status!='expired' else 'expired') }}</div>{% endfor %}
</div></details>
<details class=card><summary>Attendance <span class="t3 sm" style="margin-left:auto;margin-right:10px">{{hist|length}} total · {{nmonth}} this month</span></summary><div class=body>
{% for h in hist[:20] %}<div class=kv><span>{{fmt_d(h.practice_date)}}</span><span class=t2>{{h.location}}</span></div>{% else %}<p class=t3>No practices yet.</p>{% endfor %}</div></details>
<details class=card><summary>Profile</summary><div class=body>
<div class=kv><span>Legal name</span><span>{{m.first}} {{m.last}}</span></div>
<form method=post action=/home>{{csrf_field()}}<input type=hidden name=action value=preferred>
<label>Preferred first name (optional)<input name=preferred_first value="{{m.preferred_first or ''}}" placeholder="Leave blank to use your legal first name" autocomplete=off></label>
<button class=full>Save</button></form>
<div class=kv><span>Email</span><span>{{m.email}}</span></div>
<div class=kv><span>Phone</span><span>{{m.phone}}</span></div><div class=kv><span>Role</span><span>{{role_label(m)|capitalize}}</span></div></div></details>"""

T["chat"] = """{% if is_staff() %}<div class=seg><a href=/chat class="{{'on' if ch=='team'}}">Team</a><a href="/chat?c=coaches" class="{{'on' if ch=='coaches'}}">Coaches</a></div>{% else %}<h1>Team</h1>{% endif %}
<div class=chat id=chat></div><div style=height:90px></div>
<div class="composer noprint"><div class=preview id=prev hidden><img id=prevImg alt=""><span id=prevName></span><button type=button class="quiet compact" id=prevX>Remove</button></div>
<form id=f><input type=file id=file accept="image/jpeg,image/png,image/gif,image/webp,image/heic,image/heif,.heic" hidden>
<button type=button class="iconbtn" id=attach title="Attach image" aria-label="Attach image"><svg viewBox="0 0 24 24"><rect x="3" y="4" width="18" height="16" rx="2"/><circle cx="9" cy="10" r="2"/><path d="m21 16-5-5-9 9"/></svg></button>
<textarea id=body rows=1 maxlength=2000 placeholder="Message {{'coaches' if ch=='coaches' else 'the team'}}"></textarea>
<button class="iconbtn send" type=submit aria-label=Send><svg viewBox="0 0 24 24" aria-hidden=true><path d="m22 2-7 20-4-9-9-4Z"/><path d="M22 2 11 13"/></svg></button></form></div>
<script>
const CSRF="{{csrf_token()}}",CH="{{ch}}",EMO={{REACTIONS|tojson}};let last=0;const box=document.getElementById('chat');
const esc=s=>s.replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const t=iso=>new Date(iso).toLocaleString([], {weekday:'short',hour:'numeric',minute:'2-digit'});
function rxHtml(id,r){r=r||{};return EMO.filter(e=>r[e]).map(e=>`<button type=button class="${r[e].mine?'on':''}" data-m=${id} data-e="${e}">${e} ${r[e].n}</button>`).join('')+`<button type=button class=add data-pick=${id} aria-label="Add reaction">+</button>`}
function add(m){const d=document.createElement('div');d.className='m'+(m.mine?' mine':'')+(m.ann?' ann':'');d.id='msg'+m.id;
 d.innerHTML=`<div class=who>${m.ann?'Announcement · ':''}${esc(m.who)} · ${t(m.at)}</div>`+(m.body?`<div class=txt>${esc(m.body)}</div>`:'')+
 (m.image?`<a class=img href="${m.image.full}" data-full="${m.image.full}"><img src="${m.image.thumb}" alt="Photo from ${esc(m.who)}" loading=lazy></a>`:'')+`<div class=rx>${rxHtml(m.id)}</div>`;
 box.appendChild(d);last=Math.max(last,m.id)}
function paintRx(map){document.querySelectorAll('.m').forEach(el=>{const id=el.id.slice(3),rx=el.querySelector('.rx');const h=rxHtml(id,map[id]);if(rx.dataset.h!==h){rx.innerHTML=h;rx.dataset.h=h}})}
async function poll(){try{const r=await fetch('/api/messages?c='+CH+'&after='+last);const j=await r.json();const end=innerHeight+scrollY>=document.body.scrollHeight-120;
 j.forEach(add);paintRx(await (await fetch('/api/reactions?c='+CH)).json());if(j.length&&end)scrollTo(0,document.body.scrollHeight)}catch(e){}}
box.addEventListener('click',async e=>{const b=e.target.closest('button,a.img');if(!b)return;
 if(b.matches('a.img')){e.preventDefault();const lb=document.createElement('div');lb.className='lightbox';lb.innerHTML=`<img src="${b.dataset.full}" alt="">`;lb.onclick=()=>lb.remove();document.body.appendChild(lb);return}
 if(b.dataset.pick){const m=document.getElementById('msg'+b.dataset.pick);const old=m.querySelector('.picker');document.querySelectorAll('.picker').forEach(p=>p.remove());if(old)return;
  const p=document.createElement('div');p.className='picker';p.innerHTML=EMO.map(x=>`<button type=button data-m=${b.dataset.pick} data-e="${x}">${x}</button>`).join('');m.appendChild(p);return}
 if(b.dataset.e){document.querySelectorAll('.picker').forEach(p=>p.remove());await fetch(`/api/messages/${b.dataset.m}/react`,{method:'POST',headers:{'Content-Type':'application/json','X-CSRF':CSRF},body:JSON.stringify({emoji:b.dataset.e})});poll()}});
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
 ta.value='';grow();file.value='';prev.hidden=true;await poll();scrollTo(0,document.body.scrollHeight)};
ta.addEventListener('keydown',e=>{if(e.key==='Enter'&&!e.shiftKey&&!e.isComposing){e.preventDefault();document.getElementById('f').requestSubmit()}});
poll().then(()=>scrollTo(0,document.body.scrollHeight));setInterval(poll,3000);
</script>"""

T["practices"] = """<h1>Schedule</h1><p class="t2 sm" style="margin-top:-12px">Tue · Marina HS &nbsp;·&nbsp; Fri · Westminster HS &nbsp;·&nbsp; 7–8:30 PM</p>
{% for x in data %}{% set p = x.p %}<div class=card id=p{{p.id}} {% if p.cancelled %}style="opacity:.55"{% endif %}>
<div style="display:flex;justify-content:space-between;align-items:baseline;gap:12px"><div><div style="font-size:18px;font-weight:600">{{fmt_d(p.date)}}</div>
<div class="t2 sm">{{fmt_t(p.start)}}–{{fmt_t(p.end)}} · {{p.location}}</div>{% if p.note %}<div class="t3 sm">{{p.note}}</div>{% endif %}</div>
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
<div class=row><button name=action value=edit>Save</button>{% if p.cancelled %}<button name=action value=restore>Restore</button>{% else %}<button class=danger name=action value=cancel>Cancel practice</button>{% endif %}</div>
<a class="btn quiet full" href="/admin?date={{p.date}}" style="margin-top:6px">Open check-in</a></form></details>{% endif %}</div>{% endfor %}
{% if me().is_admin %}<details class=card><summary>Add a practice</summary><form method=post class=body>{{csrf_field()}}<label>Date<input type=date name=date required></label>
<div class=row><label>Start<input type=time name=start value=19:00></label><label>End<input type=time name=end value=20:30></label></div>
<label>Location<input name=location required></label><label>Note<input name=note></label><button class="primary full" name=action value=add>Add practice</button></form></details>{% endif %}"""

T["admin"] = ADMIN_NAV + """
<form class="row noprint" style="margin-bottom:8px"><input type=date name=date value="{{date}}" onchange=this.form.submit() style="margin:0"><input name=q value="{{q}}" placeholder="Search" style="margin:0"></form>
<h1 style="margin:20px 0 4px">{{loc}}</h1><p class="t2 sm">{{fmt_d(date)}} · {{n}} checked in{% if pr %} · {{rsvp_n}} RSVP'd{% else %} · no practice scheduled{% endif %}</p>
<div class=list>{% for r in rows %}{% set cl = clearance(r) %}{% set dl = days_left(r.usawp_valid_until) %}
<div class=li><button type=button class=ci-name onclick="this.closest('.li').nextElementSibling.toggleAttribute('hidden')">
<div class=ell style="font-weight:500">{{display_first(r)}} {{r.last}}</div>
{% if not cl.ok %}{{ st('bad','Not cleared') }}{% elif dl is not none and dl <= EXPIRING_DAYS %}{{ st('warn','Expires in %dd' % dl) }}{% else %}{{ st('ok','Cleared') }}{% endif %}
{% if r.vr_status == 'pending' %}<span class="t3 xs"> · verification requested</span>{% elif r.vr_status == 'done' %}<span class="t3 xs"> · bot answered</span>{% endif %}</button>
<form method=post>{{csrf_field()}}<input type=hidden name=member_id value={{r.id}}><input type=hidden name=date value={{date}}><input type=hidden name=q value="{{q}}">
{% if r.cid %}<button class=compact name=action value=undo title="Undo check-in">Checked in</button>{% else %}<button class="primary compact">Check in</button>{% endif %}</form></div>
<div class=panel id=m{{r.id}} hidden>
<div class=kv><span>RSVP</span><span>{% if r.going==1 %}RSVP ✓{% elif r.going==0 %}Not going{% else %}—{% endif %}</span></div>
<div class=kv><span>Membership</span><span>{{ usawp(r.usawp_status) }}{% if r.usawp_status=='verified' and dl is not none and dl <= EXPIRING_DAYS %} · {{dl}}d left{% endif %}</span></div>
{% if r.usawp_number or r.usawp_valid_until %}<div class=kv><span>Member # / expires</span><span>{{r.usawp_number or '—'}} / {{r.usawp_valid_until or '—'}}</span></div>{% endif %}
{% if not cl.ok %}<div class=kv><span>Not cleared</span><span style="text-align:right">{{cl.reasons|join(', ')}}</span></div>{% endif %}
{% if r.usawp_verified_by %}<div class=kv><span>Verified</span><span>{{r.usawp_verified_by}}, {{r.usawp_verified_at.replace('T',' ')}}</span></div>{% endif %}
{% if r.vr_status %}<div class=kv><span>Bot request</span><span>{{r.vr_status}}{% if r.vr_note %} · {{r.vr_note}}{% endif %}</span></div>{% endif %}
{% if r.preferred_first and r.preferred_first.strip() %}<div class=kv><span>Legal name</span><span>{{r.first}} {{r.last}}</span></div>{% endif %}
{% if me().is_admin %}<form method=post>{{csrf_field()}}<input type=hidden name=member_id value={{r.id}}><input type=hidden name=date value={{date}}><input type=hidden name=q value="{{q}}">
<label>Preferred first name (optional)<input name=preferred_first value="{{r.preferred_first or ''}}" placeholder="Leave blank to use legal first name"></label>
<button class=full name=action value=preferred>Save preferred name</button></form>{% endif %}
{% if me().is_admin and (not cl.ok or r.usawp_status != 'verified') %}
<h3>Verify {{r.first}} on Sport:80</h3>
<div class=row><a class="btn" target=_blank rel=noopener href="https://usawp.sport80.com/" onclick="navigator.clipboard&&navigator.clipboard.writeText('{{r.first}} {{r.last}}')">Open Sport:80</a>
<form method=post style="flex:1">{{csrf_field()}}<input type=hidden name=member_id value={{r.id}}><input type=hidden name=date value={{date}}>
<button class=full name=action value=ask_bot {% if r.vr_status=='pending' %}disabled{% endif %}>{{'Requested' if r.vr_status=='pending' else 'Ask Grunions to verify'}}</button></form></div>
<p class="t3 xs" style="margin-top:6px">Opening Sport:80 copies the name. Search the Grunions club members list and confirm membership is Current.</p>
<form method=post>{{csrf_field()}}<input type=hidden name=member_id value={{r.id}}><input type=hidden name=date value={{date}}><input type=hidden name=q value="{{q}}">
<div class=row><label>Member #<input name=number inputmode=numeric value="{{r.usawp_number or ''}}"></label><label>Expires on<input name=valid_until type=date></label></div>
<label><input type=checkbox name=no_date>Sport:80 shows no date</label><button class="primary full" name=action value=verify>Mark membership verified</button></form>
<h3>Compliance item</h3><form method=post>{{csrf_field()}}<input type=hidden name=member_id value={{r.id}}><input type=hidden name=date value={{date}}><input type=hidden name=q value="{{q}}">
<label>Item<select name=req_id>{% for it in cl.checks|sort(attribute='status') %}<option value={{it.req.id}}>{{it.req.name}} ({{it.status}})</option>{% endfor %}</select></label>
<div class=row><label>Completed<input name=completed_on type=date></label><label>Expires on<input name=expires_on type=date></label></div>
<button class=full name=action value=req>Save item</button></form>
<h3>Role</h3><form method=post class=row>{{csrf_field()}}<input type=hidden name=member_id value={{r.id}}><input type=hidden name=date value={{date}}>
<select name=role style="margin:0">{% for o in ['member','coach','admin'] %}<option {{'selected' if role_label(r)==o}}>{{o}}</option>{% endfor %}</select><button name=action value=role style="flex:0 0 auto">Save</button></form>
{% endif %}</div>{% else %}<div class=li><span class=t3>No members yet.</span></div>{% endfor %}</div>
<script>if(/^#m\\d+$/.test(location.hash)){const p=document.querySelector(location.hash);if(p)p.removeAttribute('hidden')}</script>"""

T["members"] = ADMIN_NAV + """<div style="display:flex;justify-content:space-between;align-items:baseline"><h1>Members</h1><a class="t2 sm" href=/members.csv>Export CSV</a></div>
<p class="t2 sm">{{rows|length}} total · {% for s,v in c.items() %}{{v}} {{s}}{{' · ' if not loop.last}}{% endfor %}</p>
<div class=list>{% for r in rows %}<div class=li><div class=grow><div class=ell style="font-weight:500">{{display_first(r)}} {{r.last}}</div>
<div class="t3 xs ell">{{r.email}}{% if r.preferred_first and r.preferred_first.strip() %} · legal {{r.first}}{% endif %} · {{r.visits}} practices{% if r.usawp_verified_by %} · verified by {{r.usawp_verified_by}} {{r.usawp_verified_at[:10]}}{% endif %}</div></div>
<div style="text-align:right">{{ usawp(r.usawp_status) }}{% if r.usawp_valid_until %}<div class="t3 xs">thru {{r.usawp_valid_until}}</div>{% endif %}</div></div>{% endfor %}</div>"""

T["expiring"] = ADMIN_NAV + """<h1>Expiring</h1>
<form class="row noprint" style="align-items:center;margin-bottom:8px"><span class="t2 sm" style="flex:0 0 auto">Window (days)</span><input name=days type=number value={{days}} onchange=this.form.submit() style="margin:0"></form>
{% for key, label in [('expired','Already expired'),('within_7','Next 7 days'),('within_%d'%days,'Next %d days'%days)] %}<h2>{{label}} <span class=t3>{{rep[key]|length}}</span></h2>
<div class=list>{% for r in rep[key] %}<div class=li><div class=grow><div style="font-weight:500">{{display_first(r)}} {{r.last}}</div>
<div class="t3 xs">{{r.item}} · {{r.usawp_valid_until}} · {% if r.days_left < 0 %}{{-r.days_left}}d ago{% else %}{{r.days_left}}d left{% endif %}</div></div>
<form method=post>{{csrf_field()}}<input type=hidden name=member_id value={{r.id}}><button class=compact>Remind</button></form></div>{% else %}<div class=li><span class=t3>None</span></div>{% endfor %}</div>{% endfor %}
<form method=post style="margin-top:20px">{{csrf_field()}}<button class="primary full">Remind everyone listed</button></form>
<p class="t3 xs" style="margin-top:10px">Reminders appear on each member's home screen. Daily report: <a href=/api/expiring>/api/expiring</a> or daily_expiry.py.</p>"""

T["requirements_page"] = ADMIN_NAV + """<h1>Requirements</h1><p class="t2 sm">Cleared to play means a current USAWP membership plus every required item that applies to the member's role. Keywords match Sport:80 export columns.</p>
{% for q in reqs %}<details class=card><summary><span>{{q.name}}</span><span class="t3 sm" style="margin-left:auto;margin-right:10px">{{q.applies_to}}{{'' if q.active else ' · off'}}</span></summary>
<form method=post class=body>{{csrf_field()}}<input type=hidden name=id value={{q.id}}>
<div class=row><label>Applies to<select name=applies_to>{% for o in ['all','athlete','coach'] %}<option {{'selected' if q.applies_to==o}}>{{o}}</option>{% endfor %}</select></label>
<label>Import keywords<input name=keywords value="{{q.keywords or ''}}"></label></div>
<label><input type=checkbox name=expires {{'checked' if q.expires}}>Has an expiration date</label><label><input type=checkbox name=active {{'checked' if q.active}}>Required</label>
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
<p class="t3 xs" style="margin-top:16px">Matching uses email first, then exact legal first and last name. An optional Preferred First Name column is stored as the name shown in the app and is not used for matching.</p>"""

T["qr_page"] = ADMIN_NAV + """<div style="text-align:center"><h1>New to Grunions? Scan to join.</h1>
<div style="background:#fff;border-radius:16px;padding:18px;display:inline-block"><img src=/qr.svg alt="Sign-up QR code" style="width:min(70vw,380px);display:block"></div>
<p class="t3 sm" style="margin-top:12px">{{u}}</p><button class="primary noprint" onclick=print()>Print</button></div>"""

T["admins"] = ADMIN_NAV + """<h1>Roles</h1><p class="t2 sm">{{n_admins}} admin{{'s' if n_admins!=1}} · admins manage everything; coaches get check-in and #coaches. There must always be at least one admin.</p>
<div class=list>{% for r in rows %}<div class=li><div class=grow><div class=ell style="font-weight:500">{{display_first(r)}} {{r.last}}{% if r.id==me().id %} <span class="t3 xs">(you)</span>{% endif %}</div>
<div class="t3 xs ell">{{r.email}} · {{role_label(r)}}{% if r.email in boot %} · set by ADMIN_EMAIL{% endif %}</div></div>
<form method=post class=row style="flex:0 0 auto;gap:6px;margin:0">{{csrf_field()}}<input type=hidden name=member_id value={{r.id}}>
{% if r.role=='coach' %}<button class=compact name=action value=remove_coach>Remove coach</button>{% else %}<button class=compact name=action value=make_coach>Make coach</button>{% endif %}
{% if r.is_admin %}<button class=compact name=action value=remove_admin {{'disabled title="Last admin"' if n_admins<=1 else ('disabled title="Set by ADMIN_EMAIL"' if r.email in boot else '')}}>Remove admin</button>{% else %}<button class="compact primary" name=action value=make_admin>Make admin</button>{% endif %}
</form></div>{% endfor %}</div>"""
