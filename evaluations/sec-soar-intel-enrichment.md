# Evaluation: SOAR Intel Enrichment

**Source**: ibm-qradar-soar-integration.md
**Category**: Security
**Date Evaluated**: 2026-03-19

## The Idea (In One Paragraph)

A startup that automatically enriches security incidents with threat intelligence so SOC analysts can triage faster. Instead of manually copying IOCs from an alert into a separate threat intel platform, waiting for results, and pasting context back into their SOAR tool, the product connects a threat intelligence exchange platform to IBM QRadar SOAR, auto-submitting incident artifacts for enrichment and returning context in seconds. The pitch: "We turn hours of manual incident investigation into seconds by bridging the gap between your SOAR platform and your threat intel feeds."

## Forcing Questions Assessment

### Q1: Demand Reality

Weak. There is a named customer -- described only as an "API-first cloud-native intelligence management platform" -- but no company name, no revenue figure, no expansion data, no quote from an actual user. The case study says investigation time dropped "from hours to seconds," which is a strong claim, but it is completely unsubstantiated. There is no evidence that the customer would be "genuinely upset if it disappeared tomorrow." For all we can tell, this was a one-time integration project that was delivered and handed off. There is no signal of ongoing dependency, recurring usage, or organic pull.

### Q2: Status Quo

Adequately described but generic. The status quo is that SOC analysts manually investigate incidents by cross-referencing threat intelligence from external sources -- copy-pasting IOCs, looking up hashes, checking IP reputations in separate consoles. This is a real pain point that is well-documented across the industry. However, the case study provides zero specificity about *this* customer's particular workflow. How many analysts? How many incidents per day? What tools were they duct-taping together? The status quo is described at the level of an industry whitepaper, not a customer conversation. Every SOAR vendor's marketing page says the same thing.

### Q3: Desperate Specificity

Missing almost entirely. The most specific persona referenced is "security analysts" and "SOC teams." There is no named role with a specific pain point -- no "the Tier 1 SOC analyst at a 50-person security team who spends the first 90 minutes of every shift copy-pasting IOCs into VirusTotal." The customer is anonymized to the point of being a ghost. We are told they offer an "API-first cloud-native intelligence management platform," which sounds like it could be ThreatConnect, Anomali, or a dozen others, but the vagueness undercuts any sense of urgency. You cannot email "security teams."

### Q4: Narrowest Wedge

There is a plausible wedge here: a lightweight connector that auto-enriches SOAR incidents with threat intel context. This is a well-scoped, single-function tool. But the problem is that this wedge already exists -- every major SOAR platform (including QRadar SOAR itself) ships with integration frameworks and marketplace apps for threat intel enrichment. IBM's own App Exchange has dozens of these connectors. The "narrowest wedge" is essentially an integration app for a specific pairing of platforms. Someone could build this in a weekend hackathon using QRadar SOAR's built-in function SDK. The real question is: would anyone pay a standalone subscription for this when the SOAR vendor offers it as a built-in or marketplace freebie?

### Q5: Observation & Surprise

None. Zero. The case study reads as pure spec-driven delivery. The customer had a requirement (connect platform A to platform B), Crest built it, it worked as expected. There is no mention of unexpected usage, no pivot, no "we thought they wanted X but they actually needed Y," no user feedback that revealed something non-obvious. This is the biggest red flag in the entire case study. Real product-market fit leaves fingerprints of surprise -- users doing things the builders did not anticipate. There are no fingerprints here.

### Q6: Future-Fit

Mixed. On one hand, the need for automated threat enrichment is not going away -- SOC alert volumes are growing, threat landscapes are getting more complex, and the analyst talent shortage is worsening. On the other hand, the specific technical approach here (point-to-point integration between two named platforms) is fragile. IBM has been deprioritizing QRadar in favor of its acquisition of ReaQta and its pivot to QRadar Suite / Cloud Pak for Security. More importantly, AI-native security copilots (Microsoft Security Copilot, Google Gemini in Chronicle, CrowdStrike Charlotte AI) are rapidly absorbing the "automated enrichment" function into the platform itself. In 3 years, asking a separate integration to enrich your incidents will feel like asking a separate app to spell-check your email. The trend is toward platform-native intelligence, not bolt-on connectors.

## The Paul Graham Test

### Schlep Blindness

Minimal schlep here. Integrating two security platforms via APIs is well-trodden ground. It is not the kind of unsexy, tedious problem that scares people away -- it is the kind of work that hundreds of consulting firms, MSSPs, and platform vendors do routinely. The QRadar SOAR integration SDK is well-documented. There is no deep domain schlep that creates a natural barrier to entry. Compare this to something like normalizing log formats across 200 different firewall vendors -- that is a schlep. Connecting two APIs is Tuesday.

### Do Things That Don't Scale

The consulting engagement itself is inherently unscalable, but there is no evidence that the unscalable work revealed a scalable product insight. A good "do things that don't scale" story would be: "We built this integration for one customer, and in the process we discovered that 80% of SOAR enrichment workflows follow the same 5 patterns, so we built a template engine." There is no such discovery described here. The output appears to be a bespoke integration, not a generalizable product.

### Default Alive or Default Dead

Default dead. There is no evidence of market pull -- no inbound demand, no waitlist, no organic growth signal. The revenue model would presumably be a SaaS subscription for the connector, but the competitive landscape (free marketplace apps, built-in platform features) makes pricing power dubious. You would have to drag customers to this product and explain why they should pay for something their SOAR vendor already offers in some form.

### Frighteningly Ambitious

Not at all. "We connect platform A to platform B" does not make anyone think "can they really do that?" This is an integration project. It is useful, competently executed, and completely unambitious. A frighteningly ambitious version of this would be: "We are building a universal threat intelligence enrichment layer that works across every SOAR, SIEM, and EDR platform simultaneously, with a shared intelligence graph that gets smarter across all customers." That would be frightening. This is not.

### Earnest Test

Hard to assess. The case study is written in the third-person consulting voice, which strips out any signal of personal conviction or domain passion. The technical approach is sensible -- auto-submitting artifacts for enrichment and returning context to the SOAR platform is the right architecture. But there is no evidence the builders discovered something non-obvious about the domain, pushed back on a customer requirement because they knew better, or went beyond the spec because they cared about the outcome. It reads like a competent deliverable, not a labor of love.

## Startup Quality

### Market

**Size**: The SOAR market is real -- roughly $1-2B and growing. But "connectors between specific platform pairs" is a micro-niche within that market, not a market itself. The addressable segment is "organizations running both QRadar SOAR and this specific unnamed threat intel platform," which is a tiny intersection.

**Timing**: Poor. QRadar SOAR (formerly Resilient) is a legacy platform in IBM's portfolio. IBM acquired ReaQta in 2022 and has been consolidating toward QRadar Suite and cloud-native architectures. Building a startup around a platform whose vendor is actively restructuring it is swimming against the current. Meanwhile, AI-native security copilots are making bolt-on enrichment connectors feel like last-generation tooling.

**Competition**: Intense and commoditized. Every SOAR platform has a marketplace full of threat intel integrations. Cortex XSOAR, Splunk SOAR, Swimlane, Tines -- they all ship these connectors as free community content. IBM's own App Exchange has threat intel enrichment apps. The competition here is not other startups; it is free content from platform vendors and their communities.

### Product

**Defensibility**: Essentially none. A point-to-point API integration between two platforms has no moat. There are no data network effects, no switching costs beyond re-implementation, and no proprietary intelligence. Any competent security engineer could rebuild this in days using QRadar SOAR's function SDK and the threat intel platform's API docs.

**Scalability**: Very limited. Each new SOAR-to-TIP pairing requires custom integration work. There is no described abstraction layer, no universal schema, no self-serve deployment. This is inherently a services-heavy delivery model.

**Technical depth**: Low. The case study describes a standard API integration pattern -- submit artifacts, receive enrichment, write back to the incident. There is no mention of novel algorithms, proprietary data processing, or technical innovation. This is configuration and integration work, not R&D.

### Team Signal

The team clearly has IBM QRadar SOAR expertise and knows how to build integrations on the platform. That is a useful skill, but it is widely held among IBM partners and SOAR consultants. There is no evidence of creative problem-solving or non-obvious discovery. The case study suggests competent execution of a well-defined scope, which is exactly what a consulting engagement should be -- but it does not signal the kind of insight or ambition that suggests a startup founder in disguise.

## Wild Card -- "But What If?"

### The Contrarian Question

The obvious objection is: "This is just an integration connector -- it's a feature, not a company, and it's already commoditized." What if that objection is wrong? The contrarian case would be: "What if the real problem isn't connecting two specific platforms, but the fact that threat intelligence enrichment is fragmented across dozens of SOAR/SIEM/TIP combinations, and nobody has built a universal enrichment bus that normalizes intelligence across all of them?" In that framing, this engagement is one data point in a much bigger problem. The startup would not be "QRadar SOAR + TIP X connector" -- it would be "the Segment.com of threat intelligence," a universal enrichment layer that sits between any detection platform and any intelligence source, normalizing the data model and providing a single API.

That would be interesting. But the case study provides zero evidence that the team is thinking in that direction. There is no mention of a generalized approach, no hint of abstraction beyond the two specific platforms.

### The Crazy Upside Scenario

If someone took the insight from this engagement and built a universal threat intelligence enrichment bus -- a platform-agnostic layer that auto-enriches any security event from any SOAR/SIEM/XDR with context from any TIP/OSINT/commercial intel feed -- they would be building something like what ThreatConnect, Anomali, or Recorded Future aspire to, but from the enrichment-bus angle rather than the intelligence-platform angle. If they added a shared anonymized intelligence graph across customers (so enrichments at Company A improve detections at Company B), you would get data network effects. If AI-native copilots become the new SOAR, this enrichment bus becomes the intelligence backbone they all query. Bull case: a $500M+ company that is the "intelligence plumbing" for every security operations center.

But that is a completely different company from what is described in this case study.

### Risk Worth Taking?

**No wild card here.** The case study as written describes a point-to-point integration connector between two specific platforms -- one of which (QRadar SOAR) is in the twilight of its product lifecycle. The contrarian scenario (universal enrichment bus) is interesting in theory, but the case study provides no evidence that anyone involved is thinking about it, building toward it, or has the insight to pursue it. The obvious objections -- it is a feature, it is commoditized, the underlying platform is declining -- are just correct.

## Verdict

**Startup Viability Score**: 2/10

**One-Line Verdict**: "This is a feature that the platform vendor ships for free in their marketplace -- not a company."

**What Would PG Say**: "You built a connector between two enterprise platforms. That is fine consulting work, but it is not a startup. The thing I would worry about is that IBM could ship this as a built-in feature tomorrow and your entire value proposition vanishes. If you want to build a company here, you need to answer a harder question: what do you know about threat intelligence enrichment that nobody else knows?"

**The Assignment**: Go talk to 20 SOC analysts at mid-market companies (500-2000 employees) who run multi-vendor security stacks. Do not pitch them a product. Instead, ask them to walk you through exactly what happens in the first 10 minutes after they receive a critical alert. Map every manual step, every tool switch, every copy-paste. If you find a pattern -- a step that is painful, repeated, and the same across different tool combinations -- that is your real product. The QRadar SOAR connector is not it.
