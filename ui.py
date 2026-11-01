"""Templates (Jinja strings) for the Grunions app. Restrained dark UI: one surface, gray text, one blue accent.

Colors, type, spacing, and radius are defined in regulars/foundation.css.
"""
import os
_FOUNDATION_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "regulars", "foundation.css")
with open(_FOUNDATION_PATH, encoding="utf-8") as _foundation_file:
    FOUNDATION = _foundation_file.read()

BASE = """<!doctype html><html lang=en style="background:#090D0B;color-scheme:dark"><head>
<meta charset=utf-8><meta name=color-scheme content=dark><meta name=theme-color content="#090D0B">
<meta name=viewport content="width=device-width,initial-scale=1,viewport-fit=cover">
<meta name=apple-mobile-web-app-capable content=yes><link rel=manifest href=/manifest.webmanifest>
<link rel=icon href=/static/icons/favicon-32.png sizes=32x32 type=image/png><link rel=apple-touch-icon href=/static/icons/apple-touch-icon-180.png>
<title>Grunions</title>
<style>{{ leaflet_css|safe }}</style>
<style>{{ foundation_css|safe }}
html,body{background:var(--color-bg);color:var(--color-text)}html{color-scheme:dark}
@view-transition{navigation:auto}
::view-transition{background:#090D0B}
::view-transition-group(root){animation:none;background:#090D0B}
::view-transition-image-pair(root){isolation:auto}
::view-transition-old(root),::view-transition-new(root){animation:none;animation-duration:0s;mix-blend-mode:normal}
::view-transition-group(grunions-nav),::view-transition-old(grunions-nav),::view-transition-new(grunions-nav){animation:none;mix-blend-mode:normal}
::view-transition-group(grunions-header){animation:none;overflow:clip}
::view-transition-old(grunions-header){display:none}
::view-transition-new(grunions-header){animation:none;mix-blend-mode:normal}
[hidden]{display:none!important}
*{box-sizing:border-box}html{-webkit-text-size-adjust:100%}
body{margin:0;background:var(--color-bg);color:var(--t1);font:var(--type-body-1-size)/var(--type-body-1-leading) var(--font-sans);overflow-wrap:break-word}
a{color:var(--t1)}main{max-width:640px;margin:0 auto;padding:20px 20px calc(var(--nav-clear) + 16px + env(safe-area-inset-bottom))}
header{display:flex;align-items:center;justify-content:space-between;padding:16px 20px;max-width:640px;margin:0 auto}
.brand{font-family:var(--font-display);font-weight:700;letter-spacing:-.02em;color:var(--t1);text-decoration:none}header a.sub{color:var(--t3);font-size:14px;text-decoration:none}
h1,h2,h3,.nxtitle,.datetile .dn{font-family:var(--font-display)}h1{font-size:var(--type-t1-size);line-height:var(--type-t1-line);font-weight:var(--type-t1-weight);letter-spacing:var(--type-title-1-tracking);margin:4px 0 20px}h2{font-size:var(--type-t3-size);line-height:var(--type-t3-line);font-weight:var(--type-t3-weight);margin:32px 0 12px}
p{margin:0 0 12px}.t2{color:var(--t2)}.t3{color:var(--t3)}.sm{font-size:var(--type-b2-size);line-height:var(--type-b2-line)}.xs{font-size:var(--type-b4-size);line-height:var(--type-b4-line)}
.card{background:var(--color-surface);border:1px solid var(--color-border);border-radius:var(--radius-card);padding:var(--space-5);margin:0 0 var(--space-3)}
.card.tap{cursor:pointer}a.cardlink,a.goingcount{color:inherit;text-decoration:none}a.cardlink{display:block;flex:1;min-width:0}
.nxhead{display:flex;align-items:center;justify-content:space-between;gap:12px}
.nxmain{display:flex;align-items:center;gap:12px}
.datetile{width:64px;height:64px;border-radius:var(--radius-control);background:var(--surface2);display:flex;flex-direction:column;align-items:center;justify-content:center;flex:none}
.datetile .wd,.datetile .mo{font-size:11px;font-weight:700;letter-spacing:.6px;color:var(--t3);line-height:1}
.datetile .dn{font-size:var(--type-t2-size);font-weight:var(--type-t2-weight);line-height:1.1;margin-top:2px}
.datetile .mo{margin-top:2px}
.nxcardhead{display:flex;align-items:center;justify-content:space-between;gap:12px;margin-bottom:12px}
.schedrows .nxrow{font-size:15px}.schedrows .nxrow:first-child{margin-top:0}
.nxtitle{font-size:var(--type-t4-size);font-weight:var(--type-t4-weight);line-height:var(--type-t4-line)}
.nxchev{color:var(--t3);font-size:22px;line-height:1;flex:none}
.nxnote{margin-top:10px;color:var(--t3);font-size:13px;line-height:1.4}
.pills{display:flex;gap:var(--space-2);margin-top:var(--space-4)}
.rsvprow{flex-wrap:nowrap}
.rsvprow .btn{white-space:nowrap;padding:0 8px;min-width:0}
.rsvpcheck{width:16px;height:16px;flex:none;display:block}
.pills .btn{flex:1;min-width:0}
.pills button.on{background:var(--accent);color:var(--color-on-primary)}
.nxdiv{height:1px;background:var(--line);margin:14px 0}
.nxsocial{display:flex;align-items:center;gap:12px}
.nxicon{width:40px;height:40px;border-radius:12px;background:var(--surface2);display:flex;align-items:center;justify-content:center;flex:none;color:var(--color-icon)}
.nxicon svg{display:block}
.joinpill{flex:none}
header.homehead{position:sticky;top:0;left:0;right:0;z-index:8;display:flex;width:100%;max-width:none;background:var(--color-bg);align-items:center;gap:var(--space-3);height:calc(76px + env(safe-area-inset-top));min-height:calc(76px + env(safe-area-inset-top));box-sizing:border-box;padding:calc(var(--space-4) + env(safe-area-inset-top)) var(--space-5) var(--space-4);border:0;box-shadow:none;view-transition-name:grunions-header}
header.homehead .headmain{flex:1;min-width:0;height:44px;display:flex;align-items:center;padding-right:0}
header.homehead h1{margin:0;height:var(--type-t2-line);font-size:var(--type-t2-size);line-height:var(--type-t2-line);font-weight:var(--type-t2-weight);letter-spacing:-.02em}
header.homehead .headtabs{flex:1;min-width:0;height:44px;margin:0;padding:0;align-items:center}
header.homehead a.avatar{position:static;flex:none;align-self:center;z-index:1}
header.homehead .headplus{position:relative;flex:none;align-self:center;width:44px;height:44px;margin-right:calc(12px - var(--space-3));border-radius:50%;background:var(--color-raised);color:var(--color-text);display:inline-flex;align-items:center;justify-content:center;text-decoration:none}
header.homehead .headplus svg{width:24px;height:24px;display:block}
header.homehead .headplus::after{content:"";position:absolute;inset:-2px}
a.avatar,button.avatar,span.avatar{width:44px;height:44px;min-width:44px;max-width:44px;min-height:44px;max-height:44px;border-radius:50%;padding:0;background:var(--surface2);color:var(--t1);font-size:14px;font-weight:650;letter-spacing:.2px;overflow:hidden;flex:0 0 44px;border:1px solid var(--line);display:inline-flex;align-items:center;justify-content:center}
a.avatar img,button.avatar img,span.avatar img{width:44px;height:44px;max-width:44px;max-height:44px;object-fit:cover;border-radius:50%;display:block;flex-shrink:0}
.profhead{display:flex;align-items:center;gap:14px;margin:0 0 16px}.profhead .avatar{width:64px;height:64px;font-size:20px}
.nextcard{padding:0;overflow:hidden}
.nextcard .nxbody{padding:16px 16px 0}.nextcard .nxtitle{font-size:var(--type-t3-size);line-height:var(--type-t3-line);font-weight:var(--type-t3-weight)}
.nextcard .nxcardhead{margin:0 0 2px}
.nextcard .nxcardhead .cardlink{flex:1;min-width:0}
a.usawpchip{display:inline-flex;align-items:center;gap:6px;margin-left:auto;color:var(--t2);font-size:13px;font-weight:500;line-height:1.2;text-decoration:none;white-space:nowrap;flex:none}
a.usawpchip .usawpok{width:16px;height:16px;flex:none;color:var(--color-status-cleared)}
a.usawpchip.warn,a.usawpchip.bad{color:var(--color-text)}
.numcard .nxtitle{font-size:17px;line-height:1.3}
#membership{scroll-margin-top:72px}
.pimg{position:relative;line-height:0}.pimg img{width:100%;height:200px;object-fit:cover;display:block}
.nxbadge{position:absolute;top:12px;left:12px;background:var(--color-surface);color:var(--color-text);border:1px solid var(--color-badge-border);border-radius:var(--radius-chip);padding:5px 10px;font-size:11px;font-weight:700;letter-spacing:.8px;line-height:1}
.nxrow{display:flex;align-items:center;gap:var(--space-2);margin-top:var(--space-2);color:var(--t1);font-size:15px}
.nxrow+.nxrow{margin-top:var(--space-meta)}
.nxglyph{width:16px;height:16px;flex:none;color:var(--color-icon)}
.nextcard .pills{margin:14px 16px 0}.nextcard .pills:last-child{margin-bottom:16px}
.nextcard .nxdiv{margin:14px 16px}.nextcard .nxsocial{padding:0 16px 16px}
.homemap{height:300px;margin:0 -20px 16px;background:var(--color-map);position:relative;z-index:1}
.homemap.cardmap{height:220px;margin:0 0 12px;border-radius:14px;overflow:hidden;cursor:pointer;touch-action:pan-y}
.homemap.banner{height:220px;margin:0 -20px 0;border-radius:0;overflow:hidden;position:relative}
.homemap.banner::after{content:"";position:absolute;left:0;right:0;bottom:0;height:84px;background:linear-gradient(transparent,var(--color-bg));z-index:450;pointer-events:none}
.homemap.still{height:180px;margin:0;border-radius:0;cursor:default;pointer-events:none}
.evhero{height:220px;margin:0 -20px 0;position:relative;overflow:hidden;background:var(--color-map)}
.evhero img{width:100%;height:100%;object-fit:cover;display:block}
.evhero::after{content:"";position:absolute;left:0;right:0;bottom:0;height:84px;background:linear-gradient(transparent,var(--color-bg));pointer-events:none}
.eventtag{color:var(--t2);font-size:15px;font-weight:400;margin:2px 0 0}
.profilehero .eventtag{text-align:center}
.loccard{padding:0}
a.locrow,span.locrow{display:flex;align-items:center;gap:12px;padding:14px 16px;color:inherit;text-decoration:none;width:100%}
.li.evdescrow{flex-direction:column;align-items:stretch;gap:2px}
.li.evdescrow .textlink{align-self:flex-start;padding:4px 0 0}
.clamp{display:-webkit-box;-webkit-line-clamp:4;-webkit-box-orient:vertical;overflow:hidden}
.clamp.open{display:block;-webkit-line-clamp:unset}
a.reglink{color:var(--accent);text-decoration:none;font-weight:600}
.bannerprev{margin:0 0 10px;border-radius:var(--radius-card,14px);overflow:hidden;background:var(--surface);aspect-ratio:3/2}
.bannerprev img{width:100%;height:100%;object-fit:cover;display:block}
.bannerpick .btn{position:relative;overflow:hidden}
body.practicepage main{padding-top:0}
.homemap.leaflet-container,.homemap .leaflet-container{background:var(--color-map)}
.homemap .leaflet-tile-pane{filter:grayscale(1) invert(1) contrast(.9) brightness(.82);opacity:0;transition:opacity .45s ease}
.homemap.tiles .leaflet-tile-pane{opacity:1}
.homemap .leaflet-control-attribution{background:var(--color-scrim);color:var(--color-text-secondary);font-size:10px;max-width:70%}
.homemap .leaflet-control-attribution a{color:var(--color-icon)}
.homemap .leaflet-bar a,.homemap .leaflet-bar a:hover{background:var(--color-surface-2);color:var(--color-text);border-bottom-color:var(--color-border)}
.homemap .leaflet-marker-icon.mpin{background:var(--color-selected);border:3px solid var(--color-bg);border-radius:50%;box-shadow:0 0 0 1px var(--color-selected)}
.homemap .leaflet-marker-icon.mpin.social{background:var(--color-bg);border:3px solid var(--color-selected);box-shadow:none}
body.homefull header.homehead{position:sticky;top:0;z-index:8;background:transparent}
body.homefull header.homehead.solid{background:var(--color-bg)}
body.homefull main{position:relative;z-index:1;padding:0 16px calc(var(--nav-clear) + 16px + env(safe-area-inset-bottom))}
body.homefull .homemap{position:fixed;top:0;left:0;right:0;bottom:0;height:auto;margin:0;z-index:0;border-radius:0;pointer-events:none}
body.homefull .homedock{position:relative;left:auto;right:auto;bottom:auto;z-index:2;max-height:none;overflow:visible;pointer-events:auto;margin:0;padding:0 0 12px;min-height:calc(100dvh - var(--homehead, 76px) - var(--homealerts, 0px) - var(--nav-clear) - env(safe-area-inset-bottom) - var(--peek, 24px));display:flex;flex-direction:column;justify-content:flex-end;gap:12px}
body.homefull .schedlist{position:relative;z-index:2}
.schedsame{display:none}
header.homehead .titlestack{position:relative;flex:1;min-width:0;height:44px;display:flex;flex-direction:column;align-items:flex-start;justify-content:center;gap:0}
header.homehead .titlecross{display:grid}
header.homehead .titlecross>h1{grid-area:1/1;margin:0}
header.homehead{--titlefade:0}
header.homehead .hititle{opacity:calc(1 - var(--titlefade))}
header.homehead .schedtitle{opacity:var(--titlefade)}
header.homehead .titlestack a.usawpchip{position:absolute;top:calc(100% + 2px);left:0;margin:0;opacity:calc(1 - var(--titlefade))}
header.homehead.titleaway .titlestack a.usawpchip{pointer-events:none}
body.schedopen header.homehead{--titlefade:1}
.nextcard .daychip{height:32px;margin:-3px -8px -3px 0;padding:0 11px;font-size:16px}
body.schedopen header.homehead{background:var(--color-bg)}
body.schedopen .homemap{opacity:0}
#schedule{scroll-margin-top:calc(var(--homehead, 88px) + 8px)}
@media (prefers-reduced-motion:reduce){body.homefull .homemap{transition:none}}
body.homefull .homemap .leaflet-marker-icon,body.homefull .homemap .leaflet-control-attribution{pointer-events:auto}
body.profilepage main{padding-bottom:calc(28px + env(safe-area-inset-bottom))}
header.profilebar{position:sticky;top:0;left:0;right:0;z-index:5;width:100%;max-width:none;background:var(--color-bg);display:grid;grid-template-columns:88px 1fr 88px;grid-template-rows:44px;align-items:center;padding:env(safe-area-inset-top) 6px 0;box-sizing:border-box;min-height:44px;border:0;box-shadow:none;view-transition-name:grunions-header}
header.profilebar h1{margin:0;text-align:center;font-size:var(--type-t4-size);font-weight:var(--type-t4-weight);line-height:44px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
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
button.cambadge{position:absolute;right:-4px;bottom:-4px;z-index:2;width:32px;height:32px;min-width:32px;min-height:32px;padding:0;border-radius:50%;background:var(--color-chip);color:var(--color-text);border:2px solid var(--color-text);display:flex;align-items:center;justify-content:center}
button.cambadge svg{width:16px;height:16px;display:block}
body.profile-edit button.cambadge.editonly{display:flex}
button.textlink{background:transparent;color:var(--t1);height:auto;min-height:0;padding:6px 8px;border-radius:0;font-size:14px;font-weight:600}
button.textlink.danger{color:var(--bad)}
a.rowbtn,button.rowbtn,button.coachrow{width:100%;height:auto;min-height:60px;padding:14px 18px;border-radius:0;background:transparent;color:var(--t1);font-weight:500;justify-content:flex-start;text-align:left;text-decoration:none;border-top:1px solid var(--line)}
button.coachrow{font-weight:400;align-items:flex-start;flex-direction:column;gap:2px}
button.coachrow .coachline{display:flex;align-items:center;gap:8px;min-width:0;width:100%}
.list>form{margin:0}
.list>form:not(:first-child)>button.rowbtn{border-top:1px solid var(--line)}
.pracemeta{color:var(--t2);text-align:center;margin:0;font-size:15px}
.pracemeta+.pracemeta{margin-top:2px}
.pracestatus{margin:10px 0 2px}
.stats.trio{width:100%;max-width:420px}
.stats.trio .stattile{flex:1;min-width:0;padding:12px 8px}
.list .li .coach-elig{margin-left:0;flex:none;height:24px;padding:0 8px;border-radius:999px;border:1px solid var(--line);background:var(--color-chip);font-size:12px;font-weight:600}
.profilename{margin:14px 0 4px;font-size:24px;font-weight:650;letter-spacing:-.3px;text-align:center}
.profilesub{color:var(--t2);text-align:center;margin:0 0 16px}
.stats{display:flex;gap:10px;justify-content:center;margin:0 0 8px}
.stattile{min-width:120px;background:var(--surface);border-radius:14px;padding:12px 16px;text-align:center}
.stattile b{display:block;font-size:22px;font-weight:650;line-height:1.2}
.stattile span{color:var(--t2);font-size:12px}
.seclabel{margin:var(--space-8) var(--space-1) var(--space-2);color:var(--t3);font-size:var(--type-b4-size);font-weight:var(--type-b4-weight)}
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
.dropzone{position:relative;height:140px;border-radius:var(--radius-overlay);border:1.5px dashed var(--color-border);background:transparent;overflow:hidden}
.dropzone.over,.dropzone:hover{border-color:var(--color-lime);background:color-mix(in srgb,var(--color-lime) 10%,transparent)}
.dropzone.has:hover{background:transparent}
button.dropempty{position:absolute;inset:0;width:100%;height:100%;min-height:0;padding:0;border:0;border-radius:inherit;background:transparent;color:var(--color-text);display:flex;flex-direction:column;align-items:center;justify-content:center;gap:4px;cursor:pointer}
.dropempty[hidden],.dropfill[hidden]{display:none !important}
.dropico{width:32px;height:32px;color:var(--t2);display:block}
.droplink{color:var(--color-lime);font-weight:650;font-size:16px;line-height:1.2}
.drophint{color:var(--t3);font-size:13px;line-height:1.2}
.dropfill{position:absolute;inset:0;display:flex;align-items:center;justify-content:center}
.dropfill img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;display:block}
.dropzone[data-mode=file] .dropfill img,.dropzone[data-mode=image] .filemeta{display:none}
.filemeta{display:flex;flex-direction:column;align-items:center;gap:2px;max-width:calc(100% - 24px);padding:0 12px;text-align:center;position:relative;z-index:1}
.dropname{font-weight:650;max-width:100%;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.dropsize{color:var(--t3);font-size:13px;line-height:1.2}
.dropacts{position:absolute;right:8px;bottom:8px;display:flex;gap:8px}
.dropacts button{height:32px;min-height:32px;padding:0 12px;border-radius:999px;border:1px solid var(--color-control);background:var(--color-surface);color:var(--color-text);font-size:13px;font-weight:650;width:auto}
.prefedit{margin:0}
.prefedit input{margin-top:6px}
.homealerts{position:relative;z-index:1}
.homedock{position:fixed;z-index:2;left:0;right:0;bottom:calc(var(--nav-clear) + env(safe-area-inset-bottom));max-width:640px;margin:0 auto;padding:0 12px 10px;display:flex;flex-direction:column;gap:8px;max-height:min(68vh,calc(100dvh - 150px));overflow:auto;pointer-events:none}
.homedock .card{pointer-events:auto;background:var(--color-surface);margin:0}
.menu a{display:flex;align-items:center;width:100%;height:40px;padding:0 12px;box-sizing:border-box;color:var(--t1);font-weight:500;font-size:15px;text-decoration:none;border-radius:8px}
.card .menu,.pagehead .menu{left:auto;right:0;min-width:220px}
.pagehead{display:flex;flex-direction:column;align-items:stretch;gap:var(--space-2);margin:0 0 var(--space-4)}
.mgroups{display:flex;flex-direction:column;gap:var(--space-4)}
.mgroup h2{margin:0 0 var(--space-2);padding:0 4px;font-size:13px;font-weight:650;letter-spacing:.01em;color:var(--t3)}
.mlist{background:var(--color-raised);border-radius:16px;overflow:hidden}
.mrow{display:flex;align-items:center;gap:12px;min-height:56px;padding:8px 12px 8px 10px;color:inherit;text-decoration:none;border-top:1px solid var(--line)}
.mrow:first-child{border-top:0}
.mico{width:32px;height:32px;border-radius:8px;background:var(--color-surface-2);color:var(--color-text);display:flex;align-items:center;justify-content:center;flex:none}
.mico svg{width:20px;height:20px;display:block}
.mtitle{display:block;font-weight:600;font-size:16px;line-height:1.25}
.mdesc{display:block;margin-top:1px;color:var(--t3);font-size:13px;line-height:1.3}
.mbadge{min-width:22px;height:22px;padding:0 6px;border-radius:11px;background:var(--color-badge-info);color:var(--color-badge-info-text);border:1px solid var(--color-badge-border);font-size:12px;font-weight:700;display:inline-flex;align-items:center;justify-content:center;flex:none}
.mbadge.info{background:var(--color-badge-info);color:var(--color-badge-info-text);border-color:var(--color-badge-border)}
.mbadge.warn{background:var(--color-badge-warn);color:var(--color-badge-warn-text);border-color:transparent}
.mchev{color:var(--t3);display:flex;flex:none}
.mchev svg{display:block}
header.homehead a.hubback{flex:none;width:44px;height:44px;margin-left:-10px;display:inline-flex;align-items:center;justify-content:center;color:var(--color-text)}
.pagerow{display:flex;align-items:center;justify-content:space-between;gap:var(--space-3);min-width:0}
.pagehead h1{margin:0;min-width:0;font-size:var(--type-t1-size);line-height:var(--type-t1-line);font-weight:var(--type-t1-weight);letter-spacing:var(--type-title-1-tracking)}
.pagesub{margin:0;color:var(--color-text-secondary);font-size:var(--type-b2-size);line-height:var(--type-b2-line);font-weight:var(--type-b2-weight)}
a.pageact,button.pageact{flex:none;height:auto;min-height:0;padding:var(--space-2) var(--space-3)}
body.adminpage main{padding-top:var(--space-5)}
.pagehead+.checkbar{padding-top:0}
.usawp-line{display:flex;align-items:center;justify-content:space-between;gap:12px;margin-top:12px}
.list{background:var(--surface);border-radius:var(--r);margin:0 0 12px;overflow:hidden}
.list.loose{overflow:visible}
.more{position:relative;flex:0 0 auto;margin-left:2px}
button.morebtn{width:32px;height:32px;padding:0;background:transparent;color:var(--t3);font-size:22px;line-height:1;border-radius:8px}button.morebtn svg,.m .more svg{width:20px;height:20px;display:block}
button.morebtn[aria-expanded=true]{background:var(--surface2);color:var(--t1)}
.menu{position:absolute;left:0;top:36px;z-index:20;min-width:232px;padding:6px;background:var(--color-surface);border:1px solid var(--line);border-radius:var(--radius-button);box-shadow:var(--shadow-overlay)}
.menu form{margin:0}
.menu button{width:100%;height:40px;padding:0 12px;justify-content:flex-start;background:transparent;color:var(--t1);font-weight:500;font-size:15px;border-radius:8px}
.menu button:disabled{color:var(--t3)}
.li{display:flex;align-items:center;gap:12px;padding:14px 18px;min-height:60px;border-top:1px solid var(--line)}.li:first-child{border-top:0}
.planrow{flex-wrap:wrap}.planline{flex:1;min-width:0;display:flex;align-items:center;gap:8px;flex-wrap:wrap}.planlabel{font-weight:500;color:var(--color-text)}.plantext{flex:1 0 100%;white-space:pre-wrap;margin-top:4px}
textarea.planfield{height:auto;min-height:var(--field-plan-min);line-height:var(--type-b1-line);resize:vertical;field-sizing:content}
.li.prow{padding-left:16px;padding-right:16px;gap:8px}
.editonly,.li.editonly{display:none}
body.profile-edit .editonly{display:inline-flex}
body.profile-edit .li.editonly{display:flex}
body.profile-edit .viewonly{display:none}
.grow{flex:1;min-width:0}.ell{white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
label{display:block;font-size:var(--type-b3-size);font-weight:var(--type-b3-weight);line-height:var(--type-b3-line);color:var(--t2);margin:0 0 var(--space-4)}
.checks{margin:0 0 14px}.checks label{display:flex;align-items:center;min-height:40px;margin:0;color:var(--t1);font-size:16px}
input,select,textarea{display:block;width:100%;margin-top:var(--space-2);background:var(--surface2);border:1px solid var(--color-control);color:var(--t1);border-radius:var(--radius-input);
padding:0 14px;height:var(--size-button);font:inherit;color-scheme:dark}textarea{padding:12px 14px}input[type=hidden]{display:none}input[type=checkbox]{display:inline-block;width:20px;height:20px;margin:0 8px 0 0;vertical-align:-4px;accent-color:var(--accent)}
input[type=date]::-webkit-calendar-picker-indicator,input[type=datetime-local]::-webkit-calendar-picker-indicator{cursor:pointer;background-image:url("data:image/svg+xml,%3Csvg%20xmlns%3D'http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg'%20viewBox%3D'0%200%20256%20256'%3E%3Cpath%20fill%3D'%23F2F6F1'%20d%3D'M208,32H184V24a8,8,0,0,0-16,0v8H88V24a8,8,0,0,0-16,0v8H48A16,16,0,0,0,32,48V208a16,16,0,0,0,16,16H208a16,16,0,0,0,16-16V48A16,16,0,0,0,208,32ZM72,48v8a8,8,0,0,0,16,0V48h80v8a8,8,0,0,0,16,0V48h24V80H48V48ZM208,208H48V96H208V208Z'%2F%3E%3C%2Fsvg%3E");background-repeat:no-repeat;background-size:20px 20px;background-position:center}
input[type=time]::-webkit-calendar-picker-indicator{cursor:pointer;background-image:url("data:image/svg+xml,%3Csvg%20xmlns%3D'http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg'%20viewBox%3D'0%200%20256%20256'%3E%3Cpath%20fill%3D'%23F2F6F1'%20d%3D'M128,24A104,104,0,1,0,232,128,104.11,104.11,0,0,0,128,24Zm0,192a88,88,0,1,1,88-88A88.1,88.1,0,0,1,128,216Zm64-88a8,8,0,0,1-8,8H128a8,8,0,0,1-8-8V72a8,8,0,0,1,16,0v48h48A8,8,0,0,1,192,128Z'%2F%3E%3C%2Fsvg%3E");background-repeat:no-repeat;background-size:20px 20px;background-position:center}
input:focus,select:focus,textarea:focus{outline:none;border-color:var(--color-focus)}
.btn,a.btn,button.btn,button{display:inline-flex;align-items:center;justify-content:center;gap:var(--space-2);box-sizing:border-box;height:var(--size-button);padding:0 var(--space-4);border-radius:var(--radius-button);border:0;font:inherit;font-weight:600;line-height:1;
cursor:pointer;text-decoration:none;background:var(--surface2);color:var(--color-text);transition:background-color 160ms ease,color 160ms ease}
.btn,a.btn,button.btn{min-height:var(--size-button)}
.btn:focus-visible,button:focus-visible,a.btn:focus-visible,.iconbtn:focus-visible{outline:2px solid var(--color-focus);outline-offset:2px}
button:disabled,.btn:disabled{opacity:.45}
.btn-primary,button.btn-primary,a.btn-primary,.btn.primary,button.primary{background:var(--color-lime);color:var(--color-forest)}
.btn-secondary,button.btn-secondary,a.btn-secondary{background:var(--color-surface-2);color:var(--color-text);border:1px solid var(--color-control)}
.btn-tertiary,button.btn-tertiary,a.btn-tertiary,.btn.quiet,button.quiet{background:transparent;color:var(--color-text);height:44px;min-height:44px;padding:0 var(--space-2)}
.btn-danger,button.btn-danger,a.btn-danger,.btn.danger,button.danger{background:var(--color-orange);color:var(--color-forest)}
@media (hover:hover){
.btn-primary:hover,button.btn-primary:hover,a.btn-primary:hover{background:color-mix(in srgb,var(--color-lime) 86%,var(--color-forest))}
.btn-secondary:hover,button.btn-secondary:hover,a.btn-secondary:hover{background:var(--color-hover)}
.btn-tertiary:hover,button.btn-tertiary:hover,a.btn-tertiary:hover,.btn.quiet:hover{background:var(--color-hover)}
.btn-danger:hover,button.btn-danger:hover,a.btn-danger:hover{background:color-mix(in srgb,var(--color-orange) 86%,var(--color-forest))}
.iconbtn:hover{background:var(--color-hover)}
}
.btn-primary:active,button.btn-primary:active{background:color-mix(in srgb,var(--color-lime) 72%,var(--color-forest))}
.btn-secondary:active,.btn-tertiary:active,.btn.quiet:active{background:var(--color-pressed)}
.btn-danger:active,button.btn-danger:active{background:color-mix(in srgb,var(--color-orange) 72%,var(--color-forest))}
.btn[aria-busy=true]{position:relative;color:transparent;pointer-events:none}
.btn[aria-busy=true]::after{content:"";position:absolute;width:18px;height:18px;border:2px solid var(--color-forest);border-right-color:transparent;border-radius:50%;animation:grunions-spin .7s linear infinite}
.btn-secondary[aria-busy=true]::after,.btn-tertiary[aria-busy=true]::after{border-color:var(--color-text);border-right-color:transparent}
@keyframes grunions-spin{to{transform:rotate(360deg)}}
@media (prefers-reduced-motion:reduce){.btn,.btn[aria-busy=true]::after{transition:none;animation:none}}
.btn.compact,button.compact{padding:0 14px}.full{width:100%}.row{display:flex;gap:var(--space-2)}.row>*{flex:1}
.chip,a.chip,button.chip{position:relative;display:inline-flex;align-items:center;justify-content:center;box-sizing:border-box;height:var(--size-chip);min-height:var(--size-chip);padding:0 14px;border-radius:var(--radius-chip);border:1px solid var(--color-control);background:transparent;color:var(--color-text);font-size:var(--type-b3-size);font-weight:var(--type-b3-weight);line-height:1;text-decoration:none;white-space:nowrap;flex:none;cursor:pointer}
.chip::after,a.chip::after,button.chip::after{content:"";position:absolute;left:0;right:0;top:-4px;bottom:-4px}
.chip-active,a.chip-active,button.chip-active,.chip.on,a.chip.on,button.chip.on{background:var(--color-selected);color:var(--color-on-selected);border-color:var(--color-selected)}
.chip-info,.coach-tag{display:inline-flex;align-items:center;gap:var(--space-2);height:28px;margin-left:var(--space-2);padding:0 var(--space-2);border-radius:var(--radius-chip);border:1px solid var(--line);background:var(--color-chip);color:var(--t1);font-size:var(--type-b4-size);font-weight:var(--type-b4-weight);line-height:1;white-space:nowrap;vertical-align:1px}
.chip-info.warn,.coach-tag.warn{color:var(--color-forest);border-color:var(--color-status-attention);background:var(--color-yellow)}
.chip-info.bad,.coach-tag.bad{color:var(--color-forest);border-color:var(--color-status-not-cleared);background:var(--color-coral)}
.nxbadge{margin:0;height:auto;padding:5px 10px;letter-spacing:.8px;background:var(--color-surface);color:var(--color-text);border-color:var(--color-badge-border)}
.coach-elig,.ref-elig{margin-left:8px;font-weight:650;font-size:15px}
.eligs{display:flex;flex-wrap:wrap;gap:4px 10px;margin-top:4px}.eligs .coach-elig,.eligs .ref-elig,.eligs .coach-tag,.eligs .chip-info{margin-left:0}.eligs .st{white-space:normal}
.memline{display:flex;flex-wrap:wrap;align-items:center;gap:2px 0;margin-top:2px;color:var(--t3);font-size:13px;line-height:1.4}
.st{display:inline-flex;align-items:center;gap:var(--space-2);min-height:28px;font-size:var(--type-b2-size);line-height:var(--type-b2-line);color:var(--t2);white-space:nowrap}
.st::before{content:"";width:16px;height:16px;border-radius:50%;background:var(--t3);flex:none}
.st-ok::before,.st-warn::before,.st-bad::before{border-radius:0;-webkit-mask:var(--st-icon) center/contain no-repeat;mask:var(--st-icon) center/contain no-repeat}
.st-ok{--st-icon:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 256 256'%3E%3Cpath fill='%23000' d='M229.66,77.66l-128,128a8,8,0,0,1-11.32,0l-56-56a8,8,0,0,1,11.32-11.32L96,188.69,218.34,66.34a8,8,0,0,1,11.32,11.32Z'/%3E%3C/svg%3E")}
.st-warn{--st-icon:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 256 256'%3E%3Cpath fill='%23000' d='M236.8,188.09,149.35,36.22h0a24.76,24.76,0,0,0-42.7,0L19.2,188.09a23.51,23.51,0,0,0,0,23.72A24.35,24.35,0,0,0,40.55,224h174.9a24.35,24.35,0,0,0,21.33-12.19A23.51,23.51,0,0,0,236.8,188.09ZM120,144V104a8,8,0,0,1,16,0v40a8,8,0,0,1-16,0Zm20,36a12,12,0,1,1-12-12A12,12,0,0,1,140,180Z'/%3E%3C/svg%3E")}
.st-bad{--st-icon:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 256 256'%3E%3Cpath fill='%23000' d='M205.66,194.34a8,8,0,0,1-11.32,11.32L128,139.31,61.66,205.66a8,8,0,0,1-11.32-11.32L116.69,128,50.34,61.66A8,8,0,0,1,61.66,50.34L128,116.69l66.34-66.35a8,8,0,0,1,11.32,11.32L139.31,128Z'/%3E%3C/svg%3E")}
.st-ok::before{background:var(--ok)}.st-bad::before{background:var(--bad)}.st-warn::before,.st-trial::before{background:var(--warn)}
.dot{width:8px;height:8px;border-radius:50%;background:var(--t3);flex:none;display:inline-block}.dot.ok{background:var(--ok)}.dot.bad{background:var(--bad)}.dot.warn{background:var(--warn)}
.list .menu{left:auto;right:0;min-width:280px}
.row.wrap{flex-wrap:wrap}
dialog.modal{border:0;padding:0;background:transparent;color:var(--t1);width:min(440px,calc(100vw - 32px))}
dialog.modal::backdrop{background:var(--color-backdrop)}
dialog.modal .sheet{background:var(--surface);border:1px solid var(--line);border-radius:var(--r);padding:20px}
.note{background:var(--surface);border-radius:var(--r);padding:14px 18px;margin:0 0 12px;color:var(--t2);font-size:15px}.note b{color:var(--t1)}
.toast{position:fixed;left:50%;bottom:calc(var(--nav-clear) + 12px + env(safe-area-inset-bottom));transform:translateX(-50%);z-index:30;background:var(--surface);color:var(--t1);border:1px solid var(--line);border-radius:12px;padding:12px 16px;font-size:15px;line-height:1.4;text-align:center;box-shadow:0 8px 28px rgba(0,0,0,.5);max-width:min(440px,calc(100% - 32px))}
body:has(.composer) .toast{bottom:calc(var(--nav-clear) + env(safe-area-inset-bottom) + var(--composer-h, 69px) + 12px)}
details>summary{list-style:none;cursor:pointer;display:flex;align-items:center;justify-content:space-between;min-height:56px;padding:0 18px;color:var(--t1)}
details>summary::-webkit-details-marker{display:none}details>summary::after{content:"›";color:var(--t3);font-size:22px;transition:transform .15s}
details[open]>summary::after{transform:rotate(90deg)}details.card{padding:0}details.card>.body{padding:0 18px 16px}
details.checkin{margin:4px 0 20px}details.checkin>summary{min-height:0;padding:18px 0 8px;font-size:17px;font-weight:600;justify-content:flex-start;gap:8px}
.kv{display:flex;justify-content:space-between;gap:12px;padding:10px 0;border-top:1px solid var(--line);font-size:15px}.kv:first-child{border-top:0}.kv span:first-child{color:var(--t2)}
.chiprow{display:flex;flex-wrap:nowrap;align-items:center;gap:var(--space-2);box-sizing:border-box;min-width:0;margin-inline:-20px;padding:6px 20px;overflow-x:auto;overflow-y:hidden;overscroll-behavior-x:contain;touch-action:pan-x;scrollbar-width:none;scroll-padding-inline:20px;-webkit-overflow-scrolling:touch}
.chiprow::-webkit-scrollbar{display:none}
.chip:focus-visible,a.chip:focus-visible,button.chip:focus-visible{outline:2px solid var(--color-focus);outline-offset:2px}
.admintabs,header.homehead .headtabs{flex:1;min-width:0;margin:0}
header.homehead .headtabs.chiprow{height:44px;margin:0;width:auto;padding:0;align-items:center}
.admintabs a.chip,header.homehead .headtabs a.chip{flex:none;height:var(--size-chip);min-height:var(--size-chip);padding:0 14px;border-radius:var(--radius-chip);border:1px solid var(--color-control);background:transparent;color:var(--color-text);box-shadow:none}
.admintabs a.chip.on,header.homehead .headtabs a.chip.on,header.homehead .headtabs a.chip.chip-active.on{background:var(--color-selected);color:var(--color-on-selected);border-color:var(--color-selected);box-shadow:none}
.pagetitle{display:flex;justify-content:space-between;align-items:baseline;gap:12px}.pagetitle h1{margin-bottom:12px}
.peoplebar{position:sticky;top:var(--headh,0px);z-index:6;background:var(--color-bg);margin:0 -20px 8px;padding:0 20px 10px}
.peoplebar input{height:48px;margin:0}
.fchips{margin-top:10px;margin-bottom:0}
.expage h2.egroup{position:sticky;top:var(--headh,0px);z-index:4;background:var(--color-bg);margin:18px 0 8px;padding:8px 0}
.daybadge{height:28px;padding:0 10px;margin:0;flex:none;font-weight:700}
.people h2{position:sticky;top:calc(var(--headh,0px) + var(--peoplepin,0px));z-index:4;background:var(--color-bg);padding:8px 0;margin-top:12px}
.lgroup{margin:0 0 14px}
.lgroup .list{margin:0}
h3.alpha{margin:0;padding:8px 0 6px;font-size:13px;font-weight:700;letter-spacing:.06em;color:var(--t3);position:sticky;top:calc(var(--headh,0px) + var(--peoplepin,0px));z-index:4;background:var(--color-bg)}
.psub{display:block;margin-top:2px;min-width:0;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;color:var(--color-text-secondary);font-size:var(--type-b2-size);line-height:var(--type-b2-line);font-weight:var(--type-b2-weight)}
.psub .stword{color:var(--color-text)}
.psub.st-ok::before,.psub.st-warn::before,.psub.st-bad::before,.psub.st-unknown::before{content:"";display:inline-block;width:16px;height:16px;margin-right:8px;vertical-align:-3px;-webkit-mask:var(--pico) center/contain no-repeat;mask:var(--pico) center/contain no-repeat}
.psub.st-ok{--pico:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 256 256'%3E%3Cpath fill='%23000' d='M128,24A104,104,0,1,0,232,128,104.11,104.11,0,0,0,128,24Zm45.66,85.66-56,56a8,8,0,0,1-11.32,0l-24-24a8,8,0,0,1,11.32-11.32L112,148.69l50.34-50.35a8,8,0,0,1,11.32,11.32Z'/%3E%3C/svg%3E")}
.psub.st-warn{--pico:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 256 256'%3E%3Cpath fill='%23000' d='M236.8,188.09,149.35,36.22h0a24.76,24.76,0,0,0-42.7,0L19.2,188.09a23.51,23.51,0,0,0,0,23.72A24.35,24.35,0,0,0,40.55,224h174.9a24.35,24.35,0,0,0,21.33-12.19A23.51,23.51,0,0,0,236.8,188.09ZM120,104a8,8,0,0,1,16,0v40a8,8,0,0,1-16,0Zm8,88a12,12,0,1,1,12-12A12,12,0,0,1,128,192Z'/%3E%3C/svg%3E")}
.psub.st-bad{--pico:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 256 256'%3E%3Cpath fill='%23000' d='M128,24A104,104,0,1,0,232,128,104.11,104.11,0,0,0,128,24Zm37.66,130.34a8,8,0,0,1-11.32,11.32L128,139.31l-26.34,26.35a8,8,0,0,1-11.32-11.32L116.69,128,90.34,101.66a8,8,0,0,1,11.32-11.32L128,116.69l26.34-26.35a8,8,0,0,1,11.32,11.32L139.31,128Z'/%3E%3C/svg%3E")}
.psub.st-unknown{--pico:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 256 256'%3E%3Cpath fill='%23000' d='M128,24A104,104,0,1,0,232,128,104.11,104.11,0,0,0,128,24Zm0,168a12,12,0,1,1,12-12A12,12,0,0,1,128,192Zm8-48.72V144a8,8,0,0,1-16,0v-8a8,8,0,0,1,8-8c13.23,0,24-9,24-20s-10.77-20-24-20-24,9-24,20v4a8,8,0,0,1-16,0v-4c0-19.85,17.94-36,40-36s40,16.15,40,36C168,125.38,154.24,139.93,136,143.28Z'/%3E%3C/svg%3E")}
.psub.st-ok::before{background:var(--color-status-cleared)}
.psub.st-warn::before{background:var(--color-status-attention)}
.psub.st-bad::before{background:var(--color-status-not-cleared)}
.psub.st-unknown::before{background:var(--color-status-unknown)}
.coachmark{display:inline-block;width:16px;height:16px;margin:0;flex:none;overflow:visible;font-size:0;line-height:16px}
.coachmark::before{margin-right:0;vertical-align:0}
.peoplebar .peoplesum{margin:12px 0 0;line-height:1.35}
.seg{display:flex;gap:8px;margin:0}
.seg::-webkit-scrollbar{display:none}
nav.tabs{position:fixed;left:0;right:0;bottom:calc(var(--nav-offset-bottom) + env(safe-area-inset-bottom));z-index:9;box-sizing:border-box;
width:max-content;max-width:calc(100vw - 16px);margin-inline:auto;padding:var(--nav-pad);background:var(--nav-glass-bg);
-webkit-backdrop-filter:var(--nav-glass-blur);backdrop-filter:var(--nav-glass-blur);
border:1px solid var(--nav-glass-line);border-radius:999px;box-shadow:0 8px 28px rgba(0,0,0,.28);
display:flex;justify-content:center;align-items:center;gap:var(--nav-gap);view-transition-name:grunions-nav}
nav.tabs a{position:relative;flex:none;width:var(--nav-circle);height:var(--nav-circle);min-width:48px;min-height:48px;box-sizing:border-box;
display:flex;align-items:center;justify-content:center;padding:0;margin:0;border-radius:50%;border:1px solid var(--nav-item-line);
background:var(--nav-item-glass);color:var(--color-nav-icon);text-decoration:none;transition:background-color 180ms ease,color 180ms ease}
nav.tabs a.on{background:var(--color-nav-circle-on);color:var(--color-nav-icon-on);border-color:transparent}
@media (hover:hover){nav.tabs a:not(.on):hover{background:var(--nav-item-glass-hover)}}
nav.tabs a:not(.on):active{background:var(--nav-item-glass-hover)}
@supports not ((backdrop-filter:blur(1px)) or (-webkit-backdrop-filter:blur(1px))){
nav.tabs{background:var(--color-nav);-webkit-backdrop-filter:none;backdrop-filter:none;border-color:var(--color-nav-border)}
nav.tabs a:not(.on){background:var(--color-nav-circle);border-color:transparent}
}
@media (prefers-reduced-transparency:reduce){
nav.tabs{background:var(--color-nav);-webkit-backdrop-filter:none;backdrop-filter:none;border-color:var(--color-nav-border)}
nav.tabs a:not(.on){background:var(--color-nav-circle);border-color:transparent}
}
nav.tabs .ico-reg,nav.tabs .ico-fill{display:flex;align-items:center;justify-content:center}
nav.tabs .ico-fill{display:none}
nav.tabs a.on .ico-reg{display:none}
nav.tabs a.on .ico-fill{display:flex}
nav.tabs a:focus-visible{outline:2px solid var(--color-focus);outline-offset:2px}
@media (prefers-reduced-motion:reduce){nav.tabs a{transition:none}}
.badge{display:inline-flex;align-items:center;justify-content:center;min-width:16px;height:16px;padding:0 4px;border-radius:8px;background:var(--color-coral);color:var(--color-forest);font-size:10px;font-weight:700;line-height:1}
nav.tabs a .badge{position:absolute;top:0;right:0;margin:0}.datetile{position:relative}.datetile .pdate{position:absolute;top:0;right:0}.datetile .pdate .badge{position:absolute;top:-4px;right:-4px;margin:0}
/* Phosphor icons. Nav uses Regular, and Fill on the selected circle. */
nav.tabs svg{width:var(--icon-nav);height:var(--icon-nav);flex:none;display:block}
.chat{display:flex;flex-direction:column;gap:0}.m{position:relative;-webkit-touch-callout:none;margin-top:14px;display:flex;flex-direction:column;align-items:flex-start}.m.g-mid,.m.g-last{margin-top:2px}.chat>.m:first-child{margin-top:0}.m .who{font-size:13px;color:var(--t3);margin:0 0 3px}.m .txt{background:var(--color-bubble);border-radius:var(--radius-card);padding:10px 14px;display:inline-block;max-width:85%;white-space:pre-wrap;word-wrap:break-word;color:var(--color-text)}.m .txt a.msglink{color:var(--accent);text-decoration:none}
.m.g-first:not(.mine) .txt,.m.g-first:not(.mine) .img img{border-bottom-left-radius:5px}.m.g-mid:not(.mine) .txt,.m.g-mid:not(.mine) .img img{border-top-left-radius:5px;border-bottom-left-radius:5px}.m.g-last:not(.mine) .txt,.m.g-last:not(.mine) .img img{border-top-left-radius:5px}
.m.g-first.mine .txt,.m.g-first.mine .img img{border-bottom-right-radius:5px}.m.g-mid.mine .txt,.m.g-mid.mine .img img{border-top-right-radius:5px;border-bottom-right-radius:5px}.m.g-last.mine .txt,.m.g-last.mine .img img{border-top-right-radius:5px}
.m.mine{text-align:right;align-items:flex-end}.m.mine .txt{background:var(--color-bubble-mine);text-align:left;color:var(--color-text)}.m.ann{align-items:stretch}.m.ann .txt{display:block;max-width:none;border:1px solid var(--line);background:var(--surface)}
.m .txt.deleted{font-style:italic;color:var(--t3);background:transparent}.m .edited{font-size:12px;color:var(--t3);font-weight:400}
.m .more{display:none;position:absolute;top:-4px;right:0;width:32px;height:32px;padding:0;background:none;color:var(--t3);font-size:18px}
.m.mine .more{left:0;right:auto}
@media (hover:hover) and (pointer:fine){.m:hover .more{display:inline-flex}}
.m .editbox textarea{min-height:72px;height:auto;margin:0}
.composer{position:fixed;left:0;right:0;bottom:calc(var(--nav-clear) + env(safe-area-inset-bottom));background:var(--bg);padding:10px 20px;border-top:1px solid var(--line);z-index:10}
.chatpad{height:calc(var(--composer-h, 69px) + 16px)}
.composer form{max-width:600px;margin:auto;display:flex;gap:8px;align-items:flex-end}
.composer textarea{margin:0;height:48px;min-height:48px;max-height:136px;resize:none;line-height:22px;padding:12px 14px;overflow-y:auto;scrollbar-width:none;-ms-overflow-style:none}
.composer textarea::-webkit-scrollbar{display:none}.iconbtn{width:48px;padding:0;flex:none;color:var(--t2)}.iconbtn svg{width:24px;height:24px;display:block}
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
.rx button.on{border-color:var(--color-selected);color:var(--t1);background:var(--color-chip)}
.qbar{max-width:600px;margin:0 auto 8px;display:flex;align-items:center;gap:10px;border-left:3px solid var(--color-text-tertiary);padding:2px 4px 2px 10px;color:var(--t2);font-size:13px}
.qbar b{display:block;color:var(--t1);font-size:12px;font-weight:650}.qbar span{display:block;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;max-width:70vw}
.qbar button{width:32px;height:32px;padding:0;background:none;color:var(--t3);flex:none}
.quotechip{border-left:3px solid var(--color-text-tertiary);padding:2px 8px;margin:0 0 6px;color:var(--t2);font-size:13px;text-align:left}
.quotechip b{display:block;color:var(--t3);font-weight:650;font-size:12px}
dialog.botsheet{position:fixed;z-index:30;inset:auto 0 0 0;margin:0 auto;width:min(640px,100%);height:fit-content;max-height:calc(100dvh - 8px);border:0;padding:0;background:transparent;color:var(--t1);overflow:visible}
dialog.botsheet::backdrop{background:var(--color-backdrop);opacity:1;transition:opacity .25s ease-out}
dialog.botsheet.opening::backdrop,dialog.botsheet.closing::backdrop{opacity:0}
dialog.botsheet .sheet{background:var(--color-sheet);border:1px solid var(--color-sheet-border);border-bottom:0;border-radius:var(--radius-overlay) var(--radius-overlay) 0 0;padding:0 12px calc(14px + env(safe-area-inset-bottom));max-height:calc(100dvh - 12px);overflow:auto;transform:translateY(0);transition:transform .25s ease-out}
.grab{display:block;width:100%;height:28px;margin:0 0 8px;padding:0;position:sticky;top:0;z-index:1;background:var(--color-sheet);touch-action:none;cursor:grab}
.grab::after{content:"";position:absolute;left:50%;top:12px;width:36px;height:5px;margin-left:-18px;border-radius:3px;background:var(--color-sheet-handle)}
@media (prefers-reduced-motion:reduce){dialog.botsheet::backdrop,dialog.botsheet .sheet{transition:none}}
.emogrid{display:grid;grid-template-columns:repeat(6,1fr);gap:8px;margin:0 0 14px}
.emogrid button{width:100%;aspect-ratio:1;height:auto;padding:0;border-radius:50%;background:var(--color-sheet-row);font-size:22px}
.emopick{display:grid;grid-template-columns:repeat(8,1fr);gap:6px;max-height:28vh;overflow:auto;margin:0 0 12px}
.emopick button{height:40px;padding:0;border-radius:var(--radius-input);background:var(--color-sheet-row);font-size:20px}
.actgroup{background:var(--color-sheet-row);border-radius:var(--radius-card);overflow:hidden;margin:0 0 10px}
.actgroup .actrow{width:100%;height:48px;padding:0 14px;border-radius:0;background:transparent;color:var(--t1);font-weight:500;justify-content:flex-start;gap:12px;border-bottom:1px solid var(--color-sheet-line)}
.actgroup .actrow:last-child{border-bottom:0}
.actgroup .actrow svg{width:20px;height:20px;flex:none;display:block}
.actgroup .actrow.danger,.actgroup .actrow.danger svg{color:var(--bad)}
#actConfirm{margin:0 0 10px;font-weight:600}
.lightbox{position:fixed;inset:0;background:var(--color-lightbox);display:flex;align-items:center;justify-content:center;z-index:20}.lightbox img{max-width:96vw;max-height:92vh;border-radius:8px}
.gobtn{background:none;height:auto;padding:4px 0;color:var(--t2);font-weight:500;font-size:14px}.gobtn::after{content:" ›";color:var(--t3)}
.ci-name,a.ci-name{flex:1;min-width:0;height:auto;padding:0;background:none;display:flex;align-items:center;gap:12px;text-align:left;font-weight:400;color:inherit;text-decoration:none}
.personrow .ci-name{align-items:center}
.personrow>form,.personrow>.more{flex:none}
span.avatar.ciav,span.avatar.ciav img{width:40px;height:40px;min-width:40px;max-width:40px;min-height:40px;max-height:40px;flex:0 0 40px;font-size:13px}
.filt{display:flex;gap:8px;margin:0 0 16px;flex-wrap:wrap}
.filt.chiprow,.fchips.chiprow{flex-wrap:nowrap;margin-inline:-20px;padding:6px 20px;overflow-x:auto;overflow-y:hidden;overscroll-behavior-x:contain;touch-action:pan-x;scroll-padding-inline:20px}
.lineupfilt.chiprow{margin-bottom:16px}
h2.planask{margin:0 0 var(--space-4);font-size:var(--type-t3-size);line-height:var(--type-t3-line);font-weight:var(--type-t3-weight)}
.lanepick{display:flex;flex-direction:column;gap:var(--space-3);margin:0 0 var(--space-5)}
button.lanecard{width:100%;height:auto;min-height:0;padding:var(--space-4);border-radius:var(--radius-card);background:var(--color-surface);color:var(--color-text);border:1px solid var(--color-control);text-align:left;font-weight:400;align-items:flex-start;flex-direction:column;gap:4px}
button.lanecard.on{border-color:var(--color-lime);box-shadow:inset 0 0 0 1px var(--color-lime)}
button.lanecard b{font-size:var(--type-t4-size);font-weight:650;line-height:var(--type-t4-line)}
button.lanecard span{color:var(--color-text-secondary);font-size:var(--type-b2-size);line-height:var(--type-b2-line);font-weight:400}
.livetitle{display:flex;align-items:center;justify-content:space-between;gap:var(--space-3);margin:0 0 var(--space-4)}
.livetitle strong{font-size:var(--type-t3-size);line-height:var(--type-t3-line);font-weight:var(--type-t3-weight)}
button.setrow{width:100%;height:auto;min-height:60px;padding:14px 18px;border-radius:0;background:transparent;color:var(--color-text);font-weight:500;justify-content:space-between;text-align:left}
button.setrow .sum{color:var(--color-text-secondary);font-weight:400;font-size:var(--type-b2-size)}
label:has(> .locok){display:flex;flex-wrap:wrap;align-items:center;column-gap:8px}
label:has(> .locok)>.placefield,label:has(> .locok)>input{flex:1 0 100%;min-width:100%}
.locok{display:inline-flex;align-items:center;gap:6px;margin:0;color:var(--color-status-cleared);font-size:var(--type-b2-size);line-height:1}
.placefield{position:relative;display:block}
.placedrop{position:absolute;z-index:25;left:0;right:0;top:calc(100% + 4px);max-height:min(320px,60vh);overflow:auto;background:var(--color-sheet);border:1px solid var(--color-sheet-border);border-radius:var(--radius-control);padding:4px;box-shadow:0 12px 32px rgba(0,0,0,.35)}
button.placeopt{display:flex;align-items:center;gap:12px;width:100%;min-height:48px;height:auto;margin:0;padding:8px 12px;background:transparent;color:var(--color-text);border-radius:12px;font-weight:400;text-align:left;justify-content:flex-start}
button.placeopt.on{background:var(--color-raised)}
.placeopt .pin{flex:none;width:16px;height:16px;color:var(--color-icon)}
.placeopt .grow{min-width:0;display:block}
.placeopt .pname,.placeopt .plabel{display:block;font-weight:650;line-height:1.25}
.placeopt .pdetail{display:block;margin-top:2px;color:var(--color-text-secondary);font-size:13px;line-height:1.25;font-weight:400}
.createfoot{margin-top:var(--space-5)}
.createfoot .pagesub{margin:0 0 var(--space-3)}
.planlane{display:flex;flex-direction:column;gap:12px}
.planlane .card h2{margin:0 0 4px;font-size:1.0625rem;font-weight:650}
.planlane .card p{margin:0 0 12px}
.planlinks{display:flex;flex-wrap:wrap;gap:8px}
.planlinks a.chip{text-decoration:none}
.fchips.chiprow{margin-top:10px;margin-bottom:0}
.profilehero .profswitch.chiprow{align-self:stretch;margin-top:16px;margin-bottom:8px;margin-inline:-20px}
.filt button.chip:disabled{opacity:.4;color:var(--t3);cursor:default;pointer-events:none}
.checkbar{position:sticky;top:var(--headh,0px);z-index:6;background:var(--color-bg);margin:0 -20px 8px;padding:8px 20px 10px;overflow-x:auto}
.checkbar form.row{flex-wrap:nowrap;align-items:center;gap:var(--space-2);width:100%;min-width:0;max-width:100%}
.checkbar .calpick{flex:1 1 auto;width:100%;min-width:0;max-width:100%}
.checkbar .calnav{width:44px;height:44px;min-width:44px;min-height:44px}
.checkbar .calbtn{height:44px;min-height:44px;min-width:0;flex:1 1 0}
.evcount{display:inline-flex;align-items:center;justify-content:center;box-sizing:border-box;height:44px;min-width:44px;padding:0 12px;border-radius:var(--radius-chip);border:1px solid var(--color-control);background:var(--color-surface);color:var(--color-text);font-weight:650;font-size:15px;flex:none}
button.evcount{cursor:pointer}
span.evcount{color:var(--color-text-secondary)}
.playersearch{margin:0 0 12px}
.playersearch input{margin:0;height:44px}
.checkbar .calpick{flex:0 0 auto}
.checkbar .calbtn{flex:0 0 auto}
.checkbar .calbtn span{overflow:visible;text-overflow:clip}
.checkbar input[name=q]{flex:1 1 auto;width:auto;min-width:0;margin:0;height:48px;font-size:14px}
.checkmeta{display:flex;flex-direction:column;gap:8px;margin:0 0 16px}
.checkmeta .filt.chiprow{margin:0 -20px;align-items:center;padding:6px 20px}
.evstack{display:flex;flex-direction:column;gap:8px;margin:4px 0 12px}
.evcard{padding:var(--space-4);margin:0}
.evcard .evhit{display:block;color:inherit;text-decoration:none}
.evcard .nxtitle{font-size:var(--type-t4-size);font-weight:var(--type-t4-weight);line-height:var(--type-t4-line)}
.evcard .t2{margin:2px 0 0;font-weight:400;font-size:15px}
.evcard .t3{margin:2px 0 0}
a.evcard{display:block;color:inherit;text-decoration:none;background:var(--color-surface)}
.evcard.on{box-shadow:inset 0 0 0 1px var(--color-text-secondary)}
button.dock,a.dock{background:var(--accent);color:var(--color-on-primary)}
a.quietcheck,button.quietcheck{background:var(--surface2);color:var(--color-text);border:0;border-radius:var(--radius-button)}
.emptyfind{color:var(--t2);margin:8px 0 16px}
details.lineuppast{margin-top:8px}details.lineuppast>summary{min-height:44px;padding:8px 0;font-size:17px;font-weight:600;justify-content:flex-start}
.repeatblock .repeatopts{display:none}.repeatblock:has(input[name=repeat]:checked) .repeatopts{display:block}
.tripcard{padding:0;overflow:hidden}.tripcard .evbody{padding:0 18px 18px}.tripcard .nxcardhead{flex-wrap:wrap;align-items:flex-start}.tripcard .nxcardhead .tripname{flex:1 1 100%;min-width:0}.tripcard .nxcardhead .chip-info{flex:none;margin-left:0}.lineupchips{display:flex;gap:6px;flex-wrap:wrap;align-items:center}.lineupchips .chip-info{margin:0}
div.card.tap.tripcard{padding:18px;overflow:visible}div.card.tap.tripcard .lineupchips{margin:0 0 8px}div.card.tap.tripcard .hostorg{margin:0 0 8px}div.card.tap.tripcard .nxcardhead{margin-bottom:6px}
.tripcard .tripwhere{align-items:flex-start}.tripcard .tripwhere a{min-width:0}
.evbanner{height:132px;display:flex;align-items:flex-end;padding:14px;position:relative;overflow:hidden;background:linear-gradient(160deg,var(--color-badge-border),var(--color-bg))}
.evbanner img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}.evbanner svg{position:relative;z-index:1;color:var(--color-text)}
.lineupacts{display:flex;gap:8px;flex-wrap:wrap;margin:0 0 14px}.lineupacts .btn{width:auto;padding:0 14px}
.sportline{margin-top:6px;color:var(--t3)}
.actseg{display:flex;gap:var(--space-1);flex-wrap:wrap;margin:0 0 var(--space-4);padding:var(--space-1);background:var(--color-surface-2);border-radius:var(--radius-control)}
.actseg label{position:relative;flex:1;min-width:0;margin:0}
.actseg input{position:absolute;opacity:0;width:1px;height:1px}
.actseg span{display:flex;align-items:center;justify-content:center;height:40px;min-height:40px;border-radius:var(--radius-button);background:transparent;color:var(--color-text-secondary);font-size:var(--type-b3-size);font-weight:var(--type-b3-weight);padding:0 var(--space-2)}
.actseg input:checked+span{background:var(--color-lime);color:var(--color-forest)}
.actseg input:focus-visible+span{outline:2px solid var(--color-focus);outline-offset:2px}
dialog.matpick .matpart{flex-wrap:nowrap;margin:12px 4px 0}
dialog.matpick .matpart span{white-space:nowrap;font-size:12px;padding:0 2px;height:36px;min-height:36px}
.evhost{color:var(--t2);font-size:14px;margin:2px 0 8px}.evnote{color:var(--t2);font-size:15px;line-height:1.4;margin:8px 0}
details.moredetails{margin:8px 0 12px}details.moredetails>summary{min-height:44px;padding:8px 0;font-weight:600}
.growthcard{position:relative;padding:var(--space-4) var(--space-4) var(--space-2);margin:0 0 var(--space-3)}
.growthhead{font-size:15px;font-weight:650;line-height:1.3;margin:0 0 6px}
.growthcard svg{width:100%;height:auto;display:block;touch-action:none}
.growthtip{position:absolute;z-index:2;top:36px;transform:translateX(-50%);background:var(--color-surface-2);color:var(--t1);border:1px solid var(--line);border-radius:var(--radius-input);padding:6px 10px;font-size:13px;white-space:nowrap;pointer-events:none}
.calpick{position:relative;flex:1.6;min-width:0;display:flex;align-items:center;gap:4px}
.calnav,.calmonth{flex:none;width:36px;height:36px;padding:0;display:inline-flex;align-items:center;justify-content:center;background:none;color:var(--t1);text-decoration:none;border-radius:10px}
.calnav{height:48px;width:40px}
.calnav[aria-disabled=true]{color:var(--t3);opacity:.35;pointer-events:none}
.calnav svg,.calmonth svg,.calbtn svg{display:block}.calnav svg,.calmonth svg{width:20px;height:20px}
.calbtn{flex:1;min-width:0;height:48px;min-height:48px;margin:0;padding:0 10px;background:var(--surface2);border:1px solid var(--line);color:var(--t1);border-radius:12px;font:inherit;font-weight:600;display:flex;align-items:center;justify-content:center;gap:8px;cursor:pointer}
.calbtn span{overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.calhead{display:flex;align-items:center;justify-content:space-between;gap:8px;margin:0 0 12px}
.calhead .lbl{font-weight:650;color:var(--color-text);font-size:17px}
.calwd,.calgrid{display:grid;grid-template-columns:repeat(7,1fr);gap:4px;text-align:center}
.calwd{color:var(--color-text-secondary);font-size:12px;font-weight:650;margin-bottom:6px}
.calday{position:relative;display:flex;flex-direction:column;align-items:center;justify-content:flex-start;gap:0;height:48px;padding-top:10px;border-radius:0;font-size:14px;font-weight:650;text-decoration:none;color:var(--color-text);background:transparent}
a.calday:hover{background:var(--color-raised)}
a.calday.on,a.calday.on:hover,button.calday.on{background:transparent;color:var(--color-forest)}
.calday{z-index:0}
a.calday::before,button.calday::before,span.calday[aria-disabled]::before{content:"";position:absolute;top:2px;left:50%;width:36px;height:36px;margin-left:-18px;border-radius:50%;z-index:-1}
a.calday.on::before,button.calday.on::before{background:var(--color-lime)}
.calday.today:not(.on)::before{box-shadow:inset 0 0 0 1.5px var(--color-lime)}
.caldot{width:5px;height:5px;border-radius:50%;background:var(--color-lime);display:block;position:relative;z-index:1;margin-top:4px}
a.calday.on .caldot,button.calday.on .caldot{background:var(--color-lime)}
span.calday{color:var(--t3);opacity:.4;font-weight:500}
span.calday.today{opacity:1;color:var(--color-text)}
a.calday.past:not(.on),button.calday.past:not(.on){color:var(--t3)}
.timelist{max-height:280px;overflow:auto;margin:0 0 12px;scroll-snap-type:y mandatory}
.timelist button{width:100%;height:48px;min-height:48px;margin:0;padding:0 16px;background:transparent;color:var(--color-text);border-radius:12px;font-weight:500;scroll-snap-align:center;justify-content:flex-start}
.timelist button.on{background:var(--color-lime);color:var(--color-forest)}
.timelist button:disabled{color:var(--t3);opacity:.45}
button.sheetwide{width:100%}
button.calday{width:100%;height:48px;min-height:0;padding:8px 0 0;background:transparent;color:var(--color-text);font-weight:650;border-radius:0;position:relative}
.calhead select.matmonth{flex:1;min-width:0;height:40px;margin:0;padding:0 28px 0 4px;border:0;border-radius:8px;background-color:transparent;color:var(--color-text);font-weight:650;font-size:16px;appearance:none;background-image:url("data:image/svg+xml,%3Csvg%20xmlns%3D'http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg'%20viewBox%3D'0%200%20256%20256'%3E%3Cpath%20fill%3D'%23F2F6F1'%20d%3D'M213.66,101.66l-80,80a8,8,0,0,1-11.32,0l-80-80A8,8,0,0,1,53.66,90.34L128,164.69l74.34-74.35a8,8,0,0,1,11.32,11.32Z'%2F%3E%3C%2Fsvg%3E");background-repeat:no-repeat;background-position:right 2px center;background-size:18px}
dialog.matpick{position:fixed;z-index:40;inset:0;margin:auto;width:min(360px,calc(100% - 32px));height:fit-content;max-height:min(640px,calc(100dvh - 32px));border:0;padding:0;background:transparent;color:var(--color-text);overflow:visible}
dialog.matpick::backdrop{background:var(--color-backdrop)}
dialog.matpick .sheet{background:var(--color-sheet);border:1px solid var(--color-sheet-border);border-radius:var(--radius-overlay);padding:20px 12px 8px;max-height:calc(100dvh - 32px);overflow:auto}
.matkicker{margin:0 12px 4px;color:var(--color-text-secondary);font-size:var(--type-b2-size);line-height:var(--type-b2-line)}
.matheadline{margin:0 12px 16px;font-size:2rem;line-height:1.15;font-weight:400;letter-spacing:-.02em}
.matactions{display:flex;justify-content:flex-end;gap:4px;margin:8px 4px 4px}
.yearrow{display:flex;align-items:center;justify-content:space-between;gap:8px;margin:0 4px 12px}
.yearrow .yearbtn{flex:1;height:40px;min-height:40px;margin:0;padding:0 8px;background:transparent;color:var(--color-text);font-size:16px;font-weight:650;border-radius:999px}
.yearrow .yearbtn.on{background:var(--color-lime);color:var(--color-forest)}
.yearrow button.calmonth:disabled{color:var(--t3);opacity:.35}
.monthgrid{display:grid;grid-template-columns:repeat(3,1fr);gap:12px 8px;margin:4px 8px 8px}
button.monthchip{width:100%;height:40px;min-height:40px;margin:0;padding:0 8px;border-radius:999px;background:transparent;color:var(--color-text);font-weight:650;font-size:14px}
button.monthchip.on{background:var(--color-lime);color:var(--color-forest);opacity:1}
button.monthchip:disabled:not(.on){background:transparent;color:var(--t3);opacity:.4}
.yearlist{max-height:220px;overflow:auto;margin:0 12px 8px;display:flex;flex-direction:column;gap:2px}
button.yearopt{width:100%;height:40px;min-height:40px;margin:0;border-radius:999px;background:transparent;color:var(--color-text);font-weight:650}
button.yearopt.on{background:var(--color-lime);color:var(--color-forest)}
button.mattext{height:40px;min-height:40px;padding:0 12px;background:none;color:var(--color-lime);font-weight:650}
.timebig{display:flex;align-items:center;gap:2px;margin:0 12px 8px;font-size:3rem;font-weight:400;line-height:1}
.timebig button{height:auto;min-height:0;padding:0 2px;background:none;color:var(--color-text-secondary);font:inherit;font-weight:400}
.timebig button.on{color:var(--color-lime)}
.ampm{display:flex;flex-direction:column;margin-left:12px;border:1px solid var(--color-control);border-radius:8px;overflow:hidden}
.ampm button{height:36px;min-height:36px;padding:0 10px;background:transparent;color:var(--color-text-secondary);font-size:14px;font-weight:650}
.ampm button.on{background:var(--color-lime);color:var(--color-forest)}
.clock{position:relative;width:256px;height:256px;margin:8px auto 4px;border-radius:50%;background:var(--color-surface-2)}
.clockhand{position:absolute;left:50%;top:50%;width:2px;height:78px;margin:-78px 0 0 -1px;background:var(--color-lime);transform-origin:center bottom;border-radius:2px;pointer-events:none;z-index:1}
.clock::after{content:"";position:absolute;left:50%;top:50%;width:8px;height:8px;margin:-4px 0 0 -4px;border-radius:50%;background:var(--color-lime);z-index:2}
button.clocknum{position:absolute;z-index:2;width:40px;height:40px;min-height:0;margin:-20px 0 0 -20px;padding:0;border-radius:50%;background:transparent;color:var(--color-text);font-weight:650;font-size:15px}
button.clocknum.on{background:var(--color-lime);color:var(--color-forest)}
.pickhold{position:absolute;width:1px;height:1px;margin:-1px;padding:0;overflow:hidden;clip:rect(0 0 0 0);border:0;opacity:0;pointer-events:none}
.calback{display:flex;align-items:center;gap:6px;height:40px;margin:0 0 8px;padding:0;background:none;color:var(--color-text);font-weight:650}
.panel{padding:4px 18px 18px;border-top:1px solid var(--line);background:var(--surface)}.panel h3{font-size:15px;font-weight:600;margin:18px 0 10px}
.pstat{padding:14px 0 2px}.pstatline{display:flex;align-items:center;gap:8px;flex-wrap:wrap}
.pstat .dot{width:10px;height:10px}.pstitle{font-size:20px;font-weight:650;letter-spacing:-.2px;line-height:1.2}
.pchips{margin-left:auto;display:flex;flex-wrap:wrap;gap:6px;align-items:center}
.preason{margin:6px 0 0;color:var(--t2);font-size:15px}
.panel .kv{padding:8px 0}.cred{display:inline-flex;align-items:center;gap:8px;color:var(--t1);text-align:right}
.pfoot{margin:10px 0 0}
.actpills{display:flex;flex-wrap:wrap;gap:8px;margin:14px 0 2px;align-items:center}
.actpills form{margin:0;flex:1}.actpills .btn{flex:1}
.actpills button:disabled{color:var(--t3);background:var(--color-chip)}
dialog.memberedit h2{margin:0 0 12px;font-size:var(--type-t2-size);line-height:var(--type-t2-line);font-weight:var(--type-t2-weight);letter-spacing:-.02em}
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
</style></head><body style="background:#090D0B;color:#F2F6F1;margin:0" class="{% if (tab=='home' or tab=='practices') and me() %}homefull{% if tab=='practices' %} schedopen{% endif %}{% elif tab=='profile' or tab=='member' %}profilepage{% if tab=='member' and editing %} profile-edit{% endif %}{% elif tab=='practice' or tab=='lineup_event' %}practicepage{% elif tab=='admin' or tab=='manage' %}adminpage{% endif %}">
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
{% macro hi_membership() %}{% set num = (me().usawp_number or '')|trim %}{% set tw = trial_window(me()) %}{% set on_trial = tw and tw.active and (me().usawp_status or '') != 'verified' %}{% if num %}{% set cl = clearance(me()) %}{% set dl = days_left(me().usawp_valid_until) %}{% set ns = namespace(tone='ok') %}{% if vr_pending or on_trial %}{% set ns.tone = 'warn' %}{% elif not cl.ok %}{% set ns.tone = 'bad' %}{% elif dl is not none and dl <= EXPIRING_DAYS %}{% set ns.tone = 'warn' %}{% else %}{% for it in cl.checks %}{% if it.days_left is not none and it.days_left >= 0 and it.days_left <= EXPIRING_DAYS %}{% set ns.tone = 'warn' %}{% endif %}{% endfor %}{% endif %}<a class="usawpchip{% if ns.tone != 'ok' %} {{ ns.tone }}{% endif %}" href="/profile#membership">{% if ns.tone == 'ok' %}<svg class="usawpok" width="16" height="16" viewBox="0 0 256 256" fill="currentColor" aria-hidden="true"><path d="M128,24A104,104,0,1,0,232,128,104.11,104.11,0,0,0,128,24Zm45.66,85.66-56,56a8,8,0,0,1-11.32,0l-24-24a8,8,0,0,1,11.32-11.32L112,148.69l50.34-50.35a8,8,0,0,1,11.32,11.32Z"/></svg>{% else %}<span class="dot {{ ns.tone }}" aria-hidden=true></span>{% endif %}USAWP #{{ num }}</a>{% elif on_trial and not vr_pending %}<a class="usawpchip warn" href="/profile#membership"><span class="dot warn" aria-hidden=true></span>Trial</a>{% endif %}{% endmacro %}
{% macro roster_status(r) %}{% set cl = clearance(r) %}{% set dl = days_left(r.usawp_valid_until) %}{% set tw = trial_window(r) %}{% set ex = expiry_notes(r, cl) %}{% set ns = namespace(tone='ok', text='Cleared', when='') %}
{% if dl is not none and dl >= 0 and dl <= EXPIRING_DAYS %}{% if dl == 0 %}{% set ns.when = 'expires today' %}{% elif dl == 1 %}{% set ns.when = 'expires in 1 day' %}{% else %}{% set ns.when = 'expires in ' ~ dl ~ ' days' %}{% endif %}{% endif %}
{% if tw and tw.active and r.usawp_status != 'verified' and not ex.membership %}{% set ns.tone = 'warn' %}{% set ns.text = trial_badge(tw) %}{% set ns.when = '' %}
{% elif tw and tw.expired and r.usawp_status != 'verified' %}{% set ns.tone = 'bad' %}{% set ns.text = 'Trial ended ' ~ tw.ends %}
{% elif not cl.ok %}{% set ns.tone = 'bad' %}{% set ns.text = 'Not cleared' %}
{% elif ns.when %}{% set ns.tone = 'warn' %}{% set ns.text = 'Expiring soon' %}{% endif %}
<span class="st st-{{ ns.tone }} rowstatus">{{ ns.text }}{% if ns.when %} · {{ ns.when }}{% endif %}</span>{% endmacro %}
{% macro member_status(r) %}{{ roster_status(r) }}{% endmacro %}
{% macro status_dot(s) %}{% set kind = {'verified':'ok','expired':'bad','pending':'warn'}.get(s, '') %}<span class="dot{% if kind %} {{kind}}{% endif %}" aria-hidden=true></span>{% endmacro %}
{% macro checkin_status(r) %}{{ person_sub(r) }}{% endmacro %}
{% macro person_sub(r) %}{% set cl = clearance(r) %}{% set dl = days_left(r.usawp_valid_until) %}{% set tw = trial_window(r) %}{% set ex = expiry_notes(r, cl) %}{% set ns = namespace(tone='ok', word='Cleared', rest='') %}
{% if dl is not none and dl >= 0 and dl <= EXPIRING_DAYS %}{% if dl == 0 %}{% set ns.rest = ' · expires today' %}{% elif dl == 1 %}{% set ns.rest = ' · expires in 1 day' %}{% else %}{% set ns.rest = ' · expires in ' ~ dl ~ ' days' %}{% endif %}{% endif %}
{% if tw and tw.active and r.usawp_status != 'verified' and not ex.membership %}{% set ns.tone = 'warn' %}{% set ns.word = 'Trial' %}{% set ns.rest = ' · ' ~ trial_left_phrase(tw) %}
{% elif tw and tw.expired and r.usawp_status != 'verified' %}{% set ns.tone = 'bad' %}{% set ns.word = 'Trial ended ' ~ tw.ends %}{% set ns.rest = '' %}
{% elif not cl.ok %}{% set ns.tone = 'bad' %}{% set ns.word = 'Not cleared' %}
{% elif ns.rest %}{% set ns.tone = 'warn' %}{% set ns.word = 'Expiring soon' %}{% endif %}
{% set thru = '' %}{% if not (tw and tw.active and r.usawp_status != 'verified') and r.usawp_valid_until and (dl is none or dl < 0 or dl > EXPIRING_DAYS) %}{% set thru = ' · thru ' ~ fmt_long(r.usawp_valid_until) %}{% endif %}
{% set detail = (ns.rest or '') ~ thru %}
<span class="psub ell st-{{ ns.tone }}"><span class=stword>{{ ns.word }}</span>{% if detail %}<span class=strest>{{ detail }}</span>{% endif %}</span>{% endmacro %}
{% macro person_mark(r) %}{% set cl = clearance(r) %}{% set dl = days_left(r.usawp_valid_until) %}{% set tw = trial_window(r) %}{% set ex = expiry_notes(r, cl) %}{% set ns = namespace(tone='ok') %}
{% if tw and tw.active and r.usawp_status != 'verified' and not ex.membership %}{% set ns.tone = 'warn' %}
{% elif tw and tw.expired and r.usawp_status != 'verified' %}{% set ns.tone = 'bad' %}
{% elif not cl.ok %}{% set ns.tone = 'bad' %}
{% elif dl is not none and dl >= 0 and dl <= EXPIRING_DAYS %}{% set ns.tone = 'warn' %}{% endif %}
<span class="psub st-{{ ns.tone }} coachmark" aria-hidden="true"></span>{% endmacro %}
{% macro person_link(r) %}<a class=ci-name href="/admin/member/{{ r.id }}">{% if r.photo %}<span class="avatar ciav"><img src="/avatar/{{ r.id }}?v={{ r.photo }}" alt="" width="40" height="40"></span>{% else %}<span class="avatar ciav">{{ initials(r) }}</span>{% endif %}<span class=grow style="min-width:0"><span class=ell style="display:block;font-weight:500">{{ display_first(r) }} {{ r.last }}</span>{{ person_sub(r) }}{{ caller() }}</span></a>{% endmacro %}
{% macro admin_page(title, subtitle='') %}
<div class=pagehead>
<div class=pagerow><h1>{{ title }}</h1>{% if caller is defined %}{{ caller() }}{% endif %}</div>
{% if subtitle %}<p class=pagesub>{{ subtitle }}</p>{% endif %}
</div>
{% endmacro %}
{% macro manage_row(href, title, desc, icon, count=0, tone='info') %}<a class=mrow href="{{ href }}"><span class=mico aria-hidden=true>{{ icon|safe }}</span><span class=grow><span class=mtitle>{{ title }}</span>{% if desc %}<span class=mdesc>{{ desc }}</span>{% endif %}</span>{% if count %}<span class="mbadge {{ tone }}">{{ count if count < 100 else '99+' }}</span>{% endif %}<span class=mchev aria-hidden=true><svg width="18" height="18" viewBox="0 0 256 256" fill="currentColor"><path d="M181.66,133.66l-80,80a8,8,0,0,1-11.32-11.32L164.69,128,90.34,53.66a8,8,0,0,1,11.32-11.32l80,80A8,8,0,0,1,181.66,133.66Z"/></svg></span></a>{% endmacro %}
{% macro event_chooser(staff) %}
<h2 class=planask>What are you planning?</h2>
<div class=planlane>
{% if staff %}<div class=card>
<h2>Team schedule</h2>
<p class="t3 sm">Practice, scrimmage, and game. Shows on Home.</p>
<div class=planlinks>
<a class=chip href="/events/new?type=practice">Practice</a>
<a class=chip href="/events/new?type=scrimmage">Scrimmage</a>
<a class=chip href="/events/new?type=game">Game</a>
</div>
</div>{% endif %}
<div class=card>
<h2>Lineup event</h2>
<p class="t3 sm">Tournaments, trips, and community events. Shows on Lineup.</p>
<div class=planlinks>
{% if staff %}
<a class=chip href="/lineup/new?mode=create&amp;event_type=Tournament">Tournament</a>
<a class=chip href="/lineup/new?mode=create&amp;event_type=Competition">Competition</a>
<a class=chip href="/lineup/new?mode=create&amp;event_type=Clinic">Clinic/Camp</a>
<a class=chip href="/lineup/new?mode=create&amp;event_type=Trip">Trip</a>
<a class=chip href="/lineup/new?mode=create&amp;event_type=Social">Social/Activity</a>
<a class=chip href="/lineup/new?mode=create&amp;event_type=Volunteer">Volunteer</a>
<a class=chip href="/lineup/new?mode=create&amp;event_type=Fundraiser">Fundraiser</a>
<a class=chip href="/lineup/new?mode=create&amp;event_type=Meeting">Meeting/Workshop</a>
<a class=chip href="/lineup/new?mode=create&amp;event_type=Other">Other</a>
{% else %}
<a class=chip href="/lineup/new?mode=suggest&amp;event_type=Social">Social/Activity</a>
<a class=chip href="/lineup/new?mode=suggest&amp;event_type=Volunteer">Volunteer</a>
{% endif %}
</div>
</div>
</div>
{% endmacro %}
{% macro detail_hiddens(r) %}{{csrf_field()}}<input type=hidden name=member_id value={{r.id}}><input type=hidden name=date value="{{date}}"><input type=hidden name=q value="{{q}}">{% if view is defined %}<input type=hidden name=list_view value="{{ view }}">{% endif %}{% if coach_filter is defined %}<input type=hidden name=list_coach value="{{'eligible' if coach_filter else ''}}"><input type=hidden name=list_referee value="{{'eligible' if referee_filter else ''}}">{% endif %}{% endmacro %}
{% macro cred_side(iso) %}{% if iso %}<span class=cred><span class="dot {{ date_dot(iso) }}" aria-hidden=true></span>{{ fmt_long(iso) }}</span>{% else %}<span class=t3>Not on file</span>{% endif %}{% endmacro %}
{% macro date_field(label, name, value) %}<label class="datefield{% if not value %} empty{% endif %}">{{ label }}<input type=date name={{ name }} value="{{ value or '' }}"><span class=dateph>Not on file · add date</span></label>{% endmacro %}
{% macro rsvp_btn(label, selected, on_value) -%}
<button class="btn {{ 'btn-primary' if selected else 'btn-secondary' }}" name=action value="{{ 'clear' if selected else on_value }}">{% if selected %}<svg class=rsvpcheck width="16" height="16" viewBox="0 0 256 256" fill="currentColor" aria-hidden="true"><path d="M229.66,77.66l-128,128a8,8,0,0,1-11.32,0l-56-56a8,8,0,0,1,11.32-11.32L96,188.69,218.34,66.34a8,8,0,0,1,11.32,11.32Z"/></svg>{% endif %}{{ label }}</button>
{%- endmacro %}
{% macro glyph_clock() %}<svg class="nxglyph" width="16" height="16" viewBox="0 0 256 256" fill="currentColor" aria-hidden="true"><path d="M128,24A104,104,0,1,0,232,128,104.11,104.11,0,0,0,128,24Zm0,192a88,88,0,1,1,88-88A88.1,88.1,0,0,1,128,216Zm64-88a8,8,0,0,1-8,8H128a8,8,0,0,1-8-8V72a8,8,0,0,1,16,0v48h48A8,8,0,0,1,192,128Z"/></svg>{% endmacro %}
{% macro glyph_pin() %}<svg class="nxglyph" width="16" height="16" viewBox="0 0 256 256" fill="currentColor" aria-hidden="true"><path d="M128,64a40,40,0,1,0,40,40A40,40,0,0,0,128,64Zm0,64a24,24,0,1,1,24-24A24,24,0,0,1,128,128Zm0-112a88.1,88.1,0,0,0-88,88c0,31.4,14.51,64.68,42,96.25a254.19,254.19,0,0,0,41.45,38.3,8,8,0,0,0,9.18,0A254.19,254.19,0,0,0,174,200.25c27.45-31.57,42-64.85,42-96.25A88.1,88.1,0,0,0,128,16Zm0,206c-16.53-13-72-60.75-72-118a72,72,0,0,1,144,0C200,161.23,144.53,209,128,222Z"/></svg>{% endmacro %}
{% macro glyph_people() %}<svg class="nxglyph" width="16" height="16" viewBox="0 0 256 256" fill="currentColor" aria-hidden="true"><path d="M117.25,157.92a60,60,0,1,0-66.5,0A95.83,95.83,0,0,0,3.53,195.63a8,8,0,1,0,13.4,8.74,80,80,0,0,1,134.14,0,8,8,0,0,0,13.4-8.74A95.83,95.83,0,0,0,117.25,157.92ZM40,108a44,44,0,1,1,44,44A44.05,44.05,0,0,1,40,108Zm210.14,98.7a8,8,0,0,1-11.07-2.33A79.83,79.83,0,0,0,172,168a8,8,0,0,1,0-16,44,44,0,1,0-16.34-84.87,8,8,0,1,1-5.94-14.85,60,60,0,0,1,55.53,105.64,95.83,95.83,0,0,1,47.22,37.71A8,8,0,0,1,250.14,206.7Z"/></svg>{% endmacro %}
{% macro upload_field(name, mode='image', hint='', accept='', src='', clear_name='') %}
{%- set is_file = mode == 'file' -%}
{%- set label = 'Upload a file' if is_file else 'Upload an image' -%}
{%- set hint_text = hint or ('CSV' if is_file else 'PNG or JPG') -%}
{%- set acc = accept or ('.csv,.xlsx' if is_file else 'image/jpeg,image/png,image/gif,image/webp,image/heic,image/heif,.heic') -%}
<div class="dropzone{% if src %} has{% endif %}" data-dropzone data-mode="{{ 'file' if is_file else 'image' }}"><input class=pick type=file name={{ name }} accept="{{ acc }}" aria-label="{{ label }}">{% if clear_name %}<input type=hidden name={{ clear_name }} value="" data-clear>{% endif %}<button type=button class=dropempty {% if src %}hidden{% endif %}>{% if is_file %}<svg class=dropico viewBox="0 0 256 256" fill="currentColor" aria-hidden="true"><path d="M213.66,82.34l-56-56A8,8,0,0,0,152,24H56A16,16,0,0,0,40,40V216a16,16,0,0,0,16,16H200a16,16,0,0,0,16-16V88A8,8,0,0,0,213.66,82.34ZM160,51.31,188.69,80H160ZM200,216H56V40h88V88a8,8,0,0,0,8,8h48V216Z"/></svg>{% else %}<svg class=dropico viewBox="0 0 256 256" fill="currentColor" aria-hidden="true"><path d="M216,40H40A16,16,0,0,0,24,56V200a16,16,0,0,0,16,16H216a16,16,0,0,0,16-16V56A16,16,0,0,0,216,40Zm0,16V158.75l-26.07-26.06a16,16,0,0,0-22.63,0l-20,20-44-44a16,16,0,0,0-22.62,0L40,149.37V56ZM40,172l52-52,80,80H40Zm176,28H194.63l-36-36,20-20L216,181.38V200ZM96,100a12,12,0,1,1,12-12A12,12,0,0,1,96,100Z"/></svg>{% endif %}<span class=droplink>{{ label }}</span><span class=drophint>{{ hint_text }}</span></button><div class=dropfill {% if not src %}hidden{% endif %}><img alt="" data-preview {% if src %}src="{{ src }}"{% endif %}><div class=filemeta><span class=dropname data-name></span><span class=dropsize data-size></span></div><div class=dropacts><button type=button data-replace>Replace</button><button type=button data-remove>Remove</button></div></div></div>
{%- endmacro %}
{% macro social_icon() %}<span class=nxicon aria-hidden=true><svg width="24" height="24" viewBox="0 0 256 256" fill="currentColor" aria-hidden="true"><path d="M237.66,45.66A8,8,0,0,0,232,32H24a8,8,0,0,0-5.66,13.66L120,147.31V208H88a8,8,0,0,0,0,16h80a8,8,0,0,0,0-16H136V147.31ZM43.31,48H212.69l-16,16H59.31ZM128,132.69,75.31,80H180.69Z"/></svg></span>{% endmacro %}
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
{{ upload_field('image', src=('/practice-image/' ~ p.id ~ '?v=' ~ p.image) if p.image else '', clear_name='image_clear') }}
<p class="t3 sm">Shown on the Home card only. Leave the file empty to keep the current picture.</p>
<button class="btn btn-primary full" name=action value=image>Save</button></form></div></dialog>
<dialog class=modal id=notes{{ p.id }}><div class=sheet><h2 style="margin:0 0 12px">Notes</h2>
<form method=post action="/practices/{{ p.id }}">{{ csrf_field() }}<input type=hidden name=pid value={{ p.id }}><input type=hidden name=back value="{{ back }}">
<label>Notes<textarea name=note rows=4>{{ p.note or '' }}</textarea></label>
<button class="btn btn-primary full" name=action value=note>Save</button></form></div></dialog>
{% endmacro %}
{% macro practice_host_more(p, back) %}
<span class=more><button type=button class=morebtn aria-label="More for {{ fmt_d(p.date) }}" aria-haspopup=menu aria-expanded=false><svg width="20" height="20" viewBox="0 0 256 256" fill="currentColor" aria-hidden="true"><path d="M140,128a12,12,0,1,1-12-12A12,12,0,0,1,140,128Zm56-12a12,12,0,1,0,12,12A12,12,0,0,0,196,116ZM60,116a12,12,0,1,0,12,12A12,12,0,0,0,60,116Z"/></svg></button>
<div class=menu hidden role=menu>
<button type=button data-open="social{{ p.id }}">After-practice social</button>
<button type=button data-open="message{{ p.id }}">Coach message</button>
<button type=button data-open="image{{ p.id }}">Practice image</button>
</div></span>
{{ practice_extra_dialogs(p, back) }}
{% endmacro %}
{% macro practice_more(p, coach_ids, back) %}
<span class=more><button type=button class=morebtn aria-label="More for {{ fmt_d(p.date) }}" aria-haspopup=menu aria-expanded=false><svg width="20" height="20" viewBox="0 0 256 256" fill="currentColor" aria-hidden="true"><path d="M140,128a12,12,0,1,1-12-12A12,12,0,0,1,140,128Zm56-12a12,12,0,1,0,12,12A12,12,0,0,0,196,116ZM60,116a12,12,0,1,0,12,12A12,12,0,0,0,60,116Z"/></svg></button>
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
<p class="t2 sm">{% if practice_is_month(p) %}{{ practice_when(p) }} at {{ p.location }}.{% else %}{{ fmt_d(p.date) }}, {{ fmt_t(p.start) }}–{{ fmt_t(p.end) }} at {{ p.location }}.{% endif %}</p>
<form method=post action="/practices/{{ p.id }}">{{ csrf_field() }}<input type=hidden name=pid value={{ p.id }}>
<div class=row><button class="btn btn-danger" name=action value=delete>Delete practice</button><button type=button class="btn btn-secondary" onclick="this.closest('dialog').close()">Cancel</button></div></form></div></dialog>
{% endmacro %}
{% macro mount_map(id, pins, mode) %}<section class="homemap cardmap {{ 'banner' if mode == 'card' else 'still' }}" id="{{ id }}" {% if mode == 'still' %}aria-hidden=true{% else %}aria-label="Map"{% endif %}></section>
<script>(function(){var pins={{ pins|tojson }};function start(){var el=document.getElementById({{ id|tojson }});if(el&&window.grunionsMountMap)grunionsMountMap(el,{pins:pins,mode:'{{ mode }}'});}if(window.grunionsMountMap)start();else document.addEventListener('DOMContentLoaded',start);})();</script>{% endmacro %}
{% macro event_hero(id, pins, banner_src, label) %}{% if banner_src %}<div class=evhero><img src="{{ banner_src }}" alt=""></div>{% else %}{{ mount_map(id, pins, 'card') }}{% endif %}{% endmacro %}
{% macro whos_going(people) %}<div class=seclabel>Who's going</div><div class=list>{% for r in people %}<div class=li>{% if me().is_admin or is_staff() %}<a class=ci-name href="/admin/member/{{ r.id }}">{% else %}<span class=ci-name>{% endif %}{% if r.photo %}<span class="avatar ciav"><img src="/avatar/{{ r.id }}?v={{ r.photo }}" alt="" width="40" height="40"></span>{% else %}<span class="avatar ciav">{{ initials(r) }}</span>{% endif %}<span class=grow style="min-width:0"><span class=ell style="display:block;font-weight:500">{{ display_first(r) }} {{ r.last }}</span></span>{% if me().is_admin or is_staff() %}</a>{% else %}</span>{% endif %}</div>{% else %}<div class=li><span class=t3>No one yet.</span></div>{% endfor %}</div>{% endmacro %}
{% macro event_location(id, pins, name, sub, href) %}<div class=seclabel>Location</div><div class="list loccard">{{ mount_map(id, pins, 'still') }}<a class="li locrow" href="{{ href }}" target=_blank rel=noopener {% if pins %}data-directions="{{ pins[0].lat }},{{ pins[0].lng }}"{% endif %}><span class=grow style="min-width:0"><span class=ell style="display:block;font-weight:500">{{ name }}</span>{% if sub and sub != name %}<span class="t3 sm">{{ sub }}</span>{% endif %}</span></a></div>{% endmacro %}
{% macro lineup_card(e, back='/lineup') %}<div class="card tap tripcard" onclick="if(event.target.closest('button,a,form,input,select,textarea,label'))return;location.href='/lineup/{{ e.id }}'">
<a class=cardlink href="/lineup/{{ e.id }}">
<div class=nxcardhead><div class=nxtitle>{{ e.title }}</div></div>
{% if e.tag %}<p class="eventtag">{{ e.tag }}</p>{% endif %}
{% if e.host_org %}<div class="t3 sm hostorg">Hosted by {{ e.host_org }}</div>{% endif %}
<div class=nxmain><div class=datetile>{% if e.tile.wd %}<span class=wd>{{ e.tile.wd }}</span>{% endif %}<span class=dn>{{ e.tile.dn }}</span><span class=mo>{{ e.tile.mo }}</span></div>
<div class="grow schedrows"><div class=nxrow>{{ glyph_clock() }}<span>{{ e.when }}</span></div>
{% if e.city %}<div class=nxrow>{{ glyph_pin() }}<span>{{ e.city }}</span></div>{% endif %}
<div class=nxrow>{{ glyph_people() }}<span>{{ e.count_line }}</span></div></div></div></a>
{% if e.status != 'published' %}<div class="t3 sm">{{ e.status_label }}{% if e.review_note %} · {{ e.review_note }}{% endif %}</div>{% else %}
<form method=post action=/lineup class="pills rsvprow">{{ csrf_field() }}<input type=hidden name=event_id value={{ e.id }}><input type=hidden name=back value="{{ back }}">
{{ rsvp_btn('Interested', e.mine == 'interested', 'interested') }}
{{ rsvp_btn('Going', e.mine == 'going', 'going') }}
{{ rsvp_btn('Not going', e.mine == 'notgoing', 'notgoing') }}</form>{% endif %}
</div>{% endmacro %}
{% macro app_header(fade, entry, show_plus) %}<header class="homehead apphead{% if fade %} homefade{% endif %}"{% if entry %} data-entry="{{ entry }}"{% endif %}><div class=headmain>{{ caller() }}</div>{% if show_plus %}<a class=headplus href="/events/new" aria-label="{{ 'Create event' if can_host_practice() else 'Suggest an event' }}"><svg width="24" height="24" viewBox="0 0 256 256" fill="currentColor" aria-hidden="true"><path d="M224,128a8,8,0,0,1-8,8H136v80a8,8,0,0,1-16,0V136H40a8,8,0,0,1,0-16h80V40a8,8,0,0,1,16,0v80h80A8,8,0,0,1,224,128Z"/></svg></a>{% endif %}<a class=avatar href=/profile aria-label="Profile">{% if me().photo %}<img src="/avatar/{{ me().id }}?v={{ me().photo }}" alt="" width="44" height="44">{% else %}{{ initials(me()) }}{% endif %}</a></header>{% endmacro %}
{% if tab == 'profile' and me() %}<header class=profilebar>
<div class=left><button type=button class="profileback viewonly" id=profileBack aria-label="Back"><svg width="24" height="24" viewBox="0 0 256 256" fill="currentColor" aria-hidden="true"><path d="M224,128a8,8,0,0,1-8,8H59.31l58.35,58.34a8,8,0,0,1-11.32,11.32l-72-72a8,8,0,0,1,0-11.32l72-72a8,8,0,0,1,11.32,11.32L59.31,120H216A8,8,0,0,1,224,128Z"/></svg></button><button type=button class="profileact editonly" id=profileCancel>Cancel</button></div>
<h1>Profile</h1>
<div class=right><button type=button class="profileact viewonly" id=profileEdit>Edit</button><button type=submit class="profileact savebtn editonly" id=profileSave form=profileForm>Save</button></div>
</header>{% elif me() and tab == 'member' %}<header class=profilebar>
<div class=left><button type=button class="profileback viewonly" id=profileBack aria-label="Back"><svg width="24" height="24" viewBox="0 0 256 256" fill="currentColor" aria-hidden="true"><path d="M224,128a8,8,0,0,1-8,8H59.31l58.35,58.34a8,8,0,0,1-11.32,11.32l-72-72a8,8,0,0,1,0-11.32l72-72a8,8,0,0,1,11.32,11.32L59.31,120H216A8,8,0,0,1,224,128Z"/></svg></button>{% if me().is_admin %}<button type=button class="profileact editonly" id=profileCancel>Cancel</button>{% endif %}</div>
<h1>{{ display_first(m) }} {{ m.last }}</h1>
<div class=right>{% if me().is_admin %}<button type=button class="profileact viewonly" id=profileEdit>Edit</button><button type=submit class="profileact savebtn editonly" id=profileSave form=memberForm name=action value=edit>Save</button>{% endif %}</div>
</header>{% elif me() and tab == 'lineup_edit' %}<header class=profilebar><div class=left><a class=profileact href=/lineup>Cancel</a></div><h1>Event</h1><div class=right><button type=submit class="profileact savebtn" form=eventForm name=action value=save>{{ save_label or 'Save' }}</button></div></header>{% elif me() and tab == 'lineup_event' %}<header class=profilebar><div class=left>{% if from_admin %}<a class=profileback href="/admin?date={{ admin_date }}" aria-label="Back">{% else %}<a class=profileback href=/lineup aria-label="Back">{% endif %}<svg width="24" height="24" viewBox="0 0 256 256" fill="currentColor" aria-hidden="true"><path d="M224,128a8,8,0,0,1-8,8H59.31l58.35,58.34a8,8,0,0,1-11.32,11.32l-72-72a8,8,0,0,1,0-11.32l72-72a8,8,0,0,1,11.32,11.32L59.31,120H216A8,8,0,0,1,224,128Z"/></svg></a></div><h1>Event</h1><div class=right>{% if e.can_edit %}<a class=profileact href="/lineup/{{ e.id }}/edit">Edit</a>{% endif %}</div></header>{% elif me() and tab == 'series_edit' %}<header class=profilebar><div class=left><a class=profileact href=/practices>Cancel</a></div><h1>Series</h1><div class=right><button type=submit class="profileact savebtn" form=seriesForm>Save</button></div></header>{% elif me() and tab == 'practice' %}<header class=profilebar><div class=left>{% if editing or plan_editing %}<a class=profileact href="/practices/{{ x.p.id }}{% if from_admin %}?from=admin{% endif %}">Cancel</a>{% else %}<a class=profileback href="{% if from_admin %}/admin?date={{ x.p.date }}{% else %}/practices{% endif %}" aria-label="Back"><svg width="24" height="24" viewBox="0 0 256 256" fill="currentColor" aria-hidden="true"><path d="M224,128a8,8,0,0,1-8,8H59.31l58.35,58.34a8,8,0,0,1-11.32,11.32l-72-72a8,8,0,0,1,0-11.32l72-72a8,8,0,0,1,11.32,11.32L59.31,120H216A8,8,0,0,1,224,128Z"/></svg></a>{% endif %}</div><h1>{{ SPORTS.ACTIVITY_NAME.get(x.p.activity_type or 'practice', 'Practice') }}</h1><div class=right>{% if editing %}<button type=submit class="profileact savebtn" form=practiceForm name=action value=edit>Save</button>{% elif plan_editing %}<button type=submit class="profileact savebtn" form=practiceForm name=action value=plan>Save</button>{% elif me().is_admin or is_staff() %}<a class=profileact href="/practices/{{ x.p.id }}?edit=1{% if from_admin %}&amp;from=admin{% endif %}">Edit</a>{% endif %}</div></header>{% elif me() and tab == 'event_new' %}<header class=profilebar><div class=left><a class=profileact href="{{ plan_back }}">Cancel</a></div><h1>{{ plan_title or 'Create event' }}</h1><div class=right>{% if plan_save %}<button type=submit class="profileact savebtn" form=planForm name=action value=preview>{{ plan_save }}</button>{% endif %}</div></header>{% elif me() %}{% call app_header(tab == 'home' or tab == 'practices', ('schedule' if tab == 'practices' else 'home') if (tab == 'home' or tab == 'practices') else '', tab == 'lineup' or (can_host_practice() and tab in ('home', 'practices', 'chat', 'admin', 'manage'))) %}{% if tab == 'home' or tab == 'practices' %}<div class=titlestack><div class=titlecross><h1 class=hititle>Hi, {{ display_first(me()) }}</h1><h1 class=schedtitle aria-hidden=true>Schedule</h1></div>{{ hi_membership() }}</div>{% elif tab == 'chat' and is_staff() %}<div class="seg headtabs chiprow" role=tablist><a href=/chat class="chip{{' chip-active on' if ch=='team'}}" data-badge=team>Team{{ bubble(badges().team) }}</a><a href="/chat?c=coaches" class="chip{{' chip-active on' if ch=='coaches'}}" data-badge=coaches>Coaches{{ bubble(badges().coaches) }}</a></div>{% elif tab == 'chat' %}<h1>Team</h1>{% elif tab == 'manage' %}<h1>Manage</h1>{% elif tab == 'admin' %}<a class=hubback href=/manage aria-label="Back"><svg width="24" height="24" viewBox="0 0 256 256" fill="currentColor" aria-hidden="true"><path d="M224,128a8,8,0,0,1-8,8H59.31l58.35,58.34a8,8,0,0,1-11.32,11.32l-72-72a8,8,0,0,1,0-11.32l72-72a8,8,0,0,1,11.32,11.32L59.31,120H216A8,8,0,0,1,224,128Z"/></svg></a>{% elif tab == 'lineup' %}<h1>Lineup</h1>{% elif tab == 'notifications' %}<h1>Notifications</h1>{% else %}<h1>{{ display_first(me()) }}</h1>{% endif %}{% endcall %}{% else %}<header><a class=brand href=/>Grunions</a></header>{% endif %}<main>
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
 "home": '<svg width="24" height="24" viewBox="0 0 256 256" fill="currentColor" aria-hidden="true"><path d="M219.31,108.68l-80-80a16,16,0,0,0-22.62,0l-80,80A15.87,15.87,0,0,0,32,120v96a8,8,0,0,0,8,8h64a8,8,0,0,0,8-8V160h32v56a8,8,0,0,0,8,8h64a8,8,0,0,0,8-8V120A15.87,15.87,0,0,0,219.31,108.68ZM208,208H160V152a8,8,0,0,0-8-8H104a8,8,0,0,0-8,8v56H48V120l80-80,80,80Z"/></svg>',
 "cal": '<svg width="20" height="20" viewBox="0 0 256 256" fill="currentColor" aria-hidden="true"><path d="M208,32H184V24a8,8,0,0,0-16,0v8H88V24a8,8,0,0,0-16,0v8H48A16,16,0,0,0,32,48V208a16,16,0,0,0,16,16H208a16,16,0,0,0,16-16V48A16,16,0,0,0,208,32ZM72,48v8a8,8,0,0,0,16,0V48h80v8a8,8,0,0,0,16,0V48h24V80H48V48ZM208,208H48V96H208V208Z"/></svg>',
 "lineup": '<svg width="24" height="24" viewBox="0 0 256 256" fill="currentColor" aria-hidden="true"><path d="M208,32H184V24a8,8,0,0,0-16,0v8H88V24a8,8,0,0,0-16,0v8H48A16,16,0,0,0,32,48V208a16,16,0,0,0,16,16H208a16,16,0,0,0,16-16V48A16,16,0,0,0,208,32ZM72,48v8a8,8,0,0,0,16,0V48h80v8a8,8,0,0,0,16,0V48h24V80H48V48ZM208,208H48V96H208V208Z"/></svg>',
 "chat": '<svg width="24" height="24" viewBox="0 0 256 256" fill="currentColor" aria-hidden="true"><path d="M128,24A104,104,0,0,0,36.18,176.88L24.83,210.93a16,16,0,0,0,20.24,20.24l34.05-11.35A104,104,0,1,0,128,24Zm0,192a87.87,87.87,0,0,1-44.06-11.81,8,8,0,0,0-6.54-.67L40,216,52.47,178.6a8,8,0,0,0-.66-6.54A88,88,0,1,1,128,216Z"/></svg>',
 "admin": '<svg width="24" height="24" viewBox="0 0 256 256" fill="currentColor" aria-hidden="true"><path d="M208,40H48A16,16,0,0,0,32,56v56c0,52.72,25.52,84.67,46.93,102.19,23.06,18.86,46,25.26,47,25.53a8,8,0,0,0,4.2,0c1-.27,23.91-6.67,47-25.53C198.48,196.67,224,164.72,224,112V56A16,16,0,0,0,208,40Zm0,72c0,37.07-13.66,67.16-40.6,89.42A129.3,129.3,0,0,1,128,223.62a128.25,128.25,0,0,1-38.92-21.81C61.82,179.51,48,149.3,48,112l0-56,160,0ZM82.34,141.66a8,8,0,0,1,11.32-11.32L112,148.69l50.34-50.35a8,8,0,0,1,11.32,11.32l-56,56a8,8,0,0,1-11.32,0Z"/></svg>',
 "manage": '<svg width="24" height="24" viewBox="0 0 256 256" fill="currentColor" aria-hidden="true"><path d="M216,48V208a8,8,0,0,1-8,8H48a8,8,0,0,1-8-8V48a8,8,0,0,1,8-8H208A8,8,0,0,1,216,48ZM200,56H136v64h64Zm0,80H136v64h64ZM56,200H120V136H56Zm0-80H120V56H56Z"/></svg>',
}

def _nav_anchor(key, href, label, on, badge=""):
    """One circular destination. on is True or a Jinja condition. No visible label."""
    if on is True:
        state = ' class="on" aria-current=page'
    elif on:
        state = "{%% if %s %%} class=\"on\" aria-current=page{%% endif %%}" % on
    else:
        state = ""
    extra = (" data-badge=%s" % badge) if badge else ""
    bubble = ("{{ bubble(badges().%s) }}" % badge) if badge else ""
    return '<a href=%s%s aria-label="%s"%s>%s%s</a>' % (href, state, label, extra, _nav_icon(key), bubble)

_NAV_FILL = {
 'home': '<svg width="24" height="24" viewBox="0 0 256 256" fill="currentColor" aria-hidden="true"><path d="M224,120v96a8,8,0,0,1-8,8H160a8,8,0,0,1-8-8V164a4,4,0,0,0-4-4H108a4,4,0,0,0-4,4v52a8,8,0,0,1-8,8H40a8,8,0,0,1-8-8V120a16,16,0,0,1,4.69-11.31l80-80a16,16,0,0,1,22.62,0l80,80A16,16,0,0,1,224,120Z"/></svg>',
 'lineup': '<svg width="24" height="24" viewBox="0 0 256 256" fill="currentColor" aria-hidden="true"><path d="M208,32H184V24a8,8,0,0,0-16,0v8H88V24a8,8,0,0,0-16,0v8H48A16,16,0,0,0,32,48V208a16,16,0,0,0,16,16H208a16,16,0,0,0,16-16V48A16,16,0,0,0,208,32Zm0,48H48V48H72v8a8,8,0,0,0,16,0V48h80v8a8,8,0,0,0,16,0V48h24Z"/></svg>',
 'chat': '<svg width="24" height="24" viewBox="0 0 256 256" fill="currentColor" aria-hidden="true"><path d="M232,128A104,104,0,0,1,79.12,219.82L45.07,231.17a16,16,0,0,1-20.24-20.24l11.35-34.05A104,104,0,1,1,232,128Z"/></svg>',
 'admin': '<svg width="24" height="24" viewBox="0 0 256 256" fill="currentColor" aria-hidden="true"><path d="M208,40H48A16,16,0,0,0,32,56v56c0,52.72,25.52,84.67,46.93,102.19,23.06,18.86,46,25.26,47,25.53a8,8,0,0,0,4.2,0c1-.27,23.91-6.67,47-25.53C198.48,196.67,224,164.72,224,112V56A16,16,0,0,0,208,40Zm-34.32,69.66-56,56a8,8,0,0,1-11.32,0l-24-24a8,8,0,0,1,11.32-11.32L112,148.69l50.34-50.35a8,8,0,0,1,11.32,11.32Z"/></svg>',
 'manage': '<svg width="24" height="24" viewBox="0 0 256 256" fill="currentColor" aria-hidden="true"><path d="M208,32H48A16,16,0,0,0,32,48V208a16,16,0,0,0,16,16H208a16,16,0,0,0,16-16V48A16,16,0,0,0,208,32ZM112,208H48V136h64Zm0-88H48V48h64Zm96,88H128V136h80Zm0-88H128V48h80Z"/></svg>'
}

def _nav_icon(key):
    return '<span class=ico-reg>%s</span><span class=ico-fill>%s</span>' % (ICONS[key], _NAV_FILL[key])

_HOME_ON = "tab=='home' or tab=='practices' or tab=='practice' or tab=='series_edit'"
_LINEUP_ON = "tab=='lineup' or tab=='lineup_edit' or tab=='lineup_event'"
TABS = ("""</main>{% if me() and tab != 'profile' and tab != 'member' and tab != 'event_new' %}<nav class="tabs noprint" data-total="{{ badges().total }}">"""
 + _nav_anchor("home", "/home", "Home", _HOME_ON, "schedule")
 + _nav_anchor("lineup", "/lineup", "Lineup", _LINEUP_ON)
 + _nav_anchor("chat", "/chat", "Chat", "tab=='chat'", "chat")
 + "{% if can_host_practice() %}" + _nav_anchor("manage", "/manage", "Manage", "tab=='admin' or tab=='manage'")
 + """{% endif %}
</nav>{% endif %}
<script>
if('serviceWorker' in navigator) navigator.serviceWorker.register('/sw.js?v=85');
if(window.grunionsDropzones) grunionsDropzones();
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
  var still=opts.mode==='still';
  var map=L.map(el,{zoomControl:false,attributionControl:!still,dragging:false,touchZoom:false,scrollWheelZoom:false,doubleClickZoom:false,boxZoom:false,keyboard:false});
  var tiles=L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png',{maxZoom:19,attribution:'&copy; OpenStreetMap'}).addTo(map);
  var faded=false; tiles.on('tileload',function(){if(!faded){faded=true;el.classList.add('tiles')}});
  function icon(kind){return L.divIcon({className:'mpin'+(kind==='social'?' social':''),html:'',iconSize:[18,18],iconAnchor:[9,9]});}
  var bounds=[], pool=null;
  pins.forEach(function(p){ if(p.kind==='pool') pool=p; bounds.push([p.lat,p.lng]); });
  if(!pool) pool=pins[0];
  function go(p){ var t=opts.mode==='card'?pool:p; grunionsDirections(t.lat, t.lng); }
  pins.forEach(function(p){
   var m=L.marker([p.lat,p.lng],{icon:icon(p.kind),interactive:!still,title:p.label||'Directions',zIndexOffset:p.kind==='pool'?800:0}).addTo(map);
   if(!still) m.on('click',function(ev){ if(L.DomEvent) L.DomEvent.stopPropagation(ev); go(p); });
  });
  if(opts.mode==='card') map.on('click',function(){ go(pool); });
  function place(){
   if(!el.clientHeight||!pool) return;
   if(opts.mode==='card'||still){
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
    var targetY=(cardTop*5/12)-box.top;
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
 if(doc.body) document.body.className=doc.body.className;
 var main=document.querySelector('main');
 main.replaceChildren.apply(main, [].slice.call(newMain.childNodes));
 grunionsSyncNav(newNav);
 var nextHead=doc.querySelector('header'), curHead=document.querySelector('header');
 if(nextHead&&curHead&&curHead.outerHTML!==nextHead.outerHTML) curHead.replaceWith(nextHead);
 else if(nextHead&&!curHead) document.body.insertBefore(nextHead, document.querySelector('main'));
 document.title=doc.title||document.title;
 if(!pop) history.pushState({grunions:1},'',url);
 grunionsRunScripts(scripts);
 if(window.grunionsBindPickers) grunionsBindPickers();
 if(window.grunionsDropzones) grunionsDropzones();
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
(function(){
 function pad(n){return (n<10?'0':'')+n}
 function todayISO(){ var d=new Date(); return d.getFullYear()+'-'+pad(d.getMonth()+1)+'-'+pad(d.getDate()); }
 function headline(iso){
  if(!iso||iso.length<10) return 'Select date';
  var p=iso.split('-'), dt=new Date(+p[0], +p[1]-1, +p[2]);
  var w=['Sun','Mon','Tue','Wed','Thu','Fri','Sat'][dt.getDay()];
  var mo=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'][dt.getMonth()];
  return w+', '+mo+' '+dt.getDate();
 }
 var months=['January','February','March','April','May','June','July','August','September','October','November','December'];
 var dateDlg, timeDlg, dateSt, timeSt;
 function makeDate(){
  if(dateDlg) return dateDlg;
  dateDlg=document.createElement('dialog');
  dateDlg.className='matpick'; dateDlg.id='grunionsDateDlg'; dateDlg.setAttribute('aria-label','Select date');
  dateDlg.innerHTML='<div class=sheet><div class=matkicker id=matKicker>Select date</div><div class=matheadline id=matHeadline></div><div class=calhead id=matCalHead><select id=matMonth class=matmonth aria-label="Month and year"></select><button type=button class=calmonth id=matPrev aria-label="Previous month"></button><button type=button class=calmonth id=matNext aria-label="Next month"></button></div><div class=yearrow id=matYearRow hidden><button type=button class=calmonth id=yearPrev aria-label="Previous year"></button><button type=button class=yearbtn id=yearBtn aria-label="Choose year">2027</button><button type=button class=calmonth id=yearNext aria-label="Next year"></button></div><div class=yearlist id=yearList hidden role=listbox aria-label=Years></div><div class=calwd id=matWd><span>S</span><span>M</span><span>T</span><span>W</span><span>T</span><span>F</span><span>S</span></div><div class=calgrid id=matGrid></div><div class=monthgrid id=matMonths hidden></div><div class="actseg matpart" id=matPart role=radiogroup aria-label="Part of the month" hidden><label><input type=radio name=mat_part value=all checked><span>All month</span></label><label><input type=radio name=mat_part value=early><span>Early</span></label><label><input type=radio name=mat_part value=mid><span>Mid</span></label><label><input type=radio name=mat_part value=late><span>Late</span></label></div><div class=matactions><button type=button class=mattext id=matDateCancel>Cancel</button><button type=button class=mattext id=matDateOk>OK</button></div></div>';
  document.body.appendChild(dateDlg);
  var prevSvg='<svg width="20" height="20" viewBox="0 0 256 256" fill="currentColor" aria-hidden="true"><path d="M165.66,202.34a8,8,0,0,1-11.32,11.32l-80-80a8,8,0,0,1,0-11.32l80-80a8,8,0,0,1,11.32,11.32L91.31,128Z"/></svg>';
  var nextSvg='<svg width="20" height="20" viewBox="0 0 256 256" fill="currentColor" aria-hidden="true"><path d="M181.66,133.66l-80,80a8,8,0,0,1-11.32-11.32L164.69,128,90.34,53.66a8,8,0,0,1,11.32-11.32l80,80A8,8,0,0,1,181.66,133.66Z"/></svg>';
  dateDlg.querySelector('#matPrev').innerHTML=prevSvg;
  dateDlg.querySelector('#matNext').innerHTML=nextSvg;
  dateDlg.querySelector('#yearPrev').innerHTML=prevSvg;
  dateDlg.querySelector('#yearNext').innerHTML=nextSvg;
  dateDlg.querySelector('#matPrev').onclick=function(){ shiftDate(-1); };
  dateDlg.querySelector('#matNext').onclick=function(){ shiftDate(1); };
  dateDlg.querySelector('#yearPrev').onclick=function(){ shiftYear(-1); };
  dateDlg.querySelector('#yearNext').onclick=function(){ shiftYear(1); };
  dateDlg.querySelector('#yearBtn').onclick=function(){ if(!dateSt) return; dateSt.yearOpen=!dateSt.yearOpen; paintMonth(); };
  dateDlg.querySelector('#yearList').addEventListener('click', function(e){
   var b=e.target.closest&&e.target.closest('button.yearopt'); if(!b||!dateSt) return;
   dateSt.viewYear=+b.getAttribute('data-year'); dateSt.yearOpen=false; paintMonth();
  });
  dateDlg.querySelector('#matMonths').addEventListener('click', function(e){
   var b=e.target.closest&&e.target.closest('button.monthchip'); if(!b||b.disabled||!dateSt) return;
   var ym=dateSt.viewYear+'-'+pad(+b.getAttribute('data-month'));
   dateSt.iso=ym+'-01'; dateSt.ym=ym; paintMonth();
  });
  dateDlg.querySelector('#matMonth').addEventListener('change', function(){ if(!this.value) return; if(dateSt.monthOnly) dateSt.iso=this.value+'-01'; paintDate(this.value); });
  dateDlg.querySelector('#matGrid').addEventListener('click', function(e){
   var b=e.target.closest&&e.target.closest('button.calday'); if(!b||dateSt.monthOnly) return;
   dateSt.iso=b.getAttribute('data-date'); paintDate(dateSt.iso.slice(0,7));
  });
  dateDlg.querySelector('#matPart').addEventListener('change', function(e){
   var r=e.target; if(!r||r.name!=='mat_part'||!dateSt) return;
   dateSt.part=r.value;
   if(dateSt.monthOnly) paintMonth(); else paintDate(dateSt.ym);
  });
  dateDlg.querySelector('#matDateCancel').onclick=function(){ dateDlg.close(); };
  dateDlg.querySelector('#matDateOk').onclick=function(){
   if(dateSt&&dateSt.input){
    dateSt.input.value=dateSt.monthOnly?(dateSt.iso||'').slice(0,7):(dateSt.iso||'');
    if(dateSt.monthOnly&&dateSt.input.form){
     var part=dateSt.input.form.querySelector('[data-monthpart]');
     if(part){ part.value=dateSt.part||'all'; part.dispatchEvent(new Event('input',{bubbles:true})); part.dispatchEvent(new Event('change',{bubbles:true})); }
    }
    dateSt.input.dispatchEvent(new Event('input',{bubbles:true})); dateSt.input.dispatchEvent(new Event('change',{bubbles:true}));
   }
   dateDlg.close();
  };
  dateDlg.addEventListener('click', function(e){ if(e.target===dateDlg) dateDlg.close(); });
  return dateDlg;
 }
 function fillDateMonths(sel, iso){
  var y0=(iso?+iso.slice(0,4):new Date().getFullYear())-5, html='', y, m;
  for(y=y0;y<y0+12;y++) for(m=1;m<=12;m++) html+='<option value="'+y+'-'+pad(m)+'">'+months[m-1]+' '+y+'</option>';
  sel.innerHTML=html;
 }
 function monthHead(ym, part){
  var y=+ym.slice(0,4), m=+ym.slice(5,7), label=months[m-1]+' '+y;
  if(part==='early'||part==='mid'||part==='late') return part.charAt(0).toUpperCase()+part.slice(1)+' '+label;
  return label;
 }
 var shortMonths=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];
 function showMonthChrome(on){
  dateDlg.querySelector('#matCalHead').hidden=!!on;
  dateDlg.querySelector('#matWd').hidden=!!on;
  dateDlg.querySelector('#matGrid').hidden=!!on;
  dateDlg.querySelector('#matYearRow').hidden=!on;
  if(!on){
   dateDlg.querySelector('#yearList').hidden=true;
   dateDlg.querySelector('#matMonths').hidden=true;
   if(dateSt) dateSt.yearOpen=false;
  }
 }
 function yearBounds(){
  var nowY=new Date().getFullYear(), sel=dateSt.iso?+dateSt.iso.slice(0,4):nowY;
  return {min:Math.min(nowY-1, sel), max:Math.max(nowY+15, sel)};
 }
 function paintMonth(){
  showMonthChrome(true);
  var y=dateSt.viewYear, bounds=yearBounds(), open=!!dateSt.yearOpen;
  var yearBtn=dateDlg.querySelector('#yearBtn');
  yearBtn.textContent=String(y);
  yearBtn.className='yearbtn'+(open?' on':'');
  yearBtn.setAttribute('aria-expanded', open?'true':'false');
  dateDlg.querySelector('#yearPrev').disabled=y<=bounds.min;
  dateDlg.querySelector('#yearNext').disabled=y>=bounds.max;
  var partBox=dateDlg.querySelector('#matPart'), kick=dateDlg.querySelector('#matKicker');
  if(partBox) partBox.hidden=open;
  if(kick) kick.textContent='Select month';
  dateDlg.querySelector('#matHeadline').textContent=monthHead((dateSt.iso||'').slice(0,7), dateSt.part);
  var list=dateDlg.querySelector('#yearList'), grid=dateDlg.querySelector('#matMonths');
  list.hidden=!open; grid.hidden=open;
  if(open){
   var html='', yy, onBtn;
   for(yy=bounds.min; yy<=bounds.max; yy++) html+='<button type=button class="yearopt'+(yy===y?' on':'')+'" data-year="'+yy+'">'+yy+'</button>';
   list.innerHTML=html;
   onBtn=list.querySelector('.on');
   if(onBtn) list.scrollTop=Math.max(0, onBtn.offsetTop-list.clientHeight/2);
   return;
  }
  var now=new Date(), ny=now.getFullYear(), nm=now.getMonth()+1;
  var selY=+(dateSt.iso||'').slice(0,4), selM=+(dateSt.iso||'').slice(5,7);
  var cells='', m, past, on;
  for(m=1;m<=12;m++){
   past=y<ny||(y===ny&&m<nm);
   on=y===selY&&m===selM;
   cells+='<button type=button class="monthchip'+(on?' on':'')+'" data-month="'+m+'"'+(past?' disabled':'')+'>'+shortMonths[m-1]+'</button>';
  }
  grid.innerHTML=cells;
 }
 function paintDate(ym){
  if(dateSt.monthOnly){ dateSt.viewYear=+ym.slice(0,4); return paintMonth(); }
  showMonthChrome(false);
  dateSt.ym=ym;
  var y=+ym.slice(0,4), m=+ym.slice(5,7), sel=dateDlg.querySelector('#matMonth');
  if(!sel.querySelector('option[value="'+ym+'"]')) fillDateMonths(sel, ym+'-01');
  sel.value=ym;
  var partBox=dateDlg.querySelector('#matPart'), kick=dateDlg.querySelector('#matKicker');
  if(partBox) partBox.hidden=true;
  if(kick) kick.textContent='Select date';
  dateDlg.querySelector('#matHeadline').textContent=headline(dateSt.iso);
  var blanks=new Date(y, m-1, 1).getDay(), last=new Date(y, m, 0).getDate(), html='', day, iso, today=todayISO();
  for(var i=0;i<blanks;i++) html+='<span class=calday></span>';
  for(day=1;day<=last;day++){
   iso=y+'-'+pad(m)+'-'+pad(day);
   html+='<button type=button class="calday'+(iso===dateSt.iso?' on':'')+(iso===today?' today':'')+'" data-date="'+iso+'">'+day+'</button>';
  }
  dateDlg.querySelector('#matGrid').innerHTML=html;
 }
 function shiftYear(delta){
  if(!dateSt) return;
  var bounds=yearBounds(), y=dateSt.viewYear+delta;
  if(y<bounds.min||y>bounds.max) return;
  dateSt.viewYear=y; dateSt.yearOpen=false; paintMonth();
 }
 function shiftDate(delta){
  var y=+dateSt.ym.slice(0,4), m=+dateSt.ym.slice(5,7)+delta;
  if(m<1){m=12;y--} if(m>12){m=1;y++}
  paintDate(y+'-'+pad(m));
 }
 function makeTime(){
  if(timeDlg) return timeDlg;
  timeDlg=document.createElement('dialog');
  timeDlg.className='matpick'; timeDlg.id='grunionsTimeDlg'; timeDlg.setAttribute('aria-label','Select time');
  timeDlg.innerHTML='<div class=sheet><div class=matkicker>Select time</div><div class=timebig><button type=button id=timeH></button><span>:</span><button type=button id=timeM></button><div class=ampm><button type=button id=timeAM>AM</button><button type=button id=timePM>PM</button></div></div><div class=clock id=timeClock><div class=clockhand id=timeHand></div></div><div class=matactions><button type=button class=mattext id=timeCancel>Cancel</button><button type=button class=mattext id=timeOk>OK</button></div></div>';
  document.body.appendChild(timeDlg);
  timeDlg.querySelector('#timeH').onclick=function(){ timeSt.mode='h'; paintTime(); };
  timeDlg.querySelector('#timeM').onclick=function(){ timeSt.mode='m'; paintTime(); };
  timeDlg.querySelector('#timeAM').onclick=function(){ timeSt.pm=false; paintTime(); };
  timeDlg.querySelector('#timePM').onclick=function(){ timeSt.pm=true; paintTime(); };
  timeDlg.querySelector('#timeCancel').onclick=function(){ if(timeSt&&timeSt.input) timeSt.input.value=timeSt.prev; timeDlg.close(); };
  timeDlg.querySelector('#timeOk').onclick=function(){
   if(timeSt&&timeSt.input){ var h=timeSt.h%12; if(timeSt.pm) h+=12; timeSt.input.value=pad(h)+':'+pad(timeSt.m); timeSt.input.dispatchEvent(new Event('input',{bubbles:true})); timeSt.input.dispatchEvent(new Event('change',{bubbles:true})); }
   timeDlg.close();
  };
  timeDlg.addEventListener('click', function(e){ if(e.target===timeDlg){ if(timeSt&&timeSt.input) timeSt.input.value=timeSt.prev; timeDlg.close(); } });
  return timeDlg;
 }
 function paintTime(){
  var hBtn=timeDlg.querySelector('#timeH'), mBtn=timeDlg.querySelector('#timeM');
  hBtn.textContent=String(timeSt.h); mBtn.textContent=pad(timeSt.m);
  hBtn.className=timeSt.mode==='h'?'on':''; mBtn.className=timeSt.mode==='m'?'on':'';
  timeDlg.querySelector('#timeAM').className=timeSt.pm?'':'on';
  timeDlg.querySelector('#timePM').className=timeSt.pm?'on':'';
  var clock=timeDlg.querySelector('#timeClock'), hand=timeDlg.querySelector('#timeHand');
  var labels=timeSt.mode==='h'?['12','1','2','3','4','5','6','7','8','9','10','11']:['00','05','10','15','20','25','30','35','40','45','50','55'];
  var active=timeSt.mode==='h'?String(timeSt.h):(function(){ var q=Math.round(timeSt.m/5)*5; if(q===60) q=0; return pad(q); })();
  var idx=labels.indexOf(active); if(idx<0) idx=0;
  hand.style.transform='rotate('+(idx*30)+'deg)';
  clock.querySelectorAll('button.clocknum').forEach(function(b){ b.remove(); });
  labels.forEach(function(lab, i){
   var b=document.createElement('button'); b.type='button'; b.className='clocknum'+(lab===active?' on':''); b.textContent=lab;
   var ang=(i/12)*Math.PI*2 - Math.PI/2, r=38;
   b.style.left=(50+r*Math.cos(ang))+'%'; b.style.top=(50+r*Math.sin(ang))+'%';
   b.onclick=function(){
    if(timeSt.mode==='h'){ timeSt.h=+lab||12; timeSt.mode='m'; }
    else timeSt.m=+lab;
    paintTime();
   };
   clock.appendChild(b);
  });
 }
 window.grunionsOpenDate=function(input){
  if(!input) return;
  makeDate();
  var raw=input.value||'';
  var iso=(input.type==='month' && /^\\d{4}-\\d{2}$/.test(raw))?raw+'-01':raw;
  if(!/^\\d{4}-\\d{2}-\\d{2}$/.test(iso)) iso=todayISO();
  var part='all', monthOnly=input.type==='month';
  if(monthOnly && input.form){
   var pel=input.form.querySelector('[data-monthpart]'), pv=pel?(pel.value||'').toLowerCase():'';
   if(pv==='early'||pv==='mid'||pv==='late'||pv==='all') part=pv;
  }
  dateSt={input:input, iso:iso, ym:iso.slice(0,7), monthOnly:monthOnly, part:part, viewYear:+iso.slice(0,4), yearOpen:false};
  dateDlg.querySelectorAll('input[name=mat_part]').forEach(function(r){ r.checked=r.value===part; });
  fillDateMonths(dateDlg.querySelector('#matMonth'), iso);
  paintDate(dateSt.ym);
  if(!dateDlg.open) dateDlg.showModal();
 };
 window.grunionsOpenTime=function(input){
  if(!input) return;
  makeTime();
  var v=input.value||'19:00', p=v.split(':'), hh=+p[0]||0, mm=+p[1]||0;
  var h12=hh%12; if(!h12) h12=12;
  timeSt={input:input, prev:input.value, h:h12, m:mm, pm:hh>=12, mode:'h'};
  paintTime();
  if(!timeDlg.open) timeDlg.showModal();
 };
 window.grunionsBindPickers=function(){
  document.querySelectorAll('input[type=date],input[type=time],input[type=month]').forEach(function(input){
   if(input.dataset.matarm||input.classList.contains('pickhold')) return;
   input.dataset.matarm='1';
   input.addEventListener('pointerdown', function(e){ e.preventDefault(); if(input.type==='time') grunionsOpenTime(input); else grunionsOpenDate(input); });
   input.addEventListener('keydown', function(e){ if(e.key==='Enter'||e.key===' '||e.key==='ArrowDown'){ e.preventDefault(); if(input.type==='time') grunionsOpenTime(input); else grunionsOpenDate(input); } });
  });
 };
 document.addEventListener('click', function(e){
  var b=e.target.closest&&e.target.closest('[data-matfor]'); if(!b) return;
  var input=document.getElementById(b.getAttribute('data-matfor')); if(!input) return;
  e.preventDefault();
  if(input.type==='time') grunionsOpenTime(input); else grunionsOpenDate(input);
 });
 document.addEventListener('click', function(e){
  var d=e.target; if(d&&d.matches&&d.matches('dialog.matpick')&&e.target===d) d.close();
 });
 grunionsBindPickers();
})();

window.grunionsDropzones=function(){
 document.querySelectorAll('[data-dropzone]').forEach(function(zone){
  if(zone.dataset.bound) return; zone.dataset.bound='1';
  var input=zone.querySelector('input[type=file]'), clear=zone.querySelector('[data-clear]');
  var empty=zone.querySelector('.dropempty'), fill=zone.querySelector('.dropfill'), img=zone.querySelector('[data-preview]');
  var had=!!(img && img.getAttribute('src'));
  function show(on){ if(empty) empty.hidden=on; if(fill) fill.hidden=!on; zone.classList.toggle('has', on); }
  function pick(){ if(input) input.click(); }
  var fileMode=zone.getAttribute('data-mode')==='file';
  var nameEl=zone.querySelector('[data-name]'), sizeEl=zone.querySelector('[data-size]');
  function sizeLabel(n){
   if(n<1024) return n+' B';
   if(n<1048576) return (Math.round(n/102.4)/10)+' KB';
   return (Math.round(n/104857.6)/10)+' MB';
  }
  function useFile(f){
   if(!f) return;
   if(!fileMode && f.size>8*1024*1024){ alert('Image is larger than 8 MB.'); return; }
   try{ var dt=new DataTransfer(); dt.items.add(f); input.files=dt.files; }catch(err){}
   if(fileMode){
    if(nameEl) nameEl.textContent=f.name;
    if(sizeEl) sizeEl.textContent=sizeLabel(f.size);
   } else if(img) img.src=URL.createObjectURL(f);
   if(clear) clear.value='';
   show(true);
  }
  if(empty) empty.addEventListener('click', function(e){ e.preventDefault(); pick(); });
  var rep=zone.querySelector('[data-replace]');
  if(rep) rep.addEventListener('click', function(e){ e.preventDefault(); e.stopPropagation(); pick(); });
  var rem=zone.querySelector('[data-remove]');
  if(rem) rem.addEventListener('click', function(e){
   e.preventDefault(); e.stopPropagation();
   if(input) input.value='';
   if(img) img.removeAttribute('src');
   if(nameEl) nameEl.textContent='';
   if(sizeEl) sizeEl.textContent='';
   if(clear) clear.value=had?'1':'';
   show(false);
  });
  if(input) input.addEventListener('change', function(){ var f=input.files&&input.files[0]; if(f) useFile(f); });
  zone.addEventListener('dragenter', function(e){ e.preventDefault(); zone.classList.add('over'); });
  zone.addEventListener('dragover', function(e){ e.preventDefault(); zone.classList.add('over'); });
  zone.addEventListener('dragleave', function(e){ e.preventDefault(); zone.classList.remove('over'); });
  zone.addEventListener('drop', function(e){
   e.preventDefault(); zone.classList.remove('over');
   var f=e.dataTransfer&&e.dataTransfer.files&&e.dataTransfer.files[0];
   if(f) useFile(f);
  });
 });
};
window.grunionsPlaces=function(input){
 if(!input||input.dataset.placebound) return;
 input.dataset.placebound='1';
 input.setAttribute('autocomplete','off');
 input.setAttribute('role','combobox');
 input.setAttribute('aria-autocomplete','list');
 input.setAttribute('aria-expanded','false');
 var wrap=document.createElement('div');
 wrap.className='placefield';
 input.parentNode.insertBefore(wrap, input);
 wrap.appendChild(input);
 var drop=document.createElement('div');
 drop.className='placedrop'; drop.hidden=true; drop.setAttribute('role','listbox');
 wrap.appendChild(drop);
 var label=input.closest('label');
 var badge=label?label.querySelector('.locok'):null;
 var wait, seq=0, items=[], active=-1, open=false;
 var pin='<svg class=pin viewBox="0 0 256 256" fill="currentColor" aria-hidden="true"><path d="M128,64a40,40,0,1,0,40,40A40,40,0,0,0,128,64Zm0,64a24,24,0,1,1,24-24A24,24,0,0,1,128,128Zm0-112a88.1,88.1,0,0,0-88,88c0,31.4,14.51,64.68,42,96.25a254.19,254.19,0,0,0,41.45,38.3,8,8,0,0,0,9.18,0A254.19,254.19,0,0,0,174,200.25c27.45-31.57,42-64.85,42-96.25A88.1,88.1,0,0,0,128,16Zm0,206c-16.53-13-72-60.75-72-118a72,72,0,0,1,144,0C200,161.23,144.53,209,128,222Z"/></svg>';
 function esc(s){ return String(s||'').replace(/[&<>"']/g, function(c){ return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]; }); }
 function setBadge(on){ if(badge) badge.hidden=!on; }
 function close(){ open=false; drop.hidden=true; input.setAttribute('aria-expanded','false'); active=-1; }
 function paint(){
  drop.innerHTML='';
  items.forEach(function(item, i){
   var b=document.createElement('button');
   b.type='button'; b.className='placeopt'+(i===active?' on':''); b.setAttribute('role','option');
   b.setAttribute('aria-selected', i===active?'true':'false');
   if(item.custom) b.innerHTML='<span class=grow><span class=plabel>'+esc(item.label)+'</span></span>';
   else b.innerHTML=pin+'<span class=grow><span class=pname>'+esc(item.name)+'</span>'+(item.detail?'<span class=pdetail>'+esc(item.detail)+'</span>':'')+'</span>';
   b.addEventListener('pointerdown', function(e){ e.preventDefault(); });
   b.addEventListener('click', function(e){ e.preventDefault(); choose(i); });
   drop.appendChild(b);
  });
  var on=items.length>0;
  open=on; drop.hidden=!on; input.setAttribute('aria-expanded', on?'true':'false');
 }
 function choose(i){
  var item=items[i]; if(!item) return;
  input.value=item.name;
  setBadge(!!item.verified);
  input.dispatchEvent(new Event('change',{bubbles:true}));
  close();
 }
 function show(q){
  var mine=++seq;
  fetch('/api/places?q='+encodeURIComponent(q)).then(function(r){ return r.json(); }).then(function(rows){
   if(mine!==seq||input.value.trim()!==q) return;
   items=(rows||[]).map(function(row){ return {name:row.name||'', detail:row.detail||'', verified:row.verified!==false, custom:false}; }).filter(function(row){ return row.name; });
   var typed=q;
   items.push({name:typed, detail:'', verified:false, custom:true, label:'Use “'+typed+'”'});
   active=items.length?0:-1;
   paint();
  }).catch(function(){});
 }
 input.addEventListener('input', function(){
  setBadge(false);
  clearTimeout(wait);
  var q=input.value.trim();
  if(q.length<2){ seq++; items=[]; close(); return; }
  wait=setTimeout(function(){ show(q); }, 250);
 });
 input.addEventListener('keydown', function(e){
  if(drop.hidden) return;
  if(e.key==='ArrowDown'){ e.preventDefault(); active=active<0?0:Math.min(items.length-1, active+1); paint(); }
  else if(e.key==='ArrowUp'){ e.preventDefault(); active=Math.max(0, active-1); paint(); }
  else if(e.key==='Enter'){ e.preventDefault(); if(active<0) active=0; choose(active); }
  else if(e.key==='Escape'){ e.preventDefault(); close(); }
 });
 if(input.form) input.form.addEventListener('submit', function(e){ if(!drop.hidden) e.preventDefault(); });
 input.addEventListener('blur', function(){ setTimeout(close, 180); });
 document.addEventListener('keydown', function(e){ if(e.key==='Escape'&&open) close(); });
};
function grunionsBindPlaces(){
 document.querySelectorAll('[data-places]').forEach(function(input){ if(window.grunionsPlaces) grunionsPlaces(input); });
}
document.addEventListener('focusin', function(e){
 var input=e.target; if(input&&input.matches&&input.matches('[data-places]')) grunionsPlaces(input);
});
document.addEventListener('DOMContentLoaded', function(){
 if(window.grunionsDropzones) grunionsDropzones();
 grunionsBindPlaces();
});
grunionsPinHead();
window.addEventListener('resize', grunionsPinHead);
</script>
<script>var PUSH_CSRF="{{csrf_token()}}",VAPID_PUBLIC="{{vapid_public_key()}}";</script>
</body></html>""")

ADMIN_NAV = """{% for n in admin_notices() %}<div class=note>{{n.body}}</div>{% endfor %}"""

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
{{ rsvp_btn('Going', nextev.mine == 'going', 'going') }}
{{ rsvp_btn('Not going', nextev.mine == 'notgoing', 'notgoing') }}</form>
</div>{% elif nextp %}{% set sh = social_home(nextp) %}<div class="card tap nextcard" onclick="if(event.target.closest('button,a,form,input,select,textarea,label'))return;location.href='/practices/{{nextp.id}}'">
{% if nextp.image %}<a class=cardlink href="/practices/{{nextp.id}}"><div class=pimg><img src="/practice-image/{{ nextp.id }}?v={{ nextp.image }}" alt=""><span class="chip-info nxbadge">{% if nextp.date == today %}TODAY{% else %}{{ fmt_d(nextp.date) }}{% endif %}</span></div></a>{% endif %}
<div class=nxbody><div class=nxcardhead><a class=cardlink href="/practices/{{nextp.id}}"><div class=nxtitle>{{ practice_title(nextp) }}</div></a><span class="chip-info daychip">{{ practice_chip(nextp) }}</span></div>
<a class=cardlink href="/practices/{{nextp.id}}">
<div class=nxrow>{{ glyph_clock() }}<span>{% if practice_is_month(nextp) %}{{ practice_when(nextp) }}{% else %}{{ fmt_card_date(nextp.date) }} · {{ fmt_clock(nextp.start) }} – {{ fmt_clock(nextp.end) }}{% endif %}</span></div>
<div class=nxrow>{{ glyph_pin() }}<span>{{ short_place(nextp.location) }}</span></div>
<div class=nxrow>{{ glyph_people() }}<span>{{ nextp_n }} going{% if next_coaches %} · Coaches: {{ next_coaches }}{% endif %}</span></div>
{% if practice_sports_line(nextp) %}<div class="t3 sm sportline">{{ practice_sports_line(nextp) }}</div>{% endif %}
{% if nextp.coach_note %}<div class=nxnote>{{ nextp.coach_note }} · {{ nextp.coach_note_by }} · {{ fmt_stamp(nextp.coach_note_at) }}</div>{% endif %}</a></div>
<form method=post action=/practices class=pills>{{csrf_field()}}<input type=hidden name=pid value={{nextp.id}}>
{{ rsvp_btn('Going', nextp_mine==1, 'going') }}
{{ rsvp_btn('Not going', nextp_mine==0, 'notgoing') }}</form>
{% if sh %}<div class=nxdiv></div><div class=nxsocial><a class=cardlink href="/practices/{{nextp.id}}" style="display:flex;align-items:center;gap:12px">{{ social_icon() }}
<div class=grow><div class=nxtitle>{{ sh.title }}</div><div class="t2 sm">{{ sh.place }}</div></div></a>
<form method=post action=/practices>{{csrf_field()}}<input type=hidden name=pid value={{nextp.id}}>
<button class="btn {{ 'btn-primary' if next_joined else 'btn-secondary' }}" name=action value="{{ 'social_leave' if next_joined else 'social_join' }}">{% if next_joined %}Joined ✓{% else %}Join{% endif %}</button></form></div>{% endif %}
</div>{% endif %}
</div>
<div class=schedlist id=schedule>
{% for x in data %}{% set p = x.p %}<div class="card tap{% if nextp and p.id == nextp.id %} schedsame{% endif %}" id=p{{p.id}} data-pid={{p.id}} {% if p.cancelled %}style="opacity:.55"{% endif %} onclick="if(event.target.closest('button,a,form,input,select,textarea,label,dialog'))return;location.href='/practices/{{p.id}}'">
<a class=cardlink href="/practices/{{p.id}}">
<div class=nxcardhead><div class=nxtitle>{{ practice_title(p) }}</div></div>
{% set tile = practice_tile(p) %}
<div class=nxmain><div class=datetile><span class=pdate>{% if x.unseen %}<span class=badge data-seen={{p.id}}>{{ x.unseen if x.unseen < 100 else '99+' }}</span>{% endif %}</span><span class=wd>{{ tile.wd }}</span><span class=dn>{{ tile.dn }}</span><span class=mo>{{ tile.mo }}</span></div>
<div class="grow schedrows"><div class=nxrow>{{ glyph_clock() }}<span>{% if practice_is_month(p) %}{{ practice_when(p) }}{% else %}{{ fmt_span(p.start, p.end) }}{% endif %}</span></div>
<div class=nxrow>{{ glyph_pin() }}<span>{{ p.location }}</span></div>
<div class=nxrow>{{ glyph_people() }}<span>{{ x.going|length }} going{% if x.coach_names %} · Coaches: {{ x.coach_names|join(', ') }}{% endif %}</span></div>
{% if practice_sports_line(p) %}<div class="t3 sm sportline">{{ practice_sports_line(p) }}</div>{% endif %}</div></div>
{% if p.cancelled %}{{ st('bad','Cancelled') }}{% if p.cancel_reason %}<div class="t3 sm">{{ p.cancel_reason }}</div>{% endif %}{% endif %}
{% if p.note %}<div class=nxnote>{{p.note}}</div>{% endif %}
{% if p.coach_note %}<div class=nxnote>{{ p.coach_note }} · {{ p.coach_note_by }} · {{ fmt_stamp(p.coach_note_at) }}</div>{% endif %}</a>
{% if not p.cancelled %}<form method=post action=/practices class=pills>{{csrf_field()}}<input type=hidden name=pid value={{p.id}}>
{{ rsvp_btn('Going', x.mine == 1, 'going') }}
{{ rsvp_btn('Not going', x.mine == 0, 'notgoing') }}</form>
{% endif %}</div>{% endfor %}
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
  var alertsEl=document.querySelector('.homealerts');
  document.documentElement.style.setProperty('--homealerts', ((alertsEl&&alertsEl.offsetHeight)||0)+'px');
  if(!card||!dock) return;
  var nav=document.querySelector('nav.tabs');
  var gap=24;
  var root=getComputedStyle(document.documentElement);
  var offset=parseFloat(root.getPropertyValue('--nav-offset-bottom'))||24;
  var navH=nav?nav.getBoundingClientRect().height:((parseFloat(root.getPropertyValue('--nav-circle'))||52)+(parseFloat(root.getPropertyValue('--nav-pad'))||8)*2+2);
  var safe=0;
  if(nav) safe=Math.max(0, window.innerHeight-nav.getBoundingClientRect().bottom-offset);
  else { var probe=document.createElement('div'); probe.style.cssText='position:fixed;left:0;bottom:0;width:0;height:0;padding-bottom:env(safe-area-inset-bottom);pointer-events:none;visibility:hidden'; document.body.appendChild(probe); safe=probe.offsetHeight; probe.remove(); }
  var navTop=window.innerHeight-safe-offset-navH;
  document.documentElement.style.setProperty('--peek', gap+'px');
  var top=card.getBoundingClientRect().top+window.scrollY;
  var delta=(navTop-gap)-top;
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

_CAM = '<svg width="16" height="16" viewBox="0 0 256 256" fill="currentColor" aria-hidden="true"><path d="M208,56H180.28L166.65,35.56A8,8,0,0,0,160,32H96a8,8,0,0,0-6.65,3.56L75.71,56H48A24,24,0,0,0,24,80V192a24,24,0,0,0,24,24H208a24,24,0,0,0,24-24V80A24,24,0,0,0,208,56Zm8,136a8,8,0,0,1-8,8H48a8,8,0,0,1-8-8V80a8,8,0,0,1,8-8H80a8,8,0,0,0,6.66-3.56L100.28,48h55.43l13.63,20.44A8,8,0,0,0,176,72h32a8,8,0,0,1,8,8ZM128,88a44,44,0,1,0,44,44A44.05,44.05,0,0,0,128,88Zm0,72a28,28,0,1,1,28-28A28,28,0,0,1,128,160Z"/></svg>'
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
<nav class="filt profswitch chiprow" aria-label="Profile"><a class="chip{{ ' chip-active on' if ptab == 'general' }}" href="/profile?tab=general">General</a><a class="chip{{ ' chip-active on' if ptab == 'lineup' }}" href="/profile?tab=lineup">My Lineup</a>{% if hosts %}<a class="chip{{ ' chip-active on' if ptab == 'hosting' }}" href="/profile?tab=hosting">Hosting</a>{% endif %}</nav>
</div>
</form>
{% if ptab == 'general' %}
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
{% else %}
{% if prof_upcoming or prof_past %}
{% for g in prof_upcoming %}<h2 class=lineupmonth>{{ g.label }}</h2>{% for e in g.events %}{{ lineup_card(e, prof_back) }}{% endfor %}{% endfor %}
{% if prof_past %}<details class=lineuppast><summary>Past <span class=t3>{{ prof_past_n }}</span></summary>{% for g in prof_past %}<h2 class=lineupmonth>{{ g.label }}</h2>{% for e in g.events %}{{ lineup_card(e, prof_back) }}{% endfor %}{% endfor %}</details>{% endif %}
{% else %}<p class=emptyfind>Nothing yet.</p>{% endif %}
{% endif %}
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
  if(pref) pref.value=pref.getAttribute('data-original')||'';
  if(phone) phone.value=phone.getAttribute('data-original')||'';
  if(usawp) usawp.value=usawp.getAttribute('data-original')||'';
  if(hadPhoto&&originalSrc) showPhoto(originalSrc); else showLetters();
  if(hadPhoto) removeBtn.hidden=false;
 }
 document.getElementById('profileEdit').onclick=function(){ if(/tab=(interested|mine)/.test(location.search)){ location.href='/profile?tab=general&edit=1'; return; } enter(); };
 if(/[?&]edit=1/.test(location.search)) enter();
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

T["chat"] = """<div class=chat id=chat></div><div class=chatpad></div>
<div class="composer noprint"><div class=qbar id=quoteBar hidden><div class=grow><b id=quoteWho></b><span id=quoteTxt></span></div><button type=button id=quoteX aria-label="Cancel reply">✕</button></div><div class=qbar id=editBar hidden><div class=grow><b>Editing</b><span id=editHint></span></div><button type=button id=editX aria-label="Cancel edit">✕</button></div><div class=preview id=prev hidden><img id=prevImg alt=""><span id=prevName></span><button type=button class="quiet compact" id=prevX>Remove</button></div>
<form id=f><input type=file id=file accept="image/jpeg,image/png,image/gif,image/webp,image/heic,image/heif,.heic" hidden>
<button type=button class="iconbtn" id=attach title="Attach image" aria-label="Attach image"><svg width="24" height="24" viewBox="0 0 256 256" fill="currentColor" aria-hidden="true"><path d="M216,40H40A16,16,0,0,0,24,56V200a16,16,0,0,0,16,16H216a16,16,0,0,0,16-16V56A16,16,0,0,0,216,40Zm0,16V158.75l-26.07-26.06a16,16,0,0,0-22.63,0l-20,20-44-44a16,16,0,0,0-22.62,0L40,149.37V56ZM40,172l52-52,80,80H40Zm176,28H194.63l-36-36,20-20L216,181.38V200ZM144,100a12,12,0,1,1,12,12A12,12,0,0,1,144,100Z"/></svg></button>
<textarea id=body rows=1 maxlength=2000 placeholder="Message {{'coaches' if ch=='coaches' else 'the team'}}"></textarea>
<button class="iconbtn send" type=submit aria-label=Send><svg width="24" height="24" viewBox="0 0 256 256" fill="currentColor" aria-hidden="true"><path d="M230.14,25.86a20,20,0,0,0-19.57-5.11l-.22.07L18.44,79a20,20,0,0,0-3.06,37.25L99,157l40.71,83.65a19.81,19.81,0,0,0,18,11.38c.57,0,1.15,0,1.73-.07A19.82,19.82,0,0,0,177,237.56L235.18,45.65a1.42,1.42,0,0,0,.07-.22A20,20,0,0,0,230.14,25.86ZM156.91,221.07l-34.37-70.64,46-45.95a12,12,0,0,0-17-17l-46,46L34.93,99.09,210,46Z"/></svg></button></form></div>
<dialog id=actSheet class=botsheet><div class=sheet>
<div class=grab aria-hidden=true></div>
<div class=emogrid id=actEmoji>{% for e in REACTIONS %}<button type=button data-e="{{e}}">{{e}}</button>{% endfor %}<button type=button data-more=1 aria-label="More emoji">+</button></div>
<div class=emopick id=emojiMore hidden></div>
<p id=actConfirm hidden>Delete this message?</p>
<div class=actgroup><button type=button class=actrow id=actReply><svg width="20" height="20" viewBox="0 0 256 256" fill="currentColor" aria-hidden="true"><path d="M232,200a8,8,0,0,1-16,0,88.1,88.1,0,0,0-88-88H51.31l34.35,34.34a8,8,0,0,1-11.32,11.32l-48-48a8,8,0,0,1,0-11.32l48-48A8,8,0,0,1,85.66,61.66L51.31,96H128A104.11,104.11,0,0,1,232,200Z"/></svg>Reply</button></div>
<div class=actgroup id=actCopyGroup><button type=button class=actrow id=actCopy><svg width="20" height="20" viewBox="0 0 256 256" fill="currentColor" aria-hidden="true"><path d="M216,32H88a8,8,0,0,0-8,8V80H40a8,8,0,0,0-8,8V216a8,8,0,0,0,8,8H168a8,8,0,0,0,8-8V176h40a8,8,0,0,0,8-8V40A8,8,0,0,0,216,32ZM160,208H48V96H160Zm48-48H176V88a8,8,0,0,0-8-8H96V48H208Z"/></svg>Copy</button></div>
<div class=actgroup id=actOwn><button type=button class=actrow id=actEdit><svg width="20" height="20" viewBox="0 0 256 256" fill="currentColor" aria-hidden="true"><path d="M227.31,73.37,182.63,28.68a16,16,0,0,0-22.63,0L36.69,152A15.86,15.86,0,0,0,32,163.31V208a16,16,0,0,0,16,16H92.69A15.86,15.86,0,0,0,104,219.31L227.31,96a16,16,0,0,0,0-22.63ZM92.69,208H48V163.31l88-88L180.69,120ZM192,108.68,147.31,64l24-24L216,84.68Z"/></svg>Edit</button><button type=button class="actrow danger" id=actDelete><svg width="20" height="20" viewBox="0 0 256 256" fill="currentColor" aria-hidden="true"><path d="M216,48H180V36A28,28,0,0,0,152,8H104A28,28,0,0,0,76,36V48H40a12,12,0,0,0,0,24h4V208a20,20,0,0,0,20,20H192a20,20,0,0,0,20-20V72h4a12,12,0,0,0,0-24ZM100,36a4,4,0,0,1,4-4h48a4,4,0,0,1,4,4V48H100Zm88,168H68V72H188ZM116,104v64a12,12,0,0,1-24,0V104a12,12,0,0,1,24,0Zm48,0v64a12,12,0,0,1-24,0V104a12,12,0,0,1,24,0Z"/></svg><span id=actDeleteLabel>Delete</span></button></div>
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
 d.innerHTML=(m.deleted?'':`<button type=button class=more data-act=${m.id} aria-label="Message actions"><svg width="20" height="20" viewBox="0 0 256 256" fill="currentColor" aria-hidden="true"><path d="M140,128a12,12,0,1,1-12-12A12,12,0,0,1,140,128Zm56-12a12,12,0,1,0,12,12A12,12,0,0,0,196,116ZM60,116a12,12,0,1,0,12,12A12,12,0,0,0,60,116Z"/></svg></button>`)+
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
function syncComposer(){var c=document.querySelector('.composer');if(c)document.documentElement.style.setProperty('--composer-h',c.offsetHeight+'px')}
function grow(){ta.style.height='auto';ta.style.height=Math.min(ta.scrollHeight,136)+'px';syncComposer()}ta.addEventListener('input',grow);grow();if(window.ResizeObserver){var comp=document.querySelector('.composer');if(comp)new ResizeObserver(syncComposer).observe(comp)}
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

T["lineup"] = """{% macro lineup_months(groups) %}{% for g in groups %}<h2 class=lineupmonth>{{ g.label }}</h2>{% for e in g.events %}{{ lineup_card(e) }}{% endfor %}{% endfor %}{% endmacro %}
<div class="filt lineupfilt chiprow" role=group aria-label="Type"><a class="chip{{ ' chip-active on' if not group }}" href=/lineup>All</a>{% for slug, label in filter_groups %}<a class="chip{{ ' chip-active on' if group == slug }}" href="/lineup?group={{ slug }}">{{ label }}</a>{% endfor %}</div>
{% if featured %}<h2 class=lineupmonth>Pinned</h2>{% for e in featured %}{{ lineup_card(e) }}{% endfor %}{% endif %}
{% if empty_public %}<p class=emptyfind>Nothing on the Lineup yet.</p>{% endif %}
{{ lineup_months(upcoming) }}
{% if past %}<details class=lineuppast><summary>Past <span class=t3>{{ past_n }}</span></summary>{{ lineup_months(past) }}</details>{% endif %}"""
T["lineup_event"] = """{{ event_hero('lineHero', e.pins, ('/lineup-image/' ~ e.id ~ '?v=' ~ e.banner) if e.banner else '', e.where or e.title) }}
<div class=profilehero>
<div class=profilename>{{ e.title }}</div>
{% if e.when %}<p class=pracemeta>{{ e.when }}</p>{% endif %}
{% if e.venue %}<p class=pracemeta>{{ e.venue }}</p>{% endif %}
{% if e.city %}<p class=pracemeta>{{ e.city }}</p>{% endif %}
{% if e.tag %}<p class="pracemeta eventtag">{{ e.tag }}</p>{% endif %}
<div class=pracestatus>{{ st(e.status_kind, e.status_text) }}</div>
<div class="stats trio">
<div class=stattile><b>{{ e.going_n }}</b><span>Going</span></div>
<div class=stattile><b>{{ e.interested_n }}</b><span>Interested</span></div>
{% if e.capacity %}<div class=stattile><b>{{ e.capacity }}</b><span>Spots</span></div>{% else %}<div class=stattile><b>{{ e.days }}</b><span>Days</span></div>{% endif %}
</div>
</div>
{% if e.status == 'published' %}<form method=post action="/lineup/{{ e.id }}" class="pills rsvprow">{{ csrf_field() }}
{% set going_label = 'Join waitlist' if e.full and e.mine != 'going' and e.mine != 'waitlist' else ('Waitlist' if e.mine == 'waitlist' else 'Going') %}
{{ rsvp_btn('Interested', e.mine == 'interested', 'interested') }}
{{ rsvp_btn(going_label, e.mine == 'going' or e.mine == 'waitlist', 'going') }}
{{ rsvp_btn('Not going', e.mine == 'notgoing', 'notgoing') }}</form>{% endif %}
<div class=seclabel>Details</div>
<div class=list>
{% if e.description %}<div class="li evdescrow"><div class=clamp id=evdesc>{{ e.description }}</div><button type=button class=textlink id=evmore hidden>More</button></div>{% endif %}
{% if e.host_org %}<div class="li prow"><span class=k>Host organization</span><span class=v>{{ e.host_org }}</span></div>{% endif %}
{% if e.link %}<div class="li prow"><span class=k>Registration</span><span class=v><a class=reglink href="{{ e.link }}" target=_blank rel="noopener noreferrer">Registration</a></span></div>{% endif %}
{% if e.event_type %}<div class="li prow"><span class=k>Type</span><span class=v>{{ e.event_type }}</span></div>{% endif %}
{% if e.sports_line %}<div class="li prow"><span class=k>Session</span><span class=v>{{ e.sports_line }}</span></div>{% endif %}
{% if e.details %}<div class=li>{{ e.details }}</div>{% endif %}
{% if e.cost %}<div class="li prow"><span class=k>Cost</span><span class=v>About {{ e.cost }}</span></div>{% endif %}
{% if e.capacity %}<div class="li prow"><span class=k>Spots</span><span class=v>{{ e.going_n }} of {{ e.capacity }}{% if e.wait_n %} · {{ e.wait_n }} waitlisted{% endif %}</span></div>{% endif %}
{% if e.reg_deadline %}<div class="li prow"><span class=k>Register by</span><span class=v>{{ e.reg_deadline }}</span></div>{% endif %}
</div>
{% if e.levels_raw %}<details class=card><summary>Skill levels</summary>{% for row in SPORTS.LEVELS %}{% if row[0] in e.levels_raw.split(',') %}<p><b>{{ row[1] }}</b> {{ row[2] }}</p>{% endif %}{% endfor %}</details>{% endif %}
{% if e.review_note and e.status in ('changes_requested', 'declined') %}<div class=note>{{ e.review_note }}</div>{% endif %}
{{ whos_going(e.people) }}
{% if e.can_review and e.intent == 'considering' %}<form method=post action="/lineup/{{ e.id }}" style="margin-top:10px">{{ csrf_field() }}<button class="btn btn-primary full" name=action value=official>Make official</button></form>{% endif %}
{% if e.venue or e.city %}{{ event_location('lineLoc', e.pins, e.venue or e.city, e.city if e.venue else '', e.dir_href) }}{% endif %}
<script>(function(){var el=document.getElementById('evdesc'),btn=document.getElementById('evmore');if(!el||!btn)return;if(el.scrollHeight>el.clientHeight+2)btn.hidden=false;btn.onclick=function(){var open=el.classList.toggle('open');btn.textContent=open?'Less':'More';};})();</script>"""
T["approvals"] = """{% call admin_page('Events') %}<a class="btn quiet pageact" href="/events/new">Create event</a>{% endcall %}
{% if queue %}<h2>Needs review ({{ queue|length }})</h2>
{% for e in queue %}<div class=card>
<div class=nxtitle>{{ e.title }}</div>
<div class="t3 sm">{{ e.status_text or e.status_label }}{% if e.tag %} · {{ e.tag }}{% endif %}</div>
<div class=nxrow>{{ glyph_clock() }}<span>{{ e.when }}</span></div>
{% if e.where %}<div class=nxrow>{{ glyph_pin() }}<span>{{ e.where }}</span></div>{% endif %}
{% if e.description %}<div class=evnote>{{ e.description }}</div>{% endif %}
{% if e.review_note %}<div class=note>{{ e.review_note }}</div>{% endif %}
<form method=post action=/admin/approvals style="margin-top:12px">{{ csrf_field() }}<input type=hidden name=event_id value={{ e.id }}>
<button class="btn btn-primary full" name=action value=approve>Approve &amp; Publish</button>
<label style="margin-top:12px">Note<textarea name=note rows=2 placeholder="Needed for changes or a decline"></textarea></label>
<div class=row><button class="btn btn-secondary" name=action value=changes>Request Changes</button><button class="btn btn-danger" name=action value=decline>Decline</button></div>
</form></div>{% endfor %}{% endif %}
{% for g in groups %}<h2>{{ g.label }}</h2><div class=list>{% for item in g['items'] %}<a class=li href="{{ item.href }}" style="color:inherit;text-decoration:none"><span class=grow><span class=ell style="display:block;font-weight:650">{{ item.title }}</span><span class="t3 sm">{{ item.when }}{% if item.place %} · {{ item.place }}{% endif %}</span></span></a>{% endfor %}</div>{% endfor %}
{% if not groups and not queue %}<p class=emptyfind>Nothing coming up.</p>{% endif %}"""
T["manage"] = ADMIN_NAV + """<p class=pagesub>Everything you need to run your club.</p>
<div class=mgroups>
{% for g in groups %}<section class=mgroup><h2>{{ g.label }}</h2><div class=mlist>{% for row in g.rows %}{{ manage_row(row.href, row.title, row.desc, row.icon, row.count, row.tone) }}{% endfor %}</div></section>{% endfor %}
</div>
<script>(function(){var key='grunionsManageScroll';var y=0;try{y=+sessionStorage.getItem(key)||0}catch(e){}if(y)requestAnimationFrame(function(){scrollTo(0,y)});document.querySelectorAll('a.mrow').forEach(function(a){a.addEventListener('click',function(){try{sessionStorage.setItem(key,String(scrollY))}catch(e){}})});})();</script>"""
T["manage_schedule"] = ADMIN_NAV + """{% call admin_page('Schedule', 'Practices, scrimmages, and games.') %}<a class="btn quiet pageact" href="/events/new?lane=schedule">Create</a>{% endcall %}
{% if coming %}<div class=list>{% for item in coming %}<a class=li href="{{ item.href }}" style="color:inherit;text-decoration:none"><span class=grow><span class=ell style="display:block;font-weight:600">{{ item.title }}</span><span class="t3 sm">{{ item.when }}{% if item.place %} · {{ item.place }}{% endif %}</span></span></a>{% endfor %}</div>{% else %}<p class=emptyfind>Nothing coming up.</p>{% endif %}"""
T["manage_lineup"] = ADMIN_NAV + """{% call admin_page('Lineup', 'Events, tournaments, and socials.') %}<a class="btn quiet pageact" href="/events/new?lane=lineup">Create</a>{% endcall %}
{% if coming %}<div class=list>{% for item in coming %}<a class=li href="{{ item.href }}" style="color:inherit;text-decoration:none"><span class=grow><span class=ell style="display:block;font-weight:600">{{ item.title }}</span><span class="t3 sm">{{ item.when }}{% if item.place %} · {{ item.place }}{% endif %}</span></span></a>{% endfor %}</div>{% else %}<p class=emptyfind>Nothing coming up.</p>{% endif %}"""
T["manage_requests"] = ADMIN_NAV + """{{ admin_page('Requests', 'Member-submitted events.') }}
<div class="filt chiprow" role=group aria-label="Status"><a class="chip{{ ' chip-active on' if view=='pending' }}" href="/manage/requests?view=pending">Pending</a><a class="chip{{ ' chip-active on' if view=='approved' }}" href="/manage/requests?view=approved">Approved</a><a class="chip{{ ' chip-active on' if view=='declined' }}" href="/manage/requests?view=declined">Declined</a></div>
{% if rows %}<div class=list>{% for e in rows %}<a class=li href="/manage/requests/{{ e.id }}" style="color:inherit;text-decoration:none"><span class=grow><span class=ell style="display:block;font-weight:600">{{ e.title }}</span><span class="t3 sm ell" style="display:block">{{ e.category }}{% if e.submitter %} · {{ e.submitter }}{% endif %}{% if e.when %} · {{ e.when }}{% endif %}</span></span><span class="st st-{{ e.status_kind }}">{{ e.status_text }}</span></a>{% endfor %}</div>{% else %}<p class=emptyfind>Nothing here.</p>{% endif %}"""
T["manage_request"] = ADMIN_NAV + """{{ admin_page(e.title) }}
<p class="t2 sm" style="margin-top:0">{{ e.category }}{% if e.submitter %} · {{ e.submitter }}{% endif %}{% if e.when %} · {{ e.when }}{% endif %}</p>
<p>{{ st(e.status_kind, e.status_text) }}</p>
{% if e.description %}<p>{{ e.description }}</p>{% endif %}
{% if e.review_note %}<div class=note>{{ e.review_note }}</div>{% endif %}
{% if e.status in ('pending', 'changes_requested') %}<form method=post action=/admin/approvals>{{ csrf_field() }}<input type=hidden name=event_id value={{ e.id }}>
<button class="btn btn-primary full" name=action value=approve>Approve &amp; Publish</button>
<label style="margin-top:12px">Note<textarea name=note rows=2 placeholder="Needed for changes or a decline"></textarea></label>
<div class=row><button class="btn btn-secondary" name=action value=changes>Request Changes</button><button class="btn btn-danger" name=action value=decline>Decline</button></div>
</form>{% elif e.status == 'published' %}<p style="margin-top:16px"><a class="btn btn-secondary" href="/lineup/{{ e.id }}">View on Lineup</a></p>{% endif %}"""
_CHEV = '<svg width="20" height="20" viewBox="0 0 256 256" fill="currentColor" aria-hidden="true"><path d="M181.66,133.66l-80,80a8,8,0,0,1-11.32-11.32L164.69,128,90.34,53.66a8,8,0,0,1,11.32-11.32l80,80A8,8,0,0,1,181.66,133.66Z"/></svg>'
T["event_new"] = """<form id=planForm method=post action=/events/new enctype=multipart/form-data>{{ csrf_field() }}
<input type=hidden name=lane id=laneVal value="{{ 'lineup' if not staff else lane }}">
<input type=hidden name=title_mode id=titleMode value=auto>
<input type=hidden name=mode value="{{ 'create' if staff else 'suggest' }}">
{% if staff %}<h2 class=planask>What are you planning?</h2>
<div class=lanepick role=radiogroup aria-label="What are you planning?">
<button type=button class="lanecard{{ ' on' if lane != 'lineup' }}" data-lane=schedule><b>Team schedule</b><span>Practices, scrimmages &amp; games</span></button>
<button type=button class="lanecard{{ ' on' if lane == 'lineup' }}" data-lane=lineup><b>Lineup event</b><span>Tournaments, trips, socials &amp; more</span></button>
</div>{% endif %}
{% if staff %}<div id=schedBlock {% if lane == 'lineup' %}hidden{% endif %}>
<div class=actseg role=radiogroup aria-label="Session type">
<label><input type=radio name=activity_type value=practice {% if activity != 'scrimmage' and activity != 'game' %}checked{% endif %}><span>Practice</span></label>
<label><input type=radio name=activity_type value=scrimmage {% if activity == 'scrimmage' %}checked{% endif %}><span>Scrimmage</span></label>
<label><input type=radio name=activity_type value=game {% if activity == 'game' %}checked{% endif %}><span>Game</span></label>
</div>
<label>Sport<select name=sport id=sportSel><option>Water Polo</option><option>Swimming</option></select></label>
<div class=livetitle><strong id=liveTitle>Water Polo Practice</strong><button type=button class="btn quiet" id=customize>Customize</button></div>
<label id=titleField hidden>Event name<input name=title id=titleInput autocomplete=off><button type=button class="btn quiet" id=titleReset>Reset to automatic</button></label>
</div>{% endif %}
<div id=lineBlock {% if staff and lane != 'lineup' %}hidden{% endif %}>
<label>Type<select name=event_type id=lineType>{% for name, label in line_types %}<option value="{{ name }}">{{ label }}</option>{% endfor %}</select></label>
<label>Event name<input name=line_title id=lineTitle autocomplete=off placeholder="IGLA 2027"></label>
<label>Short description<textarea name=description id=lineDesc rows=3 placeholder="What should people know?"></textarea></label>
</div>
<div class=seclabel>When</div>
{% if staff %}<div class=actseg id=whenPrec role=radiogroup aria-label=Dates>
<label><input type=radio name=date_precision value=exact checked><span>Exact dates</span></label>
<label><input type=radio name=date_precision value=month><span>Month only</span></label>
</div>{% endif %}
<div class=list id=exactWhen>
<button type=button class="li setrow" data-matfor=dateInput><span class=grow>Date<span class="sum" id=dateSum> Add a date</span></span>""" + _CHEV + """</button>
<button type=button class="li setrow" data-matfor=startInput><span class=grow>Start<span class="sum" id=startSum> 7:00 PM</span></span>""" + _CHEV + """</button>
<button type=button class="li setrow" data-matfor=endInput><span class=grow>End<span class="sum" id=endSum> 8:30 PM</span></span>""" + _CHEV + """</button>
</div>
<div class=list id=monthWhen hidden>
<button type=button class="li setrow" data-matfor=monthInput><span class=grow>Month<span class=sum id=monthSum> Choose a month</span></span>""" + _CHEV + """</button>
<input type=hidden name=date_part id=datePart data-monthpart value=all>
</div>
<label>Location<span id=locOk class=locok hidden><svg width="16" height="16" viewBox="0 0 256 256" fill="currentColor" aria-hidden="true"><path d="M128,24A104,104,0,1,0,232,128,104.11,104.11,0,0,0,128,24Zm45.66,85.66-56,56a8,8,0,0,1-11.32,0l-24-24a8,8,0,0,1,11.32-11.32L112,148.69l50.34-50.35a8,8,0,0,1,11.32,11.32Z"/></svg> Verified</span><input name=location id=locInput data-places autocomplete=off placeholder="Pool or address"></label>
<div class=seclabel>Additional settings</div>
{% if staff %}<div class=list id=schedSets {% if lane == 'lineup' %}hidden{% endif %}>
<button type=button class="li setrow" data-open=setLevels><span class=grow>Skill levels &amp; division<span class=sum id=lvlSum> Not set</span></span>""" + _CHEV + """</button>
<button type=button class="li setrow" data-open=setCoaches><span class=grow>Coaches<span class=sum id=coachSum> None</span></span>""" + _CHEV + """</button>
<button type=button class="li setrow" data-open=setSocial><span class=grow>After-session social<span class=sum id=socSum> None</span></span>""" + _CHEV + """</button>
<button type=button class="li setrow" data-open=setNotes><span class=grow>Notes &amp; media<span class=sum id=noteSum> None</span></span>""" + _CHEV + """</button>
</div>{% endif %}
<div class=list id=lineSets {% if staff and lane != 'lineup' %}hidden{% endif %}>
{% if staff %}<button type=button class="li setrow" id=planRow data-open=setPlan><span class=grow>Team plan<span class=sum id=planSum> Considering</span></span>""" + _CHEV + """</button>{% endif %}
<button type=button class="li setrow" id=partRow data-open=setHost><span class=grow>Participation<span class=sum id=partSum> Attending</span></span>""" + _CHEV + """</button>
<button type=button class="li setrow" id=regRow data-open=setReg><span class=grow>Registration<span class=sum id=regSum> Not set</span></span>""" + _CHEV + """</button>
</div>
<div class=createfoot>
<p class=pagesub id=destHint>{% if not staff %}Sent to admins for review{% elif lane == 'lineup' %}Appears on Lineup by default{% else %}Appears on Home by default{% endif %}</p>
<button class="btn btn-primary full" name=action value=preview>{{ 'Submit' if not staff else 'Preview event' }}</button>
</div>
<input class=pickhold type=date name=date id=dateInput>
<input class=pickhold type=time name=start id=startInput value=19:00>
<input class=pickhold type=time name=end id=endInput value=20:30>
<input class=pickhold type=month name=month id=monthInput>
<dialog class=botsheet id=setLevels><div class=sheet><div class=grab></div><h2>Skill levels &amp; division</h2>
<div class=checks>{% for pid, name, short, full in SPORTS.LEVELS %}<label><input type=checkbox name=level value="{{ pid }}"> {{ name }}</label>{% endfor %}</div>
<div class=checks>{% for pid, name in SPORTS.DIVISIONS %}<label><input type=checkbox name=division value="{{ pid }}"> {{ name }}</label>{% endfor %}</div>
<button type=button class="btn btn-primary full" onclick="this.closest('dialog').close()">Done</button></div></dialog>
<dialog class=botsheet id=setCoaches><div class=sheet><div class=grab></div><h2>Coaches</h2>
<div class=checks>{% for c in coaches %}<label><input type=checkbox name=coach value="{{ c.id }}"> {{ display_first(c) }} {{ c.last }}</label>{% else %}<p class=t3>No coaches on the list yet.</p>{% endfor %}</div>
<button type=button class="btn btn-primary full" onclick="this.closest('dialog').close()">Done</button></div></dialog>
<dialog class=botsheet id=setSocial><div class=sheet><div class=grab></div><h2>After-session social</h2>
<label>Place<input name=social_place id=socPlace autocomplete=off></label>
<label>Note<input name=social_note autocomplete=off></label>
<div class=checks>{% for kind in SOCIAL_KINDS %}<label><input type=checkbox name=social_kind value="{{ kind }}"> {{ kind }}</label>{% endfor %}</div>
<button type=button class="btn btn-primary full" onclick="this.closest('dialog').close()">Done</button></div></dialog>
<dialog class=botsheet id=setNotes><div class=sheet><div class=grab></div><h2>Notes &amp; media</h2>
<label>Notes<textarea name=note id=noteInput rows=3></textarea></label>
{{ upload_field('image') }}
<button type=button class="btn btn-primary full" onclick="this.closest('dialog').close()">Done</button></div></dialog>
{% if staff %}<dialog class=botsheet id=setPlan><div class=sheet><div class=grab></div><h2>Team plan</h2>
<div class=actseg role=radiogroup aria-label="Team plan">
<label><input type=radio name=team_plan value=considering checked><span>Considering</span></label>
<label><input type=radio name=team_plan value=planning><span>Planning</span></label>
<label><input type=radio name=team_plan value=committed><span>Committed</span></label>
</div>
<button type=button class="btn btn-primary full" onclick="this.closest('dialog').close()">Done</button></div></dialog>{% endif %}
<dialog class=botsheet id=setHost><div class=sheet><div class=grab></div><h2>Participation</h2>
<div class=actseg role=radiogroup aria-label="Participation">
<label><input type=radio name=hosting value=Attending checked><span>Attending</span></label>
<label><input type=radio name=hosting value=Hosting><span>Hosting</span></label>
</div>
<label>Host organization<input name=host_org autocomplete=off placeholder="IGLA+"></label>
<button type=button class="btn btn-primary full" onclick="this.closest('dialog').close()">Done</button></div></dialog>
<dialog class=botsheet id=setReg><div class=sheet><div class=grab></div><h2>Registration</h2>
<label>Format<select name=comp_format><option value="">Not set</option>{% for pid, name, blurb in SPORTS.FORMATS %}<option value="{{ pid }}">{{ name }}</option>{% endfor %}</select></label>
<label>Link<input name=link inputmode=url placeholder="https://"></label>
<label>Estimated cost<input name=cost autocomplete=off></label>
<label>Capacity<input name=capacity inputmode=numeric></label>
<label>Register by<input type=date name=reg_deadline></label>
<button type=button class="btn btn-primary full" onclick="this.closest('dialog').close()">Done</button></div></dialog>
</form>
<script>
(function(){
 var staff={{ 'true' if staff else 'false' }};
 var lane=document.getElementById('laneVal');
 var sched=document.getElementById('schedBlock'), line=document.getElementById('lineBlock');
 var schedSets=document.getElementById('schedSets'), lineSets=document.getElementById('lineSets');
 var hint=document.getElementById('destHint');
 var titleMode=document.getElementById('titleMode'), titleField=document.getElementById('titleField'), titleInput=document.getElementById('titleInput'), live=document.getElementById('liveTitle');
 function sessionName(){ var r=document.querySelector('input[name=activity_type]:checked'); var k=r?r.value:'practice'; return k==='scrimmage'?'Scrimmage':(k==='game'?'Game':'Practice'); }
 function autoTitle(){ var sportEl=document.getElementById('sportSel'); var sport=sportEl?((sportEl.value||'Water Polo').trim()||'Water Polo'):'Water Polo'; return sport+' '+sessionName(); }
 function paintTitle(){ if(!live||!titleMode) return; if(titleMode.value!=='custom'){ live.textContent=autoTitle(); if(titleInput) titleInput.value=''; } }
 function showLane(name){
  if(!staff) name='lineup';
  lane.value=name;
  var home=name!=='lineup';
  if(sched) sched.hidden=!home;
  if(line) line.hidden=home;
  if(schedSets) schedSets.hidden=!home;
  if(lineSets) lineSets.hidden=home;
  if(hint) hint.textContent=home?'Appears on Home by default':'Appears on Lineup by default';
  document.querySelectorAll('button.lanecard').forEach(function(b){ b.classList.toggle('on', b.getAttribute('data-lane')===name); });
  paintTitle(); syncLine();
 }
 function syncPrec(){
  var prec=document.getElementById('whenPrec'), exact=document.getElementById('exactWhen'), month=document.getElementById('monthWhen');
  if(prec) prec.hidden=!staff;
  var on=document.querySelector('input[name=date_precision]:checked');
  var monthOn=!!(staff && on && on.value==='month');
  if(exact){ exact.hidden=monthOn; exact.querySelectorAll('input,select,button').forEach(function(el){ el.disabled=monthOn; }); }
  if(month){ month.hidden=!monthOn; month.querySelectorAll('input,select,button').forEach(function(el){ el.disabled=!monthOn; }); }
  var monthInput=document.getElementById('monthInput'); if(monthInput) monthInput.disabled=!monthOn;
  var dateInput=document.getElementById('dateInput'); if(dateInput) dateInput.disabled=monthOn;
  ['startInput','endInput'].forEach(function(id){ var el=document.getElementById(id); if(el) el.disabled=monthOn; });
 }
 document.querySelectorAll('input[name=date_precision]').forEach(function(r){ r.addEventListener('change', syncPrec); });
 document.querySelectorAll('button.lanecard').forEach(function(b){ b.onclick=function(){ showLane(b.getAttribute('data-lane')); syncPrec(); }; });
 syncPrec();
 document.querySelectorAll('input[name=activity_type]').forEach(function(r){ r.addEventListener('change', paintTitle); });
 var sport=document.getElementById('sportSel'); if(sport) sport.addEventListener('change', paintTitle);
 var custom=document.getElementById('customize'), reset=document.getElementById('titleReset');
 if(custom) custom.onclick=function(){ titleMode.value='custom'; titleField.hidden=false; titleInput.value=live.textContent; titleInput.focus(); };
 if(reset) reset.onclick=function(){ titleMode.value='auto'; titleField.hidden=true; titleInput.value=''; paintTitle(); };
  function clock(v){ if(!v) return ''; var p=v.split(':'); var h=parseInt(p[0],10), m=p[1]||'00'; var ap=h>=12?'PM':'AM'; h=h%12; if(!h) h=12; return h+':'+m+' '+ap; }
 function monthLabel(v){ if(!v||v.length<7) return ' Choose a month'; var names=['January','February','March','April','May','June','July','August','September','October','November','December']; var partEl=document.getElementById('datePart'); var part=partEl?partEl.value:''; var prefix=part==='early'?'Early ':(part==='mid'?'Mid ':(part==='late'?'Late ':'')); return ' '+prefix+names[(parseInt(v.slice(5,7),10)||1)-1]+' '+v.slice(0,4); }
 function syncWhen(){
  var d=document.getElementById('dateInput'), s=document.getElementById('startInput'), e=document.getElementById('endInput'), mo=document.getElementById('monthInput');
  var ds=document.getElementById('dateSum'), ss=document.getElementById('startSum'), es=document.getElementById('endSum'), ms=document.getElementById('monthSum');
  if(ds) ds.textContent=d&&d.value?(' '+d.value):' Add a date';
  if(ss) ss.textContent=s&&s.value?(' '+clock(s.value)):'';
  if(es) es.textContent=e&&e.value?(' '+clock(e.value)):'';
  if(ms) ms.textContent=monthLabel(mo&&mo.value);
 }
 ['dateInput','startInput','endInput','monthInput','datePart'].forEach(function(id){ var el=document.getElementById(id); if(el) el.addEventListener('change', syncWhen); });
 syncWhen();
 function syncLine(){
  var type=document.getElementById('lineType'); var name=type?type.value:'Social';
  var plan=document.getElementById('planRow'), part=document.getElementById('partRow'), reg=document.getElementById('regRow');
  var team=name==='Tournament'||name==='Competition'||name==='Trip'||name==='Clinic';
  var social=name==='Social'||name==='Volunteer'||name==='Fundraiser'||name==='Meeting'||name==='Other';
  if(plan) plan.hidden=!team;
  if(part) part.hidden=social;
  if(reg) reg.hidden=!(name==='Tournament'||name==='Competition');
  var title=document.getElementById('lineTitle');
  if(title && !title.value){
    title.placeholder=name==='Trip'?'Fall team trip':(name==='Social'?'Fall Team Dinner':(name==='Tournament'?'IGLA 2027':'Event name'));
  }
 }
 var lt=document.getElementById('lineType'); if(lt) lt.addEventListener('change', syncLine);
 paintTitle();
})();
</script>
""" + _PRACTICE_JS
T["lineup_edit"] = """<form id=eventForm method=post action="{{ action }}" enctype=multipart/form-data>{{ csrf_field() }}
<input type=hidden name=mode value="{{ values.mode or mode }}">
<button type=submit name=action value=save style="position:absolute;left:-9999px;width:1px;height:1px;overflow:hidden" tabindex=-1>{{ save_label or 'Save' }}</button>
<div class=bannerpick>
<div class="t3 xs">Banner image</div>
{{ upload_field('banner', src=('/lineup-image/' ~ event_id ~ '?v=' ~ banner) if banner and event_id else '', clear_name='banner_clear') }}
</div>
<label>Type<select name=event_type id=lineType>{% for name, label in event_types %}<option value="{{ name }}" {% if values.event_type == name %}selected{% endif %}>{{ label }}</option>{% endfor %}</select></label>
<div class="t3 xs">Where</div>
<div class=actseg id=lineHost role=radiogroup aria-label=Where>
<label><input type=radio name=hosting value=Attending {% if values.hosting != 'Hosting' %}checked{% endif %}><span>Attending</span></label>
<label><input type=radio name=hosting value=Hosting {% if values.hosting == 'Hosting' %}checked{% endif %}><span>Hosting</span></label>
</div>
<label id=lineOrg {% if values.hosting == 'Hosting' %}hidden{% endif %}>Host organization<input name=host_org value="{{ values.host_org }}" placeholder="IGLA+" autocomplete=off></label>
{% if organizer %}
<div class="t3 xs">Status</div>
<div class=actseg role=radiogroup aria-label=Status>
<label><input type=radio name=team_intent value=considering {% if values.team_intent == 'considering' %}checked{% endif %}><span>Considering</span></label>
<label><input type=radio name=team_intent value=official {% if values.team_intent != 'considering' %}checked{% endif %}><span>Official</span></label>
</div>
{% endif %}
<label>Title<input name=title value="{{ values.title }}" required autocomplete=off></label>
<div class="t3 xs">Dates</div>
{% if organizer %}<div class=actseg role=radiogroup aria-label=Dates>
<label><input type=radio name=date_precision value=exact {% if values.date_precision != 'month' %}checked{% endif %}><span>Exact dates</span></label>
<label><input type=radio name=date_precision value=month {% if values.date_precision == 'month' %}checked{% endif %}><span>Month only</span></label>
</div>{% endif %}
<div id=exactDates {% if organizer and values.date_precision == 'month' %}hidden{% endif %}>
<div class=row><label>Starts<input type=date name=date value="{{ values.date }}"></label><label>Ends<input type=date name=end_date value="{{ values.end_date }}"></label></div>
<div class=row><label>Start time<input type=time name=start_time value="{{ values.start_time or '09:00' }}"></label><label>End time<input type=time name=end_time value="{{ values.end_time }}"></label></div>
</div>
<div id=monthDates {% if not organizer or values.date_precision != 'month' %}hidden{% endif %}>
<label>Month<input type=month name=month value="{{ values.month }}"></label>
<input type=hidden name=date_part data-monthpart value="{{ values.date_part if values.date_part in ('early', 'mid', 'late') else 'all' }}">
</div>
<label>City<span class=locok hidden><svg width="16" height="16" viewBox="0 0 256 256" fill="currentColor" aria-hidden="true"><path d="M128,24A104,104,0,1,0,232,128,104.11,104.11,0,0,0,128,24Zm45.66,85.66-56,56a8,8,0,0,1-11.32,0l-24-24a8,8,0,0,1,11.32-11.32L112,148.69l50.34-50.35a8,8,0,0,1,11.32,11.32Z"/></svg> Verified</span><input name=city value="{{ values.city }}" data-places required placeholder="Toronto, Canada" autocomplete=off></label>
<label>Venue<span class=locok hidden><svg width="16" height="16" viewBox="0 0 256 256" fill="currentColor" aria-hidden="true"><path d="M128,24A104,104,0,1,0,232,128,104.11,104.11,0,0,0,128,24Zm45.66,85.66-56,56a8,8,0,0,1-11.32,0l-24-24a8,8,0,0,1,11.32-11.32L112,148.69l50.34-50.35a8,8,0,0,1,11.32,11.32Z"/></svg> Verified</span><input name=venue value="{{ values.location }}" data-places placeholder="Name and address, optional" autocomplete=off></label>
<label>Short description<textarea name=description rows=3 required>{{ values.description }}</textarea></label>
<details class=moredetails><summary>More details</summary>
{{ sports_editor(sports_row, false, true) }}
<label>Link<input name=link value="{{ values.link }}" inputmode=url autocomplete=off placeholder="https://"></label>
<label>Capacity<input name=capacity inputmode=numeric value="{{ values.capacity }}" autocomplete=off></label>
<label>Estimated cost<input name=cost value="{{ values.cost }}" autocomplete=off></label>
<label>Register by<input type=date name=reg_deadline value="{{ values.reg_deadline }}"></label>
<label>Extra details<textarea name=details rows=3>{{ values.details }}</textarea></label>
{% if me().is_admin %}<input type=hidden name=pin_present value=1><label><input type=checkbox name=featured value=1 {% if values.featured == '1' %}checked{% endif %}> Pin</label>{% endif %}
</details>
{% if organizer and not event_id %}<button class="btn btn-secondary full" name=action value=draft>Save draft</button>{% endif %}
{% if show_cancel %}<button class="btn btn-danger full" name=action value=cancel onclick="return confirm('Cancel this event?')">Cancel event</button>{% endif %}
{% if show_delete %}<button class="btn btn-danger full" name=action value=delete onclick="return confirm('Delete this event?')">Delete event</button>{% endif %}
</form>
<script>(function(){
 var org=document.getElementById('lineOrg');
 function sync(){
  var on=document.querySelector('input[name=hosting]:checked');
  var away=!(on&&on.value==='Hosting');
  if(org){org.hidden=!away; var field=org.querySelector('input'); if(field) field.disabled=!away;}
 }
 document.querySelectorAll('input[name=hosting]').forEach(function(r){r.addEventListener('change', sync)});
 sync();
 var exactBox=document.getElementById('exactDates'), monthBox=document.getElementById('monthDates');
 var canMonth={{ 'true' if organizer else 'false' }};
 function datesMode(){
  var on=document.querySelector('input[name=date_precision]:checked');
  var month=!!(canMonth&&on&&on.value==='month');
  if(exactBox){exactBox.hidden=month; exactBox.querySelectorAll('input,select').forEach(function(el){el.disabled=month});}
  if(monthBox){monthBox.hidden=!month; monthBox.querySelectorAll('input,select').forEach(function(el){el.disabled=!month});}
 }
 document.querySelectorAll('input[name=date_precision]').forEach(function(r){r.addEventListener('change', datesMode)});
 datesMode();
})();</script>"""
T["series_edit"] = """<form id=seriesForm method=post action="{{ action }}">{{ csrf_field() }}
{{ sports_editor(series) }}
<div class=checks role=group aria-label="Weekdays"><div class="t3 xs">Weekdays</div>
{% for value, label in values.labels %}<label style="margin:8px 0"><input type=checkbox name=weekday value="{{ value }}" {% if value in values.weekdays %}checked{% endif %}>{{ label }}</label>{% endfor %}</div>
<div class=row><label>Start<input type=time name=start value="{{ values.start }}" required></label><label>End<input type=time name=end value="{{ values.end }}" required></label></div>
<label>Location<span class=locok hidden><svg width="16" height="16" viewBox="0 0 256 256" fill="currentColor" aria-hidden="true"><path d="M128,24A104,104,0,1,0,232,128,104.11,104.11,0,0,0,128,24Zm45.66,85.66-56,56a8,8,0,0,1-11.32,0l-24-24a8,8,0,0,1,11.32-11.32L112,148.69l50.34-50.35a8,8,0,0,1,11.32,11.32Z"/></svg> Verified</span><input name=location value="{{ values.location }}" data-places required autocomplete=off></label>
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
<div class=nxcardhead><div class=nxtitle>{{ practice_title(p) }}</div></div>
{% set tile = practice_tile(p) %}
<div class=nxmain><div class=datetile><span class=pdate>{% if x.unseen %}<span class=badge data-seen={{p.id}}>{{ x.unseen if x.unseen < 100 else '99+' }}</span>{% endif %}</span><span class=wd>{{ tile.wd }}</span><span class=dn>{{ tile.dn }}</span><span class=mo>{{ tile.mo }}</span></div>
<div class="grow schedrows"><div class=nxrow>{{ glyph_clock() }}<span>{% if practice_is_month(p) %}{{ practice_when(p) }}{% else %}{{ fmt_span(p.start, p.end) }}{% endif %}</span></div>
<div class=nxrow>{{ glyph_pin() }}<span>{{ p.location }}</span></div>
<div class=nxrow>{{ glyph_people() }}<span>{{ x.going|length }} going{% if x.coach_names %} · Coaches: {{ x.coach_names|join(', ') }}{% endif %}</span></div>
{% if practice_sports_line(p) %}<div class="t3 sm sportline">{{ practice_sports_line(p) }}</div>{% endif %}</div></div>
{% if p.cancelled %}{{ st('bad','Cancelled') }}{% if p.cancel_reason %}<div class="t3 sm">{{ p.cancel_reason }}</div>{% endif %}{% endif %}
{% if p.note %}<div class=nxnote>{{p.note}}</div>{% endif %}
{% if p.coach_note %}<div class=nxnote>{{ p.coach_note }} · {{ p.coach_note_by }} · {{ fmt_stamp(p.coach_note_at) }}</div>{% endif %}</a>
{% if not p.cancelled %}<form method=post action=/practices class=pills>{{csrf_field()}}<input type=hidden name=pid value={{p.id}}>
{{ rsvp_btn('Going', x.mine == 1, 'going') }}
{{ rsvp_btn('Not going', x.mine == 0, 'notgoing') }}</form>
{% endif %}</div>{% endfor %}
""" + _PRACTICE_JS

T["practice"] = """{% set p = x.p %}
{{ event_hero('practiceMap', pins if not p.image else [], ('/practice-image/' ~ p.id ~ '?v=' ~ p.image) if p.image else '', p.location or 'Practice') }}
<div class=profilehero>
<div class=profilename>{{ practice_title(p) }}</div>
{% if practice_sports_line(p) %}<p class="t3 sm sportline">{{ practice_sports_line(p) }}</p>{% endif %}
{% if p.activity_type == 'hybrid' %}{% for seg in SPORTS.parse_segments(p.segments) %}<p class="t3 sm">{{ SPORTS.ACTIVITY_NAME.get(seg.type, seg.type) }} · {{ fmt_span(seg.start, seg.end) }}</p>{% endfor %}{% endif %}
{% if p.opponent and p.activity_type == 'game' %}<p class=pracemeta>{% if p.home_away == 'home' %}Home{% elif p.home_away == 'away' %}Away{% endif %}{% if p.home_away %} · {% endif %}vs. {{ p.opponent }}</p>{% endif %}
<p class=pracemeta>{% if practice_is_month(p) %}{{ practice_when(p) }}{% else %}{{ fmt_card_date(p.date) }} · {{ fmt_clock(p.start) }} – {{ fmt_clock(p.end) }}{% endif %}</p>
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
{% if p.skill_levels %}<details class=card><summary>Skill levels</summary>{% for row in SPORTS.LEVELS %}<p><b>{{ row[1] }}</b> {{ row[3] }}</p>{% endfor %}</details>{% endif %}
{% if editing %}
<form id=practiceForm method=post action="/practices/{{ p.id }}" class=card style="margin-top:16px" enctype=multipart/form-data>{{ csrf_field() }}<input type=hidden name=pid value={{ p.id }}><input type=hidden name=back value=page>
{{ sports_editor(p) }}
<label>Date<input type=date name=date value="{{ p.date }}" required></label>
{% if p.series_id %}<label>Apply changes to<select name=series_scope><option value=once>Only this date</option><option value=following>This and following</option></select></label>{% endif %}
<div class=row><label>Start<input type=time name=start value="{{ p.start }}" required></label><label>End<input type=time name=end value="{{ p.end }}" required></label></div>
<label>Location / address<span class=locok hidden><svg width="16" height="16" viewBox="0 0 256 256" fill="currentColor" aria-hidden="true"><path d="M128,24A104,104,0,1,0,232,128,104.11,104.11,0,0,0,128,24Zm45.66,85.66-56,56a8,8,0,0,1-11.32,0l-24-24a8,8,0,0,1,11.32-11.32L112,148.69l50.34-50.35a8,8,0,0,1,11.32,11.32Z"/></svg> Verified</span><input name=location value="{{ p.location or '' }}" data-places required autocomplete=off></label>
<label>Notes<textarea name=note>{{ p.note or '' }}</textarea></label>
<div class="t3 xs" style="margin:4px 0 8px">After-practice social</div>
{{ social_fields(p) }}
{{ message_fields(p) }}
<div class="t3 xs" style="margin:4px 0 8px">Practice image</div>
{{ upload_field('image', src=('/practice-image/' ~ p.id ~ '?v=' ~ p.image) if p.image else '', clear_name='image_clear') }}
<div class=checks role=group aria-label="Coaches"><div class="t3 xs">Coaches</div>
<label style="margin:0 0 8px"><input type=radio name=lead value="" {% if not x.lead_id %}checked{% endif %}>No lead</label>
{% for c in coach_choices %}<div style="padding:8px 0;border-top:1px solid var(--line)">
<label style="margin:0"><input type=checkbox name=coach value="{{ c.id }}" {% if c.id in x.coach_ids %}checked{% endif %}>{{ display_first(c) }} {{ c.last }} {{ coach_tag(c) }}</label>
<label style="margin:8px 0 0"><input type=radio name=lead value="{{ c.id }}" {% if c.id == x.lead_id %}checked{% endif %}>Lead</label>
<label style="margin:8px 0 0">Focus group<input name="focus-{{ c.id }}" list=focusGroups value="{{ x.focuses.get(c.id, '') }}" placeholder="Beginners, Intermediate, Advanced, Goalies" autocomplete=off></label>
</div>{% else %}<p class="t3 sm">No coaches yet. Add someone on People.</p>{% endfor %}</div>
<datalist id=focusGroups><option value=Beginners><option value=Intermediate><option value=Advanced><option value=Goalies></datalist>
<label>Practice plan<textarea class=planfield name=coaching_plan rows=4>{{ p.coaching_plan or '' }}</textarea></label>
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
{{ rsvp_btn('Going', x.mine == 1, 'going') }}
{{ rsvp_btn('Not going', x.mine == 0, 'notgoing') }}</form>{% endif %}
<div class=seclabel>Details</div>
<div class=list><div class=li><div class=grow>
{% if p.note %}<div class="prow" style="padding:0"><span class=k>Notes</span><span class=v>{{ p.note }}</span></div>{% endif %}
{% if p.coach_note %}<div class="prow" style="padding:0"><span class=k>Coach note</span><span class=v>{{ p.coach_note }} · {{ p.coach_note_by }}{% if p.coach_note_at %} · {{ fmt_stamp(p.coach_note_at) }}{% endif %}</span></div>{% endif %}
{% if not p.note and not p.coach_note %}<span class=t3>No notes yet.</span>{% endif %}
</div>{% if can_host_practice() %}<button type=button class="btn btn-secondary" data-open="notes{{ p.id }}">{{ 'Edit' if p.note else 'Add' }}</button>{% endif %}</div></div>
<div class=seclabel>After-practice social</div>
<div class=list><div class=li>{% if social_line(p) %}{{ social_icon() }}{% endif %}<div class=grow>
{% if social_line(p) %}<div>{{ social_line(p) }}{% if p.social_time %} · {{ fmt_t(p.social_time) }}{% endif %}</div>
<div class="t3 sm">{{ x.social_n }} joining</div>
{% if p.social_note %}<div class="t2 sm">{{ p.social_note }}</div>{% endif %}
{% if p.social_address %}{% if p.social_address.lower().startswith('http://') or p.social_address.lower().startswith('https://') %}<div class="sm"><a href="{{ p.social_address }}" target=_blank rel=noopener>Map</a></div>{% else %}<div class="t2 sm">{{ p.social_address }} · <a href="https://www.google.com/maps/dir/?api=1&amp;destination={{ p.social_address|urlencode }}" target=_blank rel=noopener>Map</a></div>{% endif %}{% endif %}
{% else %}<span class=t3>None yet.</span>{% endif %}
</div>{% if me().is_admin or is_staff() %}<button type=button class="btn btn-secondary" data-open="social{{ p.id }}">{{ 'Edit' if social_line(p) else 'Add' }}</button>{% endif %}</div></div>
<div class=seclabel>Coaches</div>
<div class=list>
{% if plan_editing %}<form id=practiceForm method=post action="/practices/{{ p.id }}">{{ csrf_field() }}<input type=hidden name=pid value={{ p.id }}><input type=hidden name=back value=page><input type=hidden name=plan_fields value=1>
<div class=li><span class="chip-info" style="margin:0">Coaches only</span></div>
<div class=li><label class=prefedit style="width:100%;margin:0">Practice plan<textarea class=planfield name=coaching_plan rows=4>{{ p.coaching_plan or '' }}</textarea></label></div>
{% if x.coaches %}<div class=li><label style="margin:0"><input type=radio name=lead value="" {% if not x.lead_id %}checked{% endif %}>No lead</label></div>{% endif %}
{% for c in x.coaches %}<div class=li><div class=grow>
<label style="margin:0"><input type=radio name=lead value="{{ c.id }}" {% if c.is_lead %}checked{% endif %}>{{ display_first(c) }} {{ c.last }}</label>
<label style="margin:8px 0 0">Plan<input name="focus-{{ c.id }}" list=focusGroups value="{{ c.focus or '' }}" placeholder="Beginners, Intermediate, Advanced, Goalies" autocomplete=off></label>
</div></div>{% endfor %}
<datalist id=focusGroups><option value=Beginners><option value=Intermediate><option value=Advanced><option value=Goalies></datalist>
</form>
{% else %}
{% for c in x.coaches %}{% set editable = can_host_practice() and (me().is_admin or c.id == me().id) %}{% if editable %}<button type=button class="li coachrow" data-open="cfocus{{ p.id }}-{{ c.id }}"><span class=coachline>{{ person_mark(c) }}<span class=ell>{{ display_first(c) }} {{ c.last }}</span>{% if c.is_lead %}<span class="chip-info" style="margin:0">Lead</span>{% endif %}</span>{% if c.focus %}<span class="t3 sm">{{ c.focus }}</span>{% endif %}</button>{% else %}<div class=li><div class=grow><div style="display:flex;align-items:center;gap:8px;min-width:0">{% if can_host_practice() %}{{ person_mark(c) }}{% endif %}<span class=ell>{{ display_first(c) }} {{ c.last }}</span>{% if c.is_lead %}<span class="chip-info" style="margin:0">Lead</span>{% endif %}</div>{% if can_host_practice() and c.focus %}<div class="t3 sm">{{ c.focus }}</div>{% endif %}</div></div>{% endif %}{% else %}<div class=li><span class=t3>No coaches assigned.</span></div>{% endfor %}
{% if can_host_practice() %}<div class="li planrow"><div class=planline><span class=planlabel>Practice plan</span><span class="chip-info" style="margin:0">Coaches only</span></div><button type=button class="btn btn-secondary" data-open="plan{{ p.id }}">{{ 'Edit' if p.coaching_plan else 'Add' }}</button>{% if p.coaching_plan %}<div class="t3 sm plantext">{{ p.coaching_plan }}</div>{% endif %}</div>{% endif %}
{% endif %}
</div>
{{ whos_going(x.going) }}
<div class=seclabel>Can't make it</div>
<div class=list>{% for r in x.notgoing %}<div class=li><div class=grow>{{ display_first(r) }} {{ r.last }}</div></div>{% else %}<div class=li><span class=t3>No one yet.</span></div>{% endfor %}</div>
<div class=seclabel>Checked in</div>
<div class=list>{% for r in x.checked %}<div class=li><div class=grow>{{ display_first(r) }} {{ r.last }}</div></div>{% else %}<div class=li><span class=t3>No one yet.</span></div>{% endfor %}</div>
{% if p.location %}{% set dest = (pins[0].lat|string ~ ',' ~ pins[0].lng|string) if pins else (p.address or p.location) %}{{ event_location('practiceLoc', pins, p.location, p.address or '', 'https://www.google.com/maps/dir/?api=1&destination=' ~ (dest|urlencode)) }}{% endif %}
{% endif %}
{% if me().is_admin or is_staff() %}{{ practice_extra_dialogs(p, 'page') }}
<dialog class=modal id=plan{{ p.id }}><div class=sheet><h2 style="margin:0 0 12px">Practice plan</h2>
<form method=post action="/practices/{{ p.id }}">{{ csrf_field() }}<input type=hidden name=pid value={{ p.id }}><input type=hidden name=back value=page>
<textarea class=planfield name=coaching_plan rows=4 aria-label="Practice plan">{{ p.coaching_plan or '' }}</textarea>
<button class="btn btn-primary full" name=action value=plan>Save</button></form></div></dialog>
{% for c in x.coaches %}{% if me().is_admin or c.id == me().id %}<dialog class=modal id="cfocus{{ p.id }}-{{ c.id }}"><div class=sheet><h2 style="margin:0 0 12px">{{ display_first(c) }} {{ c.last }}</h2>
<form method=post action="/practices/{{ p.id }}">{{ csrf_field() }}<input type=hidden name=pid value={{ p.id }}><input type=hidden name=back value=page><input type=hidden name=coach_id value="{{ c.id }}">
<label>Plan<input name=focus list=planFocus value="{{ c.focus or '' }}" placeholder="Beginners, Intermediate, Advanced, Goalies" autocomplete=off></label>
<button class="btn btn-primary full" name=action value=coach_plan>Save</button></form></div></dialog>{% endif %}{% endfor %}
<datalist id=planFocus><option value=Beginners><option value=Intermediate><option value=Advanced><option value=Goalies></datalist>
{% endif %}
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
<p class="t2 sm">{% if practice_is_month(p) %}{{ practice_when(p) }} at {{ p.location }}.{% else %}{{ fmt_d(p.date) }}, {{ fmt_t(p.start) }}–{{ fmt_t(p.end) }} at {{ p.location }}.{% endif %}</p>
<form method=post action="/practices/{{ p.id }}">{{ csrf_field() }}<input type=hidden name=pid value={{ p.id }}>
<div class=row><button class="btn btn-danger" name=action value=delete>Delete practice</button><button type=button class="btn btn-secondary" onclick="this.closest('dialog').close()">Cancel</button></div></form></div></dialog>
{% endif %}""" + _PRACTICE_JS

_CHEV_L = '<svg width="20" height="20" viewBox="0 0 256 256" fill="currentColor" aria-hidden="true"><path d="M165.66,202.34a8,8,0,0,1-11.32,11.32l-80-80a8,8,0,0,1,0-11.32l80-80a8,8,0,0,1,11.32,11.32L91.31,128Z"/></svg>'
_CHEV_R = '<svg width="20" height="20" viewBox="0 0 256 256" fill="currentColor" aria-hidden="true"><path d="M181.66,133.66l-80,80a8,8,0,0,1-11.32-11.32L164.69,128,90.34,53.66a8,8,0,0,1,11.32-11.32l80,80A8,8,0,0,1,181.66,133.66Z"/></svg>'
_CAL_I = '<svg width="20" height="20" viewBox="0 0 256 256" fill="currentColor" aria-hidden="true"><path d="M208,32H184V24a8,8,0,0,0-16,0v8H88V24a8,8,0,0,0-16,0v8H48A16,16,0,0,0,32,48V208a16,16,0,0,0,16,16H208a16,16,0,0,0,16-16V48A16,16,0,0,0,208,32ZM72,48v8a8,8,0,0,0,16,0V48h80v8a8,8,0,0,0,16,0V48h24V80H48V48ZM208,208H48V96H208V208Z"/></svg>'
T["admin"] = ADMIN_NAV + """{% call admin_page('Schedule') %}<a class="btn quiet pageact" href="/events/new?lane=schedule">Create</a>{% endcall %}
{%- set qbit -%}{% if q %}&amp;q={{ q|urlencode }}{% endif %}{%- endset -%}
{%- set fbit -%}{% if filt != 'going' %}&amp;filt={{ filt }}{% endif %}{%- endset -%}
<div class=checkbar>
<div class=calpick id=calPick data-date="{{date}}" data-today="{{ today }}" data-q="{{q}}" data-filt="{{ '' if filt=='going' else filt }}" data-dates='{{ days|tojson }}' data-events='{{ catalog|tojson }}'>
{% if prev_href %}<a class=calnav href="{{ prev_href }}" aria-label="Previous event">""" + _CHEV_L + """</a>{% else %}<span class=calnav aria-disabled=true aria-label="Previous event">""" + _CHEV_L + """</span>{% endif %}
{% if ev_n > 1 %}<button type=button class=evcount id=evCount aria-haspopup=dialog aria-controls=evPick>{{ ev_i }}/{{ ev_n }}</button>{% elif ev_n == 1 %}<span class=evcount>{{ ev_i }}/{{ ev_n }}</span>{% endif %}
<button type=button class=calbtn id=calOpen aria-haspopup=dialog aria-expanded=false aria-controls=calPop>""" + _CAL_I + """<span>{{ fmt_d(date).replace(' ', ', ', 1) }}</span></button>
{% if next_href %}<a class=calnav href="{{ next_href }}" aria-label="Next event">""" + _CHEV_R + """</a>{% else %}<span class=calnav aria-disabled=true aria-label="Next event">""" + _CHEV_R + """</span>{% endif %}
</div>
<dialog class=matpick id=calPop aria-label="Select date"><div class=sheet>
<div class=matkicker>Select date</div>
<div class=matheadline id=calHeadline>{{ fmt_d(date).replace(' ', ', ', 1) }}</div>
<div id=calMonthView>
<div class=calhead>
<button type=button class=calmonth id=calPrevM aria-label="Previous month">""" + _CHEV_L + """</button>
<div class=lbl id=calLabel>{{ month.label }}</div>
<button type=button class=calmonth id=calNextM aria-label="Next month">""" + _CHEV_R + """</button></div>
<div class=calwd><span>S</span><span>M</span><span>T</span><span>W</span><span>T</span><span>F</span><span>S</span></div>
<div class=calgrid id=calGrid>{% for c in month.cells %}{% if c is none %}<span class=calday></span>{% elif c.has %}<a class="calday{% if c.on %} on{% endif %}{% if c.today %} today{% endif %}{% if c.past %} past{% endif %}" href="/admin?date={{ c.iso }}{{ fbit }}{{ qbit }}" data-date="{{ c.iso }}">{{ c.day }}<i class=caldot></i></a>{% else %}<span class="calday{% if c.today %} today{% endif %}{% if c.past %} past{% endif %}" aria-disabled=true>{{ c.day }}</span>{% endif %}{% endfor %}</div>
</div>
<div id=calEventView hidden>
<button type=button class=calback id=calBack aria-label="Back to the month">""" + _CHEV_L + """<span id=calEventLabel>Events</span></button>
<div class=list id=calEventList></div>
</div>
<div class=matactions>
<button type=button class=mattext id=calCancel>Cancel</button>
<button type=button class=mattext id=calOk>OK</button>
</div>
</div></dialog>
<dialog class=modal id=evPick><div class=sheet><h2 style="margin:0 0 12px">Events</h2><div class=list id=evPickList>{% for ev in events %}<a class=li href="/admin?date={{ date }}&amp;ev={{ ev.key }}{{ fbit }}{{ qbit }}" style="color:inherit;text-decoration:none"><span class=grow><span class=ell style="display:block;font-weight:650">{{ ev.title }}</span><span class="t3 sm">{{ ev.when }}</span></span></a>{% endfor %}</div><button type=button class="btn btn-secondary full" onclick="this.closest('dialog').close()">Cancel</button></div></dialog>
</div>
{% if sel %}<a class="card evcard" href="{{ sel.detail }}">
<div class=nxtitle>{{ sel.title }}</div>
<p class=t2>{{ sel.when }}</p>
{% if sel.place %}<p class=t2>{{ sel.place }}</p>{% endif %}
{% if sel.who %}<p class="t3 sm">{{ sel.who }}</p>{% endif %}
</a>{% else %}<p class=emptyfind>No events on this day</p>{% endif %}
<div class=checkmeta>
<div class="filt checkfilt chiprow" role=group aria-label="RSVP">
<a class="chip{{ ' chip-active on' if filt=='going' }}" href="/admin?date={{ date }}{% if q %}&amp;q={{ q|urlencode }}{% endif %}{% if evkey %}&amp;ev={{ evkey }}{% endif %}">Going ({{ going|length }})</a>
{% if n_not %}<a class="chip{{ ' chip-active on' if filt=='not' }}" href="/admin?date={{ date }}&amp;filt=not{% if q %}&amp;q={{ q|urlencode }}{% endif %}{% if evkey %}&amp;ev={{ evkey }}{% endif %}">Not Going ({{ n_not }})</a>{% else %}<button type=button class=chip disabled aria-disabled=true>Not Going (0)</button>{% endif %}
{% if n %}<a class="chip{{ ' chip-active on' if filt=='in' }}" href="/admin?date={{ date }}&amp;filt=in{% if q %}&amp;q={{ q|urlencode }}{% endif %}{% if evkey %}&amp;ev={{ evkey }}{% endif %}">Checked in ({{ n }})</a>{% else %}<button type=button class=chip disabled aria-disabled=true>Checked in (0)</button>{% endif %}
</div>
<form class=playersearch method=get action=/admin><input type=hidden name=date value="{{ date }}">{% if filt != 'going' %}<input type=hidden name=filt value="{{ filt }}">{% endif %}{% if evkey %}<input type=hidden name=ev value="{{ evkey }}">{% endif %}<input name=q value="{{ q }}" placeholder="Search players..." style="margin:0"></form>
</div>
{% macro ci(r) %}
<div class="li personrow cirow" data-rsvp="{{ 'going' if r.going==1 else ('not' if r.going==0 else 'none') }}" data-checked="{{ 1 if r.cid else 0 }}">{% call person_link(r) %}{% endcall %}
<form method=post>{{csrf_field()}}<input type=hidden name=member_id value={{r.id}}><input type=hidden name=date value={{date}}><input type=hidden name=q value="{{q}}"><input type=hidden name=filt value="{{filt}}">{% if evkey %}<input type=hidden name=ev value="{{ evkey }}">{% endif %}
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
{% if coming %}<div class=seclabel>Coming up</div><div class=list>{% for item in coming %}<a class=li href="{{ item.href }}" style="color:inherit;text-decoration:none"><span class=grow><span class=ell style="display:block;font-weight:600">{{ item.title }}</span><span class="t3 sm">{{ item.when }}{% if item.place %} · {{ item.place }}{% endif %}</span></span></a>{% endfor %}</div>{% endif %}
<script>
if(!window.grunionsConfirm){window.grunionsConfirm=1;
 document.addEventListener('click',function(e){var b=e.target.closest&&e.target.closest('[data-confirm]');if(!b||b.dataset.ok)return;e.preventDefault();if(window.confirm(b.getAttribute('data-confirm'))){b.dataset.ok='1';b.click()}});
}
</script>
<script>
(function(){
var root=document.getElementById('calPick'); if(!root) return;
var pop=document.getElementById('calPop'), openBtn=document.getElementById('calOpen'), grid=document.getElementById('calGrid'), label=document.getElementById('calLabel');
var monthView=document.getElementById('calMonthView'), eventView=document.getElementById('calEventView'), eventList=document.getElementById('calEventList'), eventLabel=document.getElementById('calEventLabel');
var dates=[]; try{dates=JSON.parse(root.getAttribute('data-dates')||'[]')}catch(err){dates=[]}
var catalog={}; try{catalog=JSON.parse(root.getAttribute('data-events')||'{}')}catch(err){catalog={}}
var set={}; dates.forEach(function(d){set[d]=1});
var q=root.getAttribute('data-q')||'', filt=root.getAttribute('data-filt')||'', selected=root.getAttribute('data-date')||'', today=root.getAttribute('data-today')||'', shown=selected.slice(0,7), pending=selected;
function pad(n){return (n<10?'0':'')+n}
function href(iso, ev){return '/admin?date='+iso+(ev?'&ev='+encodeURIComponent(ev):'')+(filt?'&filt='+encodeURIComponent(filt):'')+(q?'&q='+encodeURIComponent(q):'')}
function headline(iso){
 if(!iso||iso.length<10) return '';
 var p=iso.split('-'), dt=new Date(+p[0], +p[1]-1, +p[2]);
 var w=['Sun','Mon','Tue','Wed','Thu','Fri','Sat'][dt.getDay()];
 var mo=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'][dt.getMonth()];
 return w+', '+mo+' '+dt.getDate();
}
function showMonth(){ if(monthView) monthView.hidden=false; if(eventView) eventView.hidden=true; }
function showEvents(iso, list){
 if(!eventView||!eventList) return;
 if(monthView) monthView.hidden=true;
 eventView.hidden=false;
 if(eventLabel) eventLabel.textContent=headline(iso)||iso;
 eventList.innerHTML=list.map(function(ev){
  return '<a class=li href="'+href(iso, ev.key)+'" style="color:inherit;text-decoration:none"><span class=grow><span class=ell style="display:block;font-weight:650">'+String(ev.title||'').replace(/[&<>]/g,'')+'</span><span class="t3 sm">'+String(ev.when||'').replace(/[&<>]/g,'')+'</span></span></a>';
 }).join('');
}
var months=['January','February','March','April','May','June','July','August','September','October','November','December'];
function render(ym){
 shown=ym; var parts=ym.split('-'), y=+parts[0], m=+parts[1];
 if(label) label.textContent=months[m-1]+' '+y;
 var blanks=new Date(y, m-1, 1).getDay(), last=new Date(y, m, 0).getDate(), html='', day, iso, cls;
 for(var i=0;i<blanks;i++) html+='<span class=calday></span>';
 for(day=1; day<=last; day++){
  iso=y+'-'+pad(m)+'-'+pad(day);
  cls='calday'+(iso===pending?' on':'')+(iso===today?' today':'')+(iso<today?' past':'');
  if(set[iso]) html+='<a class="'+cls+'" data-date="'+iso+'" href="'+href(iso)+'">'+day+'<i class=caldot></i></a>';
  else html+='<span class="'+cls+'" aria-disabled=true>'+day+'</span>';
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
var back=document.getElementById('calBack');
if(back) back.onclick=function(){showMonth()};
var okBtn=document.getElementById('calOk'), cancelBtn=document.getElementById('calCancel'), head=document.getElementById('calHeadline');
function setHead(iso){ if(head) head.textContent=headline(iso)||'Select date'; }
if(cancelBtn) cancelBtn.onclick=function(){ pop.close(); };
if(okBtn) okBtn.onclick=function(){
 var iso=pending||selected; if(!iso){ pop.close(); return; }
 var list=catalog[iso]||[];
 if(list.length>1){ showEvents(iso, list); return; }
 if(iso===selected){ pop.close(); return; }
 location.href=href(iso);
};
openBtn.onclick=function(){
 pending=selected; showMonth(); setHead(pending);
 render(selected.slice(0,7)||shown);
 if(pop.showModal) pop.showModal();
 openBtn.setAttribute('aria-expanded','true');
};
pop.addEventListener('click', function(e){ if(e.target===pop) pop.close(); });
pop.addEventListener('close', function(){ openBtn.setAttribute('aria-expanded','false'); showMonth(); });
var countBtn=document.getElementById('evCount');
if(countBtn) countBtn.onclick=function(){ var dlg=document.getElementById('evPick'); if(dlg&&dlg.showModal) dlg.showModal(); };
grid.addEventListener('click', function(e){
 var a=e.target.closest&&e.target.closest('a.calday'); if(!a||a.getAttribute('aria-disabled')) return;
 e.preventDefault();
 pending=a.getAttribute('data-date')||pending;
 setHead(pending);
 render(pending.slice(0,7)||shown);
});
})();
</script>"""

T["transfer"] = ADMIN_NAV + """{{ admin_page('Transfer', 'Bring in a Sport:80 export, or download the roster and attendance.') }}
<h2>Import</h2>
<div class=card><ol class="t2 sm" style="margin:0;padding-left:18px;line-height:1.7">
<li>Log in at <a href=https://usawp.sport80.com>usawp.sport80.com</a> and switch to the Grunions club profile.</li>
<li>Members → Smart Lists → Edit Columns: name, email, membership status, member number, valid until, plus SafeSport / background columns.</li>
<li>Actions → Export Report, then upload the emailed file here.</li></ol>
<form method=post action=/transfer enctype=multipart/form-data style="margin-top:14px">{{csrf_field()}}{{ upload_field('file', 'file', 'CSV or Excel', '.csv,.xlsx') }}<button class="btn btn-primary full" style="margin-top:12px">Import</button></form>
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

T["members"] = ADMIN_NAV + """{% call admin_page('People') %}<a class="btn quiet pageact" href=/members.csv>Export CSV</a>{% endcall %}
{{ growth }}
<div class=peoplebar>
<form method=get action=/members><input name=q value="{{q}}" placeholder="Search people..." autocomplete=off>{% if view != 'members' %}<input type=hidden name=view value="{{view}}">{% endif %}</form>
<div class="fchips chiprow">
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
{% macro prow(r, kind) %}<div class="li personrow">{% call person_link(r) %}
<div class=eligs>{% if r.is_admin %}<span class=chip-info>Admin</span>{% endif %}{% set chip = coach_row_expiry(r) %}{% set ce = coach_eligibility(r) %}{% if r.role=='coach' or r.id in listed or ce.eligible or ce.text %}<span class="chip-info{{ ' ' ~ chip.tone if chip.tone else '' }}">Coach{% if chip.date %} · expires {{ chip.date }}{% endif %}</span>{% endif %}{% if r.id in referees %}<span class=chip-info>Referee</span>{% endif %}{{ referee_tag(r) }}</div>
{% endcall %}
<span class=more><button type=button class=morebtn aria-label="Actions for {{display_first(r)}} {{r.last}}" aria-haspopup=menu aria-expanded=false><svg width="20" height="20" viewBox="0 0 256 256" fill="currentColor" aria-hidden="true"><path d="M140,128a12,12,0,1,1-12-12A12,12,0,0,1,140,128Zm56-12a12,12,0,1,0,12,12A12,12,0,0,0,196,116ZM60,116a12,12,0,1,0,12,12A12,12,0,0,0,60,116Z"/></svg></button>
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

T["expiring"] = ADMIN_NAV + """{{ admin_page('Expiring', 'Membership, SafeSport, and other dated items. Tap a person to open them.') }}
<div class=expage>
<form class="row noprint" method=get action=/expiring style="align-items:center;margin-bottom:8px"><label class="t2 sm" style="flex:0 0 auto;margin:0">Window (days)<input name=days type=number min=1 value={{days}} onchange=this.form.submit() style="margin:6px 0 0;height:44px;width:96px"></label></form>
{% for key, label in [('expired','Expired'),('within_7','Next 7 days'),('within_%d'%days,'Next %d days'%days)] %}<h2 class=egroup>{{label}} <span class=t3>{{rep[key]|length}}</span></h2>
<div class=list>{% for r in rep[key] %}<div class=li><a class=grow href="/admin/member/{{ r.id }}" style="color:inherit;text-decoration:none;min-width:0"><div style="display:flex;align-items:center;gap:8px;min-width:0"><span class=ell style="font-weight:500;flex:1">{{display_first(r)}} {{r.last}}</span>
<span class="chip-info daybadge"><span class="dot {{ 'bad' if r.days_left < 0 else ('warn' if r.days_left <= 7 else '') }}" aria-hidden=true></span>{% if r.days_left < 0 %}{{ -r.days_left }}d ago{% elif r.days_left == 0 %}Today{% else %}{{ r.days_left }}d left{% endif %}</span></div>
<div class="t3 xs">{{ r.item }} · {{ fmt_long(r.usawp_valid_until) }}</div></a>
<a class="btn btn-secondary" href="/admin/member/{{ r.id }}?edit=1">Recheck</a></div>{% else %}<div class=li><span class=t3>None</span></div>{% endfor %}</div>{% endfor %}
<form method=post style="margin-top:20px">{{csrf_field()}}<input type=hidden name=action value=ask_all><input type=hidden name=days value="{{days}}"><button class="btn btn-primary full">Ask Grunions to recheck all</button></form>
<p class="t3 sm" style="margin-top:10px">Asks Grunions to look up everyone listed. Daily report: <a href=/api/expiring>/api/expiring</a>.</p>
</div>"""

T["requirements_page"] = ADMIN_NAV + """{{ admin_page('Rules', 'Cleared to play means a current USAWP membership and current SafeSport.') }}
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

T["qr_page"] = ADMIN_NAV + """{{ admin_page('Join QR', 'Anyone who scans this joins the team.') }}
<div style="text-align:center">
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

def _ds_nav(label, keys):
    names = {"home": "Home", "lineup": "Lineup", "chat": "Chat", "manage": "Manage"}
    links = "".join(_nav_anchor(key, "#ds-%s" % key, names[key], i == 0) for i, key in enumerate(keys))
    return '<nav class="tabs ds-sample" aria-label="%s">%s</nav>' % (label, links)

T["design_system"] = """<style>
.ds-swatches{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:var(--space-2)}
.ds-swatch{height:48px;border-radius:var(--radius-input);border:1px solid var(--line)}
.ds-name{margin:4px 0 var(--space-3);font-size:12px;color:var(--t3)}
.ds-row{display:flex;flex-wrap:wrap;gap:var(--space-2);align-items:center;margin:0 0 var(--space-4)}
nav.tabs.ds-sample{position:static;left:auto;right:auto;bottom:auto;margin:0 auto var(--space-3);view-transition-name:none}
[data-theme=light].card{color:var(--color-text)}
.ds-map{height:72px;margin:0 0 12px;border-radius:var(--radius-card);background:var(--color-map)}
.ds-sheet{margin-top:12px;background:var(--color-sheet);border:1px solid var(--color-sheet-border);border-radius:var(--radius-overlay) var(--radius-overlay) 0 0;padding:0 8px 8px}
.ds-sheet .grab{position:relative}
.card .m{margin-top:8px}
</style>
<h1>Regulars</h1>
<p class="t2">Fonts, colors, spacing, and radius change in regulars/foundation.css.</p>
<h2>Type</h2>
<div class=card>
<p style="font-size:var(--type-title-1-size);font-weight:var(--type-title-1-weight);letter-spacing:var(--type-title-1-tracking)">Title</p>
<p>Body. The default reading size.</p>
<p class="t3 sm">Caption and meta.</p>
</div>
<h2>Color</h2>
<div class=ds-swatches>
<div><div class=ds-swatch style="background:var(--color-bg)"></div><div class=ds-name>Background</div></div>
<div><div class=ds-swatch style="background:var(--color-surface)"></div><div class=ds-name>Surface</div></div>
<div><div class=ds-swatch style="background:var(--color-primary)"></div><div class=ds-name>Primary</div></div>
<div><div class=ds-swatch style="background:var(--color-status-cleared)"></div><div class=ds-name>Cleared</div></div>
<div><div class=ds-swatch style="background:var(--color-status-attention)"></div><div class=ds-name>Attention</div></div>
<div><div class=ds-swatch style="background:var(--color-status-not-cleared)"></div><div class=ds-name>Not cleared</div></div>
</div>
<h2>Buttons and chips</h2>
<p class="t3 sm">One primary in a group. Tertiary is the quiet action. Loading hides the label.</p>
<div class=ds-row>
<button type=button class="btn btn-primary">Primary</button>
<button type=button class="btn btn-secondary">Secondary</button>
<button type=button class="btn btn-tertiary">Tertiary</button>
<button type=button class="btn btn-danger">Destructive</button>
<button type=button class="btn btn-primary" disabled>Disabled</button>
<button type=button class="btn btn-primary" aria-busy=true>Saving</button>
</div>
<h2>Page header</h2>
<p class="t3 sm">Management pages use Title 1, a ghost action on the right, then an optional Body 2 subtitle. A back control returns to Manage. The gap below the block is --space-4.</p>
{% call admin_page('People', 'One line in secondary text.') %}<a class="btn quiet pageact" href="#">Export CSV</a>{% endcall %}
<h2>Filter chips</h2>
<p class="t3 sm">Lime when selected, outlined when not. Sibling views (Chat, Admin, Profile) use the same pill, one at a time.</p>
<div class=ds-row>
<span class="chip on">Selected</span>
<span class=chip>Open</span>
</div>
<h2>Status chips</h2>
<div class=ds-row>
<span class="st st-ok">Cleared</span>
<span class="st st-warn">Expiring soon · expires in 3 days</span>
<span class="st st-bad">Not cleared</span>
<span class="chip-info warn">Expiring</span>
<span class="chip-info bad">Blocked</span>
</div>
<h2>Navigation</h2>
<p class="t3 sm">One pill. Members get three circles. Coaches and admins get four. The fourth is Manage. Icons only. The selected circle is Electric Lime.</p>
""" + _ds_nav("Member navigation", ("home", "lineup", "chat")) + _ds_nav("Coach navigation", ("home", "lineup", "chat", "manage")) + """
<h2>Manage rows</h2>
<p class="t3 sm">Grouped list rows on a raised surface. A leading icon, a title, one line of description, a count only when it is above zero, and a trailing chevron. A pending Requests count is the info badge. A Compliance count is the warning badge.</p>
<div class=mgroup><h2>Activities</h2><div class=mlist>
{{ manage_row('/manage', 'Schedule', 'Practices, scrimmages & games', '<svg width="20" height="20" viewBox="0 0 256 256" fill="currentColor" aria-hidden="true"><path d="M208,32H184V24a8,8,0,0,0-16,0v8H88V24a8,8,0,0,0-16,0v8H48A16,16,0,0,0,32,48V208a16,16,0,0,0,16,16H208a16,16,0,0,0,16-16V48A16,16,0,0,0,208,32ZM72,48v8a8,8,0,0,0,16,0V48h80v8a8,8,0,0,0,16,0V48h24V80H48V48ZM208,208H48V96H208V208Z"/></svg>', 0) }}
{{ manage_row('/manage', 'Requests', 'Member-submitted events', '<svg width="20" height="20" viewBox="0 0 256 256" fill="currentColor" aria-hidden="true"><path d="M208,32H48A16,16,0,0,0,32,48V208a16,16,0,0,0,16,16H208a16,16,0,0,0,16-16V48A16,16,0,0,0,208,32Zm0,176H48V168H76.69a8,8,0,0,1,5.65,2.34l19.32,19.32a8,8,0,0,0,5.65,2.34h41.38a8,8,0,0,0,5.65-2.34l19.32-19.32a8,8,0,0,1,5.65-2.34H208Z"/></svg>', 2, 'info') }}
{{ manage_row('/manage', 'Compliance', 'Memberships & certifications', '<svg width="20" height="20" viewBox="0 0 256 256" fill="currentColor" aria-hidden="true"><path d="M208,40H48A16,16,0,0,0,32,56v56c0,52.72,25.52,84.67,46.93,102.19,23.06,18.86,46,25.26,47,25.53a8,8,0,0,0,4.2,0c1-.27,23.91-6.67,47-25.53C198.48,196.67,224,164.72,224,112V56A16,16,0,0,0,208,40Z"/></svg>', 5, 'warn') }}
</div></div>
<h2>Segmented</h2>
<p class="t3 sm">Same control as Exact dates / Month only. Figma role: Toggle group 73:2902.</p>
<div class=actseg role=radiogroup aria-label=Sample>
<label><input type=radio name=dsseg checked><span>Exact dates</span></label>
<label><input type=radio name=dsseg><span>Month only</span></label>
</div>
<h2>Field</h2>
<label>Field<input placeholder="Location"></label>
<h2>Upload</h2>
<p class="t3 sm">One field for images and files. The dashed area is the control. An image fills the zone. A file shows its name and size. Replace and Remove sit on either one.</p>
{{ upload_field('ds_image') }}
<div style="height:12px"></div>
{{ upload_field('ds_file', 'file', 'CSV', '.csv,.xlsx') }}
<h2>Card and RSVP</h2>
<div class=card>
<div class=nxtitle>Practice</div>
<p class=t2>7:00 – 8:30 PM</p>
<p class="t3 sm">Marina High School</p>
<div class=pills>
{{ rsvp_btn('Going', true, 'going') }}
{{ rsvp_btn('Not going', false, 'notgoing') }}
</div>
</div>
<p class="t3 sm">Disabled</p>
<div class=ds-row><button type=button class="btn btn-primary" disabled>Primary</button></div>
<h2>Date and time</h2>
<p class="t3 sm">A centered dialog, the same one as Schedule and every date or time field. Schedule ghosts days with no events and shows a dot. Form calendars leave every day selectable. Time is a clock. Cancel and OK confirm.</p>
<div class="sheet" style="border:1px solid var(--color-sheet-border);border-radius:var(--radius-overlay);padding:20px 12px 8px;background:var(--color-sheet)">
<div class=matkicker>Select date</div>
<div class=matheadline>Tue, Nov 3</div>
<div class=calhead><button type=button class=calmonth aria-label="Previous month"><svg width="20" height="20" viewBox="0 0 256 256" fill="currentColor" aria-hidden="true"><path d="M165.66,202.34a8,8,0,0,1-11.32,11.32l-80-80a8,8,0,0,1,0-11.32l80-80a8,8,0,0,1,11.32,11.32L91.31,128Z"/></svg></button><div class=lbl>November 2026</div><button type=button class=calmonth aria-label="Next month"><svg width="20" height="20" viewBox="0 0 256 256" fill="currentColor" aria-hidden="true"><path d="M181.66,133.66l-80,80a8,8,0,0,1-11.32-11.32L164.69,128,90.34,53.66a8,8,0,0,1,11.32-11.32l80,80A8,8,0,0,1,181.66,133.66Z"/></svg></button></div>
<div class=calwd><span>S</span><span>M</span><span>T</span><span>W</span><span>T</span><span>F</span><span>S</span></div>
<div class=calgrid><span class=calday></span><span class="calday past" aria-disabled=true>1</span><button type=button class="calday on">3</button><button type=button class=calday>4<i class=caldot></i></button></div>
<div class=matactions><button type=button class=mattext>Cancel</button><button type=button class=mattext>OK</button></div>
</div>
<h2>Map, chat, and sheet</h2>
<p class="t3 sm">Dark is the app. Light uses the same components.</p>
<div class=card>
<div class=ds-map aria-hidden=true></div>
<div class=m><div class=txt>See you at the pool.</div></div>
<div class="m mine"><div class=txt>I'll be there.</div></div>
<div class=ds-sheet><span class=grab aria-hidden=true></span><div class=actgroup><button type=button class=actrow>Reply</button></div></div>
</div>
<h2>Light</h2>
<div class=card data-theme=light>
<p style="font-weight:650">Same components, light surfaces.</p>
<div class=ds-map aria-hidden=true></div>
<div class=m><div class=txt>See you at the pool.</div></div>
<div class=ds-sheet><span class=grab aria-hidden=true></span><div class=actgroup><button type=button class=actrow>Reply</button></div></div>
<button type=button class="btn btn-primary">Primary</button>
</div>
"""
