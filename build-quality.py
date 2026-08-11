#!/usr/bin/env python3
"""Standalone before/after view: traffic quality per session, by channel."""
import importlib.util, os
spec = importlib.util.spec_from_file_location("engine", os.path.join(os.path.dirname(__file__), "engine.py"))
E = importlib.util.module_from_spec(spec); spec.loader.exec_module(E)
grouped_bars = E.grouped_bars

OUT = "/home/user/europe-ad-report/quality-before-after.html"

# channel, sess26, sess25, rev26, rev25, eng26, eng25
CHAN = [
    ("Google Ads",        17171,  7777, 109407, 79091, .748, .823),
    ("Microsoft Ads",      2051,   798,  21972,  8042, .745, .802),
    ("Meta Ads",          11530, 11030,  13801, 17805, .635, .696),
    ("Organic search",     5583,  2898,  74825, 26593, .688, .715),
    ("Direct",             4811,  4632,  98252, 79607, .652, .640),
    ("Referral / social",  3096,  2329,  11895,  5458, .796, .747),
    ("AI assistants",       149,    11,   1963,   579, .617, .636),
    ("Other",               986,   186,   5071,  2044, .414, .344),
]
PAID = ("Google Ads", "Microsoft Ads", "Meta Ads")
GDEV = [  # device, s26, s25, rps26, rps25, eng26, eng25
    ("Mobile",  13819, 4925,  4.57,  8.77, .740, .791),
    ("Desktop",  3091, 2674, 14.53, 12.34, .782, .880),
    ("Tablet",    261,  178,  5.20, 16.16, .747, .860),
]

def chip(k,t): return f'<span class="chip chip-{k}">{t}</span>'
def kpi(l,v,s="",tone=""):
    return (f'<div class="kpi {tone}"><div class="kpi-l">{l}</div>'
            f'<div class="kpi-v">{v}</div><div class="kpi-s">{s}</div></div>')
def table(h,rows,cls=""):
    th="".join(f"<th>{x}</th>" for x in h)
    tr="".join("<tr>"+"".join(f"<td>{c}</td>" for c in r)+"</tr>" for r in rows)
    return f'<div class="tw"><table class="{cls}"><thead><tr>{th}</tr></thead><tbody>{tr}</tbody></table></div>'
def delta(a,b):
    if not b: return "—"
    d=a/b-1
    return f"<b class='{'up' if d>=0 else 'dn'}'>{d:+.0%}</b>"

rows=[]
for nm,s26,s25,r26,r25,e26,e25 in CHAN:
    rps26,rps25 = r26/s26, r25/s25
    tag = chip("done","Improved") if rps26>=rps25 else chip("crit","Declined")
    rows.append([f"<b>{nm}</b>", f"£{rps25:.2f}", f"£{rps26:.2f}", delta(rps26,rps25),
                 f"{s25:,}", f"{s26:,}", delta(s26,s25), tag])
ps26=sum(c[1] for c in CHAN if c[0] in PAID); ps25=sum(c[2] for c in CHAN if c[0] in PAID)
pr26=sum(c[3] for c in CHAN if c[0] in PAID); pr25=sum(c[4] for c in CHAN if c[0] in PAID)
ts26=sum(c[1] for c in CHAN); ts25=sum(c[2] for c in CHAN)
tr26=sum(c[3] for c in CHAN); tr25=sum(c[4] for c in CHAN)
rows.append([f"<b>Paid total</b>", f"<b>£{pr25/ps25:.2f}</b>", f"<b>£{pr26/ps26:.2f}</b>",
             delta(pr26/ps26,pr25/ps25), f"<b>{ps25:,}</b>", f"<b>{ps26:,}</b>",
             delta(ps26,ps25), chip("crit","Declined")])
rows.append([f"<b>Site total</b>", f"<b>£{tr25/ts25:.2f}</b>", f"<b>£{tr26/ts26:.2f}</b>",
             delta(tr26/ts26,tr25/ts25), f"<b>{ts25:,}</b>", f"<b>{ts26:,}</b>",
             delta(ts26,ts25), chip("done","Flat")])

devrows=[]
for nm,s26,s25,rps26,rps25,e26,e25 in GDEV:
    devrows.append([f"<b>{nm}</b>", f"{s25/7777:.1%}", f"{s26/17171:.1%}",
                    f"£{rps25:.2f}", f"£{rps26:.2f}", delta(rps26,rps25),
                    f"{e25:.1%}", f"{e26:.1%}", delta(e26,e25)])

CSS_EXTRA = """
.hero{background:var(--surface);border:1px solid var(--rule);border-left:3px solid var(--brass);
 border-radius:7px;padding:20px 22px;margin:22px 0}
.hero h3{margin-top:0}
"""

DOC = f"""<title>LRD — Traffic Quality, Before vs After</title>
<style>{E.CSS}{CSS_EXTRA}</style>
<div class="wrap">
<header class="masthead">
  <p class="kicker">Lincs Rads Direct · Working draft</p>
  <h1>Traffic quality: before vs after</h1>
  <p class="sub">Value per session by channel, this period against the same window last year. A test of
  whether the traffic I bought was worth more per visit, not just larger in volume.</p>
  <div class="meta">
    <span>1 Jun – 10 Aug <b>2026 vs 2025</b></span>
    <span>Source <b>GA4 traffic acquisition</b></span>
    <span>Sessions <b>{ts26:,}</b> vs {ts25:,}</span>
  </div>
</header>

<div class="kpis">
{kpi("Site revenue/session","£7.43","vs £7.39 LY &nbsp;<b class='up'>+1%</b>")}
{kpi("Paid revenue/session","£4.72","vs £5.35 LY &nbsp;<b class='dn'>−12%</b>","warn")}
{kpi("Best paid channel","£10.71","Microsoft Ads, up 6%")}
{kpi("Weakest paid channel","£1.20","Meta Ads, down 26%","crit")}
</div>

<h2>Revenue per session, by channel</h2>
{table(["Channel","Before<br>1 Jun–10 Aug 25","After<br>1 Jun–10 Aug 26","Change",
        "Sessions before","Sessions after","Volume","Verdict"], rows, "num")}

<div class="hero">
  <h3>What this says, plainly</h3>
  <p><b>Site revenue per session is flat (+1%) on 53% more traffic.</b> That is the headline: we grew volume
  by half without diluting the average value of a visit. Holding value per session while scaling that hard
  is the harder of the two things to do.</p>
  <p>Underneath it, paid fell 12% and organic rose 46%. Microsoft is the strongest paid channel at
  <b>£10.71</b> per session and improving. Meta is the weakest at <b>£1.20</b> — roughly one ninth of
  Microsoft — which is the clearest possible justification for moving budget out of it.</p>
</div>

<h2>Why Google's number fell — it is mostly device mix</h2>
<p>Google Ads revenue per session dropped 37%, from £10.17 to £6.37. Most of that is not traffic quality.
It is that we bought a lot more mobile, and mobile monetises at a third of desktop <i>on this site</i>.</p>

{table(["Device","Share before","Share after","RPS before","RPS after","Change","Eng. before","Eng. after","Change"], devrows, "num")}

{table(["Google Ads revenue per session","Value","Read"],[
 ["Actual, last year","£10.17","63% of sessions were mobile"],
 ["Actual, this year","£6.37","81% of sessions were mobile"],
 ["<b>This year, held at last year's device mix</b>","<b>£8.01</b>","<b>−21% rather than −37%</b>"],
 ["Device mix effect","£1.64 of the £3.80 fall",chip("watch","43% of the decline is mix, not quality")],
],"num")}

<div class="hero">
  <h3>The part that matters: engagement and monetisation moved independently</h3>
  <p>On Google Ads <b>desktop</b>, engagement rate <i>fell</i> 88.0% → 78.2%, yet revenue per session
  <i>rose</i> £12.34 → £14.53. On <b>mobile</b>, engagement fell by a similar proportion (79.1% → 74.0%) but
  revenue per session <b>halved</b>, £8.77 → £4.57.</p>
  <p>The same change in engagement produced opposite outcomes on the two devices. That means the difference
  is not in the traffic — it is in what happens to that traffic after it lands. A 6-point drop in engagement
  cannot explain a 48% fall in revenue per session.</p>
  <p><b>This is the cleanest evidence yet for where the boundary sits.</b> Engagement — did the right person
  arrive and take an interest — is mine, and it moved a few points. Monetisation — did the site turn that
  interest into an order — is not mine, and on mobile it fell by half.</p>
</div>

<h2>Value per session, paid channels</h2>
{grouped_bars([(c[0].replace(" Ads",""), [(c[3]/c[1],"bar-a"),(c[4]/c[2],"bar-b")]) for c in CHAN if c[0] in PAID], axis_fmt=lambda v: f"£{v:,.0f}", tip_fmt=lambda v: f"£{v:,.2f}")}
<div class="legend"><span class="lg"><i class="sw sw-a"></i>This year</span><span class="lg"><i class="sw sw-b"></i>Last year</span></div>
<p class="note">Chart shows £ per session. Microsoft delivers nearly nine times the value per session of Meta,
on a fifth of the volume.</p>

<h2>What is missing: orders per session</h2>
<div class="callout callout-warn">
  <div class="callout-h">The better metric, and why I cannot build it yet</div>
  <p>Revenue per session mixes two things: <b>how often a session buys</b> (mine) and <b>how much it spends
  when it does</b> (not mine — that is price, range and merchandising). Orders per session strips the second
  out and is the cleaner measure of traffic quality.</p>
  <p>The GA4 export I have carries sessions, revenue and engagement, but no transactions dimension — so
  orders per session is not calculable from it.</p>
</div>

{table(["To complete this table, export","Where","Notes"],[
 ["<b>Sessions + Ecommerce purchases by Session source / medium</b>","GA4 → Reports → Acquisition → Traffic acquisition. Use the pencil icon to add <i>Ecommerce purchases</i> (or <i>Key events</i> if purchase is the only key event).","Run twice: 1 Jun–10 Aug 2026 and 1 Jun–10 Aug 2025"],
 ["<b>Same, split by device</b>","GA4 → Explore → Free form. Rows: Session source/medium + Device category. Metrics: Sessions, Ecommerce purchases, Purchase revenue.","Separates the mobile effect from the channel effect"],
])}
<p class="note">With those two, this page becomes orders per session by channel and device, before and after —
which is the number I would actually want to be judged on.</p>

<h2>Two caveats on the figures above</h2>
{table(["Caveat","Detail"],[
 ["<b>GA4 captured less revenue this year</b>","£337,185 of £365,233 (92.3%) against £219,219 of £220,623 (99.4%) last year. Roughly £28,000 of revenue is now unattributed to any channel, up from £1,400. That understates every channel's revenue per session this year and is a tracking problem worth fixing."],
 ["<b>Last-click attribution</b>","GA4 credits the last non-direct source. Meta typically loses out to search under this model — its £1.20 is a floor, not a full picture. Direct at £20.42 per session is partly other channels' work arriving uncredited."],
])}

<footer>
  Working draft, separate from the main review pack. GA4 traffic acquisition by session source/medium and
  device, 1 Jun – 10 Aug 2026 and the same window 2025. Revenue is GA4-attributed and does not reconcile
  exactly to the daily flash — see caveats.
</footer>
</div>"""

open(OUT,"w").write(DOC)
print(f"wrote {OUT} ({len(DOC):,} bytes)")
