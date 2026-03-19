# Fivetran for Security Telemetry: Directions

## The Core Thesis

Security teams drown in heterogeneous data. Every SaaS product, threat intelligence feed, endpoint agent, and cloud service emits telemetry in its own format, through its own API, with its own authentication quirks and schema drift. Getting that data into a SIEM, XDR, or security data lake in a normalized, trustworthy form is the unglamorous foundation that every detection, investigation, and response capability depends on. Today this work is done by hand — connector by connector, parser by parser, feed by feed — and it breaks constantly.

Three patterns from Crest Data's client work converge on the same structural pain:

- **SaaS Telemetry Connectors** (Sumo Logic engagement): replacing brittle agent-based collection with direct API connectors for sources like Okta, Mimecast, Google Workspace, and Azure AD. The pain: token refresh, polling schedules, rate limits, partial failures, deduplication.
- **Log Normalization Layer** (XDR platform engagement): building high-fidelity parsers that map vendor-specific log formats into a standard schema (like Chronicle UDM) so detection rules stop breaking. The pain: field-level inconsistency across 30+ security products, schema drift, false positives from bad parsing.
- **Threat Intel Integration Factory** (TruSTAR engagement): a framework for rapidly onboarding new threat intelligence feeds — analyzing source formats, extracting indicators, normalizing to a common model, and maintaining integrations at scale. The pain: every new feed is a bespoke pipeline, and source proliferation makes manual work untenable.

Individually, each of these is a thin services play (4/10 viability as standalone startups). Together, they describe a single infrastructure layer that doesn't exist as a product: the system that gets security data from any source, into any destination, in a normalized and trustworthy form. The startup is "Fivetran for security telemetry" — a managed pipeline that handles ingestion, normalization, and delivery so security teams can focus on detection and response instead of data plumbing.

---

## Direction 1: The Connector-First Pipeline

**Who it's for**: Security teams (SOC engineers, detection engineers, security data engineers) at mid-to-large enterprises who run a SIEM or security data lake and need to ingest telemetry from dozens of SaaS and security products.

**What it does**: A managed ingestion service with a growing catalog of prebuilt connectors for security-relevant data sources. Each connector handles authentication, polling, rate limiting, error recovery, deduplication, and schema normalization. The customer points a connector at a source and a destination, and data flows — normalized, reliable, and monitored.

**How it works**:
- The customer signs up and connects their SIEM/data lake as a destination (Splunk, Elastic, Chronicle, Snowflake, S3, etc.)
- They browse a connector catalog organized by source type: identity (Okta, Azure AD, Ping), email (Mimecast, Proofpoint, Google Workspace), endpoint (CrowdStrike, SentinelOne, Carbon Black), cloud (AWS CloudTrail, GCP Audit Logs, Azure Activity Log), network (Zscaler, Palo Alto), and so on
- For each connector, setup is configuration-driven: provide API credentials, select which event types to ingest, choose a normalization schema (OCSF, ECS, UDM, or custom), and activate
- The platform handles the ongoing operational burden: token refresh, API version changes, schema drift detection, backfill on failure, deduplication, and throughput monitoring
- A health dashboard shows connector status, data freshness, volume trends, error rates, and normalization coverage per source
- When a source API changes (which happens constantly), the platform ships an updated connector — the customer doesn't have to notice

**The product surface**: A web console for connector management, a CLI/API for automation, a health dashboard, and an alert system for ingestion failures. The connector catalog is the core product asset.

**Revenue model**: Usage-based pricing — per GB ingested or per source per month. Tiered plans based on number of active connectors and data volume.

**The expansion path**: Start with the 10 highest-demand security SaaS sources (Okta, CrowdStrike, Azure AD, AWS CloudTrail, Google Workspace, Mimecast, Proofpoint, SentinelOne, Palo Alto, Zscaler). Add 5-10 connectors per quarter. Expand destination support. Over time, the breadth and reliability of the connector catalog becomes the moat — each new connector maintained is a unit of operational burden the customer doesn't carry.

---

## Direction 2: The Normalization Engine

**Who it's for**: Detection engineers and security platform vendors who need raw telemetry mapped into a consistent schema so detection rules, correlation logic, and investigation workflows don't break when new sources are added.

**What it does**: Instead of leading with connectors (getting data in), this direction leads with normalization (making data usable). The product is a processing layer that sits between raw ingestion and the detection/analytics stack. It takes heterogeneous security logs — regardless of how they arrived — and transforms them into a normalized, enriched, and validated schema.

**How it works**:
- Raw security logs arrive (via the customer's existing ingestion pipeline, a Kafka topic, an S3 bucket, or a syslog stream)
- The normalization engine identifies the source type automatically (fingerprinting based on field patterns, log structure, and metadata)
- It applies the appropriate parser — a maintained mapping from the source's native schema to the customer's target schema (OCSF, ECS, Chronicle UDM, or a custom model)
- The parser extracts security-relevant fields: actor identity, target resource, action type, timestamp, severity, network tuple, file hash, process lineage — whatever the detection stack needs
- Field-level validation catches normalization errors before they reach detection rules: missing required fields, type mismatches, impossible values, timezone inconsistencies
- A normalization quality score per source gives detection engineers confidence that they can write rules against a new source without worrying about parsing surprises
- Parser updates ship continuously as source schemas drift — the customer's detection rules don't break when a vendor changes their log format

**The product surface**: A processing engine (deployed as a container, a serverless function, or a managed service), a parser management console, a schema browser, normalization quality dashboards, and a parser SDK for customers who want to extend coverage.

**Revenue model**: Per-source per-month pricing for managed parser maintenance, or a platform license for self-hosted deployment. Premium tier for custom schema support and SLA-backed parser update guarantees.

**The expansion path**: Start with parsers for the 20 most common security log sources and one target schema (OCSF, since it's emerging as the industry standard). Add more sources and more target schemas. Build a parser development framework that accelerates new parser creation using patterns learned from the existing corpus. Over time, the accumulated parsing knowledge — edge cases, field mappings, schema drift history — becomes an asset that's extremely hard to replicate.

---

## Direction 3: The Threat Intel Feed Fabric

**Who it's for**: Threat intelligence teams and security platform vendors who need to onboard, normalize, and operationalize intelligence from many external sources — commercial feeds, open-source feeds, ISACs, government advisories, and internal threat research.

**What it does**: A managed layer for threat intelligence ingestion and normalization. Instead of building a custom pipeline for every new intel source, the platform provides a framework that handles source analysis, indicator extraction, normalization to STIX/TAXII or a custom model, confidence scoring, deduplication across feeds, and delivery to downstream consumers (SIEM, SOAR, TIP, EDR).

**How it works**:
- The platform maintains a library of feed adapters — each one understands a specific threat intel source's format, API, authentication, and update cadence
- When a customer activates a feed, the adapter handles polling, extraction, and normalization automatically
- Indicators (IPs, domains, hashes, URLs, CVEs, TTPs) are extracted, deduplicated across all active feeds, enriched with metadata (first seen, last seen, confidence score, source reliability rating), and delivered in a consistent format
- Cross-feed correlation surfaces when multiple independent sources report the same indicator, increasing confidence
- A feed health dashboard shows freshness, volume, overlap between feeds, and unique coverage per source — helping the customer decide which feeds are actually worth paying for
- The platform can deliver normalized intel to multiple destinations simultaneously: push to a SIEM for detection rules, push to a SOAR for automated response playbooks, push to an EDR for blocking, or expose via API for custom workflows

**The product surface**: A feed management console, feed health and overlap analytics, a delivery configuration interface, and an API for programmatic access. The analytics layer (which feeds are redundant? which provide unique coverage?) is a differentiating feature that feed vendors themselves won't build.

**Revenue model**: Per-feed per-month for managed adapters, plus a platform fee for the correlation and analytics layer. Enterprise tier for custom feed onboarding and SLA-backed delivery guarantees.

**The expansion path**: Start with the 15 most commonly used open-source and commercial threat intel feeds. The feed overlap analytics become a wedge into procurement conversations — "you're paying for 8 feeds but 3 of them are 90% redundant." Expand into feed marketplace dynamics: become the layer through which security teams discover, evaluate, and operationalize new intelligence sources.

---

## Direction 4: The Full-Stack Security Data Pipeline

**Who it's for**: Security engineering teams that want a single platform to handle the entire journey from raw security data to analysis-ready telemetry — ingestion, normalization, enrichment, routing, and delivery.

**What it does**: Combines Directions 1, 2, and 3 into a unified pipeline. This is the full "Fivetran for security telemetry" vision: a managed platform that connects to any security data source, normalizes the output into a standard schema, enriches it with context (asset inventory, identity resolution, threat intel, geolocation), and delivers it to any destination — all with operational monitoring, quality guarantees, and zero parser maintenance for the customer.

**How it works**:
- **Ingest**: Prebuilt connectors for SaaS APIs, cloud audit logs, endpoint agents, network appliances, and threat intel feeds. Also accepts push-based input via syslog, HTTP, Kafka, and S3
- **Normalize**: Automatic source identification and schema mapping. Every event gets mapped to OCSF (or the customer's chosen schema) with field-level validation and quality scoring
- **Enrich**: Pluggable enrichment modules add context to normalized events — resolve IP to asset, map user to identity, tag indicators against active threat intel, add geolocation, classify by MITRE ATT&CK technique
- **Route**: Rules-based routing sends different event types to different destinations at different fidelities. High-value alerts go to the SIEM in full fidelity. Bulk telemetry goes to a data lake in compressed form. Compliance-relevant logs go to long-term storage
- **Deliver**: Managed delivery to any destination — Splunk, Elastic, Chronicle, Sentinel, Snowflake, Databricks, S3, or custom endpoints
- **Monitor**: End-to-end pipeline observability — source health, normalization quality, enrichment coverage, delivery latency, and cost attribution per source

**The product surface**: A full pipeline management console with visual pipeline builder, source and destination catalogs, enrichment configuration, routing rules, quality dashboards, and cost analytics. CLI and API for infrastructure-as-code workflows.

**Revenue model**: Usage-based (per GB processed) with a platform fee. Premium tiers for advanced enrichment, custom schema support, dedicated infrastructure, and SLA guarantees. This is the highest-ACV direction.

**The expansion path**: This is the end-state vision, not the starting point. The risk of building this first is that it's too broad to ship quickly and too complex to sell simply. The realistic path is to start with Direction 1 or 2 as the wedge and expand toward this over 2-3 years. But articulating the full vision matters for fundraising, hiring, and strategic positioning.

---

## Direction 5: The AI-Native Parser Factory

**Who it's for**: Security platform vendors and large security teams that need to support hundreds of log sources and can't afford to hand-build and maintain a parser for each one.

**What it does**: Uses LLMs and learned patterns from a corpus of existing parsers to semi-automate the creation and maintenance of new parsers. Instead of a human spending days analyzing a new log source, mapping fields, and writing parsing logic, the platform analyzes sample logs, proposes a field mapping, generates a parser, and validates it against the target schema — with human review for quality assurance.

**How it works**:
- The customer provides sample logs from a new source (a few hundred representative events)
- The platform's analysis engine examines the log structure: format (JSON, CSV, syslog, CEF, custom), field names, value patterns, timestamp formats, and event type taxonomy
- It proposes a field mapping to the target schema, drawing on its corpus of existing mappings for similar sources. If it's seen CrowdStrike endpoint logs before, it knows which fields map to process name, parent process, file hash, and network connection
- The proposed mapping is presented for human review with confidence scores per field. High-confidence mappings (timestamp, IP address, hostname) are usually right. Low-confidence mappings (custom vendor fields with ambiguous names) are flagged for human judgment
- Once approved, the platform generates the parser configuration in the customer's required format (Splunk SPL, Elastic ingest pipeline, Chronicle parser, Cribl pack, etc.)
- Ongoing maintenance: when the source schema drifts (new fields added, field names changed, format altered), the platform detects the drift, proposes parser updates, and flags breaking changes before detection rules fail

**The product surface**: A parser development workbench with sample log upload, automated analysis, proposed mappings, human review interface, parser export, and drift monitoring. Can be delivered as a SaaS tool or embedded into a platform vendor's parser development workflow.

**Revenue model**: Per-parser per-month for ongoing maintenance and drift monitoring. One-time fees for initial parser generation. Enterprise licensing for platform vendors who want to embed the engine.

**The expansion path**: Start by building the corpus — every parser the platform generates adds to the pattern library, making the next parser faster and more accurate. This is the direction with the strongest compounding mechanism. The corpus of field mappings, schema drift patterns, and source-specific edge cases becomes a proprietary dataset that improves with every customer. Over time, parser generation approaches full automation for common source types, and human review is only needed for novel or unusual sources.

---

## Direction 6: The Security Data Quality Layer

**Who it's for**: Detection engineering teams who need to trust the data flowing into their detection rules — and currently can't, because normalization quality is inconsistent and invisible.

**What it does**: Instead of replacing the customer's ingestion pipeline, this direction sits alongside it and continuously monitors normalization quality. It's a testing and observability layer for security data: are fields being parsed correctly? Are there missing values? Is schema drift causing silent detection failures? Think "Datadog for your security data pipeline" — not the pipeline itself, but the confidence that it's working.

**How it works**:
- The customer connects the quality layer to their normalized data stream (a Kafka topic, a SIEM index, a data lake table)
- The platform continuously samples events and evaluates normalization quality per source: field completeness, type correctness, value distribution anomalies, timestamp consistency, and schema compliance
- It maintains a quality score per source that detection engineers can check before writing rules. "CrowdStrike data is 98% normalized correctly. This new EDR source is at 72% — don't write detection rules against it yet."
- When quality degrades (a source changes its log format, a parser breaks, a field starts arriving empty), the platform alerts immediately — before the SOC notices that detections stopped firing
- It provides a normalization coverage map: which fields from which sources are reliably normalized, and which are missing or inconsistent. This directly answers the question "can I trust this data for detection?"
- Over time, the quality history per source becomes a dataset: which sources are reliable, which break often, and which parsers need the most maintenance attention

**The product surface**: A quality dashboard per source, alerting on degradation, normalization coverage maps, and integration with detection engineering workflows (e.g., "this detection rule depends on fields X, Y, Z — here's their current quality score"). Lightweight deployment — reads data, doesn't move it.

**Revenue model**: Per-source per-month for monitoring. Premium tier for automated remediation suggestions and parser fix recommendations.

**The expansion path**: This is the thinnest possible wedge into the security data pipeline. It requires no changes to the customer's existing infrastructure — it only reads. Adoption is easy because it solves an immediate pain (silent detection failures from bad data) without asking anyone to rip out their current stack. Once embedded, expand into normalization (Direction 2) and then full pipeline management (Direction 4). The quality layer is the trojan horse.

---

## Cross-Cutting Considerations

### Why "Fivetran for Security" Instead of Just Fivetran?

Fivetran, Airbyte, and other data pipeline companies handle analytics data well. But security telemetry has specific requirements that general-purpose pipelines don't address:

- **Schema standards are security-specific**: OCSF, ECS, Chronicle UDM, STIX/TAXII — these aren't generic data schemas. They encode security-domain concepts like kill chain stages, MITRE ATT&CK techniques, and indicator types.
- **Timeliness requirements are extreme**: A 15-minute delay in analytics data is fine. A 15-minute delay in security telemetry means a missed detection window. Ingestion SLAs must be measured in seconds, not minutes.
- **Data quality has safety implications**: Bad normalization in an analytics pipeline produces a wrong dashboard. Bad normalization in a security pipeline produces a missed intrusion. The quality bar and the consequences of failure are fundamentally different.
- **The source catalog is specialized**: The connectors that matter (CrowdStrike, Okta, Palo Alto, SentinelOne, Mimecast) are security products that general-purpose pipeline vendors deprioritize because they don't serve the analytics use case.
- **Enrichment is domain-specific**: Threat intel correlation, MITRE mapping, asset resolution, and identity enrichment are security concepts. A general pipeline doesn't know how to add them.

This specialization is why a security-specific pipeline company can exist alongside Fivetran — the same way Veeva exists alongside Salesforce. The domain requirements are different enough to support a dedicated product.

### The Cribl Question

Cribl (observability pipeline, $3.5B+ valuation) is the closest large-scale analog. It sits in the data-routing layer and handles security telemetry among other data types. The key differences that create room for a startup:

- Cribl routes and transforms but doesn't deeply normalize to security schemas. It's a general-purpose stream processor, not a security normalization engine.
- Cribl doesn't maintain a connector catalog for security SaaS APIs. It receives data that's already been collected.
- Cribl doesn't provide security-specific enrichment (threat intel correlation, MITRE mapping).
- Cribl's buyer is typically the observability/IT team. The security telemetry startup's buyer is the detection engineering or security data engineering team.

The risk is that Cribl expands into security normalization. The defense is depth: deeper security domain expertise, a more complete connector catalog for security sources, and tighter integration with security workflows.

### OCSF as a Tailwind

The Open Cybersecurity Schema Framework (OCSF) — backed by AWS, Splunk, CrowdStrike, IBM, and others — is creating a common language for security telemetry for the first time. This is a major tailwind: it defines the target schema that the normalization layer maps to, reducing the "which schema?" debate. A startup that becomes the best way to get data *into* OCSF format rides this adoption wave rather than competing with it.

### Build vs. Buy Dynamics

Every security team currently builds this infrastructure themselves, usually poorly. The build-vs-buy calculus favors "buy" when:

- The number of sources exceeds what one team can maintain (typically 15-20+)
- The team is tired of parsers breaking silently and detections going blind
- A new SIEM migration forces re-mapping every source from scratch
- The team wants to add a security data lake alongside their SIEM and needs dual-delivery

SIEM migrations are a particularly strong buy trigger. When a company moves from Splunk to Chronicle, or from QRadar to Sentinel, every parser and connector must be rebuilt. A pipeline that's destination-agnostic makes migration dramatically less painful.

### Who Pays?

The buyer differs by direction:

- **Directions 1, 4, 6** sell to enterprise security teams — the CISO's budget, through the detection engineering or security data engineering lead. Larger deal count, more competition for budget.
- **Directions 2, 5** sell to security platform vendors — the engineering team building an XDR, SIEM, or MDR product. Fewer buyers, larger contracts, deeper embedding.
- **Direction 3** sells to threat intelligence teams — either inside enterprises or at intel platform vendors.

Starting with platform vendors (Direction 2 or 5) gives you fewer but deeper relationships and faster learning. Starting with enterprise security teams (Direction 1 or 6) gives you more data points and a broader market. The Crest Data relationship supports the vendor-side path — they work with security platform companies daily.

### Recommended Starting Point

**Direction 6 (Security Data Quality Layer)** is the thinnest wedge with the lowest adoption barrier. It doesn't ask customers to change their pipeline — it just monitors what they already have. The insight it provides (your data quality is worse than you think, and it's silently breaking your detections) creates urgency for the fuller pipeline product. From there, expand into normalization (Direction 2), then connectors (Direction 1), then the full stack (Direction 4).

**Direction 5 (AI-Native Parser Factory)** is the strongest compounding play. If the team has conviction that parser generation can be meaningfully automated, this direction builds the most defensible asset over time. It also has a natural first customer in the Crest Data network — security platform vendors who need to support hundreds of log sources.

Either path leads toward Direction 4 (Full-Stack Pipeline) as the long-term vision. The question is which wedge gets you to real usage fastest.
