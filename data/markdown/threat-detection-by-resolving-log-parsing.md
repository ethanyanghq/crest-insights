# Enhancing Threat Detection by Resolving Log Parsing Inconsistencies for Improved Security Coverage

- URL: https://www.crestdata.ai/case-studies/threat-detection-by-resolving-log-parsing/
- Canonical URL: https://www.crestdata.ai/case-studies/threat-detection-by-resolving-log-parsing/
- Publish Date: 2024-03-28T05:51:00+00:00
- Author: Crest Data
- Tags: Security, Cyberreason
- Hero Image: https://www.crestdata.ai/wp-content/uploads/2024/03/Standardizing-Security-Logs.png

![Standardizing Security Logs](https://www.crestdata.ai/wp-content/uploads/2024/03/Standardizing-Security-Logs.png)

## Executive Summary

The customer faced serious problems parsing the logs in its XDR platform, resulting in improper creation of detection rules. As different security products and log types were in different formats, it was very hard to map the raw fields into a standardized format like the Chronicle Universal Data Model (UDM). Such inconsistencies led to frequent breaking of detection rules, resulting in false positives or missed detections, severely compromising the efficiency of the platform’s overall security. Furthermore, as the legacy development approach was lengthy, it hampered the enterprise’s ability to quickly onboard new customers and products.

## About the Customer

The customer is a leading provider of a sophisticated Extended Detection and Response (XDR) platform designed to provide holistic coverage of security events across an organization’s digital environment. Their platform utilizes advanced detection rules that analyze critical data fields based on data source categories, event types, and security categories to identify potential threats.

## Customer Challenge

The customer’s main challenge was ensuring complete coverage of all security events across its XDR platform. Despite the presence of detection rules, the customer faced significant challenges in accounting for the extensive variance across data fields. One of the major challenges was mapping the raw log fields from a variety of sources to a standard format, such as the Chronicle Universal Data Model (UDM).

The issues were worsened by inconsistent mapping of similar product categories, log types, and formats. These inconsistencies frequently violated the detection rules, making security outcomes unreliable, including missed detections and false positives. Additionally, the customer’s standard parser development approach resulted in a long development lifecycle, thus affecting the customer’s ability to rapidly onboard new customers and support new security products.

## Customer Solution

Crest Data addressed the mapping challenges by developing Silver parsers for more than 30 security products, including Microsoft Graph Alert, Cisco Umbrella, CrowdStrike EDR, and Sophos Firewall. These parsers were specifically designed to standardize security event logs, ensuring consistent mapping across diverse product categories and formats within the XDR platform.

The development process leveraged Minimum Valuable Product (MVP) data fields established by the customer to ensure that parsed security event data contained the most valuable information for generating detection rules.

**Key steps in the implementation included:**

- **Telemetry Analysis** : Deeply analyzing security products and their specific telemetry to properly define the necessary security context for events.
- **UDM Mapping** : Mapping raw log fields to the appropriate Chronicle Universal Data Model (UDM) fields based on established MVP standards.
- **Parser Development** : Creating specialized parser configuration files (.conf) based on the finalized UDM mapping.
- **Centralized Documentation:** Creating a comprehensive mapping sheet for all developed parsers to serve as a reference for creating, modifying, or troubleshooting detection rules.
- **Extended Contextual Support** : Adding support for additional logs that provide critical context during investigations, going beyond basic security use cases .

## Outcomes

Successful implementation of Silver parsers across the XDR platform ensured the creation of a standardized and efficient security operations environment:

- **Accelerated Customer Onboarding:** Reduction in parser development lifecycle, allowing for faster adoption by new customers.
- **Standardized Log Normalization:** Development of silver parsers for more than 30 products ensured consistent mapping of UDM data fields, significantly enhancing the overall quality of the parsers.
- **Strengthened Threat Detection:** Consolidation of search and detection capabilities by increasing security coverage and reducing the occurrence of failed logs within supported types.
- **Improved Detection Rule Management:** A detailed mapping sheet now serves as a central reference for creating, modifying, and troubleshooting detection rules.
- **Enriched Investigative Context:** The solution added support for supplementary logs that provide critical context during investigations, going beyond standard security use cases.
- **Comprehensive Event Coverage:** The customer achieved comprehensive coverage of security events across the platform by standardizing logs for consistent mapping across various products.

## About Crest Data

Crest Data is a data and AI-first product engineering and technology solutions provider with deep expertise in cloud and AI, cybersecurity, observability, data analytics, and workflow automation. In this case study, Crest Data applied its security data engineering and log normalization capabilities to help the customer standardize security event logs and ensure consistent UDM mapping across their XDR platform. Crest Data augmented these capabilities through the development of specialized Silver parsers for over 30 security products and a streamlined development lifecycle.

With 1,200+ experts and a track record of 5,500+ successful projects across 150+ global customers, and backed by strong partnerships with Google, AWS, Microsoft, Datadog, Dynatrace, ServiceNow, and NetApp, Crest Data delivers outcome-focused solutions that strengthen security, improve platform reliability, and enable sustainable digital growth.
