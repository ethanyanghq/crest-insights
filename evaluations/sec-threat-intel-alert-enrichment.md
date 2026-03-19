# Evaluation: Threat Intel Alert Enrichment

**Source**: ibm-qradar-intsights-tip-getting-ahead-of-the-adversaries.md
**Category**: Security
**Date Evaluated**: 2026-03-19

## The Idea (In One Paragraph)

A product that enriches enterprise SIEM alerts with threat intelligence harvested from the clear, deep, and dark web, so that security operations teams can cut through false positives and detect targeted attacks in real time. Instead of relying on generic, signature-based reputation feeds, this surfaces adversary-focused, forward-looking intelligence correlated directly with the customer's own security telemetry -- reducing mean time to detect and eliminating the analyst's need to hop between multiple systems.

## Forcing Questions Assessment

### Q1: Demand Reality

**Weak.** There is no named customer, no revenue figure, no usage data, and no concrete outcome metrics in this case study. The demand argument is entirely logical ("SIEMs are flooded with false positives, therefore enriched intel is needed"), not empirical. That said, the logical argument is sound -- SOC teams drowning in false positives is one of the most well-documented pain points in enterprise security. But "well-documented pain point" and "someone would be upset if this specific product disappeared" are different things. The case study gives us zero evidence of the latter. No deployment numbers, no analyst testimonials, no "before and after" metrics. The demand may well be real, but this case study does not prove it.

### Q2: Status Quo

**Partially addressed.** The case study describes the status quo in general terms: SIEMs flooded with raw, unvalidated threat data; analysts buried in false positives; signature-based reputation feeds that catch common malware but miss targeted attacks. This is accurate and well-understood in the industry. What is missing is any specificity about what a particular customer was doing before this integration. Were they manually cross-referencing threat intel feeds in spreadsheets? Were they running a competing TIP that was underperforming? Were they simply ignoring dark web intelligence entirely? The status quo is described at the category level, not the customer level.

### Q3: Desperate Specificity

**Vague.** The case study mentions "the SOC team" and "analysts" but never names a specific persona, organization, or scenario. We get "security team inundated with false positives" -- which is true of virtually every SOC on the planet. The question is: which SOC analyst at which kind of company is the most desperate for this? A Tier 1 analyst at a 5-person SOC in a mid-market financial firm who is personally responsible for triaging 2,000 alerts per day? A threat hunting team at a Fortune 500 that discovered their existing TIP missed a targeted campaign against them? The case study does not narrow the aperture at all. You cannot email "the SOC team."

### Q4: Narrowest Wedge

**Identifiable but not articulated.** There is a plausible narrow wedge buried here: a QRadar plugin that takes IntSights' dark web intelligence and creates high-fidelity, pre-correlated alerts, reducing the noise-to-signal ratio by some meaningful factor. That could be shipped as a marketplace app. The problem is the case study frames the value as the full integration -- "real time correlation with high volume security telemetry" plus enrichment plus proactive adversary neutralization. That sounds like a platform, not a wedge. The narrowest version would be: "Install this app, connect your IntSights account, and within 24 hours your QRadar console surfaces the 10 alerts that actually matter out of the 5,000 you got today." If that is what this does, the case study fails to say so crisply.

### Q5: Observation & Surprise

**Nothing.** The case study contains no evidence of unexpected findings, user feedback, pivot during engagement, or emergent behavior. There is no "Crest Difference" section, no lessons learned, no anecdote about something the team discovered during deployment. The write-up reads like a pre-sales solution brief, not a post-deployment retrospective. This is the single biggest gap -- the absence of any learning signal means we have no evidence that the builders discovered anything non-obvious, which is precisely the kind of signal that separates a real product insight from a spec-driven integration.

### Q6: Future-Fit

**Mixed.** Threat intelligence is becoming more essential, not less. Adversaries are increasingly sophisticated, AI enables faster attack generation, and the volume of security telemetry is exploding with cloud migration. All of this makes intelligent filtering more critical. However, the specific form factor -- a QRadar app integrating a specific TIP vendor -- is vulnerable on two fronts. First, IBM has been actively evolving QRadar (now moving toward QRadar Suite/Cloud), which could absorb or deprecate third-party app functionality. Second, IntSights was acquired by Rapid7 in 2021, meaning the underlying TIP vendor has been absorbed into a competitor's ecosystem. This specific product may be stranded. The general problem is future-fit; this specific instantiation may not be.

## The Paul Graham Test

### Schlep Blindness

There is moderate schlep here. Integrating threat intelligence with SIEM at the correlation level -- handling different data formats, managing feed freshness, deduplicating indicators, tuning correlation rules to reduce false positives without creating false negatives -- is genuinely tedious work. Most security vendors hand-wave this part. But the schlep is at the integration layer, not at the data or algorithm layer. The hardest part of this problem (gathering dark web intelligence, attributing campaigns to adversary groups) is being done by IntSights, not by this product. The integration schlep alone is not a strong enough moat.

### Do Things That Don't Scale

This is a consulting engagement, so by definition the team did unscalable things. But the case study provides no evidence that the unscalable work yielded scalable insight. Did they manually tune correlation rules for a specific customer and discover that 80% of the value came from three specific rule templates? Did they find that a particular type of dark web intelligence (credential leaks, for instance) was dramatically more actionable than others? If so, those findings could seed a product. But the case study is silent on this. The consulting wrapper was not peeled back to reveal the product kernel.

### Default Alive or Default Dead

**Default dead.** There is no evidence of organic demand pulling this product forward. No named customers, no marketplace download numbers, no expansion metrics. The value proposition depends on two specific vendors (IBM QRadar and IntSights/Rapid7) neither of which Crest controls. The revenue model is either one-time app sales or consulting fees for deployment. There is no recurring revenue hook described, no data network effect, and no self-serve path. A startup built around this would need to actively sell every deal.

### Frighteningly Ambitious

**Not at all.** This is a point integration between two existing vendor products. "We built a QRadar app for IntSights" does not make anyone think "can they really do that?" The ambitious version of this idea would be: "We are building an autonomous threat intelligence layer that ingests data from every corner of the internet and automatically reconfigures your security controls in real time without human intervention." That would be frighteningly ambitious. This case study describes plumbing.

### Earnest Test

**Inconclusive.** The case study uses the right language about adversary-focused intelligence and proactive defense, suggesting some domain understanding. But the writing is generic enough that it could have been produced by anyone with passing familiarity with the SIEM/TIP landscape. There is no moment in the case study where you feel the builders discovered something from firsthand experience. Compare this to a case study that says "We found that 73% of the alerts flagged by generic threat feeds were duplicates of indicators already in the customer's block lists -- the real value was in the 4% of indicators that came from dark web forum monitoring of threats specifically targeting the customer's industry." That kind of specificity would signal earnest domain expertise. This case study does not offer it.

## Startup Quality

### Market

**Size**: The threat intelligence platform market is real and sizable ($15B+ by some estimates). But this case study describes a narrow slice: an integration app for one SIEM vendor consuming data from one TIP vendor. The addressable market for this specific product is "QRadar customers who also use IntSights," which is a niche within a niche.

**Timing**: The timing argument is mixed. When this was published (2024), threat intelligence integration was already a mature category. The major SIEM vendors (Splunk, Microsoft Sentinel, Google SecOps) all had native or first-party TIP integrations. IntSights had already been acquired by Rapid7. There is no "why now" in this case study.

**Competition**: Extensive. QRadar has a built-in threat intelligence framework. IBM X-Force provides native threat feeds. Rapid7 (which now owns IntSights) has its own SIEM product. Major TIP vendors (Recorded Future, Mandiant, CrowdStrike Falcon Intelligence) all have QRadar integrations. This is a crowded field where platform vendors are actively absorbing the integration layer.

### Product

**Defensibility**: Minimal. A QRadar app that maps IntSights data to QRadar's reference sets and correlation rules is valuable but replicable. There is no proprietary data, no unique algorithm, and no network effect. IBM or Rapid7 could build this integration natively (and likely have, post-acquisition). Switching costs are low -- replacing a TIP integration is a weeks-long project, not a years-long one.

**Scalability**: The app itself could be self-serve (install from QRadar marketplace, configure API keys). But the real value -- tuning correlation rules, reducing false positives, operationalizing the intelligence -- likely requires services. This is the classic "the product is easy to install, hard to get value from" problem that keeps security products in the services-dependent zone.

**Technical depth**: The case study describes standard integration work: ingesting threat intel data, mapping it to SIEM reference sets, building correlation rules, enriching alerts. This is competent engineering but not technically novel. Any team with QRadar API experience and IntSights API access could build this.

### Team Signal

**Limited signal.** The case study does not describe creative problem-solving, unexpected discoveries, or non-obvious architectural decisions. The solution described is the expected solution for this problem. There is no evidence of the team going beyond the spec or discovering something that changed their understanding of the problem. The write-up reads like a standard integration deliverable.

## Wild Card -- "But What If?"

### The Contrarian Question

The obvious objection is: "This is just a vendor integration -- IBM or Rapid7 will build it themselves." But what if the real insight is that vendor-native integrations are always mediocre? What if the customers who need this most are the ones running heterogeneous security stacks -- QRadar for SIEM, IntSights for dark web intel, CrowdStrike for endpoint, Palo Alto for firewall -- and no single vendor can or will build high-quality integrations across all the permutations? The "integration tax" in enterprise security is enormous, and the vendors have no incentive to integrate well with competitors. A startup that became the universal translation layer between security tools -- not just one pair, but all pairs -- might find a real market. The problem is that this case study describes one pair, not a platform thesis.

### The Crazy Upside Scenario

If you squinted hard: Crest has done dozens of these security integrations across different SIEM, TIP, SOAR, and endpoint vendors. What if the institutional knowledge from building all these point integrations was distilled into a platform -- a universal security data fabric that normalizes, enriches, and correlates data across any combination of security tools? That is essentially what companies like Torq, Tines, and Swimlane are building in the SOAR space, and what Cribl is building for security data routing. If Crest extracted a product from their integration experience, the bull case is a company that owns the connective tissue of the enterprise security stack. But that is not what this specific case study describes. It describes one integration.

### Risk Worth Taking?

**No wild card here.** The case study describes a point integration between two specific vendor products, one of which has been acquired by a competitor. There is no proprietary data, no non-obvious insight, no evidence of unexpected demand. The contrarian angle (universal security integration layer) is interesting but requires a completely different product vision than what is described here. The obvious objections -- that this is commoditizable integration work in a crowded market with platform risk on both sides -- are just correct.

## Verdict

**Startup Viability Score**: 2/10

**One-Line Verdict**: "This is plumbing between two vendors, one of which has already been acquired by a competitor -- there is no company here."

**What Would PG Say**: "You built an integration between Product A and Product B, and now Product B has been acquired by someone who competes with Product A. That is not a startup, that is a consulting deliverable with an expiration date. The interesting question is whether you learned something from building fifty of these integrations that could become a product -- but this case study does not tell me that story."

**The Assignment**: Go talk to 10 SOC managers who run heterogeneous security stacks (not just QRadar + IntSights, but any messy combination of tools). Ask them: "How many hours per week does your team spend on problems caused by your security tools not talking to each other?" If the answer is consistently above 20 hours, and if the pain is in the correlation and enrichment layer specifically (not just data plumbing), then there might be a startup in building the universal threat intelligence normalization layer. But start with the customer conversations, not the product.
