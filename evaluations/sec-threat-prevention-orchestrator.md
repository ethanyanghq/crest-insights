# Evaluation: Threat Prevention Orchestrator

**Source**: automated-threat-prevention-to-accelerate-security-operations.md
**Category**: Security
**Date Evaluated**: 2026-03-19

## The Idea (In One Paragraph)

A product that lets SOC analysts block malicious IPs, URLs, and domains directly from within ServiceNow Security Incident Response — managing multiple block lists across multiple security gateways, with automated entry expiration and linked threat intelligence — so they can act on threats in seconds rather than manually coordinating across disparate security products.

## Forcing Questions Assessment

### Q1: Demand Reality

There is a real, named customer here: a "leading multinational provider of comprehensive IT security solutions" — an IT security vendor themselves, which is notable. If a company whose entire business is security felt they needed this, the pain is real. However, the customer is anonymized, so we cannot verify independently. The case study says manual correlation was "creating critical security gaps," which is a strong pain statement, but it is the vendor saying this, not the customer. There is no mention of expansion, recurring usage, or the customer demanding more after delivery. The demand evidence is moderate: a real engagement happened and someone paid for it, but we lack signals of ongoing pull or organic growth beyond the initial project.

### Q2: Status Quo

The status quo is clearly described: security analysts manually correlating information across "a diverse set of security products," then manually blocking malicious observables one by one, with no streamlined process. This is genuinely painful. Every SOC analyst in the world knows this workflow — the "swivel chair" problem of switching between tools, copy-pasting IOCs, and hoping nothing falls through the cracks. The case study describes higher turnaround times and "critical security gaps" as direct consequences. This is a real problem that people are already spending time and money on — through manual labor, duct-taped scripts, and partial SOAR implementations.

### Q3: Desperate Specificity

The case study actually names the human: the SOC analyst. More specifically, it is the analyst who has identified a malicious observable in a security incident and now needs to get it blocked across the organization's security gateways. The pain is concrete — they have the IOC, they know it is bad, and they cannot act on it quickly because there is no integration between their incident response platform and their blocking infrastructure. This is a specific, visceral frustration. That said, the case study does not quantify the pain (e.g., "it takes 45 minutes to block a single IOC across 6 gateways") or describe the emotional weight of watching threats slip through while you manually update lists.

### Q4: Narrowest Wedge

The narrowest wedge is clear and tight: a ServiceNow Security Incident Response module that lets you right-click on a malicious observable and push it to a block list across your security gateways, with automated expiration and threat intel linking. This is a product you could demo in 10 minutes and sell in a single meeting. The problem is that it is tightly coupled to ServiceNow SIR as the orchestration layer. The smallest version might be even simpler: a standalone tool that takes a list of IOCs and pushes them to your firewalls/proxies/DNS with one click, regardless of your ticketing platform. That version could be built in weeks and tested immediately.

### Q5: Observation & Surprise

Zero evidence of surprise. The case study reads as a clean spec-to-delivery project: customer had a requirement, Crest built the integration, it worked. There is no mention of user feedback, unexpected usage patterns, features that turned out to matter more than expected, or any pivot during the engagement. This is the biggest red flag. A consulting engagement that produces zero surprises has not been listened to closely enough, or the case study is just not capturing what actually happened.

### Q6: Future-Fit

Mixed. On one hand, threat volumes are increasing, SOC teams are perpetually understaffed, and the need for automated response is growing — this becomes more essential over time. On the other hand, this is exactly the kind of functionality that SOAR platforms (Palo Alto XSOAR, Splunk SOAR, ServiceNow's own Security Operations) are absorbing natively. ServiceNow has been aggressively building out its Security Operations suite, and automated blocking is table-stakes SOAR functionality. The risk is high that this becomes a native feature rather than a standalone product. AI-driven security orchestration could also leapfrog this by automating the entire triage-to-block workflow, making a manual "push to block list" button feel quaint.

## The Paul Graham Test

### Schlep Blindness

There is modest schlep here. Integrating ServiceNow SIR with multiple heterogeneous security gateways (different vendors, different APIs, different block list formats) is genuinely tedious work. Nobody wants to build and maintain connectors to 15 different firewall vendors' APIs. That said, this is exactly the kind of schlep that SOAR platforms already address. The schlep is real, but it is not under-explored — it is the core value proposition of an entire product category (SOAR). The work here is more "integration plumbing" than "solving a problem others cannot see."

### Do Things That Don't Scale

This entire engagement is unscalable by nature — custom integration work for a single customer's specific environment. The question is whether it revealed a scalable product, and the answer is: somewhat. The pattern — "take IOCs from your incident response platform and push them to your blocking infrastructure" — is universal. But the case study does not suggest the team extracted that pattern into something repeatable. It reads like a one-off delivery, not a product discovery process.

### Default Alive or Default Dead

Default dead. There is no revenue model beyond the consulting engagement. No indication of recurring revenue, no mention of a product being sold or licensed. The customer got their integration; the engagement presumably ended. To become a startup, someone would need to productize this, build a sales motion, and compete against entrenched SOAR vendors — all from a standing start. That is a heavy lift with no existing momentum.

### Frighteningly Ambitious

No. Blocking malicious observables from within ServiceNow is useful, incremental, and entirely predictable. It does not make anyone think "can they really do that?" It makes people think "why doesn't ServiceNow already do that?" Which is the fundamental problem — this feels like a feature gap in an existing platform, not a new category of product.

### Earnest Test

The case study suggests competent execution of a well-scoped integration project. The team understood the SecOps domain — they knew what block lists are, how gateways work, why expiration matters. But there is no evidence of deep, unusual insight or passion for the problem. It reads like a professional consulting deliverable, not the work of someone who has lived the SOC analyst's pain and thought obsessively about how to fix it.

## Startup Quality

### Market

**Size**: The SecOps automation market is large — multi-billion dollars and growing. But within that, "block list management as a ServiceNow integration" is a feature within a feature. The broader market (SOAR, security automation) is real, but the specific territory this occupies is narrow and already contested.

**Timing**: The timing argument for security automation is perennially valid — threats are increasing, analysts are overwhelmed. But there is no specific "why now" moment here. SOAR has been a category for years. The AI wave could create a new timing argument (AI-powered automated response), but this case study does not touch AI at all.

**Competition**: Palo Alto XSOAR, Splunk SOAR, Tines, Torq, Swimlane, and ServiceNow's own Security Operations product all play in this space. The competition is fierce and well-funded. The specific wedge (block list management) is too narrow to differentiate against these incumbents.

### Product

**Defensibility**: Weak. Once built, this integration could be replicated by any ServiceNow partner or by ServiceNow itself. There are no data network effects, no proprietary algorithms, and no switching costs beyond the normal integration switching costs. The only potential moat is deep knowledge of the specific customer's gateway landscape, which is not scalable.

**Scalability**: Low. The integration is ServiceNow-specific and likely requires customization for each customer's gateway environment. Moving toward self-serve would require building a connector framework for dozens of gateway vendors — which is essentially building a SOAR platform.

**Technical depth**: Modest. This is integration and configuration work — connecting APIs, managing data formats, building UI within ServiceNow. It is competent engineering, but it is not technically novel.

### Team Signal

The team demonstrated domain expertise in ServiceNow SecOps and security operations workflows. They understood the operational model well enough to include features like automated expiration and threat intel linking, which shows they thought about the analyst's workflow beyond the immediate requirement. However, there is no evidence of creative problem-solving or non-obvious discovery. This was a competently executed, well-scoped consulting engagement.

## Wild Card — "But What If?"

### The Contrarian Question

The obvious objection is: "This is a SOAR feature that ServiceNow will ship natively." But what if the real insight is that SOAR platforms are too complex and too expensive for the specific, common pain of blocking IOCs quickly? What if there is a market for a lightweight, purpose-built "IOC blocking" tool that does one thing extremely well — takes observables from any source (not just ServiceNow) and pushes them to any blocking infrastructure with one click? The SOAR platforms try to do everything; maybe the opportunity is in doing this one thing with radically less setup time and cost. Think of it as "Stripe for threat blocking" — dead simple, works immediately, no 6-month deployment.

### The Crazy Upside Scenario

If you squint hard: a startup that builds the universal "threat response execution layer" — the last mile between "we know this is bad" and "it is blocked everywhere." Not a SOAR platform (too complex), not a firewall management tool (too low-level), but a thin, API-driven layer that connects any detection source to any enforcement point. If you nail the connector ecosystem (every major firewall, proxy, DNS, cloud security group), you become the plumbing that every SOC depends on. Like Plaid for fintech, but for security enforcement. With AI-driven decision-making layered on top, it could auto-block based on confidence scores. The bull case is a $500M+ outcome as the "universal enforcement API."

### Risk Worth Taking?

**Faint pulse.** The contrarian scenario is intellectually appealing, but it requires competing against well-funded SOAR vendors, building a massive connector ecosystem, and convincing buyers that a point solution is better than their platform's native capability. The case study itself provides no evidence that the team discovered anything that would give them a unique advantage in pursuing this. The idea is plausible in the abstract but not grounded in any proprietary insight from this engagement.

## Verdict

**Startup Viability Score**: 3/10

**One-Line Verdict**: "This is a feature, not a company — and it is a feature the platform vendor is already building."

**What Would PG Say**: "You built a useful integration, but useful integrations are not startups. The SOC analyst who needs this is real, but they are going to get this from ServiceNow natively within two product cycles. If you want to build a startup here, forget ServiceNow entirely and ask: what is the universal, platform-agnostic version of 'I found something bad, now block it everywhere instantly'? That might be something."

**The Assignment**: Talk to 10 SOC analysts at companies that do NOT use ServiceNow and ask them: "When you identify a malicious IOC, how long does it take you to get it blocked across all your infrastructure, and what does that process look like step by step?" If the answer is consistently "too long and too painful," and if the pain is platform-agnostic, there might be a startup in the universal enforcement layer. If the answer is "our SOAR handles it," walk away.
