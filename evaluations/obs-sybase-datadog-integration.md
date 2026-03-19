# Evaluation: Sybase Datadog Integration

**Source**: scaling-enterprise-sybase-monitoring-through-datadog-integration.md
**Category**: Observability
**Date Evaluated**: 2026-03-19

## The Idea (In One Paragraph)

A plug-and-play Datadog integration that gives enterprises full observability into SAP Sybase ASE databases -- performance metrics, audit events, and error logs -- without installing any agent on the database servers themselves. The pitch: legacy database monitoring is fragmented, blind-spot-ridden, and incompatible with modern observability stacks. This integration makes Sybase a first-class citizen inside Datadog, the same way Postgres or MySQL already are, so managed service providers can monitor 20+ Sybase instances from a single pane of glass with pre-built dashboards and alert templates.

## Forcing Questions Assessment

### Q1: Demand Reality

There is a real customer here: a technology services provider managing 20+ mission-critical Sybase ASE databases across multiple clients. They were already paying for Datadog and already needed Sybase monitoring -- this was not a speculative engagement. The fact that the integration is published on the Datadog Marketplace (the case study links directly to `docs.datadoghq.com/integrations/crest-data-systems-sybase/`) is meaningful. Marketplace listings require Datadog's review and approval, and they only exist because someone asked for them. That is real demand.

However, the demand evidence is narrow. One unnamed customer. No expansion metrics, no revenue figures, no evidence of pull from other buyers. The question is whether this one customer represents a pattern or an outlier. Sybase ASE is a legacy database that SAP has been slowly de-emphasizing in favor of HANA. The total population of companies running mission-critical Sybase workloads is shrinking, not growing. The customer would likely be upset if this disappeared -- they clearly needed it -- but it is unclear how many other customers would feel the same.

### Q2: Status Quo

The case study describes the status quo clearly: "fragmented methods" involving multiple tools, no single source of truth, manual correlation between performance metrics and audit/error data, and slow troubleshooting. The customer was already spending time and money solving this problem badly -- they had monitoring, it just was not unified or scalable. That is a good sign. People were already doing the work, just painfully.

The key detail is the constraint: no new agents on database servers. This means the previous workarounds likely involved SSH scripts, cron jobs pulling from Sybase system tables, or separate monitoring tools entirely disconnected from Datadog. Anyone who has managed legacy database monitoring in an enterprise environment knows this is real pain -- cobbled-together scripts that break silently, dashboards that nobody trusts, and alert fatigue from poorly tuned thresholds.

### Q3: Desperate Specificity

The person who needs this most is a database operations lead at a managed services provider (MSP) -- someone responsible for SLA compliance across dozens of Sybase instances for multiple clients. They are the person who gets paged at 2 AM when a Sybase instance runs out of tempdb space, and they are the person who has to explain to the client why they did not catch it sooner. The case study gets close to naming this person but never quite does -- it stays at the level of "the team" and "the organization."

The specificity is moderate. The constraint about no agents on database servers is a real, specific operational requirement that signals genuine domain understanding. But the case study does not describe any individual's pain viscerally enough. You can infer the desperation, but you have to work for it.

### Q4: Narrowest Wedge

The narrowest wedge already exists: the Datadog Marketplace integration for Sybase ASE. This is a real, shippable product that someone can install from the Datadog Marketplace today. It comes with pre-built dashboards and alert templates. That is about as narrow and concrete as a wedge gets.

The problem is that this wedge may be too narrow. Sybase ASE is a niche database. The total addressable market for "Sybase monitoring inside Datadog" is small and shrinking. The wedge is sharp, but the log it needs to split may not be big enough to matter.

### Q5: Observation & Surprise

Nothing in this case study suggests surprise. The engagement went as planned: they identified requirements, built the integration, delivered dashboards and alerts, and the customer was satisfied. There is no mention of unexpected usage patterns, features that mattered more than expected, or pivots during the engagement. This reads like a well-executed consulting deliverable, not a product-market fit discovery process.

This is the weakest signal in the case study. Great products emerge from surprise -- from watching users do something you did not expect. There is zero evidence of that here.

### Q6: Future-Fit

This is where the idea faces its biggest headwind. Sybase ASE is a legacy technology. SAP has been pushing customers toward HANA for years. The population of Sybase ASE deployments is in long-term decline. Every year, some fraction of those 20+ databases gets migrated to a more modern platform.

On the other hand, legacy databases die slowly. Very slowly. There are mainframes from the 1970s still running in production. Sybase ASE databases powering financial systems will be around for a decade or more, precisely because migrating off them is expensive and risky. The monitoring need does not go away just because the technology is old -- in fact, as the Sybase talent pool shrinks, the need for automated monitoring arguably increases.

But "monitoring a dying technology" is a melting ice cube business. You can make money on it, but you are running a declining-revenue operation unless you expand to other legacy databases.

## The Paul Graham Test

### Schlep Blindness

This scores well on schlep blindness. Building a Datadog integration for Sybase ASE is exactly the kind of thing nobody wants to do. It requires deep knowledge of Sybase system tables, stored procedures, and monitoring APIs -- expertise that is increasingly rare. It requires understanding Datadog's integration framework and marketplace requirements. And the reward for all that work is serving a niche market of legacy database operators. Most engineers would rather build AI features than parse Sybase audit logs.

That is genuinely a schlep. The question is whether the schlep is big enough to build a company around, or just big enough to build a nice integration.

### Do Things That Don't Scale

The consulting engagement itself is the unscalable thing -- a custom integration built for one customer's specific constraints (no agents on database servers, multi-client isolation, client-specific dashboards). The Datadog Marketplace listing is the attempt to scale it. This is the right trajectory: learn from the custom work, productize the result.

But the case study does not describe what they learned from the unscalable work that they could not have known in advance. Good "do things that don't scale" stories end with "...and that is how we discovered X." This one ends with "...and we delivered what was spec'd."

### Default Alive or Default Dead

As a standalone startup focused solely on Sybase monitoring, this is default dead. The market is too small and shrinking. There is a clear revenue model (Datadog Marketplace listing, presumably with recurring fees), but the ceiling is low. You would need to expand to other legacy databases -- Oracle, DB2, Informix, older MySQL/Postgres versions -- to have a viable business. As a feature within a broader "legacy database observability" company, it might contribute to a default-alive trajectory, but not on its own.

### Frighteningly Ambitious

No. This is not frighteningly ambitious. It is competent and useful, but nobody hears "Sybase monitoring integration for Datadog" and thinks "can they really do that?" It is a well-scoped integration project, not a moonshot. There is no world-changing vision here -- just a gap in the Datadog ecosystem that someone competently filled.

### Earnest Test

The case study does suggest genuine domain knowledge. The constraint about no agents on database servers, the attention to audit and compliance requirements, the understanding of multi-tenant MSP operations -- these are not things a generic consulting team would know to care about. Someone on this team has spent real time in the trenches with enterprise database operations. That earnestness shows through, even in the polished case study language.

## Startup Quality

### Market

**Size**: Small and shrinking. Sybase ASE has an installed base, but SAP is not investing in growing it. The broader "legacy database monitoring" market is larger, but you would need to expand the product line significantly to address it. The observability market overall is massive ($50B+), but this is a very thin slice of it.

**Timing**: The timing is paradoxically both late and right. Late because Sybase is past its peak. Right because the customers who still run Sybase are increasingly desperate for modern tooling as their in-house Sybase expertise retires. The Datadog Marketplace is mature enough to be a real distribution channel. But there is no external catalyst -- no regulation, no technology shift -- creating urgency.

**Competition**: The case study says "available market solutions provided partial insights or required separate tools." This is likely true -- Sybase is niche enough that the major APM vendors (Dynatrace, New Relic, AppDynamics) have not built deep integrations. SolarWinds DPA supports Sybase, but it is a separate tool, not integrated into Datadog. The lack of competition is a signal that the market is too small, not that the opportunity is too hard.

### Product

**Defensibility**: Moderate. The integration is on the Datadog Marketplace, which provides some distribution advantage. Deep Sybase expertise is a mini-moat, as fewer engineers know this technology each year. But Datadog itself could build native Sybase support if the demand justified it. The defensibility is "nobody else cares enough to build this," which is real but fragile.

**Scalability**: The Marketplace listing is inherently self-serve -- customers can install it without a consulting engagement. That is good. But the case study describes significant customization (client-specific dashboards, tailored alert templates), which suggests the out-of-box experience may not be sufficient for most buyers. The gap between "install from Marketplace" and "actually useful in production" may still require professional services.

**Technical depth**: Moderate. Building a Datadog integration that collects Sybase metrics without an agent on the database server requires some clever engineering (likely a remote collector pattern). The pre-built dashboards and alert templates encode real operational knowledge. But this is integration engineering, not fundamental technical innovation.

### Team Signal

The team clearly has deep Sybase and Datadog expertise. The no-agent constraint and the multi-tenant MSP requirements suggest they understood the operational realities of their customer's environment. However, there is no evidence of creative problem-solving or non-obvious discoveries -- the engagement reads as competent execution of a well-understood problem.

## Wild Card -- "But What If?"

### The Contrarian Question

The obvious objection is: "Sybase is dying, why build monitoring for a dying database?" But what if that is exactly why this works? As Sybase expertise becomes rarer, the companies still running it become more desperate for automated monitoring. They cannot hire Sybase DBAs anymore -- the talent pool has aged out. They need tools that encode that expertise into software. The monitoring integration is not just collecting metrics; it is encoding the knowledge of what to watch for and when to panic into dashboards and alerts that a generalist can use.

Expand the lens: Sybase is not the only database in this situation. Oracle 11g, DB2, Informix, older SQL Server versions -- there are dozens of legacy database platforms where expertise is evaporating faster than the installed base. A company that builds best-in-class Datadog integrations for every legacy database that Datadog does not natively support well could own a real category. "Datadog for legacy infrastructure" is not sexy, but it could be a $50M+ ARR business serving the long tail of enterprise technology debt.

### The Crazy Upside Scenario

If everything breaks right: Crest Data (or a spinout) builds Datadog Marketplace integrations for every major legacy database (Sybase, Informix, DB2, older Oracle, etc.), plus legacy middleware (TIBCO, WebSphere, MQ Series) and legacy infrastructure (mainframe metrics, AS/400). They become the "Rosetta Stone" between legacy enterprise infrastructure and modern observability platforms. Every Fortune 500 company has legacy systems they cannot rip out and cannot monitor properly. Datadog, Grafana, and the other modern observability vendors do not want to invest in building integrations for dying platforms. Someone has to bridge that gap.

In the bull case, this becomes a platform company -- not just Datadog integrations, but also Grafana, New Relic, and Dynatrace connectors for legacy systems. The switching costs are high (once you have 50 legacy database instances monitored through these integrations, you are not ripping them out). The expertise moat deepens over time as fewer people know these systems. Revenue per customer is high because these are enterprise environments with real budgets. You could see $100M+ ARR in 5-7 years serving a market that every other startup is too cool to touch.

### Risk Worth Taking?

**Faint pulse.** There is a scenario here, but it requires a significant expansion beyond Sybase to other legacy databases and platforms, and it requires someone with the conviction to bet on "legacy infrastructure observability" as a category. The Sybase integration alone is not a startup -- it is a product feature. The broader vision of "modern monitoring for legacy infrastructure" is more interesting, but the case study does not articulate that vision. You would need to see evidence of expansion into other legacy platforms and pull from multiple customers to upgrade this to "interesting contrarian bet."

## Verdict

**Startup Viability Score**: 3/10

**One-Line Verdict**: "This is a good Datadog Marketplace integration, not a startup -- but there might be a legacy-infrastructure observability company hiding behind it if you squint."

**What Would PG Say**: "You built a useful thing for a real customer, and I respect the schlep. But Sybase monitoring is a feature, not a company. The interesting question is: are there 50 other legacy technologies where you could do the same thing? If so, come back and pitch me 'the last mile of enterprise observability' -- the company that bridges every dying platform to every modern monitoring tool. That might be something."

**The Assignment**: Call 10 managed service providers who run legacy databases (not just Sybase -- include DB2, Informix, older Oracle) and ask them how they monitor those systems today and what they spend on it. If you hear the same pain story from 7 out of 10, you might have a company. If Sybase is the only one where people are desperate, you have a nice integration business but not a startup.
