const { Document, Packer, Paragraph, TextRun, HeadingLevel, AlignmentType,
        BorderStyle, TabStopType, TabStopPosition } = require('docx');
const fs = require('fs');

const BRASS = "8C6A3F", INK = "1C1E20", GREY = "5F5C57";

const H1 = (t) => new Paragraph({ heading: HeadingLevel.HEADING_1, spacing:{before:360,after:140},
  children:[new TextRun({ text:t, bold:true, size:30, color:INK, font:"Calibri" })] });
const H2 = (t) => new Paragraph({ heading: HeadingLevel.HEADING_2, spacing:{before:260,after:100},
  children:[new TextRun({ text:t, bold:true, size:24, color:BRASS, font:"Calibri" })] });
const P = (t) => new Paragraph({ spacing:{after:130, line:280},
  children:[new TextRun({ text:t, size:21, color:INK, font:"Calibri" })] });
// label-led paragraph: "Label — body"
const LP = (label, body) => new Paragraph({ spacing:{after:130, line:280}, children:[
  new TextRun({ text:label+" — ", bold:true, size:21, color:INK, font:"Calibri" }),
  new TextRun({ text:body, size:21, color:INK, font:"Calibri" })]});
const RULE = () => new Paragraph({ spacing:{before:40,after:200},
  border:{ bottom:{ style:BorderStyle.SINGLE, size:6, color:"D8D4CC", space:6 } }, children:[] });

const doc = new Document({
  creator: "Lincs Rads Direct",
  title: "90-Day Review — Paid Media, SEO & Site",
  styles: { default: { document: { run: { font:"Calibri", size:21, color:INK } } } },
  sections: [{
    properties: { page: { margin: { top:1080, bottom:1080, left:1080, right:1080 } } },
    children: [

  new Paragraph({ spacing:{after:60}, children:[new TextRun({
    text:"LINCS RADS DIRECT", bold:true, size:16, color:BRASS, characterSpacing:60, font:"Calibri" })]}),
  new Paragraph({ spacing:{after:60}, children:[new TextRun({
    text:"90-Day Review", bold:true, size:44, color:INK, font:"Calibri" })]}),
  new Paragraph({ spacing:{after:40}, children:[new TextRun({
    text:"Paid Media, SEO & Site", size:26, color:GREY, font:"Calibri" })]}),
  new Paragraph({ spacing:{after:220}, children:[new TextRun({
    text:"1 June – 10 August 2026.  Started 1 June, account handover 25 June.",
    size:19, color:GREY, italics:true, font:"Calibri" })]}),
  RULE(),

  H1("What's been done so far"),
  P("The paid accounts were rebuilt from the ground up: every Google and Microsoft campaign is new, renamed to a consistent convention, and 97% of August Google spend now runs through campaigns I built, up from 13% in June. The product feed was migrated to us — I have full access and have mapped Cast Iron to the correct category, where previously it had none and Google was guessing what the products were. Meta was restructured into a proper full funnel and a new tracking pixel installed. On SEO, 10 of 12 CATalyst pages are live with the remaining 2 scheduled next week, plus 2 blog pieces to follow, deliberately paced to avoid over-publishing. Reporting was built from nothing: the daily flash and the paid media pacing document are both new processes."),

  H1("What's improved"),
  P("Sales are up 66% year on year (£365,233 vs £220,623) on 57% more orders, and site sessions are up 53%. Brand is now protected at 96.6% impression share, where previously it wasn't defended at all. Organic clicks are up 63% with average position improving from 28.0 to 12.1. Coupon usage fell from 69.3% of orders to 53.4% and the refund rate from 5.5% to 4.1%. On desktop, where the site works properly, Google Ads orders per session rose from 2.43% to 3.33%."),

  H1("What hasn't worked as expected"),
  P("PMax Cast Iron is running around 1.02x and needs a decision by the end of August. The past-purchaser exclusion applied on 31 July was meant to push new-customer acquisition and hasn't moved the mix yet (68.4% vs 69.9% before), though AOV rose over the same window. Bing costs £5.23 per session against Google's £2.62, which is mine to fix and comes down to budget throttling forcing bids into expensive slots. I also made too many changes in one week at the end of July, which makes clean attribution harder than it should have been."),

  H1("What still needs sorting"),
  P("The promotional calendar and Black Friday deal plan — I'm currently pacing budget and setting bid targets blind into the biggest quarter of the year. Whether reported revenue is inc or ex VAT, which decides whether break-even ROAS is 1.75x or 2.10x. Mobile conversion, where the number of sessions reaching checkout has halved. Meta event tracking still needs tweaking, and 612 pages carry broken JavaScript. All logged in the escalation register with owners."),

  RULE(),
  H1("Google Ads"),
  LP("What's changed","Everything. New PMax campaigns with new assets and feed segmentation, a new branded search campaign with a strong negative keyword strategy, and AI Max search campaigns for Column, Cast Iron and Electric. Google is 53% of media spend and none of the current structure existed in June."),
  LP("Brand vs non-brand","Brand is 2.6% of Google spend (£1,190) and holds 96.6% impression share with only 2.5% lost to rank. The other 97.4% buys people who've never heard of us. Brand exclusion lists on every PMax campaign stop PMax serving on our own name and claiming the conversion."),
  LP("PMax","Four PMax campaigns rebuilt with price-band listing groups and new asset groups. PMax is 75% of Google spend but publishes no search term data, which is why budget has been moving into Search where I can see and control the query."),
  LP("ROAS","Blended 4.44x against 5.39x last year. Break-even is roughly 1.75x–2.10x on the real margin data, so we're running at about twice break-even. Last July's 5.39x came off a near-dormant account (£2,412 Google spend that month), so it isn't a like-for-like benchmark."),
  LP("Spend","£44,934 on Google against £14,937 last year. Budget moved out of broad PMax and into Search: AI Max Search Column is up 300% and is the best performing campaign in the account."),
  LP("What's still testing","AI Max on brand search (highest risk, monitored weekly), AI Max Cast Iron launched 3 August, the past-purchaser exclusion, and Microsoft PMax without tROAS targets. Google's account team reviewed the work and confirmed the AI Max campaigns, URL and brand exclusions are correctly set up."),
  LP("Anything needing amending or reversing","PMax Cast Iron gets paused end of August unless the feed work moves it. The Towel campaign had URL expansion switched on while I tightened the tROAS, which pulls in opposite directions and needs reversing. Google's rep flagged a cast iron negative blocking core terms, which I've already removed."),

  H1("SEO"),
  LP("What's been fixed","10 of 12 CATalyst pages are published, with 2 more and 2 blog pieces scheduled next week to pace publishing sensibly. 290 H1 tags and 133 title tags were changed across category and product templates. Ahrefs is set up, working and in frequent use — it surfaced a set of 404 errors which I've since fixed with redirects, recovering links that were previously dead ends for both users and crawlers."),
  LP("What pages have improved","The homepage moved from position 29.5 to 7.6 and now takes 1,673 clicks against 563. Column radiators went from 22.3 to 8.2 and from 111 clicks to 635. Antique brass and traditional radiators are both new entries in the top 10."),
  LP("What opportunities are there","\"Cast iron radiators\" is 4,500 searches a month, we rank 29, and the page ranking for it is the column radiators page rather than a cast iron page. We already rank #1 for three heat pump terms, a category that grows with the boiler phase-out. Titles and meta on pages that already rank are the highest-return work available — 89 pages have Google rewriting our title."),
  LP("What needs dev support","612 pages with broken JavaScript, 178 schema validation errors, 130 pages with multiple H1s and 13 orphan pages. Half a day of Liam's time to scope, then an estimate. Best scheduled post-peak in January."),
  LP("Plan for the next 3–6 months","September: cast iron category hub, remaining CATalyst pages, title and meta rewrites. October to December: colour variant pages only, no structural changes during peak. January onwards: technical debt with dev, then re-baseline for a true year-on-year ranking comparison in February."),

  H1("Website / CRO"),
  LP("Conversion rate","Site orders per session is 2.37% against 2.31% last year, holding while sessions grew 53%. On desktop it improved materially, from 2.43% to 3.33% on paid Google."),
  LP("Product pages","The PDP layout has been refreshed and a new cast iron category layout built. Reassurance messaging added to the top bar."),
  LP("Mobile","This is the biggest gap in the business. Mobile is 78.5% of sessions but 53.4% of revenue, and a mobile session is worth £5.05 against £17.43 on desktop. Sessions reaching checkout on mobile halved from 9.83% to 4.72%, while checkout completion actually improved — so the problem is between landing and basket, not at the checkout."),
  LP("Checkout","Upsells moved underneath the basket to keep the checkout friction-free, and a sticky voucher code bar added. Checkout completion on desktop paid traffic improved from 39.6% to 48.4%."),
  LP("Upsells / accessories","Accessories take 5.4% of traffic and produce 2.3% of revenue, and TRVs got 7 clicks in Shopping across the whole period. Every radiator sold needs valves, so the opportunity is basket attachment at the point of sale rather than paid traffic to a valve page."),
  LP("Obvious issues stopping people buying","Mobile browse-to-basket, as above. 35% of sessions land on pages that produced no revenue, including our single most-visited product page (265 sessions, £0). Cast iron converts in white but the period ranges took 208 sessions and produced nothing, which points at stock, lead time or price presentation rather than demand."),

  H1("Reporting"),
  LP("Sales vs last year","£365,233 against £220,623, up 66%. July finished +0.5% against target and August is +7.2% month to date."),
  LP("Spend","£82,238 against £40,896, up 101%. Google £44,934, Meta £28,436, Bing £10,729."),
  LP("ROAS","4.44x against 5.39x, against a real break-even of roughly 1.75x–2.10x."),
  LP("Orders","1,074 against 684, up 57%."),
  LP("CVR","2.37% orders per session against 2.31%."),
  LP("AOV","£327 against £319."),
  LP("Organic","Sessions up 93%, clicks up 63%, average position from 28.0 to 12.1, orders per session from 2.00% to 3.28%."),
  LP("Paid","Sessions up 57%. Within paid, Google moved from 40% to 56% of traffic and Meta from 56% to 37%."),

  H1("Workload"),
  LP("What's taking too much time","Daily media pacing across 30+ campaigns on three platforms, maintained by hand. It's a spreadsheet doing a script's job and it's the largest recurring time cost I have."),
  LP("What could go to Flora","Daily flash data entry, weekly search term pulls for me to approve, and a weekly feed health check. Roughly a day a week. I'd write the procedures first so it's a clean handover rather than a transfer of confusion."),

  H1("Processes"),
  P("The daily flash, the pacing document and the change journal are all new and already running — the documentation habit exists. What's missing is written procedures so someone else can pick the tasks up. I'd commit to three before peak: daily pacing, weekly feed health check, and monthly reporting."),

  H1("Campaign changes"),
  LP("Why changes were made","Google changes break down roughly as ads and assets (351), budget reallocations (291), product and listing group segmentation (121), keywords (94) and negatives (75). Microsoft is similar at larger volume on ads and assets. Every change is logged with a before, an after and a reason."),
  LP("What worked","Brand exclusions on PMax, moving budget from PMax into Search, retiring five loss-making Meta ad sets worth £12,451 of last year's spend, and getting Bing cost data into GA4 where £22,860 of revenue previously had no cost attached."),
  LP("What didn't","Scaling PMax Cast Iron before checking feed eligibility, and changing two Towel campaign settings that pulled against each other."),
  LP("SEO notes","Content is paced deliberately rather than published in bulk. The cast iron cluster currently ranks on the wrong page, which is the single biggest fix available."),

  H1("Next 90 days"),
  LP("Top priorities","Fix cast iron end to end (feed, category hub, colour pages). Get Bing cost per session down. Be fully season-ready by 30 September, with no structural changes during peak."),
  LP("What I need from you","The promotional calendar and the Black Friday deal plan, both of which are bidding inputs rather than information. A peak budget envelope. Whether reported revenue is inc or ex VAT."),
  LP("What I need from Liam and Flora","Liam: scoping on mobile browse-to-basket and the 612 broken JavaScript pages. Flora: about a day a week on the flash, search term pulls and feed health checks."),
  LP("Budget / tools","No new tools needed. A peak budget number to plan against, and our best Search campaigns are currently losing 22–29% of available impressions to budget, which is the cheapest growth on the table."),

  H1("What success looks like by month 6"),
  P("Cast iron ranking top 10 on a dedicated page rather than 29 on the wrong one. Bing cost per session under £3.50. Impressions lost to budget on Search under 10%. Six live acquisition channels rather than three, with Pinterest, AWIN affiliate and the VIP Suite influencer programme added. Every item on the escalation register with a named owner."),

  H1("Basically"),
  LP("What have we learned","The account is now controllable and measurable in a way it wasn't. The biggest remaining constraints sit outside media: mobile conversion, discount depth, and the promotional calendar."),
  LP("Where are we better","Sales, orders, organic visibility, brand protection, tracking, and desktop conversion. Coupon dependency and refunds are both down."),
  LP("Where are we still weak","Mobile conversion, Bing efficiency, blog content, and Meta event tracking."),
  LP("What are we doing next","Cast iron end to end, season readiness by 30 September, then three new channels."),

  H1("Anything I'd add"),
  P("I'm in engaged conversation with VIP Suite (Run Ragged) about a structured influencer programme. I've also built custom GA4 segments isolating people who viewed a category but didn't buy — the mechanism is live and once each list passes 1,000 people we can retarget them properly."),

    ]}]});

Packer.toBuffer(doc).then(b => { fs.writeFileSync("90-day-review.docx", b); console.log("written", b.length, "bytes"); });
