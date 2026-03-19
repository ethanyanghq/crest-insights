# Google SecOps (Google Chronicle) GOLD Parser

- URL: https://www.crestdata.ai/case-studies/google-chronicle-gold-parser/
- Canonical URL: https://www.crestdata.ai/case-studies/google-chronicle-gold-parser/
- Publish Date: 2024-03-28T11:35:00+00:00
- Author: Crest Data
- Tags: Security, Google Chronicle, Google SecOps
- Hero Image: https://www.crestdata.ai/wp-content/uploads/2024/03/Slide16_9-54.webp

![Google SecOps (Google Chronicle) GOLD Parser](https://www.crestdata.ai/wp-content/uploads/2024/03/Slide16_9-54.webp)

## Executive Summary

Google Chronicle normalizes, indexes, correlates, and analyzes the data to provide instant analysis and context on risky activity.

Crest Data helped Google to adopt Chronicle GOLD parser to standardize data onboarding for all log sources and the parsing approaches for massive amounts of data.

## About Customer

Google is considered one of the Big Five companies in the information technology industry that specializes in Internet-related services and products. Chronicle is a cybersecurity telemetry platform for threat hunting, threat intelligence and is part of Google Cloud Platform.

- Chronicle ingest numerous security telemetry types through a variety of methods.
- Chronicle gives analysts a way, when they see a potential threat, to determine what it is, what it’s doing, whether it matters, and how best to respond.

![](https://images.squarespace-cdn.com/content/v1/65e76fb59ac8851284f606e6/c542af8c-20cc-402f-ba5a-15a00c39a9d4/Google+Chronicle+GOLD+Parser-img-1.jpg)

## Business Challenge

Logs ingested to Chronicle are normalized to Chronicle’s UDM (Unified Data Model) format by in-built parsers.

Google faced challenges with in-built parsers having a low parsing rate because not every event type was supported for all the log sources. Also current CBN parsers were customer specific and multiple versions of parser built for different customers and leading to more maintenance efforts for Chronicle partners.

Hence, there was a need to develop a GOLD parser which covers such log sources in both breadth and depth. This means, both a high level of coverage is required for the types of events a log source produces and also the fields present in them.

The goal is to develop a parser which captures maximum amount of information and map it to UDM from the raw logs of different data sources ingested by Chronicle partners so that further use cases of Chronicle are utilized to its maximum, for eg. rules and threat detection.

## Customer Solution

Crest Data built various GOLD parsers for different types of log sources such as Windows, Zeek, PAN, Cisco, Office 365, and more, which are used by Chronicle partners and customers.

The following are the key steps:

- Analyze various security telemetry and log sources
- Design ingestion mechanism for collecting the data (e.g. syslog via Chronicle Forwarder, Ingestion APIs, third-party tools)
- Normalize and map user context/information from raw logs with UDM
- Define detection rules and parsing scripts with the UDM fields

Crest Data actively involved at every stage of the demands of product release life cycles and rolled out various quality GOLD parsers to meet the requirements.

The following is an example of raw log ingested from Windows Sysmon log source and its corresponding normalized UDM event which is extracted using the GOLD parser:

![](https://images.squarespace-cdn.com/content/v1/65e76fb59ac8851284f606e6/bb01b57d-a2c1-4def-ac3e-42cef7717392/Google+Chronicle+GOLD+Parser-img-2.jpg)

## The Crest Difference

GOLD parsers developed by Crest helped :

- Faster onboarding of all security telemetry to Chronicle
- Increase parsing rate of different log sources for 150+ Chronicle customers
- Define better detection rules with greater number of UDM fields mapping
- Improved search, view and threat detection with the more security telemetry coverage
- Benefited Google Chronicle in scalability, cost, and coverage
