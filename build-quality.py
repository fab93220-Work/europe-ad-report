#!/usr/bin/env python3
"""Standalone before/after view: traffic quality, led by orders per session."""
import importlib.util, os
spec = importlib.util.spec_from_file_location("engine", os.path.join(os.path.dirname(__file__), "engine.py"))
E = importlib.util.module_from_spec(spec); spec.loader.exec_module(E)
grouped_bars = E.grouped_bars

OUT = "/home/user/europe-ad-report/quality-before-after.html"

# ---- sessions (GA4) ----
CHAN = [  # channel, sess26, sess25, rev26, rev25, eng26, eng25
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
GDEV = [("Mobile",13819,4925,4.57,8.77,.740,.791),
        ("Desktop",3091,2674,14.53,12.34,.782,.880),
        ("Tablet",261,178,5.20,16.16,.747,.860)]
S26 = sum(c[1] for c in CHAN); S25 = sum(c[2] for c in CHAN)

# ---- orders (WooCommerce, non-refunded) ----
O26, O25 = 1074, 684
NET26, NET25 = 350730, 218149
OPS26, OPS25 = O26/S26, O25/S25
MONTH = [  # month, orders26, aov26, coupon26, items26, orders25, aov25, coupon25, items25
    ("Jun", 455, 343, .567, 3.56, 271, 308, .661, 3.33),
    ("Jul", 477, 302, .495, 3.02, 303, 314, .700, 3.46),
    ("Aug*",142, 358, .556, 3.70, 110, 359, .755, 3.49),
]

def chip(k,t): return f'<span class="chip chip-{k}">{t}</span>'
def kpi(l,v,s="",tone=""):
    return (f'<div class="kpi {tone}"><div class="kpi-l">{l}</div>'
            f'<div class="kpi-v">{v}</div><div class="kpi-s">{s}</div></div>')
def table(h,rows,cls=""):
    th="".join(f"<th>{x}</th>" for x in h)
    tr="".join("<tr>"+"".join(f"<td>{c}</td>" for c in r)+"</tr>" for r in rows)
    return f'<div class="tw"><table class="{cls}"><thead><tr>{th}</tr></thead><tbody>{tr}</tbody></table></div>'
def delta(a,b,inv=False):
    if not b: return "—"
    d=a/b-1; good=(d<0) if inv else (d>=0)
    return f"<b class='{'up' if good else 'dn'}'>{d:+.0%}</b>"

orows=[
 ["<b>Orders per session</b>", f"{OPS25:.2%}", f"<b>{OPS26:.2%}</b>", delta(OPS26,OPS25), chip("done","Held while scaling 53%")],
 ["<b>Orders</b>", f"{O25:,}", f"<b>{O26:,}</b>", delta(O26,O25), "Volume up by more than half"],
 ["<b>Sessions</b>", f"{S25:,}", f"<b>{S26:,}</b>", delta(S26,S25), "The denominator grew hard"],
 ["<b>Orders using a coupon</b>", "69.3%", "<b>53.4%</b>", delta(.534,.693,inv=True), chip("done","16 points fewer")],
 ["<b>AOV</b>", "£319", "<b>£327</b>", delta(327,319), "Up slightly"],
 ["<b>Items per order</b>", "3.42", "<b>3.34</b>", delta(3.34,3.42), "Marginally smaller baskets"],
 ["<b>New customers</b>", "69.6%", "<b>69.6%</b>", "0%", "Unchanged"],
 ["<b>Refund rate</b>", "5.5%", "<b>4.1%</b>", delta(.041,.055,inv=True), chip("done","Improved")],
]
mrows=[]
for nm,o26,a26,c26,i26,o25,a25,c25,i25 in MONTH:
    mrows.append([f"<b>{nm}</b>", f"{o25:,}", f"{o26:,}", delta(o26,o25),
                  f"£{a25}", f"£{a26}", delta(a26,a25), f"{c25:.1%}", f"{c26:.1%}", delta(c26,c25,inv=True)])
crows=[]
for nm,s26,s25,r26,r25,e26,e25 in CHAN:
    crows.append([f"<b>{nm}</b>", f"£{r25/s25:.2f}", f"£{r26/s26:.2f}", delta(r26/s26,r25/s25),
                  f"{s25:,}", f"{s26:,}", delta(s26,s25)])
ps26=sum(c[1] for c in CHAN if c[0] in PAID); ps25=sum(c[2] for c in CHAN if c[0] in PAID)
pr26=sum(c[3] for c in CHAN if c[0] in PAID); pr25=sum(c[4] for c in CHAN if c[0] in PAID)
tr26=sum(c[3] for c in CHAN); tr25=sum(c[4] for c in CHAN)
crows.append(["<b>Paid total</b>", f"<b>£{pr25/ps25:.2f}</b>", f"<b>£{pr26/ps26:.2f}</b>",
              delta(pr26/ps26,pr25/ps25), f"<b>{ps25:,}</b>", f"<b>{ps26:,}</b>", delta(ps26,ps25)])
crows.append(["<b>Site total</b>", f"<b>£{tr25/S25:.2f}</b>", f"<b>£{tr26/S26:.2f}</b>",
              delta(tr26/S26,tr25/S25), f"<b>{S25:,}</b>", f"<b>{S26:,}</b>", delta(S26,S25)])
devrows=[]
for nm,s26,s25,rps26,rps25,e26,e25 in GDEV:
    devrows.append([f"<b>{nm}</b>", f"{s25/7777:.1%}", f"{s26/17171:.1%}",
                    f"£{rps25:.2f}", f"£{rps26:.2f}", delta(rps26,rps25),
                    f"{e25:.1%}", f"{e26:.1%}", delta(e26,e25)])

CSS_EXTRA = """
.hero{background:var(--surface);border:1px solid var(--rule);border-left:3px solid var(--brass);
 border-radius:7px;padding:20px 22px;margin:22px 0}
.hero h3{margin-top:0}
.big{font-family:var(--mono);font-size:40px;font-weight:600;letter-spacing:-.02em;line-height:1.05;
 font-variant-numeric:tabular-nums}
.bigrow{display:flex;gap:34px;flex-wrap:wrap;align-items:flex-end;margin:6px 0 4px}
.bigrow div span{display:block;font-family:var(--mono);font-size:10px;letter-spacing:.1em;
 text-transform:uppercase;color:var(--ink-3);margin-bottom:5px}
"""

DOC = f"""<title>LRD — Traffic Quality, Before vs After</title>
<style>{E.CSS}{CSS_EXTRA}</style>
<div class="wrap">
<header class="masthead">
  <p class="kicker">Lincs Rads Direct · Working draft</p>
  <h1>Traffic quality: before vs after</h1>
  <p class="sub">Did the traffic I bought convert as well as it used to, or did I just buy more of it?
  Led by orders per session, which strips out order value — that is price and range, not media.</p>
  <div class="meta">
    <span>1 Jun – 10 Aug <b>2026 vs 2025</b></span>
    <span>Sources <b>GA4 + order export</b></span>
    <span>Orders <b>{O26:,}</b> vs {O25:,}</span>
    <span>Sessions <b>{S26:,}</b> vs {S25:,}</span>
  </div>
</header>

<h2>Orders per session</h2>
<div class="hero">
  <div class="bigrow">
    <div><span>Before · 1 Jun–10 Aug 25</span><div class="big">{OPS25:.2%}</div></div>
    <div><span>After · 1 Jun–10 Aug 26</span><div class="big" style="color:var(--brass)">{OPS26:.2%}</div></div>
    <div><span>Change</span><div class="big"><span class="up" style="font-size:40px;display:inline">+{OPS26/OPS25-1:.1%}</span></div></div>
    <div><span>On sessions</span><div class="big">+{S26/S25-1:.0%}</div></div>
  </div>
  <p style="margin-top:14px"><b>Conversion held while volume grew by half.</b> That is the answer to the only
  question that matters about my half of the job: scaling paid traffic 57% did not mean scraping the barrel.
  If the extra traffic had been poor, this number would have fallen — it went up slightly.</p>
</div>

<h2>Order quality, before vs after</h2>
{table(["Measure","Before<br>1 Jun–10 Aug 25","After<br>1 Jun–10 Aug 26","Change","Read"], orows, "num")}

<h2>Month by month</h2>
{table(["","Orders before","Orders after","Change","AOV before","AOV after","Change","Coupon before","Coupon after","Change"], mrows, "num")}
<p class="note">*August is 1–10 only. July is the soft month: AOV dipped to £302 and items per order to 3.02.
August recovered to £358 and 3.70 — the strongest basket of the period.</p>

<h2>What coupons actually do</h2>
<div class="callout callout-warn">
  <div class="callout-h">This complicates the "cut discounting" advice</div>
  <p>Splitting this year's orders by whether a coupon was used:</p>
</div>
{table(["2026 orders","Orders","Share","AOV","Items per order"],[
 ["<b>With a coupon</b>","573","53.4%","<b>£372</b>","<b>3.90</b>"],
 ["<b>Without</b>","501","46.6%","£275","2.70"],
 ["<b>Difference</b>","","","<b>+35%</b>","<b>+44%</b>"],
],"num")}
<p>Coupon orders are worth <b>35% more</b> and contain <b>44% more items</b>. So discounting is not simply
margin thrown away — it is associated with materially bigger baskets.</p>
<p class="note"><b>Association, not proof of cause.</b> It may be that codes drive bigger baskets, or that
customers planning a big multi-room purchase go looking for a code first. Those two have opposite
implications: the first says keep discounting, the second says the discount is being given to people who
would have bought anyway. Worth resolving before peak, and it is a question for the business rather than
for me — but it does mean "cut the discount rate" is too blunt as an instruction.</p>

<h2>By channel — value per session</h2>
<div class="callout">
  <div class="callout-h">Why this section is revenue and not orders</div>
  <p>Orders per session cannot be split by channel with the data I have: the GA4 export carries no
  transactions dimension, and order-level channel data is not reliable enough to use. Revenue per session is
  the only channel-level quality measure available today. The export that fixes this is specified at the
  bottom of this page.</p>
</div>
{table(["Channel","RPS before","RPS after","Change","Sessions before","Sessions after","Volume"], crows, "num")}

{grouped_bars([(c[0].replace(" Ads",""), [(c[3]/c[1],"bar-a"),(c[4]/c[2],"bar-b")]) for c in CHAN if c[0] in PAID], axis_fmt=lambda v: f"£{v:,.0f}", tip_fmt=lambda v: f"£{v:,.2f}")}
<div class="legend"><span class="lg"><i class="sw sw-a"></i>This year</span><span class="lg"><i class="sw sw-b"></i>Last year</span></div>
<p class="note">Microsoft is the strongest paid channel at <b>£10.71</b> per session and improving. Meta is
weakest at <b>£1.20</b> — roughly one ninth of Microsoft — which is the clearest justification for moving
budget out of it.</p>

<h2>Why Google's number fell — mostly device mix</h2>
<p>Google Ads revenue per session dropped 37%, £10.17 to £6.37. Most of that is not traffic quality: we
bought far more mobile, and mobile monetises at a third of desktop <i>on this site</i>.</p>
{table(["Device","Share before","Share after","RPS before","RPS after","Change","Eng. before","Eng. after","Change"], devrows, "num")}
{table(["Google Ads revenue per session","Value","Read"],[
 ["Actual, last year","£10.17","63% of sessions were mobile"],
 ["Actual, this year","£6.37","81% of sessions were mobile"],
 ["<b>This year, at last year's device mix</b>","<b>£8.01</b>","<b>−21% rather than −37%</b>"],
 ["Device mix effect","£1.64 of the £3.80 fall",chip("watch","43% of the decline is mix, not quality")],
],"num")}

<div class="hero">
  <h3>Engagement and monetisation moved independently</h3>
  <p>On Google Ads <b>desktop</b>, engagement rate <i>fell</i> 88.0% → 78.2%, yet revenue per session
  <i>rose</i> £12.34 → £14.53. On <b>mobile</b>, engagement fell by a similar proportion (79.1% → 74.0%) but
  revenue per session <b>halved</b>, £8.77 → £4.57.</p>
  <p>The same change in engagement produced opposite outcomes on the two devices. The difference is not in
  the traffic — it is in what happens after it lands. A six-point drop in engagement cannot explain a 48%
  fall in revenue per session.</p>
  <p><b>This is the clearest evidence for where the boundary sits.</b> Engagement — did the right person
  arrive and take an interest — is mine, and it moved a few points. Monetisation — did the site turn that
  interest into an order — is not, and on mobile it fell by half.</p>
</div>

<h2>One result that has not worked yet</h2>
<div class="callout callout-warn">
  <div class="callout-h">Past-purchaser exclusion, 31 July</div>
  <p>Excluding past purchasers from all PMax campaigns was meant to push new-customer acquisition.
  New-customer share since: <b>68.4%</b>, against 69.9% before. It has not moved.</p>
  <p>AOV over the same window rose £321 → £359, so it has not been costly. And new customers are worth more
  than returning ones anyway — <b>£365 AOV against £238</b> — so the strategy is right on value even though
  the mix has not shifted. Ten days and 158 orders is too small to call. Reporting properly at 30 days.</p>
</div>

<h2>What unlocks orders per session by channel</h2>
{table(["Export needed","Where","What it gives"],[
 ["<b>Sessions + Ecommerce purchases by Session source / medium</b>","GA4 → Reports → Acquisition → Traffic acquisition. Pencil icon to add <i>Ecommerce purchases</i> (or <i>Key events</i> if purchase is the only key event).","Turns the channel table above into orders per session. Run for both windows."],
 ["<b>Same, split by device</b>","GA4 → Explore → Free form. Rows: Session source/medium + Device category. Metrics: Sessions, Ecommerce purchases, Purchase revenue.","Separates the mobile effect from the channel effect"],
 ["<b>Order export with a SKU column</b>","WooCommerce order export, add SKU or product ID per line item.","Joins orders to the profitability file for margin weighted by units actually sold. Product names alone match only 4.8% of units."],
])}

<h2>Caveats</h2>
{table(["Caveat","Detail"],[
 ["<b>Orders per session is site-wide</b>","Orders come from the order export, sessions from GA4. The ratio is sound at site level but cannot be attributed to a channel."],
 ["<b>GA4 captured less revenue this year</b>","£337,185 of £365,233 (92.3%) against £219,219 of £220,623 (99.4%) last year. Roughly £28,000 now unattributed to any channel, up from £1,400. That understates every channel's revenue per session this year."],
 ["<b>Last-click attribution</b>","GA4 credits the last non-direct source. Meta typically loses out to search under this model — its £1.20 is a floor. Direct at £20.42 is partly other channels' work arriving uncredited."],
 ["<b>Refunded orders excluded</b>","1,074 of 1,120 orders in 2026 and 684 of 724 in 2025, after removing refunded and on-hold."],
])}

<footer>
  Working draft, separate from the main review pack. Orders and order quality from the WooCommerce order
  export; sessions, revenue and engagement from GA4 traffic acquisition by session source/medium and device.
  1 Jun – 10 Aug 2026 against the same window 2025.
</footer>
</div>"""

open(OUT,"w").write(DOC)
print(f"wrote {OUT} ({len(DOC):,} bytes)")
