# Dataminr Real-time alerts on MS Team

- URL: https://www.crestdata.ai/case-studies/dataminrs-real-time-ai-platform/
- Canonical URL: https://www.crestdata.ai/case-studies/dataminrs-real-time-ai-platform/
- Publish Date: 2024-04-05T05:31:57+00:00
- Author: Crest Data
- Tags: Analytics, Microsoft Teams
- Hero Image: https://www.crestdata.ai/wp-content/uploads/2024/04/Slide16_9-151.webp

![Dataminr Real-time alerts on MS Team](https://www.crestdata.ai/wp-content/uploads/2024/04/Slide16_9-151.webp)

### Dataminr’s real-time AI platform detects the earliest signals of high-impact events and emerging risks from within publicly available data. Dataminr delivers alerts to newsrooms using a browser-based web interface, a dedicated mobile app, email alerts and other collaboration platforms, like Slack, MS Teams.

---

**Executive Summary**

The Dataminr users were seeing alerts on the regular interval to the MS Teams channels. The engine operated on a push architecture, aggregating alerts and sending them every minute. The Crest engineering team has improved the current system by integrating Webhooks. This enhancement aims to significantly decrease alert delivery time and boost customer adoption on the MS Teams platform.

## Business Challenge

- Dataminr Pulse and Dataminr For News Apps are published into the Microsoft Teams platform. With Microsoft Teams Apps, organizations have the ability to customize their Teams experience, seamlessly integrate third-party tools, and automate workflows. This integration significantly boosts collaboration and productivity within the Teams environment. Users can easily configure alerts directly within MS Teams channels, ensuring timely and relevant notifications to keep teams informed and responsive.

- Existing implementation is a push based alert system. This runs on a one minute scheduler and sends an alert in the batch of every minute. This is schedular based model and there is a high chance of delay in response. All the live alerts have to wait for the next scheduler. The schedule architecture may lead to delay to the message delivery system.

## Customer Solution

Crest Data and Dataminr worked together to create a webhook system for Microsoft Teams. We changed from the push mechanism to pull mechanism architecture for the alert system. This system allows users to customize how alerts appear in Microsoft Teams directly from Dataminr, and it can handle increasing amounts of messages without issue.

- The alert system can be adjusted on the fly, meaning changes can be made without stopping the service to update software.
- It includes features to limit the number of alerts sent to Teams, ensuring the system doesn’t get overwhelmed.
- If an alert fails to send, the system will try again to make sure no information is lost.
- It also allows setting limits on alerts for each webhook to prevent overloading.
- Finally, the system is designed to add new users seamlessly without needing to update the Microsoft Teams application.

![](https://images.squarespace-cdn.com/content/v1/65e76fb59ac8851284f606e6/1b4d0923-9ced-4d5c-9115-a28f3a30b50e/Screenshot+2024-04-05+111050.png)

This would enable Dataminr to:

- Streamline the communication and enable dynamic interactions between applications and users. Improving efficiency, responsiveness, and the overall user experience with Webhook.
- The solution is faster, scalable, customisable and efficient.

## The Crest Difference

### Adding Value Through Innovative Features

- Webhook-Based Subscription Model: Introduced a streamlined process for users to subscribe to their desired watchlists, enhancing user engagement and efficiency.
- Customizable Communication Templates: Developed adaptable Teams adaptive card templates within the Dataminr platform, facilitating easy modifications and allowing for personalized customer communications.

### Going Above and Beyond to Provide a Robust Solution

- Dynamic Alert Frequency Adjustment: Innovated by automatically adjusting the frequency of alerts to stay within the operational parameters of Microsoft Teams, ensuring uninterrupted communication flow.
- Advanced Error Handling: Enabled dynamic configuration of alert messages tailored to specific error scenarios, coupled with intelligent alert retry mechanisms based on those error codes, significantly boosting system reliability and effectiveness.
