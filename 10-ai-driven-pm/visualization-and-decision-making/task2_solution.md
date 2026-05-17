# Practical Task: Estimation — Part 2 (Final Deliverables)

---

## 1. EPICs

| Epic ID | Epic Name | Description |
|---------|-----------|-------------|
| E-1 | **API Integration & Backend Services** | Build backend services for authenticating with Platform X and Y APIs, fetching social media mentions, caching results, and managing rate limits. |
| E-2 | **Admin Configuration & Settings** | Enable Project Admins to configure keywords/hashtags and manage OAuth connections to Platform X and Y within project settings. |
| E-3 | **SocialConnect Feed UI** | Develop the front-end "SocialConnect" tab/section with feed display, filtering, and deep-linking to original posts. |
| E-4 | **Background Data Polling & Caching** | Implement scheduled background jobs to periodically fetch new mentions and cache results to optimize performance and API rate limit compliance. |
| E-5 | **Testing, Security & Compliance** | End-to-end testing, security review (OAuth token handling, data privacy), and compliance with platform API terms of service. |

---

## 2. User Stories

### Epic E-1: API Integration & Backend Services

| Story ID | User Story | Acceptance Criteria | Story Points |
|----------|-----------|-------------------|--------------|
| US-1.1 | As a **system**, I need to authenticate with Platform X API using OAuth 2.0 so that EPAMSuite can access public mentions data. | OAuth flow completes successfully; tokens are stored securely; token refresh works automatically. | 8 |
| US-1.2 | As a **system**, I need to authenticate with Platform Y API using OAuth 2.0 so that EPAMSuite can access public mentions data. | OAuth flow completes successfully; tokens are stored securely; token refresh works automatically. | 8 |
| US-1.3 | As a **system**, I need to fetch posts/mentions from Platform X matching configured keywords so that the feed can be populated. | API adapter fetches posts by keyword; handles pagination; respects rate limits; returns normalized data. | 8 |
| US-1.4 | As a **system**, I need to fetch posts/mentions from Platform Y matching configured keywords so that the feed can be populated. | API adapter fetches posts by keyword; handles pagination; respects rate limits; returns normalized data. | 8 |
| US-1.5 | As a **system**, I need to normalize data from Platform X and Y into a unified internal model so that the UI can render a consistent feed. | Common data model defined; adapters transform platform-specific responses; unit tests pass. | 5 |
| US-1.6 | As a **system**, I need to handle API errors and rate-limit responses gracefully so that the service degrades without crashing. | Retry logic with exponential backoff; circuit breaker pattern; error logged and surfaced to admin UI. | 5 |

### Epic E-2: Admin Configuration & Settings

| Story ID | User Story | Acceptance Criteria | Story Points |
|----------|-----------|-------------------|--------------|
| US-2.1 | As a **Project Admin**, I want to add/edit/remove keywords and hashtags to monitor so that only relevant mentions are tracked. | CRUD operations for keywords; validation (max length, max count); changes persist immediately. | 5 |
| US-2.2 | As a **Project Admin**, I want to connect EPAMSuite to our Platform X account via OAuth so that the system can fetch mentions. | OAuth connect button; redirect flow; success/error feedback; token stored securely per project. | 8 |
| US-2.3 | As a **Project Admin**, I want to connect EPAMSuite to our Platform Y account via OAuth so that the system can fetch mentions. | OAuth connect button; redirect flow; success/error feedback; token stored securely per project. | 8 |
| US-2.4 | As a **Project Admin**, I want to disconnect a platform account so that EPAMSuite stops fetching data from it. | Disconnect button; confirmation dialog; tokens revoked; feed for that platform clears gracefully. | 3 |
| US-2.5 | As a **Project Admin**, I want to see the connection status for each platform (connected/disconnected/error) so that I can troubleshoot issues. | Status indicator in settings panel; last sync timestamp; error message if token expired. | 3 |

### Epic E-3: SocialConnect Feed UI

| Story ID | User Story | Acceptance Criteria | Story Points |
|----------|-----------|-------------------|--------------|
| US-3.1 | As a **team member**, I want to see a "SocialConnect" tab in my project navigation so that I can access the social media feed. | Tab appears in project nav for all project members; respects existing design system; route works. | 3 |
| US-3.2 | As a **team member**, I want to see a feed of recent social media mentions matching my project's keywords so that I can stay informed. | Feed loads posts in reverse chronological order; shows platform icon, author, timestamp, text snippet; loading/empty states handled. | 8 |
| US-3.3 | As a **team member**, I want to filter the feed by platform (Platform X / Platform Y / All) so that I can focus on one source at a time. | Toggle filter; feed updates in real-time; filter state persists during session. | 3 |
| US-3.4 | As a **team member**, I want to filter the feed by date range (last 24h, last 7 days, last 30 days) so that I can see recent or historical mentions. | Date range selector; feed re-fetches/filters accordingly; default is "last 7 days." | 5 |
| US-3.5 | As a **team member**, I want to click on a post in the feed and be taken to the original post on Platform X or Y so that I can see the full context. | Each post card has a "View Original" link; opens in new browser tab; correct URL generated. | 2 |
| US-3.6 | As a **team member**, I want the feed to paginate or infinite-scroll so that I can browse through many mentions without performance issues. | Pagination or infinite scroll implemented; smooth UX; no duplicate posts shown. | 5 |

### Epic E-4: Background Data Polling & Caching

| Story ID | User Story | Acceptance Criteria | Story Points |
|----------|-----------|-------------------|--------------|
| US-4.1 | As a **system**, I need to periodically poll Platform X and Y APIs for new mentions so that the feed stays up-to-date. | Background worker runs on configurable schedule (e.g., every 15 min); fetches incrementally; handles failures gracefully. | 8 |
| US-4.2 | As a **system**, I need to cache API responses (e.g., in Redis) so that feed rendering is fast and API rate limits are not exceeded. | Cache populated on each poll; feed reads from cache; TTL configured; cache invalidation on keyword change. | 8 |
| US-4.3 | As a **system**, I need to deduplicate mentions across polling cycles so that users don't see duplicate posts in the feed. | Deduplication by unique post ID; tested with overlapping result sets. | 3 |

### Epic E-5: Testing, Security & Compliance

| Story ID | User Story | Acceptance Criteria | Story Points |
|----------|-----------|-------------------|--------------|
| US-5.1 | As a **QA Engineer**, I want comprehensive test coverage for SocialConnect (unit, integration, E2E) so that we ship a reliable feature. | ≥80% unit test coverage; integration tests for API adapters with mocks; E2E test for full user journey. | 8 |
| US-5.2 | As a **Security Lead**, I want OAuth tokens to be stored encrypted and access-controlled so that we comply with security policies. | Tokens encrypted at rest; access scoped to the owning project; audit logging for token operations. | 5 |
| US-5.3 | As a **PO/BA**, I want to verify that our usage of Platform X and Y APIs complies with their Terms of Service so that we avoid legal risks. | ToS reviewed; data retention policies enforced; no prohibited use cases; documentation updated. | 3 |
| US-5.4 | As a **QA Engineer**, I want to perform UAT with stakeholders so that we confirm the feature meets business expectations. | UAT plan created; UAT sessions conducted; sign-off received. | 5 |

---

## 3. Story Point Summary

| Epic | Total Story Points |
|------|-------------------|
| E-1: API Integration & Backend Services | 42 |
| E-2: Admin Configuration & Settings | 27 |
| E-3: SocialConnect Feed UI | 26 |
| E-4: Background Data Polling & Caching | 19 |
| E-5: Testing, Security & Compliance | 21 |
| **Grand Total** | **135** |

---

## 4. Overall Feature Effort Estimation (T-Shirt Sizing)

| Size | Story Point Range | Sprints (at 60 pts/sprint) |
|------|------------------|---------------------------|
| S (Small) | ≤ 40 pts | 1 sprint |
| M (Medium) | 41–80 pts | 1–2 sprints |
| **L (Large)** | **81–160 pts** | **2–3 sprints** |
| XL (Extra-Large) | > 160 pts | 4+ sprints |

### 🏷️ Overall T-Shirt Size: **LARGE (L)**

**Rationale:**
- Total estimated effort is **~135 story points**.
- At a team velocity of **60 points/sprint** (2-week sprints), this translates to approximately **2.5 sprints (~5 weeks)**.
- Adding a buffer for unknowns (new API integrations, rate-limit edge cases, shared resource availability), a realistic delivery window is **3 sprints (6 weeks)**.
- The feature involves meaningful backend work (two API integrations, caching, polling), moderate front-end work (leveraging existing design system), and cross-cutting concerns (security, compliance, testing).

---

## 5. BA Activities Estimation (PERT)

The Business Analyst (PO/BA) activities include: requirements elicitation and documentation, API research, stakeholder communication, acceptance criteria definition, UAT coordination, and backlog management.

### PERT Formula

$$E = \frac{O + 4M + P}{6}$$

$$\sigma = \frac{P - O}{6}$$

Where: $O$ = Optimistic, $M$ = Most Likely, $P$ = Pessimistic

### BA Activity Breakdown

| BA Activity | Optimistic (O) | Most Likely (M) | Pessimistic (P) | PERT Estimate (E) | Std Dev (σ) |
|-------------|:--------------:|:---------------:|:---------------:|:-----------------:|:-----------:|
| Requirements elicitation & stakeholder workshops | 2 days | 4 days | 7 days | 4.2 days | 0.83 |
| Platform X & Y API research and documentation | 2 days | 3 days | 6 days | 3.3 days | 0.67 |
| User story writing & acceptance criteria definition | 3 days | 5 days | 8 days | 5.2 days | 0.83 |
| UI/UX collaboration & wireframe review | 1 day | 2 days | 4 days | 2.2 days | 0.50 |
| Backlog grooming & sprint planning support | 2 days | 3 days | 5 days | 3.2 days | 0.50 |
| UAT planning, execution & sign-off coordination | 2 days | 3 days | 5 days | 3.2 days | 0.50 |
| Data privacy & compliance review support | 1 day | 2 days | 4 days | 2.2 days | 0.50 |
| **Total BA Effort** | **13 days** | **22 days** | **39 days** | **23.5 days** | — |

### Combined Standard Deviation

$$\sigma_{total} = \sqrt{\sum \sigma_i^2} = \sqrt{0.83^2 + 0.67^2 + 0.83^2 + 0.50^2 + 0.50^2 + 0.50^2 + 0.50^2} \approx 1.67 \text{ days}$$

### BA Effort Summary

| Metric | Value |
|--------|-------|
| **PERT Estimate** | **~23.5 working days (~4.7 weeks)** |
| **Optimistic Range** (E - σ) | ~21.8 days |
| **Pessimistic Range** (E + σ) | ~25.2 days |
| **95% Confidence Interval** (E ± 2σ) | 20.2 – 26.8 days |

> The BA will be engaged throughout the full delivery cycle (~6 weeks), with peak effort during the first 2 weeks (requirements, API research, story writing) and then a steady supporting role during development sprints, ramping up again during UAT.

---

## 6. Risks

| # | Risk | Likelihood | Impact | Mitigation |
|---|------|-----------|--------|------------|
| R1 | Platform X or Y API changes (breaking changes, deprecations) during development. | Medium | High | Pin to specific API versions; subscribe to platform developer changelogs; build adapter abstraction layer. |
| R2 | API rate limits are more restrictive than expected, limiting data freshness. | Medium | Medium | Implement aggressive caching; use webhooks if available; design polling intervals to stay well under limits. |
| R3 | OAuth token expiration/revocation causes silent failures in background polling. | Medium | Medium | Implement token health checks; alerting on auth failures; auto-refresh logic; admin notification. |
| R4 | Shared resources (Architect, UI/UX Designer) are unavailable when needed. | Medium | Medium | Schedule shared resource time early; front-load design work in Sprint 1; have developer fallback for minor UI decisions. |
| R5 | Data privacy regulations (GDPR, etc.) impose unexpected constraints on storing social media data. | Low | High | Engage legal/compliance team early; minimize stored PII; implement data retention policies from the start. |
| R6 | Platform API approval/access takes longer than expected. | Medium | High | Apply for API access in Sprint 0; have sandbox/mock data ready for development to proceed in parallel. |

---

## 7. Assumptions

| # | Assumption |
|---|-----------|
| A1 | Platform X and Y APIs are publicly available and EPAMSuite can obtain developer access within 1–2 weeks. |
| A2 | The existing EPAMSuite design system components (tabs, cards, filters, date pickers) are sufficient — no new design system components are needed. |
| A3 | The team's existing microservice infrastructure supports adding a new service without major DevOps work. |
| A4 | Redis (or equivalent caching solution) is available or can be provisioned by the infrastructure team within Sprint 1. |
| A5 | The team has access to Platform X and Y sandbox/test environments for development and testing. |
| A6 | Data privacy and compliance requirements are standard and won't require custom legal review beyond initial assessment. |
| A7 | Only English-language keywords/hashtags need to be supported in this phase. |
| A8 | The feature is behind a feature flag and can be rolled out incrementally. |

---

## 8. Technical Complexities

| # | Complexity Area | Description | Impact |
|---|----------------|-------------|--------|
| TC1 | **Dual API Integration** | Platform X and Y have different API designs, authentication flows, data models, rate limits, and pagination strategies. Two separate adapters must be built and maintained. | High — significant backend effort |
| TC2 | **Rate Limit Management** | Both platforms enforce strict rate limits. The caching and polling strategy must be carefully designed to avoid throttling while maintaining data freshness. | Medium — requires careful architecture |
| TC3 | **OAuth Token Lifecycle** | Managing token storage (encrypted), refresh, revocation, and multi-project scoping adds complexity to the auth layer. | Medium — security-sensitive |
| TC4 | **Real-time vs. Polling Trade-off** | Social media APIs may not support webhooks/streaming for keyword monitoring, requiring a polling approach with deduplication logic. | Medium — affects data freshness UX |
| TC5 | **Data Normalization** | Merging posts from two platforms into a single, chronologically sorted feed requires a well-designed unified data model and careful timestamp handling (time zones). | Low–Medium |
| TC6 | **Scalability** | If many projects configure many keywords, the total polling load can grow significantly. The system must scale horizontally. | Low for Phase 1, High long-term |

---

## 9. Delivery Timeline (Recommended)

| Sprint | Focus | Key Deliverables |
|--------|-------|-----------------|
| **Sprint 0** (Prep) | API access, architecture design, UX wireframes | API developer accounts approved; architecture document; wireframes signed off; backlog groomed |
| **Sprint 1** | Backend API adapters + Admin settings UI | OAuth flows for Platform X & Y; keyword config CRUD; API fetching (Platform X); backend tests |
| **Sprint 2** | Feed UI + Caching + Polling | SocialConnect tab; feed display; filtering; background polling; Redis caching; API fetching (Platform Y) |
| **Sprint 3** | Integration, E2E testing, UAT, hardening | E2E tests; security review; UAT; bug fixes; performance testing; documentation; release |

**Estimated Total Duration: ~6–8 weeks** (including Sprint 0 preparation)

---

## 10. Summary

| Dimension | Estimate |
|-----------|----------|
| **Overall Feature Size** | **Large (L)** — ~135 story points |
| **Delivery Duration** | ~3 sprints + Sprint 0 prep (~6–8 weeks) |
| **BA Effort (PERT)** | ~23.5 working days (~4.7 weeks) |
| **BA Effort (95% CI)** | 20.2 – 26.8 working days |
| **Key Risks** | API access delays, rate limit constraints, shared resource availability |
| **Critical Path** | API access approval → Backend adapters → Feed UI → Testing/UAT |
