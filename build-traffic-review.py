#!/usr/bin/env python3
"""Traffic & acquisition review pack — built on the shared chart engine."""
import html, importlib.util, os
spec = importlib.util.spec_from_file_location("engine", os.path.join(os.path.dirname(__file__), "engine.py"))
E = importlib.util.module_from_spec(spec); spec.loader.exec_module(E)
grouped_bars, line_chart, stacked_split = E.grouped_bars, E.line_chart, E.stacked_split

OUT = "/home/user/europe-ad-report/traffic-review.html"

# ---------------------------------------------------------------- data
CH = [
    ("Paid – Google", 17171,  7777, .748, .823),
    ("Paid – Meta",   11530, 11030, .635, .696),
    ("Organic",        5583,  2898, .688, .715),
    ("Direct",         4811,  4632, .652, .640),
    ("Referral",       3096,  2329, .796, .747),
    ("Paid – Bing",    2051,   798, .745, .802),
    ("Other",           986,   186, .414, .344),
    ("AI assistants",   149,    11, .617, .636),
]
S26 = sum(c[1] for c in CH); S25 = sum(c[2] for c in CH)
P26, P25 = 17171 + 11530 + 2051, 7777 + 11030 + 798
O26, O25 = 5583, 2898
SPEND = {"Google": (44934, 14937), "Bing": (10729, 2552), "Meta": (28436, 23837)}
SESS  = {"Google": (17171, 7777), "Bing": (2051, 798), "Meta": (11530, 11030)}
TC  = sum(v[0] for v in SPEND.values()); TC25 = sum(v[1] for v in SPEND.values())
CPS, CPS25 = TC / P26, TC25 / P25

CAMP = [
    ("GGL | PMax | ALL (excl. Col/Cast)", "PMax",   8992, 8592, 1.05,  9.6,  4.5, 73.3),
    ("GGL | PMax | Column",               "PMax",   7648, 3315, 2.31, 25.0,  5.7, 65.6),
    ("GGL | AI Max Search | Column",      "Search", 1743,  631, 2.76,  3.7, 29.1, 51.6),
    ("GGL | PMax | Cast Iron",            "PMax",   1345, 1860, 0.72, 13.4, 11.2, 48.9),
    ("GGL | Search | Brand",              "Search", 1190,  731, 1.63, 96.6,  0.9,  2.5),
    ("GGL | AI Max Search | Electric",    "Search",  393,  151, 2.60,  2.0, 22.0, 35.8),
    ("GGL | AI Max Search | Cast Iron",   "Search",  262,   49, 5.35,  1.8, 23.9, 53.4),
    ("GGL | PMax | Electric",             "PMax",    244,  163, 1.50, 16.2, 13.1, 68.2),
]
FMT  = [("Performance Max", 34337), ("Search", 9611), ("Shopping", 1551), ("Display", 160)]
FTOT = sum(f[1] for f in FMT)
DEV  = [
    ("Mobile",  35613, .785, 179888,  5.05, 22995, 4.31, .687),
    ("Desktop",  8739, .193, 152285, 17.43,  5719, 19.93, .730),
    ("Tablet",   1025, .023,   5012,  4.89,   947, 6.45, .777),
]
COVER = [("June", 13), ("July", 66), ("Aug 1–10", 97)]

def chip(k, t): return f'<span class="chip chip-{k}">{t}</span>'
def kpi(l, v, s="", tone=""):
    return (f'<div class="kpi {tone}"><div class="kpi-l">{l}</div>'
            f'<div class="kpi-v">{v}</div><div class="kpi-s">{s}</div></div>')
def table(h, rows, cls=""):
    th = "".join(f"<th>{x}</th>" for x in h)
    tr = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in rows)
    return f'<div class="tw"><table class="{cls}"><thead><tr>{th}</tr></thead><tbody>{tr}</tbody></table></div>'

SECTIONS = []
def sec(sid, nav, quote, title, body): SECTIONS.append((sid, nav, quote, title, body))

# ---- 1 SCORECARD -------------------------------------------------------
sec("scorecard", "Scorecard", "What I control: where the budget goes, what it buys, and how relevant the traffic is",
    "My scorecard", f"""
<p class="lede">This is the part of the business I actually hold the levers on: how much we spend, which
platforms and campaigns it goes to, what it costs to bring someone to the door, and whether the person who
arrives is relevant. Everything in this section is a direct result of a decision I made.</p>

<div class="kpis">
{kpi("Sessions delivered", f"{S26:,}", f"vs {S25:,} LY &nbsp;<b class='up'>+{S26/S25-1:.0%}</b>")}
{kpi("Paid sessions", f"{P26:,}", f"vs {P25:,} LY &nbsp;<b class='up'>+{P26/P25-1:.0%}</b>")}
{kpi("Organic sessions", f"{O26:,}", f"vs {O25:,} LY &nbsp;<b class='up'>+{O26/O25-1:.0%}</b>")}
{kpi("Cost per session", f"£{CPS:.2f}", f"vs £{CPS25:.2f} LY &nbsp;<b class='dn'>+{CPS/CPS25-1:.0%}</b>", "warn")}
{kpi("Brand impression share", "96.6%", "only 2.5% lost to rank")}
{kpi("Organic avg position", "12.1", "from 28.0 LY &nbsp;<b class='up'>+15.8 places</b>")}
</div>

<h3>The scorecard, in full</h3>
{table(["What I control","This period","Last year","Read"], [
 ["<b>Paid sessions delivered</b>", f"{P26:,}", f"{P25:,}", chip("done",f"+{P26/P25-1:.0%}")+" More people brought to the door"],
 ["<b>Media budget allocation</b>", "G 56% / M 37% / B 7%", "G 40% / M 56% / B 4%", chip("done","Reallocated")+" Deliberate shift out of Meta into Search"],
 ["<b>Cost per session</b>", f"£{CPS:.2f}", f"£{CPS25:.2f}", chip("watch",f"+{CPS/CPS25-1:.0%}")+" Rose while scaling 57%. See Cost of traffic."],
 ["<b>Brand impression share</b>", "96.6%", "not protected", chip("done","Locked")+" Competitors cannot take our name cheaply"],
 ["<b>Spend in controllable formats</b>", "24.4% Search + Shopping", "—", chip("part","In progress")+" 75% still in PMax, which reports no queries"],
 ["<b>Account rebuilt</b>", "97% of Aug spend", "13% in June", chip("done","Near complete")+" Share of spend in campaigns I built"],
 ["<b>Waste controls</b>", "111 negatives, 4 lists", "none", chip("done","Built")+" Mirrored on Microsoft, +166 rows"],
 ["<b>Organic avg position</b>", "12.1", "28.0", chip("done","+15.8")+" Impression-weighted across 987 pages"],
 ["<b>Organic CTR</b>", "0.76%", "0.41%", chip("done",f"+85%")+" On 13% fewer impressions"],
 ["<b>Changes logged with rationale</b>", "90+", "0", chip("done","Auditable")+" Every change has a before, after and reason"],
])}

<div class="callout">
  <div class="callout-h">What this section deliberately does not contain</div>
  <p>Conversion rate, average order value and revenue are not here. Not because they don't matter — they
  matter more than anything — but because they are the product of my work <i>and</i> price, stock, range,
  site build and season. I report them in <a href="#commercial" class="jump" data-go="commercial">Commercial
  outcome</a> without claiming or dodging them. Where I can see something outside my remit costing us money,
  it goes in the <a href="#escalation" class="jump" data-go="escalation">Escalation register</a> with a name
  against it.</p>
</div>""")

# ---- 2 MEDIA MIX -------------------------------------------------------
mixrows = []
for nm, a, b, er, erL in CH:
    yoy = f"<b class='up'>+{a/b-1:.0%}</b>" if a >= b else f"<b class='dn'>{a/b-1:.0%}</b>"
    mixrows.append([f"<b>{nm}</b>", f"{a:,}", f"{a/S26:.1%}", f"{b:,}", f"{b/S25:.1%}", yoy, f"{er:.0%}", f"{erL:.0%}"])
mixrows.append(["<b>Total</b>", f"<b>{S26:,}</b>", "100%", f"<b>{S25:,}</b>", "100%",
                f"<b class='up'>+{S26/S25-1:.0%}</b>", "", ""])

sec("mix", "Media mix", "Traffic share between paid and organic, and the changes within the paid mix",
    "Where the traffic came from", f"""
<div class="kpis">
{kpi("Total sessions", f"{S26:,}", f"<b class='up'>+{S26/S25-1:.0%}</b> YoY")}
{kpi("Paid share", f"{P26/S26:.1%}", f"vs {P25/S25:.1%} LY — broadly held")}
{kpi("Organic share", f"{O26/S26:.1%}", f"vs {O25/S25:.1%} LY &nbsp;<b class='up'>growing</b>")}
</div>

<h3>Sessions by channel</h3>
{grouped_bars([(c[0].replace("Paid – ",""), [(c[1],"bar-a"),(c[2],"bar-b")]) for c in CH[:6]])}
<div class="legend"><span class="lg"><i class="sw sw-a"></i>This year</span><span class="lg"><i class="sw sw-b"></i>Last year</span></div>

{table(["Channel","Sessions","Share","LY","LY share","YoY","Eng. rate","LY"], mixrows, "num")}

<h3>The shift inside paid</h3>
{stacked_split([
  ("This year", [("Google",17171,"seg-a"),("Meta",11530,"seg-b"),("Bing",2051,"seg-c")]),
  ("Last year", [("Google",7777,"seg-a"),("Meta",11030,"seg-b"),("Bing",798,"seg-c")]),
])}
<div class="legend"><span class="lg"><i class="sw sw-a"></i>Google</span><span class="lg"><i class="sw sw-b"></i>Meta</span><span class="lg"><i class="sw sw-c"></i>Bing</span></div>

<p><b>This is the single clearest thing I did.</b> Last year Meta was the majority of paid traffic at 56%.
Today Google is, at 56%, and Meta is 37%. That was not drift — it was a series of deliberate budget
decisions: retiring five Meta ad sets that were burning money, and pushing the freed budget into search,
where intent already exists.</p>

<h3>Paid versus organic</h3>
{table(["","Sessions","Share of all traffic","LY sessions","LY share","YoY"], [
 ["<b>Paid</b>", f"{P26:,}", f"{P26/S26:.1%}", f"{P25:,}", f"{P25/S25:.1%}", f"<b class='up'>+{P26/P25-1:.0%}</b>"],
 ["<b>Organic</b>", f"{O26:,}", f"{O26/S26:.1%}", f"{O25:,}", f"{O25/S25:.1%}", f"<b class='up'>+{O26/O25-1:.0%}</b>"],
 ["<b>Direct + referral</b>", f"{4811+3096:,}", f"{(4811+3096)/S26:.1%}", f"{4632+2329:,}", f"{(4632+2329)/S25:.1%}", f"<b class='up'>+{(4811+3096)/(4632+2329)-1:.0%}</b>"],
], "num")}
<p class="note">Organic grew faster than paid (+93% vs +57%) and now makes up a larger share of the mix than
last year. That is the healthier direction of travel: it is the only channel where the traffic keeps arriving
after you stop paying.</p>

<div class="callout">
  <div class="callout-h">One to watch — AI assistants</div>
  <p>Sessions from ChatGPT, Gemini, Perplexity and Copilot went from <b>11 to 149</b>. Still tiny, but it is
  the fastest-growing source on the site by a distance, and it is not something we are doing anything to earn
  yet. Worth a proper look before it stops being tiny.</p>
</div>""")

# ---- 3 COST OF TRAFFIC -------------------------------------------------
cprows = []
for k in ("Google", "Bing", "Meta"):
    c, c25 = SPEND[k]; s, s25 = SESS[k]
    cprows.append([f"<b>{k}</b>", f"£{c:,.0f}", f"£{c25:,.0f}", f"{s:,}", f"{s25:,}",
                   f"<b>£{c/s:.2f}</b>", f"£{c25/s25:.2f}",
                   f"<b class='dn'>+{(c/s)/(c25/s25)-1:.0%}</b>", f"<b class='up'>+{s/s25-1:.0%}</b>"])
cprows.append(["<b>Blended</b>", f"<b>£{TC:,.0f}</b>", f"<b>£{TC25:,.0f}</b>", f"<b>{P26:,}</b>", f"<b>{P25:,}</b>",
               f"<b>£{CPS:.2f}</b>", f"<b>£{CPS25:.2f}</b>",
               f"<b class='dn'>+{CPS/CPS25-1:.0%}</b>", f"<b class='up'>+{P26/P25-1:.0%}</b>"])

sec("cost", "Cost of traffic", "Spend and the efficiency of what it bought",
    "What the traffic cost", f"""
<p class="lede">Cost per session is the cleanest measure of my half of the job. It is what we paid to get a
person onto the site, before anything about price, product or the site itself comes into play.</p>

<div class="kpis">
{kpi("Blended cost per session", f"£{CPS:.2f}", f"vs £{CPS25:.2f} LY", "warn")}
{kpi("Cheapest channel", "Meta £2.47", "then Google £2.62")}
{kpi("Most expensive", "Bing £5.23", "2x Google — needs fixing", "crit")}
</div>

{table(["Channel","Spend","LY spend","Sessions","LY sessions","Cost/session","LY","Change","Volume"], cprows, "num")}

<div class="callout callout-warn">
  <div class="callout-h">Being straight about this one</div>
  <p>Cost per session rose <b>{CPS/CPS25-1:.0%}</b>. I am not going to dress that up. But the mechanism
  matters: we bought <b>{P26/P25-1:.0%} more traffic</b>, and in an auction you do not buy 57% more volume at
  the same price — you move up the demand curve. The relevant question is not "did it get more expensive"
  but "was the extra volume worth what it cost", and that is answered by the impression share data in
  <a href="#google" class="jump" data-go="google">Google Ads</a>: our best Search campaigns are still losing
  a fifth to a third of available impressions purely to budget, which means cheap growth is still on the
  table.</p>
</div>

<h3>Bing is the outlier</h3>
<p>Bing costs <b>£5.23 a session against Google's £2.62</b> — twice as much for the same job, in a market
where Bing clicks are normally cheaper, not dearer. Spend went from £2,552 to £10,729 on my watch, so this
is mine to answer for. The Microsoft campaigns spent much of July and August heavily constrained by budget
(lost impression share to budget hit 88% on some days for PMax Column and 90% for Cast Iron), which forces
the bidding into the most expensive slots. Fixing the pacing there is the single clearest efficiency job I
have in the next 30 days.</p>

<h3>Meta: fewer clicks, cheaper impressions</h3>
{table(["Metric","This year","Last year","Change"], [
 ["Spend","£28,454","£23,787","<b class='dn'>+19.6%</b>"],
 ["Impressions","3,839,972","2,889,732","<b class='up'>+32.9%</b>"],
 ["Link clicks","25,548","26,097","<b class='dn'>−2.1%</b>"],
 ["CPM","£7.41","£8.23","<b class='up'>−10.0%</b>"],
 ["Cost per link click","£1.11","£0.91","<b class='dn'>+22%</b>"],
], "num")}
<p class="note">Meta bought more reach more cheaply but converted less of it into clicks. That is the honest
read and it is the weakest part of my paid performance. What offsets it is what was removed — see below.</p>

<h3>What I retired on Meta</h3>
<p>Five ad sets that spent <b>£12,451</b> in the same window last year are now at zero:</p>
{table(["Ad set","LY spend","Status"], [
 ["LA Competition Winners – April Sale","£5,100",chip("crit","Retired")],
 ["Prospecting – Feb Sale FAC","£4,868",chip("crit","Retired")],
 ["Prospecting – Creative Testing","£1,160",chip("crit","Retired")],
 ["Best Sellers DPA","£984",chip("crit","Retired")],
 ["Prospecting – May UGC","£339",chip("crit","Retired")],
], "num")}
<p class="note">The takeover checklist estimated cold prospecting was losing around £14k a quarter. The
£12,451 retired here is the same money, and it now sits in Instant Experience and BOFU Prospecting instead.</p>""")

# ---- 4 GOOGLE ADS ------------------------------------------------------
camprows = []
for nm, ty, cost, clicks, cpc, isv, lb, lr in CAMP:
    tone = "crit" if lb >= 20 else ("watch" if lb >= 10 else "done")
    camprows.append([f"<b>{nm}</b>", ty, f"£{cost:,}", f"{clicks:,}", f"£{cpc:.2f}",
                     f"{isv:.1f}%", chip(tone, f"{lb:.1f}%"), f"{lr:.1f}%"])

sec("google", "Google Ads", "Where the impressions were won and lost, and why",
    "Google Ads — coverage and control", f"""
<div class="kpis">
{kpi("Live campaigns", "8", "all rebuilt and renamed")}
{kpi("Blended CPC", "£1.41", "across my campaigns")}
{kpi("Brand impression share", "96.6%", "2.5% lost to rank")}
{kpi("Spend in my campaigns", "97%", "August — from 13% in June")}
{kpi("Non-brand share of spend", "97.4%", "we buy demand, not our own name")}
{kpi("Spend with query visibility", "24.4%", "the rest is PMax", "crit")}
</div>

<h3>How much of the account is now mine</h3>
{line_chart([(c[0], c[1]) for c in COVER], fmt="{:.0f}", unit="%", floor_zero=True)}
<p class="note">Share of Google spend running through campaigns I built or restructured: <b>13% in June,
66% in July, 97% in August</b>. The June figure is right — I started on 1 June but did not take the account
over until the 25th, so most of that month's spend was still the inherited setup. Caveat worth stating: the
Google export lists currently-existing campaigns only, so the gap is legacy campaigns since removed.</p>

<h3>Campaign by campaign</h3>
{table(["Campaign","Type","Spend","Clicks","CPC","Impr. share","Lost to BUDGET","Lost to RANK"], camprows, "num")}

<div class="callout callout-crit">
  <div class="callout-h">The most important number on this page</div>
  <p>Impression share lost splits into two very different things. <b>Lost to rank</b> is mine — it means my
  bids, quality or relevance were not good enough. <b>Lost to budget</b> is not mine — it means the campaign
  was capable of showing and we chose not to fund it.</p>
  <p>Our three best Search campaigns are losing <b>29.1%, 23.9% and 22.0%</b> of available impressions to
  budget. That is demand we are already qualified to win, at a price we already know, going to competitors
  because the budget runs out. Going into peak, that is the cheapest growth available to us — and it needs a
  decision from you, not a change from me.</p>
</div>

<h3>Why I moved budget out of Performance Max</h3>
{stacked_split([("Google spend", [(f[0], f[1], c) for f, c in zip(FMT, ["seg-b","seg-a","seg-c","seg-c"])])])}
<p><b>{34337/FTOT:.0%} of Google spend runs through Performance Max, and Google publishes no search term
data for it at all.</b> Across the whole period I can see <b>4,243 named search terms totalling £1,907</b> —
about 4% of spend. For the other three quarters I am told the total and nothing else.</p>
<p>That is why budget has been moving into Search. It is not only that Search performs better — it is that
Search is a format where I can see the query, judge whether it was relevant, and add a negative if it was
not. Moving money from PMax to Search converts spend I cannot control into spend I can. If you want me
accountable for traffic quality, this is the mechanism that makes it possible.</p>

<h3>Brand versus non-brand</h3>
{table(["","Spend","Share of Google spend","Clicks","CPC","CTR"], [
 ["<b>Brand</b>","£1,190","2.6%","731","£1.63","38.7%"],
 ["<b>Non-brand</b>","£44,468","97.4%","—","—","—"],
], "num")}
<p class="note">Brand costs us £1,190 to hold 96.6% impression share and defend the name. Everything else —
97.4% of the budget — goes on people who have never heard of us. That is the right shape: we are buying
incremental demand, not paying to appear in front of customers who were already coming.</p>""")

# ---- 5 QUALITY ---------------------------------------------------------
sec("quality", "Traffic quality", "Whether the people I brought were the right people",
    "Was the traffic any good?", f"""
<p class="lede">Engagement rate is the fairest quality measure I have. It captures whether the person I paid
for stayed and did something — which is my responsibility — and stops short of whether they bought, which
depends on price, stock and the site.</p>

<div class="kpis">
{kpi("Paid Google engagement", "74.8%", "vs 82.3% LY", "warn")}
{kpi("Paid Bing engagement", "74.5%", "vs 80.2% LY", "warn")}
{kpi("Paid Meta engagement", "63.5%", "vs 69.6% LY", "warn")}
{kpi("Organic engagement", "68.8%", "vs 71.5% LY")}
{kpi("Negatives applied", "111", "across 4 shared lists")}
{kpi("Search terms reviewed", "4,243", "51 added, 30 excluded")}
</div>

<h3>Engagement rate by channel</h3>
{grouped_bars([(c[0].replace("Paid – ",""), [(c[3]*100,"bar-a"),(c[4]*100,"bar-b")]) for c in CH[:6]])}
<div class="legend"><span class="lg"><i class="sw sw-a"></i>This year</span><span class="lg"><i class="sw sw-b"></i>Last year</span></div>

<div class="callout callout-warn">
  <div class="callout-h">Engagement is down and I want to be the one who says so</div>
  <p>Paid Google engagement fell from 82.3% to 74.8%. Every paid channel softened. The mechanism is
  scale: at 7,777 sessions you are buying only the most obviously relevant traffic; at 17,171 you are
  reaching further out. Some dilution is the price of growth and I would expect it.</p>
  <p>What I would not accept is dilution I cannot see. Three quarters of Google spend is in a format that
  reports no queries, so for most of the budget I am judging relevance from engagement rate alone rather
  than from the search terms themselves. Getting more spend into Search fixes that, and it is why the number
  matters more than it looks.</p>
</div>

<h3>Waste controls built</h3>
{table(["Control","Scale","Where"], [
 ["Repair / DIY / informational negatives","38 keywords","Google + mirrored on Microsoft"],
 ["Second-hand & reclaimed negatives","20 keywords","Google + Microsoft"],
 ["Competitor & other brands negatives","24 keywords","Google + Microsoft"],
 ["Parts / accessories / non-product negatives","29 keywords","Google + Microsoft"],
 ["Microsoft cast iron & column negatives","166 rows","Microsoft"],
 ["Microsoft product exclusions","701 rows","Microsoft PMax Cast Iron"],
 ["Brand exclusion list (ID 11160977849)","all PMax campaigns","Google"],
])}
<p class="note">None of this existed at takeover. The brand exclusion list is the one that matters most: it
stops Performance Max serving on our own name and claiming credit for conversions we would have won anyway.</p>""")

# ---- 6 SEO -------------------------------------------------------------
sec("seo", "SEO", "Slower to move and less directly controllable, but mine to direct",
    "Organic search", f"""
<p class="lede">Less immediate control here than in paid — I can direct the work but rankings move on
Google's timetable, not mine. Google Search Console, same window, both years.</p>

<div class="kpis">
{kpi("Organic clicks", "5,828", "vs 3,575 LY &nbsp;<b class='up'>+63%</b>")}
{kpi("Avg position", "12.1", "from 28.0 &nbsp;<b class='up'>+15.8 places</b>")}
{kpi("CTR", "0.76%", "vs 0.41% &nbsp;<b class='up'>+85%</b>")}
{kpi("Impressions", "764,599", "vs 880,914 &nbsp;<b class='dn'>−13%</b>")}
{kpi("Pages ranking", "987", "vs 977 LY")}
{kpi("Rank tracker", "492 kw", "baseline now established")}
</div>

<div class="callout">
  <div class="callout-h">Read the impression drop the right way</div>
  <p>Impressions fell 13% while clicks rose 63%. That is not a loss — it is the shape you want. We stopped
  appearing on page four for things nobody clicks, and started appearing on page one for things people buy.
  Average position went from 28.0 to 12.1 and CTR nearly doubled. Fewer, better impressions.</p>
</div>

<h3>Biggest page movements</h3>
{table(["Page","Clicks LY","Clicks now","Position LY","Now"], [
 ["<code>/</code> (homepage)","563","<b>1,673</b>","29.5","<b>7.6</b>"],
 ["<code>/product-category/column-radiators/</code>","111","<b>635</b>","22.3","<b>8.2</b>"],
 ["<code>/product-category/antique-brass/</code>","0","<b>164</b>","—","<b>6.5</b>"],
 ["<code>/blog/…landlords-central-heating…</code>","0","<b>147</b>","—","<b>5.4</b>"],
 ["<code>/product-category/traditional-radiators/</code>","2","<b>59</b>","25.3","<b>8.8</b>"],
 ["<code>/product-category/cream-radiators/</code>","64","<b>120</b>","7.3","<b>4.4</b>"],
 ["<code>/product-category/heat-pump-compatible-radiators/</code>","500","<b>540</b>","9.4","<b>6.1</b>"],
], "num")}

<h3>By page type</h3>
{table(["Page type","Clicks","LY","Change"], [
 ["Homepage","1,802","632","<b class='up'>+185%</b>"],
 ["Category pages","2,065","1,050","<b class='up'>+97%</b>"],
 ["Product pages","875","566","<b class='up'>+55%</b>"],
 ["Blog","949","1,226","<b class='dn'>−23%</b>"],
 ["Other","137","101","<b class='up'>+36%</b>"],
], "num")}
<p class="note"><b>Blog is the weak spot and it is mine.</b> Down 23%, with the BTU calculator guide alone
losing 294 clicks. Commercial pages grew strongly, which is the right priority order, but the informational
content has been left to drift while I rebuilt the ad accounts. It goes on the plan.</p>

<div class="callout callout-crit">
  <div class="callout-h">The biggest SEO opportunity is CTR, not rankings</div>
  <p>We hold good positions and get too few clicks from them. The column radiators category sits at position
  <b>8.2</b> and takes <b>635 clicks from 89,900 impressions — a 0.71% CTR</b>. The cast iron category sits at
  position <b>6.7</b> with a <b>0.50% CTR</b>. At those positions you would normally expect several times
  that.</p>
  <p>Ahrefs shows <b>89 pages where our page title and the title Google displays do not match</b> — Google is
  rewriting our titles because they are not earning the click. Rewriting titles and meta descriptions on the
  pages that already rank is the highest-return SEO work available, and it needs no developer and no
  budget. It is the first thing I will do in September.</p>
</div>""")

# ---- 7 DEVICE ----------------------------------------------------------
devrows = []
for nm, s, sh, rev, rps, s25v, rps25, er in DEV:
    devrows.append([f"<b>{nm}</b>", f"{s:,}", f"{sh:.1%}", f"{er:.1%}", f"£{rev:,.0f}",
                    f"£{rps:.2f}", f"£{rps25:.2f}"])

sec("device", "Device", "The mobile question, finally answered",
    "Mobile versus desktop", f"""
<p class="lede">You asked about mobile at the last review and I could not answer it. I can now.</p>

<div class="kpis">
{kpi("Mobile share of sessions", "78.5%", "35,613 sessions")}
{kpi("Mobile share of revenue", "53.4%", "£179,888", "warn")}
{kpi("Mobile revenue/session", "£5.05", "vs desktop £17.43", "crit")}
</div>

{table(["Device","Sessions","Share","Engagement","Revenue","Rev/session","LY rev/session"], devrows, "num")}

<div class="callout callout-crit">
  <div class="callout-h">Four out of five visitors are on a phone. They generate half the revenue.</div>
  <p>A desktop session is worth <b>£17.43</b>. A mobile session is worth <b>£5.05</b> — three and a half times
  less. On paid Google specifically it is £14.53 desktop against £4.57 mobile.</p>
  <p>I can shift budget toward desktop at the margin, and I will where it is sensible. But 78.5% of the
  market is on a phone and we cannot buy our way around that — the traffic is where the traffic is. The gap
  between £5.05 and £17.43 is not a media problem. It is what happens to a phone user once they land.</p>
  <p>This is the clearest example of the boundary I want to agree with you. Finding it, sizing it and
  bringing it to you is my job. Fixing the mobile experience is not — that is Liam and a developer. It is
  logged in the <a href="#escalation" class="jump" data-go="escalation">escalation register</a> as the
  highest-value item on it.</p>
</div>

<p class="note">One honest note in the other direction: mobile revenue per session actually <b>improved</b>
year on year, from £4.31 to £5.05 (+17%), while desktop fell from £19.93 to £17.43 (−13%). So mobile is
getting better, not worse. The gap is still the gap.</p>""")

# ---- 8 ESCALATION ------------------------------------------------------
sec("escalation", "Escalation", "Things costing us money that sit outside my remit",
    "Escalation register", """
<p class="lede">Things I can see from where I sit that are costing us money, and that I cannot fix myself.
Each one needs an owner. I have left the owner column blank on purpose — I would like to fill it in with you
in the meeting rather than assume.</p>

""" + table(["Issue","What it is costing","Suggested owner","Raised","Owner agreed"], [
 ["<b>Mobile converts at a third of desktop</b>","78.5% of sessions at £5.05/session vs £17.43 desktop. The single largest value gap in the business.","Liam + dev","11 Aug","&nbsp;"],
 ["<b>Cast iron SKUs ineligible in the product feed</b>","Windsor £2,167, Oxford £2,320, Mayfair £1,470, Victorian £924–1,116 all marked \"Not eligible — excluded product or listing group\". Two campaigns built to sell products that cannot serve.","Product data — <i>unowned</i>","11 Aug","&nbsp;"],
 ["<b>Discounting at 13.3% of gross, 16.6% in August</b>","£55,669 over the period — comparable to the entire media budget, with none of the scrutiny. Every 1pt = £4,196.","Owner / commercial","11 Aug","&nbsp;"],
 ["<b>Search campaigns capped by budget</b>","Best Search campaigns losing 22–29% of impressions to budget, not rank. Cheapest available growth before peak.","Owner — budget decision","11 Aug","&nbsp;"],
 ["<b>Titles rewritten by Google on 89 pages</b>","Good rankings, poor CTR. Column radiators 0.71% CTR at position 8.2.","Me — Sept","11 Aug",chip("done","Mine")],
 ["<b>612 pages with broken JavaScript</b>","Flagged as errors in crawl. Risks rendering and anything measurement-dependent.","Liam + dev","11 Aug","&nbsp;"],
 ["<b>986 unattributable sessions (2.2%)</b>","Up from 186 LY. Engagement 41% vs 69% site average — points at a tracking or redirect fault.","Me — investigating","11 Aug",chip("done","Mine")],
 ["<b>Gross margin unknown</b>","Every efficiency judgement rests on an inferred 29.8%. With the real number by category I can tell you which categories are worth buying traffic for.","Owner","11 Aug","&nbsp;"],
]) + """
<div class="callout">
  <div class="callout-h">Why this section exists</div>
  <p>Not to push work onto other people. It is so that things I can see but cannot fix have somewhere to go
  other than my own head — and so that in three months nobody has to reconstruct who knew what and when.
  Two of the eight are mine and marked as such.</p>
</div>""")

# ---- 9 NEXT 90 ---------------------------------------------------------
sec("next", "Next 90", "Priorities, and what I need from you",
    "The next 90 days", f"""
<p class="lede">Framed around peak. Everything structural finishes before October; October to December is
monitoring and budget only.</p>

<h3>New channels to stand up</h3>
{table(["Initiative","What it is","Timing","Status"], [
 ["<b>Influencer partnership — RunRagged</b>","Partnership via The VIP Suite. I know the owner directly, so this starts warm rather than cold.","Sept — first activity before peak",chip("part","To scope")],
 ["<b>Pinterest Ads</b>","Set up and live. Strong fit: high-intent interiors audience, visual product, and a channel our competitors are not crowding.","Sept build, live for Oct",chip("part","To build")],
 ["<b>AWIN affiliate programme</b>","Affiliate marketing on a cost-per-sale basis — the only channel here where we pay after the sale rather than before it.","Oct launch",chip("part","To build")],
])}
<p class="note">All three widen the acquisition mix beyond Google and Meta, which currently carry 93% of paid
traffic between them. Affiliate in particular changes the risk shape: we pay on results, not on clicks.</p>

<h3>Month by month</h3>
{table(["","Paid","SEO","Measurement"], [
 ["<b>Aug</b>","Fix Bing cost per session — pacing and budget caps. Decision on PMax Cast Iron.","Title and meta rewrites on the pages that already rank.","Close the 986 unattributed sessions."],
 ["<b>Sept</b>","Pinterest built. RunRagged scoped. Peak budgets agreed and set.","Cast iron hub. Blog recovery started.","Device-level reporting standing. First clean brand vs non-brand read."],
 ["<b>Oct–Dec</b>","<b>Peak — monitoring and budget only.</b> AWIN launches. No structural changes.","Colour variant pages ship.","Monthly pack in this format, automated."],
 ["<b>Jan</b>","Post-peak rebuild on what peak taught us.","Technical debt with dev.","Re-baseline. First true YoY ranking comparison."],
])}

<h3>What I need from you</h3>
{table(["Ask","Why it matters","When"], [
 ["<b>A peak budget envelope</b>","Our best Search campaigns lose 22–29% of impressions to budget. I need to know the ceiling to plan against, and this is the cheapest growth on the table.",chip("crit","By mid-Sept")],
 ["<b>Blended gross margin by category</b>","Every efficiency judgement I make rests on an inferred 29.8%. With the real number I can tell you which categories to buy traffic for and which to stop.",chip("crit","This week")],
 ["<b>An owner for product feed data</b>","Cast iron broke because nobody owns feed eligibility. Name someone and I will build a weekly check around them.",chip("warn","This month")],
 ["<b>Agreement on what I am measured on</b>","The scorecard in this pack. If you want to hold me to something else, I would rather know now than in January.",chip("warn","Today")],
])}

<h3>What I need from Liam and Flora</h3>
{table(["Who","Ask"], [
 ["<b>Liam</b>","Mobile experience is the biggest value gap in the business — a phone session is worth a third of a desktop one. Plus 612 pages with broken JavaScript. Half a day to scope, then an estimate."],
 ["<b>Flora</b>","About a day a week: daily flash entry, weekly search-term pulls, and a weekly feed health check. I will write the procedures first so it is a clean handover."],
])}

<h3>What success looks like by month 6</h3>
{table(["Measure — all within my control","Today","Month 6"], [
 ["Cost per session, blended","£2.73","<b>£2.50 or better</b>"],
 ["Bing cost per session","£5.23","<b>Under £3.50</b>"],
 ["Google spend with query visibility","24.4%","<b>40%+</b>"],
 ["Paid Google engagement rate","74.8%","<b>Back above 78%</b>"],
 ["Impressions lost to budget on Search","22–29%","<b>Under 10%</b>"],
 ["Organic clicks","5,828","<b>9,000+</b> through peak"],
 ["Organic CTR","0.76%","<b>1.2%+</b>"],
 ["Blog clicks","949","<b>Back above 1,226</b> (LY level)"],
 ["Live acquisition channels","3","<b>6</b> — plus Pinterest, affiliate, influencer"],
 ["Escalations with a named owner","0 of 8","<b>8 of 8</b>"],
])}""")

# ---- 10 COMMERCIAL -----------------------------------------------------
sec("commercial", "Commercial", "Sales, spend and ROAS — reported, shared ownership",
    "Commercial outcome", f"""
<div class="kpis">
{kpi("Net sales", "£365,233", "vs £220,623 LY &nbsp;<b class='up'>+66%</b>")}
{kpi("Media spend", "£82,238", "vs £40,896 LY &nbsp;+101%")}
{kpi("Blended ROAS", "4.44x", "vs 5.39x LY")}
{kpi("Orders", "1,061", "vs 668 LY &nbsp;<b class='up'>+59%</b>")}
{kpi("AOV", "£344", "vs £330 LY &nbsp;<b class='up'>+4%</b>")}
{kpi("Discount", "13.3% of gross", "16.6% in August")}
</div>

<p>Reported without commentary or defence. These numbers move with price, stock, range, the site and the
season as much as with media, so I do not present them as a scorecard for my work — but they are the
business's numbers and they should be in front of you every month.</p>

<p class="note">Two points of context rather than argument. Last July the Google account was close to
dormant — LY spend that month was £2,412 against £18,889 this year — so the 5.39x LY ROAS is the arithmetic
of a near-zero denominator rather than a standard we previously held. And on 31 July I excluded past
purchasers from all PMax campaigns to force new-customer acquisition, logging at the time that ROAS and
conversion rate would fall short term; ROAS went 4.48x to 4.23x while AOV rose from £338 to £388.</p>

<div class="callout">
  <div class="callout-h">The one commercial number I would act on</div>
  <p>We spent <b>£82,238</b> on media and gave away <b>£55,669</b> in discount. One of those is reviewed
  daily; the other has never been on an agenda. At 13.3% of gross rising to 16.6% in August, and with half
  of all orders using a coupon, discounting is the largest single lever on profit in the business — and it
  is worth more than any efficiency I can find in the ad accounts. It is not mine to set. It is in the
  escalation register.</p>
</div>

<h3>Reconciliation notes</h3>
<ul class="bul">
  <li>Flash channel components total £84,099 against a stated media spend of £82,238 — a 2.3% variance I am correcting.</li>
  <li>GA4 sessions are not platform clicks; tracking loss and attribution differ. Trends are sound, absolute values differ by source.</li>
  <li>Meta-reported ROAS is platform-attributed and materially inflated. Used for relative ranking between ad sets only, never as a business number.</li>
  <li>The Google campaign export lists currently-existing campaigns only.</li>
  <li>Gross margin of 29.8% is inferred from the 3.36x break-even ROAS in the change journal, not given.</li>
</ul>""")

# ---------------------------------------------------------------- assemble
nav = "".join(f'<button class="tab" data-go="{sid}" role="tab" aria-selected="{"true" if i==0 else "false"}" '
              f'id="tab-{sid}" aria-controls="p-{sid}">{n}</button>'
              for i,(sid,n,q,t,b) in enumerate(SECTIONS))
panels = "".join(
    f'<section class="panel{" on" if i==0 else ""}" id="p-{sid}" role="tabpanel" aria-labelledby="tab-{sid}"'
    f'{"" if i==0 else " hidden"}><p class="eyebrow">{html.escape(q)}</p><h2>{t}</h2>{b}</section>'
    for i,(sid,n,q,t,b) in enumerate(SECTIONS))

DOC = f"""<title>LRD — Traffic &amp; Acquisition Review</title>
<style>{E.CSS if hasattr(E,'CSS') else ''}</style>
<div class="wrap">
<header class="masthead">
  <p class="kicker">Lincs Rads Direct · Paid media &amp; organic acquisition</p>
  <h1>Traffic &amp; acquisition review</h1>
  <p class="sub">Three months of demand acquisition: what I spent, where I sent it, what it cost, and whether
  the people it brought were the right ones. Commercial outcomes are reported at the end as shared ownership.</p>
  <div class="meta">
    <span>Period <b>1 Jun – 10 Aug 2026</b></span>
    <span>Started <b>1 Jun</b></span>
    <span>Handover <b>25 Jun</b></span>
    <span>Sessions <b>{S26:,}</b></span>
    <span>Paid spend <b>£{TC:,.0f}</b></span>
  </div>
</header>
<nav class="tabs" role="tablist" aria-label="Sections">{nav}</nav>
{panels}
<footer>
  Sources: GA4 traffic acquisition (source/medium × device, both years) · Google Ads campaign &amp; search
  terms exports · Microsoft Advertising campaign exports · Meta Ads Manager ad-set export · Google Search
  Console pages · Ahrefs project 9919884 · LRD Daily Flash · Master Change Journal · Paid Media Takeover
  Checklist.<br>
  Comparison window 1 Jun – 10 Aug 2026 against 1 Jun – 10 Aug 2025 throughout. Reconciliation caveats in Commercial.
</footer>
</div>
<script>{E.JS if hasattr(E,'JS') else ''}</script>"""

open(OUT,"w").write(DOC)
print(f"wrote {OUT} ({len(DOC):,} bytes, {len(SECTIONS)} sections)")
