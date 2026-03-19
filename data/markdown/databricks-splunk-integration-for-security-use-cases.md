# Databricks: Splunk Integration for Security Use Cases

- URL: https://www.crestdata.ai/case-studies/databricks-splunk-integration-for-security-use-cases/
- Canonical URL: https://www.crestdata.ai/case-studies/databricks-splunk-integration-for-security-use-cases/
- Publish Date: 2024-03-28T08:27:00+00:00
- Author: Crest Data
- Tags: Security, Databricks, Splunk
- Hero Image: https://www.crestdata.ai/wp-content/uploads/2024/03/Slide16_9-86.ng_.webp

![Databricks: Splunk Integration for Security Use Cases](https://www.crestdata.ai/wp-content/uploads/2024/03/Slide16_9-86.ng_.webp)

## Executive Summary

## Databricks customers previously needed to manually configure S3 bucket.

Integrations and create Databricks notebooks from scratch to get and parse data into Databricks environment.

## Business Challenge

### Databricks customers previously needed to manually configure S3 bucket.

Integrations and create Databricks notebooks from scratch to get and parse AWS Cloud Trail , AWS VPC logs and Syslogs data into Databricks environment for further processing and analytics. Also the customers previously needed to manually create jobs and queries from UI to run them.

## Customer Solution

Crest Data wrote Databricks notebooks to collect and parse AWS Cloud Trail , AWS VPC logs and Syslogs data from S3 buckets into Databricks environment be used for further processing. Crest created Databricks Notebooks to push specified data from Databricks to ingest into Splunk and pull data present into Splunk to Tables in Databricks environment. Crest also helped build Splunk app for Databricks which allows splunk admins to run queries in Databricks tables and execute Databricks Jobs and notebooks using custom commands from Splunk.

The following custom commands were implemented:

- **Databricksquery** : query data present in the Databricks table from Splunk.
- **Databricksrun** : submit a one-time run without creating a job on Databricks.
- **Databricksjob** : run an already created job now from Splunk.

## The Crest Difference

### The Databricks notebooks helped:

- The Databricks Notebooks helped the manual effort for collecting and parsing the data from S3 buckets.
- The custom commands in splunk helped run queries and jobs and reduce dependency on access to Databricks instance.
