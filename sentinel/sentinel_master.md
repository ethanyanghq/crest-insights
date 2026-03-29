# Sentinel — Master Reference Document

### Intelligent SRE Response Copilot

_Updated post-CEO meeting · YC Summer 2026 · Deadline May 7, 2026_

---

> **What we build:** Sentinel is an agentic AI copilot that watches how your best SRE engineers respond to production incidents, structures that response pattern into a learnable format, and automatically surfaces a recommended response — grounded in your team's own historical resolutions — the next time a similar alert fires. Human approves every action. The system gets smarter with every incident.

> **One sentence:** _Sentinel is the AI copilot that surfaces how your best engineer would respond to this alert — before they have to be woken up at 2am._

---

## PART 0 — WHAT CHANGED AFTER THE CEO MEETING

This is important context for the full team before reading anything else.

We met with the Crest Data CEO. Here is what he validated and what it changed:

**What he was excited about:**

- Layer 2 automation — responding to alerts with AI-generated recommendations, human in the loop
- Keeping a record of responses via runbook automation, storing that as institutional memory that feeds future recommendations and compounds over time
- Analyzing existing runbooks, Slack history, and Jira/Confluence when first installed — to avoid a cold start problem
- The Slack interface as the primary delivery surface
- RAG-based agentic response generation specifically for SRE-related alerts

**What he pushed us to sharpen:**

- Be more specific about where exactly in the SRE hierarchy we sit
- Nail down our ICP (Ideal Customer Profile) — size, type, specific team
- Are we ITSM or CSM? (explained below — this matters)
- Don't try to do everything the Netskope system does. Focus on 1–2 things and do them exceptionally well

**What this means for the product:**
The institutional memory angle is validated. The response recommendation angle is validated. The "analyst leaves" framing is dead — the daily operational pain is the sell. We are NOT building another triage tool. We are NOT claiming to autonomously remediate. We sit in a very specific, well-defined place in the SRE stack that nobody owns cleanly yet.

**Ongoing relationship:** Weekly meetings with the CEO and an SRE engineer from the team. This is extraordinary access. Use it to validate every product decision before building.

---

## PART 1 — THE SRE WORLD FROM SCRATCH

### What is SRE?

SRE stands for **Site Reliability Engineering**. It is a discipline invented by Google that treats operations — keeping software running reliably — as an engineering problem rather than an IT support problem. Traditional IT operations ("ops") was about firefighting. SRE is about engineering systems to be reliable and then responding intelligently when they are not.

An SRE team is the group responsible for making sure a company's software systems stay up, stay fast, and stay correct. When something breaks in production — meaning real users are affected — the SRE is the person who gets woken up at 2am to fix it.

**Simple version:** SRE = the team whose job is to make sure the product doesn't go down, and fix it fast when it does.

### What is a production incident?

A production incident is any event that degrades or breaks a service that real users depend on. It could be:

- The checkout page returning errors (lost revenue)
- The login API being slow (users churning)
- A security platform failing to process alerts (threats being missed)
- A database going down (data at risk)

Incidents are classified by severity. The standard terminology, which you need to know cold:

| Severity       | Industry Name             | Plain English                 | Example                                      |
| -------------- | ------------------------- | ----------------------------- | -------------------------------------------- |
| **SEV-0 / P0** | Critical / Major Incident | Everything is on fire         | Site completely down, all users affected     |
| **SEV-1 / P1** | High                      | Something important is broken | Payment processing failing for 30% of users  |
| **SEV-2 / P2** | Medium                    | Degraded experience           | Some API endpoints slow, some users affected |
| **SEV-3 / P3** | Low                       | Minor issue                   | Non-critical feature broken, no user impact  |

Every company uses this hierarchy slightly differently, but the structure is universal.

### What is an alert? What is an event?

These two words are often confused. Understanding the difference is foundational to understanding what Sentinel does.

**An event** is any data point that a monitoring system records. "CPU usage was 72% at 3:14pm" is an event. "200 HTTP requests were processed in the last minute" is an event. Events are constant, voluminous, and mostly meaningless on their own. A large system generates millions of events per day.

**An alert** is an event (or combination of events) that crossed a threshold and triggered a notification to a human. "CPU usage exceeded 90% for 5 consecutive minutes" — that triggers an alert. An alert is the monitoring system saying: _something crossed the line you told me to watch._ Alerts are a filtered subset of events.

**The critical distinction:** An alert tells you _something is wrong_. It does not tell you _why_, _how serious_, or _what to do_. Figuring out those three things is the work of incident response — and that work is what Sentinel assists.

**Why there are 10,000+ alerts per day at companies like Netskope:**

From the Netskope case study (real, in combined.md): 10,000+ daily alerts across 100+ locations. This number shocks people. Here is exactly why it gets that high:

1. **Distributed systems cascade.** In a microservices architecture — where a company's software is broken into dozens or hundreds of small services that talk to each other — one failing component generates alerts from every service that depends on it. One database goes down → alerts from 40 services that use that database. One root cause → 40+ alerts in seconds.

2. **Multiple monitoring tools fire independently.** The Netskope case says security data was "siloed across the customer, Okta, CrowdStrike, and other platforms." CrowdStrike fires its own alert. Okta fires its own alert. The SIEM fires its own alert. All for the same underlying event. Without a correlation layer, you get N alerts from N tools for one actual problem.

3. **Teams set conservative thresholds.** Missing a real incident costs too much — customer outage, SLA breach, regulatory fine. So teams alert at 80% CPU utilization rather than 95%, alert at 2% error rate rather than 10%. Normal operational variance constantly crosses these thresholds and fires false positives.

4. **The cry wolf effect compounds.** The Mission Control Plugins case study states this directly: _"more than half of respondents reported a rate of 50% or higher of false-positive alerts, leading to spending the majority of SOC's time trying to analyze the high volume."_ When most alerts are false positives, analysts learn to filter mentally. The signal-to-noise ratio collapses. The one real incident gets buried.

**The result:** SRE and SOC teams are not reading 10,000 alerts. They are triaging at a glance, manually correlating, ignoring most, investigating some, and inevitably missing others.

### The vocabulary you need to know cold

These are the terms that come up in every conversation about this space. Know them before you talk to any customer or investor.

**MTTR — Mean Time To Resolution.** The average time from when an incident is first detected until it is fully resolved. This is the single most important metric in incident response. Reducing MTTR is the primary value proposition of almost every tool in this space. The SRE chat case study gave a 40% MTTR reduction. Keep that number.

**MTTD — Mean Time To Detect.** How long from when a problem starts until an alert fires. Separate from MTTR because detection and resolution are different problems. The XDR case showed 70–80% faster incident detection — that is MTTD improvement.

**MTTA — Mean Time To Acknowledge.** How long from alert firing until an engineer looks at it. High MTTA usually signals alert fatigue — too many alerts, engineers have learned to hesitate.

**Toil.** Defined by Google's SRE book as manual, repetitive, automatable work that scales linearly with system growth. Tool-switching during incident investigation is toil. Manually writing postmortems is toil. Looking up the same runbook for the 30th time is toil. Eliminating toil is what SRE AI tools sell.

**Runbook.** A documented procedure for handling a specific type of incident. Think of it as the step-by-step guide: "When alert X fires, do steps 1, 2, 3." The problem with runbooks: _they go stale immediately._ Modern software deploys 10–100 times a day. The runbook written six months ago reflects a system that no longer exists. _"Runbooks are procedural artifacts frozen in time. They document what worked yesterday, codified by someone who understood a specific failure mode in a specific context."_ This is why Sentinel's dynamic, history-based recommendations are more valuable than a static runbook.

**Playbook.** Similar to a runbook but higher-level — more about process (who to call, when to escalate) than specific technical steps. A runbook might say "run kubectl rollout undo"; a playbook might say "if P1, notify the incident commander and open a war room."

**Postmortem / RCA.** A postmortem (also called a Root Cause Analysis or RCA) is the document written after an incident that explains: what happened, why it happened, what was done to fix it, and how to prevent it from happening again. Postmortems are enormously valuable — and almost universally skipped or done poorly because nobody wants to spend an hour writing documentation after the adrenaline of an incident fades.

**On-call.** A rotation system where specific engineers are designated as the first responder for incidents during a given time period. Being "on-call" means your phone might ring at 3am with a production incident. On-call burnout is one of the most cited reasons engineers leave companies.

**Alert fatigue.** When engineers receive so many alerts that they start ignoring them. This is a real psychological phenomenon, not just a process problem. A 2025 Catchpoint study found that nearly 70% of SREs report on-call stress contributing to burnout and attrition.

**PagerDuty.** The dominant alert routing platform. When a monitoring tool (Datadog, Prometheus) fires an alert, PagerDuty routes it to the correct on-call engineer via phone call, SMS, and Slack. "Getting paged" means receiving a PagerDuty notification. This is the first moment in the incident response workflow.

**SOAR — Security Orchestration, Automation and Response.** A category of security tools (IBM QRadar SOAR, Google SecOps SOAR, Splunk SOAR) that execute predefined automated playbooks in response to security events. SOAR is the security-specific automation layer. Crest has built integrations into multiple SOAR platforms.

**SIEM — Security Information and Event Management.** The tool that aggregates security logs from everywhere — endpoints, network, cloud — and provides search, alerting, and correlation. Google SecOps (Chronicle), IBM QRadar, Splunk are SIEMs. The SIEM is where security events are stored and searched.

**ITSM vs CSM — the question the CEO asked.**

This is a critical distinction. Let's define both clearly.

**ITSM — IT Service Management.** The process of managing IT services for a business. Think ServiceNow, Jira Service Management. ITSM is about managing IT as a service: ticket creation, SLA tracking, change management, problem management. The "customer" in ITSM is the internal business user asking IT for help. ITSM is more process-oriented and focuses on structured workflows, approvals, and compliance documentation. A mature ITSM implementation has formal change advisory boards, configuration management databases (CMDB), and audit trails.

**CSM — Customer Service Management / AIOps.** More specifically for our context, AIOps is the category: AI for IT Operations. This is about using AI/ML to manage infrastructure, detect anomalies, correlate events, and suggest or automate responses. It is less about process and more about operational intelligence.

**Where Sentinel sits:** We are **not** ITSM. We are not building ServiceNow workflows or compliance ticket processes. We are **AIOps** — specifically, we are in the incident response automation and intelligence layer. Our buyer is the Head of SRE or VP Engineering, not the IT Service Desk manager. Our language is MTTR and on-call toil, not ticket SLAs and change approval boards. This distinction matters in customer conversations.

### The SRE Hierarchy — Where Sentinel Fits

This is the full event management hierarchy from data collection to human response. Understanding this hierarchy is how you talk intelligently about where you sit.

```
Layer 1: Infrastructure & Applications
├── Servers, Kubernetes clusters, databases, microservices
└── These generate metrics, logs, and traces continuously

Layer 2: Observability / Monitoring
├── Prometheus, Datadog, New Relic, Grafana, CloudWatch
└── These collect telemetry and fire ALERTS when thresholds are crossed

Layer 3: Alert Routing & On-Call Management
├── PagerDuty, Opsgenie (being sunset), incident.io
└── These route alerts to the right on-call engineer and manage escalation

Layer 4: Event Correlation & SIEM (security-specific)
├── Splunk, Google SecOps/Chronicle, IBM QRadar
└── These aggregate events from many sources and correlate across them

Layer 5: SOAR / Automation (security-specific)
├── IBM QRadar SOAR, Google SecOps SOAR, Splunk SOAR
└── These execute predefined playbooks automatically when rules trigger

Layer 6: ★ SENTINEL LIVES HERE ★
├── Response Intelligence & Recommendation
└── Takes the incoming alert + all context, matches it to historical responses,
    and delivers a structured recommendation to the engineer

Layer 7: Human Analyst / On-Call Engineer
├── Receives the alert + Sentinel's briefing in Slack
└── Reviews recommendation, approves, modifies, or escalates
    → Whatever they do is captured back into Sentinel's knowledge base

Layer 8: Documentation & Postmortem
├── Jira, Confluence, ServiceNow, Notion
└── What was done gets recorded (manually today, automatically with Sentinel)
```

**We sit at Layer 6.** We are not a monitoring tool (Layer 2). We are not an alert router (Layer 3). We are not a SIEM (Layer 4). We are not a SOAR replacing predefined playbooks (Layer 5). We are the intelligence and memory layer between the alert arriving and the human responding.

The gap at Layer 6 is real. Tools at Layers 2–5 are mature and crowded. Tools that help the human at Layer 7 respond smarter, faster, and with institutional context — that is underserved. The research confirms this: every AI SRE tool in 2026 is converging on autonomous remediation from Layer 5 downward. Nobody has made the human decision support layer (Layer 6) their primary identity.

---

## PART 2 — WHAT TEAMS ACTUALLY DO WHEN AN ALERT FIRES

### The complete step-by-step of a real incident

This is not hypothetical. This is what actually happens, based on real SRE incident reports and the Crest case studies.

**Step 1 — The page fires.** PagerDuty sends a phone call, SMS, and Slack message simultaneously. If the on-call engineer does not acknowledge within 5–15 minutes, it escalates to the secondary. The engineer has been asleep. They are now awake, adrenaline spiking, reading: "P99 latency on checkout-service exceeded 2,000ms."

**Step 2 — First question: is this real?** The experienced engineer immediately asks: did a deployment just go out? Is this the alert that fires every Tuesday morning and always resolves itself? Is this correlated with anything else? This context check — which the senior engineer does instinctively in 30 seconds — is what takes a junior engineer 20 minutes of frantic tool-switching to replicate.

**Step 3 — Open the tools.** The engineer opens multiple dashboards simultaneously. There is no single pane of glass. They check:

- Datadog or Grafana for the metric spike (which service, which region, when did it start)
- The deployment log (was there a deploy in the last 30 minutes?)
- Splunk or ELK for the actual error logs (what is the service printing?)
- Kubernetes dashboard for pod health (any OOMKills? CrashLoopBackOff?)
- The Confluence runbook for this alert type (if it exists and is not stale)
- Past Jira incidents for something that looked like this (if they remember one)
- Slack history to see if someone mentioned this service recently

**Every tool switch is lost time.** Research shows the gap between "alert fired" and "troubleshooting started" runs 10–15 minutes for most teams. That gap is pure logistics: manually creating the Slack channel, pinging the on-call engineer, finding who owns the affected service, opening the runbook, updating the status page. None of that is troubleshooting. All of it is coordination overhead.

**Step 4 — Form a hypothesis.** Based on accumulated context, the engineer makes an educated guess: "This looks like the cache saturation issue we had in March. Deployment was 47 minutes ago, the error pattern matches, the fraud service latency is elevated." This hypothesis formation is where the expertise lives. This is the step that takes a senior engineer 5 minutes and a junior engineer 40 minutes — because the senior engineer has seen this pattern before and the junior engineer hasn't.

**Step 5 — Take mitigation action.** Roll back the deployment. Restart the pod. Flush the cache. Scale up the node group. Add rate limiting. The action itself is usually simple once you know what it is. The hard part was getting to the hypothesis.

**Step 6 — Resolve and communicate.** Mark the incident resolved. Write a summary in the war room Slack channel. Update the status page. Notify stakeholders.

**Step 7 — Postmortem.** Supposed to be written within 24–48 hours. In practice, the most consistently skipped step in all of incident management. There is no time. There is no incentive. There is no system that makes it easy. The knowledge of what happened, why, and how it was fixed mostly evaporates.

**Step 8 — Runbook update.** Almost never happens. The runbook for this alert type now has one more use case documented in someone's head and nowhere else.

### What actually gets captured today — and what doesn't

| What gets captured today | Where                      | Quality                     |
| ------------------------ | -------------------------- | --------------------------- |
| The alert that fired     | PagerDuty, monitoring tool | Structured, reliable        |
| Who was on-call          | PagerDuty                  | Structured, reliable        |
| When it was resolved     | PagerDuty                  | Structured, reliable        |
| A ticket/incident record | Jira, ServiceNow           | Structured but sparse       |
| The postmortem           | Confluence, Notion         | Inconsistent, often skipped |
| The runbook (if written) | Confluence                 | Frequently stale            |

| What is NOT captured today                                                  | Reality                          |
| --------------------------------------------------------------------------- | -------------------------------- |
| Which tools the engineer opened first                                       | Lives in their head              |
| Which query revealed the key insight                                        | Executed in their terminal, gone |
| Why they ruled out hypothesis A before hypothesis B                         | Pure experience                  |
| That this specific alert at this company always resolves with a cache flush | Tribal knowledge                 |
| That the last 8 times this happened, a deploy was the cause                 | Memory of whoever was on-call    |
| What questions they asked in Slack before taking action                     | Lost in Slack history            |

**This is exactly what Sentinel captures.** The structured reasoning pattern behind the response — not just what was done, but the logic of how the engineer arrived at the decision.

---

## PART 3 — THE PROBLEM STATEMENT (REWRITTEN)

### The old problem statement (retired)

~~"Analysts leave and take institutional knowledge with them."~~

This is a real problem. It is not the selling problem. It happens once a year. Nobody wakes up panicked about it today.

### The new problem statement (the daily pain)

**SRE teams are responding to the same incidents over and over, starting from scratch every single time.**

When an alert fires, a human engineer has to:

1. Figure out if it is real
2. Gather context from 5–8 disconnected tools
3. Recall whether they have seen this before
4. Form a hypothesis
5. Take action
6. Document what happened

The knowledge that makes steps 2–5 fast is tribal. It lives in the heads of senior engineers who have been on-call for two years. It is never written down in a form that can be retrieved when the next similar alert fires at 3am with a different engineer on-call.

The runbooks that are supposed to solve this problem are obsolete. Modern software deploys 10–100 times a day. _"Runbooks become obsolete very, very quickly. And unlike code that is self-documenting, when a change happens to the production system, the runbook does not get updated automatically."_ (Spiros Xanthos, Resolve AI CEO, Stack Overflow)

**The result:**

- P99 incidents take 4–6 hours when a senior engineer could resolve them in 20 minutes
- Junior engineers on the 2am rotation are flying blind
- 43% of organizations reported that operational toil _increased_ in 2025 despite widespread tool adoption (2025 SRE Report)
- Alert fatigue has driven nearly 70% of SREs to report on-call stress contributing to burnout

**The turnover argument is now the natural consequence:**
And when that senior engineer does leave — which happens 28% annually — the accumulated response knowledge leaves with them. The new hire starts from zero. This is earned, not the primary pitch.

---

## PART 4 — WHAT SENTINEL DOES (PRECISE PRODUCT DEFINITION)

### The four-element architecture — simplified

The CEO validated this model. The Netskope system had five agents. We focus on the four elements that we can do well and that create the core value loop. Here they are in plain English first, then with technical depth.

---

**Element 1: CAPTURE — How does Sentinel know what happened?**

When an SRE resolves an incident, Sentinel captures the structured response record. This is NOT screen recording. Screen recording is invasive, produces unstructured video, and security teams will reject it immediately.

What Sentinel actually captures:

_Source A — Retrospective ingestion (zero friction, day one)._ When first installed, Sentinel ingests existing Jira tickets, Confluence postmortems, ServiceNow incident records, and Slack channel history from past incidents. The SASE unicorn SRE chat case study proves this works — the system was bootstrapped from existing Jira + Confluence data and was useful immediately. This solves the cold start problem. Your first customer does not need to generate new data — they have years of it already.

_Source B — The Slack prompt (15 seconds, minimal friction)._ When PagerDuty marks an incident resolved, Sentinel's Slack bot sends one message: "Incident resolved. In one sentence: what was the root cause and fix?" One field. One sentence. This is the richest signal per unit of friction available. The engineer is already in Slack. They already marked the incident resolved. The prompt arrives at the moment of maximum recall. That single sentence, structured by alert type, service, and severity, is enormously valuable training data.

_Source C — SOAR/ITSM integration (structured, automatic)._ If the team uses ServiceNow, IBM QRadar SOAR, Jira, or Google SecOps SOAR, every closed incident has structured fields: alert type, severity, assets involved, actions taken, resolution type, time to resolution. Sentinel reads these automatically via API. The Endpoint Protection + ServiceNow integration case study shows Crest has already built this exact pipeline. No additional work required by the engineer.

**What Sentinel does NOT do in the capture layer:**

- Screen record
- Keylog commands
- Track browser history
- Monitor terminal sessions

**Why trust is solved:** Engineers are suspicious of surveillance tools. Sentinel is not one. It captures the resolution record, not the investigation process. The capture mechanism is transparent: "When you mark an incident resolved, we ask you one question and read your existing ticket data." That is it.

---

**Element 2: STRUCTURE — Turning raw incident data into something learnable**

A Jira ticket says "fixed the cache issue on checkout." A Slack message says "rolled back the 3pm deploy, that was it." These are useful but not queryable for similarity.

Sentinel's structure layer takes raw incident data and produces a standardized incident record with these fields:

```
Alert signature: {type: "high_latency", service: "checkout-service", threshold_breached: "P99 > 2000ms"}
Environment context: {cloud: "AWS", region: "us-east-1", kubernetes_version: "1.28", recent_deploys: true}
Investigation sequence: [check_deploy_log, check_cache_metrics, check_error_logs]
Hypothesis: "Cache saturation following 3pm deploy"
Action taken: "Rollback to version 2.2.3"
Resolution type: "Rollback"
TTR: 18 minutes
Confidence: High (engineer confirmed root cause)
Free text reasoning: "Deploy introduced a query that bypassed Redis, saturating the DB connection pool"
```

Each field cluster gets embedded separately into a vector database (Pinecone, Weaviate, or ChromaDB — the SRE chat case study used ChromaDB, the IT Helpdesk case used Pinecone). Chunking by attribute rather than embedding the whole document as one blob is what makes retrieval precise rather than fuzzy. You can ask "find me alerts matching this service and this symptom" and get the right thing, not just vaguely similar documents.

**The Google SecOps GOLD Parser case is the proof point here.** Crest built Google Chronicle's own UDM (Unified Data Model) normalization standard — the format that every security log source gets translated into before Chronicle can reason about it. They did this for 150+ log source types across 150+ customers. The hardest part of structure is normalization: taking heterogeneous, inconsistent data from Datadog, Splunk, ServiceNow, and Slack and mapping it to a clean unified schema. Crest has done this at production scale repeatedly. That is the engineering head start.

---

**Element 3: IDENTIFY — Matching the new alert to the right historical responses**

This is where Sentinel becomes an agent system rather than a simple RAG (Retrieval Augmented Generation) search engine.

When a new alert fires, the naive approach is: run a vector similarity search against the knowledge base, return the top three results, done. That is a RAG lookup. That is not what makes this valuable.

What makes this an agent system:

The identification layer runs multiple queries simultaneously against different attribute clusters: alert type similarity, service similarity, symptom similarity, temporal patterns (does this always happen after a deploy?), environment similarity. It then applies a second reasoning pass: of the candidate matches, which ones are actually relevant to this specific situation, and why?

The output is not "here are similar incidents." The output is:

```
MATCH 1 (confidence: HIGH — 8 similar past incidents)
Alert type: identical. Service: identical. Symptom: identical.
This team has resolved this pattern 8 times. 7 of 8 resolutions were deployment rollbacks.
Median TTR: 15 minutes.

MATCH 2 (confidence: MEDIUM — different service, same error signature)
Payment-service had the same P99 spike on Jan 7. Root cause: DB connection pool exhaustion.
Different service but same error signature. Worth checking DB pool metrics.

Recommended first steps for this environment:
1. Check deployment log — any push in last 45 minutes on checkout-service?
2. Run: kubectl rollout history checkout-service
3. Check Redis cache hit rate in Datadog (filter: last 15 min)
```

This is LangGraph multi-step reasoning, not a Pinecone query. The Netskope case uses LangGraph + AWS Bedrock + Anthropic Claude as the orchestration stack. That is our blueprint. Crest has this in production. We are not inventing a new architecture.

**The trust mechanism — this is how we are not a black box:**

Sentinel does not say "do this." It says "based on these specific past incidents, your team has typically done this." The engineer can see the evidence. They can click through to the matching past incidents. The reasoning is transparent. This is not the AI making a security decision — this is the AI surfacing your team's own historical decisions, assembled and presented clearly.

_"We can hide behind RAG — we aren't generating new solutions, we are assembling a new one based on old ones and adequately presenting that to the team."_ — This is exactly right, and it is the trust architecture. Every recommendation is sourced from the team's own resolutions. The AI is the retrieval and assembly mechanism. The humans are the source of truth.

---

**Element 4: FEEDBACK — The flywheel that makes it compound**

Every interaction with a Sentinel recommendation is training data.

| Engineer action                            | Signal to Sentinel                                                      | What it means                                        |
| ------------------------------------------ | ----------------------------------------------------------------------- | ---------------------------------------------------- |
| **Approves unchanged**                     | Strong positive — recommendation was accurate                           | Similarity match was correct                         |
| **Modifies then approves**                 | Rich signal — the diff shows where the knowledge gap was                | More detailed future recommendation for this pattern |
| **Escalates without using recommendation** | Negative signal — this alert type is more complex than the model thinks | Reduce confidence score for similar future matches   |
| **Ignores recommendation entirely**        | Strong negative                                                         | Wrong match — adjust similarity weights              |

After 6 months: Sentinel knows every alert type this team has resolved and what works.
After 12 months: It knows which alerts are always false positives at this company.
After 18 months: It is the single most valuable institutional knowledge asset the engineering team has.

**This is the flywheel. This is the moat. This is why switching costs compound over time.**

The runback automation the CEO mentioned is this: after every incident, Sentinel generates a structured runback — a summary of what happened, what was recommended, what the engineer actually did, and what the outcome was. This runback is stored and becomes part of the knowledge base. The runback IS the institutional memory being written in real time, automatically, without anyone having to write a postmortem.

---

## PART 5 — WHERE WE SIT IN THE MARKET (THE DIFFERENTIATION MAP)

### What is already built and crowded

The research reveals the AI SRE market has exploded in 2025–2026. Here is the honest map:

**Autonomous AI SRE (fully automated investigation and remediation):**

- Resolve AI, incident.io AI SRE, AutonomOps/HealR, Azure SRE Agent (Microsoft)
- These connect to all your tools, investigate autonomously, and can execute remediations with human approval
- Well-funded, growing fast, enterprise-grade
- Their identity: autonomous first responder that handles alerts without human initiation

**Incident management + AI triage:**

- Rootly, PagerDuty AI, FireHydrant, ilert
- Primarily incident coordination platforms (who's on call, war room, status page) that have added AI features
- Their identity: incident management workflow with AI as a feature, not the core

**Observability + AI layer:**

- Datadog Bits AI, Grafana, New Relic AI, Observe
- These own the data collection layer and are building AI on top of their existing telemetry
- Their identity: observability platforms with AI summaries and root cause suggestions

**Security-specific SOC triage:**

- Dropzone AI, Radiant Security, Simbian, Prophet Security, Intezer
- AI that triages security alerts specifically (malware, IOC, lateral movement)
- Their identity: autonomous SOC analysts replacing human tier-1/tier-2 security work

### Where everyone is weak — the real gap

Here is what the research confirms about what is missing across all these tools:

Most AI SRE products are thin layers on top of observability platforms. They point an LLM at observability data and try to explain what broke and why. That doesn't work. The hard part of incidents is figuring out whether the problem was a bad configuration, a noisy neighbor, a control plane deadlock, or a subtle storage regression. Answering that requires investigation, not just a runbook.

Traditional runbooks are procedural artifacts frozen in time. Modern software systems are very dynamic and change very frequently, sometimes 10–100 times a day. Runbooks become obsolete very quickly. Unlike code that is self-documenting, when a change happens to the production system, the runbook does not get updated automatically.

Most organizations lack large, consistently labeled incident datasets. Runbooks, tickets, chat threads, and postmortems often exist but are unstructured. This limits supervised learning and requires heavy use of embeddings, retrieval, or heuristic patterning to compensate.

**The specific gap Sentinel fills:**

None of the autonomous AI SRE tools are built around _your organization's own historical response patterns._ They use general observability data and generic runbooks. They are smart about what broke. They are not smart about what _your specific team_ does when this specific alert fires at _your company._

An effective AI SRE copilot has a grounded prompt with: "Users are reporting checkout failures. The payment service had a deployment 47 minutes ago. The payment service depends on the fraud service, which has shown elevated latency for the past 50 minutes. A similar incident occurred on 2025-03-15 with error code PAYMENT_TIMEOUT, where the root cause was cache saturation in the fraud service." — The copilot automates the retrieval of tribal knowledge that would otherwise vanish as people rotate off the team.

That "similar incident occurred" piece — where the system knows your specific historical incidents and surfaces them in context — is what Sentinel specializes in. Resolve AI, incident.io, and Azure SRE Agent all mention this capability. None have made it their primary identity. It is a feature in a larger platform for all of them. For Sentinel, it is the entire product.

**The naming convention:** What Sentinel builds is specifically called **Incident Similarity Matching** + **Knowledge Graph Construction** in the AIOps literature. Incident Similarity Matching uses embeddings to retrieve past SEVs, tickets, and postmortems that match current failure signatures. Knowledge Graph Construction converts incident artifacts into a graph of services, dependencies, owners, and historical outcomes so the system can learn over time. These are recognized capabilities in the AI SRE maturity model. They are not novel. They are underbuilt for the specific segment we target (explained in Part 6).

### The competitive matrix — where Sentinel wins

| Capability                                              | Rootly  | incident.io AI | Resolve AI | Azure SRE Agent | **Sentinel**             |
| ------------------------------------------------------- | ------- | -------------- | ---------- | --------------- | ------------------------ |
| Autonomous investigation                                | ✓       | ✓              | ✓          | ✓               | ✗ (human-in-loop always) |
| Your team's historical responses                        | Partial | Partial        | Partial    | Partial         | **✓ (primary)**          |
| Cold start from existing Jira/Slack                     | ✗       | ✗              | ✗          | ✗               | **✓**                    |
| Runback automation + memory storage                     | ✗       | ✗              | ✗          | Partial         | **✓**                    |
| Compounding flywheel from approvals/modifications       | ✗       | ✗              | ✗          | ✗               | **✓**                    |
| Crest Data integration depth                            | ✗       | ✗              | ✗          | ✗               | **✓**                    |
| Designed for mid-market SRE teams                       | ✗       | Partial        | ✗          | ✗               | **✓**                    |
| Requires enterprise contracts / existing infrastructure | ✓       | ✓              | ✓          | ✓ (Azure only)  | **✗**                    |

**The one-sentence positioning against each competitor:**

- vs. Rootly: "Rootly manages incident workflows. We surface how your team has resolved this specific alert before."
- vs. incident.io AI: "incident.io investigates autonomously. We recommend based on your team's own history, with full transparency into why."
- vs. Resolve AI: "Resolve uses observability data to explain what broke. We use your incident history to recommend what works at your company."
- vs. Azure SRE Agent: "Azure SRE Agent requires Azure infrastructure and generic runbooks. We work with any stack and learn from your specific team."

---

## PART 6 — IDEAL CUSTOMER PROFILE (ICP)

### Who we are NOT building for

**Not a 3-person startup:** No historical incident data to bootstrap from. No budget. No dedicated on-call rotation. No product-market fit for SRE tooling.

**Not a 10,000-person enterprise:** They have dedicated AIOps and platform engineering teams. 18-month procurement cycles. They are already buying Resolve AI or building internally. Azure SRE Agent is free for their Azure infrastructure.

### The sweet spot

**Primary ICP: Series B–D software companies with 50–500 engineers**

The specific profile:

| Characteristic                                        | Why it matters for Sentinel                                                                                                      |
| ----------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------- |
| **50–500 total engineers**                            | Enough incidents to generate valuable training data. Not so large they have dedicated AIOps teams.                               |
| **5–25 SREs or on-call engineers**                    | This is the team that feels the alert fatigue acutely and personally. The budget owner is in this group.                         |
| **Microservices on Kubernetes, multi-cloud**          | Alert volume is exponentially higher than monolithic apps. The cascade problem is severe. Each service generates its own alerts. |
| **Running PagerDuty + Datadog/Splunk**                | Already paying for the tools Sentinel connects to. No new stack required.                                                        |
| **No dedicated AIOps or SecOps automation team**      | Has not solved this internally. Will pay a vendor.                                                                               |
| **Paying customers with SLAs**                        | Downtime = lost revenue = urgency. SLA breach = financial penalty.                                                               |
| **2–5 "senior" engineers who hold all the knowledge** | The knowledge concentration is acute and the manager feels it.                                                                   |
| **High on-call burnout / engineers complaining**      | This is the symptom. The complaint is already there. Sentinel is the solution.                                                   |
| **1–3 years of Jira/Confluence/ServiceNow history**   | The existing data is there. Cold start is solved from day one.                                                                   |

**Vertical priorities based on Crest's customer evidence:**

1. **Security SaaS companies** (Netskope-type) — They manage both SRE and security operations. The Netskope multi-agentic system was built for this exact customer type. These companies have the highest alert volume AND the most at stake per missed incident. AND they already have Crest relationships.

2. **SASE/networking SaaS companies** — The SASE unicorn SRE chat case proved both the pain and the fix. 40% MTTR reduction. This company is a warm design partner lead.

3. **FinTech/RegTech** — Compliance mandates make incident documentation a regulatory requirement (ISO 27001, SOC 2). Sentinel's automatic runback generation is a compliance feature, not just an operational one. This is an additional sales angle that does not require convincing anyone the AI recommendations are good. The documentation alone is worth paying for.

4. **High-growth B2B SaaS** — Any company that has scaled from 50→300 engineers in 2 years and whose SRE processes have not kept up. This is the segment where the "2am call because only Sarah knows how to fix this" problem is most acute.

**Who signs the check:**

- VP Engineering or Head of SRE at Series B–D: $5–15K/month approval without CFO involvement
- CTO at smaller companies who are still on-call themselves
- CISO for the security-specific version (larger budget, longer cycle, compliance angle dominates)

**Deal size:**

- Pilot/design partner: free or $500–1,000/month
- Mid-market SaaS (50–200 engineers): $2,000–8,000/month
- Larger mid-market (200–500 engineers): $8,000–20,000/month
- MSSP channel (one sale reaches 20–50 clients): $200–400K/year

---

## PART 7 — CASE STUDY EVIDENCE MAP

Each case study from Crest's portfolio is linked to a specific layer of Sentinel. These are not analogies. These are production deployments proving each component works.

---

### ⭐ Case Study 1: Netskope Multi-Agentic AI — The Full Blueprint

**Source:** "Leveraging High-Volume Alerts to Derive Actionable Insights with Multi-Agentic AI Solution"

**In plain English:** Netskope is a $3B+ cybersecurity company (Security Service Edge / Zero Trust). Their security operations center was handling 10,000+ daily alerts across 100+ locations. Security data was siloed across Netskope's own platform, Okta (identity management), CrowdStrike (endpoint security), and other tools. Analysts were understaffed, couldn't investigate everything, and were doing everything manually. Critical threats were being missed.

**What Crest built:** A five-agent AI system on AWS Bedrock + LangGraph + Anthropic Claude + Streamlit + Kubernetes:

- **Alert Triage Agent** — evaluates and prioritizes incoming alerts before a human sees them
- **Context Gathering Agent** — automatically collects relevant information across all connected security systems (Okta, CrowdStrike, Netskope's own platform)
- **Correlation Agent** — identifies relationships between events that look unrelated across different tools
- **Response Recommendation Agent** — suggests appropriate actions based on the full context gathered
- **Documentation Agent** — creates investigation reports and maintains records automatically

The agents don't operate independently. There is a "sophisticated coordination layer" and "reasoning engine to determine optimal investigation paths." Agents hand off structured state to each other. **Human-in-the-loop integration points exist for critical decisions.** That last sentence is important — even at this level of sophistication, the human approves consequential actions.

**What this proves for Sentinel:** This IS Sentinel. Not a prototype. Not a design document. Real code, running in production, handling 10,000+ alerts/day. When you talk to the CEO, you say: "Your team built this for Netskope. We want to productize it." The architecture is validated. The scale is validated. The human-in-loop approach is validated.

**What is missing from the case study:** No result metrics. The case study does not say "reduced analyst workload by X%" or "false positive rate dropped." This is your most important question for the CEO next week.

**Key technical stack:** AWS Bedrock, LangGraph, Anthropic Claude, Streamlit, Kubernetes — every one of these is accessible, well-documented, and not exotic. This is an engineering execution problem, not a research problem.

---

### ⭐ Case Study 2: SRE AI Chat App — The Memory Layer Proven

**Source:** "Enhancing SRE Operations for a Unicorn Security Startup with an AI-Powered Chat Application"

**In plain English:** A "unicorn" SASE company (Security Access Service Edge — think Zscaler/Netskope competitor) had an SRE team drowning in manual work during incidents. When an incident fired, engineers had to manually search through Jira tickets and Confluence documentation to find relevant past information. This took time they did not have. New SRE hires took weeks to ramp up because all the operational knowledge was in documents they could not easily find or query.

**What Crest built:** An AI-powered chat application delivered in Slack. Engineers type natural language: "What happened last time auth-service had high latency?" The system searches Jira tickets and Confluence documentation using RAG (Retrieval Augmented Generation) and returns a structured answer with links. Key components:

- LlamaIndex for the RAG pipeline
- ChromaDB as the vector database
- Flask backend connecting to Jira and Confluence APIs
- OpenAI models for the language generation
- Slack as the delivery interface

**Confirmed results from the case study:**

- **40% reduction in time-to-resolution during incidents** — this is your primary sales metric
- **30% improvement in onboarding efficiency for new SRE hires**
- Enhanced collaboration via Slack

**What this proves for Sentinel:** This is Sentinel's memory layer, already working in production with hard metrics. Sentinel is this product made _proactive_ — instead of waiting for an engineer to ask "what happened before?", Sentinel automatically surfaces that context the moment an alert fires. The 40% TTR reduction is your headline number. The 30% onboarding improvement is your secondary pitch.

**Critical insight:** The knowledge base was Jira + Confluence — existing data the team already had. No new documentation was required to get started. This answers the cold start question definitively.

---

### ⭐ Case Study 3: IBM QRadar SOAR Integration — Investigation Time Hours → Seconds

**Source:** "Strengthening Security Posture through Automated Incident Enrichment with IBM QRadar SOAR Integration"

**In plain English:** A security operations team was spending hours on manual, error-prone work to investigate security incidents. When an alert fired, analysts had to manually pull context from multiple systems: is this IP address known to be malicious? Is this file hash associated with known malware? What threat actor uses this technique? Without automated enrichment, the team could not efficiently filter false positives, and important incidents got lost in the noise.

**What Crest built:** An automatic integration between a threat intelligence platform and IBM QRadar SOAR (the automation layer). When an incident is created in QRadar, the integration automatically submits it to the threat intelligence platform and pulls back enriched context — threat reputation, associated threat actors, related indicators. Investigation time went from hours to seconds.

**What this proves for Sentinel:** The enrichment architecture for the Context Gathering layer. When Sentinel's agent receives an alert, it does not just search the knowledge base — it also enriches the alert with context from connected tools before matching. The QRadar SOAR architecture is the blueprint for that. Also: "reducing the need to hop through multiple systems" is explicitly what Sentinel eliminates. This case proves the pain and the solution pattern simultaneously.

---

### ⭐ Case Study 4: Google SecOps SIEM Integration — Normalization at Scale

**Source:** "Accelerate Threat Detection and Reduce Triage Time with Successful Integration with Google SecOps SIEM"

**In plain English:** A major threat intelligence company had valuable security data that could not be used in Google SecOps (their SIEM) because it came in inconsistent formats. Some threat indicators were in JSON. Some were in CSV. Some had different field names for the same data. Without a normalization layer, analysts had to manually clean and translate data before they could use it — wasting hours and introducing errors.

**What Crest built:** End-to-end integration between the threat intelligence platform and Google SecOps SIEM. Key components: automated normalization into Google's UDM (Unified Data Model), scheduled threat indicator feeds, real-time correlation (when a threat indicator matches incoming network telemetry, it surfaces as an alert), and visualization dashboards.

**Why this matters for Sentinel:** Sentinel needs to ingest from Datadog, Prometheus, PagerDuty, Splunk, CrowdStrike, Jira, and Confluence simultaneously — all with different data formats. The normalization layer is the hardest part. Crest built Google's own UDM normalization standard, which is now used across 150+ Chronicle customers. They have the normalization expertise built and documented. That saves months of engineering work.

---

### ⭐ Case Study 5: IT Helpdesk GenAI — The Feedback Loop in Production

**Source:** "Revolutionizing IT Helpdesk with Generative AI"

**In plain English:** A technology enterprise's IT helpdesk team was spending 5–10 hours per week on repetitive tasks. Engineers were spending an average of 20 minutes per day on IT issues. The two biggest problems: handling complex "how to" queries without having to dig through documentation, and the constant hallucination risk of AI tools (saying things that aren't true with false confidence).

**What Crest built:** A multi-faceted AI chatbot using LangChain + Pinecone (vector database) + GPT-4 + TruLens (for model interpretability and explainability). Critical design choice: RAG to ensure responses were based on accurate, verifiable information rather than model hallucination. A continuous feedback loop to refine the knowledge base over time.

**Confirmed results:** 30% productivity increase among IT staff.

**What this proves for Sentinel:** The feedback loop architecture — the part where every engineer interaction (approval, modification, escalation) makes the system smarter — is proven in production. TruLens for model interpretability is the answer to the "how do we trust the AI" question. The anti-hallucination RAG architecture is the answer to the trust question. The feedback loop compounding over time is the moat.

---

### ⭐ Case Study 6: Mission Control Plugins — The Cry Wolf Problem Stated Clearly

**Source:** "Mission Control Plugins" (Splunk Mission Control)

This case study is important not because of what Crest built, but because of how it defines the core problem in specific, quotable language.

Direct quote: _"One of the top challenges of a SOC is the 'cry wolf effect' or understanding the incident before triage and escalation. It's not only the multitude of alerts but the fact that many of these alerts are false positives that create stress and reduce the effectiveness of analysts' responses. One survey found that more than half of the respondents reported a rate of 50% or higher of false-positive alerts."_

And: _"Even after an alert has been deemed important enough to investigate further, analysts need threat intelligence to enrich the associated data and assess the full scope of the breach, additionally, they also need all the relevant information such as network log files, endpoint logs, etc. All of this needs to be done quickly to prevent your environment from catastrophe. Today, this process involves switching across tools, context, and manually traversing through voluminous log files which makes it time-consuming and cumbersome."_

**Use this language verbatim in your pitch.** This is from Crest's own case studies, describing a real customer problem. "Switching across tools, context, and manually traversing through voluminous log files" — that is exactly what Sentinel eliminates.

---

### ⭐ Case Study 7: MSSP Portal — Multi-Tenant SaaS Architecture

**Source:** "The MSSP Portal Cloud Operations Solution"

**In plain English:** A Managed Security Service Provider (an MSSP manages cybersecurity for multiple client companies simultaneously, like a security outsourcing firm) needed a platform where they could manage multiple client environments in total isolation from each other, while still having centralized visibility across all of them.

**What Crest built:** A multi-tenant AWS SaaS platform: isolated VPCs per tenant on EKS (Kubernetes), automated provisioning via Terraform + Helm, Prometheus + ELK (Elasticsearch-Logstash-Kibana) for observability, full stack provisioning time reduced from 6–8 hours to under 60 minutes.

**What this proves for Sentinel:** Sentinel is multi-tenant SaaS. Each customer's incident knowledge base must be completely isolated from every other customer's (Company A's incident history must never be visible to Company B). The MSSP Portal architecture is the exact blueprint for how to do this correctly on AWS at enterprise scale. Crest already built it.

---

### Case Studies That Are Less Central (but Still Relevant)

**Google SecOps SOAR Integration** — The automated playbook recommendation layer. Proves risk-scoring and context-aware recommendation architecture. Blueprint for Sentinel's recommendation output format.

**XDR Cloud Operations** — 70–80% faster incident detection. Multi-tenant federated observability. Infrastructure proof that Crest can build and operate at scale.

**Moogsoft Case Study** — Crest helped Moogsoft (an AIOps company, a direct predecessor to what Sentinel does) build and maintain: data ingestion, noise reduction, ML model enhancements, workflow management, and third-party integrations. **Ask the CEO about this specifically.** Crest has been inside a company that tried to solve this problem. They know where it got hard.

---

## PART 8 — PROS AND CONS OF THE SENTINEL MODEL

### Pros

**1. The trust problem is architecturally solved.**
We are not generating new advice. We are assembling your team's own historical response patterns and surfacing them transparently. "Based on 8 similar past incidents at your company, your team resolved this with X." The engineer can verify the sources. This is fundamentally different from an autonomous AI that says "do this" without showing its work.

**2. Cold start is solved.**
Every competitor in the autonomous AI SRE space has a cold start problem — their system is useless until it has observed many incidents. Sentinel bootstraps from existing Jira/Confluence/ServiceNow data on day one. The SASE unicorn SRE chat case proved this model works. Your first customer does not wait 6 months to get value.

**3. Compounding moat.**
The longer Sentinel is deployed, the better it gets for that specific environment. After 18 months, the knowledge base knows which alerts are always false positives at this company, which services cascade, which engineers handle which incident types, and which recommendations have been consistently approved vs. modified. A competitor entering the customer 18 months later starts from zero. This is a genuine lock-in that customers actively want because it means better and better recommendations.

**4. The Crest case studies are not inspiration — they are proof.**
Every layer of the product architecture has a production deployment proving it works. This is not a hypothesis. This is a productization of proven components.

**5. Human-in-the-loop is the right design AND the trust story.**
Every recommendation requires human approval. This is not a limitation — it is a feature. It removes the liability question. It means every action is authorized. It means the system learns from every human correction. And it is the right design: research shows that enterprises never skip the trust-building stage before allowing automation on high-risk systems.

**6. The runback mechanism creates continuous documentation.**
Every resolved incident generates an automatic structured runback. This means compliance documentation (ISO 27001, SOC 2) is an automatic output of normal operations. For FinTech and security-focused companies, this is a standalone compliance feature that has nothing to do with AI trust.

### Cons and How We Address Them

**1. The market is getting crowded fast.**
Resolve AI, incident.io AI, Azure SRE Agent, Rootly AI — all have significant funding and are moving fast. The autonomous investigation market is being claimed. **Our response:** We do not compete in autonomous investigation. We compete in the recommendation and memory layer. Different product category, different buyer conversation.

**2. Are we doing too much with four elements?**
The CEO said to focus on 1–2 things. **Honest assessment:** Elements 2 (Structure) and 3 (Identify) are the core of the product. Element 1 (Capture) can be minimized to the Slack prompt + existing data ingestion — do not build the browser extension or terminal logger yet. Element 4 (Feedback) is just storing approvals/modifications — trivially simple. **The recommendation:** Build Elements 2 and 3 to production quality. Elements 1 and 4 in their simplest possible form. Add complexity to Elements 1 and 4 only after the core works.

**3. What if the historical data is incomplete or messy?**
Real Jira tickets are often poorly written. Postmortems are inconsistent. **Our response:** The structure layer uses an LLM to extract structured information from messy text. A poorly-written Jira ticket that says "fixed the thing" is unhelpful. But even basic fields — alert type, service, resolution type, time — extracted from 2 years of tickets create a meaningful knowledge base. The system degrades gracefully: low-confidence recommendations are labeled as such. The feedback loop corrects errors over time.

**4. How do we sell to engineers who are skeptical of AI?**
Engineers have been burned by AI tools that hallucinate confidently. **Our response:** Show your work. Every recommendation links to the source incidents. The confidence score is explicit. The engineer can click through and read the actual past incidents. "Don't trust the AI, trust your team's own history which the AI is surfacing" is the framing.

**5. What about the "why us" question?**
The CEO noted this was unclear. **The honest answer:** We are CS students with access to Crest Data's engineering expertise, customer relationships, and production case studies. We are not security experts. We are knowledge systems and AI engineering experts who have access to the battle-tested architecture and the warm customer relationships that convert to design partners without a cold sales cycle. That is the why us.

---

## PART 9 — QUESTIONS FOR THE NEXT CREST CEO MEETING

The meeting is in approximately 4–5 days. These questions are ranked by importance and tied to specific things we need to know before building.

---

### TIER 1 — EXISTENTIAL (These answers change what we build)

**Q1: What were the actual measurable outcomes from the Netskope multi-agentic system?**

The case study has no result metrics. The IBM QRadar case has "hours to seconds." The SRE chat case has "40% TTR reduction." The Netskope case — your most important proof point — says nothing about outcomes. You need a number. The question: "What can you tell us about measurable outcomes from the Netskope system that isn't in the public case study? Was alert workload reduced by a measurable amount? Did analysts feel the system was useful?"

_Why this is critical:_ If the Netskope system worked well, you have an elite proof point. If the outcomes were mixed or the system was abandoned, you need to understand why before repeating the architecture.

**Q2: Does the Netskope system actually learn from how analysts respond? Or is it stateless?**

The Sentinel thesis is that the system gets smarter as it captures human response patterns — what engineers approved, what they modified, what they escalated. If the Netskope system applies the same logic every time regardless of analyst feedback, the learning flywheel does not have a production proof point. Ask directly: "When an analyst reviewed the AI recommendation and did something different, did the system capture that difference and update its future behavior?"

_Why this is critical:_ The compounding moat depends on this. If the feedback loop is not proven, we are claiming something we have not validated.

**Q3: Who at your customer base does the Sentinel problem resonate with most acutely right now?**

The CEO has 150+ customer relationships. His answer to "which company type wakes up worried about this every day" is your first customer roadmap. Ask: "When you describe the problem — SRE teams drowning in alerts, starting from scratch every time, senior engineer carrying all the knowledge — who does that resonate with most acutely? Is there a company you're thinking of right now that would want this product tomorrow?"

_Why this is critical:_ This is your design partner pipeline. One name from the CEO is worth 100 cold emails.

**Q4: Has any Crest customer ever asked for the Netskope system as a product they could just turn on?**

If Crest has been fielding this request from multiple customers, that's strong market pull. If nobody has asked, you're working from first principles. Both are workable, but you need to know which situation you're in.

---

### TIER 2 — PRODUCT DESIGN (These answers shape what we build first)

**Q5: In the SRE AI chat case — at week one vs. month six, how useful was it? How much existing data was enough to make it immediately valuable?**

Cold start is your biggest early-customer risk. The answer here tells you: (a) whether the first 30 days of a customer deployment will produce value, and (b) what the minimum historical data requirement is. Also ask: "What was the biggest adoption friction with the SRE team? Did engineers resist using it? What changed their behavior?"

**Q6: The capture layer — how exactly does the Netskope system know what an analyst did during an investigation? Walk me through the capture mechanism.**

This is the part of the architecture that is least clear from the public case study. Was there API logging? Analyst notes? An explicit feedback form? Did analysts resist any part of it? The answer tells us how to design the capture layer correctly.

**Q7: Crest helped Moogsoft — an AIOps company doing something adjacent to Sentinel. What did you learn from that engagement about where this type of system gets hard to build and maintain?**

Moogsoft is a direct predecessor to what Sentinel does (AI-driven event correlation and noise reduction for SRE). Crest was inside that company. They watched a company try to build this product. What they know about where it got hard is invaluable.

**Q8: For the SRE engineer you're connecting us with — what specific part of their daily workflow do they think is most broken?**

Before the meeting with the SRE engineer, get framing from the CEO. What should we focus the SRE conversation on? What is their current biggest pain?

---

### TIER 3 — RELATIONSHIP AND NEXT STEPS (Direct asks)

**Q9: Warm introduction to the SASE unicorn from the SRE chat case.**

This is the single most valuable ask. A warm email from the CEO to the engineering leadership at the SASE unicorn transforms "CS students with an idea" into "CS students building the productized version of a tool your team already uses and loves." This is the design partner that YC needs to see.

**Q10: How does Crest want to be involved?**

This is the conversation you have to have clearly. Ask: "We want to productize something close to what you've built as a service. How does Crest think about that? Is there an advisory relationship, an equity stake, a reference arrangement, or just good karma? We want to be transparent about the relationship before we apply to YC."

**Q11: Would Crest itself be a pilot customer?**

Crest manages complex operational systems for their own customers. They have SRE workflows. Do they face the same problem internally? If they would pilot Sentinel for their own SRE team, that is your best design partner — they understand both the technical architecture AND the operational pain.

---

## PART 10 — COFOUNDER UPDATE & MEETING SUMMARY

_This section is written to be shared directly with your cofounders._

---

### What happened in the Crest CEO meeting

We met with the Crest Data CEO. He is excited about what we are building. The core thesis — capturing how engineers respond to incidents, building institutional memory from those responses, and using that memory to recommend responses to future similar incidents — landed well. He validated it.

He is setting up weekly meetings with him and a senior SRE engineer from Crest's team. This is an extraordinary level of access for a pre-product startup. We need to use it well.

### What the CEO validated

1. **The response recommendation model.** AI watches how engineers respond, captures the pattern, recommends it next time. Human approves. This is the product.

2. **The runback mechanism.** After every incident, an automatic record of what happened, what was recommended, and what was done. This feeds the knowledge base. This is the memory compounding mechanism.

3. **Cold start via existing data.** The product analyzes existing runbooks, Slack history, Jira/Confluence when installed. You do not start from zero.

4. **Slack as the primary interface.** Every SRE team lives in Slack. The recommendation arrives in Slack. The approval happens in Slack.

### What he told us to sharpen

- Narrow the ICP more specifically — we have done this (see Part 6)
- Decide whether we are ITSM or AIOps — we are AIOps (explained in Part 1)
- Focus on 1–2 core elements, not all four — we have identified Elements 2 and 3 as the core

### What we are building — the clear statement

Sentinel is an **AIOps response intelligence copilot** for mid-market SRE teams (50–500 engineers, Series B–D). It ingests your existing incident history (Jira, Confluence, ServiceNow), builds a structured knowledge base of how your team has responded to past incidents, and delivers a recommendation — grounded in your team's own history — to the on-call engineer the moment a new similar alert fires. The engineer approves, modifies, or escalates. Every interaction feeds back into the knowledge base. Over time, Sentinel knows your system's failure patterns better than any individual engineer.

**What we are not:** We are not a triage tool (Dropzone AI, Radiant Security). We are not an autonomous remediator (Resolve AI, incident.io AI SRE). We are not a monitoring platform (Datadog, Prometheus). We are the response intelligence layer between when an alert fires and when a human acts — and we get smarter with every incident.

**The Crest connection:** Every component of this system has a production deployment at a real enterprise customer. The Netskope multi-agentic AI system is the investigation layer proven. The SASE unicorn SRE AI chat is the memory layer proven with a 40% MTTR reduction. The IBM QRadar SOAR integration is the enrichment layer proven. The IT Helpdesk GenAI is the feedback loop proven. We are productizing what Crest has already built and validated.

### What we need to become experts in before May 7

**Week 1 focus — SRE and incident management fundamentals:**

- Read Google's SRE book Chapter 14 (Managing Incidents) — it is free online at sre.google/sre-book
- Understand PagerDuty's incident model — read their public documentation on severity levels and on-call workflows
- Learn the terminology cold: MTTR, MTTD, MTTA, SEV-0 through SEV-3, toil, runbook, postmortem, alert fatigue, AIOps
- Read the ClickHouse "Your AI SRE needs better observability" article in full — it is the clearest articulation of what the market is missing

**Week 1 focus — Technical architecture:**

- Understand LangGraph (the agent orchestration framework Crest used for Netskope)
- Understand what a vector database is and how RAG works — read the LlamaIndex documentation
- Know the difference between a SIEM, SOAR, and observability tool
- Understand what PagerDuty webhooks are and how they fire

**Week 1 focus — Competitive landscape:**

- Sign up for and use Rootly, incident.io, and PagerDuty free tiers
- Read every public case study from Resolve AI and incident.io
- Know Rootly's pricing and feature set cold before any investor conversation

**Week 1 focus — Customer discovery:**

- Find 10 engineers on LinkedIn with "SRE" or "Site Reliability" in their title at Series B–D companies
- Book 3 discovery calls this week using this question: "Walk me through what happens when you get paged at 2am. What tools do you open and in what order?"
- Do not pitch. Just listen. Record the call. Document the exact language they use about the pain.

### What success looks like by May 7 (application deadline)

| Milestone                                                                        | What it proves to YC                                   |
| -------------------------------------------------------------------------------- | ------------------------------------------------------ |
| Crest CEO relationship formalized (advisor / reference)                          | Unfair advantage is real, not claimed                  |
| 1 design partner committed (SASE unicorn or Netskope)                            | Market demand validated by someone paying or piloting  |
| Working prototype: Slack bot + Jira ingestion + basic similarity search          | Technical execution is real                            |
| 5+ customer discovery calls documented with direct quotes                        | Problem is validated by real SREs, not just assumption |
| All YC application questions answered with specific evidence                     | You sound like a company, not an idea                  |
| All three founders can say "what does your company do" identically in 20 seconds | Team is aligned                                        |

**The application that gets us in:**

- "We already built this in production for a $3B company. Here are the metrics. Here is our design partner. Here is our first pilot. Here is our technical architecture grounded in 5 production case studies. We are CS students backed by the engineers who built this."

That is a YC application. Not an idea. A company.

---

## PART 11 — THE TECHNOLOGY STACK

| Sentinel Layer      | Technology                                      | Crest Production Proof                               |
| ------------------- | ----------------------------------------------- | ---------------------------------------------------- |
| Agent orchestration | LangGraph                                       | Netskope (5 agents, 10K+ alerts/day)                 |
| LLM reasoning       | Anthropic Claude via AWS Bedrock                | Netskope                                             |
| RAG pipeline        | LlamaIndex                                      | SASE SRE Chat (40% TTR reduction)                    |
| Vector database     | ChromaDB (dev) → Pinecone (prod)                | SRE Chat (ChromaDB), IT Helpdesk (Pinecone)          |
| Data normalization  | Custom UDM-style schema                         | Google GOLD Parser (150+ customers)                  |
| Alert enrichment    | PagerDuty webhooks, Datadog API, Splunk HEC     | Multiple integrations                                |
| SOAR integration    | IBM QRadar SOAR, Google SecOps SOAR             | 3 separate case studies                              |
| Incident ingestion  | Jira API, Confluence API, ServiceNow API        | SRE Chat case (Jira + Confluence), SOAR integrations |
| Multi-tenant SaaS   | AWS EKS + isolated namespaces + Terraform       | MSSP Portal (85% faster provisioning)                |
| Delivery interface  | Slack bot (primary) + web dashboard (secondary) | SRE Chat App                                         |
| Feedback capture    | Slack button interactions + webhook             | Designed from SRE Chat model                         |
| Runback storage     | PostgreSQL + S3 for raw records                 | Standard, no special proof needed                    |

---

## PART 12 — THE YC APPLICATION ANSWERS (CURRENT BEST VERSIONS)

### One-liner (50 characters)

> AI copilot that recommends responses from your team's incident history

### What does your company do?

SRE teams respond to the same production incidents over and over, starting from scratch every time. The knowledge that makes a senior engineer fast lives in their head — it is never captured in a form that helps the next person on-call. We build Sentinel: an AI copilot that watches how your team resolves incidents, structures that response pattern into a learnable format, and surfaces a specific recommendation — grounded in your team's own history — the next time a similar alert fires. The engineer reviews it in Slack and approves or modifies. Every interaction makes the system smarter. After 12 months, Sentinel knows your failure patterns better than any individual engineer.

### Why did you pick this idea?

We identified it working with Crest Data, a 1,200-person AI engineering firm that has deployed components of this architecture for enterprise customers. The SASE unicorn SRE AI chat — RAG on institutional knowledge, 40% time-to-resolution reduction — is the memory layer. The Netskope multi-agentic system — LangGraph, AWS Bedrock, Claude, 10,000+ alerts/day in production — is the identification layer. The IBM QRadar SOAR integration — investigation time from hours to seconds — is the enrichment layer. We are combining proven components into a product that nobody has made their primary identity. The Crest CEO is advising us and is introducing us to design partners.

### How far along are you?

Through Crest Data, we have production deployments proving every component of the stack. We have a prototype ingesting Jira and Confluence data and returning similarity-matched recommendations via a Slack bot. We are in weekly meetings with the Crest CEO and a senior Crest SRE engineer. We have one design partner conversation in progress with a unicorn security company that uses a Crest-built SRE AI chat tool that directly inspired Sentinel.

### Who are your competitors?

Rootly (incident management + AI), incident.io AI SRE (autonomous investigation), Resolve AI (autonomous investigation), Azure SRE Agent (Microsoft, Azure-specific). None have made _recommendation from your team's own incident history_ their primary product identity. They investigate incidents. We surface your team's historical response patterns. The real competitor is the absence of any system: teams relying on Confluence runbooks that are 6 months stale, postmortems nobody reads, and senior engineers who get paged at 2am because they are the only one who knows what to do.

### What do you understand that others don't?

The market is building autonomous AI SREs that investigate better. The durable advantage is not investigation speed — it is environment-specific historical response data that makes every recommendation more accurate for your specific team over time. Competitors using generic LLM reasoning start from zero at every customer. Sentinel starts from your team's own incident history on day one and compounds from there. The data flywheel that builds after 12 months of deployment cannot be replicated by a competitor plugging in the same base model.

---

_Built on 59 Crest Data case studies + post-CEO meeting validation + deep SRE research · March 2026_
