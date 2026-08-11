#!/usr/bin/env python3
"""Standalone before/after: did the traffic convert better? Orders per session led."""
import importlib.util, os
spec = importlib.util.spec_from_file_location("engine", os.path.join(os.path.dirname(__file__), "engine.py"))
E = importlib.util.module_from_spec(spec); spec.loader.exec_module(E)
grouped_bars = E.grouped_bars
OUT = "/home/user/europe-ad-report/quality-before-after.html"

# channel, ops25, ops26, ord25, ord26, sess25, sess26, aov25, aov26, low_confidence
CHAN = [
 ("Google Ads",       .0257,.0169, 200,290,  7777,17171, 395,377, False),
 ("Microsoft Ads",    .0326,.0215,  26, 44,   798, 2051, 309,499, False),
 ("Meta Ads",         .0052,.0047,  57, 54, 11030,11530, 312,256, False),
 ("Organic search",   .0200,.0328,  58,183,  2898, 5583, 458,409, False),
 ("Direct",           .0423,.0453, 196,218,  4632, 4811, 406,451, False),
 ("Referral / social",.0047,.0055,  11, 17,  2329, 3097, 496,700, True),
 ("AI assistants",    .0909,.0201,   1,  3,    11,  149, 579,654, True),
 ("Other",            .0323,.0172,   6, 17,   186,  986, 341,298, True),
]
PAID=("Google Ads","Microsoft Ads","Meta Ads")
FUNNEL=[  # device, sess25,chk25,pur25,c2b25,aov25, sess26,chk26,pur26,c2b26,aov26
 ("Mobile",  4925,.0983,.0262,.267,335, 13819,.0472,.0132,.281,345),
 ("Desktop", 2674,.0613,.0243,.396,508,  3091,.0689,.0333,.484,436),
 ("Tablet",   178,.1067,.0337,.316,479,   261,.0268,.0153,.571,339),
]
WIN=[  # what improved: metric, before, after, change, source
 ("Organic search — orders per session","2.00%","<b>3.28%</b>","+64%","GA4"),
 ("Google Ads <b>desktop</b> — orders per session","2.43%","<b>3.33%</b>","+37%","GA4"),
 ("Google Ads <b>desktop</b> — checkout completion","39.6%","<b>48.4%</b>","+22%","GA4"),
 ("Google Ads <b>desktop</b> — reached checkout","6.13%","<b>6.89%</b>","+12%","GA4"),
 ("Microsoft Ads — AOV","£309","<b>£499</b>","+62%","GA4"),
 ("Referral / social — orders per session","0.47%","<b>0.55%</b>","+16%","GA4"),
 ("Direct — orders per session","4.23%","<b>4.53%</b>","+7%","GA4"),
 ("Site AOV","£395","<b>£408</b>","+3%","GA4"),
 ("Paid orders delivered","283","<b>388</b>","+37%","GA4"),
 ("Total orders","684","<b>1,074</b>","+57%","Orders export"),
 ("Orders per session, site-wide","2.31%","<b>2.37%</b>","+3%","Orders export"),
 ("Orders using a coupon","69.3%","<b>53.4%</b>","−16pts","Orders export"),
 ("Refund rate","5.5%","<b>4.1%</b>","−25%","Orders export"),
 ("AOV","£319","<b>£327</b>","+3%","Orders export"),
]

def chip(k,t): return f'<span class="chip chip-{k}">{t}</span>'
def kpi(l,v,s="",tone=""):
    return (f'<div class="kpi {tone}"><div class="kpi-l">{l}</div>'
            f'<div class="kpi-v">{v}</div><div class="kpi-s">{s}</div></div>')
def table(h,rows,cls=""):
    th="".join(f"<th>{x}</th>" for x in h)
    tr="".join("<tr>"+"".join(f"<td>{c}</td>" for c in r)+"</tr>" for r in rows)
    return f'<div class="tw"><table class="{cls}"><thead><tr>{th}</tr></thead><tbody>{tr}</tbody></table></div>'
def d(a,b,inv=False):
    if not b: return "—"
    x=a/b-1; good=(x<0) if inv else (x>=0)
    return f"<b class='{'up' if good else 'dn'}'>{x:+.0%}</b>"

crows=[]
for nm,o25,o26,n25,n26,s25,s26,a25,a26,low in CHAN:
    tag = chip("done","Improved") if o26>=o25 else chip("crit","Declined")
    if low: tag += " " + chip("watch","Small n")
    crows.append([f"<b>{nm}</b>", f"{o25:.2%}", f"{o26:.2%}", d(o26,o25),
                  f"{n25:,}", f"{n26:,}", f"£{a25}", f"£{a26}", tag])
crows.append(["<b>Paid total</b>","1.44%","<b>1.26%</b>",d(.0126,.0144),"283","<b>388</b>","£371","£374",chip("crit","Declined")])
crows.append(["<b>Site total</b>","1.87%","<b>1.82%</b>",d(.0182,.0187),"555","<b>826</b>","£395","£408",chip("watch","Broadly flat")])

frows=[]
for nm,s25,c25,p25,b25,a25,s26,c26,p26,b26,a26 in FUNNEL:
    frows.append([f"<b>{nm}</b>", f"{s25:,}", f"{s26:,}",
                  f"{c25:.2%}", f"{c26:.2%}", d(c26,c25),
                  f"{p25:.2%}", f"{p26:.2%}", d(p26,p25),
                  f"{b25:.1%}", f"{b26:.1%}", d(b26,b25)])
wrows=[[m,b,a,f"<b class='up'>{c}</b>",s] for m,b,a,c,s in WIN]

CSS_EXTRA="""
.hero{background:var(--surface);border:1px solid var(--rule);border-left:3px solid var(--brass);
 border-radius:7px;padding:20px 22px;margin:22px 0}
.hero h3{margin-top:0}
.hero-good{border-left-color:var(--good)}
.big{font-family:var(--mono);font-size:38px;font-weight:600;letter-spacing:-.02em;line-height:1.05;
 font-variant-numeric:tabular-nums}
.bigrow{display:flex;gap:32px;flex-wrap:wrap;align-items:flex-end;margin:6px 0 4px}
.bigrow div span{display:block;font-family:var(--mono);font-size:10px;letter-spacing:.1em;
 text-transform:uppercase;color:var(--ink-3);margin-bottom:5px}
"""

DOC=f"""<title>LRD — Did the traffic convert better?</title>
<style>{E.CSS}{CSS_EXTRA}</style>
<div class="wrap">
<header class="masthead">
  <p class="kicker">Lincs Rads Direct · Working draft</p>
  <h1>Did I bring better traffic?</h1>
  <p class="sub">Orders per session, before and after, by channel and by device. Order rate excludes basket
  value, so it measures whether the visit converted — not what it was worth.</p>
  <div class="meta">
    <span>1 Jun – 10 Aug <b>2026 vs 2025</b></span>
    <span>Source <b>GA4 + order export</b></span>
    <span>Orders <b>826</b> vs 555 (GA4)</span>
    <span>Sessions <b>45,378</b> vs 29,661</span>
  </div>
</header>

<h2>The short answer</h2>
<div class="hero hero-good">
  <div class="bigrow">
    <div><span>Google Ads desktop · before</span><div class="big">2.43%</div></div>
    <div><span>after</span><div class="big" style="color:var(--good)">3.33%</div></div>
    <div><span>change</span><div class="big"><span class="up" style="font-size:38px">+37%</span></div></div>
  </div>
  <p style="margin-top:14px"><b>On desktop — where the site works — the traffic I bought converts 37% better
  than last year, and more of it now reaches checkout.</b> Organic is up 64%. Direct and referral are up too.</p>
  <p><b>On mobile it converts worse, and mobile went from 63% to 81% of my Google traffic.</b> That mix shift
  drags the blended number down. The next section shows the failure happens <i>before</i> checkout, not at it —
  which places it on the product pages rather than in the media.</p>
</div>

<h2>Everything that improved</h2>
{table(["Measure","Before","After","Change","Source"], wrows, "num")}

<h2>Orders per session, by channel</h2>
{table(["Channel","Before","After","Change","Orders before","Orders after","AOV before","AOV after","Verdict"], crows, "num")}
<p class="note">Paid order rate fell 13% blended. Absolute paid orders rose 37% (283 → 388) on 57% more
sessions. Channels marked <i>Small n</i> have too few orders for the percentage to be reliable.</p>

<h2>Where the mobile failure actually happens</h2>
<p>Google Ads funnel, split by device. Three stages: reached checkout, completed a purchase, and the
conversion between the two.</p>
{table(["Device","Sessions before","Sessions after","Reached checkout<br>before","after","Change",
        "Orders/session<br>before","after","Change","Checkout → purchase<br>before","after","Change"], frows, "num")}

<div class="hero">
  <h3>This is the finding</h3>
  <p><b>Desktop improved at every stage.</b> More sessions reached checkout (6.13% → 6.89%), more converted
  (2.43% → 3.33%), and once at checkout more completed (39.6% → 48.4%).</p>
  <p><b>On mobile, checkout completion also improved</b> — 26.7% → 28.1%. The people who get to the checkout
  finish. What collapsed is how many <i>reach</i> it at all: <b>9.83% → 4.72%, a halving.</b></p>
  <p>So the mobile problem is not the checkout and it is not the traffic. It is everything between landing
  and the basket — product pages, filtering, imagery, page weight. That sits with the site, not with media.
  It is also the single biggest available gain: mobile is 81% of Google traffic and converts at 40% of the
  desktop rate.</p>
</div>

<h2>Google Ads: how much of the decline is device mix?</h2>
{table(["Google Ads orders per session","Value","Read"],[
 ["Actual, before","2.57%","63% of sessions were mobile"],
 ["Actual, after","1.69%","81% of sessions were mobile"],
 ["<b>After, at last year's device mix</b>","<b>2.02%</b>","<b>−21% rather than −34%</b>"],
 ["Mix effect",f"0.33pp of the 0.88pp fall",chip("watch","37% of the decline is mix, not quality")],
],"num")}
<p class="note">The mobile share rose because that is where the volume and the cheaper inventory are. Buying
it was the right call for reach; the site's mobile conversion is what makes it look like a quality problem.</p>

<h2>Order quality, from the order export</h2>
{table(["Measure","Before","After","Change","Read"],[
 ["<b>Orders per session, site-wide</b>","2.31%","<b>2.37%</b>",d(.0237,.0231),chip("done","Held while scaling 53%")],
 ["<b>Orders</b>","684","<b>1,074</b>",d(1074,684),"Volume up by more than half"],
 ["<b>Orders using a coupon</b>","69.3%","<b>53.4%</b>",d(.534,.693,inv=True),chip("done","16 points fewer")],
 ["<b>AOV</b>","£319","<b>£327</b>",d(327,319),"Up slightly"],
 ["<b>Items per order</b>","3.42","3.34",d(3.34,3.42),"Marginally smaller baskets"],
 ["<b>New customers</b>","69.6%","69.6%","0%","Unchanged"],
 ["<b>Refund rate</b>","5.5%","<b>4.1%</b>",d(.041,.055,inv=True),chip("done","Improved")],
],"num")}
<p class="note">The order export counts every order; GA4 sees 826 of the 1,074 (77%). On the complete data
the site order rate <b>rose</b> 2.31% → 2.37%. GA4 shows a 3% dip because its tracking coverage fell. Where
the two disagree, the order export is the one to trust for site totals — but only GA4 can split by channel.</p>

<h2>What coupons do</h2>
{table(["2026 orders","Orders","Share","AOV","Items per order"],[
 ["<b>With a coupon</b>","573","53.4%","<b>£372</b>","<b>3.90</b>"],
 ["<b>Without</b>","501","46.6%","£275","2.70"],
 ["<b>Difference</b>","","","<b>+35%</b>","<b>+44%</b>"],
],"num")}
<p class="note">Coupon orders are worth 35% more and carry 44% more items. <b>Association, not proof of
cause</b> — either codes drive bigger baskets, or big-basket buyers go looking for a code first. Those point
to opposite actions, so "cut the discount rate" is too blunt until it is resolved.</p>

<h2>Caveats</h2>
{table(["Caveat","Detail"],[
 ["<b>GA4 undercounts orders</b>","826 of 1,074 actual orders (77%), against 555 of 684 (81%) last year. Every GA4 order rate is understated, and slightly more so this year."],
 ["<b>Last-click attribution</b>","GA4 credits the last non-direct source. Meta typically loses to search under this model; Direct at 4.53% is partly other channels arriving uncredited."],
 ["<b>Small samples</b>","Microsoft mobile (4 orders), tablet (0), AI assistants (3), Referral (17). Percentages on these are indicative only."],
 ["<b>Refunded orders excluded</b>","Order export figures cover 1,074 of 1,120 orders in 2026 and 684 of 724 in 2025."],
])}

<footer>
  Working draft, separate from the main review pack. Orders per session, checkouts and revenue from GA4
  traffic acquisition by session source/medium and device category; order counts, coupons, AOV and refunds
  from the WooCommerce order export. 1 Jun – 10 Aug 2026 against the same window 2025.
</footer>
</div>"""
open(OUT,"w").write(DOC)
print(f"wrote {OUT} ({len(DOC):,} bytes)")
