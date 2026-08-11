#!/usr/bin/env python3
"""Generates the LRD 90-day review pack as a single self-contained HTML file."""
import json, html

OUT = "/home/user/europe-ad-report/review-pack.html"

# ---------------------------------------------------------------- data
MONTHS = [
    # name, net, ly_net, orders, ly_orders, spend, ly_spend, gross, disc, returns, google, bing, meta
    ("Jun", 160895, 85875, 458, 270, 33812, 20059, 185919, 25028, 2570, 18890, 3395, 12159),
    ("Jul", 150781, 97932, 465, 291, 35754, 13025, 171029, 20250, 7449, 18889, 5033, 12677),
    ("Aug*", 53557, 36816, 138, 107, 12672,  7812,  62620, 10391, 1329,  7155, 2301,  3600),
]
WEEKLY = [("Jun W1",4.12),("Jun W2",5.67),("Jun W3",4.91),("Jun W4",4.16),("Jun W5",5.46),
          ("Jul W1",4.07),("Jul W2",4.06),("Jul W3",4.60),("Jul W4",4.34),("Jul W5",3.76),
          ("Aug W1",4.08),("Aug W2",4.58)]
ORGANIC = [("Jun 25",2035),("Jul 25",2305),("Aug 25",2957),("Sep 25",3910),("Oct 25",4540),
           ("Nov 25",7667),("Dec 25",6199),("Jan 26",6348),("Feb 26",7854),("Mar 26",6838),
           ("Apr 26",5631),("May 26",5322),("Jun 26",6168),("Jul 26",6739),("Aug 26",6139)]
BREAKEVEN = 3.36
MARGIN = 0.298

NET=sum(m[1] for m in MONTHS); LYNET=sum(m[2] for m in MONTHS)
ORD=sum(m[3] for m in MONTHS); LYORD=sum(m[4] for m in MONTHS)
SPEND=sum(m[5] for m in MONTHS); LYSPEND=sum(m[6] for m in MONTHS)
GROSS=sum(m[7] for m in MONTHS); DISC=sum(m[8] for m in MONTHS); RET=sum(m[9] for m in MONTHS)
CONTRIB = NET*MARGIN - SPEND

# ---------------------------------------------------------------- svg helpers
def grouped_bars(data, w=680, h=250, pad_l=58, pad_b=34, pad_t=14, axis_fmt=None, tip_fmt=None):
    """data: [(label, [(value,cls),...]), ...]"""
    mx = max(v for _, vs in data for v, _ in vs) * 1.12
    iw, ih = w - pad_l - 12, h - pad_b - pad_t
    n = len(data); gw = iw / n
    s = [f'<svg viewBox="0 0 {w} {h}" class="chart" role="img">']
    for i in range(5):
        y = pad_t + ih * i / 4; val = mx * (1 - i / 4)
        s.append(f'<line x1="{pad_l}" y1="{y:.1f}" x2="{w-12}" y2="{y:.1f}" class="grid"/>')
        lab = axis_fmt(val) if axis_fmt else f"£{val/1000:.0f}k"
        s.append(f'<text x="{pad_l-8}" y="{y+4:.1f}" class="ax ax-r">{lab}</text>')
    for i, (lab, vals) in enumerate(data):
        k = len(vals); bw = gw * 0.62 / k
        x0 = pad_l + gw * i + gw * 0.19
        for j, (v, cls) in enumerate(vals):
            bh = ih * v / mx
            s.append(f'<rect x="{x0+j*bw:.1f}" y="{pad_t+ih-bh:.1f}" width="{bw-3:.1f}" '
                     f'height="{bh:.1f}" rx="2" class="{cls}">'
                     f'<title>{lab}: {tip_fmt(v) if tip_fmt else f"£{v:,.0f}"}</title></rect>')
        s.append(f'<text x="{pad_l+gw*i+gw/2:.1f}" y="{h-11}" class="ax ax-c">{lab}</text>')
    s.append('</svg>')
    return "".join(s)

def line_chart(data, w=680, h=230, pad_l=44, pad_b=36, pad_t=14, thresh=None, fmt="{:.2f}", unit="", floor_zero=False):
    import math
    vals = [v for _, v in data]
    lo, hi = min(vals), max(vals)
    if thresh: lo, hi = min(lo, thresh), max(hi, thresh)
    span = (hi - lo) or 1; lo -= span*0.16; hi += span*0.16
    # snap to a readable step so axis labels are round numbers
    raw = (hi - lo) / 3
    mag = 10 ** math.floor(math.log10(raw))
    step = next(m*mag for m in (1, 2, 2.5, 5, 10) if m*mag >= raw)
    if floor_zero:
        lo = 0.0
        raw2 = max(vals) / 3.0
        mag2 = 10 ** math.floor(math.log10(raw2))
        step = next(m*mag2 for m in (1, 2, 2.5, 5, 10) if m*mag2 >= raw2)
        hi = math.ceil(max(vals)/step)*step
    else:
        lo = math.floor(lo/step)*step
        hi = lo + step*3
        while hi < max(vals): hi += step
    span = hi - lo
    iw, ih = w - pad_l - 14, h - pad_b - pad_t
    X = lambda i: pad_l + iw * i / max(len(data)-1, 1)
    Y = lambda v: pad_t + ih * (1 - (v - lo) / span)
    s = [f'<svg viewBox="0 0 {w} {h}" class="chart" role="img">']
    for i in range(4):
        y = pad_t + ih*i/3
        s.append(f'<line x1="{pad_l}" y1="{y:.1f}" x2="{w-14}" y2="{y:.1f}" class="grid"/>')
        s.append(f'<text x="{pad_l-8}" y="{y+4:.1f}" class="ax ax-r">{fmt.format(hi-span*i/3)}{unit}</text>')
    if thresh is not None:
        ty = Y(thresh)
        s.append(f'<line x1="{pad_l}" y1="{ty:.1f}" x2="{w-14}" y2="{ty:.1f}" class="thresh"/>')
        s.append(f'<text x="{w-16}" y="{ty-7:.1f}" class="ax ax-e thresh-t">break-even {thresh}x</text>')
    pts = [(X(i), Y(v)) for i, (_, v) in enumerate(data)]
    area = f'M{pts[0][0]:.1f},{pad_t+ih:.1f} ' + " ".join(f'L{x:.1f},{y:.1f}' for x, y in pts) + \
           f' L{pts[-1][0]:.1f},{pad_t+ih:.1f} Z'
    s.append(f'<path d="{area}" class="area"/>')
    s.append('<path d="' + "M" + " L".join(f'{x:.1f},{y:.1f}' for x, y in pts) + '" class="line"/>')
    for i, ((lab, v), (x, y)) in enumerate(zip(data, pts)):
        last = i == len(data)-1
        s.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{4.2 if last else 2.8}" '
                 f'class="{"dot dot-end" if last else "dot"}"><title>{lab}: {fmt.format(v)}{unit}</title></circle>')
    step = max(1, len(data)//8)
    for i, (lab, _) in enumerate(data):
        if i % step == 0 or i == len(data)-1:
            s.append(f'<text x="{X(i):.1f}" y="{h-12}" class="ax ax-c">{lab}</text>')
    s.append('</svg>')
    return "".join(s)

def stacked_split(rows, w=680, h=None):
    """rows: [(label, [(seg_label, value, cls),...])]"""
    bh, gap = 34, 26
    if h is None: h = 16 + len(rows)*(bh+gap) - gap + 16
    mx = max(sum(v for _, v, _ in segs) for _, segs in rows)
    s = [f'<svg viewBox="0 0 {w} {h}" class="chart" role="img">']
    x0 = 96
    for i, (lab, segs) in enumerate(rows):
        y = 16 + i*(bh+gap); x = x0; tot = sum(v for _, v, _ in segs)
        s.append(f'<text x="{x0-12}" y="{y+bh/2+4:.0f}" class="ax ax-r">{lab}</text>')
        for sl, v, cls in segs:
            bwid = (w-x0-70) * v / mx
            s.append(f'<rect x="{x:.1f}" y="{y}" width="{max(bwid,0):.1f}" height="{bh}" class="{cls}">'
                     f'<title>{sl}: £{v:,.0f} ({v/tot:.0%})</title></rect>')
            if bwid > 46:
                s.append(f'<text x="{x+bwid/2:.1f}" y="{y+bh/2+4:.0f}" class="seg-t">{v/tot:.0%}</text>')
            x += bwid
        s.append(f'<text x="{x+9:.1f}" y="{y+bh/2+4:.0f}" class="ax">£{tot/1000:.0f}k</text>')
    s.append('</svg>')
    return "".join(s)


CSS = """
:root{
  --bg:#F7F6F4; --surface:#FFFFFF; --surface-2:#F1EFEB;
  --ink:#1C1E20; --ink-2:#4A4742; --ink-3:#787269;
  --rule:#DFDBD3; --rule-2:#EDEAE4;
  --brass:#8C6A3F; --brass-2:#A98254; --brass-soft:#F0E7DA;
  --good:#3F6B52; --good-soft:#E4EDE7;
  --warn:#A8762C; --warn-soft:#F6ECDA;
  --crit:#9B3B31; --crit-soft:#F7E5E2;
  --sans:ui-sans-serif,system-ui,-apple-system,"Segoe UI",Roboto,"Helvetica Neue",sans-serif;
  --serif:"Iowan Old Style","Palatino Linotype",Palatino,Georgia,serif;
  --mono:ui-monospace,SFMono-Regular,"SF Mono",Menlo,Consolas,monospace;
}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){
  --bg:#16181A; --surface:#1E2124; --surface-2:#25292C;
  --ink:#EDEAE4; --ink-2:#B9B3AA; --ink-3:#8B857C;
  --rule:#32373B; --rule-2:#282C30;
  --brass:#C79A5F; --brass-2:#D8B183; --brass-soft:#33291D;
  --good:#7FB294; --good-soft:#1D2A23;
  --warn:#D7A65B; --warn-soft:#2E2517;
  --crit:#D9776A; --crit-soft:#301E1B;
}}
:root[data-theme="dark"]{
  --bg:#16181A; --surface:#1E2124; --surface-2:#25292C;
  --ink:#EDEAE4; --ink-2:#B9B3AA; --ink-3:#8B857C;
  --rule:#32373B; --rule-2:#282C30;
  --brass:#C79A5F; --brass-2:#D8B183; --brass-soft:#33291D;
  --good:#7FB294; --good-soft:#1D2A23;
  --warn:#D7A65B; --warn-soft:#2E2517;
  --crit:#D9776A; --crit-soft:#301E1B;
}
*,*::before,*::after{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);font-family:var(--sans);
  font-size:15.5px;line-height:1.62;-webkit-font-smoothing:antialiased}
.wrap{max-width:1020px;margin:0 auto;padding:34px 22px 96px}

header.masthead{border-bottom:2px solid var(--ink);padding-bottom:18px;margin-bottom:6px}
.kicker{font-family:var(--mono);font-size:10.5px;letter-spacing:.16em;text-transform:uppercase;
  color:var(--brass);margin:0 0 10px}
h1{font-family:var(--serif);font-weight:600;font-size:clamp(27px,4.4vw,40px);line-height:1.12;
  margin:0 0 10px;letter-spacing:-.012em;text-wrap:balance}
.sub{color:var(--ink-2);margin:0;font-size:15px;max-width:64ch}
.meta{display:flex;flex-wrap:wrap;gap:7px 20px;margin-top:15px;font-family:var(--mono);
  font-size:11.5px;color:var(--ink-3);letter-spacing:.02em}
.meta b{color:var(--ink-2);font-weight:500}

nav.tabs{position:sticky;top:0;z-index:20;background:var(--bg);border-bottom:1px solid var(--rule);
  margin:0 0 30px;padding:9px 0;display:flex;gap:3px;overflow-x:auto;scrollbar-width:thin}
.tab{flex:0 0 auto;font-family:var(--sans);font-size:12.5px;font-weight:500;color:var(--ink-3);
  background:none;border:1px solid transparent;border-radius:5px;padding:6px 9px;cursor:pointer;
  white-space:nowrap;transition:color .13s,background .13s}
.tab:hover{color:var(--ink);background:var(--surface-2)}
.tab[aria-selected="true"]{color:var(--brass);background:var(--brass-soft);border-color:var(--brass)}
.tab:focus-visible{outline:2px solid var(--brass);outline-offset:2px}

.panel{animation:fade .2s ease}
@keyframes fade{from{opacity:0;transform:translateY(3px)}to{opacity:1;transform:none}}
@media (prefers-reduced-motion:reduce){.panel{animation:none}}
.eyebrow{font-family:var(--mono);font-size:11px;line-height:1.5;letter-spacing:.03em;color:var(--ink-3);
  margin:0 0 9px;padding-left:11px;border-left:2px solid var(--brass);max-width:74ch}
h2{font-family:var(--serif);font-weight:600;font-size:clamp(23px,3.4vw,31px);line-height:1.16;
  margin:0 0 20px;letter-spacing:-.011em;text-wrap:balance}
h3{font-family:var(--serif);font-weight:600;font-size:18.5px;margin:38px 0 13px;letter-spacing:-.006em}
h3:first-of-type{margin-top:30px}
p{margin:0 0 14px;max-width:74ch}
.lede{font-size:16.8px;line-height:1.58;color:var(--ink-2);max-width:70ch;margin-bottom:22px}
.note{font-size:13.4px;color:var(--ink-3);line-height:1.58;max-width:76ch;margin-top:11px}
b,strong{font-weight:640;color:var(--ink)}
i{font-style:italic}
a.jump{color:var(--brass);text-decoration:underline;text-underline-offset:2px;cursor:pointer}
code{font-family:var(--mono);font-size:.87em;background:var(--surface-2);padding:1px 5px;
  border-radius:3px;color:var(--ink-2);word-break:break-word}
.up{color:var(--good)} .dn{color:var(--crit)}

.kpis{display:grid;grid-template-columns:repeat(auto-fit,minmax(272px,1fr));gap:11px;margin:22px 0 8px}
.kpi{background:var(--surface);border:1px solid var(--rule);border-radius:7px;padding:13px 14px;
  border-top:2.5px solid var(--brass)}
.kpi.warn{border-top-color:var(--warn)} .kpi.crit{border-top-color:var(--crit)}
.kpi-l{font-family:var(--mono);font-size:10px;letter-spacing:.1em;text-transform:uppercase;
  color:var(--ink-3);margin-bottom:6px}
.kpi-v{font-family:var(--mono);font-size:24px;font-weight:600;letter-spacing:-.02em;
  font-variant-numeric:tabular-nums;line-height:1.1}
.kpi-s{font-size:12.2px;color:var(--ink-3);margin-top:4px;line-height:1.42}

.chart{width:100%;height:auto;display:block;margin:6px 0 2px;overflow:visible}
.grid{stroke:var(--rule-2);stroke-width:1}
.ax{font-family:var(--mono);font-size:10.5px;fill:var(--ink-3)}
.ax-r{text-anchor:end} .ax-c{text-anchor:middle} .ax-e{text-anchor:end}
.bar-a{fill:var(--brass)} .bar-b{fill:var(--rule)}
.seg-a{fill:var(--brass)} .seg-b{fill:var(--brass-2);opacity:.62} .seg-c{fill:var(--ink-3);opacity:.5}
.seg-t{font-family:var(--mono);font-size:11px;fill:#fff;text-anchor:middle;font-weight:600}
.line{fill:none;stroke:var(--brass);stroke-width:2;stroke-linejoin:round;stroke-linecap:round}
.area{fill:var(--brass);opacity:.09}
.dot{fill:var(--brass)} .dot-end{fill:var(--brass);stroke:var(--bg);stroke-width:2}
.thresh{stroke:var(--crit);stroke-width:1.3;stroke-dasharray:4 3}
.thresh-t{fill:var(--crit);font-size:10px}
.legend{display:flex;gap:16px;flex-wrap:wrap;margin:2px 0 4px}
.lg{display:flex;align-items:center;gap:6px;font-size:12px;color:var(--ink-3)}
.sw{width:10px;height:10px;border-radius:2px;display:inline-block}
.sw-a{background:var(--brass)} .sw-b{background:var(--brass-2);opacity:.62} .sw-c{background:var(--ink-3);opacity:.5}

.tw{overflow-x:auto;margin:14px 0;border:1px solid var(--rule);border-radius:7px;background:var(--surface)}
table{width:100%;border-collapse:collapse;font-size:13.4px;min-width:520px}
th{font-family:var(--mono);font-size:10px;letter-spacing:.09em;text-transform:uppercase;color:var(--ink-3);
  text-align:left;padding:10px 13px;border-bottom:1px solid var(--rule);font-weight:500;
  background:var(--surface-2);white-space:nowrap}
td{padding:10px 13px;border-bottom:1px solid var(--rule-2);vertical-align:top;line-height:1.5}
tr:last-child td{border-bottom:none}
tbody tr:last-child{background:var(--surface-2)}
table.num td{font-variant-numeric:tabular-nums}
table.num td:not(:first-child){font-family:var(--mono);font-size:12.6px;white-space:nowrap}

.chip{display:inline-block;font-family:var(--mono);font-size:10px;font-weight:600;letter-spacing:.05em;
  padding:2px 7px;border-radius:3px;white-space:nowrap;text-transform:uppercase}
.chip-done{background:var(--good-soft);color:var(--good)}
.chip-part{background:var(--brass-soft);color:var(--brass)}
.chip-watch{background:var(--warn-soft);color:var(--warn)}
.chip-crit{background:var(--crit-soft);color:var(--crit)}

.callout{background:var(--surface);border:1px solid var(--rule);border-left:3px solid var(--brass);
  border-radius:6px;padding:16px 18px;margin:20px 0}
.callout-warn{border-left-color:var(--warn)} .callout-crit{border-left-color:var(--crit)}
.callout-h{font-family:var(--mono);font-size:10.5px;letter-spacing:.09em;text-transform:uppercase;
  color:var(--brass);margin-bottom:8px;font-weight:600}
.callout-warn .callout-h{color:var(--warn)} .callout-crit .callout-h{color:var(--crit)}
.callout p{margin:0 0 10px;font-size:14.6px}.callout p:last-child{margin-bottom:0}

.qa{display:flex;flex-direction:column;gap:1px;background:var(--rule);border:1px solid var(--rule);
  border-radius:7px;overflow:hidden;margin:16px 0}
.qa-row{display:grid;grid-template-columns:minmax(150px,.33fr) 1fr;gap:18px;background:var(--surface);padding:15px 17px}
.qa-q{font-family:var(--serif);font-size:16px;font-weight:600;color:var(--brass);line-height:1.3}
.qa-a{font-size:14.4px;color:var(--ink-2);line-height:1.56}
@media(max-width:640px){.qa-row{grid-template-columns:1fr;gap:7px}}

.tri{display:grid;grid-template-columns:repeat(auto-fit,minmax(232px,1fr));gap:12px;margin:18px 0}
.tri-card{background:var(--surface);border:1px solid var(--rule);border-radius:7px;padding:15px 16px;
  border-top:3px solid var(--brass)}
.tri-crit{border-top-color:var(--crit)} .tri-warn{border-top-color:var(--warn)}
.tri-b{border-top-color:var(--warn)} .tri-c{border-top-color:var(--good)}
.tri-h{font-family:var(--serif);font-size:16.5px;font-weight:600;margin-bottom:8px;line-height:1.25}
.tri-card p{font-size:13.8px;margin:0 0 9px;color:var(--ink-2)}
.tri-f{font-family:var(--mono);font-size:11.2px;color:var(--ink-3);border-top:1px solid var(--rule-2);
  padding-top:9px;margin-bottom:0!important;line-height:1.45}

ul.bul{margin:12px 0;padding-left:0;list-style:none;max-width:76ch}
ul.bul li{position:relative;padding-left:19px;margin-bottom:9px;font-size:14.6px;line-height:1.56}
ul.bul li::before{content:"";position:absolute;left:3px;top:9px;width:5px;height:5px;
  background:var(--brass);border-radius:1px}
ol.steps{margin:12px 0;padding-left:0;list-style:none;counter-reset:s;max-width:76ch}
ol.steps li{position:relative;padding-left:31px;margin-bottom:11px;font-size:14.6px;line-height:1.56;counter-increment:s}
ol.steps li::before{content:counter(s);position:absolute;left:0;top:1px;width:20px;height:20px;
  background:var(--brass-soft);color:var(--brass);border-radius:3px;font-family:var(--mono);
  font-size:11px;font-weight:700;display:flex;align-items:center;justify-content:center}

footer{margin-top:56px;padding-top:18px;border-top:1px solid var(--rule);font-family:var(--mono);
  font-size:11px;color:var(--ink-3);line-height:1.7}
"""

JS = """
const tabs=[...document.querySelectorAll('.tab')];
function go(id){
  tabs.forEach(t=>{const on=t.dataset.go===id;t.setAttribute('aria-selected',on?'true':'false');});
  document.querySelectorAll('.panel').forEach(p=>{
    const on=p.id==='p-'+id; p.classList.toggle('on',on); p.hidden=!on;});
  const t=document.getElementById('tab-'+id); if(t) t.scrollIntoView({block:'nearest',inline:'center'});
  window.scrollTo({top:0,behavior:'instant'});
}
tabs.forEach(t=>t.addEventListener('click',()=>go(t.dataset.go)));
document.querySelectorAll('a.jump').forEach(a=>a.addEventListener('click',e=>{e.preventDefault();go(a.dataset.go);}));
document.addEventListener('keydown',e=>{
  if(e.target.classList.contains('tab')){
    const i=tabs.indexOf(e.target);
    if(e.key==='ArrowRight'&&i<tabs.length-1){tabs[i+1].focus();go(tabs[i+1].dataset.go);}
    if(e.key==='ArrowLeft'&&i>0){tabs[i-1].focus();go(tabs[i-1].dataset.go);}
  }});
"""
