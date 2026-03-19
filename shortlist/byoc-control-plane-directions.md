# The Vercel for BYOC: Directions

## The Core Thesis

More software vendors are being forced to deploy their products inside customer-owned cloud accounts instead of running everything in their own SaaS infrastructure. Customers demand this for data sovereignty, regulatory compliance, cost control, and security policy reasons. Every vendor that accepts this model ends up rebuilding the same painful operational layer: tenant onboarding, cross-account IAM, deployment pipelines, federated monitoring, upgrade orchestration, and support access. Nobody sells this layer as a product. The startup is the abstraction that makes deploying into someone else's cloud account as simple as pushing to your own.

---

## Direction 1: The Vendor-Side Deployment Platform

**Who it's for**: Software vendors (security companies, data infrastructure providers, AI/ML platforms, compliance tools) that sell products deployed into customer cloud accounts.

**What it does**: The vendor defines their application architecture once — containers, databases, networking requirements, IAM permissions, monitoring hooks. The platform takes that definition and handles everything needed to deploy, operate, and upgrade the application across hundreds of customer cloud accounts.

**How it works**:
- Vendor writes a declarative manifest describing their application (similar to a Helm chart or Docker Compose, but for cross-account BYOC deployment)
- When a new customer signs up, the vendor triggers a provisioning flow through the platform
- The platform creates the required infrastructure in the customer's AWS/GCP/Azure account using pre-built IaC templates
- It sets up secure communication channels between the vendor's control plane and the customer's environment (mTLS, VPN, or private link)
- It establishes federated observability: metrics, logs, and traces flow back to the vendor's monitoring stack without giving the vendor admin access to the customer's account
- When the vendor ships an update, the platform orchestrates rolling upgrades across all tenant environments
- A support dashboard gives the vendor visibility into each tenant's health, deployment status, and configuration without requiring direct account access

**The product surface**: A web dashboard for the vendor's platform engineering team, a CLI for developers, an API for automation, and a customer-facing onboarding portal that guides end-customers through connecting their cloud account.

**Revenue model**: Per-tenant per-month fee charged to the vendor. The vendor pays $X/month for each customer environment the platform manages. Price scales with the complexity of the deployment (number of services, regions, compliance requirements).

**The expansion path**: Start with one cloud (AWS) and one application pattern (containerized microservices). Expand to GCP and Azure. Add support for more deployment patterns (serverless, VMs, Kubernetes clusters). Eventually support complex multi-region deployments with data residency controls.

---

## Direction 2: The Customer-Side Receiving Dock

**Who it's for**: Enterprises that run multiple third-party vendor products inside their own cloud accounts and need a standardized way to receive, govern, and manage all of them.

**What it does**: Instead of every vendor deploying into the customer's account in their own bespoke way (each with different IAM requirements, networking assumptions, and monitoring patterns), the enterprise installs a lightweight control plane that standardizes how vendor software gets provisioned, monitored, and governed.

**How it works**:
- The enterprise deploys the control plane into their AWS/GCP/Azure account (a small set of infrastructure: an orchestrator, a policy engine, and an observability collector)
- When a new vendor needs to deploy their product, the vendor registers with the control plane and declares what resources they need
- The policy engine evaluates the request against the enterprise's security policies (allowed instance types, permitted network access, required encryption, logging mandates)
- If approved, the control plane provisions a sandboxed environment for the vendor's software with least-privilege IAM, isolated networking, and centralized logging
- The enterprise gets a unified dashboard showing all vendor software running in their account: resource consumption, compliance status, access logs, and cost attribution
- Upgrades, patches, and configuration changes from the vendor flow through the control plane, which enforces change approval policies before allowing modifications

**The product surface**: A Terraform module or CloudFormation stack that installs the control plane. A web dashboard for the enterprise's cloud/security team. A vendor portal where software providers submit deployment requests and view their tenant status.

**Revenue model**: Annual subscription charged to the enterprise, priced by number of vendor deployments managed or by cloud spend under management.

**The expansion path**: Start with the governance and visibility layer (read-only). Add provisioning automation. Add cost optimization (track per-vendor spend, recommend rightsizing). Eventually become the enterprise's single pane of glass for all third-party software running in their cloud estate.

---

## Direction 3: The BYOC Deployment Broker

**Who it's for**: Both vendors and customers, acting as the intermediary that connects them.

**What it does**: A marketplace-like platform where software vendors publish their applications in a BYOC-ready format, and enterprise customers connect their cloud accounts to receive deployments. The platform brokers the trust relationship, handles provisioning, and manages the ongoing operational lifecycle.

**How it works**:
- Vendors package their application using the platform's SDK/manifest format, defining required infrastructure, permissions, and operational parameters
- Enterprise customers create an account on the platform and connect their cloud account(s) via a cross-account IAM role or service principal
- The customer browses or is invited to install a vendor's product. They click "Deploy," review the resource and permission requirements, and approve
- The platform provisions the vendor's application inside the customer's cloud account, using the customer's own compute, storage, and networking
- Both vendor and customer get dashboards: the vendor sees operational health across all tenants, the customer sees what's running in their account, what it costs, and what access each vendor has
- The platform handles billing reconciliation: the customer pays their cloud provider directly for infrastructure, and pays the vendor's software license through the platform or directly

**The product surface**: A two-sided portal — vendor side for publishing and operating, customer side for installing and governing. APIs for both sides. A CLI for vendor developers. A Terraform provider for enterprises that want to manage deployments as code.

**Revenue model**: Transaction fee or platform fee. Take a percentage of the vendor's software license fee for each deployment brokered through the platform. Or charge both sides: vendors pay to list, customers pay for the management layer.

**The expansion path**: Start as a simple deployment broker for a narrow vendor category (e.g., security tools). Build network effects — the more vendors publish to the platform, the more attractive it is for customers, and vice versa. Eventually become the default distribution channel for BYOC enterprise software.

---

## Direction 4: The Infrastructure Primitive Library

**Who it's for**: Platform engineers at any company that needs to build BYOC deployment capability, whether they're a software vendor or an internal platform team.

**What it does**: Instead of building a full platform, sell the building blocks. Open-source or commercial Terraform modules, Pulumi components, and CDK constructs that solve the hardest recurring problems in BYOC deployment: cross-account IAM federation, tenant-isolated networking, federated observability, secure deployment pipelines, and tenant lifecycle management.

**How it works**:
- A library of production-tested, composable infrastructure modules for BYOC patterns
- Cross-account IAM module: sets up the trust relationships between vendor and customer accounts with least-privilege policies, automatic credential rotation, and audit logging
- Tenant networking module: creates isolated VPCs or subnets for each tenant with configurable connectivity back to the vendor's control plane (PrivateLink, VPN, Transit Gateway)
- Federated observability module: deploys metric collectors, log forwarders, and trace exporters in each tenant environment that ship data to the vendor's monitoring stack without granting broad access
- Deployment pipeline module: sets up a GitOps or push-based deployment flow that can target multiple tenant environments with canary/rolling/blue-green strategies
- Tenant lifecycle module: handles provisioning, scaling, hibernation, and decommissioning of tenant environments
- Each module is independently usable but designed to compose together

**The product surface**: A package registry (like a private Terraform registry), documentation site, CLI for scaffolding new BYOC projects, and a hosted service for managing module versions and configurations across tenants.

**Revenue model**: Open-core. The modules are open source; the hosted management layer, enterprise support, compliance certifications, and advanced features (multi-cloud, audit logging, RBAC) are paid. Alternatively, purely commercial licensing with per-tenant pricing.

**The expansion path**: Start with AWS modules for the most common BYOC pattern (containerized app in isolated VPC with federated monitoring). Community adoption drives awareness. Add GCP and Azure. Add a hosted control plane that orchestrates the modules across tenants. The open-source modules become the on-ramp to the commercial platform.

---

## Direction 5: The Vertical BYOC Platform (Security-First)

**Who it's for**: Security software vendors specifically — XDR, SIEM, EDR, SOAR, and threat intelligence companies that deploy agents, collectors, or analytics into customer environments.

**What it does**: The same core concept as Direction 1 (vendor-side deployment platform), but deeply specialized for security software deployment patterns. Security software has unique requirements that generic BYOC tooling doesn't handle well: it needs privileged access to customer infrastructure for threat detection, it generates massive volumes of telemetry, it must comply with specific regulatory frameworks (FedRAMP, SOC2, HIPAA), and it often runs in highly restricted environments (air-gapped, GovCloud).

**How it works**:
- The platform understands security-specific deployment patterns: agent rollout across fleets, log collector deployment, SIEM data pipeline provisioning, sensor placement for network detection
- Tenant onboarding includes automated compliance checks: does the customer environment meet the prerequisites for deploying this security product? (Required services enabled, logging configured, IAM policies in place)
- The federated observability layer is designed for security telemetry: high-volume event ingestion, alert forwarding, incident escalation paths, and forensic data access during investigations
- The platform provides a "break glass" mechanism for incident response: controlled, audited, time-limited elevated access to a customer's environment when investigating an active threat
- Compliance dashboards show deployment status mapped to specific frameworks: which tenants are FedRAMP-compliant, which need remediation, which are running outdated versions

**The product surface**: A platform tailored to the security vendor's operational model — SOC integration, incident response workflows, compliance reporting, and customer success dashboards alongside the deployment and monitoring features.

**Revenue model**: Per-tenant pricing with tiers based on compliance requirements. FedRAMP-ready deployments cost more than standard. GovCloud support costs more than commercial cloud.

**The expansion path**: Own the security vertical completely. Build the deepest possible understanding of how security software gets deployed and operated in customer environments. Then expand to adjacent verticals (data infrastructure, compliance tools, healthcare IT) using the same platform with vertical-specific extensions.

---

## Direction 6: The Onboarding-Only Wedge

**Who it's for**: Any software vendor that has already built their BYOC deployment infrastructure but struggles with the customer onboarding step specifically.

**What it does**: Solves only the narrowest, most painful slice of the BYOC problem: getting a new customer's cloud account connected, validated, provisioned, and ready to receive the vendor's software. Everything after initial deployment (monitoring, upgrades, support) is out of scope initially.

**How it works**:
- The vendor creates an onboarding flow using the platform's builder: a sequence of steps that the customer needs to complete (create IAM role, enable required services, configure networking, approve permissions)
- The customer receives a branded onboarding link and walks through a guided setup wizard
- At each step, the platform validates that the customer's environment is correctly configured (runs automated checks against the customer's cloud account)
- If something is wrong (missing permissions, incorrect VPC configuration, required service not enabled), the platform provides specific remediation instructions or offers to fix it automatically with customer approval
- Once all prerequisites are met, the platform executes the initial deployment and confirms the vendor's software is running correctly
- The vendor sees a dashboard showing onboarding status for every customer: who's in progress, who's stuck, who's complete, and what the average time-to-deploy is

**The product surface**: An onboarding flow builder for the vendor, a customer-facing setup wizard, and a status dashboard. Minimal infrastructure — this is mostly a workflow orchestration tool that calls cloud APIs.

**Revenue model**: Per-onboarding fee (charge each time a new customer is provisioned) or a flat monthly fee based on the number of active tenants.

**The expansion path**: This is the deliberate thin-wedge play. Get adopted for onboarding alone, then expand into the full lifecycle: monitoring, upgrades, support access, compliance. Each expansion is a natural upsell because the vendor already trusts the platform with their customer's cloud account connection. The onboarding flow is the trojan horse for the full control plane.

---

## Direction 7: The Multi-Cloud Abstraction

**Who it's for**: Software vendors that need to deploy into customer environments across AWS, GCP, and Azure — not just one cloud.

**What it does**: Most BYOC tooling is cloud-specific. If a vendor supports customers on AWS and GCP, they typically build and maintain two completely separate deployment stacks. This platform abstracts across clouds so the vendor defines their application once and deploys it into any customer cloud account regardless of provider.

**How it works**:
- The vendor describes their application in a cloud-agnostic manifest: compute requirements, storage needs, networking topology, IAM permissions, observability hooks
- The platform translates this manifest into cloud-specific infrastructure: ECS on AWS, Cloud Run on GCP, Container Apps on Azure (or Kubernetes everywhere as a common denominator)
- Cross-cloud tenant management: a single dashboard showing all tenants regardless of which cloud they run on, with normalized metrics, consistent upgrade workflows, and unified access controls
- The platform handles the translation layer for each cloud's IAM model, networking primitives, monitoring tools, and deployment mechanisms
- When the vendor ships an update, the platform deploys it across all clouds with cloud-appropriate strategies

**The product surface**: A unified control plane that makes multi-cloud BYOC feel like single-cloud. The vendor's platform team works in one system regardless of where their customers run.

**Revenue model**: Premium pricing justified by the multi-cloud complexity. Per-tenant pricing with a cloud multiplier (supporting a tenant on a second cloud is an upsell).

**The expansion path**: Start with two clouds (AWS + one of GCP/Azure — whichever has more BYOC demand). The multi-cloud capability itself becomes a wedge: vendors that only support AWS today want to offer GCP support without doubling their platform engineering headcount. The platform sells that capability.

---

## Direction 8: The Developer Experience Layer

**Who it's for**: Platform engineers at software vendors who already have BYOC infrastructure but struggle with visibility, developer experience, and operational tooling.

**What it does**: Does not replace the vendor's existing Terraform, Kubernetes, or deployment pipeline. Instead, sits on top and provides the operational experience layer: a dashboard for tenant management, a CLI for developers, runbooks for common operations, and alerting for tenant health issues.

**How it works**:
- The platform connects to the vendor's existing infrastructure tooling (Terraform state, Kubernetes clusters, cloud APIs, monitoring systems) via read-only integrations
- It builds a unified model of all tenant environments: what's deployed where, what version, what's the health status, when was the last upgrade, are there any drift or compliance issues
- Developers get a CLI: `byoc tenants list`, `byoc tenant acme status`, `byoc tenant acme deploy v2.3.1`, `byoc tenant acme logs --service api`
- Operations teams get a dashboard: tenant overview, deployment history, health checks, cost per tenant, alert status
- Customer success teams get a portal: onboarding status, feature adoption, support ticket context
- The platform generates runbooks and automation for common operations: tenant provisioning, version upgrades, rollbacks, scaling, incident response

**The product surface**: A web dashboard, CLI, and API that unify the operational experience for multi-tenant BYOC deployments. It integrates with existing tools rather than replacing them.

**Revenue model**: SaaS subscription priced by number of tenants under management.

**The expansion path**: Start as the visibility layer (read-only). Vendors adopt it because it solves the "I can't see what's happening across my tenants" problem without requiring them to rip out their existing infrastructure. Once embedded, add write operations: deploy through the platform, manage configurations, orchestrate upgrades. The read-only dashboard becomes the full control plane over time.

---

## Cross-Cutting Considerations

### Cloud Provider Starting Point
Every direction requires choosing which cloud to support first. AWS is the obvious default — it has the most BYOC deployments, the most complex IAM model (which means the most pain), and the largest market share in enterprise. GCP and Azure support come later as expansion.

### Kubernetes vs. Cloud-Native
A fundamental architecture decision. Build on Kubernetes (works the same everywhere, large ecosystem, but adds complexity) or build on cloud-native primitives (ECS, Cloud Run, Fargate — simpler for each cloud, but harder to go multi-cloud). Direction 7 may force Kubernetes as the common denominator. Others can choose.

### Open Source vs. Closed Source
Directions 4 and 8 lend themselves to open-core strategies. Directions 1, 2, 3, 5 are more naturally commercial products. Direction 6 could go either way. Open source accelerates adoption but requires a clear commercial conversion path.

### Who Pays: Vendor or Customer?
Directions 1, 5, 6, 7, 8 charge the vendor. Direction 2 charges the customer. Direction 3 charges both. This determines go-to-market motion: vendor-side means fewer, larger deals with platform engineering teams; customer-side means enterprise sales into security/cloud/IT teams.

### The Trust Problem
Every direction involves the startup gaining some level of access to customer cloud accounts. This is the biggest adoption barrier. The platform needs to clearly scope its access, provide audit trails, support customer-managed encryption keys, and earn trust through transparency. Security certifications (SOC2, ISO 27001) will be required early for enterprise adoption.
