#!/usr/bin/env python3
"""Traffic & acquisition review — paid media led, scoped to controllable metrics."""
import html, importlib.util, os
spec = importlib.util.spec_from_file_location("engine", os.path.join(os.path.dirname(__file__), "engine.py"))
E = importlib.util.module_from_spec(spec); spec.loader.exec_module(E)
grouped_bars, line_chart, stacked_split = E.grouped_bars, E.line_chart, E.stacked_split

OUT = "/home/user/europe-ad-report/traffic-review.html"

# ---------------------------------------------------------------- data
CH = [("Paid – Google",17171,7777,.748,.823), ("Paid – Meta",11530,11030,.635,.696),
      ("Organic",5583,2898,.688,.715), ("Direct",4811,4632,.652,.640),
      ("Referral",3096,2329,.796,.747), ("Paid – Bing",2051,798,.745,.802),
      ("Other",986,186,.414,.344), ("AI assistants",149,11,.617,.636)]
S26=sum(c[1] for c in CH); S25=sum(c[2] for c in CH)
P26,P25 = 17171+11530+2051, 7777+11030+798
SPEND={"Google":(44934,14937),"Bing":(10729,2552),"Meta":(28436,23837)}
SESS ={"Google":(17171,7777),"Bing":(2051,798),"Meta":(11530,11030)}
TC=sum(v[0] for v in SPEND.values()); TC25=sum(v[1] for v in SPEND.values())
CPS,CPS25 = TC/P26, TC25/P25
CAMP=[("GGL | PMax | ALL (excl. Col/Cast)","PMax",8992,8592,1.05,9.6,4.5,73.3),
      ("GGL | PMax | Column","PMax",7648,3315,2.31,25.0,5.7,65.6),
      ("GGL | AI Max Search | Column","Search",1743,631,2.76,3.7,29.1,51.6),
      ("GGL | PMax | Cast Iron","PMax",1345,1860,0.72,13.4,11.2,48.9),
      ("GGL | Search | Brand","Search",1190,731,1.63,96.6,0.9,2.5),
      ("GGL | AI Max Search | Electric","Search",393,151,2.60,2.0,22.0,35.8),
      ("GGL | AI Max Search | Cast Iron","Search",262,49,5.35,1.8,23.9,53.4),
      ("GGL | PMax | Electric","PMax",244,163,1.50,16.2,13.1,68.2)]
WEEKCTR=[("1 Jun",1.89),("8 Jun",2.34),("15 Jun",2.23),("22 Jun",3.87),("29 Jun",3.12),
         ("6 Jul",2.34),("13 Jul",2.19),("20 Jul",2.33),("27 Jul",1.50),("3 Aug",2.42),("10 Aug",2.70)]
COVER=[("June",13),("July",66),("Aug 1–10",97)]
FMT=[("Performance Max",34337),("Search",9611),("Shopping",1551),("Display",160)]
FTOT=sum(f[1] for f in FMT)

def chip(k,t): return f'<span class="chip chip-{k}">{t}</span>'
def kpi(l,v,s="",tone=""):
    return (f'<div class="kpi {tone}"><div class="kpi-l">{l}</div>'
            f'<div class="kpi-v">{v}</div><div class="kpi-s">{s}</div></div>')
def table(h,rows,cls=""):
    th="".join(f"<th>{x}</th>" for x in h)
    tr="".join("<tr>"+"".join(f"<td>{c}</td>" for c in r)+"</tr>" for r in rows)
    return f'<div class="tw"><table class="{cls}"><thead><tr>{th}</tr></thead><tbody>{tr}</tbody></table></div>'
SECTIONS=[]
def sec(sid,nav,quote,title,body): SECTIONS.append((sid,nav,quote,title,body))

# ---- 1 SCORECARD ------------------------------------------------------
sec("scorecard","Scorecard","What I control: budget allocation, cost of traffic, coverage, and click quality",
    "Scorecard", f"""
<div class="kpis">
{kpi("Paid sessions","30,752",f"vs 19,605 LY &nbsp;<b class='up'>+{P26/P25-1:.0%}</b>")}
{kpi("Search CTR","8.15%","vs PMax 1.60% &nbsp;<b class='up'>5.1×</b>")}
{kpi("Brand impression share","96.6%","2.5% lost to rank")}
{kpi("Account rebuilt","97%","of Aug spend — from 13% in June")}
{kpi("Meta waste retired","£12,451","5 ad sets cut to zero")}
{kpi("Cost per session","£2.73",f"vs £{CPS25:.2f} LY &nbsp;+{CPS/CPS25-1:.0%}","warn")}
</div>

{table(["Metric I control","Now","Before","Verdict"],[
 ["Paid sessions delivered","30,752","19,605",chip("done","+57%")],
 ["Search CTR","8.15%","6.93%",chip("done","+18%")],
 ["Budget mix (G / M / B)","56 / 37 / 7","40 / 56 / 4",chip("done","Reallocated")],
 ["Brand impression share","96.6%","unprotected",chip("done","Locked")],
 ["Google spend in my campaigns","97%","13%",chip("done","Rebuilt")],
 ["Loss-making Meta ad sets","0","5 (£12,451)",chip("done","Cut")],
 ["Negative keywords","111 + 166 MSFT","0",chip("done","Built")],
 ["Product exclusions (MSFT)","701","0",chip("done","Built")],
 ["Meta CPM","£7.41","£8.23",chip("done","−10%")],
 ["Cost per session","£2.73","£2.11",chip("watch","+30% while scaling 57%")],
 ["Bing cost per session","£5.23","£3.20",chip("crit","Mine to fix")],
 ["Changes logged with rationale","90+","0",chip("done","Auditable")],
])}

<p class="note">Conversion rate, AOV and revenue are not on this scorecard. They are the product of media
<i>and</i> price, stock, range, site and season. Reported in <a href="#commercial" class="jump" data-go="commercial">Commercial</a>.</p>""")

# ---- 2 WINS -----------------------------------------------------------
sec("wins","What I did","The work, and what it produced",
    "What I did", f"""
<p class="lede">Six things. Each one a decision I made, with the number it produced.</p>

<div class="tri">
  <div class="tri-card tri-a"><div class="tri-h">1 · Protected the brand</div>
  <p>Brand exclusion list applied to every PMax campaign. PMax can no longer serve on our own name and claim
  the conversion.</p>
  <p class="tri-f"><b>96.6%</b> brand impression share · only 2.5% lost to rank · £1,190 to hold it</p></div>

  <div class="tri-card tri-a"><div class="tri-h">2 · Moved budget where I can see it</div>
  <p>Out of Performance Max, into Search. PMax publishes no search term data; Search does.</p>
  <p class="tri-f">Search <b>8.15%</b> CTR vs PMax <b>1.60%</b> — 5.1× better</p></div>

  <div class="tri-card tri-a"><div class="tri-h">3 · Rebuilt the account</div>
  <p>Eight campaigns rebuilt and renamed on a <code>GGL |</code> / <code>MSFT |</code> convention. Listing
  groups subdivided by price band.</p>
  <p class="tri-f">Share of Google spend in campaigns I built: <b>13% → 97%</b></p></div>

  <div class="tri-card tri-a"><div class="tri-h">4 · Cut the Meta bleed</div>
  <p>Five prospecting ad sets retired. The takeover checklist estimated cold prospecting was losing ~£14k a
  quarter.</p>
  <p class="tri-f"><b>£12,451</b> of last year's spend now at zero · CPM <b>−10%</b></p></div>

  <div class="tri-card tri-a"><div class="tri-h">5 · Built the waste controls</div>
  <p>Four shared negative lists, mirrored across Google and Microsoft. Product-level exclusions on cast iron.</p>
  <p class="tri-f"><b>111</b> negatives · <b>166</b> MSFT rows · <b>701</b> product exclusions</p></div>

  <div class="tri-card tri-a"><div class="tri-h">6 · Scaled the traffic</div>
  <p>Paid sessions up 57% on a deliberate reallocation from Meta into search intent.</p>
  <p class="tri-f">Google <b>+121%</b> · Bing <b>+157%</b> · total paid <b>+57%</b></p></div>
</div>

<h3>Before and after</h3>
{table(["","At takeover (9 Jun)","Now"],[
 ["Brand in PMax","Not excluded — cannibalising branded conversions","Excluded on all campaigns, 96.6% IS"],
 ["Campaign naming","Legacy agency <code>ec1 -</code> names","<code>GGL |</code> / <code>MSFT |</code> convention"],
 ["Negative keywords","None","111 across 4 shared lists, mirrored"],
 ["Bing cost data in GA4","Missing — £22,860 revenue, no cost","Flowing"],
 ["Meta cold prospecting","~£14k/quarter loss","Retired — £12,451 of LY spend at zero"],
 ["Account access","Agency card, editor only","Transferred, admin"],
 ["Change record","None","90+ changes, each with before / after / reason"],
 ["Search campaigns","None running","4 live, 8.15% CTR"],
])}""")

# ---- 3 CTR ------------------------------------------------------------
sec("ctr","CTR","Did restructuring the account improve click quality?",
    "Structure and CTR", f"""
<p class="lede">CTR is the cleanest engagement signal I own. It says whether the ad matched the intent.
Split by format, because blended CTR hides the answer.</p>

<div class="kpis">
{kpi("Search CTR","8.15%","up from 6.93% during rebuild")}
{kpi("PMax CTR","1.60%","down from 2.28%","warn")}
{kpi("Gap","5.1×","Search vs PMax")}
</div>

{table(["Format","Pre-handover<br>1–24 Jun","Rebuild<br>25 Jun–30 Jul","Post-restructure<br>31 Jul–10 Aug","Direction"],[
 ["<b>Search</b> — my campaigns, my keywords, my negatives","not running","6.93%","<b>8.15%</b>",chip("done","↑ +18%")],
 ["<b>Performance Max</b> — Google's black box","2.28%","2.19%","<b>1.60%</b>",chip("crit","↓ −30%")],
 ["<b>Blended account</b>","2.28%","2.34%","1.79%",chip("watch","mix effect")],
],"num")}

<div class="callout callout-crit">
  <div class="callout-h">Read the blended number correctly</div>
  <p>Blended CTR fell because <b>PMax is 97% of impressions</b> and PMax CTR is structurally low — it buys
  Display and YouTube inventory, not just search. Search is only <b>2.9%</b> of impressions but converts
  attention five times better.</p>
  <p>Where I control the query, CTR went <b>up 18%</b>. Where Google controls it, CTR fell 30%. That gap is
  the entire argument for moving budget into Search — and it is the number I would judge me on.</p>
</div>

<h3>Weekly account CTR</h3>
{line_chart(WEEKCTR, fmt="{:.1f}", unit="%")}
<p class="note">The dip to <b>1.50%</b> in w/c 27 July is the restructure itself — 90+ changes landed that
week, including the past-purchaser exclusion. The two weeks since are <b>2.42%</b> and <b>2.70%</b>, the
strongest since June. The account absorbed the changes and came back better.</p>

<h3>Why PMax CTR fell — being straight about it</h3>
{table(["Cause","Effect","Mine?"],[
 ["PMax impressions scaled ~20× as budget moved in","Reaches further into low-intent Display and YouTube inventory",chip("part","Partly — I scaled it")],
 ["Past-purchaser exclusion, 31 Jul","Removed the highest-CTR audience in the account. Logged at the time as a deliberate trade-off.",chip("done","Yes — intentional")],
 ["Google does not report PMax queries","I cannot add negatives to what I cannot see",chip("crit","No — platform limit")],
])}
<p class="note">The fix is not to tune PMax. It is to keep shifting budget to formats where the query is
visible and negatives actually work.</p>""")

# ---- 4 MEDIA MIX ------------------------------------------------------
mixrows=[]
for nm,a,b,er,erL in CH:
    yoy=f"<b class='up'>+{a/b-1:.0%}</b>" if a>=b else f"<b class='dn'>{a/b-1:.0%}</b>"
    mixrows.append([f"<b>{nm}</b>",f"{a:,}",f"{a/S26:.1%}",f"{b:,}",yoy,f"{er:.0%}"])
mixrows.append(["<b>Total</b>",f"<b>{S26:,}</b>","100%",f"<b>{S25:,}</b>",f"<b class='up'>+{S26/S25-1:.0%}</b>",""])

sec("mix","Media mix","Paid vs organic, and the shift inside paid",
    "Media mix", f"""
<div class="kpis">
{kpi("Total sessions","45,377","vs 29,661 LY &nbsp;<b class='up'>+53%</b>")}
{kpi("Paid share","67.8%","vs 66.1% LY")}
{kpi("Google share of paid","56%","from 40% LY")}
</div>

<h3>The shift inside paid</h3>
{stacked_split([("This year",[("Google",17171,"seg-a"),("Meta",11530,"seg-b"),("Bing",2051,"seg-c")]),
                ("Last year",[("Google",7777,"seg-a"),("Meta",11030,"seg-b"),("Bing",798,"seg-c")])])}
<div class="legend"><span class="lg"><i class="sw sw-a"></i>Google</span><span class="lg"><i class="sw sw-b"></i>Meta</span><span class="lg"><i class="sw sw-c"></i>Bing</span></div>

<p><b>Meta was 56% of paid traffic. It is now 37%. Google went 40% → 56%.</b> That was five ad sets retired
and the budget moved into search intent.</p>

{table(["Why the shift","Evidence"],[
 ["Search intent converts attention better","Search CTR <b>8.15%</b> vs Meta link CTR <b>0.67%</b>"],
 ["Meta was buying reach, not clicks","Impressions <b>+33%</b>, link clicks <b>−2%</b>, cost per link click <b>+22%</b>"],
 ["Meta prospecting was loss-making","<b>£12,451</b> of LY spend on ad sets now retired"],
 ["Google had headroom","Impression share still under 10% on the main PMax campaign"],
])}

<h3>Sessions by channel</h3>
{table(["Channel","Sessions","Share","LY","YoY","Eng. rate"],mixrows,"num")}

<p class="note">Organic +93% and now 12.3% of traffic, up from 9.8%. See <a href="#seo" class="jump" data-go="seo">SEO</a>
for how much of that I can honestly claim. AI assistants went 11 → 149 sessions — still tiny, fastest-growing source on the site.</p>""")

# ---- 5 COVERAGE -------------------------------------------------------
camprows=[]
for nm,ty,cost,clicks,cpc,isv,lb,lr in CAMP:
    tone="crit" if lb>=20 else ("watch" if lb>=10 else "done")
    camprows.append([f"<b>{nm}</b>",ty,f"£{cost:,}",f"£{cpc:.2f}",f"{isv:.1f}%",chip(tone,f"{lb:.1f}%"),f"{lr:.1f}%"])

sec("coverage","Coverage & cost","Where impressions were won, lost, and what they cost",
    "Coverage and cost", f"""
<div class="kpis">
{kpi("Blended cost/session","£2.73",f"vs £{CPS25:.2f} LY","warn")}
{kpi("Cheapest","Meta £2.47","then Google £2.62")}
{kpi("Most expensive","Bing £5.23","2× Google — mine to fix","crit")}
</div>

{table(["Channel","Spend","LY","Sessions","Cost/session","LY","Change"],[
 ["<b>Google</b>","£44,934","£14,937","17,171","<b>£2.62</b>","£1.92","<b class='dn'>+36%</b>"],
 ["<b>Meta</b>","£28,436","£23,837","11,530","<b>£2.47</b>","£2.16","<b class='dn'>+14%</b>"],
 ["<b>Bing</b>","£10,729","£2,552","2,051","<b>£5.23</b>","£3.20","<b class='dn'>+64%</b>"],
 ["<b>Blended</b>",f"<b>£{TC:,.0f}</b>",f"<b>£{TC25:,.0f}</b>",f"<b>{P26:,}</b>","<b>£2.73</b>","£2.11","<b class='dn'>+30%</b>"],
],"num")}
<p class="note">Cost per session rose 30% while volume rose 57%. That is the auction curve — you do not buy
57% more traffic at the same price. Bing at £5.23 is the exception and it is mine to fix: heavy
budget throttling forced bidding into the most expensive slots.</p>

<h3>Impression share by campaign</h3>
{table(["Campaign","Type","Spend","CPC","Impr. share","Lost to BUDGET","Lost to RANK"],camprows,"num")}

<div class="callout callout-crit">
  <div class="callout-h">Lost to rank is mine. Lost to budget is yours.</div>
  <p>Three Search campaigns are losing <b>29.1%, 23.9% and 22.0%</b> of available impressions to budget —
  demand we are already qualified to win, going to competitors because the money runs out.</p>
  <p>Google's rep put the same point differently: the Column campaign is <i>"Limited by Budget, meaning there
  is still significant demand you aren't capturing"</i>, with our impression share under 10% against
  competitors holding over 50%.</p>
</div>

<h3>Account rebuild — share of Google spend in my campaigns</h3>
{line_chart([(c[0],c[1]) for c in COVER], fmt="{:.0f}", unit="%", floor_zero=True)}
<p class="note">13% in June (handover was the 25th), 66% in July, 97% in August. Caveat: the Google export
lists currently-existing campaigns only, so the gap is legacy campaigns since removed.</p>

<h3>Where the Google budget sits by format</h3>
{stacked_split([("Google spend",[(f[0],f[1],c) for f,c in zip(FMT,["seg-b","seg-a","seg-c","seg-c"])])])}
<p class="note"><b>{34337/FTOT:.0%} of Google spend is in Performance Max, which publishes no search terms.</b>
Across the period I can see 4,243 named terms totalling £1,907 — about 4% of spend.</p>""")

# ---- 6 GOOGLE VERDICT -------------------------------------------------
sec("verdict","Google's review","Independent assessment of the account",
    "Google's account review", """
<p class="lede">I asked Google's account team to review the work. Their assessment, quoted directly.</p>

<div class="callout">
  <div class="callout-h">Overall</div>
  <p>"All of the AI Max campaigns look well set up. <b>Your URL and brand exclusion look great.</b>"</p>
</div>

""" + table(["Area","Google's assessment"],[
 ["<b>PMax Column — tROAS change</b>","\"You've lowered ROAS targets from 440% to 390%. <b>This change is already showing results</b>, your daily spend has increased from roughly £200 to over £370 since the end of July, resulting in <b>over 48 conversions in the last 30 days</b>. However, this well-performing campaign is currently 'Limited by Budget', meaning there is still significant demand you aren't capturing.\""],
 ["<b>Cast Iron restructure</b>","\"On August 3rd you changed a lot… switching to Maximize Conversion Value and adding new ad groups focused on colours and vintage styles. <b>This is actually already giving results. Your Cast Iron conversions went up by 73% last week</b>, proving that your new asset groups are resonating with period-home renovators.\""],
 ["<b>Negative keyword strategy</b>","\"Search term data shows <b>these exclusions are already working</b>. Terms like 'bathroom mountain' and 'kensington radiators', which previously carried cost with no conversions, have now been blocked.\""],
 ["<b>Cast iron negatives</b>","\"By filtering these out, <b>you're helping the AI focus its bidding power</b> on shoppers seeking the specific 'Functional Art' aesthetic of your traditional units.\""],
 ["<b>Combined impact</b>","\"The collective impact of these exclusions, combined with your recent bid strategy shifts, has led to a <b>43% increase in account-level conversion value over the last week</b>… you're showing up more often but being more selective about who you pay for, resulting in a higher-quality click that is more likely to result in a high-value purchase.\""],
 ["<b>Electric line</b>","\"By shifting your Search campaign to Maximize Conversion Value, you're letting the AI know to prioritise higher-margin electric units.\""],
]) + """
<h3>What I am doing with it</h3>
""" + table(["Google's recommendation","Action","Status"],[
 ["Column campaign limited by budget — significant demand not captured","Budget increase request — the ask in <a href='#next' class='jump' data-go='next'>Next 90</a>",chip("watch","Needs your decision")],
 ["Impression share under 10%; Victorian Plumbing and Best Heating hold 50%+","Structural. Budget plus continued tROAS tuning.",chip("part","In progress")],
 ["Add \"Functional Art\" and \"Space Optimisation\" / vertical radiator trends; RAL factory finishes","New asset groups and search themes",chip("part","September")],
 ["AI Max Search Electric in Learning — no tweaks for 7 days","Frozen. No changes until it stabilises.",chip("done","Done")],
 ["Enable Customer Match for lookalike audiences","Account now eligible. Upload past-buyer list.",chip("part","This month")],
 ["Cast iron negative blocking core terms","Identified and removed",chip("done","Fixed")],
])

+ """
<p class="note">Google's figures come from their own live account view and a different window to my exports
(mine end 10 August). Quoted as their assessment, not restated as my numbers.</p>""")

# ---- 7 SEO ------------------------------------------------------------
sec("seo","SEO","Deliberately deprioritised this quarter",
    "SEO", """
<div class="callout callout-warn">
  <div class="callout-h">Straight answer: I did not do much here, on purpose</div>
  <p>Paid media brings most of the revenue and it was in bad shape. It got the quarter. SEO improved over the
  same period, but the step change began in autumn 2025, before I started — <b>I am not claiming credit for
  it.</b> Paid media is 100% mine. This is not.</p>
</div>

""" + table(["Metric","Now","Same window LY","Change"],[
 ["Organic clicks","5,828","3,575","+63%"],
 ["Impressions","764,599","880,914","−13%"],
 ["CTR","0.76%","0.41%","+85%"],
 ["Avg position (impression-weighted)","12.1","28.0","+15.8 places"],
 ["Organic sessions (GA4)","5,583","2,898","+93%"],
],"num") + """
<p class="note">Fewer impressions, better positions, higher CTR. The right shape — but largely momentum from
work that predates me.</p>

<h3>What is actually mine to do next</h3>
""" + table(["Opportunity","Evidence","When"],[
 ["<b>Titles and meta on pages that already rank</b>","Column radiators: 0.71% CTR at position 8.2. Cast iron: 0.50% at 6.7. Ahrefs shows 89 pages where Google rewrites our title.",chip("part","September")],
 ["<b>Blog recovery</b>","Blog clicks −23% YoY. BTU calculator guide alone lost 294 clicks.",chip("watch","Post-peak")],
 ["<b>Cast iron hub</b>","\"cast iron radiators\" — 4,500 searches/month, we rank 29, on the column radiators page.",chip("part","September")],
])
+ """
<p class="note">No developer or budget needed for the first one. It is the highest-return SEO work available
and it is entirely within my control.</p>""")

# ---- 8 ESCALATION -----------------------------------------------------
sec("escalation","Escalation","Costing us money, outside my remit",
    "Escalation register", """
<p class="lede">Things I can see that I cannot fix. Owner column blank on purpose — to fill in together.</p>

""" + table(["Issue","Cost","Owner","Agreed"],[
 ["<b>Mobile converts at a third of desktop</b>","78.5% of sessions at £5.05/session vs £17.43 desktop. Largest value gap in the business.","Liam + dev","&nbsp;"],
 ["<b>Discounting 13.3% of gross, 16.6% in Aug</b>","£55,669 over the period — comparable to the entire media budget. Every 1pt = £4,196.","Owner","&nbsp;"],
 ["<b>Search campaigns capped by budget</b>","22–29% of impressions lost to budget. Google's rep flags the same. Cheapest growth before peak.","Owner","&nbsp;"],
 ["<b>Gross margin unknown</b>","Efficiency judgements rest on an inferred 29.8%. Whether it is measured at full price or net of discount changes break-even from 3.36x to 5.25x — the difference between the account working and losing money.","Owner","&nbsp;"],
 ["<b>No promotional calendar</b>","Pacing budget and setting bid targets blind into the biggest quarter of the year. Discount depth changes required ROAS: 20% off more than doubles it.","Owner","&nbsp;"],
 ["<b>No Black Friday deal plan</b>","Bid strategies, feed flags and creative need 3–4 weeks' lead. If the plan lands in November we run BF on full-price targets.","Owner","&nbsp;"],
 ["<b>612 pages with broken JavaScript</b>","Crawl errors; risks rendering and measurement.","Liam + dev","&nbsp;"],
 ["<b>Product feed eligibility</b>","Cast iron SKUs were ineligible to serve — Windsor £2,167, Oxford £2,320, Mayfair £1,470.",chip("done","Mine"),chip("done","Owned")],
 ["<b>Titles rewritten by Google, 89 pages</b>","Good rankings, poor CTR.",chip("done","Mine"),chip("done","Owned")],
 ["<b>986 unattributable sessions (2.2%)</b>","Up from 186 LY. 41% engagement vs 69% site average — tracking fault.",chip("done","Mine"),chip("done","Owned")],
]) + """
<p class="note">Three of ten are mine and marked as such — including the product feed, which I own end to end.</p>""")

# ---- 9 NEXT 90 --------------------------------------------------------
sec("next","Next 90","Priorities and asks",
    "Next 90 days", """
<h3>New channels</h3>
""" + table(["Channel","Rationale","Live by"],[
 ["<b>Pinterest Ads</b>","High-intent interiors audience, visual product, competitors not crowding it.","Oct"],
 ["<b>AWIN affiliate</b>","Cost-per-sale. The only channel where we pay after the sale, not before the click.","Oct"],
 ["<b>RunRagged influencers</b> (The VIP Suite)","Direct relationship with the owner — starts warm, not cold.","Sept"],
]) + """
<p class="note">Google and Meta carry 93% of paid traffic. These three widen that and change the risk shape.</p>

<h3>Paid media plan</h3>
""" + table(["","Priority"],[
 ["<b>Aug</b>","Fix Bing cost per session (pacing, budget caps). Freeze AI Max Electric for 7 days per Google's advice. Upload Customer Match list."],
 ["<b>Sept</b>","Peak budgets set. Pinterest built. \"Functional Art\" / vertical / RAL asset groups added per Google's market data. Cast iron hub live. <b>Promo calendar and Black Friday deals confirmed.</b>"],
 ["<b>Oct</b>","Black Friday build: tROAS targets set per discount depth, feed promotion flags, listing group splits, creative approved. <b>All done by late Oct</b> — bid strategies cannot be changed during the event."],
 ["<b>Nov–Dec</b>","<b>Peak. Budget and monitoring only.</b> AWIN launches. No structural changes."],
 ["<b>Jan</b>","Post-peak rebuild. Technical debt with dev."],
]) + """
<h3>What I need from you</h3>
""" + table(["Ask","Why","When"],[
 ["<b>The promotional calendar</b>","Sale periods vs full-price periods, with dates and discount depth. Budget pacing, bid targets and creative all key off this. Right now I am pacing blind into the biggest quarter of the year.",chip("crit","This week")],
 ["<b>Black Friday plan — the actual deals</b>","What is on offer, how deep, on which categories, and the start and end dates. Not the messaging — the mechanics.",chip("crit","By 30 Sept")],
 ["<b>Peak budget envelope</b>","Search campaigns lose 22–29% of impressions to budget. Google's rep flags the Column campaign as limited by budget with significant uncaptured demand. Cheapest growth available.",chip("crit","Mid-Sept")],
 ["<b>Gross margin by category</b>","Every efficiency judgement rests on an inferred 29.8%. It also sets the floor on how deep we can discount — see below.",chip("crit","This week")],
 ["<b>A decision on discounting</b>","£55,669 given away vs £82,238 media spend. Not mine to set.",chip("crit","This week")],
 ["<b>Agreement on this scorecard</b>","If you want to measure me on something else, better to know now than in January.",chip("warn","Today")],
]) + """

<h3>Why the promo calendar is a bidding input, not an FYI</h3>
<p>Discount depth changes the ROAS I have to hit. At an assumed 29.8% margin, every extra five points off
the selling price moves break-even sharply:</p>
""" + table(["Discount off selling price","Margin left","Break-even ROAS","What that means"],[
 ["0% — full price","29.8%","<b>3.36x</b>","Current target. Comfortable."],
 ["5%","26.1%","<b>3.83x</b>","Still workable."],
 ["10%","22.0%","<b>4.55x</b>","Above our current blended 4.44x."],
 ["<b>13.3%</b> — our actual average","19.0%","<b>5.25x</b>",chip("watch","We are running 4.44x")],
 ["15%","17.4%","<b>5.74x</b>",chip("watch","Most campaigns lose money")],
 ["<b>16.6%</b> — our August rate","15.8%","<b>6.32x</b>",chip("crit","Only brand search clears this")],
 ["20%","12.2%","<b>8.16x</b>",chip("crit","Nothing in the account clears this")],
 ["25%","6.4%","<b>15.6x</b>",chip("crit","Nothing clears this")],
 ["29.8%+","0%","<b>—</b>",chip("crit","Loss on the product before any media")],
],"num") + """
<div class="callout callout-warn">
  <div class="callout-h">This is why I need the margin figure, not just the calendar</div>
  <p>Everything above depends on one thing I do not know: <b>whether the 29.8% margin is measured at full
  price or already net of discount.</b></p>
  <p>If it is measured at full price, then at our actual 13.3% discount rate the real break-even is
  <b>5.25x</b>, not 3.36x — and we are running <b>4.44x</b>. On that reading, blended paid media is below
  break-even right now and has been all quarter. If the 29.8% is already net of discount, 3.36x stands and
  we are comfortably clear.</p>
  <p><b>Those two readings are the difference between the account working and the account losing money, and
  I cannot tell them apart without the number.</b> It is a one-line answer from finance and it is the single
  most valuable thing I could be given.</p>
</div>
<p class="note">The shape holds either way: <b>a 20% promotion more than doubles the ROAS I need, and
anything past roughly 30% loses money before a penny of media is spent.</b> Bidding to a 3.36x target
through a 20%-off week means buying losses efficiently.</p>

<h3>What I need for Black Friday, specifically</h3>
""" + table(["Input","Why I need it","Lead time"],[
 ["<b>Dates — start, end, any early access</b>","Bid strategies need to be set before the period, not during it. Google's own rep advised a 7-day freeze after a bidding change to let the model stabilise.","<b>4 weeks</b> before"],
 ["<b>Discount depth by category</b>","Sets the tROAS target per campaign. Different depths need different targets — a 10% category and a 25% category cannot share a bid strategy.","<b>4 weeks</b> before"],
 ["<b>Which products are in and out</b>","Feed-level promotion flags, listing group splits, and product exclusions on anything not discounted.","<b>3 weeks</b> before"],
 ["<b>Budget for the period</b>","BF week runs at several times normal daily spend. Caps need raising in advance or we throttle on the busiest day of the year.","<b>3 weeks</b> before"],
 ["<b>Creative and offer messaging</b>","New asset groups, Meta creative, Pinterest pins. All need building and approving.","<b>3 weeks</b> before"],
 ["<b>Merchant Center promotions</b>","Sale price annotations and promotion extensions need submitting and approving by Google.","<b>2 weeks</b> before"],
]) + """
<p class="note">Working back from Black Friday, the first of these is due by <b>late October</b>. If the plan
lands in November, we run it on default settings at full price targets and lose the week.</p>

<h3>From Liam and Flora</h3>
""" + table(["Who","Ask"],[
 ["<b>Liam</b>","Mobile experience — a phone session is worth a third of a desktop one. Plus 612 pages with broken JS. Half a day to scope."],
 ["<b>Flora</b>","A day a week: daily flash entry, weekly search-term pulls, feed health check. Procedures written first."],
]) + """
<h3>Month 6 targets — all within my control</h3>
""" + table(["Measure","Now","Target"],[
 ["Search CTR","8.15%","<b>9%+</b>"],
 ["Blended cost per session","£2.73","<b>£2.50 or better</b>"],
 ["Bing cost per session","£5.23","<b>Under £3.50</b>"],
 ["Google spend with query visibility","24.4%","<b>40%+</b>"],
 ["Impressions lost to budget on Search","22–29%","<b>Under 10%</b>"],
 ["Live acquisition channels","3","<b>6</b>"],
 ["Escalations with a named owner","3 of 10","<b>10 of 10</b>"],
],"num"))

# ---- 10 COMMERCIAL ----------------------------------------------------
sec("commercial","Commercial","Reported, shared ownership",
    "Commercial outcome", """
<div class="kpis">
""" + kpi("Net sales","£365,233","vs £220,623 LY &nbsp;<b class='up'>+66%</b>") + kpi("Media spend","£82,238","vs £40,896 LY &nbsp;+101%") + kpi("Blended ROAS","4.44x","vs 5.39x LY") + kpi("Orders","1,061","vs 668 LY &nbsp;<b class='up'>+59%</b>") + kpi("AOV","£344","vs £330 LY &nbsp;<b class='up'>+4%</b>") + kpi("Discount","13.3%","of gross · 16.6% in Aug","crit") + """
</div>

<p>Reported without commentary. These move with price, stock, range, site and season as much as with media.</p>

<p class="note">Two points of context. Last July the Google account was near dormant — LY spend that month
was £2,412 against £18,889 — so 5.39x LY ROAS is a near-zero denominator, not a standard we held. And on
31 July I excluded past purchasers from all PMax to force new-customer acquisition, logging at the time that
ROAS would fall short term; it went 4.48x → 4.23x while AOV rose £338 → £388.</p>

<div class="callout callout-crit">
  <div class="callout-h">The one commercial number worth acting on</div>
  <p>£82,238 on media. <b>£55,669 given away in discount.</b> One is reviewed daily. The other has never been
  on an agenda. Half of all orders use a coupon. Not mine to set — it is in the escalation register.</p>
</div>

<h3>Reconciliation notes</h3>
""" + table(["Note",""],[
 ["Flash channel components total £84,099 against a stated media spend of £82,238","2.3% variance, being corrected"],
 ["GA4 sessions are not platform clicks","Tracking loss and attribution differ; trends sound, absolutes vary by source"],
 ["Meta-reported ROAS is platform-attributed","Used for relative ad-set ranking only, never as a business number"],
 ["Google campaign export lists current campaigns only","Legacy campaigns removed from the account do not appear"],
 ["Gross margin 29.8% is inferred","Derived from the 3.36x break-even ROAS in the change journal"],
 ["Google rep figures use a different window","Their live account view; my exports end 10 August"],
]))

# ---------------------------------------------------------------- assemble
nav="".join(f'<button class="tab" data-go="{sid}" role="tab" aria-selected="{"true" if i==0 else "false"}" '
            f'id="tab-{sid}" aria-controls="p-{sid}">{n}</button>'
            for i,(sid,n,q,t,b) in enumerate(SECTIONS))
panels="".join(f'<section class="panel{" on" if i==0 else ""}" id="p-{sid}" role="tabpanel" '
               f'aria-labelledby="tab-{sid}"{"" if i==0 else " hidden"}>'
               f'<p class="eyebrow">{html.escape(q)}</p><h2>{t}</h2>{b}</section>'
               for i,(sid,n,q,t,b) in enumerate(SECTIONS))

DOC=f"""<title>LRD — Traffic &amp; Acquisition Review</title>
<style>{E.CSS}</style>
<div class="wrap">
<header class="masthead">
  <p class="kicker">Lincs Rads Direct · Paid media &amp; acquisition</p>
  <h1>Traffic &amp; acquisition review</h1>
  <p class="sub">Three months of demand acquisition: budget allocation, cost of traffic, coverage and click
  quality. Commercial outcomes reported at the end as shared ownership.</p>
  <div class="meta">
    <span>Period <b>1 Jun – 10 Aug 2026</b></span>
    <span>Started <b>1 Jun</b></span>
    <span>Handover <b>25 Jun</b></span>
    <span>Paid sessions <b>{P26:,}</b></span>
    <span>Search CTR <b>8.15%</b></span>
  </div>
</header>
<nav class="tabs" role="tablist" aria-label="Sections">{nav}</nav>
{panels}
<footer>
  Sources: Google Ads campaign, search terms &amp; change history exports · Microsoft Advertising exports ·
  Meta Ads Manager ad-set export · GA4 traffic acquisition by source/medium and device · Google Search
  Console · Ahrefs project 9919884 · LRD Daily Flash · Master Change Journal · Paid Media Takeover Checklist ·
  Google account team review, August 2026.<br>
  All comparisons 1 Jun – 10 Aug 2026 against the same window in 2025.
</footer>
</div>
<script>{E.JS}</script>"""
open(OUT,"w").write(DOC)
print(f"wrote {OUT} ({len(DOC):,} bytes, {len(SECTIONS)} sections)")
