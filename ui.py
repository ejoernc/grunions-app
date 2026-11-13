"""Templates (Jinja strings) for the Grunions app. Restrained dark UI: one surface, gray text, one blue accent.

Colors, type, spacing, and radius are defined in regulars/foundation.css.
"""
import os
_FOUNDATION_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "regulars", "foundation.css")
with open(_FOUNDATION_PATH, encoding="utf-8") as _foundation_file:
    FOUNDATION = _foundation_file.read()
BASE = """<!doctype html><html lang=en data-theme="{{ ui_theme or 'dark' }}" style="background:var(--ink)"><head>
<meta charset=utf-8><meta name=grunions-build content="{{ build_id }}"><meta name=color-scheme content="{{ 'light dark' if ui_theme == 'system' else (ui_theme or 'dark') }}"><meta name=theme-color content="#0B0B0C">
<meta name=viewport content="width=device-width,initial-scale=1,viewport-fit=cover">
<meta name=apple-mobile-web-app-capable content=yes><meta name=apple-mobile-web-app-title content=Regulars>
<link rel=manifest href=/manifest.webmanifest?v=118>
<link rel=icon href=/static/regulars-logo.svg?v=118 type=image/svg+xml>
<link rel=apple-touch-icon href=/static/icons/apple-touch-icon-180.png?v=119>
<link rel=apple-touch-startup-image href=/static/splash/splash-1170x2532.png?v=118 media="screen and (device-width: 390px) and (device-height: 844px) and (-webkit-device-pixel-ratio: 3) and (orientation: portrait)">
<link rel=apple-touch-startup-image href=/static/splash/splash-1284x2778.png?v=118 media="screen and (device-width: 428px) and (device-height: 926px) and (-webkit-device-pixel-ratio: 3) and (orientation: portrait)">
<link rel=apple-touch-startup-image href=/static/splash/splash-1125x2436.png?v=118 media="screen and (device-width: 375px) and (device-height: 812px) and (-webkit-device-pixel-ratio: 3) and (orientation: portrait)">
<link rel=apple-touch-startup-image href=/static/splash/splash-1242x2688.png?v=118 media="screen and (device-width: 414px) and (device-height: 896px) and (-webkit-device-pixel-ratio: 3) and (orientation: portrait)">
<link rel=apple-touch-startup-image href=/static/splash/splash-828x1792.png?v=118 media="screen and (device-width: 414px) and (device-height: 896px) and (-webkit-device-pixel-ratio: 2) and (orientation: portrait)">
<link rel=apple-touch-startup-image href=/static/splash/splash-750x1334.png?v=118 media="screen and (device-width: 375px) and (device-height: 667px) and (-webkit-device-pixel-ratio: 2) and (orientation: portrait)">
<link rel=apple-touch-startup-image href=/static/splash/splash-1290x2796.png?v=118 media="screen and (device-width: 430px) and (device-height: 932px) and (-webkit-device-pixel-ratio: 3) and (orientation: portrait)">
<link rel=apple-touch-startup-image href=/static/splash/splash-1179x2556.png?v=118 media="screen and (device-width: 393px) and (device-height: 852px) and (-webkit-device-pixel-ratio: 3) and (orientation: portrait)">
<link rel=apple-touch-startup-image href=/static/splash/splash-1206x2622.png?v=118 media="screen and (device-width: 402px) and (device-height: 874px) and (-webkit-device-pixel-ratio: 3) and (orientation: portrait)">
<link rel=apple-touch-startup-image href=/static/splash/splash-1320x2868.png?v=118 media="screen and (device-width: 440px) and (device-height: 956px) and (-webkit-device-pixel-ratio: 3) and (orientation: portrait)">
<title>Regulars</title>
<style>{{ foundation_css|safe }}
html,body{background:var(--color-bg);color:var(--color-text)}html{color-scheme:dark}html[data-theme=light]{color-scheme:light}@media (prefers-color-scheme: light){html[data-theme=system]{color-scheme:light}}
html:has(#chat),body:has(#chat){height:100dvh;overflow:hidden}
body:has(#chat){display:flex;flex-direction:column}
body:has(#chat) main{flex:1;min-width:0;width:100%;max-width:640px;min-height:0;display:flex;flex-direction:column;overflow:hidden;padding:8px var(--space-5) 0}
@view-transition{navigation:none}
::view-transition{display:none;background:var(--ink)}
::view-transition-group(root){animation:none;background:var(--ink)}
::view-transition-image-pair(root){isolation:auto}
::view-transition-old(root),::view-transition-new(root){animation:none;animation-duration:0s;mix-blend-mode:normal}
::view-transition-group(grunions-nav),::view-transition-old(grunions-nav),::view-transition-new(grunions-nav){animation:none;mix-blend-mode:normal}
#boot{position:fixed;top:0;left:0;right:0;height:100dvh;z-index:80;display:flex;align-items:center;justify-content:center;background:var(--ink);overflow:hidden;isolation:isolate;transition:opacity .7s ease}
#boot.gone{opacity:0;pointer-events:none}
#boot .mark{width:calc(186px * 0.97);height:calc(186px * 0.97 * 360 / 726);flex:none;line-height:0;transform:translateY(calc((env(safe-area-inset-bottom) - env(safe-area-inset-top)) / 2 - 12px))}
#boot video,#boot .bootstill{width:calc(186px * 0.97);height:calc(186px * 0.97 * 360 / 726);display:block;margin:0;object-fit:fill;object-position:center;background:transparent;aspect-ratio:726/360}
#boot .bootstill{display:none}
#boot.bootstill video{display:none}
#boot.bootstill .bootstill{display:block}
html.booted #boot{display:none}
@media (prefers-reduced-motion:reduce){ #boot{transition:opacity .45s ease}#boot video{display:none}#boot .bootstill{display:block}}
[hidden]{display:none!important}
*{box-sizing:border-box}html{-webkit-text-size-adjust:100%}
body{margin:0;background:var(--color-bg);color:var(--t1);font:var(--type-body-1-size)/var(--type-body-1-leading) var(--font-sans);overflow-wrap:break-word}
a{color:var(--t1)}main{max-width:640px;margin:0 auto;padding:20px 20px calc(var(--nav-clear) + 32px + env(safe-area-inset-bottom))}
header{display:flex;align-items:center;justify-content:space-between;padding:16px 20px;max-width:640px;margin:0 auto}
.brand{font-family:var(--font-display);font-weight:700;letter-spacing:-.02em;color:var(--t1);text-decoration:none}a.brand img{display:block;width:40px;height:40px;border-radius:10px}
img.loginlock{display:block;width:min(66%,calc(420px * 0.66));max-width:66%;height:auto;margin:8px 0 28px calc(-79 / 1338 * min(66%, 420px * 0.66));background:transparent}
body:has(img.loginlock)>header{display:none}header a.sub{color:var(--t3);font-size:14px;text-decoration:none}
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
.cardtitle{font-size:var(--type-t3-size);line-height:var(--type-t3-line);font-weight:var(--type-t3-weight)}
.nextcard .nxcardhead>.cardtitle{flex:1;min-width:0;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.nxchev{color:var(--t3);font-size:22px;line-height:1;flex:none}
.nxnote{margin-top:10px;color:var(--t3);font-size:13px;line-height:1.4}
.pills{display:flex;gap:var(--space-2);margin-top:var(--space-4)}
.pills > .btn,.pills > .sweep-host,.rsvprow > .btn,.rsvprow > .sweep-host{flex:1 1 0%;width:0;min-width:0;max-width:none}
.pills > .sweep-host,.rsvprow > .sweep-host{display:flex}
.pills > .sweep-host > .btn,.rsvprow > .sweep-host > .btn{flex:1 1 auto;width:100%;min-width:0;max-width:none;height:100%}
form:has(.sweep-host){position:relative;z-index:3}
.nextcard:has(.sweep-host),.card:has(.sweep-host),.tripcard:has(.sweep-host),
body.homefull .homedock .card:has(.sweep-host),body.homefull .schedlist .card:has(.sweep-host){overflow:visible;z-index:6}
.rsvprow{flex-wrap:nowrap}
.rsvprow .btn{white-space:nowrap;padding:0 8px;min-width:0}
.rsvpcheck{width:16px;height:16px;flex:none;display:block}
.pills .btn,.rsvprow .btn,.nxsocial .btn{flex-direction:row;flex-wrap:nowrap;align-items:center;justify-content:center;white-space:nowrap;transition:none}
.pills .btn,.rsvprow .btn{flex:1;min-width:0}
.nxsocial{display:flex;align-items:center;gap:12px}
.nxsocial>.cardlink,.nxsocial>a{flex:1 1 auto;min-width:0}
.nxsocial .grow{min-width:0}
.nxsocial .nxtitle,.nxsocial .t2{white-space:normal;overflow-wrap:anywhere}
.nxsocial>form,.nxsocial .sweep-host,.nxsocial .btn{flex:0 0 auto;width:auto;min-width:136px;max-width:none}
.nxsocial .btn{display:inline-flex;flex-direction:row;flex-wrap:nowrap;align-items:center;justify-content:center;white-space:nowrap;padding-left:16px;padding-right:16px}
.nxsocial .sweep-host{display:flex}
.nxsocial .sweep-host>.btn{width:100%;min-width:0;height:100%}
.pills button.on{background:var(--accent);color:var(--color-on-primary)}
.nxdiv{height:1px;background:var(--line);margin:14px 0}
.nxicon{width:40px;height:40px;border-radius:12px;background:var(--surface2);display:flex;align-items:center;justify-content:center;flex:none;color:var(--color-icon)}
.nxicon svg{display:block}
.joinpill{flex:none}
header.homehead{position:sticky;top:0;left:0;right:0;z-index:8;display:flex;width:100%;max-width:none;background:var(--color-bg);align-items:center;gap:var(--space-3);height:calc(76px + env(safe-area-inset-top));min-height:calc(76px + env(safe-area-inset-top));box-sizing:border-box;padding:calc(var(--space-4) + env(safe-area-inset-top)) var(--space-5) var(--space-4);border:0;box-shadow:none;outline:none;view-transition-name:none}
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
.nextcard .nxbody{padding:16px 16px 0}
.nextcard .nxcardhead .cardlink{flex:1;min-width:0}
a.usawpchip{display:inline-flex;align-items:center;gap:6px;margin-left:auto;color:var(--t2);font-size:13px;font-weight:500;line-height:1.2;text-decoration:none;white-space:nowrap;flex:none}
a.usawpchip .usawpok{width:16px;height:16px;flex:none;color:var(--color-status-cleared)}
a.usawpchip.warn,a.usawpchip.bad{color:var(--color-text)}
.numcard .nxtitle{font-size:17px;line-height:1.3}
#membership{scroll-margin-top:72px}
.pimg{position:relative;line-height:0;overflow:hidden}.pimg img{width:100%;height:200px;object-fit:cover;display:block}
.nextcard .pimg{border-top-left-radius:var(--radius-card);border-top-right-radius:var(--radius-card)}
.nxbadge{position:absolute;top:12px;left:12px;background:var(--color-surface);color:var(--color-text);border:1px solid var(--color-badge-border);border-radius:var(--radius-chip);padding:5px 10px;font-size:11px;font-weight:700;letter-spacing:.8px;line-height:1}
.nxrow{display:flex;align-items:center;gap:var(--space-2);margin-top:var(--space-2);color:var(--t1);font-size:15px}
.nxrow+.nxrow{margin-top:var(--space-meta)}
.nxglyph{width:16px;height:16px;flex:none;color:var(--color-icon)}
.nextcard .pills{margin:14px 16px 0}.nextcard .pills:last-child{margin-bottom:16px}
.nextcard .nxdiv{margin:14px 16px}.nextcard .nxsocial{padding:0 16px 16px}
.homemap{height:300px;margin:0 -20px 16px;background:var(--ink);position:relative;z-index:1}
.homemap.cardmap{height:220px;margin:0 0 12px;border-radius:14px;overflow:hidden;cursor:pointer;touch-action:pan-y}
.homemap.banner{height:220px;margin:0 -20px 0;border-radius:0;overflow:hidden;position:relative}
.homemap.banner::after{content:"";position:absolute;left:0;right:0;bottom:0;height:84px;background:linear-gradient(transparent,var(--color-bg));z-index:450;pointer-events:none}
.homemap.still{height:180px;margin:0;border-radius:0;cursor:default;pointer-events:none}
.homemap.still.tappable{pointer-events:auto;cursor:pointer}
.evhero{height:220px;margin:0 -20px 0;position:relative;overflow:hidden;background:var(--color-map)}
.evhero img{width:100%;height:100%;object-fit:cover;display:block}
.evhero::after{content:"";position:absolute;left:0;right:0;bottom:0;height:84px;background:linear-gradient(transparent,var(--color-bg));pointer-events:none}
.eventtag{color:var(--t2);font-size:15px;font-weight:400;margin:2px 0 0}
.profilehero .eventtag{text-align:center}
.loccard{padding:0}
a.locrow,span.locrow,div.locrow{display:flex;align-items:center;gap:12px;padding:14px 16px;color:inherit;text-decoration:none;width:100%}
.locrow .btn,.driverow .btn{flex:none;height:40px;min-height:40px;padding:0 12px;white-space:nowrap}
.locrow .t3{display:block;overflow-wrap:anywhere}
a.mapgo{width:100%}
.drivechip{position:relative;z-index:3;display:flex;justify-content:center;margin:0 0 10px}
.nexstack{position:relative;width:100%;min-width:0}
.nexstack>.drivechip{position:absolute;left:50%;bottom:calc(100% + 16px);transform:translateX(-50%);z-index:3;display:flex;justify-content:center;margin:0;max-width:100%;width:max-content;pointer-events:auto}
body.homefull .nexstack{pointer-events:none}
body.homefull .nexstack>.card{pointer-events:auto}
.drivechipbtn,.drivechiptext{margin:0;max-width:100%;border-radius:999px;background:var(--color-surface);color:var(--color-text);border:1px solid var(--color-border);box-shadow:0 6px 20px rgba(11, 11, 12,.35)}
button.drivechipbtn{height:36px;min-height:36px;padding:0 14px;font-size:13px;font-weight:650}
.drivechiptext{padding:8px 12px;font-size:13px;font-weight:650;line-height:1.3;white-space:normal;text-align:center}
a.drivechiptext{display:block;text-decoration:none;cursor:pointer;color:var(--color-text)}
.drivechiptext .driveage{font-weight:400;color:var(--color-text)}
.mpin .pinpill{position:relative;z-index:1}
.afterline{color:var(--color-lime);font-weight:650}
.li.evdescrow{flex-direction:column;align-items:stretch;gap:2px}
.li.evdescrow .textlink{align-self:flex-start;padding:4px 0 0}
.clamp{display:-webkit-box;-webkit-line-clamp:4;-webkit-box-orient:vertical;overflow:hidden}
.clamp.open{display:block;-webkit-line-clamp:unset}
a.reglink{color:var(--accent);text-decoration:none;font-weight:600}
.bannerprev{margin:0 0 10px;border-radius:var(--radius-card,14px);overflow:hidden;background:var(--surface);aspect-ratio:3/2}
.bannerprev img{width:100%;height:100%;object-fit:cover;display:block}
.bannerpick .btn{position:relative;overflow:hidden}
body.practicepage main{padding-top:0}
.mapboxgl-ctrl-bottom-right{margin:0 6px 6px 0;z-index:460}
.mapboxgl-ctrl-logo{opacity:.5;transform:scale(.62);transform-origin:right bottom;margin:0;cursor:pointer}
.mapattrib{position:fixed;z-index:40;margin:0;padding:5px 8px;background:var(--carbon);border-radius:8px;font-size:10px;line-height:1.2;white-space:nowrap;box-shadow:0 4px 16px rgba(11, 11, 12,.35)}
.mapattrib a{color:rgba(246, 244, 239,.72);text-decoration:none}
.mapattrib a+a{margin-left:8px}
body.homefull .homemap .mapboxgl-ctrl-bottom-right{position:absolute;right:6px;left:auto;bottom:var(--map-attrib,12px);margin:0;pointer-events:auto;z-index:460}
body.homefull .homemap .mpin{pointer-events:auto;cursor:pointer}
body.homefull .homemap .mpin.you{pointer-events:none;cursor:default}
.pinrow{display:flex;align-items:center;gap:6px;height:18px;width:max-content}
.pinhold{width:18px;height:18px;display:flex;align-items:center;justify-content:center;flex:none}
.pindot{display:block;width:18px;height:18px;box-sizing:border-box;border-radius:50%;background:var(--color-lime);border:3px solid var(--color-bg);box-shadow:0 0 0 1px var(--color-lime)}
.mpin.social .pindot{width:12px;height:12px;background:var(--color-lime);border:0;box-shadow:none}
.youdot{display:block;width:10px;height:10px;border-radius:50%;background:rgba(246, 244, 239,.9);box-shadow:0 0 0 6px rgba(246, 244, 239,.18)}
.pinpill{background:var(--carbon);color:var(--paper);border-radius:999px;padding:3px 8px;font-size:12px;font-weight:650;line-height:1.2;white-space:nowrap}
.routeline{stroke:var(--color-lime)}
body.homefull header.homehead{position:sticky;top:0;z-index:8;background:transparent}
body.homefull header.homehead.solid{background:var(--color-bg)}
body.homefull main{position:relative;z-index:1;padding:0 16px calc(var(--nav-clear) + 16px + env(safe-area-inset-bottom));pointer-events:none}
body.schedopen main{padding-bottom:calc(var(--nav-clear) + 80px + env(safe-area-inset-bottom))}
body.homefull .homemap{position:fixed;top:0;left:0;right:0;bottom:0;height:auto;margin:0;z-index:0;border-radius:0;pointer-events:none;touch-action:auto;background:var(--ink)}
body.homefull .homedock{position:relative;left:auto;right:auto;bottom:auto;z-index:2;max-height:none;overflow:visible;pointer-events:none;margin:0;padding:0 0 12px;min-height:calc(100dvh - var(--homehead, 76px) - var(--homealerts, 0px) - var(--nav-clear) - env(safe-area-inset-bottom) - var(--peek, 24px));display:flex;flex-direction:column;justify-content:flex-end;gap:12px}
body.schedopen .homedock{min-height:0;justify-content:flex-start}
body.homefull .homealerts,body.homefull .homedock .card,body.homefull .schedlist .card{position:relative;z-index:4;pointer-events:auto}
body.homefull .schedlist{position:relative;z-index:2}
.schedsame{display:none}
.schedfeed{display:flex;flex-direction:column;gap:24px}
body.homefull .schedfeed{position:relative;z-index:2;pointer-events:auto}
body.schedhome{overflow:hidden;height:100dvh;--drawer-h:52dvh}
body.schedhome header.homehead{height:0;min-height:0;padding:0;overflow:hidden;background:transparent}
body.schedhome main{overflow:hidden;height:100dvh;max-height:100dvh;padding-bottom:0}
body.schedhome .weekhi{--titlefade:0;position:fixed;z-index:4;top:16px;left:calc(var(--rail-w, 0px) + 16px);right:72px;pointer-events:none;color:var(--paper)}
/* 04.01: as the sheet rises, Hi → Upcoming crossfade in place at the same size, the map fades to the page color,
   and the cards slide up behind a solid header. --mapfade is the same 0→1 progress, set on body. */
body.schedhome .weekhi::before{content:"";position:fixed;z-index:-1;left:0;right:0;top:0;height:calc(80px + env(safe-area-inset-top));background:var(--ink);opacity:var(--mapdone, 0);pointer-events:none}
body.schedhome .homemap,body.schedhome .mapcontrols{opacity:calc(1 - var(--mapfade, 0))}
body.schedhome .weekdrawer{background:color-mix(in srgb, var(--ink) calc(var(--mapfade, 0) * 100%), var(--carbon));border-radius:calc(32px * (1 - var(--sheetp, 0))) calc(32px * (1 - var(--sheetp, 0))) 0 0}
body.schedhome .weekbody{padding-top:calc(var(--sheetp, 0) * 64px)}
body.schedhome .sheetgrab{opacity:calc(1 - var(--sheetp, 0))}
body.schedhome .weekeye{display:block;min-height:12px;font:600 12px/1 var(--r2-font-sans);letter-spacing:.04em;color:var(--paper);opacity:calc(1 - var(--titlefade))}
body.schedhome .weekhi .titlecross{display:grid;align-items:end}
body.schedhome .weekhi .titlecross>h1{grid-area:1/1;margin:4px 0 0}
body.schedhome .weekhi h1{font:700 40px/1.05 var(--r2-font-display);letter-spacing:-.04em;white-space:nowrap}
body.schedhome .weekhi .hititle{opacity:calc(1 - var(--titlefade))}
body.schedhome .weekhi h1.schedtitle{opacity:var(--titlefade);transform:none}
body.schedhome .weekhi .maplegend{position:static;display:flex;gap:10px;margin-top:10px;width:auto;opacity:calc(1 - var(--titlefade));max-height:24px;overflow:hidden}
.weekdrawer{position:fixed;z-index:3;left:0;right:0;bottom:0;height:var(--drawer-h);pointer-events:auto;display:flex;flex-direction:column;gap:8px;margin:0;padding:8px 16px 0;overflow:hidden;color:var(--paper);background:var(--carbon);border-radius:32px 32px 0 0}
.weekdrawer.peek .weekthis>*:not(.r2-drive){display:none}
.weekthis{display:flex;flex-direction:column;gap:12px;min-height:0}
.weekdrawer.full{border-radius:0}


body.schedhome:has(.weekdrawer.full) .homemap{opacity:0}
@media (max-width:767px){
 body.schedhome .weekdrawer,body.schedhome .weekdrawer .weekbody{touch-action:none}
 body.schedhome .weekdrawer:not(.full) .weekbody{overflow:hidden}
}
body.schedhome.sheetdrag{user-select:none}
.weekbody{flex:1;min-height:0;overflow-y:auto;overflow-anchor:none;display:flex;flex-direction:column;gap:12px;padding-bottom:0;-webkit-overflow-scrolling:touch}
/* A real spacer, not padding: scroll containers that are flex columns drop bottom padding, which left
   View full schedule under the nav. */
.weekbody>*{flex-shrink:0}  /* children must not squash: .weekthis was shrinking, so the list never got taller than the sheet */
.weekbody::after{content:"";flex:none;height:calc(var(--nav-clear) + 16px + env(safe-area-inset-bottom))}
.weekhead{display:flex;align-items:baseline;justify-content:space-between;gap:12px}
.weekhead h2{margin:0;font:700 28px/1 var(--r2-font-display);letter-spacing:-.03em}
.weekhead h2 span{color:var(--smoke);font:700 16px/1 var(--r2-font-sans)}
.weekhead a{color:var(--lime);font:700 15px/1 var(--r2-font-sans);text-decoration:none}
.weekbody{display:flex;flex-direction:column;gap:12px}
.clearbanner{border-radius:24px;background:var(--team-tangerine);color:var(--ink);padding:16px 18px}
.clearbanner b{display:block;font:700 11px/1 var(--r2-font-sans);letter-spacing:.06em}
.clearbanner strong{display:block;margin-top:6px;font:700 22px/1.15 var(--r2-font-display)}
.clearbanner p{margin:6px 0 10px;font:600 13px/1.3 var(--r2-font-sans)}
.clearbanner a{display:inline-flex;align-items:center;min-height:40px;padding:0 14px;border-radius:999px;background:var(--ink);color:var(--paper);font:700 14px/1 var(--r2-font-sans);text-decoration:none}
.ridebtns{display:flex;gap:8px}
.ridebtns button{flex:1;min-height:48px;border:0;border-radius:999px;background:var(--graphite);color:var(--paper);font:700 15px/1 var(--r2-font-sans)}
.ridebtns button:first-child{background:var(--lime);color:var(--ink)}
.weekempty{border-radius:24px;background:var(--graphite);padding:16px 18px}
.weekempty span{font:700 11px/1 var(--r2-font-sans);letter-spacing:.06em;color:var(--smoke)}
.weekempty b{display:block;margin-top:8px;font:700 22px/1.15 var(--r2-font-display)}
.weekempty p{margin:6px 0 12px;color:var(--smoke);font:600 13px/1.3 var(--r2-font-sans)}
.weekempty a{display:inline-flex;align-items:center;min-height:40px;padding:0 14px;border-radius:999px;background:var(--lime);color:var(--ink);font:700 14px/1 var(--r2-font-sans);text-decoration:none}
.fullsched{display:flex;align-items:center;justify-content:center;min-height:52px;border-radius:999px;border:1px solid var(--smoke);color:var(--paper);text-decoration:none;font:700 15px/1 var(--r2-font-sans)}
.fullhint{margin:0;text-align:center;color:var(--smoke);font:600 12px/1 var(--r2-font-sans)}
.socialcond{display:flex;align-items:center;gap:12px;min-height:60px;padding:10px 12px;border-radius:20px;background:var(--team-bubblegum);color:var(--ink)}
.socialcond b{display:block;font:700 11px/1.2 var(--r2-font-sans);letter-spacing:.03em}
.socialcond span span{display:block;margin-top:2px;font:700 15px/1.2 var(--r2-font-sans)}
.socialcond small{display:block;font:600 12px/1.2 var(--r2-font-sans)}
.socialcond button{border:0;border-radius:999px;min-height:36px;padding:0 14px;background:var(--paper);color:var(--ink);font:700 14px/1 var(--r2-font-sans)}
.evcard2.sky{background:var(--team-sky)}
.yougo.datechip{background:var(--ink);color:var(--paper)}
.mapcontrols{position:fixed;z-index:2;right:16px;bottom:calc(var(--drawer-h) + 16px);display:flex;flex-direction:column;gap:8px;pointer-events:auto}
.mapcontrols button{width:44px;height:44px;border:0;border-radius:999px;background:var(--graphite);color:var(--paper);font:700 22px/1 var(--r2-font-sans);box-shadow:none}
body.schedhome:has(.weekdrawer.full) .mapcontrols,body.schedhome.mapcovered .mapcontrols{display:none}
.ridechips{display:flex;gap:8px;margin:8px 0 12px}
.ridechips button{border:0;border-radius:999px;padding:8px 12px;background:var(--graphite);color:var(--paper);font:700 13px/1 var(--r2-font-sans)}
.ridechips button.on{background:var(--lime);color:var(--ink)}
.ridearea{margin:0 0 8px;padding:14px 16px;border-radius:16px;background:var(--graphite);font:700 16px/1.2 var(--r2-font-sans)}
.ridek{margin:8px 0 4px;color:var(--smoke);font:700 11px/1 var(--r2-font-sans);letter-spacing:.06em}
.rideback{display:flex;align-items:center;justify-content:space-between;gap:12px;margin:0 0 12px}
.rideback small{display:block;color:var(--smoke);font:600 12px/1.2 var(--r2-font-sans)}
.rideon{color:var(--lime);font:700 14px/1 var(--r2-font-sans)}
.rideback input{position:absolute;opacity:0}
.previewstates{margin:8px 0 0;color:var(--smoke);font:600 12px/1.4 var(--r2-font-sans)}
.previewstates a{color:var(--lime);text-decoration:none}
@media (min-width:768px){
 body.schedhome .weekdrawer{top:16px;right:16px;bottom:16px;left:auto;width:420px;height:auto;border-radius:28px}
 body.schedhome .weekdrawer.peek .weekthis>*:not(.r2-drive){display:block}
 body.schedhome .weekdrawer.peek .weekthis>*{display:flex}
 body.schedhome .weekdrawer.full{top:16px;border-radius:28px}
 body.schedhome .weekdrawer.full .weekbody{padding-top:0}
 body.schedhome.mapcovered .mapcontrols{display:flex}
 body.schedhome .mapcontrols{top:24px;bottom:auto;right:452px;display:flex}
}
@media (min-width:1280px){
 body.schedhome .weekdrawer{width:440px;right:24px}
 body.schedhome .mapcontrols{right:480px;top:24px;bottom:auto}
}
body.schedhome .schedsheet.up{margin-top:12px}
body.schedhome .sheetgrab{display:block;flex:none;width:100%;height:22px;margin:0;padding:0;border:0;border-radius:0;background:transparent;position:relative}
body.schedhome .sheetgrab::after{content:"";position:absolute;left:50%;top:8px;width:40px;height:5px;margin-left:-20px;border-radius:3px;background:var(--smoke)}
body.schedhome .sheetexpanded{display:none}
body.schedhome .schedsheet.up .sheetcollapsed{display:none}
body.schedhome .schedsheet.up .sheetexpanded{display:flex;flex-direction:column;gap:12px}
.sheettopline{display:flex;align-items:center;justify-content:space-between;gap:12px}
.sheettopline h2{margin:0;font:700 28px/1 var(--r2-font-display);letter-spacing:-.03em}
.sheettopline a,.sheettopline button{border:0;background:transparent;color:var(--lime);font:700 14px/1 var(--r2-font-sans);text-decoration:none}
.maplegend{position:fixed;z-index:2;top:16px;left:16px;right:16px;display:flex;gap:10px;align-items:center;color:var(--paper);font:600 12px/1 var(--r2-font-sans);pointer-events:none}
.maplegend i{display:inline-block;width:14px;height:3px;margin-right:4px;border-radius:2px;vertical-align:middle}
.maplegend .legclear{background:var(--lime)}.maplegend .legslow{background:var(--team-sun)}.maplegend .legjam{background:var(--team-tangerine)}
.maplegend b,.mappinchip{margin-left:auto;padding:6px 10px;border-radius:999px;background:var(--carbon);font:600 12px/1 var(--r2-font-sans)}
.mappinchip{position:fixed;z-index:2;top:16px;right:16px;margin:0;color:var(--paper);pointer-events:none}
body.schedhome .mappinchip{opacity:calc(1 - var(--mapfade, 0))}
.mapmiss{position:relative;z-index:3;margin:24px 16px 0;color:var(--paper);pointer-events:auto}
.mapmiss a{color:var(--lime)}
.socialcard{border-radius:32px;background:var(--team-bubblegum);color:var(--ink);padding:18px 18px 16px}
.socialtop{display:flex;align-items:center;justify-content:space-between;gap:8px}
.socialcard .socialkicker{font:700 11px/1.2 var(--r2-font-sans);letter-spacing:.04em}
.till{display:inline-flex;align-items:center;gap:4px;padding:4px 8px;border-radius:999px;background:var(--ink);color:var(--lime);font:700 12px/1 var(--r2-font-sans);flex:none}
.till i{width:8px;height:8px;border-radius:999px;background:var(--lime);font-style:normal}
.socialcard b{display:block;margin-top:10px;font:700 40px/.95 var(--r2-font-display);letter-spacing:-.04em}
.socialcard p,.socialcard small{display:block;margin:6px 0 0;font:600 14px/1.3 var(--r2-font-sans)}
.socialwho{display:flex;align-items:center;gap:6px;margin-top:12px;font:700 14px/1.2 var(--r2-font-sans)}
.socialwho i{width:28px;height:28px;border-radius:999px;display:inline-flex;align-items:center;justify-content:center;background:var(--ink);color:var(--team-bubblegum);font:700 10px/1 var(--r2-font-sans);font-style:normal}
.socialacts{display:flex;gap:8px;margin-top:14px}
.socialacts form{flex:1;margin:0}
.socialgo,.socialdir{display:flex;align-items:center;justify-content:center;width:100%;min-height:48px;border-radius:999px;border:1.5px solid var(--ink);background:transparent;color:var(--ink);font:700 15px/1 var(--r2-font-sans);text-decoration:none}
.socialgo.on{background:var(--ink);color:var(--paper)}
.drivemain{position:relative}
.drivego{margin-left:auto;width:44px;height:44px;border-radius:999px;display:inline-flex;align-items:center;justify-content:center;background:var(--ink);color:var(--lime);font:700 18px/1 var(--r2-font-sans);flex:none}
.drivecard{border-radius:28px;background:var(--lime);color:var(--ink);padding:16px 18px}
.drivetop{display:flex;justify-content:space-between;align-items:center;font:700 11px/1 var(--r2-font-sans);letter-spacing:.06em}
.drivetop b{padding:6px 10px;border-radius:999px;background:var(--ink);color:var(--lime);letter-spacing:0}
.drivemain{display:flex;align-items:flex-end;gap:10px;margin-top:8px}
.drivemain strong{font:700 64px/.85 var(--r2-font-display);letter-spacing:-.05em}
.drivemain small{display:flex;flex-direction:column;gap:2px;padding-bottom:10px;font:600 13px/1.2 var(--r2-font-sans)}
.drivemain small i{font:700 12px/1 var(--r2-font-sans);font-style:normal;letter-spacing:.06em}
.mpin.mate{width:32px;height:32px;border-radius:999px;background:var(--team-sky);color:var(--ink);display:flex;align-items:center;justify-content:center;font:700 11px/1 var(--r2-font-sans)}
a.homecard{display:flex;align-items:center;gap:12px;padding:16px 18px;border-radius:28px;background:var(--team-sun);color:var(--ink);text-decoration:none}
a.homecard.scrimmage,a.homecard.game{background:var(--carbon);color:var(--paper)}
a.homecard.cancelled{background:var(--carbon);color:var(--smoke)}
a.homecard>b{font:700 36px/.9 var(--r2-font-display);letter-spacing:-.04em}
a.homecard span{flex:1;min-width:0}
a.homecard i{display:block;font:700 10px/1 var(--r2-font-sans);letter-spacing:.08em;font-style:normal}
a.homecard small{display:block;margin-top:4px;font:600 12px/1.2 var(--r2-font-sans)}
a.homecard em{font:700 28px/1 var(--r2-font-display);font-style:normal}
.kindpills{display:flex;gap:8px;overflow:auto}
.kindpills button{border:0;border-radius:999px;padding:8px 12px;background:var(--graphite);color:var(--paper);font:700 13px/1 var(--r2-font-sans);white-space:nowrap}
.kindpills button.on{background:var(--paper);color:var(--ink)}
.weekstrip{display:flex;gap:6px}
.weekstrip a{flex:1;display:flex;flex-direction:column;align-items:center;gap:4px;padding:8px 0;border-radius:16px;color:var(--smoke);text-decoration:none;font:700 11px/1 var(--r2-font-sans)}
.weekstrip a.on{background:var(--paper);color:var(--ink)}
.weekstrip b{font:700 16px/1 var(--r2-font-display)}
.homeday{margin:8px 0 0;color:var(--smoke);font:700 12px/1 var(--r2-font-sans);letter-spacing:.06em}
.segpill{display:flex;gap:4px;height:52px;padding:4px;border-radius:999px;background:var(--graphite);box-sizing:border-box}
.segpill a{flex:1;display:flex;align-items:center;justify-content:center;border-radius:999px;color:var(--paper);text-decoration:none;font:700 15px/1 var(--r2-font-sans)}
.segpill a.on{background:var(--paper);color:var(--ink)}
.anncard{border-radius:32px;background:var(--team-lavender);color:var(--ink);padding:20px 22px 22px}
.anncard b{display:block;font:700 10px/1.2 var(--r2-font-sans);letter-spacing:.08em}
.anncard p{margin:10px 0 0;font:700 15px/.95 var(--r2-font-display);letter-spacing:-.03em}
.daygroup{display:flex;gap:12px;align-items:flex-start}
.daygroup .dayrail{width:52px;padding-top:0}
.daygroup .dayrail span{font:700 10px/1 var(--r2-font-sans);letter-spacing:.08em;color:var(--smoke)}
.daygroup .dayrail b{margin-top:2px;font:700 40px/.95 var(--r2-font-display);letter-spacing:-.05em;color:var(--paper)}
.daycards{flex:1;min-width:0;display:flex;flex-direction:column}
.daycards>*+*{margin-top:-10px}
.evcard2,.evrow2,.evcancel{display:block;box-sizing:border-box;text-decoration:none;position:relative;cursor:pointer}
.evcard2{border-radius:40px;background:var(--team-sun);color:var(--ink);padding:24px;min-height:296px;display:flex;flex-direction:column;box-sizing:border-box}
.evrow2{display:flex;justify-content:space-between;gap:8px;border-radius:32px;background:var(--team-sun);color:var(--ink);padding:16px 72px 16px 20px;min-height:126px;box-sizing:border-box;position:relative}
.evcancel{border-radius:32px;background:var(--carbon);color:var(--paper);padding:20px 22px}
.evmeta{display:flex;justify-content:space-between;align-items:center;gap:8px;font:700 11px/1 var(--r2-font-sans);letter-spacing:.08em}
.yougo{display:inline-flex;align-items:center;gap:4px;padding:4px 8px;border-radius:999px;background:var(--ink);color:var(--lime);font:700 12px/1 var(--r2-font-sans);letter-spacing:0}
.evname{margin-top:12px;font:700 30px/1 var(--r2-font-display);letter-spacing:-.03em}
.evtime{display:flex;align-items:flex-end;gap:8px;margin-top:8px}
.evtime b{font:700 104px/.8 var(--r2-font-display);letter-spacing:-.07em}
.evtime span{display:flex;flex-direction:column;gap:2px;padding-bottom:10px;font:700 12px/1 var(--r2-font-sans);letter-spacing:.04em}
.evtime i{font-style:normal}
.evtime i:first-child{font:700 18px/1 var(--r2-font-display)}
.evfoot{display:flex;align-items:flex-end;gap:12px;margin-top:auto;padding-top:12px}
.evfootmain{display:flex;flex-direction:column;gap:6px;min-width:0;flex:1}
.evwho{display:flex;align-items:center;font:700 14px/1 var(--r2-font-sans)}
.evwho i{width:28px;height:28px;margin-left:-8px;border-radius:999px;display:inline-flex;align-items:center;justify-content:center;background:var(--ink);color:var(--team-sun);font:700 10px/1 var(--r2-font-sans);font-style:normal}
.evwho i:first-child{margin-left:0}
.evwho em{margin-left:8px;font-style:normal}
.evvenue{display:block;color:var(--ink);font:600 13px/1.2 var(--r2-font-sans)}
.evchev{margin-left:auto;width:44px;height:44px;border-radius:999px;display:inline-flex;align-items:center;justify-content:center;background:var(--ink);color:var(--lime);font:700 20px/1 var(--r2-font-sans);flex:none}
.evrow2 .evcap{display:block;font:700 10px/1 var(--r2-font-sans);letter-spacing:.08em}
.evrow2 b{display:block;margin-top:6px;font:700 24px/.95 var(--r2-font-display);letter-spacing:-.03em}
.evrow2 small{display:block;margin-top:8px;font:600 12px/1.2 var(--r2-font-sans)}
.evrow2 .evcount{position:absolute;right:18px;top:36px;display:flex;flex-direction:column;align-items:flex-end;gap:0;flex:none;background:transparent;border:0;height:auto;min-width:0;padding:0;border-radius:0;color:inherit}
.evrow2 .evcount b{margin:0;font:700 56px/.85 var(--r2-font-display);letter-spacing:-.06em}
.evrow2 .evcount span{font:700 10px/1 var(--r2-font-sans);letter-spacing:.08em}
.evrow2 .evcount i{position:absolute;top:-22px;right:0;font-style:normal;font:700 18px/1 var(--r2-font-sans)}
.cancelpill{padding:4px 8px;border-radius:999px;background:var(--team-tangerine);color:var(--ink);letter-spacing:0;font:700 11px/1 var(--r2-font-sans)}
.evcantitle{margin-top:10px;color:var(--smoke);font:700 36px/1 var(--r2-font-display);letter-spacing:-.03em}
.evcancel p{margin:8px 0 0;color:var(--paper);font:600 14px/1.3 var(--r2-font-sans)}
.schedrow{display:flex;gap:12px;align-items:flex-start;margin:0 0 12px}
.dayrail{width:52px;flex:none;padding-top:10px}
.dayrail span{display:block;color:var(--r2-smoke);font:700 11px/1 var(--r2-font-sans);letter-spacing:.04em}
.dayrail b{display:block;margin-top:4px;color:var(--r2-paper);font:700 28px/1 var(--r2-font-display)}
.schedrow>.card{flex:1;min-width:0;margin:0}
.calwhen,.calkinds{display:flex;flex-wrap:wrap;gap:6px;margin:0 0 10px}
.calwhen a,.calkinds a{display:inline-flex;align-items:center;height:28px;padding:0 10px;border-radius:999px;background:var(--r2-graphite);color:var(--r2-paper);font:700 12px/1 var(--r2-font-sans);text-decoration:none}
.calwhen a.on,.calkinds a.on{background:var(--r2-paper);color:var(--r2-fixed-ink)}
.calday{margin:16px 0 6px;color:var(--r2-smoke);font:700 11px/1 var(--r2-font-sans);letter-spacing:.08em}
.calrow{display:flex;align-items:center;gap:14px;min-height:76px;margin:0 0 8px;padding:12px 16px;border-radius:28px;background:var(--carbon);color:inherit;text-decoration:none}
.calrow b{display:block;font:700 15px/1.2 var(--r2-font-sans);color:var(--r2-paper)}
.calrow small{display:block;margin-top:2px;color:var(--r2-smoke);font:600 12px/1.2 var(--r2-font-sans)}
.calrow .go{margin-left:auto;color:var(--r2-smoke);font:700 16px/1 var(--r2-font-sans)}
a.practlink{display:flex;align-items:center;gap:12px;min-height:64px;margin:14px 0;padding:10px 14px 10px 10px;border-radius:26px;background:var(--r2-graphite);color:inherit;text-decoration:none}
a.practlink .mark{width:48px;height:48px;border-radius:999px;display:inline-flex;align-items:center;justify-content:center;background:var(--r2-sun);color:var(--r2-fixed-ink);font:700 18px/1 var(--r2-font-display);flex:none}
a.practlink b{display:block;font:700 15px/1.2 var(--r2-font-sans);color:var(--r2-paper)}
a.practlink small{display:block;margin-top:2px;color:var(--r2-smoke);font:600 12px/1.3 var(--r2-font-sans)}
.heldsocial{display:none !important}
body.practicepage:not(.editor) .profilehero,body.practicepage:not(.editor) .evhero,body.practicepage:not(.editor) .homemap.banner{display:none}
body.practicepage:not(.editor) .p5 .seclabel,body.practicepage:not(.editor) .p5>.list,body.practicepage:not(.editor) .p5 .sechead{display:none}
body.practicepage:not(.editor) .p5 .list.loccard{display:block}
.p5{display:flex;flex-direction:column;gap:20px;padding:0 0 24px}
.p5cover{margin:0 -16px;height:220px;overflow:hidden}
.p5cover img{width:100%;height:100%;object-fit:cover}
.p5hero{position:relative;display:flex;flex-direction:column;gap:14px;border-radius:40px;background:var(--team-sun);color:var(--fixed-ink);padding:22px 22px 24px}
.p5hero.off{background:var(--carbon);color:var(--paper)}
.p5over{font:700 10px/1.2 var(--r2-font-sans);letter-spacing:.08em;min-height:27px;display:flex;align-items:center;padding-right:110px}
.p5chip{position:absolute;top:22px;right:22px;padding:7px 12px;border-radius:999px;background:var(--fixed-ink);color:var(--fixed-paper);font:700 12px/1 var(--r2-font-sans)}
.p5hero.off .p5chip{background:var(--team-tangerine);color:var(--fixed-ink)}
.p5hero h2{margin:0;font:700 44px/.95 var(--r2-font-display);letter-spacing:-.05em}
.p5time{display:flex;align-items:flex-end;gap:10px;margin:0}
.p5time b{font:700 clamp(88px,30vw,120px)/.86 var(--r2-font-display);letter-spacing:-.05em}
.p5time span{display:flex;flex-direction:column;gap:2px;padding-bottom:12px;font:700 12px/1 var(--r2-font-sans)}
.p5time i:first-child{font:700 20px/.95 var(--r2-font-display)}
.p5time i{font-style:normal}
.p5venue{margin:0;font:700 15px/1.2 var(--r2-font-sans)}
.p5metrics{display:flex;gap:10px}
.p5metrics>.rg-metric{flex:1;min-width:0}
.p5rsvp{display:flex;gap:10px}
.p5rsvp .btn{flex:1;height:56px;border-radius:999px}
.p5rsvp .btn-primary{background:var(--lime);color:var(--ink)}
.p5rsvp .btn-secondary{background:var(--graphite);color:var(--paper);border:0}
.p5chat{display:flex;gap:8px}
.p5chat .practlink{flex:1;margin:0;min-height:56px;border-radius:999px;justify-content:center;background:var(--graphite)}
.p5more{width:56px;height:56px;border-radius:999px;display:flex;align-items:center;justify-content:center;background:var(--graphite);color:var(--paper);text-decoration:none}
.p5social{display:flex;align-items:center;gap:12px;min-height:64px;padding:12px 14px;border-radius:28px;background:var(--team-bubblegum);color:var(--ink)}
.p5social b{display:block;font:700 11px/1.2 var(--r2-font-sans);letter-spacing:.04em}
.p5social span{display:block;margin-top:4px;font:600 14px/1.2 var(--r2-font-sans)}
.p5social button{border:0;border-radius:999px;padding:8px 14px;background:var(--ink);color:var(--paper);font:700 13px/1 var(--r2-font-sans)}
.p5sec{margin:0;font:700 28px/.95 var(--r2-font-display);letter-spacing:-.03em;color:var(--paper)}
.p5person{display:flex;align-items:center;gap:14px;min-height:76px;margin-top:8px;padding:12px 16px 12px 12px;border-radius:28px;background:var(--carbon);color:var(--paper)}
.p5person .av{width:44px;height:44px;border-radius:999px;display:flex;align-items:center;justify-content:center;background:var(--graphite);font:700 14px/1 var(--r2-font-display)}
.p5person b{display:block;font:700 16px/1.2 var(--r2-font-sans)}
.p5person small{color:var(--smoke);font:600 12px/1.2 var(--r2-font-sans)}
.goingchip,.outchip{margin-left:auto;padding:6px 10px;border-radius:999px;font:700 12px/1 var(--r2-font-sans)}
.goingchip{background:var(--lime);color:var(--ink)}
.outchip{background:var(--team-tangerine);color:var(--ink)}
.p5info{margin-top:8px;padding:16px 20px;border-radius:28px;background:var(--carbon)}
.p5info span{display:block;color:var(--smoke);font:700 11px/1 var(--r2-font-sans);letter-spacing:.06em}
.p5info b{display:block;margin-top:6px;font:600 16px/1.3 var(--r2-font-sans);color:var(--paper)}
.p5empty{color:var(--smoke)}
.newevent{margin:8px 0 18px;font:700 clamp(52px,14vw,72px)/.9 var(--r2-font-display);letter-spacing:-.045em}
.lanecard.on{background:var(--lime);color:var(--ink)}
body.editor header.profilebar{grid-template-columns:auto 1fr auto;padding:calc(8px + env(safe-area-inset-top)) 16px 0;background:var(--ink)}
body.editor header.profilebar a.profileact,body.editor header.profilebar button.profileact{height:40px;min-height:40px;padding:0 16px;border-radius:999px;background:var(--graphite);color:var(--paper)}
body.editor:not(.eventnew) header.profilebar button.savebtn{background:var(--lime);color:var(--ink)}
body.eventnew header.profilebar h1{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0,0,0,0)}
body.editor main,body.adminpage main{padding-bottom:calc(var(--nav-clear) + 88px + env(safe-area-inset-bottom))}
body.editor .lanepick{display:grid;grid-template-columns:1fr 1fr;gap:10px}
body.editor button.lanecard{min-height:132px;padding:16px;border:0;border-radius:28px;background:var(--graphite);color:var(--paper);box-shadow:none}
body.editor button.lanecard.on{background:var(--lime);color:var(--ink);border:0;box-shadow:none}
body.editor button.lanecard.on span,body.editor button.lanecard span{color:inherit;opacity:.8}
body.editor h2.planask,body.editor .fldlab{margin:18px 0 8px;font:700 11px/1 var(--r2-font-sans);letter-spacing:.08em;text-transform:uppercase;color:var(--smoke)}
body.editor .actseg{gap:8px;margin:0 0 16px;padding:0;background:transparent}
body.editor .actseg span{height:40px;min-height:40px;padding:0 14px;border-radius:999px;background:var(--graphite);color:var(--paper)}
body.editor #schedBlock .actseg input:checked+span,body.editor .hostseg input:checked+span,body.editor #whenPrec input:checked+span{background:var(--team-sun);color:var(--ink)}
body.editor #lineBlock .actseg input:checked+span,body.editor #eventForm .actseg input:checked+span{background:var(--team-lavender);color:var(--ink)}
body.editor .colordots{display:flex;gap:10px;margin:0 0 16px}
body.editor button.cdot{width:28px;height:28px;min-height:28px;padding:0;border-radius:999px;border:0;background:var(--c);box-shadow:0 0 0 2px var(--ink)}
body.editor button.cdot.on{box-shadow:0 0 0 2px var(--ink),0 0 0 4px var(--paper)}
body.editor .typechips{display:flex;flex-wrap:wrap;gap:8px;margin:-8px 0 16px}
body.editor .typechips button{height:40px;min-height:40px;padding:0 14px;border:0;border-radius:999px;background:var(--graphite);color:var(--paper)}
body.editor .typechips button.on{background:var(--team-lavender);color:var(--ink)}
body.editor label{font:700 11px/1.2 var(--r2-font-sans);letter-spacing:.08em;text-transform:uppercase;color:var(--smoke)}
body.editor label input,body.editor label select,body.editor label textarea,body.editor .livetitle{text-transform:none;letter-spacing:0;font:600 16px/1.3 var(--r2-font-sans);color:var(--paper)}
body.editor input:not([type=checkbox]):not([type=radio]):not([type=hidden]):not([type=file]),body.editor select,body.editor textarea.planfield{background:var(--carbon);border:0;border-radius:22px;min-height:56px;color:var(--paper)}
body.editor input.bad,body.editor button.setrow.bad{outline:2px solid var(--team-tangerine);outline-offset:0}
body.editor #exactWhen{display:grid;grid-template-columns:1fr 1fr;gap:10px;background:transparent;border:0}
body.editor #exactWhen .setrow{min-height:72px;border:0;border-radius:22px;background:var(--carbon);color:var(--paper);align-items:flex-start;flex-direction:column;padding:12px 14px}
body.editor #exactWhen .setrow[data-matfor=dateInput],body.editor #exactWhen #repeatRow,body.editor #exactWhen #freqRow,body.editor #exactWhen #endsRow,body.editor #exactWhen #skipRow{grid-column:1 / -1}
body.editor .livetitle{display:flex;align-items:center;justify-content:space-between;min-height:56px;margin:0 0 16px;padding:0 16px;border-radius:22px;background:var(--carbon)}
body.editor .plancards{flex-direction:row;align-items:stretch}
body.editor label.plancard{flex:1;min-height:132px;border:0;border-radius:28px;background:var(--graphite);color:var(--paper);box-shadow:none}
body.editor label.plancard .planmark{display:none}
body.editor label.plancard:has(input:checked){background:var(--team-lavender);color:var(--ink);border:0;box-shadow:none}
body.editor label.plancard:has(input:checked) .plantxt span{color:var(--ink)}
body.editor .signupopts{display:flex;flex-direction:column;gap:8px;margin:0 0 16px}
body.editor label.sigopt{display:flex;align-items:center;gap:12px;margin:0;padding:14px 16px;border-radius:22px;background:var(--carbon);text-transform:none;letter-spacing:0;color:var(--paper)}
body.editor label.sigopt b{display:block;font:700 16px/1.2 var(--r2-font-sans);text-transform:none;letter-spacing:0;color:var(--paper)}
body.editor label.sigopt small{display:block;color:var(--smoke);font:600 13px/1.3 var(--r2-font-sans);text-transform:none;letter-spacing:0}
body.editor label.sigopt:has(input:checked){box-shadow:inset 0 0 0 2px var(--lime)}
body.editor main .note{background:var(--team-tangerine);color:var(--ink);border:0;border-radius:22px;padding:14px 16px;font-weight:700}
body.editor .daypicks{display:flex;flex-wrap:wrap;gap:8px}
body.editor .daypicks label{margin:0;text-transform:none;letter-spacing:0}
body.editor .daypicks input{position:absolute;opacity:0;width:1px;height:1px}
body.editor .daypicks span{display:inline-flex;align-items:center;height:40px;padding:0 14px;border-radius:999px;background:var(--graphite);color:var(--paper);font:700 14px/1 var(--r2-font-sans)}
body.editor .daypicks input:checked+span{background:var(--team-sun);color:var(--ink)}
#grunionsDateDlg .calday.today{background:var(--lime);color:var(--ink);border-radius:999px}
#grunionsDateDlg .calday.on{box-shadow:inset 0 0 0 2px var(--lime);border-radius:999px;color:var(--paper)}
#grunionsDateDlg .calday.has{color:var(--team-sun)}
#grunionsDateDlg .callegend{display:flex;gap:16px;margin:8px 8px 4px;color:var(--smoke);font:600 12px/1 var(--r2-font-sans)}
#grunionsDateDlg .callegend i{display:inline-block;width:8px;height:8px;margin-right:6px;border-radius:999px;background:var(--lime)}
#grunionsDateDlg .callegend .practicedot{background:var(--team-sun)}
#grunionsDateDlg .matactions,#grunionsTimeDlg .matactions{display:flex;gap:10px}
#grunionsDateDlg .matactions button,#grunionsTimeDlg .matactions button{flex:1;height:52px;border-radius:999px;background:var(--graphite);color:var(--paper)}
#grunionsDateDlg #matDateOk,#grunionsTimeDlg #timeOk{background:var(--lime);color:var(--ink)}
/* Month mode (Nov 13): 2.0 segmented control for part of month; no day legend. */
#grunionsDateDlg:has(#matMonths:not([hidden])) .callegend,#grunionsDateDlg:not(:has(#matGrid .has)) .callegend{display:none}
#grunionsDateDlg .matpart{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:4px;margin:12px 0 4px;padding:4px;border-radius:999px;background:var(--carbon);flex-wrap:nowrap}
#grunionsDateDlg .matpart label{margin:0;min-width:0;text-transform:none;letter-spacing:0;font:inherit}
#grunionsDateDlg .matpart span{height:40px;min-height:0;padding:0 4px;border-radius:999px;background:transparent;color:var(--smoke);font:700 14px/1 var(--r2-font-sans);text-transform:none;letter-spacing:0;white-space:nowrap}
#grunionsDateDlg .matpart input:checked+span{background:var(--paper);color:var(--ink)}
/* Compact date picker: whole month fits without scrolling (Nov 13). */
#grunionsDateDlg .sheet{overflow:visible;padding:16px 12px 12px}
#grunionsDateDlg .matkicker{margin:0 8px 2px}
#grunionsDateDlg .matheadline{margin:0 8px 8px;font-size:1.5rem}
#grunionsDateDlg .calhead{margin:0 0 4px}
#grunionsDateDlg .calwd span{font-size:12px;line-height:28px}
#grunionsDateDlg .calgrid{gap:2px 0}
#grunionsDateDlg button.calday{height:40px!important;min-height:0!important;padding:0!important;margin:0;display:flex;align-items:center;justify-content:center;font-size:15px;line-height:1}
#grunionsDateDlg button.calday::before{display:none}
#grunionsDateDlg .calday.today,#grunionsDateDlg .calday.on{width:40px;justify-self:center}
#grunionsDateDlg .matactions{margin:8px 0 0}
#grunionsDateDlg .matactions button{height:44px;min-height:0}
.mseg{display:flex;gap:8px;flex-wrap:wrap;margin:0 0 4px}
.mseg .chip{background:var(--graphite);color:var(--paper);border:0;border-radius:999px}
.mseg .chip.on{background:var(--paper);color:var(--ink)}
.needban{display:flex;align-items:center;gap:12px;min-height:64px;margin:8px 0;padding:12px 12px 12px 16px;border-radius:999px;background:var(--team-tangerine);color:var(--ink);text-decoration:none}
.needban b{font:700 15px/1.2 var(--r2-font-sans)}
.needban em{margin-left:auto;padding:8px 14px;border-radius:999px;background:var(--ink);color:var(--paper);font:700 13px/1 var(--r2-font-sans);font-style:normal}
.wkrow{display:flex;align-items:center;gap:12px;min-height:76px;margin:0 0 10px;padding:14px 14px 14px 18px;border-radius:28px;background:var(--graphite);color:var(--paper);text-decoration:none}
.wkrow.sky{background:var(--team-sky);color:var(--ink)}
.wkrow b{display:block;font:700 16px/1.25 var(--r2-font-sans)}
.wkrow small{display:block;margin-top:2px;color:inherit;opacity:.75;font:600 13px/1.3 var(--r2-font-sans)}
.wkact{margin-left:auto;padding:8px 12px;border-radius:999px;background:var(--ink);color:var(--paper);font:700 13px/1 var(--r2-font-sans)}
.wkrow.sky .wkact{background:var(--ink);color:var(--paper)}
.wkadd{display:flex;align-items:center;justify-content:center;min-height:56px;margin:4px 0 12px;border-radius:999px;border:1.5px solid var(--smoke);color:var(--paper);text-decoration:none;font:700 15px/1 var(--r2-font-sans)}
.prow2{display:flex;align-items:center;gap:12px;min-height:76px;margin:0 0 10px;padding:14px 16px;border-radius:28px;background:var(--carbon);color:var(--paper);text-decoration:none}
.prow2 b{display:block;font:700 16px/1.2 var(--r2-font-sans)}
.prow2 small{display:block;color:var(--smoke);font:600 13px/1.3 var(--r2-font-sans)}
.stchip{margin-left:auto;padding:6px 10px;border-radius:999px;font:700 12px/1 var(--r2-font-sans)}
.stchip.tang{background:var(--team-tangerine);color:var(--ink)}
.stchip.lime{background:var(--lime);color:var(--ink)}
.stchip.ink{background:var(--graphite);color:var(--paper)}
a.mrow.mtile{min-height:96px;margin:0 0 10px;border:0;border-radius:28px;padding:18px 20px;color:var(--fixed-ink)}
a.mrow.mtile.sun{background:var(--team-sun)}a.mrow.mtile.sky{background:var(--team-sky)}a.mrow.mtile.tangerine{background:var(--team-tangerine)}a.mrow.mtile.lavender{background:var(--team-lavender)}a.mrow.mtile.lime{background:var(--lime)}a.mrow.mtile.aqua{background:var(--team-aqua)}a.mrow.mtile.mango{background:var(--team-mango)}a.mrow.mtile.bubblegum{background:var(--team-bubblegum)}a.mrow.mtile.carbon{background:var(--graphite);color:var(--paper)}
a.mrow.mtile .mico{display:none}
a.mrow.mtile .mtitle{font:700 26px/1.05 var(--r2-font-display);letter-spacing:-.03em;color:inherit}
a.mrow.mtile .mdesc{display:block;margin-top:4px;color:rgba(11,11,12,.72);font:600 13px/1.3 var(--r2-font-sans)}
a.mrow.mtile.carbon .mdesc{color:var(--smoke)}
a.mrow.mtile .tnum{margin-left:auto;font:700 40px/.9 var(--r2-font-display)}
a.mrow.mtile .mbadge{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0,0,0,0)}
a.mrow.mtile .mchev{margin-left:auto;color:inherit}
body.adminpage .pagehead h1{font:700 clamp(48px,14vw,72px)/.9 var(--r2-font-display);letter-spacing:-.04em}
body.adminpage .evcard{background:var(--team-sun);color:var(--ink);border-radius:32px;padding:18px 20px 16px}
body.adminpage .evcard .nxtitle,body.adminpage .evcard .t2,body.adminpage .evcard .t3{color:var(--ink)}
body.adminpage .chkhero{display:flex;align-items:flex-end;gap:10px;margin-top:8px}
body.adminpage .chkhero b{font:700 64px/.85 var(--r2-font-display);letter-spacing:-.04em}
body.adminpage .chkhero span{margin-bottom:8px;font:700 12px/1 var(--r2-font-sans);letter-spacing:.06em}
body.adminpage .checkfilt .chip{border:0;border-radius:999px;background:var(--graphite);color:var(--paper)}
body.adminpage .checkfilt .chip.on,body.adminpage .checkfilt .chip-active{background:var(--paper);color:var(--ink)}
.reqcard{margin:0 0 12px;padding:16px;border-radius:28px;background:var(--team-bubblegum);color:var(--ink)}
.reqcard.carbon{background:var(--carbon);color:var(--paper)}
.reqcard.carbon .btn-secondary{color:var(--paper);border-color:var(--paper)}
.reqcard a{color:inherit;text-decoration:none}
.reqcard b{font:700 22px/1.15 var(--r2-font-display)}
.reqpill{float:right;padding:6px 10px;border-radius:999px;background:var(--ink);color:var(--paper);font:700 12px/1 var(--r2-font-sans)}
.reqacts{display:flex;gap:8px;margin-top:12px}
.reqacts .btn{flex:1;border-radius:999px}
.reqacts .btn-primary{background:var(--ink);color:var(--paper)}
.reqacts .btn-secondary{background:transparent;color:var(--ink);border:1.5px solid var(--ink)}
.roleopt{display:flex;align-items:center;gap:12px;width:100%;min-height:72px;margin:0 0 8px;padding:12px 14px;border:0;border-radius:22px;background:var(--graphite);color:var(--paper);text-align:left}
.roleopt small{display:block;color:var(--smoke);font:600 13px/1.3 var(--r2-font-sans)}
.roleopt em{margin-left:auto;padding:6px 10px;border-radius:999px;background:var(--graphite);color:var(--paper);font:700 12px/1 var(--r2-font-sans);font-style:normal;border:1px solid var(--smoke)}
.roleopt.on{box-shadow:inset 0 0 0 1.5px var(--smoke)}
.roleopt.on em{background:var(--lime);color:var(--ink);border-color:transparent}
.coachmore{display:flex;flex-direction:column;gap:8px;margin-top:8px}
.coachmore a{color:var(--paper);text-decoration:none;font:700 16px/1.2 var(--r2-font-sans)}
#lineBlock:not([hidden]) ~ .lanepick .lanecard[data-lane=lineup],body .lanecard.on[data-lane=lineup]{background:var(--team-lavender);color:var(--ink)}
.btn-tangerine{background:var(--team-tangerine);color:var(--ink);border:0}
header.homehead .titlestack{position:relative;flex:1;min-width:0;height:44px;display:flex;flex-direction:column;align-items:flex-start;justify-content:center;gap:0}
header.homehead .titlecross{display:grid}
header.homehead .titlecross>h1{grid-area:1/1;margin:0}
header.homehead{--titlefade:0}
header.homehead .hititle{opacity:calc(1 - var(--titlefade))}
header.homehead .schedtitle{opacity:var(--titlefade)}
header.homehead .titlestack a.usawpchip{position:absolute;top:calc(100% + 2px);left:0;margin:0;opacity:calc(1 - var(--titlefade))}
header.homehead.titleaway .titlestack a.usawpchip{pointer-events:none}
body.schedopen header.homehead{--titlefade:1}
.nextcard .daychip{height:32px;margin:0 -8px 0 0;padding:0 11px;font-size:16px;align-self:center;flex:none}
body.schedopen header.homehead{background:var(--color-bg)}
body.homefull .homemap{opacity:0}
body.homefull .homemap.mapready{opacity:1}
body.homefull .homemap.mapready.mapin{transition:opacity .3s ease}
body.homefull.schedhome .homemap.mapready,body.homefull.schedhome .homemap.mapready.mapin{opacity:calc(1 - var(--mapfade, 0));transition:none}
body.schedopen .homemap,body.schedopen .homemap.mapready,body.schedopen .homemap.mapready.mapin{opacity:0;transition:none}
#schedule{scroll-margin-top:calc(var(--homehead, 88px) + 8px)}
@media (prefers-reduced-motion:reduce){body.homefull .homemap,body.homefull .homemap.mapready.mapin{transition:none}}
body.profilepage main{padding-bottom:calc(var(--nav-clear) + 32px + env(safe-area-inset-bottom))}
header.profilebar{position:sticky;top:0;left:0;right:0;z-index:5;width:100%;max-width:none;background:var(--color-bg);display:grid;grid-template-columns:88px 1fr 88px;grid-template-rows:44px;align-items:center;padding:env(safe-area-inset-top) 6px 0;box-sizing:border-box;min-height:44px;border:0;box-shadow:none;outline:none;view-transition-name:none}
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
a.rowbtn,button.rowbtn{width:100%;height:auto;min-height:60px;padding:14px 18px;border-radius:0;background:transparent;color:var(--t1);font-weight:500;justify-content:flex-start;text-align:left;text-decoration:none;border-top:1px solid var(--line)}
.switchrow{display:flex;align-items:center;justify-content:space-between;gap:12px;min-height:48px;margin:0 0 var(--space-4);color:var(--color-text);font-size:16px;font-weight:500}
.switch{position:relative;width:44px;height:28px;flex:none}
.switch input{position:absolute;opacity:0;width:1px;height:1px}
.switch span{display:block;width:44px;height:28px;border-radius:999px;background:var(--color-surface-2);border:1px solid var(--color-control)}
.switch span::after{content:"";position:absolute;top:3px;left:3px;width:20px;height:20px;border-radius:50%;background:var(--color-text)}
.switch input:checked+span{background:var(--color-lime);border-color:var(--color-lime)}
.switch input:checked+span::after{transform:translateX(16px);background:var(--color-forest)}
.switch input:focus-visible+span{outline:2px solid var(--color-focus);outline-offset:2px}
.list>form{margin:0}
.list>form:not(:first-child)>button.rowbtn{border-top:1px solid var(--line)}
.pracemeta{color:var(--t2);text-align:center;margin:0;font-size:15px}
.pracemeta+.pracemeta{margin-top:2px}
.pracestatus{margin:10px 0 2px}
.stats.trio{width:100%;max-width:420px}
.stats.trio .stattile{flex:1;min-width:0;padding:12px 8px}
.list .li .coach-elig{margin-left:0;flex:none;height:24px;padding:0 8px;border-radius:999px;border:1px solid var(--line);background:var(--color-chip);font-size:12px;font-weight:600}
.profilename{margin:14px 0 4px;font-size:24px;font-weight:650;letter-spacing:-.3px;text-align:center}
.card.cancelled{opacity:.55}
.card.cancelled .nxcardhead .nxtitle,.profilename.cancelled{text-decoration:line-through;color:var(--t3)}
.profilesub{color:var(--t2);text-align:center;margin:0 0 16px}
.stats{display:flex;gap:10px;justify-content:center;margin:0 0 8px}
.stattile{min-width:120px;background:var(--surface);border-radius:14px;padding:12px 16px;text-align:center}
.stattile b{display:block;font-size:22px;font-weight:650;line-height:1.2}
.stattile span{color:var(--t2);font-size:12px}
body.practicepage header.profilebar h1{font:700 20px/1 var(--r2-font-display);letter-spacing:-.02em}
body.practicepage header.profilebar{background:transparent}
body.practicepage header.profilebar .profileback,body.practicepage header.profilebar a.profileback{width:44px;height:44px;min-width:44px;padding:0;border-radius:999px;background:var(--r2-graphite);color:var(--r2-paper)}
body.practicepage .stattile{background:var(--r2-carbon);border-radius:22px;color:var(--r2-paper)}
body.practicepage .stattile b{font:700 28px/1 var(--r2-font-display);color:var(--r2-paper)}
body.practicepage .stattile span{color:var(--r2-smoke);font:600 12px/1.2 var(--r2-font-sans)}
body.adminpage .evcard{border:0;border-radius:28px;background:var(--r2-carbon);color:var(--r2-paper);padding:18px 20px}
body.adminpage .playersearch input{height:48px;border:0;border-radius:999px;background:var(--r2-graphite);color:var(--r2-paper)}
body.adminpage h2{font-family:var(--r2-font-display);letter-spacing:-.03em}
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
.cropstage{position:relative;width:min(280px,100%);aspect-ratio:1;margin:0 auto 12px;border-radius:50%;overflow:hidden;touch-action:none;background:var(--color-surface-2);cursor:grab}
.cropstage img{position:absolute;left:0;top:0;max-width:none;transform-origin:0 0;user-select:none;-webkit-user-drag:none;pointer-events:none}
.cropstage.dragging{cursor:grabbing}
.croprange{margin:0 0 12px}
.prefedit{margin:0}
.prefedit input{margin-top:6px}
.homealerts{position:relative;z-index:1}
.homedock{position:fixed;z-index:2;left:0;right:0;bottom:calc(var(--nav-clear) + env(safe-area-inset-bottom));max-width:640px;margin:0 auto;padding:0 12px 10px;display:flex;flex-direction:column;gap:8px;max-height:min(68vh,calc(100dvh - 150px));overflow:auto;pointer-events:none}
.homedock .card{pointer-events:auto;background:var(--color-surface);margin:0}
.menu a{display:flex;align-items:center;width:100%;height:40px;padding:0 12px;box-sizing:border-box;color:var(--t1);font-weight:500;font-size:15px;text-decoration:none;border-radius:8px}
.card .menu,.pagehead .menu{left:auto;right:0;min-width:220px}
.pagehead{display:flex;flex-direction:column;align-items:stretch;gap:var(--space-2);margin:0 0 var(--space-4)}
.managehome{display:flex;flex-direction:column;gap:12px;padding-bottom:24px}
.mq{margin:0}
.mqfield{position:relative;display:block;margin-top:8px}
.mqfield input{width:100%;margin:0;padding-right:44px}
.mqfield input[type=search]::-webkit-search-decoration,.mqfield input[type=search]::-webkit-search-cancel-button,.mqfield input[type=search]::-webkit-search-results-button{display:none}
button.mqclear{position:absolute;right:4px;top:50%;transform:translateY(-50%);width:36px;height:36px;min-height:36px;padding:0;border:0;border-radius:8px;background:transparent;color:var(--t2);font-size:22px;font-weight:400;line-height:1}
.qactions{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:8px}
.qact{display:flex;flex-direction:column;justify-content:flex-end;min-height:72px;padding:12px;border-radius:16px;background:var(--color-raised);color:inherit;text-decoration:none;font-size:13px;font-weight:650}
.mseclabel{margin:4px 0 0;font-size:13px;font-weight:650;color:var(--t3)}
.orggrid{display:grid;grid-template-columns:1fr 1fr;gap:12px}
.orggrid[hidden],.qactions[hidden],#manageHits[hidden]{display:none}
.orgcard{display:flex;flex-direction:column;align-items:flex-start;gap:6px;min-height:124px;padding:20px;border-radius:32px;background:var(--r2-graphite);color:var(--r2-paper);text-decoration:none}
.orgcard b{font:700 22px/1.05 var(--r2-font-display);letter-spacing:-.03em}
.orgcard .mdesc{color:var(--r2-smoke);font:500 13px/1.35 var(--r2-font-sans)}
.mseclabel{margin:8px 0 0;color:var(--r2-smoke);font:700 10px/1.2 var(--r2-font-sans);letter-spacing:.08em;text-transform:uppercase}
.mqfield input{height:48px;border:0;border-radius:999px;background:var(--r2-graphite);color:var(--r2-paper);font:600 15px/48px var(--r2-font-sans);padding:0 44px 0 16px;box-sizing:border-box}
header.homehead h1,header.profilebar h1{font-family:var(--r2-font-display);font-weight:700;letter-spacing:-.03em}
header.homehead:has(.displayhead){height:auto;min-height:0;align-items:flex-end;padding-bottom:12px}
header.homehead:has(.displayhead) .headmain{height:auto;align-items:flex-end}
header.homehead .displayhead{display:flex;flex-direction:column;align-items:flex-start;gap:6px;min-width:0}
header.homehead .displayeye{margin:0;color:var(--r2-smoke);font:700 11px/1.2 var(--r2-font-sans);letter-spacing:.08em;text-transform:uppercase}
header.homehead .displayeye .usawpchip{height:auto;margin:0;padding:0;border:0;background:transparent;color:var(--r2-smoke);font:700 11px/1.2 var(--r2-font-sans);letter-spacing:.08em;text-transform:uppercase}
header.homehead .displayhead h1{height:auto;margin:0;color:var(--r2-paper);font:700 clamp(52px,16vw,80px)/.86 var(--r2-font-display);letter-spacing:-.05em}
header.homehead .displayhead h1::after{content:"."}
body.homefull header.homehead:has(.displayhead){background:linear-gradient(180deg,color-mix(in srgb,var(--r2-ink) 92%,transparent),transparent)}
body.schedopen header.homehead:has(.displayhead){background:var(--color-bg);padding-bottom:20px}
.profilename{font-family:var(--r2-font-display);font-weight:700;font-size:32px;letter-spacing:-.03em}
.seclabel{color:var(--r2-smoke);font:700 10px/1.2 var(--r2-font-sans);letter-spacing:.08em;text-transform:uppercase}
.lineupfilt .chip,.profswitch .chip,.rolechips .chip{background:var(--r2-graphite);color:var(--r2-paper);border-color:transparent;border-radius:999px;font:700 13px/1 var(--r2-font-sans)}
.lineupfilt .chip.on,.profswitch .chip.on,.rolechips .chip.on{background:var(--r2-paper);color:var(--r2-ink);border-color:transparent}
body.homefull .homedock .card,body.homefull .schedlist .card,div.card.tap.tripcard{border-radius:36px;border-color:transparent;background:var(--r2-carbon);color:var(--r2-paper)}
body.homefull .homedock .nextcard:not(.cancelled){background:var(--r2-sun);color:var(--r2-fixed-ink)}
body.homefull .homedock .nextcard:not(.cancelled) .nxtitle,body.homefull .homedock .nextcard:not(.cancelled) .nxrow,body.homefull .homedock .nextcard:not(.cancelled) .cardtitle,body.homefull .homedock .nextcard:not(.cancelled) .datetile{color:var(--r2-fixed-ink)}
body.homefull .homealerts .card:not(#pushCard){background:var(--r2-lavender);color:var(--r2-fixed-ink);border-radius:32px;padding:20px 22px}
body.homefull .homealerts .card:not(#pushCard) .t3,body.homefull .homealerts .card:not(#pushCard) p{color:var(--r2-fixed-ink)}
.drivechipbtn,.drivechiptext{background:var(--r2-lime);color:var(--r2-fixed-ink);border-color:transparent}
.drivechiptext .driveage{color:var(--r2-fixed-ink)}
main:has(.lineupfilt) .seclabel{color:var(--r2-smoke);font:700 28px/.95 var(--r2-font-display);letter-spacing:-.03em;text-transform:none}
.linekind{display:inline-flex;margin:0 0 8px;padding:5px 10px;border-radius:999px;background:var(--r2-fixed-ink);color:var(--r2-fixed-paper);font:700 11px/1 var(--r2-font-sans)}
.tripcard .nxtitle.cardtitle{font:700 34px/.95 var(--r2-font-display);letter-spacing:-.03em}
div.card.tap.tripcard[data-kind]:not(.cancelled){background:var(--r2-sun);color:var(--r2-fixed-ink)}
div.card.tap.tripcard[data-kind=Tournament]:not(.cancelled),div.card.tap.tripcard[data-kind=Competition]:not(.cancelled){background:var(--r2-lavender);color:var(--r2-fixed-ink)}
div.card.tap.tripcard[data-kind=Volunteer]:not(.cancelled),div.card.tap.tripcard[data-kind=Fundraiser]:not(.cancelled){background:var(--r2-bubblegum);color:var(--r2-fixed-ink)}
div.card.tap.tripcard[data-kind=Social]:not(.cancelled),div.card.tap.tripcard[data-kind=Meeting]:not(.cancelled),div.card.tap.tripcard[data-kind=Other]:not(.cancelled){background:var(--r2-mango);color:var(--r2-fixed-ink)}
div.card.tap.tripcard[data-kind=Trip]:not(.cancelled){background:var(--r2-aqua);color:var(--r2-fixed-ink)}
div.card.tap.tripcard[data-kind=Clinic]:not(.cancelled){background:var(--r2-sky);color:var(--r2-fixed-ink)}
div.card.tap.tripcard[data-kind]:not(.cancelled) .nxtitle,div.card.tap.tripcard[data-kind]:not(.cancelled) .nxrow,div.card.tap.tripcard[data-kind]:not(.cancelled) .cardsub,div.card.tap.tripcard[data-kind]:not(.cancelled) .datetile,div.card.tap.tripcard[data-kind]:not(.cancelled) .cardtitle{color:var(--r2-fixed-ink)}
div.card.tap.tripcard[data-kind]:not(.cancelled) .datetile{background:rgba(11,11,12,.12)}
div.card.tap.tripcard[data-kind]:not(.cancelled) .btn-secondary{background:var(--ink);color:var(--paper);border-color:transparent}
div.card.tap.tripcard.cancelled{background:var(--r2-carbon);color:var(--r2-smoke)}
main:has(.lineupfilt){padding-bottom:calc(var(--nav-clear) + 80px + env(safe-area-inset-bottom))}
.lmetrics{display:flex;gap:8px;margin:2px 0 8px}
.lmetric{flex:1;min-width:0;min-height:110px;border-radius:28px;padding:14px 12px 12px;display:flex;flex-direction:column;justify-content:space-between}
.lmetric b{font:700 60px/.85 var(--r2-font-display);letter-spacing:-.06em}
.lmetric span{font:700 10px/1.1 var(--r2-font-sans);letter-spacing:.08em}
.lmetric.hrs{background:var(--carbon);color:var(--lime)}
.lmetric.reg{background:var(--lime);color:var(--ink)}
.lmetric.dec{background:var(--team-sun);color:var(--ink)}
.lmonth,details.lineuppast>summary{margin:18px 0 10px;color:var(--smoke);font:700 28px/.95 var(--r2-font-display);letter-spacing:-.03em;text-transform:none}
details.lineuppast{border:0}
details.lineuppast>summary{cursor:pointer;list-style:none}
details.lineuppast>summary::-webkit-details-marker{display:none}
.card.tap.tripcard.lcard{color:inherit;padding:22px 20px 20px;border-radius:36px;gap:10px;min-height:156px;box-sizing:border-box;display:flex;flex-direction:column;text-decoration:none;overflow:hidden}
div.card.tap.tripcard.lcard.ltall{gap:12px;min-height:208px}
div.card.tap.tripcard.lcard.ltall.pinned{min-height:228px}
.lcard .lctop,.lcard .ltop,.lcard .ltfoot,.lcard .lcfoot,.lcard .lmain{display:flex;align-items:center;justify-content:space-between;gap:10px}
.lcard .lcpill{background:var(--ink);color:var(--paper);border-radius:999px;padding:5px 10px;font:700 11px/1 var(--r2-font-sans)}
.lcard .lcstatus,.lcard .lover{display:inline-flex;align-items:center;gap:4px;font:700 12px/1 var(--r2-font-sans);color:inherit}
.lcard .lover{font-size:10px;letter-spacing:.08em}
.lcard .lccheck{display:block;flex:none}
.lcard .lctitle{margin:0;font:700 34px/.95 var(--r2-font-display);letter-spacing:-.03em;color:inherit}
.lcard .lttitle{display:block;margin:0;font:700 36px/.95 var(--r2-font-display);letter-spacing:-.03em;color:inherit}
.lcard .lcmeta,.lcard .ltmeta{margin:0;font:600 12px/1.35 var(--r2-font-sans);color:inherit}
.lcard .lcfoot{margin-top:auto}
.lcard .lctrack{flex:1;height:10px;border-radius:5px;background:rgba(11, 11, 12,.2);overflow:hidden}
.lcard .lctrack i{display:block;height:100%;background:var(--ink);border-radius:5px}
.lcard .lmain{align-items:flex-start;justify-content:flex-start}
.lcard .ldate{display:flex;flex-direction:column;align-items:flex-start;min-width:88px;color:inherit}
.lcard .ldate b{font:700 104px/.86 var(--r2-font-display);letter-spacing:-.05em;color:inherit}
.lcard.past .ldate b{font-size:80px}
.lcard .ldate span{font:700 11px/1 var(--r2-font-sans);letter-spacing:.08em;text-transform:uppercase;color:inherit}
.lcard .lgrow{min-width:0;flex:1}
.lcard .ltfoot span,.lcard .lcfoot>span:last-child{font:700 13px/1 var(--r2-font-sans);color:inherit;white-space:nowrap}
.lcard .lacts{display:flex;gap:8px;margin:0}
.lcard button.lghost,.lcard button.lfill{width:auto;height:auto;min-height:0;padding:8px 12px;border-radius:999px;font:700 12px/1 var(--r2-font-sans)}
.lcard button.lghost{background:transparent;color:var(--ink);border:1.5px solid var(--ink)}
.lcard button.lfill{background:var(--ink);color:var(--paper);border:0}
.lcard .pastpill{background:var(--graphite);color:var(--paper);border-radius:999px;padding:4px 8px;font:700 11px/1 var(--r2-font-sans)}
.lcard .cardlink{color:inherit;text-decoration:none;display:flex;flex-direction:column;gap:12px}
div.card.tap.tripcard.lcard[data-kind] .lctitle,div.card.tap.tripcard.lcard[data-kind] .lttitle,div.card.tap.tripcard.lcard[data-kind] .lcmeta,div.card.tap.tripcard.lcard[data-kind] .ltmeta,div.card.tap.tripcard.lcard[data-kind] .lover,div.card.tap.tripcard.lcard[data-kind] .lcstatus,div.card.tap.tripcard.lcard[data-kind] .ldate,div.card.tap.tripcard.lcard[data-kind] .ldate b{color:inherit}
body.profilepage .profilehero{align-items:flex-start;padding:4px 0 8px}body.profilepage .profilename::after{content:"."}body.profilepage .seclabel{font:700 28px/.95 var(--r2-font-display);letter-spacing:-.03em;color:var(--paper)}body.profilepage .numcard{margin-bottom:28px}body.profilepage main{padding-bottom:calc(var(--nav-clear) + 48px + env(safe-area-inset-bottom))}
body.profilepage .avatar.hero{background:var(--r2-sun);color:var(--r2-fixed-ink);border:0;font:700 40px/.95 var(--r2-font-display);letter-spacing:-.04em}
body.profilepage .profilename{margin:14px 0 8px;text-align:left;font:700 clamp(48px,14vw,64px)/.86 var(--r2-font-display);letter-spacing:-.05em}
body.profilepage .profilename::after{content:"."}
body.profilepage .profilerow{display:flex;align-items:center;gap:8px;flex-wrap:wrap;width:100%;margin:0 0 16px}
body.profilepage .profilesub{margin:0;text-align:left;color:var(--r2-smoke);font:600 13px/1.3 var(--r2-font-sans)}
.rolechip{display:inline-flex;align-items:center;height:27px;padding:0 12px;border-radius:999px;background:var(--r2-graphite);color:var(--r2-paper);font:700 12px/1 var(--r2-font-sans)}
body.profilepage .metrics{display:grid;grid-template-columns:1fr 1fr;gap:10px;width:100%;margin:0 0 16px}
body.profilepage .metric{min-height:108px;padding:18px 20px 16px;border-radius:32px;color:var(--r2-fixed-ink)}
body.profilepage .metric b{display:block;font:700 clamp(40px,12vw,64px)/.85 var(--r2-font-display);letter-spacing:-.06em}
body.profilepage .metric span{font:700 10px/1.2 var(--r2-font-sans);letter-spacing:.08em;text-transform:uppercase}
body.profilepage .metric.sun{background:var(--r2-sun)}
body.profilepage .metric.sky{background:var(--r2-sky)}
body.profilepage header.profilebar{grid-template-columns:44px 1fr auto;gap:8px;padding:env(safe-area-inset-top) 16px 0;background:var(--r2-ink)}
body.profilepage header.profilebar h1{text-align:left;font:700 20px/44px var(--r2-font-display);letter-spacing:-.02em}
body.profilepage .morebtn{width:40px;height:40px;min-width:40px;padding:0;border-radius:999px;background:var(--r2-graphite);color:var(--r2-paper);font:700 18px/1 var(--r2-font-sans)}
header.profilebar #profileEdit{display:none !important}
.msgpill{display:flex;align-items:center;justify-content:center;box-sizing:border-box;width:100%;min-height:52px;margin:0 0 16px;border-radius:999px;background:var(--r2-lime);color:var(--r2-fixed-ink);font:700 16px/1 var(--r2-font-sans);text-decoration:none}
.needcard{margin:0 0 16px;padding:16px 18px;border-radius:28px;background:var(--team-tangerine);color:var(--ink)}
.needkicker{margin:0 0 6px;font:700 10px/1.2 var(--r2-font-sans);letter-spacing:.08em;text-transform:uppercase}
.needcard b{display:block;margin:0 0 8px;font:700 28px/1.05 var(--r2-font-display);letter-spacing:-.03em}
.needcard p{margin:0;font:600 14px/1.35 var(--r2-font-sans)}
.sporthead{display:flex;align-items:center;gap:8px;margin:0 0 4px;font:700 16px/1.2 var(--r2-font-sans);color:var(--r2-paper)}
.minichip{padding:4px 8px;border-radius:999px;background:var(--r2-graphite);color:var(--r2-paper);font:700 11px/1 var(--r2-font-sans)}
.sportline{display:flex;align-items:center;justify-content:space-between;gap:12px;min-height:48px;color:var(--r2-paper);font:700 16px/1.2 var(--r2-font-sans)}
.menuwho{display:flex;align-items:center;gap:12px;margin:0 0 12px}
.menuwho .mark{width:44px;height:44px;border-radius:999px;display:inline-flex;align-items:center;justify-content:center;background:var(--r2-sun);color:var(--r2-fixed-ink);font:700 14px/1 var(--r2-font-display)}
.menuwho .mark.sky{background:var(--r2-sky)}
.menuwho b{display:block;color:var(--r2-paper);font:700 16px/1.2 var(--r2-font-sans)}
.menuwho small{display:block;color:var(--r2-smoke);font:600 12px/1.3 var(--r2-font-sans)}
.privcard{display:flex;flex-direction:column;margin:0 0 18px;padding:6px;border-radius:26px;background:var(--r2-graphite)}
.privrow{display:flex;align-items:center;gap:12px;padding:12px 10px;color:var(--r2-paper)}
.privrow b{display:block;font:700 15px/1.2 var(--r2-font-sans)}
.privrow small{display:block;margin-top:2px;color:var(--r2-smoke);font:600 12px/1.35 var(--r2-font-sans)}
.privgo{flex:none;color:var(--r2-smoke);font:700 14px/1.2 var(--r2-font-sans)}
.r2switch{position:relative;width:52px;height:32px;flex:none}
.r2switch input{position:absolute;opacity:0;width:100%;height:100%;margin:0}
.r2switch i{position:absolute;inset:0;border-radius:999px;background:var(--smoke);pointer-events:none}
.r2switch i:before{content:"";position:absolute;width:26px;height:26px;left:3px;top:3px;border-radius:50%;background:var(--paper);transition:transform .15s ease}
.r2switch input:checked+i{background:var(--r2-lime)}
.r2switch input:checked+i:before{transform:translateX(20px)}
.btn-tangerine{background:var(--team-tangerine);color:var(--ink);border:0}
.btn-tangerine:disabled{opacity:.45}
.privacyform{max-width:400px}
@media (min-width:768px){
 body.profilepage .privacyform{margin:24px auto}
 dialog.profmenu.popover{position:fixed;width:340px;height:auto;max-height:90dvh;inset:auto;margin:0}
 dialog.profmenu.popover .sheet{border-radius:24px;border:1px solid var(--r2-graphite);max-height:min(90dvh,640px)}
 dialog.profmenu.popover .grab{display:none}
}
body.profilepage header.profilebar .profileback{width:44px;height:44px;min-width:44px;padding:0;border-radius:999px;background:var(--r2-graphite);color:var(--r2-paper)}
body.profilepage:not(.profile-edit) #profileBack{display:none}
body.profilepage .seclabel{margin:22px 0 8px;color:var(--r2-paper);font:700 28px/.95 var(--r2-font-display);letter-spacing:-.03em;text-transform:none}
body.profilepage .list,body.adminpage .list,body.adminpage .mlist{background:transparent;display:flex;flex-direction:column;gap:8px;overflow:visible}
body.profilepage .list>.li,body.profilepage .list>a.li,body.adminpage .list>.li,body.adminpage .list>a.li,body.adminpage .mrow{background:var(--r2-carbon);color:var(--r2-paper);border:0;border-radius:28px}
body.profilepage:not(.profile-edit) .infogrid{display:grid;grid-template-columns:1fr 1fr;gap:8px}
body.profilepage:not(.profile-edit) .infogrid .prow{flex-direction:column;align-items:flex-start;gap:6px}
body.profilepage:not(.profile-edit) .infogrid .prow .k{color:var(--r2-smoke);font:700 10px/1.2 var(--r2-font-sans);letter-spacing:.08em;text-transform:uppercase}
body.profilepage:not(.profile-edit) .infogrid .prow .v{text-align:left;color:var(--r2-paper);font:700 16px/1.25 var(--r2-font-sans)}
body.profilepage.profile-edit .infogrid{display:flex;flex-direction:column}
a.ghostpill{display:flex;align-items:center;justify-content:center;height:56px;margin-top:8px;border-radius:999px;border:1.5px solid var(--r2-graphite);background:transparent;color:var(--r2-paper);font:700 16px/1 var(--r2-font-sans)}
body.adminpage .pagehead h1{font:700 clamp(36px,8vw,56px)/.9 var(--r2-font-display);letter-spacing:-.04em}
@media (min-width:476px){.orggrid{gap:16px}}
@media (min-width:768px){.orggrid{grid-template-columns:repeat(3,minmax(0,1fr))}header.homehead .displayhead h1{font-size:80px}body.profilepage .profilename{font-size:64px}}
@media (min-width:1280px){.orggrid{grid-template-columns:repeat(4,minmax(0,1fr))}}
.orgcard .mchev{margin-top:auto;align-self:flex-end}
.rolechips{display:flex;gap:8px;overflow-x:auto;margin:0 0 8px;scrollbar-width:none}
.rolechips .chip{flex:none}
.mgroups{display:flex;flex-direction:column;gap:var(--space-3)}
.mgroup h2{margin:0 0 var(--space-2);padding:0 4px;font-size:13px;font-weight:650;letter-spacing:.01em;color:var(--t3)}
.mlist{background:var(--color-raised);border-radius:16px;overflow:hidden}
.mrow{display:flex;align-items:center;gap:12px;min-height:72px;padding:16px 12px 16px 10px;color:inherit;text-decoration:none;border-top:1px solid var(--line)}
.sporttag{display:inline-flex;align-items:center;height:22px;margin:4px 6px 0 0;padding:0 8px;border-radius:999px;border:1px solid var(--color-control);font-size:12px;font-weight:650}
.clubform{padding-bottom:12px}
.passform{padding-bottom:28px}
.passform .btn-primary{margin-top:16px}
#passForm [hidden]{display:none !important}
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
.menu.floating{position:fixed;z-index:50;left:auto;top:auto;right:auto;margin:0;max-height:min(320px,calc(100dvh - var(--nav-clear) - 24px));overflow:auto}
.menu form{margin:0}
.menu button{width:100%;height:40px;padding:0 12px;justify-content:flex-start;background:transparent;color:var(--t1);font-weight:500;font-size:15px;border-radius:8px}
.menu button:disabled{color:var(--t3)}
.li{display:flex;align-items:center;gap:12px;padding:14px 18px;min-height:60px;border-top:1px solid var(--line)}.li:first-child{border-top:0}
.formsec{margin:22px 0 0}.formsec>h2{margin:0 4px 8px;font-size:13px;font-weight:650;letter-spacing:.01em;color:var(--t3)}
button.selfield{width:100%;min-height:44px;background:transparent;color:inherit;border-radius:0;height:auto;padding:14px 16px;justify-content:flex-start;text-align:left}
.selfieldk{flex:none;font-weight:500;color:var(--color-text)}.selfieldv{flex:1;min-width:0;text-align:right;color:var(--t3);font-weight:400}
.selfield svg{flex:none;color:var(--t3)}
.sheetlist{margin:0 0 12px}.sheetopt{display:flex;align-items:flex-start;gap:12px;min-height:44px;padding:10px 0;border-top:1px solid var(--line);color:var(--color-text);font-size:16px}
.sheetopt:first-child{border-top:0}.sheetopt b{display:block;font-weight:600}.sheetopt small{display:block;color:var(--t3);font-size:13px;line-height:1.35;font-weight:400}
.sheetopt input{margin-top:2px}
.sheetsearch{margin:0 0 8px}
.skipchips{display:flex;flex-wrap:wrap;gap:8px;margin:8px 0 12px}
.skipchip{display:inline-flex;align-items:center;gap:4px;min-height:44px;padding:0 4px 0 12px;border-radius:999px;background:var(--surface2);color:var(--t1);font-size:15px;font-weight:500}
.skipchip button{width:44px;height:44px;min-height:44px;padding:0;background:transparent;color:var(--t2);font-size:20px;font-weight:400}
.coachrow{display:flex;align-items:center;gap:12px;min-height:52px;padding:8px 0;border-top:1px solid var(--line)}
.coachrow .avatar{width:36px;height:36px;min-width:36px;max-width:36px;min-height:36px;max-height:36px;flex:0 0 36px;font-size:13px}
body.editor nav.tabs,body.profile-edit nav.tabs{display:none}
body.editor main,body.profile-edit main{padding-bottom:calc(var(--nav-clear) + 32px + env(safe-area-inset-bottom))}
.planrow{flex-wrap:wrap;align-items:center}.planline{flex:1;min-width:0;display:flex;align-items:center;justify-content:flex-start;gap:8px;flex-wrap:wrap;text-align:left}.planlabel{font-weight:500;color:var(--color-text);text-align:left}.plantext{flex:1 0 100%;white-space:pre-wrap;margin-top:4px;text-align:left}
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
padding:0 14px;height:var(--size-button);font:inherit;color-scheme:dark}textarea{padding:12px 14px}input[type=hidden]{display:none}input[type=checkbox],.checks input[type=radio]{display:inline-block;width:20px;height:20px;margin:0 8px 0 0;vertical-align:-4px;accent-color:var(--accent);flex:none}
input[type=file].pick{position:absolute;left:0;top:0;width:1px;height:1px;margin:0;padding:0;border:0;overflow:hidden;clip:rect(0,0,0,0);opacity:0;pointer-events:none}
.sheetopt input,.coachrow input{display:inline-block;width:22px;height:22px;min-width:22px;flex:none;margin:2px 0 0;padding:0;background:transparent}
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
.eventacts{display:flex;gap:12px;margin:12px 0 0}.eventacts .btn{flex:1 1 0;width:auto;min-width:0}
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
dialog.modal{border:0;padding:0;background:transparent;color:var(--t1);width:min(440px,calc(100vw - 32px));max-height:calc(100dvh - 32px);overflow:hidden}
dialog.modal::backdrop{background:var(--color-backdrop)}
dialog.modal .sheet{background:var(--surface);border:1px solid var(--line);border-radius:var(--r);padding:20px;max-height:calc(100dvh - 32px);overflow:auto}
dialog.modal .sheet form>.btn,dialog.modal .sheet form>button.btn,dialog.modal .sheet form>.row:last-child,dialog.botsheet .sheet form>.btn,dialog.botsheet .sheet form>button.btn,dialog.botsheet .sheet form>.row:last-child,dialog.modal .sheet>.btn,dialog.botsheet .sheet>.btn{margin-top:var(--space-form-action)}
dialog.modal .sheet form>:has(+.btn),dialog.modal .sheet form>:has(+button.btn),dialog.modal .sheet form>:has(+.row),dialog.botsheet .sheet form>:has(+.btn),dialog.botsheet .sheet form>:has(+button.btn),dialog.modal .sheet>:has(+.btn),dialog.botsheet .sheet>:has(+.btn){margin-bottom:0}
#photoDlg .sheet{padding:var(--space-5)}
#photoDlg:has(#photoCrop:not([hidden])) .attachphone,#photoDlg:has(#photoCrop:not([hidden])) .attachwide,#photoDlg:has(#photoCrop:not([hidden])) #photoRemove{display:none}
#photoRemove{margin-top:var(--space-form-action)}
.note{background:var(--surface);border-radius:var(--r);padding:14px 18px;margin:0 0 12px;color:var(--t2);font-size:15px}.note b{color:var(--t1)}
.toast{position:fixed;left:50%;bottom:calc(var(--nav-clear) + 12px + env(safe-area-inset-bottom));transform:translateX(-50%);z-index:30;background:var(--surface);color:var(--t1);border:1px solid var(--line);border-radius:12px;padding:12px 16px;font-size:15px;line-height:1.4;text-align:center;box-shadow:0 8px 28px rgba(11, 11, 12,.5);max-width:min(440px,calc(100% - 32px))}
body:has(.composer) .toast{bottom:calc(var(--nav-clear) + env(safe-area-inset-bottom) + var(--composer-h, 69px) + 12px)}
details>summary{list-style:none;cursor:pointer;display:flex;align-items:center;justify-content:space-between;min-height:56px;padding:0 18px;color:var(--t1)}
details>summary::-webkit-details-marker{display:none}details>summary::after{content:"›";color:var(--t3);font-size:22px;transition:transform .15s}
details[open]>summary::after{transform:rotate(90deg)}details.card{padding:0}details>.body{padding:0 18px 18px}details>.body>p:last-child{margin-bottom:0}
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
.people{padding-bottom:48px}
.peoplebar{position:sticky;top:var(--headh,0px);z-index:6;background:var(--color-bg);margin:0 -20px 0;padding:0 20px 18px}
.peoplebar input{height:48px;margin:0}
.fchips{margin-top:10px;margin-bottom:0}
.expage h2.egroup{position:sticky;top:var(--headh,0px);z-index:4;background:var(--color-bg);margin:18px 0 8px;padding:8px 0}
.daybadge{height:28px;padding:0 10px;margin:0;flex:none;font-weight:700}
.people h2{position:sticky;top:calc(var(--headh,0px) + var(--peoplepin,0px));z-index:4;background:var(--color-bg);padding:8px 0;margin-top:12px}
.lgroup{margin:0 0 14px}
.lgroup .list{margin:0}
h3.alpha{margin:0 -20px;padding:12px 20px 14px;font-size:13px;font-weight:700;letter-spacing:.06em;color:var(--t3);position:sticky;top:calc(var(--headh,0px) + var(--peoplepin,0px));z-index:5;background:var(--color-bg);line-height:1.2}
.lgroup .list{position:relative;z-index:0;margin-top:0;scroll-margin-top:calc(var(--headh,0px) + var(--peoplepin,0px) + 44px)}
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
border:1px solid var(--nav-glass-line);border-radius:999px;box-shadow:0 8px 28px rgba(11, 11, 12,.28);
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
body.editor nav.nav3,body.profile-edit nav.nav3{display:none}
body:has(nav.nav3){--nav-clear:104px}
nav.nav3{position:fixed;z-index:9;left:var(--r2-space-4);right:var(--r2-space-4);bottom:calc(20px + env(safe-area-inset-bottom));height:72px;display:flex;align-items:center;justify-content:flex-start;gap:6px;padding:8px;border:0;border-radius:var(--r2-radius-pill);background:transparent;box-sizing:border-box;overflow:visible;touch-action:pan-y}
nav.nav3::before{content:"";position:absolute;inset:0;border-radius:inherit;background:var(--r2-nav-translucent);-webkit-backdrop-filter:blur(24px);backdrop-filter:blur(24px);z-index:0;pointer-events:none}
.nav3-crest,.nav3-tabs{z-index:1}
@media (min-width:476px) and (max-width:767px){
 nav.nav3{bottom:calc(28px + env(safe-area-inset-bottom))}
 body:has(nav.nav3){--nav-clear:120px}
}
@media (max-width:767px){
 nav.nav3{background:transparent}
 nav.nav3::before{background:var(--r2-nav-translucent);-webkit-backdrop-filter:blur(24px);backdrop-filter:blur(24px)}
}
.nav3-crest{position:relative;width:56px;height:56px;flex:none;display:flex;align-items:center;justify-content:center;gap:10px;padding:0;border:0;border-radius:var(--r2-radius-pill);background:transparent;color:var(--r2-fixed-ink);cursor:pointer}
.nav3-crest-face{width:56px;height:56px;flex:none;display:flex;align-items:center;justify-content:center;border-radius:var(--r2-radius-pill);background:var(--r2-sun);color:var(--r2-fixed-ink);font:700 20px/1 var(--r2-font-display);box-sizing:border-box}
nav.nav3[data-place="me"] .nav3-crest-face{background:var(--r2-paper);color:var(--r2-ink)}
nav.nav3[data-place="everything"] .nav3-crest-face{background:var(--r2-ink);color:var(--r2-lime);border:1px solid var(--r2-smoke)}
.nav3-logo{display:none}
nav.nav3[data-place="everything"] .nav3-logo.lg.lime{display:block;width:32px;height:12.525px}
[data-theme="light"] nav.nav3[data-place="everything"] .nav3-logo.lg.lime{display:none}
[data-theme="light"] nav.nav3[data-place="everything"] .nav3-logo.lg.ink{display:block;width:32px;height:12.525px}
.nav3-initials{display:none}
.nav3-photo{display:none;width:100%;height:100%;object-fit:cover;border-radius:inherit}
nav.nav3[data-place="me"] .nav3-initials,nav.nav3[data-place="team"] .nav3-initials{display:block}
nav.nav3[data-place="me"] .nav3-photo{display:block}
nav.nav3[data-place="me"]:has(.nav3-photo) .nav3-initials{display:none}
.crestmark.who img{width:100%;height:100%;object-fit:cover;border-radius:inherit}
.nav3-more{position:absolute;left:38px;top:38px;width:20px;height:20px;border-radius:var(--r2-radius-pill);background:var(--r2-ink);color:var(--r2-paper);font:700 11px/20px var(--r2-font-sans);display:flex;align-items:center;justify-content:center}
.nav3-switch-copy,.nav3-chevron,.nav3-menu-label,.nav3-rule,.nav3-dot{display:none}
.nav3-tabs{position:relative;display:flex;flex:1;align-items:center;justify-content:flex-start;gap:6px;min-width:0;height:56px;padding:0;box-sizing:border-box}
.nav3-slide{position:absolute;z-index:0;left:0;top:0;height:56px;border-radius:var(--r2-radius-pill);background:var(--r2-lime);pointer-events:none;transition:left 280ms cubic-bezier(0.22,1,0.36,1),top 280ms cubic-bezier(0.22,1,0.36,1),width 280ms cubic-bezier(0.22,1,0.36,1),height 280ms cubic-bezier(0.22,1,0.36,1),background-color 280ms ease,border-radius 280ms ease}
.nav3-slide.manage{background:var(--r2-tangerine)}
.nav3-tabs a{position:relative;z-index:1;width:68px;height:56px;flex:0 0 68px;min-width:68px;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:3px;padding:0;border-radius:var(--r2-radius-pill);background:transparent;color:var(--r2-smoke);text-decoration:none;font:700 9px/normal var(--r2-font-sans);box-sizing:border-box;overflow:visible;transition:color 280ms ease,font-size 280ms cubic-bezier(0.22,1,0.36,1)}
.nav3-tabs a.on{flex:1 1 auto;width:auto;min-width:0;flex-direction:row;flex-wrap:nowrap;justify-content:center;align-items:center;gap:6px;padding:0 14px;background:transparent;color:var(--r2-fixed-ink);font:700 13px/16px var(--r2-font-sans);overflow:visible}
nav.nav3:has(.nav3-tabs>a:nth-child(5)){gap:4px}
nav.nav3:has(.nav3-tabs>a:nth-child(5)) .nav3-tabs{gap:4px}
nav.nav3:has(.nav3-tabs>a:nth-child(5)) .nav3-tabs a{flex:0 0 58px;width:58px;min-width:58px;padding:0}
nav.nav3:has(.nav3-tabs>a:nth-child(5)) .nav3-tabs a.on{flex:1 1 auto;width:auto;min-width:0;padding:0 14px}
.nav3-glyph,.nav3-label{transition:transform 280ms cubic-bezier(0.22,1,0.36,1)}
.nav3-glyph{width:20px;height:20px;display:block;flex:none;color:var(--r2-smoke)}
.nav3-tabs a.on .nav3-glyph{color:var(--r2-fixed-ink)}
.nav3-tabs a:focus-visible,.nav3-crest:focus-visible,.crestrow:focus-visible,.crestgo:focus-visible,.crestout:focus-visible{outline:2px solid var(--color-focus);outline-offset:2px}
dialog.crestmenu{position:fixed;margin:0;inset:auto auto calc(92px + env(safe-area-inset-bottom)) 16px;border:0;border-radius:36px;background:var(--r2-carbon);color:var(--r2-paper);width:min(358px,calc(100vw - 32px));max-height:min(626px,calc(100dvh - 112px - env(safe-area-inset-bottom)));padding:20px 16px;overflow:auto;box-sizing:border-box;display:none;flex-direction:column;gap:10px}
dialog.crestmenu[open]{display:flex}
dialog.crestmenu:focus{outline:none}
dialog.crestmenu::backdrop{background:rgba(11,11,12,.45)}
.crestlabel{margin:0;color:var(--r2-smoke);font:700 10px/normal var(--r2-font-sans);letter-spacing:0.8px}
.crestline{display:block;height:1px;background:var(--r2-graphite);width:100%}
.crestrow{display:flex;align-items:center;gap:var(--r2-space-3);padding:8px 14px 8px 10px;border-radius:28px;color:inherit;text-decoration:none;box-sizing:border-box}
.crestrow.here{background:var(--r2-graphite)}
.crestrow b{display:block;font:700 15px/normal var(--r2-font-sans);color:var(--r2-paper)}
.crestrow small{display:block;margin-top:1px;color:var(--r2-smoke);font:600 11px/normal var(--r2-font-sans)}
.crestmark{width:40px;height:40px;border-radius:var(--r2-radius-pill);display:inline-flex;align-items:center;justify-content:center;flex:none;font:700 14px/1 var(--r2-font-display);letter-spacing:-0.42px;color:var(--r2-fixed-ink)}
.crestmark.brand{background:var(--r2-lime)}
.crestmark.who{background:var(--r2-paper);color:var(--r2-ink)}
.crestmark.team{background:var(--r2-sun)}
.crestmark img{width:26px;height:10px;display:block}
.rolechip{margin-left:auto;padding:5px 10px;border-radius:var(--r2-radius-pill);font:700 11px/normal var(--r2-font-sans);display:inline-flex;align-items:center;flex:none}
.role-member{background:var(--r2-graphite);color:var(--r2-paper)}
.role-coach{background:var(--r2-sky);color:var(--r2-fixed-ink)}
.role-admin{background:var(--r2-tangerine);color:var(--r2-fixed-ink)}
.crestgo,.crestout{display:flex;align-items:center;justify-content:center;box-sizing:border-box;width:100%;padding:14px;border-radius:var(--r2-radius-pill);border:2px solid var(--r2-graphite);background:transparent;color:var(--r2-paper);font:700 14px/normal var(--r2-font-sans);text-decoration:none}
.crestout{border-color:var(--r2-tangerine);color:var(--r2-tangerine)}
.r2caps{margin:0 0 8px;color:var(--r2-smoke);font:var(--r2-caps);letter-spacing:.08em;text-transform:uppercase}
main:has(.chathead){padding:16px 16px calc(var(--nav-clear) + 48px + env(safe-area-inset-bottom))}
.chathead{display:flex;align-items:center;justify-content:space-between;gap:12px;min-height:76px;margin:0 0 16px}
.chatdisplay{margin:0;font:700 88px/.86 var(--r2-font-display);letter-spacing:-.05em;color:var(--r2-paper)}
.chatplus{width:52px;height:52px;flex:none;border:0;border-radius:999px;background:var(--r2-lime);color:var(--r2-fixed-ink);font:700 24px/1 var(--r2-font-display);letter-spacing:-.03em;cursor:pointer}
.chatlist{display:flex;flex-direction:column;gap:2px;margin:0 0 18px}
.chatlist a.chatrow{display:flex;gap:12px;align-items:center;min-height:64px;padding:10px 14px 10px 10px;border-radius:26px;background:transparent;color:inherit;text-decoration:none}
.chatlist a.chatrow .grow{flex:1;min-width:0}
.chatlist a.chatrow b{display:flex;gap:6px;align-items:center;font:700 15px/1.2 var(--r2-font-sans);color:var(--r2-paper)}
.chatlist a.chatrow small{display:block;margin-top:2px;color:var(--r2-smoke);font:600 12px/1.3 var(--r2-font-sans)}
.chatlist .mark{width:44px;height:44px;border-radius:999px;display:inline-flex;align-items:center;justify-content:center;background:var(--r2-sun);color:var(--r2-fixed-ink);font:700 18px/1 var(--r2-font-display);letter-spacing:-.03em;flex:none}
.chatlist .mark svg{width:22px;height:22px;display:block}
.chatlist .mark.lime{background:var(--r2-lime)}
.chatlist .mark.sky{background:var(--r2-sky)}
.chatlist .mark.grape{background:var(--r2-grape)}
.chatlist .mark.bubble{background:var(--r2-bubblegum)}
.chatlist .mark.mango{background:var(--r2-mango)}
.chatlist .count{padding:5px 10px;border-radius:999px;background:var(--r2-graphite);color:var(--r2-paper);font:700 11px/1 var(--r2-font-sans)}
.chatlist .chatside{display:flex;flex-direction:column;align-items:flex-end;gap:4px;flex:none}
.chatlist .chattime,.chatgo{color:var(--r2-smoke);font:600 11px/1.2 var(--r2-font-sans)}
.chatgo{font:700 16px/1 var(--r2-font-sans)}
.chatlist .unread{min-width:18px;padding:2px 7px;border-radius:999px;background:var(--r2-lime);color:var(--r2-fixed-ink);font:700 11px/16px var(--r2-font-sans);text-align:center}
.chatlist .chatmute{display:inline-flex;align-items:center;justify-content:center;color:var(--r2-smoke)}
.chatlist .chatmute svg{display:block;width:16px;height:16px}
.practcard{display:block;margin:8px 0 16px;padding:16px 18px 18px 20px;border-radius:34px;background:var(--r2-sun);color:var(--r2-fixed-ink);text-decoration:none}
.practcard .practtop{display:flex;justify-content:space-between;align-items:center;gap:8px;font:700 10px/1.2 var(--r2-font-sans);letter-spacing:.08em;text-transform:uppercase}
.practcard .unread{display:inline-flex;align-items:center;justify-content:center;box-sizing:border-box;height:20px;padding:3px 8px;border-radius:999px;background:var(--r2-fixed-ink);color:var(--r2-sun);font:700 11px/14px var(--r2-font-sans);letter-spacing:0;text-transform:none;flex:none}
.practcard .practbody{display:flex;align-items:flex-end;gap:10px;margin-top:8px}
.practcard .practtime{font:700 64px/.86 var(--r2-font-display);letter-spacing:-.05em}
.practcard .practmeta b{display:block;font:700 13px/1.2 var(--r2-font-sans)}
.practcard .practmeta small{display:block;font:600 12px/1.3 var(--r2-font-sans)}
dialog.newchat::backdrop,dialog.pickpeople::backdrop{background:rgba(11,11,12,.6)}
dialog.newchat .sheet,dialog.pickpeople .sheet{max-height:90dvh}
.newtitle{margin:0 0 12px;font:700 28px/1 var(--r2-font-display);letter-spacing:-.03em}
.newcard{display:flex;flex-direction:column;gap:2px;margin:0 0 16px;padding:6px;border-radius:26px;background:var(--r2-graphite)}
.newrow{display:flex;align-items:center;gap:12px;width:100%;min-height:64px;padding:8px 10px;border:0;border-radius:22px;background:transparent;color:var(--r2-paper);text-align:left;text-decoration:none;font:inherit;cursor:pointer}
.newrow b{display:block;font:700 15px/1.2 var(--r2-font-sans)}
.newrow small{display:block;margin-top:2px;color:var(--r2-smoke);font:600 12px/1.3 var(--r2-font-sans)}
dialog#chatActions .sheet,dialog.msgactions .sheet{background:var(--carbon);color:var(--paper);border-radius:28px 28px 0 0;padding:10px 16px 28px;gap:12px}
dialog#chatActions::backdrop,dialog.msgactions::backdrop{background:rgba(11,11,12,.6)}
dialog#chatActions .grab,dialog.msgactions .grab{width:40px;height:5px;border-radius:3px;background:var(--smoke)}
dialog#chatActions .acthead{display:flex;align-items:center;gap:12px;min-height:44px;margin:0 4px 16px}
dialog#chatActions .actmark{width:44px;height:44px;border-radius:14px;background:var(--lime);color:var(--ink);display:flex;align-items:center;justify-content:center;flex:none;font:700 18px/1 var(--r2-font-display)}
dialog#chatActions .acthead b{display:block;font:700 18px/1.1 var(--r2-font-display);color:var(--paper)}
dialog#chatActions .acthead small{display:block;margin-top:2px;font:500 12px/1.3 var(--r2-font-sans);color:var(--smoke)}
dialog#chatActions .actcards{display:flex;flex-direction:column;gap:12px}
dialog#chatActions .actcard{display:flex;flex-direction:column;gap:0;margin:0;padding:0;border-radius:20px;background:var(--graphite);overflow:hidden}
dialog#chatActions .actcard form{margin:0}
dialog#chatActions .newrow{min-height:52px;margin:0;padding:13px 16px;border-radius:0;gap:12px;background:transparent;color:var(--paper);text-align:left;justify-content:flex-start}
dialog#chatActions .newrow:focus,dialog#chatActions .newrow:focus-visible,dialog.msgactions .actrow:focus,dialog.msgactions .actrow:focus-visible,dialog.profmenu .newrow:focus,dialog.profmenu .newrow:focus-visible{outline:none}
dialog#chatActions .newrow b{font:600 16px/1.2 var(--r2-font-sans);color:inherit}
dialog#chatActions .newrow small{font:500 12px/1.3 var(--r2-font-sans);color:var(--smoke)}
dialog#chatActions .actico{width:24px;height:24px;flex:none;color:var(--paper)}
dialog#chatActions .actstatus,dialog#chatActions .chatgo{color:var(--smoke);font:600 13px/1 var(--r2-font-sans);flex:none}
dialog#chatActions .actrowdim{opacity:.4}
dialog#chatActions .newrow.actdanger{background:transparent;color:var(--team-cherry)}
dialog#chatActions .newrow.actdanger .actico{color:var(--team-cherry)}
dialog#chatActions .actfoot{margin:12px 4px 4px;color:var(--smoke);font:500 12px/1.4 var(--r2-font-sans)}
dialog#chatActions [hidden]{display:none !important}
dialog.msgactions .actgroup{background:var(--graphite);border-radius:20px;overflow:hidden;margin:0}
dialog.msgactions .emogrid{margin:4px 0 12px}
dialog.msgactions .emogrid button{background:var(--graphite);border:0;color:var(--paper)}
dialog.msgactions .actgroup .actrow{border-bottom:0;height:52px;padding:0 16px;color:var(--paper);font:600 16px/1.2 var(--r2-font-sans);justify-content:flex-start;gap:12px}
dialog.msgactions .actgroup .actrow svg{width:24px;height:24px}
dialog.msgactions .actrow.danger,dialog.msgactions .actrow.danger svg{color:var(--team-cherry);background:transparent}
dialog.profmenu .sheet{background:var(--carbon);color:var(--paper);border:0;border-radius:28px 28px 0 0;padding:10px 16px 28px}
dialog.profmenu .grab{width:40px;height:5px;border-radius:3px;background:var(--smoke)}
dialog.profmenu .newcard{background:var(--graphite);border-radius:20px;padding:0;margin:0 0 12px;gap:0;overflow:hidden}
dialog.profmenu .newrow{min-height:52px;padding:13px 16px;border-radius:0;text-align:left;justify-content:flex-start}
dialog.profmenu .newrow b{font:600 16px/1.2 var(--r2-font-sans)}
dialog.profmenu .newrow.actdanger{background:transparent;color:var(--team-cherry)}
.newrow .mark{width:44px;height:44px;border-radius:999px;display:inline-flex;align-items:center;justify-content:center;flex:none;font:700 14px/1 var(--r2-font-display);color:var(--r2-fixed-ink)}
.newrow .mark svg{width:22px;height:22px;display:block}
.newrow .mark.lime{background:var(--r2-lime)}
.newrow .mark.sky{background:var(--r2-sky)}
.newrow .mark.sun{background:var(--r2-sun)}
.newrow .mark.grape{background:var(--r2-grape)}
.newrow .mark.mango{background:var(--r2-mango)}
.newrow .mark.bubble{background:var(--r2-bubblegum)}
.newrow .mark.aqua{background:var(--r2-aqua)}
.mini{margin-left:8px;padding:5px 8px;border:1px solid var(--r2-smoke);border-radius:999px;color:var(--r2-smoke);font:700 10px/1 var(--r2-font-sans);letter-spacing:.04em;text-transform:uppercase}
dialog.pickpeople .sheet{background:var(--r2-carbon);border:0;border-radius:28px 28px 0 0;padding:10px 16px 28px;display:flex;flex-direction:column;gap:14px}
dialog.pickpeople .grab{width:40px;height:5px;margin:0 auto;padding:0;border-radius:3px;background:var(--r2-smoke)}
dialog.pickpeople .grab::after{content:none}
.pickhead{display:flex;align-items:center;justify-content:space-between;gap:8px;margin:0;width:100%}
.pickhead h2{margin:0;font:700 17px/1 var(--r2-font-display);color:var(--r2-paper)}
.pickhead button{border:0;background:transparent;color:var(--r2-smoke);font:600 15px/1 var(--r2-font-sans);padding:0}
#pickNext{height:auto;padding:8px 14px;border-radius:999px;background:var(--r2-lime);color:var(--r2-fixed-ink);font:700 14px/1 var(--r2-font-sans)}
#pickNext:disabled{opacity:.45}
#pickData{display:none !important}
.picksearch{display:flex;align-items:center;gap:10px;box-sizing:border-box;width:100%;height:48px;margin:0;padding:0 16px;border-radius:999px;background:var(--r2-graphite)}
.picksearch svg{flex:none;display:block}
dialog.pickpeople .picksearch input{flex:1;width:100%;height:auto;margin:0;padding:0;border:0;border-radius:0;background:transparent;color:var(--r2-paper);font:500 15px/1.2 var(--r2-font-sans)}
dialog.pickpeople .picksearch input::placeholder{color:var(--r2-smoke)}
.pickchips{display:flex;flex-wrap:wrap;gap:8px;margin:0;width:100%}
.pickchip{display:inline-flex;align-items:center;gap:6px;border:0;border-radius:999px;background:var(--r2-graphite);color:var(--r2-paper);padding:4px 10px 4px 4px;font:600 13px/1 var(--r2-font-sans)}
.pickchip .mark{width:24px;height:24px;border-radius:999px;display:inline-flex;align-items:center;justify-content:center;font:700 9px/1 var(--r2-font-sans);color:var(--r2-fixed-ink)}
.pickbox{box-sizing:border-box;width:24px;height:24px;border:1.5px solid var(--r2-smoke);border-radius:999px;background:transparent;display:inline-flex;align-items:center;justify-content:center;flex:none}
.pickbox svg{display:block}
.pickbox.on{background:var(--lime);border-color:var(--lime)}
dialog.pickpeople #pickList,dialog.pickpeople #pickRecent{display:flex;flex-direction:column;gap:0;background:var(--r2-graphite);border-radius:20px;overflow:hidden}
dialog.pickpeople #pickList:empty,dialog.pickpeople #pickRecent:empty{display:none}
dialog.pickpeople .newrow{min-height:0;padding:10px 14px;border-radius:0;gap:12px}
dialog.pickpeople .newrow .mark{width:40px;height:40px;font:700 14.4px/1 var(--r2-font-sans)}
dialog.pickpeople .newrow b{font:600 15px/1.2 var(--r2-font-sans)}
dialog.pickpeople .newrow small{margin-top:1px;font:500 12px/1.3 var(--r2-font-sans)}
dialog.pickpeople #pickTeam,dialog.pickpeople #pickRecentLabel{margin:0;font:700 11px/1 var(--r2-font-sans);letter-spacing:.88px}
dialog.pickpeople #pickFoot{margin:0;font:500 12px/1.35 var(--r2-font-sans);color:var(--r2-smoke)}
.plusacts{display:flex;flex-direction:column;gap:8px}
.plusacts button,.sheetcancel{width:100%;min-height:52px;border:0;border-radius:999px;background:var(--r2-graphite);color:var(--r2-paper);font:700 15px/1 var(--r2-font-sans)}
.sheetcancel{margin-top:8px;background:transparent;color:var(--r2-smoke)}
.hashfield{display:flex;align-items:center;gap:4px;min-height:52px;padding:0 16px;border-radius:16px;background:var(--r2-graphite);color:var(--r2-smoke);font:600 16px/1 var(--r2-font-sans)}
.hashfield input{flex:1;border:0;background:transparent;color:var(--r2-paper);font:inherit;padding:0}
.audchips{display:flex;flex-wrap:wrap;gap:8px;margin:0 0 12px}
.audchips button{border:0;border-radius:999px;padding:10px 14px;background:var(--r2-graphite);color:var(--r2-paper);font:700 13px/1 var(--r2-font-sans)}
.audchips button.on{background:var(--r2-lime);color:var(--r2-fixed-ink)}
.switchrow{display:flex;align-items:center;justify-content:space-between;gap:12px;padding:14px 0;border-top:1px solid var(--r2-graphite);font:700 15px/1.3 var(--r2-font-sans);color:var(--r2-paper)}
.switchrow small{display:block;margin-top:4px;color:var(--r2-smoke);font:600 12px/1.35 var(--r2-font-sans)}
button.switchrow{width:100%;border:0;background:transparent;text-align:left;cursor:pointer;color:inherit}
.switchrow .onword{color:var(--r2-lime);font:700 14px/1 var(--r2-font-sans);flex:none}
.switchrow .onword.off{color:var(--r2-smoke)}
.postchoices{display:flex;flex-direction:column;gap:8px;margin:0 0 8px}
.postchoices button{min-height:44px;border:0;border-radius:16px;background:var(--r2-graphite);color:var(--r2-paper);font:700 14px/1.2 var(--r2-font-sans);text-align:left;padding:0 14px}
.postchoices button.on{background:var(--r2-lime);color:var(--r2-fixed-ink)}
.peoplepick{display:flex;flex-direction:column;gap:4px;max-height:46vh;overflow:auto}
.peoplepick label{display:flex;align-items:center;gap:12px;min-height:52px;color:var(--r2-paper);font:700 15px/1.2 var(--r2-font-sans)}
.nav3-meta{display:inline-flex;align-items:center;justify-content:center;gap:6px;flex:none;min-width:max-content;max-width:none;white-space:nowrap}
.nav3-label{white-space:nowrap;flex:none}
.nav3-badge{position:absolute;top:2px;right:2px;box-sizing:border-box;display:inline-flex;align-items:center;justify-content:center;min-width:16px;height:16px;padding:0 4px;border-radius:999px;background:var(--r2-lime);color:var(--r2-fixed-ink);font:700 10px/1 var(--r2-font-sans);text-align:center}
.nav3-tabs a.on .nav3-badge{position:static;top:auto;right:auto;flex:none;min-width:20px;height:20px;padding:0 5px;background:var(--r2-fixed-ink);color:var(--r2-lime);font-size:12.5px}
.nav3-tabs a.on .nav3-label{min-width:max-content;white-space:nowrap;flex:none}
.chatlock{margin:12px 0;padding:12px 14px;border-radius:16px;background:var(--r2-carbon);color:var(--r2-smoke);font:600 13px/1.4 var(--r2-font-sans)}
.pchatbar{display:flex;align-items:center;justify-content:space-between;gap:12px;margin:0 0 12px}
.pchatbar a,.askcoach{color:var(--r2-paper);font:700 15px/1.2 var(--r2-font-sans);text-decoration:none}
.askcoach{border:0;background:transparent;padding:0;cursor:pointer}
.datechip{display:inline-flex;align-items:center;height:36px;padding:0 14px;border-radius:999px;background:var(--r2-carbon);color:var(--r2-paper)}
.chatsearch{margin:0 0 16px}
.chatsearch input{width:100%;border-radius:999px;background:var(--r2-carbon);color:var(--r2-paper);border:0;padding:14px 16px}
.chatlist a.upnext{background:var(--r2-sun);color:var(--r2-fixed-ink);border-radius:26px}
.chatlist a.upnext b,.chatlist a.upnext small,.chatlist a.upnext .chattime{color:var(--r2-fixed-ink)}
.chatlist a.upnext .mark{background:var(--r2-sun);color:var(--r2-fixed-ink)}
.chatlist a.upnext .unread{background:var(--r2-fixed-ink);color:var(--r2-paper)}
.histlist .mark{width:48px;height:48px;font:700 18px/1 var(--r2-font-display)}
.searchpill{margin:18px 0 0}
.searchpill input{width:100%;height:56px;margin:0;border-radius:999px;border:1.5px solid var(--r2-graphite);background:transparent;text-align:center;color:var(--r2-paper);font:700 16px/1 var(--r2-font-sans)}
.searchpill input::placeholder{color:var(--r2-paper);opacity:1}
.chatlist .mark.graphite{background:var(--r2-graphite);color:var(--r2-paper)}
@media (min-width:768px){
 dialog.newchat,dialog.pickpeople{position:fixed;width:340px;height:auto;max-height:90dvh;inset:auto;margin:0}
 dialog.newchat .sheet,dialog.pickpeople .sheet{border-radius:24px;border:1px solid var(--r2-graphite);max-height:min(90dvh,640px)}
 dialog.newchat .grab,dialog.pickpeople .grab{display:none}
 body:has(nav.nav3){padding-left:var(--r2-rail);--nav-clear:16px;--nav-offset-bottom:0px}
 nav.nav3{top:0;bottom:0;left:0;right:auto;width:var(--r2-rail);height:auto;flex-direction:column;align-items:center;justify-content:flex-start;gap:10px;padding:24px 0;border-radius:0;overflow:visible;background:var(--r2-carbon);-webkit-backdrop-filter:none;backdrop-filter:none;touch-action:auto}
 .nav3-crest,.nav3-crest-face{width:60px;height:60px}
 .nav3-crest-face{font-size:22px;letter-spacing:-0.66px}
 .nav3-more{display:none}
 .nav3-menu-label{display:block;margin:0;color:var(--r2-smoke);font:700 9px/normal var(--r2-font-sans)}
 .nav3-rule{display:block;width:40px;height:2px;background:var(--r2-graphite)}
 .nav3-tabs{flex:none;flex-direction:column;justify-content:flex-start;width:76px;height:auto;gap:10px;padding-right:0}
 nav.nav3:has(.nav3-tabs>a:nth-child(5)){gap:6px}
 nav.nav3:has(.nav3-tabs>a:nth-child(5)) .nav3-tabs{gap:6px}
 .nav3-slide{border-radius:22px}
 nav.nav3::before{content:none}
 .nav3-tabs a,.nav3-tabs a.on,nav.nav3:has(.nav3-tabs>a:nth-child(5)) .nav3-tabs a,nav.nav3:has(.nav3-tabs>a:nth-child(5)) .nav3-tabs a.on{width:76px;flex-basis:auto;min-width:0;height:auto;flex:none;flex-direction:column;gap:4px;padding:10px 6px;border-radius:22px;background:transparent;color:var(--r2-smoke);font:700 11px/normal var(--r2-font-sans)}
 .nav3-tabs a.on{padding:10px 6px;background:transparent;color:var(--r2-fixed-ink)}nav.nav3 .nav3-tabs a.on,nav.nav3:has(.nav3-tabs>a:nth-child(5)) .nav3-tabs a.on{color:var(--r2-fixed-ink)}
 body:has(nav.nav3) .composer,body:has(nav.nav3).homefull .homemap{left:var(--r2-rail)}
 dialog.crestmenu{top:24px;left:108px;bottom:auto;width:340px}
}
@media (min-width:1280px){
 body:has(nav.nav3){padding-left:260px}
 nav.nav3{width:260px;align-items:stretch;gap:4px;padding:24px 16px}
 .nav3-crest{width:100%;height:auto;justify-content:flex-start;padding:8px 14px 8px 8px;background:var(--r2-graphite)}
 .nav3-crest-face{width:40px;height:40px;font-size:14px;letter-spacing:-0.42px}
 nav.nav3[data-place="everything"] .nav3-crest-face{background:var(--r2-lime);border:0}
 nav.nav3[data-place="everything"] .nav3-logo.lg{display:none}
 nav.nav3[data-place="everything"] .nav3-logo.sm.ink{display:block;width:26px;height:10px}
 .nav3-menu-label,.nav3-rule,.nav3-more{display:none}
 .nav3-glyph{display:block}
 .nav3-dot{display:none}
 .nav3-switch-copy{display:flex;flex:1;flex-direction:column;min-width:0;text-align:left}
 .nav3-switch-copy b{font:700 13px/normal var(--r2-font-sans);color:var(--r2-paper)}
 .nav3-switch-copy small{font:600 10px/normal var(--r2-font-sans);color:var(--r2-smoke)}
 .nav3-chevron{display:block;font:700 10px/normal var(--r2-font-sans);color:var(--r2-smoke)}
 .nav3-chevron::before{content:"▼"}
 .nav3-crest[aria-expanded="true"] .nav3-chevron::before{content:"▲"}
 .nav3-tabs{width:100%;align-items:stretch;margin-top:22px;gap:8px}
 nav.nav3:has(.nav3-tabs>a:nth-child(5)) .nav3-tabs{gap:4px}
 .nav3-slide{border-radius:var(--r2-radius-pill)}
 .nav3-tabs a,.nav3-tabs a.on,nav.nav3:has(.nav3-tabs>a:nth-child(5)) .nav3-tabs a,nav.nav3:has(.nav3-tabs>a:nth-child(5)) .nav3-tabs a.on{width:100%;flex:none;flex-basis:auto;min-width:0;height:auto;flex-direction:row;justify-content:flex-start;gap:10px;padding:10px 14px;border-radius:var(--r2-radius-pill);background:transparent;color:var(--r2-paper);font:700 14px/normal var(--r2-font-sans)}
 .nav3-dot{display:block;width:14px;height:14px;box-sizing:border-box;border:2px solid var(--r2-smoke);border-radius:var(--r2-radius-pill);flex:none}
 .nav3-tabs a.on{background:transparent;color:var(--r2-fixed-ink)}
 .nav3-tabs a.on .nav3-dot{border-color:var(--r2-fixed-ink)}
 nav.nav3 .nav3-tabs a.on,nav.nav3:has(.nav3-tabs>a:nth-child(5)) .nav3-tabs a.on{color:var(--r2-fixed-ink)}
 body:has(nav.nav3) .composer,body:has(nav.nav3).homefull .homemap{left:260px}
 dialog.crestmenu{top:84px;left:16px;width:340px}
}
@media (prefers-reduced-motion:reduce){
 .nav3-slide,.nav3-tabs a,.nav3-glyph,.nav3-label{transition:none}
}
button.earlier{width:100%;height:auto;min-height:0;margin:0;padding:8px 0 4px;background:none;color:var(--t3);font-size:13px;font-weight:650}.chatin{display:flex;flex-direction:column;justify-content:flex-end;min-height:100%;width:100%;min-width:0}.chat{display:block;flex:1;min-height:0;overflow-x:hidden;overflow-y:auto;overflow-anchor:auto;overscroll-behavior:contain;scrollbar-width:none}.chat.scrolling{scrollbar-width:thin;scrollbar-color:rgba(246, 244, 239,.45) transparent}.chat::-webkit-scrollbar{width:0;height:0}.chat.scrolling::-webkit-scrollbar{width:8px;height:8px}.chat.scrolling::-webkit-scrollbar-thumb{background:rgba(246, 244, 239,.4);border-radius:8px}.m{position:relative;-webkit-touch-callout:none;margin-top:14px;display:flex;flex-direction:column;align-items:flex-start}.m.g-mid,.m.g-last{margin-top:2px}.chat>.m:first-child{margin-top:auto}.m .who{font-size:13px;color:var(--t3);margin:0 0 3px}.m .txt{background:var(--color-bubble);border-radius:var(--radius-card);padding:10px 14px;display:inline-block;max-width:85%;white-space:pre-wrap;word-wrap:break-word;color:var(--color-text)}.m .txt a.msglink{color:var(--accent);text-decoration:none}
.m.g-first:not(.mine) .txt,.m.g-first:not(.mine) .img img{border-bottom-left-radius:5px}.m.g-mid:not(.mine) .txt,.m.g-mid:not(.mine) .img img{border-top-left-radius:5px;border-bottom-left-radius:5px}.m.g-last:not(.mine) .txt,.m.g-last:not(.mine) .img img{border-top-left-radius:5px}
.m.g-first.mine .txt,.m.g-first.mine .img img{border-bottom-right-radius:5px}.m.g-mid.mine .txt,.m.g-mid.mine .img img{border-top-right-radius:5px;border-bottom-right-radius:5px}.m.g-last.mine .txt,.m.g-last.mine .img img{border-top-right-radius:5px}
.m.mine{text-align:right;align-items:flex-end}.m.mine .txt{background:var(--color-bubble-mine);text-align:left;color:var(--color-text)}.m.ann{align-items:stretch}.m.ann .txt{display:block;max-width:none;border:1px solid var(--line);background:var(--surface)}
.m .txt.deleted{font-style:italic;font-size:12px;font-weight:500;line-height:1.3;color:var(--t3);background:transparent;padding:0}.m .edited{font-size:12px;color:var(--t3);font-weight:400}
.m .more{display:none;position:absolute;top:-4px;right:0;width:32px;height:32px;padding:0;background:none;color:var(--t3);font-size:18px}
.m.mine .more{left:0;right:auto}
@media (hover:hover) and (pointer:fine){.m:hover .more{display:inline-flex}}
.m .editbox textarea{min-height:72px;height:auto;margin:0}
.composer{position:fixed;left:0;right:0;bottom:calc(var(--nav-clear) + env(safe-area-inset-bottom));background:transparent;padding:0 16px 8px;border:0;z-index:10}
.chatpad{flex:none;height:calc(var(--composer-h, 76px) + var(--nav-clear) + env(safe-area-inset-bottom) + 12px)}
.composer form{max-width:640px;margin:0 auto;display:flex;align-items:center;gap:10px;min-height:60px;padding:6px 6px 6px 20px;border-radius:999px;background:var(--r2-graphite);box-sizing:border-box}
.composer textarea{flex:1;align-self:center;margin:0;height:44px;min-height:44px;max-height:120px;border:0;background:transparent;color:var(--r2-paper);resize:none;font:600 15px/22px var(--r2-font-sans);padding:11px 0;overflow-y:auto;scrollbar-width:none;-ms-overflow-style:none;box-sizing:border-box}
.composer textarea::placeholder{color:var(--r2-smoke);font:600 15px/22px var(--r2-font-sans)}
.threadbar{display:flex;align-items:center;gap:8px;min-height:48px;margin:0 0 8px}
.threadbar button{border:0;background:transparent;padding:0;color:var(--r2-paper);font:700 17px/1.2 var(--r2-font-sans);cursor:pointer}
.threadmore{display:none;margin-left:auto;width:36px;height:36px;border-radius:999px;align-items:center;justify-content:center;font:700 20px/1 var(--r2-font-sans)}
@media (min-width:768px){.threadmore{display:inline-flex}}
.chead{display:flex;align-items:center;gap:10px;height:48px;margin:0 0 8px;padding:4px 0;box-sizing:border-box}
.cheadback,.cheadmore{width:40px;height:40px;flex:none;border:0;border-radius:999px;background:var(--r2-graphite);color:var(--r2-paper);display:inline-flex;align-items:center;justify-content:center;padding:0;text-decoration:none;cursor:pointer}
.cheadmore{margin-left:0;font:700 13px/1 var(--r2-font-sans);letter-spacing:.12em}
.cheadmark{width:40px;height:40px;flex:none;border-radius:12px;display:inline-flex;align-items:center;justify-content:center;overflow:hidden;background:var(--r2-lime);color:var(--r2-fixed-ink);font:700 18px/1 var(--r2-font-display)}
.cheadmark img{width:100%;height:100%;object-fit:cover;display:block}
.cheadmark.sun{background:var(--r2-sun)}.cheadmark.mango{background:var(--r2-mango)}.cheadmark.bubble{background:var(--r2-bubblegum)}.cheadmark.grape{background:var(--r2-grape)}.cheadmark.sky{background:var(--r2-sky)}.cheadmark.lime{background:var(--r2-lime)}
.cheadname{flex:1;min-width:0;display:flex;flex-direction:column;align-items:flex-start;gap:1px;border:0;background:transparent;padding:0;text-align:left;cursor:pointer;color:inherit}
.cheadname b{display:block;max-width:100%;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;font:700 18px/1 var(--r2-font-display);color:var(--r2-paper)}
.cheadname small{display:block;max-width:100%;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;font:500 12px/1.2 var(--r2-font-sans);color:var(--r2-smoke)}
@media (min-width:768px){.cheadback{display:none}}
.daydiv{align-self:center;text-align:center;margin:18px auto 6px;color:var(--smoke);font:700 10px/1.3 var(--r2-font-sans);letter-spacing:.08em}
.exact{display:none;margin-top:3px;color:var(--smoke);font:700 11px/1.2 var(--r2-font-sans)}
.m.showtime .exact{display:block}
@media (hover:hover) and (pointer:fine){.m:hover .exact{display:block}}
.m:not(.mine) .rx{justify-content:flex-end}
.m.mine .rx{justify-content:flex-start}
.reqbar{display:flex;flex-wrap:wrap;align-items:center;gap:8px 10px;background:var(--team-lavender);color:var(--graphite);border-radius:20px;padding:12px 14px;margin:0 0 8px}
.reqbar button,.reqbar a{color:var(--graphite);font:700 17px/1.2 var(--r2-font-sans);text-decoration:none}
.reqbar .reqback{flex:none;font:700 13px/1 var(--r2-font-sans)}
.reqbar .datechip{margin-left:auto;background:var(--paper);color:var(--graphite);height:32px}
.reqbar #threadName{flex-basis:100%;text-align:left}
.reqtop{display:flex;align-items:center;gap:8px;width:100%}
.reqsubject{display:block;width:100%;border:0;background:transparent;padding:0;text-align:left;cursor:pointer;font:700 32px/1 var(--r2-font-display);letter-spacing:-.03em;color:var(--graphite)}
.reqmeta{flex-basis:100%;margin:0}
.reqchip{display:inline-flex;align-items:center;margin-left:8px;padding:3px 8px;border-radius:999px;background:var(--team-grape);color:var(--paper);font:700 10px/1.2 var(--r2-font-sans);letter-spacing:.08em;text-transform:uppercase}
.reqmeta{margin:4px 0 0;color:var(--team-grape);font:600 12px/1.3 var(--r2-font-sans)}
.resolvebar{position:fixed;z-index:11;left:16px;right:16px;max-width:640px;margin:0 auto;bottom:calc(var(--nav-clear) + env(safe-area-inset-bottom) + var(--composer-h, 76px) + 8px);display:flex;flex-wrap:wrap;gap:8px;align-items:center;padding:8px 10px;border-radius:16px;background:var(--r2-graphite);color:var(--r2-paper);font:600 13px/1.2 var(--r2-font-sans)}
.resolvebar select,.resolvebar button{height:36px;border-radius:999px;border:0;padding:0 12px;font:700 13px/1 var(--r2-font-sans)}
.resolvebar button{background:var(--r2-lime);color:var(--r2-fixed-ink)}
body:has(.resolvebar) .chatpad{height:calc(var(--composer-h, 76px) + var(--nav-clear) + env(safe-area-inset-bottom) + 72px)}
.actnote{margin:0;padding:8px 10px;color:var(--r2-smoke);font:600 12px/1.3 var(--r2-font-sans)}
.newrow.danger{color:var(--team-tangerine)}
button.newrow.actdanger,button.newrow.actdanger b{background:transparent;color:var(--team-tangerine);box-shadow:none;font-weight:700}
@media (min-width:768px){
 dialog.botsheet.popover{width:340px;height:auto;max-height:90dvh;inset:auto;margin:0}
 dialog.botsheet.popover .sheet{border-radius:24px;border-bottom:1px solid var(--r2-graphite);max-height:min(90dvh,640px)}
 dialog.botsheet.popover .grab{display:none}
}
.composer textarea::-webkit-scrollbar{display:none}.iconbtn{width:44px;height:44px;padding:0;flex:none;border:0;border-radius:999px;background:var(--r2-lime);color:var(--r2-fixed-ink);font:700 28px/44px var(--r2-font-display)}.iconbtn svg{width:24px;height:24px;display:block}
.iconbtn.send.ready{font-size:22px}
.thumbs{display:flex;gap:8px;max-width:640px;margin:0 auto 8px;overflow:auto}
.thumbs figure{position:relative;margin:0;flex:none}
.thumbs img{width:72px;height:72px;object-fit:contain;border-radius:16px;display:block;background:var(--r2-graphite)}
.thumbs button{position:absolute;top:-4px;right:-4px;width:22px;height:22px;border:0;border-radius:999px;background:var(--r2-ink);color:var(--r2-paper);font:700 12px/22px var(--r2-font-sans)}
.attachphone{display:flex;flex-direction:column;gap:14px;width:100%}
.attachhead h2,.attachwidehead h2{margin:0;font:700 20px/1.2 var(--r2-font-display);color:var(--r2-paper);letter-spacing:0}
.attachsub{margin:4px 0 0;color:var(--r2-smoke);font:500 13px/1.3 var(--r2-font-sans)}
.attachtiles{display:flex;gap:12px;margin:0}
dialog.attachsheet button.attachtile{flex:1;min-width:0;height:auto;min-height:0;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:10px;padding:20px 16px;border:0;border-radius:20px;background:var(--r2-graphite);color:var(--r2-paper);font:600 15px/1.2 var(--r2-font-sans)}
.attachico{width:48px;height:48px;border-radius:24px;background:var(--r2-lime);display:flex;align-items:center;justify-content:center;flex:none}
.attachico img,.attachbrowse img{width:24px;height:24px;display:block}
dialog.attachsheet button.attachcancel{width:100%;height:52px;min-height:52px;padding:0;border:0;border-radius:999px;background:var(--r2-graphite);color:var(--r2-paper);font:600 16px/1 var(--r2-font-sans)}
.attachwide{display:none}
.attachwidehead{display:flex;align-items:center;gap:8px;width:100%}
dialog.attachsheet button.attachx{width:32px;height:32px;min-height:32px;padding:0;border:0;border-radius:999px;background:transparent;color:var(--r2-smoke);font:600 18px/1 var(--r2-font-sans)}
.attachdrop{box-sizing:border-box;height:200px;border:2px dashed var(--r2-smoke);border-radius:20px;background:var(--r2-graphite);display:flex;flex-direction:column;align-items:center;justify-content:center;gap:10px;padding:24px;text-align:center}
.attachdrop .hot{display:none}
.attachdrop.over{border-style:solid;border-color:var(--r2-lime);background:color-mix(in srgb,var(--r2-lime) 12%,transparent)}
.attachdrop.over .idle{display:none}
.attachdrop.over .hot{display:flex;flex-direction:column;align-items:center;gap:6px}
.attachdrop b{font:700 16px/1.2 var(--r2-font-sans);color:var(--r2-paper)}
.attachcount{margin:0;color:var(--r2-smoke);font:500 13px/1.2 var(--r2-font-sans)}
dialog.attachsheet button.attachbrowse{height:auto;min-height:0;display:inline-flex;align-items:center;gap:8px;padding:10px 18px;border:0;border-radius:999px;background:var(--r2-paper);color:var(--r2-carbon);font:600 14px/1 var(--r2-font-sans)}
.attachnote{margin:0;color:var(--r2-smoke);font:500 12px/1.35 var(--r2-font-sans)}
.attacherr{margin:0;color:var(--r2-tangerine);font:600 13px/1.3 var(--r2-font-sans)}
.attacherr[hidden]{display:none}
.fileclip{position:fixed;left:0;top:0;width:1px;height:1px;margin:0;padding:0;border:0;opacity:0;overflow:hidden;clip:rect(0,0,0,0);clip-path:inset(50%)}
dialog.attachsheet{width:min(640px,100%)}
dialog.attachsheet:focus{outline:none}
dialog.attachsheet::backdrop{background:rgba(11,11,12,.6)}
dialog.attachsheet .sheet{background:var(--r2-carbon);color:var(--r2-paper);border:0;border-radius:28px 28px 0 0;padding:10px 16px calc(28px + env(safe-area-inset-bottom));display:flex;flex-direction:column;gap:14px}
dialog.attachsheet .grab{height:5px;margin:0 0 0;padding:0;background:transparent}
dialog.attachsheet .grab::after{top:0;width:40px;height:5px;margin-left:-20px;background:var(--r2-smoke)}
.dropcard{position:fixed;z-index:40;left:50%;top:50%;transform:translate(-50%,-50%);width:min(420px,calc(100vw - 32px));padding:20px;border-radius:28px;background:var(--r2-carbon);box-shadow:0 16px 48px rgba(11, 11, 12,.35);pointer-events:none}
.dropcard[hidden]{display:none}
.chat{position:relative}
.msgfoot{display:flex;align-items:center;gap:8px;margin-top:4px}
.msgtime{color:var(--r2-smoke);font:600 11px/1.2 var(--r2-font-sans)}
@media (min-width:768px){
 dialog.attachsheet{width:420px;height:auto;max-height:none;inset:auto;margin:0}
 dialog.attachsheet .sheet{border-radius:28px;padding:20px}
 dialog.attachsheet .grab,dialog.attachsheet .attachphone{display:none}
 dialog.attachsheet .attachwide{display:flex;flex-direction:column;gap:14px;width:100%}
}
.m .img{display:block;margin:0;width:min(66%,260px);max-width:min(66%,260px);height:auto;aspect-ratio:auto;max-height:min(70vh,520px)}.m .txt+.img{margin-top:4px}.m.mine .img,.m.mine .mstack>.img{margin-left:auto;align-self:flex-end}.m .img img{width:100%;height:auto;max-width:100%;max-height:min(70vh,520px);object-fit:contain;border-radius:20px;display:block;background:transparent}
.m .bubble{display:inline-block;max-width:min(85%,280px);background:var(--color-bubble);border-radius:var(--radius-card);overflow:hidden}.m.mine .bubble{background:var(--color-bubble-mine)}.m .bubble .txt{background:transparent;display:block;max-width:min(70vw,280px);border-radius:0}.m .bubble .img,.m .bubble .txt+.img{margin:0}.m .bubble .img img{border-radius:0}
.mstack{display:inline-flex;flex-direction:column;align-items:stretch;align-self:flex-start;width:max-content;max-width:85%;min-width:0}
.m.mine .mstack{align-self:flex-end}
.m.ann .mstack{display:flex;width:100%;max-width:none;align-self:stretch}
.m .mstack>.txt{max-width:none;align-self:stretch;min-width:0}
.m .mstack>.bubble{align-self:stretch;min-width:0;width:max-content;max-width:min(70vw,280px)}
.m .mstack>.img{align-self:flex-start;min-width:0;width:min(66%,260px);max-width:min(66%,260px);margin-left:0;margin-right:0}
.m.mine .mstack>.img{align-self:flex-end;margin-left:auto;margin-right:0}
.m .mstack>.quotechip{width:0;min-width:100%;max-width:100%;box-sizing:border-box;overflow:hidden}
.msgfoot{display:flex;align-items:center;gap:8px;width:0;min-width:100%;max-width:100%;box-sizing:border-box;align-self:stretch;flex-wrap:nowrap;overflow:hidden}
.msgfoot:has(.rx:not(:empty)){margin-top:6px}.msgfoot:has(.seenline){margin-top:3px}
.rx{display:flex;flex-wrap:nowrap;gap:6px;margin:0;flex:1 1 auto;min-width:0;justify-content:flex-start;overflow:hidden}
.seenline{display:block;width:fit-content;max-width:100%;min-width:0;height:auto;min-height:1.3em;margin:0 0 0 auto;padding:0;background:none;border:0;border-radius:0;color:var(--t3);font-size:12px;font-weight:500;line-height:1.3;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;flex:0 1 auto;align-self:flex-start}
span.avatar.seenav,span.avatar.seenav img{width:32px;height:32px;min-width:32px;max-width:32px;min-height:32px;max-height:32px;flex:0 0 32px;font-size:12px}
.seenrow{display:flex;align-items:center;gap:10px;min-height:40px}
.seenlist{max-height:38vh;overflow:auto}
.seenh{margin:14px 0 6px;font-size:13px;font-weight:650;color:var(--t3);letter-spacing:.02em}
.rx button{height:30px;min-height:30px;padding:0 10px;border-radius:999px;font-size:14px;font-weight:500;background:var(--surface);color:var(--t2);border:1px solid var(--line);white-space:nowrap;flex:none}
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
dialog#chatActions .grab,dialog.msgactions .grab,dialog.botsheet.profmenu .grab{display:block;width:40px;height:5px;margin:2px auto 0;padding:0;position:relative;top:auto;z-index:0;background:var(--smoke);border-radius:3px;flex:none}
dialog#chatActions .grab::after,dialog.msgactions .grab::after,dialog.botsheet.profmenu .grab::after{content:none}
dialog.botsheet.profmenu .sheet{background:var(--carbon);color:var(--paper);border:0;border-radius:28px 28px 0 0;padding:10px 16px 28px}
dialog.botsheet.attachsheet::backdrop{background:rgba(11,11,12,.6)}
dialog.botsheet.attachsheet .sheet{background:var(--r2-carbon);color:var(--r2-paper);border:0;border-radius:28px 28px 0 0;padding:10px 16px calc(28px + env(safe-area-inset-bottom));gap:14px}
dialog.botsheet.attachsheet .grab{height:5px;margin:0;padding:0;background:transparent;position:relative}
dialog.botsheet.attachsheet .grab::after{top:0;width:40px;height:5px;margin-left:-20px;background:var(--r2-smoke)}
/* 2.0 / Sheet (Figma 02 Components · H · Sheets, pickers & selects): every slide-up uses this.
   Carbon sheet, 28px top corners, 10/16/28 padding, 40x5 grabber, 22px title, graphite 20px groups, 52px rows. */
dialog.botsheet::backdrop{background:rgba(11,11,12,.6)}
dialog.botsheet .sheet{background:var(--carbon);color:var(--paper);border:0;border-radius:28px 28px 0 0;padding:10px 16px calc(28px + env(safe-area-inset-bottom))}
dialog.botsheet .grab{background:var(--carbon);height:20px;margin:0 0 6px}
dialog.botsheet .grab::after{top:0;width:40px;height:5px;margin-left:-20px;border-radius:3px;background:var(--smoke)}
dialog.botsheet .sheet>h2,dialog.botsheet .sheet>form>h2,dialog.botsheet .sheet .newtitle,dialog.botsheet .sheet .attachhead h2{margin:0 0 4px;font:700 22px/1.1 var(--r2-font-display);letter-spacing:-.02em;color:var(--paper)}
dialog.botsheet .sheet :is(.ty-muted,.attachsub,.t3){color:var(--smoke)}
dialog.botsheet .sheet>form,dialog.botsheet form.sheet{display:grid;gap:14px}
dialog.botsheet .newcard,dialog.botsheet .actgroup{background:var(--graphite);border-radius:20px;padding:0;margin:0 0 12px;gap:0;overflow:hidden}
dialog.botsheet .newcard .newrow{height:auto}
dialog.botsheet :is(.newrow,.actrow):focus{outline:none}dialog.botsheet :is(.newrow,.actrow):focus-visible{background:color-mix(in srgb,var(--paper) 8%,transparent)}
dialog.botsheet .newcard .newrow,dialog.botsheet .actgroup .actrow{min-height:52px;padding:13px 16px;border-radius:0;border-bottom:0;background:transparent;color:var(--paper);font:600 16px/1.2 var(--r2-font-sans);justify-content:flex-start;gap:12px}
dialog.botsheet .newcard .newrow small{font:500 13px/1.3 var(--r2-font-sans);color:var(--smoke)}
dialog.botsheet :is(.newrow.actdanger,.actrow.danger),dialog.botsheet :is(.newrow.actdanger,.actrow.danger) :is(svg,b){color:var(--team-cherry)}
dialog.botsheet .emogrid{background:var(--graphite);border-radius:26px;padding:6px 8px;margin:0 0 12px}
dialog.botsheet .emogrid button{background:transparent;color:var(--paper);border:0}
dialog.botsheet .attachopt{background:var(--graphite);color:var(--paper);border:0}
dialog.botsheet :is(.sheet,.sheet>form,form.sheet)>:is(.btn,.rg-btn){width:100%;min-height:52px;border-radius:999px}
dialog.botsheet :is(.sheet,.sheet>form,form.sheet)>:is(.btn-secondary,.rg-btn.secondary),dialog.botsheet .attachcancel{background:var(--graphite);color:var(--paper);border:0}
dialog.botsheet .newcard,dialog.botsheet .newcard>*,dialog.botsheet .actgroup>*{flex-shrink:0}
dialog.botsheet.profmenu .grab,dialog#chatActions .grab,dialog.msgactions .grab{margin-bottom:14px}
@media (prefers-reduced-motion:reduce){dialog.botsheet::backdrop,dialog.botsheet .sheet{transition:none}}
@media (min-width:768px){
 dialog.botsheet.newchat,dialog.botsheet.pickpeople{width:340px;height:auto;max-height:90dvh;inset:auto;margin:0}
 dialog.botsheet.newchat .sheet,dialog.botsheet.pickpeople .sheet{border-radius:24px;border:1px solid var(--r2-graphite);border-bottom:1px solid var(--r2-graphite);max-height:min(90dvh,640px)}
 dialog.botsheet.newchat .grab,dialog.botsheet.pickpeople .grab{display:none}
 dialog.botsheet.attachsheet{width:420px;height:auto;max-height:none;inset:auto;margin:0}
 dialog.botsheet.attachsheet .sheet{border-radius:28px;border:0;padding:20px;max-height:none}
 dialog.botsheet.attachsheet .grab,dialog.botsheet.attachsheet .attachphone{display:none}
 dialog.botsheet.attachsheet .attachwide{display:flex}
}
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
.lightbox{position:fixed;inset:0;background:var(--color-lightbox);display:flex;flex-direction:column;align-items:center;justify-content:center;gap:16px;z-index:20;padding:16px}.lightbox img{max-width:96vw;max-height:80vh;border-radius:8px}.lightbox .savephoto{flex:none}
.gobtn{background:none;height:auto;padding:4px 0;color:var(--t2);font-weight:500;font-size:14px}.gobtn::after{content:" ›";color:var(--t3)}
.ci-name,a.ci-name{flex:1;min-width:0;height:auto;padding:0;background:none;display:flex;align-items:center;gap:12px;text-align:left;font-weight:400;color:inherit;text-decoration:none}
.personrow{align-items:center;min-height:60px}
.personrow .ci-name{align-items:center}
.personrow>form,.personrow>.more{flex:none;align-self:center;margin:0}
.personrow .menu{left:auto;right:0}
.coachbody{display:flex;flex-direction:column;justify-content:center;align-items:stretch;gap:2px;min-width:0;flex:1;align-self:center;margin:0}
.coachbody>:first-child{margin-top:0}
.coachline{display:flex;align-items:center;gap:8px;min-width:0;width:100%;min-height:24px}
.coachplan{margin:0}
button.coachopen{display:flex;flex-direction:column;align-items:flex-start;justify-content:center;height:auto;min-height:0;width:auto;flex:1;padding:0;margin:0;background:transparent;border-radius:0;font-weight:400;color:inherit;text-align:left;gap:2px}
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
.plancards{display:flex;flex-direction:column;gap:8px;margin:0 0 16px}
label.plancard{position:relative;display:flex;align-items:flex-start;gap:12px;width:100%;min-height:72px;margin:0;padding:14px 16px;border-radius:var(--radius-card);background:var(--color-surface);border:1px solid var(--color-control);box-shadow:inset 0 0 0 1px transparent;color:var(--color-text);font-size:16px;font-weight:400;line-height:1.3;text-align:left;cursor:pointer}
label.plancard input{position:absolute;width:1px;height:1px;margin:0;padding:0;opacity:0}
label.plancard .planmark{flex:none;width:22px;height:22px;margin-top:1px;border-radius:50%;border:1.5px solid var(--color-control);display:inline-flex;align-items:center;justify-content:center;color:var(--color-forest)}
label.plancard .planmark svg{opacity:0}
label.plancard:has(input:checked){border-color:var(--color-lime);box-shadow:inset 0 0 0 1px var(--color-lime)}
label.plancard:has(input:checked) .planmark{background:var(--color-lime);border-color:var(--color-lime)}
label.plancard:has(input:checked) .planmark svg{opacity:1}
label.plancard .plantxt{display:flex;flex-direction:column;gap:2px;min-width:0}
label.plancard .plantxt b{font-size:16px;font-weight:650}
label.plancard .plantxt span{color:var(--color-text-secondary);font-size:13px;font-weight:400;line-height:1.35}
.livetitle{display:flex;align-items:center;justify-content:space-between;gap:var(--space-3);margin:0 0 var(--space-4)}
.livetitle strong{font-size:var(--type-t3-size);line-height:var(--type-t3-line);font-weight:var(--type-t3-weight)}
button.setrow{width:100%;height:auto;min-height:60px;padding:14px 18px;border-radius:0;background:transparent;color:var(--color-text);font-weight:500;justify-content:space-between;text-align:left}
button.setrow .sum{color:var(--color-text-secondary);font-weight:400;font-size:var(--type-b2-size)}
label:has(> .locok){display:flex;flex-wrap:wrap;align-items:center;column-gap:8px}
label:has(> .locok)>.placefield,label:has(> .locok)>input,label:has(> .locok)>.placeaddr{flex:1 0 100%;min-width:100%}
.placeaddr{margin:6px 0 0}
.locok{display:inline-flex;align-items:center;gap:6px;margin:0;color:var(--color-status-cleared);font-size:var(--type-b2-size);line-height:1}
.placefield{position:relative;display:block}
.placedrop{position:absolute;z-index:25;left:0;right:0;top:calc(100% + 4px);max-height:min(320px,60vh);overflow:auto;background:var(--color-sheet);border:1px solid var(--color-sheet-border);border-radius:var(--radius-control);padding:4px;box-shadow:0 12px 32px rgba(11, 11, 12,.35)}
button.placeopt{display:flex;align-items:center;gap:12px;width:100%;min-height:48px;height:auto;margin:0;padding:8px 12px;background:transparent;color:var(--color-text);border-radius:12px;font-weight:400;text-align:left;justify-content:flex-start}
button.placeopt.on{background:var(--color-raised)}
.gcheck{width:18px;height:18px;border:1.5px solid var(--color-control);border-radius:4px;flex:none;box-sizing:border-box}
button.placeopt.checked .gcheck{background:var(--color-lime);border-color:var(--color-lime);background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 256 256'%3E%3Cpath fill='%23090D0B' d='M229.66,77.66l-128,128a8,8,0,0,1-11.32,0l-56-56a8,8,0,0,1,11.32-11.32L96,188.69,218.34,66.34a8,8,0,0,1,11.32,11.32Z'/%3E%3C/svg%3E");background-repeat:no-repeat;background-position:center;background-size:12px}
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
.checkbar{position:sticky;top:var(--headh,0px);z-index:6;background:var(--color-bg);margin:0 -20px var(--space-4);padding:8px 20px 12px;overflow-x:auto}
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
.checkmeta{display:flex;flex-direction:column;gap:var(--space-4);margin:0}
.checkmeta .filt.chiprow{margin:0 -20px;align-items:center;padding:0 20px}
.checkmeta .playersearch{margin:0}
.checkmeta+h2{margin-top:var(--space-4)}
.evstack{display:flex;flex-direction:column;gap:8px;margin:4px 0 12px}
.evcard{padding:var(--space-4);margin:0 0 var(--space-4)}
.evcard .evhit{display:block;color:inherit;text-decoration:none}
.evcard .nxtitle{font-size:var(--type-t4-size);font-weight:var(--type-t4-weight);line-height:var(--type-t4-line)}
.evcard .t2{margin:2px 0 0;font-weight:400;font-size:15px}
.evcard .t3{margin:2px 0 0}
a.evcard{display:block;color:inherit;text-decoration:none;background:var(--color-surface)}
.evcard.on{box-shadow:inset 0 0 0 2px var(--color-lime);scroll-margin-top:calc(var(--headh, 76px) + 88px)}
.sechead.checkhead{align-items:center}
.sechead.checkhead .btn{flex:none}
button.dock,a.dock{background:var(--accent);color:var(--color-on-primary)}
a.quietcheck,button.quietcheck{background:var(--surface2);color:var(--color-text);border:0;border-radius:var(--radius-button)}
.emptyfind{color:var(--t2);margin:8px 0 16px}
details.lineuppast{margin:20px 0 28px}details.lineuppast>summary{display:flex;align-items:center;gap:8px;list-style:none;min-height:48px;padding:12px 0 8px;font:700 22px/1 var(--r2-font-display);letter-spacing:-.03em;color:var(--r2-paper);cursor:pointer}details.lineuppast>summary::-webkit-details-marker,details.lineuppast>summary::marker{content:none;display:none}details.lineuppast>summary .pastn{color:var(--smoke);font:700 15px/1 var(--r2-font-sans)}details.lineuppast>summary::after{content:"›";margin-left:auto;color:var(--smoke);font:700 18px/1 var(--r2-font-sans)}
.repeatblock .repeatopts{display:none}.repeatblock:has(input[name=repeat]:checked) .repeatopts{display:block}
.tripcard{padding:0;overflow:hidden}.tripcard .evbody{padding:0 18px 18px}.tripcard .nxcardhead{display:flex;flex-direction:column;align-items:stretch;gap:2px;min-width:0}.tripcard .cardsub{margin:0;color:var(--color-text-secondary);min-width:0;max-width:100%}.lineupchips{display:flex;gap:6px;flex-wrap:wrap;align-items:center}.lineupchips .chip-info{margin:0}
div.card.tap.tripcard{padding:18px;overflow:visible}div.card.tap.tripcard .nxcardhead{margin:0 0 10px}
.tripcard .tripwhere{align-items:flex-start}.tripcard .tripwhere a{min-width:0}
.evbanner{height:132px;display:flex;align-items:flex-end;padding:14px;position:relative;overflow:hidden;background:linear-gradient(160deg,var(--color-badge-border),var(--color-bg))}
.evbanner img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}.evbanner svg{position:relative;z-index:1;color:var(--color-text)}
.lineupacts{display:flex;gap:8px;flex-wrap:wrap;margin:0 0 14px}.lineupacts .btn{width:auto;padding:0 14px}
.sportline{margin-top:6px;color:var(--t3)}
.actseg{display:flex;gap:var(--space-1);flex-wrap:wrap;margin:0 0 var(--space-4);padding:var(--space-1);background:var(--color-surface-2);border-radius:var(--radius-control)}
.actseg label{position:relative;flex:1;min-width:0;margin:0}
.actseg input{position:absolute;opacity:0;width:1px;height:1px}
.actseg span{display:flex;align-items:center;justify-content:center;height:40px;min-height:40px;border-radius:var(--radius-button);background:transparent;color:var(--color-text-secondary);font-size:var(--type-b3-size);font-weight:var(--type-b3-weight);padding:0 var(--space-2)}
.fldlab{display:block;margin:0 0 var(--space-2);padding:0;font-size:var(--type-b3-size);font-weight:var(--type-b3-weight);line-height:var(--type-b3-line);color:var(--t2);text-align:left}
.actseg.hostseg{flex-wrap:nowrap}
.actseg.hostseg span{white-space:nowrap;height:44px;min-height:44px;padding:0 10px}
@media (max-width:359px){body .actseg.hostseg span{white-space:normal;height:auto;min-height:44px;padding:6px 10px;text-align:center;line-height:1.15}}
.hostblock{margin:0 0 var(--space-4)}
.hostadd{display:flex;gap:8px;align-items:center}
.hostadd input{flex:1;width:auto;min-width:0;margin:0;height:var(--size-button);box-sizing:border-box}
.hostadd button{flex:none;height:var(--size-button);min-height:var(--size-button);margin:0;box-sizing:border-box}
.hostchips{display:flex;flex-wrap:wrap;gap:8px;margin:var(--space-3) 0 0}
.hostchips:empty{display:none;margin:0}
.actseg input:checked+span{background:var(--color-lime);color:var(--color-forest)}
.actseg input:focus-visible+span{outline:2px solid var(--color-focus);outline-offset:2px}
dialog.matpick .matpart{flex-wrap:nowrap;margin:12px 4px 0}
dialog.matpick .matpart span{white-space:nowrap;font-size:12px;padding:0 2px;height:36px;min-height:36px}
.evhost{color:var(--t2);font-size:14px;margin:2px 0 8px}.evnote{color:var(--t2);font-size:15px;line-height:1.4;margin:8px 0}
details.moredetails{margin:8px 0 12px}details.moredetails>summary{min-height:44px;padding:8px 0;font-weight:600}
a.growthcard,div.growthcard{position:relative;background:transparent;border:0;border-radius:0;padding:0;margin:0 0 16px}
a.growthcard,a.growthpane{display:block;color:inherit;text-decoration:none}
.growthheadrow{display:flex;align-items:flex-start;justify-content:space-between;gap:8px;margin:0 0 6px}
.growthtitles{position:relative;flex:1;min-width:0;display:grid}
.growthhead{grid-area:1/1;margin:0;opacity:0;transition:opacity .28s ease}
.growthhead.on{opacity:1}
.growthtitle{font-size:15px;font-weight:650;line-height:1.3}
.growthsub{margin:2px 0 0}
.growthswitch{display:flex;gap:6px;flex:none}
.growthswitch button.growthchip{width:32px;height:32px;min-height:32px;padding:0;border-radius:50%;border:1px solid var(--color-control);background:var(--color-raised);color:var(--color-text);flex:none}
.growthswitch button.growthchip svg{width:16px;height:16px;display:block}
.growthstage{display:grid}
.growthpane{grid-area:1/1;min-width:0;opacity:0;transition:opacity .28s ease;pointer-events:none;color:inherit;text-decoration:none}
.growthpane.on{opacity:1;pointer-events:auto}
.growthcard svg{width:100%;height:auto;display:block;touch-action:pan-y}
.growthtip{position:absolute;z-index:2;top:64px;transform:translateX(-50%);background:var(--color-surface-2);color:var(--t1);border:1px solid var(--line);border-radius:var(--radius-input);padding:6px 10px;font-size:13px;white-space:nowrap;pointer-events:none}
@media (prefers-reduced-motion:reduce){.growthhead,.growthpane{transition:none}}
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
.datefield{position:relative;display:block;width:100%;min-width:0;margin:0}
.li.editonly .datefield{flex:1 1 100%}
.datefield input[type=date]{width:100%;height:var(--size-button);min-height:var(--size-button);margin-top:6px;box-sizing:border-box}
.datefield .dateph{display:none;position:absolute;left:14px;right:42px;bottom:0;height:var(--size-button);line-height:var(--size-button);color:var(--t3);pointer-events:none;font-size:16px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.datefield.empty .dateph{display:block}
.datefield.empty input[type=date]{color:transparent}
.datefield.empty input[type=date]::-webkit-datetime-edit,.datefield.empty input[type=date]::-webkit-datetime-edit-fields-wrapper{color:transparent}
@media print{header,nav,.noprint{display:none!important}body{background:var(--paper);color:var(--ink)}.card{background:var(--paper)}}
/* Regulars loader sweep, approved as regulars23 / run #19. */
.btn.primary[data-sweep],
.btn.primary[data-sweep]:hover {
  background: var(--lime);
  color: var(--ink);
  border: 1px solid var(--lime);
  transition: none;
}
.pills > .btn.btn-primary,
.rsvprow > .btn.btn-primary,
.pills > .sweep-host > .btn.btn-primary,
.rsvprow > .sweep-host > .btn.btn-primary {
  border: 1px solid var(--color-lime);
}
.btn[data-sweep]{position:relative;overflow:visible}
.btn[data-sweep][value="going"]:not(.primary),
.btn[data-sweep][value="going"]:not(.primary):hover,
.btn[data-sweep][value="going"]:not(.primary):active {
  background: transparent;
  color: var(--color-lime);
  border: 1px solid var(--color-lime);
}
.sweep-clip, .sweep-halo, .sweep-face, .sweep-label {
  pointer-events: none;
}
.sweep-label {
  position: relative;
  z-index: 2;
  display: inline-flex;
  flex-direction: row;
  flex-wrap: nowrap;
  align-items: center;
  justify-content: center;
  gap: var(--space-2);
  white-space: nowrap;
  color: inherit;
  mix-blend-mode: normal;
}
.sweep-clip, .sweep-halo, .sweep-face {
  position: absolute;
}
.sweep-face {
  inset: 0;
  z-index: 1;
  border-radius: inherit;
  background: var(--lime);
}
.sweep-clip {
  inset: 0;
  z-index: 2;
  border-radius: inherit;
  overflow: hidden;
}
.sweep-label { z-index: 3; }
.sweep-host {
  position: relative;
  display: inline-flex;
  width: max-content;
  overflow: visible;
  vertical-align: middle;
  z-index: 0;
}
.sweep-host > .btn {
  position: relative;
  z-index: 1;
}
.sweep-halo {
  position: absolute;
  inset: -28px;
  z-index: 0;
  pointer-events: none;
  overflow: visible;
  opacity: 0.5;
  -webkit-mask-image: url("/static/sweep/sweep-halo-mask.svg?v=23");
  mask-image: url("/static/sweep/sweep-halo-mask.svg?v=23");
  -webkit-mask-repeat: no-repeat;
  mask-repeat: no-repeat;
  animation: regulars-halo 2.6s linear 1 both;
}
.sweep-rim {
  position: absolute;
  inset: 27px;
  border-radius: 13px;
  background: var(--lime);
}
.sweep-rim-soft { filter: blur(8px); opacity: 1; }
.sweep-rim-tight { filter: blur(1px); opacity: 1; }
.sweep-rim-tight + .sweep-rim-tight { mix-blend-mode: plus-lighter; }
.sweep-ribbon {
  position: absolute;
  top: -30%;
  bottom: -30%;
  transform: translateX(-50%);
  transform-origin: center center;
  animation: regulars-band 2.6s linear 1 both;
  background: var(--team-sun);
  -webkit-mask-image: url("/static/sweep/sweep-band.svg?v=22");
  mask-image: url("/static/sweep/sweep-band.svg?v=22");
  -webkit-mask-size: 100% 100%;
  mask-size: 100% 100%;
  -webkit-mask-repeat: no-repeat;
  mask-repeat: no-repeat;
}
@keyframes regulars-band {
  0% { left: -80%; width: 80%; }
  8% { left: 14%; width: 100%; }
  22% { left: 32%; width: 120%; }
  38% { left: 48%; width: 128%; }
  55% { left: 56%; width: 130%; }
  70% { left: 72%; width: 126%; }
  84% { left: 94%; width: 108%; }
  100% { left: 180%; width: 78%; }
}
@keyframes regulars-halo {
  0% { -webkit-mask-size: 113% 170%; mask-size: 113% 170%; -webkit-mask-position: 760% 50%; mask-position: 760% 50%; }
  8% { -webkit-mask-size: 142% 170%; mask-size: 142% 170%; -webkit-mask-position: 120% 50%; mask-position: 120% 50%; }
  22% { -webkit-mask-size: 170% 170%; mask-size: 170% 170%; -webkit-mask-position: 71% 50%; mask-position: 71% 50%; }
  38% { -webkit-mask-size: 181% 170%; mask-size: 181% 170%; -webkit-mask-position: 52% 50%; mask-position: 52% 50%; }
  55% { -webkit-mask-size: 184% 170%; mask-size: 184% 170%; -webkit-mask-position: 44% 50%; mask-position: 44% 50%; }
  70% { -webkit-mask-size: 179% 170%; mask-size: 179% 170%; -webkit-mask-position: 27% 50%; mask-position: 27% 50%; }
  84% { -webkit-mask-size: 153% 170%; mask-size: 153% 170%; -webkit-mask-position: -17% 50%; mask-position: -17% 50%; }
  100% { -webkit-mask-size: 111% 170%; mask-size: 111% 170%; -webkit-mask-position: -820% 50%; mask-position: -820% 50%; }
}
@media (prefers-reduced-motion: reduce) {
  .sweep-ribbon, .sweep-halo { animation: none; }
}
</style>
<script>try{if(sessionStorage.getItem("grunionsBoot"))document.documentElement.classList.add("booted")}catch(e){}</script>
</head><body style="background:var(--ink);color:var(--paper);margin:0" class="{% if (tab=='home' or tab=='practices') and me() %}homefull{% if sched_home %} schedhome{% elif tab=='practices' %} schedopen{% endif %}{% elif tab=='profile' or tab=='member' or tab=='person' or tab=='privacy' %}profilepage{% if tab=='member' and editing %} profile-edit{% endif %}{% elif tab=='practice' or tab=='lineup_event' %}practicepage{% elif tab=='admin' or tab=='manage' %}adminpage{% endif %}{% if tab=='event_new' or tab=='lineup_edit' or tab=='series_edit' or (tab=='practice' and editing) %} editor{% endif %}{% if tab=='event_new' %} eventnew{% endif %}">
<div id=boot role=status aria-label="Loading"><div class=mark><video class=bootvid autoplay muted loop playsinline preload=auto poster=/static/loader-first-frame.png><source src=/static/regulars-loader-hevc.mov type='video/quicktime; codecs="hvc1"'><source src=/static/regulars-loader-transparent.webm type=video/webm></video><img class=bootstill alt="" src=/static/regulars-logo.svg></div></div>
<script>(function(){var el=document.getElementById("boot");if(!el)return;if(document.documentElement.classList.contains("booted")){el.remove();return;}var vid=el.querySelector("video"),still=el.querySelector(".bootstill");var reduce=window.matchMedia&&matchMedia("(prefers-reduced-motion: reduce)").matches;var ios=/iPhone|iPad|iPod/.test(navigator.userAgent||"")||(navigator.platform==="MacIntel"&&navigator.maxTouchPoints>1);function showStill(){el.classList.add("bootstill");if(!vid)return;try{vid.pause()}catch(e){}vid.removeAttribute("src");while(vid.firstChild)vid.removeChild(vid.firstChild);try{vid.load()}catch(e){}}function blackFrame(){if(!vid||vid.readyState<2)return false;try{var c=document.createElement("canvas");c.width=16;c.height=8;var g=c.getContext("2d",{willReadFrequently:true});if(!g)return false;g.drawImage(vid,0,0,16,8);var d=g.getImageData(0,0,16,8).data,lime=0,dark=0,n=0;for(var i=0;i<d.length;i+=4){n++;var r=d[i],gc=d[i+1],b=d[i+2],a=d[i+3];if(a<12)continue;if(gc>80&&gc>r+15&&gc>b+10)lime++;else if(r<28&&gc<28&&b<28)dark++;}return lime===0&&dark>n*0.6;}catch(e){return false;}}if(reduce)showStill();else if(vid){try{vid.currentTime=0}catch(e){}function fast(){try{vid.playbackRate=2.0}catch(e){}}fast();vid.addEventListener("loadedmetadata",fast);vid.addEventListener("play",fast);vid.addEventListener("error",showStill);var play=vid.play();if(play&&play.catch)play.catch(function(){showStill()});if(ios){setTimeout(function(){if(blackFrame())showStill();},350);setTimeout(function(){if(blackFrame())showStill();},800);}}var started=Date.now(),MIN=2000,arm=false;function hide(){if(arm)return;arm=true;setTimeout(finish,Math.max(0,MIN-(Date.now()-started)));}function finish(){try{sessionStorage.setItem("grunionsBoot","1")}catch(e){}el.classList.add("gone");setTimeout(function(){if(el.parentNode)el.remove()},reduce?480:760);}if(document.readyState==="complete")hide();else window.addEventListener("load",hide);setTimeout(hide,8000);})();</script>
<script>
/* regulars23: post the RSVP immediately, keep the 2.6s pass on the same boxes, and do not navigate. */
(function () {
  var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var RSVP = {going:1, notgoing:1, clear:1, interested:1, social_join:1, social_leave:1};
  var CHECK = '<svg class="rsvpcheck" width="16" height="16" viewBox="0 0 256 256" fill="currentColor" aria-hidden="true"><path d="M229.66,77.66l-128,128a8,8,0,0,1-11.32,0l-56-56a8,8,0,0,1,11.32-11.32L96,188.69,218.34,66.34a8,8,0,0,1,11.32,11.32Z"/></svg>';
  function textOf(el) { return (el.textContent || "").replace(/\\s+/g, " ").trim(); }
  function field(form, name) {
    var el = form.querySelector('input[name="' + name + '"]');
    return el ? el.value : "";
  }
  function matchingForms(root, pid, eid) {
    return Array.prototype.filter.call(root.querySelectorAll("form"), function (f) {
      return (pid && field(f, "pid") === pid) || (eid && field(f, "event_id") === eid);
    });
  }
  function isSocialForm(form) {
    var buttons = form.querySelectorAll('button[name="action"]');
    if (!buttons.length) return false;
    for (var i = 0; i < buttons.length; i++) if (choiceOf(buttons[i]) !== "social") return false;
    return true;
  }
  function groupForms(root, pid, eid, social) {
    return matchingForms(root, pid, eid).filter(function (f) { return isSocialForm(f) === social; });
  }
  function goingSpan(root) {
    var spans = root.querySelectorAll(".nxrow span");
    for (var i = 0; i < spans.length; i++) if (/\\d+ going/.test(spans[i].textContent)) return spans[i];
    return null;
  }
  function showError() {
    var old = document.querySelector(".toast.rsvperr");
    if (old) old.remove();
    var t = document.createElement("div");
    t.className = "toast noprint rsvperr";
    t.setAttribute("role", "status");
    t.textContent = "Couldn't save that. Try again.";
    var main = document.querySelector("main") || document.body;
    main.insertBefore(t, main.firstChild);
    window.setTimeout(function () { if (t.parentNode) t.remove(); }, 3200);
  }
  function snapshot(form) {
    return Array.prototype.map.call(form.querySelectorAll('button[name="action"]'), function (b) {
      return {button: b, className: b.className, value: b.value, html: b.innerHTML, sweep: b.hasAttribute("data-sweep")};
    });
  }
  function restore(form, snap) {
    var host = form.querySelector(".sweep-host");
    if (host) {
      var btn = host.querySelector("button");
      if (btn) host.parentNode.insertBefore(btn, host);
      host.remove();
    }
    snap.forEach(function (s) {
      if (!s.button.isConnected) return;
      s.button.className = s.className;
      s.button.value = s.value;
      s.button.innerHTML = s.html;
      if (s.sweep) s.button.setAttribute("data-sweep", "");
      else s.button.removeAttribute("data-sweep");
      var clip = s.button.querySelector(".sweep-clip");
      if (clip) clip.remove();
      var label = s.button.querySelector(".sweep-label");
      if (label) { while (label.firstChild) s.button.insertBefore(label.firstChild, label); label.remove(); }
      delete s.button.dataset.sweeping;
      s.button.style.pointerEvents = "";
      s.button.style.flex = "";
      s.button.style.width = "";
      s.button.style.minWidth = "";
      s.button.style.maxWidth = "";
    });
    delete form.dataset.rsvpBusy;
  }
  function choiceOf(btn) {
    var t = textOf(btn);
    if (t === "Join" || t === "Joined") return "social";
    if (t === "Going" || t === "Waitlist" || t === "Join waitlist") return "going";
    if (t === "Not going") return "not";
    if (t === "Interested") return "interested";
    return t;
  }
  function plainLabel(choice, btn) {
    if (choice === "social") return "Join";
    if (choice === "going") return textOf(btn) === "Join waitlist" ? "Join waitlist" : (textOf(btn) === "Waitlist" ? "Going" : textOf(btn));
    return textOf(btn);
  }
  function writeLabel(btn, label, wantCheck) {
    btn.querySelectorAll(".rsvpcheck").forEach(function (n) { n.remove(); });
    var textNode = null;
    Array.prototype.forEach.call(btn.childNodes, function (n) { if (n.nodeType === 3) textNode = n; });
    if (!textNode) { textNode = document.createTextNode(""); btn.appendChild(textNode); }
    textNode.nodeValue = label;
    if (wantCheck) btn.insertAdjacentHTML("afterbegin", CHECK);
  }
  function deselect(btn) {
    var choice = choiceOf(btn);
    btn.classList.remove("primary", "primary", "is-sweeping");
    btn.classList.add("secondary");
    if (choice === "going") {
      var goingLabel = textOf(btn);
      if (goingLabel === "Waitlist") goingLabel = "Join waitlist";
      btn.value = "going";
      if (goingLabel === "Going") btn.setAttribute("data-sweep", "");
      else btn.removeAttribute("data-sweep");
      writeLabel(btn, goingLabel, false);
    }
    else if (choice === "not") { btn.value = "notgoing"; btn.removeAttribute("data-sweep"); writeLabel(btn, "Not going", false); }
    else if (choice === "interested") { btn.value = "interested"; btn.removeAttribute("data-sweep"); writeLabel(btn, "Interested", false); }
    else if (choice === "social") { btn.value = "social_join"; btn.setAttribute("data-sweep", ""); writeLabel(btn, "Join", false); }
    else { btn.removeAttribute("data-sweep"); writeLabel(btn, plainLabel(choice, btn), false); }
  }
  function selectVisual(btn) {
    var choice = choiceOf(btn);
    btn.classList.remove("secondary", "primary", "is-sweeping");
    btn.classList.add("primary");
    btn.removeAttribute("data-sweep");
    btn.value = choice === "social" ? "social_leave" : "clear";
    var current = textOf(btn);
    var label = current;
    if (choice === "social") label = "Joined";
    else if (choice === "going" && current === "Join waitlist") label = "Waitlist";
    else if (choice === "going") label = "Going";
    writeLabel(btn, label, true);
  }
  function cancelSweeps(forms) {
    forms.forEach(function (f) {
      var host = f.querySelector(".sweep-host");
      if (host) {
        var btn = host.querySelector("button");
        if (btn) {
          host.parentNode.insertBefore(btn, host);
          var label = btn.querySelector(".sweep-label");
          if (label) { while (label.firstChild) btn.insertBefore(label.firstChild, label); label.remove(); }
          btn.querySelectorAll(".sweep-clip").forEach(function (n) { n.remove(); });
          delete btn.dataset.sweeping;
        }
        host.remove();
      }
      Array.prototype.forEach.call(f.querySelectorAll("button"), function (b) {
        b.style.pointerEvents = "";
        b.style.flex = "";
        b.style.width = "";
        b.style.minWidth = "";
        b.style.maxWidth = "";
      });
      delete f.dataset.rsvpBusy;
    });
  }
  function showExclusive(forms, chosen, posted) {
    var choice = choiceOf(chosen);
    var selecting = posted !== "clear" && posted !== "social_leave";
    var sweepThis = false; // the sweep/fade-across-the-button animation is retired everywhere
    forms.forEach(function (f) {
      Array.prototype.forEach.call(f.querySelectorAll('button[name="action"]'), function (b) {
        if (b === chosen && sweepThis) return;
        if (selecting && choiceOf(b) === choice) selectVisual(b);
        else deselect(b);
      });
    });
  }
  function paintButton(btn, label, wantCheck) {
    var layers = btn.querySelector(".sweep-clip");
    btn.querySelectorAll(".rsvpcheck").forEach(function (n) { n.remove(); });
    var textNode = null;
    Array.prototype.forEach.call(btn.childNodes, function (n) {
      if (n.nodeType === 3) textNode = n;
    });
    if (!textNode) {
      textNode = document.createTextNode("");
      var labelEl = btn.querySelector(".sweep-label");
      (labelEl || btn).appendChild(textNode);
    }
    textNode.nodeValue = label;
    if (wantCheck) {
      var parent = btn.querySelector(".sweep-label") || btn;
      parent.insertAdjacentHTML("afterbegin", CHECK);
    }
    if (layers && layers.parentNode !== btn) btn.insertBefore(layers, btn.firstChild);
  }
  function syncButtons(localForm, freshForm) {
    var fresh = Array.prototype.slice.call(freshForm.querySelectorAll('button[name="action"]'));
    Array.prototype.forEach.call(localForm.querySelectorAll('button[name="action"]'), function (local, idx) {
      var match = fresh[idx];
      if (!match) return;
      if (local.dataset.sweeping === "playing") {
        local.dataset.finalClass = match.className;
        local.dataset.finalValue = match.value;
        local.dataset.finalSweep = match.hasAttribute("data-sweep") ? "1" : "";
        local.dataset.finalCheck = match.querySelector(".rsvpcheck") ? "1" : "";
        local.dataset.finalLabel = textOf(match);
        return;
      }
      local.className = match.className;
      local.value = match.value;
      if (match.hasAttribute("data-sweep")) local.setAttribute("data-sweep", "");
      else local.removeAttribute("data-sweep");
      paintButton(local, textOf(match), !!match.querySelector(".rsvpcheck"));
    });
  }
  function applyHtml(html, pid, eid, social) {
    var doc = new DOMParser().parseFromString(html, "text/html");
    var freshForms = groupForms(doc, pid, eid, social);
    var localForms = groupForms(document, pid, eid, social);
    function signature(form) {
      return Array.prototype.map.call(form.querySelectorAll('button[name="action"]'), function (b) {
        var t = textOf(b);
        if (t === "Join" || t === "Joined") return "social";
        if (t === "Going" || t === "Waitlist" || t === "Join waitlist") return "going";
        if (t === "Not going") return "not";
        if (t === "Interested") return "interested";
        return t;
      }).join("|");
    }
    localForms.forEach(function (local) {
      var key = signature(local);
      var fresh = null;
      for (var i = 0; i < freshForms.length; i++) if (signature(freshForms[i]) === key) { fresh = freshForms[i]; break; }
      if (!fresh) return;
      syncButtons(local, fresh);
      var card = local.closest(".card");
      var freshCard = fresh.closest(".card");
      if (!social && card && freshCard) {
        var a = goingSpan(card), b = goingSpan(freshCard);
        if (a && b) a.textContent = b.textContent;
      }
    });
    if (!social && (location.pathname.indexOf("/practices/") === 0 || location.pathname.indexOf("/lineup/") === 0)) {
      var lb = document.querySelectorAll(".stattile b, .r2-metric b"), fb = doc.querySelectorAll(".stattile b, .r2-metric b");
      if (lb.length && lb.length === fb.length) {
        for (var i = 0; i < lb.length; i++) lb[i].textContent = fb[i].textContent;
      }
      var lp = document.querySelectorAll(".p5people"), fp = doc.querySelectorAll(".p5people");
      if (lp.length && lp.length === fp.length) {
        for (var p = 0; p < lp.length; p++) lp[p].innerHTML = fp[p].innerHTML;
      }
    }
    if (!social && location.pathname.indexOf("/lineup/") === 0) {
      function rosterList(root, label) {
        var labels = root.querySelectorAll(".rg-day");
        for (var i = 0; i < labels.length; i++) {
          if (labels[i].textContent.trim() === label) {
            var list = labels[i].nextElementSibling;
            if (list && list.classList && list.classList.contains("list")) return list;
          }
        }
        return null;
      }
      ["Who's interested", "Who's going"].forEach(function (label) {
        var localList = rosterList(document, label), freshList = rosterList(doc, label);
        if (localList && freshList) localList.innerHTML = freshList.innerHTML;
      });
      function spotValue(root) {
        var rows = root.querySelectorAll(".li.prow");
        for (var i = 0; i < rows.length; i++) {
          var k = rows[i].querySelector(".k");
          if (k && k.textContent.trim() === "Spots") return rows[i].querySelector(".v");
        }
        return null;
      }
      var spotLocal = spotValue(document), spotFresh = spotValue(doc);
      if (spotLocal && spotFresh) spotLocal.textContent = spotFresh.textContent;
    }
    if (social && location.pathname.indexOf("/practices/") === 0) {
      function joining(root) {
        var nodes = root.querySelectorAll("div");
        for (var i = 0; i < nodes.length; i++) if (/^\\d+ joining$/.test(nodes[i].textContent.trim())) return nodes[i];
        return null;
      }
      var ja = joining(document), jb = joining(doc);
      if (ja && jb) ja.textContent = jb.textContent.trim();
    }
  }
  function settle(button) {
    var form = button.form;
    var host = button.parentNode;
    if (host && host.classList && host.classList.contains("sweep-host")) {
      host.parentNode.insertBefore(button, host);
      host.remove();
    }
    button.querySelectorAll(".sweep-clip").forEach(function (n) { n.remove(); });
    var label = button.querySelector(".sweep-label");
    if (label) {
      while (label.firstChild) button.insertBefore(label.firstChild, label);
      label.remove();
    }
    if (button.dataset.finalClass) {
      button.className = button.dataset.finalClass;
      button.value = button.dataset.finalValue || button.value;
      if (button.dataset.finalSweep) button.setAttribute("data-sweep", "");
      else button.removeAttribute("data-sweep");
      paintButton(button, button.dataset.finalLabel || textOf(button), button.dataset.finalCheck === "1");
    }
    delete button.dataset.sweeping;
    button.style.pointerEvents = "";
    button.style.flex = "";
    button.style.width = "";
    button.style.minWidth = "";
    button.style.maxWidth = "";
    if (form) {
      Array.prototype.forEach.call(form.querySelectorAll("button"), function (other) {
        other.style.pointerEvents = "";
        other.style.flex = "";
        other.style.width = "";
        other.style.minWidth = "";
        other.style.maxWidth = "";
      });
      delete form.dataset.rsvpBusy;
    }
  }
  function lockRow(form, button) {
    Array.prototype.forEach.call(form.querySelectorAll(":scope > button.rg-btn"), function (el) {
      var w = el.getBoundingClientRect().width;
      el.style.flex = "0 0 " + w + "px";
      el.style.width = w + "px";
      el.style.minWidth = w + "px";
      el.style.maxWidth = w + "px";
    });
    var held = button.getBoundingClientRect().width;
    return held;
  }
  function startSweep(button) {
    var form = button.form;
    var held = lockRow(form, button);
    if (button.value === "social_join" || button.value === "social_leave") held = Math.max(held, 136);
    button.classList.add("primary");
    button.classList.remove("secondary");
    button.dataset.sweeping = "playing";
    button.classList.add("is-sweeping");
    if (!button.querySelector(".sweep-label")) {
      var label = document.createElement("span");
      label.className = "sweep-label";
      while (button.firstChild) label.appendChild(button.firstChild);
      button.appendChild(label);
    }
    if (!button.querySelector(".sweep-clip")) {
      button.insertAdjacentHTML("afterbegin", '<span class="sweep-clip" aria-hidden="true"><span class="sweep-ribbon"></span></span>');
    }
    var host = button.parentNode;
    if (!host || !host.classList || !host.classList.contains("sweep-host")) {
      host = document.createElement("span");
      host.className = "sweep-host";
      button.parentNode.insertBefore(host, button);
      host.appendChild(button);
    }
    host.style.flex = "0 0 " + held + "px";
    host.style.width = held + "px";
    host.style.minWidth = held + "px";
    host.style.maxWidth = held + "px";
    button.style.flex = "1 1 auto";
    button.style.width = "100%";
    button.style.minWidth = "0";
    button.style.maxWidth = "none";
    if (!host.querySelector(".sweep-halo")) {
      host.insertAdjacentHTML("afterbegin", '<span class="sweep-halo" aria-hidden="true"><span class="sweep-rim sweep-rim-soft"></span><span class="sweep-rim sweep-rim-tight"></span><span class="sweep-rim sweep-rim-tight"></span></span>');
    }
    var labelEl = button.querySelector(".sweep-label");
    if (labelEl && !labelEl.querySelector(".rsvpcheck")) labelEl.insertAdjacentHTML("afterbegin", CHECK);
    if (button.value === "social_join") {
      var node = labelEl && labelEl.lastChild;
      while (node && node.nodeType !== 3) node = node.previousSibling;
      if (node) node.nodeValue = "Joined";
    }
  }
  var rsvpGen = {};
  var rsvpAbort = {};
  function save(button, sweep) {
    var form = button.form;
    var choice = choiceOf(button);
    var posted = button.value;
    if (choice === "not") posted = "notgoing";
    else if (choice === "going") posted = "going";
    else if (choice === "interested") posted = "interested";
    var pid = field(form, "pid"), eid = field(form, "event_id");
    var social = isSocialForm(form);
    if(pid && !social && window.grunionsDriveSetGoing) window.grunionsDriveSetGoing(posted==="going"?"1":(posted==="notgoing"?"0":""));
    var key = (pid ? ("p" + pid) : ("e" + eid)) + (social ? ":social" : ":rsvp");
    var forms = groupForms(document, pid, eid, social);
    if (!forms.length) forms = [form];
    if (rsvpGen[key] == null) {
      var floor = 0;
      forms.forEach(function (f) {
        var v = parseInt(field(f, "rsvp_base"), 10);
        if (v > floor) floor = v;
      });
      rsvpGen[key] = floor;
    }
    var gen = rsvpGen[key] + 1;
    rsvpGen[key] = gen;
    var snaps = forms.map(function (f) { return {form: f, snap: snapshot(f)}; });
    cancelSweeps(forms);
    showExclusive(forms, button, posted);
    if (sweep) startSweep(button);
    var data = new FormData(form);
    if (button.name) data.set(button.name, posted);
    data.set("rsvp_seq", String(gen));
    var action = form.getAttribute("action") || location.href;
    var pending = {ok: false, html: "", done: false};
    if (rsvpAbort[key]) rsvpAbort[key].abort();
    var ctrl = new AbortController();
    rsvpAbort[key] = ctrl;
    fetch(action, {method: "POST", body: data, credentials: "same-origin", redirect: "follow", headers: {Accept: "text/html"}, signal: ctrl.signal})
      .then(function (res) {
        // Going can need a step first: the one-sheet sign-up (05.15) or Before you go. Open it instead of faking the RSVP.
        if (res.ok && res.redirected && /\/practices\/\d+\/(signup|participate)$/.test(new URL(res.url).pathname)) {
          pending.handled = true; snaps.forEach(function (row) { restore(row.form, row.snap); });
          location.href = res.url; return;
        }
        return res.text().then(function (html) { if (!res.ok) throw new Error("save"); pending.ok = true; pending.html = html; }); })
      .then(function () { pending.done = true; if (pending.ok && rsvpGen[key] === gen) applyHtml(pending.html, pid, eid, social); })
      .catch(function () {
        pending.done = true;
        pending.ok = false;
        if (rsvpGen[key] !== gen || pending.handled) return;
        pending.handled = true;
        snaps.forEach(function (row) { restore(row.form, row.snap); });
        showError();
      });
    function finish() {
      if (rsvpGen[key] !== gen || pending.handled) return;
      if (!pending.done) { window.setTimeout(finish, 40); return; }
      if (!pending.ok) {
        pending.handled = true;
        snaps.forEach(function (row) { restore(row.form, row.snap); });
        showError();
        return;
      }
      if (sweep) settle(button);
      else delete form.dataset.rsvpBusy;
    }
    if (sweep) window.setTimeout(finish, 2640);
    else finish();
  }
  document.addEventListener("click", function (event) {
    var button = event.target.closest && event.target.closest('button[name="action"]');
    if (!button || !button.form || !RSVP[button.value]) return;
    // 2.0 social cards swap between condensed (Join) and expanded (Joined) — let the server re-render the card.
    if (button.closest(".rg-social")) return;
    if (button.dataset.sweeping === "playing") {
      event.preventDefault();
      event.stopPropagation();
      if (choiceOf(button) !== "social") return;
      delete button.dataset.sweeping;
      button.value = "social_leave";
      save(button, false);
      return;
    }
    event.preventDefault();
    event.stopPropagation();
    var sweep = false; // the sweep/fade-across-the-button animation is retired everywhere
    button.form.dataset.rsvpBusy = "1";
    save(button, sweep);
  }, true);
})();
</script>
{% macro st(kind, label) %}<span class="st st-{{kind}}">{{label}}</span>{% endmacro %}
{% macro bubble(n) %}{% if n %}<span class=badge>{{ n if n < 100 else '99+' }}</span>{% endif %}{% endmacro %}
{% macro usawp(s) %}{{ st({'verified':'ok','expired':'bad','pending':'warn'}.get(s,'none'), 'USAWP ' ~ s) }}{% endmacro %}
{% macro coach_tag(m) %}{% if can_see_member_status(m) %}{% set ce = coach_eligibility(m) %}{% if ce.eligible %}<span class="st st-ok coach-elig">Coach eligible</span>{% elif ce.text %}<span class="st st-bad coach-elig">{{ce.text}}</span>{% endif %}{% endif %}{% endmacro %}
{% macro referee_tag(m) %}{% if can_see_member_status(m) %}{% set rf = referee_eligibility(m) %}{% if rf.eligible %}<span class="st st-ok ref-elig">Referee eligible</span>{% elif rf.text %}<span class="st st-bad ref-elig">{{rf.text}}</span>{% endif %}{% endif %}{% endmacro %}
{% macro bg_line(m) %}{% if can_see_member_status(m) %}{% set bg = background_view(m) %}{% if bg %}{{ st(bg.kind, bg.text) }}{% endif %}{% endif %}{% endmacro %}
{% macro bg_status(m) %}{% if can_see_member_status(m) %}{% set bg = background_view(m) %}{% if bg %}{{ st(bg.kind, ('expires ' ~ bg.date) if bg.date else 'missing') }}{% endif %}{% endif %}{% endmacro %}
{% macro member_expiry(m) %}{% if can_see_member_status(m) %}{% set left = days_left(m.usawp_valid_until) %}{% if not m.usawp_valid_until %}{{ st('bad', 'missing') }}{% elif left < 0 %}{{ st('bad', 'expires ' ~ m.usawp_valid_until) }}{% elif left <= EXPIRING_DAYS %}{{ st('warn', 'expires ' ~ m.usawp_valid_until) }}{% else %}{{ st('ok', 'expires ' ~ m.usawp_valid_until) }}{% endif %}{% endif %}{% endmacro %}
{% macro expiry_kind(m) %}{% set left = days_left(m.usawp_valid_until) %}{% if not m.usawp_valid_until %}bad{% elif left < 0 %}bad{% elif left <= EXPIRING_DAYS %}warn{% else %}ok{% endif %}{% endmacro %}
{% macro expiry_text(m) %}{% if not m.usawp_valid_until %}missing{% else %}expires {{ m.usawp_valid_until }}{% endif %}{% endmacro %}
{% macro titledot(kind, title) %}<span class=rowtitle><span class="dot{% if kind %} {{ kind }}{% endif %}" aria-hidden=true></span>{{ title }}</span>{% endmacro %}
{% macro memhead(m) %}<div class=sechead id=membership><div class=rg-day>Compliance</div><span hidden>Water Polo Membership</span>{% if m.usawp_verified_at %}<div class=verifiedwhen>Verified {{ m.usawp_verified_at[:10] }}</div>{% endif %}</div>{% endmacro %}
{# Credential line on the list-row component: ok = Cleared (lime), warn = Expiring (sun), anything else = Not cleared (tangerine). #}
{% macro cred_row(kind, title, side) -%}{{ rg_row(title, side, '', '', '', '', {'ok':'Cleared','warn':'Expiring'}.get(kind|trim, 'Not cleared'), {'ok':'going','warn':'expiring'}.get(kind|trim, 'notcleared')) }}{%- endmacro %}
{% macro membership_section(m, vr_pending) %}{% if can_see_member_status(m) %}{% set cl = clearance(m) %}{% set dl = days_left(m.usawp_valid_until) %}{% set tw = trial_window(m) %}{% set ex = expiry_notes(m, cl) %}{% set cc = coach_clearance(m) %}{% set left = days_left(m.usawp_valid_until) %}{% set locked = m.usawp_status == 'verified' and not (left is not none and left < 0) %}{% set on_trial = tw and tw.active and not ex.membership and m.usawp_status != 'verified' and not vr_pending %}
{{ memhead(m) }}
<div class=list>
{{ cred_row('warn' if on_trial else expiry_kind(m)|trim, 'USAWP #' ~ (m.usawp_number or '—'), (trial_badge(tw)|striptags) if on_trial else expiry_text(m)|trim) }}
{% if not locked %}<div class="li prow editonly"><label class=prefedit style="width:100%;margin:0">USAWP number<input form=profileForm id=usawpNumber name=usawp_number inputmode=numeric autocomplete=off value="{{ m.usawp_number or '' }}" data-original="{{ m.usawp_number or '' }}"></label></div>{% endif %}
{% for it in cl.checks %}{% set sk = {'ok':'ok','no date':'warn'}.get(it.status,'bad') %}{% set side = (('expires ' ~ it.mr.expires_on) if it.mr and it.mr.expires_on else ('done ' ~ it.mr.completed_on) if it.mr and it.mr.completed_on else 'missing') if it.status != 'expired' else 'expired' %}{{ cred_row(sk, it.req.name, side) }}{% endfor %}
{% if background_view(m) %}{% set bg = background_view(m) %}{{ cred_row(bg.kind, 'Background screening', ('expires ' ~ bg.date) if bg.date else 'missing') }}{% endif %}
{% if cc %}{{ cred_row('ok' if cc.ok else 'bad', 'Coaching', 'cleared' if cc.ok else cc.text) }}{% elif coach_eligibility(m).text %}{% set ce = coach_eligibility(m) %}{{ cred_row('ok' if ce.eligible else 'bad', 'Coaching', ce.text) }}{% endif %}
</div>
{% if tw and tw.expired and not ex.membership and m.usawp_status != 'verified' and not vr_pending %}<p class="sm" style="margin:8px 0 0">Trial ended {{tw.ends}}</p>{% endif %}
{% if not cl.ok %}{% if not vr_pending %}{% for line in ex.lines %}<p class="sm" style="margin:8px 0 0">{{line}}</p>{% endfor %}{% elif ex.safesport %}<p class="sm" style="margin:8px 0 0">SafeSport expired {{ex.safesport}}</p>{% endif %}
{% if ex.rest %}<p class="ty-body sm" style="margin:8px 0 0">Needs: {{ex.rest|join(', ')}}</p>{% endif %}{% endif %}
{% if m.usawp_status=='verified' and dl is not none and dl <= EXPIRING_DAYS %}<p class="sm" style="margin:8px 0 0"><span class="st st-warn"></span> Your membership expires in <b>{{dl}} days</b> ({{m.usawp_valid_until}}). <a href=https://usawp.sport80.com>Renew</a></p>{% endif %}
{% if m.usawp_status != 'verified' %}<p class="ty-body sm" style="margin:8px 0 0">Register or renew at <a href=https://usawp.sport80.com>usawp.sport80.com</a> with {{m.email}} and choose Grunions as your club.</p>{% endif %}
{% if ex.membership and not vr_pending %}
<button type=button class="rg-btn primary full" id=reverifyOpen style="margin-top:14px">Reverify membership</button>
<form id=reverifyForm hidden method=post action=/home style="margin-top:14px">{{csrf_field()}}
<div class=row style="align-items:flex-end"><label style="margin:0">USAWP Membership #<input name=usawp_number inputmode=numeric value="{{m.usawp_number or ''}}" autocomplete=off></label>
<label style="margin:0">Background screening expires<input name=background_expires type=date value="{{ (background_view(m).date if background_view(m) else '') }}"></label>
<button class="rg-btn primary" style="flex:0 0 auto">Send</button></div></form>
<script>document.getElementById('reverifyOpen').onclick=function(){var f=document.getElementById('reverifyForm');f.hidden=false;this.hidden=true;f.querySelector('input[name=usawp_number]').focus()};</script>
{% elif m.usawp_status == 'verified' %}
{% set bg = background_view(m) %}{% if bg and bg.required and bg.kind == 'bad' and not vr_pending %}
<form method=post action=/home style="margin-top:14px">{{csrf_field()}}<input type=hidden name=action value=reverify_background>
<button class="rg-btn primary full">Reverify background screening</button></form>{% endif %}
{% endif %}
{% endif %}{% endmacro %}
{% macro expiry_slot(m) %}{% if can_see_member_status(m) %}{% set left = days_left(m.usawp_valid_until) %}{% if left is not none and left >= 0 and left <= EXPIRING_DAYS %}<span class="ty-muted ty-sm xs">{% if left == 0 %} · expires today{% elif left == 1 %} · expires in 1 day{% else %} · expires in {{ left }} days{% endif %}</span>{% endif %}{% endif %}{% endmacro %}
{% macro hi_membership() %}{% set num = (me().usawp_number or '')|trim %}{% set tw = trial_window(me()) %}{% set on_trial = tw and tw.active and (me().usawp_status or '') != 'verified' %}{% if num %}{% set cl = clearance(me()) %}{% set dl = days_left(me().usawp_valid_until) %}{% set ns = namespace(tone='ok') %}{% if vr_pending or on_trial %}{% set ns.tone = 'warn' %}{% elif not cl.ok %}{% set ns.tone = 'bad' %}{% elif dl is not none and dl <= EXPIRING_DAYS %}{% set ns.tone = 'warn' %}{% else %}{% for it in cl.checks %}{% if it.days_left is not none and it.days_left >= 0 and it.days_left <= EXPIRING_DAYS %}{% set ns.tone = 'warn' %}{% endif %}{% endfor %}{% endif %}<a class="usawpchip{% if ns.tone != 'ok' %} {{ ns.tone }}{% endif %}" href="/profile#membership">{% if ns.tone == 'ok' %}<svg class="usawpok" width="16" height="16" viewBox="0 0 256 256" fill="currentColor" aria-hidden="true"><path d="M128,24A104,104,0,1,0,232,128,104.11,104.11,0,0,0,128,24Zm45.66,85.66-56,56a8,8,0,0,1-11.32,0l-24-24a8,8,0,0,1,11.32-11.32L112,148.69l50.34-50.35a8,8,0,0,1,11.32,11.32Z"/></svg>{% else %}<span class="dot {{ ns.tone }}" aria-hidden=true></span>{% endif %}USAWP #{{ num }}</a>{% elif on_trial and not vr_pending %}<a class="usawpchip warn" href="/profile#membership"><span class="dot warn" aria-hidden=true></span>Trial</a>{% endif %}{% endmacro %}
{% macro roster_status(r) %}{% if can_see_member_status(r) %}{% set cl = clearance(r) %}{% set dl = days_left(r.usawp_valid_until) %}{% set tw = trial_window(r) %}{% set ex = expiry_notes(r, cl) %}{% set ns = namespace(tone='ok', text='Cleared', when='') %}
{% if dl is not none and dl >= 0 and dl <= EXPIRING_DAYS %}{% if dl == 0 %}{% set ns.when = 'expires today' %}{% elif dl == 1 %}{% set ns.when = 'expires in 1 day' %}{% else %}{% set ns.when = 'expires in ' ~ dl ~ ' days' %}{% endif %}{% endif %}
{% if tw and tw.active and r.usawp_status != 'verified' and not ex.membership %}{% set ns.tone = 'warn' %}{% set ns.text = trial_badge(tw) %}{% set ns.when = '' %}
{% elif tw and tw.expired and r.usawp_status != 'verified' %}{% set ns.tone = 'bad' %}{% set ns.text = 'Trial ended ' ~ tw.ends %}
{% elif not cl.ok %}{% set ns.tone = 'bad' %}{% set ns.text = 'Not cleared' %}
{% elif ns.when %}{% set ns.tone = 'warn' %}{% set ns.text = 'Expiring soon' %}{% endif %}
<span class="st st-{{ ns.tone }} rowstatus">{{ ns.text }}{% if ns.when %} · {{ ns.when }}{% endif %}</span>{% endif %}{% endmacro %}
{% macro member_status(r) %}{{ roster_status(r) }}{% endmacro %}
{% macro status_dot(s) %}{% set kind = {'verified':'ok','expired':'bad','pending':'warn'}.get(s, '') %}<span class="dot{% if kind %} {{kind}}{% endif %}" aria-hidden=true></span>{% endmacro %}
{% macro checkin_status(r) %}{{ person_sub(r) }}{% endmacro %}
{% macro person_sub(r) %}{% if can_see_member_status(r) %}{% if view is defined and view in ('members', 'coaches', 'admins', 'referees', 'compliance', 'membership') %}{% set st = list_row_status(r, view) %}<span class="psub ell st-{{ st.tone }}"><span class=stword>{{ st.word }}</span>{% if st.rest %}<span class=strest>{{ st.rest }}</span>{% endif %}</span>{% else %}{% set cl = clearance(r) %}{% set dl = days_left(r.usawp_valid_until) %}{% set tw = trial_window(r) %}{% set ex = expiry_notes(r, cl) %}{% set ns = namespace(tone='ok', word='Cleared', rest='') %}
{% if dl is not none and dl >= 0 and dl <= EXPIRING_DAYS %}{% if dl == 0 %}{% set ns.rest = ' · expires today' %}{% elif dl == 1 %}{% set ns.rest = ' · expires in 1 day' %}{% else %}{% set ns.rest = ' · expires in ' ~ dl ~ ' days' %}{% endif %}{% endif %}
{% if tw and tw.active and r.usawp_status != 'verified' and not ex.membership %}{% set ns.tone = 'warn' %}{% set ns.word = 'Trial' %}{% set ns.rest = ' · ' ~ trial_left_phrase(tw) %}
{% elif tw and tw.expired and r.usawp_status != 'verified' %}{% set ns.tone = 'bad' %}{% set ns.word = 'Trial ended ' ~ tw.ends %}{% set ns.rest = '' %}
{% elif not cl.ok %}{% set ns.tone = 'bad' %}{% set ns.word = 'Not cleared' %}
{% elif ns.rest %}{% set ns.tone = 'warn' %}{% set ns.word = 'Expiring soon' %}{% endif %}
{% set thru = '' %}{% if not (tw and tw.active and r.usawp_status != 'verified') and r.usawp_valid_until and (dl is none or dl < 0 or dl > EXPIRING_DAYS) %}{% set thru = ' · thru ' ~ fmt_long(r.usawp_valid_until) %}{% endif %}
{% set detail = (ns.rest or '') ~ thru %}
<span class="psub ell st-{{ ns.tone }}"><span class=stword>{{ ns.word }}</span>{% if detail %}<span class=strest>{{ detail }}</span>{% endif %}</span>{% endif %}{% endif %}{% endmacro %}
{% macro person_mark(r) %}{% if can_see_member_status(r) %}{% set cl = clearance(r) %}{% set dl = days_left(r.usawp_valid_until) %}{% set tw = trial_window(r) %}{% set ex = expiry_notes(r, cl) %}{% set ns = namespace(tone='ok') %}
{% if tw and tw.active and r.usawp_status != 'verified' and not ex.membership %}{% set ns.tone = 'warn' %}
{% elif tw and tw.expired and r.usawp_status != 'verified' %}{% set ns.tone = 'bad' %}
{% elif not cl.ok %}{% set ns.tone = 'bad' %}
{% elif dl is not none and dl >= 0 and dl <= EXPIRING_DAYS %}{% set ns.tone = 'warn' %}{% endif %}
<span class="psub st-{{ ns.tone }} coachmark" aria-hidden="true"></span>{% endif %}{% endmacro %}
{% macro person_link(r) %}<a class=ci-name href="/admin/member/{{ r.id }}">{% if r.photo %}<span class="avatar ciav"><img src="/avatar/{{ r.id }}?v={{ r.photo }}" alt="" width="40" height="40"></span>{% else %}<span class="avatar ciav">{{ initials(r) }}</span>{% endif %}<span class=grow style="min-width:0"><span class=ell style="display:block;font-weight:500">{{ display_first(r) }} {{ r.last }}</span>{{ person_sub(r) }}{{ caller() }}</span></a>{% endmacro %}
{% macro admin_page(title, subtitle='') %}{{ rg_page_title(title, subtitle, caller() if caller is defined else '') }}{% endmacro %}
{% macro manage_row(href, title, desc, icon, count=0, tone='info', tile='carbon', num=false) %}{{ rg_manage_tile(href, title, desc, icon, count, tone, tile, num) }}{% endmacro %}
{% macro type_select(types, selected='') %}<select name=event_type id=lineType>{% for glabel, options in lineup_type_groups(types) %}<optgroup label="{{ glabel }}">{% for name, label in options %}<option value="{{ name }}" {% if selected == name %}selected{% endif %}>{{ label }}</option>{% endfor %}</optgroup>{% endfor %}</select>{% endmacro %}
{% macro event_chooser(staff) %}
<h2 class=planask>What are you planning?</h2>
<div class=planlane>
{% if staff %}<div class=card>
<h2>Team schedule</h2>
<p class="ty-muted ty-sm sm">Practice, scrimmage, and game. Shows on Home.</p>
<div class=planlinks>
<a class=chip href="/events/new?type=practice">Practice</a>
<a class=chip href="/events/new?type=scrimmage">Scrimmage</a>
<a class=chip href="/events/new?type=game">Game</a>
</div>
</div>{% endif %}
<div class=card>
<h2>Lineup event</h2>
<p class="ty-muted ty-sm sm">Tournaments, camps, trips, and community events. Shows on Lineup.</p>
{% for glabel, options in lineup_type_groups(EVENT_TYPE_LABELS if staff else MEMBER_TYPE_LABELS) %}
<div class="ty-muted ty-sm xs" style="margin:8px 0 4px">{{ glabel }}</div>
<div class=planlinks>
{% for name, label in options %}<a class=chip href="/lineup/new?mode={{ 'create' if staff else 'suggest' }}&amp;event_type={{ name }}">{{ label }}</a>{% endfor %}
</div>
{% endfor %}
</div>
</div>
{% endmacro %}
{% macro detail_hiddens(r) %}{{csrf_field()}}<input type=hidden name=member_id value={{r.id}}><input type=hidden name=date value="{{date}}"><input type=hidden name=q value="{{q}}">{% if view is defined %}<input type=hidden name=list_view value="{{ view }}">{% endif %}{% if coach_filter is defined %}<input type=hidden name=list_coach value="{{'eligible' if coach_filter else ''}}"><input type=hidden name=list_referee value="{{'eligible' if referee_filter else ''}}">{% endif %}{% endmacro %}
{% macro cred_side(iso) %}{% if iso %}<span class=cred><span class="dot {{ date_dot(iso) }}" aria-hidden=true></span>{{ fmt_long(iso) }}</span>{% else %}<span class='ty-muted ty-sm'>Not on file</span>{% endif %}{% endmacro %}
{% macro date_field(label, name, value) %}<label class="datefield{% if not value %} empty{% endif %}">{{ label }}<input type=date name={{ name }} value="{{ value or '' }}" placeholder="Not on file"><span class=dateph>Not on file</span></label>{% endmacro %}
{# Event cards and rows: thin wrappers so existing call sites render the one component in components.py. #}
{% macro r2_event_card(href, sport, title, clock, meridiem, duration, venue, people, extra, you=false, tone='', went=false) -%}
{%- set inits = [] -%}{%- for person in people[:3] %}{% set _ = inits.append(initials(person)) %}{% endfor -%}
{{ rg_event_card(href, sport, title, clock, meridiem, duration, venue, inits, people|length, you or went, tone or 'sun', '' if (you or went) else extra, went) }}
{%- endmacro %}
{% macro r2_event_row(href, variant, kicker, title, meta, count, kind='', went=false) -%}
{%- if variant == 'cancelled' -%}{{ rg_event_cancelled(href, kicker, title, meta) }}
{%- elif variant == 'stack' -%}{{ rg_event_row(href, kind or 'WATER POLO', kicker ~ ' ' ~ title, meta, count, 'WENT' if went else 'GOING', event_tone(kind)) }}
{%- else -%}{{ rg_event_line(href, kicker ~ ' · ' ~ title, meta ~ ((' · ' ~ count ~ ' going') if count else ''), 'graphite' if variant == 'off' else event_tone(kind)) }}{%- endif -%}
{%- endmacro %}
{% macro r2_social_card(card, variant='home') -%}{{ rg_social_card(card, csrf_field(), 'page' if variant == 'row' else 'home', fmt_clock(card.clock) if card.clock else '') }}{%- endmacro %}
{% macro r2_drive_card(minutes, detail, leave, placeholder=false, kicker='YOUR DRIVE', href='') -%}
<{{ 'a' if href else 'div' }} class="r2-drive drivecard" data-r2="drive-card"{% if href %} href="{{ href }}" aria-label="Plan when to leave"{% endif %} {% if placeholder %}data-placeholder=1{% endif %}><div class=drivetop><span>{{ kicker }}</span>{% if leave %}<b>{{ leave }}</b>{% endif %}</div><div class=drivemain><strong>{{ minutes }}</strong><small><i>MIN</i>{{ detail }}</small><span class=drivego aria-hidden=true>›</span></div></{{ 'a' if href else 'div' }}>
{%- endmacro %}
{% macro r2_metric(value, label, tone='ink') -%}{{ rg_metric(value, label, {'ink':'carbon','lime':'lime'}.get(tone, tone)) }}{%- endmacro %}
{% macro r2_info(kicker, body) -%}{{ rg_info(kicker, body) }}{%- endmacro %}
{% macro r2_section(title) -%}{{ rg_section(title) }}{%- endmacro %}
{% macro r2_list_row(name, sub, letters, chip='') -%}{{ rg_row(name, sub, '', letters, 'sun', '', chip, 'going' if chip == 'Going' else ('notcleared' if chip == 'Out' else 'neutral'), false, 'person') }}{%- endmacro %}
{% macro r2_practice_actions(href, label, count) -%}{{ rg_practice_actions(href, label, count) }}{%- endmacro %}
{% macro r2_legend(pin) -%}
<div class="r2-legend maplegend" data-r2="traffic-legend" data-traffic="placeholder" aria-hidden=true><span><i class=legclear></i>Clear</span><span><i class=legslow></i>Slow</span><span><i class=legjam></i>Jammed</span>{% if pin %}<b>{{ pin }}</b>{% endif %}</div>
{%- endmacro %}
{% macro r2_map_unavailable() -%}{{ rg_map_unavailable() }}{%- endmacro %}
{% macro r2_cover(src) -%}
<div class="r2-cover p5cover" data-r2="cover-image"><img src="{{ src }}" alt=""></div>
{%- endmacro %}
{% macro r2_chip(label, on=false) -%}
<span class="r2-chip{% if on %} on{% endif %}" data-r2="chip">{{ label }}</span>
{%- endmacro %}
{% macro rsvp_btn(label, selected, on_value) -%}
{%- set sweep = (not selected) and on_value == 'going' and label == 'Going' -%}
<button class="btn {{ 'btn-primary' if selected else 'btn-secondary' }}"{% if sweep %} data-sweep{% endif %} name=action value="{{ 'clear' if selected else on_value }}">{% if selected %}<svg class=rsvpcheck width="16" height="16" viewBox="0 0 256 256" fill="currentColor" aria-hidden="true"><path d="M229.66,77.66l-128,128a8,8,0,0,1-11.32,0l-56-56a8,8,0,0,1,11.32-11.32L96,188.69,218.34,66.34a8,8,0,0,1,11.32,11.32Z"/></svg>{% endif %}{{ label }}</button>
{%- endmacro %}
{# Regulars 2.0 components live in components.py (Jinja globals rg_*). Don't add one-off card or row markup here. #}
{% macro rsvp_base(key) -%}<input type=hidden name=rsvp_base value="{{ (session.get('rsvp_seq') or {}).get(key, 0) }}">{%- endmacro %}
{% macro glyph_clock() %}<svg class="nxglyph" width="16" height="16" viewBox="0 0 256 256" fill="currentColor" aria-hidden="true"><path d="M128,24A104,104,0,1,0,232,128,104.11,104.11,0,0,0,128,24Zm0,192a88,88,0,1,1,88-88A88.1,88.1,0,0,1,128,216Zm64-88a8,8,0,0,1-8,8H128a8,8,0,0,1-8-8V72a8,8,0,0,1,16,0v48h48A8,8,0,0,1,192,128Z"/></svg>{% endmacro %}
{% macro glyph_pin() %}<svg class="nxglyph" width="16" height="16" viewBox="0 0 256 256" fill="currentColor" aria-hidden="true"><path d="M128,64a40,40,0,1,0,40,40A40,40,0,0,0,128,64Zm0,64a24,24,0,1,1,24-24A24,24,0,0,1,128,128Zm0-112a88.1,88.1,0,0,0-88,88c0,31.4,14.51,64.68,42,96.25a254.19,254.19,0,0,0,41.45,38.3,8,8,0,0,0,9.18,0A254.19,254.19,0,0,0,174,200.25c27.45-31.57,42-64.85,42-96.25A88.1,88.1,0,0,0,128,16Zm0,206c-16.53-13-72-60.75-72-118a72,72,0,0,1,144,0C200,161.23,144.53,209,128,222Z"/></svg>{% endmacro %}
{% macro glyph_people() %}<svg class="nxglyph" width="16" height="16" viewBox="0 0 256 256" fill="currentColor" aria-hidden="true"><path d="M117.25,157.92a60,60,0,1,0-66.5,0A95.83,95.83,0,0,0,3.53,195.63a8,8,0,1,0,13.4,8.74,80,80,0,0,1,134.14,0,8,8,0,0,0,13.4-8.74A95.83,95.83,0,0,0,117.25,157.92ZM40,108a44,44,0,1,1,44,44A44.05,44.05,0,0,1,40,108Zm210.14,98.7a8,8,0,0,1-11.07-2.33A79.83,79.83,0,0,0,172,168a8,8,0,0,1,0-16,44,44,0,1,0-16.34-84.87,8,8,0,1,1-5.94-14.85,60,60,0,0,1,55.53,105.64,95.83,95.83,0,0,1,47.22,37.71A8,8,0,0,1,250.14,206.7Z"/></svg>{% endmacro %}
{% macro upload_field(name, mode='image', hint='', accept='', src='', clear_name='') %}
{%- set is_file = mode == 'file' -%}
{%- set label = 'Upload a file' if is_file else 'Upload an image' -%}
{%- set hint_text = hint or ('CSV' if is_file else 'PNG or JPG') -%}
{%- set acc = accept or ('.csv,.xlsx' if is_file else 'image/*,image/heic,image/heif,image/heic-sequence,image/heif-sequence,.heic,.heif') -%}
<div class="dropzone{% if src %} has{% endif %}" data-dropzone data-mode="{{ 'file' if is_file else 'image' }}"><input class=pick type=file name={{ name }} accept="{{ acc }}" aria-label="{{ label }}">{% if clear_name %}<input type=hidden name={{ clear_name }} value="" data-clear>{% endif %}<button type=button class=dropempty {% if src %}hidden{% endif %}>{% if is_file %}<svg class=dropico viewBox="0 0 256 256" fill="currentColor" aria-hidden="true"><path d="M213.66,82.34l-56-56A8,8,0,0,0,152,24H56A16,16,0,0,0,40,40V216a16,16,0,0,0,16,16H200a16,16,0,0,0,16-16V88A8,8,0,0,0,213.66,82.34ZM160,51.31,188.69,80H160ZM200,216H56V40h88V88a8,8,0,0,0,8,8h48V216Z"/></svg>{% else %}<svg class=dropico viewBox="0 0 256 256" fill="currentColor" aria-hidden="true"><path d="M216,40H40A16,16,0,0,0,24,56V200a16,16,0,0,0,16,16H216a16,16,0,0,0,16-16V56A16,16,0,0,0,216,40Zm0,16V158.75l-26.07-26.06a16,16,0,0,0-22.63,0l-20,20-44-44a16,16,0,0,0-22.62,0L40,149.37V56ZM40,172l52-52,80,80H40Zm176,28H194.63l-36-36,20-20L216,181.38V200ZM96,100a12,12,0,1,1,12-12A12,12,0,0,1,96,100Z"/></svg>{% endif %}<span class=droplink>{{ label }}</span><span class=drophint>{{ hint_text }}</span></button><div class=dropfill {% if not src %}hidden{% endif %}><img alt="" data-preview {% if src %}src="{{ src }}"{% endif %}><div class=filemeta><span class=dropname data-name></span><span class=dropsize data-size></span></div><div class=dropacts><button type=button data-replace>Replace</button><button type=button data-remove>Remove</button></div></div></div>
{%- endmacro %}
{% macro social_icon() %}<span class=nxicon aria-hidden=true><svg width="24" height="24" viewBox="0 0 256 256" fill="currentColor" aria-hidden="true"><path d="M237.66,45.66A8,8,0,0,0,232,32H24a8,8,0,0,0-5.66,13.66L120,147.31V208H88a8,8,0,0,0,0,16h80a8,8,0,0,0,0-16H136V147.31ZM43.31,48H212.69l-16,16H59.31ZM128,132.69,75.31,80H180.69Z"/></svg></span>{% endmacro %}
{% macro social_fields(p) %}
<div class="ty-muted ty-sm xs">Type</div>
<div class=checks role=group aria-label="Type"><input type=hidden name=social_kind value="">
{% for kind in SOCIAL_KINDS %}<label><input type=checkbox name=social_kind value="{{ kind }}" {% if kind in (p.social_kind or '').split(',') %}checked{% endif %}>{{ kind }}</label>{% endfor %}
</div>
<label>Address<span class=locok {% if not p.social_address %}hidden{% endif %}><svg width="16" height="16" viewBox="0 0 256 256" fill="currentColor" aria-hidden="true"><path d="M128,24A104,104,0,1,0,232,128,104.11,104.11,0,0,0,128,24Zm45.66,85.66-56,56a8,8,0,0,1-11.32,0l-24-24a8,8,0,0,1,11.32-11.32L112,148.69l50.34-50.35a8,8,0,0,1,11.32,11.32Z"/></svg> Verified</span><input name=social_address value="{{ p.social_address or '' }}" data-places data-place-name=social_place{{ place_proximity(p.lat, p.lng) }} autocomplete=off placeholder="Search for an address"></label>
<label>Place name<input name=social_place value="{{ p.social_place or '' }}" autocomplete=off placeholder="Name of the place"></label>
<label>Time (optional)<input data-native type=time name=social_time min="{{ (p.end or '20:30')[:5] }}" value="{{ p.social_time or (p.end or '20:30')[:5] }}"></label>
<label>Note (optional)<textarea class=planfield name=social_note rows=4>{{ p.social_note or '' }}</textarea></label>
{% endmacro %}
{% macro message_fields(p) %}
<label>Coach message<textarea class=planfield name=message maxlength=280 rows=4>{{ p.coach_note or '' }}</textarea></label>
<p class="ty-muted ty-sm sm">Leave blank to clear it.{% if p.coach_note_by %} Last set by {{ p.coach_note_by }}{% if p.coach_note_at %} · {{ fmt_stamp(p.coach_note_at) }}{% endif %}.{% endif %}</p>
{% endmacro %}
{% macro practice_extra_dialogs(p, back) %}
<dialog class=modal id=social{{ p.id }}><div class=sheet><h2 style="margin:0 0 12px">After-practice social</h2>
<form method=post action="/practices/{{ p.id }}">{{ csrf_field() }}<input type=hidden name=pid value={{ p.id }}><input type=hidden name=back value="{{ back }}">
{{ social_fields(p) }}
<button class="rg-btn primary full" name=action value=social>Save</button></form></div></dialog>
<dialog class=modal id=message{{ p.id }}><div class=sheet><h2 style="margin:0 0 12px">Coach message</h2>
<form method=post action="/practices/{{ p.id }}">{{ csrf_field() }}<input type=hidden name=pid value={{ p.id }}><input type=hidden name=back value="{{ back }}">
{{ message_fields(p) }}
<button class="rg-btn primary full" name=action value=message>Save</button></form></div></dialog>
<dialog class=modal id=image{{ p.id }}><div class=sheet><h2 style="margin:0 0 12px">Practice image</h2>
<form method=post action="/practices/{{ p.id }}" enctype=multipart/form-data>{{ csrf_field() }}<input type=hidden name=pid value={{ p.id }}><input type=hidden name=back value="{{ back }}">
{{ upload_field('image', src=('/practice-image/' ~ p.id ~ '?v=' ~ p.image) if p.image else '', clear_name='image_clear') }}
<p class="ty-muted ty-sm sm">Shown on the Home card only. Leave the file empty to keep the current picture.</p>
<button class="rg-btn primary full" name=action value=image>Save</button></form></div></dialog>
<dialog class=modal id=notes{{ p.id }}><div class=sheet><h2 style="margin:0 0 12px">Notes</h2>
<form method=post action="/practices/{{ p.id }}">{{ csrf_field() }}<input type=hidden name=pid value={{ p.id }}><input type=hidden name=back value="{{ back }}">
<label>Notes<textarea class=planfield name=note rows=4>{{ p.note or '' }}</textarea></label>
<button class="rg-btn primary full" name=action value=note>Save</button></form></div></dialog>
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
{% elif not practice_ended(p) %}<button type=button data-open="cancel{{ p.id }}">Send cancellation</button>{% endif %}
<a href="/events/new?lane=schedule&amp;copy={{ p.id }}">Duplicate practice</a>
<button type=button data-copy="{{ app_base() }}/practices/{{ p.id }}">Copy link</button>
{% if not practice_ended(p) %}<button type=button data-open="delete{{ p.id }}">Delete practice</button>{% endif %}
</div></span>
{{ practice_extra_dialogs(p, back) }}
<dialog class=modal id=assign{{ p.id }}><div class=sheet><h2 style="margin:0 0 12px">Assign coaches</h2>
<form method=post action="/practices/{{ p.id }}">{{ csrf_field() }}<input type=hidden name=pid value={{ p.id }}><input type=hidden name=back value="{{ back }}">
<div class=checks role=group aria-label="Coaches">{% for c in coach_choices %}<label><input type=checkbox name=coach value="{{ c.id }}" {% if c.id in coach_ids %}checked{% endif %}>{{ display_first(c) }} {{ c.last }} {{ coach_tag(c) }}</label>
{% else %}<p class="ty-muted ty-sm sm">No coaches yet. Add someone on People.</p>{% endfor %}</div>
<div class=row><button class="rg-btn primary" name=action value=assign>Save</button><button type=button class="rg-btn secondary" onclick="this.closest('dialog').close()">Cancel</button></div></form></div></dialog>
{% if not practice_ended(p) %}
<dialog class=modal id=cancel{{ p.id }}><div class=sheet><h2 style="margin:0 0 8px">Send cancellation</h2>
<p class="ty-body sm">Members get an email and a push that include this reason.</p>
<form method=post action="/practices/{{ p.id }}">{{ csrf_field() }}<input type=hidden name=pid value={{ p.id }}><input type=hidden name=back value="{{ back }}">
<label>Reason<textarea class=planfield name=reason rows=4 required></textarea></label>
<button class="rg-btn danger full" name=action value=cancel>Confirm</button></form></div></dialog>
<dialog class=modal id=delete{{ p.id }}><div class=sheet><h2 style="margin:0 0 8px">Delete this practice?</h2>
<p class="ty-body sm">{% if practice_is_month(p) %}{{ practice_when(p) }} at {{ p.location }}.{% else %}{{ fmt_d(p.date) }}, {{ fmt_t(p.start) }}–{{ fmt_t(p.end) }} at {{ p.location }}.{% endif %}</p>
<form method=post action="/practices/{{ p.id }}">{{ csrf_field() }}<input type=hidden name=pid value={{ p.id }}>
<div class=row><button class="rg-btn danger" name=action value=delete>Delete practice</button><button type=button class="rg-btn secondary" onclick="this.closest('dialog').close()">Cancel</button></div></form></div></dialog>
{% endif %}
{% endmacro %}
{% macro mount_map(id, pins, mode, href='', route=None) %}{% if pins %}{{ map_boot() }}{% endif %}<section class="homemap cardmap {{ 'banner' if mode == 'card' else ('still tappable' if mode == 'tap' else 'still') }}" id="{{ id }}" {% if mode == 'tap' and pins %}data-map-open data-directions="{{ pins[0].lat }},{{ pins[0].lng }}" data-map-href="{{ href }}" data-map-label="{{ pins[0].label or 'Location' }}" role=button tabindex=0 aria-label="Map of {{ pins[0].label or 'the location' }}"{% elif mode == 'still' %}aria-hidden=true{% else %}aria-label="Map"{% endif %}></section>
<script>(function(){var pins={{ pins|tojson }};var route={{ route|tojson if route else '[]' }};function start(){var el=document.getElementById({{ id|tojson }});if(el&&window.grunionsMountMap)grunionsMountMap(el,{pins:pins,mode:'{{ 'still' if mode == 'tap' else mode }}',route:route});}if(window.grunionsMountMap)start();else document.addEventListener('DOMContentLoaded',start);})();</script>{% endmacro %}
{% macro event_hero(id, pins, banner_src, label, route=None) %}{% if banner_src %}<div class=evhero><img src="{{ banner_src }}" alt=""></div>{% else %}{{ mount_map(id, pins, 'card', '', route) }}{% endif %}{% endmacro %}
{% macro whos_going(people, kind="going") %}<div class=rg-day>{% if kind == "interested" %}Who's interested{% else %}Who's going{% endif %}</div><div class=list>{% for r in people %}<div class=li>{% if me().is_admin or is_staff() %}<a class=ci-name href="/admin/member/{{ r.id }}">{% else %}<span class=ci-name>{% endif %}{% if r.photo %}<span class="avatar ciav"><img src="/avatar/{{ r.id }}?v={{ r.photo }}" alt="" width="40" height="40"></span>{% else %}<span class="avatar ciav">{{ initials(r) }}</span>{% endif %}<span class=grow style="min-width:0"><span class=ell style="display:block;font-weight:500">{{ display_first(r) }} {{ r.last }}</span></span>{% if kind == 'going' and r.id != me().id %}{% set lo = me().id if me().id < r.id else r.id %}{% set hi = r.id if me().id < r.id else me().id %}<a href="/chat?c=dm:{{ lo }}:{{ hi }}&place=me">Message</a>{% endif %}{% if me().is_admin or is_staff() %}</a>{% else %}</span>{% endif %}</div>{% else %}<div class=li><span class='ty-muted ty-sm'>No one yet.</span></div>{% endfor %}</div>{% endmacro %}
{% macro event_location(id, pins, name, sub, href, route=None, route_min=None, social_name='', social_sub='', social_href='', social_dest='') %}<div class="rg-getthere">{% if pins %}{{ mount_map(id, pins, 'tap', href, route) }}{% endif %}
{% set _ld %}target=_blank rel=noopener{% if pins %} data-directions="{{ pins[0].lat }},{{ pins[0].lng }}"{% endif %}{% endset %}{{ rg_info('LOCATION', name ~ ((' · ' ~ sub) if sub and sub != name else ''), href, _ld) }}
{% if social_name %}{% set _sd %}target=_blank rel=noopener{% if social_dest %} data-directions="{{ social_dest }}"{% endif %}{% endset %}{{ rg_info('SOCIAL' ~ ((' · ' ~ route_min ~ ' MIN DRIVE') if route_min else ''), social_name ~ ((' · ' ~ social_sub) if social_sub and social_sub != social_name else ''), social_href, _sd) }}{% elif route_min %}{{ rg_info('DRIVE', route_min ~ ' min') }}{% endif %}
</div>{% endmacro %}
{% macro lineup_fill(e, mode, past=false) -%}
{%- if past -%}var(--carbon)
{%- elif mode == 'tall' and e.event_type == 'Trip' -%}var(--team-mango)
{%- elif mode == 'tall' and e.event_type in ('Social', 'Meeting', 'Other', 'Volunteer', 'Fundraiser') -%}var(--team-bubblegum)
{%- elif e.event_type in ('Tournament', 'Competition') -%}var(--team-lavender)
{%- elif e.event_type in ('Volunteer', 'Fundraiser') -%}var(--team-bubblegum)
{%- elif e.event_type == 'Trip' -%}var(--team-aqua)
{%- elif e.event_type == 'Clinic' -%}var(--team-aqua)
{%- else -%}var(--team-mango)
{%- endif -%}
{%- endmacro %}
{% macro lineup_card(e, back='/lineup', mode='compact', past=false) %}
{%- set title = e.title if e.title.endswith('.') else e.title ~ '.' -%}
{%- set place = e.city or e.venue -%}
{%- set fill = lineup_fill(e, mode, past) -%}
{%- set ink = 'var(--paper)' if past else 'var(--ink)' -%}
{%- set pill = {'Tournament':'Compete','Competition':'Compete','Volunteer':'Volunteer','Fundraiser':'Volunteer','Trip':'Trips','Clinic':'Clinic'}.get(e.event_type, 'Community') -%}
{%- set over = {'Tournament':'TOURNAMENT','Competition':'TOURNAMENT','Clinic':'CLINIC','Trip':'TRIP','Volunteer':'VOLUNTEER','Fundraiser':'FUNDRAISER'}.get(e.event_type, 'SOCIAL') -%}
{%- set ns = namespace(bar=0, foot=(e.going_n ~ (' went' if past else ' going'))) -%}
{%- if e.capacity -%}
{%- set ns.bar = (e.going_n * 100 / e.capacity)|round(0, 'floor')|int -%}
{%- if ns.bar > 100 %}{% set ns.bar = 100 %}{% endif %}
{%- set ns.foot = e.going_n ~ '/' ~ e.capacity ~ (' team' if e.event_type in ('Tournament', 'Competition') else (' seats' if e.event_type == 'Trip' else ' filled')) -%}
{%- elif e.going_n -%}
{%- set ns.bar = 12 + e.going_n * 8 if e.going_n < 11 else 100 -%}
{%- endif %}
{% if mode == 'tall' %}<div class="lcard ltall card tap tripcard{% if past %} past{% endif %}{% if e.featured %} pinned{% endif %}{% if e.status == 'canceled' %} cancelled{% endif %}" data-kind="{{ e.event_type or '' }}" data-r2="lineup-card" data-variant="tall" style="background:{{ fill }};color:{{ ink }}" onclick="if(event.target.closest('button,a,form,input,select,textarea,label'))return;location.href='/lineup/{{ e.id }}'">
<a class=cardlink href="/lineup/{{ e.id }}"><div class=ltop><span class=lover>{{ 'PINNED · ' if e.featured else '' }}{{ over }}</span>{% if past %}<span class=pastpill>Past</span>{% endif %}</div>
<div class=lmain><div class=ldate>{% if e.tile.wd %}<span>{{ e.tile.wd }}</span>{% endif %}<b>{{ e.tile.dn }}</b><span>{{ e.tile.mo }}</span></div>
<div class=lgrow><b class=lttitle>{{ title }}</b><p class=ltmeta>{{ e.when }}{% if place %} · {{ place }}{% endif %}</p></div></div></a>
{% if e.status != 'published' %}<p class=ltmeta>{{ e.status_label }}{% if e.review_note %} · {{ e.review_note }}{% endif %}</p>
{% elif past %}<div class=ltfoot><span>{{ e.going_n }} went</span></div>
{% else %}<div class=ltfoot><span>{% if e.interested_n and not e.going_n %}{{ e.interested_n }} interested{% else %}{{ e.going_n }} going{% endif %}</span>
<form method=post action=/lineup class=lacts>{{ csrf_field() }}<input type=hidden name=event_id value={{ e.id }}><input type=hidden name=back value="{{ back }}">{{ rsvp_base('e' ~ e.id) }}
<button class="lghost{% if e.mine == 'interested' %} on{% endif %}" name=action value="{{ 'clear' if e.mine == 'interested' else 'interested' }}">Interested</button>
<button class="lfill{% if e.mine == 'going' %} on{% endif %}" name=action value="{{ 'clear' if e.mine == 'going' else 'going' }}">Going</button>
</form></div>{% endif %}
</div>{% else %}<a class="lcard lcompact card tap tripcard{% if past %} past{% endif %}{% if e.status == 'canceled' %} cancelled{% endif %}" data-kind="{{ e.event_type or '' }}" data-r2="lineup-card" data-variant="compact" style="background:{{ fill }};color:{{ ink }}" href="/lineup/{{ e.id }}">
<div class=lctop><span class=lcpill>{{ pill }}</span><span class=lcstatus>{% if e.mine == 'going' %}Registered<svg class=lccheck width="13" height="13" viewBox="0 0 16 16" fill="none" aria-hidden="true"><path d="M3 8.2 6.2 11.5 13 4.5" stroke="#0B0B0C" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>{% elif e.event_type in ('Volunteer', 'Fundraiser') %}Pick a shift{% elif e.event_type == 'Trip' %}Claim a seat{% else %}RSVP{% endif %}</span></div>
<b class=lctitle>{{ title }}</b>
<p class=lcmeta>{{ e.span_label }}{% if place %} · {{ place }}{% endif %}{% if e.mine == 'going' %} · you're registered{% endif %}</p>
{% if not past %}<div class=lcfoot><span class=lctrack><i style="width:{{ ns.bar }}%"></i></span><span>{{ ns.foot }}</span></div>{% else %}<div class=lcfoot><span>{{ e.going_n }} went</span></div>{% endif %}
</a>{% endif %}
{% endmacro %}
{% macro app_header(fade, entry, plus_href, plus_label='Add') %}<header class="homehead apphead{% if fade %} homefade{% endif %}"{% if entry %} data-entry="{{ entry }}"{% endif %}><div class=headmain>{{ caller() }}{% if plus_href %}{{ rg_plus(plus_href, plus_label, 'createSheet' if plus_href == '/events/new' else '') }}{% endif %}</div></header>{% endmacro %}
{% set _tbact %}{% if tab == 'practice' and (me().is_admin or is_staff()) %}<a class=rg-tbdisc href="/practices/{{ x.p.id }}?edit=1" aria-label="Edit practice">{{ rg_icon('edit') }}</a>{% elif tab == 'lineup_event' and e and e.can_edit %}<a class=rg-tbdisc href="/lineup/{{ e.id }}/edit" aria-label="Edit event">{{ rg_icon('edit') }}</a>{% elif tab == 'person' %}<button type=button class="rg-tbdisc morebtn" id=profileMore aria-label="Profile menu">{{ rg_icon('more') }}</button>{% elif tab == 'member' and me().is_admin %}<button type=button class="rg-tbdisc viewonly" id=profileEdit aria-label="Edit member">{{ rg_icon('edit') }}</button><button type=submit class="rg-btn primary editonly" id=profileSave form=memberForm name=action value=edit>Save</button>{% endif %}{% endset %}{% if nav_kind == 'sheet' and me() and tab in ('flow', 'settings_sheet') %}{{ rg_sheet_head(nav_title, nav_back_href) }}{% elif nav_topbar and me() and not (editing or plan_editing) %}{{ rg_top_bar('compact', nav_back_title, back_href=nav_back_href, back_label=nav_back_title, action_html=_tbact) }}{% elif tab == 'profile' and me() %}<header class=profilebar>
<div class=left><button type=button class="profileback viewonly" id=profileBack aria-label="Back"><svg width="24" height="24" viewBox="0 0 256 256" fill="currentColor" aria-hidden="true"><path d="M224,128a8,8,0,0,1-8,8H59.31l58.35,58.34a8,8,0,0,1-11.32,11.32l-72-72a8,8,0,0,1,0-11.32l72-72a8,8,0,0,1,11.32,11.32L59.31,120H216A8,8,0,0,1,224,128Z"/></svg></button><button type=button class="profileact editonly" id=profileCancel>Cancel</button></div>
<h1>Profile</h1>
<div class=right><button type=button class="profileact viewonly morebtn" id=profileMore aria-label="Profile menu">•••</button><button type=button id=profileEdit hidden>Edit</button><button type=submit class="profileact savebtn editonly" id=profileSave form=profileForm>Save</button></div>
</header>{% elif me() and tab == 'person' %}<header class=profilebar>
<div class=left><a class=profileback href="/chat?view=list" aria-label="Back"><svg width="24" height="24" viewBox="0 0 256 256" fill="currentColor" aria-hidden="true"><path d="M224,128a8,8,0,0,1-8,8H59.31l58.35,58.34a8,8,0,0,1-11.32,11.32l-72-72a8,8,0,0,1,0-11.32l72-72a8,8,0,0,1,11.32,11.32L59.31,120H216A8,8,0,0,1,224,128Z"/></svg></a></div>
<h1>Profile</h1>
<div class=right><button type=button class="profileact morebtn" id=profileMore aria-label="Profile menu">•••</button></div>
</header>{% elif me() and tab == 'privacy' %}<header class=profilebar>
<div class=left><a class=profileback href="/profile" aria-label="Back"><svg width="24" height="24" viewBox="0 0 256 256" fill="currentColor" aria-hidden="true"><path d="M224,128a8,8,0,0,1-8,8H59.31l58.35,58.34a8,8,0,0,1-11.32,11.32l-72-72a8,8,0,0,1,0-11.32l72-72a8,8,0,0,1,11.32,11.32L59.31,120H216A8,8,0,0,1,224,128Z"/></svg></a></div>
<h1>Privacy</h1>
<div class=right></div>
</header>{% elif me() and tab == 'member' %}<header class=profilebar>
<div class=left><button type=button class="profileback viewonly" id=profileBack aria-label="Back"><svg width="24" height="24" viewBox="0 0 256 256" fill="currentColor" aria-hidden="true"><path d="M224,128a8,8,0,0,1-8,8H59.31l58.35,58.34a8,8,0,0,1-11.32,11.32l-72-72a8,8,0,0,1,0-11.32l72-72a8,8,0,0,1,11.32,11.32L59.31,120H216A8,8,0,0,1,224,128Z"/></svg></button>{% if me().is_admin %}<button type=button class="profileact editonly" id=profileCancel>Cancel</button>{% endif %}</div>
<h1>{{ display_first(m) }} {{ m.last }}</h1>
<div class=right>{% if me().is_admin %}<button type=button class="profileact viewonly" id=profileEdit>Edit</button><button type=submit class="profileact savebtn editonly" id=profileSave form=memberForm name=action value=edit>Save</button>{% endif %}</div>
</header>{% elif me() and tab == 'lineup_edit' %}<header class=profilebar><div class=left><a class=profileact href=/lineup>Cancel</a></div><h1>Event</h1><div class=right><button type=submit class="profileact savebtn" form=eventForm name=action value=save>{{ save_label or 'Save' }}</button></div></header>{% elif me() and tab == 'lineup_event' %}<header class=profilebar><div class=left>{% if from_admin %}<a class=profileback href="/admin?date={{ admin_date }}" aria-label="Back">{% else %}<a class=profileback href=/lineup aria-label="Back">{% endif %}<svg width="24" height="24" viewBox="0 0 256 256" fill="currentColor" aria-hidden="true"><path d="M224,128a8,8,0,0,1-8,8H59.31l58.35,58.34a8,8,0,0,1-11.32,11.32l-72-72a8,8,0,0,1,0-11.32l72-72a8,8,0,0,1,11.32,11.32L59.31,120H216A8,8,0,0,1,224,128Z"/></svg></a></div><h1>Event</h1><div class=right>{% if e.can_edit %}<a class=profileact href="/lineup/{{ e.id }}/edit">Edit</a>{% endif %}</div></header>{% elif me() and tab == 'series_edit' %}<header class=profilebar><div class=left><a class=profileact href=/practices>Cancel</a></div><h1>Series</h1><div class=right><button type=submit class="profileact savebtn" form=seriesForm>Save</button></div></header>{% elif me() and tab == 'practice' %}<header class=profilebar><div class=left>{% if editing or plan_editing %}<a class=profileact href="/practices/{{ x.p.id }}{% if from_admin %}?from=admin{% endif %}">Cancel</a>{% else %}<a class=profileback href="{% if from_admin %}/admin?date={{ x.p.date }}{% else %}/practices{% endif %}" aria-label="Back"><svg width="24" height="24" viewBox="0 0 256 256" fill="currentColor" aria-hidden="true"><path d="M224,128a8,8,0,0,1-8,8H59.31l58.35,58.34a8,8,0,0,1-11.32,11.32l-72-72a8,8,0,0,1,0-11.32l72-72a8,8,0,0,1,11.32,11.32L59.31,120H216A8,8,0,0,1,224,128Z"/></svg></a>{% endif %}</div><h1>{% if editing or plan_editing %}Edit practice{% else %}Practice{% endif %}</h1><div class=right>{% if editing %}<button type=submit class="profileact savebtn" form=practiceForm name=action value=edit>Save</button>{% elif plan_editing %}<button type=submit class="profileact savebtn" form=practiceForm name=action value=plan>Save</button>{% elif me().is_admin or is_staff() %}<a class=profileact href="/practices/{{ x.p.id }}?edit=1{% if from_admin %}&amp;from=admin{% endif %}">Edit</a>{% endif %}</div></header>{% elif me() and tab == 'event_new' %}<header class=profilebar><div class=left><a class=profileact href="{{ plan_back }}">Cancel</a></div><h1>{{ plan_title or 'Create event' }}</h1><div class=right>{% if plan_save %}<button type=submit class="profileact savebtn" form=planForm name=action value=preview>{{ plan_save }}</button>{% endif %}</div></header>{% elif me() and tab == 'chat' %}{% elif me() %}{% call app_header(tab == 'home' or tab == 'practices', ('schedule' if tab == 'practices' else 'home') if (tab == 'home' or tab == 'practices') else '', ('/events/new' if can_host_practice() and (tab == 'lineup' or (tab == 'practices' and not sched_home)) else ('/lineup/new' if tab == 'lineup' else '')), 'Create' if can_host_practice() else 'Suggest an event') %}{% if tab == 'practices' %}{% if sched_list %}<div class=displayhead><h1>Schedule</h1></div>{% else %}<div class=displayhead><h1>Schedule</h1></div>{% endif %}{% elif tab == 'home' %}<div class=displayhead><div class=displayeye>{{ hi_membership() }}</div><h1>Hi, {{ display_first(me()) }}</h1></div>{% elif tab == 'discover' %}<h1>Discover.</h1>{% elif tab == 'calendar' %}<div class=displayhead><p class=displayeye>{{ display_first(me()) }} {{ me().last }}</p><h1>Calendar</h1></div>{% elif tab == 'manage' %}<div class=displayhead><h1>Manage</h1></div>{% elif tab == 'admin' %}{% elif tab == 'lineup' %}<div class=displayhead><h1>Lineup</h1></div>{% elif tab == 'notifications' %}<h1>Notifications</h1>{% elif tab in ('appearance', 'rides', 'availability', 'flow') %}{% else %}<h1>{{ display_first(me()) }}</h1>{% endif %}{% endcall %}{% else %}<header><a class=brand href=/ aria-label=Regulars><img src="/static/icons/icon-192.png?v=119" alt=""></a></header>{% endif %}<main>
{% if me() and can_host_practice() %}<dialog id=createSheet class="botsheet profmenu modal" data-sheet-name=create><div class=sheet><div class=grab aria-hidden=true></div>
<h2 class=newtitle>Create.</h2><p class=ty-muted>What are you planning?</p>
{{ rg_label('Team schedule') }}
<div class=newcard>
<a class=newrow href="/events/new?lane=schedule&amp;type=practice"><span class=grow><b>Practice</b><small>Shows on Schedule · members tap Going</small></span><span class=chatgo>›</span></a>
<a class=newrow href="/events/new?lane=schedule&amp;type=scrimmage"><span class=grow><b>Scrimmage</b><small>Against another team</small></span><span class=chatgo>›</span></a>
<a class=newrow href="/events/new?lane=schedule&amp;type=game"><span class=grow><b>Game</b><small>League or tournament game</small></span><span class=chatgo>›</span></a>
</div>
{{ rg_label('Lineup') }}
<div class=newcard>
<a class=newrow href="/events/new?lane=lineup"><span class=grow><b>Lineup event</b><small>Tournaments, camps, trips and socials</small></span><span class=chatgo>›</span></a>
</div>
</div></dialog>{% endif %}
{% for cat, msg in get_flashed_messages(with_categories=true) %}{% if cat == 'toast' %}<div class="toast noprint" role=status>{{msg}}</div>{% else %}<div class=note>{{msg|safe}}</div>{% endif %}{% endfor %}
<script>document.querySelectorAll('.toast').forEach(function(t){setTimeout(function(){t.remove()},3000)})</script>
{% macro push_card() %}{{ rg_callout_card('Notifications', 'Allow notifications for chat, practice reminders, and membership expiry. This works on Android, and on iPhone once Regulars is on your Home Screen (iOS 16.4 or later).', 'Allow notifications', 'allowPush', 'Notification settings', '/notifications', 'lavender', 'pushCard', '<p id=iosPushHint hidden>On iPhone or iPad, add Regulars to your Home Screen to get notifications. Tap Share, then Add to Home Screen, and open the app from there (iOS 16.4 or later).</p><p id=pushDenied hidden>Notifications are blocked in this browser. Allow them in the site settings, then come back.</p>', True) }}{% endmacro %}"""

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

def _glyph(paths):
    return '<svg class="nav3-glyph" width="20" height="20" viewBox="0 0 20 20" fill="none" aria-hidden="true">' + "".join(
        '<path d="%s" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round"/>' % d for d in paths) + "</svg>"

_NAV3_GLYPHS = {
    "chevron_left": ("M12.5 4.5L7 10L12.5 15.5",),
    "chevron_right": ("M7.5 4.5L13 10L7.5 15.5",),
    "plus": ("M10 4V16M4 10H16",),
    "edit": ("M4 16L4.5 13L13.5 4L16 6.5L7 15.5L4 16Z", "M12 5.5L14.5 8"),
    "more": ("M5 10H5.01M10 10H10.01M15 10H15.01",),
    "close": ("M5 5L15 15M15 5L5 15",),
    "search": ("M14.25 9C14.25 11.8995 11.8995 14.25 9 14.25C6.10051 14.25 3.75 11.8995 3.75 9C3.75 6.10051 6.10051 3.75 9 3.75C11.8995 3.75 14.25 6.10051 14.25 9Z", "M13.2 13.2L16.5 16.5"),
    "calendar": ("M5.5 5H14.5C15.6046 5 16.5 5.89543 16.5 7V15C16.5 16.1046 15.6046 17 14.5 17H5.5C4.39543 17 3.5 16.1046 3.5 15V7C3.5 5.89543 4.39543 5 5.5 5Z", "M3.5 8.5H16.5M7 3.5V6.5M13 3.5V6.5"),
    "pin": ("M10 17.5C10 17.5 15.5 12.3 15.5 8.5C15.5 7.04131 14.9205 5.64236 13.8891 4.61091C12.8576 3.57946 11.4587 3 10 3C8.54131 3 7.14236 3.57946 6.11091 4.61091C5.07946 5.64236 4.5 7.04131 4.5 8.5C4.5 12.3 10 17.5 10 17.5Z", "M11.75 8.5C11.75 9.4665 10.9665 10.25 10 10.25C9.0335 10.25 8.25 9.4665 8.25 8.5C8.25 7.5335 9.0335 6.75 10 6.75C10.9665 6.75 11.75 7.5335 11.75 8.5Z"),
    "chat": ("M4 4.5H16C16.3978 4.5 16.7794 4.65804 17.0607 4.93934C17.342 5.22064 17.5 5.60218 17.5 6V13C17.5 13.3978 17.342 13.7794 17.0607 14.0607C16.7794 14.342 16.3978 14.5 16 14.5H9L5.5 17V14.5H4C3.60218 14.5 3.22064 14.342 2.93934 14.0607C2.65804 13.7794 2.5 13.3978 2.5 13V6C2.5 5.60218 2.65804 5.22064 2.93934 4.93934C3.22064 4.65804 3.60218 4.5 4 4.5Z",),
    "settings": ("M12.4 10C12.4 11.3255 11.3255 12.4 10 12.4C8.67452 12.4 7.6 11.3255 7.6 10C7.6 8.67452 8.67452 7.6 10 7.6C11.3255 7.6 12.4 8.67452 12.4 10Z", "M10 3.5V5.7M10 14.3V16.5M3.5 10H5.7M14.3 10H16.5M5.4 5.4L7 7M13 13L14.6 14.6M14.6 5.4L13 7M7 13L5.4 14.6"),
    "ticket": ("M4 5C2.9 5 2 5.9 2 7V8.5C2.8 8.5 3.5 9.2 3.5 10C3.5 10.8 2.8 11.5 2 11.5V13C2 14.1 2.9 15 4 15H16C17.1 15 18 14.1 18 13V11.5C17.2 11.5 16.5 10.8 16.5 10C16.5 9.2 17.2 8.5 18 8.5V7C18 5.9 17.1 5 16 5H4Z", "M12 6.5V7.5M12 9.5V10.5M12 12.5V13.5"),
}
_NAV3_GLYPHS["manage"] = _NAV3_GLYPHS["settings"]
_NAV3_GLYPHS["people"] = ("M7.5 9.5C9.15685 9.5 10.5 8.15685 10.5 6.5C10.5 4.84315 9.15685 3.5 7.5 3.5C5.84315 3.5 4.5 4.84315 4.5 6.5C4.5 8.15685 5.84315 9.5 7.5 9.5Z",
                          "M2 16.5C2 13.7386 4.46243 11.5 7.5 11.5C10.5376 11.5 13 13.7386 13 16.5",
                          "M13 9.5C14.3807 9.5 15.5 8.38071 15.5 7C15.5 5.61929 14.3807 4.5 13 4.5", "M15.25 11.9C16.85 12.55 18 14.15 18 16.5")
_NAV3_GLYPHS["profile"] = _NAV3_GLYPHS["people"]  # Figma Nav 3.0: Me › Profile uses Icon / People

def nav_icon(key):
    return _glyph(_NAV3_GLYPHS.get(key) or _NAV3_GLYPHS["pin"])

_HOME_ON = "tab=='home' or tab=='practices' or tab=='practice' or tab=='series_edit'"
_LINEUP_ON = "tab=='lineup' or tab=='lineup_edit' or tab=='lineup_event'"
TABS = ("""</main>{% set nav = nav_context() %}{% if nav.show and not (nav_kind == 'sheet' and tab == 'flow') and tab != 'event_new' and tab != 'lineup_edit' and tab != 'series_edit' and not (tab=='practice' and editing) %}<nav class="nav3 noprint" data-place="{{ nav.place }}" aria-label="Places">
<button type="button" class="nav3-crest" aria-expanded="false" aria-controls="crestMenu" aria-label="Open places"><span class="nav3-crest-face"><img class="nav3-logo lg lime" src="/static/nav/mark-lime.svg" width="32" height="13" alt=""><img class="nav3-logo lg ink" src="/static/nav/mark-ink.svg" width="32" height="13" alt=""><img class="nav3-logo sm ink" src="/static/nav/mark-ink.svg" width="26" height="10" alt="">{% if nav.place == 'me' and me().photo %}<img class="nav3-photo" src="/avatar/{{ me().id }}?v={{ me().photo }}" alt="">{% endif %}<span class="nav3-initials">{{ nav.crest }}</span></span><span class="nav3-more" aria-hidden="true">⋯</span><span class="nav3-switch-copy"><b>{{ nav.switch_title }}</b><small>{{ nav.switch_sub }}</small></span><span class="nav3-chevron" aria-hidden="true"></span></button>
<p class="nav3-menu-label">Menu</p>
<span class="nav3-rule"></span>
<div class="nav3-tabs"><span class="nav3-slide" aria-hidden="true"></span>{% for key, label, href, on in nav.tabs %}<a href="{{ href }}" data-tab="{{ key }}" {% if on %}class=on aria-current=page {% endif %}>{{ nav_icon(key)|safe }}<span class="nav3-dot"></span><span class="nav3-meta"><span class="nav3-label">{{ label }}</span>{% if label == 'Chat' and nav.chat_unread %}<span class=nav3-badge>{{ nav.chat_unread }}</span>{% endif %}</span></a>{% endfor %}</div>
</nav>
<dialog id="crestMenu" class="crestmenu" tabindex="-1">
<p class="crestlabel">GO TO</p>
<a class="crestrow{% if nav.place == 'everything' %} here{% endif %}" href="{{ nav.everything_href }}"><span class="crestmark brand"><img src="/static/nav/mark-ink.svg" width="26" height="10" alt=""></span><span><b>Everything</b><small>{{ nav.everything_sub }}</small></span></a>
<a class="crestrow{% if nav.place == 'me' %} here{% endif %}" href="/calendar"><span class="crestmark who">{% if me().photo %}<img src="/avatar/{{ me().id }}?v={{ me().photo }}" alt="">{% else %}{{ initials(me()) }}{% endif %}</span><span><b>{{ nav.name }}</b><small>Calendar · chat · profile</small></span></a>
<span class="crestline"></span>
<p class="crestlabel">YOUR TEAMS</p>
<a class="crestrow{% if nav.place == 'team' %} here{% endif %}" href="/practices"><span class="crestmark team">G</span><span><b>Grunions</b><small>Default · opens here</small></span><span class="rolechip role-{{ nav.role|lower }}">{{ nav.role }}</span></a>
{% if nav.show_find %}<a class="crestgo" href="/discover">+ Find or join a team</a>{% endif %}
<a class="crestout" href="/logout">Log out</a>
</dialog>{% endif %}
<script>
if('serviceWorker' in navigator) navigator.serviceWorker.register('/sw.js?v=119');
function grunionsClearTransition(){try{var t=document.activeViewTransition; if(t&&t.skipTransition) t.skipTransition();}catch(e){}}
grunionsClearTransition();
window.addEventListener('pageshow', grunionsClearTransition);
function grunionsCaptureArea(){
 var replaced=false;
 try{
  replaced=sessionStorage.getItem('grunionsTabReplace')==='1';
  sessionStorage.removeItem('grunionsTabReplace');
  if(replaced) return;
  var nav=sessionStorage.getItem('grunionsNavFrom')||'';
  var path=nav.split('?')[0];
  if(path && path!==location.pathname){
   sessionStorage.setItem('grunionsAreaFrom', nav);
   sessionStorage.setItem('grunionsOpenedFrom', nav);
  }
  else sessionStorage.removeItem('grunionsAreaFrom');
 }catch(e){}
}
function grunionsLeave(fallback){
 var dest='';
 try{ dest=sessionStorage.getItem('grunionsOpenedFrom')||sessionStorage.getItem('grunionsAreaFrom')||''; }catch(e){}
 var path=dest.split('?')[0].split('#')[0];
 if(path && path!==location.pathname){ location.href=dest; return; }
 location.href=fallback||'/home';
}
grunionsCaptureArea();
(function(){
 var crest=document.querySelector('.nav3-crest'), menu=document.getElementById('crestMenu');
 if(!crest||!menu) return;
 function shut(){ if(menu.open) menu.close(); crest.setAttribute('aria-expanded','false'); }
 crest.addEventListener('click', function(){
  if(menu.open) shut();
  else { menu.showModal(); menu.focus(); crest.setAttribute('aria-expanded','true'); }
 });
 menu.addEventListener('click', function(e){ if(e.target===menu) shut(); });
 menu.addEventListener('close', function(){ crest.setAttribute('aria-expanded','false'); });
})();
function nav3Reduced(){ return !!(window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches); }
function nav3Place(animate){
 var tabs=document.querySelector('nav.nav3 .nav3-tabs');
 if(!tabs) return;
 var slide=tabs.querySelector('.nav3-slide'), on=tabs.querySelector('a.on');
 if(!slide||!on) return;
 var nextW=on.offsetWidth, nextH=on.offsetHeight;
 if(!nextW||!nextH) return;
 var jump=!animate || nav3Reduced() || !slide.offsetWidth || Math.abs(slide.offsetWidth-nextW)>48;
 if(jump) slide.style.transition='none';
 else slide.style.transition='';
 slide.classList.toggle('manage', on.getAttribute('data-tab')==='manage');
 slide.style.left=on.offsetLeft+'px';
 slide.style.top=on.offsetTop+'px';
 slide.style.width=nextW+'px';
 slide.style.height=nextH+'px';
 if(jump){ slide.offsetWidth; slide.style.transition=''; }
}
function nav3MoveTo(anchor){
 var tabs=anchor&&anchor.closest&&anchor.closest('.nav3-tabs');
 if(!tabs||anchor.classList.contains('on')) return;
 var slide=tabs.querySelector('.nav3-slide');
 var nodes=[].slice.call(tabs.querySelectorAll('.nav3-glyph,.nav3-label'));
 var before=nodes.map(function(n){ return n.getBoundingClientRect(); });
 var old=slide?{l:slide.offsetLeft,t:slide.offsetTop,w:slide.offsetWidth,h:slide.offsetHeight}:null;
 tabs.querySelectorAll('a').forEach(function(x){ x.classList.remove('on'); x.removeAttribute('aria-current'); });
 anchor.classList.add('on');
 anchor.setAttribute('aria-current','page');
 if(nav3Reduced()){ nav3Place(false); return; }
 nodes.forEach(function(n,i){
  var a=before[i], b=n.getBoundingClientRect();
  var dx=a.left-b.left, dy=a.top-b.top;
  if(Math.abs(dx)<0.5 && Math.abs(dy)<0.5) return;
  n.style.transition='none';
  n.style.transform='translate('+dx+'px,'+dy+'px)';
 });
 if(slide&&old){
  slide.style.transition='none';
  slide.style.left=old.l+'px'; slide.style.top=old.t+'px'; slide.style.width=old.w+'px'; slide.style.height=old.h+'px';
 }
 requestAnimationFrame(function(){ requestAnimationFrame(function(){
  nodes.forEach(function(n){ n.style.transition=''; n.style.transform=''; });
  if(slide) slide.style.transition='';
  nav3Place(true);
 }); });
}
function nav3Sync(newNav){
 var nav=document.querySelector('nav.nav3');
 if(!nav||!newNav) return;
 var tabs=nav.querySelector('.nav3-tabs');
 if(!tabs) return;
 var incoming=[].slice.call(newNav.querySelectorAll('.nav3-tabs a'));
 var current=[].slice.call(tabs.querySelectorAll('a'));
 var same=current.length===incoming.length;
 if(same) for(var i=0;i<current.length;i++) if(current[i].getAttribute('href')!==incoming[i].getAttribute('href')) same=false;
 nav.setAttribute('data-place', newNav.getAttribute('data-place')||nav.getAttribute('data-place')||'');
 var face=nav.querySelector('.nav3-crest-face'), nface=newNav.querySelector('.nav3-crest-face');
 if(face&&nface&&face.innerHTML!==nface.innerHTML) face.innerHTML=nface.innerHTML;
 var copy=nav.querySelector('.nav3-switch-copy'), ncopy=newNav.querySelector('.nav3-switch-copy');
 if(copy&&ncopy) copy.innerHTML=ncopy.innerHTML;
 var menu=document.getElementById('crestMenu'), nmenu=newNav.ownerDocument.getElementById('crestMenu');
 if(menu&&nmenu){
  var rows=[].slice.call(menu.querySelectorAll('.crestrow')), nrows=[].slice.call(nmenu.querySelectorAll('.crestrow'));
  for(var r=0;r<rows.length&&r<nrows.length;r++) rows[r].className=nrows[r].className;
  var chip=menu.querySelector('.rolechip'), nchip=nmenu.querySelector('.rolechip');
  if(chip&&nchip){ chip.className=nchip.className; chip.textContent=nchip.textContent; }
  var sub=menu.querySelector('.crestmark.who')&&menu.querySelector('.crestmark.who').parentElement.querySelector('small');
  var nsub=nmenu.querySelector('.crestmark.who')&&nmenu.querySelector('.crestmark.who').parentElement.querySelector('small');
  if(sub&&nsub) sub.textContent=nsub.textContent;
 }
 if(same){
  var target=null, changed=false;
  for(var k=0;k<current.length;k++){
   var now=incoming[k].classList.contains('on');
   if(current[k].classList.contains('on')!==now) changed=true;
   if(now) target=current[k];
  }
  if(changed&&target) nav3MoveTo(target);
  return;
 }
 var slide=tabs.querySelector('.nav3-slide');
 var oldBox=slide?slide.getBoundingClientRect():null;
 [].slice.call(tabs.querySelectorAll('a')).forEach(function(a){ a.remove(); });
 incoming.forEach(function(a){ tabs.appendChild(document.importNode(a, true)); });
 if(!slide||!oldBox||nav3Reduced()){ nav3Place(false); return; }
 var box=tabs.getBoundingClientRect();
 slide.style.transition='none';
 slide.style.left=(oldBox.left-box.left)+'px';
 slide.style.top=(oldBox.top-box.top)+'px';
 slide.style.width=oldBox.width+'px';
 slide.style.height=oldBox.height+'px';
 slide.offsetWidth;
 requestAnimationFrame(function(){ slide.style.transition=''; nav3Place(true); });
}
function nav3Follow(anchor){
 if(!anchor) return;
 var menu=document.getElementById('crestMenu');
 if(menu&&menu.open) menu.close();
 var tab=anchor.closest('nav.nav3 .nav3-tabs a');
 if(tab) nav3MoveTo(tab);
 if(window.grunionsGo) grunionsGo(anchor.href, false);
 else location.href=anchor.href;
}
(function(){
 nav3Place(false);
 var swipe={x:0,y:0,on:false,used:false};
 document.addEventListener('pointerdown', function(e){
  swipe.used=false; swipe.on=false;
  if(window.innerWidth>=768 || e.button) return;
  var nav=e.target.closest&&e.target.closest('nav.nav3');
  if(!nav) return;
  var menu=document.getElementById('crestMenu');
  if(menu&&menu.open) return;
  swipe.x=e.clientX; swipe.y=e.clientY; swipe.on=true;
 });
 document.addEventListener('pointerup', function(e){
  if(!swipe.on) return;
  swipe.on=false;
  var dx=e.clientX-swipe.x, dy=e.clientY-swipe.y;
  if(Math.abs(dx)<48 || Math.abs(dx)<=Math.abs(dy)) return;
  var links=[].slice.call(document.querySelectorAll('nav.nav3 .nav3-tabs a'));
  var i=-1; links.forEach(function(a,n){ if(a.classList.contains('on')) i=n; });
  var next=dx<0?i+1:i-1;
  if(next<0 || next>=links.length) return;
  swipe.used=true;
  nav3Follow(links[next]);
 });
 document.addEventListener('click', function(e){
  if(swipe.used){ swipe.used=false; e.preventDefault(); e.stopPropagation(); return; }
  if(e.button||e.metaKey||e.ctrlKey||e.shiftKey||e.altKey) return;
  var a=e.target.closest&&e.target.closest('a[href]');
  if(!a||!(a.closest('nav.nav3 .nav3-tabs')||a.closest('dialog.crestmenu'))) return;
  var abs; try{ abs=new URL(a.href, location.href); }catch(err){ return; }
  if(abs.origin!==location.origin||abs.pathname==='/logout') return;
  e.preventDefault();
  e.stopPropagation();
  if(abs.pathname===location.pathname&&abs.search===location.search){
   var openMenu=document.getElementById('crestMenu');
   if(openMenu&&openMenu.open) openMenu.close();
   return;
  }
  nav3Follow(a);
 }, true);
 window.addEventListener('resize', function(){ nav3Place(false); });
})();
document.addEventListener('click',function(e){
 if(e.button||e.metaKey||e.ctrlKey||e.shiftKey||e.altKey) return;
 var a=e.target.closest&&e.target.closest('a[href]');
 if(!a||!a.closest('[data-seg]')) return;
 var abs; try{abs=new URL(a.href,location.href);}catch(err){return;}
 if(abs.origin!==location.origin) return;
 e.preventDefault();
 e.stopPropagation();
 var next=abs.pathname+abs.search+abs.hash;
 if(abs.pathname==='/profile'||!document.querySelector('nav.nav3, nav.tabs')){
  try{sessionStorage.setItem('grunionsTabReplace','1')}catch(err){}
  location.replace(next); return;
 }
 grunionsSaveScroll();
 grunionsGo(abs.href,false,true);
},true);
document.addEventListener('submit',function(e){
 if(e.defaultPrevented) return;
 var form=e.target;
 if(!form||(form.getAttribute('method')||'get').toLowerCase()!=='get') return;
 if(form.target&&form.target!=='_self') return;
 var abs; try{abs=new URL(form.getAttribute('action')||location.pathname,location.href);}catch(err){return;}
 if(abs.origin!==location.origin||abs.pathname!==location.pathname) return;
 var params=new URLSearchParams();
 [].slice.call(form.elements||[]).forEach(function(el){
  if(!el.name||el.disabled||el.type==='submit'||el.type==='button'||el.type==='image') return;
  if((el.type==='checkbox'||el.type==='radio')&&!el.checked) return;
  params.append(el.name, el.value);
 });
 var next=abs.pathname+(params.toString()?'?'+params.toString():'')+(abs.hash||'');
 e.preventDefault();
 if(abs.pathname==='/profile'||!document.querySelector('nav.nav3, nav.tabs')){
  try{sessionStorage.setItem('grunionsTabReplace','1')}catch(err){}
  location.replace(next); return;
 }
 grunionsGo(next,false,true);
},true);
if(window.grunionsDropzones) grunionsDropzones();
function grunionsEditor(){
 function optName(input){
  var lab=input.closest('label');
  return (lab&&lab.getAttribute('data-label'))||'';
 }
 function chosen(box){
  return [].slice.call(box.querySelectorAll('input')).filter(function(i){ return i.checked && i.id!=='allLevels' && i.value; }).map(optName).filter(Boolean);
 }
 function summarize(names, empty){
  if(!names.length) return empty||'Not set';
  if(names.length===1) return names[0];
  if(names.length===2) return names[0]+' + 1';
  return names.length+' selected';
 }
 function paintBox(box){
  var key=box.getAttribute('data-sum');
  var target=document.querySelector('[data-for="'+key+'"]');
  if(!target) return;
  var all=box.querySelector('#allLevels');
  if(all&&all.checked){ target.textContent='All levels'; return; }
  if(key==='division'||key==='social'||key==='lead'){
   var on=box.querySelector('input:checked');
   var name=on?optName(on):'';
   if(key==='division'&&on&&on.value==='custom'){
    var custom=document.querySelector('[name=division_custom]');
    if(custom&&custom.value.trim()) name=custom.value.trim();
    var divLab=document.getElementById('divCustom'); if(divLab) divLab.hidden=false;
   } else if(key==='division'){ var divLab2=document.getElementById('divCustom'); if(divLab2) divLab2.hidden=true; }
   if(key==='social'&&on&&on.value==='Other'){
    var label=document.querySelector('[name=social_custom]');
    if(label&&label.value.trim()) name=label.value.trim();
    var customLab=document.getElementById('socialCustom'); if(customLab) customLab.hidden=false;
   } else if(key==='social'){ var customLab2=document.getElementById('socialCustom'); if(customLab2) customLab2.hidden=true; }
   target.textContent=name||box.getAttribute('data-empty')||'Not set';
   if(key==='social'){ var soc=document.getElementById('socialSum'); if(soc&&name) soc.textContent=name; }
   return;
  }
  target.textContent=summarize(chosen(box), box.getAttribute('data-empty'));
 }
 document.querySelectorAll('[data-sum]').forEach(function(box){
  box.addEventListener('change', function(){ paintBox(box); });
  paintBox(box);
 });
 var boxes=[].slice.call(document.querySelectorAll('input[name=level]'));
 var all=document.getElementById('allLevels');
 function syncAll(){ if(all) all.checked=boxes.length&&boxes.every(function(b){ return b.checked; }); }
 if(all) all.addEventListener('change', function(){ boxes.forEach(function(b){ b.checked=all.checked; }); var box=all.closest('[data-sum]'); if(box) paintBox(box); });
 boxes.forEach(function(b){ b.addEventListener('change', function(){ syncAll(); var box=b.closest('[data-sum]'); if(box) paintBox(box); }); });
 syncAll();
 function syncCoaches(){
  var chosen={};
  document.querySelectorAll('#sheetCoaches input[name='+'coach]').forEach(function(c){ if(c.checked) chosen[c.value]=c.getAttribute('data-name')||'Coach'; });
  document.querySelectorAll('[data-lead]').forEach(function(row){
   var id=row.getAttribute('data-lead'); if(!id) return;
   row.hidden=!chosen[id];
   var radio=row.querySelector('input');
   if(row.hidden&&radio&&radio.checked){ var none=document.querySelector('#sheetLead input[name=lead][value=""]'); if(none) none.checked=true; }
  });
  var leadBox=document.querySelector('[data-sum=lead]'); if(leadBox) paintBox(leadBox);
  var coachBox=document.querySelector('[data-sum=coaches]'); if(coachBox) paintBox(coachBox);
  var list=document.getElementById('assignedCoaches'); if(!list) return;
  list.innerHTML='';
  Object.keys(chosen).forEach(function(id){
   var b=document.createElement('button'); b.type='button'; b.className='li selfield';
   b.innerHTML='<span class=selfieldk></span><span class=selfieldv>Details</span>';
   b.querySelector('.selfieldk').textContent=chosen[id];
   b.onclick=function(){
    var home=document.getElementById('focusHome'), slot=document.getElementById('focusSlot'), title=document.getElementById('focusTitle');
    if(slot){ while(slot.firstChild){ var back=document.getElementById('focusHome'); if(back) back.appendChild(slot.firstChild); } }
    var field=home&&home.querySelector('[data-coach="'+id+'"]');
    if(slot&&field) slot.appendChild(field);
    if(title) title.textContent=chosen[id];
    var sheet=document.getElementById('focusSheet'); if(sheet&&sheet.showModal) sheet.showModal();
   };
   list.appendChild(b);
  });
 }
 document.querySelectorAll('#sheetCoaches input[name='+'coach],#sheetLead input[name=lead]').forEach(function(el){ el.addEventListener('change', syncCoaches); });
 if(document.getElementById('sheetCoaches')) syncCoaches();
 document.querySelectorAll('[data-sheetsearch]').forEach(function(input){
  input.addEventListener('input', function(){
   var q=input.value.trim().toLowerCase();
   var sheet=input.closest('dialog'); if(!sheet) return;
   sheet.querySelectorAll('[data-search]').forEach(function(row){ row.hidden=!!(q&&(row.getAttribute('data-search')||'').toLowerCase().indexOf(q)<0); });
  });
 });
 document.querySelectorAll('[data-sheetdone]').forEach(function(b){ b.addEventListener('click', function(){ var d=b.closest('dialog'); if(d) d.close(); }); });
 var toggle=document.getElementById('socialToggle'), sbody=document.getElementById('socialBody'), clearer=document.getElementById('socialClear');
 if(toggle&&sbody) toggle.addEventListener('click', function(){ sbody.hidden=false; if(clearer) clearer.disabled=true; });
 var removeSocial=document.getElementById('socialRemove');
 if(removeSocial&&sbody) removeSocial.addEventListener('click', function(){
  sbody.querySelectorAll('input[type=radio][name=social_kind]').forEach(function(r){ r.checked=false; });
  if(clearer) clearer.disabled=false;
  sbody.hidden=true;
  var sum=document.getElementById('socialSum'); if(sum) sum.textContent='Not added';
 });
 document.addEventListener('focusin', function(e){
  if(!document.body.classList.contains('editor')&&!document.body.classList.contains('profile-edit')) return;
  var el=e.target; if(!el||!el.scrollIntoView||el.closest('dialog')) return;
  var type=(el.type||'').toLowerCase();
  if(type==='radio'||type==='checkbox'||type==='hidden'||el.closest('.plancard,.actseg,.switch,.switchrow')) return;
  setTimeout(function(){ try{ el.scrollIntoView({block:'center'}); }catch(err){} }, 80);
 });
}
if(document.querySelector('[data-editorform],#sheetLevels')) grunionsEditor();
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
// Chart card (02 Components): dots switch views (remembered per browser); tapping a bar shows its numbers.
if(!window.grunionsCharts){window.grunionsCharts=1;
document.addEventListener('click',function(e){
 var dot=e.target.closest&&e.target.closest('.rg-ccdot');
 if(dot){var card=dot.closest('[data-chartcard]'), key=dot.getAttribute('data-cc'); grunionsChartShow(card,key); try{localStorage.setItem('grunionsChart:'+card.id,key)}catch(err){} return;}
 var col=e.target.closest&&e.target.closest('.rg-cccol');
 if(col){var view=col.closest('.rg-ccview'); view.querySelectorAll('.rg-cccol[aria-pressed]').forEach(function(c){c.removeAttribute('aria-pressed')});
  col.setAttribute('aria-pressed','true'); var tip=view.querySelector('.rg-cctip'); if(tip) tip.textContent=col.getAttribute('data-tip');}
});
window.grunionsChartShow=function(card,key){ if(!card) return; var hit=false;
 card.querySelectorAll('.rg-ccview').forEach(function(v){var on=v.getAttribute('data-cc')===key; v.hidden=!on; hit=hit||on;});
 if(!hit){var first=card.querySelector('.rg-ccview'); if(first){first.hidden=false; key=first.getAttribute('data-cc');}}
 card.querySelectorAll('.rg-ccdot').forEach(function(d){d.setAttribute('aria-selected', d.getAttribute('data-cc')===key?'true':'false')});};
document.addEventListener('DOMContentLoaded',function(){document.querySelectorAll('[data-chartcard]').forEach(function(card){var k=null; try{k=localStorage.getItem('grunionsChart:'+card.id)}catch(err){} if(k) grunionsChartShow(card,k);});});}
// The one history pop in the app: an overlay (sheet/menu) pushed its own entry so Android back closes it;
// closing it in-page pops that entry. Never used for page navigation — back is always a link to the parent.
function grunionsPopOverlay(){ history.back(); }
// Tasks are sheets addressed by ?sheet=<name> so they're linkable.
window.grunionsSavedToast=function(msg){ var t=document.createElement('div'); t.className='toast noprint'; t.setAttribute('role','status'); t.textContent=msg||'Saved'; document.body.appendChild(t); setTimeout(function(){ t.remove(); }, 1800); };
/* Forms marked data-autosave save on change (Figma 62: settings save themselves, no page Save). */
document.addEventListener('change', function(e){
 var f=e.target.closest&&e.target.closest('form[data-autosave]'); if(!f) return;
 var fd=new FormData(f); if(e.target.name&&e.target.type==='checkbox'&&!e.target.checked) fd.set(e.target.name, '0');
 fd.set('field', e.target.name||'');
 fetch(f.getAttribute('action')||location.pathname, {method:'POST', body:fd, credentials:'same-origin', headers:{'X-Autosave':'1'}}).then(function(r){ return r.ok?r.json():Promise.reject(r); }).then(function(j){
  grunionsSavedToast(j&&j.toast||'Saved');
  if(j&&j.set) Object.keys(j.set).forEach(function(k){ document.querySelectorAll('[data-live="'+k+'"]').forEach(function(el){ el.textContent=j.set[k]; }); });
  if(j&&j.dim) Object.keys(j.dim).forEach(function(k){ document.querySelectorAll('[data-dim="'+k+'"]').forEach(function(el){ el.classList.toggle('rg-dim', !!j.dim[k]); }); });
  f.dispatchEvent(new CustomEvent('autosaved', {detail:j}));
 }).catch(function(){ grunionsSavedToast("Couldn't save. Try again."); });
});
window.grunionsSheetFromUrl=function(){ try{ var n=new URLSearchParams(location.search).get('sheet'); if(!n) return; var d=document.querySelector('dialog[data-sheet-name="'+n+'"]'); if(d&&d.showModal&&!d.open){ if(window.grunionsOpenSheet) grunionsOpenSheet(d); else d.showModal(); } }catch(e){} };
if(document.readyState==='loading') document.addEventListener('DOMContentLoaded', function(){ setTimeout(grunionsSheetFromUrl,0); }); else setTimeout(grunionsSheetFromUrl,0);
// Shared: any [data-open-dialog=id] opens that dialog; tapping the backdrop closes it.
if(!window.grunionsDialogs){window.grunionsDialogs=1;
document.addEventListener('click',function(e){var t=e.target.closest&&e.target.closest('[data-open-dialog]');
 if(t){var d=document.getElementById(t.getAttribute('data-open-dialog')); if(d&&d.showModal){e.preventDefault(); if(window.grunionsOpenSheet&&d.classList.contains('botsheet')) grunionsOpenSheet(d); else d.showModal();} return;}
 var sh=e.target.closest&&e.target.closest('[data-share-text]');
 if(sh){e.preventDefault(); var txt=sh.getAttribute('data-share-text'), note=sh.parentNode.querySelector('[data-share-note]');
  // Share trip (04.19): the member's own share sheet or clipboard. The club never sends the text.
  if(navigator.share){navigator.share({text:txt}).catch(function(){}); return;}
  var done=function(){ if(note){note.hidden=false; note.textContent='Copied. Paste it to anyone you like.';} };
  if(navigator.clipboard&&navigator.clipboard.writeText) navigator.clipboard.writeText(txt).then(done, function(){ if(note){note.hidden=false; note.textContent=txt;} });
  else if(note){note.hidden=false; note.textContent=txt;}
  return;}
 if(e.target.tagName==='DIALOG'&&e.target.open&&e.target.classList.contains('modal')) e.target.close();});}
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
  var type=(old.getAttribute('type')||'').toLowerCase();
  if(type && type!=='text/javascript' && type!=='application/javascript' && type!=='module') return;
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
 var dest=lat+','+lng, ua=navigator.userAgent||'';
 var apple=/iPhone|iPad|iPod/.test(ua), android=/Android/i.test(ua);
 var url=apple?('https://maps.apple.com/?daddr='+encodeURIComponent(dest)):(android?('geo:0,0?q='+encodeURIComponent(dest)):('https://www.google.com/maps/dir/?api=1&destination='+encodeURIComponent(dest)));
 if(android) location.href=url; else window.open(url,'_blank','noopener');
};
window.grunionsPlace=function(lat,lng,label){
 var ll=lat+','+lng, name=String(label||'').trim(), ua=navigator.userAgent||'';
 var apple=/iPhone|iPad|iPod/.test(ua), android=/Android/i.test(ua);
 var url=apple?('https://maps.apple.com/?ll='+encodeURIComponent(ll)+'&q='+encodeURIComponent(name||ll)):(android?('geo:'+ll+'?q='+encodeURIComponent(ll+(name?'('+name+')':''))):('https://www.google.com/maps/search/?api=1&query='+encodeURIComponent(ll)));
 if(android) location.href=url; else window.open(url,'_blank','noopener');
};
window.grunionsOfferMaps=function(el){
 if(!el) return;
 var sheet=document.getElementById('mapSheet'), dest=el.getAttribute('data-directions')||'', href=el.getAttribute('data-map-href')||'';
 var label=el.getAttribute('data-map-label')||'Location';
 if(!sheet||!window.grunionsOpenSheet){
  var parts=dest.split(',');
  if(parts.length>=2&&parts[0]&&parts[1]) grunionsDirections(parts[0], parts[1]);
  else if(href) window.open(href,'_blank','noopener');
  return;
 }
 if(sheet.open) return;
 var title=document.getElementById('mapSheetTitle'), go=document.getElementById('mapSheetGo');
 if(title) title.textContent=label;
 if(go){
  if(dest) go.setAttribute('data-directions', dest); else go.removeAttribute('data-directions');
  go.href=href||('https://www.google.com/maps/dir/?api=1&destination='+encodeURIComponent(dest));
 }
 grunionsOpenSheet(sheet);
};
function grunionsDriveConsent(row){
 var id=row.getAttribute('data-drive-user')||'';
 var key='grunionsDrive:'+id, v='';
 try{ v=localStorage.getItem(key)||''; }catch(e){ return ''; }
 if(v) return v;
 try{
  var owner=localStorage.getItem('grunionsDriveUser')||'';
  var global=localStorage.getItem('grunionsDrive')||'';
  if(global && (!owner || owner===String(id))){
   localStorage.setItem('grunionsDriveUser', String(id));
   localStorage.setItem(key, global);
   return global;
  }
 }catch(e){}
 return '';
}
function grunionsDriveRemember(row, value){
 var id=row.getAttribute('data-drive-user')||'';
 try{
  localStorage.setItem('grunionsDrive:'+id, value);
  localStorage.setItem('grunionsDriveUser', String(id));
  localStorage.setItem('grunionsDrive', value);
 }catch(e){}
}
function grunionsDriveAge(row){
 var at=+(row.dataset.driveFetched||0);
 if(at) return Math.floor((Date.now()-at)/1000);
 return +(row.getAttribute('data-drive-age')||0);
}
function grunionsDriveStale(row){ return grunionsDriveAge(row)>=15*60; }
function grunionsNeedLine(){
 var el=document.getElementById('homeMap');
 return !(el && el._you && el._driveRoute && el._driveRoute.length>1);
}
function grunionsDriveOver(row){
 var until=+(row.getAttribute('data-drive-until')||0);
 return !!(until && Date.now()>=until*1000);
}
function grunionsClearCommute(){
 var el=document.getElementById('homeMap'); if(!el) return;
 el._you=null; el._driveRoute=null; el._driveCongestion=null; el._commuteFramed=false;
 if(el._commuteTimer){ clearTimeout(el._commuteTimer); el._commuteTimer=0; }
 if(el._youMarker){ try{ el._youMarker.remove(); }catch(e){} el._youMarker=null; }
 if(el._applyRoute) el._applyRoute();
}
function grunionsLeaveChip(label){
 var chip=document.querySelector('.nextcard .daychip');
 if(!chip) return;
 var live=chip.getAttribute('data-live')||'Upcoming';
 if(label){ chip.textContent=label; return; }
 if(chip.textContent.indexOf('Leave by ')===0) chip.textContent=live;
}
function grunionsDriveEnd(row){
 if(!row || row.dataset.driveEnded==='1') return;
 row.dataset.driveEnded='1';
 row.hidden=true;
 if(row._driveTimer){ clearTimeout(row._driveTimer); row._driveTimer=0; }
 if(row._driveRefresh){ clearTimeout(row._driveRefresh); row._driveRefresh=0; }
 grunionsClearCommute();
 var chip=document.querySelector('.nextcard .daychip');
 if(chip && (chip.textContent.indexOf('Leave by ')===0 || (chip.getAttribute('data-live')||'Upcoming')==='Upcoming')) chip.textContent='In progress';
}
function grunionsDriveArmEnd(row){
 if(row._driveTimer) clearTimeout(row._driveTimer);
 var until=+(row.getAttribute('data-drive-until')||0);
 if(!until) return;
 var wait=until*1000-Date.now();
 if(wait<=0){ grunionsDriveEnd(row); return; }
 row._driveTimer=setTimeout(function(){ if(grunionsDriveOver(row)) grunionsDriveEnd(row); }, Math.min(wait, 2147483647));
}
function grunionsDriveArmRefresh(row){
 if(row._driveRefresh) clearTimeout(row._driveRefresh);
 if(row.dataset.driveEnded==='1' || grunionsDriveOver(row) || grunionsDriveConsent(row)!=='yes') return;
 var line=row.querySelector('[data-drive-line]');
 if(!line || line.hidden || line.dataset.saved!=='1') return;
 var wait=Math.max(1000, (15*60-grunionsDriveAge(row))*1000);
 row._driveRefresh=setTimeout(function(){ if(!document.hidden) grunionsAskDrive(row, true); }, wait);
}
function grunionsDriveDest(row){
 var dest=(row&&row.getAttribute('data-drive-dest')||'').trim();
 return dest.indexOf(',')>0 ? dest : '';
}
function grunionsDriveLink(line, on){
 if(!line) return;
 var row=line.closest&&line.closest('[data-drive]');
 var dest=on?grunionsDriveDest(row):'';
 if(dest){
  line.setAttribute('data-directions', dest);
  line.href='https://www.google.com/maps/dir/?api=1&destination='+encodeURIComponent(dest);
  line.setAttribute('aria-label', 'Driving directions to practice, '+(line.textContent||'').replace(/\\s+/g,' ').trim());
 } else {
  line.removeAttribute('data-directions');
  line.removeAttribute('href');
  line.removeAttribute('aria-label');
 }
}
function grunionsPaintDrive(line, text){
 if(!line) return;
 var mark=' · updated', i=String(text||'').indexOf(mark);
 while(line.firstChild) line.removeChild(line.firstChild);
 if(i<0){ line.appendChild(document.createTextNode(text||'')); }
 else {
  line.appendChild(document.createTextNode(text.slice(0,i)));
  var age=document.createElement('span');
  age.className='driveage';
  age.textContent=text.slice(i);
  line.appendChild(age);
 }
 grunionsDriveLink(line, line.dataset.saved==='1');
}
function grunionsKeepDrive(row, line, btn){
 if(!line || line.dataset.saved!=='1') return false;
 var text=line.textContent;
 if(text.indexOf("couldn't refresh")<0) text+=" · couldn't refresh";
 grunionsPaintDrive(line, text);
 line.hidden=false;
 line.dataset.driveRetry='1';
 if(btn){ btn.hidden=true; btn.disabled=false; }
 row.dataset.driveBusy='';
 return true;
}
function grunionsShowDriveLine(points, here, congestion){
 var el=document.getElementById('homeMap'); if(!el) return;
 var line=[], levels=(congestion||[]).slice();
 if(here && isFinite(+here.lat) && isFinite(+here.lng)){
  line.push([+here.lat, +here.lng]);
  if(levels.length) levels.unshift('unknown');
 }
 (points||[]).forEach(function(p){ if(p && p.length>=2 && isFinite(+p[0]) && isFinite(+p[1])) line.push([+p[0], +p[1]]); });
 el._driveRoute=line.length>1 ? line : null;
 el._driveCongestion=(el._driveRoute && levels.length===el._driveRoute.length-1) ? levels : null;
 if(el._reframe) el._reframe();
 else if(el._applyRoute) el._applyRoute();
}
function grunionsDriveHalt(row){
 if(!row) return;
 row.dataset.driveGen=String((+(row.dataset.driveGen)||0)+1);
 row.dataset.driveBlocked='1';
 row.dataset.driveBusy='';
 row.hidden=true;
 if(row._driveTimer){ clearTimeout(row._driveTimer); row._driveTimer=0; }
 if(row._driveRefresh){ clearTimeout(row._driveRefresh); row._driveRefresh=0; }
 grunionsClearCommute();
 var chip=document.querySelector('.nextcard .daychip');
 if(chip && chip.textContent.indexOf('Leave by ')===0) chip.textContent=chip.getAttribute('data-live')||'Upcoming';
}
window.grunionsDriveSetGoing=function(going){
 var row=document.querySelector('[data-drive]');
 if(!row) return;
 var spec={}; try{ spec=JSON.parse(row.getAttribute('data-drive')||'{}'); }catch(e){}
 if(String(spec.kind||'')!=='practice') return;
 if(grunionsDriveOver(row)){ grunionsDriveEnd(row); return; }
 row.setAttribute('data-drive-going', going);
 if(going==='0'){ grunionsDriveHalt(row); return; }
 row.dataset.driveBlocked='';
 row.hidden=false;
 var line=row.querySelector('[data-drive-line]');
 var saved=!!(line && line.dataset.saved==='1');
 var btn=row.querySelector('[data-drive-ask]');
 if(going==='1' && grunionsDriveConsent(row)==='yes'){ grunionsAskDrive(row, saved); return; }
 if(!saved){
  if(btn){ btn.hidden=false; btn.disabled=false; }
  if(line && line.dataset.saved!=='1') line.hidden=true;
 }
};
function grunionsAskDrive(row, quiet){
 if(!row||row.dataset.driveBusy||row.dataset.driveEnded==='1'||row.dataset.driveBlocked==='1') return;
 if(row.getAttribute('data-drive-going')==='0'){ grunionsDriveHalt(row); return; }
 if(grunionsDriveOver(row)){ grunionsDriveEnd(row); return; }
 var driveGen=row.dataset.driveGen||'0';
 if(!navigator.geolocation){ var missing=row.querySelector('[data-drive-line]'); if(missing && missing.dataset.saved!=='1'){ missing.hidden=false; missing.textContent='Location is not available on this device.'; } return; }
 row.dataset.driveBusy='1';
 var btn=row.querySelector('[data-drive-ask]'), line=row.querySelector('[data-drive-line]');
 if(btn) btn.disabled=true;
 if(line && !quiet && line.dataset.saved!=='1'){ line.hidden=false; line.textContent='Checking traffic…'; }
 navigator.geolocation.getCurrentPosition(function(pos){
  if((row.dataset.driveGen||'0')!==driveGen||row.dataset.driveBlocked==='1'||row.getAttribute('data-drive-going')==='0'){ row.dataset.driveBusy=''; return; }
  if(grunionsDriveOver(row) || row.dataset.driveEnded==='1'){ row.dataset.driveBusy=''; return; }
  grunionsDriveRemember(row, 'yes');
  if(window.grunionsShowYou && document.querySelector('[data-drive]')) grunionsShowYou(pos.coords.latitude, pos.coords.longitude);
  var spec={}; try{ spec=JSON.parse(row.getAttribute('data-drive')||'{}'); }catch(err){}
  fetch('/api/drive',{method:'POST',headers:{'Content-Type':'application/json','X-CSRF':window.PUSH_CSRF||''},body:JSON.stringify({kind:spec.kind,id:spec.id,lat:pos.coords.latitude,lng:pos.coords.longitude})})
   .then(function(r){ return r.json().then(function(j){ return {ok:r.ok,j:j}; }); })
   .then(function(res){
    row.dataset.driveBusy='';
    if((row.dataset.driveGen||'0')!==driveGen||row.dataset.driveBlocked==='1'||row.getAttribute('data-drive-going')==='0') return;
    if(grunionsDriveOver(row)){ grunionsDriveEnd(row); return; }
    if(res.ok && res.j && res.j.show===false){ if(row.getAttribute('data-drive-going')==='0') grunionsDriveHalt(row); else grunionsDriveEnd(row); return; }
    if(!(res.ok && res.j && res.j.text)){ if(!grunionsKeepDrive(row, line, btn)){ if(btn){ btn.disabled=false; btn.hidden=false; } if(line){ line.hidden=false; line.textContent='Could not check drive time.'; } } return; }
    if(btn) btn.hidden=true;
    if(line){ line.hidden=false; line.dataset.saved='1'; line.dataset.driveRetry=res.j.stale?'1':''; grunionsPaintDrive(line, res.j.text); }
    if(!res.j.estimated) grunionsLeaveChip(res.j.chip||'');
    row.dataset.driveFetched=String(Date.now()-((+res.j.stale)?grunionsDriveAge(row)*1000:0));
    if(!res.j.stale) row.setAttribute('data-drive-age','0');
    if(res.j.line && res.j.line.length && !res.j.estimated && !res.j.stale) grunionsShowDriveLine(res.j.line, {lat:pos.coords.latitude,lng:pos.coords.longitude}, res.j.congestion);
    grunionsDriveArmRefresh(row);
   }).catch(function(){ row.dataset.driveBusy=''; if(!grunionsKeepDrive(row, line, btn)){ if(btn){ btn.disabled=false; btn.hidden=false; } if(line){ line.hidden=false; line.textContent='Could not check drive time.'; } } });
 }, function(err){
  row.dataset.driveBusy='';
  if(err&&err.code===1) grunionsDriveRemember(row, 'no');
  if(grunionsKeepDrive(row, line, btn)) return;
  if(btn) btn.disabled=false;
  if(line){ line.hidden=false; line.textContent='Location stays on this device. Allow it to see your drive time.'; }
 }, {enableHighAccuracy:false, maximumAge:900000, timeout:8000});
}
function grunionsDriveRefresh(){
 if(document.hidden) return;
 document.querySelectorAll('[data-drive]').forEach(function(row){
  if(row.getAttribute('data-drive-going')==='0'||row.dataset.driveBlocked==='1'){ grunionsDriveHalt(row); return; }
  if(row.dataset.driveEnded==='1' || grunionsDriveOver(row)){ grunionsDriveEnd(row); return; }
  if(grunionsDriveConsent(row)!=='yes') return;
  var line=row.querySelector('[data-drive-line]');
  if(line && line.dataset.saved==='1' && !line.hidden && !grunionsDriveStale(row) && !grunionsNeedLine()) return;
  grunionsAskDrive(row, !!(line && line.dataset.saved==='1'));
 });
}
window.grunionsDriveScan=function(){
 var rows=document.querySelectorAll('[data-drive]');
 var onHome=location.pathname==='/home'||location.pathname==='/practices'||document.body.classList.contains('homefull');
 if(!rows.length){ if(onHome) grunionsClearCommute(); return; }
 rows.forEach(function(row){
  if(row.getAttribute('data-drive-going')==='0'||row.dataset.driveBlocked==='1'){ grunionsDriveHalt(row); return; }
  if(grunionsDriveOver(row)){ grunionsDriveEnd(row); return; }
  grunionsDriveArmEnd(row);
  var consent=grunionsDriveConsent(row);
  var line=row.querySelector('[data-drive-line]');
  var saved=!!(line && line.dataset.saved==='1' && !line.hidden);
  if(saved && consent==='yes' && row.getAttribute('data-drive-going')==='1') grunionsDriveArmRefresh(row);
  if(row.dataset.driveOn==='1') return;
  row.dataset.driveOn='1';
  if(consent!=='yes') return;
  if(row.getAttribute('data-drive-going')!=='1' && !saved) return;
  grunionsAskDrive(row, saved);
 });
};
if(!window.grunionsDrive){window.grunionsDrive=1;
 document.addEventListener('click', function(e){
  var ask=e.target.closest&&e.target.closest('[data-drive-ask]');
  if(ask){ e.preventDefault(); var row=ask.closest('[data-drive]'); if(row) grunionsAskDrive(row); return; }
  var again=e.target.closest&&e.target.closest('[data-drive-retry]');
  if(again){ e.preventDefault(); var retryRow=again.closest('[data-drive]'); if(retryRow) grunionsAskDrive(retryRow); return; }
  var map=e.target.closest&&e.target.closest('[data-map-open]');
  if(!map||e.target.closest('a,button')) return;
  grunionsOfferMaps(map);
 });
 document.addEventListener('keydown', function(e){
  if(e.key!=='Enter'&&e.key!==' ') return;
  var map=e.target.closest&&e.target.closest('[data-map-open]');
  if(!map||e.target!==map) return;
  e.preventDefault(); grunionsOfferMaps(map);
 });
 document.addEventListener('visibilitychange', function(){ if(!document.hidden) grunionsDriveRefresh(); });
 grunionsDriveScan();
}
if(!window.grunionsDirClick){window.grunionsDirClick=1;
 document.addEventListener('click',function(e){
  var a=e.target.closest&&e.target.closest('[data-directions]'); if(!a) return;
  var parts=(a.getAttribute('data-directions')||'').split(',');
  if(parts.length<2||!parts[0]||!parts[1]) return;
  e.preventDefault();
  grunionsDirections(parts[0], parts[1]);
 });
 document.addEventListener('keydown',function(e){
  if(e.key!==' ') return;
  var a=e.target.closest&&e.target.closest('a[data-directions]');
  if(!a||e.target!==a) return;
  e.preventDefault();
  a.click();
 });
}
function grunionsPinHead(){
 var h=document.querySelector('header.homehead');
 var sticky=h && !document.body.classList.contains('homefull');
 document.documentElement.style.setProperty('--headh', sticky ? (h.offsetHeight+'px') : '0px');
}
window.grunionsPinHead=grunionsPinHead;
function grunionsScrollId(url){try{var u=new URL(url,location.origin);return u.pathname+u.search}catch(e){return ''}}
function grunionsChildBack(from,dest){
 var fp=(from||'').split('?')[0], dp=(dest||'').split('?')[0];
 if(dp==='/manage') return fp==='/admin'||fp==='/members'||fp==='/expiring'||fp==='/transfer'||fp==='/requirements'||fp==='/qr'||fp.indexOf('/manage/')===0;
 if(dp==='/lineup'&&fp.indexOf('/lineup/')===0) return true;
 if((dp==='/practices'||dp==='/home')&&fp.indexOf('/practices/')===0) return true;
 if(dp==='/members'&&fp.indexOf('/admin/member/')===0) return true;
 if(dp==='/admin'&&fp.indexOf('/practices/')===0) return true;
 return false;
}
function grunionsSaveScroll(){
 try{
  var map=JSON.parse(sessionStorage.getItem('grunionsScroll')||'{}')||{};
  map[grunionsScrollId(location.href)]=window.scrollY||0;
  sessionStorage.setItem('grunionsScroll', JSON.stringify(map));
  sessionStorage.setItem('grunionsNavFrom', grunionsScrollId(location.href));
 }catch(e){}
}
function grunionsMarkBack(url){try{sessionStorage.setItem('grunionsBackNav', grunionsScrollId(url))}catch(e){}}
function grunionsTakeBack(url){
 var id=grunionsScrollId(url), flag='';
 try{flag=sessionStorage.getItem('grunionsBackNav')||''; sessionStorage.removeItem('grunionsBackNav')}catch(e){}
 if(!flag||flag!==id) return null;
 try{var map=JSON.parse(sessionStorage.getItem('grunionsScroll')||'{}')||{}; var y=+map[id]; return y>0?y:0}catch(e){return 0}
}
function grunionsIsBackLink(a){var l=a&&(a.getAttribute('aria-label')||'');return !!(a&&(a.classList.contains('profileback')||l==='Back'||l.indexOf('Back to ')===0))}
function grunionsParkHomeMap(){
 var live=document.getElementById('homeMap');
 if(!live||!live._gmap) return;
 var park=document.getElementById('mapPark');
 if(!park){
  park=document.createElement('div');
  park.id='mapPark';
  park.hidden=true;
  park.setAttribute('aria-hidden','true');
  document.body.appendChild(park);
 }
 park.appendChild(live);
}
function grunionsRestoreHomeMap(main){
 var parked=document.querySelector('#mapPark > #homeMap');
 if(!parked||!main) return;
 var slot=main.querySelector('#homeMap');
 if(!slot) return;
 slot.replaceWith(parked);
 if(window.grunionsRefreshMap) grunionsRefreshMap(parked, !(parked._gmap || (window.grunionsMapAlive && grunionsMapAlive(parked))));
}
function grunionsApply(html,url,pop,replace,quiet){
 var keepY=quiet?(window.scrollY||0):null;
 var doc=new DOMParser().parseFromString(html,'text/html');
 var newMain=doc.querySelector('main'), newNav=doc.querySelector('nav.tabs');
 if(!newMain){location.href=url; return;}
 // A deploy changed the CSS/templates: this tab's inline CSS is stale, so load the page in full.
 var nb=doc.querySelector('meta[name=grunions-build]'), cb=document.querySelector('meta[name=grunions-build]');
 if(nb&&cb&&nb.content&&nb.content!==cb.content){location.href=url; return;}
 grunionsClearPage();
 document.querySelectorAll('body>.menu.floating').forEach(function(m){ m.remove(); });
 var scripts=[].slice.call(newMain.querySelectorAll('script'));
 scripts.forEach(function(s){
  var type=(s.getAttribute('type')||'').toLowerCase();
  var js=!type || type==='text/javascript' || type==='application/javascript' || type==='module';
  if(js && s.parentNode) s.parentNode.removeChild(s);
 });
 if(doc.body) document.body.className=doc.body.className;
 var main=document.querySelector('main');
 grunionsParkHomeMap();
 main.replaceChildren.apply(main, [].slice.call(newMain.childNodes));
 grunionsRestoreHomeMap(main);
 var nav=document.querySelector('nav.tabs');
 if(newNav){
  if(nav) grunionsSyncNav(newNav);
  else main.insertAdjacentElement('afterend', document.importNode(newNav, true));
 } else if(nav) nav.remove();
 var newNav3=doc.querySelector('nav.nav3'), curNav3=document.querySelector('nav.nav3');
 if(newNav3&&curNav3) nav3Sync(newNav3);
 else if(!newNav3&&curNav3){ curNav3.remove(); var crestMenu=document.getElementById('crestMenu'); if(crestMenu) crestMenu.remove(); }
 var nextHead=doc.querySelector('header'), curHead=document.querySelector('header');
 if(nextHead&&curHead){
  if(curHead.outerHTML!==nextHead.outerHTML){
   [].slice.call(curHead.attributes).forEach(function(a){ if(!nextHead.hasAttribute(a.name)) curHead.removeAttribute(a.name); });
   [].slice.call(nextHead.attributes).forEach(function(a){ curHead.setAttribute(a.name, a.value); });
   curHead.innerHTML=nextHead.innerHTML;
  }
 } else if(nextHead&&!curHead) document.body.insertBefore(document.importNode(nextHead, true), document.querySelector('main'));
 else if(!nextHead&&curHead) curHead.remove();
 document.title=doc.title||document.title;
 if(!pop){ if(replace) history.replaceState({grunions:1},'',url); else history.pushState({grunions:1},'',url); }
 var backY=grunionsTakeBack(url);
 window.grunionsRestoreY=backY;
 grunionsRunScripts(scripts);
 if(window.grunionsBindPickers) grunionsBindPickers();
 if(window.grunionsDropzones) grunionsDropzones();
 if(window.grunionsPinHead) grunionsPinHead();
 grunionsPushCard();
 if(window.grunionsRefresh) grunionsRefresh();
 var hash=url.split('#')[1]||'';
 if(keepY!==null) scrollTo(0, keepY);
 else if(hash){var el=document.getElementById(hash); if(el) el.scrollIntoView(); else scrollTo(0,0);}
 else if(typeof window.grunionsRestoreY==='number') scrollTo(0, window.grunionsRestoreY);
 else scrollTo(0,0);
 try{sessionStorage.setItem('grunionsNavFrom', grunionsScrollId(url))}catch(e){}
 var seen=/^#p(\\d+)$/.exec(location.hash);
 if(seen&&location.pathname==='/practices') grunionsSeen(seen[1]);
 if(window.grunionsWakeHome) grunionsWakeHome();
}
// Back/forward swipe: Chrome previews the previous entry, then shows this document. If the swap waits on the
// network, the page being left flashes in between. Pages already seen are kept here (HTML only, in memory,
// newest 20) and drawn synchronously on popstate, then refreshed quietly in the background.
var grunionsPages=new Map();
function grunionsPageKey(u){ try{var a=new URL(u,location.href); return a.pathname+a.search;}catch(e){return u;} }
function grunionsCachePage(u,html){ var k=grunionsPageKey(u); grunionsPages.delete(k); grunionsPages.set(k,html); while(grunionsPages.size>20) grunionsPages.delete(grunionsPages.keys().next().value); }
function grunionsBackTo(url){
 var k=grunionsPageKey(url), html=grunionsPages.get(k);
 if(!html){ grunionsGo(url,true); return; }
 var gen=++grunionsNavGen;
 grunionsApply(html,url,true,false);
 fetch(url,{credentials:'same-origin',cache:'no-store',headers:{Accept:'text/html','X-Grunions-Nav':'1'}}).then(function(res){
  if(gen!==grunionsNavGen || (res.headers.get('content-type')||'').indexOf('text/html')===-1) return;
  return res.text().then(function(fresh){
   if(gen!==grunionsNavGen || grunionsPageKey(location.href)!==k) return;
   grunionsCachePage(url, fresh);
   if(fresh!==html) grunionsApply(fresh,location.href,true,false,true);
  });
 }).catch(function(){});
}
function grunionsGo(url,pop,replace){
 var abs; try{abs=new URL(url,location.href);}catch(e){location.href=url; return;}
 if(abs.origin!==location.origin){location.href=abs.href; return;}
 var gen=++grunionsNavGen;
 fetch(abs.href,{credentials:'same-origin',cache:'no-store',headers:{Accept:'text/html','X-Grunions-Nav':'1'}}).then(function(res){
  if(gen!==grunionsNavGen) return;
  var ct=res.headers.get('content-type')||'';
  if(ct.indexOf('text/html')===-1){location.href=abs.href; return;}
  return res.text().then(function(html){
   if(gen!==grunionsNavGen) return;
   var dest=res.url||abs.href; if(abs.hash&&dest.indexOf('#')<0) dest+=abs.hash;
   grunionsCachePage(dest, html); if(dest!==abs.href) grunionsCachePage(abs.href, html);
   grunionsApply(html,dest,pop,replace);
  });
 }).catch(function(){if(gen===grunionsNavGen) location.href=abs.href;});
}
if(document.querySelector('nav.nav3, nav.tabs')){
 try{var adminLast=localStorage.getItem('grunionsAdminTab');var adminLink=document.querySelector('nav.tabs a[href="/admin"], nav.tabs a[href="/members"]');
  if(adminLink&&adminLast&&['/admin','/members','/expiring','/transfer','/requirements','/qr'].indexOf(adminLast)>=0) adminLink.setAttribute('href', adminLast);}catch(e){}
 history.scrollRestoration='manual';
 history.replaceState({grunions:1},'',location.href);
 (function(first){ var go=function(){ fetch(first,{credentials:'same-origin',cache:'no-store',headers:{Accept:'text/html','X-Grunions-Nav':'1'}}).then(function(r){ if((r.headers.get('content-type')||'').indexOf('text/html')>=0) return r.text().then(function(h){ if(!grunionsPages.has(grunionsPageKey(first))) grunionsCachePage(first,h); }); }).catch(function(){}); };
  if(window.requestIdleCallback) requestIdleCallback(go,{timeout:4000}); else setTimeout(go,1500); })(location.href);
 try{sessionStorage.setItem('grunionsNavFrom', grunionsScrollId(location.href))}catch(e){}
 if((function(){try{return sessionStorage.getItem('grunionsBackNav')||''}catch(e){return ''}})()===grunionsScrollId(location.href)){window.grunionsRestoreY=grunionsTakeBack(location.href); if(typeof window.grunionsRestoreY==='number') scrollTo(0, window.grunionsRestoreY)}
 document.addEventListener('click',function(e){
  if(e.defaultPrevented||e.button||e.metaKey||e.ctrlKey||e.shiftKey||e.altKey) return;
  var a=e.target.closest&&e.target.closest('a'); if(!a||!a.href||a.hasAttribute('download')) return;
  if(a.target&&a.target!=='_self') return;
  var abs; try{abs=new URL(a.href,location.href);}catch(err){return;}
  if(abs.origin!==location.origin) return;
  try{ if(abs.pathname!==location.pathname) sessionStorage.setItem('grunionsOpenedFrom', location.pathname+location.search); }catch(err){}
  grunionsSaveScroll();
  if(grunionsIsBackLink(a)) grunionsMarkBack(abs.href);
  else try{sessionStorage.removeItem('grunionsBackNav')}catch(err){}
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
}
function grunionsHomeHeader(){
 if(location.pathname!=='/home') return;
 document.body.classList.remove('schedopen');
 var head=document.querySelector('header.homefade');
 if(!head||(window.scrollY||0)>=8) return;
 head.style.setProperty('--titlefade','0');
 head.classList.remove('titleaway','solid');
 var hi=head.querySelector('.hititle'), sch=head.querySelector('.schedtitle');
 if(hi) hi.setAttribute('aria-hidden','false');
 if(sch) sch.setAttribute('aria-hidden','true');
}
function grunionsWakeHome(force){
 grunionsHomeHeader();
 if(window.grunionsRefreshMap) window.grunionsRefreshMap(document.getElementById('homeMap'), !!force);
}
window.grunionsWakeHome=grunionsWakeHome;
window.addEventListener('pageshow',function(){
 grunionsHomeHeader();
 var el=document.getElementById('homeMap');
 if(!el) return;
 if(window.grunionsMapAlive && grunionsMapAlive(el)) grunionsWakeHome(false);
 else grunionsWakeHome(true);
});
document.addEventListener('visibilitychange',function(){
 if(document.hidden||location.pathname!=='/home') return;
 var el=document.getElementById('homeMap');
 if(el&&window.grunionsMapAlive&&!grunionsMapAlive(el)) grunionsWakeHome(true);
});
window.addEventListener('load',function(){
 var el=document.getElementById('homeMap');
 if(!el||!window.grunionsRefreshMap) return;
 if((window.grunionsMapAlive&&grunionsMapAlive(el))||el._gmap||el.dataset.mapon||el._mapRevealed) grunionsRefreshMap(el, false);
 else grunionsRefreshMap(el, true);
});
window.addEventListener('popstate',function(){
 if(window.grunionsMenuPop){ window.grunionsMenuPop=0; if(window.grunionsCloseMenu) window.grunionsCloseMenu(true); return; }
 if(window.grunionsCloseMenu && window.grunionsCloseMenu(true)) return;
 var from=''; try{from=sessionStorage.getItem('grunionsNavFrom')||''}catch(e){}
 var dest=location.pathname+location.search;
 if(grunionsChildBack(from, dest)) grunionsMarkBack(location.href);
 else try{sessionStorage.removeItem('grunionsBackNav')}catch(e){}
 if(document.querySelector('nav.nav3, nav.tabs')) grunionsBackTo(location.href);
 else if(window.grunionsWakeHome) grunionsWakeHome();
});
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
 document.addEventListener('click',function(e){var d=e.target; if(!d||!d.matches||!d.matches('dialog.modal')||!d.open) return; d.close();});
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
  dateDlg.innerHTML='<div class=sheet><div class=matkicker id=matKicker>Select date</div><div class=matheadline id=matHeadline></div><div class=calhead id=matCalHead><select id=matMonth class=matmonth aria-label="Month and year"></select><button type=button class=calmonth id=matPrev aria-label="Previous month"></button><button type=button class=calmonth id=matNext aria-label="Next month"></button></div><div class=yearrow id=matYearRow hidden><button type=button class=calmonth id=yearPrev aria-label="Previous year"></button><button type=button class=yearbtn id=yearBtn aria-label="Choose year">2027</button><button type=button class=calmonth id=yearNext aria-label="Next year"></button></div><div class=yearlist id=yearList hidden role=listbox aria-label=Years></div><div class=calwd id=matWd><span>S</span><span>M</span><span>T</span><span>W</span><span>T</span><span>F</span><span>S</span></div><div class=calgrid id=matGrid></div><div class=monthgrid id=matMonths hidden></div><div class="actseg matpart" id=matPart role=radiogroup aria-label="Part of the month" hidden><label><input type=radio name=mat_part value=all checked><span>All month</span></label><label><input type=radio name=mat_part value=early><span>Early</span></label><label><input type=radio name=mat_part value=mid><span>Mid</span></label><label><input type=radio name=mat_part value=late><span>Late</span></label></div><div class=callegend><span><i></i>Today</span><span><i class=practicedot></i>Has practice</span></div><div class=matactions><button type=button class=mattext id=matDateCancel>Cancel</button><button type=button class=mattext id=matDateOk>Done</button></div></div>';
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
   var has=window.grunionsPracticeDays&&window.grunionsPracticeDays[iso];
   html+='<button type=button class="calday'+(iso===dateSt.iso?' on':'')+(iso===today?' today':'')+(has?' has':'')+'" data-date="'+iso+'">'+day+(has?'<i class=caldot></i>':'')+'</button>';
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
  timeDlg.innerHTML='<div class=sheet><div class=matkicker>Select time</div><div class=timebig><button type=button id=timeH></button><span>:</span><button type=button id=timeM></button><div class=ampm><button type=button id=timeAM>AM</button><button type=button id=timePM>PM</button></div></div><div class=clock id=timeClock><div class=clockhand id=timeHand></div></div><div class=matactions><button type=button class=mattext id=timeCancel>Cancel</button><button type=button class=mattext id=timeOk>Done</button></div></div>';
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
  if(!dateDlg.open){ dateDlg.showModal(); if(document.activeElement&&dateDlg.contains(document.activeElement)) document.activeElement.blur(); }
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
   if(input.dataset.matarm||input.classList.contains('pickhold')||input.hasAttribute('data-native')) return;
   input.dataset.matarm='1';
   // Open on a real tap only: a scroll that starts on the field must not open the picker.
   var px=null, py=0, pt=0;
   function openIt(){ if(input.type==='time') grunionsOpenTime(input); else grunionsOpenDate(input); }
   input.addEventListener('pointerdown', function(e){ px=e.clientX; py=e.clientY; pt=Date.now(); if(e.pointerType==='mouse'){ e.preventDefault(); } });
   input.addEventListener('pointercancel', function(){ px=null; });
   input.addEventListener('pointerup', function(e){ if(px===null) return; var moved=Math.abs(e.clientX-px)>10||Math.abs(e.clientY-py)>10; px=null; if(moved||Date.now()-pt>700) return; e.preventDefault(); openIt(); });
   input.addEventListener('click', function(e){ e.preventDefault(); });
   input.addEventListener('focus', function(){ if(input.type!=='time' && input.type!=='date' && input.type!=='month') return; });
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
 function nameField(){
  var key=input.getAttribute('data-place-name');
  if(!key||!input.form) return null;
  return input.form.querySelector('[name="'+key+'"]');
 }
 var named=nameField();
 if(named&&!named.dataset.nameWatch){
  named.dataset.nameWatch='1';
  named.addEventListener('input', function(){ named.setAttribute('data-name-edited', named.value.trim()?'1':'0'); });
 }
 function session(){
  if(!input._placeSession) input._placeSession=(window.crypto&&crypto.randomUUID)?crypto.randomUUID():(Date.now().toString(16)+Math.random().toString(16).slice(2));
  return input._placeSession;
 }
 function proximity(){
  var raw=input.getAttribute('data-proximity')||'';
  return /^-?\d+(\.\d+)?,-?\d+(\.\d+)?$/.test(raw)?raw:'';
 }
 function applyChoice(item){
  var place=nameField();
  if(place){
   input.value=item.custom ? item.name : (item.address||item.detail||item.map||item.name);
   if(place.getAttribute('data-name-edited')!=='1') place.value=item.custom ? '' : (item.business||'');
  } else input.value=item.name;
  setBadge(!!item.verified&&!item.custom);
  input.dispatchEvent(new Event('change',{bubbles:true}));
  close();
  input._placeSession='';
 }
 function choose(i){
  var item=items[i]; if(!item) return;
  if(item.id && !item.custom){
   var token=session();
   fetch('/api/places/retrieve?id='+encodeURIComponent(item.id)+'&session='+encodeURIComponent(token)).then(function(r){ return r.json(); }).then(function(row){
    if(row && (row.address||row.name)) applyChoice({name:row.name||item.name, detail:row.detail||item.detail, address:row.address||item.address, business:row.business||item.business, verified:true, custom:false});
    else applyChoice(item);
   }).catch(function(){ applyChoice(item); });
   return;
  }
  applyChoice(item);
 }
 function show(q){
  var mine=++seq;
  var url='/api/places?q='+encodeURIComponent(q)+'&session='+encodeURIComponent(session());
  var sport=document.querySelector('[name=sport]');
  if(sport && sport.value) url+='&sport='+encodeURIComponent(sport.value);
  var near=proximity(); if(near) url+='&proximity='+encodeURIComponent(near);
  fetch(url).then(function(r){ return r.json(); }).then(function(rows){
   if(mine!==seq||input.value.trim()!==q) return;
   items=(rows||[]).map(function(row){ return {name:row.name||'', detail:row.detail||'', address:row.address||row.detail||'', map:row.map||'', business:row.business||'', id:row.id||'', verified:row.verified!==false, custom:false}; }).filter(function(row){ return row.name; });
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
  if(q.length<3){ seq++; items=[]; close(); return; }
  wait=setTimeout(function(){ show(q); }, 300);
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
function grunionsHostChips(){
 var box=document.getElementById('hostChips'), add=document.getElementById('hostAdd'), btn=document.getElementById('hostAddBtn');
 if(!box||!add||box.dataset.bound) return;
 box.dataset.bound='1';
 function drop(chip){ var b=chip.querySelector('button'); if(b) b.onclick=function(){ chip.remove(); }; }
 box.querySelectorAll('.skipchip').forEach(drop);
 function addName(raw){
  var name=String(raw||'').replace(/\s+/g,' ').trim();
  if(!name) return;
  var taken=false;
  box.querySelectorAll('input[name='+'cohost_org]').forEach(function(el){ if(el.value.toLowerCase()===name.toLowerCase()) taken=true; });
  if(taken){ add.value=''; return; }
  var chip=document.createElement('span'); chip.className='skipchip';
  var label=document.createElement('span'); label.textContent=name;
  var b=document.createElement('button'); b.type='button'; b.textContent='×'; b.setAttribute('aria-label','Remove '+name);
  var hidden=document.createElement('input'); hidden.type='hidden'; hidden.name='cohost_org'; hidden.value=name;
  chip.appendChild(label); chip.appendChild(b); chip.appendChild(hidden);
  drop(chip); box.appendChild(chip); add.value='';
 }
 if(btn) btn.addEventListener('click', function(){ addName(add.value); });
 add.addEventListener('keydown', function(e){ if(e.key==='Enter'){ e.preventDefault(); addName(add.value); } });
}
window.grunionsGroups=function(input){
 if(!input||input.dataset.groupbound) return;
 input.dataset.groupbound='1';
 input.setAttribute('autocomplete','off');
 input.setAttribute('role','combobox');
 input.setAttribute('aria-autocomplete','list');
 input.setAttribute('aria-expanded','false');
 var groups=(input.getAttribute('data-groups')||'').split(',').map(function(s){return s.trim()}).filter(Boolean);
 var wrap=document.createElement('div');
 wrap.className='placefield';
 input.parentNode.insertBefore(wrap, input);
 wrap.appendChild(input);
 var drop=document.createElement('div');
 drop.className='placedrop'; drop.hidden=true; drop.setAttribute('role','listbox');
 wrap.appendChild(drop);
 function esc(s){ return String(s||'').replace(/[&<>"']/g, function(c){ return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]; }); }
 function selected(){ return input.value.split(',').map(function(s){return s.trim()}).filter(Boolean); }
 function setSelected(list){
  var seen={}, out=[];
  list.forEach(function(s){ var k=s.toLowerCase(); if(!s||seen[k]) return; seen[k]=1; out.push(s); });
  input.value=out.join(', ');
 }
 function has(name){ var k=name.toLowerCase(); return selected().some(function(s){return s.toLowerCase()===k}); }
 function toggle(name){
  var list=selected(), k=name.toLowerCase(), i=list.findIndex(function(s){return s.toLowerCase()===k});
  if(i>=0) list.splice(i,1); else list.push(name);
  setSelected(list); paint();
 }
 function close(){ drop.hidden=true; input.setAttribute('aria-expanded','false'); }
 function paint(){
  var parts=input.value.split(','), typing=(parts[parts.length-1]||'').trim().toLowerCase();
  if(typing && has(typing)) typing='';
  drop.innerHTML='';
  groups.forEach(function(name){
   if(typing && name.toLowerCase().indexOf(typing)<0 && !has(name)) return;
   var b=document.createElement('button');
   b.type='button'; b.className='placeopt'+(has(name)?' checked':''); b.setAttribute('role','option');
   b.setAttribute('aria-selected', has(name)?'true':'false');
   b.innerHTML='<span class=gcheck></span><span class=grow><span class=plabel>'+esc(name)+'</span></span>';
   b.addEventListener('pointerdown', function(e){ e.preventDefault(); });
   b.addEventListener('click', function(e){ e.preventDefault(); toggle(name); });
   drop.appendChild(b);
  });
  if(typing && !groups.some(function(g){return g.toLowerCase()===typing})){
   var add=document.createElement('button');
   add.type='button'; add.className='placeopt'; add.setAttribute('role','option');
   add.innerHTML='<span class=grow><span class=plabel>'+esc('Add “'+typing+'”')+'</span></span>';
   add.addEventListener('pointerdown', function(e){ e.preventDefault(); });
   add.addEventListener('click', function(e){
    e.preventDefault();
    var list=selected().filter(function(s){return s.toLowerCase()!==typing});
    list.push(typing.replace(/\\s+/g,' ').trim());
    setSelected(list); paint();
   });
   drop.appendChild(add);
  }
  var on=drop.children.length>0;
  drop.hidden=!on; input.setAttribute('aria-expanded', on?'true':'false');
 }
 input.addEventListener('focus', paint);
 input.addEventListener('input', paint);
 input.addEventListener('keydown', function(e){ if(e.key==='Escape'){ e.preventDefault(); close(); } });
 input.addEventListener('blur', function(){ setTimeout(close, 180); });
 paint();
};
document.addEventListener('focusin', function(e){
 var input=e.target; if(!input||!input.matches) return;
 if(input.matches('[data-places]')) grunionsPlaces(input);
 if(input.matches('[data-groups]')) grunionsGroups(input);
});
document.addEventListener('DOMContentLoaded', function(){
 if(window.grunionsDropzones) grunionsDropzones();
 grunionsBindPlaces();
 grunionsHostChips();
});
grunionsHostChips();
grunionsPinHead();
window.addEventListener('resize', grunionsPinHead);
</script>
<script>var PUSH_CSRF="{{csrf_token()}}",VAPID_PUBLIC="{{vapid_public_key()}}";</script>
<dialog class=botsheet id=mapSheet><div class=sheet><div class=grab></div><h2 id=mapSheetTitle>Location</h2><a class="rg-btn primary mapgo" id=mapSheetGo href="https://www.google.com/maps/dir/?api=1&destination=">Open in Maps</a></div></dialog>
</body></html>""")

ADMIN_NAV = """{% for n in admin_notices() %}<div class=note>{{n.body}}</div>{% endfor %}"""

MAP_JS = '''window.grunionsPinHit=function(a,b,gap){gap=gap==null?8:gap;return !!(a&&b&&a.left<b.right+gap&&b.left<a.right+gap&&a.top<b.bottom+gap&&b.top<a.bottom+gap);};
window.grunionsPinGap=function(a,b){if(!a||!b)return Infinity;var gx=0,gy=0;if(a.right<=b.left)gx=b.left-a.right;else if(b.right<=a.left)gx=a.left-b.right;if(a.bottom<=b.top)gy=b.top-a.bottom;else if(b.bottom<=a.top)gy=a.top-b.bottom;if(gx>0&&gy>0)return Math.hypot(gx,gy);if(gx>0)return gx;if(gy>0)return gy;return 0;};
window.grunionsPinStack=function(practice,social,gap){gap=gap==null?2:gap;if(!practice||!social||window.grunionsPinGap(practice,social)>=gap)return {practice:0,social:0};return {practice:0,social:(practice.bottom+gap)-social.top};};
window.grunionsBandTarget=function(top,low){var band=Math.max(80, low-top);return top+band*2/3;};
window.grunionsPinNudge=function(a,b,gap){gap=gap==null?8:gap;if(!window.grunionsPinHit(a,b,gap))return {dx:0,dy:0};var up=(a.top-gap)-b.bottom,down=(a.bottom+gap)-b.top;if(Math.abs(up)<=Math.abs(down))return {dx:0,dy:up};return {dx:0,dy:down};};
window.grunionsPinAbove=function(obstacle,pill,gap){gap=gap==null?8:gap;if(!window.grunionsPinHit(obstacle,pill,gap))return {dx:0,dy:0};return {dx:0,dy:(obstacle.top-gap)-pill.bottom};};
window.grunionsPinClamp=function(rect,bounds,gap){gap=gap==null?8:gap;if(!rect||!bounds)return {dx:0,dy:0};var dx=0;if(rect.right>bounds.right-gap)dx=(bounds.right-gap)-rect.right;if(rect.left+dx<bounds.left+gap)dx=(bounds.left+gap)-rect.left;return {dx:dx,dy:0};};
window.grunionsMountMap=function(el, opts){
 if(!el) return;
 opts=opts||{};
 function boot(){
  el._mapOpts=opts;
  if(!el._glLost){
   el._glLost=1;
   el.addEventListener('webglcontextlost', function(ev){
    ev.preventDefault();
    if(ev.target&&ev.target.dataset) ev.target.dataset.lost='1';
    el._mapDead=true;
    el._mapSpins=(el._mapSpins||0)+1;
    if(el._mapSpins>5) return;
    setTimeout(function(){ if(window.grunionsRefreshMap) grunionsRefreshMap(el, true); }, 30);
   }, true);
  }
  if(window.ResizeObserver&&!el._mapWatch){
   el._mapWatch=1;
   new ResizeObserver(function(){
    if(el.clientWidth<2||el.clientHeight<2) return;
    var live=el._gmap;
    if(!live) return;
    try{ if(live.resize) live.resize(); }catch(e){}
    try{ if(live.invalidateSize) live.invalidateSize(); }catch(e){}
    try{ if(el._reframe) el._reframe(); }catch(e){}
   }).observe(el);
  }
  if(el._gmap && !el._mapDead && window.grunionsMapAlive && grunionsMapAlive(el)){
   try{ if(el._gmap.resize) el._gmap.resize(); }catch(e){}
   try{ if(el._gmap.invalidateSize) el._gmap.invalidateSize(); }catch(e){}
   try{ if(el._reframe) el._reframe(); }catch(e){}
   return;
  }
  if(el._gmap){
   var parent=el.parentNode, next=el.nextSibling;
   try{ el._gmap.remove(); }catch(e){}
   if(parent&&el.isConnected===false) parent.insertBefore(el, next);
   el._gmap=null;
  }
  el._mapDead=false;
  delete el.dataset.mapon;
  delete el.dataset.marked;
  if(!el.isConnected) return;
  var pins=opts.pins||[];
  if(!pins.length) return;
  var mb=window.GRUNIONS_MAPBOX||{};
  function pinText(s){return String(s||'').replace(/[&<>"']/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]});}
  function showPlain(){
   var parent=el.parentNode, next=el.nextSibling, map=el._gmap;
   try{ if(map&&map.remove) map.remove(); }catch(e){}
   if(parent&&el.isConnected===false) parent.insertBefore(el, next);
   el.innerHTML='';
   el.classList.remove('mapboxgl-map','mapready','mapin');
   el.removeAttribute('style');
   el._gmap=null;
   delete el.dataset.mapon;
   delete el.dataset.marked;
   el.style.background='var(--ink)';
  }
  function afterPaint(fn){
   function go(){ requestAnimationFrame(function(){ setTimeout(fn, 0); }); }
   if(document.readyState==='loading') document.addEventListener('DOMContentLoaded', go); else go();
  }
  afterPaint(function(){
   var tries=0;
   function begin(){
    if(!el.isConnected||el._gmap) return;
    if(mb.token&&mb.style) bootMapbox(pins);
    else showPlain();
   }
   function waitSize(){
    if(!el.isConnected) return;
    if((el.clientWidth>1&&el.clientHeight>1)||tries++>90) begin();
    else requestAnimationFrame(waitSize);
   }
   waitSize();
  });
  return;
 function bootMapbox(pins){
  var gaveUp=false;
  function giveUp(){
   if(gaveUp) return;
   gaveUp=true;
   if(!el.isConnected) return;
   showPlain();
  }
  function start(){
   if(gaveUp) return;
   if(!el.isConnected||el.dataset.mapon||!window.mapboxgl) return;
   var map;
   try{
    mapboxgl.accessToken=mb.token;
    var camera={};
    var seed=null;
    pins.forEach(function(p){ if(!seed){ var lng=Number(p.lng), lat=Number(p.lat); if(isFinite(lng)&&isFinite(lat)) seed=[lng, lat]; } });
    var home=opts.mode==='home'||el.id==='homeMap';
    if(seed){ camera.center=seed; camera.zoom=home?12:14; }
    map=new mapboxgl.Map(Object.assign({container:el,style:mb.style,interactive:false,attributionControl:false,logoPosition:'bottom-right',fadeDuration:0,pitch:0,bearing:0,maxPitch:0,pixelRatio:Math.min(window.devicePixelRatio||1,2),scrollZoom:false,boxZoom:false,dragRotate:false,dragPan:false,keyboard:false,doubleClickZoom:false,touchZoomRotate:false,touchPitch:false}, camera));
    staticCredit();
   }catch(err){ giveUp(); return; }
   el.dataset.mapon='1';
   el._gmap=map;
   map.on('movestart', function(ev){ if(ev && ev.originalEvent) el._mapHeld=true; });
   map.on('move', function(){ if(el._pinTick) return; el._pinTick=1; requestAnimationFrame(function(){ el._pinTick=0; try{ separatePins(); }catch(e){} }); });
   var settled=false;
   function tuckAttrib(){
    var card=document.querySelector('.nextcard');
    if((opts.mode!=='home'&&el.id!=='homeMap')||!card) return;
    var box=el.getBoundingClientRect();
    var lift=Math.max(6, Math.round(box.bottom-card.getBoundingClientRect().top+6));
    el.style.setProperty('--map-attrib', lift+'px');
   }
   tuckAttrib();
   setTimeout(tuckAttrib, 0);
   setTimeout(tuckAttrib, 250);
   window.addEventListener('resize', tuckAttrib);
   map.on('error', function(ev){
    if(settled) return;
    var err=ev&&ev.error, status=err&&(err.status||err.statusCode), msg=String((err&&err.message)||'');
    if((status&&status>=400)||/unauthorized|forbidden|invalid token|failed to load style|style not found/i.test(msg)) giveUp();
   });
   var youMarker=null;
   function hideLabels(){
    try{
     var style=map.getStyle(); if(!style||!style.layers) return;
     style.layers.forEach(function(layer){
      if(layer.type==='symbol'){ try{ map.setLayoutProperty(layer.id,'visibility','none'); }catch(e){} }
     });
    }catch(e){}
   }
   function homeView(){ return opts.mode==='home'||el.id==='homeMap'; }
   function cardEdge(){
    var box=el.getBoundingClientRect();
    var card=document.querySelector('.nextcard');
    var cardTop=card?card.getBoundingClientRect().top:(box.top+box.height*0.62);
    var chip=document.querySelector('.nexstack>.drivechip');
    if(chip && !chip.hidden && chip.getClientRects().length){
     var c=chip.getBoundingClientRect();
     if(c.height>1 && c.top<cardTop) cardTop=c.top;
    }
    return {box:box, cardTop:cardTop};
   }
   function headerFloor(){
    var best=0;
    ['.weekhi','header.homehead .titlestack','header.homehead .usawpchip','header.homehead .hititle','header.homehead .headplus','header.homehead a.avatar','header.homehead'].forEach(function(sel){
     var n=document.querySelector(sel); if(!n) return;
     var b=n.getBoundingClientRect().bottom;
     if(b>best) best=b;
    });
    return best||76;
   }
   function chipPad(){
    var above=11, wide=18;
    el.querySelectorAll('.pinpill,.pinrow').forEach(function(n){
     var r=n.getBoundingClientRect();
     if(r.height>above*2) above=Math.ceil(r.height/2);
     if(r.width>wide) wide=Math.ceil(r.width);
    });
    return {above:above+2, left:48, right:Math.max(160, wide-9+24)};
   }
   function lowerLimit(){
    var box=el.getBoundingClientRect();
    var drawer=document.querySelector('.weekdrawer');
    if(drawer){ var d=drawer.getBoundingClientRect(); if(d.height>1) return d.top; }
    var card=document.querySelector('.nextcard');
    var edge=card?card.getBoundingClientRect().top:(box.top+box.height*0.62);
    var chip=document.querySelector('.nexstack>.drivechip');
    if(chip && !chip.hidden && chip.getClientRects().length){
     var c=chip.getBoundingClientRect();
     if(c.height>1 && c.top<edge) edge=c.top;
    }
    return edge;
   }
   function focalPad(count){
    var box=el.getBoundingClientRect(), chip=chipPad();
    var top=Math.round(headerFloor()-box.top+24);
    var low=lowerLimit()-box.top;
    var h=box.height||el.clientHeight||1;
    if((count||1)<=1){
     var target=window.grunionsBandTarget(top, low);
     var bottom=Math.round(top+h-2*target);
     if(bottom<24) bottom=24;
     return {top:top, bottom:bottom, left:24, right:24};
    }
    top=Math.round(top+chip.above);
    var floor=lowerLimit()-16;
    var bottomMulti=Math.round(box.bottom-floor+chip.above);
    if(bottomMulti<24) bottomMulti=24;
    var minInner=80;
    if(top+bottomMulti>h-minInner){
     var room=Math.max(0, h-minInner), sum=top+bottomMulti||1;
     top=Math.round(room*top/sum); bottomMulti=room-top;
    }
    return {top:top, bottom:bottomMulti, left:24, right:24};
   }
   function staticCredit(){
    var logo=el.querySelector('.mapboxgl-ctrl-logo');
    if(!logo||logo.dataset.credit) return;
    logo.dataset.credit='1';
    var pop=document.createElement('div');
    pop.className='mapattrib';
    pop.hidden=true;
    pop.innerHTML='<a href="https://www.mapbox.com/about/maps/" target="_blank" rel="noopener">© Mapbox</a>';
    document.body.appendChild(pop);
    function place(){
     var r=logo.getBoundingClientRect();
     pop.style.left='auto';
     pop.style.top='auto';
     pop.style.right=Math.max(8, Math.round(window.innerWidth-r.right))+'px';
     pop.style.bottom=Math.max(8, Math.round(window.innerHeight-r.top+6))+'px';
    }
    logo.addEventListener('click', function(e){
     e.preventDefault();
     e.stopPropagation();
     var show=pop.hidden;
     document.querySelectorAll('.mapattrib').forEach(function(n){ n.hidden=true; });
     if(!show) return;
     place();
     pop.hidden=false;
    });
    if(!window.grunionsMapAttrib){
     window.grunionsMapAttrib=1;
     document.addEventListener('click', function(e){
      if(e.target.closest&&(e.target.closest('.mapattrib')||e.target.closest('.mapboxgl-ctrl-logo'))) return;
      document.querySelectorAll('.mapattrib').forEach(function(n){ n.hidden=true; });
     });
     window.addEventListener('resize', function(){
      document.querySelectorAll('.mapattrib').forEach(function(n){ n.hidden=true; });
     });
    }
   }
   function pads(){
    var head=document.querySelector('header.homehead'), card=document.querySelector('.nextcard');
    var box=el.getBoundingClientRect();
    if(opts.mode!=='home'&&el.id!=='homeMap') return {top:28,bottom:28,left:36,right:200};
    var headBottom=head?head.getBoundingClientRect().bottom:76;
    var cardTop=card?card.getBoundingClientRect().top:(box.top+box.height*0.58);
    return {top:Math.max(28, headBottom-box.top+20), bottom:Math.max(28, box.bottom-cardTop+16), left:40, right:110};
   }
   function points(){
    var pts=[];
    pins.forEach(function(p){ var ll=lngLat(p); if(ll) pts.push(ll); });
    (opts.route||[]).forEach(function(p){ if(p&&p.length>=2 && isFinite(Number(p[0])) && isFinite(Number(p[1]))) pts.push([Number(p[1]), Number(p[0])]); });
    if(el._you && isFinite(el._you.lng) && isFinite(el._you.lat)) pts.push([el._you.lng, el._you.lat]);
    return pts;
   }
   function lngLat(p){
    if(!p) return null;
    var lng=Number(p.lng), lat=Number(p.lat);
    if(!isFinite(lng)||!isFinite(lat)) return null;
    return [lng, lat];
   }
   function venueLL(){
    var pts=[];
    pins.forEach(function(p){ var ll=lngLat(p); if(ll) pts.push(ll); });
    return pts;
   }
   function activeRoute(){
    if(homeView()) return (el._driveRoute && el._driveRoute.length>1) ? el._driveRoute : [];
    return opts.route||[];
   }
   function commuteLL(){
    var pts=venueLL();
    activeRoute().forEach(function(p){
     if(p&&p.length>=2&&isFinite(+p[0])&&isFinite(+p[1])) pts.push([+p[1], +p[0]]);
    });
    if(el._you && isFinite(el._you.lng) && isFinite(el._you.lat)) pts.push([Number(el._you.lng), Number(el._you.lat)]);
    return pts;
   }
   function focusPoints(){ return commuteLL(); }
   function reduceMotion(){ return !!(window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches); }
   function contentFits(){
    var floor=headerFloor()+24, box=el.getBoundingClientRect(), above=chipPad().above;
    function north(lng, lat, lift){
     var pt; try{ pt=map.project([+lng, +lat]); }catch(e){ return floor; }
     if(!pt||!isFinite(pt.y)) return floor;
     return box.top+pt.y-lift;
    }
    var i, p;
    for(i=0;i<pins.length;i++){
     p=pins[i];
     if(isFinite(+p.lng)&&isFinite(+p.lat)&&north(p.lng, p.lat, above)<floor-1) return false;
    }
    var route=activeRoute();
    for(i=0;i<route.length;i++){
     p=route[i];
     if(p&&p.length>=2&&isFinite(+p[0])&&isFinite(+p[1])&&north(p[1], p[0], 3)<floor-1) return false;
    }
    return true;
   }
   function separatePins(){
    var pinsNow=[].slice.call(el.querySelectorAll('.mpin:not(.you)'));
    var practice=null, social=null;
    pinsNow.forEach(function(pin){ if(pin.classList.contains('social')) social=pin; else if(!practice) practice=pin; });
    function shift(pill, dx, dy){
     var x=(parseFloat(pill.dataset.dx)||0)+dx, y=(parseFloat(pill.dataset.dy)||0)+dy;
     pill.dataset.dx=String(x); pill.dataset.dy=String(y);
     pill.style.transform='translate('+x+'px,'+y+'px)';
    }
    pinsNow.forEach(function(pin){
     var pill=pin.querySelector('.pinpill');
     if(pill){ pill.style.transform=''; pill.dataset.dx='0'; pill.dataset.dy='0'; }
    });
    function stackLabels(){
     if(!practice||!social||!window.grunionsPinStack) return;
     var pp=practice.querySelector('.pinpill'), sp=social.querySelector('.pinpill');
     if(!pp||!sp) return;
     var n=grunionsPinStack(pp.getBoundingClientRect(), sp.getBoundingClientRect(), 2);
     if(n.social) shift(sp, 0, n.social);
     if(n.practice) shift(pp, 0, n.practice);
     var pr=pp.getBoundingClientRect(), sr=sp.getBoundingClientRect();
     if(window.grunionsPinGap(pr, sr)<2){
      var extra=(pr.bottom+2)-sr.top;
      if(extra>0) shift(sp, 0, extra);
     }
    }
    stackLabels();
    var chip=document.querySelector('.nexstack>.drivechip');
    if(chip && !chip.hidden && chip.getClientRects().length && window.grunionsPinAbove){
     var ob=chip.getBoundingClientRect();
     pinsNow.forEach(function(pin){
      var pill=pin.querySelector('.pinpill'); if(!pill) return;
      var n=grunionsPinAbove(ob, pill.getBoundingClientRect(), 8);
      if(n.dx||n.dy) shift(pill, n.dx, n.dy);
     });
    }
    if(window.grunionsPinClamp){
     var bounds=el.getBoundingClientRect();
     pinsNow.forEach(function(pin){
      var pill=pin.querySelector('.pinpill'); if(!pill) return;
      var n=grunionsPinClamp(pill.getBoundingClientRect(), bounds, 8);
      if(n.dx||n.dy) shift(pill, n.dx, n.dy);
     });
    }
    stackLabels();
   }
   el._separatePins=separatePins;
   function groupScreen(){
    var L=Infinity,R=-Infinity,T=Infinity,B=-Infinity, box=el.getBoundingClientRect();
    function take(l,t,r,b){
     if(!isFinite(l)||!isFinite(t)||!isFinite(r)||!isFinite(b)) return;
     if(l<L)L=l; if(r>R)R=r; if(t<T)T=t; if(b>B)B=b;
    }
    el.querySelectorAll('.mpin').forEach(function(n){
     var rec=n.getBoundingClientRect();
     if(rec.width<1&&rec.height<1) return;
     var extra=n.classList.contains('you')?11:0;
     take(rec.left-extra, rec.top-extra, rec.right+extra, rec.bottom+extra);
    });
    function addRoute(route, rad){
     (route||[]).forEach(function(p){
      if(!p||p.length<2||!isFinite(+p[0])||!isFinite(+p[1])) return;
      var pt; try{ pt=map.project([+p[1], +p[0]]); }catch(e){ return; }
      if(!pt||!isFinite(pt.x)||!isFinite(pt.y)) return;
      take(box.left+pt.x-rad, box.top+pt.y-rad, box.left+pt.x+rad, box.top+pt.y+rad);
     });
    }
    if(homeView()) addRoute(el._driveRoute, 3);
    addRoute(opts.route, 2);
    if(!isFinite(L)) return null;
    return {left:L, right:R, top:T, bottom:B};
   }
   function shiftCamera(sx, sy, pad){
    var c=map.project(map.getCenter());
    var next=map.unproject([c.x+sx, c.y+sy]);
    map.jumpTo({center:next, zoom:map.getZoom(), bearing:0, pitch:0, padding:pad});
   }
   function settleHome(pad, bounds, cap){
    var guard=0;
    while(guard<8){
     separatePins();
     var g=groupScreen();
     if(!g) break;
     var box=el.getBoundingClientRect();
     var band={left:box.left+24, right:box.right-24, top:headerFloor()+24, bottom:lowerLimit()-16};
     var roomW=band.right-band.left, roomH=band.bottom-band.top;
     if((g.right-g.left)>roomW+1 || (g.bottom-g.top)>roomH+1){
      cap=Math.max(8, map.getZoom()-0.35);
      map.fitBounds(bounds, {padding:pad, maxZoom:cap, animate:false, bearing:0, pitch:0});
      guard++;
      continue;
     }
     var dx=((g.left+g.right)/2)-((band.left+band.right)/2);
     var leftAfter=g.left-dx;
     if(leftAfter<band.left) dx=g.left-band.left;
     if(g.right-dx>band.right) dx=g.right-band.right;
     var dy=0;
     if(g.top<band.top) dy=g.top-band.top;
     else if(g.bottom>band.bottom) dy=g.bottom-band.bottom;
     if(Math.abs(dx)<1 && Math.abs(dy)<1) break;
     shiftCamera(dx, dy, pad);
     guard++;
    }
    separatePins();
   }
   function frame(animate){
    var pts=(homeView()?(animate?commuteLL():venueLL()):points()).filter(function(p){ return p && isFinite(p[0]) && isFinite(p[1]); });
    if(!pts.length) return;
    var lngs=pts.map(function(p){return p[0];}), lats=pts.map(function(p){return p[1];});
    var pad=homeView()?focalPad(pts.length):pads();
    var pinsOnly=0;
    pins.forEach(function(p){ if(lngLat(p)) pinsOnly++; });
    var multi=pinsOnly>1||(activeRoute().length>1)||!!(homeView()&&el._you);
    var cap=homeView()?(multi?15:12):(pts.length===1?14:15);
    var bounds=[[Math.min.apply(null,lngs), Math.min.apply(null,lats)],[Math.max.apply(null,lngs), Math.max.apply(null,lats)]];
    if(homeView()){
     if(el._mapHeld) return;
     if(animate && !reduceMotion() && map.cameraForBounds && map.easeTo){
      var cam=map.cameraForBounds(bounds, {padding:pad, maxZoom:cap});
      if(cam){
       map.easeTo({center:cam.center, zoom:cam.zoom, padding:pad, bearing:0, pitch:0, duration:800, essential:true});
       map.once('moveend', function(){ settleHome(pad, bounds, cap); });
       return;
      }
     }
     if(map.fitBounds){
      map.fitBounds(bounds, {padding:pad, maxZoom:cap, animate:false, bearing:0, pitch:0});
      settleHome(pad, bounds, cap);
      return;
     }
    }
    function southClear(){
     var low=lowerLimit()-16, high=headerFloor()+8, nodes=el.querySelectorAll('.mpin:not(.you) .pinpill, .mpin:not(.you) .pindot'), i, r;
     for(i=0;i<nodes.length;i++){
      r=nodes[i].getBoundingClientRect();
      if(r.height<1) continue;
      if(r.bottom>low+0.5||r.top<high-0.5) return false;
     }
     return true;
    }
    var guard=0;
    while(guard<8){
     map.fitBounds(bounds, {padding:pad, maxZoom:cap, animate:false});
     if(homeView() && pts.length>1){
      separatePins();
      var southOk=southClear(), northOk=contentFits();
      if(southOk && northOk) break;
      if(!southOk) pad={top:pad.top, bottom:pad.bottom+16, left:pad.left, right:pad.right};
      if(!northOk) cap=Math.max(8, map.getZoom()-0.5);
     } else if(!homeView()||contentFits()||cap<=8) break;
     else cap=Math.max(8, map.getZoom()-0.5);
     guard++;
    }
    requestAnimationFrame(function(){ separatePins(); });
   }
   function viewContains(pts){
    var box=el.getBoundingClientRect(), pad=homeView()?focalPad(pts.length):pads(), i, pt;
    for(i=0;i<pts.length;i++){
     try{ pt=map.project(pts[i]); }catch(e){ return false; }
     if(!pt||!isFinite(pt.x)||!isFinite(pt.y)) return false;
     var x=box.left+pt.x, y=box.top+pt.y;
     if(x<box.left+pad.left||x>box.right-pad.right||y<box.top+pad.top||y>box.bottom-pad.bottom) return false;
    }
    return true;
   }
   function revealOpen(){
    return !el._mapRevealed || (el._revealAt && (Date.now()-el._revealAt)<300);
   }
   function revealMap(){
    if(!homeView() || el._mapRevealed) return;
    el._mapRevealed=true;
    el._revealAt=Date.now();
    el.classList.add('mapready');
    if(reduceMotion() || document.body.classList.contains('schedopen')) return;
    el.classList.add('mapin');
    el.addEventListener('transitionend', function done(ev){
     if(!ev || ev.propertyName!=='opacity') return;
     el.classList.remove('mapin');
     el.removeEventListener('transitionend', done);
    });
   }
   function armReveal(){
    if(!homeView() || el._mapRevealed) return;
    map.once('render', function(){ revealMap(); });
    if(map.triggerRepaint) map.triggerRepaint();
   }
   function scheduleCommuteFrame(){
    if(el._mapHeld || !el._venuesFramed) return;
    if(el._commuteFramed){
     var stuck=commuteLL().filter(function(p){ return p && isFinite(p[0]) && isFinite(p[1]); });
     if(stuck.length && !viewContains(stuck)) frame(true);
     return;
    }
    var wait=revealOpen()?0:280;
    if(el._commuteTimer) clearTimeout(el._commuteTimer);
    el._commuteTimer=setTimeout(function(){
     el._commuteTimer=0;
     if(el._mapHeld || !el._gmap) return;
     el._commuteFramed=true;
     frame(true);
    }, wait);
   }
   function pinEl(kind, label, lat, lng){
    var name=pinText(label), pill=name?'<span class=pinpill>'+name+'</span>':'';
    var node=document.createElement('div');
    node.className='mpin'+(kind==='social'?' social':(kind==='mate'?' mate':''));
    node.dataset.lng=String(lng); node.dataset.lat=String(lat); node.dataset.kind=kind==='social'?'social':(kind==='mate'?'mate':'practice');
    node.innerHTML=kind==='mate'?'<span class=pinmate>'+(name||'')+'</span>':'<span class=pinrow><span class=pinhold><span class=pindot></span></span>'+pill+'</span>';
    node.setAttribute('role','link');
    node.tabIndex=0;
    node.setAttribute('aria-label', (label||'Location')+' in Maps');
    function openPlace(ev){
     if(ev){ ev.preventDefault(); ev.stopPropagation(); }
     if(window.grunionsPlace) grunionsPlace(lat, lng, label);
    }
    node.addEventListener('click', openPlace);
    node.addEventListener('keydown', function(ev){ if(ev.key==='Enter'||ev.key===' ') openPlace(ev); });
    return node;
   }
   function draw(){
    if(settled) return;
    settled=true;
    gaveUp=true;
    el._mapSpins=0;
    tuckAttrib();
    staticCredit();
    hideLabels();
    try{ if(el._applyRoute) el._applyRoute(); }catch(e){}
    try{
     if(!el.dataset.marked){
      el.dataset.marked='1';
      pins.forEach(function(p){
       var ll=lngLat(p); if(!ll) return;
       new mapboxgl.Marker({element:pinEl(p.kind, p.label, p.lat, p.lng), anchor:'top-left', offset:[-9,-9]}).setLngLat(ll).addTo(map);
      });
      if(opts.mode==='card'&&pins[0]) el.addEventListener('click',function(){ grunionsDirections(pins[0].lat, pins[0].lng); });
     }
    }catch(e){}
    try{ frame(false); el._venuesFramed=true; }catch(e){}
    tuckAttrib();
    armReveal();
    if(homeView() && (el._you || (el._driveRoute && el._driveRoute.length>1))) scheduleCommuteFrame();
   }
   function routeCoords(route){
    return (route||[]).map(function(p){ return [Number(p[1]), Number(p[0])]; }).filter(function(p){ return isFinite(p[0]) && isFinite(p[1]); });
   }
   function mapToken(name, fallback){
    var v=(getComputedStyle(document.documentElement).getPropertyValue(name)||'').trim();
    return v || fallback;
   }
   function trafficData(route, levels){
    var coords=routeCoords(route);
    if(coords.length<2) return null;
    var use=(levels && levels.length===coords.length-1) ? levels : null;
    if(!use) return {type:'FeatureCollection', features:[{type:'Feature', properties:{traffic:'unknown'}, geometry:{type:'LineString', coordinates:coords}}]};
    var features=[], start=0, i, k, seg;
    for(i=1;i<=use.length;i++){
     if(i===use.length || use[i]!==use[start]){
      seg=[];
      for(k=start;k<=i;k++) seg.push(coords[k]);
      features.push({type:'Feature', properties:{traffic:use[start]}, geometry:{type:'LineString', coordinates:seg}});
      start=i;
     }
    }
    return {type:'FeatureCollection', features:features};
   }
   function paintLine(id, route){
    var coords=routeCoords(route);
    if(coords.length<2){
     if(map.getLayer(id)) map.removeLayer(id);
     if(map.getSource(id)) map.removeSource(id);
     return;
    }
    var accent=mapToken('--color-lime','var(--lime)');
    var data={type:'Feature',geometry:{type:'LineString',coordinates:coords}};
    if(map.getSource(id)) map.getSource(id).setData(data);
    else {
     map.addSource(id,{type:'geojson',data:data});
     map.addLayer({id:id,type:'line',source:id,paint:{'line-color':accent,'line-width':4,'line-opacity':0.95}});
    }
   }
   function paintTraffic(id, route, levels){
    var data=trafficData(route, levels);
    var keys=['lime','yellow','coral'];
    function drop(lid){
     if(map.getLayer&&map.getLayer(lid)) map.removeLayer(lid);
     if(map.getSource&&map.getSource(lid)) map.removeSource(lid);
    }
    if(!data){ keys.forEach(function(k){ drop(id+'-'+k); }); drop(id); return; }
    var yellow=mapToken('--color-yellow','var(--team-sun)'), coral=mapToken('--color-coral','var(--team-tangerine)'), lime=mapToken('--color-lime','var(--lime)');
    var buckets={lime:[], yellow:[], coral:[]};
    data.features.forEach(function(f){
     var t=f.properties&&f.properties.traffic;
     var key=(t==='heavy'||t==='severe')?'coral':(t==='moderate'?'yellow':'lime');
     buckets[key].push(f);
    });
    var order=[['lime', lime], ['yellow', yellow], ['coral', coral]];
    var empty={type:'FeatureCollection', features:[]};
    order.forEach(function(pair){
     var lid=id+'-'+pair[0], features=buckets[pair[0]], fc={type:'FeatureCollection', features:features};
     if(!features.length){ if(map.getSource(lid)) map.getSource(lid).setData(empty); return; }
     if(map.getSource(lid)) map.getSource(lid).setData(fc);
     else {
      map.addSource(lid,{type:'geojson',data:fc});
      map.addLayer({id:lid,type:'line',source:lid,layout:{'line-cap':'round','line-join':'round'},paint:{'line-color':pair[1],'line-width':6,'line-opacity':1}});
     }
    });
    order.forEach(function(pair){
     var lid=id+'-'+pair[0];
     try{ if(map.getLayer&&map.getLayer(lid)&&map.moveLayer) map.moveLayer(lid); }catch(e){}
    });
   }
   el._applyRoute=function(){
    try{
     if(homeView()){
      paintLine('social-route', opts.route||[]);
      paintTraffic('practice-route', el._driveRoute||[], el._driveCongestion);
     } else paintLine('social-route', opts.route||[]);
    }catch(e){
     if(!el._routeArmed && map.once && /not done loading/i.test(String(e&&e.message||e))){
      el._routeArmed=1;
      map.once('load', function(){ el._routeArmed=0; if(el._applyRoute) el._applyRoute(); });
     }
    }
   };
   map.on('load', draw);
   if(map.loaded()) draw();
   el._reframe=function(){
    if(el._you){
     if(!youMarker){
      var node=document.createElement('div'); node.className='mpin you'; node.innerHTML='<span class=pinhold><span class=youdot></span></span>';
      youMarker=new mapboxgl.Marker({element:node, anchor:'center'}).setLngLat([el._you.lng, el._you.lat]).addTo(map);
     } else youMarker.setLngLat([el._you.lng, el._you.lat]);
     el._youMarker=youMarker;
    } else if(youMarker){
     try{ youMarker.remove(); }catch(e){}
     youMarker=null; el._youMarker=null;
    }
    if(el._applyRoute) el._applyRoute();
    if(!el._venuesFramed){ try{ frame(false); el._venuesFramed=true; }catch(e){} }
    if(homeView() && (el._you || (el._driveRoute && el._driveRoute.length>1))) scheduleCommuteFrame();
    else requestAnimationFrame(function(){ separatePins(); });
   };
  }
  if(window.mapboxgl){ start(); return; }
  if(!document.querySelector('link[data-mapbox]')){
   var css=document.createElement('link'); css.rel='stylesheet'; css.href='https://api.mapbox.com/mapbox-gl-js/v3.6.0/mapbox-gl.css'; css.setAttribute('data-mapbox','1'); document.head.appendChild(css);
  }
  var s=document.querySelector('script[data-mapbox]');
  if(!s){ s=document.createElement('script'); s.async=true; s.src='https://api.mapbox.com/mapbox-gl-js/v3.6.0/mapbox-gl.js'; s.setAttribute('data-mapbox','1'); s.onerror=function(){ giveUp(); }; s.onload=start; document.head.appendChild(s); }
  else if(window.mapboxgl) start();
  else { s.addEventListener('load', start); s.addEventListener('error', function(){ giveUp(); }); }
 }
}
boot();
};
window.grunionsPlaceMap=function(){
 var el=document.getElementById('homeMap');
 if(el&&el._reframe) el._reframe();
};
window.grunionsShowYou=function(lat,lng){
 if(!document.querySelector('[data-drive]')) return;
 var el=document.getElementById('homeMap'); if(!el) return;
 el._you={lat:lat,lng:lng};
 if(el._reframe) el._reframe();
};
window.grunionsMapAlive=function(el){
 if(!el||!el.isConnected||el._mapDead||!el._gmap) return false;
 if(el.clientWidth<2||el.clientHeight<2) return false;
 var canvas=el.querySelector('canvas');
 if(!canvas||canvas.dataset.lost==='1') return false;
 return canvas.width>1&&canvas.height>1;
};
window.grunionsRefreshMap=function(el, force){
 if(!el) return;
 if((window.scrollY||0)<8) el.style.opacity='';
 if(!force && el._mapOpts && window.grunionsMapAlive && !grunionsMapAlive(el)) force=true;
 if(force && el._gmap){
  var parent=el.parentNode, next=el.nextSibling;
  try{ el._gmap.remove(); }catch(e){}
  if(parent && el.isConnected===false) parent.insertBefore(el, next);
  el._gmap=null;
  delete el.dataset.mapon;
  delete el.dataset.marked;
  el.innerHTML='';
  el.className='homemap';
 }
 var map=el._gmap;
 if(map && !force){
  try{ if(map.resize) map.resize(); }catch(e){}
  try{ if(map.invalidateSize) map.invalidateSize(); }catch(e){}
  try{ if(map.triggerRepaint) map.triggerRepaint(); }catch(e){}
  try{ if(el._reframe) el._reframe(); }catch(e){}
  requestAnimationFrame(function(){
   try{ if(el._gmap&&el._gmap.resize) el._gmap.resize(); }catch(e){}
   try{ if(el._gmap&&el._gmap.invalidateSize) el._gmap.invalidateSize(); }catch(e){}
   try{ if(el._reframe) el._reframe(); }catch(e){}
  });
  return;
 }
 if(el._mapOpts && window.grunionsMountMap){
  delete el.dataset.mapon;
  window.grunionsMountMap(el, el._mapOpts);
 }
};
'''

def map_script(mapbox_json):
    return "<script>\nwindow.GRUNIONS_MAPBOX=" + mapbox_json + ";\n" + MAP_JS + "</script>\n"

APPEARANCE_PAGE = """
<div class=fxpage>
<a class=fxback href=/profile>‹ Profile</a>
<h1 class=ty-display-m>Appearance</h1>
<p class=ty-muted>System follows your phone or computer. Team colors stay the same in both.</p>
<form method=post>{{ csrf_field() }}
{{ rg_seg_choice('appearance', [('system','System'),('light','Light'),('dark','Dark')], ui_theme or 'dark', True) }}
<noscript><button class="rg-btn primary">Save</button></noscript>
</form>
</div>
"""

T = {}
T["join"] = """<h1>Join the Grunions</h1>
<p class=ty-body>Tuesdays at Marina High School and Fridays at Westminster High School, 7–8:30 PM. Membership is $45/mo starting in November; a current USA Water Polo membership is required.</p>
<form method=post>{{csrf_field()}}
<label>Legal first name<input name=first required autocomplete=given-name></label>
<label>Preferred first name (optional)<input name=preferred_first autocomplete=off placeholder="Leave blank to use your legal first name"></label>
<label>Legal last name<input name=last required autocomplete=family-name></label>
<label>Email<input name=email type=email required autocomplete=email placeholder="The one on your USA Water Polo account"></label>
<label>Phone<input name=phone type=tel required autocomplete=tel></label>
<label>Date of birth <span class=r2-chip>18+ only</span><input name=birth_date type=date required autocomplete=bday></label>
<p class="ty-muted ty-sm sm">Grunions is an adults club. If you're under 18 you can't join. We'll point you to youth programs nearby.</p>
<button class="rg-btn primary full">Create account</button></form>
<p class="ty-muted ty-sm sm" style="text-align:center;margin-top:20px">Already a member? <a href=/login>Log in</a></p>"""

T["login"] = """<img class=loginlock src="/static/regulars-lockup.svg" alt="Regulars" width="1338" height="261">
<h1>Log in</h1>
{% if google_enabled() %}<a class="rg-btn secondary full" href=/auth/google style="background:var(--surface2);color:var(--t1);border:1px solid var(--line)"><svg width=18 height=18 viewBox="0 0 48 48" aria-hidden=true><path fill="#EA4335" d="M24 9.5c3.5 0 6.6 1.2 9.1 3.6l6.8-6.8C35.8 2.4 30.3 0 24 0 14.6 0 6.6 5.4 2.7 13.3l7.9 6.1C12.5 13.6 17.8 9.5 24 9.5z"/><path fill="#4285F4" d="M46.1 24.5c0-1.6-.1-3.1-.4-4.5H24v9h12.4c-.5 2.9-2.2 5.3-4.6 6.9l7.4 5.7c4.3-4 6.9-9.9 6.9-17.1z"/><path fill="#FBBC05" d="M10.6 28.6c-.5-1.4-.8-3-.8-4.6s.3-3.2.8-4.6l-7.9-6.1C1 16.6 0 20.2 0 24s1 7.4 2.7 10.7l7.9-6.1z"/><path fill="#34A853" d="M24 48c6.5 0 11.9-2.1 15.9-5.8l-7.4-5.7c-2.1 1.4-4.8 2.3-8.5 2.3-6.2 0-11.5-4.1-13.4-9.9l-7.9 6.1C6.6 42.6 14.6 48 24 48z"/></svg>Sign in with Google</a>
<p class="ty-muted ty-sm sm" style="text-align:center;margin:16px 0 4px">or</p>{% endif %}<p class=ty-body>We'll email you a one-time login link.</p>
<form method=post>{{csrf_field()}}<label>Email<input name=email type=email required autocomplete=email></label>
<button class="rg-btn primary full">Send login link</button></form>
<p class="ty-muted ty-sm sm" style="text-align:center;margin-top:20px">New here? <a href=/join>Join the team</a></p>"""

T["home"] = """{% if (tab=='home' or sched_home) and pins %}
<section class=homemap id=homeMap aria-label="Practice map"></section>
{{ map_boot() }}
<script>
(function(){
 var pins={{ pins|tojson }};
 var route={{ route|tojson if route else '[]' }};
 function start(){ var el=document.getElementById('homeMap'); if(el&&window.grunionsMountMap) grunionsMountMap(el,{pins:pins,mode:'home',route:route}); }
 if(window.grunionsMountMap) start(); else document.addEventListener('DOMContentLoaded', start);
 if(window.grunionsDriveScan) grunionsDriveScan();
})();
</script>
{% endif %}
{% if tab != 'practices' and not sched_home %}<div class=homealerts>{{ push_card() }}
{% for n in notices %}<div class="note notice">{{n.body}}</div>{% endfor %}
{% if ann %}<div class=card><div class="ty-muted ty-sm xs">ANNOUNCEMENT · {{display_first(ann)|upper}}</div><p style="margin:6px 0 0">{{ann.body}}</p></div>{% endif %}</div>{% endif %}
{% macro schedule_feed(when, rows, note) %}
{{ rg_seg([('upcoming','Upcoming','/practices?view=list&when=upcoming'),('past','Past','/practices?view=list&when=past'),('all','All','/practices?view=list&when=all')], when) }}
{% if note %}<div class=anncard><b>ANNOUNCEMENT · {{ display_first(note)|upper }}</b><p>{{ note.body }}</p></div>{% endif %}
{% set ns = namespace(day='', open=false, featured=true) %}
{% for x in rows %}{% set p = x.p %}{% set tile = practice_tile(p) %}{% set key = tile.wd ~ tile.dn %}
{% if key != ns.day %}{% if ns.open %}</div></div>{% endif %}{% set ns.day = key %}{% set ns.open = true %}
<div class=daygroup><div class=dayrail><span>{{ tile.wd }}</span><b>{{ tile.dn }}</b></div><div class=daycards>
{% endif %}
{% set ended = practice_ended(p) or when == 'past' %}
{% if not ended and not p.cancelled %}{% for card in x.before or [] %}{{ r2_social_card(card, 'home' if card.joined else 'condensed') }}{% endfor %}{% endif %}
{% if p.cancelled %}
{{ r2_event_row('/practices/' ~ p.id, 'cancelled', tile.wd ~ ' · ' ~ month_abbr(p.date) ~ ' ' ~ tile.dn ~ ' · ' ~ (p.sport or 'Water Polo')|upper, practice_title(p), p.cancel_reason, 0) }}
{% elif ns.featured and when != 'past' %}{% set ns.featured = false %}{% set clk = fmt_clock(p.start).split(' ') %}
{{ r2_event_card('/practices/' ~ p.id, (p.sport or 'Water Polo')|upper, practice_title(p), clk[0], clk[1], practice_duration(p.start, p.end), short_place(p.location), x.going, '', x.mine == 1, '', ended) }}
{% else %}
{{ r2_event_row('/practices/' ~ p.id, 'stack', weekday_name(p.date), practice_title(p), fmt_clock(p.start) ~ ' · ' ~ short_place(p.location), x.going|length, (p.sport or 'Water Polo')|upper, ended) }}
{% endif %}
{% if not ended and not p.cancelled %}{% for card in x.after or [] %}{{ r2_social_card(card, 'home' if card.joined else 'condensed') }}{% endfor %}{% endif %}
{% endfor %}{% if ns.open %}</div></div>{% endif %}
{% if not rows %}<p class="ty-muted ty-sm">Nothing coming up.</p>{% endif %}
{% endmacro %}
{% if sched_home %}
{% set _setup = setup_card() %}{% set _start = preview_drawer or ('full' if (not_cleared or (_setup and _setup.show) or (tab == 'home' and not (me().usawp_number or '')|trim)) else 'half') %}
<div class=weekhi><span class=weekeye>{% if not_cleared %}NOT CLEARED{% elif me().usawp_number %}USAWP #{{ me().usawp_number }}{% endif %}</span>{% if can_host_practice() %}<span class=weekplus>{{ rg_plus('/events/new', 'Create', 'createSheet') }}</span>{% endif %}<div class=titlecross><h1 class=hititle>Hi, {{ display_first(me()) }}.</h1><h1 class=schedtitle aria-hidden=true>{% if _start == 'full' %}Hi, {{ display_first(me()) }}.{% else %}Upcoming{% endif %}</h1></div>{{ r2_legend('') }}</div>
{% if pin_label %}<b class=mappinchip>{{ pin_label }}</b>{% endif %}
<div class=mapcontrols><button type=button data-zoom=1 aria-label="Zoom in">+</button><button type=button data-zoom=-1 aria-label="Zoom out">−</button></div>
{% if not pins %}{{ r2_map_unavailable() }}{% endif %}
<div class="weekdrawer {{ 'peek' if _start == 'peek' else ('full' if _start == 'full' else 'half') }}" id=schedSheet data-start="{{ _start }}">
<button type=button class=sheetgrab id=sheetGrab aria-label="Drag the week"></button>
{% if not_cleared %}<div class=clearbanner><b>NOT CLEARED YET</b><strong>Add your USAWP number to go to practice.</strong><p>Takes 2 minutes. Coaches can see you once it’s verified.</p><a href=/profile#membership>Add USAWP number</a></div>{% endif %}
<div class=weekbody id=weekBody>
<div class=weekhead><h2>This week{% if week_n %} <span>({{ '%02d'|format(week_n) }})</span>{% endif %}</h2><a href="/practices?view=list">See all ›</a></div>
<div class=weekthis>
{% if tab == 'home' %}<div class=homealerts>{{ push_card() }}{% for n in notices %}<div class="note notice">{{n.body}}</div>{% endfor %}</div>
{% if not (me().usawp_number or '')|trim %}{{ rg_usawp_card(csrf_field(), not trial_window(me()), TRIAL_JOIN_URL) }}{% endif %}{% endif %}
{% if show_drive %}{{ r2_drive_card(drive_num or '18', drive_note or drive_detail, drive_chip, drive_placeholder, drive_kicker or 'YOUR DRIVE · 7.4 MI', ('/practices/' ~ nextp.id ~ '/leave-by') if nextp else '') }}{% endif %}
{% if show_rides %}<div class=ridebtns><button type=button id=needRide>{{ ride_label }}</button><button type=button id=offerRide>Offer a ride</button></div>{% endif %}
{% if ann %}<div class=anncard><b>ANNOUNCEMENT · {{ display_first(ann)|upper }}</b><p>{{ ann.body }}</p></div>{% endif %}
{% if not week_sessions %}<div class=weekempty><span>THIS WEEK</span><b>Nothing scheduled this week.</b><p>Your team hasn’t posted anything yet. Check Lineup for events or look at the full schedule.</p><a href=/lineup>See Lineup</a></div>{% endif %}
{% set wk = namespace(day='', open=false) %}{% for s in week_sessions %}{% set tile = practice_tile(s.p) %}{% set key = tile.wd ~ tile.dn %}
{% if key != wk.day %}{% if wk.open %}</div></div>{% endif %}{% set wk.day = key %}{% set wk.open = true %}<div class=daygroup><div class=dayrail><span>{{ tile.wd }}</span><b>{{ tile.dn }}</b></div><div class=daycards>{% endif %}
{% for card in s.before %}{{ r2_social_card(card, 'home' if card.joined else 'condensed') }}{% endfor %}
{% if s.cancelled %}{{ r2_event_row('/practices/' ~ s.p.id, 'cancelled', (s.p.sport or 'Water Polo')|upper, practice_title(s.p), s.p.cancel_reason or 'Cancelled', s.going|length) }}
{% else %}{% set clk = fmt_clock(s.p.start).split(' ') %}{{ r2_event_card('/practices/' ~ s.p.id, (s.p.sport or 'Water Polo')|upper, practice_title(s.p), clk[0], clk[1] if clk|length > 1 else '', practice_duration(s.p.start, s.p.end), short_place(s.p.location), s.going, '' if s.mine == 1 and not home_out else day_chip(s.p.date), s.mine == 1 and not home_out, event_tone(s.kind or 'practice'), practice_ended(s.p)) }}{% endif %}
{% for card in s.after %}{{ r2_social_card(card, 'home' if card.joined else 'condensed') }}{% endfor %}
{% endfor %}{% if wk.open %}</div></div>{% endif %}
<a class=fullsched href="/practices?view=list">View full schedule ›</a>

</div>
</div>
</div>
{% if ride_pid %}<dialog id=rideAsk class="botsheet modal"><form method=post action="/practices/{{ ride_pid }}/rides" class=sheet>{{ csrf_field() }}<input type=hidden name=next value=home>
<div class=grab aria-hidden=true></div>
<h2>Ask for a ride.</h2>
<label class=rg-field><span>PICKUP AREA</span><input name=area required maxlength=60 placeholder="Neighborhood or city" value="{{ ride_area }}"></label>
<p class=ty-muted>Drivers going today see this area, never your address.</p>
<label class=checkline><input type=checkbox name=back value=1 checked> Ride back too{% if nextp %} · practice ends {{ fmt_clock(nextp.end) }}{% endif %}</label>
<button class="rg-btn primary" name=action value=ask id=rideAskGo>Ask drivers</button>
<a class=rg-calink href="/practices/{{ ride_pid }}/rides">See the ride board</a>
</form></dialog>
<dialog id=rideOffer class="botsheet modal"><form method=post action="/practices/{{ ride_pid }}/rides" class=sheet>{{ csrf_field() }}<input type=hidden name=next value=home>
<div class=grab aria-hidden=true></div>
<h2>Offer a ride.</h2>
<label class=rg-field><span>LEAVING FROM (AREA)</span><input name=area required maxlength=60 placeholder="Neighborhood or city" value="{{ ride_area }}"></label>
<label class=rg-field><span>SEATS</span><select name=seats>{% for n in range(1,7) %}<option{% if n == ride_seats %} selected{% endif %}>{{ n }}</option>{% endfor %}</select></label>
<label class=checkline><input type=checkbox name=back value=1 checked> I can drive people back</label>
<button class="rg-btn primary" name=action value=offer>Offer seats</button>
<a class=rg-calink href=/rides/settings>Ride settings</a>
</form></dialog>{% endif %}
<script>
(function(){
 var sheet=document.getElementById('schedSheet'); if(!sheet) return;
 if(window.grunionsSchedAbort) window.grunionsSchedAbort.abort();
 var ac=new AbortController(); window.grunionsSchedAbort=ac;
 function live(){ return document.body.classList.contains('schedhome') && document.getElementById('schedSheet')===sheet; }
 var scroller=document.getElementById('weekBody');
 var h=0, anim=0, drag=null, wheelT=0, wheelFull=false, wasFull=false;
 function wide(){ return window.innerWidth>=768; }
 function metrics(){
  var vh=window.innerHeight||document.documentElement.clientHeight||1;
  // 04.01: the default (half) height is the floor. The sheet only grows upward; it never drops to a peek that hides the cards.
  var half=Math.round(vh*0.52);
  return {peek:half, half:half, full:vh, vh:vh};
 }
 function apply(next){
  var m=metrics();
  if(next<m.peek) next=m.peek;
  if(next>m.full) next=m.full;
  h=next;
  var atFull=h>=m.full-1;
  sheet.classList.toggle('full', atFull);
  sheet.classList.remove('peek');
  sheet.classList.toggle('half', !atFull && Math.abs(h-m.half)<1.5);
  document.body.style.setProperty('--drawer-h', Math.round(h)+'px');
  var morph=(h-m.half)/((m.full-m.half)||1);
  if(morph<0) morph=0; if(morph>1) morph=1;
  var hi=document.querySelector('.weekhi');
  if(hi){
   hi.style.setProperty('--titlefade', Math.min(1, morph*2.5).toFixed(3));  // same curve as the map: done when the map is gone
   // The map is gone in the first ~40% of the pull; padding and corners follow the whole pull, so nothing snaps.
   var mf=Math.min(1, morph*2.5);
   document.body.style.setProperty('--mapfade', mf.toFixed(3));
   document.body.style.setProperty('--mapdone', mf>=0.999?'1':'0');
   document.body.style.setProperty('--sheetp', morph.toFixed(3));
   var big=hi.querySelector('.hititle'), small=hi.querySelector('.schedtitle');
   if(big) big.setAttribute('aria-hidden', morph*2.5>=0.5?'true':'false');
   if(small) small.setAttribute('aria-hidden', morph*2.5>=0.5?'false':'true');
   var wp=hi.querySelector('.weekplus'); if(wp) wp.classList.toggle('on', morph*2.5>=0.5);
  }
  document.body.classList.toggle('mapcovered', !wide() && (m.vh-h)<120);
  if(scroller && !atFull && scroller.scrollTop) scroller.scrollTop=0;
  else if(scroller && atFull!==wasFull) scroller.scrollTop=0;
  wasFull=atFull;
 }
 function pinList(){
  if(!scroller || sheet.classList.contains('full')) return;
  scroller.scrollTop=0;
 }
 function animateTo(target){
  if(anim) cancelAnimationFrame(anim);
  var reduced=window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var from=h, t0=performance.now(), dur=reduced?0:280;
  function frame(now){
   var p=dur?Math.min(1,(now-t0)/dur):1, e=1-Math.pow(1-p,3);
   apply(from+(target-from)*e);
   if(p<1) anim=requestAnimationFrame(frame);
   else { anim=0; requestAnimationFrame(pinList); }
  }
  anim=requestAnimationFrame(frame);
 }
 function settle(vy, fromFull){
  var m=metrics(), midUp=(m.half+m.full)/2, midDown=(m.peek+m.half)/2, target=m.half;
  if(fromFull && h<m.full-8) target=m.half;
  else if(vy<-0.6 && h>midDown) target=m.full;
  else if(vy>0.6 && h<midDown) target=m.peek;
  else if(h>=midUp) target=m.full;
  else if(h<=midDown) target=m.peek;
  animateTo(target);
 }
 function resetWide(){
  if(anim) cancelAnimationFrame(anim);
  anim=0; drag=null; wasFull=false;
  sheet.classList.remove('peek','full'); sheet.classList.add('half');
  document.body.style.removeProperty('--drawer-h');
  document.body.classList.remove('mapcovered','sheetdrag');
  var hi=document.querySelector('.weekhi'); if(hi) hi.style.setProperty('--titlefade','0');
  ['--mapfade','--mapdone','--sheetp'].forEach(function(k){ document.body.style.removeProperty(k); });
 }
 function blocked(el){
  if(!el||!el.closest) return true;
  if(el.closest('nav,dialog,.mapcontrols')) return true;
  if(el.closest('#sheetGrab')) return false;
  if(el.closest('button,input,textarea,select')) return true;
  return false;
 }
 document.addEventListener('pointerdown', function(e){
  if(!live()||wide()||e.button||e.pointerType==='touch'||blocked(e.target)) return;
  if(anim){ cancelAnimationFrame(anim); anim=0; }
  var inSheet=!!e.target.closest('#schedSheet'), full=sheet.classList.contains('full');
  if(full && inSheet && !e.target.closest('#sheetGrab') && scroller && scroller.scrollTop>2) return;
  drag={y:e.clientY,h:h,id:e.pointerId,moved:false,fromFull:full,pull:full&&inSheet&&!e.target.closest('#sheetGrab'),lastY:e.clientY,lastT:performance.now(),vy:0};
 }, {signal:ac.signal});
 document.addEventListener('pointermove', function(e){
  if(!drag||e.pointerId!==drag.id) return;
  if(!live()){ drag=null; return; }
  var dy=e.clientY-drag.y, now=performance.now();
  drag.vy=(e.clientY-drag.lastY)/((now-drag.lastT)||16);
  drag.lastY=e.clientY; drag.lastT=now;
  if(!drag.moved){
   if(Math.abs(dy)<8) return;
   if(drag.pull && dy<0){ drag=null; return; }
   drag.moved=true; document.body.classList.add('sheetdrag');
  }
  apply(drag.h-dy);
  if(e.cancelable) e.preventDefault();
 }, {passive:false, signal:ac.signal});
 function endDrag(e){
  if(!drag||(e&&e.pointerId!==drag.id)) return;
  var moved=drag.moved, vy=drag.vy||0, fromFull=!!drag.fromFull;
  drag=null; document.body.classList.remove('sheetdrag');
  if(!moved) return;
  var stop=function(ev){ ev.preventDefault(); ev.stopPropagation(); document.removeEventListener('click', stop, true); };
  document.addEventListener('click', stop, true);
  setTimeout(function(){ document.removeEventListener('click', stop, true); }, 400);
  settle(vy, fromFull);
 }
 var touch=null;
 document.addEventListener('touchstart', function(e){
  if(!live()||wide()||e.touches.length!==1) return;
  var t=e.target;
  if(t.closest&&(t.closest('nav,dialog,.mapcontrols')||(t.closest('button,input,textarea,select')&&!t.closest('#sheetGrab')))) return;
  if(anim){ cancelAnimationFrame(anim); anim=0; }
  touch={y:e.touches[0].clientY,t:performance.now(),vy:0,moved:false,fromFull:sheet.classList.contains('full')};
 }, {passive:true, signal:ac.signal});
 document.addEventListener('touchmove', function(e){
  if(!touch||!live()||wide()) return;
  var y=e.touches[0].clientY, now=performance.now(), dy=y-touch.y;
  touch.vy=dy/((now-touch.t)||16); touch.y=y; touch.t=now;
  if(!touch.moved && Math.abs(dy)<8) return;
  var full=sheet.classList.contains('full');
  var more=scroller && scroller.scrollTop+scroller.clientHeight<scroller.scrollHeight-1;
  var above=scroller && scroller.scrollTop>0;
  if(e.cancelable) e.preventDefault();
  touch.moved=true;
  // The sheet and the list are one surface: we drive both, so the same swipe grows the sheet and then
  // keeps scrolling the cards up under the header like a normal page (no native hand-off that can stall).
  if(full && scroller && dy<0){ if(more){ scroller.scrollTop-=dy; touch.scrolled=true; } return; }
  if(full && scroller && dy>0 && (above || touch.scrolled)){ scroller.scrollTop-=dy; touch.scrolled=true; return; }
  apply(h-dy);
 }, {passive:false, signal:ac.signal});
 function glide(v){
  // Momentum after a hand-driven scroll (px per ms), easing out.
  if(!scroller) return;
  var last=performance.now();
  (function step(now){
   var dt=now-last; last=now; v*=Math.pow(0.996, dt);
   if(Math.abs(v)<0.02 || !sheet.classList.contains('full')) return;
   var before=scroller.scrollTop; scroller.scrollTop-=v*dt;
   if(scroller.scrollTop===before) return;
   requestAnimationFrame(step);
  })(last);
 }
 document.addEventListener('touchend', function(){
  if(!touch) return;
  var moved=touch.moved, vy=touch.vy||0, fromFull=touch.fromFull, scrolled=touch.scrolled;
  touch=null;
  if(!moved) return;
  if(sheet.classList.contains('full') && (scrolled || vy<0)){ glide(vy); return; }
  settle(vy, fromFull);
 }, {signal:ac.signal});
 document.addEventListener('pointerup', endDrag, {signal:ac.signal});
 document.addEventListener('pointercancel', endDrag, {signal:ac.signal});
 document.addEventListener('wheel', function(e){
  if(!live()||wide()||(e.target.closest&&e.target.closest('dialog'))) return;
  var full=sheet.classList.contains('full');
  var atTop=!scroller || scroller.scrollTop<=2;
  if(full && scroller && e.deltaY>0){
   scroller.scrollTop+=e.deltaY;
   if(e.cancelable) e.preventDefault();
   return;
  }
  if(full && scroller && e.deltaY<0 && !atTop){
   scroller.scrollTop+=e.deltaY;
   if(e.cancelable) e.preventDefault();
   return;
  }
  if(e.cancelable) e.preventDefault();
  if(anim){ cancelAnimationFrame(anim); anim=0; }
  if(!wheelT) wheelFull=full;
  apply(h+e.deltaY);
  clearTimeout(wheelT);
  wheelT=setTimeout(function(){ var started=wheelFull; wheelT=0; settle(0, started); }, 160);
 }, {passive:false, signal:ac.signal});
 window.addEventListener('resize', function(){ if(!live()) return; if(wide()) resetWide(); else apply(sheet.classList.contains('full')?metrics().full:(h||metrics().half)); }, {signal:ac.signal});
 // Setup still open (Finish setup, USAWP # or not cleared): the week opens pinned to the top and covers the map.
 // Once those are done it opens at half height and the map shows. (Direction, Nov 13.)
 var start=sheet.getAttribute('data-start');
 if(wide()) resetWide(); else apply(start==='full'?metrics().full:(start==='peek'?metrics().peek:metrics().half));
 var ask=document.getElementById('rideAsk'), offer=document.getElementById('rideOffer');
 var need=document.getElementById('needRide'); if(need) need.onclick=function(){ if(window.grunionsOpenSheet) grunionsOpenSheet(ask); else ask.showModal(); };
 var off=document.getElementById('offerRide'); if(off) off.onclick=function(){ if(window.grunionsOpenSheet) grunionsOpenSheet(offer); else offer.showModal(); };


 var map=document.getElementById('homeMap');
 document.querySelectorAll('.mapcontrols button').forEach(function(b){
  b.onclick=function(){ var g=map&&map._gmap; if(g&&g.zoomIn){ if(b.getAttribute('data-zoom')==='1') g.zoomIn(); else g.zoomOut(); } };
 });
})();
</script>
{% elif tab == 'practices' %}
<div class=schedfeed id=schedule>{{ schedule_feed(sched_when, sched_rows, ann) }}</div>
{% else %}
<div class=homedock>
{% set cl = clearance(m) %}{% set dl = days_left(m.usawp_valid_until) %}{% set tw = trial_window(m) %}{% set num = (m.usawp_number or '')|trim %}
{% set ns = namespace(tone='ok') %}
{% if vr_pending or (tw and tw.active and (m.usawp_status or '') != 'verified') %}{% set ns.tone = 'warn' %}
{% elif not cl.ok %}{% set ns.tone = 'bad' %}
{% elif dl is not none and dl <= EXPIRING_DAYS %}{% set ns.tone = 'warn' %}
{% else %}{% for it in cl.checks %}{% if it.days_left is not none and it.days_left >= 0 and it.days_left <= EXPIRING_DAYS %}{% set ns.tone = 'warn' %}{% endif %}{% endfor %}{% endif %}
{% if tab != 'practices' and not num %}<div class="card numcard"><div class=nxtitle>Enter your USAWP membership number</div>
<form method=post action=/home style="margin-top:12px">{{csrf_field()}}
<label>USAWP Membership #<input name=usawp_number inputmode=numeric value="" autocomplete=off></label>
<button class="rg-btn primary full">Save</button>
{% if not tw %}<button type=button class="rg-btn secondary full" id=trialOpen style="margin-top:8px">2-week USAWP trial</button>{% endif %}</form>
{% if not tw %}<dialog id=trialDialog class=modal><div class=sheet>
<p>I will complete the USA Water Polo 2-week trial membership before I get in the pool. I understand I need to get a full USAWP membership soon, otherwise I will not be able to practice.</p>
<form method=post action=/home>{{csrf_field()}}<input type=hidden name=action value=trial>
<button class="rg-btn primary full">I confirm</button></form>
<a class="rg-btn secondary full" style="margin-top:10px" href="{{TRIAL_JOIN_URL}}" target=_blank rel=noopener>Get USAWP trial membership</a>
</div></dialog>
<script>document.getElementById('trialOpen').onclick=function(){document.getElementById('trialDialog').showModal()};
document.getElementById('trialDialog').addEventListener('click',function(e){if(e.target===this)this.close()});</script>{% endif %}
</div>{% endif %}
{% if next_kind == 'event' and nextev %}<div class="card tap nextcard{% if nextev.status == 'canceled' %} cancelled{% endif %}" onclick="if(event.target.closest('button,a,form,input,select,textarea,label'))return;location.href='/lineup/{{ nextev.id }}'">
<div class=nxbody><a class=cardlink href="/lineup/{{ nextev.id }}">
<div class=nxcardhead><div class="nxtitle cardtitle">{{ nextev.title }}</div><span class="chip-info daychip">{{ nextev.chip_label }}</span></div>
<div class=nxmain><div class=datetile>{% if nextev.tile.wd %}<span class=wd>{{ nextev.tile.wd }}</span>{% endif %}<span class=dn>{{ nextev.tile.dn }}</span><span class=mo>{{ nextev.tile.mo }}</span></div>
<div class="grow schedrows"><div class=nxrow>{{ glyph_clock() }}<span>{{ nextev.when }}</span></div>
{% if nextev.where %}<div class=nxrow>{{ glyph_pin() }}<span>{{ nextev.where }}</span></div>{% endif %}
<div class=nxrow>{{ glyph_people() }}<span>{{ nextev.count_line }} · {{ nextev.host_line }}</span></div></div></div></a></div>
<form method=post action=/lineup class=pills>{{ csrf_field() }}<input type=hidden name=event_id value={{ nextev.id }}><input type=hidden name=back value=/home>{{ rsvp_base('e' ~ nextev.id) }}
{{ rsvp_btn('Going', nextev.mine == 'going', 'going') }}
{{ rsvp_btn('Not going', nextev.mine == 'notgoing', 'notgoing') }}</form>
</div>{% elif nextp %}{% set sh = social_home(nextp) %}<div class=nexstack>{% if drive_on %}<div class="drivechip" data-drive="{{ {'kind':'practice','id':nextp.id}|tojson|forceescape }}" data-drive-until="{{ drive_until }}" data-drive-user="{{ m.id }}" data-drive-age="{{ drive_age }}" data-drive-dest="{{ nextp.lat }},{{ nextp.lng }}" data-drive-going="{{ drive_going }}"><button type=button class=drivechipbtn data-drive-ask{% if drive_saved %} hidden{% endif %}>Show my drive time</button><a class=drivechiptext data-drive-line{% if drive_saved %} data-saved=1 data-directions="{{ nextp.lat }},{{ nextp.lng }}" href="https://www.google.com/maps/dir/?api=1&destination={{ (nextp.lat|string ~ ',' ~ nextp.lng|string)|urlencode }}" target=_blank rel=noopener aria-label="Driving directions to practice, {{ drive_saved }}"{% else %} hidden{% endif %}>{% if drive_saved %}{{ drive_saved.split(' · updated', 1)[0] }}{% if ' · updated' in drive_saved %}<span class=driveage> · updated{{ drive_saved.split(' · updated', 1)[1] }}</span>{% endif %}{% endif %}</a></div>{% endif %}<div class="card tap nextcard{% if nextp.cancelled %} cancelled{% endif %}" onclick="if(event.target.closest('button,a,form,input,select,textarea,label,.drivechip,.nxmap'))return;location.href='/practices/{{nextp.id}}'">
{% if social_after and sh %}<div class="nxnote afterline">After practice: {{ sh.place }}{% if social_mins %} · {{ social_mins }} min drive{% endif %}</div>{% endif %}
{% if nextp.image %}<a class=cardlink href="/practices/{{nextp.id}}"><div class=pimg><img src="/practice-image/{{ nextp.id }}?v={{ nextp.image }}" alt=""><span class="chip-info nxbadge">{% if nextp.date == today %}TODAY{% else %}{{ fmt_d(nextp.date) }}{% endif %}</span></div></a>{% endif %}
<div class=nxbody><a class=cardlink href="/practices/{{nextp.id}}">
<div class=nxcardhead><div class="nxtitle cardtitle">{{ practice_title(nextp) }}</div><span class="chip-info daychip" data-live="{{ practice_live_chip(nextp) }}">{% if drive_chip %}{{ drive_chip }}{% else %}{{ practice_live_chip(nextp) }}{% endif %}</span></div>
{% set tile = practice_tile(nextp) %}
<div class=nxmain><div class=datetile><span class=wd>{{ tile.wd }}</span><span class=dn>{{ tile.dn }}</span><span class=mo>{{ tile.mo }}</span></div>
<div class="grow schedrows"><div class=nxrow>{{ glyph_clock() }}<span>{% if practice_is_month(nextp) %}{{ practice_when(nextp) }}{% else %}{{ fmt_span(nextp.start, nextp.end) }}{% endif %}</span></div>
<div class=nxrow>{{ glyph_pin() }}<span>{{ nextp.location }}</span></div>
<div class=nxrow>{{ glyph_people() }}<span>{{ practice_going_line(nextp_n, nextp) }}</span></div></div></div>
{% if nextp.coach_note %}<div class=nxnote>{{ nextp.coach_note }} · {{ nextp.coach_note_by }} · {{ fmt_stamp(nextp.coach_note_at) }}</div>{% endif %}</a></div>
<form method=post action=/practices class=pills>{{csrf_field()}}<input type=hidden name=pid value={{nextp.id}}>{{ rsvp_base('p' ~ nextp.id) }}
{{ rsvp_btn('Going', nextp_mine==1, 'going') }}
{{ rsvp_btn('Not going', nextp_mine==0, 'notgoing') }}</form>
{% if sh %}<div class=nxdiv></div><div class=nxsocial><a class=cardlink href="/practices/{{nextp.id}}" style="display:flex;align-items:center;gap:12px">{{ social_icon() }}
<div class=grow><div class=nxtitle>{{ sh.title }}</div><div class="ty-body sm">{{ sh.place }}</div></div></a>
<form method=post action=/practices>{{csrf_field()}}<input type=hidden name=pid value={{nextp.id}}>{{ rsvp_base('ps' ~ nextp.id) }}
<button class="btn {{ 'btn-primary' if next_joined else 'btn-secondary' }}"{% if not next_joined %} data-sweep{% endif %} name=action value="{{ 'social_leave' if next_joined else 'social_join' }}">{% if next_joined %}<svg class=rsvpcheck width="16" height="16" viewBox="0 0 256 256" fill="currentColor" aria-hidden="true"><path d="M229.66,77.66l-128,128a8,8,0,0,1-11.32,0l-56-56a8,8,0,0,1,11.32-11.32L96,188.69,218.34,66.34a8,8,0,0,1,11.32,11.32Z"/></svg>{% endif %}{{ 'Joined' if next_joined else 'Join' }}</button></form></div>{% endif %}
</div></div>{% endif %}
</div>
{% if sport_filter_names() %}<div class="rolechips chiprow" id=sportFilters role=group aria-label="Sport">{% for name in [""] + sport_filter_names() %}<button type=button {% if not name %}class=on aria-current=true{% endif %} data-sport="{{ name }}">{{ name or 'All' }}</button>{% endfor %}</div>{% endif %}
<div class=schedlist id=schedule>
{% for x in data %}{% set p = x.p %}{% set tile = practice_tile(p) %}<div class="schedrow{% if nextp and p.id == nextp.id %} schedsame{% endif %}"><div class=dayrail><span>{{ tile.wd }}</span><b>{{ tile.dn }}</b></div><div class="card tap{% if nextp and p.id == nextp.id %} schedsame{% endif %}{% if p.cancelled %} cancelled{% endif %}" id=p{{p.id}} data-pid={{p.id}} data-sport="{{ p.sport or 'Water Polo' }}" onclick="if(event.target.closest('button,a,form,input,select,textarea,label,dialog'))return;location.href='/practices/{{p.id}}'">
<a class=cardlink href="/practices/{{p.id}}">
<div class=nxcardhead><div class="nxtitle cardtitle">{{ practice_title(p) }}</div><span class="chip-info sportstat">{{ p.sport or 'Water Polo' }} · {{ sport_card_status(p, x.mine) }}</span></div>
{% set tile = practice_tile(p) %}
<div class=nxmain><div class=datetile><span class=pdate>{% if x.unseen %}<span class=badge data-seen={{p.id}}>{{ x.unseen if x.unseen < 100 else '99+' }}</span>{% endif %}</span><span class=wd>{{ tile.wd }}</span><span class=dn>{{ tile.dn }}</span><span class=mo>{{ tile.mo }}</span></div>
<div class="grow schedrows"><div class=nxrow>{{ glyph_clock() }}<span>{% if practice_is_month(p) %}{{ practice_when(p) }}{% else %}{{ fmt_span(p.start, p.end) }}{% endif %}</span></div>
<div class=nxrow>{{ glyph_pin() }}<span>{{ p.location }}</span></div>
<div class=nxrow>{{ glyph_people() }}<span>{{ practice_going_line(x.going|length, p) }}</span></div></div></div>
{% if p.cancelled %}{{ st('bad','Cancelled') }}{% if p.cancel_reason %}<div class="ty-muted ty-sm sm">{{ p.cancel_reason }}</div>{% endif %}{% endif %}
{% if p.note %}<div class=nxnote>{{p.note}}</div>{% endif %}
{% if p.coach_note %}<div class=nxnote>{{ p.coach_note }} · {{ p.coach_note_by }} · {{ fmt_stamp(p.coach_note_at) }}</div>{% endif %}</a>
{% if not p.cancelled %}<form method=post action=/practices class=pills>{{csrf_field()}}<input type=hidden name=pid value={{p.id}}>{{ rsvp_base('p' ~ p.id) }}
{{ rsvp_btn('Going', x.mine == 1, 'going') }}
{{ rsvp_btn('Not going', x.mine == 0, 'notgoing') }}</form>
{% endif %}</div></div>{% endfor %}
</div>
{% endif %}
<script>
(function(){
 var bar=document.getElementById("sportFilters"); if(!bar) return;
 bar.addEventListener("click", function(ev){
  var btn=ev.target.closest("button"); if(!btn) return;
  [].slice.call(bar.querySelectorAll("button")).forEach(function(other){ other.classList.toggle("on", other===btn); });
  var sport=btn.getAttribute("data-sport");
  [].slice.call(document.querySelectorAll("#schedule .card")).forEach(function(card){
   var label=card.getAttribute("data-sport")||"";
   card.hidden=!!sport && label!==sport;
  });
 });
})();
</script>
<script>
(function(){
 var head=document.querySelector('header.homefade'); if(!head||head.dataset.bound) return; head.dataset.bound='1';
 var map=document.getElementById('homeMap');
 var reduced=window.matchMedia('(prefers-reduced-motion: reduce)').matches, ticking=false;
 function measure(){
  var card=document.querySelector('#schedule .card:not(.schedsame)');
  var dock=document.querySelector('.homedock');
  if(head.getAttribute('data-entry')==='schedule'){ if(dock) dock.style.minHeight='0'; return; }
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
  var held=typeof window.grunionsRestoreY==='number' && window.grunionsRestoreY>0;
  if(!held && head.getAttribute('data-entry')==='schedule' && location.pathname!=='/practices' && (!hash || hash==='#schedule')) window.scrollTo(0, range());
  if(location.pathname==='/home') document.body.classList.remove('schedopen');
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
<div class=profilehero>
<div class=avatarwrap>
<button type=button class="avatar hero" id=avatarBtn aria-label="Profile photo">{% if m.photo %}<img id=avatarImg src="/avatar/{{ m.id }}?v={{ m.photo }}" alt="" width="112" height="112">{% else %}<img id=avatarImg alt="" width="112" height="112" hidden>{% endif %}<span id=avatarLetters {% if m.photo %}hidden{% endif %}>{{ initials(m) }}</span></button>
<button type=button class=cambadge id=camBadge aria-label="Choose photo">""" + _CAM + """</button>
</div>
<dialog class="botsheet attachsheet" id=photoDlg><div class=sheet>
<div class=grab aria-hidden=true></div>
<div class=attachphone id=photoPhone>
<div class=attachhead><h2>Add an image</h2><p class=attachsub>Up to 10 · JPG, PNG, HEIC</p></div>
<div class=attachtiles>
<button type=button class=attachtile id=photoTake><span class=attachico><img src="/static/nav/attach-camera.svg" width="24" height="24" alt=""></span>Take photo</button>
<button type=button class=attachtile id=photoChoose><span class=attachico><img src="/static/nav/attach-image.svg" width="24" height="24" alt=""></span>Choose photos</button>
</div>
<button type=button class=attachcancel id=photoPickCancel>Cancel</button>
</div>
<div class=attachwide id=photoWide>
<div class=attachwidehead><h2>Add an image</h2><button type=button class=attachx id=photoWideX aria-label="Close">✕</button></div>
<div class=attachdrop id=photoWideDrop>
<div class=idle><span class=attachico><img src="/static/nav/attach-upload.svg" width="24" height="24" alt=""></span><b>Drop an image here</b><button type=button class=attachbrowse id=photoComputer><svg width="24" height="24" viewBox="0 0 24 24" fill="none" aria-hidden="true"><rect x="3" y="4" width="18" height="16" rx="3" stroke="currentColor" stroke-width="2"/><circle cx="8" cy="9" r="2" fill="currentColor"/><path d="M3 19L10 12L14 16L17 13L21 17" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>Choose from computer</button></div>
<div class=hot><span class=attachico><img src="/static/nav/attach-upload.svg" width="24" height="24" alt=""></span><b>Drop to add</b><p class=attachcount id=photoDropCount>1 image</p></div>
</div>
<p class=attachnote>Up to 10 · JPG, PNG, HEIC, GIF · 20 MB each. You can also paste (⌘V) or drag straight into the chat.</p>
</div>
<p class=attacherr id=photoErr hidden></p>
<input class="pick fileclip" type=file name=photo id=photoFile accept="image/*,image/heic,image/heif,image/heic-sequence,image/heif-sequence,.heic,.heif">
<div id=photoDrop hidden>
<div class=dropzone id=photoZone>
<button type=button class=dropempty id=photoPick><span class=droplink>Drop a photo here</span><span class=drophint>or Select photo</span></button>
</div>
</div>
<button type=button class="rg-btn danger full" id=photoRemove {% if not m.photo %}hidden{% endif %}>Remove photo</button>
<div id=photoCrop hidden>
<div class=cropstage id=cropStage><img id=cropImg alt=""></div>
<label class=croprange>Zoom<input type=range id=cropZoom min=1 max=4 step=0.01 value=1></label>
<div class=row><button type=button class="rg-btn secondary" id=cropCancel>Cancel</button><button type=button class="rg-btn primary" id=cropUse>Use photo</button></div>
<button type=button class="rg-btn ghost full" id=cropOther>Choose a different photo</button>
</div>
</div></dialog>
<div id=photoDragCard class=dropcard hidden><div class="attachdrop over"><span class=attachico><img src="/static/nav/attach-upload.svg" width="24" height="24" alt=""></span><b>Drop to add</b><p class=attachcount id=photoDragCount>1 image</p></div></div>
<div class=profilename>{{ display_first(m) }} {{ m.last }}</div>
<div class=profilerow><span class=rolechip>{{ role_label(m)|capitalize }}</span><p class=profilesub>{{ hist|length }} practice{{ '' if hist|length == 1 else 's' }} attended{% if nmonth %} · {{ nmonth }} this month{% endif %}</p></div>
<div class=metrics><div class="metric sun"><b>{{ '%02d'|format(hist|length) }}</b><span>Attended</span></div><div class="metric sky"><b>{{ '%02d'|format(nmonth or 0) }}</b><span>This month</span></div></div>

</div>
</form>
{% if ptab == 'general' %}
{% if not (m.usawp_number or '')|trim %}
<div class="card numcard"><div class=nxtitle>Enter your USAWP membership number</div>
<form method=post action=/home style="margin-top:12px">{{ csrf_field() }}
<label>USAWP Membership #<input name=usawp_number inputmode=numeric value="" autocomplete=off></label>
<button class="rg-btn primary full">Save</button></form>
<p class='ty-muted ty-sm'><a href=/notifications>Notification settings</a></p>
</div>{% endif %}
{% set mine_clear = clearance(m) %}{{ rg_label('Cleared sports') }}
{{ rg_row('Water polo', 'Grunions' ~ (' · Admin' if (m.is_admin or m.board_member) else (' · Coach' if m.role == 'coach' else '')), '', '', '', '', 'Cleared' if mine_clear.ok else 'Pending', 'going' if mine_clear.ok else 'expiring') }}
{{ membership_section(m, vr_pending) }}
<div class=rg-day>Personal</div>
<div class="list infogrid">
<div class="li prow"><span class=k>Legal name</span><span class=v>{{ m.first }} {{ m.last }}</span></div>
<div class=viewonly>{{ rg_row('Preferred name', m.preferred_first or '—', chevron=False) }}</div>
<div class="li prow editonly"><label class=prefedit style="width:100%;margin:0">Preferred name<input form=profileForm name=preferred_first id=prefName value="{{ m.preferred_first or '' }}" data-original="{{ m.preferred_first or '' }}" placeholder="Leave blank to use your legal first name" autocomplete=off></label></div>
<div class="li prow"><span class=k>Email</span><span class=v>{{ m.email }}</span></div>
<div class="li prow viewonly"><span class=k>Phone</span><span class=v>{{ fmt_phone(m.phone) }}</span></div>
<div class="li prow editonly"><label class=prefedit style="width:100%;margin:0">Phone<input form=profileForm name=phone id=phoneInput type=tel inputmode=numeric autocomplete=tel value="{{ '' if fmt_phone(m.phone) == '—' else fmt_phone(m.phone) }}" data-original="{{ '' if fmt_phone(m.phone) == '—' else fmt_phone(m.phone) }}"></label></div>
</div>
{{ rg_label('Account') }}
<div class=rg-srows>{{ rg_settings_row('Settings', '', '/settings') }}</div>
{% else %}
{% if prof_upcoming or prof_past %}
{% for g in prof_upcoming %}<div class=rg-day>{{ g.label }}</div>{% for e in g.events %}{{ lineup_card(e, prof_back) }}{% endfor %}{% endfor %}
{% if prof_past %}<details class=lineuppast><summary>Past <span class=pastn>{{ prof_past_n }}</span></summary>{% for g in prof_past %}<div class=rg-day>{{ g.label }}</div>{% for e in g.events %}{{ lineup_card(e, prof_back) }}{% endfor %}{% endfor %}</details>{% endif %}
{% else %}<p class=emptyfind>Nothing yet.</p>{% endif %}
{% endif %}
<dialog id=selfMenu class="botsheet profmenu"><div class=sheet><div class=grab aria-hidden=true></div>
<div class=menuwho><span class="mark sun">{{ initials(m) }}</span><span class=grow><b>{{ display_first(m) }} {{ m.last }}</b><small>Your profile</small></span></div>
<div class=newcard>
<button type=button class=newrow data-menu=photo><span class=grow><b>Change photo</b><small>Take a photo or choose one</small></span><span class=chatgo>›</span></button>
<button type=button class=newrow data-menu=edit><span class=grow><b>Edit profile</b><small>Name, email, phone</small></span><span class=chatgo>›</span></button>
<a class=newrow href=/privacy><span class=grow><b>Privacy</b><small>Who sees your email and phone</small></span><span class=chatgo>›</span></a>
</div>
<div class=newcard>
<button type=button class="newrow actdanger" data-menu=delete><span class=grow><b>Delete account</b><small>Leaves every club. Can't be undone.</small></span></button>
</div>
<p class='ty-muted ty-sm'>Delete account lives here and in Settings › Account. It's yours alone — admins can only remove you from their club.</p>
</div></dialog>
<dialog id=editSheet class="botsheet profmenu"><div class=sheet><div class=grab aria-hidden=true></div>
<form method=post action=/profile>{{ csrf_field() }}<input type=hidden name=action value=identity>
<h2 class=newtitle>Edit profile</h2>
<label>Legal name<input name=first value="{{ m.first }}" required autocomplete=off></label>
<label>Last name<input name=last value="{{ m.last }}" required autocomplete=off></label>
<label>Preferred name<input name=preferred_first value="{{ m.preferred_first or '' }}" autocomplete=off></label>
<label>Pronouns<input name=pronouns value="{{ m.pronouns or '' }}" placeholder="she/her" autocomplete=off></label>
<label>Sex on your sport membership<select name=legal_gender><option value="">Not set</option>{% for k, v in LEGAL_GENDERS %}<option value="{{ k }}"{% if m.legal_gender == k %} selected{% endif %}>{{ v }}</option>{% endfor %}</select></label>
<label>Gender identity<select name=gender_identity id=genderId><option value="">Not set</option>{% for k, v in GENDER_IDENTITIES %}<option value="{{ k }}"{% if m.gender_identity == k %} selected{% endif %}>{{ v }}</option>{% endfor %}</select></label>
<label id=genderSelfRow{% if m.gender_identity != 'self' %} hidden{% endif %}>In your words<input name=gender_self maxlength=40 value="{{ m.gender_self or '' }}" autocomplete=off></label>
<p class='ty-muted ty-sm'>Sex on your sport membership is whatever your governing body (like USA Water Polo) has on file. Only admins see it, for insurance rosters. Gender identity is how you identify. It's never shown on your profile and is only used for women &amp; non-binary rides if you turn them on.</p>
<label>Email<input name=email type=email value="{{ m.email }}" required autocomplete=email></label>
<label>Phone<input name=phone type=tel inputmode=numeric value="{{ '' if fmt_phone(m.phone) == '—' else fmt_phone(m.phone) }}" required autocomplete=tel></label>
<p class='ty-muted ty-sm'>Your legal name is only shown to club admins. Changing your email changes how you sign in.</p>
<button class="rg-btn primary full">Save</button>
</form></div></dialog>
<dialog id=deleteSheet class="botsheet profmenu"><div class=sheet><div class=grab aria-hidden=true></div>
<form method=post action=/profile/delete>{{ csrf_field() }}
<h2 class=newtitle>Delete your account?</h2>
<p class='ty-muted ty-sm'>This can't be undone.</p>
<p><b>You'll leave</b><br>Grunions and every other club.</p>
<p><b>Deleted</b><br>Profile, photo, compliance records, direct chats.</p>
<p><b>Stays</b><br>Team chat messages show as “Former member”.</p>
<label>Type DELETE to confirm<input id=deleteWord name=confirm autocomplete=off></label>
<button class="rg-btn secondary btn-tangerine full" id=deleteGo disabled>Delete account</button>
</form>
<button type=button class="rg-btn secondary full" onclick="this.closest('dialog').close()">Cancel</button>
<p class='ty-muted ty-sm'>Want a break instead? Leave a single club from its page.</p>
</div></dialog>
<script>
(function(){
 var file=document.getElementById('photoFile'), clear=document.getElementById('photoClear'), img=document.getElementById('avatarImg'), letters=document.getElementById('avatarLetters'), pref=document.getElementById('prefName'), phone=document.getElementById('phoneInput'), removeBtn=document.getElementById('photoRemove'), usawp=document.getElementById('usawpNumber');
 var dlg=document.getElementById('photoDlg'), drop=document.getElementById('photoDrop'), cropBox=document.getElementById('photoCrop'), zone=document.getElementById('photoZone');
 var stage=document.getElementById('cropStage'), cropImg=document.getElementById('cropImg'), zoomInput=document.getElementById('cropZoom');
 var originalSrc=img.getAttribute('src')||'', hadPhoto={{ 'true' if m.photo else 'false' }}, preview=null;
 var cropUrl=null, zoom=1, panX=0, panY=0, drag=null, pts={}, pinch=null, applying=false;
 function editing(){ return document.body.classList.contains('profile-edit'); }
 function showPhoto(src){img.hidden=false; img.src=src; letters.hidden=true; if(removeBtn) removeBtn.hidden=false;}
 function showLetters(){img.hidden=true; img.removeAttribute('src'); letters.hidden=false; if(removeBtn) removeBtn.hidden=true;}
 function hasPhoto(){ return !!(img && !img.hidden && img.getAttribute('src')); }
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
 var more=document.getElementById('profileMore'), selfMenu=document.getElementById('selfMenu');
 function placeMenu(el){ if(!el||window.innerWidth<768){ if(el){el.style.left='';el.style.top='';el.classList.remove('popover');} return; } el.classList.add('popover'); var w=el.classList.contains('privacy')?400:340; var r=more.getBoundingClientRect(); var left=Math.max(16, Math.min(window.innerWidth-16-w, r.right-w)); var top=r.bottom+8; el.style.left=left+'px'; el.style.top=top+'px'; el.style.margin='0'; }
 if(more&&selfMenu) more.onclick=function(){ if(window.grunionsOpenSheet) grunionsOpenSheet(selfMenu); else selfMenu.showModal(); requestAnimationFrame(function(){ placeMenu(selfMenu); }); };
 function openNamed(id){ var el=document.getElementById(id); if(!el) return; if(window.grunionsOpenSheet) grunionsOpenSheet(el); else el.showModal(); placeMenu(el); }
 (function(){ var g=document.getElementById('genderId'), r=document.getElementById('genderSelfRow'); if(g&&r) g.addEventListener('change', function(){ r.hidden = g.value!=='self'; }); if(/[?&]edit=identity(&|$)/.test(location.search) && document.getElementById('editSheet')) setTimeout(function(){ openNamed('editSheet'); }, 0); })();
 if(selfMenu) selfMenu.addEventListener('click', function(e){ var b=e.target.closest&&e.target.closest('[data-menu]'); if(!b) return; var kind=b.getAttribute('data-menu'); if(window.grunionsCloseSheet) grunionsCloseSheet(selfMenu); else selfMenu.close(); if(kind==='photo') openPhoto(); else if(kind==='edit') openNamed('editSheet'); else if(kind==='delete') openNamed('deleteSheet'); });
 var delBox=document.getElementById('deleteWord'); if(delBox) delBox.addEventListener('input', function(){ var go=document.getElementById('deleteGo'); if(go) go.disabled=delBox.value!=='DELETE'; });
 if(/[?&]edit=1/.test(location.search)) enter();
 document.getElementById('profileCancel').onclick=leave;
 document.getElementById('profileBack').onclick=function(){ grunionsLeave('/home'); };
 function placePhoto(){ if(!dlg||window.innerWidth<768){ if(dlg){dlg.style.left='';dlg.style.top=''} return; } var panel=dlg.querySelector('.sheet'); var w=420, h=(panel&&panel.offsetHeight)||324; var anchor=document.getElementById('avatarBtn'); var r=anchor.getBoundingClientRect(); var left=Math.max(16, Math.min(window.innerWidth-16-w, r.left)); var top=r.bottom+12; if(top+h>window.innerHeight-16) top=Math.max(16, r.top-12-h); dlg.style.left=left+'px'; dlg.style.top=top+'px'; dlg.style.margin='0'; }
 function openPhoto(){ if(cropBox) cropBox.hidden=true; if(drop) drop.hidden=true; if(removeBtn) removeBtn.hidden=!hasPhoto(); var err=document.getElementById('photoErr'); if(err) err.hidden=true; if(dlg && !dlg.open){ if(window.grunionsOpenSheet) grunionsOpenSheet(dlg); else dlg.showModal(); } requestAnimationFrame(function(){ requestAnimationFrame(function(){ placePhoto(); dlg.tabIndex=-1; dlg.focus(); }); }); }
 document.getElementById('avatarBtn').onclick=openPhoto;
 document.getElementById('camBadge').onclick=function(e){ e.stopPropagation(); openPhoto(); };
 document.getElementById('photoPick').onclick=function(){ file.click(); };
 document.getElementById('photoTake').onclick=function(){ file.setAttribute('capture','environment'); file.click(); };
 document.getElementById('photoChoose').onclick=function(){ file.removeAttribute('capture'); file.click(); };
 document.getElementById('photoComputer').onclick=function(){ file.removeAttribute('capture'); file.click(); };
 document.getElementById('photoPickCancel').onclick=function(){ if(window.grunionsCloseSheet) grunionsCloseSheet(dlg); else dlg.close(); };
 document.getElementById('photoWideX').onclick=function(){ if(window.grunionsCloseSheet) grunionsCloseSheet(dlg); else dlg.close(); };
 zone.addEventListener('dragenter', function(e){ e.preventDefault(); zone.classList.add('over'); });
 zone.addEventListener('dragover', function(e){ e.preventDefault(); zone.classList.add('over'); });
 zone.addEventListener('dragleave', function(e){ e.preventDefault(); zone.classList.remove('over'); });
 zone.addEventListener('drop', function(e){ e.preventDefault(); zone.classList.remove('over'); var f=e.dataTransfer&&e.dataTransfer.files&&e.dataTransfer.files[0]; if(f) startCrop(f); });
 if(phone) phone.addEventListener('input', function(){ var next=formatPhone(phone.value); if(phone.value!==next) phone.value=next; });
 function cover(){ var c=stage.clientWidth||280; return Math.max(c/cropImg.naturalWidth, c/cropImg.naturalHeight); }
 function viewScale(){ return cover()*zoom; }
 function clampPan(){
  var c=stage.clientWidth||280, s=viewScale(), w=cropImg.naturalWidth*s, h=cropImg.naturalHeight*s;
  if(panX>0) panX=0; if(panY>0) panY=0;
  if(panX<c-w) panX=c-w; if(panY<c-h) panY=c-h;
 }
 function paintCrop(){
  clampPan();
  var s=viewScale();
  cropImg.style.width=(cropImg.naturalWidth*s)+'px';
  cropImg.style.height=(cropImg.naturalHeight*s)+'px';
  cropImg.style.transform='translate('+panX+'px,'+panY+'px)';
 }
 function setZoom(z){
  z=Math.max(1, Math.min(4, z));
  var c=stage.clientWidth||280, old=viewScale();
  zoom=z;
  var next=viewScale(), cx=c/2, cy=c/2;
  if(old){ panX=cx-(cx-panX)*(next/old); panY=cy-(cy-panY)*(next/old); }
  if(zoomInput) zoomInput.value=String(zoom);
  paintCrop();
 }
 function resetCrop(){
  zoom=1; if(zoomInput) zoomInput.value='1';
  var c=stage.clientWidth||280, s=viewScale();
  panX=(c-cropImg.naturalWidth*s)/2; panY=(c-cropImg.naturalHeight*s)/2;
  paintCrop();
 }
 function profileFileOk(f){
  var err=document.getElementById('photoErr');
  if(!f||f.size>20*1024*1024||((f.type||'').indexOf('video/')===0)){ if(err){err.hidden=false;err.textContent='Photos only, up to 20 MB'} return false; }
  if(err) err.hidden=true;
  return true;
 }
 function startCrop(f){
  if(!profileFileOk(f)) return;
  if(cropUrl) URL.revokeObjectURL(cropUrl);
  cropUrl=URL.createObjectURL(f);
  cropImg.onload=function(){ drop.hidden=true; cropBox.hidden=false; requestAnimationFrame(resetCrop); };
  cropImg.onerror=function(){ backToDrop(); };
  cropImg.src=cropUrl;
 }
 file.addEventListener('change', function(){ if(applying) return; var f=file.files&&file.files[0]; if(f) startCrop(f); });
 var photoZoneDrop=document.getElementById('photoWideDrop');
 function photoDrag(e){ return e.dataTransfer&&[].slice.call(e.dataTransfer.types||[]).indexOf('Files')>=0; }
 if(photoZoneDrop){
  photoZoneDrop.addEventListener('dragover', function(e){ if(!photoDrag(e)) return; e.preventDefault(); photoZoneDrop.classList.add('over'); var n=(e.dataTransfer.items&&e.dataTransfer.items.length)||1; var c=document.getElementById('photoDropCount'); if(c) c.textContent=n===1?'1 image':n+' images'; });
  photoZoneDrop.addEventListener('dragleave', function(){ photoZoneDrop.classList.remove('over'); });
  photoZoneDrop.addEventListener('drop', function(e){ if(!photoDrag(e)) return; e.preventDefault(); e.stopPropagation(); photoZoneDrop.classList.remove('over'); var f=e.dataTransfer.files&&e.dataTransfer.files[0]; if(f) startCrop(f); });
 }
 document.addEventListener('paste', function(e){ if(!dlg.open||(cropBox&&!cropBox.hidden)) return; var list=e.clipboardData&&e.clipboardData.files; if(list&&list[0]){ e.preventDefault(); startCrop(list[0]); } });
 var photoDragDepth=0;
 document.addEventListener('dragenter', function(e){ if(!photoDrag(e)) return; photoDragDepth++; var n=(e.dataTransfer.items&&e.dataTransfer.items.length)||1; var label=n===1?'1 image':n+' images'; if(dlg.open&&window.innerWidth>=768&&photoZoneDrop){ photoZoneDrop.classList.add('over'); var c=document.getElementById('photoDropCount'); if(c) c.textContent=label; return; } var card=document.getElementById('photoDragCard'); if(card){ card.hidden=false; var dc=document.getElementById('photoDragCount'); if(dc) dc.textContent=label; } });
 document.addEventListener('dragover', function(e){ if(!photoDrag(e)) return; e.preventDefault(); });
 document.addEventListener('dragleave', function(e){ if(!photoDrag(e)) return; photoDragDepth=Math.max(0, photoDragDepth-1); if(photoDragDepth) return; if(photoZoneDrop) photoZoneDrop.classList.remove('over'); var card=document.getElementById('photoDragCard'); if(card) card.hidden=true; });
 document.addEventListener('drop', function(e){ if(!photoDrag(e)) return; e.preventDefault(); photoDragDepth=0; if(photoZoneDrop) photoZoneDrop.classList.remove('over'); var card=document.getElementById('photoDragCard'); if(card) card.hidden=true; var f=e.dataTransfer.files&&e.dataTransfer.files[0]; if(f){ if(!dlg.open) openPhoto(); startCrop(f); } });
 if(zoomInput) zoomInput.addEventListener('input', function(){ setZoom(parseFloat(zoomInput.value)||1); });
 stage.addEventListener('pointerdown', function(e){
  stage.setPointerCapture(e.pointerId);
  pts[e.pointerId]={x:e.clientX,y:e.clientY};
  stage.classList.add('dragging');
  var ids=Object.keys(pts);
  if(ids.length>=2){ drag=null; var a=pts[ids[0]], b=pts[ids[1]]; pinch={dist:Math.hypot(a.x-b.x,a.y-b.y)||1, zoom:zoom}; }
  else drag={x:e.clientX,y:e.clientY,panX:panX,panY:panY};
 });
 stage.addEventListener('pointermove', function(e){
  if(!pts[e.pointerId]) return;
  pts[e.pointerId]={x:e.clientX,y:e.clientY};
  var ids=Object.keys(pts);
  if(ids.length>=2 && pinch){
   var a=pts[ids[0]], b=pts[ids[1]], dist=Math.hypot(a.x-b.x,a.y-b.y)||1;
   setZoom(pinch.zoom*(dist/pinch.dist));
  } else if(drag){ panX=drag.panX+(e.clientX-drag.x); panY=drag.panY+(e.clientY-drag.y); paintCrop(); }
 });
 function endPointer(e){
  delete pts[e.pointerId];
  var ids=Object.keys(pts);
  if(ids.length<2) pinch=null;
  if(ids.length===1){ var p=pts[ids[0]]; drag={x:p.x,y:p.y,panX:panX,panY:panY}; }
  else { drag=null; stage.classList.remove('dragging'); }
 }
 stage.addEventListener('pointerup', endPointer);
 stage.addEventListener('pointercancel', endPointer);
 function backToDrop(){ cropBox.hidden=true; drop.hidden=true; file.value=''; if(removeBtn) removeBtn.hidden=!hasPhoto(); }
 function discardCrop(){ if(cropBox && !cropBox.hidden) backToDrop(); }
 dlg.addEventListener('click', function(e){ if(e.target===dlg) discardCrop(); });
 dlg.addEventListener('cancel', function(){ discardCrop(); });
 document.getElementById('cropCancel').onclick=function(){ backToDrop(); dlg.close(); };
 document.getElementById('cropOther').onclick=function(){ backToDrop(); file.click(); };
 document.getElementById('cropUse').onclick=function(){
  var c=stage.clientWidth||280, s=viewScale(), out=512;
  var canvas=document.createElement('canvas'); canvas.width=out; canvas.height=out;
  var ctx=canvas.getContext('2d'), ratio=out/c;
  ctx.drawImage(cropImg, panX*ratio, panY*ratio, cropImg.naturalWidth*s*ratio, cropImg.naturalHeight*s*ratio);
  canvas.toBlob(function(blob){
   if(!blob) return;
   var cropped=new File([blob], 'profile.jpg', {type:'image/jpeg'});
   applying=true;
   try{ var dt=new DataTransfer(); dt.items.add(cropped); file.files=dt.files; }catch(err){}
   applying=false;
   var local=URL.createObjectURL(blob);
   if(editing()){ if(preview) URL.revokeObjectURL(preview); preview=local; clear.value=''; showPhoto(local); dlg.close(); return; }
   var body=new FormData();
   body.append('csrf', document.querySelector('#profileForm [name=csrf]').value);
   body.append('action','photo');
   body.append('photo', cropped);
   fetch('/profile', {method:'POST', body:body, headers:{'Accept':'application/json'}}).then(function(r){ return r.json().then(function(j){ return {ok:r.ok, j:j}; }); }).then(function(res){
    if(!res.ok){ return; }
    if(preview) URL.revokeObjectURL(preview);
    preview=null; file.value=''; clear.value='';
    showPhoto(res.j.url); hadPhoto=true; originalSrc=res.j.url;
    dlg.close();
   }).catch(function(){});
  }, 'image/jpeg', 0.92);
 };
 removeBtn.onclick=function(){
  file.value=''; if(preview){ URL.revokeObjectURL(preview); preview=null; }
  if(editing()){ clear.value=hadPhoto?'1':''; showLetters(); dlg.close(); return; }
  var body=new FormData();
  body.append('csrf', document.querySelector('#profileForm [name=csrf]').value);
  body.append('action','photo');
  body.append('photo_clear','1');
  fetch('/profile', {method:'POST', body:body, headers:{'Accept':'application/json'}}).then(function(r){ if(!r.ok) return; clear.value=''; hadPhoto=false; originalSrc=''; showLetters(); dlg.close(); }).catch(function(){});
 };
})();
</script>"""

T["privacy"] = """<form method=post action=/privacy class=privacyform>{{ csrf_field() }}
<p class="rg-day">Who sees your profile</p>
<div class=privcard>
<div class=privrow><span class=grow><b>Profile visible to</b><small>Your teams · coaches &amp; admins always see clearance</small></span><span class=privgo>My teams ›</span></div>
<label class=privrow><span class=grow><b>Show practices attended</b><small>Teammates see your count (e.g. {{ hist|length }} this season)</small></span><span class=r2switch><input type=checkbox name=show_attendance value=1 {% if prefs.show_attendance %}checked{% endif %}><i></i></span></label>
<label class=privrow><span class=grow><b>Show pronouns</b><small>she/her</small></span><span class=r2switch><input type=checkbox name=show_pronouns value=1 {% if prefs.show_pronouns %}checked{% endif %}><i></i></span></label>
</div>
<p class="rg-day">Messages</p>
<div class=privcard>
<label class=privrow><span class=grow><b>Messages from outside my teams</b><small>Off: only people on your teams can message you. Coaches &amp; admins always can.</small></span><span class=r2switch><input type=checkbox name=messages_outside value=1 {% if prefs.messages_outside %}checked{% endif %}><i></i></span></label>
<label class=privrow><span class=grow><b>Show me in 'Message someone'</b><small>Teammates can find you when starting a chat</small></span><span class=r2switch><input type=checkbox name=show_in_picker value=1 {% if prefs.show_in_picker %}checked{% endif %}><i></i></span></label>
</div>
<p class="rg-day">Rides</p>
<div class=privcard>
<label class=privrow><span class=grow><b>Share my exact location</b><small>Only with a driver who agreed to pick you up. Everyone else sees an area.</small></span><span class=r2switch><input type=checkbox name=share_exact_location value=1 {% if prefs.share_exact_location %}checked{% endif %}><i></i></span></label>
</div>
<p class="rg-day">Location</p>
<div class=privcard>
<label class=privrow><span class=grow><b>Save my last location</b><small>{% if prefs.loc_at %}Last saved {{ prefs.loc_at }}, to about 100 m. {% endif %}Used for leave-by alerts and travel time. Only you see it.</small></span><span class=r2switch><input type=checkbox name=save_location value=1 {% if prefs.save_location %}checked{% endif %}><i></i></span></label>
{% if prefs.loc_at %}<div class=privrow><span class=grow><b>Forget my location</b><small>Deletes the saved spot now</small></span><button class="rg-btn ink" form=forgetLoc>Forget</button></div>{% endif %}
</div>
<p class='ty-muted ty-sm'>Public (people not on your teams): first name + last initial and your club only. No stats, no About, no Message.</p>
<button class="rg-btn primary full">Save</button>
</form>
<form id=forgetLoc method=post action=/privacy/location/forget>{{ csrf_field() }}</form>"""

T["settings"] = """<div class="rg-screen rg-settings">
<h1 class=ty-display-l>Settings.</h1>
{{ rg_label('Teams & roles') }}
<div class=rg-srows>{% for org, role in my_roles %}{{ rg_settings_row(org, role) }}{% endfor %}</div>
{{ rg_label('Account') }}
<div class=rg-srows>
{{ rg_settings_row('Notifications', 'On' if push_on else 'Off', '/notifications') }}
{{ rg_settings_row('Privacy', '', '/privacy') }}
{{ rg_settings_row('Appearance', {'system':'System','light':'Light','dark':'Dark'}[ui_theme or 'dark'], '/appearance') }}
{{ rg_settings_row('Your week', (me().avail_days or 'Not set')|replace(',', ' · '), '/calendar?when=availability') }}
{{ rg_settings_row('Rides', 'Offering' if me().ride_offer else 'Off', '/rides/settings') }}
</div>
{{ rg_button('Log out', 'secondary', '/logout') }}
</div>"""

T["person"] = """<div class=profilehero>
<div class=avatarwrap><span class="avatar hero">{% if m.photo %}<img src="/avatar/{{ m.id }}?v={{ m.photo }}" alt="" width="112" height="112">{% else %}{{ initials(m) }}{% endif %}</span></div>
<div class=profilename>{{ display_first(m) }} {{ m.last }}</div>
<p class=profilesub>{% if attendance_private %}Practices attended are private{% else %}{{ hist|length }} practice{{ '' if hist|length == 1 else 's' }} attended{% endif %}</p>
<a class=msgpill href="{{ message_href }}">Message {{ display_first(m) }}</a>
{% if staff %}
<p class=rg-day style="color:var(--team-tangerine)">Club fields · you can edit</p>
<div class=list>
<button type=button class="li prow" data-open=roleSheet><span class=k>Role</span><span class=v>{% if m.is_admin %}Admin{% elif m.role == 'coach' %}Coach{% else %}Member{% endif %} · Change</span></button>
<div class="li prow"><span class=k>Clearance</span><span class="stchip {{ 'tang' if not cleared else 'lime' }}">{% if cleared %}Cleared{% else %}Not cleared{% endif %}</span></div>
</div>
<p class=rg-day>Theirs · view only</p>
{% if me().is_admin %}<div class=list><div class="li prow"><span class=k>Sex on sport membership</span><span class=v>{{ dict(LEGAL_GENDERS).get(m.legal_gender or '', 'Not set') }}</span></div></div>
<p class='ty-muted ty-sm'>For governing-body and insurance rosters. Admins only.</p>{% endif %}
{% endif %}
{% if staff and needs %}<div class=needcard><p class=needkicker>Needs attention</p><b>{{ display_first(m) }}'s {{ needs }}.</b><p>Once you've checked USAWP and SafeSport, mark them in ⋯ › Update compliance.</p></div>{% endif %}
<div class=metrics><div class="metric sun"><b>{{ '%02d'|format(0 if attendance_private else hist|length) }}</b><span>Attended</span></div><div class="metric sky"><b>{{ '%02d'|format(0 if attendance_private else (nmonth or 0)) }}</b><span>This month</span></div></div>
<div class=rg-day>Cleared sports</div>
<div class=sporthead><b>Grunions</b></div>
{% if staff %}
<div class=sportline><span>Water polo</span><span class="st {{ 'st-ok' if cleared else 'st-warn' }}">{{ 'Cleared' if cleared else 'Pending' }}</span></div>
{% if not cleared %}<p class='ty-muted ty-sm'>Not cleared for any sports yet</p>{% endif %}
<div class=rg-day>Compliance</div>
<div class=list>
<div class="li prow"><span class=rowtitle><span class="dot {{ 'ok' if m.usawp_status=='verified' else 'warn' }}" aria-hidden=true></span>Water polo membership</span><span class=v>{% if m.usawp_number %}USAWP #{{ m.usawp_number }}{% else %}Not on file{% endif %}</span></div>
<div class="li prow"><span class=rowtitle><span class="dot {{ 'ok' if safesport else 'bad' }}" aria-hidden=true></span>SafeSport training</span><span class=v>{% if safesport %}expires {{ safesport }}{% else %}Missing{% endif %}</span></div>
<div class="li prow"><span class=rowtitle><span class="dot {{ 'ok' if background else 'warn' }}" aria-hidden=true></span>Background screening</span><span class=v>{% if background %}expires {{ background }}{% else %}Not on file{% endif %}</span></div>
</div>
<div class=rg-day>Personal</div>
<div class="list infogrid">
<div class="li prow"><span class=k>Legal name</span><span class=v>{{ m.first }} {{ m.last }}</span></div>
<div class="li prow"><span class=k>Preferred name</span><span class=v>{{ m.preferred_first or '—' }}</span></div>
{{ rg_row('Email', m.email, 'mailto:' ~ m.email, chevron=False) }}
{{ rg_row('Phone', fmt_phone(m.phone) or '—', ('tel:' ~ m.phone) if m.phone else '', chevron=False) }}
</div>
{% else %}
<p class='ty-muted ty-sm'>Not cleared for any sports yet</p>
{% endif %}
</div>
<dialog id=personMenu class="botsheet profmenu"><div class=sheet><div class=grab aria-hidden=true></div>
<div class=menuwho><span class="mark sky">{{ initials(m) }}</span><span class=grow><b>{{ display_first(m) }} {{ m.last }}</b><small>{% if staff %}Grunions · {{ 'Admin' if m.is_admin else ('Coach' if m.role=='coach' else 'Member') }} · you're {{ 'an admin' if me().is_admin else 'a coach' }}{% else %}Grunions{% endif %}</small></span></div>
{% if staff %}
<div class=newcard>
<a class=newrow href="{{ message_href }}"><span class=grow><b>Message {{ display_first(m) }}</b><small>From you, not the board</small></span><span class=chatgo>›</span></a>
<button type=button class=newrow data-open=editDetails><span class=grow><b>Edit details</b><small>Name, email, phone</small></span><span class=chatgo>›</span></button>
<a class=newrow href="/admin/member/{{ m.id }}"><span class=grow><b>Update compliance</b><small>USAWP, SafeSport, background</small></span><span class=chatgo>›</span></a>
<button type=button class=newrow data-open=mergeSheet><span class=grow><b>Merge duplicate…</b><small>Two accounts for the same person</small></span><span class=chatgo>›</span></button>
</div>
<button type=button class=newrow data-open=roleSheet><span class=grow><b>Change role</b><small>Member, coach or admin in Grunions</small></span><span class=chatgo>›</span></button>
<div class=newcard>
<button type=button class="newrow actdanger" data-open=removeSheet><span class=grow><b>Remove from Grunions</b><small>{{ display_first(m) }}'s account and other clubs stay</small></span></button>
</div>
<p class='ty-muted ty-sm'>Only Grunions admins see these. Nothing here changes {{ display_first(m) }}'s other clubs.</p>
{% else %}
<div class=newcard>
<a class=newrow href="{{ message_href }}"><span class=grow><b>Message {{ display_first(m) }}</b><small>Opens a direct chat</small></span><span class=chatgo>›</span></a>
<form method=post action="/profile/{{ m.id }}/report">{{ csrf_field() }}<button class=newrow><span class=grow><b>Report</b><small>Tell the Grunions admins</small></span></button></form>
<form method=post action=/chat/block>{{ csrf_field() }}<input type=hidden name=c value="{{ dm }}"><button class="newrow actdanger"><span class=grow><b>Block</b><small>{{ display_first(m) }} can't message you</small></span></button></form>
</div>
<p class='ty-muted ty-sm'>Members don't see compliance, contact info or roles.</p>
{% endif %}
</div></dialog>
{% if staff %}
<dialog id=roleSheet class="botsheet profmenu"><div class=sheet><div class=grab aria-hidden=true></div>
<form method=post action="/profile/{{ m.id }}/role">{{ csrf_field() }}
<h2 class=newtitle>Role on Grunions</h2>
{% set cur = 'admin' if m.is_admin else ('coach' if m.role == 'coach' else 'member') %}
<button class="roleopt{% if cur == 'member' %} on{% endif %}" name=role value=member><span class=grow><b>Member</b><small>RSVP, chat, Lineup</small></span><em>{% if cur == 'member' %}Current{% else %}Choose{% endif %}</em></button>
<button class="roleopt{% if cur == 'coach' %} on{% endif %}" name=role value=coach><span class=grow><b>Coach</b><small>Manage: schedule + roster</small></span><em>{% if cur == 'coach' %}Current{% else %}Choose{% endif %}</em></button>
<button class="roleopt{% if cur == 'admin' %} on{% endif %}" name=role value=admin><span class=grow><b>Admin</b><small>Everything in Manage</small></span><em>{% if cur == 'admin' %}Current{% else %}Choose{% endif %}</em></button>
<p class="ty-muted ty-sm sm">Roles are per team. {{ display_first(m) }} stays a member on any other team they're on. Board is not a role on this sheet.</p>
</form></div></dialog>
<dialog id=editDetails class="botsheet profmenu"><div class=sheet><div class=grab aria-hidden=true></div>
<form method=post action="/profile/{{ m.id }}/details">{{ csrf_field() }}
<h2 class=newtitle>Edit {{ display_first(m) }}'s details</h2>
<label>Legal name<input name=first value="{{ m.first }}" required></label>
<label>Last name<input name=last value="{{ m.last }}" required></label>
<label>Preferred name<input name=preferred_first value="{{ m.preferred_first or '' }}"></label>
<label>Email<input name=email type=email value="{{ m.email }}" required></label>
<label>Phone<input name=phone value="{{ '' if fmt_phone(m.phone) == '—' else fmt_phone(m.phone) }}" required></label>
<p class='ty-muted ty-sm'>{{ display_first(m) }} gets an email about any change. USAWP and SafeSport numbers are {{ display_first(m) }}'s to edit — you can only mark their status. The preview does not send that email.</p>
<button class="rg-btn primary full">Save</button>
</form></div></dialog>
<dialog id=removeSheet class="botsheet profmenu"><div class=sheet><div class=grab aria-hidden=true></div>
<form method=post action="/profile/{{ m.id }}/remove">{{ csrf_field() }}
<h2 class=newtitle>Remove {{ display_first(m) }} from Grunions?</h2>
<p>{{ display_first(m) }}'s account stays. Only Grunions access ends.</p>
<p><b>Leaves</b><br>Grunions chats, schedule and lineup.</p>
<p><b>Kept</b><br>Attendance history in your club records.</p>
<p><b>Not affected</b><br>{{ display_first(m) }}'s other clubs and login.</p>
<button class="rg-btn secondary btn-tangerine full">Remove from Grunions</button>
</form>
<button type=button class="rg-btn secondary full" onclick="this.closest('dialog').close()">Cancel</button>
<p class='ty-muted ty-sm'>{{ display_first(m) }} gets an email. You can add {{ display_first(m) }} back from Manage › People. The preview does not send that email.</p>
</div></dialog>
<dialog id=mergeSheet class="botsheet profmenu"><div class=sheet><div class=grab aria-hidden=true></div>
<form method=post action="/profile/{{ m.id }}/merge" id=mergeForm>{{ csrf_field() }}
<input type=hidden name=other id=mergeOther>
<input type=hidden name=step id=mergeStep value=merge>
<h2 class=newtitle id=mergeTitle>Merge duplicate.</h2>
<div id=mergeFind>
<p class='ty-muted ty-sm'>Which account is also {{ display_first(m) }} {{ m.last }}? We look for the same email, phone or name in Grunions.</p>
<p class=rg-day>Likely matches</p>
<div id=mergeMatches></div>
<label>Search<input id=mergeSearch placeholder="Search name, email or phone" autocomplete=off></label>
<button type=button class="rg-btn primary full" id=mergeContinue disabled>Continue</button>
</div>
<div id=mergeKeep hidden>
<p class='ty-muted ty-sm'>Keep which details? Pick one for each. Everything else is combined.</p>
<div id=mergeFields></div>
<p class=rg-day>Combined automatically</p>
<p class='ty-muted ty-sm'>Attendance counts add. Compliance keeps the newest valid record. Role in Grunions keeps the higher of the two. Chats and history move into one inbox.</p>
<button type=button class="rg-btn primary full" id=mergeReview>Review merge</button>
</div>
<div id=mergeConfirm hidden>
<p id=mergeConfirmCopy></p>
<button class="rg-btn primary full" id=mergeGo>Merge accounts</button>
</div>
<div id=mergeAsk hidden>
<p id=mergeAskCopy></p>
<p class='ty-muted ty-sm'>Not affected until they confirm. Until then, both accounts stay as they are.</p>
<button class="rg-btn primary full" id=mergeAskGo>Send request</button>
</div>
<div id=mergeDone hidden>
<h2 class=newtitle>Merged.</h2>
<p id=mergeDoneCopy></p>
</div>
</form></div></dialog>
<script type="application/json" id=mergeData>{{ people|tojson }}</script>
{% endif %}
<script>
(function(){
 var more=document.getElementById('profileMore'), menu=document.getElementById('personMenu');
 function place(el){ if(!el) return; if(window.innerWidth<768){ el.style.left=''; el.style.top=''; el.classList.remove('popover'); return; } el.classList.add('popover'); var w=340, r=more.getBoundingClientRect(); el.style.left=Math.max(16, Math.min(window.innerWidth-16-w, r.right-w))+'px'; el.style.top=(r.bottom+8)+'px'; el.style.margin='0'; }
 function open(el){ if(!el) return; if(window.grunionsOpenSheet) grunionsOpenSheet(el); else el.showModal(); place(el); }
 if(more&&menu) more.onclick=function(){ open(menu); };
 if(menu) menu.addEventListener('click', function(e){ var b=e.target.closest&&e.target.closest('[data-open]'); if(!b) return; var el=document.getElementById(b.getAttribute('data-open')); if(window.grunionsCloseSheet) grunionsCloseSheet(menu); else menu.close(); open(el); });
 var raw=document.getElementById('mergeData'); if(!raw) return;
 var people=[]; try{ people=JSON.parse(raw.textContent||'[]'); }catch(err){ people=[]; }
 var picked=null, kept=document.getElementById('m');
 var first=({{ display_first(m)|tojson }}+' '+{{ m.last|tojson }}).trim();
 function show(id){ ['mergeFind','mergeKeep','mergeConfirm','mergeAsk','mergeDone'].forEach(function(n){ var el=document.getElementById(n); if(el) el.hidden=n!==id; }); }
 function paint(){
  var q=(document.getElementById('mergeSearch').value||'').trim().toLowerCase();
  var list=people.filter(function(p){ if(!q) return p.likely; return (p.name+' '+p.email+' '+p.phone).toLowerCase().indexOf(q)>=0; });
  document.getElementById('mergeMatches').innerHTML=list.map(function(p){ return '<button type=button class="newrow'+(picked&&picked.id===p.id?' on':'')+'" data-pick="'+p.id+'"><span class=grow><b>'+p.name+'</b><small>'+(p.chips||'Search result')+'</small></span></button>'; }).join('')||'<p class='ty-muted ty-sm'>No matches.</p>';
  document.getElementById('mergeContinue').disabled=!picked;
 }
 document.getElementById('mergeSearch').addEventListener('input', function(){ picked=null; paint(); });
 document.getElementById('mergeMatches').addEventListener('click', function(e){ var b=e.target.closest('[data-pick]'); if(!b) return; picked=people.filter(function(p){ return String(p.id)===b.getAttribute('data-pick'); })[0]; paint(); });
 document.getElementById('mergeContinue').onclick=function(){ if(!picked) return; document.getElementById('mergeOther').value=picked.id; document.getElementById('mergeTitle').textContent='Keep which details?'; var rows=['name','email','phone','photo']; document.getElementById('mergeFields').innerHTML=rows.map(function(key){ var a=picked.fields[key], b=picked.keep[key]; return '<p><b>'+key+'</b><br><label><input type=radio name=keep_'+key+' value=other checked> '+a+'</label><br><label><input type=radio name=keep_'+key+' value=kept> '+b+'</label></p>'; }).join(''); show('mergeKeep'); };
 document.getElementById('mergeReview').onclick=function(){
  if(picked.other){ document.getElementById('mergeStep').value='ask'; document.getElementById('mergeTitle').textContent='Needs '+picked.name.split(' ')[0]; document.getElementById('mergeAskCopy').textContent=picked.name+' is also in '+picked.other+'. You can only merge accounts that are just in Grunions. We will ask them to confirm by signing in to both. Other club: not affected until they confirm.'; document.getElementById('mergeAskGo').textContent='Send request to '+picked.name.split(' ')[0]; show('mergeAsk'); return; }
  document.getElementById('mergeStep').value='merge'; document.getElementById('mergeTitle').textContent='Merge into '+first+'?'; document.getElementById('mergeConfirmCopy').textContent=picked.name+"'s login stops working. "+first.split(' ')[0]+' gets an email that the accounts were merged. You can undo this for 30 days from Manage › People › History. The preview does not send that email.'; show('mergeConfirm');
 };
 paint();
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
<div class="list memlist">
<div class=viewonly>
{{ cred_row('warn' if on_trial else date_dot(m.usawp_valid_until)|trim, 'USAWP # ' ~ (m.usawp_number or '—'), (trial_badge(tw)|striptags) if on_trial else (fmt_long(m.usawp_valid_until) if m.usawp_valid_until else 'Not on file')) }}
{{ cred_row(date_dot(cred.safesport)|trim, 'SafeSport training', fmt_long(cred.safesport) if cred.safesport else 'Not on file') }}
{{ cred_row(date_dot(cred.background)|trim, 'Background screening', fmt_long(cred.background) if cred.background else 'Not on file') }}
{% set rf = referee_eligibility(m) %}{{ cred_row(date_dot(cred.referee)|trim, 'Referee', (fmt_long(cred.referee) if cred.referee else 'Not on file') ~ ((' · eligibility expired ' ~ fmt_long(rf.expired)) if rf.expired and not rf.eligible else '')) }}
{% if cc %}{{ cred_row('ok' if cc.ok else 'bad', 'Coaching', 'cleared' if cc.ok else cc.text) }}{% elif ce.eligible %}{{ cred_row('ok', 'Coaching', 'Coach eligible') }}{% elif ce.text %}{{ cred_row('bad' if ce.expired else 'warn', 'Coaching', ce.text) }}{% endif %}
</div>
{% if me().is_admin %}
<div class="li editonly"><label class=prefedit style="width:100%;margin:0">USAWP number<input name=number inputmode=numeric autocomplete=off value="{{ m.usawp_number or '' }}"></label></div>
<div class="li editonly"><label class=prefedit style="width:100%;margin:0">Status<select name=verified><option value=yes {{ 'selected' if m.usawp_status=='verified' }}>Verified</option><option value=no {{ 'selected' if m.usawp_status!='verified' }}>Not verified</option></select></label></div>
<div class="li editonly"><label class=prefedit style="width:100%;margin:0">Membership type<input name=membership_type value="{{ m.membership_type or '' }}" placeholder="Individual Membership, Coach" autocomplete=off></label></div>
<div class="li editonly">{{ date_field('Membership expires', 'valid_until', m.usawp_valid_until) }}</div>
<div class="li editonly">{{ date_field('SafeSport expires', 'safesport_expires', cred.safesport) }}</div>
<div class="li editonly">{{ date_field('Background screening expires', 'background_expires', cred.background) }}</div>
<div class="li editonly">{{ date_field('Referee certification expires', 'referee_expires', cred.referee) }}</div>
<div class="li editonly"><label class=prefedit style="width:100%;margin:0">Note<textarea class=planfield name=note rows=4 placeholder="Recorded from Sport:80"></textarea></label></div>
{% endif %}
</div>
{% if not on_trial and ps.reason %}<p class="sm viewonly" style="margin:8px 0 0">{{ ps.reason }}</p>{% endif %}
{% if not cl.ok or m.usawp_status != 'verified' %}<p class="ty-muted ty-sm sm viewonly" style="margin:8px 0 0"><a target=_blank rel=noopener href="https://usawp.sport80.com/">Open Sport:80</a> if you want to look it up yourself.</p>{% endif %}
<h3 class=rg-day>Personal</h3>
<div class="list memlist">
<div class=viewonly>{{ rg_row('Legal name', m.first ~ ' ' ~ m.last, chevron=False) }}</div>
{% if me().is_admin %}
<div class="li prow editonly"><label class=prefedit style="width:100%;margin:0">Legal first name<input name=first value="{{ m.first }}" autocomplete=off required></label></div>
<div class="li prow editonly"><label class=prefedit style="width:100%;margin:0">Legal last name<input name=last value="{{ m.last }}" autocomplete=off required></label></div>
{% endif %}
<div class=viewonly>{{ rg_row('Preferred name', m.preferred_first or '—', chevron=False) }}</div>
{% if me().is_admin %}<div class="li prow editonly"><label class=prefedit style="width:100%;margin:0">Preferred first name<input name=preferred_first value="{{ m.preferred_first or '' }}" placeholder="Leave blank to use legal first name" autocomplete=off></label></div>{% endif %}
{{ rg_row('Email', m.email, 'mailto:' ~ m.email, chevron=False) }}
{{ rg_row('Phone', fmt_phone(m.phone) or '—', ('tel:' ~ m.phone) if m.phone else '', chevron=False) }}
</div>
{% if me().is_admin %}
<h3 class=rg-day>Role</h3>
<div class="list memlist">
{% set _roles = (['Admin'] if m.is_admin else []) + (['Coach'] if m.role=='coach' else []) + (['Referee'] if on_referees else []) %}<div class=viewonly>{{ rg_row('Roles', _roles|join(' · ') if _roles else 'Member', chevron=False) }}</div>
<div class="li editonly"><input type=hidden name=roles_present value=1 form=memberForm><label style="margin:0"><input type=checkbox name=is_admin value=1 form=memberForm {% if m.is_admin %}checked{% endif %}> Admin</label></div>
<div class="li editonly"><label style="margin:0"><input type=checkbox name=is_coach value=1 form=memberForm {% if m.role=='coach' %}checked{% endif %}> Active coach</label></div>
<div class="li editonly"><label style="margin:0"><input type=checkbox name=is_referee value=1 form=memberForm {% if on_referees %}checked{% endif %}> Referee</label></div>
</div>
{% endif %}
{% for a in audits %}<p class="ty-muted ty-sm sm viewonly" style="margin:8px 0 0">{{ a.actor }} changed {{ a.old_name }} → {{ a.new_name }} · {{ fmt_when(a.at) }}</p>{% endfor %}
</form>
{% if me().is_admin %}
{% if program_eligibility is defined and program_eligibility %}<div class=viewonly>{{ program_eligibility|safe }}</div>{% endif %}
<div class=viewonly>
<h3 class=rg-day id=paid>Paid membership</h3>
<div class="rg-list memlist">
{% for ent in paid_details %}{{ rg_row(ent.plan, (('Paid through ' ~ fmt_long(ent.end)) if ent.end else 'No end date') ~ ' · ' ~ (ent.source or 'manual'), '#', '', '', '', ent.status|capitalize, {'active':'paid','pending':'expiring'}.get(ent.status, 'notcleared'), extra='data-open-dialog="paidSheet' ~ ent.id ~ '"') }}
{% endfor %}
{{ rg_row('Add a paid membership', 'Paying is separate from clearance', '#', rg_icon('plus'), 'graphite', extra='data-open-dialog="paidNew"') }}
{% if paid_audits %}{{ rg_row('Membership history', paid_audits|length ~ ' change' ~ ('' if paid_audits|length == 1 else 's'), '#', extra='data-open-dialog="paidHistory"') }}{% endif %}
</div>
<h3 class=rg-day>Clearance</h3>
<div class="rg-list memlist">
{% if m.vr_status == 'pending' %}{{ rg_row('Waiting on an admin', 'Check Sport:80, then enter their membership', chevron=False) }}{% endif %}
<button type=button class="rg-row rg-settings memrowbtn" id=memberManual><span class="rg-lead tone-graphite">{{ rg_icon('edit') }}</span><span class=rg-txt><b>Edit clearance</b><small>USAWP number, SafeSport, background, referee</small></span><span class=rg-chev aria-hidden=true>→</span></button>
</div>
</div>
{% for ent in paid_details %}
<dialog id="paidSheet{{ ent.id }}" class="botsheet modal"><form method=post action="/admin/member/{{ m.id }}#paid" class=sheet>{{ csrf_field() }}<div class=grab aria-hidden=true></div>
<input type=hidden name=action value=paid><input type=hidden name=entitlement_id value="{{ ent.id }}">
<p class=ty-caps>{{ display_first(m) }} {{ m.last }}</p><h2>{{ ent.plan }}.</h2>
<p class=ty-muted>{% if ent.programs %}{{ ent.programs|join(', ') }} · {% endif %}{{ ent.source or 'manual' }}. Paying doesn't clear them; insurance still counts.</p>
<label class=rg-field><span>PLAN</span><select name=plan_id>{% for plan in paid_plans if plan.active or plan.id==ent.plan_id %}<option value="{{ plan.id }}" {% if plan.id==ent.plan_id %}selected{% endif %}>{{ plan.name }}</option>{% endfor %}</select></label>
<label class=rg-field><span>STATUS</span><select name=paid_status>{% for name in paid_statuses %}<option value="{{ name }}" {% if name==ent.status %}selected{% endif %}>{{ name|capitalize }}</option>{% endfor %}</select></label>
<div class=rg-fieldpair><label class=rg-field><span>VALID FROM</span><input type=date name=valid_from value="{{ ent.start }}"></label>
<label class=rg-field><span>PAID THROUGH</span><input type=date name=paid_through value="{{ ent.end }}"></label></div>
<label class=rg-field><span>NOTES</span><textarea name=paid_notes rows=2>{{ ent.notes }}</textarea></label>
<button class="rg-btn primary" name=paid_action value=edit>Save</button>
<button class="rg-btn ghost" name=paid_action value=end>End membership</button>
</form></dialog>
{% endfor %}
<dialog id=paidNew class="botsheet modal"><form method=post action="/admin/member/{{ m.id }}#paid" class=sheet>{{ csrf_field() }}<div class=grab aria-hidden=true></div>
<input type=hidden name=action value=paid>
<p class=ty-caps>{{ display_first(m) }} {{ m.last }}</p><h2>Add a paid membership.</h2>
<p class=ty-muted>Record a payment you've seen. This doesn't charge a card, change an RSVP, or clear them for USA Water Polo or USMS.</p>
<label class=rg-field><span>PLAN</span><select name=plan_id>{% for plan in paid_plans if plan.active %}<option value="{{ plan.id }}">{{ plan.name }}</option>{% endfor %}</select></label>
<label class=rg-field><span>STATUS</span><select name=paid_status>{% for name in paid_statuses %}<option value="{{ name }}">{{ name|capitalize }}</option>{% endfor %}</select></label>
<div class=rg-fieldpair><label class=rg-field><span>VALID FROM</span><input type=date name=valid_from></label>
<label class=rg-field><span>PAID THROUGH</span><input type=date name=paid_through></label></div>
<label class=rg-field><span>NOTES</span><textarea name=paid_notes rows=2></textarea></label>
<button class="rg-btn primary" name=paid_action value=save>Save</button>
<button class="rg-btn ghost" name=paid_action value=active>Save as active</button>
</form></dialog>
{% if paid_audits %}<dialog id=paidHistory class="botsheet modal"><div class=sheet><div class=grab aria-hidden=true></div>
<p class=ty-caps>{{ display_first(m) }} {{ m.last }}</p><h2>Membership history.</h2>
<div class="rg-list memlist">{% for row in paid_audits %}{{ rg_row(row.detail, fmt_when(row.at) ~ ' · ' ~ row.actor, chevron=False) }}{% endfor %}</div>
</div></dialog>{% endif %}
{% set chk = list_row_status(m, 'members') %}
{% endif %}
<script>
(function(){
 var edit=document.getElementById('profileEdit'), cancel=document.getElementById('profileCancel'), back=document.getElementById('profileBack'), manual=document.getElementById('memberManual');
 function openManual(){document.body.classList.add('profile-edit'); var el=document.getElementById('membership'); if(el) el.scrollIntoView({block:'start'});}
 if(edit) edit.onclick=openManual;
 if(manual) manual.onclick=openManual;
 if(cancel) cancel.onclick=function(){document.body.classList.remove('profile-edit'); if(/[?&]edit=1/.test(location.search)) history.replaceState(null,'',location.pathname);};
 if(back) back.onclick=function(){ grunionsLeave('{{ "/members" if me().is_admin else "/admin" }}'); };
 if(/[?&]edit=1/.test(location.search)) openManual();
})();
</script>"""

T["notifications"] = """<div class=rg-screen>
{{ rg_page_title('Notifications', 'Pushes go to this device once you allow them.') }}
{{ push_card() }}
<form method=post action=/notifications class=fxsheet>{{csrf_field()}}
{{ rg_label('Push') }}
{% for key, label in types %}<label class=rg-toggle><span><b>{{ label }}</b></span><input type=checkbox name=push value="{{key}}" {% if prefs.get(key, True) %}checked{% endif %}><i aria-hidden=true></i></label>
{% endfor %}
{{ rg_label('Practice reminders') }}
{{ rg_seg_choice('practice_reminder', [('both','Both'),('email','Email'),('inapp','In-app'),('off','Off')], practice_reminder) }}
<p class="ty-muted ty-sm">In-app uses the push you allow above. Emails include a link to turn practice reminder emails off.</p>
{{ rg_label('Email') }}
<label class=rg-toggle><span><b>Membership, SafeSport and trial reminders</b><small>7 days before, 1 day before, and on the day it expires. Practice cancellation emails always send.</small></span><input type=checkbox name=email_reminders value=1 {% if email_on %}checked{% endif %}><i aria-hidden=true></i></label>
{{ rg_button('Save', 'primary') }}
</form></div>"""

T["chat"] = """<template id=chatSeed>{{ chat_seed|tojson }}</template><div class=chat id=chat><div class=chatin><button type=button id=earlier class=earlier hidden>Load earlier messages</button></div></div><div class=chatpad></div>
{% if chat_locked %}<p class=chatlock>read-only · this practice ended.</p>{% endif %}<div class="composer noprint"><div class=qbar id=quoteBar hidden><div class=grow><b id=quoteWho></b><span id=quoteTxt></span></div><button type=button id=quoteX aria-label="Cancel reply">✕</button></div><div class=qbar id=editBar hidden><div class=grow><b>Editing</b><span id=editHint></span></div><button type=button id=editX aria-label="Cancel edit">✕</button></div><div class=thumbs id=prev hidden></div>
<form id=f><input class=fileclip type=file id=file accept="image/*,image/heic,image/heif,image/heic-sequence,image/heif-sequence,.heic,.heif,.gif,.png,.jpg,.jpeg,.webp" multiple>
<textarea id=body rows=1 maxlength=2000 placeholder="{{ chat_placeholder or 'Message' }}" {% if chat_locked %}disabled{% endif %}></textarea>
<button type=button class="iconbtn send" id=attach aria-label="Add photo">+</button>
</form></div>
<dialog id=attachSheet class="botsheet attachsheet"><div class=sheet>
<div class=grab aria-hidden=true></div>
<div class=attachphone>
<div class=attachhead><h2>Add an image</h2><p class=attachsub>Up to 10 · JPG, PNG, HEIC</p></div>
<div class=attachtiles>
<button type=button class=attachtile id=takePhoto><span class=attachico><img src="/static/nav/attach-camera.svg" width="24" height="24" alt=""></span>Take photo</button>
<button type=button class=attachtile id=choosePhotos><span class=attachico><img src="/static/nav/attach-image.svg" width="24" height="24" alt=""></span>Choose photos</button>
</div>
<button type=button class=attachcancel id=attachCancel>Cancel</button>
</div>
<div class=attachwide>
<div class=attachwidehead><h2>Add an image</h2><button type=button class=attachx id=attachWideX aria-label="Close">✕</button></div>
<div class=attachdrop id=attachDrop>
<div class=idle><span class=attachico><img src="/static/nav/attach-upload.svg" width="24" height="24" alt=""></span><b>Drop an image here</b><button type=button class=attachbrowse id=chooseComputer><svg width="24" height="24" viewBox="0 0 24 24" fill="none" aria-hidden="true"><rect x="3" y="4" width="18" height="16" rx="3" stroke="currentColor" stroke-width="2"/><circle cx="8" cy="9" r="2" fill="currentColor"/><path d="M3 19L10 12L14 16L17 13L21 17" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>Choose from computer</button></div>
<div class=hot><span class=attachico><img src="/static/nav/attach-upload.svg" width="24" height="24" alt=""></span><b>Drop to add</b><p class=attachcount id=attachCount>1 image</p></div>
</div>
<p class=attachnote>Up to 10 · JPG, PNG, HEIC, GIF · 20 MB each. You can also paste (⌘V) or drag straight into the chat.</p>
</div>
<p class=attacherr id=attachErr hidden></p>
</div></dialog>
<div id=dropveil class=dropcard hidden><div class="attachdrop over"><span class=attachico><img src="/static/nav/attach-upload.svg" width="24" height="24" alt=""></span><b>Drop to add</b><p class=attachcount id=dropCount>1 image</p></div></div>
<dialog id=actSheet class="botsheet msgactions"><div class=sheet>
<div class=grab aria-hidden=true></div>
<div class=emogrid id=actEmoji>{% for e in REACTIONS %}<button type=button data-e="{{e}}">{{e}}</button>{% endfor %}<button type=button data-more=1 aria-label="More emoji">+</button></div>
<div class=emopick id=emojiMore hidden></div>
<p id=actConfirm hidden>Delete this message?</p>
<div class=actgroup>
<button type=button class=actrow id=actReply><svg width="24" height="24" viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M20 16a8 8 0 0 0-8-8H6.5M9 4.5 5 8l4 3.5" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>Reply</button>
<div id=actSaveGroup hidden><button type=button class=actrow id=actSave><svg width="24" height="24" viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M12 4v10M8 10l4 4 4-4M5 20h14" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>Save photo</button></div>
<div id=actCopyGroup><button type=button class=actrow id=actCopy><svg width="24" height="24" viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M8 8V5.5A1.5 1.5 0 0 1 9.5 4h9A1.5 1.5 0 0 1 20 5.5v9a1.5 1.5 0 0 1-1.5 1.5H16M5.5 8h9A1.5 1.5 0 0 1 16 9.5v9A1.5 1.5 0 0 1 14.5 20h-9A1.5 1.5 0 0 1 4 18.5v-9A1.5 1.5 0 0 1 5.5 8Z" stroke="currentColor" stroke-width="1.8"/></svg>Copy text</button></div>
<button type=button class=actrow id=actReport><svg width="24" height="24" viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M6 20V4M6 5h11l-2 3.5L17 12H6" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>Report</button>
<div id=actOwn><button type=button class=actrow id=actEdit><svg width="24" height="24" viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M4 20h4L19 9l-4-4L4 16v4Z" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round"/></svg>Edit</button><button type=button class="actrow danger" id=actDelete><svg width="24" height="24" viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M5 7h14M9 7V5h6v2M8 7l1 13h6l1-13" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg><span id=actDeleteLabel>Delete</span></button></div>
</div>
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
<button type=button class="rg-btn secondary full" id=seenClose style="margin-top:12px">Close</button>
</div></dialog>
<script>
const CSRF="{{csrf_token()}}",CH="{{ch}}",EMO={{REACTIONS|tojson}},PAGE=50;let last=0,oldest=0,more=false,loadingOlder=false;const box=document.getElementById('chat'),msgs={};
var chatSeedNode=document.getElementById('chatSeed'); if(chatSeedNode){ try{ window.GRUNIONS_CHAT_SEED=JSON.parse(chatSeedNode.textContent); }catch(e){} chatSeedNode.remove(); }
const esc=s=>s.replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
function chatWhen(iso, now){
 var zone='America/Los_Angeles', MONTHS=['JAN','FEB','MAR','APR','MAY','JUN','JUL','AUG','SEP','OCT','NOV','DEC'];
 function parts(value){
  var out={};
  new Intl.DateTimeFormat('en-US',{timeZone:zone,weekday:'short',year:'numeric',month:'numeric',day:'numeric',hour:'numeric',minute:'2-digit',hourCycle:'h23'}).formatToParts(new Date(value)).forEach(function(p){ if(p.type!=='literal') out[p.type]=p.value; });
  return out;
 }
 function index(p){ return Date.UTC(+p.year, +p.month-1, +p.day)/86400000; }
 function clock(p){ var h=+p.hour, h12=h%12||12; return h12+':'+p.minute+' '+(h<12?'AM':'PM'); }
 function burst(iso, prevIso, now){
  var p=parts(iso), n=parts(now||Date.now()), time=clock(p);
  if(prevIso){
   var prev=parts(prevIso);
   // Rolling gap from the previous message. A reply 29 minutes later stays in the burst and the window starts over. A chain can run for hours.
   if(index(prev)===index(p)) return (new Date(iso)-new Date(prevIso))>=30*60*1000 ? time : '';
  }
  var days=index(n)-index(p);
  if(days<=0){ var h=+p.hour; return (h<12?'THIS MORNING':(h>=17?'TONIGHT':'TODAY'))+' · '+time; }
  if(days===1) return 'YESTERDAY · '+time;
  if(days<7) return String(p.weekday||'').toUpperCase()+' · '+time;
  return MONTHS[(+p.month||1)-1]+' '+(+p.day)+' · '+time;
 }
 chatWhen.burst=burst;
 chatWhen.clock=function(iso){ return clock(parts(iso)); };
 return chatWhen.clock(iso);
}
function burstWhen(iso, prevIso, now){ chatWhen(iso); return chatWhen.burst(iso, prevIso, now); }
const t=iso=>chatWhen(iso);
function rxHtml(id,r){r=r||{};return Object.keys(r).sort().map(e=>`<button type=button class="${r[e].mine?'on':''}" data-m=${id} data-e="${esc(e)}">${e} ${r[e].n}</button>`).join('')}
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
 var text=m.body?`<div class=txt>${linkify(m.body)}${m.edited?' <span class=edited>(edited)</span>':''}</div>`:'';
 var img='';
 if(m.image){
  var iw=+m.image.w||0, ih=+m.image.h||0;
  var ratio=iw>0&&ih>0?';aspect-ratio:'+iw+'/'+ih:'';
  img=`<a class=img style="--iw:${iw};--ih:${ih}${ratio}" href="${m.image.full}" data-full="${m.image.full}"><img src="${m.image.thumb}" alt="Photo from ${esc(m.who)}"${iw&&ih?' width="'+iw+'" height="'+ih+'"':''}></a>`;
 }
 return h+img+text||'<div class=txt></div>'}
function fill(d,m){
 var kept=d.querySelector&&d.querySelector('#seenLine');
 if(kept&&kept.parentNode) kept.parentNode.removeChild(kept);
 d.className='m'+(m.mine?' mine':'')+(m.ann&&!m.deleted?' ann':'');
 d.dataset.g='';
 var html=(m.deleted?'':`<button type=button class=more data-act=${m.id} aria-label="Message actions"><svg width="20" height="20" viewBox="0 0 256 256" fill="currentColor" aria-hidden="true"><path d="M140,128a12,12,0,1,1-12-12A12,12,0,0,1,140,128Zm56-12a12,12,0,1,0,12,12A12,12,0,0,0,196,116ZM60,116a12,12,0,1,0,12,12A12,12,0,0,0,60,116Z"/></svg></button>`)+
  '<div class=mstack>'+bodyHtml(m)+'<div class=msgfoot><span class="exact msgtime">'+esc(t(m.at))+'</span><div class=rx>'+rxHtml(m.id,m.rx)+'</div></div></div>';
 d.innerHTML=html;
 var rxEl=d.querySelector('.rx'); if(rxEl) rxEl.dataset.h=rxHtml(m.id,m.rx);
 var foot=d.querySelector('.msgfoot'), home=foot||d;
 if(m&&m.seen&&m.seen.label){ seenInfo=m.seen; var line=kept||document.getElementById('seenLine'); if(!line){ line=document.createElement('button'); line.type='button'; line.id='seenLine'; line.className='seenline'; } var key=seenKey(m.seen); if(line.dataset.seen!==key){ if(line.textContent!==m.seen.label) line.textContent=m.seen.label; line.dataset.seen=key; } if(line.parentNode!==home) home.appendChild(line); }
 else if(kept){ if(foot) foot.appendChild(kept); else d.appendChild(kept); }}
let grouping=false;
function sameGroup(prev,cur){
 if(!prev||!cur||prev.uid!==cur.uid) return false;
 if(!!(prev.ann&&!prev.deleted)!==!!(cur.ann&&!cur.deleted)) return false;
 var delta=new Date(cur.at)-new Date(prev.at);
 // 30 minutes from this message, not from the first message of the burst.
 return delta>=0&&delta<30*60*1000}
function placeWho(el,m,at){
 var text=((m.ann&&!m.deleted)?'Announcement · ':'')+m.who;
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
  i=j+1}
 placeDividers()}
function placeDividers(){
 // prev is the message just before this one. The 30 minutes restarts there, so the burst is not capped at 30 minutes from its first message.
 var rows=[].slice.call(box.querySelectorAll('.m')), prev=null;
 rows.forEach(function(el){
  var m=msgs[+el.id.slice(3)];
  var label=m?burstWhen(m.at, prev?prev.at:null):'';
  var existing=el.previousElementSibling;
  if(label){
   if(!existing||!existing.classList.contains('daydiv')){
    var d=document.createElement('div'); d.className='daydiv'; d.textContent=label;
    el.parentNode.insertBefore(d, el);
   } else if(existing.textContent!==label) existing.textContent=label;
  } else if(existing&&existing.classList.contains('daydiv')) existing.remove();
  if(m) prev=m;
 })}
function mergeSeen(m){var prev=msgs[m.id];if(prev&&prev.seen&&m&&m.seen==null)m.seen=prev.seen;if(m&&m.deleted)m.rx={};else if(m&&m.rx==null&&prev&&prev.rx)m.rx=prev.rx;return m}
function expiredDelete(m){
 if(!m||!m.deleted) return false;
 var at=m.deleted_at?Date.parse(m.deleted_at):0;
 return !at||Date.now()-at>=5*60*1000}
function dropMessage(id){var el=document.getElementById('msg'+id);if(el)el.remove();delete msgs[id]}
function sweepDeleted(){var changed=false;Object.keys(msgs).forEach(function(id){if(expiredDelete(msgs[id])){dropMessage(id);changed=true}});if(changed&&!grouping)groupMessages()}
function track(m){if(!oldest||m.id<oldest)oldest=m.id;last=Math.max(last,m.id)}
function thread(){return box.querySelector('.chatin')||box}
function add(m){m=mergeSeen(m);if(expiredDelete(m)){dropMessage(m.id);return}msgs[m.id]=m;track(m);if(document.getElementById('msg'+m.id))return;const d=document.createElement('div');d.id='msg'+m.id;fill(d,m);thread().appendChild(d);if(!grouping)groupMessages()}
function sameBubble(a,b){
 if(!a||!b) return false;
 var img=function(x){return x&&x.image?x.image.full+'|'+x.image.thumb:''};
 var rep=function(x){return x&&x.reply?x.reply.id+'|'+x.reply.who+'|'+x.reply.body:''};
 return a.body===b.body&&!!a.deleted===!!b.deleted&&!!a.edited===!!b.edited&&!!a.ann===!!b.ann&&a.who===b.who&&!!a.mine===!!b.mine&&a.uid===b.uid&&img(a)===img(b)&&rep(a)===rep(b)}
function upsert(m,force){m=mergeSeen(m);if(expiredDelete(m)){dropMessage(m.id);if(!grouping)groupMessages();return}var prev=msgs[m.id];msgs[m.id]=m;const d=document.getElementById('msg'+m.id);if(!d){if(!oldest||m.id>=oldest)add(m);return}last=Math.max(last,m.id);if(!force&&d.querySelector('.editbox'))return;if(!force&&sameBubble(prev,m))return;fill(d,m);if(!grouping)groupMessages()}
function paintRx(map){var floor=last-300,rows=[].slice.call(box.querySelectorAll('.m')),pending=[];rows.forEach(function(el){var id=el.id.slice(3),rx=el.querySelector('.rx');if(!rx)return;var known=Object.prototype.hasOwnProperty.call(map,id);if(!known&&+id<=floor)return;var data=known?map[id]:{};if(msgs[id])msgs[id].rx=data;var h=rxHtml(id,data);if(rx.dataset.h===h)return;pending.push(rx,h)});if(!pending.length)return;var anchor=null,before=0,edge=box.getBoundingClientRect().top+4,follow=stick;for(var i=0;i<rows.length;i++){if(rows[i].getBoundingClientRect().bottom>edge){anchor=rows[i];before=anchor.getBoundingClientRect().top;break}}anchoring=true;box.style.overflowAnchor='none';for(var p=0;p<pending.length;p+=2){pending[p].innerHTML=pending[p+1];pending[p].dataset.h=pending[p+1]}if(follow)pinBottom();else if(anchor){var dy=anchor.getBoundingClientRect().top-before;if(dy)box.scrollTop+=dy}box.style.overflowAnchor='';requestAnimationFrame(function(){anchoring=false;if(!follow)stick=nearBottom()})}
let pollGen=0;
function receipt(res, rows){
 var raw=res&&res.headers?res.headers.get('X-Chat-Seen'):null, header;
 if(!raw) header=undefined; else { try{ header=JSON.parse(raw); }catch(e){ header=undefined; } }
 var embedded=null;
 (rows||[]).forEach(function(m){ if(m&&m.seen&&(!embedded||+m.id>+embedded.id)) embedded=m.seen; });
 if(embedded){
  if(header&&header.id!=null&&+header.id===+embedded.id){ embedded.n=header.n; embedded.total=header.total; embedded.label=header.label; }
  return embedded;
 }
 if(header&&header.id!=null){ if(seenInfo&&+seenInfo.id===+header.id) header.seen=seenInfo.seen; return header; }
 if(header===null) return null;
 return undefined;
}
function paintEarlier(){var btn=document.getElementById('earlier');if(btn)btn.hidden=!more}
async function loadEarlier(){if(!more||loadingOlder||!oldest)return;loadingOlder=true;stick=false;try{const r=await fetch('/api/messages?c='+CH+'&before='+oldest+'&limit='+PAGE);const j=await r.json();if(!Array.isArray(j)||j.length<PAGE)more=false;var frag=document.createDocumentFragment(),home=thread();grouping=true;(j||[]).forEach(function(m){m=mergeSeen(m);if(!m||expiredDelete(m)||document.getElementById('msg'+m.id))return;msgs[m.id]=m;track(m);var d=document.createElement('div');d.id='msg'+m.id;fill(d,m);frag.appendChild(d)});var rows=home.querySelectorAll('.m'),anchor=rows[0]||null,edge=box.getBoundingClientRect().top+4;for(var i=0;i<rows.length;i++){if(rows[i].getBoundingClientRect().bottom>edge){anchor=rows[i];break}}var before=anchor?anchor.getBoundingClientRect().top:0;box.style.overflowAnchor='none';var firstMsg=rows[0];if(firstMsg)home.insertBefore(frag,firstMsg);else home.appendChild(frag);grouping=false;groupMessages();paintEarlier();function hold(){if(!anchor)return;var dy=anchor.getBoundingClientRect().top-before;if(dy)box.scrollTop+=dy}if(anchor){anchoring=true;hold();requestAnimationFrame(function(){hold();box.style.overflowAnchor='';anchoring=false;stick=nearBottom()})}else{box.style.overflowAnchor='';stick=nearBottom()}}catch(e){grouping=false;box.style.overflowAnchor=''}loadingOlder=false}
async function refreshOpen(gen,epoch){try{const rs=await fetch('/api/messages?c='+CH+'&sync=1');const sync=await rs.json();if(gen!==pollGen||(window.grunionsNavEpoch|0)!==epoch)return;grouping=true;sync.forEach(function(m){if(gen===pollGen)upsert(m)});grouping=false;groupMessages();const rx=await (await fetch('/api/reactions?c='+CH)).json();if(gen!==pollGen||(window.grunionsNavEpoch|0)!==epoch)return;paintRx(rx);sweepDeleted();var info=receipt(rs,sync);if(info)paintSeen([{id:info.id,seen:info}]);else if(info===null)clearSeen();if(window.grunionsRefresh)grunionsRefresh()}catch(e){grouping=false}}
let pollN=0;
async function poll(){const gen=++pollGen,epoch=window.grunionsNavEpoch|0;try{const first=!box.querySelector('.m');var r=null,j;if(first&&window.GRUNIONS_CHAT_SEED){j=window.GRUNIONS_CHAT_SEED;window.GRUNIONS_CHAT_SEED=null;}else{r=await fetch('/api/messages?c='+CH+'&after='+last+(first?'&limit='+PAGE:''));j=await r.json();}if(gen!==pollGen||(window.grunionsNavEpoch|0)!==epoch)return;const follow=stick;
 if(first)box.style.visibility='hidden';
 grouping=true;j.forEach(add);grouping=false;groupMessages();var seenNow=receipt(r,j);if(seenNow)paintSeen([{id:seenNow.id,seen:seenNow}]);else if(seenNow===null)clearSeen();if(first){more=j.length>=PAGE;paintEarlier()}if((first||j.length)&&follow&&stick)pinBottom();if(first)box.style.visibility='';
 pollN++;if(first){setTimeout(function(){refreshOpen(gen,epoch).then(function(){if(stick)pinBottom()})},0);return}if(pollN%4===0){var h=box.scrollHeight;await refreshOpen(gen,epoch);if(follow&&stick&&box.scrollHeight!==h)pinBottom()}else if(j.length){if(follow&&stick)pinBottom()}}catch(e){grouping=false;box.style.visibility=''}}
let seenInfo=null;
function personRow(p){
 const av=p.photo?`<span class="avatar seenav"><img src="${esc(p.photo)}" alt="" width="32" height="32"></span>`:`<span class="avatar seenav">${esc(p.initials||'')}</span>`;
 return `<div class=seenrow>${av}<span>${esc(p.name||'')}</span></div>`}
function seenKey(info){return info.id+'|'+info.n+'|'+info.total+'|'+info.label}
function clearSeen(){var line=document.getElementById('seenLine');if(line)line.remove();seenInfo=null}
function paintSeen(list){
 var hit=null;
 (list||[]).forEach(function(m){ if(m&&m.seen&&(!hit||+m.id>+hit.id)) hit=m; });
 if(!hit) return;
 var row=document.getElementById('msg'+hit.seen.id);
 var line=document.getElementById('seenLine');
 var extras=0;
 document.querySelectorAll('.seenline').forEach(function(el){ if(el!==line) extras++; });
 var key=seenKey(hit.seen);
 var foot=row&&row.querySelector('.msgfoot'), home=row?(foot||row):null;
 var same=!!(row&&line&&line.dataset.seen===key&&line.textContent===hit.seen.label&&line.parentNode===home&&!extras);
 var hold=!same&&typeof box!=='undefined'&&!!box&&!!box.getBoundingClientRect;
 var anchor=null, beforeTop=0, follow=false;
 if(hold){ follow=!!stick; anchoring=true; box.style.overflowAnchor='none'; var edge=box.getBoundingClientRect().top+4, rows=box.querySelectorAll('.m'); for(var i=0;i<rows.length;i++){ if(rows[i].getBoundingClientRect().bottom>edge){ anchor=rows[i]; beforeTop=anchor.getBoundingClientRect().top; break; } } }
 document.querySelectorAll('.seenline').forEach(function(el){ if(el!==line) el.remove(); });
 if(!row){ if(hold){ box.style.overflowAnchor=''; anchoring=false; } return; }
 Object.keys(msgs).forEach(function(id){ if(+id!==+hit.seen.id&&msgs[id]&&msgs[id].seen) delete msgs[id].seen; });
 if(msgs[hit.seen.id]) msgs[hit.seen.id].seen=hit.seen;
 seenInfo=hit.seen;
 if(!line){ line=document.createElement('button'); line.type='button'; line.id='seenLine'; line.className='seenline'; }
 if(line.dataset.seen!==key){ if(line.textContent!==seenInfo.label) line.textContent=seenInfo.label; line.dataset.seen=key; }
 if(line.parentNode!==home) home.appendChild(line);
 if(!hold) return;
 if(follow) pinBottom();
 else if(anchor){ var dy=anchor.getBoundingClientRect().top-beforeTop; if(dy) box.scrollTop+=dy; }
 box.style.overflowAnchor='';
 requestAnimationFrame(function(){ anchoring=false; if(!follow) stick=nearBottom(); });
}
function openSeen(info){
 document.getElementById('seenPeople').innerHTML=(info.seen||[]).map(personRow).join('')||'<p class="ty-muted ty-sm sm">No one has seen this yet.</p>';
 grunionsOpenSheet(document.getElementById('seenSheet'))}
const sheet=document.getElementById('actSheet'),actEdit=document.getElementById('actEdit'),actDelete=document.getElementById('actDelete'),actConfirm=document.getElementById('actConfirm'),actOwn=document.getElementById('actOwn'),actCopyGroup=document.getElementById('actCopyGroup'),emojiMore=document.getElementById('emojiMore'),quoteBar=document.getElementById('quoteBar'),editBar=document.getElementById('editBar');
const MORE=["😀","😁","😊","😉","😍","😘","😎","🤔","😭","😡","🤯","🤗","🫡","🤝","👏","🙌","💪","✌️","👋","✅","⭐","💧","🏊","🤽","🏆","📣","📸","🧡","💛","💚","💙","💜","🖤","🤍","💔","🤣","😅","😴","🎉"];
emojiMore.innerHTML=MORE.map(e=>`<button type=button data-e="${e}">${e}</button>`).join('');
let actId=null,confirming=false,replyTo=null,editId=null;
function buzz(){try{if(navigator.vibrate)navigator.vibrate(12)}catch(err){}}
function closeSheet(){actId=null;confirming=false;actConfirm.hidden=true;document.getElementById('actDeleteLabel').textContent='Delete';emojiMore.hidden=true;grunionsCloseSheet(sheet)}
function openSheet(id){const m=msgs[id];if(!m||m.deleted)return;actId=id;confirming=false;actConfirm.hidden=true;document.getElementById('actDeleteLabel').textContent='Delete';emojiMore.hidden=true;
 actEdit.hidden=!(m.mine&&!m.deleted);actDelete.hidden=!m.can_delete;actOwn.hidden=actEdit.hidden&&actDelete.hidden;actCopyGroup.hidden=!m.body;
 document.getElementById('actSaveGroup').hidden=!(m.image&&m.image.full);
 grunionsOpenSheet(sheet)}
async function savePhoto(url){
 var name='grunions-photo.jpg';
 try{
  var res=await fetch(url,{credentials:'same-origin'});
  if(!res.ok) throw new Error('fetch');
  var blob=await res.blob();
  var kind=blob.type||'';
  var ext=kind.indexOf('png')>=0?'png':(kind.indexOf('gif')>=0?'gif':(kind.indexOf('webp')>=0?'webp':'jpg'));
  name='grunions-photo.'+ext;
  var file=new File([blob], name, {type:kind||'image/jpeg'});
  if(navigator.canShare&&navigator.canShare({files:[file]})){await navigator.share({files:[file], title:'Photo'});return}
  var a=document.createElement('a'); a.href=URL.createObjectURL(blob); a.download=name;
  document.body.appendChild(a); a.click(); a.remove();
  setTimeout(function(){URL.revokeObjectURL(a.href)},1500);
 }catch(err){
  if(err&&err.name==='AbortError') return;
  var link=document.createElement('a'); link.href=url; link.download=name; link.rel='noopener';
  document.body.appendChild(link); link.click(); link.remove();
 }}
function clearCompose(){const field=document.getElementById('body');field.value='';document.getElementById('file').value='';document.getElementById('prev').hidden=true;document.getElementById('prev').innerHTML='';replyTo=null;editId=null;quoteBar.hidden=true;editBar.hidden=true;grow()}
function startReply(id){const m=msgs[id];if(!m||m.deleted)return;editId=null;editBar.hidden=true;replyTo=id;document.getElementById('quoteWho').textContent=m.who;document.getElementById('quoteTxt').textContent=(m.body||'Photo').slice(0,140);quoteBar.hidden=false;document.getElementById('body').focus()}
function startEdit(id){const m=msgs[id];if(!m||m.deleted||!m.mine)return;replyTo=null;quoteBar.hidden=true;editId=id;const field=document.getElementById('body');field.value=m.body||'';grow();document.getElementById('editHint').textContent=(m.body||'Photo').slice(0,80);editBar.hidden=false;field.focus()}
async function reactWith(id,emoji){pollGen++;await fetch('/api/messages/'+id+'/react',{method:'POST',headers:{'Content-Type':'application/json','X-CSRF':CSRF},body:JSON.stringify({emoji:emoji})});closeSheet();poll()}
async function showWho(pill){const r=await fetch('/api/messages/'+pill.dataset.m+'/reactors?emoji='+encodeURIComponent(pill.dataset.e));const j=await r.json().catch(()=>({}));document.getElementById('whoTitle').textContent=pill.dataset.e||'';document.getElementById('whoList').innerHTML=(j.people||[]).map(personRow).join('')||'<p class="ty-muted ty-sm sm">No one</p>';grunionsOpenSheet(document.getElementById('whoSheet'))}
function toast(msg, ms){const el=document.createElement('div');el.className='toast noprint';el.setAttribute('role','status');el.textContent=msg;document.body.appendChild(el);setTimeout(()=>el.remove(),ms||2000)}
function photoKind(f){
 var name=(f.name||'').toLowerCase(), type=(f.type||'').toLowerCase();
 var ext=name.indexOf('.')>=0?name.split('.').pop():'';
 if(type.indexOf('video/')===0||ext==='mov'||ext==='mp4') return 'video';
 if(type.indexOf('dng')>=0||type.indexOf('proraw')>=0||ext==='dng') return 'proraw';
 var okType={'image/jpeg':1,'image/jpg':1,'image/png':1,'image/gif':1,'image/webp':1,'image/heic':1,'image/heif':1,'image/heic-sequence':1,'image/heif-sequence':1};
 var okExt={jpg:1,jpeg:1,png:1,gif:1,webp:1,heic:1,heif:1};
 if(okType[type]||(type.indexOf('image/')===0&&okExt[ext])||(!type&&okExt[ext])) return '';
 return 'other';
}
function photoError(kind){
 if(kind==='video') return "Live Photo videos aren't supported. Send the still photo. Use a JPG, PNG, GIF, WEBP, or HEIC photo.";
 if(kind==='proraw') return "ProRAW isn't supported. Export it as a JPEG or HEIC still. Use a JPG, PNG, GIF, WEBP, or HEIC photo.";
 return "That photo isn't supported. Use a JPG, PNG, GIF, WEBP, or HEIC photo.";
}
document.getElementById('actReply').onclick=()=>{const id=actId;closeSheet();startReply(id)};
document.getElementById('actCopy').onclick=async()=>{const m=msgs[actId];if(!m||!m.body)return;try{await navigator.clipboard.writeText(m.body)}catch(err){const t=document.createElement('textarea');t.value=m.body;document.body.appendChild(t);t.select();document.execCommand('copy');t.remove()}closeSheet();toast('Copied')};
document.getElementById('actReport').onclick=()=>{closeSheet();var form=document.getElementById('requestForm');if(form){if(form.subject)form.subject.value='Report a message';if(window.grunionsPaintRequest)grunionsPaintRequest();if(window.grunionsOpenSheet)grunionsOpenSheet(document.getElementById('requestSheet'));return}location.href='/chat?c=requests'};
document.getElementById('actSave').onclick=async()=>{const m=msgs[actId];if(!m||!m.image)return;var url=m.image.full;closeSheet();await savePhoto(url)};
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
 var tapped=e.target.closest&&e.target.closest('.m');
 if(tapped&&!(e.target.closest&&e.target.closest('button,a,.rx'))){
  tapped.classList.add('showtime');
  clearTimeout(tapped._time);
  tapped._time=setTimeout(function(){tapped.classList.remove('showtime')},3000);
 }
 var skip=e.target.closest&&e.target.closest('a.msglink');
 if(skip&&skip.dataset.suppress){ e.preventDefault(); delete skip.dataset.suppress; return; }
 const b=e.target.closest('button,a.img');if(!b||b.dataset.save!=null||b.hasAttribute('data-cancel'))return;
 if(b.classList.contains('seenline')){if(seenInfo)openSeen(seenInfo);return}
 if(b.matches('a.img')){e.preventDefault();const lb=document.createElement('div');lb.className='lightbox';const full=b.dataset.full;lb.innerHTML=`<img src="${full}" alt=""><button type=button class="rg-btn secondary savephoto">Save photo</button>`;lb.querySelector('.savephoto').onclick=function(ev){ev.stopPropagation();savePhoto(full)};lb.addEventListener('click',function(ev){if(ev.target===lb||ev.target.tagName==='IMG')lb.remove()});document.body.appendChild(lb);return}
 if(b.dataset.act){openSheet(+b.dataset.act);return}
 if(b.dataset.e){if(b.dataset.held){delete b.dataset.held;return}pollGen++;await fetch('/api/messages/'+b.dataset.m+'/react',{method:'POST',headers:{'Content-Type':'application/json','X-CSRF':CSRF},body:JSON.stringify({emoji:b.dataset.e})});poll()}});
const ta=document.getElementById('body'),file=document.getElementById('file'),prev=document.getElementById('prev');
let stick=true,anchoring=false;
function nearBottom(){return box.scrollHeight-box.scrollTop-box.clientHeight<=80}
function pinBottom(){anchoring=true;box.scrollTop=box.scrollHeight;stick=true;requestAnimationFrame(function(){anchoring=false})}
var scrollHide;box.addEventListener('scroll',function(){if(!anchoring)stick=nearBottom();box.classList.add('scrolling');clearTimeout(scrollHide);scrollHide=setTimeout(function(){box.classList.remove('scrolling')},700);if(!anchoring&&!loadingOlder&&more&&box.scrollHeight>box.clientHeight+40&&box.scrollTop<48)loadEarlier()},{passive:true});
if(window.visualViewport){var vvTick;visualViewport.addEventListener('resize',function(){clearTimeout(vvTick);vvTick=setTimeout(function(){if(stick)pinBottom()},50)})}
var earlierBtn=document.getElementById('earlier');if(earlierBtn){earlierBtn.addEventListener('mousedown',function(e){e.preventDefault()});earlierBtn.onclick=function(){loadEarlier()}}
box.addEventListener('load',function(e){if(e.target&&e.target.tagName==='IMG'&&stick)pinBottom()},true);
function syncComposer(){var c=document.querySelector('.composer');if(!c)return;var h=c.offsetHeight+'px';if(document.documentElement.style.getPropertyValue('--composer-h')===h)return;document.documentElement.style.setProperty('--composer-h',h);if(stick)pinBottom()}
function filesNow(){return [].slice.call(file.files||[])}
function composeReady(){return !ta.disabled && (!!ta.value.trim() || filesNow().length);}
function paintCompose(){var act=document.getElementById('attach');if(!act)return;if(ta.disabled){act.disabled=true;act.textContent='↑';act.classList.add('ready');act.setAttribute('aria-label','Read only');return}act.disabled=false;if(composeReady()){act.textContent='↑';act.classList.add('ready');act.setAttribute('aria-label','Send')}else{act.textContent='+';act.classList.remove('ready');act.setAttribute('aria-label','Add photo')}}
function paintThumbs(){
 var files=filesNow();
 prev.hidden=!files.length;
 prev.innerHTML=files.map(function(f,i){return '<figure><img alt="" data-i="'+i+'"><button type=button data-x="'+i+'" aria-label="Remove photo">×</button></figure>'}).join('');
 [].slice.call(prev.querySelectorAll('img')).forEach(function(img,i){
  var f=files[i], url=URL.createObjectURL(f);
  img.onerror=function(){createImageBitmap(f).then(function(bmp){var c=document.createElement('canvas');var scale=Math.min(1,520/Math.max(bmp.width,bmp.height));c.width=Math.max(1,Math.round(bmp.width*scale));c.height=Math.max(1,Math.round(bmp.height*scale));c.getContext('2d').drawImage(bmp,0,0,c.width,c.height);img.onerror=null;img.src=c.toDataURL('image/jpeg',0.85)}).catch(function(){})};
  img.src=url;
 });
 paintCompose();
}
function setFiles(list){var dt=new DataTransfer();list.forEach(function(f){dt.items.add(f)});file.files=dt.files;paintThumbs()}
function attachError(msg){var el=document.getElementById('attachErr');if(el){el.hidden=!msg;el.textContent=msg||''}if(msg)toast(msg,4500)}
function takePhotos(list){
 var next=filesNow().concat(list);
 if(next.length>10){attachError('Photos only, up to 20 MB');return false}
 for(var i=0;i<list.length;i++){if(list[i].size>20*1024*1024){attachError('Photos only, up to 20 MB');return false}var kind=photoKind(list[i]);if(kind){attachError(photoError(kind));return false}}
 attachError('');
 setFiles(next.slice(0,10));
 return true;
}
function grow(){if(!ta.value){ta.style.height='44px';syncComposer();paintCompose();return}ta.style.height='44px';ta.style.height=Math.max(44, Math.min(ta.scrollHeight,120))+'px';syncComposer();paintCompose()}ta.addEventListener('input',grow);grow();if(window.ResizeObserver){var comp=document.querySelector('.composer');if(comp)new ResizeObserver(syncComposer).observe(comp)}
function placeAttach(){var sheet=document.getElementById('attachSheet'), anchor=document.getElementById('attach'); if(!sheet||window.innerWidth<768){if(sheet){sheet.style.left='';sheet.style.top=''}return} var panel=sheet.querySelector('.sheet'); var w=420, h=(panel&&panel.offsetHeight)||324; var r=anchor.getBoundingClientRect(); var left=Math.max(16, Math.min(window.innerWidth-16-w, r.right-w)); var top=r.top-12-h; if(top<16) top=Math.min(window.innerHeight-16-h, r.bottom+12); if(top<16) top=16; sheet.style.left=left+'px'; sheet.style.top=top+'px'; sheet.style.margin='0'; }
function openAttach(){var sheet=document.getElementById('attachSheet');attachError('');if(window.grunionsOpenSheet)grunionsOpenSheet(sheet);else sheet.showModal();requestAnimationFrame(function(){requestAnimationFrame(function(){placeAttach();sheet.tabIndex=-1;sheet.focus()})})}
function shutAttach(){var sheet=document.getElementById('attachSheet');if(window.grunionsCloseSheet)grunionsCloseSheet(sheet);else sheet.close()}
document.getElementById('attach').onclick=function(){if(composeReady()) document.getElementById('f').requestSubmit(); else openAttach();};
document.getElementById('attachCancel').onclick=shutAttach;
document.getElementById('attachWideX').onclick=shutAttach;
document.getElementById('takePhoto').onclick=function(){file.setAttribute('capture','environment');file.click()};
document.getElementById('choosePhotos').onclick=function(){file.removeAttribute('capture');file.click()};
document.getElementById('chooseComputer').onclick=function(){file.removeAttribute('capture');file.click()};
file.onchange=()=>{var picked=[].slice.call(file.files||[]);file.value='';if(picked.length&&takePhotos(picked))shutAttach()};
prev.addEventListener('click',function(e){var b=e.target.closest('button[data-x]');if(!b)return;var list=filesNow();list.splice(+b.getAttribute('data-x'),1);setFiles(list)});
function fileDrag(e){return e.dataTransfer&&[].slice.call(e.dataTransfer.types||[]).indexOf('Files')>=0}
function dragLabel(e){var n=(e.dataTransfer.items&&e.dataTransfer.items.length)||1;return n===1?'1 image':n+' images'}
var dragDepth=0;
function showDrag(e){var label=dragLabel(e);var sheet=document.getElementById('attachSheet'), zone=document.getElementById('attachDrop'), count=document.getElementById('attachCount'); if(sheet&&sheet.open&&zone&&window.innerWidth>=768){zone.classList.add('over');if(count)count.textContent=label;return} var veil=document.getElementById('dropveil'); if(veil){veil.hidden=false;var c=document.getElementById('dropCount');if(c)c.textContent=label}}
function hideDrag(){var zone=document.getElementById('attachDrop');if(zone)zone.classList.remove('over');var veil=document.getElementById('dropveil');if(veil)veil.hidden=true}
document.addEventListener('dragenter',function(e){if(!fileDrag(e))return;dragDepth++;showDrag(e)});
document.addEventListener('dragover',function(e){if(!fileDrag(e))return;e.preventDefault();showDrag(e)});
document.addEventListener('dragleave',function(e){if(!fileDrag(e))return;dragDepth=Math.max(0,dragDepth-1);if(!dragDepth)hideDrag()});
document.addEventListener('drop',function(e){if(!fileDrag(e))return;e.preventDefault();dragDepth=0;hideDrag();var list=[].slice.call(e.dataTransfer.files||[]);if(list.length&&takePhotos(list)&&document.getElementById('attachSheet').open)shutAttach()});
ta.addEventListener('paste',function(e){var list=[].slice.call((e.clipboardData&&e.clipboardData.files)||[]);if(list.length){e.preventDefault();takePhotos(list)}});
document.getElementById('quoteX').onclick=()=>{replyTo=null;quoteBar.hidden=true};
document.getElementById('editX').onclick=()=>{editId=null;editBar.hidden=true;ta.value='';grow()};
let sending=false;
document.getElementById('f').onsubmit=async e=>{e.preventDefault();if(sending)return;const f=file.files[0];const text=ta.value;
 if(editId){const m=msgs[editId];if(!text.trim()&&!(m&&m.image))return;sending=true;
  try{const r=await fetch('/api/messages/'+editId,{method:'POST',headers:{'Content-Type':'application/json','X-CSRF':CSRF},body:JSON.stringify({body:text})});
  const j=await r.json().catch(()=>({}));if(!r.ok){alert(j.error||'Could not save.');return}clearCompose();if(j.message)upsert(j.message,true)}finally{sending=false}return}
 var batch=filesNow();
 if(!text.trim()&&!batch.length)return;sending=true;
 try{let r;if(batch.length){for(var i=0;i<batch.length;i++){const fd=new FormData();fd.append('body',i?'':text);fd.append('image',batch[i]);if(replyTo)fd.append('reply_to',replyTo);
  r=await fetch('/api/messages?c='+CH,{method:'POST',headers:{'X-CSRF':CSRF},body:fd});
  if(!r.ok){const j=await r.json().catch(()=>({}));toast(j.error||'Could not send.',4500);return}}}
 else r=await fetch('/api/messages?c='+CH,{method:'POST',headers:{'Content-Type':'application/json','X-CSRF':CSRF},body:JSON.stringify({body:text,reply_to:replyTo})});
 if(r&&!r.ok){const j=await r.json().catch(()=>({}));toast(j.error||'Could not send.',4500);return}
 const epoch=window.grunionsNavEpoch|0;clearCompose();stick=true;await poll();if((window.grunionsNavEpoch|0)!==epoch)return;if(stick)pinBottom()}finally{sending=false}};
ta.addEventListener('keydown',e=>{if(e.key==='Enter'&&!e.shiftKey&&!e.isComposing){e.preventDefault();document.getElementById('f').requestSubmit()}});
poll();setInterval(poll,3000);setInterval(sweepDeleted,15000);
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

T["lineup"] = """{% macro lineup_months(groups, mode, past=false) %}{% for g in groups %}<div class=lmonth>{% if mode == 'tall' %}{{ g.label }}{% if past %} · Past{% endif %}{% else %}{{ g.label.split(' ')[0] }}{% endif %}</div>{% for e in g.events %}{{ lineup_card(e, '/lineup' ~ ('?group=' ~ group if group else ''), mode, past) }}{% endfor %}{% endfor %}{% endmacro %}
<div class="rg-filters filt lineupfilt chiprow" data-seg role=group aria-label="Type"><a {% if not group %}class=on aria-current=true{% endif %} href=/lineup>All</a>{% for slug, label in filter_groups %}<a {% if group == slug %}class=on aria-current=true{% endif %} href="/lineup?group={{ slug }}">{{ label }}</a>{% endfor %}</div>
{% if not group %}<div class=lmetrics><div class="lmetric hrs"><b>{{ '%02d'|format(lineup_hours) }}</b><span>SERVICE HRS</span></div><div class="lmetric reg"><b>{{ '%02d'|format(lineup_registered) }}</b><span>REGISTERED</span></div><div class="lmetric dec"><b>{{ '%02d'|format(lineup_decide) }}</b><span>TO DECIDE</span></div></div>{% endif %}
{% if featured %}<div class=lmonth>Pinned</div>{% for e in featured %}{{ lineup_card(e, '/lineup?group=' ~ group, 'tall') }}{% endfor %}{% endif %}
{% if empty_public %}<p class=emptyfind>Nothing on the Lineup yet.</p>{% endif %}
{{ lineup_months(upcoming, 'tall' if group else 'compact') }}
{% if past %}<details class=lineuppast open><summary>{% if group %}Past{% else %}Past{% endif %} <span class=pastn>{{ past_n }}</span></summary>{{ lineup_months(past, 'tall' if group else 'compact', true) }}</details>{% endif %}"""
T["lineup_event"] = """{{ event_hero('lineHero', e.pins, ('/lineup-image/' ~ e.id ~ '?v=' ~ e.banner) if e.banner else '', e.where or e.title) }}
{{ rg_event_hero(e.event_type or 'Event', e.title, [e.when, e.venue, e.city]|select|join(' · '), 'graphite' if e.status == 'canceled' else event_tone(e.event_type), e.status_text if e.status != 'published' else (e.tag or '')) }}
{% if e.status == 'published' %}<form method=post action="/lineup/{{ e.id }}" class="rg-rsvp2 rsvprow">{{ csrf_field() }}<input type=hidden name=event_id value={{ e.id }}>{{ rsvp_base('e' ~ e.id) }}
{% set going_label = 'Join waitlist' if e.full and e.mine != 'going' and e.mine != 'waitlist' else ('Waitlist' if e.mine == 'waitlist' else 'Going') %}
<div class=rg-rsvp2main>{{ rsvp_btn(going_label, e.mine == 'going' or e.mine == 'waitlist', 'going') }}
{{ rsvp_btn('Maybe', e.mine == 'interested', 'interested') }}</div>
{% if e.mine == 'notgoing' %}<button class=rg-cant name=action value=clear>You said you can't make it · Undo</button>{% else %}<button class=rg-cant name=action value=notgoing>Can't make it</button>{% endif %}</form>{% endif %}
<p class=rg-evcount>{{ e.going_n }} going · {{ e.interested_n }} maybe{% if e.capacity %} · {{ e.capacity }} spots{% endif %}</p>
{% if e.shift_mine %}{{ rg_callout("You're volunteering", e.shift_mine.title, 'Your shift →', '/lineup/' ~ e.id ~ '/shifts/' ~ e.shift_mine.id, 'bubblegum') }}
{% elif e.shifts_n %}{{ rg_callout('Volunteer shifts', (e.shifts_open ~ ' spot' ~ ('' if e.shifts_open == 1 else 's') ~ ' open') if e.shifts_open else 'All shifts are full', 'Pick a shift →', '/lineup/' ~ e.id ~ '/shifts', 'bubblegum') }}
{% elif e.can_edit %}<a class=rg-calink href="/lineup/{{ e.id }}/shifts">Add volunteer shifts</a>{% endif %}
<div class=rg-day>Details</div>
<div class="list rg-evdetails">
{% if e.description %}<div class="li evdescrow"><div class=clamp id=evdesc>{{ e.description }}</div><button type=button class=textlink id=evmore hidden>More</button></div>{% endif %}
{% if e.host_org %}<div class="li prow"><span class=k>Host organization</span><span class=v>{{ e.host_org }}</span></div>{% endif %}
{% if e.cohosts %}<div class="li prow"><span class=k>Co-host organizations</span><span class=v>{{ e.cohosts|join(', ') }}</span></div>{% endif %}
{% if e.link %}<div class="li prow"><span class=k>Registration</span><span class=v><a class=reglink href="{{ e.link }}" target=_blank rel="noopener noreferrer">Registration</a></span></div>{% endif %}
{% if e.event_type %}<div class="li prow"><span class=k>Type</span><span class=v>{{ e.event_type }}</span></div>{% endif %}
{% if e.sports_line %}<div class="li prow"><span class=k>Session</span><span class=v>{{ e.sports_line }}</span></div>{% endif %}
{% if e.details %}<div class=li>{{ e.details }}</div>{% endif %}
{% if e.cost %}<div class="li prow"><span class=k>Cost</span><span class=v>About {{ e.cost }}</span></div>{% endif %}
{% if e.capacity %}<div class="li prow"><span class=k>Spots</span><span class=v>{{ e.going_n }} of {{ e.capacity }}{% if e.wait_n %} · {{ e.wait_n }} waitlisted{% endif %}</span></div>{% endif %}
{% if e.reg_deadline %}<div class="li prow"><span class=k>Register by</span><span class=v>{{ e.reg_deadline }}</span></div>{% endif %}
</div>
{% if e.levels_raw %}<details class=card><summary>Skill levels</summary><div class=body>{% for row in level_catalog(e.sport if e.sport is defined else 'Water Polo', e.levels_raw) %}{% if row[0] in e.levels_raw.split(',') %}<p><b>{{ row[1] }}</b> {{ row[2] }}</p>{% endif %}{% endfor %}</div></details>{% endif %}
{% if e.review_note and e.status in ('changes_requested', 'declined') %}<div class=note>{{ e.review_note }}</div>{% endif %}
{{ whos_going(e.interested, "interested") }}
{{ whos_going(e.people) }}
{% if e.can_review and e.intent == 'considering' %}<form method=post action="/lineup/{{ e.id }}" style="margin-top:10px">{{ csrf_field() }}<button class="rg-btn primary full" name=action value=official>Make official</button></form>{% endif %}
{% if e.venue or e.city %}{{ event_location('lineLoc', e.pins, e.venue or e.city, e.city if e.venue else '', e.dir_href) }}{% endif %}
<script>(function(){var el=document.getElementById('evdesc'),btn=document.getElementById('evmore');if(!el||!btn)return;if(el.scrollHeight>el.clientHeight+2)btn.hidden=false;btn.onclick=function(){var open=el.classList.toggle('open');btn.textContent=open?'Less':'More';};})();</script>"""
T["approvals"] = """{% call admin_page('Events') %}<a class="rg-btn ghost pageact" href="/events/new">Create event</a>{% endcall %}
{% if queue %}<h2>Needs review ({{ queue|length }})</h2>
{% for e in queue %}<div class=card>
<div class=nxtitle>{{ e.title }}</div>
<div class="ty-muted ty-sm sm">{{ e.status_text or e.status_label }}{% if e.tag %} · {{ e.tag }}{% endif %}</div>
<div class=nxrow>{{ glyph_clock() }}<span>{{ e.when }}</span></div>
{% if e.where %}<div class=nxrow>{{ glyph_pin() }}<span>{{ e.where }}</span></div>{% endif %}
{% if e.description %}<div class=evnote>{{ e.description }}</div>{% endif %}
{% if e.review_note %}<div class=note>{{ e.review_note }}</div>{% endif %}
<form method=post action=/admin/approvals style="margin-top:12px">{{ csrf_field() }}<input type=hidden name=event_id value={{ e.id }}>
<button class="rg-btn primary full" name=action value=approve>Approve &amp; Publish</button>
<label style="margin-top:12px">Note<textarea class=planfield name=note rows=4 placeholder="Needed for changes or a decline"></textarea></label>
<div class=row><button class="rg-btn secondary" name=action value=changes>Request Changes</button><button class="rg-btn danger" name=action value=decline>Decline</button></div>
</form></div>{% endfor %}{% endif %}
{% for g in groups %}<h2>{{ g.label }}</h2><div class=list>{% for item in g['items'] %}<a class=li href="{{ item.href }}" style="color:inherit;text-decoration:none"><span class=grow><span class=ell style="display:block;font-weight:650">{{ item.title }}</span><span class="ty-muted ty-sm sm">{{ item.when }}{% if item.place %} · {{ item.place }}{% endif %}</span></span></a>{% endfor %}</div>{% endfor %}
{% if not groups and not queue %}<p class=emptyfind>Nothing coming up.</p>{% endif %}"""
T["usage"] = ADMIN_NAV + """<div class="rg-screen rg-usage">
{{ rg_page_title('Usage', 'Map and traffic calls. Free tier resets ' ~ resets ~ '.') }}
{{ rg_stat('MAPBOX CALLS TODAY', calls, delta, bars) }}
<div class=rg-metrics>{{ rg_metric(month_calls, 'This month', 'lime') }}{{ rg_metric(pct ~ '%', 'Of ' ~ free_label ~ ' free', 'carbon') }}</div>
{{ rg_label('What uses it') }}
<div class=rg-srows>{% for label, n in uses %}{{ rg_settings_row(label, n) }}{% endfor %}</div>
<p class="ty-muted ty-sm">{% if not uses_tracked %}The breakdown starts counting from today. {% endif %}If the daily limit ({{ cap }}) is hit, maps fall back to the venue address. Nothing breaks.</p>
</div>"""
T["manage"] = ADMIN_NAV + """<div class=managehome id=manageHome>
{# 08.13 Manage home: search · Avg checked in · four hub tiles. Every piece is a component. #}
<div id=manageSearchWrap>{{ rg_search('manageSearch', 'Search settings, people, tools…', '/manage/area/club' if club_admin else '', 'settings', 'manageClear') }}</div>
<div id=manageHits class=mgroups hidden aria-live=polite></div>
<div id=manageBody class=rg-stack>
{% if needs_n %}{{ rg_callout(needs_n ~ ' need you', needs_n ~ ' not cleared', 'Review', '/members?view=compliance', 'tangerine') }}{% endif %}
{{ rg_chart_switch(charts if club_admin else charts[:1]) }}
<div class=rg-hubgrid>
{{ rg_hub('/manage/area/activities', week|length, 'Activities', 'Schedule, Lineup, Bulletin & requests', 'sun') }}
{% if club_admin %}{{ rg_hub('/manage/area/people', people_n, 'People', 'Participants, members, coaches, admins & refs', 'sky') }}
{{ rg_hub('/manage/area/club', club_rows|length, 'Club', 'Sports, plans & sharing', 'tangerine') }}
{{ rg_hub('/manage/area/tools', tool_rows|length, 'Tools', 'QR codes, data transfer & usage', 'lavender') }}{% else %}
{{ rg_hub('/admin', week|length, 'Check-in', 'Today and upcoming practices', 'sky') }}{% endif %}
</div>
</div>
</div>
<script>
(function(){
  var input=document.getElementById("manageSearch");
  var hits=document.getElementById("manageHits");
  var clearBtn=document.getElementById("manageClear");
  var wrap=document.getElementById("manageSearchWrap");
  if(!input||!hits) return;
  var seq=0, timer=0, current="schedule";
  function seg(){
    var q=(input.value||"").trim();
    var body=document.getElementById("manageBody"); if(body) body.hidden=!!q;
    hits.hidden=!q;
    if(clearBtn) clearBtn.hidden=!q;
  }
  document.querySelectorAll("[data-mseg]").forEach(function(b){
    b.addEventListener("click", function(){
      if((input.value||"").trim()){ input.value=""; hits.textContent=""; }
      seg(b.getAttribute("data-mseg"));
    });
  });
  function note(text){
    hits.textContent="";
    var p=document.createElement("p");
    p.className="emptyfind";
    p.textContent=text;
    hits.appendChild(p);
  }
  function personRow(row){
    var a=document.createElement("a");
    a.className="prow2";
    a.href=row.href;
    var grow=document.createElement("span");
    grow.className="grow";
    var title=document.createElement("b");
    title.textContent=row.name||"";
    var desc=document.createElement("small");
    desc.textContent=(row.role||"Member")+(row.status?" \\u00b7 "+row.status:"");
    grow.appendChild(title); grow.appendChild(desc);
    a.appendChild(grow);
    if(row.status){
      var chip=document.createElement("span");
      chip.className="stchip "+((row.status||"").toLowerCase().indexOf("not")===0?"tang":"lime");
      chip.textContent=row.status;
      a.appendChild(chip);
    }
    return a;
  }
  function settingRow(row){
    var a=document.createElement("a");
    a.className="mrow mtile sun";
    a.href=row.href;
    var grow=document.createElement("span");
    grow.className="grow";
    var title=document.createElement("span");
    title.className="mtitle";
    title.textContent=row.title||"";
    var desc=document.createElement("span");
    desc.className="mdesc";
    desc.textContent=row.desc||"";
    grow.appendChild(title); grow.appendChild(desc);
    a.appendChild(grow);
    return a;
  }
  function group(title, rows, make){
    if(!rows||!rows.length) return;
    var sec=document.createElement("section");
    sec.className="mgroup";
    var h=document.createElement("h2");
    h.className="mseclabel";
    h.textContent=title;
    var list=document.createElement("div");
    rows.forEach(function(row){ list.appendChild(make(row)); });
    sec.appendChild(h); sec.appendChild(list);
    hits.appendChild(sec);
  }
  function paint(q, data){
    hits.textContent="";
    var people=(data&&data.people)||[];
    var settings=(data&&data.settings)||[];
    if(!people.length&&!settings.length){ note("No matches for \\u201c"+q+"\\u201d"); return; }
    group("People", people, personRow);
    group("Settings", settings, settingRow);
  }
  function run(){
    var q=(input.value||"").replace(/\\s+/g," ").trim();
    seg(current);
    if(!q){ hits.textContent=""; return; }
    if(wrap) wrap.hidden=false;
    hits.hidden=false;
    document.querySelectorAll(".mpanel").forEach(function(p){ p.hidden=true; });
    var mine=++seq;
    fetch("/manage/search?q="+encodeURIComponent(q),{credentials:"same-origin",headers:{Accept:"application/json"}})
      .then(function(r){ if(!r.ok) throw new Error("search"); return r.json(); })
      .then(function(data){ if(mine!==seq) return; paint(q, data); })
      .catch(function(){ if(mine!==seq) return; note("Search didn\\u2019t load. Try again."); });
  }
  input.addEventListener("input", function(){
    if(timer) clearTimeout(timer);
    if(!(input.value||"").trim()){ run(); return; }
    if(wrap) wrap.hidden=false;
    hits.hidden=false;
    timer=setTimeout(run, 160);
  });
  input.addEventListener("keydown", function(e){
    if(e.key!=="Enter") return;
    e.preventDefault();
    if(timer) clearTimeout(timer);
    run();
  });
  input.addEventListener("search", function(){
    if(timer) clearTimeout(timer);
    run();
  });
  if(clearBtn) clearBtn.addEventListener("click", function(){
    input.value="";
    if(timer) clearTimeout(timer);
    run();
    input.focus();
  });
  var params=new URLSearchParams(location.search);
  if(params.get("tab")&&document.querySelector('[data-mseg="'+params.get("tab")+'"]')) seg(params.get("tab"));
})();
</script>"""
T["manage_area"] = ADMIN_NAV + """{{ admin_page(title, subtitle) }}
{% if tiles %}<div class=rg-tilestack>{% for href, t, sub, n, tone in tiles %}{{ rg_stack_tile(href, t, sub, n, tone) }}{% endfor %}</div>{% endif %}
<div class=mlist style="margin-bottom:120px">{% for row in rows %}{{ manage_row(row.href, row.title, row.desc, row.icon, row.count, row.tone, row.tile, row.num) }}{% endfor %}</div>"""
T["manage_schedule"] = ADMIN_NAV + """{{ admin_page('Schedule', 'Practices, scrimmages, and games.') }}
{% if coming %}<div class=list>{% for item in coming %}<a class=li href="{{ item.href }}" style="color:inherit;text-decoration:none"><span class=grow><span class=ell style="display:block;font-weight:600">{{ item.title }}</span><span class="ty-muted ty-sm sm">{{ item.when }}{% if item.place %} · {{ item.place }}{% endif %}</span></span></a>{% endfor %}</div>{% else %}<p class=emptyfind>Nothing coming up.</p>{% endif %}"""
T["manage_lineup"] = ADMIN_NAV + """{{ admin_page('Lineup', 'Events, tournaments, camps, and socials.') }}
{% if coming %}<div class=list>{% for item in coming %}<a class=li href="{{ item.href }}" style="color:inherit;text-decoration:none"><span class=grow><span class=ell style="display:block;font-weight:600">{{ item.title }}</span><span class="ty-muted ty-sm sm">{{ item.when }}{% if item.place %} · {{ item.place }}{% endif %}</span></span></a>{% endfor %}</div>{% else %}<p class=emptyfind>Nothing coming up.</p>{% endif %}
<a class=wkadd href="/events/new?lane=lineup">+ New lineup event</a>"""
T["manage_requests"] = ADMIN_NAV + """{{ admin_page('Requests', 'Member-submitted events.') }}
<div class="rg-filters filt chiprow" data-seg role=group aria-label="Status"><a {% if view=='pending' %}class=on aria-current=true{% endif %} href="/manage/requests?view=pending">Pending</a><a {% if view=='approved' %}class=on aria-current=true{% endif %} href="/manage/requests?view=approved">Approved</a><a {% if view=='declined' %}class=on aria-current=true{% endif %} href="/manage/requests?view=declined">Declined</a></div>
{% if rows %}{% for e in rows %}<article class="reqcard{% if view != 'pending' %} carbon{% endif %}">
<a href="/manage/requests/{{ e.id }}"><span class=reqpill>{{ e.status_text }}</span><b>{{ e.title }}</b>
<p>{{ e.category }}{% if e.submitter %} · {{ e.submitter }}{% endif %}{% if e.when %} · {{ e.when }}{% endif %}</p></a>
{% if e.status in ('pending', 'changes_requested') %}<div class=reqacts>
<form method=post action=/admin/approvals>{{ csrf_field() }}<input type=hidden name=event_id value={{ e.id }}><button class="rg-btn primary" name=action value=approve>Approve</button></form>
<a class="rg-btn secondary" href="/manage/requests/{{ e.id }}">Decline</a>
</div>{% endif %}
</article>{% endfor %}{% else %}<p class=emptyfind>Nothing here.</p>{% endif %}"""
T["manage_request"] = ADMIN_NAV + """{{ admin_page(e.title) }}
<p class="ty-body sm" style="margin-top:0">{{ e.category }}{% if e.submitter %} · {{ e.submitter }}{% endif %}{% if e.when %} · {{ e.when }}{% endif %}</p>
<p>{{ st(e.status_kind, e.status_text) }}</p>
{% if e.description %}<p>{{ e.description }}</p>{% endif %}
{% if e.review_note %}<div class=note>{{ e.review_note }}</div>{% endif %}
{% if e.status in ('pending', 'changes_requested') %}<form method=post action=/admin/approvals>{{ csrf_field() }}<input type=hidden name=event_id value={{ e.id }}>
<button class="rg-btn primary full" name=action value=approve>Approve &amp; Publish</button>
<label style="margin-top:12px">Note<textarea class=planfield name=note rows=4 placeholder="Needed for changes or a decline"></textarea></label>
<div class=row><button class="rg-btn secondary" name=action value=changes>Request Changes</button><button class="rg-btn danger" name=action value=decline>Decline</button></div>
</form>{% elif e.status == 'published' %}<p style="margin-top:16px"><a class="rg-btn secondary" href="/lineup/{{ e.id }}">View on Lineup</a></p>{% endif %}"""
_CHEV = '<svg width="20" height="20" viewBox="0 0 256 256" fill="currentColor" aria-hidden="true"><path d="M181.66,133.66l-80,80a8,8,0,0,1-11.32-11.32L164.69,128,90.34,53.66a8,8,0,0,1,11.32-11.32l80,80A8,8,0,0,1,181.66,133.66Z"/></svg>'
T["event_new"] = """<form id=planForm method=post action=/events/new enctype=multipart/form-data data-editorform data-practicedays='{{ practice_days|tojson }}'>{{ csrf_field() }}
<h1 class=newevent id=newEventTitle>{% if lane == 'lineup' %}New lineup event.{% else %}New event.{% endif %}</h1>
<input type=hidden name=lane id=laneVal value="{{ 'lineup' if not staff else lane }}">
<input type=hidden name=title_mode id=titleMode value="{{ 'custom' if dup and dup.title else 'auto' }}">
{% if dup %}<input type=hidden name=copy_from value="{{ dup.id }}"><textarea name=coaching_plan hidden>{{ dup.coaching_plan }}</textarea>{% endif %}
<input type=hidden name=mode value="{{ 'create' if staff else 'suggest' }}">
{% if staff %}<h2 class=planask>What are you planning?</h2>
<div class=lanepick role=radiogroup aria-label="What are you planning?">
<button type=button class="lanecard{{ ' on' if lane != 'lineup' }}" data-lane=schedule><b>Team schedule</b><span>Practices, scrimmages &amp; games</span></button>
<button type=button class="lanecard{{ ' on' if lane == 'lineup' }}" data-lane=lineup><b>Lineup event</b><span>Tournaments, camps, trips &amp; socials</span></button>
</div>{% endif %}
{% if staff %}<div id=schedBlock {% if lane == 'lineup' %}hidden{% endif %}>
<div class=actseg role=radiogroup aria-label="Session type">
<label><input type=radio name=activity_type value=practice {% if activity != 'scrimmage' and activity != 'game' %}checked{% endif %}><span>Practice</span></label>
<label><input type=radio name=activity_type value=scrimmage {% if activity == 'scrimmage' %}checked{% endif %}><span>Scrimmage</span></label>
<label><input type=radio name=activity_type value=game {% if activity == 'game' %}checked{% endif %}><span>Game</span></label>
</div>
<div class=rg-day>Team color</div>
<div class=colordots role=radiogroup aria-label="Team color">
<button type=button class="cdot on" style="--c:var(--team-sun)" aria-label="Sun"></button>
<button type=button class=cdot style="--c:var(--team-sky)" aria-label="Sky"></button>
<button type=button class=cdot style="--c:var(--team-tangerine)" aria-label="Tangerine"></button>
<button type=button class=cdot style="--c:var(--lime)" aria-label="Lime"></button>
<button type=button class=cdot style="--c:var(--team-aqua)" aria-label="Aqua"></button>
<button type=button class=cdot style="--c:var(--team-cobalt)" aria-label="Blue"></button>
<button type=button class=cdot style="--c:var(--team-bubblegum)" aria-label="Bubblegum"></button>
<button type=button class=cdot style="--c:var(--team-cherry)" aria-label="Coral"></button>
</div>
<label>Sport<select name=sport id=sportSel><option{% if not dup or dup.sport == 'Water Polo' %} selected{% endif %}>Water Polo</option><option{% if dup and dup.sport == 'Swimming' %} selected{% endif %}>Swimming</option>{% if dup and dup.sport not in ('Water Polo', 'Swimming') %}<option selected>{{ dup.sport }}</option>{% endif %}</select></label>
<div class=rg-day>Display name</div>
<div class=livetitle><strong id=liveTitle>{% if dup and dup.title %}{{ dup.title }}{% else %}Water Polo Practice{% endif %}</strong><button type=button class="rg-btn ghost" id=customize>Customize</button></div>
<label id=titleField {% if not dup or not dup.title %}hidden{% endif %}>Event name<input name=title id=titleInput value="{{ dup.title if dup else '' }}" autocomplete=off><button type=button class="rg-btn ghost" id=titleReset>Reset to automatic</button></label>
</div>{% endif %}
<div id=lineBlock {% if staff and lane != 'lineup' %}hidden{% endif %}>
<label>Type{{ type_select(line_types) }}</label>
{% if staff %}<div class=typechips id=typeChips>
<button type=button data-type=Tournament class=on>Tournament</button>
<button type=button data-type=Clinic>Clinic</button>
<button type=button data-type=Trip>Trip</button>
<button type=button data-type=Social>Social</button>
</div>{% endif %}
<div class=rg-day>Who's hosting?</div>
<div class="actseg hostseg" id=whoHost role=radiogroup aria-label="Who's hosting?">
<label><input type=radio name=hosting value=Hosting checked><span>Our organization</span></label>
<label><input type=radio name=hosting value=Attending><span>Another organization</span></label>
</div>
<label class=switchrow>Co-hosted?<span class=switch><input type=checkbox name=cohosted id=coHosted value=1><span></span></span></label>
<label id=lineOrg hidden>Host organization<input name=host_org id=hostOrg autocomplete=off placeholder="West Hollywood Aquatics"></label>
<div id=lineCo hidden class=hostblock>
<div class=rg-day>Co-host organizations</div>
<div class=hostadd><input id=hostAdd autocomplete=off placeholder="Santa Monica" aria-label="Co-host organization"><button type=button class="rg-btn secondary" id=hostAddBtn>Add</button></div>
<div id=hostChips class=hostchips></div>
</div>
{% if staff %}
<div id=orgPlanLabel class=rg-day hidden>What are our organization's plans?</div>
<div class=plancards id=orgPlans hidden role=radiogroup aria-label="What are our organization's plans?">
<label class=plancard><input type=radio name=team_plan value=considering checked disabled><span class=planmark aria-hidden=true><svg width="14" height="14" viewBox="0 0 256 256" fill="currentColor"><path d="M229.66,77.66l-128,128a8,8,0,0,1-11.32,0l-56-56a8,8,0,0,1,11.32-11.32L96,188.69,218.34,66.34a8,8,0,0,1,11.32,11.32Z"/></svg></span><span class=plantxt><b>Gauging interest</b><span>See who wants to participate before committing.</span></span></label>
<label class=plancard><input type=radio name=team_plan value=committed disabled><span class=planmark aria-hidden=true><svg width="14" height="14" viewBox="0 0 256 256" fill="currentColor"><path d="M229.66,77.66l-128,128a8,8,0,0,1-11.32,0l-56-56a8,8,0,0,1,11.32-11.32L96,188.69,218.34,66.34a8,8,0,0,1,11.32,11.32Z"/></svg></span><span class=plantxt><b>We're attending</b><span>Our organization has decided to participate.</span></span></label>
</div>
{% endif %}
<label>Event name<input name=line_title id=lineTitle autocomplete=off placeholder="IGLA 2027"></label>
<label>Short description<textarea class=planfield name=description id=lineDesc rows=4 placeholder="What should people know?"></textarea></label>
</div>
<div class=rg-day>When</div>
{% if staff %}<div class=actseg id=whenPrec role=radiogroup aria-label=Dates>
<label data-prec=exact><input type=radio name=date_precision value=exact checked><span>Exact dates</span></label>
<label data-prec=recur {% if lane == 'lineup' %}hidden{% endif %}><input type=radio name=date_precision value=recur {% if lane == 'lineup' %}disabled{% endif %}><span>Recurring</span></label>
<label data-prec=month {% if lane != 'lineup' %}hidden{% endif %}><input type=radio name=date_precision value=month {% if lane != 'lineup' %}disabled{% endif %}><span>Month only</span></label>
</div>{% endif %}
<div class=list id=exactWhen>
<button type=button class="li setrow" data-matfor=dateInput><span class=grow><span id=dateLab>Date</span><span class="sum" id=dateSum> Add a date</span></span>""" + _CHEV + """</button>
<button type=button class="li setrow" data-matfor=startInput><span class=grow>Start<span class="sum" id=startSum> 7:00 PM</span></span>""" + _CHEV + """</button>
<button type=button class="li setrow" data-matfor=endInput><span class=grow>End<span class="sum" id=endSum> 8:30 PM</span></span>""" + _CHEV + """</button>
<button type=button class="li setrow" id=repeatRow data-open=sheetDays hidden aria-haspopup=dialog aria-controls=sheetDays><span class=grow><span id=daysLab>Choose days</span><span class=sum id=daysSum></span></span>""" + _CHEV + """</button>
<button type=button class="li setrow" id=freqRow data-open=sheetFreq hidden aria-haspopup=dialog aria-controls=sheetFreq><span class=grow>Frequency<span class=sum id=freqSum> Weekly</span></span>""" + _CHEV + """</button>
<button type=button class="li setrow" id=endsRow data-open=sheetEnds hidden aria-haspopup=dialog aria-controls=sheetEnds><span class=grow>Ends<span class=sum id=endsSum> Never</span></span>""" + _CHEV + """</button>
<button type=button class="li setrow" id=skipRow data-open=sheetSkips hidden aria-haspopup=dialog aria-controls=sheetSkips><span class=grow>Skip dates<span class=sum id=skipSum> None</span></span>""" + _CHEV + """</button>
</div>
<div class=list id=monthWhen hidden>
<button type=button class="li setrow" data-matfor=monthInput><span class=grow>Month<span class=sum id=monthSum> Choose a month</span></span>""" + _CHEV + """</button>
<input type=hidden name=date_part id=datePart data-monthpart value=all>
</div>
<label>Location<span id=locOk class=locok hidden><svg width="16" height="16" viewBox="0 0 256 256" fill="currentColor" aria-hidden="true"><path d="M128,24A104,104,0,1,0,232,128,104.11,104.11,0,0,0,128,24Zm45.66,85.66-56,56a8,8,0,0,1-11.32,0l-24-24a8,8,0,0,1,11.32-11.32L112,148.69l50.34-50.35a8,8,0,0,1,11.32,11.32Z"/></svg> Verified</span><input name=location id=locInput data-places value="{{ dup.location if dup else '' }}" autocomplete=off placeholder="Pool or address"></label>
<div class=rg-day>Additional settings</div>
{% if staff %}<div id=schedSets {% if lane == 'lineup' %}hidden{% endif %}>
<div class=formsec><h2>Practice details</h2><div class=list>
<button type=button class="li selfield" data-open=sheetLevels><span class=selfieldk>Skill levels</span><span class="selfieldv ell" data-for=levels>Not set</span>""" + _CHEV + """</button>
<button type=button class="li selfield" data-open=sheetDivision><span class=selfieldk>Division</span><span class="selfieldv ell" data-for=division>Not set</span>""" + _CHEV + """</button>
</div></div>
<div class=formsec><h2>Coaching</h2><div class=list>
<button type=button class="li selfield" data-open=sheetCoaches><span class=selfieldk>Coaches</span><span class="selfieldv ell" data-for=coaches>None</span>""" + _CHEV + """</button>
<button type=button class="li selfield" data-open=sheetLead><span class=selfieldk>Head coach</span><span class="selfieldv ell" data-for=lead>No head coach</span>""" + _CHEV + """</button>
</div><div id=assignedCoaches class=list></div></div>
<div class=formsec><h2>Additional details</h2><div class=list>
<button type=button class="li selfield" data-open=setSocial><span class=selfieldk>After-practice social</span><span class="selfieldv ell" id=socSum>Not added</span>""" + _CHEV + """</button>
<button type=button class="li selfield" data-open=setNotes><span class=selfieldk>Notes &amp; cover image</span><span class="selfieldv ell" id=noteSum>{% if dup and (dup.note or dup.image) %}Added{% else %}Not added{% endif %}</span>""" + _CHEV + """</button>
</div></div>
</div>{% endif %}
<div class=list id=lineSets {% if staff and lane != 'lineup' %}hidden{% endif %}>
<button type=button class="li setrow" id=regRow data-open=setReg><span class=grow>Registration<span class=sum id=regSum> Not set</span></span>""" + _CHEV + """</button>
</div>
<div id=signupBlock {% if not staff or lane != 'lineup' %}hidden{% endif %}>
<div class=rg-day>Who can sign up</div>
<p class="ty-muted ty-sm sm">For this event. Club default is set in Manage · Club.</p>
<div class=signupopts role=radiogroup aria-label="Who can sign up">
<label class=sigopt><input type=radio name=signup_scope value=anyone><span><b>Anyone</b><small>Open to people outside Grunions. They can see it on the public schedule.</small></span></label>
<label class=sigopt><input type=radio name=signup_scope value=network><span><b>Our network</b><small>Grunions plus partner clubs you've linked.</small></span></label>
<label class=sigopt><input type=radio name=signup_scope value=team checked><span><b>Team members only</b><small>Outside people can see it but can't sign up.</small></span></label>
</div>
</div>
<div class=createfoot>
<p class=pagesub id=destHint>{% if not staff %}Sent to admins for review{% elif lane == 'lineup' %}Appears on Lineup by default{% else %}Appears on Home by default{% endif %}</p>
<button class="rg-btn primary full" name=action value=preview>{% if dup %}Save{% elif not staff %}Submit{% else %}Create event{% endif %}</button>
</div>
<input class=pickhold type=date name=date id=dateInput value="{{ dup.date if dup else '' }}">
<input class=pickhold type=time name=start id=startInput value="{{ dup.start if dup else '19:00' }}">
<input class=pickhold type=time name=end id=endInput value="{{ dup.end if dup else '20:30' }}">
<input class=pickhold type=month name=month id=monthInput>
<input class=pickhold type=date name=recur_until id=untilInput>
<input class=pickhold type=date id=skipPick>
<dialog class=botsheet id=sheetDays><div class=sheet><div class=grab></div><h2>Repeats on</h2>
<div class=sheetlist>
<label class=sheetopt data-label=Mon><input type=checkbox name=weekday value=0><span><b>Monday</b></span></label>
<label class=sheetopt data-label=Tue><input type=checkbox name=weekday value=1><span><b>Tuesday</b></span></label>
<label class=sheetopt data-label=Wed><input type=checkbox name=weekday value=2><span><b>Wednesday</b></span></label>
<label class=sheetopt data-label=Thu><input type=checkbox name=weekday value=3><span><b>Thursday</b></span></label>
<label class=sheetopt data-label=Fri><input type=checkbox name=weekday value=4><span><b>Friday</b></span></label>
<label class=sheetopt data-label=Sat><input type=checkbox name=weekday value=5><span><b>Saturday</b></span></label>
<label class=sheetopt data-label=Sun><input type=checkbox name=weekday value=6><span><b>Sunday</b></span></label>
</div>
<button type=button class="rg-btn primary full" data-sheetdone>Done</button></div></dialog>
<dialog class=botsheet id=sheetFreq><div class=sheet><div class=grab></div><h2>Frequency</h2>
<div class=sheetlist>
<label class=sheetopt data-label=Weekly><input type=radio name=recur_interval value=1 checked><span><b>Weekly</b></span></label>
<label class=sheetopt data-label="Every 2 weeks"><input type=radio name=recur_interval value=2><span><b>Every 2 weeks</b></span></label>
</div>
<button type=button class="rg-btn primary full" data-sheetdone>Done</button></div></dialog>
<dialog class=botsheet id=sheetEnds><div class=sheet><div class=grab></div><h2>Ends</h2>
<div class=sheetlist>
<label class=sheetopt data-label=Never><input type=radio name=recur_end value=never checked><span><b>Never</b><small>Keeps about six months on the schedule</small></span></label>
<label class=sheetopt data-label="On a date"><input type=radio name=recur_end value=date><span><b>On a date</b></span></label>
<label class=sheetopt data-label="After"><input type=radio name=recur_end value=count><span><b>After</b></span></label>
</div>
<button type=button class="li setrow" id=endDateRow data-matfor=untilInput hidden><span class=grow>End date<span class=sum id=untilSum> Add a date</span></span>""" + _CHEV + """</button>
<label id=recurCountField hidden>Times<input type=number name=recur_count id=recurCount min=1 max=104 value=8 inputmode=numeric></label>
<button type=button class="rg-btn primary full" data-sheetdone>Done</button></div></dialog>
<dialog class=botsheet id=sheetSkips><div class=sheet><div class=grab></div><h2>Skip dates</h2>
<p class="ty-muted ty-sm sm">These dates have no practice.</p>
<button type=button class="li setrow" data-matfor=skipPick><span class=grow>Add a date</span>""" + _CHEV + """</button>
<div id=skipChips class=skipchips></div>
<input type=hidden name=skip_dates_present value=1>
<button type=button class="rg-btn primary full" data-sheetdone>Done</button></div></dialog>
<dialog class=botsheet id=sheetLevels><div class=sheet><div class=grab></div><h2>Skill levels</h2>
<div class=sheetlist data-sum=levels data-empty="Not set">
<label class=sheetopt data-label="All levels"><input type=checkbox id=allLevels {% if dup and dup.all_levels %}checked{% endif %}><span><b>All levels</b><small>Every skill level</small></span></label>
{% for pid, name, short, full in level_catalog(dup.sport if dup else 'Water Polo', (dup.levels|join(',')) if dup else '') %}<label class=sheetopt data-label="{{ name }}"><input type=checkbox name=level value="{{ pid }}" {% if dup and pid in dup.levels %}checked{% endif %}><span><b>{{ name }}</b><small>{{ short }}</small></span></label>{% endfor %}
</div>
<button type=button class="rg-btn primary full" data-sheetdone>Done</button></div></dialog>
<dialog class=botsheet id=sheetDivision><div class=sheet><div class=grab></div><h2>Division</h2>
<div class=sheetlist data-sum=division data-empty="Not set">
<label class=sheetopt data-label="Not set"><input type=radio name=division value="" {% if not dup or not dup.division %}checked{% endif %}><span><b>Not set</b></span></label>
{% for pid, name in SPORTS.DIVISIONS %}<label class=sheetopt data-label="{{ name }}"><input type=radio name=division value="{{ pid }}" {% if dup and dup.division == pid %}checked{% endif %}><span><b>{{ name }}</b></span></label>{% endfor %}
</div>
<label id=divCustom {% if not dup or dup.division != 'custom' %}hidden{% endif %}>Custom label<input name=division_custom value="{{ dup.division_custom if dup else '' }}" autocomplete=off></label>
<button type=button class="rg-btn primary full" data-sheetdone>Done</button></div></dialog>
<dialog class=botsheet id=sheetCoaches><div class=sheet><div class=grab></div><h2>Coaches</h2>
<input class=sheetsearch placeholder="Search coaches" autocomplete=off data-sheetsearch>
<div class=sheetlist data-sum=coaches data-empty=None>
{% for c in coaches %}<label class=coachrow data-search="{{ display_first(c) }} {{ c.last }}" data-label="{{ display_first(c) }} {{ c.last }}"><span class=avatar>{{ initials(c) }}</span><span class=grow><b>{{ display_first(c) }} {{ c.last }}</b></span><input type=checkbox name=coach value="{{ c.id }}"{% if dup and c.id in dup.coaches %} checked{% endif %} data-name="{{ display_first(c) }} {{ c.last }}"></label>
{% else %}<p class='ty-muted ty-sm'>No coaches on the list yet.</p>{% endfor %}
</div>
<button type=button class="rg-btn primary full" data-sheetdone>Done</button></div></dialog>
<dialog class=botsheet id=sheetLead><div class=sheet><div class=grab></div><h2>Head coach</h2>
<div class=sheetlist data-sum=lead data-empty="No head coach">
<label class=sheetopt data-lead="" data-label="No head coach"><input type=radio name=lead value="" {% if not dup or not dup.lead %}checked{% endif %}><span><b>No head coach</b></span></label>
{% for c in coaches %}<label class=sheetopt data-lead="{{ c.id }}" data-label="{{ display_first(c) }} {{ c.last }}" {% if not dup or c.id not in dup.coaches %}hidden{% endif %}><input type=radio name=lead value="{{ c.id }}" {% if dup and dup.lead == c.id %}checked{% endif %}><span><b>{{ display_first(c) }} {{ c.last }}</b></span></label>{% endfor %}
</div>
<button type=button class="rg-btn primary full" data-sheetdone>Done</button></div></dialog>
<dialog class=botsheet id=focusSheet><div class=sheet><div class=grab></div><h2 id=focusTitle>Coach</h2><div id=focusSlot></div><button type=button class="rg-btn primary full" data-sheetdone>Done</button></div></dialog>
<div id=focusHome hidden>{% for c in coaches %}<label data-coach="{{ c.id }}">Focus group<input name="focus-{{ c.id }}" data-groups="Beginners,Intermediate,Advanced,Goalies" value="{{ dup.focuses.get(c.id, '') if dup else '' }}" placeholder="Beginners, Intermediate, Advanced, Goalies" autocomplete=off></label>{% endfor %}</div>
<dialog class=botsheet id=setSocial><div class=sheet><div class=grab></div><h2>After-practice social</h2>
<div class=sheetlist data-sum=social data-empty="Not added">
{% for kind in SOCIAL_KINDS %}<label class=sheetopt data-label="{{ kind }}"><input type=radio name=social_kind value="{{ kind }}" {% if dup and dup.social_kind == kind %}checked{% endif %}><span><b>{{ kind }}</b></span></label>{% endfor %}
</div>
<label id=socialCustom {% if not dup or dup.social_kind != 'Other' %}hidden{% endif %}>Label<input name=social_custom value="{{ dup.social_custom if dup else '' }}" autocomplete=off></label>
<label>Address<span class=locok {% if not dup or not dup.social_address %}hidden{% endif %}><svg width="16" height="16" viewBox="0 0 256 256" fill="currentColor" aria-hidden="true"><path d="M128,24A104,104,0,1,0,232,128,104.11,104.11,0,0,0,128,24Zm45.66,85.66-56,56a8,8,0,0,1-11.32,0l-24-24a8,8,0,0,1,11.32-11.32L112,148.69l50.34-50.35a8,8,0,0,1,11.32,11.32Z"/></svg> Verified</span><input name=social_address id=socPlace value="{{ dup.social_address if dup else '' }}" data-places data-place-name=social_place autocomplete=off placeholder="Search for an address"></label>
<label>Place name<input name=social_place value="{{ dup.social_place if dup else '' }}" autocomplete=off placeholder="Name of the place"></label>
<label>Time (optional)<input data-native type=time name=social_time min="{{ (dup.end if dup else '20:30')[:5] }}" value="{{ (dup.social_time or dup.end) if dup else '20:30' }}"></label>
<label>Note<textarea class=planfield name=social_note rows=4>{{ dup.social_note if dup else '' }}</textarea></label>
<button type=button class="rg-btn primary full" data-sheetdone>Done</button></div></dialog>
<dialog class=botsheet id=setNotes><div class=sheet><div class=grab></div><h2>Notes &amp; media</h2>
<label>Notes<textarea class=planfield name=note id=noteInput rows=4>{{ dup.note if dup else '' }}</textarea></label>
{{ upload_field('image', src=(dup.image_src if dup else ''), clear_name=('image_clear' if dup and dup.image else '')) }}
<button type=button class="rg-btn primary full" onclick="this.closest('dialog').close()">Done</button></div></dialog>
<dialog class=botsheet id=setReg><div class=sheet><div class=grab></div><h2>Registration</h2>
<label>Format<select name=comp_format><option value="">Not set</option>{% for pid, name, blurb in SPORTS.FORMATS %}<option value="{{ pid }}">{{ name }}</option>{% endfor %}</select></label>
<label>Link<input name=link inputmode=url placeholder="https://"></label>
<label>Estimated cost<input name=cost autocomplete=off></label>
<label>Capacity<input name=capacity inputmode=numeric></label>
<label>Register by<input type=date name=reg_deadline></label>
<button type=button class="rg-btn primary full" onclick="this.closest('dialog').close()">Done</button></div></dialog>
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
  var signup=document.getElementById('signupBlock'); if(signup) signup.hidden=!staff || home;
  if(hint) hint.textContent=home?'Appears on Home by default':'Appears on Lineup by default';
  var big=document.getElementById('newEventTitle'); if(big) big.textContent=home?'New event.':'New lineup event.';
  document.querySelectorAll('button.lanecard').forEach(function(b){ b.classList.toggle('on', b.getAttribute('data-lane')===name); });
  paintTitle(); syncLine();
 }
 function dayNames(){ return ['Mon','Tue','Wed','Thu','Fri','Sat','Sun']; }
 function syncDays(){
  var picked=[].slice.call(document.querySelectorAll('#sheetDays input[name=weekday]:checked')).map(function(i){ return dayNames()[+i.value]||''; }).filter(Boolean);
  var lab=document.getElementById('daysLab'), sum=document.getElementById('daysSum');
  if(!picked.length){ if(lab) lab.textContent='Choose days'; if(sum) sum.textContent=''; }
  else { if(lab) lab.textContent='Repeats on'; if(sum) sum.textContent=' '+picked.join(', '); }
 }
 function syncFreq(){
  var on=document.querySelector('#sheetFreq input[name=recur_interval]:checked');
  var sum=document.getElementById('freqSum');
  if(sum) sum.textContent=on&&on.value==='2'?' Every 2 weeks':' Weekly';
 }
 function prettyDay(iso){
  var p=(iso||'').split('-'); if(p.length<3) return iso||'';
  var months=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];
  return months[(+p[1]||1)-1]+' '+(+p[2]);
 }
 function syncSkips(){
  var dates=[].slice.call(document.querySelectorAll('#skipChips input[name=skip_date]')).map(function(i){ return i.value; });
  var sum=document.getElementById('skipSum'); if(!sum) return;
  if(!dates.length) sum.textContent=' None';
  else if(dates.length===1) sum.textContent=' '+prettyDay(dates[0]);
  else if(dates.length===2) sum.textContent=' '+prettyDay(dates[0])+' + 1';
  else sum.textContent=' '+dates.length+' dates';
 }
 function addSkip(iso){
  if(!iso||document.querySelector('#skipChips input[name=skip_date][value="'+iso+'"]')) return;
  var chip=document.createElement('span'); chip.className='skipchip';
  var label=document.createElement('span'); label.textContent=prettyDay(iso);
  var btn=document.createElement('button'); btn.type='button'; btn.setAttribute('aria-label','Remove '+prettyDay(iso)); btn.textContent='×';
  var hidden=document.createElement('input'); hidden.type='hidden'; hidden.name='skip_date'; hidden.value=iso;
  btn.onclick=function(){ chip.remove(); syncSkips(); };
  chip.appendChild(label); chip.appendChild(btn); chip.appendChild(hidden);
  var box=document.getElementById('skipChips'); if(box) box.appendChild(chip);
  syncSkips();
 }
 function syncRecurEnd(){
  var on=document.querySelector('input[name=date_precision]:checked');
  var recurOn=!!(on && on.value==='recur' && !on.disabled);
  var end=document.querySelector('#sheetEnds input[name=recur_end]:checked');
  var mode=end?end.value:'never';
  var dateRow=document.getElementById('endDateRow'), countBox=document.getElementById('recurCountField');
  if(dateRow) dateRow.hidden=mode!=='date';
  if(countBox) countBox.hidden=mode!=='count';
  var until=document.getElementById('untilInput'); if(until) until.disabled=!recurOn || mode!=='date';
  var num=document.getElementById('recurCount'); if(num) num.disabled=!recurOn || mode!=='count';
  var sum=document.getElementById('endsSum');
  if(sum){
   if(mode==='count'){ var n=num&&num.value?num.value:''; sum.textContent=' After '+(n||'N')+(n==='1'?' time':' times'); }
   else if(mode==='date') sum.textContent=until&&until.value?(' '+until.value):' On a date';
   else sum.textContent=' Never';
  }
 }
 function syncPrec(){
  var prec=document.getElementById('whenPrec'), exact=document.getElementById('exactWhen'), month=document.getElementById('monthWhen');
  if(prec) prec.hidden=!staff;
  var home=!lane || lane.value!=='lineup';
  var allow=home?{exact:1,recur:1}:{exact:1,month:1};
  document.querySelectorAll('#whenPrec label[data-prec]').forEach(function(lab){
   var v=lab.getAttribute('data-prec');
   var show=!!(staff && allow[v]);
   lab.hidden=!show;
   var input=lab.querySelector('input');
   if(input) input.disabled=!show;
  });
  var on=document.querySelector('input[name=date_precision]:checked');
  if(staff && (!on || on.disabled || !allow[on.value])){
   var exactRadio=document.querySelector('#whenPrec input[value=exact]');
   if(exactRadio){ exactRadio.disabled=false; exactRadio.checked=true; }
   on=exactRadio;
  }
  var mode=on && !on.disabled ? on.value : 'exact';
  var monthOn=mode==='month', recurOn=mode==='recur';
  if(exact){ exact.hidden=monthOn; exact.querySelectorAll('input,select,button').forEach(function(el){ el.disabled=monthOn; }); }
  if(month){ month.hidden=!monthOn; month.querySelectorAll('input,select,button').forEach(function(el){ el.disabled=!monthOn; }); }
  ['repeatRow','freqRow','endsRow','skipRow'].forEach(function(id){ var row=document.getElementById(id); if(row){ row.hidden=!recurOn; row.disabled=monthOn; } });
  ['sheetDays','sheetFreq','sheetEnds','sheetSkips'].forEach(function(id){
   var sheet=document.getElementById(id); if(!sheet) return;
   sheet.querySelectorAll('input,select,button').forEach(function(el){ el.disabled=!recurOn; });
  });
  var monthInput=document.getElementById('monthInput'); if(monthInput) monthInput.disabled=!monthOn;
  var dateInput=document.getElementById('dateInput'); if(dateInput) dateInput.disabled=monthOn;
  ['startInput','endInput'].forEach(function(id){ var el=document.getElementById(id); if(el) el.disabled=monthOn; });
  var dateLab=document.getElementById('dateLab'); if(dateLab) dateLab.textContent=recurOn?'Starts':'Date';
  syncDays(); syncFreq(); syncSkips(); syncRecurEnd();
 }
 document.querySelectorAll('input[name=date_precision]').forEach(function(r){ r.addEventListener('change', syncPrec); });
 document.querySelectorAll('#sheetDays input[name=weekday]').forEach(function(r){ r.addEventListener('change', syncDays); });
 document.querySelectorAll('#sheetFreq input[name=recur_interval]').forEach(function(r){ r.addEventListener('change', syncFreq); });
 document.querySelectorAll('#sheetEnds input[name=recur_end]').forEach(function(r){ r.addEventListener('change', syncRecurEnd); });
 var skipPick=document.getElementById('skipPick'); if(skipPick) skipPick.addEventListener('change', function(){ addSkip(skipPick.value); skipPick.value=''; });
 var recurCount=document.getElementById('recurCount'); if(recurCount) recurCount.addEventListener('input', syncRecurEnd);
 document.querySelectorAll('button.lanecard').forEach(function(b){ b.onclick=function(){ showLane(b.getAttribute('data-lane')); syncPrec(); }; });
 document.querySelectorAll('button.cdot').forEach(function(b){ b.onclick=function(){ document.querySelectorAll('button.cdot').forEach(function(x){ x.classList.remove('on'); }); b.classList.add('on'); }; });
 document.querySelectorAll('#typeChips button').forEach(function(b){
  b.onclick=function(){
   var sel=document.getElementById('lineType'); if(!sel) return;
   var opt=[].slice.call(sel.options).some(function(o){ return o.value===b.getAttribute('data-type'); });
   if(!opt) return;
   sel.value=b.getAttribute('data-type');
   sel.dispatchEvent(new Event('change',{bubbles:true}));
   document.querySelectorAll('#typeChips button').forEach(function(x){ x.classList.toggle('on', x===b); });
  };
 });
 (function(){
  var form=document.getElementById('planForm'), raw=form&&form.getAttribute('data-practicedays');
  window.grunionsPracticeDays={};
  try{ JSON.parse(raw||'[]').forEach(function(d){ window.grunionsPracticeDays[d]=1; }); }catch(err){}
  var note=document.querySelector('main > .note');
  if(note && /date|location/i.test(note.textContent||'')){
   var dateBtn=document.querySelector('[data-matfor=dateInput]'), loc=document.getElementById('locInput'), date=document.getElementById('dateInput');
   if(dateBtn && date && !date.value) dateBtn.classList.add('bad');
   if(loc && !loc.value) loc.classList.add('bad');
  }
 })();
 syncPrec();
 document.querySelectorAll('input[name=activity_type]').forEach(function(r){ r.addEventListener('change', paintTitle); });
 var sport=document.getElementById('sportSel'); if(sport) sport.addEventListener('change', paintTitle);
 var custom=document.getElementById('customize'), reset=document.getElementById('titleReset');
 if(custom) custom.onclick=function(){ titleMode.value='custom'; titleField.hidden=false; titleInput.value=live.textContent; titleInput.focus(); };
 if(reset) reset.onclick=function(){ titleMode.value='auto'; titleField.hidden=true; titleInput.value=''; paintTitle(); };
  function clock(v){ if(!v) return ''; var p=v.split(':'); var h=parseInt(p[0],10), m=p[1]||'00'; var ap=h>=12?'PM':'AM'; h=h%12; if(!h) h=12; return h+':'+m+' '+ap; }
 function monthLabel(v){ if(!v||v.length<7) return ' Choose a month'; var names=['January','February','March','April','May','June','July','August','September','October','November','December']; var partEl=document.getElementById('datePart'); var part=partEl?partEl.value:''; var prefix=part==='early'?'Early ':(part==='mid'?'Mid ':(part==='late'?'Late ':'')); return ' '+prefix+names[(parseInt(v.slice(5,7),10)||1)-1]+' '+v.slice(0,4); }
 function syncWhen(){
  var d=document.getElementById('dateInput'), s=document.getElementById('startInput'), e=document.getElementById('endInput'), mo=document.getElementById('monthInput'), u=document.getElementById('untilInput');
  var ds=document.getElementById('dateSum'), ss=document.getElementById('startSum'), es=document.getElementById('endSum'), ms=document.getElementById('monthSum'), us=document.getElementById('untilSum');
  if(ds) ds.textContent=d&&d.value?(' '+d.value):' Add a date';
  if(ss) ss.textContent=s&&s.value?(' '+clock(s.value)):'';
  if(es) es.textContent=e&&e.value?(' '+clock(e.value)):'';
  if(ms) ms.textContent=monthLabel(mo&&mo.value);
  if(us) us.textContent=u&&u.value?(' '+u.value):' Add a date';
  syncRecurEnd();
 }
 ['dateInput','startInput','endInput','monthInput','datePart','untilInput'].forEach(function(id){ var el=document.getElementById(id); if(el) el.addEventListener('change', syncWhen); });
 syncWhen();
 function syncHost(){
  var host=document.querySelector('#whoHost input[name=hosting]:checked');
  var mode=host?host.value:'Hosting';
  var co=document.getElementById('coHosted');
  var type=document.getElementById('lineType'); var name=type?type.value:'';
  var team=name==='Tournament'||name==='Competition'||name==='Trip'||name==='Clinic';
  var org=document.getElementById('lineOrg'), cos=document.getElementById('lineCo');
  var plans=document.getElementById('orgPlans'), planLabel=document.getElementById('orgPlanLabel');
  var showOrg=mode==='Attending';
  var showCo=!!(co&&co.checked);
  if(org){ org.hidden=!showOrg; org.querySelectorAll('input').forEach(function(el){ el.disabled=!showOrg; }); }
  if(cos){ cos.hidden=!showCo; cos.querySelectorAll('input,button').forEach(function(el){ el.disabled=!showCo; }); }
  var showPlans=!!(plans&&showOrg&&team);
  if(planLabel) planLabel.hidden=!showPlans;
  if(plans){ plans.hidden=!showPlans; plans.querySelectorAll('input').forEach(function(el){ el.disabled=!showPlans; }); }
 }
 function syncLine(){
  var type=document.getElementById('lineType'); var name=type?type.value:'Social';
  var reg=document.getElementById('regRow');
  if(reg) reg.hidden=!(name==='Tournament'||name==='Competition');
  syncHost();
  var title=document.getElementById('lineTitle');
  if(title && !title.value){
    title.placeholder=name==='Trip'?'Fall team trip':(name==='Social'?'Fall Team Dinner':(name==='Tournament'?'IGLA 2027':'Event name'));
  }
  document.querySelectorAll('#typeChips button').forEach(function(b){ b.classList.toggle('on', b.getAttribute('data-type')===name); });
 }
 var lt=document.getElementById('lineType'); if(lt) lt.addEventListener('change', syncLine);
 document.querySelectorAll('#whoHost input[name=hosting]').forEach(function(r){ r.addEventListener('change', syncHost); });
 var coHosted=document.getElementById('coHosted'); if(coHosted) coHosted.addEventListener('change', syncHost);
 syncHost();
 paintTitle();
})();
</script>
""" + _PRACTICE_JS
T["lineup_edit"] = """<form id=eventForm method=post action="{{ action }}" enctype=multipart/form-data>{{ csrf_field() }}
<h1 class=newevent>{% if event_id %}{{ values.title }}.{% else %}New lineup event.{% endif %}</h1>
<input type=hidden name=mode value="{{ values.mode or mode }}">
<button type=submit name=action value=save style="position:absolute;left:-9999px;width:1px;height:1px;overflow:hidden" tabindex=-1>{{ save_label or 'Save' }}</button>
<div class=bannerpick>
<div class="ty-muted ty-sm xs">Banner image</div>
{{ upload_field('banner', src=('/lineup-image/' ~ event_id ~ '?v=' ~ banner) if banner and event_id else '', clear_name='banner_clear') }}
</div>
<label>Type{{ type_select(event_types, values.event_type) }}</label>
<div class=rg-day>Who's hosting?</div>
<div class="actseg hostseg" id=whoHost role=radiogroup aria-label="Who's hosting?">
<label><input type=radio name=hosting value=Hosting {% if values.hosting != 'Attending' %}checked{% endif %}><span>Our organization</span></label>
<label><input type=radio name=hosting value=Attending {% if values.hosting == 'Attending' %}checked{% endif %}><span>Another organization</span></label>
</div>
<label class=switchrow>Co-hosted?<span class=switch><input type=checkbox name=cohosted id=coHosted value=1 {% if values.cohosted == '1' %}checked{% endif %}><span></span></span></label>
<label id=lineOrg {% if values.hosting != 'Attending' %}hidden{% endif %}>Host organization<input name=host_org id=hostOrg value="{{ values.host_org }}" autocomplete=off placeholder="West Hollywood Aquatics" {% if values.hosting != 'Attending' %}disabled{% endif %}></label>
<div id=lineCo class=hostblock {% if values.cohosted != '1' %}hidden{% endif %}>
<div class=rg-day>Co-host organizations</div>
<div class=hostadd><input id=hostAdd autocomplete=off placeholder="Santa Monica" aria-label="Co-host organization" {% if values.cohosted != '1' %}disabled{% endif %}><button type=button class="rg-btn secondary" id=hostAddBtn {% if values.cohosted != '1' %}disabled{% endif %}>Add</button></div>
<div id=hostChips class=hostchips>{% for name in values.cohost_orgs %}<span class=skipchip><span>{{ name }}</span><button type=button aria-label="Remove {{ name }}">×</button><input type=hidden name=cohost_org value="{{ name }}" {% if values.cohosted != '1' %}disabled{% endif %}></span>{% endfor %}</div>
</div>
{% if organizer %}
<div id=orgPlanLabel class=rg-day {% if values.hosting != 'Attending' %}hidden{% endif %}>What are our organization's plans?</div>
<div class=plancards id=orgPlans {% if values.hosting != 'Attending' %}hidden{% endif %} role=radiogroup aria-label="What are our organization's plans?">
<label class=plancard><input type=radio name=team_plan value=considering {% if values.team_plan != 'committed' %}checked{% endif %} {% if values.hosting != 'Attending' %}disabled{% endif %}><span class=planmark aria-hidden=true><svg width="14" height="14" viewBox="0 0 256 256" fill="currentColor"><path d="M229.66,77.66l-128,128a8,8,0,0,1-11.32,0l-56-56a8,8,0,0,1,11.32-11.32L96,188.69,218.34,66.34a8,8,0,0,1,11.32,11.32Z"/></svg></span><span class=plantxt><b>Gauging interest</b><span>See who wants to participate before committing.</span></span></label>
<label class=plancard><input type=radio name=team_plan value=committed {% if values.team_plan == 'committed' %}checked{% endif %} {% if values.hosting != 'Attending' %}disabled{% endif %}><span class=planmark aria-hidden=true><svg width="14" height="14" viewBox="0 0 256 256" fill="currentColor"><path d="M229.66,77.66l-128,128a8,8,0,0,1-11.32,0l-56-56a8,8,0,0,1,11.32-11.32L96,188.69,218.34,66.34a8,8,0,0,1,11.32,11.32Z"/></svg></span><span class=plantxt><b>We're attending</b><span>Our organization has decided to participate.</span></span></label>
</div>
{% endif %}
<label>Event name<input name=title value="{{ values.title }}" required autocomplete=off></label>
<div class="ty-muted ty-sm xs">Dates</div>
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
<label>City<span class=locok hidden><svg width="16" height="16" viewBox="0 0 256 256" fill="currentColor" aria-hidden="true"><path d="M128,24A104,104,0,1,0,232,128,104.11,104.11,0,0,0,128,24Zm45.66,85.66-56,56a8,8,0,0,1-11.32,0l-24-24a8,8,0,0,1,11.32-11.32L112,148.69l50.34-50.35a8,8,0,0,1,11.32,11.32Z"/></svg> Verified</span><input name=city value="{{ values.city }}" data-places{% if sports_row is defined and sports_row %}{{ place_proximity(sports_row.lat, sports_row.lng) }}{% endif %} required placeholder="Toronto, Canada" autocomplete=off></label>
<label>Venue<span class=locok hidden><svg width="16" height="16" viewBox="0 0 256 256" fill="currentColor" aria-hidden="true"><path d="M128,24A104,104,0,1,0,232,128,104.11,104.11,0,0,0,128,24Zm45.66,85.66-56,56a8,8,0,0,1-11.32,0l-24-24a8,8,0,0,1,11.32-11.32L112,148.69l50.34-50.35a8,8,0,0,1,11.32,11.32Z"/></svg> Verified</span><input name=venue value="{{ values.location }}" data-places{% if sports_row is defined and sports_row %}{{ place_proximity(sports_row.lat, sports_row.lng) }}{% endif %} placeholder="Name and address, optional" autocomplete=off></label>
<label>Short description<textarea class=planfield name=description rows=4 required>{{ values.description }}</textarea></label>
<details class=moredetails><summary>More details</summary>
{{ sports_editor(sports_row, false, true) }}
<label>Link<input name=link value="{{ values.link }}" inputmode=url autocomplete=off placeholder="https://"></label>
<label>Capacity<input name=capacity inputmode=numeric value="{{ values.capacity }}" autocomplete=off></label>
<label>Estimated cost<input name=cost value="{{ values.cost }}" autocomplete=off></label>
<label>Register by<input type=date name=reg_deadline value="{{ values.reg_deadline }}"></label>
<label>Extra details<textarea class=planfield name=details rows=4>{{ values.details }}</textarea></label>
{% if me().is_admin %}<input type=hidden name=pin_present value=1><label><input type=checkbox name=featured value=1 {% if values.featured == '1' %}checked{% endif %}> Pin</label>{% endif %}
</details>
{% if organizer and not event_id %}<button class="rg-btn secondary full" name=action value=draft>Save draft</button>{% endif %}
{% if event_id %}<button class="rg-btn primary full" name=action value=save>Save event</button>{% endif %}
{% if show_cancel or show_delete %}<div class=eventacts>
{% if show_cancel %}<button class="rg-btn secondary" name=action value=cancel formnovalidate onclick="return confirm('Cancel this event?')">Cancel event</button>{% endif %}
{% if show_delete %}<button class="rg-btn secondary" name=action value=delete formnovalidate onclick="return confirm('Delete this event?')">Delete event</button>{% endif %}
</div>{% endif %}
</form>
<script>(function(){
 var org=document.getElementById('lineOrg'), cos=document.getElementById('lineCo');
 function sync(){
  var on=document.querySelector('#whoHost input[name=hosting]:checked');
  var mode=on?on.value:'Hosting';
  var co=document.getElementById('coHosted');
  var showOrg=mode==='Attending';
  var showCo=!!(co&&co.checked);
  var type=document.getElementById('lineType'); var name=type?type.value:'';
  var team=name==='Tournament'||name==='Competition'||name==='Trip'||name==='Clinic';
  if(org){ org.hidden=!showOrg; org.querySelectorAll('input').forEach(function(el){ el.disabled=!showOrg; }); }
  if(cos){ cos.hidden=!showCo; cos.querySelectorAll('input,button').forEach(function(el){ el.disabled=!showCo; }); }
  var plans=document.getElementById('orgPlans'), planLabel=document.getElementById('orgPlanLabel');
  var showPlans=showOrg&&team;
  if(planLabel) planLabel.hidden=!showPlans;
  if(plans){ plans.hidden=!showPlans; plans.querySelectorAll('input').forEach(function(el){ el.disabled=!showPlans; }); }
 }
 document.querySelectorAll('#whoHost input[name=hosting]').forEach(function(r){r.addEventListener('change', sync)});
 var coHosted=document.getElementById('coHosted'); if(coHosted) coHosted.addEventListener('change', sync);
 var lt=document.getElementById('lineType'); if(lt) lt.addEventListener('change', sync);
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
<h1 class=newevent>Add day.</h1>
<p class='ty-muted ty-sm'>One weekday and its times. Saving does not add a session.</p>
{{ sports_editor(series) }}
<div class="ty-muted ty-sm xs">Day</div>
<div class="checks daypicks" role=group aria-label="Weekdays">
{% for value, label in values.labels %}<label><input type=checkbox name=weekday value="{{ value }}" {% if value in values.weekdays %}checked{% endif %}><span>{{ label[:3] }}</span></label>{% endfor %}</div>
<div class=row><label>Start<input type=time name=start value="{{ values.start }}" required></label><label>End<input type=time name=end value="{{ values.end }}" required></label></div>
<label>Location<span class=locok hidden><svg width="16" height="16" viewBox="0 0 256 256" fill="currentColor" aria-hidden="true"><path d="M128,24A104,104,0,1,0,232,128,104.11,104.11,0,0,0,128,24Zm45.66,85.66-56,56a8,8,0,0,1-11.32,0l-24-24a8,8,0,0,1,11.32-11.32L112,148.69l50.34-50.35a8,8,0,0,1,11.32,11.32Z"/></svg> Verified</span><input name=location value="{{ values.location }}" data-places required autocomplete=off></label>
<div class=row><label>Starts<input type=date name=start_date value="{{ values.start_date }}" required></label></div>
<div class="ty-muted ty-sm xs">Ends</div>
<div class=actseg role=radiogroup aria-label="Series end">
<label><input type=radio name=recur_end value=never {% if values.end_mode == 'never' %}checked{% endif %}><span>Never</span></label>
<label><input type=radio name=recur_end value=date {% if values.end_mode == 'date' %}checked{% endif %}><span>On a date</span></label>
<label><input type=radio name=recur_end value=count {% if values.end_mode == 'count' %}checked{% endif %}><span>After</span></label>
</div>
<label id=seriesUntil {% if values.end_mode != 'date' %}hidden{% endif %}>End date<input type=date name=end_date value="{{ values.end_date }}"></label>
<label id=seriesCount {% if values.end_mode != 'count' %}hidden{% endif %}>Times<input type=number name=recur_count min=1 max=104 value="{{ values.end_count or 8 }}"></label>
<p class="ty-muted ty-sm sm">Never keeps about six months on the schedule and adds later dates as time moves forward.</p>
<div class="ty-muted ty-sm xs">Skip dates</div>
<div id=skipChips class=skipchips>{% for day in future_skips %}<span class=skipchip><span>{{ fmt_d(day) }}</span><button type=button aria-label="Remove {{ fmt_d(day) }}">×</button><input type=hidden name=skip_date value="{{ day }}"></span>{% endfor %}</div>
<label>Add a skip date<input type=date id=seriesSkipPick></label>
<input type=hidden name=skip_dates_present value=1>
<div class=checks role=group aria-label="Coaches"><div class="ty-muted ty-sm xs">Coaches</div>
<label style="margin:0 0 8px"><input type=radio name=lead value="" {% if not values.lead %}checked{% endif %}>No head coach</label>
{% for c in coach_choices %}<div style="padding:8px 0;border-top:1px solid var(--line)">
<label style="margin:0"><input type=checkbox name=coach value="{{ c.id }}" {% if c.id in values.coaches %}checked{% endif %}>{{ display_first(c) }} {{ c.last }}</label>
<label style="margin:8px 0 0"><input type=radio name=lead value="{{ c.id }}" {% if values.lead == c.id|string %}checked{% endif %}>Head coach</label>
</div>{% else %}<p class="ty-muted ty-sm sm">No coaches on the coaching list yet.</p>{% endfor %}</div>
</form>
<script>(function(){
 function ends(){
  var on=document.querySelector('#seriesForm input[name=recur_end]:checked');
  var mode=on?on.value:'never';
  var until=document.getElementById('seriesUntil'), count=document.getElementById('seriesCount');
  if(until){ until.hidden=mode!=='date'; var f=until.querySelector('input'); if(f) f.disabled=mode!=='date'; }
  if(count){ count.hidden=mode!=='count'; var n=count.querySelector('input'); if(n) n.disabled=mode!=='count'; }
 }
 document.querySelectorAll('#seriesForm input[name=recur_end]').forEach(function(r){ r.addEventListener('change', ends); });
 ends();
 var box=document.getElementById('skipChips'), pick=document.getElementById('seriesSkipPick');
 function drop(chip){ var b=chip.querySelector('button'); if(b) b.onclick=function(){ chip.remove(); }; }
 if(box) box.querySelectorAll('.skipchip').forEach(drop);
 if(pick&&box) pick.addEventListener('change', function(){
  var iso=pick.value; pick.value='';
  if(!iso||box.querySelector('input[value="'+iso+'"]')) return;
  var chip=document.createElement('span'); chip.className='skipchip';
  var label=document.createElement('span'); label.textContent=iso;
  var btn=document.createElement('button'); btn.type='button'; btn.textContent='×'; btn.setAttribute('aria-label','Remove '+iso);
  var hidden=document.createElement('input'); hidden.type='hidden'; hidden.name='skip_date'; hidden.value=iso;
  chip.appendChild(label); chip.appendChild(btn); chip.appendChild(hidden); drop(chip); box.appendChild(chip);
 });
})();</script>
{% if occurrences %}<div class=rg-day id=manage>Manage series</div>
<form method=post action="{{ action }}">{{ csrf_field() }}
<div class=list>{% for p in occurrences %}<label class="li sheetopt"><input type=checkbox name=pick value="{{ p.id }}"><span class=grow><b>{{ fmt_d(p.date) }}</b><small>{{ fmt_span(p.start, p.end) }} · {{ p.location }}{% if p.cancelled %} · Canceled{% endif %}</small></span></label>{% endfor %}</div>
<div class=row><label>Start<input type=time name=pick_start></label><label>End<input type=time name=pick_end></label></div>
<label>Location<input name=pick_location autocomplete=off placeholder="Leave blank to keep it"></label>
<label>Reason<textarea class=planfield name=reason rows=3 placeholder="Needed when canceling"></textarea></label>
<div class=row><button class="rg-btn secondary" name=action value=edit_selected>Edit selected</button><button class="rg-btn secondary" name=action value=cancel_selected>Cancel selected</button><button class="rg-btn danger" name=action value=delete_selected>Delete selected</button></div>
</form>{% endif %}
{% if skips %}<div class=rg-day>Skipped dates</div><div class=list>{% for day in skips %}<form method=post action="{{ action }}" class=li>{{ csrf_field() }}<input type=hidden name=action value=unskip><input type=hidden name=date value="{{ day }}"><span class=grow>{{ fmt_d(day) }}</span><button class="rg-btn secondary" type=submit>Undo skip</button></form>{% endfor %}</div>{% endif %}"""
T["practices"] = """<p class="ty-body sm" style="margin-top:0">Tue · Marina HS &nbsp;·&nbsp; Fri · Westminster HS &nbsp;·&nbsp; 7–8:30 PM</p>
{% for x in data %}{% set p = x.p %}<div class="card tap{% if p.cancelled %} cancelled{% endif %}" id=p{{p.id}} data-pid={{p.id}} onclick="if(event.target.closest('button,a,form,input,select,textarea,label,dialog'))return;location.href='/practices/{{p.id}}'">
<a class=cardlink href="/practices/{{p.id}}">
<div class=nxcardhead><div class="nxtitle cardtitle">{{ practice_title(p) }}</div></div>
{% set tile = practice_tile(p) %}
<div class=nxmain><div class=datetile><span class=pdate>{% if x.unseen %}<span class=badge data-seen={{p.id}}>{{ x.unseen if x.unseen < 100 else '99+' }}</span>{% endif %}</span><span class=wd>{{ tile.wd }}</span><span class=dn>{{ tile.dn }}</span><span class=mo>{{ tile.mo }}</span></div>
<div class="grow schedrows"><div class=nxrow>{{ glyph_clock() }}<span>{% if practice_is_month(p) %}{{ practice_when(p) }}{% else %}{{ fmt_span(p.start, p.end) }}{% endif %}</span></div>
<div class=nxrow>{{ glyph_pin() }}<span>{{ p.location }}</span></div>
<div class=nxrow>{{ glyph_people() }}<span>{{ practice_going_line(x.going|length, p) }}</span></div></div></div>
{% if p.cancelled %}{{ st('bad','Cancelled') }}{% if p.cancel_reason %}<div class="ty-muted ty-sm sm">{{ p.cancel_reason }}</div>{% endif %}{% endif %}
{% if p.note %}<div class=nxnote>{{p.note}}</div>{% endif %}
{% if p.coach_note %}<div class=nxnote>{{ p.coach_note }} · {{ p.coach_note_by }} · {{ fmt_stamp(p.coach_note_at) }}</div>{% endif %}</a>
{% if not p.cancelled %}<form method=post action=/practices class=pills>{{csrf_field()}}<input type=hidden name=pid value={{p.id}}>{{ rsvp_base('p' ~ p.id) }}
{{ rsvp_btn('Going', x.mine == 1, 'going') }}
{{ rsvp_btn('Not going', x.mine == 0, 'notgoing') }}</form>
{% endif %}</div>{% endfor %}
""" + _PRACTICE_JS

T["practice"] = """{% set p = x.p %}
{{ event_hero('practiceMap', pins if not p.image else [], ('/practice-image/' ~ p.id ~ '?v=' ~ p.image) if p.image else '', p.location or 'Practice', social_route_points(p)) }}
{% if not editing %}<div class=profilehero>
<div class="profilename{% if p.cancelled %} cancelled{% endif %}">{{ practice_title(p) }}</div>
{% if practice_sports_line(p) %}<p class="ty-muted ty-sm sm sportline">{{ practice_sports_line(p) }}</p>{% endif %}
{% if p.activity_type == 'hybrid' %}{% for seg in SPORTS.parse_segments(p.segments) %}<p class="ty-muted ty-sm sm">{{ SPORTS.ACTIVITY_NAME.get(seg.type, seg.type) }} · {{ fmt_span(seg.start, seg.end) }}</p>{% endfor %}{% endif %}
{% if p.opponent and p.activity_type == 'game' %}<p class=pracemeta>{% if p.home_away == 'home' %}Home{% elif p.home_away == 'away' %}Away{% endif %}{% if p.home_away %} · {% endif %}vs. {{ p.opponent }}</p>{% endif %}
<p class=pracemeta>{% if practice_is_month(p) %}{{ practice_when(p) }}{% else %}{{ fmt_card_date(p.date) }} · {{ fmt_clock(p.start) }} – {{ fmt_clock(p.end) }}{% endif %}</p>
{% if p.location %}<p class=pracemeta>{{ p.location }}</p>{% endif %}
<div class=pracestatus>{% if p.cancelled %}{{ st('bad','Cancelled') }}{% else %}{{ st('ok','Scheduled') }}{% endif %}</div>
{% if p.cancelled and p.cancel_reason %}<p class="ty-muted ty-sm sm" style="margin:6px 0 0">{{ p.cancel_reason }}</p>{% endif %}
{% if me().is_admin and p.cancelled and not editing and p.skipped %}<div class=eventacts><form method=post action="/practices/{{ p.id }}">{{ csrf_field() }}<input type=hidden name=pid value={{ p.id }}><input type=hidden name=back value=page><button class="rg-btn secondary" name=action value=unskip>Undo skip</button></form>{% if not practice_ended(p) %}<button type=button class="rg-btn secondary" data-open="delete{{ p.id }}">Delete event</button>{% endif %}</div>
{% elif me().is_admin and p.cancelled and not editing %}<div class=eventacts><form method=post action="/practices/{{ p.id }}">{{ csrf_field() }}<input type=hidden name=pid value={{ p.id }}><input type=hidden name=back value=page><button class="rg-btn secondary" name=action value=restore>Undo cancel</button></form>{% if not practice_ended(p) %}<button type=button class="rg-btn secondary" data-open="delete{{ p.id }}">Delete event</button>{% endif %}</div>{% endif %}
{% if me().is_admin and p.series_id and not p.cancelled %}<div style="display:flex;gap:10px;margin-top:12px"><form method=post action="/practices/{{ p.id }}">{{ csrf_field() }}<input type=hidden name=pid value={{ p.id }}><input type=hidden name=back value=page><button class="rg-btn secondary" name=action value=skip onclick="return confirm('Skip this date?')">Skip this date</button></form><a class="rg-btn secondary" href="/practices/series/{{ p.series_id }}">Edit series</a><a class="rg-btn secondary" href="/practices/series/{{ p.series_id }}#manage">Manage series</a></div>{% endif %}
<div class="stats trio">
<div class=stattile><b>{{ x.going|length }}</b><span>Going</span></div>
<div class=stattile><b>{{ x.coaches|length }}</b><span>Coaches</span></div>
<div class=stattile><b>{{ x.checked|length }}</b><span>Checked in</span></div>
</div>
</div>{% endif %}
{% if p.skill_levels %}<details class=card><summary>Skill levels</summary><div class=body>{% for row in level_catalog(p.sport, p.skill_levels) %}{% if row[0] in p.skill_levels.split(',') %}<p><b>{{ row[1] }}</b> {{ row[2] }}</p>{% endif %}{% endfor %}</div></details>{% endif %}
{% if editing %}
<div class=p5>
<div class="p5hero{% if p.cancelled %} off{% endif %}">
<div class=p5over>{{ (p.sport or 'Water Polo')|upper }} · {{ weekday_name(p.date)[:3]|upper }} · {{ month_abbr(p.date)|upper }} {{ day_num(p.date) }}</div>
<span class="p5chip{% if p.cancelled %} bad{% endif %}">{% if p.cancelled %}Cancelled{% else %}Scheduled{% endif %}</span>
<h2>{% if p.activity_type == 'game' %}Game{% elif p.activity_type == 'scrimmage' %}Scrimmage{% else %}Practice{% endif %}</h2>
{% set clk = fmt_clock(p.start).split(' ') %}
<div class=p5time><b>{{ clk[0] }}</b><span><i>{{ clk[1] if clk|length > 1 else '' }}</i><i>TO {{ fmt_clock(p.end) }}</i></span></div>
{% if p.location %}<div class=p5venue>{{ p.location }}</div>{% endif %}
</div>
<div class=p5metrics>
{{ r2_metric('%02d'|format(x.going|length), 'GOING', 'lime') }}
{{ r2_metric('%02d'|format(x.coaches|length), 'COACHES') }}
{{ r2_metric('%02d'|format(x.checked|length), 'CHECKED IN') }}
</div>
</div>
<form id=practiceForm method=post action="/practices/{{ p.id }}" class="card editorform" style="margin-top:16px" data-editorform enctype=multipart/form-data>{{ csrf_field() }}<input type=hidden name=pid value={{ p.id }}><input type=hidden name=back value=page>
<div class=formsec><h2>Practice details</h2>
{{ sports_editor(p) }}
</div>
<div class=formsec><h2>Schedule &amp; location</h2>
<label>Date<input type=date name=date value="{{ p.date }}" required></label>
{% if p.series_id %}<div class=checks role=radiogroup aria-label="Apply changes to"><div class="ty-muted ty-sm xs">Recurrence</div>
<label><input type=radio name=series_scope value=once checked> This event</label>
<label><input type=radio name=series_scope value=following> This and following</label>
<label><input type=radio name=series_scope value=all> All events</label>
</div>{% endif %}
<div class=row><label>Start<input type=time name=start value="{{ p.start }}" required></label><label>End<input type=time name=end value="{{ p.end }}" required></label></div>
<label>Venue<span class=locok hidden><svg width="16" height="16" viewBox="0 0 256 256" fill="currentColor" aria-hidden="true"><path d="M128,24A104,104,0,1,0,232,128,104.11,104.11,0,0,0,128,24Zm45.66,85.66-56,56a8,8,0,0,1-11.32,0l-24-24a8,8,0,0,1,11.32-11.32L112,148.69l50.34-50.35a8,8,0,0,1,11.32,11.32Z"/></svg> Verified</span><input name=location value="{{ p.location or '' }}" data-places{{ place_proximity(p.lat, p.lng) }} required autocomplete=off placeholder="Pool or address"></label>
</div>
<div class=formsec><h2>Coaching</h2>
<div class=list>
<button type=button class="li selfield" data-open=sheetCoaches><span class=selfieldk>Coaches</span><span class="selfieldv ell" data-for=coaches>None</span>""" + _CHEV + """</button>
<button type=button class="li selfield" data-open=sheetLead><span class=selfieldk>Head coach</span><span class="selfieldv ell" data-for=lead>No head coach</span>""" + _CHEV + """</button>
</div>
<div id=assignedCoaches class=list></div>
<dialog class=botsheet id=sheetCoaches><div class=sheet><div class=grab></div><h2>Coaches</h2>
<input class=sheetsearch name=coachq placeholder="Search coaches" autocomplete=off data-sheetsearch>
<div class=sheetlist data-sum=coaches data-empty=None>
{% for c in coach_choices %}<label class=coachrow data-search="{{ display_first(c) }} {{ c.last }}" data-label="{{ display_first(c) }} {{ c.last }}"><span class=avatar>{{ initials(c) }}</span><span class=grow><b>{{ display_first(c) }} {{ c.last }}</b> {{ coach_tag(c) }}</span><input type=checkbox name=coach value="{{ c.id }}" data-name="{{ display_first(c) }} {{ c.last }}" {% if c.id in x.coach_ids %}checked{% endif %}></label>
{% else %}<p class="ty-muted ty-sm sm">No coaches yet. Add someone on People.</p>{% endfor %}
</div>
<button type=button class="rg-btn primary full" data-sheetdone>Done</button></div></dialog>
<dialog class=botsheet id=sheetLead><div class=sheet><div class=grab></div><h2>Head coach</h2>
<div class=sheetlist data-sum=lead data-empty="No head coach">
<label class=sheetopt data-lead="" data-label="No head coach"><input type=radio name=lead value="" {% if not x.lead_id %}checked{% endif %}><span><b>No head coach</b></span></label>
{% for c in coach_choices %}<label class=sheetopt data-lead="{{ c.id }}" data-label="{{ display_first(c) }} {{ c.last }}" {% if c.id not in x.coach_ids %}hidden{% endif %}><input type=radio name=lead value="{{ c.id }}" {% if c.id == x.lead_id %}checked{% endif %}><span><b>{{ display_first(c) }} {{ c.last }}</b></span></label>{% endfor %}
</div>
<button type=button class="rg-btn primary full" data-sheetdone>Done</button></div></dialog>
<dialog class=botsheet id=focusSheet><div class=sheet><div class=grab></div><h2 id=focusTitle>Coach</h2><div id=focusSlot></div><button type=button class="rg-btn primary full" data-sheetdone>Done</button></div></dialog>
<div id=focusHome hidden>{% for c in coach_choices %}<label data-coach="{{ c.id }}">Focus group<input name="focus-{{ c.id }}" data-groups="Beginners,Intermediate,Advanced,Goalies" value="{{ x.focuses.get(c.id, '') }}" placeholder="Beginners, Intermediate, Advanced, Goalies" autocomplete=off></label>{% endfor %}</div>
<label>Practice plan<textarea class=planfield name=coaching_plan rows=4>{{ p.coaching_plan or '' }}</textarea></label>
</div>
<div class=formsec><h2>Additional details</h2>
<label>Notes<textarea class=planfield name=note rows=4>{{ p.note or '' }}</textarea></label>
{{ message_fields(p) }}
<details class=optsec {% if p.image %}open{% endif %}><summary class="li selfield"><span class=selfieldk>Cover image</span><span class=selfieldv>{% if p.image %}Added{% else %}Not added{% endif %}</span></summary>
{{ upload_field('image', src=('/practice-image/' ~ p.id ~ '?v=' ~ p.image) if p.image else '', clear_name='image_clear') }}
</details>
{% set ns = namespace(kind='', custom='') %}
{% for kind in SOCIAL_KINDS %}{% if not ns.kind and kind in (p.social_kind or '').split(',') %}{% set ns.kind = kind %}{% endif %}{% endfor %}
{% if p.social_kind and not ns.kind %}{% set ns.kind = 'Other' %}{% set ns.custom = p.social_kind %}{% endif %}
<button type=button class="li selfield" id=socialToggle><span class=selfieldk>After-practice social</span><span class="selfieldv ell" id=socialSum>{% if ns.kind %}{{ ns.custom or ns.kind }}{% else %}Not added{% endif %}</span>""" + _CHEV + """</button>
<div id=socialBody {% if not ns.kind %}hidden{% endif %}>
<button type=button class="li selfield" data-open=sheetSocial><span class=selfieldk>Social type</span><span class="selfieldv ell" data-for=social>{{ ns.custom or ns.kind or 'Not set' }}</span>""" + _CHEV + """</button>
<dialog class=botsheet id=sheetSocial><div class=sheet><div class=grab></div><h2>Social type</h2>
<div class=sheetlist data-sum=social data-empty="Not set">
{% for kind in SOCIAL_KINDS %}<label class=sheetopt data-label="{{ kind }}"><input type=radio name=social_kind value="{{ kind }}" {% if ns.kind == kind %}checked{% endif %}><span><b>{{ kind }}</b></span></label>{% endfor %}
</div>
<label id=socialCustom {% if ns.kind != 'Other' %}hidden{% endif %}>Label<input name=social_custom value="{{ ns.custom }}" autocomplete=off></label>
<button type=button class="rg-btn primary full" data-sheetdone>Done</button></div></dialog>
<label>Address<span class=locok {% if not p.social_address %}hidden{% endif %}><svg width="16" height="16" viewBox="0 0 256 256" fill="currentColor" aria-hidden="true"><path d="M128,24A104,104,0,1,0,232,128,104.11,104.11,0,0,0,128,24Zm45.66,85.66-56,56a8,8,0,0,1-11.32,0l-24-24a8,8,0,0,1,11.32-11.32L112,148.69l50.34-50.35a8,8,0,0,1,11.32,11.32Z"/></svg> Verified</span><input name=social_address value="{{ p.social_address or '' }}" data-places data-place-name=social_place{{ place_proximity(p.lat, p.lng) }} autocomplete=off placeholder="Search for an address"></label>
<label>Place name<input name=social_place value="{{ p.social_place or '' }}" autocomplete=off placeholder="Name of the place"></label>
<label>Time (optional)<input data-native type=time name=social_time min="{{ (p.end or '20:30')[:5] }}" value="{{ p.social_time or (p.end or '20:30')[:5] }}"></label>
<label>Notes (optional)<textarea class=planfield name=social_note rows=4>{{ p.social_note or '' }}</textarea></label>
<button type=button class="rg-btn danger full" id=socialRemove>Remove social</button>
<input type=hidden name=social_kind value="" id=socialClear {% if ns.kind %}disabled{% endif %}>
</div>
</div>
<input type=hidden name=plan_fields value=1>
</form>
{% if me().is_admin %}<div class=rg-day>Manage</div><div class=list>
<button type=button class="li rowbtn" data-open="assign{{ p.id }}">Assign coaches</button>
<a class="li rowbtn" href="/admin?date={{ p.date }}">Check in</a>
{% if p.cancelled %}<form method=post action="/practices/{{ p.id }}">{{ csrf_field() }}<input type=hidden name=pid value={{ p.id }}><input type=hidden name=back value=page><button class="li rowbtn" name=action value=restore>Undo cancel</button></form>
{% endif %}
<a class="li rowbtn" href="/events/new?lane=schedule&amp;copy={{ p.id }}">Duplicate practice</a>
<button type=button class="li rowbtn" data-copy="{{ app_base() }}/practices/{{ p.id }}">Copy link</button>
</div>
{% if not practice_ended(p) %}<div class=eventacts>
{% if not p.cancelled %}<button type=button class="rg-btn secondary btn-tangerine full" data-open="cancel{{ p.id }}">Cancel this practice</button>{% endif %}
<button type=button class="rg-btn secondary" data-open="delete{{ p.id }}">Delete event</button>
</div>{% endif %}
{% endif %}
{% else %}
<div class=p5>
{% if p.image %}{{ r2_cover('/practice-image/' ~ p.id ~ '?v=' ~ p.image) }}{% endif %}
<div class="p5hero{% if p.cancelled %} off{% endif %}">
<div class=p5over>{{ (p.sport or 'Water Polo')|upper }} · {{ weekday_name(p.date)[:3]|upper }} · {{ month_abbr(p.date)|upper }} {{ day_num(p.date) }}</div>
<span class="p5chip{% if p.cancelled %} bad{% endif %}">{% if p.cancelled %}Cancelled{% else %}Scheduled{% endif %}</span>
<h2>{% if p.activity_type == 'game' %}Game{% elif p.activity_type == 'scrimmage' %}Scrimmage{% else %}Practice{% endif %}</h2>
{% set clk = fmt_clock(p.start).split(' ') %}
<div class=p5time><b>{{ clk[0] }}</b><span><i>{{ clk[1] }}</i><i>TO {{ fmt_clock(p.end) }}</i></span></div>
{% if p.location %}<div class=p5venue>{{ p.location }}</div>{% endif %}
{% if p.cancelled and p.cancel_reason %}<p>{{ p.cancel_reason }}</p>{% endif %}
</div>
<div class=p5metrics>
{{ r2_metric('%02d'|format(x.going|length), 'GOING', 'lime') }}
{{ r2_metric('%02d'|format(x.coaches|length), 'COACHES') }}
{{ r2_metric('%02d'|format(x.checked|length), 'CHECKED IN') }}
</div>
{% if not p.cancelled %}<form method=post action="/practices/{{ p.id }}" class="pills p5rsvp">{{ csrf_field() }}<input type=hidden name=pid value={{ p.id }}><input type=hidden name=back value=page>{{ rsvp_base('p' ~ p.id) }}
{{ rsvp_btn('Going', x.mine == 1, 'going') }}
{{ rsvp_btn('Not going', x.mine == 0, 'notgoing') }}</form>
{{ r2_practice_actions('/chat?c=practice:' ~ p.id ~ ('&peek=1' if x.mine != 1 else ''), 'Practice Chat', x.going|length) }}
{% endif %}
{% for card in social_cards %}{{ r2_social_card(card, 'row') }}{% endfor %}
{{ r2_section("Who's going") }}
<div class=p5people>{% for r in x.going %}{{ r2_list_row(display_first(r) ~ ' ' ~ r.last, 'Player', initials(r), 'Going') }}{% else %}<p class=p5empty>No one yet.</p>{% endfor %}</div>
{{ r2_section("Can't make it") }}
<div class=p5people>{% for r in x.notgoing %}{{ r2_list_row(display_first(r) ~ ' ' ~ r.last, '', initials(r), 'Out') }}{% else %}<p class=p5empty>No one yet.</p>{% endfor %}</div>
{{ r2_section('Details') }}
{{ r2_info('DETAILS', p.note if p.note else 'No notes yet.') }}
{% if not social_cards %}{{ r2_info('AFTER-PRACTICE SOCIAL', 'None yet.') }}{% endif %}
{{ r2_info('COACHES', x.coaches|map(attribute='first')|join(', ') if x.coaches else 'No coaches assigned.') }}
<div class=heldsocial hidden><div class=rg-day>After-practice social</div>
<div class=list><div class=li>{% if social_line(p) %}{{ social_icon() }}{% endif %}<div class=grow>
{% if social_line(p) %}<div>{{ social_line(p) }}{% if p.social_time %} · {{ fmt_t(p.social_time) }}{% endif %}</div>
<div class="ty-muted ty-sm sm">{{ x.social_n }} joining</div>
{% if p.social_note %}<div class="ty-body sm" style="white-space:pre-wrap">{{ p.social_note }}</div>{% endif %}
{% else %}<span class='ty-muted ty-sm'>None yet.</span>{% endif %}
</div>{% if me().is_admin or is_staff() %}<button type=button class="rg-btn secondary" data-open="social{{ p.id }}">{{ 'Edit' if social_line(p) else 'Add' }}</button>{% endif %}</div></div></div>
<div class=rg-day>Coaches</div>
<div class=list>
{% if plan_editing %}<form id=practiceForm method=post action="/practices/{{ p.id }}">{{ csrf_field() }}<input type=hidden name=pid value={{ p.id }}><input type=hidden name=back value=page><input type=hidden name=plan_fields value=1>
<div class=li><span class="chip-info" style="margin:0">Coaches only</span></div>
<div class=li><label class=prefedit style="width:100%;margin:0">Practice plan<textarea class=planfield name=coaching_plan rows=4>{{ p.coaching_plan or '' }}</textarea></label></div>
{% if x.coaches %}<div class=li><label style="margin:0"><input type=radio name=lead value="" {% if not x.lead_id %}checked{% endif %}>No head coach</label></div>{% endif %}
{% for c in x.coaches %}<div class=li><div class=grow>
<label style="margin:0"><input type=radio name=lead value="{{ c.id }}" {% if c.is_lead %}checked{% endif %}>{{ display_first(c) }} {{ c.last }}</label>
<label style="margin:8px 0 0">Plan<input name="focus-{{ c.id }}" data-groups="Beginners,Intermediate,Advanced,Goalies" value="{{ c.focus or '' }}" placeholder="Beginners, Intermediate, Advanced, Goalies" autocomplete=off></label>
</div></div>{% endfor %}
</form>
{% else %}
{% for c in x.coaches %}{% set editable = can_host_practice() and (me().is_admin or c.id == me().id) %}<div class="li personrow">{% if editable %}<button type=button class="coachopen coachbody" data-open="cfocus{{ p.id }}-{{ c.id }}">{% else %}<div class="grow coachbody">{% endif %}<span class=coachline>{% if can_host_practice() %}{{ person_mark(c) }}{% endif %}<span class=ell>{{ display_first(c) }} {{ c.last }}</span>{% if c.is_lead %}<span class="chip-info" style="margin:0">Head coach</span>{% endif %}</span>{% if can_host_practice() and c.focus %}<span class="ty-muted ty-sm sm coachplan">{{ c.focus }}</span>{% endif %}{% if editable %}</button>{% else %}</div>{% endif %}</div>{% else %}<div class=li><span class="ty-muted ty-sm grow">No coaches assigned.</span>{% if me().is_admin %}<button type=button class="rg-btn secondary" data-open="assign{{ p.id }}">Add</button>{% endif %}</div>{% endfor %}
{% if can_host_practice() %}<div class="li planrow"><div class=planline><span class=planlabel>Practice plan</span><span class="chip-info" style="margin:0">Coaches only</span></div><button type=button class="rg-btn secondary" data-open="plan{{ p.id }}">{{ 'Edit' if p.coaching_plan else 'Add' }}</button>{% if p.coaching_plan %}<div class="ty-muted ty-sm sm plantext">{{ p.coaching_plan }}</div>{% endif %}</div>{% endif %}
{% endif %}
</div>
{{ whos_going(x.going) }}
<div class=rg-day>Can't make it</div>
<div class=list>{% for r in x.notgoing %}<div class=li><div class=grow>{{ display_first(r) }} {{ r.last }}</div></div>{% else %}<div class=li><span class='ty-muted ty-sm'>No one yet.</span></div>{% endfor %}</div>
{% set check_href = '/admin?date=' ~ p.date ~ '&ev=p-' ~ p.id ~ '#ev-p-' ~ p.id %}
{% if can_host_practice() and x.checked %}<div class="sechead checkhead"><span class=rg-day>Checked in</span><a class="rg-btn secondary" href="{{ check_href }}">Check in</a></div>
{% else %}<div class=rg-day>Checked in</div>{% endif %}
<div class=list>{% for r in x.checked %}<div class=li><div class=grow>{{ display_first(r) }} {{ r.last }}</div></div>{% else %}<div class=li><span class="ty-muted ty-sm grow">No one yet.</span>{% if can_host_practice() %}<a class="rg-btn secondary" href="{{ check_href }}">Check in</a>{% endif %}</div>{% endfor %}</div>
{% if p.location %}{% set dest = (pins[0].lat|string ~ ',' ~ pins[0].lng|string) if pins else (p.address or p.location) %}{% set soc = namespace(name='', sub='', href='', dest='') %}{% if social_line(p) %}{% set soc.name = (p.social_place or '')|trim %}{% set _saddr = (p.social_address or '')|trim %}{% if _saddr and not (_saddr.lower().startswith('http://') or _saddr.lower().startswith('https://')) %}{% set soc.sub = _saddr %}{% endif %}{% set _spin = namespace(lat=none, lng=none) %}{% for pin in pins %}{% if pin.kind == 'social' %}{% set _spin.lat = pin.lat %}{% set _spin.lng = pin.lng %}{% endif %}{% endfor %}{% if _saddr.lower().startswith('http://') or _saddr.lower().startswith('https://') %}{% set soc.href = _saddr %}{% elif _spin.lat is not none %}{% set soc.dest = _spin.lat|string ~ ',' ~ _spin.lng|string %}{% set soc.href = 'https://www.google.com/maps/dir/?api=1&destination=' ~ (soc.dest|urlencode) %}{% else %}{% set soc.href = 'https://www.google.com/maps/dir/?api=1&destination=' ~ ((soc.sub or soc.name)|urlencode) %}{% endif %}{% endif %}{{ r2_section('Getting there') }}{{ event_location('practiceLoc', pins, p.location, p.address or '', 'https://www.google.com/maps/dir/?api=1&destination=' ~ (dest|urlencode), social_route_points(p), p.social_drive_min if pins|selectattr('kind','equalto','social')|list else none, soc.name, soc.sub, soc.href, soc.dest) }}{% endif %}
</div>
{% endif %}
{% if me().is_admin or is_staff() %}{{ practice_extra_dialogs(p, 'page') }}
<dialog class=modal id=plan{{ p.id }}><div class=sheet><h2 style="margin:0 0 12px">Practice plan</h2>
<form method=post action="/practices/{{ p.id }}">{{ csrf_field() }}<input type=hidden name=pid value={{ p.id }}><input type=hidden name=back value=page>
<textarea class=planfield name=coaching_plan rows=4 aria-label="Practice plan">{{ p.coaching_plan or '' }}</textarea>
<button class="rg-btn primary full" name=action value=plan>Save</button></form></div></dialog>
{% for c in x.coaches %}{% if me().is_admin or c.id == me().id %}<dialog class=modal id="cfocus{{ p.id }}-{{ c.id }}"><div class=sheet><h2 style="margin:0 0 12px">{{ display_first(c) }} {{ c.last }}</h2>
<form method=post action="/practices/{{ p.id }}">{{ csrf_field() }}<input type=hidden name=pid value={{ p.id }}><input type=hidden name=back value=page><input type=hidden name=coach_id value="{{ c.id }}">
<label class=switchrow>Head coach<span class=switch><input type=checkbox name=head_coach value=1 {% if c.is_lead %}checked{% endif %}><span></span></span></label>
<label>Groups<input name=focus data-groups="Beginners,Intermediate,Advanced,Goalies" value="{{ c.focus or '' }}" placeholder="Beginners, Intermediate, Advanced, Goalies" autocomplete=off></label>
<label>Plan details<textarea class=planfield name=plan_note rows=4>{{ c.plan_note or '' }}</textarea></label>
<button class="rg-btn primary full" name=action value=coach_plan>Save</button></form></div></dialog>{% endif %}{% endfor %}
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
{% else %}<p class="ty-muted ty-sm sm">No coaches yet. Add someone on People.</p>{% endfor %}</div>
<div class=row><button class="rg-btn primary" name=action value=assign>Save</button><button type=button class="rg-btn secondary" onclick="this.closest('dialog').close()">Cancel</button></div></form></div></dialog>
{% if not practice_ended(p) %}
<dialog class=modal id=cancel{{ p.id }}><div class=sheet><h2 style="margin:0 0 8px">Send cancellation</h2>
<p class="ty-body sm">Members get an email and a push that include this reason.</p>
<form method=post action="/practices/{{ p.id }}">{{ csrf_field() }}<input type=hidden name=pid value={{ p.id }}><input type=hidden name=back value=page>
{% if p.series_id %}<div class=checks role=radiogroup aria-label="Cancel">
<label><input type=radio name=series_scope value=once checked> This event</label>
<label><input type=radio name=series_scope value=following> This and following</label>
<label><input type=radio name=series_scope value=all> All events</label>
</div>{% endif %}
<label>Reason<textarea class=planfield name=reason rows=4 required></textarea></label>
<button class="rg-btn danger full" name=action value=cancel>Confirm</button></form></div></dialog>
<dialog class=modal id=delete{{ p.id }}><div class=sheet><h2 style="margin:0 0 8px">Delete this practice?</h2>
<p class="ty-body sm">{% if practice_is_month(p) %}{{ practice_when(p) }} at {{ p.location }}.{% else %}{{ fmt_d(p.date) }}, {{ fmt_t(p.start) }}–{{ fmt_t(p.end) }} at {{ p.location }}.{% endif %}</p>
<form method=post action="/practices/{{ p.id }}">{{ csrf_field() }}<input type=hidden name=pid value={{ p.id }}>
{% if p.series_id %}<div class=checks role=radiogroup aria-label="Delete">
<label><input type=radio name=series_scope value=once checked> This event</label>
<label><input type=radio name=series_scope value=following> This and following</label>
<label><input type=radio name=series_scope value=all> All events</label>
</div>{% endif %}
<div class=row><button class="rg-btn danger" name=action value=delete>Delete practice</button><button type=button class="rg-btn secondary" onclick="this.closest('dialog').close()">Cancel</button></div></form></div></dialog>
{% endif %}
{% endif %}""" + _PRACTICE_JS

_CHEV_L = '<svg width="20" height="20" viewBox="0 0 256 256" fill="currentColor" aria-hidden="true"><path d="M165.66,202.34a8,8,0,0,1-11.32,11.32l-80-80a8,8,0,0,1,0-11.32l80-80a8,8,0,0,1,11.32,11.32L91.31,128Z"/></svg>'
_CHEV_R = '<svg width="20" height="20" viewBox="0 0 256 256" fill="currentColor" aria-hidden="true"><path d="M181.66,133.66l-80,80a8,8,0,0,1-11.32-11.32L164.69,128,90.34,53.66a8,8,0,0,1,11.32-11.32l80,80A8,8,0,0,1,181.66,133.66Z"/></svg>'
_CAL_I = '<svg width="20" height="20" viewBox="0 0 256 256" fill="currentColor" aria-hidden="true"><path d="M208,32H184V24a8,8,0,0,0-16,0v8H88V24a8,8,0,0,0-16,0v8H48A16,16,0,0,0,32,48V208a16,16,0,0,0,16,16H208a16,16,0,0,0,16-16V48A16,16,0,0,0,208,32ZM72,48v8a8,8,0,0,0,16,0V48h80v8a8,8,0,0,0,16,0V48h24V80H48V48ZM208,208H48V96H208V208Z"/></svg>'
T["admin"] = ADMIN_NAV + """{{ admin_page('Check-in') }}
{%- set qbit -%}{% if q %}&amp;q={{ q|urlencode }}{% endif %}{%- endset -%}
{%- set fbit -%}{% if filt != 'going' %}&amp;filt={{ filt }}{% endif %}{%- endset -%}
<div class=checkbar>
<div class=calpick id=calPick data-seg data-date="{{date}}" data-today="{{ today }}" data-q="{{q}}" data-filt="{{ '' if filt=='going' else filt }}" data-dates='{{ days|tojson }}' data-events='{{ catalog|tojson }}'>
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
<div class=list id=calEventList data-seg></div>
</div>
<div class=matactions>
<button type=button class=mattext id=calCancel>Cancel</button>
<button type=button class=mattext id=calOk>OK</button>
</div>
</div></dialog>
<dialog class=modal id=evPick><div class=sheet><h2 style="margin:0 0 12px">Events</h2><div class=list id=evPickList data-seg>{% for ev in events %}<a class=li href="/admin?date={{ date }}&amp;ev={{ ev.key }}{{ fbit }}{{ qbit }}" style="color:inherit;text-decoration:none"><span class=grow><span class=ell style="display:block;font-weight:650">{{ ev.title }}</span><span class="ty-muted ty-sm sm">{{ ev.when }}</span></span></a>{% endfor %}</div><button type=button class="rg-btn secondary full" onclick="this.closest('dialog').close()">Cancel</button></div></dialog>
</div>
{% if sel %}<div id="ev-{{ sel.key }}" class="evpin{% if ev_pinned %} on{% endif %}">{{ rg_checkin_hero(n, going|length, sel.title, sel.when ~ (' · ' ~ sel.place if sel.place else ''), sel.tone or 'sun', sel.detail) }}</div>{% else %}<p class=emptyfind>No events on this day</p>{% endif %}
{%- set ebit -%}{% if evkey %}&ev={{ evkey }}{% endif %}{%- endset -%}
{%- set qq -%}{% if q %}&q={{ q|urlencode }}{% endif %}{%- endset -%}
{{ rg_filters([('going', 'Going ' ~ going|length, '/admin?date=' ~ date ~ qq ~ ebit), ('not', 'Not going ' ~ n_not, '/admin?date=' ~ date ~ '&filt=not' ~ qq ~ ebit), ('in', 'Checked in ' ~ n, '/admin?date=' ~ date ~ '&filt=in' ~ qq ~ ebit)], filt) }}
<form class="playersearch rg-cisearch" method=get action=/admin><input type=hidden name=date value="{{ date }}">{% if filt != 'going' %}<input type=hidden name=filt value="{{ filt }}">{% endif %}{% if evkey %}<input type=hidden name=ev value="{{ evkey }}">{% endif %}<label class=rg-search>{{ rg_icon('search') }}<input name=q type=search value="{{ q }}" placeholder="Search players" enterkeyhint=search autocomplete=off></label></form>
{% macro ci(r) -%}
{%- set info = checkin_info(r, pr.id if pr else None) -%}
{%- set fields -%}{{csrf_field()}}<input type=hidden name=member_id value={{r.id}}><input type=hidden name=date value={{date}}><input type=hidden name=q value="{{q}}"><input type=hidden name=filt value="{{filt}}">{% if evkey %}<input type=hidden name=ev value="{{ evkey }}">{% endif %}{%- endset -%}
{{ rg_checkin_row(display_first(r) ~ ' ' ~ r.last, '/admin/member/' ~ r.id ~ '?from=admin', info.sub, fields|safe, checked=r.cid, hold=('' if r.cid else info.hold), pick=info.pick) }}
{%- endmacro %}
{% if q and ((filt=='not' and not not_going) or (filt=='in' and not checked) or (filt=='going' and not going and not rest)) %}<p class=emptyfind>No players match “{{ q }}”.</p>{% endif %}
{% macro walkin() %}{% if pr %}<a class=rg-walkin href="/qr"><b>+ Walk-in</b><small>Show a QR. They do the one-sheet sign-up on their own phone.</small></a><a class=rg-wrapbtn href="/practices/{{ pr.id }}/wrap">Wrap up practice</a>{% endif %}{% endmacro %}
{% if filt == 'not' %}
<h2 class=rg-cisec>Not going <span>{{ n_not }}</span></h2>
<div class=rg-cilist>{% for r in not_going %}{{ ci(r) }}{% else %}<p class=emptyfind>No one yet.</p>{% endfor %}</div>
{% elif filt == 'in' %}
<h2 class=rg-cisec>Checked in <span>{{ n }}</span></h2>
<div class=rg-cilist>{% for r in checked %}{{ ci(r) }}{% else %}<p class=emptyfind>No one yet.</p>{% endfor %}</div>
{{ walkin() }}
{% else %}
<div class=rg-cilist>{% for r in going %}{{ ci(r) }}{% else %}<p class=emptyfind>No one going yet.</p>{% endfor %}</div>
{{ walkin() }}
{% if rest %}<h2 class=rg-cisec>Everyone else <span>{{rest|length}}</span></h2>
<div class=rg-cilist>{% for r in rest %}{{ ci(r) }}{% endfor %}</div>{% endif %}
{% endif %}
{% if ev_pinned %}<script>(function(){var el=document.querySelector('.evpin.on'); if(el) el.scrollIntoView({block:'center'});})();</script>{% endif %}
{% if coming %}<div class=rg-day>Coming up</div><div class=list>{% for item in coming %}<a class=li href="{{ item.href }}" style="color:inherit;text-decoration:none"><span class=grow><span class=ell style="display:block;font-weight:600">{{ item.title }}</span><span class="ty-muted ty-sm sm">{{ item.when }}{% if item.place %} · {{ item.place }}{% endif %}</span></span></a>{% endfor %}</div>{% endif %}
<a class=wkadd href="/events/new?lane=schedule">+ New practice or event</a>
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
  return '<a class=li href="'+href(iso, ev.key)+'" style="color:inherit;text-decoration:none"><span class=grow><span class=ell style="display:block;font-weight:650">'+String(ev.title||'').replace(/[&<>]/g,'')+'</span><span class="ty-muted ty-sm sm">'+String(ev.when||'').replace(/[&<>]/g,'')+'</span></span></a>';
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
 if(window.grunionsGo) grunionsGo(href(iso),false,true); else location.replace(href(iso));
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

T["transfer"] = ADMIN_NAV + """<div class=rg-screen>
{{ rg_page_title('Data transfer', 'Bring members in, take records out. Nothing is deleted.') }}
{% if stats %}{{ rg_callout('Imported', 'Read ' ~ stats.rows ~ ' rows · updated ' ~ stats.matched ~ ' members · ' ~ (stats.req_updates or 0) ~ ' compliance items · ' ~ (stats.unmatched|length) ~ ' not in the app', '', '', 'lime') }}
{% if stats.unmatched %}<details class=rg-tableview><summary>Not signed up in the app</summary>{% for u in stats.unmatched %}<p class=ty-muted>{{ u }}</p>{% endfor %}</details>{% endif %}{% endif %}
{{ rg_label('Import') }}
<div class=rg-srows><button type=button class=rg-srow data-open-dialog=importSheet><span class=rg-srlabel>Members from CSV</span><span class=rg-srvalue>Upload</span>{{ rg_icon('chevron_right', 'sm') }}</button></div>
<p class="ty-muted ty-sm">Matching uses email first, then exact legal first and last name. Nothing is removed.</p>
{{ rg_label('Export') }}
<div class=rg-srows>
{{ rg_settings_row('Members & clearance', 'CSV', '/members.csv') }}
{{ rg_settings_row('Practices', 'CSV', '/export/practices.csv?start=' ~ year0 ~ '&end=' ~ today_iso) }}
{{ rg_settings_row('Attendance', 'CSV', '/export/practices.csv?detail=1&start=' ~ year0 ~ '&end=' ~ today_iso) }}
{{ rg_settings_row('Payments recorded', 'CSV', '/export/payments.csv') }}
</div>
<p class="ty-muted ty-sm">Practices and attendance cover this year so far.</p>
{{ rg_button('Export everything (.zip)', 'primary', '/export/all.zip') }}
{% if last_export %}<p class="ty-muted ty-sm">Last export · {{ last_export }}</p>{% endif %}
{% if sheet_on %}{{ rg_label('Google Sheet') }}
<p class="ty-muted ty-sm">{% if sheet_status.at %}Last sync {{sheet_status.at}} PT · {{sheet_status.label}}{% else %}Not synced yet{% endif %}{% if sheet_status.detail and not sheet_status.ok %} · {{sheet_status.detail}}{% endif %}. Members, Practices and Attendance stay in sync after changes; a full rewrite also runs daily.</p>
<form method=post action=/export/sheet>{{csrf_field()}}{{ rg_button('Sync to Google Sheet now', 'secondary') }}</form>{% endif %}
<dialog id=importSheet class="botsheet modal" data-sheet-name=import><form method=post action=/manage/tools/transfer enctype=multipart/form-data class=sheet>{{csrf_field()}}<div class=grab aria-hidden=true></div>
<h2>Members from CSV.</h2>
<ol class=ty-muted style="margin:0;padding-left:18px;line-height:1.6">
<li>Log in at <a href=https://usawp.sport80.com>usawp.sport80.com</a> and switch to the club profile.</li>
<li>Members → Smart Lists → Edit Columns: name, email, membership status, member number, valid until, plus SafeSport / background.</li>
<li>Actions → Export Report, then upload the emailed file here.</li></ol>
{{ upload_field('file', 'file', 'CSV or Excel', '.csv,.xlsx') }}
<button class="rg-btn primary">Import</button>
</form></dialog>
</div>"""

T["members"] = ADMIN_NAV + """{% call admin_page(title) %}<a class="rg-btn ghost pageact" href=/members.csv>Export CSV</a>{% endcall %}
<div class=peoplebar>
<form method=get action=/members><input name=q value="{{q}}" placeholder="Search people..." autocomplete=off>{% if view != 'members' %}<input type=hidden name=view value="{{view}}">{% endif %}{% if filt %}<input type=hidden name=filt value="{{ filt }}">{% endif %}</form>
<div class="rg-filters fchips chiprow" data-seg>
<a href="/members{% if view != 'members' %}?view={{ view }}{% endif %}{% if q %}{{ '&amp;' if view != 'members' else '?' }}q={{ q|urlencode }}{% endif %}" {% if not filt %}class=on aria-current=true{% endif %}>All</a>
<a href="/members?{% if view != 'members' %}view={{ view }}&amp;{% endif %}filt=expiring{% if q %}&amp;q={{ q|urlencode }}{% endif %}" {% if filt=='expiring' %}class=on aria-current=true{% endif %}>Expiring</a>
<a href="/members?{% if view != 'members' %}view={{ view }}&amp;{% endif %}filt=uncleared{% if q %}&amp;q={{ q|urlencode }}{% endif %}" {% if filt=='uncleared' %}class=on aria-current=true{% endif %}>Not cleared</a>
</div>
{{ rg_counts([(rows|length, 'Total', 'graphite'), (c.verified, 'Verified', 'lime'), (c.pending, 'Pending', 'sun'), (c.expired, 'Expired', 'cherry'), (c.unknown, 'Unknown', 'tangerine')]) }}
</div>
{% macro prow(r, kind) %}<div class="li personrow">{% call person_link(r) %}{% for tag in person_tags(r) %}<span class=sporttag>{{ tag }}</span>{% endfor %}<span class=sporttag>{{ pay_label(r) }}</span>{% endcall %}
<span class=more><button type=button class=morebtn aria-label="Actions for {{display_first(r)}} {{r.last}}" aria-haspopup=menu aria-expanded=false><svg width="20" height="20" viewBox="0 0 256 256" fill="currentColor" aria-hidden="true"><path d="M140,128a12,12,0,1,1-12-12A12,12,0,0,1,140,128Zm56-12a12,12,0,1,0,12,12A12,12,0,0,0,196,116ZM60,116a12,12,0,1,0,12,12A12,12,0,0,0,60,116Z"/></svg></button>
<div class=menu hidden role=menu>
{% set rowst = list_row_status(r, view) %}
{% set who = display_first(r) ~ ' ' ~ (r.last or '') %}
{% if rowst.tone in ('bad', 'warn') and (r.vr_status or '') != 'pending' %}<button type=button data-sheet=insSheet data-mid="{{ r.id }}" data-who="{{ who }}" data-num="{{ r.usawp_number or '' }}">Check insurance</button>{% endif %}
{% if member_plans %}<button type=button data-sheet=memSheet data-mid="{{ r.id }}" data-who="{{ who }}">Check membership</button>{% endif %}
{% if kind == 'members' %}
{% if r.id in board_ids %}<form method=post>{{csrf_field()}}<input type=hidden name=member_id value={{r.id}}><input type=hidden name=list_view value="{{ view }}"><input type=hidden name=q value="{{q}}"><input type=hidden name=filt value="{{ filt }}"><button name=action value=remove_board>Remove from leadership</button></form>{% else %}<button type=button data-sheet=boardSheet data-mid="{{ r.id }}" data-who="{{ who }}">Add to leadership</button>{% endif %}
{% if r.is_admin %}{% if n_admins<=1 or r.email in boot %}<button type=button disabled title="{% if n_admins<=1 %}Last admin{% else %}Set by ADMIN_EMAIL{% endif %}">Remove admin</button>{% else %}<form method=post>{{csrf_field()}}<input type=hidden name=member_id value={{r.id}}><input type=hidden name=list_view value="{{ view }}"><input type=hidden name=q value="{{q}}"><input type=hidden name=filt value="{{ filt }}"><button name=action value=remove_admin>Remove admin</button></form>{% endif %}{% else %}<form method=post>{{csrf_field()}}<input type=hidden name=member_id value={{r.id}}><input type=hidden name=list_view value="{{ view }}"><input type=hidden name=q value="{{q}}"><input type=hidden name=filt value="{{ filt }}"><button name=action value=make_admin>Make admin</button></form>{% endif %}
{% if r.id in listed %}<form method=post>{{csrf_field()}}<input type=hidden name=member_id value={{r.id}}><input type=hidden name=list_view value="{{ view }}"><input type=hidden name=q value="{{q}}"><input type=hidden name=filt value="{{ filt }}"><button name=action value=remove_coaching>Remove from coaches</button></form>{% else %}<form method=post>{{csrf_field()}}<input type=hidden name=member_id value={{r.id}}><input type=hidden name=list_view value="{{ view }}"><input type=hidden name=q value="{{q}}"><input type=hidden name=filt value="{{ filt }}"><button name=action value=add_coaching>Add to coaches</button></form>{% endif %}
{% if r.id in referees %}<form method=post>{{csrf_field()}}<input type=hidden name=member_id value={{r.id}}><input type=hidden name=list_view value="{{ view }}"><input type=hidden name=q value="{{q}}"><input type=hidden name=filt value="{{ filt }}"><button name=action value=remove_referee>Remove from referees</button></form>{% else %}<form method=post>{{csrf_field()}}<input type=hidden name=member_id value={{r.id}}><input type=hidden name=list_view value="{{ view }}"><input type=hidden name=q value="{{q}}"><input type=hidden name=filt value="{{ filt }}"><button name=action value=add_referee>Add to referees</button></form>{% endif %}
{% elif kind == 'coaches' %}
{% if r.role=='coach' %}<form method=post>{{csrf_field()}}<input type=hidden name=member_id value={{r.id}}><input type=hidden name=list_view value=coaches><input type=hidden name=q value="{{q}}"><input type=hidden name=filt value="{{ filt }}"><button name=action value=remove_coach>Remove active coach</button></form>{% else %}<form method=post>{{csrf_field()}}<input type=hidden name=member_id value={{r.id}}><input type=hidden name=list_view value=coaches><input type=hidden name=q value="{{q}}"><input type=hidden name=filt value="{{ filt }}"><button name=action value=make_coach>Make active coach</button></form>{% endif %}
<form method=post>{{csrf_field()}}<input type=hidden name=member_id value={{r.id}}><input type=hidden name=list_view value=coaches><input type=hidden name=q value="{{q}}"><input type=hidden name=filt value="{{ filt }}"><button name=action value=remove_coaching>Remove from coaches</button></form>
{% elif kind == 'eligible' %}
<form method=post>{{csrf_field()}}<input type=hidden name=member_id value={{r.id}}><input type=hidden name=list_view value=coaches><input type=hidden name=q value="{{q}}"><input type=hidden name=filt value="{{ filt }}"><button name=action value=add_coaching>Add to coaches</button></form>
{% if r.role=='coach' %}<form method=post>{{csrf_field()}}<input type=hidden name=member_id value={{r.id}}><input type=hidden name=list_view value=coaches><input type=hidden name=q value="{{q}}"><input type=hidden name=filt value="{{ filt }}"><button name=action value=remove_coach>Remove active coach</button></form>{% else %}<form method=post>{{csrf_field()}}<input type=hidden name=member_id value={{r.id}}><input type=hidden name=list_view value=coaches><input type=hidden name=q value="{{q}}"><input type=hidden name=filt value="{{ filt }}"><button name=action value=make_coach>Make active coach</button></form>{% endif %}
{% elif kind == 'admins' %}
{% if n_admins<=1 or r.email in boot %}<button type=button disabled title="{% if n_admins<=1 %}Last admin{% else %}Set by ADMIN_EMAIL{% endif %}">Remove admin</button>{% else %}<form method=post>{{csrf_field()}}<input type=hidden name=member_id value={{r.id}}><input type=hidden name=list_view value=admins><input type=hidden name=q value="{{q}}"><input type=hidden name=filt value="{{ filt }}"><button name=action value=remove_admin>Remove admin</button></form>{% endif %}
{% elif kind == 'referees' %}
<form method=post>{{csrf_field()}}<input type=hidden name=member_id value={{r.id}}><input type=hidden name=list_view value=referees><input type=hidden name=q value="{{q}}"><input type=hidden name=filt value="{{ filt }}"><button name=action value=remove_referee>Remove from referees</button></form>
{% elif kind == 'ref_eligible' %}
<form method=post>{{csrf_field()}}<input type=hidden name=member_id value={{r.id}}><input type=hidden name=list_view value=referees><input type=hidden name=q value="{{q}}"><input type=hidden name=filt value="{{ filt }}"><button name=action value=add_referee>Add to referees</button></form>
{% endif %}
</div></span></div><!--endrow-->{% endmacro %}
{% macro sheet_hidden() %}{{ csrf_field() }}<input type=hidden name=member_id value="" data-fill=mid><input type=hidden name=list_view value="{{ view }}"><input type=hidden name=q value="{{ q }}"><input type=hidden name=filt value="{{ filt }}">{% endmacro %}
<dialog id=insSheet class="botsheet modal"><form method=post class=sheet>{{ sheet_hidden() }}<div class=grab aria-hidden=true></div>
<p class=ty-caps data-fill=who></p><h2>Check insurance.</h2>
<p class=ty-muted>Look them up on Sport:80, then enter their USA Water Polo membership here.</p>
<label class=rg-field><span>USAWP MEMBER #</span><input name=number inputmode=numeric maxlength=20 autocomplete=off data-fill=num></label>
<label class=rg-field><span>VALID UNTIL</span><input type=date name=valid_until min="{{ today_iso }}"></label>
<label class=checkline><input type=checkbox name=no_date value=1> No expiration date on Sport:80</label>
<button class="rg-btn primary" name=action value=verify>Mark insured</button>
</form></dialog>
{% if member_plans %}<dialog id=memSheet class="botsheet modal"><form method=post class=sheet>{{ sheet_hidden() }}<div class=grab aria-hidden=true></div>
<p class=ty-caps data-fill=who></p><h2>Check membership.</h2>
<p class=ty-muted>Mark them paying once you've seen the payment. Paying isn't clearance; insurance still counts.</p>
<label class=rg-field><span>PLAN</span><select name=plan_id required id=memPlan>{% for p in member_plans %}<option value="{{ p.id }}" data-kind="{{ p.kind }}">{{ p.name }} · {{ 'Monthly' if p.kind == 'monthly' else 'Annual' }}</option>{% endfor %}</select></label>
<label class=rg-field><span>PAID THROUGH</span><input type=date name=paid_through required min="{{ today_iso }}" id=memThrough></label>
<button class="rg-btn primary" name=action value=membership>Mark paying</button>
</form></dialog>{% endif %}
<dialog id=boardSheet class="botsheet modal"><form method=post class=sheet>{{ sheet_hidden() }}<div class=grab aria-hidden=true></div>
<p class=ty-caps data-fill=who></p><h2>Add to leadership.</h2>
<p class=ty-muted>Pick their role or add a new one. Leadership joins Board chat and gets full Manage access.</p>
{% if board_roles %}<label class=rg-field><span>ROLE</span><select name=role_id id=boardRole>{% for r in board_roles %}<option value="{{ r.id }}">{{ r.name }}</option>{% endfor %}<option value="">New role…</option></select></label>{% endif %}
<label class=rg-field id=boardNewRow{% if board_roles %} hidden{% endif %}><span>NEW ROLE</span><input name=new_role maxlength=80 placeholder="e.g. Treasurer" autocomplete=off></label>
<button class="rg-btn primary" name=action value=add_board>Add to leadership</button>
</form></dialog>
<script>
(function(){
 if(window.grunionsPeopleSheets) return; window.grunionsPeopleSheets=1;
 document.addEventListener('click',function(e){
  var b=e.target.closest&&e.target.closest('[data-sheet]'); if(!b) return;
  var d=document.getElementById(b.getAttribute('data-sheet')); if(!d) return;
  e.preventDefault(); e.stopPropagation();
  d.querySelectorAll('[data-fill=mid]').forEach(function(x){x.value=b.getAttribute('data-mid')});
  d.querySelectorAll('[data-fill=who]').forEach(function(x){x.textContent=b.getAttribute('data-who')});
  d.querySelectorAll('[data-fill=num]').forEach(function(x){x.value=b.getAttribute('data-num')||''});
  if(window.grunionsDismissMenu) grunionsDismissMenu();
  setTimeout(function(){ if(window.grunionsOpenSheet) grunionsOpenSheet(d); else d.showModal(); }, 0);
 }, true);
 document.addEventListener('change',function(e){
  if(e.target.id==='boardRole'){ var row=document.getElementById('boardNewRow'); row.hidden=!!e.target.value; if(!row.hidden) row.querySelector('input').focus(); }
  if(e.target.id==='memPlan') fillThrough();
 });
 function fillThrough(){ var sel=document.getElementById('memPlan'), out=document.getElementById('memThrough'); if(!sel||!out) return;
  var kind=sel.options[sel.selectedIndex].getAttribute('data-kind'), t=new Date();
  if(kind==='annual') t.setFullYear(t.getFullYear()+1); else t.setMonth(t.getMonth()+1);
  out.value=t.getFullYear()+'-'+String(t.getMonth()+1).padStart(2,'0')+'-'+String(t.getDate()).padStart(2,'0'); }
 fillThrough();
})();
</script>
<div class=people>
{% macro lettered() %}{% set ns = namespace(letter='') %}{% for r in rows %}{% set letter = ((r.last or '?')[:1])|upper %}{% if letter != ns.letter %}{% if ns.letter %}</div></div>{% endif %}<div class=lgroup><h3 class=alpha>{{ letter }}</h3><div class="list loose">{% set ns.letter = letter %}{% endif %}{% if view == 'coaches' %}{{ prow(r, 'coaches' if r.id in listed else 'eligible') }}{% elif view == 'referees' %}{{ prow(r, 'referees' if r.id in referees else 'ref_eligible') }}{% elif view == 'admins' %}{{ prow(r, 'admins') }}{% else %}{{ prow(r, 'members') }}{% endif %}{% else %}<div class="list loose"><div class=li><span class='ty-muted ty-sm'>{% if q %}No people match “{{ q }}”.{% else %}No one here.{% endif %}</span></div></div>{% endfor %}{% if ns.letter %}</div></div>{% endif %}{% endmacro %}
{{ lettered() }}
</div>
<script>
(function(){var bar=document.querySelector('.peoplebar'); function pin(){ if(bar) document.documentElement.style.setProperty('--peoplepin', bar.offsetHeight+'px'); } pin(); window.addEventListener('resize', pin); if(window.ResizeObserver&&bar) new ResizeObserver(pin).observe(bar);})();
</script>
<script>
(function(){
 var state=window.grunionsPeopleMenu||(window.grunionsPeopleMenu={btn:null,pushed:false});
 document.querySelectorAll('body>.menu.floating').forEach(function(m){ m.remove(); });
 function menuOf(btn){ return btn && (btn._menu || (btn.parentNode && btn.parentNode.querySelector('.menu'))); }
 function hide(){
  document.querySelectorAll('.menu').forEach(function(m){ m.hidden=true; });
  if(state.btn) state.btn.setAttribute('aria-expanded','false');
  state.btn=null;
 }
 function closeAll(fromPop){
  hide();
  if(fromPop){ state.pushed=false; return; }
  if(state.pushed){ state.pushed=false; window.grunionsMenuPop=1; grunionsPopOverlay(); }
 }
 function place(btn){
  var menu=menuOf(btn); if(!menu) return;
  if(!menu._btn){ menu._btn=btn; btn._menu=menu; }
  if(menu.parentNode!==document.body) document.body.appendChild(menu);
  menu.classList.add('floating');
  menu.hidden=false;
  var nav=document.querySelector('nav.tabs');
  var limit=nav ? nav.getBoundingClientRect().top-8 : window.innerHeight-8;
  menu.style.maxHeight=Math.max(120, limit-16)+'px';
  var r=btn.getBoundingClientRect();
  var mw=menu.offsetWidth, mh=menu.offsetHeight;
  var left=Math.max(8, Math.min(window.innerWidth-mw-8, r.right-mw));
  var top=r.bottom+6;
  if(top+mh>limit){
   var above=r.top-6-mh;
   top=above>=8 ? above : Math.max(8, limit-mh);
  }
  menu.style.left=Math.round(left)+'px';
  menu.style.top=Math.round(top)+'px';
  menu.style.right='auto';
 }
 document.querySelectorAll('.people .morebtn').forEach(function(btn){
  btn.onclick=function(e){
   e.preventDefault(); e.stopPropagation();
   var menu=menuOf(btn);
   var was=menu && !menu.hidden && state.btn===btn;
   hide();
   if(was){ if(state.pushed){ state.pushed=false; window.grunionsMenuPop=1; grunionsPopOverlay(); } return; }
   if(!menu) return;
   state.btn=btn;
   btn.setAttribute('aria-expanded','true');
   place(btn);
   if(!state.pushed){ history.pushState({grunionsMenu:1}, '', location.href); state.pushed=true; }
  };
 });
 window.grunionsCloseMenu=function(){
  if(!state.btn && !document.querySelector('.menu.floating:not([hidden])')) return false;
  closeAll(true);
  return true;
 };
 window.grunionsPlacePeopleMenu=function(){ if(state.btn) place(state.btn); };
 window.grunionsDismissMenu=function(){ closeAll(false); };
 if(!window.grunionsPeopleMenuBound){ window.grunionsPeopleMenuBound=1;
  document.addEventListener('click', function(e){
   if(e.target.closest && e.target.closest('.menu,.morebtn')) return;
   var st=window.grunionsPeopleMenu; if(!st||(!st.btn&&!st.pushed)) return;
   if(st.pushed && e.target.closest && e.target.closest('a[href]')){ st.pushed=false; try{ history.replaceState({grunions:1}, '', location.href); }catch(err){} if(window.grunionsCloseMenu) window.grunionsCloseMenu(true); return; }
   closeAll(false);
  });
  document.addEventListener('keydown', function(e){ if(e.key==='Escape' && window.grunionsPeopleMenu && window.grunionsPeopleMenu.btn) closeAll(false); });
  document.addEventListener('submit', function(){ var st=window.grunionsPeopleMenu; if(st&&st.pushed){ st.pushed=false; try{ history.replaceState({grunions:1}, '', location.href); }catch(err){} } }, true);
  window.addEventListener('resize', function(){ if(window.grunionsPlacePeopleMenu) window.grunionsPlacePeopleMenu(); });
  window.addEventListener('scroll', function(){ if(window.grunionsPlacePeopleMenu) window.grunionsPlacePeopleMenu(); }, true);
 }
})();
</script>"""

T["expiring"] = ADMIN_NAV + """{{ admin_page('Expiring', 'Membership, SafeSport, and other dated items. Tap a person to open them.') }}
<div class=expage>
<form class="row noprint" method=get action=/expiring style="align-items:center;margin-bottom:8px"><label class="ty-body sm" style="flex:0 0 auto;margin:0">Window (days)<input name=days type=number min=1 value={{days}} onchange=this.form.submit() style="margin:6px 0 0;height:44px;width:96px"></label></form>
{% for key, label in [('expired','Expired'),('within_7','Next 7 days'),('within_%d'%days,'Next %d days'%days)] %}<h2 class=egroup>{{label}} <span class='ty-muted ty-sm'>{{rep[key]|length}}</span></h2>
<div class=list>{% for r in rep[key] %}<div class=li><a class=grow href="/admin/member/{{ r.id }}" style="color:inherit;text-decoration:none;min-width:0"><div style="display:flex;align-items:center;gap:8px;min-width:0"><span class=ell style="font-weight:500;flex:1">{{display_first(r)}} {{r.last}}</span>
<span class="chip-info daybadge"><span class="dot {{ 'bad' if r.days_left < 0 else ('warn' if r.days_left <= 7 else '') }}" aria-hidden=true></span>{% if r.days_left < 0 %}{{ -r.days_left }}d ago{% elif r.days_left == 0 %}Today{% else %}{{ r.days_left }}d left{% endif %}</span></div>
<div class="ty-muted ty-sm xs">{{ r.item }} · {{ fmt_long(r.usawp_valid_until) }}</div></a>
<a class="rg-btn secondary" href="/admin/member/{{ r.id }}">Check</a></div>{% else %}<div class=li><span class='ty-muted ty-sm'>None</span></div>{% endfor %}</div>{% endfor %}
<p class="ty-muted ty-sm sm" style="margin-top:20px">Check each person on Sport:80 and update them from their page. Daily report: <a href=/api/expiring>/api/expiring</a>.</p>
</div>"""

T["requirements_page"] = ADMIN_NAV + """{{ admin_page('Rules', 'Cleared to play means a current USAWP membership and current SafeSport.') }}
{% if not reqs %}<p class=emptyfind>No rules yet.</p>{% endif %}
{% for q in reqs %}<details class=card><summary><span>{{q.name}}</span><span class="ty-muted ty-sm sm" style="margin-left:auto;margin-right:10px">{{q.applies_to}}{{'' if q.active else ' · off'}}</span></summary>
<form method=post class=body>{{csrf_field()}}<input type=hidden name=id value={{q.id}}>
<div class=row><label>Applies to<select name=applies_to>{% for o in ['all','athlete','coach'] %}<option {{'selected' if q.applies_to==o}}>{{o}}</option>{% endfor %}</select></label>
<label>Import keywords<input name=keywords value="{{q.keywords or ''}}"></label></div>
<label><input type=checkbox name=expires {{'checked' if q.expires}}>Has an expiration date</label><label><input type=checkbox name=active {{'checked' if q.active}}>Active</label>
<button class="rg-btn primary full" name=action value=save>Save</button></form></details>{% endfor %}
<details class=card><summary>Add a rule</summary><form method=post class=body>{{csrf_field()}}<label>Name<input name=name placeholder="CPR / First Aid"></label>
<div class=row><label>Applies to<select name=applies_to><option>all</option><option>athlete</option><option>coach</option></select></label><label>Keywords<input name=keywords placeholder="cpr,firstaid"></label></div>
<label><input type=checkbox name=expires checked>Has an expiration date</label><button class="rg-btn secondary full" name=action value=add>Add</button></form></details>"""

T["website"] = ADMIN_NAV + """<div class="rg-screen rg-website">
{# Figma 62 · W1 Website & sharing: status first, small preview, settings that save themselves, code in a sheet. #}
{{ rg_page_title('Website', 'Your public schedule, on your site.') }}
<form method=post action="/manage/widget" data-autosave>{{ csrf_field() }}
{{ rg_status_toggle('widget_on', w.enabled, host, ('Published · last change ' ~ changed) if w.enabled else 'Not published · visitors see nothing yet') }}
</form>
{{ rg_section_count('Preview', events|length) }}
<div class=rg-miniprev>
{% for ev in events[:2] %}{{ rg_event_row('', ev.kicker, ev.title, ev.meta, ev.count, 'GOING', ev.tone) }}{% else %}<p class=rg-note>Nothing coming up yet. Published practices and Lineup events show here.</p>{% endfor %}
<a class="rg-btn secondary" href="/widget?preview=1" target=_blank rel=noopener>Open full preview</a>
</div>
{{ rg_section_count('What visitors see', 6) }}
<div class=rg-stack8>
{{ rg_settings_row('Tabs', tabs_label, '#', 'data-open-dialog=tabsSheet', 'tabs') }}
{{ rg_settings_row('Opens on', opens_label, '#', 'data-open-dialog=opensSheet', 'opens') }}
<form method=post action="/manage/widget" data-autosave class=rg-stack8>{{ csrf_field() }}
{{ rg_toggle('include_schedule', 'Regular schedule', '', w.include_schedule) }}
{{ rg_toggle('show_pricing', 'Prices', 'Only ones you filled in', w.show_pricing) }}
{{ rg_toggle('show_trial', 'Free-trial message', '', w.show_trial) }}
{{ rg_toggle('show_counts', 'How many are going', 'Numbers only — never names or photos', w.show_counts) }}
</form>
</div>
{{ rg_section_count('Add to your site', 2) }}
<div class=rg-stack8>
{{ rg_settings_row('Embed code', 'Copy', '#', 'data-open-dialog=embedSheet') }}
{% if share_url %}{{ rg_settings_row('Share link', 'Share', '#', 'data-share-url="' ~ share_url ~ '" data-share-title="Schedule"') }}{% else %}{{ rg_settings_row('Share link', 'Publish first') }}{% endif %}
</div>
<p class=rg-note>Changes save as you make them. Your embed updates on its own — paste it once.</p>
</div>
<dialog id=tabsSheet class="botsheet modal"><form method=post action="/manage/widget" data-autosave class=sheet>{{ csrf_field() }}<div class=grab aria-hidden=true></div>
<input type=hidden name=chips_present value=1>
<h2>Tabs.</h2><p class=ty-muted>Which tabs visitors can switch between. All is always there.</p>
{{ rg_choice_chips('chips', chip_choices, w.chips, true) }}
<button type=button class="rg-btn primary" data-sheet-close onclick="this.closest('dialog').close()">Done</button>
</form></dialog>
<dialog id=opensSheet class="botsheet modal"><form method=post action="/manage/widget" data-autosave class=sheet>{{ csrf_field() }}<div class=grab aria-hidden=true></div>
<h2>Opens on.</h2><p class=ty-muted>The tab visitors see first.</p>
{% for slug, label in chip_choices if slug in w.chips %}{{ rg_choice('default_chip', slug, label, '', w.default_chip == slug) }}{% endfor %}
<button type=button class="rg-btn primary" onclick="this.closest('dialog').close()">Done</button>
</form></dialog>
<dialog id=embedSheet class="botsheet modal" data-sheet-name=embed><div class=sheet><div class=grab aria-hidden=true></div>
<h2>Add to your site.</h2><p class=ty-muted>Paste it once. Schedule changes show up on their own.</p>
{{ rg_choice_chips('platform', platforms, 'squarespace', false, 'id=platformPick') }}
{{ rg_code(embed, 'embedCode') }}
{% for key, label, lines in platform_steps %}<div data-platform="{{ key }}"{% if key != 'squarespace' %} hidden{% endif %}>{{ rg_steps(lines) }}</div>{% endfor %}
<div class=rg-btnrow>
<a class="rg-btn secondary" id=embedEmail href="mailto:?subject={{ ('Our schedule for the website')|urlencode }}&body={{ ('Hi! Please paste this into our website where the schedule should go. It updates on its own.\n\n' ~ embed)|urlencode }}">Email it</a>
<button type=button class="rg-btn primary" id=copyEmbed>Copy code</button>
</div>
</div></dialog>
<template id=embedText>{{ embed }}</template>
<script>
(function(){
 var pick=document.getElementById('platformPick');
 if(pick) pick.addEventListener('change', function(e){ document.querySelectorAll('[data-platform]').forEach(function(el){ el.hidden=el.getAttribute('data-platform')!==e.target.value; }); });
 var copy=document.getElementById('copyEmbed');
 if(copy) copy.onclick=function(){ var t=document.getElementById('embedText').innerHTML.replace(/&lt;/g,'<').replace(/&gt;/g,'>').replace(/&quot;/g,'"').replace(/&#34;/g,'"').replace(/&#39;/g,"'").replace(/&amp;/g,'&');
  (navigator.clipboard?navigator.clipboard.writeText(t):Promise.reject()).then(function(){ grunionsSavedToast('Copied'); }, function(){ grunionsSavedToast('Select the code and copy it'); }); };
 document.addEventListener('click', function(e){ var b=e.target.closest&&e.target.closest('[data-share-url]'); if(!b) return; e.preventDefault();
  var u=b.getAttribute('data-share-url'); if(navigator.share){ navigator.share({title:b.getAttribute('data-share-title')||'', url:u}).catch(function(){}); }
  else if(navigator.clipboard){ navigator.clipboard.writeText(u).then(function(){ grunionsSavedToast('Link copied'); }); } });
 document.querySelectorAll('form[data-autosave]').forEach(function(f){ f.addEventListener('autosaved', function(ev){ var j=ev.detail||{}; if(j.reload) location.reload(); }); });
})();
</script>"""
T["qr_page"] = ADMIN_NAV + """<div class=rg-screen>
{{ rg_page_title('QR codes', 'Print or share. Each code opens one thing.') }}
<div class=rg-qrgrid>
{{ rg_qr_card('Join the club', 'Opens the join page with the team picked.', '/qr.svg?for=join' if join_url else '', join_url, 'join-qr.svg', 'The join link is not ready yet.') }}
</div>
</div>"""

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
<p class="ty-body">Fonts, colors, spacing, and radius change in regulars/foundation.css.</p>
<h2>Type</h2>
<div class=card>
<p style="font-size:var(--type-title-1-size);font-weight:var(--type-title-1-weight);letter-spacing:var(--type-title-1-tracking)">Title</p>
<p>Body. The default reading size.</p>
<p class="ty-muted ty-sm sm">Caption and meta.</p>
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
<p class="ty-muted ty-sm sm">One primary in a group. Tertiary is the quiet action. Loading hides the label.</p>
<div class=ds-row>
<button type=button class="rg-btn primary">Primary</button>
<button type=button class="rg-btn secondary">Secondary</button>
<button type=button class="rg-btn secondary btn-tertiary">Tertiary</button>
<button type=button class="rg-btn danger">Destructive</button>
<button type=button class="rg-btn primary" disabled>Disabled</button>
<button type=button class="rg-btn primary" aria-busy=true>Saving</button>
</div>
<h2>Page header</h2>
<p class="ty-muted ty-sm sm">Management pages use Title 1, a ghost action on the right, then an optional Body 2 subtitle. A back control returns to Manage. The gap below the block is --space-4.</p>
{% call admin_page('People', 'One line in secondary text.') %}<a class="rg-btn ghost pageact" href="#">Export CSV</a>{% endcall %}
<h2>Filter chips</h2>
<p class="ty-muted ty-sm sm">Lime when selected, outlined when not. Sibling views (Chat, Admin, Profile) use the same pill, one at a time.</p>
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
<p class="ty-muted ty-sm sm">One pill. Members get three circles. Coaches and admins get four. The fourth is Manage. Icons only. The selected circle is Electric Lime.</p>
""" + _ds_nav("Member navigation", ("home", "lineup", "chat")) + _ds_nav("Coach navigation", ("home", "lineup", "chat", "manage")) + """
<h2>Manage rows</h2>
<p class="ty-muted ty-sm sm">Grouped list rows on a raised surface. A leading icon, a title, one line of description, a count only when it is above zero, and a trailing chevron. A pending Requests count is the info badge. A Compliance count is the warning badge.</p>
<div class=mgroup><h2>Activities</h2><div class=mlist>
{{ manage_row('/manage', 'Schedule', 'Practices, scrimmages & games', '<svg width="20" height="20" viewBox="0 0 256 256" fill="currentColor" aria-hidden="true"><path d="M208,32H184V24a8,8,0,0,0-16,0v8H88V24a8,8,0,0,0-16,0v8H48A16,16,0,0,0,32,48V208a16,16,0,0,0,16,16H208a16,16,0,0,0,16-16V48A16,16,0,0,0,208,32ZM72,48v8a8,8,0,0,0,16,0V48h80v8a8,8,0,0,0,16,0V48h24V80H48V48ZM208,208H48V96H208V208Z"/></svg>', 0) }}
{{ manage_row('/manage', 'Requests', 'Member-submitted events', '<svg width="20" height="20" viewBox="0 0 256 256" fill="currentColor" aria-hidden="true"><path d="M208,32H48A16,16,0,0,0,32,48V208a16,16,0,0,0,16,16H208a16,16,0,0,0,16-16V48A16,16,0,0,0,208,32Zm0,176H48V168H76.69a8,8,0,0,1,5.65,2.34l19.32,19.32a8,8,0,0,0,5.65,2.34h41.38a8,8,0,0,0,5.65-2.34l19.32-19.32a8,8,0,0,1,5.65-2.34H208Z"/></svg>', 2, 'info') }}
{{ manage_row('/manage', 'Compliance', 'Memberships & certifications', '<svg width="20" height="20" viewBox="0 0 256 256" fill="currentColor" aria-hidden="true"><path d="M208,40H48A16,16,0,0,0,32,56v56c0,52.72,25.52,84.67,46.93,102.19,23.06,18.86,46,25.26,47,25.53a8,8,0,0,0,4.2,0c1-.27,23.91-6.67,47-25.53C198.48,196.67,224,164.72,224,112V56A16,16,0,0,0,208,40Z"/></svg>', 5, 'warn') }}
</div></div>
<h2>Segmented</h2>
<p class="ty-muted ty-sm sm">Same control as Exact dates / Month only. Figma role: Toggle group 73:2902.</p>
<div class=actseg role=radiogroup aria-label=Sample>
<label><input type=radio name=dsseg checked><span>Exact dates</span></label>
<label><input type=radio name=dsseg><span>Month only</span></label>
</div>
<h2>Field</h2>
<label>Field<input placeholder="Location"></label>
<h2>Upload</h2>
<p class="ty-muted ty-sm sm">One field for images and files. The dashed area is the control. An image fills the zone. A file shows its name and size. Replace and Remove sit on either one.</p>
{{ upload_field('ds_image') }}
<div style="height:12px"></div>
{{ upload_field('ds_file', 'file', 'CSV', '.csv,.xlsx') }}
<h2>Card and RSVP</h2>
<div class=card>
<div class=nxtitle>Practice</div>
<p class=ty-body>7:00 – 8:30 PM</p>
<p class="ty-muted ty-sm sm">Marina High School</p>
<div class=pills>
{{ rsvp_btn('Going', true, 'going') }}
{{ rsvp_btn('Not going', false, 'notgoing') }}
</div>
</div>
<p class="ty-muted ty-sm sm">Disabled</p>
<div class=ds-row><button type=button class="rg-btn primary" disabled>Primary</button></div>
<h2>Date and time</h2>
<p class="ty-muted ty-sm sm">A centered dialog, the same one as Schedule and every date or time field. Schedule ghosts days with no events and shows a dot. Form calendars leave every day selectable. Time is a clock. Cancel and OK confirm.</p>
<div class="sheet" style="border:1px solid var(--color-sheet-border);border-radius:var(--radius-overlay);padding:20px 12px 8px;background:var(--color-sheet)">
<div class=matkicker>Select date</div>
<div class=matheadline>Tue, Nov 3</div>
<div class=calhead><button type=button class=calmonth aria-label="Previous month"><svg width="20" height="20" viewBox="0 0 256 256" fill="currentColor" aria-hidden="true"><path d="M165.66,202.34a8,8,0,0,1-11.32,11.32l-80-80a8,8,0,0,1,0-11.32l80-80a8,8,0,0,1,11.32,11.32L91.31,128Z"/></svg></button><div class=lbl>November 2026</div><button type=button class=calmonth aria-label="Next month"><svg width="20" height="20" viewBox="0 0 256 256" fill="currentColor" aria-hidden="true"><path d="M181.66,133.66l-80,80a8,8,0,0,1-11.32-11.32L164.69,128,90.34,53.66a8,8,0,0,1,11.32-11.32l80,80A8,8,0,0,1,181.66,133.66Z"/></svg></button></div>
<div class=calwd><span>S</span><span>M</span><span>T</span><span>W</span><span>T</span><span>F</span><span>S</span></div>
<div class=calgrid><span class=calday></span><span class="calday past" aria-disabled=true>1</span><button type=button class="calday on">3</button><button type=button class=calday>4<i class=caldot></i></button></div>
<div class=matactions><button type=button class=mattext>Cancel</button><button type=button class=mattext>OK</button></div>
</div>
<h2>Map, chat, and sheet</h2>
<p class="ty-muted ty-sm sm">Dark is the app. Light uses the same components.</p>
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
<button type=button class="rg-btn primary">Primary</button>
</div>
"""
