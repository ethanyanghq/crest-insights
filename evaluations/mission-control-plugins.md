# Evaluation: Mission Control Plugins

**Source**: mission-control-plugins.md
**Category**: Security
**Date Evaluated**: 2026-03-19

## The Idea (In One Paragraph)

A plugin marketplace and development framework for Splunk Mission Control that gives SOC analysts instant, in-context enrichment — threat intel, endpoint data, cloud logs, CASB signals — surfaced directly inside the incident they're triaging, so they stop toggling between six browser tabs and start resolving incidents in minutes instead of hours. The pitch: we build the connective tissue between a SOC's existing tools and the triage workflow, drastically reducing Mean Time to Acknowledge and Mean Time to Resolve.

## Forcing Questions Assessment

### Q1: Demand Reality

**Weak.** The case study names no specific customer. It says Crest built plugins "for a number of customers across CASB, Threat Intel, EDR, VAPT, and Cloud solutions," but not who those customers are, what they paid, or how much usage the plugins see. The strongest demand signal is that Crest was involved since Splunk Mission Control's beta program and built plugins for "early access partners," which implies Splunk itself pulled them in — but that's partner-channel demand, not end-user pull. There is no evidence of a customer who would be "genuinely upset if this disappeared tomorrow." The case study leans on generic survey data ("more than half of respondents reported a rate of 50% or higher of false-positive alerts") rather than specific customer outcomes. This is a brochure, not a demand signal.

### Q2: Status Quo

**Described but generic.** The case study paints a clear picture of the current pain: SOC analysts manually switch between tools, copy-paste IOCs into separate threat intel platforms, manually comb through network and endpoint logs, and context-switch constantly during triage. The "cry wolf effect" — false-positive fatigue — is well-documented in the industry and genuinely painful. But the description is textbook SOC pain. Every SOAR vendor, every XDR pitch deck, and every SIEM marketing page describes this exact problem. The case study does not describe what specific workarounds these particular customers were using before the plugins existed, which would have been far more revealing.

### Q3: Desperate Specificity

**Partially there.** The case study does identify the SOC analyst as the target user and names the specific pain of false-positive triage fatigue. That is a real human with a real problem. But it never goes deeper — no specific tier of analyst (Tier 1 vs. Tier 2), no specific type of alert that was most painful, no quote from an actual analyst, no description of what their day looked like before and after. "SOC analyst who spends the majority of their time analyzing high volumes of alerts" is an industry cliche, not a persona built from observation. The mention of Jainil Desai as TPM is a team credit, not a customer voice.

### Q4: Narrowest Wedge

**There is a wedge, but it is platform-dependent.** The narrowest wedge is a single enrichment plugin — say, one that pulls VirusTotal or CrowdStrike threat intel into the Mission Control incident view with zero configuration. That is a thing a SOC analyst would use the moment it's installed. The problem is that this wedge only works inside Splunk Mission Control. You are building a plugin for someone else's platform, not a standalone product. The value of the wedge is real, but the distribution and survival of the wedge is entirely at Splunk's discretion. If Splunk decides to build this natively, or changes the plugin framework, or deprecates Mission Control (which, post-Cisco acquisition, is a live risk), the wedge evaporates.

### Q5: Observation & Surprise

**Nothing.** The case study provides zero evidence of unexpected user behavior, surprising adoption patterns, or emergent usage. Everything described was spec-driven: Crest was given a plugin framework, built plugins to spec, delivered them to partners. There is no moment of "we thought they'd use it for X but they actually used it for Y." This is pure consulting delivery narrative.

### Q6: Future-Fit

**Mixed, trending negative.** On one hand, SOC automation and enrichment are durable needs — the volume of alerts only grows, and the analyst shortage only deepens. On the other hand, the specific vehicle (Splunk Mission Control plugins) is precarious. Cisco acquired Splunk in March 2024. Cisco has its own XDR story, its own SOAR (SecureX), and its own roadmap. Mission Control as a standalone surface area may not survive the integration. More broadly, the trend in security is toward AI-native triage — systems that don't just surface enrichment but actually make triage decisions autonomously. Building enrichment plugins is solving yesterday's version of the problem. In three years, the analyst may not be manually reviewing enrichment data at all; an AI agent will be doing initial triage. This makes the specific product less essential, even as the underlying problem (too many alerts, not enough analysts) becomes more acute.

## The Paul Graham Test

### Schlep Blindness

**Moderate schlep, but not uniquely so.** Building integrations between security tools is tedious, requires deep knowledge of multiple vendor APIs, and involves dealing with messy data formats — all hallmarks of a real schlep. But this is exactly the schlep that dozens of companies (Tines, Torq, Swimlane, every SOAR vendor) are already grinding through. The schlep here is not avoided by the market; it is actively contested. There is no proprietary schlep advantage — building a VirusTotal enrichment plugin for Splunk Mission Control is not a schlep that competitors cannot replicate. The only schlep advantage Crest had was being early (beta partner), which is a timing advantage, not a structural one.

### Do Things That Don't Scale

**Yes, inherently, but without the learning loop.** A consulting engagement is, by definition, unscalable. Crest did manual, white-glove plugin development for individual customers and for Splunk itself. This is exactly the "do things that don't scale" approach. But the key question PG asks is: did the unscalable work teach you something a product team building in isolation never would? There is no evidence of that here. The case study reads as: we built plugins, we delivered them. There is no mention of discovering that, for example, 80% of triage time was spent on one specific enrichment type, or that analysts used the plugins in an unexpected workflow. The unscalable work happened, but the insight extraction apparently did not.

### Default Alive or Default Dead

**Default dead.** There is no independent revenue model here. The revenue came from Splunk paying Crest to build plugins as a consulting engagement. If you extracted this as a standalone startup — "we build and sell Mission Control plugins" — you would need Splunk's continued support, access to the plugin framework, and customers willing to pay for plugins on top of their Mission Control license. You would be default dead, dependent on a single platform vendor's goodwill and roadmap. Post-Cisco acquisition, that dependency is even more precarious.

### Frighteningly Ambitious

**No.** Building plugins for an existing platform's plugin framework is not frighteningly ambitious. It is useful, competent integration work. A frighteningly ambitious version of this idea would be: "We are building the universal SOC triage brain that works across every SIEM, SOAR, and XDR — it doesn't matter which platform you use, our layer sits on top and makes your analysts 10x faster." That would be ambitious. Building Mission Control plugins is building apps for someone else's app store.

### Earnest Test

**Partially passes.** The involvement since Mission Control's beta program and the breadth of plugins across CASB, Threat Intel, EDR, VAPT, and Cloud suggest genuine domain knowledge and a real relationship with the security operations workflow. Crest clearly understands the SOC analyst's pain. But the earnestness is directed at being a great Splunk partner, not at solving the analyst's problem independently. The loyalty is to the platform, not the user.

## Startup Quality

### Market

**Size**: SOC tooling is a massive market — SIEM alone is $5B+, SOAR is $1B+, XDR is growing rapidly. But "Mission Control plugins" is a niche within a niche within a niche: specifically, plugins for one feature of one product from one vendor (now owned by Cisco). The addressable market as described is tiny. **Timing**: The timing was good in 2023-2024 (Mission Control was new, needed an ecosystem). By 2026, post-Cisco acquisition, the timing has likely passed. Cisco is rearchitecting the Splunk security stack around its own XDR vision. **Competition**: Splunk itself is the primary competitor — they can build any plugin natively. Other Splunk partners (Accenture, Deloitte, etc.) can build plugins too. There is no meaningful competitive moat for a third-party plugin developer.

### Product

**Defensibility**: Near zero as a standalone product. Plugins built on someone else's framework have no moat. Splunk can copy them, deprecate the framework, or change the API. **Scalability**: The plugins themselves could theoretically be self-serve (install from a marketplace), but the case study describes custom development for individual customers, which is consulting. There is no evidence of a productized, install-and-go plugin that scales without services. **Technical depth**: Moderate. Building enrichment plugins requires understanding of security data models, vendor APIs, and the Mission Control framework. But this is integration engineering, not proprietary algorithmic innovation.

### Team Signal

The team was trusted enough by Splunk to be a beta partner, which signals competence and domain credibility. Building plugins across five security categories (CASB, Threat Intel, EDR, VAPT, Cloud) suggests breadth of security domain knowledge. But there is no evidence of creative problem-solving or non-obvious discovery. The engagement reads as: Splunk gave us a framework, we built plugins, we delivered them. Competent execution, not product insight.

## Wild Card — "But What If?"

### The Contrarian Question

The obvious objection is: "You're building features for someone else's platform — you don't own anything." But what if the contrarian angle is this: what if the deep plugin-building experience across five security verticals taught Crest something about the universal enrichment problem that no single-platform vendor understands? Every SIEM vendor builds enrichment for their own platform. Every SOAR vendor builds playbooks for their own orchestration layer. But no one has built a universal enrichment layer that works across ALL of them — a single plugin architecture that can surface threat intel, endpoint data, and cloud context into Splunk, Chronicle, Sentinel, QRadar, and Elastic simultaneously. That would be platform-agnostic, and the cross-platform knowledge from building plugins across multiple vendor ecosystems could be the non-obvious advantage.

### The Crazy Upside Scenario

If everything breaks right: Crest takes the enrichment and triage acceleration knowledge from Mission Control plugins, generalizes it into a vendor-agnostic "SOC enrichment API" — a layer that sits between your threat intel sources and whatever SIEM/SOAR you use, and provides instant, contextual enrichment in a unified format. As enterprises go multi-SIEM (common in large orgs) and as the SIEM market fragments (Splunk, Chronicle, Sentinel, Elastic, CrowdStrike LogScale), the need for a platform-agnostic enrichment layer grows. Add AI-powered triage recommendations on top of the enrichment data, and you have a product that becomes the intelligence layer for every SOC, regardless of their SIEM choice. That is a fundable company. But it requires completely rethinking the current approach.

### Risk Worth Taking?

**Faint pulse.** There is a scenario where the cross-vertical plugin expertise becomes the foundation for a platform-agnostic enrichment product, but it requires multiple leaps: (1) abstracting the knowledge from Splunk-specific work, (2) building for multiple platforms, (3) competing with well-funded SOAR vendors who are already trying to own this layer, and (4) doing all of this without the crutch of Splunk partnership revenue. The odds are long, and the case study provides no evidence that the team is thinking in this direction.

## Verdict

**Startup Viability Score**: 3/10

**One-Line Verdict**: "You built apps for someone else's app store — where's the thing you own?"

**What Would PG Say**: "This is skilled integration work, and I can see the SOC analyst pain is real. But you're a subcontractor to Splunk's roadmap. The moment Cisco decides Mission Control plugins should be built in-house, you're done. If you want a startup here, you need to own the relationship with the analyst, not rent it from Splunk."

**The Assignment**: Go talk to 10 SOC analysts (not their managers, the actual Tier 1 analysts) who have used your Mission Control plugins. Ask them: "If Splunk Mission Control disappeared tomorrow, what would you miss most about these plugins — and would you pay for that capability as a standalone tool that works with any SIEM?" If more than 3 of them say yes and can describe what they'd pay for, you might have a product. If they all shrug and say "I'd just use whatever Splunk replaces it with," you have your answer.
