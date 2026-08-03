# UK Search Campaign — Cast Iron Radiators (AI Max enabled)

**Advertiser:** Lincolnshire Radiators Direct
**Final URL:** `https://lincsradsdirect.co.uk/product-category/cast-iron-radiators/`
**Market:** United Kingdom
**Source data:** `Keyword Stats 2026-08-03` (Google Keyword Planner, Jul 2025 – Jun 2026 avg. monthly searches)

Files in this folder are ready for Google Ads Editor import:

| File | Contents |
|---|---|
| `keywords.csv` | 88 keywords across 6 ad groups, with match type + KWP volume |
| `ads-rsa.csv` | 6 responsive search ads (15 headlines / 4 descriptions each) |
| `negative-keywords.csv` | 109 campaign-level negatives in 4 themed groups |

---

## 1. TL;DR recommendation

One campaign, **five ad groups at launch** (a sixth is conditional on stock), built on
**exact + phrase only** — no broad match. AI Max's search term matching is the expansion
layer, so broad match keywords would duplicate it while giving you less reporting clarity
and less control.

The keyword data is extremely top-heavy: the generic "cast iron radiator(s)" cluster is
~15,600 searches/month, which is **~78% of all commercial volume in your export**. Everything
else is a modifier tail. So the structure below is deliberately not symmetrical — one core
ad group carries the volume, and four modifier ad groups exist so that ad copy can match
the specific intent (colour, size, period style, purchase intent).

---

## 2. Volume analysis — where the themes actually are

Keyword Planner reports identical volume for terms it has clustered together (e.g.
`cast iron radiators`, `castironradiators` and `radiator iron cast` all show 12,100 — that is
one bucket of 12,100, not 36,300). The table below is **de-duplicated**, so these are real
addressable volumes.

| Theme | De-duplicated avg. monthly searches | Share | Ad group |
|---|---:|---:|---|
| Generic "cast iron radiator(s)" | ~15,600 | 78% | 01 Core |
| Vintage / traditional / ornate / replica | ~1,650 | 8% | 03 Vintage |
| Size & fit (tall, small, slim, wall mounted, low) | ~940 | 5% | 05 Size |
| Colour & finish (black, white, grey, cream, brass…) | ~850 | 4% | 04 Colour |
| Buy / for sale / near me / cheap | ~580 | 3% | 02 Buy |
| Electric cast iron | ~410 | 2% | 06 Electric (conditional) |

**Deliberately excluded from the build:**

- `castironradiatorcentre` (1,600) and `cast iron radiator center` (40) — competitor brand.
  Also `paladin` (50), `b and q cast iron radiators` (90), `cast iron radiators for you` (40).
  These go in the negative list *and* in the AI Max brand exclusions.
- `silver radiator` (390) — high volume but not cast-iron-specific. Mixed intent (towel rails,
  car radiators, general chrome/silver panel rads). Worth a controlled test later in the Colour
  ad group at a low bid ceiling, not at launch.
- `cast iron radiator feet` cluster (170) and gaskets/bushes/wall ties — accessory intent, not
  the category page. Add a separate accessories ad group only if you stock and want to sell parts;
  otherwise they are negatives (they are in the negative file by default).
- `refurbished / restored / reconditioned cast iron radiators` (~220 combined) — these searchers
  want reclaimed originals. **Only add these if you actually sell restored stock.** They are
  negatives by default; delete that block from `negative-keywords.csv` if you do.
- Repair/DIY informational terms (leaking, bleeding, sandblasting, welding, sizing, moving…) —
  ~250 combined, all non-commercial. Negatives.

**Seasonality note for pacing:** the trend in your export is clear — peaks in Oct/Nov and again
in Jan (14,800/mo on the head term), trough in Jun (6,600). That is a **2.2x swing**. The head
term is also down 19% YoY and −33% over three months, so budget your Q4 ramp on the monthly
columns rather than on the 12-month average.

---

## 3. Campaign settings

| Setting | Recommendation | Why |
|---|---|---|
| Campaign type | Search, "Website traffic"/"Sales" goal, no display network, no search partners at launch | Keep the AI Max signal clean; test search partners after 4 weeks |
| Networks | Google Search only | Uncheck Display and Search Partners initially |
| Locations | United Kingdom, **Presence: people in your targeted locations** | Default "presence or interest" wastes budget on non-UK research traffic |
| Language | English | |
| Bidding | **Maximise conversions with tCPA**, or **tROAS** if you pass purchase value | AI Max's search term matching, text customisation and final URL expansion all require conversion-based Smart Bidding — they will not function on manual CPC |
| Budget | Start at a level that gives the campaign **≥30 conversions/month** | Below that, Smart Bidding + AI Max cannot learn. If your budget can't support 5 ad groups at that level, launch with 3 (see §4) |
| Ad rotation | Optimise (default) | |
| Ad schedule | All hours at launch | |
| Device | No modifiers at launch | |
| Final URL | Category page for all ad groups | As specified |

### AI Max settings

| Control | Setting | Notes |
|---|---|---|
| Search term matching | **On** | This is the expansion engine. It learns from your keywords, ad copy and landing pages |
| Final URL expansion | **On, with URL rules** | Lets Google route a query for "black cast iron radiator" to the actual black product page instead of the category page. Add **URL exclusions** for `/blog/`, `/about/`, `/basket/`, `/checkout/`, `/my-account/`, `/contact/` so it can't send paid traffic to non-commercial pages |
| Text customisation | **On** | Generates headlines/descriptions from your landing page. Requires strong base assets — this is why each ad group below has the full 15 headlines |
| Brand inclusions | Leave off | You want non-brand reach here |
| Brand exclusions | **Add:** Cast Iron Radiator Centre, Paladin, Arroll, Carron, Trads, B&Q, Screwfix, Wickes, Homebase, UKAA, Castrads | Stops AI Max matching to competitor-brand queries |
| Locations of interest | Optional — add Lincolnshire/regional if you want local weighting | Only if you see value in local intent |
| Text guidelines | Add your brand/tone rules and any claims you can't legally make | e.g. lock the guarantee wording |

### Interaction with your existing Performance Max campaign

This matters, because you're running Pmax on the same theme:

- A Search campaign keyword that **exactly matches** the user's query (or its spell-corrected
  form) takes priority over Performance Max. Everything else is decided on Ad Rank, and Pmax
  usually wins those.
- **Implication:** the exact-match keywords in this build are your guarantee of serving on the
  head terms. That's why the highest-volume terms are exact match, not just phrase.
- AI Max's keywordless expansion competes with Pmax on Ad Rank rather than beating it by rule,
  so expect some of the new reach to be reallocated rather than incremental. Watch total
  category cost/conv, not just this campaign's.
- Don't add the same negatives to Pmax that you add here, or you'll suppress the theme in both.
- If either campaign becomes budget-limited, the precedence rule silently stops applying —
  a budget-limited Search campaign hands its exact-match queries back to Pmax.

---

## 4. Ad group structure

All six ad groups point at the same final URL, with paths `/cast-iron/radiators`.

| # | Ad group | Match types | Keywords | Est. volume |
|---|---|---|---|---:|
| 01 | Cast Iron Radiators (Core) | Exact + Phrase | 14 | ~15,600 |
| 02 | Cast Iron Radiators For Sale (Buy) | Exact + Phrase | 14 | ~580 |
| 03 | Vintage & Traditional Cast Iron | Exact + Phrase | 15 | ~1,650 |
| 04 | Cast Iron Radiators By Colour | Exact + Phrase | 17 | ~850 |
| 05 | Cast Iron Radiators By Size & Fit | Exact + Phrase | 21 | ~940 |
| 06 | Electric Cast Iron Radiators | Exact + Phrase | 7 | ~410 |

**Ad group 06 is conditional** — build it only if you stock electric or dual-fuel cast iron.
If you don't, add `electric`, `dual fuel` and `oil filled` to the negative list instead.

**If budget is tight (< ~£40/day):** launch with three ad groups only — 01 Core, 03 Vintage,
and a merged "Colour & Size" group — then split out as conversion volume builds. Six thin ad
groups will each sit below the data threshold Smart Bidding needs, and AI Max performs
noticeably better with consolidated conversion signal.

### Why exact + phrase, and not broad

With AI Max on, broad match and search term matching do substantially the same job. Running both
means you can't tell which mechanism found a converting query, and broad match will pull budget
from your head terms during the learning period. Keep exact for the head, phrase for the
modifier tail, and let AI Max own everything beyond that. If after 6 weeks the Search Terms
report shows AI Max isn't finding new queries, that's when to test broad on the core group.

---

## 5. Keywords by ad group

Full list with volumes is in `keywords.csv`. Summary:

### 01 — Cast Iron Radiators (Core) · ~15,600/mo
**Exact:** `[cast iron radiators]` (12,100) · `[cast iron radiator]` (2,400) · `[cast iron rads]` ·
`[cast iron rad]` · `[iron radiator]` (480) · `[iron radiators]`
**Phrase:** `"cast iron radiators"` · `"cast iron radiator"` · `"cast iron rads"` · `"iron radiators"` ·
`"cast iron radiator heater"` (2,400) · `"wrought iron radiators"` (90) · `"cast iron heaters"` (40) ·
`"cast iron central heating radiators"`

> `wrought iron radiators` is a misnomer — there's no such product — but the searcher wants cast iron.
> Keep it.

### 02 — Cast Iron Radiators For Sale (Buy) · ~580/mo
**Exact:** `[cast iron radiators for sale]` (320) · `[cast iron rads for sale]` ·
`[cast iron radiators near me]` (110) · `[buy cast iron radiators]`
**Phrase:** `"cast iron radiators for sale"` · `"cast iron radiator for sale"` · `"cast iron rads for sale"` ·
`"buy cast iron radiator"` · `"cast iron radiators near me"` · `"cheap cast iron radiators"` (110) ·
`"affordable cast iron radiators"` · `"iron radiators for sale"` · `"trade cast iron radiators"` ·
`"cast iron radiators price"`

> `"cheap cast iron radiators"` has 110/mo and a 100% ad impression share in your export — it's
> contested and low-margin. If you're positioned on quality rather than price, move it to negatives.

### 03 — Vintage & Traditional Cast Iron · ~1,650/mo
**Exact:** `[vintage radiators]` (1,300) · `[ornate cast iron radiators]` (90)
**Phrase:** `"vintage cast iron radiators"` · `"vintage radiators"` · `"antique cast iron radiators"` ·
`"traditional cast iron radiators"` · `"victorian cast iron radiators"` · `"ornate cast iron radiators"` ·
`"ornate radiators"` (50) · `"decorative cast iron radiators"` (50) · `"period cast iron radiators"` ·
`"reproduction cast iron radiators"` · `"replica cast iron radiators"` (70) ·
`"classic cast iron radiators"` · `"original cast iron radiators"`

> `vintage radiators` at 1,300/mo is the second-biggest theme in the whole dataset, but it's the
> riskiest: a meaningful share want *reclaimed originals*, not new reproductions. The reclaimed
> negatives in `negative-keywords.csv` are what make this ad group viable. Watch its search terms
> weekly for the first month.

### 04 — Cast Iron Radiators By Colour · ~850/mo
**Exact:** `[black cast iron radiator]` (390) · `[white cast iron radiators]` (260)
**Phrase:** `"black cast iron radiators"` · `"cast iron radiator black"` · `"matt black cast iron radiator"` ·
`"white cast iron radiators"` · `"cast iron white radiator"` · `"grey cast iron radiator"` ·
`"anthracite cast iron radiator"` · `"cream cast iron radiator"` · `"brass cast iron radiator"` (40) ·
`"bronze cast iron radiators"` · `"polished cast iron radiator"` · `"chrome cast iron radiator"` ·
`"gunmetal grey cast iron radiator"` · `"pewter cast iron radiators"` · `"coloured cast iron radiators"`

> Black is 46% of this ad group on its own. This is the ad group where **final URL expansion earns
> its keep** — let it route colour queries to the matching product/filter pages.

### 05 — Cast Iron Radiators By Size & Fit · ~940/mo
**Exact:** `[tall cast iron radiators]` (210) · `[wall mounted cast iron radiators]` (170) ·
`[small cast iron radiator]` (140)
**Phrase:** `"tall cast iron radiators"` · `"small cast iron radiators"` · `"wall mounted cast iron radiators"` ·
`"cast iron wall radiators"` · `"slim cast iron radiators"` (90) · `"slimline cast iron radiators"` ·
`"narrow cast iron radiator"` (50) · `"thin cast iron radiators"` · `"low cast iron radiators"` (50) ·
`"low level cast iron radiators"` · `"low profile cast iron radiator"` · `"large cast iron radiators"` ·
`"long cast iron radiators"` · `"curved cast iron radiator"` (40) · `"column cast iron radiators"` ·
`"2 / 3 / 4 column cast iron radiators"`

> The column keywords are **not in your export** — I added them from category structure. Run them
> through Keyword Planner before launch; in my experience they carry real UK volume that your
> seed list didn't surface because the seed was "cast iron" rather than "column".

### 06 — Electric Cast Iron Radiators (conditional) · ~410/mo
**Exact:** `[electric cast iron radiator]` (390)
**Phrase:** `"electric cast iron radiators"` · `"cast iron electric radiators"` ·
`"electric radiators cast iron"` · `"cast iron oil filled electric radiators"` ·
`"oil filled cast iron radiator"` · `"dual fuel cast iron radiators"`

> Note this theme is one of the few in your data that is **flat YoY (0%)** while the head term is
> −19%. If you stock it, it's the growth pocket.

---

## 6. Negative keywords

109 phrase-match negatives in `negative-keywords.csv`, in four blocks. Apply as a **shared
negative list** at campaign level so you can reuse it:

1. **Repair, DIY & informational** (33) — how to, leaking, bleeding, sandblasting, welding, sizing,
   moving, fitting, on carpet…
2. **Second-hand & reclaimed** (22) — used, reclaimed, salvage, ebay, gumtree, scrap, refurbished,
   restored… *Delete this block if you sell restored stock.*
3. **Competitor & other brands** (25) — Cast Iron Radiator Centre, Paladin, B&Q, Screwfix, Trads,
   Arroll, Carron… **Check these against your own product names first** — `duchess`, `daisy`,
   `kensington`, `windsor`, `coventry`, `sovereign` appear in your keyword export and several of
   those are common *model* names in this category. If any are your own SKUs, remove them from the
   list and put them in ad group 03 instead.
4. **Parts, accessories & non-product** (29) — feet, gaskets, bushes, valves, covers, towel rail,
   car radiator, hydronic, steam…

Also add `hydronic`, `steam`, `american`, `st paul`, `wagner`, `clow` — these are US-market terms
that appear in your export and will never convert on a UK site.

---

## 7. Responsive search ads

Full assets in `ads-rsa.csv`. **Specs used** — RSA allows up to 15 headlines at 30 characters and
4 descriptions at 90 characters, minimum 3 headlines and 2 descriptions; two display paths at 15
characters each. Every asset below has been length-checked and is within limits.

**Pinning:** don't pin anything. Pinned assets are excluded from AI Max text customisation, so
pinning throws away the feature you're enabling. If compliance forces a pin, pin one headline to
position 1 and leave the other 14 free.

### 01 — Cast Iron Radiators (Core)

**Headlines:** Cast Iron Radiators · Cast Iron Radiators UK · Buy Cast Iron Radiators ·
Cast Iron Radiators Online · Shop Cast Iron Rads Direct · Free UK Delivery · Up To 20 Year Guarantee ·
12 Colours & Colour Match · Finished In Lincolnshire · Traditional Cast Iron Rads ·
Classic Style, Modern Heat · Expert Radiator Advice · Order Direct & Save · Trusted By UK Homeowners ·
See The Full Range Today

**Descriptions:**
1. Classic cast iron radiators with free UK delivery. 12 colours or matched to your own.
2. Authentic period styling with the heat output your rooms need. Order online today.
3. Bespoke sizes and finishes, backed by a guarantee of up to 20 years. Free delivery.
4. Browse the full cast iron range, compare outputs and buy direct from our experts.

### 02 — Cast Iron Radiators For Sale (Buy)

**Headlines:** Cast Iron Radiators For Sale · Buy Cast Iron Radiators · Cast Iron Rads For Sale ·
Cast Iron Radiators Near You · Shop Cast Iron Radiators · Free Delivery On All Orders ·
Great Value Cast Iron Rads · Buy Direct From The Experts · Direct Prices, No Middleman ·
Up To 20 Year Guarantee · Fast UK Dispatch · 12 Colours To Choose From · Order Online In Minutes ·
Get A Quote Today · Cast Iron Radiators UK

**Descriptions:**
1. Cast iron radiators for sale with free UK delivery on every order. Buy online today.
2. Buy direct and skip the showroom mark-up. Expert help by phone or email when you need it.
3. Hundreds of sizes and 12 colours in stock-ready finishes. Up to 20 year guarantee.
4. Compare sizes, outputs and prices online, then order your cast iron radiators direct.

### 03 — Vintage & Traditional Cast Iron

**Headlines:** Vintage Cast Iron Radiators · Traditional Radiators · Victorian Style Radiators ·
Ornate Cast Iron Radiators · Decorative Cast Iron Rads · Reproduction Cast Iron Rads ·
Period Style, Modern Heat · Classic Column Designs · Authentic Cast Iron Detail · 12 Heritage Colours ·
Colour Matched To Your Home · Free UK Delivery · Up To 20 Year Guarantee · Shop The Vintage Range ·
Finished In Lincolnshire

**Descriptions:**
1. Vintage-style cast iron radiators with period detailing and modern heat output.
2. Victorian and ornate column designs in 12 colours, or matched to your own scheme.
3. New reproduction cast iron radiators. No restoration needed, free UK delivery.
4. Traditional looks, guaranteed for up to 20 years. Browse the full range online.

> Descriptions 3 explicitly says "new reproduction" — that's intentional pre-qualification against
> the reclaimed-seeker traffic this ad group attracts.

### 04 — Cast Iron Radiators By Colour

**Headlines:** Black Cast Iron Radiators · White Cast Iron Radiators · Coloured Cast Iron Rads ·
Anthracite & Grey Finishes · Matt Black, Cream & More · 12 Colours To Choose From ·
Colour Matched To Any RAL · Polished & Brass Finishes · Bespoke Radiator Finishes ·
Order Your Colour Online · See The Full Colour Range · Cast Iron Radiators UK · Free UK Delivery ·
Up To 20 Year Guarantee · Finished In Lincolnshire

**Descriptions:**
1. Cast iron radiators in black, white, anthracite, cream and 8 more stock colours.
2. Cannot find your shade? We colour match cast iron radiators to your chosen finish.
3. Hand-finished in Lincolnshire and delivered free anywhere in the UK. Order online.
4. Pick your size, then pick your colour. Up to 20 year guarantee on every radiator.

### 05 — Cast Iron Radiators By Size & Fit

**Headlines:** Tall Cast Iron Radiators · Small Cast Iron Radiators · Slim Cast Iron Radiators ·
Low Level Cast Iron Rads · Wall Mounted Cast Iron Rads · Sizes To Fit Any Room ·
Heights From Low To Tall · 2, 3 & 4 Column Options · Made To Your Size · Bespoke Cast Iron Radiators ·
Find Your Perfect Fit · Check Heat Output Online · Cast Iron Radiators UK · Free UK Delivery ·
Up To 20 Year Guarantee

**Descriptions:**
1. Tall, small, slim or low level cast iron radiators to fit the space you have.
2. Awkward alcove or under a window? Bespoke sizes built to your measurements.
3. Filter by height, width and heat output to find the right fit. Free UK delivery.
4. Floor standing or wall mounted, in 12 colours. Guaranteed for up to 20 years.

### 06 — Electric Cast Iron Radiators (conditional)

**Headlines:** Electric Cast Iron Radiators · Cast Iron, No Plumbing · Electric & Dual Fuel Options ·
Classic Look, Electric Heat · Thermostat Controlled · Shop Electric Cast Iron · 12 Colours Available ·
Free UK Delivery · Up To 20 Year Guarantee · Cast Iron Radiators UK · Order Online Today ·
Period Style, Plug In Heat

**Descriptions:**
1. Electric cast iron radiators with the classic look and no pipework needed.
2. Thermostatic control, period styling and free UK delivery on every order.
3. Choose electric or dual fuel, in 12 colours or matched to your own scheme.
4. Traditional cast iron, guaranteed for up to 20 years. Order online today.

### ⚠ Claims to verify before you publish

I sourced these from public pages about the site; I could not load the site directly from this
environment (egress policy blocked it). **Confirm each before the ads go live** — Google holds you
to claim accuracy, and a wrong guarantee figure is a legal problem, not just a policy one:

- "Free UK delivery" / "Free delivery on all orders" — is it truly all orders, or over a threshold?
- "Up To 20 Year Guarantee" — confirm the exact term and whether it applies to the whole cast iron range
- "12 Colours" — confirm the stock colour count on this category
- "Finished In Lincolnshire" / "Hand-finished" — confirm this is accurate for cast iron specifically
- "2, 3 & 4 Column Options" — confirm the column configurations you actually sell
- "Fast UK Dispatch" / "stock-ready finishes" — confirm lead times before making a speed claim

---

## 8. Campaign assets (extensions)

| Asset | Recommendation |
|---|---|
| Sitelinks (min 4, aim 6) | Black Cast Iron / Victorian Column / Shop By Size / Colour Matching / Delivery & Guarantee / Request a Quote — each with 25-char text and both description lines filled |
| Callouts (min 4, aim 8) | Free UK Delivery · Up To 20 Year Guarantee · 12 Stock Colours · Bespoke Colour Match · Made To Measure · Expert Advice · Buy Direct · UK Finished |
| Structured snippets | Header "Styles": Victorian, Ornate, Column, Traditional, Decorative, Wall Mounted. Header "Types": Cast Iron, Electric, Dual Fuel |
| Image assets | 3–5 lifestyle shots (1200×1200 and 1200×628). Materially lifts Search CTR and feeds AI Max |
| Price assets | Add if you have clean per-model pricing — strong for category-page traffic |
| Call asset | Add if you take phone orders; this category has high consultative intent |
| Location asset | Only if you want showroom/collection traffic |

Sitelinks deserve a note under AI Max: with final URL expansion on, automated sitelinks can drift
to irrelevant pages. Add your six manual sitelinks so the automated ones have less room, and check
them in week 1.

---

## 9. Launch and measurement plan

**Before launch**
1. Verify the claims in §7.
2. Confirm conversion tracking is firing purchases (and enquiry forms) with value.
3. Run the column keywords through Keyword Planner.
4. Cross-check the competitor negative list against your own model names.
5. Decide on ad group 06 (electric) and the restored/refurbished block.

**Launch method — use the AI Max one-click experiment.** Rather than switching AI Max on for the
whole campaign, build the campaign, then run a 50/50 experiment (AI Max on vs off). You need
**4 weeks minimum, 6 preferred**, to clear the learning period and get a readable result. If you're
already confident from your other live campaign, you can skip straight to on — but you lose the
clean read on incrementality against Pmax.

**Week 1–2:** check search terms daily-ish. AI Max expansion is where waste appears first. Mine
`Search terms` and the AI Max `search term matching` report, and add negatives aggressively.
Don't touch bids.

**Week 3–4:** review ad group 03 (Vintage) specifically for reclaimed-intent leakage. Check final
URL expansion's landing pages report — if it's sending traffic to junk, tighten URL exclusions.

**Week 5–6:** first structural decisions. Split out any modifier that's earning meaningful volume;
merge any ad group under ~10 conversions/month back into Core.

**Ongoing:** the metric that matters is **blended cost/conversion across Search + Pmax**, not this
campaign in isolation. Given the 97% search-term overlap typical between Pmax and Search, some of
what this campaign reports will be reallocated from Pmax rather than new. Judge it on category
totals.

---

## Sources

- [Set up AI Max for Search campaigns — Google Ads Help](https://support.google.com/google-ads/answer/15909989?hl=en)
- [How AI Max for Search campaigns works — Google Ads Help](https://support.google.com/google-ads/answer/15910187?hl=en)
- [About Final URL expansion in Search — Google Ads Help](https://support.google.com/google-ads/answer/16230205?hl=en)
- [How Performance Max interacts with other campaigns in your account — Google Ads Help](https://support.google.com/google-ads/answer/13810170?hl=en)
- [About keyword matching options — Google Ads Help](https://support.google.com/google-ads/answer/7478529?hl=en)
- [Google Responsive Search Ads Character Limits (2026) — TextKit](https://textkit.dev/blog/google-responsive-search-ads-character-limits)
- [Google Ads Character Limits 2026 — AdsPreview](https://adspreview.us/guides/google-ads-character-limits)
- [Google AI MAX for Search Campaigns: Implementation Checklist — ALM Corp](https://almcorp.com/blog/google-ai-max-search-campaigns-complete-checklist-performance-analysis/)
- [Best Practices Guide for Google Ads AI Max for Search — Lachi Media](https://lachimedia.com/blog/google-ads/google-ads-ai-max-for-search-best-practices/)
- [Is Performance Max Cannibalizing Your Search Campaigns? — Optmyzr](https://www.optmyzr.com/blog/is-pmax-cannibalizing-search/)
- [Lincolnshire Radiators Direct — Cast Iron Radiators](https://lincsradsdirect.co.uk/product-category/cast-iron-radiators/)
