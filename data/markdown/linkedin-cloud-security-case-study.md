# LinkedIn Cloud Security Case Study

- URL: https://www.crestdata.ai/case-studies/linkedin-cloud-security-case-study/
- Canonical URL: https://www.crestdata.ai/case-studies/linkedin-cloud-security-case-study/
- Publish Date: 2024-03-28T11:35:00+00:00
- Author: Crest Data
- Tags: DevOps, Microsoft Azure
- Hero Image: https://www.crestdata.ai/wp-content/uploads/2024/03/Slide16_9-58.webp

![LinkedIn Cloud Security Case Study](https://www.crestdata.ai/wp-content/uploads/2024/03/Slide16_9-58.webp)

## Executive Summary

## The LinkedIn Cloud Security Operations team

needed a DevSecOps solution to implement various security policies in an automated way and at scale to their fast growing Azure cloud infrastructure.

## Business Challenge

LinkedIn’s Azure Cloud infrastructure is growing rapidly with more than 150k resources across multiple Azure Tenants in just 3 years. Various different teams were using various different custom automation tools for provisioning their own infrastructure on Azure. To meet the Cloud security standards, the company’s Information Security team was using Azure Security Policies to allow a secure and standardized way of provisioning resources. At such a huge scale, with that kind of growth rate of resources, and with growing number of Azure policies, it was required to have a solution to manage Azure policies at scale.

## Customer Solution

Crest Data built various automated workflows using Azure DevOps based CICD pipelines for the LinkedIn Information Security Team

- To deploy and assign Security Policies on multiple tenant, management group and subscription scopes in Azure
- To grant temporary or permanent exemptions for Security Policies by capturing user requests from a React based frontend portal
- To remediate non-compliant resources reported by Security Policies
- To send email notifications to the owners of non-compliant or insecure resources
- To collect Azure tenant data for analytics purposes

To help visualize the security posture of their Azure Infrastructure, Crest Data used the data collected from Azure Tenants to build various PowerBI dashboards for use cases like

- Resource Inventory to monitor various types of resources
- Identity and Access Management to monitor privileges
- Policy Compliance Scores to compare their environment health with various Cloud Security Regulatory Controls

## The Crest Difference

The automated workflows and visualizations of Azure Infrastructure implemented by Crest helped LinkedIn Information Security team to:

- Enforce or Exempt Policies on 150k+ Azure resources within minutes
- Follow up with each resource owner to fix their non-compliant resources
- Prioritize remediation of non-compliant resources based on various parameters in a phased manner
- Monitoring high privileged entities and roles and removing stale entities
- Achieve compliances for various Cloud Security Regulations
