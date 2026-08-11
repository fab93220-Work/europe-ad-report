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
def grouped_bars(data, w=680, h=250, pad_l=58, pad_b=34, pad_t=14):
    """data: [(label, [(value,cls),...]), ...]"""
    mx = max(v for _, vs in data for v, _ in vs) * 1.12
    iw, ih = w - pad_l - 12, h - pad_b - pad_t
    n = len(data); gw = iw / n
    s = [f'<svg viewBox="0 0 {w} {h}" class="chart" role="img">']
    for i in range(5):
        y = pad_t + ih * i / 4; val = mx * (1 - i / 4)
        s.append(f'<line x1="{pad_l}" y1="{y:.1f}" x2="{w-12}" y2="{y:.1f}" class="grid"/>')
        s.append(f'<text x="{pad_l-8}" y="{y+4:.1f}" class="ax ax-r">£{val/1000:.0f}k</text>')
    for i, (lab, vals) in enumerate(data):
        k = len(vals); bw = gw * 0.62 / k
        x0 = pad_l + gw * i + gw * 0.19
        for j, (v, cls) in enumerate(vals):
            bh = ih * v / mx
            s.append(f'<rect x="{x0+j*bw:.1f}" y="{pad_t+ih-bh:.1f}" width="{bw-3:.1f}" '
                     f'height="{bh:.1f}" rx="2" class="{cls}"><title>{lab}: £{v:,.0f}</title></rect>')
        s.append(f'<text x="{pad_l+gw*i+gw/2:.1f}" y="{h-11}" class="ax ax-c">{lab}</text>')
    s.append('</svg>')
    return "".join(s)

def line_chart(data, w=680, h=230, pad_l=44, pad_b=36, pad_t=14, thresh=None, fmt="{:.2f}", unit=""):
    import math
    vals = [v for _, v in data]
    lo, hi = min(vals), max(vals)
    if thresh: lo, hi = min(lo, thresh), max(hi, thresh)
    span = (hi - lo) or 1; lo -= span*0.16; hi += span*0.16
    # snap to a readable step so axis labels are round numbers
    raw = (hi - lo) / 3
    mag = 10 ** math.floor(math.log10(raw))
    step = next(m*mag for m in (1, 2, 2.5, 5, 10) if m*mag >= raw)
    lo = math.floor(lo/step)*step; hi = lo + step*3; span = hi - lo
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

def stacked_split(rows, w=680, h=132):
    """rows: [(label, [(seg_label, value, cls),...])]"""
    mx = max(sum(v for _, v, _ in segs) for _, segs in rows)
    s = [f'<svg viewBox="0 0 {w} {h}" class="chart" role="img">']
    bh, gap, x0 = 34, 26, 96
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

# ---------------------------------------------------------------- content
def chip(kind, text):
    return f'<span class="chip chip-{kind}">{text}</span>'

def kpi(label, value, sub="", tone=""):
    return (f'<div class="kpi {tone}"><div class="kpi-l">{label}</div>'
            f'<div class="kpi-v">{value}</div><div class="kpi-s">{sub}</div></div>')

def table(headers, rows, cls=""):
    th = "".join(f"<th>{h}</th>" for h in headers)
    tr = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in rows)
    return f'<div class="tw"><table class="{cls}"><thead><tr>{th}</tr></thead><tbody>{tr}</tbody></table></div>'

SECTIONS = []
def sec(sid, nav, quote, title, body):
    SECTIONS.append((sid, nav, quote, title, body))

# ---- 1. SUMMARY -------------------------------------------------------
sec("summary", "Summary", "What have we learned? Where are we better? Where are we still weak? What are we doing next?",
    "The 90 days in one page", f"""
<p class="lede">Sales are up {NET/LYNET-1:.0%} year on year. That growth is real, it is not a reporting artefact, and it
was bought with {SPEND/LYSPEND-1:.0%} more media. The efficiency question your message raises is the right one — but the
answer is not where I expected it to be, and it is not ROAS.</p>

<div class="kpis">
{kpi("Net sales", f"£{NET:,.0f}", f"vs £{LYNET:,.0f} LY &nbsp;<b class='up'>+{NET/LYNET-1:.0%}</b>")}
{kpi("Orders", f"{ORD:,}", f"vs {LYORD:,} LY &nbsp;<b class='up'>+{ORD/LYORD-1:.0%}</b>")}
{kpi("AOV", f"£{NET/ORD:,.0f}", f"vs £{LYNET/LYORD:,.0f} LY &nbsp;<b class='up'>+{(NET/ORD)/(LYNET/LYORD)-1:.0%}</b>")}
{kpi("Media spend", f"£{SPEND:,.0f}", f"vs £{LYSPEND:,.0f} LY &nbsp;<b class='dn'>+{SPEND/LYSPEND-1:.0%}</b>", "warn")}
{kpi("Blended ROAS", f"{NET/SPEND:.2f}x", f"vs {LYNET/LYSPEND:.2f}x LY &nbsp;<b class='dn'>{(NET/SPEND)/(LYNET/LYSPEND)-1:.0%}</b>", "warn")}
{kpi("Contribution after media", f"£{CONTRIB:,.0f}", f"{CONTRIB/NET:.1%} of net sales", "crit")}
</div>

<h3>The four answers</h3>

<div class="qa">
  <div class="qa-row"><div class="qa-q">What have we learned?</div><div class="qa-a">
  That the profit leak is <b>discounting, not media efficiency</b>. We gave away <b>£{DISC:,.0f}</b> in discount over the
  period — {DISC/GROSS:.1%} of gross sales, rising to {MONTHS[2][8]/MONTHS[2][7]:.1%} in August. Media cost
  £{SPEND:,.0f}. Discount is comparable in size to the entire advertising budget, and it has had none of the scrutiny.</div></div>

  <div class="qa-row"><div class="qa-q">Where are we better?</div><div class="qa-a">
  Sales, orders and AOV are all up double digits. The account is no longer an agency black box: brand is protected,
  PMax can no longer harvest branded conversions, spend has moved out of broad PMax into Search, and every change since
  31 July is logged with a before, an after and a reason. Bing cost data is visible instead of £22,860 of revenue with no cost attached.</div></div>

  <div class="qa-row"><div class="qa-q">Where are we still weak?</div><div class="qa-a">
  Contribution after media is <b>{CONTRIB/NET:.1%}</b> of net sales and falling — {(MONTHS[0][1]*MARGIN-MONTHS[0][5])/MONTHS[0][1]:.1%}
  in June, {(MONTHS[1][1]*MARGIN-MONTHS[1][5])/MONTHS[1][1]:.1%} in July, {(MONTHS[2][1]*MARGIN-MONTHS[2][5])/MONTHS[2][1]:.1%} in August. Cast iron is our
  biggest opportunity and it is currently broken in the feed, on the site and in search at the same time. And
  {35.1:.0f}% of site sessions land on pages that produced no revenue at all.</div></div>

  <div class="qa-row"><div class="qa-q">What are we doing next?</div><div class="qa-a">
  Three things before peak: fix cast iron end to end, put a floor under discounting, and get the account season-ready
  by the end of September. Detail in <a href="#next90" class="jump" data-go="next90">Next 90 days</a>.</div></div>
</div>

<div class="callout callout-crit">
  <div class="callout-h">The one thing to take away</div>
  <p>Every one percentage point we take off the discount rate is worth <b>£{GROSS*0.01:,.0f}</b> over a period like this
  one — against a total contribution after media of <b>£{CONTRIB:,.0f}</b>. Moving discount from
  {DISC/GROSS:.1%} to 10% would add roughly <b>£{GROSS*(DISC/GROSS-0.10):,.0f}</b>, which is more than half the
  contribution the entire trading period generated. No plausible ROAS improvement comes close to that.</p>
</div>

<div class="callout">
  <div class="callout-h">On the ROAS drop, before anyone else raises it</div>
  <p>Blended ROAS fell from {LYNET/LYSPEND:.2f}x to {NET/SPEND:.2f}x. Two things about that comparison. First, last
  July the accounts were close to dormant — LY Google spend that month was £2,412 against £18,889 this year — so the
  {LYNET/LYSPEND:.2f}x is the arithmetic of a near-zero denominator, not a standard we were previously hitting.
  Second, at a daily level the highest-spending third of days still returns <b>4.44x</b> against 4.57x for the middle
  third. Efficiency bends slightly as we scale; it does not fall over. That is the evidence that says we can spend
  into October rather than throttle back.</p>
</div>""")

# ---- 2. BASELINE ------------------------------------------------------
sec("baseline", "Baseline", "What's been done so far",
    "The account I inherited", """
<p class="lede">Recorded in the takeover checklist dated 9 June, before any changes were made. This is the baseline
everything below is measured against.</p>

""" + table(["Finding at takeover","Why it mattered","Status now"], [
    ["PMax running at <b>2.38x</b> vs Paid Search <b>3.09x</b>", "Budget concentrated in the weaker of the two formats", chip("done","Reallocated")],
    ["Brand keywords <b>not excluded</b> from PMax", "PMax harvesting branded conversions and claiming the credit — the single biggest ROAS distortion available", chip("done","Fixed 31 Jul")],
    ["No confirmed brand protection campaign", "Competitors free to bid on our name", chip("done","Live, budget +33%")],
    ["<b>£22,860</b> Bing-attributed revenue with no cost data in GA4", "Flying blind on an entire channel", chip("done","Cost data visible")],
    ["Meta cold prospecting losing an estimated <b>£14k/quarter</b>", "Straight cash burn", chip("done","Prospecting paused")],
    ["Billing on the agency's card; editor not admin access", "Access could be revoked instantly", chip("done","Transferred")],
    ["Bing suspected to be an unmodified Google import", "Overpaying — Bing CPCs run 30–50% cheaper", chip("part","Rebid, still tuning")],
    ["Meta CAPI / server-side tracking unverified", "iOS users invisible to optimisation", chip("watch","Open — see Gaps")],
]) + """
<p class="note">The checklist ran to 24 line items across Google, Bing and Meta. Every critical and high-priority item
is closed or in flight. The two that remain open are named in <a href="#gaps" class="jump" data-go="gaps">Gaps &amp; asks</a>
rather than left implicit.</p>""")

# ---- 3. TRADING -------------------------------------------------------
mrows = []
for nm, net, ly, o, lo, sp, lsp, gr, ds, rt, g, b, mt in MONTHS:
    mrows.append([f"<b>{nm}</b>", f"£{net:,.0f}", f"£{ly:,.0f}",
                  f"<b class='up'>+{net/ly-1:.0%}</b>", f"{o:,}", f"<b class='up'>+{o/lo-1:.0%}</b>",
                  f"£{net/o:,.0f}", f"£{sp:,.0f}", f"{net/sp:.2f}x",
                  f"{ds/gr:.1%}"])
mrows.append(["<b>Total</b>", f"<b>£{NET:,.0f}</b>", f"<b>£{LYNET:,.0f}</b>",
              f"<b class='up'>+{NET/LYNET-1:.0%}</b>", f"<b>{ORD:,}</b>", f"<b class='up'>+{ORD/LYORD-1:.0%}</b>",
              f"<b>£{NET/ORD:,.0f}</b>", f"<b>£{SPEND:,.0f}</b>", f"<b>{NET/SPEND:.2f}x</b>", f"<b>{DISC/GROSS:.1%}</b>"])

sec("trading", "Trading", "Sales vs last year · Spend · ROAS · Orders · CVR · AOV · Organic · Paid",
    "Trading and reporting", f"""
<div class="kpis">
{kpi("Net sales vs LY", f"+{NET/LYNET-1:.0%}", f"£{NET:,.0f} vs £{LYNET:,.0f}")}
{kpi("Orders vs LY", f"+{ORD/LYORD-1:.0%}", f"{ORD:,} vs {LYORD:,}")}
{kpi("AOV vs LY", f"+{(NET/ORD)/(LYNET/LYORD)-1:.0%}", f"£{NET/ORD:,.0f} vs £{LYNET/LYORD:,.0f}")}
{kpi("Site CVR", "2.33%", "wk 30 Jul–5 Aug, 4,511 sessions")}
{kpi("vs target", "on plan", "Jul +0.5% · Aug MTD +7.2%")}
{kpi("Organic sessions", "+192%", "Jul YoY, Ahrefs estimate")}
</div>

<h3>Net sales against last year</h3>
{grouped_bars([(m[0], [(m[1],"bar-a"),(m[2],"bar-b")]) for m in MONTHS])}
<div class="legend"><span class="lg"><i class="sw sw-a"></i>This year</span><span class="lg"><i class="sw sw-b"></i>Last year</span></div>

<h3>Month by month</h3>
{table(["","Net sales","LY","YoY","Orders","Orders YoY","AOV","Media","ROAS","Discount"], mrows, "num")}
<p class="note">*August is 1–10 only. June had no sales target set; July finished +0.5% against target and August is
+7.2% month to date. Net sales = gross less discount, per the flash's own columns; returns are reported separately.
The August column carries a £1,328 variance against that identity, equal to the month's returns figure — a data-entry
issue in the flash I am correcting, flagged here rather than smoothed over.</p>

<h3>Weekly ROAS against break-even</h3>
{line_chart(WEEKLY, thresh=BREAKEVEN, fmt="{:.1f}", unit="x")}
<p class="note">Break-even sits at {BREAKEVEN}x on the margin assumption carried in the change journal. We have been
above it every week. The proportion of individual days finishing below break-even is worth watching: 27% in June,
23% in July, <b>40% in the first ten days of August</b>. That is the number I would hold myself to next month.</p>

<h3>Where the money went, this year and last</h3>
{stacked_split([
  ("This year", [("Google",sum(m[10] for m in MONTHS),"seg-a"),("Meta",sum(m[12] for m in MONTHS),"seg-b"),("Bing",sum(m[11] for m in MONTHS),"seg-c")]),
  ("Last year", [("Google",14937,"seg-a"),("Meta",23837,"seg-b"),("Bing",2552,"seg-c")]),
])}
<div class="legend"><span class="lg"><i class="sw sw-a"></i>Google</span><span class="lg"><i class="sw sw-b"></i>Meta</span><span class="lg"><i class="sw sw-c"></i>Bing</span></div>
<p class="note">Last year Meta took 58% of the budget. This year Google does, at 55%, with Meta down to 35%. That shift
is deliberate and it is the main reason order volume grew faster than spend.</p>

<h3>Organic sessions, 15 months</h3>
{line_chart(ORGANIC, fmt="{:,.0f}")}
<p class="note"><b>Read this one carefully.</b> Organic is up 192% year on year, but the step change happened in autumn
2025, before I arrived. From May 2026 — my first full month — to the July peak, organic grew 5,322 → 6,739, or
<b>+27%</b>. That 27% is the honest number for this period. The 192% is real but it is not mine to claim.</p>""")

# ---- 4. PROFIT --------------------------------------------------------
prows=[]
for nm,net,ly,o,lo,sp,lsp,gr,ds,rt,g,b,mt in MONTHS:
    gp=net*MARGIN; c=gp-sp
    prows.append([f"<b>{nm}</b>", f"£{gr:,.0f}", f"£{ds:,.0f}", f"<b>{ds/gr:.1%}</b>", f"£{net:,.0f}",
                  f"£{gp:,.0f}", f"£{sp:,.0f}", f"<b>£{c:,.0f}</b>", f"<b>{c/net:.1%}</b>"])
prows.append(["<b>Total</b>",f"<b>£{GROSS:,.0f}</b>",f"<b>£{DISC:,.0f}</b>",f"<b>{DISC/GROSS:.1%}</b>",
              f"<b>£{NET:,.0f}</b>",f"<b>£{NET*MARGIN:,.0f}</b>",f"<b>£{SPEND:,.0f}</b>",
              f"<b>£{CONTRIB:,.0f}</b>",f"<b>{CONTRIB/NET:.1%}</b>"])

sec("profit", "Profit", "Protect sales growth, but improve profit — I don't want sales dropping just so reports look cleaner",
    "Where the profit actually goes", f"""
<div class="callout callout-crit">
  <div class="callout-h">This is the section I would spend the meeting on</div>
  <p>You asked me to improve profit without sacrificing growth. I went looking in the media accounts and found the
  answer somewhere else. Over the period we spent <b>£{SPEND:,.0f}</b> on media and gave away <b>£{DISC:,.0f}</b>
  in discount. One of those two numbers gets reviewed daily. The other has never been on an agenda.</p>
</div>

<div class="kpis">
{kpi("Discount given away", f"£{DISC:,.0f}", f"{DISC/GROSS:.1%} of gross sales", "crit")}
{kpi("Media spend", f"£{SPEND:,.0f}", f"{SPEND/NET:.1%} of net sales", "warn")}
{kpi("Contribution after media", f"£{CONTRIB:,.0f}", f"{CONTRIB/NET:.1%} of net sales", "crit")}
{kpi("Worth 1pt of discount", f"£{GROSS*0.01:,.0f}", "over a period this size")}
{kpi("Orders using a coupon", "56% → 49%", "June → July")}
{kpi("Returns", f"£{RET:,.0f}", f"{RET/GROSS:.1%} of gross · Jul spiked to 4.4%", "warn")}
</div>

<h3>The contribution walk</h3>
{table(["","Gross","Discount","Disc %","Net","Gross profit","Media","Contribution","% of net"], prows, "num")}

<div class="callout callout-warn">
  <div class="callout-h">Assumption you need to confirm</div>
  <p>Gross margin of <b>{MARGIN:.1%}</b> is inferred, not given — it is the margin implied by the {BREAKEVEN}x
  break-even ROAS carried in the change journal. Every contribution figure above moves with it. <b>If you give me the
  real blended gross margin by product category, I will rebuild this properly</b> — and it changes which categories we
  should be buying traffic for. This is my single most valuable ask from you.</p>
</div>

<h3>What the discount data says</h3>
<ul class="bul">
  <li>Discount as a share of gross: June {MONTHS[0][8]/MONTHS[0][7]:.1%}, July {MONTHS[1][8]/MONTHS[1][7]:.1%},
      <b>August {MONTHS[2][8]/MONTHS[2][7]:.1%}</b>. The trend is the wrong way and August is the worst month on record in this set.</li>
  <li><b>56% of June orders and 49% of July orders used a coupon.</b> At that rate a discount is not a promotion, it is
      the price. We are running a permanent sale and calling it a promotion.</li>
  <li>July returns jumped to <b>4.4%</b> of gross from 1.4% in June — £7,449 in one month. Worth understanding before
      peak, when volumes triple.</li>
  <li>AOV is rising (£{MONTHS[0][1]/MONTHS[0][3]:,.0f} → £{MONTHS[2][1]/MONTHS[2][3]:,.0f}) at the same time as the
      discount rate. We are selling bigger baskets and discounting them harder.</li>
</ul>

<h3>What I would do about it</h3>
<ol class="steps">
  <li><b>Put a floor under the discount rate.</b> Target 10% of gross by the end of October. Worth roughly
      £{GROSS*(DISC/GROSS-0.10):,.0f} on a period like this one.</li>
  <li><b>Stop stacking.</b> Audit which codes are live, where they are surfaced, and whether paid traffic is landing on
      pages that advertise a code the customer had not asked for.</li>
  <li><b>Shift from blanket codes to threshold codes</b> — spend-based rather than sitewide, so the discount buys AOV
      instead of just costing margin.</li>
  <li><b>Protect peak.</b> Going into October at a {MONTHS[2][8]/MONTHS[2][7]:.1%} discount rate on triple the volume
      is the single largest profit risk in the next 90 days.</li>
</ol>
<p class="note">To be explicit about scope: pricing and promotions are not mine to set. I am flagging the number, not
proposing to change it unilaterally. If you want me to own it, I will.</p>""")

# ---- 5. GOOGLE ADS ----------------------------------------------------
sec("google", "Google Ads", "What's changed · Brand vs non-brand · PMax · ROAS · Spend · What's still testing · Anything to amend or reverse",
    "Google Ads", f"""
<h3>What changed</h3>
<ul class="bul">
  <li><b>Brand protected.</b> A negative brand list (ID 11160977849) is applied to every PMax campaign. PMax can no
      longer serve on brand queries and take credit for conversions we would have won anyway. This was the biggest
      single distortion in the inherited account.</li>
  <li><b>Account structure rebuilt.</b> Six campaigns renamed to a <code>GGL |</code> convention, matched by
      <code>MSFT |</code> on Microsoft. Towel merged into the catch-all. Listing groups subdivided by price band.</li>
  <li><b>New: AI Max Search | Cast Iron</b>, built 3 August — four ad groups, 32 broad keywords, 46 negatives, UK only.</li>
  <li><b>Negatives at account level.</b> Four shared lists, 111 keywords: repair/DIY and informational (38),
      second-hand and reclaimed (20), competitor and other brands (24), parts/accessories and non-product (29).
      Mirrored on Microsoft. A further 166 negative rows on Microsoft cast iron and column.</li>
  <li><b>Budget moved out of broad PMax into Search.</b> PMax All cut 40% to £120/day; AI Max Search Column raised 300%
      to £80/day as the best-performing Search campaign.</li>
</ul>

<h3>Brand vs non-brand — an honest answer</h3>
<p>The controls are in place and the reporting split is now possible for the first time. What I do not yet have is a
clean brand vs non-brand performance read, because the brand exclusions only went live on 31 July and the pre-31-July
data is contaminated by exactly the cannibalisation the exclusions were built to stop. <b>Comparing the two periods
would produce a number that looks precise and means nothing.</b> First clean read is late September, once there is a
full month of uncontaminated data. I would rather tell you that than hand you a chart I do not believe.</p>

<h3>Still testing</h3>
{table(["Test","Started","What I am watching","Call by"], [
  ["AI Max on Search | Brand","31 Jul","Logged at the time as <b>highest risk</b> in the account. Brand spend and query mix, weekly. Constrained by brand list.","End Aug"],
  ["AI Max Search | Cast Iron","3 Aug","New campaign. CPA and query relevance against 46 negatives.","Mid Sep"],
  ["Past-purchaser exclusion on all PMax","31 Jul","Deliberate trade-off — see below.","End Aug"],
  ["PMax Cast Iron with price-band listing groups","3 Aug","Currently ~1.02x ROAS, well below the 3.36x break-even.","<b>End Aug — hard stop</b>"],
  ["Microsoft PMax with no tROAS target","4 Aug","Removed targets to let Max Conversion Value find its level on thin volume.","Mid Sep"],
]) }

<div class="callout">
  <div class="callout-h">The deliberate trade-off, and how it turned out</div>
  <p>On 31 July I excluded past purchasers from all four Google PMax campaigns to force new-customer acquisition. The
  change journal entry written at the time reads: <i>"Expect short-term CVR and ROAS to FALL — past purchasers are the
  highest-converting audience being removed."</i></p>
  <p>Ten days of data since: ROAS 4.48x → <b>4.23x</b>, a 6% dip rather than the fall I had budgeted for, while
  <b>AOV rose from £338 to £388</b> and daily net sales went up. The trade-off has so far cost less than expected and
  bought new customers going into peak. I am not declaring victory on ten days, but the early read is good.</p>
</div>

<h3>Amend or reverse</h3>
{table(["Campaign","Issue","Recommendation"], [
  ["<b>GGL | PMax | Cast Iron</b>","Running at roughly <b>1.02x</b> against a {0}x break-even. Losing money on every pound.".format(BREAKEVEN),
   chip("crit","Reverse")+" Pause by end Aug unless the feed fix (see Cast Iron) moves it. The products it needs to sell are not eligible to serve."],
  ["<b>GGL | PMax | Towel</b>","Final URL expansion was switched <b>on</b> at the same time as the tROAS was tightened — two settings pushing opposite ways. I logged the conflict when I made it.",
   chip("part","Amend")+" Turn expansion back off; keep the tighter target."],
  ["<b>MSFT | PMax | All</b>","Was using 32% of its budget at 1.50x against break-even.",
   chip("done","Done")+" Budget cut 57% on 31 Jul. Risk control, not a verdict — it launched 17 Jul and is still learning."],
  ["<b>Search | Brand</b> (AI Max)","Highest-risk change in the account.",
   chip("watch","Monitor")+" Weekly brand spend and query review. Reverse immediately if non-brand queries start leaking in."],
])}""")

# ---- 6. SEO -----------------------------------------------------------
sec("seo", "SEO", "What's been fixed · What pages improved · What opportunities · What needs dev · Plan for 3–6 months",
    "SEO", f"""
<div class="kpis">
{kpi("Site health score", "83 / 100", "Ahrefs crawl, 10 Aug · 3,783 URLs")}
{kpi("Organic sessions", "6,739", "July, the highest since Feb")}
{kpi("Growth since I started", "+27%", "May 5,322 → Jul 6,739")}
{kpi("Tracked keywords", "492", "rank tracker now live")}
{kpi("Pages with broken JS", "612", "flagged as errors", "crit")}
{kpi("Images missing alt text", "612", "", "warn")}
</div>

<h3>What has been fixed</h3>
<ul class="bul">
  <li><b>290 H1 tags and 133 title tags changed</b> in the current crawl window — the on-page pass across category and
      product templates.</li>
  <li>Pages dropped out of the top 10 improved by 14 over the crawl period.</li>
  <li>Rank tracking established across 492 keywords. Which is also a caveat: <b>there was no ranking baseline before
      this</b>, so I can show you where we stand today but I cannot honestly show you a before-and-after on positions.
      From now on we can.</li>
</ul>

<h3>Where we rank now</h3>
{table(["Keyword","Volume/mo","Position","Ranking URL"], [
  ["column radiators","9,300",chip("done","3"),"/product-category/"],
  ["designer radiators","5,100",chip("done","4"),"/product-category/designer-radiators/"],
  ["<b>cast iron radiators</b>","<b>4,500</b>",chip("crit","29"),"/product-category/column-radiators/ &nbsp;<i>— wrong page</i>"],
  ["column radiators uk","2,600",chip("done","3"),"/product-category/column-radiators/"],
  ["radiators direct","2,600",chip("watch","9"),"/"],
  ["traditional radiators","2,300",chip("done","4"),"/product-category/traditional-radiators/"],
  ["column radiator","2,000",chip("done","3"),"/product-category/column-radiators/"],
  ["brass radiator","1,800",chip("watch","12"),"/product-category/antique-brass/"],
  ["antique brass radiator","1,600",chip("done","2"),"/product-category/antique-brass/"],
  ["designer radiators uk","1,600",chip("watch","7"),"/product-category/designer-radiators/"],
  ["old fashioned radiators","1,200",chip("crit","18"),"/product-category/traditional-radiators/"],
  ["aluminium radiators for heat pumps","200",chip("done","1"),"/product-category/heat-pump-compatible-radiators/"],
])}

<h3>The opportunities</h3>
<ol class="steps">
  <li><b>Cast iron is the whole game.</b> "cast iron radiators" is 4,500 searches a month and we sit at 29 — with the
      column radiators page ranking for it, not a cast iron page. We also rank mid-page across a dozen cast iron
      variants ("cast iron style" 9, "cast iron look" 6, "cast iron effect" 7, "cast iron column" 5) all pointing at
      the same wrong URL. Full plan in <a href="#castiron" class="jump" data-go="castiron">Cast Iron</a>.</li>
  <li><b>Heat pumps are a free win we are already holding.</b> We rank <b>#1</b> for "aluminium radiators for heat
      pumps", "best radiators for heat pumps" and "best radiators for air source heat pump". Low volume today, but this
      is a category that grows with the boiler ban and we already own it. Worth defending and expanding.</li>
  <li><b>Colour variants.</b> Nine keyword research documents are already written, one per cast iron colour —
      anthracite, black, bronze, cream, green, brass, grey, blue, gold, white. The research is done. They need pages.</li>
  <li><b>"old fashioned radiators" (1,200) at 18 and "brass radiator" (1,800) at 12</b> are both realistic top-five
      targets with the on-page work we already know how to do.</li>
</ol>

<h3>What needs dev support</h3>
{table(["Issue","Scale","Impact","Priority"], [
  ["<b>Broken JavaScript on pages</b>","612 pages","Flagged as an error. Risks rendering and anything measurement-dependent. Needs a dev to identify the failing script.",chip("crit","High")],
  ["Missing image alt text","612 images","Accessibility and image search. Bulk-fixable.",chip("watch","Medium")],
  ["schema.org validation errors","178 pages","Blocks rich results on product pages.",chip("part","High")],
  ["Multiple H1 tags","130 pages","Template-level fix.",chip("watch","Medium")],
  ["Title too long","210 pages","Truncation in SERPs. Partly template.",chip("watch","Medium")],
  ["Page and SERP titles do not match","89 pages","Google rewriting our titles — signal that they are not earning the click.",chip("watch","Medium")],
  ["Orphan pages","13 pages","No internal links in. Invisible to crawlers and customers.",chip("part","Quick win")],
  ["Pages to submit to IndexNow","575 pages","Faster indexation of the new content.",chip("part","Quick win")],
])}

<h3>The 3–6 month plan</h3>
{table(["","Focus","Deliverable"], [
  ["<b>Sep</b>","Cast iron hub","Dedicated /cast-iron-radiators category built and internally linked, taking the cluster off the column page. Colour variant pages one to four."],
  ["<b>Oct</b>","Peak protection","No structural changes during peak. Colour variants five to nine ship. Technical fixes only."],
  ["<b>Nov</b>","Heat pump expansion","Build out the category we already rank #1 in, ahead of winter demand and grant-driven search."],
  ["<b>Dec–Jan</b>","Technical debt","Broken JS, schema, H1s and titles cleared with dev. Post-peak is the right window."],
  ["<b>Feb</b>","Review and re-baseline","First genuine year-on-year ranking comparison, using the baseline established this month."],
])}""")

# ---- 7. SITE / CRO ----------------------------------------------------
sec("cro", "Site &amp; CRO", "Conversion rate · Product pages · Mobile · Checkout · Upsells/accessories · Any obvious issues stopping people buying",
    "Website and conversion", f"""
<p class="lede">GA4 landing-page data, week of 30 July to 5 August: 4,511 sessions, £33,473 revenue, 105 key events.
Site conversion rate <b>2.33%</b>, revenue per session <b>£7.42</b>.</p>

<div class="kpis">
{kpi("Site CVR","2.33%","105 key events / 4,511 sessions")}
{kpi("Revenue per session","£7.42","")}
{kpi("Sessions on £0 pages","35.1%","1,583 sessions, 37 pages","crit")}
{kpi("Basket → key event","17.9%","28 sessions")}
{kpi("Checkout → key event","22.2%","18 sessions")}
{kpi("Untracked sessions","5.3%","237 sessions unattributable","warn")}
</div>

<h3>The obvious issue stopping people buying</h3>
<div class="callout callout-crit">
  <div class="callout-h">Our single most-visited product page converts nothing</div>
  <p><code>/product/glo-kensington-range-column-radiator-horizontal-antique-brass</code> took <b>265 sessions</b> in the
  week — more than any page except the homepage and the column radiators category. It produced <b>£0</b>, zero key
  events, a 41% bounce rate and just <b>34 seconds</b> of engagement against a 90-second average on comparable pages.</p>
  <p>People arrive, look for a few seconds, and leave. That is a page problem, not a traffic problem — and we are
  actively buying traffic to it. It is the first thing I would fix on the site.</p>
</div>

<h3>High-traffic pages producing no revenue</h3>
{table(["Page","Sessions","Bounce","Engagement","Read"], [
  ["<code>…column-radiator-horizontal-antique-brass</code>","265","41%","34s","Top product page. £0. Fix first."],
  ["<code>(not set)</code>","196","98%","12s",chip("crit","Tracking")+" Unattributable. Measurement gap."],
  ["<code>/product-category/cast-iron-radiators</code>","118","26%","90s","Strong engagement, zero sales. Intent is there."],
  ["<code>…traditional-cast-iron-horizontal-anthracite</code>","87","31%","89s","Engaged, no conversion."],
  ["<code>/product-category/heat-pump-compatible-radiators</code>","60","17%","67s","Lowest bounce on the site. Nothing to buy?"],
  ["<code>…victorian-traditional-cast-iron-radiator</code>","60","32%","44s","£0."],
  ["<code>…trv-angled-radiator-valves-antique-brass</code>","56","50%","39s","Top accessory page. £0."],
  ["<code>/product-category/antique-brass</code>","46","13%","72s","Very low bounce, no revenue."],
])}
<p class="note"><b>37 pages, 1,583 sessions, 35.1% of all site traffic, £0 revenue.</b> Several have low bounce and high
engagement, which is the tell: these are not bad pages attracting the wrong people. They are pages where interested
people fail to complete.</p>

<h3>Product pages</h3>
<ul class="bul">
  <li>Cast iron in <b>white</b> converts: <code>traditional-cast-iron-horizontal-white</code> did £2,179 from 78
      sessions (5.1% key event rate) and the vertical white £821 from 32 (9.4%) — both well above the 2.33% site average.</li>
  <li>Cast iron in <b>every other finish</b> does not. Anthracite, Victorian, Windsor, Piccadilly, Mayfair and Oxford
      took <b>208 sessions between them and produced £0</b>.</li>
  <li>That is not a demand problem — it is the same product family. It points at stock, price display, or lead times on
      the period ranges. This needs a merchandising answer, not a marketing one.</li>
</ul>

<h3>Upsells and accessories</h3>
<p>Accessories — valves, feet, pipe covers, wall stays — took <b>245 sessions (5.4% of traffic)</b> and produced
<b>£777, or 2.3% of revenue</b>. In Shopping the picture is worse: TRVs got <b>7 clicks and £5.90 of spend</b> across
the whole reporting period. We are effectively not selling the attachment.</p>
<p>For a radiator business that is real money left on the table: every radiator sold needs valves. The opportunity is
basket attachment at the point of sale, not paid traffic to a valve page. That is a site change — a "you'll also need"
module on the product page and in the basket — and it is on the 90-day list.</p>

<h3>Checkout</h3>
<p>Basket-entry sessions convert at 17.9% and checkout-entry at 22.2%, both healthy. The funnel is not obviously
leaking at the end. I would not prioritise checkout work over the product-page problem above.</p>

<div class="callout callout-warn">
  <div class="callout-h">Mobile — I cannot answer this one yet</div>
  <p>You asked about mobile specifically and I do not have a device split in the data I hold. I am not going to
  estimate it. Device-level CVR reporting is in the 90-day plan and I will have it for the next review. Given that
  mobile is typically the majority of traffic and the weaker converter, this is a genuine gap rather than a formality.</p>
</div>""")

# ---- 8. CAST IRON -----------------------------------------------------
sec("castiron", "Cast Iron", "What opportunities are there",
    "Cast iron: one opportunity, broken in three places", """
<p class="lede">This is the clearest finding in the whole review. Cast iron is simultaneously our biggest search
opportunity, our newest paid investment and our largest content programme — and it is broken in the product feed, on
the site and in search at the same time. Fix it in one place and the other two stay broken. Fix all three and it
compounds.</p>

<div class="tri">
  <div class="tri-card tri-crit">
    <div class="tri-h">In the feed</div>
    <p>The flagship cast iron SKUs — Victorian (£924–£1,116), Windsor (£2,167), Mayfair (£1,470), Oxford (£2,320),
    Piccadilly — are all marked <b>"Not eligible — excluded product or listing group"</b>.</p>
    <p class="tri-f">They cannot serve. We built two campaigns to sell products that are switched off.</p>
  </div>
  <div class="tri-card tri-crit">
    <div class="tri-h">On the site</div>
    <p>The cast iron category took <b>118 sessions at 90 seconds engagement and made £0</b>. The period ranges took
    another 208 sessions, also £0. Only the white finishes convert, and they convert well.</p>
    <p class="tri-f">Intent is arriving and failing to complete.</p>
  </div>
  <div class="tri-card tri-warn">
    <div class="tri-h">In search</div>
    <p>"cast iron radiators" is <b>4,500 searches/month</b> and we rank <b>29</b> — with the column radiators page,
    not a cast iron page. A dozen cast iron variants rank 5–15 on that same wrong URL.</p>
    <p class="tri-f">We have the authority. It is pointed at the wrong page.</p>
  </div>
</div>

<h3>What is already built and waiting</h3>
<ul class="bul">
  <li>Nine keyword research documents, one per colour — anthracite, black, bronze, brass, cream, green, grey, blue, gold, white.</li>
  <li>Two how-to guides written: keeping a white cast iron radiator clean, installing a black cast iron radiator.</li>
  <li>A dedicated <code>GGL | AI Max Search | Cast Iron</code> campaign, 4 ad groups, 32 keywords, 46 negatives.</li>
  <li><code>PMax | Cast Iron</code> with price-band listing groups, five search themes and a 46-asset group.</li>
  <li>On Microsoft: 701 product exclusion rows and 166 negative keyword rows already configured.</li>
</ul>
<p class="note">The marketing work is done. The blocker is upstream of marketing.</p>

<h3>The sequence</h3>
<ol class="steps">
  <li><b>Feed eligibility first, this month.</b> Nothing else pays back until the products can serve. This needs
      whoever owns the product data — I need to know who that is.</li>
  <li><b>Then the category hub.</b> A real <code>/cast-iron-radiators</code> page that takes the cluster off the column
      page, internally linked from the ranking pages that currently absorb it.</li>
  <li><b>Then the colour pages</b>, using the nine research documents already written.</li>
  <li><b>Then reassess the paid campaigns.</b> PMax Cast Iron at 1.02x gets paused at the end of August if the feed is
      not fixed. I am not going to keep funding a campaign whose products cannot appear.</li>
  <li><b>Diagnose why only white converts.</b> Merchandising question — stock, lead time, or price presentation on the
      period ranges. Needs someone from the product side.</li>
</ol>""")

# ---- 9. CHANGES -------------------------------------------------------
sec("changes", "Changes", "Why changes were made · What worked · What didn't",
    "The change log", """
<p class="lede">Every change since 31 July is logged with a timestamp, the before value, the after value and the reason.
Ninety-plus entries. Round-trip edits are netted out so the log shows real movement rather than activity. This is the
document that answers "why did you do that" for any campaign, on any date.</p>

<h3>Budget movements, net of round-trips</h3>
""" + table(["Campaign","Before","After","Change","Reason"], [
  ["GGL | AI Max Search | Column","£20","£80","<b class='up'>+300%</b>","Best-performing Search campaign in the account"],
  ["GGL | AI Max Search | Cast Iron","£20","£50","<b class='up'>+150%</b>","New campaign, scaling into the cast iron push"],
  ["GGL | PMax | Cast Iron","£60","£100","<b class='up'>+67%</b>","Scaled before the feed problem was known. Under review."],
  ["GGL | Search | Brand","£45","£60","<b class='up'>+33%</b>","Brand protection, cheap clicks, guaranteed position"],
  ["GGL | PMax | Column","£340","£300","<b class='dn'>−12%</b>","Trimmed to fund Search"],
  ["GGL | PMax | ALL","£200","£120","<b class='dn'>−40%</b>","Weakest format. Moved into Search."],
  ["MSFT | AI Max Search | Column","£10","£55","<b class='up'>+450%</b>","Best Bing performer, was budget-capped"],
  ["MSFT | Pmax | Cast Iron","£15","£50","<b class='up'>+233%</b>","Mirror of the Google cast iron structure"],
  ["MSFT | PMax | Column","£215","£100","<b class='dn'>−54%</b>","Overdelivering with weak return"],
  ["MSFT | PMax | All","£85","£50","<b class='dn'>−41%</b>","1.50x against 3.36x break-even"],
]) + """
<p class="note">Direction of travel: out of broad PMax, into Search and cast iron. Google PMax budgets are down roughly
a third in aggregate; Search budgets are up multiples.</p>

<h3>What worked</h3>
<ul class="bul">
  <li><b>Brand exclusions on PMax.</b> The structural fix the account most needed. Stops the cannibalisation recurring.</li>
  <li><b>Moving budget from PMax into Search.</b> Search was already the stronger format at takeover (3.09x vs 2.38x)
      and AI Max Search Column is now the best performer in the account.</li>
  <li><b>Pausing Meta cold prospecting.</b> Removed an estimated £14k/quarter of loss.</li>
  <li><b>Getting Bing cost data into GA4.</b> £22,860 of revenue that previously had no cost attached to it.</li>
  <li><b>The past-purchaser exclusion.</b> Cost less than forecast and lifted AOV 15%.</li>
</ul>

<h3>What didn't</h3>
<ul class="bul">
  <li><b>PMax Cast Iron.</b> ~1.02x against 3.36x break-even. In fairness to the campaign, its products are not
      eligible to serve — but it should not have been scaled 67% before I checked feed eligibility. That is on me, and
      it is the specific lesson from this quarter: check the feed before funding the campaign.</li>
  <li><b>Towel campaign settings pulled in opposite directions.</b> I switched Final URL expansion on while tightening
      the tROAS. I logged the conflict at the time, which is right, but I should not have made both changes together.</li>
  <li><b>Too many changes in one window.</b> Ninety-plus edits across 31 July to 6 August, several as round trips.
      Genuine attribution of what caused what is harder than it should be. Fewer, better-spaced changes from here.</li>
  <li><b>The Microsoft customer-match list</b> was applied on 4 August and removed by 6 August — churn that produced
      nothing.</li>
</ul>""")

# ---- 10. WORKLOAD -----------------------------------------------------
sec("workload", "Workload", "What's taking too much time · What could go to Flora · What needs documenting",
    "Workload and process", """
<h3>What is taking too much time</h3>
""" + table(["Task","Frequency","Time","Verdict"], [
  ["<b>Daily media pacing</b> — hour-by-hour spend tracking across 30+ campaigns on three platforms, manually maintained",
   "Daily","Largest single recurring cost", chip("crit","Automate")+" This is a spreadsheet doing a script's job."],
  ["Daily sales flash entry","Daily","Moderate", chip("part","Delegate")+" Mechanical data entry. Good fit for Flora."],
  ["Change journal upkeep","Per change","Moderate", chip("done","Keep")+" This is the control that makes the account auditable. Worth the time."],
  ["Search term and negative keyword review","Weekly","Moderate", chip("part","Part-delegate")+" Flora can pull and pre-sort; I make the calls."],
  ["Feed and product data QA","Ad hoc","Rising", chip("watch","Needs an owner")+" Currently nobody's job, which is how cast iron broke."],
]) + """

<h3>What could go to Flora</h3>
<ol class="steps">
  <li><b>Daily flash data entry</b> — clear rules, low judgement, high repetition. Straight handover with a written procedure.</li>
  <li><b>Weekly search-term pulls</b> — Flora extracts and pre-sorts against the four negative lists; I approve the additions.</li>
  <li><b>Feed health monitoring</b> — a weekly eligibility check against the merchant report. Had this existed, the cast
      iron problem would have surfaced in week one rather than week ten.</li>
  <li><b>Content production against the keyword docs</b> — the nine cast iron colour briefs are written and ready to be
      turned into pages.</li>
</ol>
<p class="note">What I would keep: bidding, budget allocation, campaign structure, and anything touching the brand
exclusions. Those need the account context, and mistakes there are expensive.</p>

<h3>On documenting the process</h3>
<div class="callout">
  <p>You wrote: <i>"Not to micromanage, but so the business owns the process."</i> That is the right instinct and I
  agree with it — with one thing worth saying plainly.</p>
  <p>The change journal, the takeover checklist and the daily flash already exist and are already maintained. This pack
  is built entirely from them. So the documentation habit is there; what is missing is the <b>procedures</b> — the
  written "how to do this task" that lets someone else pick it up. Those are what make the business own the process,
  and they are what I would write next.</p>
  <p>Three I would commit to before peak: <b>daily pacing</b>, <b>weekly feed health check</b>, and
  <b>monthly reporting</b>. One page each, written so Flora or anyone else can run them without me.</p>
</div>""")

# ---- 11. NEXT 90 ------------------------------------------------------
sec("next90", "Next 90", "Top priorities · What support you need from me · From Liam/Flora · Any budget/tools needed · What success looks like by month 6",
    "The next 90 days", f"""
<p class="lede">Framed around peak. October to December is the season this business lives on, and the work divides
cleanly into what must be finished before it starts and what must not be touched during it.</p>

<h3>The three priorities</h3>
<div class="tri">
  <div class="tri-card tri-a"><div class="tri-h">1 · Fix cast iron end to end</div>
  <p>Feed eligibility, then the category hub, then the colour pages, then reassess the paid campaigns. Biggest single
  opportunity in the business and the research is already written.</p>
  <p class="tri-f">Owner: me, blocked on product data access</p></div>
  <div class="tri-card tri-b"><div class="tri-h">2 · Put a floor under discounting</div>
  <p>Target {DISC/GROSS:.1%} → 10% of gross by end of October. Worth roughly £{GROSS*(DISC/GROSS-0.10):,.0f} on a
  period this size — more than half of total contribution.</p>
  <p class="tri-f">Owner: needs to be agreed — not mine to set</p></div>
  <div class="tri-card tri-c"><div class="tri-h">3 · Be season-ready by 30 September</div>
  <p>All structural changes done and settled, budgets set, procedures written. Then no structural changes during peak
  — only monitoring and budget.</p>
  <p class="tri-f">Owner: me</p></div>
</div>

<h3>Month by month</h3>
{table(["","Paid","SEO / site","Process"], [
  ["<b>Aug</b> (rest)","Call on PMax Cast Iron. Turn off Towel URL expansion. Weekly brand-query review.","Cast iron feed eligibility fixed.","Daily pacing procedure written."],
  ["<b>Sep</b>","Budgets set for peak. Clean brand vs non-brand read. Device-level CVR reporting live.","Cast iron hub built. Colour pages 1–4. Fix the antique brass product page.","Feed health check running weekly. Flash handed to Flora."],
  ["<b>Oct–Dec</b>","<b>Peak. Monitoring and budget only.</b> No structural changes.","Colour pages 5–9. Accessory attachment module.","Monthly reporting pack, this format, automated."],
  ["<b>Jan–Feb</b>","Post-peak review. Rebuild on what peak taught us.","Technical debt: broken JS, schema, H1s, titles.","Re-baseline. First true YoY ranking comparison."],
])}

<h3>What I need from you</h3>
{table(["Ask","Why","Urgency"], [
  ["<b>Blended gross margin by product category</b>","Every profit figure in this pack rests on an inferred 29.8%. With the real number I can tell you which categories are worth buying traffic for — and which we are currently paying to lose money on.",chip("crit","This week")],
  ["<b>A decision on the discount rate</b>","The largest profit lever available and it is not mine to pull. I need either a target or a mandate.",chip("crit","This week")],
  ["<b>Who owns product feed data</b>","Cast iron broke because nobody owns feed eligibility. Name someone and I will build the check around them.",chip("warn","This month")],
  ["<b>Peak budget envelope</b>","Efficiency holds at 4.44x on our highest-spend days, so there is room to scale. I need to know the ceiling to plan against it.",chip("warn","By mid-Sep")],
])}

<h3>What I need from Liam and Flora</h3>
{table(["Who","Ask"], [
  ["<b>Liam</b>","Dev time for the 612 pages with broken JavaScript and the 178 schema errors. Half a day scoping, then an estimate. Ideally scheduled for January, but the broken JS should be diagnosed sooner."],
  ["<b>Flora</b>","Roughly a day a week to take on the daily flash, weekly search-term pulls and the feed health check. I will write the procedures first so the handover is clean, not a transfer of confusion."],
])}

<h3>Budget and tools</h3>
<ul class="bul">
  <li><b>No new tools requested.</b> Ahrefs and GA4 cover what we need; the gap is procedure, not software.</li>
  <li><b>Peak media budget</b> — a number to plan against, not an increase request. The efficiency data supports scaling.</li>
  <li>Possible small spend on cast iron product photography if the period ranges turn out to have a presentation
      problem rather than a stock one. I will confirm which before asking.</li>
</ul>

<h3>What success looks like by month 6</h3>
{table(["Measure","Today","Month 6 target"], [
  ["Contribution after media","{:.1%} of net".format(CONTRIB/NET),"<b>10%+</b>, driven mainly by discount discipline"],
  ["Discount rate","{:.1%} of gross".format(DISC/GROSS),"<b>10%</b> or below"],
  ["Days below break-even ROAS","40% in Aug","<b>Under 20%</b>"],
  ["&quot;cast iron radiators&quot; rank","29","<b>Top 10</b>, on a dedicated cast iron page"],
  ["Site conversion rate","2.33%","<b>2.8%+</b>, with device split reported"],
  ["Accessory attachment","2.3% of revenue","<b>5%+</b>"],
  ["Sessions on zero-revenue pages","35.1%","<b>Under 20%</b>"],
  ["Documented procedures","0","<b>3 written and in use</b>"],
])}""")

# ---- 12. GAPS ---------------------------------------------------------
sec("gaps", "Gaps", "What hasn't worked as expected · What still needs sorting",
    "What I cannot yet tell you, and why", """
<p class="lede">Rather than fill these with estimates, here is what is genuinely missing, why, and when it will be
answered. If any of these matter more than I have judged, tell me and I will reprioritise.</p>

""" + table(["Gap","Why it exists","When it is answered"], [
  ["<b>Mobile vs desktop conversion rate</b>","No device split in the data I hold. Given mobile is usually the majority of traffic and the weaker converter, this is a real gap.","Device reporting live in September"],
  ["<b>Brand vs non-brand performance split</b>","Brand exclusions only went live 31 July. Pre-31-July data is contaminated by the exact cannibalisation the exclusions were built to stop. Any comparison now would look precise and mean nothing.","Late September, after a clean month"],
  ["<b>True gross margin</b>","Inferred at 29.8% from the break-even ROAS in the change journal. Not a given figure.","As soon as you send it"],
  ["<b>Ranking movement since I started</b>","No rank tracking existed before this month. I can show where we stand, not how far we have come. The tracker is now live across 492 keywords.","February, for a true YoY read"],
  ["<b>Meta CAPI / server-side tracking</b>","On the takeover checklist, still unverified. Without it a large share of users are invisible to optimisation.","September"],
  ["<b>Why only white cast iron converts</b>","208 sessions across the period ranges produced £0 while white converts above site average. This is a merchandising question — stock, lead time or price presentation — not a marketing one.","Needs product-side input"],
  ["<b>237 unattributable sessions (5.3%)</b>","Landing page recorded as (not set) or blank, 98–100% bounce. Points at a tracking or redirect fault.","Investigating now"],
]) + """

<h3>What has not worked as expected</h3>
<ul class="bul">
  <li><b>PMax Cast Iron</b> — scaled before feed eligibility was checked. 1.02x against a 3.36x break-even. My error,
      and the reason a feed health check is now on the process list.</li>
  <li><b>Change volume</b> — 90+ edits in one week makes clean attribution harder than it needed to be.</li>
  <li><b>The Towel campaign</b> — two settings pushed against each other in the same session.</li>
  <li><b>August discount rate</b> — went the wrong way, to 16.6%, at exactly the point I was focused on media efficiency.
      I was looking at the smaller of the two numbers.</li>
</ul>

<div class="callout">
  <div class="callout-h">One thing I would like to agree</div>
  <p>This pack took a working day to build because the data lives in six places. Most of it can be automated into a
  monthly pack in this format. If that is useful, I would rather send it to you monthly unprompted than assemble it for
  reviews — it is less work for me and it means nothing waits ninety days to surface.</p>
</div>"""
)

# ---------------------------------------------------------------- assemble
nav = "".join(f'<button class="tab" data-go="{sid}" role="tab" aria-selected="{"true" if i==0 else "false"}" '
              f'id="tab-{sid}" aria-controls="p-{sid}">{n}</button>'
              for i,(sid,n,q,t,b) in enumerate(SECTIONS))
panels = "".join(
    f'<section class="panel{" on" if i==0 else ""}" id="p-{sid}" role="tabpanel" aria-labelledby="tab-{sid}"'
    f'{"" if i==0 else " hidden"}>'
    f'<p class="eyebrow">{html.escape(q)}</p><h2>{t}</h2>{b}</section>'
    for i,(sid,n,q,t,b) in enumerate(SECTIONS))

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

DOC = f"""<title>Lincs Rads Direct — 90 Day Review</title>
<style>{CSS}</style>
<div class="wrap">
<header class="masthead">
  <p class="kicker">Lincs Rads Direct · Paid media, SEO &amp; site</p>
  <h1>90-day review</h1>
  <p class="sub">Everything on your list, answered from the daily flash, the change journal, the takeover checklist,
  GA4 and Ahrefs. Where the data does not support an answer, it says so rather than estimating.</p>
  <div class="meta">
    <span>Period <b>1 Jun – 10 Aug 2026</b></span>
    <span>Trading days <b>71</b></span>
    <span>Net sales <b>£{NET:,.0f}</b></span>
    <span>Sources <b>6</b></span>
    <span>Logged changes <b>90+</b></span>
  </div>
</header>
<nav class="tabs" role="tablist" aria-label="Review sections">{nav}</nav>
{panels}
<footer>
  Built from: LRD Daily Flash 2026 · Master Change Journal · Paid Media Takeover Checklist (9 Jun) ·
  MerchantCatalogReport · GA4 landing page export (30 Jul–5 Aug) · Ahrefs project 9919884 (crawl 10 Aug).<br>
  Gross margin of {MARGIN:.1%} is inferred from the {BREAKEVEN}x break-even ROAS recorded in the change journal and
  requires confirmation. August figures cover 1–10 August only.
</footer>
</div>
<script>{JS}</script>"""

open(OUT,"w").write(DOC)
print(f"wrote {OUT}  ({len(DOC):,} bytes, {len(SECTIONS)} sections)")
