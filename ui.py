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
.card.tap{cursor:pointer}a.cardlink,a.goingcount{color:inherit;text-decoration:none}a.cardlink{display:block;flex:1;min-width:0}
.nxhead{display:flex;align-items:center;justify-content:space-between;gap:12px}
.nxmain{display:flex;align-items:center;gap:12px}
.datetile{width:64px;height:64px;border-radius:14px;background:var(--surface2);display:flex;flex-direction:column;align-items:center;justify-content:center;flex:none}
.datetile .wd,.datetile .mo{font-size:11px;font-weight:700;letter-spacing:.6px;color:var(--t3);line-height:1}
.datetile .dn{font-size:22px;font-weight:650;line-height:1.1;margin-top:2px}
.datetile .mo{margin-top:2px}
.nxcardhead{display:flex;align-items:center;justify-content:space-between;gap:12px;margin-bottom:12px}
.schedrows .nxrow{margin-top:6px;font-size:15px}.schedrows .nxrow:first-child{margin-top:0}
.nxtitle{font-size:16px;font-weight:650;line-height:1.3}
.nxchev{color:var(--t3);font-size:22px;line-height:1;flex:none}
.nxnote{margin-top:10px;color:var(--t3);font-size:13px;line-height:1.4}
.pills{display:flex;gap:10px;margin-top:14px}
.pills button{flex:1;height:44px;border-radius:999px;border:1px solid var(--line);background:transparent;color:var(--t1);font-weight:600}
.pills button.on{background:#ececee;color:#0a0a0b;border-color:#ececee}
.nxdiv{height:1px;background:var(--line);margin:14px 0}
.nxsocial{display:flex;align-items:center;gap:12px}
.nxicon{width:40px;height:40px;border-radius:12px;background:var(--surface2);display:flex;align-items:center;justify-content:center;flex:none;color:#C8CDD3}
.nxicon svg{display:block}
.joinpill{height:36px;padding:0 14px;border-radius:999px;border:1px solid var(--line);background:transparent;color:var(--t1);font-weight:600;flex:none}
.joinpill.on{background:#ececee;color:#0a0a0b;border-color:#ececee}
header.homehead{align-items:center}header.homehead h1{margin:0}
button.avatar,span.avatar{width:44px;height:44px;border-radius:50%;padding:0;background:var(--surface2);color:var(--t1);font-size:14px;font-weight:650;letter-spacing:.2px;overflow:hidden;flex:none;border:1px solid var(--line);display:inline-flex;align-items:center;justify-content:center}
.avatar img{width:100%;height:100%;object-fit:cover;display:block}
.profhead{display:flex;align-items:center;gap:14px;margin:0 0 16px}.profhead .avatar{width:64px;height:64px;font-size:20px}
.nextcard{padding:0;overflow:hidden}
.nextcard .nxbody{padding:16px 16px 0}.nextcard .nxtitle{font-size:20px}
.pimg{position:relative;line-height:0}.pimg img{width:100%;height:200px;object-fit:cover;display:block}
.nxbadge{position:absolute;top:12px;left:12px;background:#151517;color:#ececee;border:1px solid #3a3a40;border-radius:999px;padding:5px 10px;font-size:11px;font-weight:700;letter-spacing:.8px;line-height:1}
.nxrow{display:flex;align-items:center;gap:10px;margin-top:8px;color:var(--t1);font-size:15px}
.nxglyph{width:18px;height:18px;flex:none;color:#C8CDD3}
.nextcard .pills{margin:14px 16px 0}.nextcard .pills:last-child{margin-bottom:16px}
.nextcard .nxdiv{margin:14px 16px}.nextcard .nxsocial{padding:0 16px 16px}
.homemap{height:300px;margin:0 -20px 16px;background:#121214;position:relative;z-index:1}
.menu a{display:flex;align-items:center;width:100%;height:40px;padding:0 12px;box-sizing:border-box;color:var(--t1);font-weight:500;font-size:15px;text-decoration:none;border-radius:8px}
.card .menu,.pagehead .menu{left:auto;right:0;min-width:220px}
.mapframe{display:block;width:100%;height:220px;border:0;border-radius:12px;background:var(--surface2)}
.pagehead{display:flex;justify-content:space-between;align-items:flex-start;gap:12px}
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
.coach-tag.warn{color:var(--warn);border-color:#8a6410}.coach-tag.bad{color:var(--bad);border-color:#7a302c}
.coach-elig,.ref-elig{margin-left:8px;font-weight:650;font-size:15px}
.eligs{display:flex;flex-wrap:wrap;gap:4px 10px;margin-top:4px}.eligs .coach-elig,.eligs .ref-elig,.eligs .coach-tag{margin-left:0}.eligs .st{white-space:normal}
.memline{display:flex;flex-wrap:wrap;align-items:center;gap:2px 0;margin-top:2px;color:var(--t3);font-size:13px;line-height:1.4}
.st{display:inline-flex;align-items:center;gap:7px;font-size:14px;color:var(--t2);white-space:nowrap}
.st::before{content:"";width:8px;height:8px;border-radius:50%;background:var(--t3)}.st-ok::before{background:var(--ok)}.st-bad::before{background:var(--bad)}.st-warn::before{background:var(--warn)}.st-trial::before{background:var(--ok)}
.dot{width:8px;height:8px;border-radius:50%;background:var(--t3);flex:none;display:inline-block}.dot.ok{background:var(--ok)}.dot.bad{background:var(--bad)}.dot.warn{background:var(--warn)}
.list .menu{left:auto;right:0;min-width:280px}
.row.wrap{flex-wrap:wrap}
dialog.modal{border:0;padding:0;background:transparent;color:var(--t1);width:min(440px,calc(100vw - 32px))}
dialog.modal::backdrop{background:rgba(0,0,0,.72)}
dialog.modal .sheet{background:var(--surface);border:1px solid var(--line);border-radius:var(--r);padding:20px}
.note{background:var(--surface);border-radius:var(--r);padding:14px 18px;margin:0 0 12px;color:var(--t2);font-size:15px}.note b{color:var(--t1)}
.toast{position:fixed;left:50%;bottom:calc(76px + env(safe-area-inset-bottom));transform:translateX(-50%);z-index:30;background:var(--surface);color:var(--t1);border:1px solid var(--line);border-radius:12px;padding:12px 16px;font-size:15px;line-height:1.4;text-align:center;box-shadow:0 8px 28px rgba(0,0,0,.5);max-width:min(440px,calc(100% - 32px))}
details>summary{list-style:none;cursor:pointer;display:flex;align-items:center;justify-content:space-between;min-height:56px;padding:0 18px;color:var(--t1)}
details>summary::-webkit-details-marker{display:none}details>summary::after{content:"›";color:var(--t3);font-size:22px;transition:transform .15s}
details[open]>summary::after{transform:rotate(90deg)}details.card{padding:0}details.card>.body{padding:0 18px 16px}
details.playcard>summary{gap:8px;flex-wrap:nowrap;padding-left:16px;padding-right:14px;container-type:inline-size;container-name:playline}
details.playcard>summary .playtitle{display:flex;align-items:center;gap:8px;flex:0 1 auto;min-width:0;font-size:15px;font-weight:600;line-height:1.2;white-space:nowrap}
details.playcard>summary .playnum{flex:none;margin-left:auto;color:var(--t2);font-size:13px;font-weight:500;white-space:nowrap}
.playopen{display:none}
details.playcard[open]>summary .playclosed{display:none}
details.playcard[open]>summary .playopen{display:inline}
details.playcard>summary::after{flex:none;font-size:16px;margin-left:2px}
@container playline (max-width:420px){details.playcard>summary{gap:6px}details.playcard>summary .playtitle{font-size:14px;letter-spacing:-.15px;gap:6px}details.playcard>summary .playnum{font-size:12.5px}}
@container playline (max-width:300px){details.playcard>summary::after{content:none}}
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
nav.tabs a .badge{position:absolute;top:4px;left:50%;margin-left:8px}.datetile{position:relative}.datetile .pdate{position:absolute;top:0;right:0}.datetile .pdate .badge{position:absolute;top:-4px;right:-4px;margin:0}
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
.ci-name{flex:1;min-width:0;height:auto;padding:0;background:none;display:flex;align-items:center;gap:12px;text-align:left;font-weight:400}
.ciav{width:40px;height:40px;font-size:13px}
.filt{display:flex;gap:8px;margin:0 0 16px;flex-wrap:wrap}
.filt button{height:36px;padding:0 14px;border-radius:999px;border:1px solid var(--line);background:transparent;color:var(--t1);font-weight:600}
.filt button.on{background:#ececee;color:#0a0a0b;border-color:#ececee}
.usawprow{display:flex;align-items:center;gap:10px;background:var(--surface);border-radius:var(--r);padding:14px 16px;margin:0 0 12px;color:inherit;text-decoration:none}
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
{% macro bg_status(m) %}{% set bg = background_view(m) %}{% if bg %}{{ st(bg.kind, ('expires ' ~ bg.date) if bg.date else 'missing') }}{% endif %}{% endmacro %}
{% macro member_expiry(m) %}{% set left = days_left(m.usawp_valid_until) %}{% if not m.usawp_valid_until %}{{ st('bad', 'missing') }}{% elif left < 0 %}{{ st('bad', 'expires ' ~ m.usawp_valid_until) }}{% elif left <= EXPIRING_DAYS %}{{ st('warn', 'expires ' ~ m.usawp_valid_until) }}{% else %}{{ st('ok', 'expires ' ~ m.usawp_valid_until) }}{% endif %}{% endmacro %}
{% macro member_status(r) %}{% set cl = clearance(r) %}{% set dl = days_left(r.usawp_valid_until) %}{% set tw = trial_window(r) %}{% set ex = expiry_notes(r, cl) %}
{% if tw and tw.active and r.usawp_status != 'verified' and not ex.membership %}{{ st('trial', trial_badge(tw)) }}<div class="t3 xs">Ends {{tw.ends}}</div>{% elif not cl.ok %}{{ st('bad','Not cleared') }}{% elif dl is not none and dl <= EXPIRING_DAYS %}{{ st('warn','Expires in %dd' % dl) }}{% else %}{{ st('ok','Cleared') }}{% endif %}
{% if tw and tw.expired and r.usawp_status != 'verified' %}<div class="xs">Trial ended {{tw.ends}}</div>{% endif %}
{% if r.vr_status == 'pending' %}<span class="t3 xs"> · verification requested</span>{% elif r.vr_status == 'done' %}<span class="t3 xs"> · bot answered</span>{% endif %}{% endmacro %}
{% macro status_dot(s) %}{% set kind = {'verified':'ok','expired':'bad','pending':'warn'}.get(s, '') %}<span class="dot{% if kind %} {{kind}}{% endif %}" aria-hidden=true></span>{% endmacro %}
{% macro checkin_status(r) %}{% set cl = clearance(r) %}{% set dl = days_left(r.usawp_valid_until) %}{% set tw = trial_window(r) %}{% set ex = expiry_notes(r, cl) %}
{% if tw and tw.active and r.usawp_status != 'verified' and not ex.membership %}{{ st('trial', 'Trial') }}{% elif tw and tw.expired and r.usawp_status != 'verified' %}{{ st('bad', 'Trial ended') }}{% elif not cl.ok %}{{ st('bad','Not cleared') }}{% elif dl is not none and dl <= EXPIRING_DAYS %}{{ st('warn','Expiring soon') }}{% else %}{{ st('ok','Cleared') }}{% endif %}
{% if r.vr_status == 'pending' %}<span class="t3 xs"> · verification requested</span>{% elif r.vr_status == 'done' %}<span class="t3 xs"> · bot answered</span>{% endif %}{% endmacro %}
{% macro member_panel(r) %}{% set cl = clearance(r) %}{% set dl = days_left(r.usawp_valid_until) %}{% set tw = trial_window(r) %}{% set ex = expiry_notes(r, cl) %}{% set cred = credential_dates(r) %}
<div class=panel id=m{{r.id}} hidden>
<div class=kv><span>RSVP</span><span>{% if r.going==1 %}RSVP ✓{% elif r.going==0 %}Not going{% else %}—{% endif %}</span></div>
<div class=kv><span>Membership</span><span>{{ usawp(r.usawp_status) }}{% if r.usawp_status=='verified' and dl is not none and dl <= EXPIRING_DAYS %} · {{dl}}d left{% endif %}</span></div>
<div class=kv><span>Member # {{r.usawp_number or '—'}}</span>{{ member_expiry(r) }}</div>
{% if tw %}<div class=kv><span>Trial</span><span>{% if tw.active and r.usawp_status != 'verified' %}{{ trial_badge(tw) }} · Ends {{tw.ends}}{% elif tw.expired %}Trial ended {{tw.ends}}{% else %}—{% endif %}</span></div>{% endif %}
<div class=kv><span>SafeSport</span><span>{% if cred.safesport %}expires {{cred.safesport}}{% else %}missing{% endif %}</span></div>
<div class=kv><span>Background screening</span>{% if background_view(r) %}{{ bg_status(r) }}{% else %}<span>Not on file</span>{% endif %}</div>
<div class=kv><span>Eligibility</span><span>{% if coach_eligibility(r).text or referee_eligibility(r).text %}{{ coach_tag(r) }} {{ referee_tag(r) }}{% else %}—{% endif %}</span></div>
{% if not cl.ok %}<div class=kv><span>Not cleared</span><span style="text-align:right">{{cl.reasons|join(', ')}}</span></div>{% endif %}
{% if me().is_admin %}<form method=post>{{csrf_field()}}<input type=hidden name=member_id value={{r.id}}><input type=hidden name=date value="{{date}}"><input type=hidden name=q value="{{q}}">{% if view is defined %}<input type=hidden name=list_view value="{{ view }}">{% endif %}{% if coach_filter is defined %}<input type=hidden name=list_coach value="{{'eligible' if coach_filter else ''}}"><input type=hidden name=list_referee value="{{'eligible' if referee_filter else ''}}">{% endif %}
<label>Background screening expires<input name=expires_on type=date value="{{ background_view(r).date if background_view(r) else '' }}"></label>
<button class=full name=action value=background>Save background screening</button></form>{% endif %}
{% if r.usawp_verified_by %}<div class=kv><span>Verified</span><span>{{r.usawp_verified_by}}, {{r.usawp_verified_at.replace('T',' ')}}</span></div>{% endif %}
{% if r.vr_status %}<div class=kv><span>Bot request</span><span>{{r.vr_status}}{% if r.vr_note %} · {{r.vr_note}}{% endif %}</span></div>{% endif %}
{% if me().is_admin %}<details class=recheck {% if r.vr_status == 'pending' %}open{% endif %}><summary>Recheck membership</summary>
<form method=post class=body>{{csrf_field()}}<input type=hidden name=member_id value={{r.id}}><input type=hidden name=date value="{{date}}"><input type=hidden name=q value="{{q}}">{% if view is defined %}<input type=hidden name=list_view value="{{ view }}">{% endif %}{% if coach_filter is defined %}<input type=hidden name=list_coach value="{{'eligible' if coach_filter else ''}}"><input type=hidden name=list_referee value="{{'eligible' if referee_filter else ''}}">{% endif %}
<p class="t3 sm">Look this member up on Sport:80 and enter what you find. Grunions does not contact Sport:80.{% if r.vr_status == 'pending' %} Saving answers the pending verification request.{% endif %}</p>
<label>Verified<select name=verified><option value=yes {{'selected' if r.usawp_status=='verified'}}>Yes</option><option value=no {{'selected' if r.usawp_status!='verified'}}>No</option></select></label>
<label>Membership type<input name=membership_type value="{{r.membership_type or ''}}" placeholder="Individual Membership, Coach"></label>
<label>Membership expires<input type=date name=valid_until value="{{r.usawp_valid_until or ''}}"></label>
<label>SafeSport expires<input type=date name=safesport_expires value="{{cred.safesport or ''}}"></label>
<label>Background screening expires<input type=date name=background_expires value="{{cred.background or ''}}"></label>
<label>Referee certification expires<input type=date name=referee_expires value="{{cred.referee or ''}}"></label>
<button class="primary full" name=action value=recheck>Save Sport:80 result</button></form>
<form method=post class=body style="margin-top:10px">{{csrf_field()}}<input type=hidden name=member_id value={{r.id}}><input type=hidden name=date value="{{date}}"><input type=hidden name=q value="{{q}}">{% if view is defined %}<input type=hidden name=list_view value="{{ view }}">{% endif %}{% if coach_filter is defined %}<input type=hidden name=list_coach value="{{'eligible' if coach_filter else ''}}"><input type=hidden name=list_referee value="{{'eligible' if referee_filter else ''}}">{% endif %}
<button class=full name=action value=ask_bot {% if r.vr_status=='pending' %}disabled{% endif %}>{{'Requested' if r.vr_status=='pending' else 'Ask Grunions to verify'}}</button></form></details>{% endif %}
{% if r.preferred_first and r.preferred_first.strip() %}<div class=kv><span>Legal name</span><span>{{r.first}} {{r.last}}</span></div>{% endif %}
{% if me().is_admin %}<form method=post>{{csrf_field()}}<input type=hidden name=member_id value={{r.id}}><input type=hidden name=date value="{{date}}"><input type=hidden name=q value="{{q}}">{% if view is defined %}<input type=hidden name=list_view value="{{ view }}">{% endif %}{% if coach_filter is defined %}<input type=hidden name=list_coach value="{{'eligible' if coach_filter else ''}}"><input type=hidden name=list_referee value="{{'eligible' if referee_filter else ''}}">{% endif %}
<label>Preferred first name (optional)<input name=preferred_first value="{{r.preferred_first or ''}}" placeholder="Leave blank to use legal first name"></label>
<button class=full name=action value=preferred>Save preferred name</button></form>{% endif %}
{% if me().is_admin and (not cl.ok or r.usawp_status != 'verified') %}
<h3>Verify {{r.first}} on Sport:80</h3>
<div class=row><a class="btn" target=_blank rel=noopener href="https://usawp.sport80.com/" onclick="navigator.clipboard&&navigator.clipboard.writeText('{{r.first}} {{r.last}}')">Open Sport:80</a></div>
<p class="t3 xs" style="margin-top:6px">Opening Sport:80 copies the name. Search the Grunions club members list and confirm membership is Current. Enter what you find with Recheck membership.</p>
<h3>Compliance item</h3><form method=post>{{csrf_field()}}<input type=hidden name=member_id value={{r.id}}><input type=hidden name=date value="{{date}}"><input type=hidden name=q value="{{q}}">{% if view is defined %}<input type=hidden name=list_view value="{{ view }}">{% endif %}{% if coach_filter is defined %}<input type=hidden name=list_coach value="{{'eligible' if coach_filter else ''}}"><input type=hidden name=list_referee value="{{'eligible' if referee_filter else ''}}">{% endif %}
<label>Item<select name=req_id>{% for it in cl.checks|sort(attribute='status') %}<option value={{it.req.id}}>{{it.req.name}} ({{it.status}})</option>{% endfor %}</select></label>
<div class=row><label>Completed<input name=completed_on type=date></label><label>Expires on<input name=expires_on type=date></label></div>
<button class=full name=action value=req>Save item</button></form>
<h3>Role</h3><form method=post class=row>{{csrf_field()}}<input type=hidden name=member_id value={{r.id}}><input type=hidden name=date value="{{date}}">{% if view is defined %}<input type=hidden name=list_view value="{{ view }}">{% endif %}{% if coach_filter is defined %}<input type=hidden name=list_coach value="{{'eligible' if coach_filter else ''}}"><input type=hidden name=list_referee value="{{'eligible' if referee_filter else ''}}">{% endif %}
<select name=role style="margin:0">{% for o in ['member','coach','admin'] %}<option {{'selected' if role_label(r)==o}}>{{o}}</option>{% endfor %}</select><button name=action value=role style="flex:0 0 auto">Save</button></form>
{% endif %}</div>{% endmacro %}
{% macro glyph_clock() %}<svg class=nxglyph viewBox="0 0 24 24" aria-hidden=true><circle cx="12" cy="12" r="8" fill="none" stroke="currentColor" stroke-width="1.8"/><path d="M12 8v5l3 2" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/></svg>{% endmacro %}
{% macro glyph_pin() %}<svg class=nxglyph viewBox="0 0 24 24" aria-hidden=true><path d="M12 21s7-6.2 7-11a7 7 0 1 0-14 0c0 4.8 7 11 7 11z" fill="none" stroke="currentColor" stroke-width="1.8"/><circle cx="12" cy="10" r="2.2" fill="none" stroke="currentColor" stroke-width="1.8"/></svg>{% endmacro %}
{% macro glyph_people() %}<svg class=nxglyph viewBox="0 0 24 24" aria-hidden=true><circle cx="9" cy="8" r="2.3" fill="none" stroke="currentColor" stroke-width="1.8"/><path d="M4.6 18c.5-2.5 2.3-3.7 4.4-3.7s3.9 1.2 4.4 3.7" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/><circle cx="16.2" cy="9" r="1.8" fill="none" stroke="currentColor" stroke-width="1.8"/><path d="M15.6 14.5c1.5.3 2.7 1.2 3.3 3.2" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/></svg>{% endmacro %}
{% macro social_icon() %}<span class=nxicon aria-hidden=true><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1536 1536" fill="none" width="32" height="32"><path fill="currentColor" fill-rule="evenodd" d="M 778 1101 L 778 1132 L 783 1156 L 793 1178 L 801 1190 L 816 1206 L 839 1222 L 865 1232 L 887 1235 L 1213 1235 L 1239 1231 L 1251 1227 L 1267 1219 L 1281 1209 L 1297 1193 L 1305 1182 L 1314 1165 L 1320 1146 L 1323 1125 L 1323 1101 L 1321 1100 Z M 712 970 L 714 991 L 720 1005 L 725 1012 L 741 1026 L 755 1032 L 766 1034 L 1335 1034 L 1352 1030 L 1366 1022 L 1376 1012 L 1382 1003 L 1388 985 L 1387 961 L 1384 952 L 1376 939 L 1359 924 L 1348 919 L 1334 916 L 766 916 L 749 920 L 739 925 L 729 933 L 721 943 L 715 955 Z M 778 819 L 779 852 L 1323 851 L 1323 826 L 1318 798 L 1309 777 L 1297 759 L 1281 743 L 1258 728 L 1235 720 L 1215 717 L 885 717 L 869 719 L 854 723 L 840 729 L 828 736 L 809 752 L 799 764 L 787 785 L 782 799 Z M 755 183 L 751 184 L 573 331 L 567 342 L 548 453 L 544 467 L 221 468 L 235 641 L 238 663 L 239 689 L 242 710 L 244 748 L 247 770 L 248 796 L 251 817 L 252 843 L 255 864 L 257 903 L 261 936 L 262 962 L 264 971 L 271 1068 L 274 1090 L 276 1127 L 279 1149 L 280 1174 L 284 1191 L 294 1210 L 308 1225 L 326 1236 L 339 1240 L 354 1242 L 580 1241 L 597 1236 L 614 1226 L 628 1212 L 638 1195 L 642 1184 L 644 1172 L 644 1163 L 647 1149 L 649 1124 L 660 1047 L 662 1022 L 684 859 L 685 842 L 688 828 L 689 811 L 702 718 L 703 701 L 715 616 L 733 467 L 603 467 L 602 463 L 620 365 L 789 226 Z M 601 467 L 602 471 L 598 495 L 595 505 L 585 568 L 582 578 L 580 596 L 577 606 L 567 669 L 540 814 L 535 849 L 527 887 L 507 1006 L 504 1016 L 484 1136 L 482 1140 L 476 1140 L 428 1131 L 427 1124 L 436 1079 L 442 1039 L 446 1023 L 456 960 L 464 922 L 465 910 L 477 849 L 484 803 L 487 793 L 493 752 L 505 692 L 507 674 L 509 669 L 544 468 Z"/></svg></span>{% endmacro %}
{% macro social_fields(p) %}
<div class="t3 xs">Type</div>
<div class=checks role=group aria-label="Type"><input type=hidden name=social_kind value="">
{% for kind in SOCIAL_KINDS %}<label><input type=checkbox name=social_kind value="{{ kind }}" {% if kind in (p.social_kind or '').split(',') %}checked{% endif %}>{{ kind }}</label>{% endfor %}
</div>
<label>Place<input name=social_place value="{{ p.social_place or '' }}" autocomplete=off></label>
<label>Address or map link (optional)<input name=social_address value="{{ p.social_address or '' }}" autocomplete=off></label>
<label>Time (optional)<input type=time name=social_time value="{{ p.social_time or '' }}"></label>
<label>Note (optional)<input name=social_note value="{{ p.social_note or '' }}" autocomplete=off></label>
{% endmacro %}
{% macro message_fields(p) %}
<label>Coach message<textarea name=message maxlength=280>{{ p.coach_note or '' }}</textarea></label>
<p class="t3 sm">Leave blank to clear it.{% if p.coach_note_by %} Last set by {{ p.coach_note_by }}{% if p.coach_note_at %} · {{ fmt_stamp(p.coach_note_at) }}{% endif %}.{% endif %}</p>
{% endmacro %}
{% macro practice_extra_dialogs(p, back) %}
<dialog class=modal id=social{{ p.id }}><div class=sheet><h2 style="margin:0 0 12px">After-practice social</h2>
<form method=post action="/practices/{{ p.id }}">{{ csrf_field() }}<input type=hidden name=pid value={{ p.id }}><input type=hidden name=back value="{{ back }}">
{{ social_fields(p) }}
<button class="primary full" name=action value=social>Save</button></form></div></dialog>
<dialog class=modal id=message{{ p.id }}><div class=sheet><h2 style="margin:0 0 12px">Coach message</h2>
<form method=post action="/practices/{{ p.id }}">{{ csrf_field() }}<input type=hidden name=pid value={{ p.id }}><input type=hidden name=back value="{{ back }}">
{{ message_fields(p) }}
<button class="primary full" name=action value=message>Save</button></form></div></dialog>
<dialog class=modal id=image{{ p.id }}><div class=sheet><h2 style="margin:0 0 12px">Practice image</h2>
<form method=post action="/practices/{{ p.id }}" enctype=multipart/form-data>{{ csrf_field() }}<input type=hidden name=pid value={{ p.id }}><input type=hidden name=back value="{{ back }}">
<label>Image<input type=file name=image accept="image/jpeg,image/png,image/gif,image/webp,image/heic,image/heif,.heic"></label>
{% if p.image %}<label><input type=checkbox name=image_clear value=1> Remove image</label>{% endif %}
<p class="t3 sm">Shown on the Home card only. Leave the file empty to keep the current picture.</p>
<button class="full" name=action value=image style="background:#ececee;color:#0a0a0b">Save</button></form></div></dialog>
{% endmacro %}
{% macro practice_host_more(p, back) %}
<span class=more><button type=button class=morebtn aria-label="More for {{ fmt_d(p.date) }}" aria-haspopup=menu aria-expanded=false>⋯</button>
<div class=menu hidden role=menu>
<button type=button data-open="social{{ p.id }}">After-practice social</button>
<button type=button data-open="message{{ p.id }}">Coach message</button>
<button type=button data-open="image{{ p.id }}">Practice image</button>
</div></span>
{{ practice_extra_dialogs(p, back) }}
{% endmacro %}
{% macro practice_more(p, coach_ids, back) %}
<span class=more><button type=button class=morebtn aria-label="More for {{ fmt_d(p.date) }}" aria-haspopup=menu aria-expanded=false>⋯</button>
<div class=menu hidden role=menu>
<button type=button data-open="social{{ p.id }}">After-practice social</button>
<button type=button data-open="message{{ p.id }}">Coach message</button>
<button type=button data-open="image{{ p.id }}">Practice image</button>
<button type=button data-open="assign{{ p.id }}">Assign coaches</button>
<a href="/admin?date={{ p.date }}">Check in</a>
<a href="/practices/{{ p.id }}?edit=1">Edit practice</a>
{% if p.cancelled %}<form method=post action="/practices/{{ p.id }}">{{ csrf_field() }}<input type=hidden name=pid value={{ p.id }}><input type=hidden name=back value="{{ back }}"><button name=action value=restore>Undo cancel</button></form>
{% else %}<button type=button data-open="cancel{{ p.id }}">Send cancellation</button>{% endif %}
<form method=post action="/practices/{{ p.id }}">{{ csrf_field() }}<input type=hidden name=pid value={{ p.id }}><input type=hidden name=back value="{{ back }}"><button name=action value=duplicate>Duplicate practice</button></form>
<button type=button data-copy="{{ app_base() }}/practices/{{ p.id }}">Copy link</button>
<button type=button data-open="delete{{ p.id }}">Delete practice</button>
</div></span>
{{ practice_extra_dialogs(p, back) }}
<dialog class=modal id=assign{{ p.id }}><div class=sheet><h2 style="margin:0 0 12px">Assign coaches</h2>
<form method=post action="/practices/{{ p.id }}">{{ csrf_field() }}<input type=hidden name=pid value={{ p.id }}><input type=hidden name=back value="{{ back }}">
<div class=checks role=group aria-label="Coaches">{% for c in coach_choices %}<label><input type=checkbox name=coach value="{{ c.id }}" {% if c.id in coach_ids %}checked{% endif %}>{{ display_first(c) }} {{ c.last }} {{ coach_tag(c) }}</label>
{% else %}<p class="t3 sm">No coaches yet. Add someone on People.</p>{% endfor %}</div>
<div class=row><button class=primary name=action value=assign>Save</button><button type=button onclick="this.closest('dialog').close()">Cancel</button></div></form></div></dialog>
<dialog class=modal id=cancel{{ p.id }}><div class=sheet><h2 style="margin:0 0 8px">Send cancellation</h2>
<p class="t2 sm">Members get an email and a push that include this reason.</p>
<form method=post action="/practices/{{ p.id }}">{{ csrf_field() }}<input type=hidden name=pid value={{ p.id }}><input type=hidden name=back value="{{ back }}">
<label>Reason<textarea name=reason required></textarea></label>
<button class="primary full" name=action value=cancel>Confirm</button></form></div></dialog>
<dialog class=modal id=delete{{ p.id }}><div class=sheet><h2 style="margin:0 0 8px">Delete this practice?</h2>
<p class="t2 sm">{{ fmt_d(p.date) }}, {{ fmt_t(p.start) }}–{{ fmt_t(p.end) }} at {{ p.location }}.</p>
<form method=post action="/practices/{{ p.id }}">{{ csrf_field() }}<input type=hidden name=pid value={{ p.id }}>
<div class=row><button class=danger name=action value=delete>Delete practice</button><button type=button onclick="this.closest('dialog').close()">Cancel</button></div></form></div></dialog>
{% endmacro %}
<header{% if tab == 'home' and me() %} class=homehead{% endif %}>{% if tab == 'home' and me() %}<h1>Hi, {{ display_first(me()) }}</h1><button type=button class=avatar id=profileOpen aria-haspopup=dialog aria-controls=profileSheet aria-label="Profile">{% if me().photo %}<img src="/avatar/{{ me().id }}?v={{ me().photo }}" alt="">{% else %}{{ initials(me()) }}{% endif %}</button>{% else %}<a class=brand href=/>Grunions</a>{% if me() %}<a class=sub href=/logout>Log out</a>{% endif %}{% endif %}</header><main>
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
{% if is_staff() %}<a href=/admin class="{{'on' if tab=='admin'}}">""" + ICONS["admin"] + """Admin</a>{% elif me().is_admin %}<a href=/members class="{{'on' if tab=='admin'}}">""" + ICONS["admin"] + """Admin</a>{% endif %}
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

ADMIN_NAV = """<div class="seg noprint">{% set ep = request.endpoint %}{% if is_staff() %}<a href=/admin class="{{'on' if ep=='admin'}}">Check-in</a>{% endif %}
{% if me().is_admin %}<a href=/members class="{{'on' if ep=='members'}}">People</a><a href=/transfer class="{{'on' if ep=='transfer_page'}}">Transfer</a><a href=/expiring class="{{'on' if ep=='expiring'}}">Expiring</a>
<a href=/requirements class="{{'on' if ep=='requirements_page'}}">Rules</a><a href=/qr class="{{'on' if ep=='qr_page'}}">QR</a>{% endif %}</div>
{% set al = admin_alert() %}{% if al and ep!='admin' %}<a href=/expiring class="note noprint" style="display:block;text-decoration:none"><span class="st st-warn"></span> USAWP: <b>{{al[0]}}</b> expired · <b>{{al[1]}}</b> expiring within {{EXPIRING_DAYS}} days</a>{% endif %}
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

T["home"] = """{{ push_card() }}
{% for n in notices %}<div class="note notice">{{n.body}}</div>{% endfor %}
{% if nextp %}{% set sh = social_home(nextp) %}<div class="card tap nextcard" onclick="if(event.target.closest('button,a,form,input,select,textarea,label'))return;location.href='/practices/{{nextp.id}}'"><a class=cardlink href="/practices/{{nextp.id}}">
{% if nextp.image %}<div class=pimg><img src="/practice-image/{{ nextp.id }}?v={{ nextp.image }}" alt=""><span class=nxbadge>{% if nextp.date == today %}TODAY{% else %}{{ fmt_d(nextp.date) }}{% endif %}</span></div>{% endif %}
<div class=nxbody><div class=nxtitle>{{ fmt_d(nextp.date) }}</div>
<div class=nxrow>{{ glyph_clock() }}<span>{{ fmt_clock(nextp.start) }} – {{ fmt_clock(nextp.end) }}</span></div>
<div class=nxrow>{{ glyph_pin() }}<span>{{ short_place(nextp.location) }}</span></div>
<div class=nxrow>{{ glyph_people() }}<span>{{ nextp_n }} going{% if next_coaches %} · Coaches: {{ next_coaches }}{% endif %}</span></div>
{% if nextp.coach_note %}<div class=nxnote>{{ nextp.coach_note }} · {{ nextp.coach_note_by }} · {{ fmt_stamp(nextp.coach_note_at) }}</div>{% endif %}</div></a>
<form method=post action=/practices class=pills>{{csrf_field()}}<input type=hidden name=pid value={{nextp.id}}>
<button {% if nextp_mine==1 %}class=on {% endif %}name=action value="{{ 'clear' if nextp_mine==1 else 'going' }}">I'm going{% if nextp_mine==1 %} ✓{% endif %}</button>
<button {% if nextp_mine==0 %}class=on {% endif %}name=action value="{{ 'clear' if nextp_mine==0 else 'notgoing' }}">I'm not going{% if nextp_mine==0 %} ✓{% endif %}</button></form>
{% if sh %}<div class=nxdiv></div><div class=nxsocial><a class=cardlink href="/practices/{{nextp.id}}" style="display:flex;align-items:center;gap:12px">{{ social_icon() }}
<div class=grow><div class=nxtitle>{{ sh.title }}</div><div class="t2 sm">{{ sh.place }}</div></div></a>
<form method=post action=/practices>{{csrf_field()}}<input type=hidden name=pid value={{nextp.id}}>
<button class="joinpill{{ ' on' if next_joined }}" name=action value="{{ 'social_leave' if next_joined else 'social_join' }}">{% if next_joined %}Joined ✓{% else %}Join{% endif %}</button></form></div>{% endif %}
</div>{% endif %}
{% set cl = clearance(m) %}{% set dl = days_left(m.usawp_valid_until) %}{% set tw = trial_window(m) %}{% set ex = expiry_notes(m, cl) %}{% set cc = coach_clearance(m) %}
{% if vr_pending %}{% set play_title = 'Verification pending' %}{% set play_dot = 'warn' %}
{% elif cl.ok %}{% set play_title = 'Cleared for water polo' %}{% set play_dot = 'ok' %}
{% else %}{% set play_title = 'Not cleared for water polo' %}{% set play_dot = 'bad' %}{% endif %}
<details class="card playcard"><summary><span class=playtitle>{{play_title}}<span class="dot {{play_dot}}" aria-hidden=true></span></span><span class=playnum><span class=playclosed>USAWP # {{m.usawp_number or '—'}}</span>{% if m.usawp_verified_at %}<span class=playopen>Verified {{ m.usawp_verified_at[:10] }}</span>{% endif %}</span></summary><div class=body>
<div class=kv><span>USAWP # {{m.usawp_number or '—'}}</span>{{ member_expiry(m) }}</div>
{% for it in cl.checks %}<div class=kv><span>{{it.req.name}}</span>{{ st({'ok':'ok','no date':'warn'}.get(it.status,'bad'),
 (('expires ' ~ it.mr.expires_on) if it.mr and it.mr.expires_on else ('done ' ~ it.mr.completed_on) if it.mr and it.mr.completed_on else 'missing') if it.status!='expired' else 'expired') }}</div>{% endfor %}
{% if background_view(m) %}<div class=kv><span>Background screening</span>{{ bg_status(m) }}</div>{% endif %}
{% if cc %}<div class=kv><span>Coaching</span>{{ st('ok' if cc.ok else 'bad', cc.text) }}</div>{% elif coach_eligibility(m).text %}<div style="margin-top:8px">{{ coach_tag(m) }}</div>{% endif %}
{% if tw and tw.active and not ex.membership and m.usawp_status != 'verified' and not vr_pending %}<div style="margin-top:8px">{{ st('trial', trial_badge(tw)) }}</div><p class="sm" style="margin:8px 0 0">Ends {{tw.ends}}</p>{% elif tw and tw.expired and not ex.membership and m.usawp_status != 'verified' and not vr_pending %}<p class="sm" style="margin:8px 0 0">Trial ended {{tw.ends}}</p>{% endif %}
{% if not cl.ok %}{% if not vr_pending %}{% for line in ex.lines %}<p class="sm" style="margin:8px 0 0">{{line}}</p>{% endfor %}{% elif ex.safesport %}<p class="sm" style="margin:8px 0 0">SafeSport expired {{ex.safesport}}</p>{% endif %}
{% if ex.rest %}<p class="t2 sm" style="margin:8px 0 0">Needs: {{ex.rest|join(', ')}}</p>{% endif %}{% endif %}
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
{% set bg = background_view(m) %}{% if bg and bg.required and bg.kind == 'bad' and not vr_pending %}
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
{% endif %}</div></details>
{% if pins %}
<style>{{ leaflet_css|safe }}
.homemap .leaflet-tile-pane{filter:grayscale(1) invert(1) contrast(.9) brightness(.82)}
.homemap .leaflet-control-attribution{background:rgba(10,10,11,.72);color:#a0a0a8;font-size:10px;max-width:70%}
.homemap .leaflet-control-attribution a{color:#c8cdd3}
.homemap .leaflet-bar a,.homemap .leaflet-bar a:hover{background:#1d1d20;color:#ececee;border-bottom-color:#26262a}
.homemap .leaflet-div-icon.mpin{background:#ececee;border:2px solid #0a0a0b;border-radius:50%;box-shadow:0 0 0 1px #8a8a92}
.homemap .leaflet-div-icon.mpin.social{background:#0a0a0b;border:2px solid #ececee;box-shadow:none}
</style>
<section class=homemap id=homeMap aria-label="Practice map"></section>
<script src=/static/leaflet/leaflet.js></script>
<script>
(function(){
 var el=document.getElementById('homeMap'); if(!el||!window.L) return;
 var pins={{ pins|tojson }};
 var map=L.map(el,{zoomControl:true,attributionControl:true,scrollWheelZoom:false});
 L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png',{maxZoom:19,attribution:'&copy; OpenStreetMap'}).addTo(map);
 function directions(lat,lng){
  var dest=lat+','+lng, apple=/iPhone|iPad|iPod/.test(navigator.userAgent||'');
  var url=apple?('https://maps.apple.com/?daddr='+encodeURIComponent(dest)):('https://www.google.com/maps/dir/?api=1&destination='+encodeURIComponent(dest));
  window.open(url,'_blank','noopener');
 }
 function icon(kind){return L.divIcon({className:'mpin'+(kind==='social'?' social':''),html:'',iconSize:[16,16],iconAnchor:[8,8]});}
 var bounds=[];
 pins.forEach(function(p){
  var m=L.marker([p.lat,p.lng],{icon:icon(p.kind),title:p.label||'Directions'}).addTo(map);
  m.on('click',function(){directions(p.lat,p.lng);});
  bounds.push([p.lat,p.lng]);
 });
 if(bounds.length>1) map.fitBounds(bounds,{padding:[40,40],maxZoom:15});
 else if(bounds.length) map.setView(bounds[0],15);
 setTimeout(function(){map.invalidateSize();},0);
})();
</script>
{% endif %}
<dialog class=modal id=profileSheet><div class=sheet>
<div class=profhead>{% if m.photo %}<span class=avatar><img src="/avatar/{{ m.id }}?v={{ m.photo }}" alt=""></span>{% else %}<span class=avatar>{{ initials(m) }}</span>{% endif %}
<div><div style="font-weight:650">{{ display_first(m) }} {{ m.last }}</div>
<div class="t2 sm">{{ hist|length }} practice{{ '' if hist|length == 1 else 's' }} attended{% if nmonth %} · {{ nmonth }} this month{% endif %}</div></div></div>
<form method=post action=/home enctype=multipart/form-data>{{ csrf_field() }}<input type=hidden name=action value=avatar>
<label>Profile picture<input type=file name=photo accept="image/jpeg,image/png,image/gif,image/webp,image/heic,image/heif,.heic"></label>
<button class=full style="background:#ececee;color:#0a0a0b">Save picture</button></form>
{% if m.photo %}<form method=post action=/home style="margin-top:8px">{{ csrf_field() }}<input type=hidden name=action value=avatar_clear>
<button class=full>Remove picture</button></form>{% endif %}
<p class="sm" style="margin:16px 0 0"><a href=/notifications>Notifications</a></p>
<a class="btn full" href=/logout style="margin-top:12px">Log out</a>
</div></dialog>
<script>document.getElementById('profileOpen').onclick=function(){document.getElementById('profileSheet').showModal()};
document.getElementById('profileSheet').addEventListener('click',function(e){if(e.target===this)this.close()});</script>
{% if ann %}<div class=card><div class="t3 xs">ANNOUNCEMENT · {{display_first(ann)|upper}}</div><p style="margin:6px 0 0">{{ann.body}}</p></div>{% endif %}
<details class=card><summary>Attendance</summary><div class=body>
{% for h in hist[:20] %}<div class=kv><span>{{fmt_d(h.practice_date)}}</span><span class=t2>{{h.location}}</span></div>{% else %}<p class=t3>No practices yet.</p>{% endfor %}</div></details>
<details class=card><summary>Profile</summary><div class=body>
<div class=kv><span>Legal name</span><span>{{m.first}} {{m.last}}</span></div>
<form method=post action=/home>{{csrf_field()}}<input type=hidden name=action value=preferred>
<label>Preferred first name (optional)<input name=preferred_first value="{{m.preferred_first or ''}}" placeholder="Leave blank to use your legal first name" autocomplete=off></label>
<button class=full>Save</button></form>
<div class=kv><span>Email</span><span>{{m.email}}</span></div>
<div class=kv><span>Phone</span><span>{{m.phone}}</span></div><div class=kv><span>Role</span><span>{{role_label(m)|capitalize}}</span></div>
</div></details>"""

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

_PRACTICE_JS = """<script>
(function(){
 function closeAll(){document.querySelectorAll('.menu').forEach(function(m){m.hidden=true; var b=m.parentNode&&m.parentNode.querySelector('.morebtn'); if(b) b.setAttribute('aria-expanded','false');});}
 document.querySelectorAll('.morebtn').forEach(function(btn){
  if(btn.dataset.bound) return; btn.dataset.bound='1';
  btn.onclick=function(e){e.stopPropagation(); e.preventDefault(); var menu=btn.parentNode.querySelector('.menu'); var open=menu.hidden; closeAll(); if(open){menu.hidden=false; btn.setAttribute('aria-expanded','true');}};
 });
 document.querySelectorAll('[data-open]').forEach(function(b){
  if(b.dataset.bound) return; b.dataset.bound='1';
  b.onclick=function(e){e.stopPropagation(); e.preventDefault(); closeAll(); var d=document.getElementById(b.getAttribute('data-open')); if(d) d.showModal();};
 });
 document.querySelectorAll('[data-copy]').forEach(function(b){
  if(b.dataset.bound) return; b.dataset.bound='1';
  b.onclick=function(e){e.stopPropagation(); e.preventDefault(); var url=b.getAttribute('data-copy');
   var done=function(){var prev=b.textContent; b.textContent='Copied'; setTimeout(function(){b.textContent=prev;},1200);};
   if(navigator.clipboard&&navigator.clipboard.writeText) navigator.clipboard.writeText(url).then(done, done); else done();};
 });
 document.querySelectorAll('dialog.modal').forEach(function(d){d.addEventListener('click', function(e){if(e.target===d) d.close();});});
 if(!window.grunionsMore){window.grunionsMore=1;
  document.addEventListener('click', closeAll);
  document.addEventListener('keydown', function(e){if(e.key==='Escape') closeAll();});
 }
})();
</script>"""

T["practices"] = """<h1>Schedule</h1><p class="t2 sm" style="margin-top:-12px">Tue · Marina HS &nbsp;·&nbsp; Fri · Westminster HS &nbsp;·&nbsp; 7–8:30 PM</p>
{% for x in data %}{% set p = x.p %}<div class="card tap" id=p{{p.id}} data-pid={{p.id}} {% if p.cancelled %}style="opacity:.55"{% endif %} onclick="if(event.target.closest('button,a,form,input,select,textarea,label,dialog'))return;location.href='/practices/{{p.id}}'">
<a class=cardlink href="/practices/{{p.id}}">
<div class=nxcardhead><div class=nxtitle>Water Polo Practice</div><span class=nxchev aria-hidden=true>›</span></div>
<div class=nxmain><div class=datetile><span class=pdate>{% if x.unseen %}<span class=badge data-seen={{p.id}}>{{ x.unseen if x.unseen < 100 else '99+' }}</span>{% endif %}</span><span class=wd>{{ weekday_abbr(p.date) }}</span><span class=dn>{{ day_num(p.date) }}</span><span class=mo>{{ month_abbr(p.date) }}</span></div>
<div class="grow schedrows"><div class=nxrow>{{ glyph_clock() }}<span>{{ fmt_span(p.start, p.end) }}</span></div>
<div class=nxrow>{{ glyph_pin() }}<span>{{ p.location }}</span></div>
<div class=nxrow>{{ glyph_people() }}<span>{{ x.going|length }} going{% if x.coach_names %} · Coaches: {{ x.coach_names|join(', ') }}{% endif %}</span></div></div></div>
{% if p.cancelled %}{{ st('bad','Cancelled') }}{% if p.cancel_reason %}<div class="t3 sm">{{ p.cancel_reason }}</div>{% endif %}{% endif %}
{% if p.note %}<div class=nxnote>{{p.note}}</div>{% endif %}
{% if p.coach_note %}<div class=nxnote>{{ p.coach_note }} · {{ p.coach_note_by }} · {{ fmt_stamp(p.coach_note_at) }}</div>{% endif %}</a>
{% if not p.cancelled %}<form method=post action=/practices class=pills>{{csrf_field()}}<input type=hidden name=pid value={{p.id}}>
<button {% if x.mine == 1 %}class=on {% endif %}name=action value="{{ 'clear' if x.mine==1 else 'going' }}">I'm going{% if x.mine==1 %} ✓{% endif %}</button>
<button {% if x.mine == 0 %}class=on {% endif %}name=action value="{{ 'clear' if x.mine==0 else 'notgoing' }}">I'm not going{% if x.mine==0 %} ✓{% endif %}</button></form>
{% endif %}</div>{% endfor %}
{% if me().is_admin %}<details class=card><summary>Add a practice</summary><form method=post class=body>{{csrf_field()}}<label>Date<input type=date name=date required></label>
<div class=row><label>Start<input type=time name=start value=19:00></label><label>End<input type=time name=end value=20:30></label></div>
<label>Location<input name=location required></label><label>Note<input name=note></label><button class="primary full" name=action value=add>Add practice</button></form></details>{% endif %}""" + _PRACTICE_JS

T["practice"] = """{% set p = x.p %}<p class="t3 sm" style="margin-top:0"><a href=/practices>Schedule</a></p>
<div class=pagehead><div><h1 style="margin-bottom:4px">{{ fmt_d(p.date) }}</h1>
<div class="t2">{{ fmt_t(p.start) }}–{{ fmt_t(p.end) }} · {{ p.location }}</div>
<div style="margin-top:8px">{% if p.cancelled %}{{ st('bad','Cancelled') }}{% else %}{{ st('ok','Scheduled') }}{% endif %}</div>
{% if p.cancelled and p.cancel_reason %}<p style="margin:8px 0 0">{{ p.cancel_reason }}</p>{% endif %}
{% if me().is_admin and not p.cancelled and not x.any_eligible %}<div class="sm" style="margin-top:8px">{{ st('warn', 'No assigned coach is coach-eligible') }}</div>{% endif %}
{% if not editing and p.coach_note %}<p style="margin:12px 0 0">{{ p.coach_note }}</p><p class="t3 sm">{{ p.coach_note_by }} · {{ fmt_stamp(p.coach_note_at) }}</p>{% endif %}</div>
{% if me().is_admin %}<div style="display:flex;align-items:center;gap:8px">{% if not editing %}<a class=btn href="/practices/{{ p.id }}?edit=1">Edit</a>{% endif %}{{ practice_more(p, x.coach_ids, 'page') }}</div>{% elif is_staff() %}{{ practice_host_more(p, 'page') }}{% endif %}</div>
{% if editing %}<form method=post action="/practices/{{ p.id }}" class=card style="margin-top:16px" enctype=multipart/form-data>{{ csrf_field() }}<input type=hidden name=pid value={{ p.id }}><input type=hidden name=back value=page>
<label>Date<input type=date name=date value="{{ p.date }}" required></label>
<div class=row><label>Start<input type=time name=start value="{{ p.start }}" required></label><label>End<input type=time name=end value="{{ p.end }}" required></label></div>
<label>Location / address<input name=location value="{{ p.location or '' }}" required></label>
<label>Notes<textarea name=note>{{ p.note or '' }}</textarea></label>
<div class="t3 xs" style="margin:4px 0 8px">After-practice social</div>
{{ social_fields(p) }}
{{ message_fields(p) }}
<label>Practice image<input type=file name=image accept="image/jpeg,image/png,image/gif,image/webp,image/heic,image/heif,.heic"></label>
{% if p.image %}<label><input type=checkbox name=image_clear value=1> Remove image</label>{% endif %}
<div class=checks role=group aria-label="Coaches"><div class="t3 xs">Coaches</div>
{% for c in coach_choices %}<label><input type=checkbox name=coach value="{{ c.id }}" {% if c.id in x.coach_ids %}checked{% endif %}>{{ display_first(c) }} {{ c.last }} {{ coach_tag(c) }}</label>
{% else %}<p class="t3 sm">No coaches yet. Add someone on People.</p>{% endfor %}</div>
<div class=row><button class=primary name=action value=edit>Save</button><a class=btn href="/practices/{{ p.id }}">Cancel</a></div></form>
{% else %}
{% if not p.cancelled %}<form method=post action="/practices/{{ p.id }}" class=pills style="margin-top:16px">{{ csrf_field() }}<input type=hidden name=pid value={{ p.id }}><input type=hidden name=back value=page>
<button {% if x.mine == 1 %}class=on {% endif %}name=action value="{{ 'clear' if x.mine==1 else 'going' }}">I'm going{% if x.mine==1 %} ✓{% endif %}</button>
<button {% if x.mine == 0 %}class=on {% endif %}name=action value="{{ 'clear' if x.mine==0 else 'notgoing' }}">I'm not going{% if x.mine==0 %} ✓{% endif %}</button></form>{% endif %}
{% if social_line(p) or me().is_admin or is_staff() %}<h2>After-practice social</h2>
<div class=list><div class=li>{% if social_line(p) %}{{ social_icon() }}{% endif %}<div class=grow>
{% if social_line(p) %}<div>{{ social_line(p) }}{% if p.social_time %} · {{ fmt_t(p.social_time) }}{% endif %}</div>
<div class="t3 sm">{{ x.social_n }} joining</div>
{% if p.social_note %}<div class="t2 sm">{{ p.social_note }}</div>{% endif %}
{% if p.social_address %}{% if p.social_address.lower().startswith('http://') or p.social_address.lower().startswith('https://') %}<div class="sm"><a href="{{ p.social_address }}" target=_blank rel=noopener>Map</a></div>{% else %}<div class="t2 sm">{{ p.social_address }} · <a href="https://www.google.com/maps/dir/?api=1&amp;destination={{ p.social_address|urlencode }}" target=_blank rel=noopener>Map</a></div>{% endif %}{% endif %}
{% else %}<span class=t3>None yet.</span>{% endif %}
</div>{% if me().is_admin or is_staff() %}<button type=button class=compact data-open="social{{ p.id }}">{{ 'Edit' if social_line(p) else 'Add' }}</button>{% endif %}</div></div>{% endif %}
<h2>Coaches</h2>
<div class=list>{% for c in x.coaches %}<div class=li><div class=grow>{{ display_first(c) }} {{ c.last }} {{ coach_tag(c) }}</div></div>{% else %}<div class=li><span class=t3>No coaches assigned.</span></div>{% endfor %}</div>
<h2>Going <span class=t3>{{ x.going|length }}</span></h2>
<div class=list>{% for r in x.going %}<div class=li><div class=grow>{{ display_first(r) }} {{ r.last }}</div></div>{% else %}<div class=li><span class=t3>No one yet.</span></div>{% endfor %}</div>
<h2>Can't make it <span class=t3>{{ x.notgoing|length }}</span></h2>
<div class=list>{% for r in x.notgoing %}<div class=li><div class=grow>{{ display_first(r) }} {{ r.last }}</div></div>{% else %}<div class=li><span class=t3>No one yet.</span></div>{% endfor %}</div>
<h2>Checked in <span class=t3>{{ x.checked|length }}</span></h2>
<div class=list>{% for r in x.checked %}<div class=li><div class=grow>{{ display_first(r) }} {{ r.last }}</div></div>{% else %}<div class=li><span class=t3>No one yet.</span></div>{% endfor %}</div>
{% if p.location %}<h2>Map</h2>
<iframe class=mapframe title="Map of {{ p.location }}" src="https://maps.google.com/maps?q={{ p.location|urlencode }}&amp;z=15&amp;output=embed" loading=lazy referrerpolicy=no-referrer-when-downgrade></iframe>
<p style="margin-top:10px"><a class=btn href="https://www.google.com/maps/dir/?api=1&amp;destination={{ p.location|urlencode }}" target=_blank rel=noopener>Directions</a></p>{% endif %}
<h2>Notes</h2>
<p>{{ p.note if p.note else 'No notes.' }}</p>
{% endif %}""" + _PRACTICE_JS

_CHEV_L = '<svg width="20" height="20" viewBox="0 0 24 24" aria-hidden="true"><path d="M15 6 9 12l6 6" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>'
_CHEV_R = '<svg width="20" height="20" viewBox="0 0 24 24" aria-hidden="true"><path d="M9 6l6 6-6 6" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>'
_CAL_I = '<svg width="18" height="18" viewBox="0 0 24 24" aria-hidden="true"><rect x="3" y="5" width="18" height="16" rx="2" fill="none" stroke="currentColor" stroke-width="1.8"/><path d="M3 10h18M8 3v4M16 3v4" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/></svg>'
T["admin"] = ADMIN_NAV + """
{% if me().is_admin %}{% set al = admin_alert() or (0, 0) %}<a class=usawprow href=/expiring><span class="dot {{ 'bad' if al[0] else ('warn' if al[1] else '') }}" aria-hidden=true></span><span class=grow>USAWP: {{ al[0] }} expired · {{ al[1] }} expiring within {{ EXPIRING_DAYS }} days</span><span class=nxchev aria-hidden=true>›</span></a>{% endif %}
<form class="row noprint" method=get action=/admin style="margin-bottom:8px"><div class=calpick id=calPick data-date="{{date}}" data-q="{{q}}" data-dates='{{ days|tojson }}'>
{% if prev_d %}<a class=calnav href="/admin?date={{prev_d}}{% if q %}&amp;q={{q|urlencode}}{% endif %}" aria-label="Previous practice">""" + _CHEV_L + """</a>{% else %}<span class=calnav aria-disabled=true aria-label="Previous practice">""" + _CHEV_L + """</span>{% endif %}
<button type=button class=calbtn id=calOpen aria-haspopup=dialog aria-expanded=false aria-controls=calPop>""" + _CAL_I + """<span>{{ fmt_d(date).replace(' ', ', ', 1) }}</span></button>
{% if next_d %}<a class=calnav href="/admin?date={{next_d}}{% if q %}&amp;q={{q|urlencode}}{% endif %}" aria-label="Next practice">""" + _CHEV_R + """</a>{% else %}<span class=calnav aria-disabled=true aria-label="Next practice">""" + _CHEV_R + """</span>{% endif %}
<div class=calpop id=calPop hidden role=dialog aria-label="Choose a practice"><div class=calhead>
<button type=button class=calmonth id=calPrevM aria-label="Previous month">""" + _CHEV_L + """</button><div class=lbl id=calLabel>{{month.label}}</div>
<button type=button class=calmonth id=calNextM aria-label="Next month">""" + _CHEV_R + """</button></div>
<div class=calwd><span>S</span><span>M</span><span>T</span><span>W</span><span>T</span><span>F</span><span>S</span></div>
<div class=calgrid id=calGrid>{% for c in month.cells %}{% if c is none %}<span class=calday></span>{% elif c.has %}<a class="calday{{' on' if c.on}}" href="/admin?date={{c.iso}}{% if q %}&amp;q={{q|urlencode}}{% endif %}">{{c.day}}</a>{% else %}<span class=calday aria-disabled=true>{{c.day}}</span>{% endif %}{% endfor %}</div></div></div>
<input type=hidden name=date value="{{date}}"><input name=q value="{{q}}" placeholder="Search players..." style="margin:0"></form>
<h1 style="margin:8px 0 4px">{{loc}}</h1>
<p class="t2 sm" style="margin-top:0">{% if pr %}{{ fmt_span(pr.start, pr.end) }}{% else %}no practice scheduled{% endif %}{% if coach_names %} · Coaches: {{ coach_names|join(', ') }}{% endif %}{% if n %} · {{ n }} checked in{% endif %}</p>
{% if coach_warn %}<p class="sm" style="margin-top:0">{{ st('warn', 'No assigned coach is coach-eligible') }}</p>{% endif %}
<div class=filt role=group aria-label="RSVP">
<button type=button data-filter=going>Going ({{ going|length }})</button>
<button type=button data-filter=not>Not Going ({{ n_not }})</button>
<button type=button data-filter=none>No Response ({{ n_none }})</button>
</div>
{% macro ci(r) %}
<div class="li cirow" data-rsvp="{{ 'going' if r.going==1 else ('not' if r.going==0 else 'none') }}"><button type=button class=ci-name onclick="this.closest('.li').nextElementSibling.toggleAttribute('hidden')">
{% if r.photo %}<span class="avatar ciav"><img src="/avatar/{{ r.id }}?v={{ r.photo }}" alt=""></span>{% else %}<span class="avatar ciav">{{ initials(r) }}</span>{% endif %}
<span class=grow style="min-width:0"><span class=ell style="display:block;font-weight:500">{{ display_first(r) }} {{ r.last }}</span>{{ checkin_status(r) }}</span></button>
<form method=post>{{csrf_field()}}<input type=hidden name=member_id value={{r.id}}><input type=hidden name=date value={{date}}><input type=hidden name=q value="{{q}}">
{% if r.cid %}<button class=compact name=action value=undo title="Undo check-in">Checked in</button>{% else %}<button class="primary compact">Check in</button>{% endif %}</form></div>
{{ member_panel(r) }}{% endmacro %}
<h2>Going <span class=t3>{{going|length}}</span></h2>
<div class=list>{% for r in going %}{{ ci(r) }}{% else %}<div class=li><span class=t3>No one yet.</span></div>{% endfor %}</div>
<h2>Everyone else <span class=t3>{{rest|length}}</span></h2>
<div class=list>{% for r in rest %}{{ ci(r) }}{% else %}<div class=li><span class=t3>No one yet.</span></div>{% endfor %}</div>
<script>
document.querySelectorAll('.filt button').forEach(function(b){
 b.onclick=function(){var on=b.classList.contains('on');
  document.querySelectorAll('.filt button').forEach(function(x){x.classList.remove('on')});
  var key=on?'':b.getAttribute('data-filter'); if(!on) b.classList.add('on');
  document.querySelectorAll('.cirow').forEach(function(row){row.hidden=!!(key&&row.getAttribute('data-rsvp')!==key);});
 };
});
</script>
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

T["transfer"] = ADMIN_NAV + """<h1>Transfer</h1>
<h2>Import</h2>
<div class=card><ol class="t2 sm" style="margin:0;padding-left:18px;line-height:1.7">
<li>Log in at <a href=https://usawp.sport80.com>usawp.sport80.com</a> and switch to the Grunions club profile.</li>
<li>Members → Smart Lists → Edit Columns: name, email, membership status, member number, valid until, plus SafeSport / background columns.</li>
<li>Actions → Export Report, then upload the emailed file here.</li></ol>
<form method=post action=/transfer enctype=multipart/form-data style="margin-top:14px">{{csrf_field()}}<input type=file name=file accept=".csv,.xlsx" style="padding:11px 14px"><button class="primary full" style="margin-top:12px">Import</button></form>
{% if stats %}<div class=note style="margin-top:16px">Read {{stats.rows}} rows · updated {{stats.matched}} members · {{stats.req_updates or 0}} compliance items · {{stats.unmatched|length}} roster rows not in the app</div>
{% if stats.unmatched %}<details style="margin-top:12px"><summary>Not signed up in the app</summary><div class=body>{% for u in stats.unmatched %}<div class="kv t2">{{u}}</div>{% endfor %}</div></details>{% endif %}{% endif %}
<p class="t3 xs" style="margin:12px 0 0">Matching uses email first, then exact legal first and last name. An optional Preferred First Name column is stored as the name shown in the app and is not used for matching. A Membership Type or Member Type column adds USAWP coaches to the coaching list.</p></div>
<h2>Export</h2>
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

T["members"] = ADMIN_NAV + """<div style="display:flex;justify-content:space-between;align-items:baseline"><h1>People</h1><a class="t2 sm" href=/members.csv>Export CSV</a></div>
<div class=seg><a href=/members {% if view=='members' %}class=on{% endif %}>Members</a><a href="/members?view=coaches" {% if view=='coaches' %}class=on{% endif %}>Coaches</a><a href="/members?view=admins" {% if view=='admins' %}class=on{% endif %}>Admins</a><a href="/members?view=referees" {% if view=='referees' %}class=on{% endif %}>Referees</a></div>
{% macro prow(r, kind) %}{% set tw = trial_window(r) %}{% set ex = expiry_notes(r) %}<div class=li><div class=grow onclick="if(event.target.closest('button,a,form,input,select'))return;this.closest('.li').nextElementSibling.toggleAttribute('hidden')" style="cursor:pointer"><div style="display:flex;align-items:center;gap:8px;min-width:0">{{ status_dot(r.usawp_status) }}<span class=ell style="font-weight:500">{{display_first(r)}} {{r.last}}</span></div>
<div class="t3 xs" style="margin-top:2px">{% if kind=='admins' %}{% if r.role=='coach' %}Active coach{% else %}Not an active coach{% endif %} · {% endif %}{% if tw and tw.active and r.usawp_status != 'verified' and not ex.membership %}Ends {{tw.ends}} · {% elif tw and tw.expired and r.usawp_status != 'verified' and not ex.membership %}Trial ended {{tw.ends}} · {% elif r.usawp_valid_until %}thru {{r.usawp_valid_until}} · {% endif %}{{r.email}}{% if r.preferred_first and r.preferred_first.strip() %} · legal {{r.first}}{% endif %} · {{r.visits}} practices</div>
<div class=eligs>{% if r.is_admin %}<span class=coach-tag>Admin</span>{% endif %}{% set chip = coach_row_expiry(r) %}{% set ce = coach_eligibility(r) %}{% if r.role=='coach' or r.id in listed or ce.eligible or ce.text %}<span class="coach-tag{{ ' ' ~ chip.tone if chip.tone else '' }}">Coach{% if chip.date %} · expires {{ chip.date }}{% endif %}</span>{% endif %}{% if r.id in referees %}<span class=coach-tag>Referee</span>{% endif %}{{ referee_tag(r) }}</div>
</div>
<span class=more><button type=button class=morebtn aria-label="Actions for {{display_first(r)}} {{r.last}}" aria-haspopup=menu aria-expanded=false>⋯</button>
<div class=menu hidden role=menu>
{% if kind == 'members' %}
{% if r.is_admin %}{% if n_admins<=1 or r.email in boot %}<button type=button disabled title="{% if n_admins<=1 %}Last admin{% else %}Set by ADMIN_EMAIL{% endif %}">Remove admin</button>{% else %}<form method=post>{{csrf_field()}}<input type=hidden name=member_id value={{r.id}}><input type=hidden name=list_view value=members><button name=action value=remove_admin>Remove admin</button></form>{% endif %}{% else %}<form method=post>{{csrf_field()}}<input type=hidden name=member_id value={{r.id}}><input type=hidden name=list_view value=members><button name=action value=make_admin>Make admin</button></form>{% endif %}
{% if r.id in listed %}<form method=post>{{csrf_field()}}<input type=hidden name=member_id value={{r.id}}><input type=hidden name=list_view value=members><button name=action value=remove_coaching>Remove from coaches</button></form>{% else %}<form method=post>{{csrf_field()}}<input type=hidden name=member_id value={{r.id}}><input type=hidden name=list_view value=members><button name=action value=add_coaching>Add to coaches</button></form>{% endif %}
{% if r.id in referees %}<form method=post>{{csrf_field()}}<input type=hidden name=member_id value={{r.id}}><input type=hidden name=list_view value=members><button name=action value=remove_referee>Remove from referees</button></form>{% else %}<form method=post>{{csrf_field()}}<input type=hidden name=member_id value={{r.id}}><input type=hidden name=list_view value=members><button name=action value=add_referee>Add to referees</button></form>{% endif %}
{% elif kind == 'coaches' %}
{% if r.role=='coach' %}<form method=post>{{csrf_field()}}<input type=hidden name=member_id value={{r.id}}><input type=hidden name=list_view value=coaches><button name=action value=remove_coach>Remove active coach</button></form>{% else %}<form method=post>{{csrf_field()}}<input type=hidden name=member_id value={{r.id}}><input type=hidden name=list_view value=coaches><button name=action value=make_coach>Make active coach</button></form>{% endif %}
<form method=post>{{csrf_field()}}<input type=hidden name=member_id value={{r.id}}><input type=hidden name=list_view value=coaches><button name=action value=remove_coaching>Remove from coaches</button></form>
{% elif kind == 'eligible' %}
<form method=post>{{csrf_field()}}<input type=hidden name=member_id value={{r.id}}><input type=hidden name=list_view value=coaches><button name=action value=add_coaching>Add to coaches</button></form>
{% if r.role=='coach' %}<form method=post>{{csrf_field()}}<input type=hidden name=member_id value={{r.id}}><input type=hidden name=list_view value=coaches><button name=action value=remove_coach>Remove active coach</button></form>{% else %}<form method=post>{{csrf_field()}}<input type=hidden name=member_id value={{r.id}}><input type=hidden name=list_view value=coaches><button name=action value=make_coach>Make active coach</button></form>{% endif %}
{% elif kind == 'admins' %}
{% if n_admins<=1 or r.email in boot %}<button type=button disabled title="{% if n_admins<=1 %}Last admin{% else %}Set by ADMIN_EMAIL{% endif %}">Remove admin</button>{% else %}<form method=post>{{csrf_field()}}<input type=hidden name=member_id value={{r.id}}><input type=hidden name=list_view value=admins><button name=action value=remove_admin>Remove admin</button></form>{% endif %}
{% elif kind == 'referees' %}
<form method=post>{{csrf_field()}}<input type=hidden name=member_id value={{r.id}}><input type=hidden name=list_view value=referees><button name=action value=remove_referee>Remove from referees</button></form>
{% elif kind == 'ref_eligible' %}
<form method=post>{{csrf_field()}}<input type=hidden name=member_id value={{r.id}}><input type=hidden name=list_view value=referees><button name=action value=add_referee>Add to referees</button></form>
{% endif %}
</div></span></div>{{ member_panel(r) }}{% endmacro %}
{% if view == 'coaches' %}
<h2>Coaches <span class=t3>{{ rows|selectattr('id','in',listed)|list|length }}</span></h2>
<div class="list loose">{% for r in rows if r.id in listed %}{{ prow(r, 'coaches') }}{% else %}<div class=li><span class=t3>No one on the coaching list yet.</span></div>{% endfor %}</div>
<h2>Coach eligible <span class=t3>{{ rows|selectattr('id','in',coach_ids)|rejectattr('id','in',listed)|list|length }}</span></h2>
<div class="list loose">{% for r in rows if r.id in coach_ids and r.id not in listed %}{{ prow(r, 'eligible') }}{% else %}<div class=li><span class=t3>No one waiting.</span></div>{% endfor %}</div>
{% elif view == 'referees' %}
<h2>Referees <span class=t3>{{ rows|selectattr('id','in',referees)|list|length }}</span></h2>
<div class="list loose">{% for r in rows if r.id in referees %}{{ prow(r, 'referees') }}{% else %}<div class=li><span class=t3>No one on the referee list yet.</span></div>{% endfor %}</div>
<h2>Referee eligible <span class=t3>{{ rows|selectattr('id','in',ref_ids)|rejectattr('id','in',referees)|list|length }}</span></h2>
<div class="list loose">{% for r in rows if r.id in ref_ids and r.id not in referees %}{{ prow(r, 'ref_eligible') }}{% else %}<div class=li><span class=t3>No one waiting.</span></div>{% endfor %}</div>
{% elif view == 'admins' %}
<p class="t2 sm">{{ n_admins }} admin{{ 's' if n_admins != 1 }}</p>
<div class="list loose">{% for r in rows if r.is_admin %}{{ prow(r, 'admins') }}{% endfor %}</div>
{% else %}
<p class="t2 sm">{{rows|length}} total · {% for s,v in c.items() %}{{v}} {{s}}{{' · ' if not loop.last}}{% endfor %}</p>
<div class="list loose">{% for r in rows %}{{ prow(r, 'members') }}{% endfor %}</div>
{% endif %}
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

T["qr_page"] = ADMIN_NAV + """<div style="text-align:center"><h1>New to Grunions? Scan to join.</h1>
<div style="background:#fff;border-radius:16px;padding:18px;display:inline-block"><img src=/qr.svg alt="Sign-up QR code" style="width:min(70vw,380px);display:block"></div>
<p class="t3 sm" style="margin-top:12px">{{u}}</p><button class="primary noprint" onclick=print()>Print</button></div>"""
