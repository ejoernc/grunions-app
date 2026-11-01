"""Templates (Jinja strings) for the Grunions app. Restrained dark UI: one surface, gray text, one blue accent."""

BASE = """<!doctype html><html lang=en style="background:#0a0a0b;color-scheme:dark"><head>
<meta charset=utf-8><meta name=color-scheme content=dark><meta name=theme-color content="#0a0a0b">
<meta name=viewport content="width=device-width,initial-scale=1,viewport-fit=cover">
<meta name=apple-mobile-web-app-capable content=yes><link rel=manifest href=/manifest.webmanifest>
<link rel=icon href=/static/icons/favicon-32.png sizes=32x32 type=image/png><link rel=apple-touch-icon href=/static/icons/apple-touch-icon-180.png>
<title>Grunions</title>
<style>{{ leaflet_css|safe }}</style>
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
.pills .btn{flex:1;min-width:0}
.pills button.on{background:var(--accent);color:#fff}
.nxdiv{height:1px;background:var(--line);margin:14px 0}
.nxsocial{display:flex;align-items:center;gap:12px}
.nxicon{width:40px;height:40px;border-radius:12px;background:var(--surface2);display:flex;align-items:center;justify-content:center;flex:none;color:#C8CDD3}
.nxicon svg{display:block}
.joinpill{flex:none}
header.homehead{position:sticky;top:0;z-index:8;background:#0a0a0b;align-items:center;gap:12px;min-height:calc(76px + env(safe-area-inset-top));box-sizing:border-box;padding:calc(16px + env(safe-area-inset-top)) 20px 16px}
header.homehead .headmain{flex:1;min-width:0;display:flex;align-items:center;padding-right:56px}
header.homehead h1{margin:0;font-size:28px;line-height:1.15;letter-spacing:-.3px}
header.homehead .headtabs{flex:1;min-width:0;margin:0;padding:0}
header.homehead a.avatar{position:absolute;right:20px;top:calc(16px + env(safe-area-inset-top));z-index:1}
a.avatar,button.avatar,span.avatar{width:44px;height:44px;min-width:44px;max-width:44px;min-height:44px;max-height:44px;border-radius:50%;padding:0;background:var(--surface2);color:var(--t1);font-size:14px;font-weight:650;letter-spacing:.2px;overflow:hidden;flex:0 0 44px;border:1px solid var(--line);display:inline-flex;align-items:center;justify-content:center}
a.avatar img,button.avatar img,span.avatar img{width:44px;height:44px;max-width:44px;max-height:44px;object-fit:cover;border-radius:50%;display:block;flex-shrink:0}
.profhead{display:flex;align-items:center;gap:14px;margin:0 0 16px}.profhead .avatar{width:64px;height:64px;font-size:20px}
.nextcard{padding:0;overflow:hidden}
.nextcard .nxbody{padding:16px 16px 0}.nextcard .nxtitle{font-size:20px}
.nextcard .nxcardhead{margin:0 0 2px}
.nextcard .nxcardhead .cardlink{flex:1;min-width:0}
a.usawpchip{display:inline-flex;align-items:center;gap:6px;margin-left:auto;color:var(--t2);font-size:13px;font-weight:500;line-height:1.2;text-decoration:none;white-space:nowrap;flex:none}
a.usawpchip.warn{color:var(--warn)}
a.usawpchip.bad{color:var(--bad)}
.numcard .nxtitle{font-size:17px;line-height:1.3}
#membership{scroll-margin-top:72px}
.pimg{position:relative;line-height:0}.pimg img{width:100%;height:200px;object-fit:cover;display:block}
.nxbadge{position:absolute;top:12px;left:12px;background:#151517;color:#ececee;border:1px solid #3a3a40;border-radius:999px;padding:5px 10px;font-size:11px;font-weight:700;letter-spacing:.8px;line-height:1}
.nxrow{display:flex;align-items:center;gap:10px;margin-top:8px;color:var(--t1);font-size:15px}
.nxglyph{width:18px;height:18px;flex:none;color:#C8CDD3}
.nextcard .pills{margin:14px 16px 0}.nextcard .pills:last-child{margin-bottom:16px}
.nextcard .nxdiv{margin:14px 16px}.nextcard .nxsocial{padding:0 16px 16px}
.homemap{height:300px;margin:0 -20px 16px;background:#1a1c20;position:relative;z-index:1}
.homemap.cardmap{height:220px;margin:0 0 12px;border-radius:14px;overflow:hidden;cursor:pointer;touch-action:pan-y}
.homemap.banner{height:220px;margin:0 -20px 0;border-radius:0;overflow:hidden;position:relative}
.homemap.banner::after{content:"";position:absolute;left:0;right:0;bottom:0;height:84px;background:linear-gradient(transparent,#0a0a0b);z-index:450;pointer-events:none}
body.practicepage main{padding-top:0}
.homemap.leaflet-container,.homemap .leaflet-container{background:#1a1c20}
.homemap .leaflet-tile-pane{filter:grayscale(1) invert(1) contrast(.9) brightness(.82);opacity:0;transition:opacity .45s ease}
.homemap.tiles .leaflet-tile-pane{opacity:1}
.homemap .leaflet-control-attribution{background:rgba(10,10,11,.72);color:#a0a0a8;font-size:10px;max-width:70%}
.homemap .leaflet-control-attribution a{color:#c8cdd3}
.homemap .leaflet-bar a,.homemap .leaflet-bar a:hover{background:#1d1d20;color:#ececee;border-bottom-color:#26262a}
.homemap .leaflet-marker-icon.mpin{background:#ececee;border:3px solid #0a0a0b;border-radius:50%;box-shadow:0 0 0 1px #ececee}
.homemap .leaflet-marker-icon.mpin.social{background:#0a0a0b;border:3px solid #ececee;box-shadow:none}
body.homefull header.homehead{position:sticky;top:0;z-index:8;background:transparent}
body.homefull header.homehead.solid{background:#0a0a0b}
body.homefull main{position:relative;z-index:1;padding:0 16px calc(64px + env(safe-area-inset-bottom))}
body.homefull .homemap{position:fixed;top:0;left:0;right:0;bottom:calc(64px + env(safe-area-inset-bottom));height:auto;margin:0;z-index:0;border-radius:0;pointer-events:none}
body.homefull .homedock{position:relative;left:auto;right:auto;bottom:auto;z-index:2;max-height:none;overflow:visible;pointer-events:auto;margin:0;padding:0 0 12px;min-height:calc(100dvh - var(--homehead, 76px) - var(--homealerts, 0px) - 64px - env(safe-area-inset-bottom) - var(--peek, 60px));display:flex;flex-direction:column;justify-content:flex-end;gap:12px}
body.homefull .schedlist{position:relative;z-index:2}
.schedsame{display:none}
header.homehead .titlestack{position:relative;flex:1;min-width:0;display:flex;flex-direction:column;align-items:flex-start;gap:2px}
header.homehead .titlecross{display:grid}
header.homehead .titlecross>h1{grid-area:1/1;margin:0}
header.homehead{--titlefade:0}
header.homehead .hititle{opacity:calc(1 - var(--titlefade))}
header.homehead .schedtitle{opacity:var(--titlefade)}
header.homehead .titlestack a.usawpchip{margin:0;opacity:calc(1 - var(--titlefade))}
header.homehead.titleaway .titlestack a.usawpchip{pointer-events:none}
body.schedopen header.homehead{--titlefade:1}
.nextcard .daychip{height:32px;margin:-3px -8px -3px 0;padding:0 11px;font-size:16px}
body.schedopen header.homehead{background:#0a0a0b}
body.schedopen .homemap{opacity:0}
#schedule{scroll-margin-top:calc(var(--homehead, 88px) + 8px)}
@media (prefers-reduced-motion:reduce){body.homefull .homemap{transition:none}}
body.homefull .homemap .leaflet-marker-icon,body.homefull .homemap .leaflet-control-attribution{pointer-events:auto}
body.profilepage main{padding-bottom:calc(28px + env(safe-area-inset-bottom))}
header.profilebar{position:sticky;top:0;z-index:5;background:#0a0a0b;display:grid;grid-template-columns:88px 1fr 88px;grid-template-rows:44px;align-items:center;padding:env(safe-area-inset-top) 6px 0;box-sizing:border-box;min-height:44px}
header.profilebar h1{margin:0;text-align:center;font-size:17px;font-weight:650;line-height:44px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
header.profilebar .left,header.profilebar .right{display:flex;align-items:center;height:44px;min-width:0}
header.profilebar .left{justify-self:start;justify-content:flex-start}header.profilebar .right{justify-self:end;justify-content:flex-end}
header.profilebar button,header.profilebar a.profileback,header.profilebar a.profileact{background:none;color:var(--t1);height:44px;min-width:44px;max-height:44px;padding:0 10px;font-weight:600;font-size:16px;text-decoration:none;display:inline-flex;align-items:center;justify-content:center}
header.profilebar button.editonly,header.profilebar a.editonly{display:none}
body.profile-edit header.profilebar button.viewonly,body.profile-edit header.profilebar a.viewonly{display:none}
body.profile-edit header.profilebar button.editonly,body.profile-edit header.profilebar a.editonly{display:inline-flex}
header.profilebar button.savebtn{color:var(--accent);font-weight:650}
.profilehero{display:flex;flex-direction:column;align-items:center;padding:12px 0 4px}
.avatarwrap{position:relative;width:112px;height:112px;flex:none}
button.avatar.hero,span.avatar.hero{width:112px;height:112px;min-width:112px;max-width:112px;min-height:112px;max-height:112px;flex:0 0 112px;font-size:36px}
button.avatar.hero img,span.avatar.hero img{width:112px;height:112px;max-width:112px;max-height:112px}
button.cambadge{position:absolute;right:-4px;bottom:-4px;z-index:2;width:32px;height:32px;min-width:32px;min-height:32px;padding:0;border-radius:50%;background:#2a2a2e;color:#ececee;border:2px solid #ececee;display:flex;align-items:center;justify-content:center}
button.cambadge svg{width:16px;height:16px;fill:none;stroke:currentColor;stroke-linecap:round;stroke-linejoin:round}
body.profile-edit button.cambadge.editonly{display:flex}
button.textlink{background:transparent;color:var(--t1);height:auto;min-height:0;padding:6px 8px;border-radius:0;font-size:14px;font-weight:600}
button.textlink.danger{color:var(--bad)}
a.rowbtn,button.rowbtn{width:100%;height:auto;min-height:60px;padding:14px 18px;border-radius:0;background:transparent;color:var(--t1);font-weight:500;justify-content:flex-start;text-decoration:none;border-top:1px solid var(--line)}
.list>form{margin:0}
.list>form:not(:first-child)>button.rowbtn{border-top:1px solid var(--line)}
.pracemeta{color:var(--t2);text-align:center;margin:0;font-size:15px}
.pracemeta+.pracemeta{margin-top:2px}
.pracestatus{margin:10px 0 2px}
.stats.trio{width:100%;max-width:420px}
.stats.trio .stattile{flex:1;min-width:0;padding:12px 8px}
.list .li .coach-elig{margin-left:0;flex:none;height:24px;padding:0 8px;border-radius:999px;border:1px solid var(--line);background:#2a2a2e;font-size:12px;font-weight:600}
.profilename{margin:14px 0 4px;font-size:24px;font-weight:650;letter-spacing:-.3px;text-align:center}
.profilesub{color:var(--t2);text-align:center;margin:0 0 16px}
.stats{display:flex;gap:10px;justify-content:center;margin:0 0 8px}
.stattile{min-width:120px;background:var(--surface);border-radius:14px;padding:12px 16px;text-align:center}
.stattile b{display:block;font-size:22px;font-weight:650;line-height:1.2}
.stattile span{color:var(--t2);font-size:12px}
.seclabel{margin:22px 4px 8px;color:var(--t3);font-size:13px;font-weight:600}
.sechead{display:flex;align-items:baseline;justify-content:space-between;gap:12px;margin:22px 4px 8px}
.sechead .seclabel{margin:0}
.verifiedwhen{margin:0;color:var(--t3);font-size:13px;font-weight:400;font-family:inherit;line-height:1.5;text-align:right;flex:none}
.rowtitle{display:inline-flex;align-items:center;gap:6px;flex:none;white-space:nowrap}
.prow .v{font-size:14px;color:var(--t2);text-align:right}
.prow{justify-content:space-between;gap:8px;padding-left:16px;padding-right:16px}
.prow .k{color:var(--t2)}
.prow .v{text-align:right}
a.chevrow{color:inherit;text-decoration:none;width:100%}
a.chevrow .nxchev{color:var(--t3);font-size:22px}
a.logoutrow{color:var(--bad);text-decoration:none;width:100%;justify-content:center;font-weight:600}
.textlink{background:none;color:var(--t1);height:auto;padding:8px 12px;font-weight:600}
.textlink.danger{color:var(--bad)}
.editonly{display:none}
body.profile-edit .editonly{display:block}
body.profile-edit .editonly.inline{display:inline-flex}
body.profile-edit .viewonly{display:none}
input[type=file].pick{position:absolute;width:1px;height:1px;padding:0;margin:-1px;overflow:hidden;clip:rect(0,0,0,0);border:0;opacity:0}
.prefedit{margin:0}
.prefedit input{margin-top:6px}
.homealerts{position:relative;z-index:1}
.homedock{position:fixed;z-index:2;left:0;right:0;bottom:calc(64px + env(safe-area-inset-bottom));max-width:640px;margin:0 auto;padding:0 12px 10px;display:flex;flex-direction:column;gap:8px;max-height:min(68vh,calc(100dvh - 150px));overflow:auto;pointer-events:none}
.homedock .card{pointer-events:auto;background:#151517;margin:0}
.menu a{display:flex;align-items:center;width:100%;height:40px;padding:0 12px;box-sizing:border-box;color:var(--t1);font-weight:500;font-size:15px;text-decoration:none;border-radius:8px}
.card .menu,.pagehead .menu{left:auto;right:0;min-width:220px}
.pagehead{display:flex;justify-content:space-between;align-items:flex-start;gap:12px}
.usawp-line{display:flex;align-items:center;justify-content:space-between;gap:12px;margin-top:12px}
.list{background:var(--surface);border-radius:var(--r);margin:0 0 12px;overflow:hidden}
.list.loose{overflow:visible}
.more{position:relative;flex:0 0 auto;margin-left:2px}
button.morebtn{width:32px;height:32px;padding:0;background:transparent;color:var(--t3);font-size:22px;line-height:1;border-radius:8px}button.morebtn svg,.m .more svg{width:22px;height:22px;display:block;fill:none;stroke:currentColor;stroke-linecap:round;stroke-linejoin:round}
button.morebtn[aria-expanded=true]{background:var(--surface2);color:var(--t1)}
.menu{position:absolute;left:0;top:36px;z-index:20;min-width:232px;padding:6px;background:#151517;border:1px solid var(--line);border-radius:12px;box-shadow:0 10px 28px rgba(0,0,0,.45)}
.menu form{margin:0}
.menu button{width:100%;height:40px;padding:0 12px;justify-content:flex-start;background:transparent;color:var(--t1);font-weight:500;font-size:15px;border-radius:8px}
.menu button:disabled{color:var(--t3)}
.li{display:flex;align-items:center;gap:12px;padding:14px 18px;min-height:60px;border-top:1px solid var(--line)}.li:first-child{border-top:0}
.li.prow{padding-left:16px;padding-right:16px;gap:8px}
.editonly,.li.editonly{display:none}
body.profile-edit .editonly{display:inline-flex}
body.profile-edit .li.editonly{display:flex}
body.profile-edit .viewonly{display:none}
.grow{flex:1;min-width:0}.ell{white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
label{display:block;font-size:13px;color:var(--t2);margin:0 0 14px}
.checks{margin:0 0 14px}.checks label{display:flex;align-items:center;min-height:40px;margin:0;color:var(--t1);font-size:16px}
input,select,textarea{display:block;width:100%;margin-top:6px;background:var(--surface2);border:1px solid var(--line);color:var(--t1);border-radius:10px;
padding:0 14px;height:48px;font:inherit;color-scheme:dark}textarea{padding:12px 14px}input[type=hidden]{display:none}input[type=checkbox]{display:inline-block;width:20px;height:20px;margin:0 8px 0 0;vertical-align:-4px;accent-color:var(--accent)}
input[type=date]::-webkit-calendar-picker-indicator,input[type=datetime-local]::-webkit-calendar-picker-indicator{cursor:pointer;background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Crect x='3' y='5' width='18' height='16' rx='2' fill='none' stroke='%23ececee' stroke-width='1.8'/%3E%3Cpath d='M3 10h18M8 3v4M16 3v4' fill='none' stroke='%23ececee' stroke-width='1.8' stroke-linecap='round'/%3E%3C/svg%3E");background-repeat:no-repeat;background-size:18px 18px;background-position:center}
input[type=time]::-webkit-calendar-picker-indicator{cursor:pointer;background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Ccircle cx='12' cy='12' r='8' fill='none' stroke='%23ececee' stroke-width='1.8'/%3E%3Cpath d='M12 8v5l3 2' fill='none' stroke='%23ececee' stroke-width='1.8' stroke-linecap='round'/%3E%3C/svg%3E");background-repeat:no-repeat;background-size:18px 18px;background-position:center}
input:focus,select:focus,textarea:focus{outline:none;border-color:var(--accent)}
.btn,a.btn,button.btn,button{display:inline-flex;align-items:center;justify-content:center;gap:6px;box-sizing:border-box;height:48px;padding:0 18px;border-radius:12px;border:0;font:inherit;font-weight:600;line-height:1;
cursor:pointer;text-decoration:none;background:var(--surface2);color:#fff}
.btn,a.btn,button.btn{min-height:48px}
.btn-primary,button.btn-primary,a.btn-primary,.btn.primary,button.primary{background:var(--accent);color:#fff}
.btn-secondary,button.btn-secondary,a.btn-secondary{background:var(--surface2);color:#fff}
.btn-danger,button.btn-danger,a.btn-danger,.btn.danger,button.danger{background:var(--surface2);color:var(--bad)}
.btn.quiet,button.quiet{background:transparent;color:var(--t2);height:44px;min-height:44px;padding:0 8px}
.btn.compact,button.compact{padding:0 14px}.full{width:100%}.row{display:flex;gap:10px}.row>*{flex:1}
.chip,a.chip,button.chip{display:inline-flex;align-items:center;justify-content:center;box-sizing:border-box;height:36px;min-height:36px;padding:0 14px;border-radius:999px;border:1px solid var(--line);background:transparent;color:var(--t2);font-size:14px;font-weight:600;line-height:1;text-decoration:none;white-space:nowrap;flex:none;cursor:pointer}
.chip-active,a.chip-active,button.chip-active,.chip.on,a.chip.on,button.chip.on{background:#ececee;color:#0a0a0b;border-color:#ececee}
.chip-info,.coach-tag{display:inline-flex;align-items:center;gap:6px;height:24px;margin-left:6px;padding:0 8px;border-radius:999px;border:1px solid var(--line);background:#2a2a2e;color:var(--t1);font-size:12px;font-weight:600;line-height:1;white-space:nowrap;vertical-align:1px}
.chip-info.warn,.coach-tag.warn{color:var(--warn);border-color:#8a6410;background:transparent}
.chip-info.bad,.coach-tag.bad{color:var(--bad);border-color:#7a302c;background:transparent}
.nxbadge{margin:0;height:auto;padding:5px 10px;letter-spacing:.8px;background:#151517;color:#ececee;border-color:#3a3a40}
.coach-elig,.ref-elig{margin-left:8px;font-weight:650;font-size:15px}
.eligs{display:flex;flex-wrap:wrap;gap:4px 10px;margin-top:4px}.eligs .coach-elig,.eligs .ref-elig,.eligs .coach-tag,.eligs .chip-info{margin-left:0}.eligs .st{white-space:normal}
.memline{display:flex;flex-wrap:wrap;align-items:center;gap:2px 0;margin-top:2px;color:var(--t3);font-size:13px;line-height:1.4}
.st{display:inline-flex;align-items:center;gap:7px;font-size:14px;color:var(--t2);white-space:nowrap}
.st::before{content:"";width:8px;height:8px;border-radius:50%;background:var(--t3)}.st-ok::before{background:var(--ok)}.st-bad::before{background:var(--bad)}.st-warn::before{background:var(--warn)}.st-trial::before{background:var(--warn)}
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
details.checkin{margin:4px 0 20px}details.checkin>summary{min-height:0;padding:18px 0 8px;font-size:17px;font-weight:600;justify-content:flex-start;gap:8px}
.kv{display:flex;justify-content:space-between;gap:12px;padding:10px 0;border-top:1px solid var(--line);font-size:15px}.kv:first-child{border-top:0}.kv span:first-child{color:var(--t2)}
.admintabs{display:flex;gap:8px;overflow-x:auto;margin:0 0 16px;padding:2px 0 4px;scrollbar-width:none;-webkit-overflow-scrolling:touch}
.admintabs::-webkit-scrollbar{display:none}
.admintabs a.chip{flex:none}
.pagetitle{display:flex;justify-content:space-between;align-items:baseline;gap:12px}.pagetitle h1{margin-bottom:12px}
.peoplebar{position:sticky;top:var(--headh,0px);z-index:6;background:#0a0a0b;margin:0 -20px 8px;padding:0 20px 10px}
.peoplebar input{height:48px;margin:0}
.fchips{display:flex;gap:8px;margin:10px 0 0;overflow-x:auto;scrollbar-width:none;-webkit-overflow-scrolling:touch}
.fchips::-webkit-scrollbar{display:none}
.fchips a.chip{flex:none}
.expage h2.egroup{position:sticky;top:var(--headh,0px);z-index:4;background:#0a0a0b;margin:18px 0 8px;padding:8px 0}
.daybadge{height:28px;padding:0 10px;margin:0;flex:none;font-weight:700}
.people h2{position:sticky;top:calc(var(--headh,0px) + var(--peoplepin,0px));z-index:4;background:#0a0a0b;padding:8px 0;margin-top:12px}
.lgroup{margin:0 0 14px}
.lgroup .list{margin:0}
h3.alpha{margin:0;padding:8px 0 6px;font-size:13px;font-weight:700;letter-spacing:.06em;color:var(--t3);position:sticky;top:calc(var(--headh,0px) + var(--peoplepin,0px));z-index:4;background:#0a0a0b}
.psub{display:block;margin-top:1px;color:var(--t2);font-size:14px;line-height:1.35;min-width:0}
.peoplebar .peoplesum{margin:12px 0 0;line-height:1.35}
.seg{display:flex;gap:8px;margin:0 0 16px;overflow-x:auto;scrollbar-width:none}
.seg::-webkit-scrollbar{display:none}
nav.tabs{position:fixed;left:0;right:0;bottom:0;z-index:9;box-sizing:border-box;
height:calc(64px + env(safe-area-inset-bottom));padding:0 0 env(safe-area-inset-bottom);background:#0a0a0b;
border-top:1px solid var(--line);display:flex;justify-content:center;view-transition-name:grunions-nav}
nav.tabs a{position:relative;flex:1;max-width:140px;height:64px;min-height:64px;box-sizing:border-box;
display:flex;flex-direction:column;align-items:center;justify-content:center;gap:4px;padding:0;margin:0;
color:var(--t3);text-decoration:none;font:500 12px/14px -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,system-ui,sans-serif}
.badge{display:inline-flex;align-items:center;justify-content:center;min-width:16px;height:16px;padding:0 4px;border-radius:8px;background:var(--bad);color:#fff;font-size:10px;font-weight:700;line-height:1}
nav.tabs a .badge{position:absolute;top:4px;left:50%;margin-left:8px}.datetile{position:relative}.datetile .pdate{position:absolute;top:0;right:0}.datetile .pdate .badge{position:absolute;top:-4px;right:-4px;margin:0}
/* Line icons: Streamline Plump free set, CC BY 4.0. https://creativecommons.org/licenses/by/4.0/ */
nav.tabs a.on{color:var(--accent)}nav.tabs svg{width:24px;height:24px;flex:none;display:block;fill:none;stroke:currentColor;stroke-linecap:round;stroke-linejoin:round}
.chat{display:flex;flex-direction:column;gap:0}.m{position:relative;-webkit-touch-callout:none;margin-top:14px;display:flex;flex-direction:column;align-items:flex-start}.m.g-mid,.m.g-last{margin-top:2px}.chat>.m:first-child{margin-top:0}.m .who{font-size:13px;color:var(--t3);margin:0 0 3px}.m .txt{background:var(--surface);border-radius:14px;padding:10px 14px;display:inline-block;max-width:85%;white-space:pre-wrap;word-wrap:break-word}.m .txt a.msglink{color:var(--accent);text-decoration:none}
.m.g-first:not(.mine) .txt,.m.g-first:not(.mine) .img img{border-bottom-left-radius:5px}.m.g-mid:not(.mine) .txt,.m.g-mid:not(.mine) .img img{border-top-left-radius:5px;border-bottom-left-radius:5px}.m.g-last:not(.mine) .txt,.m.g-last:not(.mine) .img img{border-top-left-radius:5px}
.m.g-first.mine .txt,.m.g-first.mine .img img{border-bottom-right-radius:5px}.m.g-mid.mine .txt,.m.g-mid.mine .img img{border-top-right-radius:5px;border-bottom-right-radius:5px}.m.g-last.mine .txt,.m.g-last.mine .img img{border-top-right-radius:5px}
.m.mine{text-align:right;align-items:flex-end}.m.mine .txt{background:var(--surface2);text-align:left}.m.ann{align-items:stretch}.m.ann .txt{display:block;max-width:none;border:1px solid var(--line);background:var(--surface)}
.m .txt.deleted{font-style:italic;color:var(--t3);background:transparent}.m .edited{font-size:12px;color:var(--t3);font-weight:400}
.m .more{display:none;position:absolute;top:-4px;right:0;width:32px;height:32px;padding:0;background:none;color:var(--t3);font-size:18px}
.m.mine .more{left:0;right:auto}
@media (hover:hover) and (pointer:fine){.m:hover .more{display:inline-flex}}
.m .editbox textarea{min-height:72px;height:auto;margin:0}
.composer{position:fixed;left:0;right:0;bottom:calc(64px + env(safe-area-inset-bottom));background:var(--bg);padding:10px 20px;border-top:1px solid var(--line);z-index:8}
.composer form{max-width:600px;margin:auto;display:flex;gap:8px;align-items:flex-end}
.composer textarea{margin:0;height:48px;min-height:48px;max-height:136px;resize:none;line-height:22px;padding:12px 14px;overflow-y:auto;scrollbar-width:none;-ms-overflow-style:none}
.composer textarea::-webkit-scrollbar{display:none}.iconbtn{width:48px;padding:0;flex:none;color:var(--t2)}.iconbtn svg{width:22px;height:22px;fill:none;stroke:currentColor;stroke-linecap:round;stroke-linejoin:round}
.iconbtn.send{color:var(--accent)}
.preview{max-width:600px;margin:0 auto 8px;display:flex;align-items:center;gap:10px;color:var(--t2);font-size:14px}.preview img{height:48px;border-radius:8px}
.m .img{display:block;margin:0}.m .txt+.img{margin-top:4px}.m.mine .img{margin-left:auto}.m .img img{max-width:min(70vw,280px);max-height:280px;border-radius:12px;display:block;background:var(--surface)}.m.mine .img{width:fit-content}
.rx{display:flex;flex-wrap:wrap;gap:6px;margin:0}.rx:not(:empty){margin-top:6px}.m.mine .rx{justify-content:flex-end}
.seenline{display:block;width:fit-content;height:auto;margin:4px 0 0;padding:0;background:none;border:0;border-radius:0;color:var(--t3);font-size:12px;font-weight:500;line-height:1.3}
.m.mine .seenline{margin-left:auto}
span.avatar.seenav,span.avatar.seenav img{width:32px;height:32px;min-width:32px;max-width:32px;min-height:32px;max-height:32px;flex:0 0 32px;font-size:12px}
.seenrow{display:flex;align-items:center;gap:10px;min-height:40px}
.seenlist{max-height:38vh;overflow:auto}
.seenh{margin:14px 0 6px;font-size:13px;font-weight:650;color:var(--t3);letter-spacing:.02em}
.rx button{height:30px;min-height:30px;padding:0 10px;border-radius:999px;font-size:14px;font-weight:500;background:var(--surface);color:var(--t2);border:1px solid var(--line)}
.rx button.on{border-color:#ececee;color:var(--t1);background:#2a2a2e}
.qbar{max-width:600px;margin:0 auto 8px;display:flex;align-items:center;gap:10px;border-left:3px solid #6c6c74;padding:2px 4px 2px 10px;color:var(--t2);font-size:13px}
.qbar b{display:block;color:var(--t1);font-size:12px;font-weight:650}.qbar span{display:block;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;max-width:70vw}
.qbar button{width:32px;height:32px;padding:0;background:none;color:var(--t3);flex:none}
.quotechip{border-left:3px solid #6c6c74;padding:2px 8px;margin:0 0 6px;color:var(--t2);font-size:13px;text-align:left}
.quotechip b{display:block;color:var(--t3);font-weight:650;font-size:12px}
dialog.botsheet{position:fixed;z-index:30;inset:auto 0 0 0;margin:0 auto;width:min(640px,100%);height:fit-content;max-height:calc(100dvh - 8px);border:0;padding:0;background:transparent;color:var(--t1);overflow:visible}
dialog.botsheet::backdrop{background:rgba(0,0,0,.62);opacity:1;transition:opacity .25s ease-out}
dialog.botsheet.opening::backdrop,dialog.botsheet.closing::backdrop{opacity:0}
dialog.botsheet .sheet{background:#1c1c1f;border:1px solid #2e2e32;border-bottom:0;border-radius:18px 18px 0 0;padding:0 12px calc(14px + env(safe-area-inset-bottom));max-height:calc(100dvh - 12px);overflow:auto;transform:translateY(0);transition:transform .25s ease-out}
.grab{display:block;width:100%;height:28px;margin:0 0 8px;padding:0;position:sticky;top:0;z-index:1;background:#1c1c1f;touch-action:none;cursor:grab}
.grab::after{content:"";position:absolute;left:50%;top:12px;width:36px;height:5px;margin-left:-18px;border-radius:3px;background:#5a5a60}
@media (prefers-reduced-motion:reduce){dialog.botsheet::backdrop,dialog.botsheet .sheet{transition:none}}
.emogrid{display:grid;grid-template-columns:repeat(6,1fr);gap:8px;margin:0 0 14px}
.emogrid button{width:100%;aspect-ratio:1;height:auto;padding:0;border-radius:50%;background:#2c2c2e;font-size:22px}
.emopick{display:grid;grid-template-columns:repeat(8,1fr);gap:6px;max-height:28vh;overflow:auto;margin:0 0 12px}
.emopick button{height:40px;padding:0;border-radius:10px;background:#2c2c2e;font-size:20px}
.actgroup{background:#2c2c2e;border-radius:14px;overflow:hidden;margin:0 0 10px}
.actgroup .actrow{width:100%;height:48px;padding:0 14px;border-radius:0;background:transparent;color:var(--t1);font-weight:500;justify-content:flex-start;gap:12px;border-bottom:1px solid #3a3a3e}
.actgroup .actrow:last-child{border-bottom:0}
.actgroup .actrow svg{width:20px;height:20px;flex:none;fill:none;stroke:currentColor;stroke-linecap:round;stroke-linejoin:round}
.actgroup .actrow.danger,.actgroup .actrow.danger svg{color:var(--bad)}
#actConfirm{margin:0 0 10px;font-weight:600}
.lightbox{position:fixed;inset:0;background:rgba(0,0,0,.92);display:flex;align-items:center;justify-content:center;z-index:20}.lightbox img{max-width:96vw;max-height:92vh;border-radius:8px}
.gobtn{background:none;height:auto;padding:4px 0;color:var(--t2);font-weight:500;font-size:14px}.gobtn::after{content:" ›";color:var(--t3)}
.ci-name,a.ci-name{flex:1;min-width:0;height:auto;padding:0;background:none;display:flex;align-items:center;gap:12px;text-align:left;font-weight:400;color:inherit;text-decoration:none}
.cirow .st{display:block;overflow:hidden;text-overflow:ellipsis}
span.avatar.ciav,span.avatar.ciav img{width:40px;height:40px;min-width:40px;max-width:40px;min-height:40px;max-height:40px;flex:0 0 40px;font-size:13px}
.filt{display:flex;gap:8px;margin:0 0 16px;flex-wrap:wrap}
.filt button.chip:disabled{opacity:.4;color:var(--t3);cursor:default;pointer-events:none}
.checkbar{position:sticky;top:var(--headh,0px);z-index:6;background:#0a0a0b;margin:0 -20px 8px;padding:8px 20px 10px}
.checkbar form.row{flex-wrap:nowrap;align-items:center;gap:8px}
.checkbar .calpick{flex:0 0 auto}
.checkbar .calbtn{flex:0 0 auto}
.checkbar .calbtn span{overflow:visible;text-overflow:clip}
.checkbar input[name=q]{flex:1 1 auto;width:auto;min-width:0;margin:0;height:48px;font-size:14px}
.checkprog{margin:8px 0 0;color:var(--t2);font-size:14px;font-weight:600}
a.schedlink{display:flex;align-items:center;gap:10px;margin:8px 0 4px;color:inherit;text-decoration:none}
a.schedlink h1{margin:0}
a.schedlink p{margin:2px 0 0}
a.schedlink .schedchev{flex:none;color:var(--t3);display:flex}
a.schedlink .schedchev svg{display:block}
button.dock,a.dock{background:var(--accent);color:#fff}
a.quietcheck,button.quietcheck{background:var(--surface2);color:#fff;border:0;border-radius:12px}
.emptyfind{color:var(--t2);margin:8px 0 16px}
details.lineuppast{margin-top:8px}details.lineuppast>summary{min-height:44px;padding:8px 0;font-size:17px;font-weight:600;justify-content:flex-start}
.repeatblock .repeatopts{display:none}.repeatblock:has(input[name=repeat]:checked) .repeatopts{display:block}
.tripcard{padding:0;overflow:hidden}.tripcard .evbody{padding:0 18px 18px}.tripcard .nxcardhead{flex-wrap:wrap;align-items:flex-start}.tripcard .nxcardhead .tripname{flex:1 1 100%;min-width:0}.tripcard .nxcardhead .chip-info{flex:none;margin-left:0}.lineupchips{display:flex;gap:6px;flex-wrap:wrap;align-items:center}.lineupchips .chip-info{margin:0}
.tripcard .tripwhere{align-items:flex-start}.tripcard .tripwhere a{min-width:0}
.evbanner{height:132px;display:flex;align-items:flex-end;padding:14px;position:relative;overflow:hidden;background:linear-gradient(160deg,#3a3a40,#141416)}
.evbanner.cat-activities{background:linear-gradient(165deg,#2e3238,#141416)}.evbanner.cat-club{background:linear-gradient(150deg,#34343a,#121214)}.evbanner.cat-learn{background:linear-gradient(170deg,#32363c,#141418)}.evbanner.cat-service{background:linear-gradient(155deg,#2c3036,#121214)}.evbanner.cat-travel{background:linear-gradient(160deg,#3a3e46,#101014)}.evbanner.cat-social{background:linear-gradient(160deg,#3a3a40,#16161a)}
.evbanner img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}.evbanner svg{position:relative;z-index:1;color:#ececee}
.lineupacts{display:flex;gap:8px;flex-wrap:wrap;margin:0 0 14px}.lineupacts .btn{width:auto;padding:0 14px}
.evhost{color:var(--t2);font-size:14px;margin:2px 0 8px}.evnote{color:var(--t2);font-size:15px;line-height:1.4;margin:8px 0}
details.moredetails{margin:8px 0 12px}details.moredetails>summary{min-height:44px;padding:8px 0;font-weight:600}
.growthcard{position:relative;padding:14px 14px 8px;margin:0 0 12px}
.growthhead{font-size:15px;font-weight:650;line-height:1.3;margin:0 0 6px}
.growthcard svg{width:100%;height:auto;display:block;touch-action:none}
.growthtip{position:absolute;z-index:2;top:36px;transform:translateX(-50%);background:#1d1d20;color:var(--t1);border:1px solid var(--line);border-radius:10px;padding:6px 10px;font-size:13px;white-space:nowrap;pointer-events:none}
.calpick{position:relative;flex:1.6;min-width:0;display:flex;align-items:center;gap:4px}
.calnav,.calmonth{flex:none;width:36px;height:36px;padding:0;display:inline-flex;align-items:center;justify-content:center;background:none;color:var(--t1);text-decoration:none;border-radius:10px}
.calnav{height:48px;width:40px}
.calnav[aria-disabled=true]{color:var(--t3);opacity:.35;pointer-events:none}
.calnav svg,.calmonth svg,.calbtn svg{fill:none;stroke:currentColor;stroke-linecap:round;stroke-linejoin:round;display:block}.calnav svg,.calmonth svg{stroke-width:1.8}
.calbtn{flex:1;min-width:0;height:48px;min-height:48px;margin:0;padding:0 10px;background:var(--surface2);border:1px solid var(--line);color:var(--t1);border-radius:12px;font:inherit;font-weight:600;display:flex;align-items:center;justify-content:center;gap:8px;cursor:pointer}
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
.pstat{padding:14px 0 2px}.pstatline{display:flex;align-items:center;gap:8px;flex-wrap:wrap}
.pstat .dot{width:10px;height:10px}.pstitle{font-size:20px;font-weight:650;letter-spacing:-.2px;line-height:1.2}
.pchips{margin-left:auto;display:flex;flex-wrap:wrap;gap:6px;align-items:center}
.preason{margin:6px 0 0;color:var(--t2);font-size:15px}
.panel .kv{padding:8px 0}.cred{display:inline-flex;align-items:center;gap:8px;color:var(--t1);text-align:right}
.pfoot{margin:10px 0 0}
.actpills{display:flex;flex-wrap:wrap;gap:8px;margin:14px 0 2px;align-items:center}
.actpills form{margin:0;flex:1}.actpills .btn{flex:1}
.actpills button:disabled{color:var(--t3);background:#2a2a2e}
dialog.memberedit h2{margin:0 0 12px;font-size:22px;letter-spacing:-.3px}
dialog.memberedit h3{font-size:13px;letter-spacing:.04em;text-transform:uppercase;color:var(--t3);margin:20px 0 8px;font-weight:650}
dialog.memberedit h3[data-section=membership]{margin-top:0}
dialog.memberedit .help{margin:0 0 12px}
dialog.memberedit .help a{color:var(--t1)}
.datefield{position:relative}
.datefield .dateph{display:none;position:absolute;left:14px;right:42px;bottom:0;height:48px;line-height:48px;color:var(--t3);pointer-events:none;font-size:16px}
.datefield.empty .dateph{display:block}
.datefield.empty input[type=date]{color:transparent}
.datefield.empty input[type=date]::-webkit-datetime-edit,.datefield.empty input[type=date]::-webkit-datetime-edit-fields-wrapper{color:transparent}
@media print{header,nav,.noprint{display:none!important}body{background:#fff;color:#000}.card{background:#fff}}
</style></head><body style="background:#0a0a0b;color:#ececee;margin:0" class="{% if (tab=='home' or tab=='practices') and me() %}homefull{% if tab=='practices' %} schedopen{% endif %}{% elif tab=='profile' or tab=='member' %}profilepage{% if tab=='member' and editing %} profile-edit{% endif %}{% elif tab=='practice' %}practicepage{% endif %}">
{% macro st(kind, label) %}<span class="st st-{{kind}}">{{label}}</span>{% endmacro %}
{% macro bubble(n) %}{% if n %}<span class=badge>{{ n if n < 100 else '99+' }}</span>{% endif %}{% endmacro %}
{% macro usawp(s) %}{{ st({'verified':'ok','expired':'bad','pending':'warn'}.get(s,'none'), 'USAWP ' ~ s) }}{% endmacro %}
{% macro coach_tag(m) %}{% set ce = coach_eligibility(m) %}{% if ce.eligible %}<span class="st st-ok coach-elig">Coach eligible</span>{% elif ce.text %}<span class="st st-bad coach-elig">{{ce.text}}</span>{% endif %}{% endmacro %}
{% macro referee_tag(m) %}{% set rf = referee_eligibility(m) %}{% if rf.eligible %}<span class="st st-ok ref-elig">Referee eligible</span>{% elif rf.text %}<span class="st st-bad ref-elig">{{rf.text}}</span>{% endif %}{% endmacro %}
{% macro bg_line(m) %}{% set bg = background_view(m) %}{% if bg %}{{ st(bg.kind, bg.text) }}{% endif %}{% endmacro %}
{% macro bg_status(m) %}{% set bg = background_view(m) %}{% if bg %}{{ st(bg.kind, ('expires ' ~ bg.date) if bg.date else 'missing') }}{% endif %}{% endmacro %}
{% macro member_expiry(m) %}{% set left = days_left(m.usawp_valid_until) %}{% if not m.usawp_valid_until %}{{ st('bad', 'missing') }}{% elif left < 0 %}{{ st('bad', 'expires ' ~ m.usawp_valid_until) }}{% elif left <= EXPIRING_DAYS %}{{ st('warn', 'expires ' ~ m.usawp_valid_until) }}{% else %}{{ st('ok', 'expires ' ~ m.usawp_valid_until) }}{% endif %}{% endmacro %}
{% macro expiry_kind(m) %}{% set left = days_left(m.usawp_valid_until) %}{% if not m.usawp_valid_until %}bad{% elif left < 0 %}bad{% elif left <= EXPIRING_DAYS %}warn{% else %}ok{% endif %}{% endmacro %}
{% macro expiry_text(m) %}{% if not m.usawp_valid_until %}missing{% else %}expires {{ m.usawp_valid_until }}{% endif %}{% endmacro %}
{% macro titledot(kind, title) %}<span class=rowtitle><span class="dot{% if kind %} {{ kind }}{% endif %}" aria-hidden=true></span>{{ title }}</span>{% endmacro %}
{% macro memhead(m) %}<div class=sechead id=membership><div class=seclabel>Water Polo Membership</div>{% if m.usawp_verified_at %}<div class=verifiedwhen>Verified {{ m.usawp_verified_at[:10] }}</div>{% endif %}</div>{% endmacro %}
{% macro membership_section(m, vr_pending) %}{% set cl = clearance(m) %}{% set dl = days_left(m.usawp_valid_until) %}{% set tw = trial_window(m) %}{% set ex = expiry_notes(m, cl) %}{% set cc = coach_clearance(m) %}{% set left = days_left(m.usawp_valid_until) %}{% set locked = m.usawp_status == 'verified' and not (left is not none and left < 0) %}{% set on_trial = tw and tw.active and not ex.membership and m.usawp_status != 'verified' and not vr_pending %}
{{ memhead(m) }}
<div class=list>
<div class="li prow">{{ titledot('warn' if on_trial else expiry_kind(m)|trim, 'USAWP #' ~ (m.usawp_number or '—')) }}<span class=v>{% if on_trial %}{{ trial_badge(tw) }}{% else %}{{ expiry_text(m)|trim }}{% endif %}</span></div>
{% if not locked %}<div class="li prow editonly"><label class=prefedit style="width:100%;margin:0">USAWP number<input form=profileForm id=usawpNumber name=usawp_number inputmode=numeric autocomplete=off value="{{ m.usawp_number or '' }}" data-original="{{ m.usawp_number or '' }}"></label></div>{% endif %}
{% for it in cl.checks %}{% set sk = {'ok':'ok','no date':'warn'}.get(it.status,'bad') %}{% set side = (('expires ' ~ it.mr.expires_on) if it.mr and it.mr.expires_on else ('done ' ~ it.mr.completed_on) if it.mr and it.mr.completed_on else 'missing') if it.status != 'expired' else 'expired' %}<div class="li prow">{{ titledot(sk, it.req.name) }}<span class=v>{{ side }}</span></div>{% endfor %}
{% if background_view(m) %}{% set bg = background_view(m) %}<div class="li prow">{{ titledot(bg.kind, 'Background screening') }}<span class=v>{{ ('expires ' ~ bg.date) if bg.date else 'missing' }}</span></div>{% endif %}
{% if cc %}<div class="li prow">{{ titledot('ok' if cc.ok else 'bad', 'Coaching') }}<span class=v>{{ 'cleared' if cc.ok else cc.text }}</span></div>{% elif coach_eligibility(m).text %}{% set ce = coach_eligibility(m) %}<div class="li prow">{{ titledot('ok' if ce.eligible else 'bad', 'Coaching') }}<span class=v>{{ ce.text }}</span></div>{% endif %}
</div>
{% if tw and tw.expired and not ex.membership and m.usawp_status != 'verified' and not vr_pending %}<p class="sm" style="margin:8px 0 0">Trial ended {{tw.ends}}</p>{% endif %}
{% if not cl.ok %}{% if not vr_pending %}{% for line in ex.lines %}<p class="sm" style="margin:8px 0 0">{{line}}</p>{% endfor %}{% elif ex.safesport %}<p class="sm" style="margin:8px 0 0">SafeSport expired {{ex.safesport}}</p>{% endif %}
{% if ex.rest %}<p class="t2 sm" style="margin:8px 0 0">Needs: {{ex.rest|join(', ')}}</p>{% endif %}{% endif %}
{% if m.usawp_status=='verified' and dl is not none and dl <= EXPIRING_DAYS %}<p class="sm" style="margin:8px 0 0"><span class="st st-warn"></span> Your membership expires in <b>{{dl}} days</b> ({{m.usawp_valid_until}}). <a href=https://usawp.sport80.com>Renew</a></p>{% endif %}
{% if m.usawp_status != 'verified' %}<p class="t2 sm" style="margin:8px 0 0">Register or renew at <a href=https://usawp.sport80.com>usawp.sport80.com</a> with {{m.email}} and choose Grunions as your club.</p>{% endif %}
{% if ex.membership and not vr_pending %}
<button type=button class="btn btn-primary full" id=reverifyOpen style="margin-top:14px">Reverify membership</button>
<form id=reverifyForm hidden method=post action=/home style="margin-top:14px">{{csrf_field()}}
<div class=row style="align-items:flex-end"><label style="margin:0">USAWP Membership #<input name=usawp_number inputmode=numeric value="{{m.usawp_number or ''}}" autocomplete=off></label>
<label style="margin:0">Background screening expires<input name=background_expires type=date value="{{ (background_view(m).date if background_view(m) else '') }}"></label>
<button class="btn btn-primary" style="flex:0 0 auto">Send</button></div></form>
<script>document.getElementById('reverifyOpen').onclick=function(){var f=document.getElementById('reverifyForm');f.hidden=false;this.hidden=true;f.querySelector('input[name=usawp_number]').focus()};</script>
{% elif m.usawp_status == 'verified' %}
{% set bg = background_view(m) %}{% if bg and bg.required and bg.kind == 'bad' and not vr_pending %}
<form method=post action=/home style="margin-top:14px">{{csrf_field()}}<input type=hidden name=action value=reverify_background>
<button class="btn btn-primary full">Reverify background screening</button></form>{% endif %}
{% endif %}
{% endmacro %}
{% macro expiry_slot(m) %}{% set left = days_left(m.usawp_valid_until) %}{% if left is not none and left >= 0 and left <= EXPIRING_DAYS %}<span class="t3 xs">{% if left == 0 %} · expires today{% elif left == 1 %} · expires in 1 day{% else %} · expires in {{ left }} days{% endif %}</span>{% endif %}{% endmacro %}
{% macro hi_membership() %}{% set num = (me().usawp_number or '')|trim %}{% set tw = trial_window(me()) %}{% set on_trial = tw and tw.active and (me().usawp_status or '') != 'verified' %}{% if num %}{% set cl = clearance(me()) %}{% set dl = days_left(me().usawp_valid_until) %}{% set ns = namespace(tone='ok') %}{% if vr_pending or on_trial %}{% set ns.tone = 'warn' %}{% elif not cl.ok %}{% set ns.tone = 'bad' %}{% elif dl is not none and dl <= EXPIRING_DAYS %}{% set ns.tone = 'warn' %}{% else %}{% for it in cl.checks %}{% if it.days_left is not none and it.days_left >= 0 and it.days_left <= EXPIRING_DAYS %}{% set ns.tone = 'warn' %}{% endif %}{% endfor %}{% endif %}<a class="usawpchip{% if ns.tone != 'ok' %} {{ ns.tone }}{% endif %}" href="/profile#membership"><span class="dot {{ ns.tone }}" aria-hidden=true></span>USAWP #{{ num }}</a>{% elif on_trial and not vr_pending %}<a class="usawpchip warn" href="/profile#membership"><span class="dot warn" aria-hidden=true></span>Trial</a>{% endif %}{% endmacro %}
{% macro member_status(r) %}{% set cl = clearance(r) %}{% set dl = days_left(r.usawp_valid_until) %}{% set tw = trial_window(r) %}{% set ex = expiry_notes(r, cl) %}
{% if tw and tw.active and r.usawp_status != 'verified' and not ex.membership %}{{ st('warn', trial_badge(tw)) }}{% elif not cl.ok %}{{ st('bad','Not cleared') }}{% elif dl is not none and dl <= EXPIRING_DAYS %}{{ st('warn','Expiring soon') }}{% else %}{{ st('ok','Cleared') }}{% endif %}
{% if tw and tw.expired and r.usawp_status != 'verified' %}<div class="xs">Trial ended {{tw.ends}}</div>{% endif %}{{ expiry_slot(r) }}{% endmacro %}
{% macro status_dot(s) %}{% set kind = {'verified':'ok','expired':'bad','pending':'warn'}.get(s, '') %}<span class="dot{% if kind %} {{kind}}{% endif %}" aria-hidden=true></span>{% endmacro %}
{% macro checkin_status(r) %}{% set cl = clearance(r) %}{% set dl = days_left(r.usawp_valid_until) %}{% set tw = trial_window(r) %}{% set ex = expiry_notes(r, cl) %}
{% if tw and tw.active and r.usawp_status != 'verified' and not ex.membership %}{{ st('warn', trial_badge(tw)) }}{% elif tw and tw.expired and r.usawp_status != 'verified' %}{{ st('bad', 'Trial ended') }}{% elif not cl.ok %}{{ st('bad','Not cleared') }}{% elif dl is not none and dl <= EXPIRING_DAYS %}{{ st('warn','Expiring soon') }}{% else %}{{ st('ok','Cleared') }}{% endif %}{% if not (tw and tw.active and r.usawp_status != 'verified' and not ex.membership) %}{{ expiry_slot(r) }}{% endif %}{% endmacro %}
{% macro detail_hiddens(r) %}{{csrf_field()}}<input type=hidden name=member_id value={{r.id}}><input type=hidden name=date value="{{date}}"><input type=hidden name=q value="{{q}}">{% if view is defined %}<input type=hidden name=list_view value="{{ view }}">{% endif %}{% if coach_filter is defined %}<input type=hidden name=list_coach value="{{'eligible' if coach_filter else ''}}"><input type=hidden name=list_referee value="{{'eligible' if referee_filter else ''}}">{% endif %}{% endmacro %}
{% macro cred_side(iso) %}{% if iso %}<span class=cred><span class="dot {{ date_dot(iso) }}" aria-hidden=true></span>{{ fmt_long(iso) }}</span>{% else %}<span class=t3>Not on file</span>{% endif %}{% endmacro %}
{% macro date_field(label, name, value) %}<label class="datefield{% if not value %} empty{% endif %}">{{ label }}<input type=date name={{ name }} value="{{ value or '' }}"><span class=dateph>Not on file · add date</span></label>{% endmacro %}
{% macro glyph_clock() %}<svg class=nxglyph viewBox="0 0 48 48" aria-hidden=true><g fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="3"><path d="M3 24a21 21 0 1 0 42 0a21 21 0 1 0-42 0"/><path d="M9 24a15 15 0 1 0 30 0a15 15 0 1 0-30 0"/><path d="M24 15v9l6 6"/></g></svg>{% endmacro %}
{% macro glyph_pin() %}<svg class=nxglyph viewBox="0 0 48 48" aria-hidden=true><g fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="3"><path d="M42 21c0 12.919-13.35 22.128-17.056 24.436a1.77 1.77 0 0 1-1.888 0C19.351 43.128 6 33.919 6 21c0-9.941 8.059-18 18-18s18 8.059 18 18"/><path d="M32 21a8 8 0 1 1-16 0a8 8 0 0 1 16 0"/></g></svg>{% endmacro %}
{% macro glyph_people() %}<svg class=nxglyph viewBox="0 0 48 48" aria-hidden=true><g fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="3"><path d="M12.527 7c.551-2.024 2.29-3.486 4.473-3.643C19.556 3.173 23.335 3 28.5 3c5.133 0 8.897.171 11.452.354c2.558.182 4.512 2.136 4.694 4.694c.183 2.555.354 6.32.354 11.452c0 5.165-.173 8.944-.357 11.5c-.157 2.183-1.62 3.922-3.643 4.473"/><path d="M35.646 17.047c-.182-2.557-2.136-4.51-4.694-4.693C28.397 12.17 24.632 12 19.5 12c-5.133 0-8.897.171-11.452.354c-2.558.182-4.512 2.136-4.694 4.694C3.17 19.602 3 23.367 3 28.5s.171 8.897.354 11.453c.182 2.557 2.136 4.51 4.694 4.693c2.555.183 6.32.354 11.452.354c5.133 0 8.897-.171 11.452-.354c2.558-.182 4.512-2.136 4.694-4.694c.183-2.555.354-6.32.354-11.452c0-5.133-.171-8.897-.354-11.453"/><path d="M24.026 30.727a7 7 0 1 0-8.066-.01c-2.496.933-4.485 2.709-5.5 4.92c-.646 1.405.16 3.087 1.704 3.18l.044.003a150 150 0 0 0 7.77.18c3.309 0 5.874-.081 7.77-.18l.045-.003c1.543-.093 2.35-1.775 1.704-3.18c-1.012-2.203-2.989-3.974-5.471-4.91"/></g></svg>{% endmacro %}
{% macro social_icon() %}<span class=nxicon aria-hidden=true><svg width="32" height="32" viewBox="0 0 48 48" aria-hidden=true><g fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="3"><path d="M35 21h2.42c2.83 0 5.255 1.988 5.452 4.81a53 53 0 0 1 0 7.38C42.675 36.012 40.251 38 37.42 38H35m-5-17a7 7 0 1 0-2.276-13.622A9 9 0 0 0 20 3a9 9 0 0 0-7.724 4.378A7 7 0 1 0 10 21h.002c.005 1.065.018 1.99.034 2.784C10.087 26.112 11.671 28 14 28s3.915-1.888 3.963-4.216c.018-.85.031-1.625.036-2.784z"/><path d="M34.71 19.179c.163 2.297.29 5.48.29 9.821c0 3.287-.109 5.909-.268 7.986c-.358 4.67-3.893 7.735-8.575 7.91c-1.685.063-3.719.104-6.157.104s-4.472-.041-6.157-.104c-4.682-.175-8.216-3.24-8.575-7.91C5.11 34.909 5 32.286 5 29c0-4.342.127-7.524.29-9.821"/></g></svg></span>{% endmacro %}
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
<button class="btn btn-primary full" name=action value=social>Save</button></form></div></dialog>
<dialog class=modal id=message{{ p.id }}><div class=sheet><h2 style="margin:0 0 12px">Coach message</h2>
<form method=post action="/practices/{{ p.id }}">{{ csrf_field() }}<input type=hidden name=pid value={{ p.id }}><input type=hidden name=back value="{{ back }}">
{{ message_fields(p) }}
<button class="btn btn-primary full" name=action value=message>Save</button></form></div></dialog>
<dialog class=modal id=image{{ p.id }}><div class=sheet><h2 style="margin:0 0 12px">Practice image</h2>
<form method=post action="/practices/{{ p.id }}" enctype=multipart/form-data>{{ csrf_field() }}<input type=hidden name=pid value={{ p.id }}><input type=hidden name=back value="{{ back }}">
<label>Image<input type=file name=image accept="image/jpeg,image/png,image/gif,image/webp,image/heic,image/heif,.heic"></label>
{% if p.image %}<label><input type=checkbox name=image_clear value=1> Remove image</label>{% endif %}
<p class="t3 sm">Shown on the Home card only. Leave the file empty to keep the current picture.</p>
<button class="btn btn-primary full" name=action value=image>Save</button></form></div></dialog>
{% endmacro %}
{% macro practice_host_more(p, back) %}
<span class=more><button type=button class=morebtn aria-label="More for {{ fmt_d(p.date) }}" aria-haspopup=menu aria-expanded=false><svg width="22" height="22" viewBox="0 0 48 48" aria-hidden=true><g fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="3"><path d="M3 24a21 21 0 1 0 42 0a21 21 0 1 0-42 0"/><path d="M20.5 24a3.5 3.5 0 1 0 7 0a3.5 3.5 0 1 0-7 0m-12 0a3.5 3.5 0 1 0 7 0a3.5 3.5 0 1 0-7 0m24 0a3.5 3.5 0 1 0 7 0a3.5 3.5 0 1 0-7 0"/></g></svg></button>
<div class=menu hidden role=menu>
<button type=button data-open="social{{ p.id }}">After-practice social</button>
<button type=button data-open="message{{ p.id }}">Coach message</button>
<button type=button data-open="image{{ p.id }}">Practice image</button>
</div></span>
{{ practice_extra_dialogs(p, back) }}
{% endmacro %}
{% macro practice_more(p, coach_ids, back) %}
<span class=more><button type=button class=morebtn aria-label="More for {{ fmt_d(p.date) }}" aria-haspopup=menu aria-expanded=false><svg width="22" height="22" viewBox="0 0 48 48" aria-hidden=true><g fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="3"><path d="M3 24a21 21 0 1 0 42 0a21 21 0 1 0-42 0"/><path d="M20.5 24a3.5 3.5 0 1 0 7 0a3.5 3.5 0 1 0-7 0m-12 0a3.5 3.5 0 1 0 7 0a3.5 3.5 0 1 0-7 0m24 0a3.5 3.5 0 1 0 7 0a3.5 3.5 0 1 0-7 0"/></g></svg></button>
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
<div class=row><button class="btn btn-primary" name=action value=assign>Save</button><button type=button class="btn btn-secondary" onclick="this.closest('dialog').close()">Cancel</button></div></form></div></dialog>
<dialog class=modal id=cancel{{ p.id }}><div class=sheet><h2 style="margin:0 0 8px">Send cancellation</h2>
<p class="t2 sm">Members get an email and a push that include this reason.</p>
<form method=post action="/practices/{{ p.id }}">{{ csrf_field() }}<input type=hidden name=pid value={{ p.id }}><input type=hidden name=back value="{{ back }}">
<label>Reason<textarea name=reason required></textarea></label>
<button class="btn btn-danger full" name=action value=cancel>Confirm</button></form></div></dialog>
<dialog class=modal id=delete{{ p.id }}><div class=sheet><h2 style="margin:0 0 8px">Delete this practice?</h2>
<p class="t2 sm">{{ fmt_d(p.date) }}, {{ fmt_t(p.start) }}–{{ fmt_t(p.end) }} at {{ p.location }}.</p>
<form method=post action="/practices/{{ p.id }}">{{ csrf_field() }}<input type=hidden name=pid value={{ p.id }}>
<div class=row><button class="btn btn-danger" name=action value=delete>Delete practice</button><button type=button class="btn btn-secondary" onclick="this.closest('dialog').close()">Cancel</button></div></form></div></dialog>
{% endmacro %}
{% if tab == 'profile' and me() %}<header class=profilebar>
<div class=left><button type=button class="profileback viewonly" id=profileBack aria-label="Back"><svg width="22" height="22" viewBox="0 0 24 24" aria-hidden="true"><path d="M15 6 9 12l6 6" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg></button><button type=button class="profileact editonly" id=profileCancel>Cancel</button></div>
<h1>Profile</h1>
<div class=right><button type=button class="profileact viewonly" id=profileEdit>Edit</button><button type=submit class="profileact savebtn editonly" id=profileSave form=profileForm>Save</button></div>
</header>{% elif me() and tab == 'member' %}<header class=profilebar>
<div class=left><button type=button class="profileback viewonly" id=profileBack aria-label="Back"><svg width="22" height="22" viewBox="0 0 24 24" aria-hidden="true"><path d="M15 6 9 12l6 6" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg></button>{% if me().is_admin %}<button type=button class="profileact editonly" id=profileCancel>Cancel</button>{% endif %}</div>
<h1>{{ display_first(m) }} {{ m.last }}</h1>
<div class=right>{% if me().is_admin %}<button type=button class="profileact viewonly" id=profileEdit>Edit</button><button type=submit class="profileact savebtn editonly" id=profileSave form=memberForm name=action value=edit>Save</button>{% endif %}</div>
</header>{% elif me() and tab == 'lineup_edit' %}<header class=profilebar><div class=left><a class=profileact href=/lineup>Cancel</a></div><h1>Event</h1><div class=right><button type=submit class="profileact savebtn" form=eventForm name=action value=save>{{ save_label or 'Save' }}</button></div></header>{% elif me() and tab == 'lineup_event' %}<header class=profilebar><div class=left><a class=profileback href=/lineup aria-label="Back"><svg width="22" height="22" viewBox="0 0 24 24" aria-hidden="true"><path d="M15 6 9 12l6 6" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg></a></div><h1>Event</h1><div class=right>{% if e.can_edit %}<a class=profileact href="/lineup/{{ e.id }}/edit">Edit</a>{% endif %}</div></header>{% elif me() and tab == 'series_edit' %}<header class=profilebar><div class=left><a class=profileact href=/practices>Cancel</a></div><h1>Series</h1><div class=right><button type=submit class="profileact savebtn" form=seriesForm>Save</button></div></header>{% elif me() and tab == 'practice' %}<header class=profilebar><div class=left>{% if editing or plan_editing %}<a class=profileact href="/practices/{{ x.p.id }}{% if from_admin %}?from=admin{% endif %}">Cancel</a>{% else %}<a class=profileback href="{% if from_admin %}/admin?date={{ x.p.date }}{% else %}/practices{% endif %}" aria-label="Back"><svg width="22" height="22" viewBox="0 0 24 24" aria-hidden="true"><path d="M15 6 9 12l6 6" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg></a>{% endif %}</div><h1>Practice</h1><div class=right>{% if editing %}<button type=submit class="profileact savebtn" form=practiceForm name=action value=edit>Save</button>{% elif plan_editing %}<button type=submit class="profileact savebtn" form=practiceForm name=action value=plan>Save</button>{% elif me().is_admin or is_staff() %}<a class=profileact href="/practices/{{ x.p.id }}?edit=1{% if from_admin %}&amp;from=admin{% endif %}">Edit</a>{% endif %}</div></header>{% elif me() %}<header class="homehead{% if tab=='home' or tab=='practices' %} homefade{% endif %}"{% if tab=='home' or tab=='practices' %} data-entry="{{ 'schedule' if tab=='practices' else 'home' }}"{% endif %}><div class=headmain>{% if tab == 'home' or tab == 'practices' %}<div class=titlestack><div class=titlecross><h1 class=hititle>Hi, {{ display_first(me()) }}</h1><h1 class=schedtitle aria-hidden=true>Schedule</h1></div>{{ hi_membership() }}</div>{% elif tab == 'chat' and is_staff() %}<div class="seg headtabs" role=tablist><a href=/chat class="chip{{' chip-active on' if ch=='team'}}" data-badge=team>Team{{ bubble(badges().team) }}</a><a href="/chat?c=coaches" class="chip{{' chip-active on' if ch=='coaches'}}" data-badge=coaches>Coaches{{ bubble(badges().coaches) }}</a></div>{% elif tab == 'chat' %}<h1>Team</h1>{% elif tab == 'admin' %}<div class="admintabs noprint headtabs" role=tablist>{% set ep = request.endpoint %}{% if is_staff() %}<a href=/admin class="chip{{' chip-active on' if ep=='admin'}}">Schedule</a>{% endif %}{% if can_host_practice() %}<a href=/admin/approvals class="chip{{' chip-active on' if ep=='approvals'}}">Approvals ({{ approval_count() }})</a>{% endif %}{% if me().is_admin %}<a href=/members class="chip{{' chip-active on' if ep=='members'}}">People</a><a href=/expiring class="chip{{' chip-active on' if ep=='expiring'}}">Expiring</a><a href=/transfer class="chip{{' chip-active on' if ep=='transfer_page'}}">Transfer</a><a href=/requirements class="chip{{' chip-active on' if ep=='requirements_page'}}">Rules</a><a href=/qr class="chip{{' chip-active on' if ep=='qr_page'}}">QR</a>{% endif %}</div>{% elif tab == 'lineup' %}<h1>Lineup</h1>{% elif tab == 'notifications' %}<h1>Notifications</h1>{% else %}<h1>{{ display_first(me()) }}</h1>{% endif %}</div><a class=avatar href=/profile aria-label="Profile">{% if me().photo %}<img src="/avatar/{{ me().id }}?v={{ me().photo }}" alt="" width="44" height="44">{% else %}{{ initials(me()) }}{% endif %}</a></header>{% else %}<header><a class=brand href=/>Grunions</a></header>{% endif %}<main>
{% for cat, msg in get_flashed_messages(with_categories=true) %}{% if cat == 'toast' %}<div class="toast noprint" role=status>{{msg}}</div>{% else %}<div class=note>{{msg|safe}}</div>{% endif %}{% endfor %}
<script>document.querySelectorAll('.toast').forEach(function(t){setTimeout(function(){t.remove()},3000)})</script>
{% macro push_card() %}<div class=card id=pushCard hidden>
<div style="font-weight:600">Notifications</div>
<p class="t2 sm" id=iosPushHint hidden>On iPhone or iPad, add Grunions to your Home Screen to get notifications. Tap Share, then Add to Home Screen, and open the app from there (iOS 16.4 or later).</p>
<p class="t2 sm">Allow notifications for chat, practice reminders, and membership expiry. This works on Android, and on iPhone once Grunions is on your Home Screen (iOS 16.4 or later).</p>
<p class="t2 sm" id=pushDenied hidden>Notifications are blocked in this browser. Allow them in the site settings, then come back.</p>
<button type=button class="btn btn-primary full" id=allowPush>Allow notifications</button>
<p class="t3 sm" style="margin:10px 0 0"><a href=/notifications>Notification settings</a></p>
</div>{% endmacro %}"""

ICONS = {
 "home": '<svg width="24" height="24" viewBox="0 0 48 48" aria-hidden=true><path fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M26.815 4.16c7.235 3.211 12.719 7.43 15.554 9.867c1.433 1.232 2.232 3.005 2.33 4.892C44.836 21.51 45 25.565 45 30c0 3.412-.097 6.706-.204 9.293a5.69 5.69 0 0 1-5.512 5.47c-3.46.12-8.595.237-15.284.237s-11.823-.118-15.284-.236a5.69 5.69 0 0 1-5.512-5.47A230 230 0 0 1 3 30c0-4.435.165-8.49.3-11.081c.1-1.887.898-3.66 2.331-4.892c2.835-2.438 8.32-6.656 15.554-9.867a6.94 6.94 0 0 1 5.63 0M16 38h16"/></svg>',
 "cal": '<svg width="24" height="24" viewBox="0 0 48 48" aria-hidden=true><g fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="3"><path d="M22 25h4m6 0h4m-20 0h-4m10 10h4m6 0h4m-20 0h-4m-.997-26.437c-1.137.11-2.12.225-2.952.336c-2.199.293-3.877 1.948-4.192 4.144C3.451 15.887 3 20.41 3 26.5s.451 10.614.859 13.458c.315 2.196 1.993 3.85 4.192 4.144c3.13.417 8.38.898 15.949.898s12.818-.48 15.949-.898c2.199-.293 3.877-1.948 4.192-4.144c.408-2.844.859-7.368.859-13.458s-.451-10.613-.859-13.457c-.315-2.196-1.993-3.851-4.192-4.144a82 82 0 0 0-2.952-.336M29 8.074A164 164 0 0 0 24 8q-2.693.002-5 .074"/><path d="M29.013 9.27c.043 2.08 1.409 3.694 3.489 3.726a33 33 0 0 0 .996 0c2.08-.032 3.446-1.646 3.489-3.726a61 61 0 0 0 0-2.54c-.043-2.08-1.409-3.694-3.489-3.726a32 32 0 0 0-.996 0c-2.08.032-3.446 1.646-3.489 3.726a61 61 0 0 0 0 2.54m-18 0c.043 2.08 1.409 3.694 3.489 3.726a33 33 0 0 0 .996 0c2.08-.032 3.446-1.646 3.489-3.726a61 61 0 0 0 0-2.54c-.043-2.08-1.409-3.694-3.489-3.726a32 32 0 0 0-.996 0c-2.08.032-3.446 1.646-3.489 3.726a61 61 0 0 0 0 2.54"/></g></svg>',
 "lineup": '<svg width="24" height="24" viewBox="0 0 48 48" aria-hidden=true><g fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="3"><path d="M38.872 15.507c-.351-.98-1.549-3.567-5.268-7.213c-3.941-3.864-6.67-4.952-7.52-5.218A162 162 0 0 0 21 3c-6.264 0-10.566.32-13.248.627c-2.201.252-3.85 1.903-4.092 4.105C3.34 10.622 3 15.473 3 23s.341 12.378.66 15.268c.242 2.202 1.891 3.853 4.092 4.105c1.898.217 4.607.44 8.248.553"/><path d="M38.886 15.958c-2.087.311-5.841.072-8.69-.191a4.664 4.664 0 0 1-4.229-4.211c-.268-2.802-.506-6.466-.18-8.488M41 34.258s-.473-2.108-3.312-4.946C34.85 26.473 32.742 26 32.742 26M10 13l4 4l5-7m-9 14l4 4l5-7"/><path d="M43.665 31.592c1.454-1.453 2.01-3.577.794-5.235a18 18 0 0 0-1.77-2.046c-.74-.74-1.43-1.318-2.047-1.77c-1.657-1.216-3.781-.66-5.235.793l-12.34 12.34c-.543.544-.915 1.233-.979 2c-.087 1.041-.151 2.81.017 5.428a1.92 1.92 0 0 0 1.793 1.793c2.617.168 4.387.104 5.428.016c.766-.064 1.456-.435 2-.98z"/></g></svg>',
 "chat": '<svg width="24" height="24" viewBox="0 0 48 48" aria-hidden=true><g fill="none" stroke="currentColor" stroke-linejoin="round" stroke-width="3"><path stroke-linecap="round" d="M42.6 19C40.747 9.871 32.676 3 23 3C11.954 3 3 11.954 3 23c0 3.796 1.058 7.345 2.894 10.369c-.891 2.137-1.798 4.663-2.378 6.985c-.325 1.303.818 2.401 2.112 2.042c2.243-.623 4.711-1.53 6.838-2.392A19.9 19.9 0 0 0 19 42.6"/><path d="M21 33c0-6.627 5.373-12 12-12s12 5.373 12 12c0 2.303-.648 4.454-1.773 6.28c.431.912.86 1.961 1.2 3.086c.387 1.286-.765 2.391-2.041 1.974a29 29 0 0 1-2.994-1.182A11.94 11.94 0 0 1 33 45c-6.627 0-12-5.373-12-12Z"/></g></svg>',
 "admin": '<svg width="24" height="24" viewBox="0 0 48 48" aria-hidden=true><g fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="3"><path d="M29.14 42.987c5.119-.063 8.743-.344 11.108-.614c2.2-.252 3.85-1.903 4.092-4.105c.319-2.89.66-7.741.66-15.268c0-2.876-.05-5.361-.13-7.496c-.351-.982-1.55-3.568-5.266-7.21c-3.941-3.864-6.67-4.952-7.519-5.217A162 162 0 0 0 27 3c-6.264 0-10.566.32-13.248.627c-2.201.252-3.85 1.903-4.092 4.105c-.225 2.034-.46 5.04-.58 9.268"/><path d="M44.884 15.96c-2.087.31-5.84.072-8.688-.192a4.664 4.664 0 0 1-4.228-4.21c-.269-2.803-.507-6.468-.181-8.489M3 33a12 12 0 1 0 24 0a12 12 0 1 0-24 0"/><path d="m20 29l-5.882 8L10 32.333"/></g></svg>',
}
TABS = ("""</main>{% if me() and tab != 'profile' and tab != 'member' %}<nav class="tabs noprint" data-total="{{ badges().total }}">
<a href=/home class="{{'on' if tab=='home' or tab=='practices' or tab=='practice' or tab=='series_edit'}}" data-badge=schedule>""" + ICONS["home"] + """Home{{ bubble(badges().schedule) }}</a>
<a href=/lineup class="{{'on' if tab=='lineup' or tab=='lineup_edit' or tab=='lineup_event'}}">""" + ICONS["lineup"] + """Lineup</a>
<a href=/chat class="{{'on' if tab=='chat'}}" data-badge=chat>""" + ICONS["chat"] + """Chat{{ bubble(badges().chat) }}</a>
{% if is_staff() %}<a href=/admin class="{{'on' if tab=='admin'}}">""" + ICONS["admin"] + """Admin</a>{% elif me().is_admin %}<a href=/members class="{{'on' if tab=='admin'}}">""" + ICONS["admin"] + """Admin</a>{% endif %}
</nav>{% endif %}
<script>
if('serviceWorker' in navigator) navigator.serviceWorker.register('/sw.js?v=49');
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
window.grunionsDirections=function(lat,lng){
 var dest=lat+','+lng, apple=/iPhone|iPad|iPod/.test(navigator.userAgent||'');
 var url=apple?('https://maps.apple.com/?daddr='+encodeURIComponent(dest)):('https://www.google.com/maps/dir/?api=1&destination='+encodeURIComponent(dest));
 window.open(url,'_blank','noopener');
};
if(!window.grunionsDirClick){window.grunionsDirClick=1;
 document.addEventListener('click',function(e){
  var a=e.target.closest&&e.target.closest('[data-directions]'); if(!a) return;
  var parts=(a.getAttribute('data-directions')||'').split(',');
  if(parts.length<2||!parts[0]||!parts[1]) return;
  e.preventDefault();
  grunionsDirections(parts[0], parts[1]);
 });
}
window.grunionsMountMap=function(el, opts){
 if(!el) return;
 opts=opts||{};
 function boot(){
  if(!window.L||!el.isConnected||el.dataset.mapon) return;
  var pins=opts.pins||[];
  if(!pins.length) return;
  el.dataset.mapon='1';
  var map=L.map(el,{zoomControl:false,attributionControl:true,dragging:false,touchZoom:false,scrollWheelZoom:false,doubleClickZoom:false,boxZoom:false,keyboard:false});
  var tiles=L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png',{maxZoom:19,attribution:'&copy; OpenStreetMap'}).addTo(map);
  var faded=false; tiles.on('tileload',function(){if(!faded){faded=true;el.classList.add('tiles')}});
  function icon(kind){return L.divIcon({className:'mpin'+(kind==='social'?' social':''),html:'',iconSize:[18,18],iconAnchor:[9,9]});}
  var bounds=[], pool=null;
  pins.forEach(function(p){ if(p.kind==='pool') pool=p; bounds.push([p.lat,p.lng]); });
  if(!pool) pool=pins[0];
  function go(p){ var t=opts.mode==='card'?pool:p; grunionsDirections(t.lat, t.lng); }
  pins.forEach(function(p){
   var m=L.marker([p.lat,p.lng],{icon:icon(p.kind),title:p.label||'Directions',zIndexOffset:p.kind==='pool'?800:0}).addTo(map);
   m.on('click',function(ev){ if(L.DomEvent) L.DomEvent.stopPropagation(ev); go(p); });
  });
  if(opts.mode==='card') map.on('click',function(){ go(pool); });
  function place(){
   if(!el.clientHeight||!pool) return;
   if(opts.mode==='card'){
    if(bounds.length>1) map.fitBounds(bounds,{padding:[24,24],maxZoom:16,animate:false});
    else map.setView([pool.lat, pool.lng], 15, {animate:false});
    return;
   }
   var box=el.getBoundingClientRect();
   var card=document.querySelector('.nextcard');
   var cardTop=card?card.getBoundingClientRect().top:(box.top+box.height*0.62);
   var visTop=Math.max(box.top, 0);
   var visBottom=Math.min(cardTop, box.bottom);
   if(visBottom-visTop<80) visBottom=Math.min(box.bottom, visTop+80);
   var padTop=Math.max(0, visTop-box.top);
   var padBottom=Math.max(0, box.bottom-visBottom);
   var regional=12;
   function frame(z){
    map.setView([pool.lat, pool.lng], z, {animate:false});
    var pt=map.latLngToContainerPoint([pool.lat, pool.lng]);
    var targetX=el.clientWidth/2;
    var targetY=padTop+(el.clientHeight-padTop-padBottom)/3;
    map.panBy([pt.x-targetX, pt.y-targetY], {animate:false});
   }
   function fits(){
    var pad=24;
    var topLimit=padTop+pad, botLimit=el.clientHeight-padBottom-pad;
    for(var i=0;i<bounds.length;i++){
     var q=map.latLngToContainerPoint(bounds[i]);
     if(q.x<pad||q.y<topLimit||q.x>el.clientWidth-pad||q.y>botLimit) return false;
    }
    return true;
   }
   var z=regional;
   frame(z);
   if(bounds.length>1){ while(z>8 && !fits()){ z-=1; frame(z); } }
  }
  window.grunionsPlaceMap=place;
  setTimeout(function(){map.invalidateSize();place();},0);
  setTimeout(function(){map.invalidateSize();place();},250);
  function onResize(){if(!el.isConnected){window.removeEventListener('resize',onResize);return;}map.invalidateSize();place();}
  window.addEventListener('resize',onResize);
 }
 if(window.L) boot();
 else {
  var s=document.querySelector('script[data-leaflet]');
  if(!s){ s=document.createElement('script'); s.src='/static/leaflet/leaflet.js'; s.setAttribute('data-leaflet','1'); s.onload=boot; document.body.appendChild(s); }
  else s.addEventListener('load', boot);
 }
};
function grunionsPinHead(){
 var h=document.querySelector('header.homehead');
 var sticky=h && !document.body.classList.contains('homefull');
 document.documentElement.style.setProperty('--headh', sticky ? (h.offsetHeight+'px') : '0px');
}
window.grunionsPinHead=grunionsPinHead;
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
 var nextHead=doc.querySelector('header'), curHead=document.querySelector('header');
 if(nextHead&&curHead&&curHead.outerHTML!==nextHead.outerHTML) curHead.replaceWith(nextHead);
 else if(nextHead&&!curHead) document.body.insertBefore(nextHead, document.querySelector('main'));
 document.title=doc.title||document.title;
 if(doc.body) document.body.className=doc.body.className;
 if(!pop) history.pushState({grunions:1},'',url);
 grunionsRunScripts(scripts);
 if(window.grunionsPinHead) grunionsPinHead();
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
 try{var adminLast=localStorage.getItem('grunionsAdminTab');var adminLink=document.querySelector('nav.tabs a[href="/admin"], nav.tabs a[href="/members"]');
  if(adminLink&&adminLast&&['/admin','/members','/expiring','/transfer','/requirements','/qr'].indexOf(adminLast)>=0) adminLink.setAttribute('href', adminLast);}catch(e){}
 history.scrollRestoration='manual';
 history.replaceState({grunions:1},'',location.href);
 document.addEventListener('click',function(e){
  if(e.defaultPrevented||e.button||e.metaKey||e.ctrlKey||e.shiftKey||e.altKey) return;
  var a=e.target.closest&&e.target.closest('a'); if(!a||!a.href||a.hasAttribute('download')) return;
  if(a.target&&a.target!=='_self') return;
  var abs; try{abs=new URL(a.href,location.href);}catch(err){return;}
  if(abs.origin!==location.origin) return;
  if(/^\\/(logout|login|join|profile|admin\\/member|auth\\/|static\\/|api\\/)/.test(abs.pathname)) return;
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
window.grunionsOpenSheet=function(d){
 if(!d||d.classList.contains('closing')) return;
 var panel=d.querySelector('.sheet');
 d.classList.remove('closing'); d.classList.add('opening');
 if(panel){panel.style.transition='none';panel.style.transform='translateY(110%)'}
 if(!d.open) d.showModal();
 requestAnimationFrame(function(){requestAnimationFrame(function(){
  d.classList.remove('opening');
  if(panel){panel.style.transition='transform .25s ease-out';panel.style.transform='translateY(0)'}
 })});
};
window.grunionsCloseSheet=function(d){
 if(!d||!d.open||d.classList.contains('closing')) return;
 d.classList.add('closing');
 var panel=d.querySelector('.sheet');
 if(panel){panel.style.transition='transform .25s ease-out';panel.style.transform='translateY(110%)'}
 setTimeout(function(){d.classList.remove('closing');if(panel){panel.style.transition='';panel.style.transform=''}if(d.open)d.close()},250);
};
if(!window.grunionsSheetDrag){window.grunionsSheetDrag=1;
 document.addEventListener('pointerdown',function(e){
  var grab=e.target.closest&&e.target.closest('dialog.botsheet .grab'); if(!grab||e.button) return;
  var d=grab.closest('dialog'), panel=d.querySelector('.sheet'); if(!panel) return;
  var y0=e.clientY, dy=0, drag=true;
  panel.style.transition='none';
  grab.setPointerCapture&&grab.setPointerCapture(e.pointerId);
  function move(ev){if(!drag)return;dy=Math.max(0,ev.clientY-y0);panel.style.transform='translateY('+dy+'px)'}
  function end(){if(!drag)return;drag=false;grab.removeEventListener('pointermove',move);grab.removeEventListener('pointerup',end);grab.removeEventListener('pointercancel',end);
   if(dy>80) grunionsCloseSheet(d); else {panel.style.transition='transform .25s ease-out';panel.style.transform='translateY(0)'}}
  grab.addEventListener('pointermove',move); grab.addEventListener('pointerup',end); grab.addEventListener('pointercancel',end);
 });
 document.addEventListener('click',function(e){var d=e.target.closest&&e.target.closest('dialog.botsheet'); if(d&&e.target===d) grunionsCloseSheet(d)});
 document.addEventListener('cancel',function(e){var d=e.target; if(d&&d.matches&&d.matches('dialog.botsheet')){e.preventDefault();grunionsCloseSheet(d)}},true);
}
document.addEventListener('click',function(e){
 var b=e.target.closest&&e.target.closest('[data-member-edit]'); if(!b) return;
 var d=document.getElementById(b.getAttribute('data-member-edit')); if(!d||!d.showModal) return;
 e.preventDefault(); grunionsOpenSheet(d);
 var sheet=d.querySelector('.sheet'), sec=b.getAttribute('data-focus');
 var el=sec?d.querySelector('[data-section="'+sec+'"]'):null;
 if(sheet) sheet.scrollTop=0;
 if(el&&sheet){var top=el.getBoundingClientRect().top-sheet.getBoundingClientRect().top+sheet.scrollTop; sheet.scrollTop=Math.max(0,top-12);}
});
document.addEventListener('change',function(e){var t=e.target; if(t&&t.matches&&t.matches('.datefield input[type=date]')) t.closest('.datefield').classList.toggle('empty',!t.value);});
grunionsPinHead();
window.addEventListener('resize', grunionsPinHead);
</script>
<script>var PUSH_CSRF="{{csrf_token()}}",VAPID_PUBLIC="{{vapid_public_key()}}";</script>
</body></html>""")

ADMIN_NAV = """<script>(function(){var key='grunionsAdminTab';document.querySelectorAll('.admintabs a').forEach(function(a){a.addEventListener('click',function(){try{localStorage.setItem(key,a.getAttribute('href'))}catch(e){}})});var on=document.querySelector('.admintabs a.on');if(on&&on.parentNode){var sc=on.parentNode;if(on.offsetLeft+on.offsetWidth>sc.clientWidth+sc.scrollLeft)sc.scrollLeft=Math.max(0,on.offsetLeft-8);}})();</script>
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
<button class="btn btn-primary full">Create account</button></form>
<p class="t3 sm" style="text-align:center;margin-top:20px">Already a member? <a href=/login>Log in</a></p>"""

T["login"] = """<h1>Log in</h1>
{% if google_enabled() %}<a class="btn full" href=/auth/google style="background:var(--surface2);color:var(--t1);border:1px solid var(--line)"><svg width=18 height=18 viewBox="0 0 48 48" aria-hidden=true><path fill="#EA4335" d="M24 9.5c3.5 0 6.6 1.2 9.1 3.6l6.8-6.8C35.8 2.4 30.3 0 24 0 14.6 0 6.6 5.4 2.7 13.3l7.9 6.1C12.5 13.6 17.8 9.5 24 9.5z"/><path fill="#4285F4" d="M46.1 24.5c0-1.6-.1-3.1-.4-4.5H24v9h12.4c-.5 2.9-2.2 5.3-4.6 6.9l7.4 5.7c4.3-4 6.9-9.9 6.9-17.1z"/><path fill="#FBBC05" d="M10.6 28.6c-.5-1.4-.8-3-.8-4.6s.3-3.2.8-4.6l-7.9-6.1C1 16.6 0 20.2 0 24s1 7.4 2.7 10.7l7.9-6.1z"/><path fill="#34A853" d="M24 48c6.5 0 11.9-2.1 15.9-5.8l-7.4-5.7c-2.1 1.4-4.8 2.3-8.5 2.3-6.2 0-11.5-4.1-13.4-9.9l-7.9 6.1C6.6 42.6 14.6 48 24 48z"/></svg>Sign in with Google</a>
<p class="t3 sm" style="text-align:center;margin:16px 0 4px">or</p>{% endif %}<p class=t2>We'll email you a one-time login link.</p>
<form method=post>{{csrf_field()}}<label>Email<input name=email type=email required autocomplete=email></label>
<button class="btn btn-primary full">Send login link</button></form>
<p class="t3 sm" style="text-align:center;margin-top:20px">New here? <a href=/join>Join the team</a></p>"""

T["home"] = """{% if pins %}
<section class=homemap id=homeMap aria-label="Practice map"></section>
<script>
(function(){
 var pins={{ pins|tojson }};
 function start(){ var el=document.getElementById('homeMap'); if(el&&window.grunionsMountMap) grunionsMountMap(el,{pins:pins,mode:'home'}); }
 if(window.grunionsMountMap) start(); else document.addEventListener('DOMContentLoaded', start);
})();
</script>
{% endif %}
<div class=homealerts>{{ push_card() }}
{% for n in notices %}<div class="note notice">{{n.body}}</div>{% endfor %}
{% if ann %}<div class=card><div class="t3 xs">ANNOUNCEMENT · {{display_first(ann)|upper}}</div><p style="margin:6px 0 0">{{ann.body}}</p></div>{% endif %}</div>
<div class=homedock>
{% set cl = clearance(m) %}{% set dl = days_left(m.usawp_valid_until) %}{% set tw = trial_window(m) %}{% set num = (m.usawp_number or '')|trim %}
{% set ns = namespace(tone='ok') %}
{% if vr_pending or (tw and tw.active and (m.usawp_status or '') != 'verified') %}{% set ns.tone = 'warn' %}
{% elif not cl.ok %}{% set ns.tone = 'bad' %}
{% elif dl is not none and dl <= EXPIRING_DAYS %}{% set ns.tone = 'warn' %}
{% else %}{% for it in cl.checks %}{% if it.days_left is not none and it.days_left >= 0 and it.days_left <= EXPIRING_DAYS %}{% set ns.tone = 'warn' %}{% endif %}{% endfor %}{% endif %}
{% if not num %}<div class="card numcard"><div class=nxtitle>Enter your USAWP membership number</div>
<form method=post action=/home style="margin-top:12px">{{csrf_field()}}
<label>USAWP Membership #<input name=usawp_number inputmode=numeric value="" autocomplete=off></label>
<button class="btn btn-primary full">Save</button>
{% if not tw %}<button type=button class="btn btn-secondary full" id=trialOpen style="margin-top:8px">2-week USAWP trial</button>{% endif %}</form>
{% if not tw %}<dialog id=trialDialog class=modal><div class=sheet>
<p>I will complete the USA Water Polo 2-week trial membership before I get in the pool. I understand I need to get a full USAWP membership soon, otherwise I will not be able to practice.</p>
<form method=post action=/home>{{csrf_field()}}<input type=hidden name=action value=trial>
<button class="btn btn-primary full">I confirm</button></form>
<a class="btn full" style="margin-top:10px" href="{{TRIAL_JOIN_URL}}" target=_blank rel=noopener>Get USAWP trial membership</a>
</div></dialog>
<script>document.getElementById('trialOpen').onclick=function(){document.getElementById('trialDialog').showModal()};
document.getElementById('trialDialog').addEventListener('click',function(e){if(e.target===this)this.close()});</script>{% endif %}
</div>{% endif %}
{% if next_kind == 'event' and nextev %}<div class="card tap nextcard" onclick="if(event.target.closest('button,a,form,input,select,textarea,label'))return;location.href='/lineup/{{ nextev.id }}'">
<div class=nxbody><div class=nxcardhead><a class=cardlink href="/lineup/{{ nextev.id }}"><div class=nxtitle>{{ nextev.title }}</div></a><span class="chip-info daychip">{{ nextev.chip_label }}</span></div>
<a class=cardlink href="/lineup/{{ nextev.id }}">
<div class=nxrow>{{ glyph_clock() }}<span>{{ nextev.when }}</span></div>
{% if nextev.where %}<div class=nxrow>{{ glyph_pin() }}<span>{{ nextev.where }}</span></div>{% endif %}
<div class=nxrow>{{ glyph_people() }}<span>{{ nextev.count_line }} · {{ nextev.host_line }}</span></div></a></div>
<form method=post action=/lineup class=pills>{{ csrf_field() }}<input type=hidden name=event_id value={{ nextev.id }}><input type=hidden name=back value=/home>
<button class="btn {{ 'btn-primary' if nextev.mine == 'going' else 'btn-secondary' }}" name=action value="{{ 'clear' if nextev.mine == 'going' else 'going' }}">I'm going{% if nextev.mine == 'going' %} ✓{% endif %}</button>
<button class="btn {{ 'btn-primary' if nextev.mine == 'notgoing' else 'btn-secondary' }}" name=action value="{{ 'clear' if nextev.mine == 'notgoing' else 'notgoing' }}">I'm not going{% if nextev.mine == 'notgoing' %} ✓{% endif %}</button></form>
</div>{% elif nextp %}{% set sh = social_home(nextp) %}<div class="card tap nextcard" onclick="if(event.target.closest('button,a,form,input,select,textarea,label'))return;location.href='/practices/{{nextp.id}}'">
{% if nextp.image %}<a class=cardlink href="/practices/{{nextp.id}}"><div class=pimg><img src="/practice-image/{{ nextp.id }}?v={{ nextp.image }}" alt=""><span class="chip-info nxbadge">{% if nextp.date == today %}TODAY{% else %}{{ fmt_d(nextp.date) }}{% endif %}</span></div></a>{% endif %}
<div class=nxbody><div class=nxcardhead><a class=cardlink href="/practices/{{nextp.id}}"><div class=nxtitle>{{ practice_title(nextp) }}</div></a><span class="chip-info daychip">{{ relative_day(nextp.date) }}</span></div>
<a class=cardlink href="/practices/{{nextp.id}}">
<div class=nxrow>{{ glyph_clock() }}<span>{{ fmt_card_date(nextp.date) }} · {{ fmt_clock(nextp.start) }} – {{ fmt_clock(nextp.end) }}</span></div>
<div class=nxrow>{{ glyph_pin() }}<span>{{ short_place(nextp.location) }}</span></div>
<div class=nxrow>{{ glyph_people() }}<span>{{ nextp_n }} going{% if next_coaches %} · Coaches: {{ next_coaches }}{% endif %}</span></div>
{% if nextp.coach_note %}<div class=nxnote>{{ nextp.coach_note }} · {{ nextp.coach_note_by }} · {{ fmt_stamp(nextp.coach_note_at) }}</div>{% endif %}</a></div>
<form method=post action=/practices class=pills>{{csrf_field()}}<input type=hidden name=pid value={{nextp.id}}>
<button class="btn {{ 'btn-primary' if nextp_mine==1 else 'btn-secondary' }}" name=action value="{{ 'clear' if nextp_mine==1 else 'going' }}">I'm going{% if nextp_mine==1 %} ✓{% endif %}</button>
<button class="btn {{ 'btn-primary' if nextp_mine==0 else 'btn-secondary' }}" name=action value="{{ 'clear' if nextp_mine==0 else 'notgoing' }}">I'm not going{% if nextp_mine==0 %} ✓{% endif %}</button></form>
{% if sh %}<div class=nxdiv></div><div class=nxsocial><a class=cardlink href="/practices/{{nextp.id}}" style="display:flex;align-items:center;gap:12px">{{ social_icon() }}
<div class=grow><div class=nxtitle>{{ sh.title }}</div><div class="t2 sm">{{ sh.place }}</div></div></a>
<form method=post action=/practices>{{csrf_field()}}<input type=hidden name=pid value={{nextp.id}}>
<button class="btn {{ 'btn-primary' if next_joined else 'btn-secondary' }}" name=action value="{{ 'social_leave' if next_joined else 'social_join' }}">{% if next_joined %}Joined ✓{% else %}Join{% endif %}</button></form></div>{% endif %}
</div>{% endif %}
</div>
<div class=schedlist id=schedule>
{% for x in data %}{% set p = x.p %}<div class="card tap{% if nextp and p.id == nextp.id %} schedsame{% endif %}" id=p{{p.id}} data-pid={{p.id}} {% if p.cancelled %}style="opacity:.55"{% endif %} onclick="if(event.target.closest('button,a,form,input,select,textarea,label,dialog'))return;location.href='/practices/{{p.id}}'">
<a class=cardlink href="/practices/{{p.id}}">
<div class=nxcardhead><div class=nxtitle>Water Polo Practice</div></div>
<div class=nxmain><div class=datetile><span class=pdate>{% if x.unseen %}<span class=badge data-seen={{p.id}}>{{ x.unseen if x.unseen < 100 else '99+' }}</span>{% endif %}</span><span class=wd>{{ weekday_abbr(p.date) }}</span><span class=dn>{{ day_num(p.date) }}</span><span class=mo>{{ month_abbr(p.date) }}</span></div>
<div class="grow schedrows"><div class=nxrow>{{ glyph_clock() }}<span>{{ fmt_span(p.start, p.end) }}</span></div>
<div class=nxrow>{{ glyph_pin() }}<span>{{ p.location }}</span></div>
<div class=nxrow>{{ glyph_people() }}<span>{{ x.going|length }} going{% if x.coach_names %} · Coaches: {{ x.coach_names|join(', ') }}{% endif %}</span></div></div></div>
{% if p.cancelled %}{{ st('bad','Cancelled') }}{% if p.cancel_reason %}<div class="t3 sm">{{ p.cancel_reason }}</div>{% endif %}{% endif %}
{% if p.note %}<div class=nxnote>{{p.note}}</div>{% endif %}
{% if p.coach_note %}<div class=nxnote>{{ p.coach_note }} · {{ p.coach_note_by }} · {{ fmt_stamp(p.coach_note_at) }}</div>{% endif %}</a>
{% if not p.cancelled %}<form method=post action=/practices class=pills>{{csrf_field()}}<input type=hidden name=pid value={{p.id}}>
<button class="btn {{ 'btn-primary' if x.mine == 1 else 'btn-secondary' }}" name=action value="{{ 'clear' if x.mine==1 else 'going' }}">I'm going{% if x.mine==1 %} ✓{% endif %}</button>
<button class="btn {{ 'btn-primary' if x.mine == 0 else 'btn-secondary' }}" name=action value="{{ 'clear' if x.mine==0 else 'notgoing' }}">I'm not going{% if x.mine==0 %} ✓{% endif %}</button></form>
{% endif %}</div>{% endfor %}
{% if me().is_admin %}<details class=card><summary>Add a practice</summary><form method=post class=body>{{csrf_field()}}<label>Date<input type=date name=date required></label>
<div class=row><label>Start<input type=time name=start value=19:00></label><label>End<input type=time name=end value=20:30></label></div>
<label>Location<input name=location required></label><label>Note<input name=note></label>
<div class=repeatblock><label class=repeatline><input type=checkbox name=repeat value=1> Repeat</label>
<div class=repeatopts><div class=checks role=group aria-label="Weekdays"><div class="t3 xs">Weekdays</div>
<label style="margin:8px 0"><input type=checkbox name=weekday value=0> Mon</label><label style="margin:8px 0"><input type=checkbox name=weekday value=1> Tue</label><label style="margin:8px 0"><input type=checkbox name=weekday value=2> Wed</label><label style="margin:8px 0"><input type=checkbox name=weekday value=3> Thu</label><label style="margin:8px 0"><input type=checkbox name=weekday value=4> Fri</label><label style="margin:8px 0"><input type=checkbox name=weekday value=5> Sat</label><label style="margin:8px 0"><input type=checkbox name=weekday value=6> Sun</label></div>
<label>Ends (optional)<input type=date name=end_date></label>
<p class="t3 sm">Starts on the date above. Occurrences fall on the weekdays you pick, through the end date, or for the next eight weeks.</p>
{% if coach_choices %}<div class=checks role=group aria-label="Coaches"><div class="t3 xs">Coaches</div>{% for c in coach_choices %}<label style="margin:8px 0"><input type=checkbox name=coach value="{{ c.id }}">{{ display_first(c) }} {{ c.last }}</label>{% endfor %}</div>{% endif %}
</div></div>
<button class="btn btn-primary full" name=action value=add>Add practice</button></form></details>{% endif %}
</div>
<script>
(function(){
 var head=document.querySelector('header.homefade'); if(!head||head.dataset.bound) return; head.dataset.bound='1';
 var map=document.getElementById('homeMap');
 var reduced=window.matchMedia('(prefers-reduced-motion: reduce)').matches, ticking=false;
 function measure(){
  var card=document.querySelector('#schedule .card:not(.schedsame)');
  var dock=document.querySelector('.homedock');
  var headH=head.offsetHeight||76;
  document.documentElement.style.setProperty('--homehead', headH+'px');
  if(!card||!dock) return;
  var nav=document.querySelector('nav.tabs');
  var navTop=window.innerHeight-(nav?nav.offsetHeight:64);
  var want=Math.round(card.offsetHeight*0.25);
  document.documentElement.style.setProperty('--peek', want+'px');
  var top=card.getBoundingClientRect().top+window.scrollY;
  var delta=(navTop-want)-top;
  dock.style.minHeight=Math.max(0, Math.round(dock.offsetHeight+delta))+'px';
  if(window.grunionsPlaceMap) window.grunionsPlaceMap();
 }
 function range(){
  var mark=document.querySelector('.nextcard')||document.getElementById('schedule'); if(!mark) return 160;
  var top=mark.getBoundingClientRect().top+window.scrollY-(head.offsetHeight||0);
  return Math.max(80, top);
 }
 function paint(){
  ticking=false;
  var y=window.scrollY||0, span=range(), p=span?y/span:0;
  if(p<0) p=0; if(p>1) p=1;
  if(reduced) p=y>12?1:0;
  if(map) map.style.opacity=String(1-p);
  head.classList.toggle('solid', p>0.92);
  var fade=y/48; if(fade<0) fade=0; if(fade>1) fade=1;
  if(reduced) fade=y>8?1:0;
  head.style.setProperty('--titlefade', fade.toFixed(3));
  head.classList.toggle('titleaway', fade>0.85);
  var hi=head.querySelector('.hititle'), sch=head.querySelector('.schedtitle');
  if(hi) hi.setAttribute('aria-hidden', fade>=0.5?'true':'false');
  if(sch) sch.setAttribute('aria-hidden', fade>=0.5?'false':'true');
 }
 function onScroll(){ if(ticking) return; ticking=true; requestAnimationFrame(paint); }
 window.addEventListener('scroll', onScroll, {passive:true});
 measure();
 var alerts=document.querySelector('.homealerts');
 if(window.ResizeObserver&&alerts) new ResizeObserver(function(){ measure(); }).observe(alerts);
 function land(){
  var hash=location.hash;
  if(head.getAttribute('data-entry')==='schedule' && (!hash || hash==='#schedule')) window.scrollTo(0, range());
  document.body.classList.remove('schedopen');
  paint();
 }
 land();
 requestAnimationFrame(function(){ measure(); land(); });
 window.addEventListener('resize', function(){ measure(); paint(); }, {passive:true});
})();
</script>
"""

_CAM = '<svg viewBox="0 0 48 48" aria-hidden=true><g fill="none" stroke="currentColor" stroke-linejoin="round" stroke-width="3"><path d="M14.07 10.794c-2.181.073-4.008.163-5.48.252c-2.713.164-4.856 2.235-5.097 4.943A125 125 0 0 0 3 26.864c0 4.257.246 8.09.493 10.874c.241 2.708 2.384 4.78 5.098 4.943c3.323.2 8.455.41 15.409.41s12.086-.21 15.41-.41c2.713-.164 4.856-2.235 5.097-4.943c.247-2.783.493-6.617.493-10.874s-.246-8.091-.493-10.875c-.241-2.708-2.384-4.779-5.098-4.943c-1.471-.089-3.298-.18-5.48-.252l-1.46-3.011c-.712-1.466-2.094-2.49-3.718-2.613A64 64 0 0 0 24 5c-1.932 0-3.539.079-4.75.17c-1.625.123-3.007 1.147-3.718 2.613l-1.461 3.01Z"/><path d="M15 26a9 9 0 1 0 18 0a9 9 0 1 0-18 0"/></g></svg>'
T["profile"] = """<form id=profileForm method=post action=/profile enctype=multipart/form-data>{{ csrf_field() }}<input type=hidden name=action value=save><input type=hidden name=photo_clear id=photoClear value="">
<input class=pick type=file name=photo id=photoFile accept="image/jpeg,image/png,image/gif,image/webp,image/heic,image/heif,.heic">
<div class=profilehero>
<div class=avatarwrap>
<button type=button class="avatar hero" id=avatarBtn aria-label="Profile photo">{% if m.photo %}<img id=avatarImg src="/avatar/{{ m.id }}?v={{ m.photo }}" alt="" width="112" height="112">{% else %}<img id=avatarImg alt="" width="112" height="112" hidden>{% endif %}<span id=avatarLetters {% if m.photo %}hidden{% endif %}>{{ initials(m) }}</span></button>
<button type=button class="cambadge editonly" id=camBadge aria-label="Choose photo">""" + _CAM + """</button>
</div>
<button type=button class="textlink danger editonly" id=removePhoto {% if not m.photo %}hidden{% endif %}>Remove photo</button>
<div class=profilename>{{ display_first(m) }} {{ m.last }}</div>
<p class=profilesub>{{ hist|length }} practice{{ '' if hist|length == 1 else 's' }} attended{% if nmonth %} · {{ nmonth }} this month{% endif %}</p>
<div class=stats><div class=stattile><b>{{ hist|length }}</b><span>Attended</span></div><div class=stattile><b>{{ nmonth }}</b><span>This month</span></div></div>
</div>
</form>
{{ membership_section(m, vr_pending) }}
<div class=seclabel>Personal</div>
<div class=list>
<div class="li prow"><span class=k>Legal name</span><span class=v>{{ m.first }} {{ m.last }}</span></div>
<div class="li prow viewonly"><span class=k>Preferred name</span><span class=v>{{ m.preferred_first or '—' }}</span></div>
<div class="li prow editonly"><label class=prefedit style="width:100%;margin:0">Preferred name<input form=profileForm name=preferred_first id=prefName value="{{ m.preferred_first or '' }}" data-original="{{ m.preferred_first or '' }}" placeholder="Leave blank to use your legal first name" autocomplete=off></label></div>
<div class="li prow"><span class=k>Email</span><span class=v>{{ m.email }}</span></div>
<div class="li prow viewonly"><span class=k>Phone</span><span class=v>{{ fmt_phone(m.phone) }}</span></div>
<div class="li prow editonly"><label class=prefedit style="width:100%;margin:0">Phone<input form=profileForm name=phone id=phoneInput type=tel inputmode=numeric autocomplete=tel value="{{ '' if fmt_phone(m.phone) == '—' else fmt_phone(m.phone) }}" data-original="{{ '' if fmt_phone(m.phone) == '—' else fmt_phone(m.phone) }}"></label></div>
</div>
<div class=seclabel>Role</div>
<div class=list><div class="li prow"><span class=k>Role</span><span class="chip-info" style="margin:0">{{ role_label(m)|capitalize }}</span></div></div>
<div class=seclabel>Settings</div>
<div class=list><a class="li prow chevrow" href=/notifications><span>Notifications</span><span class=nxchev aria-hidden=true>›</span></a></div>
<div class=seclabel>Account</div>
<a class="btn btn-secondary full" href=/logout>Log out</a>
<script>
(function(){
 var file=document.getElementById('photoFile'), clear=document.getElementById('photoClear'), img=document.getElementById('avatarImg'), letters=document.getElementById('avatarLetters'), pref=document.getElementById('prefName'), phone=document.getElementById('phoneInput'), removeBtn=document.getElementById('removePhoto'), usawp=document.getElementById('usawpNumber');
 var originalSrc=img.getAttribute('src')||'', hadPhoto={{ 'true' if m.photo else 'false' }}, preview=null;
 function showPhoto(src){img.hidden=false; img.src=src; letters.hidden=true; removeBtn.hidden=false;}
 function showLetters(){img.hidden=true; img.removeAttribute('src'); letters.hidden=false; removeBtn.hidden=true;}
 function formatPhone(v){
  var d=(v||'').replace(/\\D/g,'');
  if(d.length>10 && d.charAt(0)==='1') d=d.slice(1);
  d=d.slice(0,10);
  if(!d) return '';
  if(d.length<4) return '('+d;
  if(d.length<7) return '('+d.slice(0,3)+') '+d.slice(3);
  return '('+d.slice(0,3)+') '+d.slice(3,6)+'-'+d.slice(6);
 }
 function enter(){document.body.classList.add('profile-edit');}
 function leave(){
  document.body.classList.remove('profile-edit');
  if(preview){URL.revokeObjectURL(preview); preview=null;}
  file.value=''; clear.value='';
  pref.value=pref.getAttribute('data-original')||'';
  if(phone) phone.value=phone.getAttribute('data-original')||'';
  if(usawp) usawp.value=usawp.getAttribute('data-original')||'';
  if(hadPhoto&&originalSrc) showPhoto(originalSrc); else showLetters();
  if(hadPhoto) removeBtn.hidden=false;
 }
 document.getElementById('profileEdit').onclick=enter;
 document.getElementById('profileCancel').onclick=leave;
 document.getElementById('profileBack').onclick=function(){ if(history.length>1) history.back(); else location.href='/home'; };
 function pick(){ file.click(); }
 document.getElementById('avatarBtn').onclick=function(){ if(document.body.classList.contains('profile-edit')) pick(); };
 document.getElementById('camBadge').onclick=function(){ if(document.body.classList.contains('profile-edit')) pick(); };
 if(phone) phone.addEventListener('input', function(){ var next=formatPhone(phone.value); if(phone.value!==next) phone.value=next; });
 file.onchange=function(){ var f=file.files&&file.files[0]; if(!f) return; if(preview) URL.revokeObjectURL(preview); preview=URL.createObjectURL(f); clear.value=''; showPhoto(preview); };
 removeBtn.onclick=function(){ file.value=''; if(preview){URL.revokeObjectURL(preview); preview=null;} clear.value=hadPhoto?'1':''; showLetters(); };
})();
</script>"""

T["member"] = """{% set cl = clearance(m) %}{% set cred = credential_dates(m) %}{% set ps = panel_status(m) %}{% set cc = coach_clearance(m) %}{% set ce = coach_eligibility(m) %}{% set tw = trial_window(m) %}{% set on_trial = tw and tw.active and (m.usawp_status or '') != 'verified' %}
<form id=memberForm method=post action="/admin/member/{{ m.id }}">{{ csrf_field() }}<input type=hidden name=member_id value={{ m.id }}>
<div class=profilehero>
<div class=avatarwrap>
<span class="avatar hero">{% if m.photo %}<img src="/avatar/{{ m.id }}?v={{ m.photo }}" alt="" width="112" height="112">{% else %}{{ initials(m) }}{% endif %}</span>
</div>
<div class=profilename>{{ display_first(m) }} {{ m.last }}</div>
<p class=profilesub>{{ hist|length }} practice{{ '' if hist|length == 1 else 's' }} attended{% if nmonth %} · {{ nmonth }} this month{% endif %}</p>
<div class=stats><div class=stattile><b>{{ hist|length }}</b><span>Attended</span></div><div class=stattile><b>{{ nmonth }}</b><span>This month</span></div></div>
</div>
{{ memhead(m) }}
<div class=list>
<div class="li prow viewonly">{{ titledot('warn' if on_trial else date_dot(m.usawp_valid_until), 'USAWP # ' ~ (m.usawp_number or '—')) }}<span class=v>{% if on_trial %}{{ trial_badge(tw) }}{% elif m.usawp_valid_until %}{{ fmt_long(m.usawp_valid_until) }}{% else %}Not on file{% endif %}</span></div>
<div class="li prow viewonly">{{ titledot(date_dot(cred.safesport), 'SafeSport training') }}<span class=v>{% if cred.safesport %}{{ fmt_long(cred.safesport) }}{% else %}Not on file{% endif %}</span></div>
<div class="li prow viewonly">{{ titledot(date_dot(cred.background), 'Background screening') }}<span class=v>{% if cred.background %}{{ fmt_long(cred.background) }}{% else %}Not on file{% endif %}</span></div>
<div class="li prow viewonly">{% set rf = referee_eligibility(m) %}{{ titledot(date_dot(cred.referee), 'Referee') }}<span class=v>{% if cred.referee %}{{ fmt_long(cred.referee) }}{% else %}Not on file{% endif %}{% if rf.eligible %} {{ referee_tag(m) }}{% elif rf.expired %}<span class="st st-bad ref-elig">Referee eligibility expired {{ fmt_long(rf.expired) }}</span>{% elif rf.text %} {{ referee_tag(m) }}{% endif %}</span></div>
{% if cc or ce.eligible or ce.text %}<div class="li prow viewonly">{% if cc %}{{ titledot('ok' if cc.ok else 'bad', 'Coaching') }}<span class=v>{{ 'cleared' if cc.ok else cc.text }}</span>{% elif ce.eligible %}{{ titledot('ok', 'Coaching') }}<span class=v>Coach eligible</span>{% else %}{{ titledot('bad' if ce.expired else 'warn', 'Coaching') }}<span class=v>{{ ce.text or 'Not eligible' }}</span>{% endif %}</div>{% endif %}
{% if me().is_admin %}
<div class="li editonly"><p class="t3 sm" style="margin:0">Look this member up on Sport:80 and enter what you find. Grunions does not contact Sport:80.{% if m.vr_status == 'pending' %} Saving answers the pending verification request.{% endif %}</p></div>
<div class="li editonly"><label class=prefedit style="width:100%;margin:0">USAWP number<input name=number inputmode=numeric autocomplete=off value="{{ m.usawp_number or '' }}"></label></div>
<div class="li editonly"><label class=prefedit style="width:100%;margin:0">Status<select name=verified><option value=yes {{ 'selected' if m.usawp_status=='verified' }}>Verified</option><option value=no {{ 'selected' if m.usawp_status!='verified' }}>Not verified</option></select></label></div>
<div class="li editonly"><label class=prefedit style="width:100%;margin:0">Membership type<input name=membership_type value="{{ m.membership_type or '' }}" placeholder="Individual Membership, Coach" autocomplete=off></label></div>
<div class="li editonly">{{ date_field('Membership expires', 'valid_until', m.usawp_valid_until) }}</div>
<div class="li editonly">{{ date_field('SafeSport expires', 'safesport_expires', cred.safesport) }}</div>
<div class="li editonly">{{ date_field('Background screening expires', 'background_expires', cred.background) }}</div>
<div class="li editonly">{{ date_field('Referee certification expires', 'referee_expires', cred.referee) }}</div>
<div class="li editonly"><label class=prefedit style="width:100%;margin:0">Note<textarea name=note rows=2 placeholder="Recorded from Sport:80"></textarea></label></div>
{% endif %}
</div>
{% if not on_trial and ps.reason %}<p class="sm viewonly" style="margin:8px 0 0">{{ ps.reason }}</p>{% endif %}
{% if not cl.ok or m.usawp_status != 'verified' %}<p class="sm viewonly" style="margin:8px 0 0"><a target=_blank rel=noopener href="https://usawp.sport80.com/" onclick="navigator.clipboard&&navigator.clipboard.writeText('{{ m.first }} {{ m.last }}')">Verify {{ m.first }} on Sport:80</a></p>{% endif %}
<div class=seclabel>Personal</div>
<div class=list>
<div class="li prow viewonly"><span class=k>Legal name</span><span class=v>{{ m.first }} {{ m.last }}</span></div>
{% if me().is_admin %}
<div class="li prow editonly"><label class=prefedit style="width:100%;margin:0">Legal first name<input name=first value="{{ m.first }}" autocomplete=off required></label></div>
<div class="li prow editonly"><label class=prefedit style="width:100%;margin:0">Legal last name<input name=last value="{{ m.last }}" autocomplete=off required></label></div>
{% endif %}
<div class="li prow viewonly"><span class=k>Preferred name</span><span class=v>{{ m.preferred_first or '—' }}</span></div>
{% if me().is_admin %}<div class="li prow editonly"><label class=prefedit style="width:100%;margin:0">Preferred first name<input name=preferred_first value="{{ m.preferred_first or '' }}" placeholder="Leave blank to use legal first name" autocomplete=off></label></div>{% endif %}
<div class="li prow"><span class=k>Email</span><span class=v>{{ m.email }}</span></div>
<div class="li prow"><span class=k>Phone</span><span class=v>{{ fmt_phone(m.phone) }}</span></div>
</div>
{% for a in audits %}<p class="t3 sm viewonly" style="margin:8px 0 0">{{ a.actor }} changed {{ a.old_name }} → {{ a.new_name }} · {{ fmt_when(a.at) }}</p>{% endfor %}
</form>
{% if me().is_admin %}
<div class=seclabel>Actions</div>
<button type=button class="btn btn-secondary full viewonly" id=memberRecheck>Recheck</button>
<form method=post action="/admin/member/{{ m.id }}" style="margin-top:10px">{{ csrf_field() }}<input type=hidden name=member_id value={{ m.id }}><button class="btn btn-secondary full" name=action value=ask_bot {% if m.vr_status=='pending' %}disabled{% endif %}>Ask Grunions to verify</button></form>
{% endif %}
<script>
(function(){
 var edit=document.getElementById('profileEdit'), cancel=document.getElementById('profileCancel'), back=document.getElementById('profileBack'), recheck=document.getElementById('memberRecheck');
 if(edit) edit.onclick=function(){document.body.classList.add('profile-edit'); var el=document.getElementById('membership'); if(el) el.scrollIntoView({block:'start'});};
 if(cancel) cancel.onclick=function(){document.body.classList.remove('profile-edit'); if(/[?&]edit=1/.test(location.search)) history.replaceState(null,'',location.pathname);};
 if(back) back.onclick=function(){ if(history.length>1) history.back(); else location.href='{{ "/members" if me().is_admin else "/admin" }}'; };
 if(recheck) recheck.onclick=function(){document.body.classList.add('profile-edit'); var el=document.getElementById('membership'); if(el) el.scrollIntoView({block:'start'});};
})();
</script>"""

T["notifications"] = """
{{ push_card() }}
<form method=post action=/notifications>{{csrf_field()}}
<div class=list>{% for key, label in types %}
<label class=li><input type=checkbox name=push value="{{key}}" {% if prefs.get(key, True) %}checked{% endif %}>{{label}}</label>
{% endfor %}</div>
<label style="margin-top:16px"><input type=checkbox name=email_reminders value=1 {% if email_on %}checked{% endif %}>Email reminders for membership, SafeSport, and the 2-week trial</label>
<p class="t3 sm">These emails go out 7 days before, 1 day before, and on the day it expires. Practice cancellation emails always send.</p>
<button class="btn btn-primary full">Save</button></form>"""

T["chat"] = """<div class=chat id=chat></div><div style=height:90px></div>
<div class="composer noprint"><div class=qbar id=quoteBar hidden><div class=grow><b id=quoteWho></b><span id=quoteTxt></span></div><button type=button id=quoteX aria-label="Cancel reply">✕</button></div><div class=qbar id=editBar hidden><div class=grow><b>Editing</b><span id=editHint></span></div><button type=button id=editX aria-label="Cancel edit">✕</button></div><div class=preview id=prev hidden><img id=prevImg alt=""><span id=prevName></span><button type=button class="quiet compact" id=prevX>Remove</button></div>
<form id=f><input type=file id=file accept="image/jpeg,image/png,image/gif,image/webp,image/heic,image/heif,.heic" hidden>
<button type=button class="iconbtn" id=attach title="Attach image" aria-label="Attach image"><svg  viewBox="0 0 48 48" aria-hidden=true><g fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="3"><path d="M35.474 7c-.552-2.024-2.29-3.486-4.473-3.643C28.445 3.173 24.665 3 19.5 3c-5.134 0-8.898.171-11.453.354c-2.557.182-4.512 2.136-4.694 4.694C3.17 10.603 3 14.368 3 19.5c0 5.165.174 8.944.357 11.5c.157 2.183 1.62 3.922 3.643 4.473"/><path d="M12.354 17.047c.182-2.557 2.136-4.51 4.694-4.693C19.602 12.17 23.367 12 28.5 12s8.897.171 11.452.354c2.558.182 4.512 2.136 4.694 4.694c.183 2.555.354 6.32.354 11.452c0 5.133-.171 8.897-.354 11.453c-.182 2.557-2.136 4.51-4.694 4.693c-2.555.183-6.32.354-11.452.354c-5.133 0-8.897-.171-11.453-.354c-2.557-.182-4.51-2.136-4.693-4.694C12.17 37.398 12 33.633 12 28.5s.171-8.897.354-11.453"/><path d="M44.846 36.389c-2.255-2.114-3.88-3.522-5.008-4.444c-1.338-1.095-3.102-1.254-4.543-.293c-1.11.74-2.634 1.87-4.625 3.579c-2.96-2.831-5-4.61-6.338-5.705s-3.102-1.253-4.543-.293c-1.62 1.08-4.123 2.992-7.668 6.318M32 22a3 3 0 1 0 6 0a3 3 0 1 0-6 0"/></g></svg></button>
<textarea id=body rows=1 maxlength=2000 placeholder="Message {{'coaches' if ch=='coaches' else 'the team'}}"></textarea>
<button class="iconbtn send" type=submit aria-label=Send><svg  viewBox="0 0 48 48" aria-hidden=true><path fill="none" stroke="currentColor" stroke-linejoin="round" stroke-width="3" d="M3.988 7.331c-.907-2.236 1.145-4.368 3.425-3.578c7.73 2.679 22.423 8.422 35.323 17.184a3.683 3.683 0 0 1 0 6.127c-12.9 8.761-27.593 14.505-35.323 17.184c-2.28.79-4.332-1.343-3.425-3.579c1.95-4.803 4.178-9.412 5.287-11.643a3.9 3.9 0 0 1 2.178-1.93L20 24l-8.547-3.095a3.9 3.9 0 0 1-2.178-1.93c-1.109-2.231-3.337-6.84-5.287-11.644Z"/></svg></button></form></div>
<dialog id=actSheet class=botsheet><div class=sheet>
<div class=grab aria-hidden=true></div>
<div class=emogrid id=actEmoji>{% for e in REACTIONS %}<button type=button data-e="{{e}}">{{e}}</button>{% endfor %}<button type=button data-more=1 aria-label="More emoji">+</button></div>
<div class=emopick id=emojiMore hidden></div>
<p id=actConfirm hidden>Delete this message?</p>
<div class=actgroup><button type=button class=actrow id=actReply><svg  viewBox="0 0 48 48" aria-hidden=true><path fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M27.519 32.739c1.411-1.987.336-4.284-2.096-4.452a113 113 0 0 0-4.489-.209a556 556 0 0 1-.107-5.898c-.056-4.299 2.757-8 7.057-8c4.531 0 7.587 3.942 7.587 8.473V34.01c0 1.665.881 3.2 2.526 3.458c.633.1 1.393.167 2.29.167c.899 0 1.66-.067 2.292-.167c1.645-.258 2.526-1.793 2.526-3.459V21.264c0-9.894-7.327-18.26-17.221-18.26c-10.676 0-18.68 9.058-18.818 19.732a807 807 0 0 1-.085 5.346c-1.78.052-3.23.125-4.402.206c-2.432.168-3.507 2.465-2.096 4.453c1.024 1.44 2.43 3.306 4.336 5.637c2.913 3.562 5.048 5.494 6.405 6.52c1.083.82 2.47.82 3.553 0c1.357-1.026 3.492-2.958 6.405-6.52c1.907-2.332 3.313-4.197 4.337-5.638Z"/></svg>Reply</button></div>
<div class=actgroup id=actCopyGroup><button type=button class=actrow id=actCopy><svg  viewBox="0 0 48 48" aria-hidden=true><g fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="3"><path d="M42 31.335c.812.48 1.493.908 2.049 1.274c1.044.686 1.044 2.097 0 2.783c-1.6 1.052-4.229 2.623-8.049 4.442c-4.872 2.32-8.776 3.429-10.699 3.889a5.6 5.6 0 0 1-2.602 0c-1.923-.46-5.827-1.57-10.699-3.89c-3.82-1.818-6.449-3.39-8.049-4.441c-1.044-.686-1.044-2.097 0-2.783A51 51 0 0 1 6 31.335"/><path d="M42 21.21c.812.48 1.492.91 2.049 1.275c1.044.686 1.044 2.097 0 2.783c-1.6 1.052-4.23 2.623-8.05 4.442c-4.872 2.32-8.775 3.429-10.698 3.889a5.6 5.6 0 0 1-2.603 0c-1.922-.46-5.826-1.57-10.698-3.89c-3.82-1.818-6.45-3.39-8.05-4.441c-1.043-.686-1.043-2.097 0-2.783A51 51 0 0 1 6 21.21"/><path d="M22.699 4.278a5.6 5.6 0 0 1 2.602 0c1.923.46 5.827 1.569 10.699 3.889c3.82 1.82 6.449 3.39 8.049 4.442c1.044.686 1.044 2.097 0 2.783c-1.6 1.052-4.229 2.623-8.049 4.442c-4.872 2.32-8.776 3.429-10.699 3.889a5.6 5.6 0 0 1-2.602 0c-1.923-.46-5.827-1.57-10.699-3.89c-3.82-1.818-6.449-3.39-8.049-4.441c-1.044-.686-1.044-2.097 0-2.783C5.551 11.557 8.18 9.986 12 8.167c4.872-2.32 8.776-3.43 10.699-3.889"/></g></svg>Copy</button></div>
<div class=actgroup id=actOwn><button type=button class=actrow id=actEdit><svg  viewBox="0 0 48 48" aria-hidden=true><g fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="3"><path d="M42.945 13.617c1.492 2.293.74 5.11-1.191 7.048L20.66 41.833a3.82 3.82 0 0 1-2.483 1.132c-1.724.1-5.016.247-10.039.295a.96.96 0 0 1-.585-.186a13 13 0 0 1-1.41-1.217c-.49-.49-.896-.98-1.218-1.411a.96.96 0 0 1-.186-.585c.048-5.023.195-8.314.295-10.04a3.82 3.82 0 0 1 1.132-2.482L27.334 6.245c1.939-1.931 4.755-2.683 7.048-1.19c1.331.865 2.932 2.105 4.695 3.868c1.762 1.762 3.002 3.363 3.868 4.694"/><path d="m35.769 6.027l1.846-1.582c1.087-.932 2.529-1.482 3.794-.81c.527.28 1.11.683 1.691 1.265a7.1 7.1 0 0 1 1.266 1.692c.672 1.265.122 2.706-.81 3.793l-1.583 1.847m-3.117 11.321s-1.403-3.1-6.356-8.053c-4.953-4.952-8.053-6.355-8.053-6.355m-5.008 33.521c-1.55-2.102-3.793-4.892-6.593-7.682a68 68 0 0 0-7.512-6.425M27 6.5c-1.4-.84-3.113-1.21-4.35-1.372c-1.051-.138-2.071.294-2.822 1.044L11 15M6 42l-3 3"/></g></svg>Edit</button><button type=button class="actrow danger" id=actDelete><svg  viewBox="0 0 48 48" aria-hidden=true><g fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="3"><path d="M20.5 36.5c-1.024 0-1.93-.058-2.682-.135c-1.225-.125-1.877-1.392-1.346-2.503C17.74 31.203 19 29 19 29l-4.5 1m7.005-4.804a27 27 0 0 1 1.458-2.255c.72-.998 2.144-.93 2.84.086a84 84 0 0 1 2.947 4.62l1.384-4.397m.361 8.304c.512.886.915 1.701 1.224 2.39c.505 1.123-.267 2.321-1.495 2.417c-2.936.23-5.474.242-5.474.242L27.866 40"/><path d="M6.183 15.842c3.076.249 8.554.522 17.796.522c9.288 0 14.774-.276 17.843-.526c-.888 13.818-1.736 21.005-2.241 24.427c-.255 1.73-1.392 3.14-3.092 3.548C34.173 44.37 30.187 45 24.002 45s-10.171-.63-12.487-1.186c-1.7-.408-2.837-1.818-3.092-3.548c-.505-3.421-1.353-10.608-2.24-24.423Z"/><path d="M31.036 7.176c3.56.066 6.334.174 8.322.275c2.39.12 4.61 1.393 5.278 3.691q.152.517.276 1.097c.394 1.84-.983 3.421-2.858 3.58c-3.02.255-8.547.545-18.077.545c-9.529 0-15.057-.29-18.076-.545c-1.876-.158-3.261-1.75-2.776-3.568c.175-.655.39-1.253.616-1.784c.813-1.903 2.77-2.885 4.836-2.999c1.908-.104 4.685-.222 8.387-.292A7 7 0 0 1 23.37 3h1.262a7 7 0 0 1 6.405 4.176Z"/></g></svg><span id=actDeleteLabel>Delete</span></button></div>
</div></dialog>
<dialog id=whoSheet class=botsheet><div class=sheet>
<div class=grab aria-hidden=true></div>
<h2 id=whoTitle style="margin:0 0 8px;font-size:20px"></h2>
<div class=seenlist id=whoList></div>
</div></dialog>
<dialog id=seenSheet class=botsheet><div class=sheet>
<div class=grab aria-hidden=true></div>
<h2 style="margin:0 0 8px">Seen by</h2>
<div class=seenlist id=seenPeople></div>
<button type=button class="btn btn-secondary full" id=seenClose style="margin-top:12px">Close</button>
</div></dialog>
<script>
const CSRF="{{csrf_token()}}",CH="{{ch}}",EMO={{REACTIONS|tojson}};let last=0;const box=document.getElementById('chat'),msgs={};
const esc=s=>s.replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const t=iso=>new Date(iso).toLocaleString([], {weekday:'short',hour:'numeric',minute:'2-digit'});
function rxHtml(id,r){r=r||{};return Object.keys(r).map(e=>`<button type=button class="${r[e].mine?'on':''}" data-m=${id} data-e="${esc(e)}">${e} ${r[e].n}</button>`).join('')}
function safeHttp(url){
 var u=String(url||'');
 if(/^www\\./i.test(u)) u='https://'+u;
 else if(!/^https?:\\/\\//i.test(u)) u='https://'+u;
 try{
  var parsed=new URL(u);
  if(parsed.protocol!=='http:'&&parsed.protocol!=='https:') return '';
  if(!parsed.hostname||parsed.hostname.indexOf('.')<0) return '';
  return parsed.href;
 }catch(err){ return ''; }
}
function linkify(raw){
 raw=String(raw||'');
 var spans=[], used=[], i, m, text, href;
 function taken(a,b){ for(var k=0;k<used.length;k++){ if(a<used[k][1]&&b>used[k][0]) return true; } return false; }
 function add(a,b,kind,href,text){ if(b<=a||taken(a,b)) return; used.push([a,b]); spans.push({i:a,j:b,kind:kind,href:href,text:text}); }
 var urlRe=/\\b(?:(?:https?:\\/\\/|www\\.)[^\\s<>"']+|(?<![@/\\w])(?:[a-z0-9-]+\\.)+[a-z]{2,}(?:\\/[^\\s<>"']*)?)/gi;
 while((m=urlRe.exec(raw))){
  text=m[0].replace(/[.,;:!?)\\]]+$/,'');
  href=text&&safeHttp(text);
  if(href) add(m.index, m.index+text.length, 'url', href, text);
  if(urlRe.lastIndex===m.index) urlRe.lastIndex++;
 }
 var addrRe=/\\b\\d{1,6}\\s+[A-Za-z0-9.'-]+(?:\\s+[A-Za-z0-9.'-]+){0,4}\\s+(?:Street|St|Avenue|Ave|Boulevard|Blvd|Road|Rd|Drive|Dr|Lane|Ln|Court|Ct|Way|Place|Pl|Terrace|Ter|Circle|Cir|Parkway|Pkwy|Highway|Hwy)\\.?(?:,\\s*[A-Za-z][A-Za-z .'-]*?,\\s*[A-Z]{2}(?:\\s+\\d{5}(?:-\\d{4})?)?)?/gi;
 var stop={the:1,a:1,an:1,at:1,on:1,in:1,to:1,of:1,and:1,pm:1,am:1,for:1};
 while((m=addrRe.exec(raw))){
  text=m[0];
  var bits=text.replace(/[.,]/g,' ').split(/\\s+/), okName=false, w;
  for(w=1;w<bits.length;w++){
   if(/^(?:Street|St|Avenue|Ave|Boulevard|Blvd|Road|Rd|Drive|Dr|Lane|Ln|Court|Ct|Way|Place|Pl|Terrace|Ter|Circle|Cir|Parkway|Pkwy|Highway|Hwy)\\.?$/i.test(bits[w])){
    okName=!stop[(bits[w-1]||'').replace(/\\.$/,'').toLowerCase()];
    break;
   }
  }
  if(!okName) continue;
  href='https://www.google.com/maps/search/?api=1&query='+encodeURIComponent(text);
  add(m.index, m.index+text.length, 'map', href, text);
  if(addrRe.lastIndex===m.index) addrRe.lastIndex++;
 }
 spans.sort(function(a,b){return a.i-b.i});
 var out='', pos=0, s;
 for(i=0;i<spans.length;i++){
  s=spans[i];
  if(s.i<pos) continue;
  out+=esc(raw.slice(pos,s.i));
  if(s.kind==='url') out+='<a class=msglink href="'+esc(s.href)+'" target=_blank rel="noopener noreferrer">'+esc(s.text)+'</a>';
  else out+='<a class="msglink maplink" href="'+esc(s.href)+'" data-map="'+esc(s.text)+'" target=_blank rel="noopener noreferrer">'+esc(s.text)+'</a>';
  pos=s.j;
 }
 out+=esc(raw.slice(pos));
 return out;
}
function bodyHtml(m){
 if(m.deleted) return '<div class="txt deleted">Message deleted</div>';
 let h='';
 if(m.reply) h+=`<div class=quotechip><b>${esc(m.reply.who||'')}</b><span>${esc(m.reply.body||'')}</span></div>`;
 if(m.body) h+=`<div class=txt>${linkify(m.body)}${m.edited?' <span class=edited>(edited)</span>':''}</div>`;
 if(m.image) h+=`<a class=img href="${m.image.full}" data-full="${m.image.full}"><img src="${m.image.thumb}" alt="Photo from ${esc(m.who)}" loading=lazy></a>`;
 return h||'<div class=txt></div>'}
function fill(d,m){
 var kept=d.querySelector&&d.querySelector('#seenLine');
 if(kept) kept.remove();
 d.className='m'+(m.mine?' mine':'')+(m.ann&&!m.deleted?' ann':'');
 d.dataset.g='';
 d.innerHTML=(m.deleted?'':`<button type=button class=more data-act=${m.id} aria-label="Message actions"><svg width="22" height="22" viewBox="0 0 48 48" aria-hidden=true><g fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="3"><path d="M3 24a21 21 0 1 0 42 0a21 21 0 1 0-42 0"/><path d="M20.5 24a3.5 3.5 0 1 0 7 0a3.5 3.5 0 1 0-7 0m-12 0a3.5 3.5 0 1 0 7 0a3.5 3.5 0 1 0-7 0m24 0a3.5 3.5 0 1 0 7 0a3.5 3.5 0 1 0-7 0"/></g></svg></button>`)+
  bodyHtml(m)+`<div class=rx>${rxHtml(m.id)}</div>`;
 if(kept) d.appendChild(kept);}
let grouping=false;
function sameGroup(prev,cur){
 if(!prev||!cur||prev.uid!==cur.uid) return false;
 if(!!(prev.ann&&!prev.deleted)!==!!(cur.ann&&!cur.deleted)) return false;
 var delta=new Date(cur.at)-new Date(prev.at);
 return delta>=0&&delta<=5*60*1000}
function placeWho(el,m,at){
 var text=((m.ann&&!m.deleted)?'Announcement · ':'')+m.who+' · '+t(at);
 var who=el.querySelector('.who');
 if(!who){
  who=document.createElement('div'); who.className='who';
  var more=el.querySelector('.more');
  if(more) more.insertAdjacentElement('afterend', who);
  else el.insertBefore(who, el.firstChild);
 }
 if(who.textContent!==text) who.textContent=text}
function groupMessages(){
 var rows=[].slice.call(box.querySelectorAll('.m')), i=0;
 while(i<rows.length){
  var prev=msgs[+rows[i].id.slice(3)], j=i;
  while(j+1<rows.length&&sameGroup(prev, msgs[+rows[j+1].id.slice(3)])){ j++; prev=msgs[+rows[j].id.slice(3)]; }
  var latest=msgs[+rows[j].id.slice(3)];
  for(var k=i;k<=j;k++){
   var el=rows[k], m=msgs[+el.id.slice(3)];
   var pos=i===j?'solo':(k===i?'first':(k===j?'last':'mid'));
   if(el.dataset.g!==pos){
    el.classList.remove('g-solo','g-first','g-mid','g-last');
    el.classList.add('g-'+pos);
    el.dataset.g=pos;
   }
   if(k===i) placeWho(el, m, latest.at);
   else { var w=el.querySelector('.who'); if(w) w.remove(); }
  }
  i=j+1}}
function add(m){msgs[m.id]=m;last=Math.max(last,m.id);if(document.getElementById('msg'+m.id))return;const d=document.createElement('div');d.id='msg'+m.id;fill(d,m);box.appendChild(d);if(!grouping)groupMessages()}
function sameBubble(a,b){
 if(!a||!b) return false;
 var img=function(x){return x&&x.image?x.image.full+'|'+x.image.thumb:''};
 var rep=function(x){return x&&x.reply?x.reply.id+'|'+x.reply.who+'|'+x.reply.body:''};
 return a.body===b.body&&!!a.deleted===!!b.deleted&&!!a.edited===!!b.edited&&!!a.ann===!!b.ann&&a.who===b.who&&!!a.mine===!!b.mine&&a.uid===b.uid&&img(a)===img(b)&&rep(a)===rep(b)}
function upsert(m,force){var prev=msgs[m.id];msgs[m.id]=m;const d=document.getElementById('msg'+m.id);if(!d){add(m);return}last=Math.max(last,m.id);if(!force&&d.querySelector('.editbox'))return;if(!force&&sameBubble(prev,m))return;fill(d,m);if(!grouping)groupMessages()}
function paintRx(map){document.querySelectorAll('.m').forEach(el=>{const id=el.id.slice(3),rx=el.querySelector('.rx');if(!rx)return;const h=rxHtml(id,map[id]);if(rx.dataset.h!==h){rx.innerHTML=h;rx.dataset.h=h}})}
let pollGen=0;
async function poll(){const gen=++pollGen,epoch=window.grunionsNavEpoch|0;try{const r=await fetch('/api/messages?c='+CH+'&after='+last);const j=await r.json();if(gen!==pollGen||(window.grunionsNavEpoch|0)!==epoch)return;const end=innerHeight+scrollY>=document.body.scrollHeight-120;
 grouping=true;j.forEach(add);const sync=await (await fetch('/api/messages?c='+CH+'&sync=1')).json();if(gen!==pollGen||(window.grunionsNavEpoch|0)!==epoch){grouping=false;return}sync.forEach(m=>{if(gen===pollGen)upsert(m)});grouping=false;groupMessages();
 const rx=await (await fetch('/api/reactions?c='+CH)).json();if(gen!==pollGen||(window.grunionsNavEpoch|0)!==epoch)return;paintRx(rx);paintSeen(sync.concat(j));if(window.grunionsRefresh)grunionsRefresh();if(j.length&&end)scrollTo(0,document.body.scrollHeight)}catch(e){grouping=false}}
let seenInfo=null;
function personRow(p){
 const av=p.photo?`<span class="avatar seenav"><img src="${esc(p.photo)}" alt="" width="32" height="32"></span>`:`<span class="avatar seenav">${esc(p.initials||'')}</span>`;
 return `<div class=seenrow>${av}<span>${esc(p.name||'')}</span></div>`}
function seenKey(info){return info.id+'|'+info.n+'|'+info.total+'|'+info.label}
function paintSeen(list){
 let hit=null;
 (list||[]).forEach(m=>{if(m&&m.seen&&(!hit||m.id>hit.id)) hit=m});
 Object.keys(msgs).forEach(id=>{const m=msgs[id]; if(m&&m.seen&&(!hit||m.id>hit.id)) hit=m});
 if(hit) Object.keys(msgs).forEach(id=>{if(+id!==hit.id&&msgs[id]&&msgs[id].seen) delete msgs[id].seen});
 seenInfo=hit?hit.seen:null;
 var row=seenInfo?document.getElementById('msg'+seenInfo.id):null;
 var line=document.getElementById('seenLine');
 document.querySelectorAll('.seenline').forEach(function(el){ if(el!==line) el.remove(); });
 if(!seenInfo||!row){ if(line) line.remove(); return; }
 if(!line){ line=document.createElement('button'); line.type='button'; line.id='seenLine'; line.className='seenline'; }
 var key=seenKey(seenInfo);
 if(line.dataset.seen!==key){ line.textContent=seenInfo.label; line.dataset.seen=key; }
 if(line.parentNode!==row) row.appendChild(line);
}
function openSeen(info){
 document.getElementById('seenPeople').innerHTML=(info.seen||[]).map(personRow).join('')||'<p class="t3 sm">No one has seen this yet.</p>';
 grunionsOpenSheet(document.getElementById('seenSheet'))}
const sheet=document.getElementById('actSheet'),actEdit=document.getElementById('actEdit'),actDelete=document.getElementById('actDelete'),actConfirm=document.getElementById('actConfirm'),actOwn=document.getElementById('actOwn'),actCopyGroup=document.getElementById('actCopyGroup'),emojiMore=document.getElementById('emojiMore'),quoteBar=document.getElementById('quoteBar'),editBar=document.getElementById('editBar');
const MORE=["😀","😁","😊","😉","😍","😘","😎","🤔","😭","😡","🤯","🤗","🫡","🤝","👏","🙌","💪","✌️","👋","✅","⭐","💧","🏊","🤽","🏆","📣","📸","🧡","💛","💚","💙","💜","🖤","🤍","💔","🤣","😅","😴","🎉"];
emojiMore.innerHTML=MORE.map(e=>`<button type=button data-e="${e}">${e}</button>`).join('');
let actId=null,confirming=false,replyTo=null,editId=null;
function buzz(){try{if(navigator.vibrate)navigator.vibrate(12)}catch(err){}}
function closeSheet(){actId=null;confirming=false;actConfirm.hidden=true;document.getElementById('actDeleteLabel').textContent='Delete';emojiMore.hidden=true;grunionsCloseSheet(sheet)}
function openSheet(id){const m=msgs[id];if(!m||m.deleted)return;actId=id;confirming=false;actConfirm.hidden=true;document.getElementById('actDeleteLabel').textContent='Delete';emojiMore.hidden=true;
 actEdit.hidden=!(m.mine&&!m.deleted);actDelete.hidden=!m.can_delete;actOwn.hidden=actEdit.hidden&&actDelete.hidden;actCopyGroup.hidden=!m.body;
 grunionsOpenSheet(sheet)}
function clearCompose(){const field=document.getElementById('body');field.value='';grow();document.getElementById('file').value='';document.getElementById('prev').hidden=true;replyTo=null;editId=null;quoteBar.hidden=true;editBar.hidden=true}
function startReply(id){const m=msgs[id];if(!m||m.deleted)return;editId=null;editBar.hidden=true;replyTo=id;document.getElementById('quoteWho').textContent=m.who;document.getElementById('quoteTxt').textContent=(m.body||'Photo').slice(0,140);quoteBar.hidden=false;document.getElementById('body').focus()}
function startEdit(id){const m=msgs[id];if(!m||m.deleted||!m.mine)return;replyTo=null;quoteBar.hidden=true;editId=id;const field=document.getElementById('body');field.value=m.body||'';grow();document.getElementById('editHint').textContent=(m.body||'Photo').slice(0,80);editBar.hidden=false;field.focus()}
async function reactWith(id,emoji){pollGen++;await fetch('/api/messages/'+id+'/react',{method:'POST',headers:{'Content-Type':'application/json','X-CSRF':CSRF},body:JSON.stringify({emoji:emoji})});closeSheet();poll()}
async function showWho(pill){const r=await fetch('/api/messages/'+pill.dataset.m+'/reactors?emoji='+encodeURIComponent(pill.dataset.e));const j=await r.json().catch(()=>({}));document.getElementById('whoTitle').textContent=pill.dataset.e||'';document.getElementById('whoList').innerHTML=(j.people||[]).map(personRow).join('')||'<p class="t3 sm">No one</p>';grunionsOpenSheet(document.getElementById('whoSheet'))}
function toast(msg){const el=document.createElement('div');el.className='toast noprint';el.setAttribute('role','status');el.textContent=msg;document.body.appendChild(el);setTimeout(()=>el.remove(),2000)}
document.getElementById('actReply').onclick=()=>{const id=actId;closeSheet();startReply(id)};
document.getElementById('actCopy').onclick=async()=>{const m=msgs[actId];if(!m||!m.body)return;try{await navigator.clipboard.writeText(m.body)}catch(err){const t=document.createElement('textarea');t.value=m.body;document.body.appendChild(t);t.select();document.execCommand('copy');t.remove()}closeSheet();toast('Copied')};
actEdit.onclick=(e)=>{e.preventDefault();e.stopPropagation();const id=actId;closeSheet();setTimeout(()=>startEdit(id),0)};
actDelete.onclick=async()=>{if(!confirming){confirming=true;actConfirm.hidden=false;document.getElementById('actDeleteLabel').textContent='Delete message';return}
 const id=actId;pollGen++;const r=await fetch('/api/messages/'+id,{method:'DELETE',headers:{'X-CSRF':CSRF}}),j=await r.json().catch(()=>({}));closeSheet();if(r.ok&&j.message)upsert(j.message,true)};
sheet.addEventListener('click',e=>{if(e.target===sheet)closeSheet()});
sheet.addEventListener('close',()=>{confirming=false;actConfirm.hidden=true;document.getElementById('actDeleteLabel').textContent='Delete';emojiMore.hidden=true});
document.getElementById('actEmoji').addEventListener('click',e=>{const b=e.target.closest('button');if(!b)return;if(b.dataset.more){emojiMore.hidden=!emojiMore.hidden;return}if(actId&&b.dataset.e)reactWith(actId,b.dataset.e)});
emojiMore.addEventListener('click',e=>{const b=e.target.closest('button');if(b&&b.dataset.e&&actId)reactWith(actId,b.dataset.e)});
box.addEventListener('pointerdown',e=>{if(e.button)return;
 const pill=e.target.closest('.rx button');
 if(pill){const x=e.clientX,y=e.clientY,timer=setTimeout(()=>{pill.dataset.held='1';buzz();showWho(pill)},450);
  const cancel=ev=>{if(ev.type==='pointermove'&&Math.hypot(ev.clientX-x,ev.clientY-y)<10)return;clearTimeout(timer);pill.removeEventListener('pointerup',cancel);pill.removeEventListener('pointercancel',cancel);pill.removeEventListener('pointermove',cancel)};
  pill.addEventListener('pointerup',cancel);pill.addEventListener('pointercancel',cancel);pill.addEventListener('pointermove',cancel);return}
 if(e.target.closest('button,textarea,.seenline'))return;
 var msgLink=e.target.closest('a.msglink');
 if(e.target.closest('a')&&!msgLink)return;
 const row=e.target.closest('.m');if(!row)return;
 const id=+row.id.slice(3),x=e.clientX,y=e.clientY,timer=setTimeout(function(){if(msgLink)msgLink.dataset.suppress='1';buzz();openSheet(id)},500);
 const cancel=ev=>{if(ev.type==='pointermove'&&Math.hypot(ev.clientX-x,ev.clientY-y)<10)return;clearTimeout(timer);row.removeEventListener('pointerup',cancel);row.removeEventListener('pointercancel',cancel);row.removeEventListener('pointermove',cancel)};
 row.addEventListener('pointerup',cancel);row.addEventListener('pointercancel',cancel);row.addEventListener('pointermove',cancel)});
box.addEventListener('contextmenu',e=>{const pill=e.target.closest('.rx button');if(pill){e.preventDefault();showWho(pill);return}const row=e.target.closest('.m');if(!row||e.target.closest('textarea'))return;e.preventDefault();openSheet(+row.id.slice(3))});
document.getElementById('seenClose').onclick=()=>grunionsCloseSheet(document.getElementById('seenSheet'));
box.addEventListener('click',function(e){
 var map=e.target.closest&&e.target.closest('a.maplink'); if(!map) return;
 if(map.dataset.suppress){ e.preventDefault(); delete map.dataset.suppress; return; }
 e.preventDefault();
 var addr=map.getAttribute('data-map')||'';
 var apple=/iPhone|iPad|iPod/.test(navigator.userAgent||''), android=/Android/i.test(navigator.userAgent||'');
 var url=apple?('https://maps.apple.com/?daddr='+encodeURIComponent(addr)):(android?('geo:0,0?q='+encodeURIComponent(addr)):('https://www.google.com/maps/search/?api=1&query='+encodeURIComponent(addr)));
 window.open(url,'_blank','noopener');
});
box.addEventListener('click',async e=>{
 var skip=e.target.closest&&e.target.closest('a.msglink');
 if(skip&&skip.dataset.suppress){ e.preventDefault(); delete skip.dataset.suppress; return; }
 const b=e.target.closest('button,a.img');if(!b||b.dataset.save!=null||b.hasAttribute('data-cancel'))return;
 if(b.classList.contains('seenline')){if(seenInfo)openSeen(seenInfo);return}
 if(b.matches('a.img')){e.preventDefault();const lb=document.createElement('div');lb.className='lightbox';lb.innerHTML=`<img src="${b.dataset.full}" alt="">`;lb.onclick=()=>lb.remove();document.body.appendChild(lb);return}
 if(b.dataset.act){openSheet(+b.dataset.act);return}
 if(b.dataset.e){if(b.dataset.held){delete b.dataset.held;return}pollGen++;await fetch('/api/messages/'+b.dataset.m+'/react',{method:'POST',headers:{'Content-Type':'application/json','X-CSRF':CSRF},body:JSON.stringify({emoji:b.dataset.e})});poll()}});
const ta=document.getElementById('body'),file=document.getElementById('file'),prev=document.getElementById('prev');
function grow(){ta.style.height='auto';ta.style.height=Math.min(ta.scrollHeight,136)+'px'}ta.addEventListener('input',grow);
document.getElementById('attach').onclick=()=>file.click();
file.onchange=()=>{const f=file.files[0];if(!f)return;if(f.size>8*1024*1024){alert('Image is larger than 8 MB.');file.value='';return}
 prev.hidden=false;document.getElementById('prevName').textContent=f.name;document.getElementById('prevImg').src=URL.createObjectURL(f)};
document.getElementById('prevX').onclick=()=>{file.value='';prev.hidden=true};
document.getElementById('quoteX').onclick=()=>{replyTo=null;quoteBar.hidden=true};
document.getElementById('editX').onclick=()=>{editId=null;editBar.hidden=true;ta.value='';grow()};
document.getElementById('f').onsubmit=async e=>{e.preventDefault();const f=file.files[0];
 if(editId){const m=msgs[editId];if(!ta.value.trim()&&!(m&&m.image))return;
  const r=await fetch('/api/messages/'+editId,{method:'POST',headers:{'Content-Type':'application/json','X-CSRF':CSRF},body:JSON.stringify({body:ta.value})});
  const j=await r.json().catch(()=>({}));if(!r.ok){alert(j.error||'Could not save.');return}clearCompose();if(j.message)upsert(j.message,true);return}
 if(!ta.value.trim()&&!f)return;
 let r;if(f){const fd=new FormData();fd.append('body',ta.value);fd.append('image',f);if(replyTo)fd.append('reply_to',replyTo);
  r=await fetch('/api/messages?c='+CH,{method:'POST',headers:{'X-CSRF':CSRF},body:fd})}
 else r=await fetch('/api/messages?c='+CH,{method:'POST',headers:{'Content-Type':'application/json','X-CSRF':CSRF},body:JSON.stringify({body:ta.value,reply_to:replyTo})});
 if(!r.ok){const j=await r.json().catch(()=>({}));alert(j.error||'Could not send.');return}
 const epoch=window.grunionsNavEpoch|0;clearCompose();await poll();if((window.grunionsNavEpoch|0)!==epoch)return;scrollTo(0,document.body.scrollHeight)};
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
  b.onclick=function(e){e.stopPropagation(); e.preventDefault(); closeAll(); var d=document.getElementById(b.getAttribute('data-open')); var parent=b.closest('dialog'); if(parent&&parent!==d) parent.close(); if(d) d.showModal();};
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

T["lineup"] = """{% macro ev_icon() %}<svg width="28" height="28" viewBox="0 0 48 48" aria-hidden="true"><g fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="3"><path d="M8 10h32v28H8z"/><path d="M8 18h32M16 6v8M32 6v8"/></g></svg>{% endmacro %}
{% macro lineup_card(e) %}<div class="card tap tripcard" onclick="if(event.target.closest('button,a,form,input,select,textarea,label'))return;location.href='/lineup/{{ e.id }}'"><div class="evbanner cat-{{ e.slug }}">{% if e.banner %}<img src="/lineup-image/{{ e.id }}?v={{ e.banner }}" alt="">{% else %}{{ ev_icon() }}{% endif %}</div><div class=evbody>
<div class=nxcardhead><div class=tripname><a class=cardlink href="/lineup/{{ e.id }}"><div class=nxtitle>{{ e.title }}</div></a></div><span class=lineupchips>{% if e.hosting %}<span class=chip-info>{{ e.hosting }}</span>{% endif %}{% if e.subtype %}<span class=chip-info>{{ e.subtype }}</span>{% endif %}<span class=chip-info>{{ e.chip or e.category }}</span>{% if e.intent == 'considering' %}<span class=chip-info>Considering</span>{% elif e.intent == 'official' %}<span class=chip-info>Official</span>{% endif %}</span></div>
<div class=evhost>{% if e.member_event %}Member event · {% endif %}{{ e.host_line }}</div>
{% if e.where %}<div class="nxrow tripwhere">{{ glyph_pin() }}<a href="{{ e.map_href }}" target=_blank rel="noopener noreferrer">{{ e.where }}</a></div>{% endif %}
<div class=nxrow>{{ glyph_clock() }}<span>{{ e.when }}</span></div>
{% if e.description %}<div class=evnote>{{ e.description }}</div>{% endif %}
<div class="t3 sm" style="margin-top:8px">{{ e.count_line }}</div>
{% if e.roster %}<div class="t2 sm">{{ e.roster|join(', ') }}</div>{% endif %}
<form method=post action=/lineup class=pills>{{ csrf_field() }}<input type=hidden name=event_id value={{ e.id }}><input type=hidden name=back value=/lineup>
{% if e.intent == 'considering' %}
<button class="btn {{ 'btn-primary' if e.mine == 'interested' else 'btn-secondary' }}" name=action value="{{ 'clear' if e.mine == 'interested' else 'interested' }}">I'm Interested{% if e.mine == 'interested' %} ✓{% endif %}</button>
<button class="btn {{ 'btn-primary' if e.mine == 'going' else 'btn-secondary' }}" name=action value="{{ 'clear' if e.mine == 'going' else 'going' }}">Going{% if e.mine == 'going' %} ✓{% endif %}</button>
{% else %}
<button class="btn {{ 'btn-primary' if e.mine == 'going' else 'btn-secondary' }}" name=action value="{{ 'clear' if e.mine == 'going' else 'going' }}">I'm Going{% if e.mine == 'going' %} ✓{% endif %}</button>
<button class="btn {{ 'btn-primary' if e.mine == 'interested' else 'btn-secondary' }}" name=action value="{{ 'clear' if e.mine == 'interested' else 'interested' }}">Interested{% if e.mine == 'interested' %} ✓{% endif %}</button>
{% endif %}
<button class="btn {{ 'btn-primary' if e.mine == 'notgoing' else 'btn-secondary' }}" name=action value="{{ 'clear' if e.mine == 'notgoing' else 'notgoing' }}">Not going{% if e.mine == 'notgoing' %} ✓{% endif %}</button></form>
{% if e.can_review and e.intent == 'considering' %}<form method=post action="/lineup/{{ e.id }}" style="margin-top:10px">{{ csrf_field() }}<button class="btn btn-secondary full" name=action value=official>Make official</button></form>{% endif %}
{% if e.can_edit %}<a class="btn btn-secondary full" style="margin-top:10px" href="/lineup/{{ e.id }}/edit">Edit</a>{% endif %}
</div></div>{% endmacro %}
{% macro lineup_months(groups) %}{% for g in groups %}<h2 class=lineupmonth>{{ g.label }}</h2>{% for e in g.events %}{{ lineup_card(e) }}{% endfor %}{% endfor %}{% endmacro %}
<div class=lineupacts>{% if can_host_practice() %}<a class="btn btn-secondary" href="/lineup/new?mode=create">Create event</a><a class="btn btn-secondary" href="/lineup/new?mode=propose">Propose opportunity</a>{% else %}<a class="btn btn-secondary" href="/lineup/new?mode=suggest">Suggest an event</a>{% endif %}</div>
<div class=filt role=group aria-label="Category"><a class="chip{{ ' chip-active on' if not cat }}" href=/lineup>All</a>{% for c in filter_chips %}<a class="chip{{ ' chip-active on' if cat == c.slug }}" href="/lineup?cat={{ c.slug }}">{{ c.chip }}</a>{% endfor %}</div>
{% if featured %}<h2 class=lineupmonth>Featured</h2>{% for e in featured %}{{ lineup_card(e) }}{% endfor %}{% endif %}
{% if empty_public %}<p class=emptyfind>Nothing on the Lineup yet.</p>{% endif %}
{{ lineup_months(upcoming) }}
{% if past %}<details class=lineuppast><summary>Past <span class=t3>{{ past_n }}</span></summary>{{ lineup_months(past) }}</details>{% endif %}
{% if mine %}<h2>My events</h2>{% for e in mine %}<a class="card" href="/lineup/{{ e.id }}" style="display:block;color:inherit;text-decoration:none"><div class=nxtitle>{{ e.title }}</div><div class="t3 sm">{{ e.status_label }}{% if e.review_note %} · {{ e.review_note }}{% endif %}</div></a>{% endfor %}{% endif %}
{% if interested %}<h2>Interested</h2>{% for e in interested %}<a class="li" href="/lineup/{{ e.id }}" style="display:flex;color:inherit;text-decoration:none"><span class=grow>{{ e.title }}</span><span class=t3>{{ e.when }}</span></a>{% endfor %}{% endif %}"""
T["lineup_event"] = """<div class="card tripcard" style="padding:0"><div class="evbanner cat-{{ e.slug }}">{% if e.banner %}<img src="/lineup-image/{{ e.id }}?v={{ e.banner }}" alt="">{% endif %}</div>
<div class=evbody>
<div class=lineupchips style="margin-bottom:8px">{% if e.member_event %}<span class=chip-info>Member event</span>{% else %}<span class=chip-info>Club</span>{% endif %}{% if e.hosting %}<span class=chip-info>{{ e.hosting }}</span>{% endif %}{% if e.subtype %}<span class=chip-info>{{ e.subtype }}</span>{% endif %}<span class=chip-info>{{ e.category }}</span>{% if e.intent == 'considering' %}<span class=chip-info>Considering</span>{% elif e.intent == 'official' %}<span class=chip-info>Official</span>{% endif %}{% if e.status != 'published' %}<span class=chip-info>{{ e.status_label }}</span>{% endif %}</div>
<div class=profilename style="font-size:28px;font-weight:650;letter-spacing:-.3px">{{ e.title }}</div>
<div class=evhost>{{ e.host_line }}</div>
<div class=nxrow>{{ glyph_clock() }}<span>{{ e.when }}</span></div>
{% if e.where %}<div class="nxrow tripwhere">{{ glyph_pin() }}<a href="{{ e.map_href }}" target=_blank rel="noopener noreferrer">{{ e.where }}</a></div>{% endif %}
{% if e.description %}<div class=evnote>{{ e.description }}</div>{% endif %}
{% if e.details %}<div class=evnote>{{ e.details }}</div>{% endif %}
{% if e.link %}<div class=evnote><a href="{{ e.link }}" target=_blank rel="noopener noreferrer">Registration</a></div>{% endif %}
{% if e.cost %}<div class="t3 sm">About {{ e.cost }}</div>{% endif %}
{% if e.capacity %}<div class="t3 sm">{{ e.going_n }} of {{ e.capacity }} spots{% if e.wait_n %} · {{ e.wait_n }} waitlisted{% endif %}</div>{% endif %}
{% if e.reg_deadline %}<div class="t3 sm">Register by {{ e.reg_deadline }}</div>{% endif %}
{% if e.review_note and e.status in ('changes_requested', 'declined') %}<div class=note>{{ e.review_note }}</div>{% endif %}
<div class="t2 sm" style="margin-top:10px">{{ e.count_line }}</div>
{% if e.roster %}<div class="t2 sm">{{ e.roster|join(', ') }}</div>{% endif %}
{% if e.status == 'published' %}<form method=post action="/lineup/{{ e.id }}" class=pills>{{ csrf_field() }}
{% if e.intent == 'considering' %}
<button class="btn {{ 'btn-primary' if e.mine == 'interested' else 'btn-secondary' }}" name=action value="{{ 'clear' if e.mine == 'interested' else 'interested' }}">I'm Interested{% if e.mine == 'interested' %} ✓{% endif %}</button>
<button class="btn {{ 'btn-primary' if e.mine == 'going' else 'btn-secondary' }}" name=action value="{{ 'clear' if e.mine == 'going' else 'going' }}">{% if e.full and e.mine != 'going' %}Join waitlist{% else %}Going{% endif %}{% if e.mine == 'going' or e.mine == 'waitlist' %} ✓{% endif %}</button>
{% else %}
<button class="btn {{ 'btn-primary' if e.mine == 'going' else 'btn-secondary' }}" name=action value="{{ 'clear' if e.mine == 'going' else 'going' }}">{% if e.full and e.mine != 'going' %}Join waitlist{% else %}I'm Going{% endif %}{% if e.mine == 'going' or e.mine == 'waitlist' %} ✓{% endif %}</button>
<button class="btn {{ 'btn-primary' if e.mine == 'interested' else 'btn-secondary' }}" name=action value="{{ 'clear' if e.mine == 'interested' else 'interested' }}">Interested{% if e.mine == 'interested' %} ✓{% endif %}</button>
{% endif %}
<button class="btn {{ 'btn-primary' if e.mine == 'notgoing' else 'btn-secondary' }}" name=action value="{{ 'clear' if e.mine == 'notgoing' else 'notgoing' }}">Not going{% if e.mine == 'notgoing' %} ✓{% endif %}</button></form>{% endif %}
{% if e.can_review and e.intent == 'considering' %}<form method=post action="/lineup/{{ e.id }}" style="margin-top:10px">{{ csrf_field() }}<button class="btn btn-primary full" name=action value=official>Make official</button></form>{% endif %}
</div></div>"""
T["approvals"] = """<h1>Approvals</h1>
{% for e in queue %}<div class="card tripcard"><div class="evbanner cat-{{ e.slug }}">{% if e.banner %}<img src="/lineup-image/{{ e.id }}?v={{ e.banner }}" alt="">{% endif %}</div><div class=evbody>
<div class=nxtitle>{{ e.title }}</div>
<div class="t3 sm">{{ e.status_label }} · {{ e.category }}{% if e.subtype %} · {{ e.subtype }}{% endif %}</div>
<div class=evhost>{{ e.host_line }}</div>
<div class=nxrow>{{ glyph_clock() }}<span>{{ e.when }}</span></div>
{% if e.where %}<div class=nxrow>{{ glyph_pin() }}<span>{{ e.where }}</span></div>{% endif %}
{% if e.description %}<div class=evnote>{{ e.description }}</div>{% endif %}
{% if e.submitted %}<div class="t3 sm">Submitted {{ e.submitted }}</div>{% endif %}
{% if e.review_note %}<div class=note>{{ e.review_note }}</div>{% endif %}
<form method=post action=/admin/approvals style="margin-top:12px">{{ csrf_field() }}<input type=hidden name=event_id value={{ e.id }}>
<button class="btn btn-primary full" name=action value=approve>Approve &amp; Publish</button>
<label style="margin-top:12px">Note<textarea name=note rows=2 placeholder="Needed for changes or a decline"></textarea></label>
<div class=row><button class="btn btn-secondary" name=action value=changes>Request Changes</button><button class="btn btn-danger" name=action value=decline>Decline</button></div>
</form></div></div>{% else %}<p class=emptyfind>No events waiting for review.</p>{% endfor %}
<details class=card><summary>Categories</summary><div class=body>
{% for c in categories %}<form method=post action=/admin/approvals class=li>{{ csrf_field() }}<input type=hidden name=action value=category_toggle><input type=hidden name=category_id value={{ c.id }}><span class=grow>{{ c.name }} · {{ c.chip }}{% if not c.active %} · hidden{% endif %}</span><button class="btn btn-secondary">{{ 'Show' if not c.active else 'Hide' }}</button></form>{% endfor %}
<form method=post action=/admin/approvals>{{ csrf_field() }}<input type=hidden name=action value=category_add>
<label>Name<input name=name required></label><label>Filter label<input name=chip required placeholder="Social"></label>
<label><input type=checkbox name=member_ok value=1 checked> Members can suggest</label>
<label><input type=checkbox name=intent_ok value=1> Team intent</label>
<label><input type=checkbox name=hosting_ok value=1> Away / Hosting</label>
<button class="btn btn-primary full">Add category</button></form></div></details>"""
T["lineup_edit"] = """<form id=eventForm method=post action="{{ action }}" enctype=multipart/form-data>{{ csrf_field() }}
<input type=hidden name=mode value="{{ values.mode or mode }}">
<button type=submit name=action value=save style="position:absolute;left:-9999px;width:1px;height:1px;overflow:hidden" tabindex=-1>{{ save_label or 'Save' }}</button>
<label>Category<select name=category id=lineCat>{% for c in categories %}<option value="{{ c.slug }}" data-hosting="{{ c.hosting_ok }}" data-intent="{{ c.intent_ok }}" {% if values.category == c.slug %}selected{% endif %}>{{ c.name }}</option>{% endfor %}</select></label>
<label id=lineSub>Subtype<select name=subtype id=lineSubSel><option value="">None</option>{% for name in subtypes.get(values.category, []) %}<option value="{{ name }}" {% if values.subtype == name %}selected{% endif %}>{{ name }}</option>{% endfor %}</select></label>
<label id=lineHost>Away / Hosting<select name=hosting><option value=Away {% if values.hosting != 'Hosting' %}selected{% endif %}>Away</option><option value=Hosting {% if values.hosting == 'Hosting' %}selected{% endif %}>Hosting</option></select></label>
{% if organizer %}<label id=lineIntent>Team intent<select name=team_intent><option value=considering {% if values.team_intent != 'official' %}selected{% endif %}>Considering</option><option value=official {% if values.team_intent == 'official' %}selected{% endif %}>Official</option></select></label>
<input type=hidden name=official value=0><label id=lineOfficial><input type=checkbox name=official value=1 {% if values.official == '1' or mode == 'create' or mode == 'propose' %}checked{% endif %}> Official club event</label>{% endif %}
<label>Title<input name=title value="{{ values.title }}" required autocomplete=off></label>
<div class=row><label>Date<input type=date name=date value="{{ values.date }}" required></label><label>Start<input type=time name=start_time value="{{ values.start_time or '09:00' }}" required></label></div>
<label>Location / meeting point<input name=location value="{{ values.location }}" required autocomplete=off></label>
<label>Short description<textarea name=description rows=3 required>{{ values.description }}</textarea></label>
<details class=moredetails><summary>More details</summary>
<label>Subtype is set above. End date<input type=date name=end_date value="{{ values.end_date }}"></label>
<label>End time<input type=time name=end_time value="{{ values.end_time }}"></label>
<label>City<input name=city value="{{ values.city }}" autocomplete=off></label>
<label>Banner<input type=file name=banner accept="image/jpeg,image/png,image/gif,image/webp,image/heic,image/heif,.heic"></label>
<label>Link<input name=link value="{{ values.link }}" inputmode=url autocomplete=off placeholder="https://"></label>
<label>Capacity<input name=capacity inputmode=numeric value="{{ values.capacity }}" autocomplete=off></label>
<label>Estimated cost<input name=cost value="{{ values.cost }}" autocomplete=off></label>
<label>Register by<input type=date name=reg_deadline value="{{ values.reg_deadline }}"></label>
<label>Extra details<textarea name=details rows=3>{{ values.details }}</textarea></label>
{% if organizer %}<label><input type=checkbox name=featured value=1 {% if values.featured == '1' %}checked{% endif %}> Feature on the Lineup</label>{% endif %}
</details>
{% if organizer and not event_id %}<button class="btn btn-secondary full" name=action value=draft>Save draft</button>{% endif %}
{% if show_cancel %}<button class="btn btn-danger full" name=action value=cancel onclick="return confirm('Cancel this event?')">Cancel event</button>{% endif %}
{% if show_delete %}<button class="btn btn-danger full" name=action value=delete onclick="return confirm('Delete this event?')">Delete event</button>{% endif %}
</form>
<script>(function(){
 var cat=document.getElementById('lineCat'), sub=document.getElementById('lineSub'), sel=document.getElementById('lineSubSel');
 var host=document.getElementById('lineHost'), intent=document.getElementById('lineIntent'), official=document.getElementById('lineOfficial');
 var subtypes={{ subtypes|tojson }}, current={{ values.subtype|tojson }}, mode={{ mode|tojson }};
 function sync(){
  var opt=cat.options[cat.selectedIndex], slug=cat.value;
  var names=subtypes[slug]||[], html='<option value="">None</option>';
  names.forEach(function(n){html+='<option'+(n===current?' selected':'')+'>'+n.replace(/</g,'')+'</option>'});
  sel.innerHTML=html; if(current && names.indexOf(current)<0){var o=document.createElement('option'); o.textContent=current; o.selected=true; sel.appendChild(o);}
  var showHost=opt&&opt.getAttribute('data-hosting')==='1'; host.hidden=!showHost;
  var showIntent=opt&&opt.getAttribute('data-intent')==='1';
  if(intent) intent.hidden=!showIntent;
  if(mode==='propose'&&showIntent){cat.value='travel';}
 }
 cat.addEventListener('change', function(){current=sel.value; sync()}); sync();
})();</script>"""
T["series_edit"] = """<form id=seriesForm method=post action="{{ action }}">{{ csrf_field() }}
<div class=checks role=group aria-label="Weekdays"><div class="t3 xs">Weekdays</div>
{% for value, label in values.labels %}<label style="margin:8px 0"><input type=checkbox name=weekday value="{{ value }}" {% if value in values.weekdays %}checked{% endif %}>{{ label }}</label>{% endfor %}</div>
<div class=row><label>Start<input type=time name=start value="{{ values.start }}" required></label><label>End<input type=time name=end value="{{ values.end }}" required></label></div>
<label>Location<input name=location value="{{ values.location }}" required autocomplete=off></label>
<div class=row><label>Starts<input type=date name=start_date value="{{ values.start_date }}" required></label><label>Ends (optional)<input type=date name=end_date value="{{ values.end_date }}"></label></div>
<p class="t3 sm">Dates are added through the end date, or for the next eight weeks when there is no end date.</p>
<div class=checks role=group aria-label="Coaches"><div class="t3 xs">Coaches</div>
<label style="margin:0 0 8px"><input type=radio name=lead value="" {% if not values.lead %}checked{% endif %}>No lead</label>
{% for c in coach_choices %}<div style="padding:8px 0;border-top:1px solid var(--line)">
<label style="margin:0"><input type=checkbox name=coach value="{{ c.id }}" {% if c.id in values.coaches %}checked{% endif %}>{{ display_first(c) }} {{ c.last }}</label>
<label style="margin:8px 0 0"><input type=radio name=lead value="{{ c.id }}" {% if values.lead == c.id|string %}checked{% endif %}>Lead</label>
</div>{% else %}<p class="t3 sm">No coaches on the coaching list yet.</p>{% endfor %}</div>
</form>
{% if skips %}<div class=seclabel>Skipped dates</div><div class=list>{% for day in skips %}<form method=post action="{{ action }}" class=li>{{ csrf_field() }}<input type=hidden name=action value=unskip><input type=hidden name=date value="{{ day }}"><span class=grow>{{ fmt_d(day) }}</span><button class="btn btn-secondary" type=submit>Undo skip</button></form>{% endfor %}</div>{% endif %}"""
T["practices"] = """<p class="t2 sm" style="margin-top:0">Tue · Marina HS &nbsp;·&nbsp; Fri · Westminster HS &nbsp;·&nbsp; 7–8:30 PM</p>
{% for x in data %}{% set p = x.p %}<div class="card tap" id=p{{p.id}} data-pid={{p.id}} {% if p.cancelled %}style="opacity:.55"{% endif %} onclick="if(event.target.closest('button,a,form,input,select,textarea,label,dialog'))return;location.href='/practices/{{p.id}}'">
<a class=cardlink href="/practices/{{p.id}}">
<div class=nxcardhead><div class=nxtitle>Water Polo Practice</div></div>
<div class=nxmain><div class=datetile><span class=pdate>{% if x.unseen %}<span class=badge data-seen={{p.id}}>{{ x.unseen if x.unseen < 100 else '99+' }}</span>{% endif %}</span><span class=wd>{{ weekday_abbr(p.date) }}</span><span class=dn>{{ day_num(p.date) }}</span><span class=mo>{{ month_abbr(p.date) }}</span></div>
<div class="grow schedrows"><div class=nxrow>{{ glyph_clock() }}<span>{{ fmt_span(p.start, p.end) }}</span></div>
<div class=nxrow>{{ glyph_pin() }}<span>{{ p.location }}</span></div>
<div class=nxrow>{{ glyph_people() }}<span>{{ x.going|length }} going{% if x.coach_names %} · Coaches: {{ x.coach_names|join(', ') }}{% endif %}</span></div></div></div>
{% if p.cancelled %}{{ st('bad','Cancelled') }}{% if p.cancel_reason %}<div class="t3 sm">{{ p.cancel_reason }}</div>{% endif %}{% endif %}
{% if p.note %}<div class=nxnote>{{p.note}}</div>{% endif %}
{% if p.coach_note %}<div class=nxnote>{{ p.coach_note }} · {{ p.coach_note_by }} · {{ fmt_stamp(p.coach_note_at) }}</div>{% endif %}</a>
{% if not p.cancelled %}<form method=post action=/practices class=pills>{{csrf_field()}}<input type=hidden name=pid value={{p.id}}>
<button class="btn {{ 'btn-primary' if x.mine == 1 else 'btn-secondary' }}" name=action value="{{ 'clear' if x.mine==1 else 'going' }}">I'm going{% if x.mine==1 %} ✓{% endif %}</button>
<button class="btn {{ 'btn-primary' if x.mine == 0 else 'btn-secondary' }}" name=action value="{{ 'clear' if x.mine==0 else 'notgoing' }}">I'm not going{% if x.mine==0 %} ✓{% endif %}</button></form>
{% endif %}</div>{% endfor %}
{% if me().is_admin %}<details class=card><summary>Add a practice</summary><form method=post class=body>{{csrf_field()}}<label>Date<input type=date name=date required></label>
<div class=row><label>Start<input type=time name=start value=19:00></label><label>End<input type=time name=end value=20:30></label></div>
<label>Location<input name=location required></label><label>Note<input name=note></label>
<div class=repeatblock><label class=repeatline><input type=checkbox name=repeat value=1> Repeat</label>
<div class=repeatopts><div class=checks role=group aria-label="Weekdays"><div class="t3 xs">Weekdays</div>
<label style="margin:8px 0"><input type=checkbox name=weekday value=0> Mon</label><label style="margin:8px 0"><input type=checkbox name=weekday value=1> Tue</label><label style="margin:8px 0"><input type=checkbox name=weekday value=2> Wed</label><label style="margin:8px 0"><input type=checkbox name=weekday value=3> Thu</label><label style="margin:8px 0"><input type=checkbox name=weekday value=4> Fri</label><label style="margin:8px 0"><input type=checkbox name=weekday value=5> Sat</label><label style="margin:8px 0"><input type=checkbox name=weekday value=6> Sun</label></div>
<label>Ends (optional)<input type=date name=end_date></label>
<p class="t3 sm">Starts on the date above. Occurrences fall on the weekdays you pick, through the end date, or for the next eight weeks.</p>
{% if coach_choices %}<div class=checks role=group aria-label="Coaches"><div class="t3 xs">Coaches</div>{% for c in coach_choices %}<label style="margin:8px 0"><input type=checkbox name=coach value="{{ c.id }}">{{ display_first(c) }} {{ c.last }}</label>{% endfor %}</div>{% endif %}
</div></div>
<button class="btn btn-primary full" name=action value=add>Add practice</button></form></details>{% endif %}""" + _PRACTICE_JS

T["practice"] = """{% set p = x.p %}
{% if p.location %}<section class="homemap cardmap banner" id=practiceMap aria-label="Map of {{ p.location }}"></section>
<script>
(function(){
 var pins={{ pins|tojson }};
 function start(){ var el=document.getElementById('practiceMap'); if(el&&window.grunionsMountMap) grunionsMountMap(el,{pins:pins,mode:'card'}); }
 if(window.grunionsMountMap) start(); else document.addEventListener('DOMContentLoaded', start);
})();
</script>{% endif %}
<div class=profilehero>
<div class=profilename>{{ practice_title(p) }}</div>
<p class=pracemeta>{{ fmt_card_date(p.date) }} · {{ fmt_clock(p.start) }} – {{ fmt_clock(p.end) }}</p>
{% if p.location %}<p class=pracemeta>{{ p.location }}</p>{% endif %}
<div class=pracestatus>{% if p.cancelled %}{{ st('bad','Cancelled') }}{% else %}{{ st('ok','Scheduled') }}{% endif %}</div>
{% if p.cancelled and p.cancel_reason %}<p class="t3 sm" style="margin:6px 0 0">{{ p.cancel_reason }}</p>{% endif %}
{% if me().is_admin and p.cancelled and p.skipped %}<form method=post action="/practices/{{ p.id }}" style="margin-top:12px">{{ csrf_field() }}<input type=hidden name=pid value={{ p.id }}><input type=hidden name=back value=page><button class="btn btn-secondary" name=action value=unskip>Undo skip</button></form>
{% elif me().is_admin and p.cancelled %}<form method=post action="/practices/{{ p.id }}" style="margin-top:12px">{{ csrf_field() }}<input type=hidden name=pid value={{ p.id }}><input type=hidden name=back value=page><button class="btn btn-secondary" name=action value=restore>Undo cancel</button></form>{% endif %}
{% if me().is_admin and p.series_id and not p.cancelled %}<div style="display:flex;gap:10px;margin-top:12px"><form method=post action="/practices/{{ p.id }}">{{ csrf_field() }}<input type=hidden name=pid value={{ p.id }}><input type=hidden name=back value=page><button class="btn btn-secondary" name=action value=skip onclick="return confirm('Skip this date?')">Skip this date</button></form><a class="btn btn-secondary" href="/practices/series/{{ p.series_id }}">Edit series</a></div>{% endif %}
<div class="stats trio">
<div class=stattile><b>{{ x.going|length }}</b><span>Going</span></div>
<div class=stattile><b>{{ x.coaches|length }}</b><span>Coaches</span></div>
<div class=stattile><b>{{ x.checked|length }}</b><span>Checked in</span></div>
</div>
</div>
{% if editing %}
<form id=practiceForm method=post action="/practices/{{ p.id }}" class=card style="margin-top:16px" enctype=multipart/form-data>{{ csrf_field() }}<input type=hidden name=pid value={{ p.id }}><input type=hidden name=back value=page>
<label>Date<input type=date name=date value="{{ p.date }}" required></label>
{% if p.series_id %}<label>Apply changes to<select name=series_scope><option value=once>Only this date</option><option value=following>This and following</option></select></label>{% endif %}
<div class=row><label>Start<input type=time name=start value="{{ p.start }}" required></label><label>End<input type=time name=end value="{{ p.end }}" required></label></div>
<label>Location / address<input name=location value="{{ p.location or '' }}" required></label>
<label>Notes<textarea name=note>{{ p.note or '' }}</textarea></label>
<div class="t3 xs" style="margin:4px 0 8px">After-practice social</div>
{{ social_fields(p) }}
{{ message_fields(p) }}
<label>Practice image<input type=file name=image accept="image/jpeg,image/png,image/gif,image/webp,image/heic,image/heif,.heic"></label>
{% if p.image %}<label><input type=checkbox name=image_clear value=1> Remove image</label>{% endif %}
<div class=checks role=group aria-label="Coaches"><div class="t3 xs">Coaches</div>
<label style="margin:0 0 8px"><input type=radio name=lead value="" {% if not x.lead_id %}checked{% endif %}>No lead</label>
{% for c in coach_choices %}<div style="padding:8px 0;border-top:1px solid var(--line)">
<label style="margin:0"><input type=checkbox name=coach value="{{ c.id }}" {% if c.id in x.coach_ids %}checked{% endif %}>{{ display_first(c) }} {{ c.last }} {{ coach_tag(c) }}</label>
<label style="margin:8px 0 0"><input type=radio name=lead value="{{ c.id }}" {% if c.id == x.lead_id %}checked{% endif %}>Lead</label>
<label style="margin:8px 0 0">Focus group<input name="focus-{{ c.id }}" list=focusGroups value="{{ x.focuses.get(c.id, '') }}" placeholder="Beginners, Intermediate, Advanced, Goalies" autocomplete=off></label>
</div>{% else %}<p class="t3 sm">No coaches yet. Add someone on People.</p>{% endfor %}</div>
<datalist id=focusGroups><option value=Beginners><option value=Intermediate><option value=Advanced><option value=Goalies></datalist>
<label>Today's plan<textarea name=coaching_plan rows=4>{{ p.coaching_plan or '' }}</textarea></label>
<input type=hidden name=plan_fields value=1>
</form>
{% if me().is_admin %}<div class=seclabel>Manage</div><div class=list>
<button type=button class="li rowbtn" data-open="assign{{ p.id }}">Assign coaches</button>
<a class="li rowbtn" href="/admin?date={{ p.date }}">Check in</a>
{% if p.cancelled %}<form method=post action="/practices/{{ p.id }}">{{ csrf_field() }}<input type=hidden name=pid value={{ p.id }}><input type=hidden name=back value=page><button class="li rowbtn" name=action value=restore>Undo cancel</button></form>
{% else %}<button type=button class="li rowbtn" data-open="cancel{{ p.id }}">Send cancellation</button>{% endif %}
<form method=post action="/practices/{{ p.id }}">{{ csrf_field() }}<input type=hidden name=pid value={{ p.id }}><input type=hidden name=back value=page><button class="li rowbtn" name=action value=duplicate>Duplicate practice</button></form>
<button type=button class="li rowbtn" data-copy="{{ app_base() }}/practices/{{ p.id }}">Copy link</button>
<button type=button class="li rowbtn" data-open="delete{{ p.id }}">Delete practice</button>
</div>{% endif %}
{% else %}
{% if not p.cancelled %}<form method=post action="/practices/{{ p.id }}" class=pills style="margin-top:8px">{{ csrf_field() }}<input type=hidden name=pid value={{ p.id }}><input type=hidden name=back value=page>
<button class="btn {{ 'btn-primary' if x.mine == 1 else 'btn-secondary' }}" name=action value="{{ 'clear' if x.mine==1 else 'going' }}">I'm going{% if x.mine==1 %} ✓{% endif %}</button>
<button class="btn {{ 'btn-primary' if x.mine == 0 else 'btn-secondary' }}" name=action value="{{ 'clear' if x.mine==0 else 'notgoing' }}">I'm not going{% if x.mine==0 %} ✓{% endif %}</button></form>{% endif %}
<div class=seclabel>Details</div>
<div class=list>
<div class="li prow"><span class=k>Time</span><span class=v>{{ fmt_clock(p.start) }} – {{ fmt_clock(p.end) }}</span></div>
<div class="li prow"><span class=k>Location</span><span class=v>{{ p.address or p.location or '—' }}</span></div>
{% if p.location %}<a class="li prow chevrow" {% if pins %}data-directions="{{ pins[0].lat }},{{ pins[0].lng }}"{% endif %} href="https://www.google.com/maps/dir/?api=1&amp;destination={{ ((pins[0].lat|string ~ ',' ~ pins[0].lng|string) if pins else (p.address or p.location))|urlencode }}" target=_blank rel=noopener><span>Directions</span><span class=nxchev aria-hidden=true>›</span></a>{% endif %}
{% if p.note %}<div class="li prow"><span class=k>Notes</span><span class=v>{{ p.note }}</span></div>{% endif %}
{% if p.coach_note %}<div class="li prow"><span class=k>Coach note</span><span class=v>{{ p.coach_note }} · {{ p.coach_note_by }}{% if p.coach_note_at %} · {{ fmt_stamp(p.coach_note_at) }}{% endif %}</span></div>{% endif %}
</div>
<div class=seclabel>After-practice social</div>
<div class=list><div class=li>{% if social_line(p) %}{{ social_icon() }}{% endif %}<div class=grow>
{% if social_line(p) %}<div>{{ social_line(p) }}{% if p.social_time %} · {{ fmt_t(p.social_time) }}{% endif %}</div>
<div class="t3 sm">{{ x.social_n }} joining</div>
{% if p.social_note %}<div class="t2 sm">{{ p.social_note }}</div>{% endif %}
{% if p.social_address %}{% if p.social_address.lower().startswith('http://') or p.social_address.lower().startswith('https://') %}<div class="sm"><a href="{{ p.social_address }}" target=_blank rel=noopener>Map</a></div>{% else %}<div class="t2 sm">{{ p.social_address }} · <a href="https://www.google.com/maps/dir/?api=1&amp;destination={{ p.social_address|urlencode }}" target=_blank rel=noopener>Map</a></div>{% endif %}{% endif %}
{% else %}<span class=t3>None yet.</span>{% endif %}
</div>{% if me().is_admin or is_staff() %}<button type=button class="btn btn-secondary" data-open="social{{ p.id }}">{{ 'Edit' if social_line(p) else 'Add' }}</button>{% endif %}</div></div>
<div class=seclabel>Coaches</div>
<div class=list>{% for c in x.coaches %}{% set ce = coach_eligibility(c) %}<div class=li><div class=grow><div style="display:flex;align-items:center;gap:8px;min-width:0"><span class=ell>{% if me().is_admin or is_staff() %}<a href="/admin/member/{{ c.id }}" style="color:inherit;text-decoration:none">{{ display_first(c) }} {{ c.last }}</a>{% else %}{{ display_first(c) }} {{ c.last }}{% endif %}</span>{% if c.is_lead %}<span class="chip-info" style="margin:0">Lead</span>{% endif %}</div>{% if can_host_practice() and c.focus %}<div class="t3 sm">{{ c.focus }}</div>{% endif %}</div>{% if ce.eligible %}{{ coach_tag(c) }}{% else %}<span class="st st-warn coach-elig">{{ ce.text or 'Not eligible' }}</span>{% endif %}</div>{% else %}<div class=li><span class=t3>No coaches assigned.</span></div>{% endfor %}</div>
{% if can_host_practice() %}
<div class=seclabel style="display:flex;align-items:center;gap:8px">Coaching plan <span class="chip-info" style="margin:0">Coaches only</span></div>
{% if plan_editing %}<form id=practiceForm method=post action="/practices/{{ p.id }}">{{ csrf_field() }}<input type=hidden name=pid value={{ p.id }}><input type=hidden name=back value=page><input type=hidden name=plan_fields value=1>
<div class=list>
<div class=li><label class=prefedit style="width:100%;margin:0">Today's plan<textarea name=coaching_plan rows=4>{{ p.coaching_plan or '' }}</textarea></label></div>
{% if x.coaches %}<div class=li><label style="margin:0"><input type=radio name=lead value="" {% if not x.lead_id %}checked{% endif %}>No lead</label></div>{% endif %}
{% for c in x.coaches %}<div class=li><div class=grow>
<label style="margin:0"><input type=radio name=lead value="{{ c.id }}" {% if c.is_lead %}checked{% endif %}>{{ display_first(c) }} {{ c.last }}</label>
<label style="margin:8px 0 0">Focus group<input name="focus-{{ c.id }}" list=focusGroups value="{{ c.focus or '' }}" placeholder="Beginners, Intermediate, Advanced, Goalies" autocomplete=off></label>
</div></div>{% endfor %}
</div>
<datalist id=focusGroups><option value=Beginners><option value=Intermediate><option value=Advanced><option value=Goalies></datalist>
</form>
{% else %}<div class=list>
<div class="li prow" style="align-items:flex-start"><span class=k>Today's plan</span><span class=v style="white-space:pre-wrap">{{ p.coaching_plan or '—' }}</span></div>
{% for c in x.coaches %}<div class="li prow"><span class=k>{{ display_first(c) }} {{ c.last }}{% if c.is_lead %} · Lead{% endif %}</span><span class=v>{{ c.focus or '—' }}</span></div>{% else %}<div class=li><span class=t3>Assign a coach to set a focus group.</span></div>{% endfor %}
</div>{% endif %}
{% endif %}
<div class=seclabel>Going</div>
<div class=list>{% for r in x.going %}<div class=li><div class=grow>{% if me().is_admin or is_staff() %}<a href="/admin/member/{{ r.id }}" style="color:inherit;text-decoration:none">{{ display_first(r) }} {{ r.last }}</a>{% else %}{{ display_first(r) }} {{ r.last }}{% endif %}</div></div>{% else %}<div class=li><span class=t3>No one yet.</span></div>{% endfor %}</div>
<div class=seclabel>Can't make it</div>
<div class=list>{% for r in x.notgoing %}<div class=li><div class=grow>{{ display_first(r) }} {{ r.last }}</div></div>{% else %}<div class=li><span class=t3>No one yet.</span></div>{% endfor %}</div>
<div class=seclabel>Checked in</div>
<div class=list>{% for r in x.checked %}<div class=li><div class=grow>{{ display_first(r) }} {{ r.last }}</div></div>{% else %}<div class=li><span class=t3>No one yet.</span></div>{% endfor %}</div>
{% endif %}
{% if me().is_admin or is_staff() %}{{ practice_extra_dialogs(p, 'page') }}{% endif %}
{% if is_staff() and not me().is_admin %}
<dialog class=modal id=hostedit{{ p.id }}><div class=sheet><h2 style="margin:0 0 12px">Edit practice</h2>
<div class=list>
<button type=button class="li rowbtn" data-open="social{{ p.id }}">After-practice social</button>
<button type=button class="li rowbtn" data-open="message{{ p.id }}">Coach message</button>
<button type=button class="li rowbtn" data-open="image{{ p.id }}">Practice image</button>
</div></div></dialog>
{% endif %}
{% if me().is_admin %}
<dialog class=modal id=assign{{ p.id }}><div class=sheet><h2 style="margin:0 0 12px">Assign coaches</h2>
<form method=post action="/practices/{{ p.id }}">{{ csrf_field() }}<input type=hidden name=pid value={{ p.id }}><input type=hidden name=back value=page>
<div class=checks role=group aria-label="Coaches">{% for c in coach_choices %}<label><input type=checkbox name=coach value="{{ c.id }}" {% if c.id in x.coach_ids %}checked{% endif %}>{{ display_first(c) }} {{ c.last }} {{ coach_tag(c) }}</label>
{% else %}<p class="t3 sm">No coaches yet. Add someone on People.</p>{% endfor %}</div>
<div class=row><button class="btn btn-primary" name=action value=assign>Save</button><button type=button class="btn btn-secondary" onclick="this.closest('dialog').close()">Cancel</button></div></form></div></dialog>
<dialog class=modal id=cancel{{ p.id }}><div class=sheet><h2 style="margin:0 0 8px">Send cancellation</h2>
<p class="t2 sm">Members get an email and a push that include this reason.</p>
<form method=post action="/practices/{{ p.id }}">{{ csrf_field() }}<input type=hidden name=pid value={{ p.id }}><input type=hidden name=back value=page>
<label>Reason<textarea name=reason required></textarea></label>
<button class="btn btn-danger full" name=action value=cancel>Confirm</button></form></div></dialog>
<dialog class=modal id=delete{{ p.id }}><div class=sheet><h2 style="margin:0 0 8px">Delete this practice?</h2>
<p class="t2 sm">{{ fmt_d(p.date) }}, {{ fmt_t(p.start) }}–{{ fmt_t(p.end) }} at {{ p.location }}.</p>
<form method=post action="/practices/{{ p.id }}">{{ csrf_field() }}<input type=hidden name=pid value={{ p.id }}>
<div class=row><button class="btn btn-danger" name=action value=delete>Delete practice</button><button type=button class="btn btn-secondary" onclick="this.closest('dialog').close()">Cancel</button></div></form></div></dialog>
{% endif %}""" + _PRACTICE_JS

_CHEV_L = '<svg width="20" height="20" viewBox="0 0 24 24" aria-hidden="true"><path d="M15 6 9 12l6 6" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>'
_CHEV_R = '<svg width="20" height="20" viewBox="0 0 24 24" aria-hidden="true"><path d="M9 6l6 6-6 6" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>'
_CAL_I = '<svg width="18" height="18" viewBox="0 0 48 48" aria-hidden=true><g fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="3"><path d="M22 25h4m6 0h4m-20 0h-4m10 10h4m6 0h4m-20 0h-4m-.997-26.437c-1.137.11-2.12.225-2.952.336c-2.199.293-3.877 1.948-4.192 4.144C3.451 15.887 3 20.41 3 26.5s.451 10.614.859 13.458c.315 2.196 1.993 3.85 4.192 4.144c3.13.417 8.38.898 15.949.898s12.818-.48 15.949-.898c2.199-.293 3.877-1.948 4.192-4.144c.408-2.844.859-7.368.859-13.458s-.451-10.613-.859-13.457c-.315-2.196-1.993-3.851-4.192-4.144a82 82 0 0 0-2.952-.336M29 8.074A164 164 0 0 0 24 8q-2.693.002-5 .074"/><path d="M29.013 9.27c.043 2.08 1.409 3.694 3.489 3.726a33 33 0 0 0 .996 0c2.08-.032 3.446-1.646 3.489-3.726a61 61 0 0 0 0-2.54c-.043-2.08-1.409-3.694-3.489-3.726a32 32 0 0 0-.996 0c-2.08.032-3.446 1.646-3.489 3.726a61 61 0 0 0 0 2.54m-18 0c.043 2.08 1.409 3.694 3.489 3.726a33 33 0 0 0 .996 0c2.08-.032 3.446-1.646 3.489-3.726a61 61 0 0 0 0-2.54c-.043-2.08-1.409-3.694-3.489-3.726a32 32 0 0 0-.996 0c-2.08.032-3.446 1.646-3.489 3.726a61 61 0 0 0 0 2.54"/></g></svg>'
T["admin"] = ADMIN_NAV + """
{%- set qbit -%}{% if q %}&amp;q={{ q|urlencode }}{% endif %}{%- endset -%}
{%- set fbit -%}{% if filt != 'going' %}&amp;filt={{ filt }}{% endif %}{%- endset -%}
<div class=checkbar>
<form class="row noprint" method=get action=/admin style="margin-bottom:0"><div class=calpick id=calPick data-date="{{date}}" data-q="{{q}}" data-filt="{{ '' if filt=='going' else filt }}" data-dates='{{ days|tojson }}'>
{% if prev_d %}<a class=calnav href="/admin?date={{prev_d}}{{ fbit }}{{ qbit }}" aria-label="Previous practice">""" + _CHEV_L + """</a>{% else %}<span class=calnav aria-disabled=true aria-label="Previous practice">""" + _CHEV_L + """</span>{% endif %}
<button type=button class=calbtn id=calOpen aria-haspopup=dialog aria-expanded=false aria-controls=calPop>""" + _CAL_I + """<span>{{ fmt_d(date).replace(' ', ', ', 1) }}</span></button>
{% if next_d %}<a class=calnav href="/admin?date={{next_d}}{{ fbit }}{{ qbit }}" aria-label="Next practice">""" + _CHEV_R + """</a>{% else %}<span class=calnav aria-disabled=true aria-label="Next practice">""" + _CHEV_R + """</span>{% endif %}
<div class=calpop id=calPop hidden role=dialog aria-label="Choose a practice"><div class=calhead>
<button type=button class=calmonth id=calPrevM aria-label="Previous month">""" + _CHEV_L + """</button><div class=lbl id=calLabel>{{month.label}}</div>
<button type=button class=calmonth id=calNextM aria-label="Next month">""" + _CHEV_R + """</button></div>
<div class=calwd><span>S</span><span>M</span><span>T</span><span>W</span><span>T</span><span>F</span><span>S</span></div>
<div class=calgrid id=calGrid>{% for c in month.cells %}{% if c is none %}<span class=calday></span>{% elif c.has %}<a class="calday{{' on' if c.on}}" href="/admin?date={{c.iso}}{{ fbit }}{{ qbit }}">{{c.day}}</a>{% else %}<span class=calday aria-disabled=true>{{c.day}}</span>{% endif %}{% endfor %}</div></div></div>
<input type=hidden name=date value="{{date}}">{% if filt != 'going' %}<input type=hidden name=filt value="{{filt}}">{% endif %}<input name=q value="{{q}}" placeholder="Search players..." style="margin:0"></form>
<p class=checkprog>Checked in {{ n }} / Going {{ going|length }}</p>
</div>
{% if pr %}<a class=schedlink href="/practices/{{ pr.id }}?from=admin"><div class=grow><h1>{{loc}}</h1><p class="t2 sm">{% if pr %}{{ fmt_span(pr.start, pr.end) }}{% else %}no practice scheduled{% endif %}{% if coach_names %} · Coaches: {{ coach_names|join(', ') }}{% endif %}{% if n %} · {{ n }} checked in{% endif %}</p></div><span class=schedchev aria-hidden=true><svg width="20" height="20" viewBox="0 0 24 24"><path d="M9 6l6 6-6 6" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg></span></a>{% else %}<h1 style="margin:8px 0 4px">{{loc}}</h1>
<p class="t2 sm" style="margin-top:0">no practice scheduled{% if n %} · {{ n }} checked in{% endif %}</p>{% endif %}
<div class=filt role=group aria-label="RSVP">
<a class="chip{{ ' chip-active on' if filt=='going' }}" href="/admin?date={{ date }}{% if q %}&amp;q={{ q|urlencode }}{% endif %}">Going ({{ going|length }})</a>
{% if n_not %}<a class="chip{{ ' chip-active on' if filt=='not' }}" href="/admin?date={{ date }}&amp;filt=not{% if q %}&amp;q={{ q|urlencode }}{% endif %}">Not Going ({{ n_not }})</a>{% else %}<button type=button class=chip disabled aria-disabled=true>Not Going (0)</button>{% endif %}
{% if n %}<a class="chip{{ ' chip-active on' if filt=='in' }}" href="/admin?date={{ date }}&amp;filt=in{% if q %}&amp;q={{ q|urlencode }}{% endif %}">Checked in ({{ n }})</a>{% else %}<button type=button class=chip disabled aria-disabled=true>Checked in (0)</button>{% endif %}
</div>
{% macro ci(r) %}
<div class="li cirow" data-rsvp="{{ 'going' if r.going==1 else ('not' if r.going==0 else 'none') }}" data-checked="{{ 1 if r.cid else 0 }}"><a class=ci-name href="/admin/member/{{ r.id }}">
{% if r.photo %}<span class="avatar ciav"><img src="/avatar/{{ r.id }}?v={{ r.photo }}" alt="" width="40" height="40"></span>{% else %}<span class="avatar ciav">{{ initials(r) }}</span>{% endif %}
<span class=grow style="min-width:0"><span class=ell style="display:block;font-weight:500">{{ display_first(r) }} {{ r.last }}</span>{{ checkin_status(r) }}</span></a>
<form method=post>{{csrf_field()}}<input type=hidden name=member_id value={{r.id}}><input type=hidden name=date value={{date}}><input type=hidden name=q value="{{q}}"><input type=hidden name=filt value="{{filt}}">
{% if r.cid %}<button class="btn btn-secondary" name=action value=undo title="Undo check-in">✓ Checked in</button>{% else %}<button class="btn btn-primary" {% if not clearance(r).ok %}data-confirm="Not cleared — check in anyway?"{% endif %}>Check in</button>{% endif %}</form></div>{% endmacro %}
{% if q and ((filt=='not' and not not_going) or (filt=='in' and not checked) or (filt=='going' and not going and not rest)) %}<p class=emptyfind>No players match “{{ q }}”.</p>{% endif %}
{% if filt == 'not' %}
<h2>Not Going <span class=t3>{{ n_not }}</span></h2>
<div class=list>{% for r in not_going %}{{ ci(r) }}{% else %}<div class=li><span class=t3>No one yet.</span></div>{% endfor %}</div>
{% elif filt == 'in' %}
<h2>Checked in <span class=t3>{{ n }}</span></h2>
<div class=list>{% for r in checked %}{{ ci(r) }}{% else %}<div class=li><span class=t3>No one yet.</span></div>{% endfor %}</div>
{% else %}
<h2>Going <span class=t3>{{going|length}}</span></h2>
<div class=list>{% for r in going %}{{ ci(r) }}{% else %}<div class=li><span class=t3>No one yet.</span></div>{% endfor %}</div>
<h2>Everyone else <span class=t3>{{rest|length}}</span></h2>
<div class=list>{% for r in rest %}{{ ci(r) }}{% else %}<div class=li><span class=t3>No one yet.</span></div>{% endfor %}</div>
{% endif %}
<script>
if(!window.grunionsConfirm){window.grunionsConfirm=1;
 document.addEventListener('click',function(e){var b=e.target.closest&&e.target.closest('[data-confirm]');if(!b||b.dataset.ok)return;e.preventDefault();if(window.confirm(b.getAttribute('data-confirm'))){b.dataset.ok='1';b.click()}});
}
</script>
<script>
(function(){
var root=document.getElementById('calPick'); if(!root) return;
var pop=document.getElementById('calPop'), openBtn=document.getElementById('calOpen'), grid=document.getElementById('calGrid'), label=document.getElementById('calLabel');
var dates=[]; try{dates=JSON.parse(root.getAttribute('data-dates')||'[]')}catch(err){dates=[]}
var set={}; dates.forEach(function(d){set[d]=1});
var q=root.getAttribute('data-q')||'', filt=root.getAttribute('data-filt')||'', selected=root.getAttribute('data-date')||'', shown=selected.slice(0,7);
function pad(n){return (n<10?'0':'')+n}
function href(iso){return '/admin?date='+iso+(filt?'&filt='+encodeURIComponent(filt):'')+(q?'&q='+encodeURIComponent(q):'')}
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
<p class="t2 sm" style="margin-top:-8px">Bring in a Sport:80 export, or download the roster and attendance.</p>
<h2>Import</h2>
<div class=card><ol class="t2 sm" style="margin:0;padding-left:18px;line-height:1.7">
<li>Log in at <a href=https://usawp.sport80.com>usawp.sport80.com</a> and switch to the Grunions club profile.</li>
<li>Members → Smart Lists → Edit Columns: name, email, membership status, member number, valid until, plus SafeSport / background columns.</li>
<li>Actions → Export Report, then upload the emailed file here.</li></ol>
<form method=post action=/transfer enctype=multipart/form-data style="margin-top:14px">{{csrf_field()}}<input type=file name=file accept=".csv,.xlsx" style="padding:11px 14px;height:44px"><button class="btn btn-primary full" style="margin-top:12px">Import</button></form>
{% if stats %}<div class=note style="margin-top:16px">Read {{stats.rows}} rows · updated {{stats.matched}} members · {{stats.req_updates or 0}} compliance items · {{stats.unmatched|length}} roster rows not in the app</div>
{% if stats.unmatched %}<details style="margin-top:12px"><summary>Not signed up in the app</summary><div class=body>{% for u in stats.unmatched %}<div class="kv t2">{{u}}</div>{% endfor %}</div></details>{% endif %}
{% else %}<p class="t3 sm" style="margin:12px 0 0">No file imported yet.</p>{% endif %}
<p class="t3 xs" style="margin:12px 0 0">Matching uses email first, then exact legal first and last name. An optional Preferred First Name column is stored as the name shown in the app and is not used for matching. A Membership Type or Member Type column adds USAWP coaches to the coaching list.</p></div>
<h2>Export</h2>
<div class=card><h2 style="margin:0 0 8px">Members</h2>
<p class="t2 sm">Legal name, preferred name, phone, role, clearance, USAWP number, membership, SafeSport, background screening, trial dates, and attendance.</p>
<a class="btn btn-secondary full" href=/members.csv>Download members CSV</a></div>
<div class=card><h2 style="margin:0 0 8px">Practices and attendance</h2>
<form method=get action=/export/practices.csv>
<div class=row><label>Start<input type=date name=start value="{{start}}" required></label><label>End<input type=date name=end value="{{end}}" required></label></div>
<button class="btn btn-secondary full" name=detail value=0>Download practices CSV</button>
<button class="btn btn-secondary full" style="margin-top:10px" name=detail value=1>Download detailed attendance CSV</button></form>
<p class="t3 sm" style="margin:12px 0 0">Practices is one row per practice, with the assigned coaches, a coach count, and how many of those coaches are coach-eligible. Detailed attendance is one row per member per practice, with RSVP and check-in.</p></div>
{% if sheet_on %}<div class=card><h2 style="margin:0 0 8px">Google Sheet</h2>
<p class="t2 sm">{% if sheet_status.at %}Last sync {{sheet_status.at}} PT · {{sheet_status.label}}{% else %}Not synced yet{% endif %}{% if sheet_status.detail and not sheet_status.ok %} · {{sheet_status.detail}}{% endif %}</p>
<p class="t3 sm">Members, Practices, and Attendance stay in sync after changes. A full rewrite also runs daily.</p>
<form method=post action=/export/sheet>{{csrf_field()}}<button class="btn btn-secondary full">Sync to Google Sheet now</button></form></div>{% endif %}"""

T["members"] = ADMIN_NAV + """<div class=pagetitle><h1>People</h1><a class="t2 sm" href=/members.csv>Export CSV</a></div>
{{ growth }}
<div class=peoplebar>
<form method=get action=/members><input name=q value="{{q}}" placeholder="Search people..." autocomplete=off>{% if view != 'members' %}<input type=hidden name=view value="{{view}}">{% endif %}</form>
<div class=fchips>
<a href="/members{% if q %}?q={{ q|urlencode }}{% endif %}" class="chip{{ ' chip-active on' if view=='members' }}">All</a>
<a href="/members?view=coaches{% if q %}&amp;q={{ q|urlencode }}{% endif %}" class="chip{{ ' chip-active on' if view=='coaches' }}">Coaches</a>
<a href="/members?view=admins{% if q %}&amp;q={{ q|urlencode }}{% endif %}" class="chip{{ ' chip-active on' if view=='admins' }}">Admins</a>
<a href="/members?view=expiring{% if q %}&amp;q={{ q|urlencode }}{% endif %}" class="chip{{ ' chip-active on' if view=='expiring' }}">Expiring</a>
<a href="/members?view=uncleared{% if q %}&amp;q={{ q|urlencode }}{% endif %}" class="chip{{ ' chip-active on' if view=='uncleared' }}">Not cleared</a>
<a href="/members?view=referees{% if q %}&amp;q={{ q|urlencode }}{% endif %}" class="chip{{ ' chip-active on' if view=='referees' }}">Referees</a>
</div>
{% if view == 'admins' %}<p class="t2 sm peoplesum">{{ n_admins }} admin{{ 's' if n_admins != 1 }}</p>
{% elif view != 'coaches' and view != 'referees' %}<p class="t2 sm peoplesum">{% if view=='expiring' %}Expiring or expired{% elif view=='uncleared' %}Not cleared to play{% else %}{{rows|length}} total · {% for s,v in c.items() %}{{v}} {{s}}{{' · ' if not loop.last}}{% endfor %}{% endif %}</p>{% endif %}
</div>
{% macro people_sub(r) %}{% set tw = trial_window(r) %}{% set cl = clearance(r) %}{% set ex = expiry_notes(r, cl) %}{% set dl = days_left(r.usawp_valid_until) %}{% set ns = namespace(tone='ok', label='Cleared', detail='') %}
{% if tw and tw.active and r.usawp_status != 'verified' and not ex.membership %}{% set ns.tone = 'warn' %}{% set ns.label = 'Trial' %}{% set ns.detail = trial_left_phrase(tw) %}
{% elif tw and tw.expired and r.usawp_status != 'verified' %}{% set ns.tone = 'bad' %}{% set ns.label = 'Trial ended ' ~ tw.ends %}
{% elif not cl.ok %}{% set ns.tone = 'bad' %}{% set ns.label = 'Not cleared' %}
{% elif dl is not none and dl <= EXPIRING_DAYS %}{% set ns.tone = 'warn' %}{% set ns.label = 'Expiring soon' %}{% endif %}
{% if not ns.detail %}{% if dl is not none and dl >= 0 and dl <= EXPIRING_DAYS %}{% if dl == 0 %}{% set ns.detail = 'expires today' %}{% elif dl == 1 %}{% set ns.detail = 'expires in 1 day' %}{% else %}{% set ns.detail = 'expires in ' ~ dl ~ ' days' %}{% endif %}{% elif r.usawp_valid_until %}{% set ns.detail = 'thru ' ~ fmt_long(r.usawp_valid_until) %}{% endif %}{% endif %}
<span class="psub ell">{{ st(ns.tone, ns.label) }}{% if ns.detail %} · {{ ns.detail }}{% endif %} · {{ r.visits }} practice{{ '' if r.visits == 1 else 's' }}</span>{% endmacro %}
{% macro prow(r, kind) %}<div class=li><a class=ci-name href="/admin/member/{{ r.id }}">{% if r.photo %}<span class="avatar ciav"><img src="/avatar/{{ r.id }}?v={{ r.photo }}" alt="" width="40" height="40"></span>{% else %}<span class="avatar ciav">{{ initials(r) }}</span>{% endif %}<span class=grow style="min-width:0"><span class=ell style="display:block;font-weight:500">{{ display_first(r) }} {{ r.last }}</span>{{ people_sub(r) }}
<div class=eligs>{% if r.is_admin %}<span class=chip-info>Admin</span>{% endif %}{% set chip = coach_row_expiry(r) %}{% set ce = coach_eligibility(r) %}{% if r.role=='coach' or r.id in listed or ce.eligible or ce.text %}<span class="chip-info{{ ' ' ~ chip.tone if chip.tone else '' }}">Coach{% if chip.date %} · expires {{ chip.date }}{% endif %}</span>{% endif %}{% if r.id in referees %}<span class=chip-info>Referee</span>{% endif %}{{ referee_tag(r) }}</div>
</span></a>
<span class=more><button type=button class=morebtn aria-label="Actions for {{display_first(r)}} {{r.last}}" aria-haspopup=menu aria-expanded=false><svg width="22" height="22" viewBox="0 0 48 48" aria-hidden=true><g fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="3"><path d="M3 24a21 21 0 1 0 42 0a21 21 0 1 0-42 0"/><path d="M20.5 24a3.5 3.5 0 1 0 7 0a3.5 3.5 0 1 0-7 0m-12 0a3.5 3.5 0 1 0 7 0a3.5 3.5 0 1 0-7 0m24 0a3.5 3.5 0 1 0 7 0a3.5 3.5 0 1 0-7 0"/></g></svg></button>
<div class=menu hidden role=menu>
{% if kind == 'members' %}
{% if r.is_admin %}{% if n_admins<=1 or r.email in boot %}<button type=button disabled title="{% if n_admins<=1 %}Last admin{% else %}Set by ADMIN_EMAIL{% endif %}">Remove admin</button>{% else %}<form method=post>{{csrf_field()}}<input type=hidden name=member_id value={{r.id}}><input type=hidden name=list_view value="{{ view }}"><input type=hidden name=q value="{{q}}"><button name=action value=remove_admin>Remove admin</button></form>{% endif %}{% else %}<form method=post>{{csrf_field()}}<input type=hidden name=member_id value={{r.id}}><input type=hidden name=list_view value="{{ view }}"><input type=hidden name=q value="{{q}}"><button name=action value=make_admin>Make admin</button></form>{% endif %}
{% if r.id in listed %}<form method=post>{{csrf_field()}}<input type=hidden name=member_id value={{r.id}}><input type=hidden name=list_view value="{{ view }}"><input type=hidden name=q value="{{q}}"><button name=action value=remove_coaching>Remove from coaches</button></form>{% else %}<form method=post>{{csrf_field()}}<input type=hidden name=member_id value={{r.id}}><input type=hidden name=list_view value="{{ view }}"><input type=hidden name=q value="{{q}}"><button name=action value=add_coaching>Add to coaches</button></form>{% endif %}
{% if r.id in referees %}<form method=post>{{csrf_field()}}<input type=hidden name=member_id value={{r.id}}><input type=hidden name=list_view value="{{ view }}"><input type=hidden name=q value="{{q}}"><button name=action value=remove_referee>Remove from referees</button></form>{% else %}<form method=post>{{csrf_field()}}<input type=hidden name=member_id value={{r.id}}><input type=hidden name=list_view value="{{ view }}"><input type=hidden name=q value="{{q}}"><button name=action value=add_referee>Add to referees</button></form>{% endif %}
{% elif kind == 'coaches' %}
{% if r.role=='coach' %}<form method=post>{{csrf_field()}}<input type=hidden name=member_id value={{r.id}}><input type=hidden name=list_view value=coaches><input type=hidden name=q value="{{q}}"><button name=action value=remove_coach>Remove active coach</button></form>{% else %}<form method=post>{{csrf_field()}}<input type=hidden name=member_id value={{r.id}}><input type=hidden name=list_view value=coaches><input type=hidden name=q value="{{q}}"><button name=action value=make_coach>Make active coach</button></form>{% endif %}
<form method=post>{{csrf_field()}}<input type=hidden name=member_id value={{r.id}}><input type=hidden name=list_view value=coaches><input type=hidden name=q value="{{q}}"><button name=action value=remove_coaching>Remove from coaches</button></form>
{% elif kind == 'eligible' %}
<form method=post>{{csrf_field()}}<input type=hidden name=member_id value={{r.id}}><input type=hidden name=list_view value=coaches><input type=hidden name=q value="{{q}}"><button name=action value=add_coaching>Add to coaches</button></form>
{% if r.role=='coach' %}<form method=post>{{csrf_field()}}<input type=hidden name=member_id value={{r.id}}><input type=hidden name=list_view value=coaches><input type=hidden name=q value="{{q}}"><button name=action value=remove_coach>Remove active coach</button></form>{% else %}<form method=post>{{csrf_field()}}<input type=hidden name=member_id value={{r.id}}><input type=hidden name=list_view value=coaches><input type=hidden name=q value="{{q}}"><button name=action value=make_coach>Make active coach</button></form>{% endif %}
{% elif kind == 'admins' %}
{% if n_admins<=1 or r.email in boot %}<button type=button disabled title="{% if n_admins<=1 %}Last admin{% else %}Set by ADMIN_EMAIL{% endif %}">Remove admin</button>{% else %}<form method=post>{{csrf_field()}}<input type=hidden name=member_id value={{r.id}}><input type=hidden name=list_view value=admins><input type=hidden name=q value="{{q}}"><button name=action value=remove_admin>Remove admin</button></form>{% endif %}
{% elif kind == 'referees' %}
<form method=post>{{csrf_field()}}<input type=hidden name=member_id value={{r.id}}><input type=hidden name=list_view value=referees><input type=hidden name=q value="{{q}}"><button name=action value=remove_referee>Remove from referees</button></form>
{% elif kind == 'ref_eligible' %}
<form method=post>{{csrf_field()}}<input type=hidden name=member_id value={{r.id}}><input type=hidden name=list_view value=referees><input type=hidden name=q value="{{q}}"><button name=action value=add_referee>Add to referees</button></form>
{% endif %}
</div></span></div><!--endrow-->{% endmacro %}
<div class=people>
{% macro lettered(kind) %}{% set ns = namespace(letter='') %}{% for r in rows %}{% set letter = ((r.last or '?')[:1])|upper %}{% if letter != ns.letter %}{% if ns.letter %}</div></div>{% endif %}<div class=lgroup><h3 class=alpha>{{ letter }}</h3><div class="list loose">{% set ns.letter = letter %}{% endif %}{{ prow(r, kind) }}{% else %}<div class="list loose"><div class=li><span class=t3>{% if q %}No people match “{{ q }}”.{% else %}No one here.{% endif %}</span></div></div>{% endfor %}{% if ns.letter %}</div></div>{% endif %}{% endmacro %}
{% if view == 'coaches' %}
<h2>Coaches <span class=t3>{{ rows|selectattr('id','in',listed)|list|length }}</span></h2>
<div class="list loose">{% for r in rows if r.id in listed %}{{ prow(r, 'coaches') }}{% else %}<div class=li><span class=t3>{% if q %}No people match “{{ q }}”.{% else %}No one on the coaching list yet.{% endif %}</span></div>{% endfor %}</div>
<h2>Coach eligible <span class=t3>{{ rows|selectattr('id','in',coach_ids)|rejectattr('id','in',listed)|list|length }}</span></h2>
<div class="list loose">{% for r in rows if r.id in coach_ids and r.id not in listed %}{{ prow(r, 'eligible') }}{% else %}<div class=li><span class=t3>{% if q %}No people match “{{ q }}”.{% else %}No one waiting.{% endif %}</span></div>{% endfor %}</div>
{% elif view == 'referees' %}
<h2>Referees <span class=t3>{{ rows|selectattr('id','in',referees)|list|length }}</span></h2>
<div class="list loose">{% for r in rows if r.id in referees %}{{ prow(r, 'referees') }}{% else %}<div class=li><span class=t3>{% if q %}No people match “{{ q }}”.{% else %}No one on the referee list yet.{% endif %}</span></div>{% endfor %}</div>
<h2>Referee eligible <span class=t3>{{ rows|selectattr('id','in',ref_ids)|rejectattr('id','in',referees)|list|length }}</span></h2>
<div class="list loose">{% for r in rows if r.id in ref_ids and r.id not in referees %}{{ prow(r, 'ref_eligible') }}{% else %}<div class=li><span class=t3>{% if q %}No people match “{{ q }}”.{% else %}No one waiting.{% endif %}</span></div>{% endfor %}</div>
{% elif view == 'admins' %}
{{ lettered('admins') }}
{% else %}
{{ lettered('members') }}
{% endif %}
</div>
<script>
(function(){var bar=document.querySelector('.peoplebar'); function pin(){ if(bar) document.documentElement.style.setProperty('--peoplepin', bar.offsetHeight+'px'); } pin(); window.addEventListener('resize', pin);})();
</script>
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

T["expiring"] = ADMIN_NAV + """<div class=expage><h1>Expiring</h1>
<p class="t2 sm" style="margin-top:-8px">Membership, SafeSport, and other dated items. Tap a person to open them.</p>
<form class="row noprint" method=get action=/expiring style="align-items:center;margin-bottom:8px"><label class="t2 sm" style="flex:0 0 auto;margin:0">Window (days)<input name=days type=number min=1 value={{days}} onchange=this.form.submit() style="margin:6px 0 0;height:44px;width:96px"></label></form>
{% for key, label in [('expired','Expired'),('within_7','Next 7 days'),('within_%d'%days,'Next %d days'%days)] %}<h2 class=egroup>{{label}} <span class=t3>{{rep[key]|length}}</span></h2>
<div class=list>{% for r in rep[key] %}<div class=li><a class=grow href="/admin/member/{{ r.id }}" style="color:inherit;text-decoration:none;min-width:0"><div style="display:flex;align-items:center;gap:8px;min-width:0"><span class=ell style="font-weight:500;flex:1">{{display_first(r)}} {{r.last}}</span>
<span class="chip-info daybadge"><span class="dot {{ 'bad' if r.days_left < 0 else ('warn' if r.days_left <= 7 else '') }}" aria-hidden=true></span>{% if r.days_left < 0 %}{{ -r.days_left }}d ago{% elif r.days_left == 0 %}Today{% else %}{{ r.days_left }}d left{% endif %}</span></div>
<div class="t3 xs">{{ r.item }} · {{ fmt_long(r.usawp_valid_until) }}</div></a>
<a class="btn btn-secondary" href="/admin/member/{{ r.id }}?edit=1">Recheck</a></div>{% else %}<div class=li><span class=t3>None</span></div>{% endfor %}</div>{% endfor %}
<form method=post style="margin-top:20px">{{csrf_field()}}<input type=hidden name=action value=ask_all><input type=hidden name=days value="{{days}}"><button class="btn btn-primary full">Ask Grunions to recheck all</button></form>
<p class="t3 sm" style="margin-top:10px">Asks Grunions to look up everyone listed. Daily report: <a href=/api/expiring>/api/expiring</a>.</p>
</div>"""

T["requirements_page"] = ADMIN_NAV + """<h1>Rules</h1>
<p class="t2 sm" style="margin-top:-8px">Cleared to play means a current USAWP membership and current SafeSport.</p>
{% if not reqs %}<p class=emptyfind>No rules yet.</p>{% endif %}
{% for q in reqs %}<details class=card><summary><span>{{q.name}}</span><span class="t3 sm" style="margin-left:auto;margin-right:10px">{{q.applies_to}}{{'' if q.active else ' · off'}}</span></summary>
<form method=post class=body>{{csrf_field()}}<input type=hidden name=id value={{q.id}}>
<div class=row><label>Applies to<select name=applies_to>{% for o in ['all','athlete','coach'] %}<option {{'selected' if q.applies_to==o}}>{{o}}</option>{% endfor %}</select></label>
<label>Import keywords<input name=keywords value="{{q.keywords or ''}}"></label></div>
<label><input type=checkbox name=expires {{'checked' if q.expires}}>Has an expiration date</label><label><input type=checkbox name=active {{'checked' if q.active}}>Active</label>
<button class="btn btn-primary full" name=action value=save>Save</button></form></details>{% endfor %}
<details class=card><summary>Add a rule</summary><form method=post class=body>{{csrf_field()}}<label>Name<input name=name placeholder="CPR / First Aid"></label>
<div class=row><label>Applies to<select name=applies_to><option>all</option><option>athlete</option><option>coach</option></select></label><label>Keywords<input name=keywords placeholder="cpr,firstaid"></label></div>
<label><input type=checkbox name=expires checked>Has an expiration date</label><button class="btn btn-secondary full" name=action value=add>Add</button></form></details>"""

T["qr_page"] = ADMIN_NAV + """<div style="text-align:center"><h1>Join QR</h1>
<p class="t2 sm" style="margin-top:-8px">Anyone who scans this joins the team.</p>
{% if u %}<div style="background:#fff;border-radius:16px;padding:18px;display:inline-block;margin-top:8px"><img src=/qr.svg alt="Sign-up QR code" width="240" height="240" style="width:min(64vw,240px);height:auto;display:block"></div>
<p class="t3 sm" id=joinLink style="margin-top:12px;word-break:break-all">{{u}}</p>
<button class="btn btn-primary full noprint" type=button id=copyJoin>Copy link</button>
<button class="btn btn-secondary full noprint" type=button id=shareJoin style="margin-top:8px">Share</button>
<button class="btn btn-secondary noprint" type=button onclick="print()" style="margin-top:8px">Print</button>
{% else %}<p class=emptyfind>The join link is not ready yet.</p>{% endif %}</div>
<script>
(function(){
 var link=document.getElementById('joinLink'), copy=document.getElementById('copyJoin'), share=document.getElementById('shareJoin');
 if(!link||!copy) return;
 function text(){return (link.textContent||'').trim()}
 function copied(){copy.textContent='Copied'; setTimeout(function(){copy.textContent='Copy link'},1600)}
 function fallback(value){var ta=document.createElement('textarea'); ta.value=value; document.body.appendChild(ta); ta.select(); try{document.execCommand('copy')}catch(e){} ta.remove()}
 copy.onclick=function(){
  var value=text();
  if(navigator.clipboard&&navigator.clipboard.writeText) navigator.clipboard.writeText(value).then(copied, function(){fallback(value); copied()});
  else {fallback(value); copied()}
 };
 if(share) share.onclick=function(){
  var value=text();
  if(navigator.share) navigator.share({title:'Join the Grunions', url:value}).catch(function(){});
  else copy.click();
 };
})();
</script>"""
