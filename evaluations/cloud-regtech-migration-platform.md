# Evaluation: RegTech Cloud Migration Platform

**Source**: regtech-business-growth-through-aws-cloud-migration.md
**Category**: CloudOps
**Date Evaluated**: 2026-03-19

## The Idea (In One Paragraph)

A RegTech company that provides AML, KYC, and compliance platforms to financial institutions was stuck on legacy on-prem infrastructure that couldn't scale, cost too much to maintain, and lacked disaster recovery. The pitch, stripped of consulting language: "We migrate RegTech platforms to AWS so they can scale with their growing customer base, hit 99.99% availability, cut infrastructure costs 30-40%, and meet financial compliance requirements out of the box." In startup terms, this would be a managed cloud migration and operations platform purpose-built for regulated financial software vendors.

## Forcing Questions Assessment

### Q1: Demand Reality

**Moderate signal, but generic.** There is a real, named customer category -- a RegTech solutions provider serving financial institutions -- and the case study describes concrete business pain: infrastructure costs rising, provisioning cycles too slow, no disaster recovery, availability at only 90%. These are real constraints that directly impacted revenue (inability to onboard new financial institution clients). The customer clearly paid for this work. However, the demand evidence is for "cloud migration consulting" broadly, not for a differentiated product. Any competent AWS partner could have pitched this engagement. The customer would not be upset if *this specific vendor* disappeared -- they'd be upset if *their AWS environment* disappeared, which is a different thing entirely.

### Q2: Status Quo

**Clearly described.** The customer was running everything on-premises with manual provisioning cycles, no infrastructure-as-code, 90% availability (which is terrible for financial services -- that's over 36 days of downtime per year), and no disaster recovery. They were using legacy monitoring (likely manual checks or basic tools before Nagios was introduced). The status quo was painful and expensive. But the status quo solution is also well-known: hire an AWS partner, migrate to the cloud. This is not an unsolved problem. It's a well-understood problem with a well-understood playbook. The customer was solving it badly by simply not having migrated yet.

### Q3: Desperate Specificity

**Weak.** The case study never names the customer. It never names a specific person at the customer. We get "a RegTech solutions provider" -- which is a category, not a human. Who at this company was in pain? The VP of Engineering who couldn't ship features because provisioning took weeks? The CTO who was losing deals because they couldn't promise 99.9% uptime to bank prospects? The compliance officer who couldn't sleep because there was no DR plan and regulators were asking questions? Any of these would be compelling. We get none of them. The case study reads like it was written for a marketing page, not from deep understanding of a specific person's suffering.

### Q4: Narrowest Wedge

**Possible but not explored.** The narrowest wedge here might be something like: "Terraform templates + AWS architecture blueprints pre-configured for RegTech compliance requirements (BSA, AML)." A startup could sell a RegTech-specific cloud landing zone -- a pre-built, compliance-ready AWS environment that a RegTech vendor could deploy in days instead of months. That's narrow, specific, and potentially valuable. But the case study doesn't describe building anything like a reusable product. It describes a bespoke migration engagement. The Terraform templates were built for this one customer. Nothing suggests they were designed for reuse.

### Q5: Observation & Surprise

**Nothing.** This is the biggest red flag. The case study reads like a textbook AWS migration: assess current state, design target architecture, provision with Terraform, set up monitoring, configure DR. Everything went "as expected." No pivots. No user feedback. No moment where the team discovered something unexpected about how RegTech platforms behave in the cloud, or how compliance requirements create unusual architectural constraints. The absence of surprise suggests this was execution, not discovery. Pure spec-driven delivery.

### Q6: Future-Fit

**Mixed.** On one hand, regulatory compliance in financial services is only getting stricter, and cloud adoption in regulated industries is still early. More RegTech companies will need to migrate. On the other hand, AWS itself is aggressively building compliance-ready services and landing zones. AWS Control Tower, AWS Config conformance packs for financial services, and the growing ecosystem of cloud compliance tools all commoditize what this engagement delivered. Three years from now, migrating a RegTech platform to AWS will be easier, not harder -- which means the value of the consulting engagement shrinks, not grows. The trend favors the platform vendor, not the integrator.

## The Paul Graham Test

### Schlep Blindness

**Some schlep, but not enough.** Cloud migration for regulated industries is genuinely tedious. Dealing with financial compliance requirements, data residency, encryption mandates, audit trails -- this is unsexy work that most developers don't want to do. That's a mild point in its favor. But this is also one of the most crowded segments in cloud consulting. Hundreds of AWS partners do exactly this. The schlep isn't avoided -- it's a well-staffed industry. Real schlep blindness would be something like: building the tooling that automates the compliance-specific parts of migration so you don't need a 6-month engagement every time. That tool doesn't seem to exist here.

### Do Things That Don't Scale

**Yes, by default -- it's consulting.** Every consulting engagement is "doing things that don't scale." The question is whether the unscalable work revealed a scalable product. Did the team build Terraform modules that could become a product? Did they discover compliance configuration patterns that repeat across every RegTech migration? Did they create monitoring templates specific to AML/KYC workloads? The case study gives no indication that any of this happened. The hands-on work appears to have taught them how to do this one migration, not how to build a product that does many migrations.

### Default Alive or Default Dead

**Default dead.** If you extracted this as a startup today, you'd have a cloud migration consulting firm competing with Accenture, Deloitte, Slalom, and hundreds of AWS Advanced Partners. Your revenue comes from one engagement at a time. You need to sell each project individually. There's no recurring revenue, no product leverage, no network effect. You'd need to either (a) build software that automates the migration, or (b) find a niche so specific that the big firms can't be bothered. Neither is evident here.

### Frighteningly Ambitious

**Not at all.** Migrating a RegTech company to AWS is important work, but it's not the kind of idea that makes you think "can they really do that?" It's the kind of idea that makes you think "yes, and so can 200 other firms." There's no vision here for transforming how RegTech companies operate, no platform play, no AI-driven automation of compliance infrastructure. It's a well-executed migration. That's valuable to the customer. It's not a startup.

### Earnest Test

**Moderate.** The team clearly understands AWS well and made sensible architectural choices (multi-AZ, Terraform, proper security controls). The choice of Nagios for monitoring alongside CloudWatch suggests pragmatism -- they picked tools that work rather than chasing the latest trend. But there's no evidence of deep RegTech domain expertise. The compliance mentions (BSA, AML laws) are surface-level. An earnest founder in this space would be talking about specific regulatory reporting requirements, specific data lineage challenges, specific audit scenarios that break standard cloud architectures. We don't see that depth.

## Startup Quality

### Market

**Size**: Cloud migration for financial services is a large market (tens of billions globally). But "large market" is not a startup advantage when you're a services firm competing on execution. The RegTech sub-segment is more interesting but still dominated by large consultancies.

**Timing**: The timing argument ("RegTech companies are migrating to cloud") is real but not urgent. This migration could have happened 3 years ago or 3 years from now. There's no forcing function that makes *right now* uniquely important. No new regulation, no platform shift, no technology inflection.

**Competition**: Extremely crowded. Every major AWS partner offers this. AWS itself offers migration assistance programs. The competitive advantage described in this case study is "we did it well," which is necessary but not sufficient for a startup.

### Product

**Defensibility**: Near zero. Terraform templates for AWS migration are not defensible. The architecture patterns described (multi-AZ, ALB, auto-scaling, CloudWatch) are AWS best practices documented in AWS Well-Architected Framework. Any competent team with AWS certifications could replicate this.

**Scalability**: No path to self-serve. Every engagement requires a team of cloud engineers doing custom work. The Terraform modules could theoretically become a product, but that's a massive leap from what's described. There's no evidence of productization.

**Technical depth**: Low. The technical work described -- Terraform provisioning, CloudWatch monitoring, Nagios setup, multi-AZ DR -- is standard AWS infrastructure work. There's no proprietary algorithm, no novel architecture, no technical innovation that would be hard to replicate.

### Team Signal

The team appears competent at AWS infrastructure and follows best practices. The choice of Terraform for IaC and the security controls implemented suggest professional-grade execution. However, there's no evidence of creative problem-solving or non-obvious discovery. The engagement followed a standard migration playbook. Nothing in the case study suggests the team has unique insight into RegTech that competitors lack.

## Wild Card -- "But What If?"

### The Contrarian Question

**What if the boring, compliance-heavy nature of RegTech cloud infrastructure is actually a moat?**

The obvious objection is: "This is just cloud migration consulting -- anyone can do it." But what if the intersection of *RegTech domain expertise* and *cloud infrastructure automation* is actually underserved? Big cloud consultancies don't specialize deeply enough in RegTech to build reusable compliance blueprints. RegTech companies themselves don't have the cloud expertise to do it alone. And AWS's generic compliance tools don't understand the specific requirements of AML/KYC platforms.

If someone built a *product* -- not a consulting engagement -- that was a compliance-ready cloud platform specifically for RegTech vendors (pre-configured audit logging for BSA requirements, data residency controls for different jurisdictions, monitoring dashboards tuned for AML transaction processing patterns), that could be a real wedge. The schlep of understanding both financial compliance *and* cloud architecture is real, and most teams only have one of those skills.

### The Crazy Upside Scenario

If everything breaks right: A team does 10-15 of these RegTech migrations, extracts the common patterns into a platform, and builds "Heroku for RegTech" -- a compliance-ready cloud platform where RegTech vendors can deploy their applications without worrying about infrastructure, compliance, DR, or monitoring. Financial regulators start requiring cloud-based RegTech platforms to meet specific infrastructure standards (as is already happening in some jurisdictions). This platform becomes the default way RegTech vendors deploy. The platform collects operational data across all its customers, uses it to improve reliability and compliance automation, creating a data network effect. You become the infrastructure layer that the entire RegTech industry runs on.

That's genuinely interesting. It's also about five major pivots away from what this case study describes.

### Risk Worth Taking?

**Faint pulse.** There's a scenario where deep specialization in RegTech cloud infrastructure becomes a platform play, but it requires: (1) building a product out of consulting patterns, (2) multiple customers to validate the patterns are general, (3) a team with both deep financial compliance expertise and cloud platform engineering skills, and (4) timing a market where RegTech vendors are actively seeking this. The case study provides evidence of (3) at a basic level and nothing else. The gap between "we migrated one RegTech company to AWS" and "we're the platform for RegTech cloud infrastructure" is enormous.

## Verdict

**Startup Viability Score**: 2/10

**One-Line Verdict**: "This is a well-executed AWS migration -- it's a project, not a product."

**What Would PG Say**: "You did good work for this customer, but I don't see what you learned that nobody else knows. If I asked you 'what's the non-obvious thing about running RegTech platforms in the cloud?' and you couldn't immediately tell me something surprising, then you don't have a startup yet. You have a consulting practice."

**The Assignment**: Go talk to 10 CTOs at RegTech companies that have already migrated to the cloud. Don't pitch them anything. Ask them: "What broke that you didn't expect? What compliance requirement turned into an infrastructure nightmare? What do you wish existed that doesn't?" If five of them describe the same unexpected pain point, you might have a product. If they all describe different problems, you have a consulting business.
