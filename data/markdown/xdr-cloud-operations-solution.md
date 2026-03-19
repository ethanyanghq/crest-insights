# XDR Cloud Operations Solution

- URL: https://www.crestdata.ai/case-studies/xdr-cloud-operations-solution/
- Canonical URL: https://www.crestdata.ai/case-studies/xdr-cloud-operations-solution/
- Publish Date: 2025-11-15T17:05:34+00:00
- Author: Crest Data
- Tags: CloudOps, AWS
- Hero Image: https://www.crestdata.ai/wp-content/uploads/2025/11/XDRCloudOperationsSolution.webp

![XDR Cloud Operations Solution](https://www.crestdata.ai/wp-content/uploads/2025/11/XDRCloudOperationsSolution.webp)

## Executive Summary

This case study details the successful implementation of build automation and observability for our Extended Detection and Response (XDR) product on AWS. Following AWS best practices, the solution harnesses native cloud services to deliver comprehensive visibility, high availability, and operational efficiency. By integrating tightly with AWS’s secure and scalable infrastructure, the deployment enables real-time monitoring, accelerates incident response, and optimizes system performance.

## About the Customer

The customer is an innovative cybersecurity firm focused on developing cloud-native, scalable, and intelligent security solutions tailored for modern enterprises. Their flagship XDR platform emphasizes advanced threat detection, automated response, and deep observability across complex, distributed environments. By leveraging AWS, the customer ensures secure, resilient, and high-performance deployments that conform to industry standards and best practices.

## Customer Challenge

The customer faced a distinctive architectural challenge: deploying their XDR product directly within end-users’ cloud environments without having direct access or administrative control. This required designing a fully automated, zero-touch deployment framework capable of operating reliably across heterogeneous customer infrastructures. Additionally, securing communications—through automated management of VPN tunnels and encrypted data flows—without manual intervention added significant complexity.

If unaddressed, these challenges risked causing deployment delays, increasing operational overhead, and introducing security vulnerabilities. More importantly, failure to automate observability and maintain secure, scalable communications would have impeded product adoption, eroded customer trust, and compromised the ability to deliver a seamless, secure experience to end-users.

---

## Why AWS

The customer selected AWS as the cloud platform for its solution due to its extensive portfolio of native services, global scalability, and industry-leading security features. AWS offered the flexibility and reliability necessary to support a highly distributed, customer-managed deployment model, enabling seamless deployment of the XDR product across diverse end-user cloud environments. With services like AWS CloudFormation and AWS Systems Manager, the platform facilitated automation of complex deployment and observability workflows at scale.

Moreover, AWS’s strong security architecture and compliance framework aligned closely with the customer’s zero-trust principles, where secure communication and data integrity were paramount. By adopting AWS, the customer was able to deliver a secure, scalable, and cloud-agnostic XDR solution with minimal operational complexity.

---

## Why the Customer Chose Crest Data

The customer engaged the partner for their specialized expertise in cloud-native security solutions and deep familiarity with the AWS ecosystem. The partner successfully designed and implemented the XDR platform to fulfill the unique requirement of secure, autonomous deployments within end-user environments—without requiring direct administrative access. By utilizing AWS’s scalable infrastructure, the partner delivered a highly automated and resilient platform aligned with cloud best practices.

A distinguishing factor was Crest Data’s capability to build a federated observability architecture, enabling each new tenant deployment to be automatically integrated into a centralized monitoring and analytics system. This approach provided unified, real-time visibility and operational insights across all environments. Crest Data’s combined strength in AWS architecture and infrastructure automation positioned them as the optimal choice to address the customer’s complex security and deployment needs.

## The Crest Data Solution

Crest Data addressed the customer’s challenge of automating the deployment of their product in AWS by designing a scalable, secure, and fully automated cloud architecture. The solution emphasized seamless tenant onboarding, infrastructure as code, continuous integration and deployment (CI/CD), and robust observability, all tailored to meet enterprise-grade requirements. This implementation leveraged DevOps and GitOps best practices.

The deployment process was initiated using AWS CloudFormation, which provisioned the foundational networking infrastructure, including VPCs, Subnets, NAT Gateways, Internet Gateways, Security Groups, and Route Tables. Additionally, the CloudFormation template deployed EC2 instances configured as self-hosted GitHub Actions runners for the Crest Data’s private repositories. Leveraging these EC2 runners, further infrastructure components were provisioned using Terraform in conjunction with GitHub Actions workflows.

The deployment infrastructure incorporated Amazon EKS to host tenant workloads as well as observability components. Persistent storage for EKS workloads was facilitated through AWS EFS and EBS, while AWS S3 was employed for long-term, cold storage requirements.

The architecture featured multiple AWS Load Balancer endpoints to serve microservices and observability-related traffic, all secured through mutual TLS (mTLS) enabled by underlying NGINX ingress controllers.

Each onboarded tenant environment operated its own Prometheus instance, which was scraped securely over mTLS by a central SaaS Prometheus deployment, providing granular observability into tenant-specific metrics. Furthermore, tenants deployed Logstash instances responsible for forwarding log data to a centralized Elasticsearch cluster hosted within the Crest Data’s SaaS platform. This architecture ensured secure, comprehensive, and scalable observability across all tenant environments.

![](https://www.crestdata.ai/wp-content/uploads/2025/11/MainArchDiagram.webp)

### Observability Architecture which includes logging and monitoring components deployed over SaaS and Tenant platforms:

![](https://www.crestdata.ai/wp-content/uploads/2025/11/MonitoringArchDiagram.webp)

## Automation & Observability:

**Infrastructure Automation**

- Entire infrastructure defined using Infrastructure as Code (IaC).
- Terraform scripts and Helm charts (stored in Git) define network, compute, and security resources.
- Github Actions and ArgoCD automated deployment of Terraform/Helm stacks on code merges.

**Monitoring & Logging**

- A federated observability architecture was implemented using Prometheus and the ELK stack (Elasticsearch, Logstash, Kibana), enabling centralized monitoring and logging across all tenant environments.
- Metrics are collected using Prometheus within each tenant cluster and securely transmitted over mTLS to the central customer SaaS platform.
- Logs are forwarded via Filebeat and visualized through Kibana, with data securely ingested into a centralized Elasticsearch cluster.
- Both logging and monitoring pipelines are fully automated to ensure consistent deployment, scalability, and operational efficiency across all environments.

**Environment Setup**

- The customer’s SaaS platform and each tenant environment are deployed in separate AWS accounts, ensuring strict isolation, enhanced security, and regulatory compliance.
- Each environment is provisioned with its own dedicated VPC containing public and private subnets.
- Subnets are distributed across three Availability Zones (AZs) to provide high availability and fault tolerance.

**DevSecOps Best Practices**

- Version-controlled infrastructure code.
- Rolling upgrades for services.
- Secure secrets management with AWS Secrets Manager and 1-password.

---

## Results and Benefits

The deployment of the automated XDR platform on AWS delivered significant operational and strategic benefits to the customer. By leveraging AWS-native services alongside infrastructure-as-code and GitOps practices, the partner enabled fully automated, repeatable, and scalable tenant provisioning. The streamlined automation process reduced deployment time for new environments from numerous hours to under **30 minutes** , improving engineering efficiency and accelerating customer onboarding.

The solution also drove cost efficiency. By using scalable services like Amazon EKS and storage tiers such as EBS, EFS, and S3, the customer reduced infrastructure and maintenance costs **by over 35%** compared to traditional deployment models. GitHub Actions and self-hosted runners eliminated the need for third-party CI/CD tooling, further optimizing cost and control.

Operational visibility improved significantly through a multi-tenant observability model that centralized monitoring and logging while maintaining strict isolation and security. With Prometheus and Elasticsearch integrated across tenants and securely accessed via mutual TLS, **the team achieved 70-80% faster** incident detection and response times, while also reducing MTTR (mean time to resolution) across environments.
