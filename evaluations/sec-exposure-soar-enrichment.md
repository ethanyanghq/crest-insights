# Evaluation: Exposure SOAR Enrichment

**Source**: integration-for-google-secops-soar.md
**Category**: Security
**Date Evaluated**: 2026-03-19

## The Idea (In One Paragraph)

A product that bridges the gap between Continuous Exposure Management (CEM) platforms and Security Orchestration, Automation and Response (SOAR) tools, specifically Google SecOps SOAR. The pitch: security analysts today are drowning in alerts but starved of context. They see a vulnerability but cannot see the attack path leading to it, the assets connected to it, or the risk relative to everything else. This product automatically enriches SOAR alerts with attack path data, risk scores, and breach point identification, then provides automated playbooks and visualization widgets so analysts can prioritize and remediate faster -- regardless of which SIEM they run underneath.

## Forcing Questions Assessment

### Q1: Demand Reality

**Weak.** The case study names no customer. It refers to "the customer" throughout but heavily anonymizes them, and the hero image and metadata strongly suggest this is XM Cyber. That means the "customer" here is a cybersecurity vendor wanting its own product to integrate with Google SecOps SOAR -- not an end-user enterprise desperate for a solution. This is vendor enablement, not user pull. The demand signal is one vendor wanting its data surfaced in another vendor's platform. That is a real need, but it is the vendor's need, not the end user's. There is no evidence of end-user organizations banging on the door asking for this integration. No expansion metrics, no "after deployment, usage grew X%," no quotes from SOC analysts saying this changed their workflow. The strongest demand signal is simply that the integration was commissioned at all, which suggests the CEM vendor believes it needs Google SecOps SOAR compatibility to compete. That is a distribution requirement, not product-market fit.

### Q2: Status Quo

**Partially described.** The case study states that analysts had "limited context," "manual workflows," and "prioritization difficulties." These are real and common pain points in security operations. But the description is generic -- these are the same complaints you would hear from any SOC anywhere. The specific status quo before this integration is not described. Were analysts alt-tabbing between the CEM console and Google SOAR? Were they exporting CSVs? Were they ignoring CEM data entirely because it was not in their primary workflow? The case study does not say. The mention of "platform dependencies" (organizations using non-Google SIEMs facing integration challenges) is actually the most interesting status quo detail -- it hints that the real pain is multi-platform compatibility, not just enrichment.

### Q3: Desperate Specificity

**Missing.** No specific human is named or described with enough specificity to be actionable. "Security analysts at the customer side" is the closest we get. We do not know: What size SOC? How many analysts? What tier (L1 triage vs. L3 threat hunting)? What vertical? What compliance pressures? The case study describes the problem at a category level -- "organizations needed a way to integrate" -- rather than painting a picture of a specific person's daily misery. You cannot email "organizations."

### Q4: Narrowest Wedge

**Identifiable but buried.** The narrowest wedge here is probably the risk scoring engine: a lightweight service that takes entity data from a CEM platform and returns a single, weighted risk score that can be consumed by any SOAR tool. Nine risk factors, customizable weights, actionable output. That could be a standalone API product -- "send us an entity, get back a prioritized risk score with attack path context" -- that does not require the full integration, the playbooks, or the visualization widgets. But the case study does not present it that way. Instead, everything is bundled into a comprehensive integration package that presumably required significant custom work. The mention that the solution "could be easily migrated to the Content pack once it is GA" suggests this is heading toward a packaged product, but it is not there yet.

### Q5: Observation & Surprise

**None reported.** The case study reads as a clean delivery narrative: problem, solution, capabilities. There is no mention of anything unexpected -- no "we built the integration and discovered analysts were actually using it for X instead of Y," no "the breach point management feature turned out to be the most-used capability despite not being in the original scope." Everything went as planned, which in startup terms is a red flag. Real products emerge from surprise. This reads like a spec was written, the spec was executed, and a case study was published.

### Q6: Future-Fit

**Mixed.** On one hand, CEM is a growing category, SOAR adoption is increasing, and the need for cross-platform enrichment is real and durable. On the other hand, this faces a massive platform risk: Google could build this integration natively. In fact, Google has strong incentives to build first-party integrations with major CEM vendors to drive Google SecOps adoption. The case study even notes the solution could migrate to a "Content pack" -- meaning the natural home for this is as a first-party or marketplace integration, not a standalone product. Additionally, AI-driven security copilots (like Google's own Gemini in Security) are evolving to provide exactly this kind of contextual enrichment natively. In 3 years, the enrichment and playbook automation described here could be a built-in feature of the platform.

## The Paul Graham Test

### Schlep Blindness

**Moderate schlep, but not unique.** Building SOAR integrations is genuinely tedious -- you need to understand both platforms deeply, handle edge cases in data models, deal with API rate limits, and build playbooks that work in real SOC workflows. Most security vendors would rather hire a Crest Data to do this than build it themselves. That is a real schlep. But it is also a well-known schlep -- there are multiple integration consulting firms that do exactly this work. The schlep is real but not blind; it is a recognized cost of doing business in the security ecosystem.

### Do Things That Don't Scale

**This IS the unscalable thing.** The entire engagement is a custom integration built for one vendor's needs. The question PG would ask is: "What did you learn from doing this by hand that would let you do it automatically next time?" If the answer is "we now have a reusable framework for building CEM-to-SOAR integrations," that is interesting. If the answer is "we built a one-off integration using the Google SOAR SDK and our knowledge of the customer's API," that is just consulting. The case study does not give enough signal to determine which it is, but the mention of "Content pack" migration suggests some productization thinking.

### Default Alive or Default Dead

**Default dead as a startup.** There is no self-serve revenue model here. Each deployment would require understanding the customer's specific CEM platform, their SOAR configuration, their risk scoring preferences, and their playbook requirements. The revenue model is services, not software. You would need to build a genuinely self-serve product -- a universal CEM-to-SOAR adapter that works out of the box -- to be default alive, and nothing in the case study suggests that exists yet.

### Frighteningly Ambitious

**No.** Building an integration between two enterprise security platforms is useful but not ambitious in the way PG means. "Frighteningly ambitious" in this space would be: "We are replacing the entire SOAR platform with AI agents that automatically investigate and remediate security incidents using attack path data." That would make people uncomfortable. An integration that enriches alerts with risk scores does not make anyone uncomfortable.

### Earnest Test

**Mixed.** The case study demonstrates real domain knowledge -- understanding of CEM data models, SOAR playbook architecture, risk scoring methodologies, and the practical challenges of cross-platform security operations. The detail about 20+ filtering parameters for breach points and nine risk factors suggests genuine depth. But the writing is pure consulting-speak: "strategic solution design," "true operational value beyond basic connectivity," "profound understanding." Earnest founders talk about the problem; consulting firms talk about their own capabilities.

## Startup Quality

### Market

**Size**: The CEM-to-SOAR integration market is a niche within a niche. The broader SOAR market is real (~$2-3B and growing), and the CEM market is emerging fast (XM Cyber, Tenable, Qualys, etc.). But the specific intersection -- enriching SOAR workflows with CEM data -- is a feature-level market, not a company-level market. The "universal SIEM compatibility" angle hints at a broader play (a universal security data enrichment layer), but the case study does not pursue that framing.

**Timing**: Decent. CEM is a hot category, Google SecOps is gaining share, and the proliferation of security tools creates genuine integration pain. But platform vendors are rapidly building their own integration ecosystems (Google Marketplace, Splunk's ecosystem, etc.), which could absorb this value quickly.

**Competition**: SOAR platforms themselves are building integration frameworks. XM Cyber (the likely customer here) has its own integrations team. Google has a marketplace for SecOps integrations. Torq, Tines, and other next-gen SOAR platforms are building universal connectors. The space is getting crowded at every layer.

### Product

**Defensibility**: Weak. The integration itself is not defensible -- any competent security engineering team could replicate it given the same API access. The playbooks and risk scoring logic have some value but are not proprietary in a meaningful sense. Once built, the CEM vendor could maintain it in-house. The only defensibility argument is speed-to-market and accumulated knowledge of edge cases, which is a consulting moat, not a product moat.

**Scalability**: Low. Each new CEM vendor or SOAR platform requires significant custom work. The case study describes features specific to one CEM platform's data model (attack paths, breach points, entity scoring). Generalizing this to N CEM platforms times M SOAR platforms is an O(N*M) problem, which is the classic integration tax that does not scale.

**Technical depth**: Moderate. The risk scoring algorithm with nine weighted factors and the breach point filtering with 20+ parameters suggest non-trivial logic. The visualization widgets add value. But the core technical work is API integration, data mapping, and playbook authoring -- skilled work, but not novel engineering.

### Team Signal

The case study suggests competent integration engineers who understand both the CEM domain and the Google SecOps SOAR platform well. The cross-platform SIEM compatibility work hints at architectural thinking beyond the immediate scope. But there is no evidence of creative problem-solving or non-obvious discovery. The engagement reads as a well-executed professional services delivery.

## Wild Card -- "But What If?"

### The Contrarian Question

**What if the N*M integration problem is actually the opportunity?** The obvious objection is: "This is just one integration between one CEM platform and one SOAR platform. That is a feature, not a company." But what if the pain of connecting security data sources to orchestration platforms is so universal, so tedious, and so poorly served that there is room for a "Plaid for security" -- a universal data enrichment layer that sits between any detection tool and any response tool? Every SOC has this problem: their tools do not talk to each other, and building integrations is expensive and fragile. If you have built 10 of these integrations by hand, you might have the pattern recognition to build a universal adapter that no one building their first integration could match. The consulting dependency becomes the training data for the product.

### The Crazy Upside Scenario

If everything breaks right: you start with CEM-to-SOAR integrations because that is where the pain is most acute. You build a universal security context layer -- a service that ingests data from any security tool (CEM, EDR, vulnerability scanners, threat intel, identity) and exposes it as enriched, prioritized context to any orchestration platform (SOAR, SIEM, ticketing). You become the connective tissue of the SOC. Every new data source you add makes you more valuable to every customer, creating a mild network effect. Platform vendors cannot replicate you because they only care about their own ecosystem; you are the neutral party. You are Mulesoft for security operations. Acquisition target for Palo Alto, Google, or Microsoft at $500M-$1B within 5 years.

### Risk Worth Taking?

**Faint pulse.** The universal security enrichment layer is a real idea, and the consulting work described here could be the first step toward building it. But the case study itself does not provide evidence that the team is thinking in those terms. The engagement is scoped as a single-vendor, single-platform integration. The "universal SIEM compatibility" feature is interesting but modest. To make the bull case work, you would need to: (1) abstract the data model beyond one CEM vendor, (2) support multiple SOAR platforms, not just Google, (3) build a self-serve deployment model, and (4) find 10 paying customers who want this as a product, not a project. None of that is evidenced here. The pulse is there, but it is faint.

## Verdict

**Startup Viability Score**: 3/10

**One-Line Verdict**: "This is vendor enablement work packaged as a case study -- it is a feature that the CEM vendor should own, not a standalone company."

**What Would PG Say**: "You built an integration for a security vendor to make their product work with Google's platform. That is useful work, but it is their feature, not your company. The interesting question is whether you have built enough of these integrations to see the pattern nobody else sees -- the universal security context layer. If you have, stop doing one-off integrations and go build that. If you have not, do five more and then come back."

**The Assignment**: Talk to 10 SOC managers (not CEM vendors, but the actual SOC teams that use both CEM and SOAR tools) and ask them: "How many hours per week does your team spend manually correlating data between security tools that do not talk to each other?" If the answer is consistently double-digit hours, you have a startup. If it is "we have an integration for that," you do not.
