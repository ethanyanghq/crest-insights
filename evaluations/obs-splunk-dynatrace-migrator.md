# Evaluation: Splunk to Dynatrace Migrator

**Source**: accelerating-enterprise-observability-with-ai-driven-migration-to-dynatrace.md
**Category**: Observability
**Date Evaluated**: 2026-03-19

## The Idea (In One Paragraph)

An AI-powered migration engine that automatically converts observability assets (dashboards, alerts, queries) from one monitoring platform to another -- specifically Splunk to Dynatrace. Instead of manually rewriting 3,000+ dashboards and alerts by hand (a 120 man-day slog), the engine automates ~65% of the conversion, translating Splunk queries into Dynatrace Query Language and reconstructing dashboard JSON definitions, cutting migration time by roughly half. The pitch: every large enterprise eventually has to migrate between observability platforms, and doing it manually is a nightmare of tedious, error-prone translation work that nobody wants to do.

## Forcing Questions Assessment

### Q1: Demand Reality

There is a real customer here -- a "globally recognized financial services enterprise" with operations spanning hundreds of countries, processing millions of transactions. The description strongly suggests a major payment network (the profile matches Visa or Mastercard scale). They paid for this work. They had 3,000+ dashboards and alerts that needed migrating, and they clearly could not do it themselves in any reasonable timeframe. That is real demand. However, the demand is for a one-time migration event, not an ongoing product. The customer needed this once. They are not going to need it again next quarter. The question is whether there are enough enterprises in the pipeline going through Splunk-to-Dynatrace migrations to sustain a product business, versus a consulting engagement that recurs only as long as platform migrations keep happening. The case study also cites "5,500+ projects for 150+ global customers," which suggests Crest Data has broad consulting demand, but that is demand for the consulting firm, not necessarily for this specific migration engine as a standalone product.

### Q2: Status Quo

The status quo is extremely clear and painful: manual migration. The case study states the original estimate was 120 man-days of manual effort -- that is roughly 6 months of a full-time engineer's life spent rewriting dashboards one by one. In practice, what enterprises do today is assign a team of contractors or junior engineers to go through each dashboard, understand the Splunk query, manually translate it to the target platform's query language, rebuild the dashboard layout, and test it. This is brutally tedious, error-prone, and expensive. Some enterprises avoid the pain entirely by staying on legacy platforms longer than they should, paying escalating licensing costs and accumulating technical debt, because the migration cost is so daunting. Others do partial migrations and end up running two platforms in parallel, which is even worse. The pain is real, specific, and quantifiable.

### Q3: Desperate Specificity

The most desperate person here is the **platform engineering lead or observability team lead** at a large enterprise who has been told by leadership to migrate off Splunk (maybe because of licensing costs after the Cisco acquisition, maybe because of a strategic move to Dynatrace/Datadog/etc.) and is staring at 3,000+ dashboards that need to be recreated. They know that if they do it manually, it will take 6+ months, the team will hate them for assigning the work, errors will slip through, and critical monitoring gaps will appear in production during the transition. They are also personally on the hook if anything breaks during migration. This person is real and exists at hundreds of large enterprises right now, especially in the wake of Splunk's acquisition by Cisco, which is driving a wave of re-platforming decisions. The case study does not name this person explicitly, but the profile is very concrete.

### Q4: Narrowest Wedge

The narrowest wedge is clear: **a Splunk-to-Dynatrace query translator**. Not a full migration service. Not a consulting engagement. Just a tool that takes a Splunk SPL query, converts it to DQL, and outputs a valid Dynatrace dashboard JSON. You could ship this as a CLI tool or a web app. Upload your Splunk dashboard export, get back a Dynatrace-compatible version. Charge per dashboard or per migration. The case study already describes a "65/35 approach" -- 65% automated, 35% manual validation. A product version of this would aim to push that ratio to 85/15 or 90/10 over time. The wedge is tight enough that you could build an MVP in weeks, not months. The problem is that this wedge may be too narrow -- it is a point-to-point migration tool (Splunk to Dynatrace specifically), and the total addressable market for that exact migration path is limited. The bigger play would be a universal observability migration engine that handles any source-to-destination pair, but that is a much harder product to build.

### Q5: Observation & Surprise

Nothing. The case study reads as a clean, planned execution. The 65/35 automation-to-manual ratio is stated as a design choice, not a discovery. There is no mention of unexpected findings, surprising usage patterns, dashboards that revealed something unexpected about the customer's monitoring practices, or features of the migration engine that emerged from the work itself. Everything went "as expected." This is a red flag from a startup perspective. The most interesting products emerge when builders discover something non-obvious during hands-on work with customers. The absence of any surprises suggests this was a well-executed but routine consulting engagement.

### Q6: Future-Fit

Mixed signal. On one hand, observability platform migrations are likely to increase in the near term. The Cisco acquisition of Splunk is driving re-platforming decisions. The observability market is consolidating. Enterprises that adopted Splunk for monitoring 5-10 years ago are now evaluating purpose-built observability platforms like Dynatrace, Datadog, and Grafana. This creates a wave of migration demand. On the other hand, this is a transitional need, not a durable one. Once enterprises migrate, they do not need the tool again. And the major observability platforms themselves are investing in migration tooling -- Dynatrace, Datadog, and others all have an incentive to make it easy for customers to switch TO their platform. AI is also a double-edged sword here: yes, AI makes the translation engine better, but generalist LLMs are also getting very good at code translation tasks, including query language conversion. In 3 years, an enterprise might just paste their SPL queries into an AI assistant and get DQL back without a specialized tool. The window for this as a standalone product may be 2-3 years, not 10.

## The Paul Graham Test

### Schlep Blindness

This is where the case study gets interesting. Observability migration is a genuine schlep. It is boring. It is tedious. Nobody wants to build a company around translating dashboard queries from one proprietary language to another. Most engineers would rather work on literally anything else. And yet, every major enterprise going through a platform migration has this problem, and it costs them hundreds of thousands of dollars in labor to solve manually. The unsexy nature of the work is a real schlep-blindness signal. However, the schlep here is not deep enough to be a lasting moat. Query translation is fundamentally a bounded problem -- once you have good mappings between SPL and DQL, the hard part is done. It does not compound in the way that, say, building a data pipeline platform does.

### Do Things That Don't Scale

The 65/35 approach is literally doing things that don't scale -- 35% manual validation for every migration. This is fine for a consulting engagement but the question is whether the unscalable work is teaching them something that leads to a scalable product. The case study does not provide evidence of that learning loop. Are they feeding the manual corrections back into the engine to improve automation rates? Are they discovering patterns across customers that generalize? If so, that is the path to a product. If not, it stays consulting.

### Default Alive or Default Dead

Default dead as a standalone startup. The revenue model is project-based (one-time migrations), not recurring. Each customer pays once and never comes back. You would need a constant pipeline of new enterprises migrating between the same pair of platforms. The market timing is favorable right now (post-Splunk-acquisition wave), but that wave will crest and recede. There is no organic growth mechanism -- customers do not expand usage over time, they finish and leave. To be default alive, you would need to either (a) expand to many platform pairs to keep the pipeline full, or (b) pivot to ongoing observability management, not just migration.

### Frighteningly Ambitious

No. Migrating dashboards from one platform to another is useful but not ambitious. It does not make you think "can they really do that?" It makes you think "that sounds tedious but tractable." The frighteningly ambitious version would be: "We are building the universal translation layer for all observability data, so enterprises never have platform lock-in again. Any query, any dashboard, any alert, portable across any observability platform, in real time." That would be frightening. What is described here is a point migration tool.

### Earnest Test

The case study reads as competent but not passionate. The language is polished consulting-speak: "accelerated time-to-value," "unified observability," "future-ready operating model." There is no evidence of the builders being deeply frustrated by the migration problem themselves, or having a strong point of view about how observability should work. It reads like a well-executed deliverable for a client, not a team that discovered something they could not stop thinking about. That said, the "proprietary in-house migration engine" suggests someone on the team cared enough to build tooling rather than just throwing bodies at the problem. That impulse -- to automate rather than just staff up -- is the seed of a product mindset.

## Startup Quality

### Market

**Size**: The observability market is large (~$20B+), but the migration tooling sub-market is small and transient. Every enterprise migrates once. The total number of enterprises migrating from Splunk specifically is in the low thousands. At $50-200K per migration, the total addressable market for Splunk-to-Dynatrace migration specifically might be $500M-$1B over the life of the migration wave -- real money, but a shrinking pie over time. If you generalize to all observability platform migrations (any source to any destination), the market expands significantly but the product complexity also multiplies.

**Timing**: The timing is good right now. Cisco's acquisition of Splunk (closed 2024) is creating uncertainty and driving re-platforming evaluations. Dynatrace, Datadog, and Grafana are all aggressively courting Splunk customers. This window will last 2-4 years. After that, most enterprises that were going to migrate will have done so.

**Competition**: Dynatrace itself offers migration assistance. Datadog has migration tooling. Every major observability vendor has a "migrate from Splunk" program because it is in their direct commercial interest. Consulting firms like Accenture, Deloitte, and specialized shops all offer migration services. The proprietary migration engine is a differentiator within the consulting market, but as a standalone product it would face competition from the platform vendors themselves, who are motivated to give migration tooling away for free to win the subscription.

### Product

**Defensibility**: Weak as a standalone product. The migration engine's value is in the quality of its SPL-to-DQL translation mappings and its handling of edge cases. This is real IP, but it is not deeply defensible. A well-funded competitor (or the platform vendor itself) could replicate the core functionality. There are no network effects. There are no data moats. Switching costs are low because migration is a one-time event. The only defensibility is execution speed and accuracy, which matters but is not structural.

**Scalability**: The 65/35 automation ratio is a bottleneck. If that ratio does not improve significantly (to 90%+ automation), every migration still requires a human validation team, which means the business scales linearly with headcount, not exponentially with software. The case study does not describe a self-serve product path. Could you imagine a customer uploading their Splunk exports and getting Dynatrace-ready assets back without human intervention? Technically yes, but the case study does not demonstrate that the engine is close to that level of reliability.

**Technical depth**: Moderate. Building a robust query language translator is non-trivial -- SPL and DQL have different semantics, different function libraries, different approaches to time-series data. Handling 3,000+ dashboards with their varied complexity levels requires dealing with many edge cases. This is real engineering work, not just configuration. But it is fundamentally a bounded translation problem, not an open-ended technical challenge.

### Team Signal

The team clearly has deep Splunk and Dynatrace expertise -- you cannot build a 65%-accurate migration engine without understanding both platforms intimately. The decision to build a migration engine rather than just assigning manual labor shows product instinct. The "5,500+ projects for 150+ global customers" suggests a team that has seen a wide range of enterprise environments. However, the case study does not surface any non-obvious insight or creative problem-solving. It reads as competent execution of a well-understood problem.

## Wild Card -- "But What If?"

### The Contrarian Question

The obvious objection is: "This is a one-time migration tool. Customers use it once and never come back. That is not a business." But what if the one-time nature is actually the opportunity?

Here is the contrarian angle: **What if observability portability becomes a permanent need, not a one-time event?** Right now, enterprises treat platform migrations as rare, painful events. But what if the future is multi-platform observability? What if enterprises want to run Dynatrace for APM, Datadog for infrastructure, and Grafana for custom dashboards -- and they need a universal translation layer that keeps everything in sync? What if the "migration engine" is actually the seed of an "observability abstraction layer" -- a product that lets enterprises write monitoring logic once and deploy it to any platform?

This is the Terraform analogy: Terraform did not just help you set up AWS once. It created an abstraction layer that let you manage infrastructure across any cloud provider. If someone built the "Terraform for observability" -- a platform-agnostic way to define, manage, and deploy dashboards, alerts, and monitoring logic across any observability platform -- that could be genuinely big.

### The Crazy Upside Scenario

If everything breaks right: The Splunk migration wave generates early customers and revenue. The migration engine evolves into a universal observability definition language (think: "Observability as Code"). Enterprises adopt it not just for migration but for ongoing management -- defining their monitoring logic in a platform-agnostic format that can be deployed to any backend. The product becomes the control plane for multi-cloud, multi-platform observability. Major enterprises standardize on it because it eliminates vendor lock-in. The company becomes the "HashiCorp of observability" -- not the monitoring platform itself, but the abstraction layer that sits above all monitoring platforms. In this scenario, the TAM is not the migration market ($500M-$1B) but the observability management market ($5B+), and the company has a genuine platform moat built on the complexity of managing cross-platform observability at scale.

### Risk Worth Taking?

**Faint pulse.** The migration-to-abstraction-layer path is intellectually compelling but requires a significant leap from what is described in the case study. The current product is a point-to-point migration tool (Splunk to Dynatrace), not a universal observability layer. To get to the bull case, you would need to (a) generalize to many source/destination pairs, (b) shift from one-time migration to ongoing management, and (c) convince enterprises to adopt a new abstraction layer on top of their observability stack. Each of these is a major product and go-to-market challenge. The migration wave timing is real and creates a window, but the window is 2-3 years, which is tight to make the full leap. The risk-reward is asymmetric in the right direction -- the downside is a profitable consulting niche, the upside is a platform company -- but the probability of reaching the upside is low based on what is shown here.

## Verdict

**Startup Viability Score**: 3/10

**One-Line Verdict**: "This is a profitable consulting engagement with a useful internal tool, not a startup -- but the tool is the most interesting part."

**What Would PG Say**: "You built something that saves enterprises 47% of the effort on a painful migration. That is genuinely useful. But the customer does this once and leaves. The interesting question is not whether you can migrate more dashboards faster -- it is whether you can turn this translation layer into something enterprises keep running permanently. Right now you have a very good drill, but you need to find a reason for people to keep drilling."

**The Assignment**: Go talk to 10 enterprises that have already completed observability platform migrations (your own past customers). Ask them one question: "Now that you are on Dynatrace/Datadog/whatever, what is still painful about managing your dashboards and alerts?" If the answer is "nothing, it is fine," then this is a consulting engagement and you should keep printing money. If the answer involves ongoing pain around multi-platform management, dashboard sprawl, or observability drift, then you have the seed of a product that goes beyond migration. That conversation will tell you whether the "Terraform for observability" thesis has legs.
