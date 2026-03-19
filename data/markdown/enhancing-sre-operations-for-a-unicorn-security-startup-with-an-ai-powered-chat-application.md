# Enhancing SRE Operations for a Unicorn Security Startup with an AI-Powered Chat Application

- URL: https://www.crestdata.ai/case-studies/enhancing-sre-operations-for-a-unicorn-security-startup-with-an-ai-powered-chat-application/
- Canonical URL: https://www.crestdata.ai/case-studies/enhancing-sre-operations-for-a-unicorn-security-startup-with-an-ai-powered-chat-application/
- Publish Date: 2024-11-28T10:59:38+00:00
- Author: Crest Data
- Tags: AI/ML, llamaindex
- Hero Image: https://www.crestdata.ai/wp-content/uploads/2024/11/CrestDataAI-anAI-PoweredChatApplication_new.webp

![Enhancing SRE Operations for a Unicorn Security Startup with an AI-Powered Chat Application](https://www.crestdata.ai/wp-content/uploads/2024/11/CrestDataAI-anAI-PoweredChatApplication_new.webp)

## Customer Background

The customer, a leading player in the Secure Access Service Edge (SASE) space, sought to enhance the productivity and efficiency of its Site Reliability Engineering (SRE) team. Their challenge revolved around streamlining the retrieval and correlation of critical operational information stored in Jira and Confluence, key tools for incident management and operational knowledge.

### Key Challenges

- **Delayed Incident Responses** : Searching for and correlating relevant information across Jira and Confluence during incidents was time-consuming, leading to delays in resolution.
- **Information Overload** : The team faced difficulty navigating large volumes of documentation and past incident reports to retrieve actionable insights quickly.
- **Onboarding Complexity** : New SRE team members found it challenging to assimilate detailed SRE processes and past resolutions without concise summaries.
- **Scattered Knowledge** : Contextual correlations between active tickets and historical data were often overlooked, complicating the preparation for incident escalations.

## Crest Data’s Solution

Crest Data designed and implemented an **AI-Powered Chat Application** tailored to the needs of the customer SRE team. The solution leveraged advanced technologies to provide seamless integration, data interrogation, and intuitive user experiences.

---

## Solution Overview

### The chat application featured:

- **Natural Language Querying** : Enabled SRE members to search Jira tickets and Confluence documentation using intuitive language, significantly reducing search time.
- **Real-Time Information Correlation** : Automatically suggested related Jira tickets, Confluence documents, and insightful comments to aid in resolving complex issues.
- **Summarization for Onboarding** : Provided concise, relevant summaries of key documents, easing the onboarding process for new team members.
- **Cross-Referencing Capabilities** : Allowed easy cross-referencing of active tickets with historical data to improve preparation for escalations.

---

## Architecture Highlights :

- **Slack Integration** : Delivered responses within the Slack environment for convenient team collaboration.
- **Backend with Flask** : Ensured efficient processing of user queries with integration into Confluence and Jira.
- **Vector Database** : Chroma DB stored embeddings of operational data, enabling rapid retrieval and contextual insights.
- **RAG Approach** : Leveraged Retrieval-Augmented Generation (RAG) for accurate, context-aware responses using [LlamaIndex](https://www.llamaindex.ai/) and [OpenAI](https://openai.com/) models.

![](https://images.squarespace-cdn.com/content/v1/65e76fb59ac8851284f606e6/b0782b4e-6cfa-4cf0-8002-9718f4da2509/image1.png)

---

## Benefits Delivered

1. **Improved Incident Response Time** : The intuitive search capabilities reduced delays in accessing critical information.
2. **Enhanced Operational Insights** : Correlations and summarizations empowered SREs to make informed decisions quickly.
3. **Seamless Onboarding** : New team members were able to ramp up faster, benefiting from summarized insights into SRE practices and historical incidents.
4. **Streamlined Knowledge Management** : Automated updates ensured the most relevant and up-to-date data was always accessible.

## Results

- Reduced time-to-resolution during incidents by over **40%** .
- Improved onboarding efficiency by **30%** for new SRE hires.
- Enhanced team collaboration and communication via Slack-based integration.

---

## Crest Data’s Value Addition

Crest’s expertise in AI and system integration was pivotal in transforming customer’s SRE processes. Our team:

- Analyzed customer’s operational bottlenecks and designed a solution aligned with their specific needs.
- Delivered a scalable and maintainable system with periodic updates to ensure continuous improvement.
- Provided dedicated support to ensure smooth adoption and optimal use of the application.
