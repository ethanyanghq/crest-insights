# Expanding Threat Detection Visibility with Google SecOps Ingestion Scripts

- URL: https://www.crestdata.ai/case-studies/google-chronicle-ingestion-scripts/
- Canonical URL: https://www.crestdata.ai/case-studies/google-chronicle-ingestion-scripts/
- Publish Date: 2024-03-28T06:33:00+00:00
- Author: Crest Data
- Tags: Security, Google Chronicle, Google SecOps
- Hero Image: https://www.crestdata.ai/wp-content/uploads/2024/03/Expanding-Threat-Detection-Visibility-with-Google-SecOps-Ingestion-Scripts.webp

![Expanding Threat Detection Visibility with Google SecOps Ingestion Scripts](https://www.crestdata.ai/wp-content/uploads/2024/03/Expanding-Threat-Detection-Visibility-with-Google-SecOps-Ingestion-Scripts.webp)

## Executive Summary

To perform full threat detection, many enterprises need to ingest security telemetry data from a diverse array of sources into their security operations center. However, the customer using the Google SecOps (formerly known as Google Chronicle) platform found that it supported feeds for a limited number of data sources, resulting in many environments being unsupported. In the absence of any standardized method to ingest data from external sources into the platform, enterprises were able to leverage the advanced capabilities of the platform, resulting in poor visibility gaps.

This case study describes how Crest Data addressed this challenge by developing configurable ingestion scripts for 15+ sources, including Box Events, OneLogin, Slack, Citrix, and more. The customer leverages the power of the Google SecOps (formerly known as Google Chronicle) platform, as these scripts pull data from various sources and ingest it into the platform. The common reusable library for data ingestion into Chronicle optimizes the process by abstracting away complexity, saving customers valuable time and resources.

## About the Customer

The customer was facing problems using Google SecOps (formerly known as Google Chronicle), where they found that it supported feeds for a limited number of data sources, resulting in many environments being unsupported. The customer operates in complex digital environments that require comprehensive visibility into various third-party services, cloud infrastructure, and SaaS applications.

## Customer Challenge

The customer faced significant challenges in their security operations when using Google SecOps (formerly Google Chronicle) for threat detection. To efficiently monitor security, an enterprise must ingest telemetry data from a wide range of sources. However, the platform offered feeds only for a small subset of data sources originally. As a result, many vital environments were ignored, and visibility gaps were created regarding the enterprise security posture.

Additionally, there was no standardized way for customers to bring data from these unsupported sources into Google SecOps (formerly known as Google Chronicle). This technical hurdle hampered organizations from maximizing the platform’s advanced features, as they cannot constantly synchronize and analyze security data across disparate third-party applications and infrastructure.

## Proposed Solution

Crest Data developed a comprehensive suite of 15+ configurable ingestion scripts to pull telemetry data from diverse sources and ingest it into Google SecOps (formerly known as Google Chronicle). To simplify the integration process, these scripts utilize a common reusable library that abstracts the technical complexities, enabling the enterprise to leverage the platform’s potential while saving time and resources.

Key features and implementation details of the solution include:

- **Flexible Deployment** : The scripts were optimized to run within the GCP Cloud Function environment. The security teams are able to easily access these scripts and make them configurable, as they were made publicly accessible through GitHub repositories.
- **Automated Synchronization** : Users can use a scheduler to initiate cloud functions automatically at regular time intervals. This ensures that the security data is always up-to-date and in-sync with the most recent telemetry data from the field.
- **Wide Source Support** : The solution provides standardized ingestion for a broad range of critical data sources, including:
- **SaaS & Communication** : Slack, Box, and Proofpoint.
- **Identity & Access Management** : Duo Admin and OneLogin (Users and Events).
- **Cloud Infrastructure** : Azure Event Hub, Google Cloud Storage, and Citrix (Audit logs and Sessions).
- **Threat Intelligence & Vulnerability** : MISP, Stix Taxii, and Tenable.io (Assets and Vulnerabilities).
- **Endpoint & Network Security** : Trend Micro Cloud App Security and Aruba Central.
- **Messaging Middleware:** PubSub.

With these scripts, Crest Data provided a consistent way of getting data from unsupported sources into Google SecOps, enabling organizations to benefit fully from its advanced threat detection capabilities.

## Outcomes & Success Metrics

The implementation of the configurable ingestion scripts by Crest Data resulted in several key benefits for organizations using Google SecOps (formerly known as Google Chronicle):

- **Maximized Platform Potential:** By ingesting data from sources where ingestion was previously unsupported, the customer can maximize the advanced threat detection capabilities of the Google SecOps (formerly known as Google Chronicle) platform.
- **Expanded Threat Visibility:** The solution enabled streamlined access to security telemetry from 15+ different sources, like Box, Slack, OneLogin, Azure Event Hub, etc., to close various security visibility gaps.
- **Increased Operational Efficiency:** We developed a common reusable library that abstracted the technical complexity, ensuring a streamlined integration process that saves customers valuable time and resources.
- **Real-Time Data Synchronization:** Use of scheduled GCP cloud functions keeps security data up-to-date and in-sync with the latest telemetry data from the field.
- **Flexible and Accessible Integration:** The built-in configurable options in the scripts, along with their free access via a public GitHub repository, enable users to adopt the solution as per their specific environment needs.

## About Crest Data

Crest Data is a data and AI-first, security-led product engineering and technology solutions provider with deep expertise in cloud and AI, cybersecurity, observability, data analytics, and workflow automation. In this case study, Crest Data used its cloud integration and security automation capabilities to help the customer strengthen its security posture by maximizing the potential of Google SecOps (formerly known as Google Chronicle) by developing a set of configurable ingestion scripts for 15+ varied sources.

With 1,200+ experts and a track record of 5,500+ successful projects across 150+ global customers, and backed by strong partnerships with Google, AWS, Microsoft, Datadog, Dynatrace, ServiceNow, and NetApp, Crest Data delivers outcome-focused solutions that strengthen security, improve platform reliability, and enable sustainable digital growth.
