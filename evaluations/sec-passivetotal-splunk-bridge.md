# Evaluation: PassiveTotal Splunk Bridge

**Source**: risk-iq-splunk-app-development-for-passivetotal.md
**Category**: Analytics
**Date Evaluated**: 2026-03-19

## The Idea (In One Paragraph)

A Splunk app that pulls RiskIQ's PassiveTotal threat intelligence data directly into Splunk so security analysts can see which internal IPs are talking to which external domains, enrich indicators in bulk, and match threat indicators against their existing Splunk data — all without leaving the Splunk interface. The pitch: instead of forcing analysts to context-switch between two screens (Splunk for logs, RiskIQ for threat intel), unify them into a single pane of glass.

## Forcing Questions Assessment

### Q1: Demand Reality

**Weak.** There is exactly one named customer here: RiskIQ itself, which is the vendor that wanted its product embedded in Splunk. This is a vendor-driven integration, not a pull from end users screaming for a solution. The case study says "enterprise security teams require a full view of their digital attackers," which is a generic category-level assertion, not evidence of specific demand. There is no mention of how many Splunk customers adopted the app, no usage metrics, no retention data, no expansion evidence. RiskIQ was acquired by Microsoft in 2021 for approximately $500M, which means the platform this app was built for has been absorbed into Microsoft Defender Threat Intelligence. The customer who commissioned this work has literally disappeared as an independent entity. If this app vanished tomorrow, it is unclear anyone would notice — the underlying data source has been folded into a different product.

### Q2: Status Quo

**Partially addressed.** The case study implies the status quo: security teams are toggling between RiskIQ's standalone interface and Splunk, manually looking up indicators, and lacking a unified view of internal-to-external communication patterns. There is a mention of "monitoring for security teams from two different screens." That is a real pain — context-switching during incident triage costs time and creates cognitive overhead. But the case study never quantifies this pain. How many hours per investigation? How many investigations per week? Without numbers, the pain remains abstract. The broader workaround is well-known: analysts copy-paste IOCs between tools, run manual lookups, maintain spreadsheets of enrichment data. This is a real problem, but it is also a problem every threat intel vendor and every SIEM vendor is already working on.

### Q3: Desperate Specificity

**Very weak.** The case study speaks in pure category language: "enterprise security teams," "every enterprise security team," "customers." There is no named persona. The closest we get is an implied SOC analyst who needs to check whether specific indicators appear in Splunk data. But there is no title, no workflow, no specific pain consequence. We cannot picture this person. We cannot email them. The case study does not even mention a specific vertical or company size that would narrow the audience. This reads like marketing copy, not customer discovery.

### Q4: Narrowest Wedge

**The narrowest wedge is identifiable but commoditized.** The smallest valuable thing here would be: a Splunk command that takes an IP or domain as input and returns PassiveTotal enrichment data inline in a Splunk search. That is genuinely useful and could be built in a week. The case study describes three features that could each be a wedge: (1) lookup a single indicator against RiskIQ, (2) bulk-upload indicators for enrichment, (3) match a set of threat indicators against all Splunk data. Feature #3 — "search those indicators in the whole Splunk environment" — is the most interesting because it reverses the flow from pull to push. But this is the kind of feature Splunk's own Threat Intelligence Management module already supports natively with multiple threat feeds. The wedge exists, but it is a feature of a feature.

### Q5: Observation & Surprise

**None whatsoever.** The case study reads as pure spec-driven delivery. RiskIQ wanted their data in Splunk; Crest Data built the integration. There is no mention of user feedback, unexpected usage patterns, feature reprioritization, or any discovery during the engagement. The phrase "providing the same look and feel" strongly suggests the goal was faithful replication of the RiskIQ UI inside Splunk — the opposite of learning from users. This is a porting exercise, not a product discovery process.

### Q6: Future-Fit

**Actively unfavorable.** Several trends work against this:

1. **RiskIQ was acquired by Microsoft in 2021.** The product has been rebranded as Microsoft Defender Threat Intelligence. A Splunk app for a product that no longer exists independently is on borrowed time.
2. **Splunk was acquired by Cisco in 2024.** The Splunk platform itself is undergoing significant changes in ownership and direction.
3. **SIEM platforms are consolidating threat intel natively.** Splunk, Sentinel, Chronicle, and others are all building first-party threat intelligence integrations. Third-party apps that merely pipe data from one vendor into another are being commoditized.
4. **AI-driven SOC automation is replacing manual indicator enrichment.** The entire workflow this app supports — manually looking up indicators and enriching data — is being automated by AI copilots and automated triage systems.

The world in 3 years makes this less essential, not more.

## The Paul Graham Test

### Schlep Blindness

**Minimal schlep.** Building a Splunk app that calls an API and renders dashboards is well-understood integration work. It requires knowledge of the Splunk SDK and the RiskIQ API, but neither is arcane. Thousands of Splunk apps exist on Splunkbase. The technical barriers are low, the domain knowledge required is moderate, and the work is not the kind of unsexy slog that others avoid — it is the kind of bread-and-butter integration that system integrators do routinely. There is no schlep blindness to exploit here because the schlep is not scary enough to deter anyone.

### Do Things That Don't Scale

**The engagement itself does not scale, and it did not reveal a scalable product.** This is a one-time app build for a vendor. The "unscalable" thing — custom Splunk app development — is the actual deliverable, not a stepping stone to something bigger. There is no evidence that the hands-on work taught the team something surprising about the market or created an insight that could not have been obtained by reading the Splunk SDK docs. Contrast this with, say, a team that did 50 custom Splunk integrations and noticed a pattern — "every customer asks for the same three features" — which could become a product. Here, we have one integration for one vendor.

### Default Alive or Default Dead

**Default dead.** If extracted as a startup today, you would be selling a Splunk app for a threat intel product that has been absorbed into Microsoft. Your customer base is RiskIQ users who also use Splunk — a shrinking intersection. There is no obvious revenue model beyond a one-time app sale or per-seat Splunkbase license. The underlying vendor has been acquired, the SIEM market is consolidating, and the specific integration is headed toward obsolescence. You would need to pivot to survive.

### Frighteningly Ambitious

**Not at all.** This is a Splunk dashboard. Building a Splunk app for a single vendor's API is the opposite of frighteningly ambitious. It does not make anyone think "can they really do that?" It makes people think "yes, obviously they can, that's what Splunk apps are for." The ambition ceiling of this project is capped by the fact that it is a bridge between two specific products, both of which are now owned by larger companies with their own integration roadmaps.

### Earnest Test

**Unclear, leaning negative.** The case study is extremely short and reads like a marketing summary rather than a description of work by people who deeply care about the security analyst's experience. There is no evidence of domain passion. The emphasis on "same look and feel" suggests the goal was fidelity to the vendor's spec, not a deep understanding of the analyst's workflow. A team that cared deeply would have said something like "we discovered that analysts need X during triage" — instead, we get "we integrated RiskIQ PassiveTotal into Splunk."

## Startup Quality

### Market

**Size**: Threat intelligence is a large market (~$15B+ by 2026), but "Splunk apps for specific threat intel vendors" is a micro-niche. The TAM of "people who use both Splunk and RiskIQ PassiveTotal" was always small and is now approaching zero as the product has been absorbed into Microsoft.

**Timing**: The timing was reasonable when the engagement occurred — RiskIQ was an independent company and Splunk was the dominant SIEM. By 2026, both have been acquired. The window has closed.

**Competition**: Splunk's own Threat Intelligence Management, the Splunkbase ecosystem of free and paid apps, and Microsoft's own integration of Defender TI into Sentinel are all direct competitors. The competitive landscape has moved on.

### Product

**Defensibility**: None. A Splunk app that calls an API has no moat. The vendor could build it themselves (and once Microsoft acquired RiskIQ, they had every incentive to integrate with their own products, not Splunk). There are no data network effects, no switching costs beyond configuration, and no proprietary technology.

**Scalability**: A Splunk app can be distributed at scale via Splunkbase, so the distribution mechanism exists. But the product is tied to a single vendor's API, so it cannot generalize. Every new threat intel source requires building a new app. This is inherently a services pattern, not a platform pattern.

**Technical depth**: Low. API integration, dashboard rendering, bulk data ingestion into Splunk indexes. These are standard Splunk development tasks. Any Splunk developer with a week of time could replicate this.

### Team Signal

**Minimal signal.** The case study is too brief and too generic to infer deep domain expertise. There is no evidence of creative problem-solving — the solution appears to be a straightforward implementation of a vendor's requirements. There is no mention of discovery, iteration, or non-obvious insights. The team may well be excellent Splunk developers, but this case study does not demonstrate it.

## Wild Card — "But What If?"

### The Contrarian Question

The obvious objection is: "This is just a Splunk app for one vendor's data. It's a feature, not a company." What if that objection is wrong?

The contrarian angle would be: what if the real opportunity is not this specific integration, but a **universal threat intelligence normalization layer for SIEMs**? Every security team uses 5-10 threat feeds. Every SIEM requires custom integration for each feed. What if someone built a single product that ingests any threat intel feed (STIX/TAXII, proprietary APIs, open source feeds) and normalizes it into any SIEM (Splunk, Sentinel, Chronicle, QRadar) with one-click deployment?

But this angle falls apart quickly. ThreatConnect, Anomali, and Recorded Future already do this. Splunk's own TI framework supports it. The "universal adapter" for threat intel has been attempted many times and has largely been commoditized. The contrarian bet here does not hold up under scrutiny.

### The Crazy Upside Scenario

In the most optimistic scenario, the team that built this app realizes that the real value is not in any single integration but in the **pattern** of building integrations. They build a no-code platform for creating SIEM integrations — any data source to any SIEM, configured in hours instead of weeks. They become the Zapier of security data. Companies pay $50K/year to connect their security stack without hiring Splunk developers.

But even this bull case has problems: Tines, Torq, and Swimlane already occupy the security automation/orchestration space. The integration-as-a-platform opportunity is real but already contested. And the case study shows no evidence that the team is thinking in this direction.

### Risk Worth Taking?

**No wild card here.** The obvious objections are just correct. This is a consulting engagement to build a vendor-specific Splunk app. The vendor has been acquired. The platform is consolidating. The technical work is commodity integration. There is no hidden product, no surprising insight, and no contrarian angle that survives scrutiny. This is a consulting project, and it was a perfectly fine one — but it is not a startup.

## Verdict

**Startup Viability Score**: 2/10

**One-Line Verdict**: "This is a feature of a feature — a Splunk app for a product that no longer exists independently."

**What Would PG Say**: "You built a dashboard that connects product A to product B, and then product A got acquired. This is what happens when you build on someone else's platform without owning any of the value chain. The question isn't whether you can build Splunk apps — it's whether you noticed something while building them that nobody else sees."

**The Assignment**: Go talk to 10 SOC analysts who used to use PassiveTotal and ask them what they do now that it is part of Microsoft Defender TI. Specifically ask: "What is the most annoying part of your threat intelligence workflow today?" If 7 out of 10 describe the same pain, you might have the seed of something. But do not start from the app you built — start from the problem the analyst has right now, in 2026, with the tools they are actually using.
