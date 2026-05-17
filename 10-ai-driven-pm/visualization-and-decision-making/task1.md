Context
SocialConnect feature integration

EPAMSuite is a company that provides an established cloud-based project management platform used by medium-to-large enterprises. Marketing and Sales have identified a strong demand from existing and potential clients to integrate basic social media monitoring capabilities directly within EPAMSuite. The goal is to allow project teams to track mentions of their project keywords or brand hashtags on major social media platforms without leaving EPAMSuite.

High-Level Requirements:

Setup: Project Admins should be able to configure specific keywords/hashtags to monitor for their project within EPAMSuite's project settings area. They need to authenticate EPAMSuite to access their company's Platform X and Y accounts via official APIs.

Feed Display: A new tab or section within each project called "SocialConnect" should display a feed of recent posts/mentions from Platform X and Y containing the configured keywords/hashtags.

Basic Filtering: Users should be able to filter the feed by platform (Platform X / Y) and maybe by a date range (e.g., last 24 hours, last 7 days).

Linking: Clicking on a post in the feed should ideally link out to the original post on the respective platform.

API Integration: The solution must use the official APIs provided by Platform X and Y. Rate limits, authentication, and data privacy considerations are crucial.

UI Integration: The new "SocialConnect" tab/section needs to seamlessly integrate with EPAMSuite's existing UI design system and navigation.

Exclusions (Out of Scope for this Phase): Sentiment analysis, automated reporting, replying/interacting with posts from within EPAMSuite, historical data import beyond what the APIs readily provide (e.g., maybe only the last 7-30 days).

Team:

Standard Scrum team ( 1 PO/BA, 1 Scrum Master, 6 Developers, 2 QA). Other resources, like an Architect and a UI/UX designer, are shared resources. A cross-functional and experienced scrum team with velocity in a similar feature of 60 points.

It’s a T&M project, so no fixed budget or time.

Main Goal
Your goal is to estimate the effort required to deliver the "SocialConnect" feature described above and communicate it to management.

Decomposition: Break down the high-level requirements into smaller, estimable work items (Epics, User Stories).

Estimation: Provide an overall high-level effort estimate for delivering this entire feature. In addition, provide high-level estimates for BA activities individually.

Steps to Do (Part 1)
Use DIAL. For more comprehensive and accurate results, consider using the Gemini 2.5 Pro Model, but feel free to try any other available LLM.

Write the Prompt:

Ensure the prompt asks the AI to understand the existing information/chat history.

Include instructions for the AI to ask 2-3 clarifying questions to identify: the typical effort required for delivering the feature and the estimated effort for Business Analyst (BA) activities.

Use T-Shirt Sizing for the overall effort estimation (e.g., Small, Medium, Large, XL).

Use PERT for BA activities estimation.

Copy output in Markdown format. See the example below:
Question 1: What is your favorite color? Response: My favorite color is blue.

Question 2: What is your favorite hobby? Response: My favorite hobby is reading books.

Copy your conversation, including any clarifying questions asked by the AI and your responses. Submit this content as the solution to the task. Do not include the final deliverables (the final LLM responce with Estimations).
Proceed with Practical Task: Estimation. Part 2
