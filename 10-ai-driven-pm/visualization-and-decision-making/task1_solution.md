# Practical Task: Estimation — Part 1 (Conversation Log)

## Initial Prompt

> You are an experienced Agile Project Manager and Business Analyst. I need your help estimating the effort required to deliver a new feature called **"SocialConnect"** for EPAMSuite — a cloud-based project management platform used by medium-to-large enterprises.
>
> Please review the following context carefully:
>
> **Feature Summary:** SocialConnect will allow project teams to track mentions of project keywords or brand hashtags on major social media platforms (Platform X and Platform Y) directly within EPAMSuite — without leaving the application.
>
> **High-Level Requirements:**
> 1. **Setup:** Project Admins configure keywords/hashtags in project settings. They authenticate EPAMSuite with Platform X and Y via official APIs.
> 2. **Feed Display:** A new "SocialConnect" tab/section displays recent posts/mentions from Platform X and Y.
> 3. **Basic Filtering:** Filter by platform (X / Y) and by date range (last 24 hours, last 7 days).
> 4. **Linking:** Clicking a post links out to the original post on the respective platform.
> 5. **API Integration:** Must use official APIs. Rate limits, authentication, and data privacy are crucial.
> 6. **UI Integration:** Must seamlessly integrate with EPAMSuite's existing UI design system and navigation.
> 7. **Out of Scope:** Sentiment analysis, automated reporting, replying to posts from within EPAMSuite, historical data import beyond API limits (7–30 days).
>
> **Team:** Standard Scrum team — 1 PO/BA, 1 Scrum Master, 6 Developers, 2 QA. Shared Architect and UI/UX Designer. Velocity: ~60 story points per sprint. T&M project (no fixed budget or time).
>
> Before providing estimations, please ask me **2–3 clarifying questions** to better understand:
> - The typical effort required for delivering the feature end-to-end.
> - The estimated effort for Business Analyst (BA) activities specifically.
>
> Use **T-Shirt Sizing** (S, M, L, XL) for the overall feature effort estimation and **PERT** (Optimistic, Most Likely, Pessimistic) for BA activities estimation.

---

## AI Clarifying Questions

**Question 1:** Regarding API integration complexity — do you already have existing integrations with any third-party APIs in EPAMSuite (e.g., OAuth 2.0 flows, webhook handlers, rate-limit management), or would this be the first external API integration? This significantly impacts both the backend development effort and the BA effort to define API contracts and error-handling scenarios.

**Question 2:** For the UI/UX component — does EPAMSuite have a mature, well-documented design system (component library, design tokens, etc.) that the team can leverage, or will the UI/UX designer need to create new components from scratch for the feed display, filtering controls, and settings panels?

**Question 3:** What is the expected sprint length, and how mature is the team's CI/CD pipeline? Specifically, will the team need to set up new infrastructure (e.g., a caching layer for API responses, a message queue for background polling) or can they deploy into an existing microservices architecture?

---

## My Responses

**Response to Question 1:**
EPAMSuite already has a few existing third-party integrations (e.g., email services and a calendar sync feature) that use OAuth 2.0 flows, so the team is familiar with the pattern. However, we have **not** integrated with social media APIs before, so Platform X and Y API specifics (rate limits, data formats, pagination) will be new territory. There are existing utility libraries for OAuth and HTTP clients that can be reused, but new adapters will need to be built for each platform. The BA will need to research and document API constraints and map the platform data models to our internal models.

**Response to Question 2:**
EPAMSuite has a **mature design system** with a comprehensive component library (built on React) including cards, tabs, filters, date pickers, and list views. Most of the UI for the SocialConnect feed can be assembled from existing components. The UI/UX designer will mainly need to define the layout and any minor customizations (e.g., a social post card component showing platform icon, author, timestamp, and snippet). No major new design system components are expected.

**Response to Question 3:**
Sprint length is **2 weeks**. The team has a solid CI/CD pipeline with automated testing and containerized deployments. The existing architecture is microservice-based, so a new "SocialConnect" microservice can be added. However, we will likely need a **caching layer** (e.g., Redis) for API responses to avoid hitting rate limits, and a **background polling mechanism** (scheduled jobs or a lightweight worker) to periodically fetch new mentions. The infrastructure team can provision these, but the development team will need to integrate them.

---

## AI Preliminary Decomposition (EPICs and User Stories)

Thank you for the detailed answers. Based on the context and your responses, here is my **preliminary decomposition** of the SocialConnect feature into EPICs and User Stories before I proceed with the full estimation.

### Proposed EPICs

| Epic ID | Epic Name | Description |
|---------|-----------|-------------|
| E-1 | **API Integration & Backend Services** | Build backend services to authenticate with Platform X and Y APIs, fetch mentions, normalize data, and handle rate limits/errors. |
| E-2 | **Admin Configuration & Settings** | Allow Project Admins to configure keywords/hashtags and manage OAuth connections to each platform. |
| E-3 | **SocialConnect Feed UI** | Develop the front-end "SocialConnect" tab with feed display, filtering (platform, date range), and deep-linking to original posts. |
| E-4 | **Background Polling & Caching** | Implement scheduled background jobs to poll APIs periodically and cache results in Redis for performance and rate-limit compliance. |
| E-5 | **Testing, Security & Compliance** | End-to-end testing, security review of OAuth token handling, data privacy compliance, and UAT. |

### High-Level User Stories per Epic

**Epic E-1 — API Integration & Backend Services:**
- US-1.1: As a system, I need to authenticate with Platform X API via OAuth 2.0 so EPAMSuite can access mentions data.
- US-1.2: As a system, I need to authenticate with Platform Y API via OAuth 2.0 so EPAMSuite can access mentions data.
- US-1.3: As a system, I need to fetch posts/mentions from Platform X matching configured keywords.
- US-1.4: As a system, I need to fetch posts/mentions from Platform Y matching configured keywords.
- US-1.5: As a system, I need to normalize data from both platforms into a unified internal model.
- US-1.6: As a system, I need to handle API errors and rate-limit responses gracefully (retry, circuit breaker, logging).

**Epic E-2 — Admin Configuration & Settings:**
- US-2.1: As a Project Admin, I want to add/edit/remove keywords and hashtags to monitor.
- US-2.2: As a Project Admin, I want to connect EPAMSuite to our Platform X account via OAuth.
- US-2.3: As a Project Admin, I want to connect EPAMSuite to our Platform Y account via OAuth.
- US-2.4: As a Project Admin, I want to disconnect a platform account and revoke tokens.
- US-2.5: As a Project Admin, I want to see the connection status for each platform (connected/disconnected/error).

**Epic E-3 — SocialConnect Feed UI:**
- US-3.1: As a team member, I want to see a "SocialConnect" tab in the project navigation.
- US-3.2: As a team member, I want to see a feed of recent social media mentions matching project keywords.
- US-3.3: As a team member, I want to filter the feed by platform (Platform X / Y / All).
- US-3.4: As a team member, I want to filter the feed by date range (last 24h, 7 days, 30 days).
- US-3.5: As a team member, I want to click a post and be taken to the original post on the respective platform.
- US-3.6: As a team member, I want the feed to paginate or infinite-scroll for large result sets.

**Epic E-4 — Background Polling & Caching:**
- US-4.1: As a system, I need to periodically poll Platform X and Y APIs for new mentions.
- US-4.2: As a system, I need to cache API responses in Redis so the feed loads fast and rate limits are respected.
- US-4.3: As a system, I need to deduplicate mentions across polling cycles.

**Epic E-5 — Testing, Security & Compliance:**
- US-5.1: As a QA Engineer, I want comprehensive test coverage (unit, integration, E2E) for SocialConnect.
- US-5.2: As a Security Lead, I want OAuth tokens stored encrypted and access-controlled.
- US-5.3: As a PO/BA, I want to verify API usage complies with Platform X and Y Terms of Service.
- US-5.4: As a QA Engineer, I want to conduct UAT with stakeholders before release.

### My Feedback on the Decomposition

The decomposition looks good and covers all the high-level requirements. A few notes:
- Epic E-1 is the heaviest — two separate API adapters with different data models and rate limits.
- Epic E-3 should be relatively straightforward given the mature design system.
- Epic E-4 is critical for production readiness — without caching, we'd hit rate limits quickly.
- Please proceed with the full estimation including story points, T-Shirt sizing, PERT for BA activities, risks, assumptions, and technical complexities.

---

*Proceed to Part 2 for the final deliverables (detailed estimations, PERT analysis, risks, assumptions).*
