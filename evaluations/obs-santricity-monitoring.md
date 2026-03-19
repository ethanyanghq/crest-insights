# Evaluation: SANtricity Monitoring

**Source**: splunk-application-development-for-netapp-santricity.md
**Category**: Analytics / Observability
**Date Evaluated**: 2026-03-19

## The Idea (In One Paragraph)

A monitoring product for NetApp E-Series and EF-Series storage arrays that ingests machine-generated data into Splunk and presents dashboards covering inventory configuration, hardware/software health, critical array events, and performance metrics (IOPS, latency, throughput). The pitch, stripped of consulting language: "We give storage admins a single pane of glass to monitor their NetApp SAN environment without leaving Splunk."

## Forcing Questions Assessment

### Q1: Demand Reality

**Weak.** The case study says "customer did not have a way to monitor and troubleshoot the multiple platforms in their environment" and that "day to day IT operations were quite time consuming and complex." But there is no named customer, no revenue figure, no deployment count, no metric showing expanded usage or workflow dependency. The word "customer" appears generically. The entire demand argument rests on the truism that enterprises generate lots of data and want visibility. That is a description of the entire observability market, not evidence that this specific product is needed. There is zero evidence anyone would be "genuinely upset" if this disappeared -- because there is zero evidence anyone is actually using it beyond the initial engagement.

### Q2: Status Quo

**Barely addressed.** The case study mentions that "day to day IT operations were quite time consuming and complex" and that customers lacked a way to "monitor and troubleshoot the multiple platforms in their environment." But it never describes what admins were actually doing before -- were they SSH-ing into each array? Using NetApp's native SANtricity System Manager? Checking email alerts? Running CLI scripts? Without knowing the specific workaround, we cannot assess how much pain this solves. NetApp already ships SANtricity System Manager and SANtricity Unified Manager as free management tools. The case study does not explain why those were insufficient, which is a critical omission.

### Q3: Desperate Specificity

**Missing entirely.** The person who needs this is presumably a storage administrator or infrastructure engineer managing a fleet of NetApp E-Series/EF-Series arrays in an enterprise that has standardized on Splunk. But the case study never names this person, their title, their team size, or the specific consequence of the problem (data loss? downtime? SLA violations? wasted hours?). The framing is entirely category-level: "customers want greater data visibility." You cannot build a startup on a sentence that could appear in any enterprise software brochure from the last 20 years.

### Q4: Narrowest Wedge

**Identifiable but commoditized.** The narrowest wedge is clear: a Splunk app (a TA + dashboards) that pulls data from the NetApp SANtricity Web Services Proxy REST API and visualizes it. This is a well-defined, buildable artifact. You could ship a v1 in a few weeks. The problem is that Splunk apps for hardware monitoring are a known, crowded pattern. Dozens of these exist on Splunkbase for every major storage, network, and compute vendor. The wedge is narrow, but it is also shallow -- there is no indication of unique value beyond "we built the connector for this specific vendor's API."

### Q5: Observation & Surprise

**None.** The case study is 29 lines long and contains zero mentions of user feedback, unexpected usage, surprising findings, or pivots during the engagement. Everything reads as pure spec-driven delivery: customer needed dashboards, dashboards were built. This is the strongest signal that this was a straightforward integration project, not a product discovery process.

### Q6: Future-Fit

**Trending negative.** Several forces work against this idea over a 3-year horizon. First, NetApp itself continues to invest in native monitoring (Cloud Insights, formerly OnCommand Insight) that provides SAN monitoring without Splunk. Second, the broader trend in observability is toward platforms that auto-discover and auto-instrument infrastructure (Datadog, Dynatrace, New Relic), reducing the need for vendor-specific Splunk apps. Third, E-Series/EF-Series is NetApp's legacy SAN product line, increasingly overshadowed by ONTAP-based systems and cloud-native storage. Building deeper into a narrowing hardware niche on a platform (Splunk) that is itself under competitive pressure from cheaper alternatives is a bet against the current.

## The Paul Graham Test

### Schlep Blindness

There is a mild schlep here -- wrangling the SANtricity Web Services Proxy API, understanding NetApp's data model for arrays/controllers/volumes/drives, and mapping that into Splunk's data model is tedious work that requires domain knowledge. But it is not the kind of deep, structural schlep that creates defensibility. Any Splunk consulting shop with a storage engineer on staff can replicate this. The schlep is real but shallow.

### Do Things That Don't Scale

The entire engagement is "things that don't scale" -- it is a consulting project to build a Splunk app for a single customer. The question is whether the unscalable work revealed something scalable. There is no evidence that it did. The case study describes a standard integration deliverable. No insight about storage monitoring workflows, no discovery of a deeper problem, no "aha" moment that points toward a product.

### Default Alive or Default Dead

**Default dead.** If someone extracted this as a standalone product tomorrow, they would have a Splunk app for a specific NetApp hardware line. The addressable market is the intersection of {companies running NetApp E-Series/EF-Series} and {companies using Splunk Enterprise for infrastructure monitoring}. That intersection is small and shrinking. There is no organic pull described, no viral mechanism, and the "customer" would need to be convinced to use Splunk for storage monitoring rather than NetApp's own tools or a general-purpose infrastructure monitoring platform. You would have to drag every customer to this.

### Frighteningly Ambitious

**Not at all.** This is a Splunk dashboard for a storage array. It is the opposite of frighteningly ambitious. It is a feature, and a fairly standard one at that. No one hears "we built a Splunk app for NetApp SANtricity" and thinks "can they really pull that off?"

### Earnest Test

**Inconclusive but leaning negative.** The case study is too thin to assess whether the builders cared deeply about storage monitoring. There is no evidence of domain depth, creative problem-solving, or genuine engagement with the user's workflow. The description reads like a generic consulting deliverable -- inventory dashboards, health dashboards, event tracking, performance metrics. This is the checklist you get from any RFP for storage monitoring. It does not suggest a team that lived and breathed this problem.

## Startup Quality

### Market

**Size**: Very small. The market is NetApp E-Series/EF-Series monitoring via Splunk. E-Series is NetApp's legacy block storage line, primarily used in specialized workloads (video surveillance, HPC, backup). It is a niche within a niche within a niche. Even broadening to "all storage monitoring via Splunk" is a small market that is being absorbed by platform vendors.

**Timing**: No "why now" is apparent. NetApp E-Series has existed for over a decade. Splunk has supported custom apps for over a decade. There is no regulatory change, technology shift, or market event that makes this more urgent today than five years ago. If anything, the timing is getting worse as both Splunk (now owned by Cisco) and NetApp invest in their own integrated monitoring.

**Competition**: NetApp's own tools (SANtricity System Manager, Cloud Insights), general infrastructure monitoring platforms (Datadog, Dynatrace), and other Splunk apps for storage monitoring. The competitive landscape is well-populated and moving toward consolidation.

### Product

**Defensibility**: Near zero. Splunk apps are configuration artifacts -- dashboards, saved searches, data inputs. They are easy to replicate. The REST API is documented. There are no data network effects, no switching costs beyond reconfiguring dashboards, and no proprietary technology described. Splunk (Cisco) or NetApp could ship an equivalent in a sprint.

**Scalability**: A Splunk app is inherently distributable via Splunkbase, so in theory it could be self-serve. But the value is so thin (dashboards for one vendor's storage line) that it is hard to build a business around it. You would need to expand to many vendors, at which point you are competing with the monitoring platforms themselves.

**Technical depth**: None described. The case study lists standard monitoring capabilities (inventory, health, events, IOPS/latency/throughput) that map directly to the SANtricity API endpoints. There is no mention of anomaly detection, predictive analytics, automated remediation, or any feature that goes beyond "pull data, show dashboard."

### Team Signal

The case study provides almost no signal about team capability. There is no description of technical challenges overcome, no mention of domain expertise applied, and no evidence of creative problem-solving. The absence of a "Crest Difference" section (which other case studies from this company include) is itself notable -- there may have been nothing differentiated to highlight.

## Wild Card -- "But What If?"

### The Contrarian Question

The obvious objection is: "This is a commodity Splunk app for legacy storage hardware -- there is no startup here." What if that objection is wrong?

The contrarian angle would be: what if the real opportunity is not "monitoring NetApp E-Series" but "unified storage observability across heterogeneous SAN environments"? Enterprises rarely run a single vendor's storage. They have NetApp, Dell EMC, Pure Storage, HPE, and others, all with different management tools, different APIs, different alert formats. The storage admin managing a mixed fleet has no single pane of glass. Each vendor wants you to use their tool. Each monitoring platform treats storage as an afterthought.

If you built deep connectors for every major SAN vendor and normalized the data into a single model -- health scores, capacity forecasting, performance anomalies, failure prediction -- you might have something. The schlep of integrating with 10 different storage APIs is real, and most teams will not do it.

But this case study gives zero indication that the team was thinking in that direction. It is a single-vendor app with no mention of multi-vendor ambitions.

### The Crazy Upside Scenario

If everything breaks right: you start with NetApp E-Series, expand to ONTAP, then Dell PowerStore, then Pure FlashArray, then HPE Primera. You build a normalized storage data model. You add ML-based failure prediction and capacity planning. Enterprises with 500+ arrays across 5 vendors pay $50K/year for a platform that replaces the 5 separate vendor monitoring tools they are juggling. You become the "Datadog for storage infrastructure" -- a category that Datadog itself has not deeply pursued because the SAN world is too fragmented and too legacy for their taste.

In this scenario, you are a $100M ARR company in 5 years serving the 2,000 largest enterprises in the world. It is plausible. But it requires a completely different ambition level than what this case study describes.

### Risk Worth Taking?

**Faint pulse.** There is a theoretical path from "Splunk app for NetApp E-Series" to "unified storage observability platform," but the case study provides no evidence that anyone involved was thinking about that path. The work described is a single-vendor dashboard build with no technical innovation, no user discovery, and no expansion vision. The contrarian scenario requires reimagining the entire project from scratch. The raw material -- familiarity with storage APIs and Splunk -- is a starting point, but barely.

## Verdict

**Startup Viability Score**: 2/10

**One-Line Verdict**: "This is a Splunk dashboard, not a company."

**What Would PG Say**: "You built a dashboard for one vendor's storage array on someone else's platform. That is not a startup -- that is a weekend project for a storage admin who knows SPL. If you want to make this interesting, tell me about the storage admin who is managing 500 arrays from 5 different vendors and wants to throw their laptop out the window. That person might pay for something. But this is not that thing."

**The Assignment**: Go find 5 storage administrators at Fortune 500 companies who manage mixed-vendor SAN environments (NetApp + Dell EMC + Pure, etc.). Ask them one question: "How do you monitor all of your storage from one place?" If the answer is consistently "I don't, and it drives me insane," you might have the seed of a real product. If the answer is "we use Cloud Insights / Datadog / our vendor tools and it is fine," then this is a dead end. Do this before writing a single line of code.
