# User Story Generation: AI Courses Catalog Platform

## Prompt Used in EPAM DIAL (GPT-4o)

> I am sharing the feature decomposition results for an AI Courses Catalog platform below. For **each sub-feature**, please generate a detailed user story using the following template:
>
> **User Story Template:**
> - **ID:** US-[Feature#]-[SubFeature#]
> - **Title:** Short imperative title
> - **User Story:** As a [role], I want to [action], so that [benefit].
> - **Description:** 2–3 sentences providing additional context.
> - **Acceptance Criteria:**
>   - Given / When / Then format (at least 3 criteria)
> - **Priority:** Must Have / Should Have / Could Have / Won't Have (MoSCoW)
> - **Story Points:** Fibonacci estimate (1, 2, 3, 5, 8, 13)
> - **Notes / Assumptions:** Any relevant notes or open questions.
>
> Generate one user story per sub-feature. Use the feature decomposition below as your input.
>
> [Feature decomposition pasted here — see feature-decomposition/task1_solution.md]

---

## Outcome of Prompt Execution

---

## Feature 1: Course Discovery and Browsing

---

### US-1-1 · Course Catalog Grid View

**Title:** View all available AI courses in a grid layout

**User Story:**
As a **Learner**, I want to see all available AI courses displayed in a responsive card grid, so that I can quickly scan the full catalog and identify courses of interest.

**Description:**
The catalog grid is the primary landing surface of the platform. It must present courses in a uniform, scannable card format that works across desktop and mobile viewports. Loading performance is critical to ensure a smooth first impression.

**Acceptance Criteria:**
- **Given** I open the AI Courses Catalog page, **When** the page loads, **Then** I see a grid of course cards displaying up to 24 courses per page within 2 seconds.
- **Given** I am on a desktop browser, **When** the catalog renders, **Then** courses are shown in a multi-column grid (3–4 columns).
- **Given** I am on a mobile device, **When** the catalog renders, **Then** the grid collapses to a single-column layout without horizontal scrolling.
- **Given** no courses exist matching current filters, **When** the grid loads, **Then** an empty-state message is displayed with a suggestion to reset filters.

**Priority:** Must Have
**Story Points:** 5
**Notes / Assumptions:** Assumes back-end pagination API is available. Initial page size is 24 cards.

---

### US-1-2 · Course Card Summary

**Title:** Display key course metadata on each course card

**User Story:**
As a **Learner**, I want to see essential course information on each card without opening the course, so that I can evaluate relevance and decide whether to enroll.

**Description:**
Each card must show the course title, category tag, difficulty badge, estimated duration, instructor name, star rating, and learner enrollment count. Visual hierarchy should make the title and CTA button the most prominent elements.

**Acceptance Criteria:**
- **Given** a course card is rendered, **When** I view it, **Then** I can see: title, category tag, difficulty badge, duration, instructor name, star rating (e.g., ★★★★☆ 4.2), and learner count.
- **Given** a course thumbnail image is unavailable, **When** the card renders, **Then** a branded placeholder image is shown instead.
- **Given** a course title exceeds the card width, **When** the card renders, **Then** the title is truncated with an ellipsis and the full title is accessible via tooltip on hover.
- **Given** a course has a difficulty level, **When** the badge is rendered, **Then** it is color-coded (Beginner = green, Intermediate = orange, Advanced = red).

**Priority:** Must Have
**Story Points:** 3
**Notes / Assumptions:** Rating and learner count are periodically refreshed (every 15–30 min), not real-time.

---

### US-1-3 · Results Count Display

**Title:** Show the number of courses matching current filters

**User Story:**
As a **Learner**, I want to see how many courses match my current search and filter state, so that I can understand the breadth of results and adjust filters if needed.

**Description:**
A results count label above the grid (e.g., "Showing 24 of 87 courses") helps learners gauge whether filters are too narrow or too broad. It should update in sync with any search or filter change.

**Acceptance Criteria:**
- **Given** I open the catalog with no filters applied, **When** the page loads, **Then** I see a label showing the total number of available courses (e.g., "Showing 24 of 87 courses").
- **Given** I apply one or more filters, **When** the grid updates, **Then** the results count label updates simultaneously to reflect the filtered count.
- **Given** no courses match the active filters, **When** the grid renders, **Then** the label shows "0 courses found" and the grid shows the empty state.

**Priority:** Should Have
**Story Points:** 2
**Notes / Assumptions:** Count reflects server-side total; client-side display shows items on the current page vs. total.

---

### US-1-4 · Course Detail Navigation

**Title:** Navigate to a course detail page from the catalog card

**User Story:**
As a **Learner**, I want to click on a course card to open its detail page, so that I can read full course information before deciding to enroll.

**Description:**
Clicking anywhere on the card body (excluding the CTA button and bookmark icon) navigates the user to the Course Detail page. This page provides the full syllabus, instructor bio, reviews, and enrollment options.

**Acceptance Criteria:**
- **Given** I click on a course card body, **When** the click is registered, **Then** I am navigated to the Course Detail page for that course.
- **Given** I click the "Enroll Now" button on a card, **When** the click is registered, **Then** the enrollment flow is triggered instead of navigating to the detail page.
- **Given** I click the bookmark icon on a card, **When** the click is registered, **Then** the bookmark is toggled and I remain on the catalog page.
- **Given** I navigate back from the Course Detail page, **When** I return to the catalog, **Then** my previous scroll position and active filters are preserved.

**Priority:** Must Have
**Story Points:** 3
**Notes / Assumptions:** Session-level state preservation (scroll position, filters) is required.

---

## Feature 2: Search

---

### US-2-1 · Keyword-Based Search

**Title:** Search for courses by keyword

**User Story:**
As a **Learner**, I want to type a keyword into the search bar to find relevant courses, so that I can quickly locate specific topics or technologies without manually browsing the full catalog.

**Description:**
The search bar is positioned prominently in the header. It accepts free-text input and filters the course grid to return courses whose title, category, or description match the entered term.

**Acceptance Criteria:**
- **Given** I type a keyword into the search bar, **When** I have entered 2 or more characters, **Then** the course grid updates to show only courses matching the keyword.
- **Given** I clear the search bar, **When** the input is empty, **Then** the full unfiltered catalog is restored.
- **Given** no courses match the keyword, **When** the search executes, **Then** an empty-state message "No courses found for '[keyword]'" is shown.
- **Given** I enter a keyword, **When** results are returned, **Then** the matching term is visually highlighted within course titles.

**Priority:** Must Have
**Story Points:** 5
**Notes / Assumptions:** Search is case-insensitive. Searches course title, category, and short description fields.

---

### US-2-2 · Live Search Results

**Title:** Display search results dynamically as the user types

**User Story:**
As a **Learner**, I want search results to update automatically as I type, so that I can see relevant courses in real time without pressing Enter or a search button.

**Description:**
Live search improves efficiency by giving instant feedback on keyword relevance. Results must appear within 300 ms of the user pausing input to feel responsive. A debounce mechanism prevents excessive API calls.

**Acceptance Criteria:**
- **Given** I am typing in the search bar, **When** I pause for 300 ms after typing 2+ characters, **Then** the course grid updates without a full page reload.
- **Given** I type rapidly, **When** multiple keystrokes occur within 300 ms, **Then** only the final input state triggers a search (debounce applied).
- **Given** the search API is slow, **When** results take more than 300 ms to return, **Then** a loading indicator is shown in the grid area.
- **Given** I am using the keyboard, **When** I press Escape while the search bar is focused, **Then** the search bar is cleared and focus is returned.

**Priority:** Must Have
**Story Points:** 3
**Notes / Assumptions:** Debounce interval is 300 ms. Leverages client-side filtering where catalog is small enough; falls back to API search for large catalogs.

---

## Feature 3: Filtering

---

### US-3-1 · Category Filter

**Title:** Filter courses by subject category

**User Story:**
As a **Learner**, I want to filter the course catalog by subject category, so that I can view only the courses relevant to my area of interest.

**Description:**
The category filter presents available domains (e.g., Generative AI, Machine Learning, NLP, Computer Vision, Data Science) as selectable options. Selecting a category instantly updates the grid.

**Acceptance Criteria:**
- **Given** I open the category filter dropdown, **When** it renders, **Then** I see all available categories with course counts next to each option.
- **Given** I select a category, **When** the selection is applied, **Then** the grid updates immediately to show only courses in that category.
- **Given** I select a category that yields no results, **When** the grid updates, **Then** an empty-state message is shown.
- **Given** I deselect a category, **When** the filter is cleared, **Then** the grid restores results without that category constraint.

**Priority:** Must Have
**Story Points:** 3
**Notes / Assumptions:** Single-select category filter in this phase. Multi-select can be added in a later iteration.

---

### US-3-2 · Difficulty Level Filter

**Title:** Filter courses by difficulty level

**User Story:**
As a **Learner**, I want to filter courses by difficulty level (Beginner, Intermediate, Advanced), so that I can find courses appropriate to my current skill level.

**Description:**
The difficulty filter allows learners to self-select their proficiency and view only matching courses, reducing decision fatigue for users who know their experience level.

**Acceptance Criteria:**
- **Given** I open the difficulty filter, **When** it renders, **Then** I see three options: Beginner, Intermediate, and Advanced, each with a course count.
- **Given** I select "Beginner", **When** the filter is applied, **Then** only beginner-level courses are shown in the grid.
- **Given** I select multiple difficulty levels, **When** the filter is applied, **Then** courses matching any of the selected levels are shown (OR logic within the filter).
- **Given** I clear the difficulty filter, **When** the filter is removed, **Then** the grid restores all difficulty levels.

**Priority:** Must Have
**Story Points:** 3
**Notes / Assumptions:** Difficulty levels are defined by the course author at creation time and stored as an enum.

---

### US-3-3 · Duration Filter

**Title:** Filter courses by estimated duration

**User Story:**
As a **Learner**, I want to filter courses by their estimated duration, so that I can find courses that fit my available time.

**Description:**
Duration ranges (e.g., under 2 hours, 2–5 hours, 5–10 hours, 10+ hours) allow time-constrained learners to quickly discover short-form content or commit to longer learning paths.

**Acceptance Criteria:**
- **Given** I open the duration filter, **When** it renders, **Then** I see duration range options with course counts.
- **Given** I select a duration range, **When** the filter is applied, **Then** only courses whose total duration falls within the selected range are shown.
- **Given** I select multiple duration ranges, **When** the filter is applied, **Then** courses falling within any selected range are shown.
- **Given** I clear the duration filter, **When** the filter is removed, **Then** all courses are shown regardless of duration.

**Priority:** Should Have
**Story Points:** 3
**Notes / Assumptions:** Duration is stored in minutes at the course level and grouped into ranges for display.

---

### US-3-4 · Multi-Filter Combination

**Title:** Apply multiple filters simultaneously

**User Story:**
As a **Learner**, I want to apply multiple filters at the same time (e.g., category + difficulty + duration), so that I can precisely narrow the catalog to exactly the courses that meet all my criteria.

**Description:**
Filters combine with AND logic across different filter dimensions, allowing progressive refinement. For example, a user can filter by "Generative AI" AND "Beginner" AND "under 2 hours" to find highly targeted results.

**Acceptance Criteria:**
- **Given** I have applied a category filter, **When** I also apply a difficulty filter, **Then** the grid shows only courses that match both the category AND the difficulty (AND logic across filter types).
- **Given** I apply filters that result in zero matches, **When** the grid updates, **Then** an empty state is shown with a "Reset all filters" button.
- **Given** I apply multiple filters, **When** I view the filter bar, **Then** all active selections are visually indicated simultaneously.
- **Given** I reload the page with active filters, **When** the page restores session state, **Then** the same filters remain active.

**Priority:** Should Have
**Story Points:** 5
**Notes / Assumptions:** Session-level filter persistence is required. Cross-filter AND logic; within-filter OR logic.

---

### US-3-5 · Active Filter Chips

**Title:** Display and remove active filters as chips

**User Story:**
As a **Learner**, I want to see my currently active filters as removable tags, so that I can quickly understand what filters are applied and remove individual ones without resetting everything.

**Description:**
Active filter chips provide transparency and control. Each chip shows the filter label and an × remove button. A "Clear all" button resets the entire filter state at once.

**Acceptance Criteria:**
- **Given** I apply a filter, **When** the filter is active, **Then** a chip with the filter label appears below the filter bar.
- **Given** I click the × on a filter chip, **When** the chip is dismissed, **Then** that specific filter is removed and the grid updates accordingly.
- **Given** multiple filters are active, **When** I click "Clear all filters", **Then** all chips are removed and the full unfiltered catalog is restored.
- **Given** no filters are applied, **When** I view the filter area, **Then** no chips are shown and the "Clear all" button is hidden.

**Priority:** Should Have
**Story Points:** 2
**Notes / Assumptions:** Chips are rendered below the filter bar in a scrollable row if many are active simultaneously.

---

## Feature 4: Sorting

---

### US-4-1 · Sort by Most Popular

**Title:** Sort courses by popularity

**User Story:**
As a **Learner**, I want to sort the course catalog by popularity, so that I can discover the courses most learners have found valuable.

**Description:**
Popularity is determined by total enrollment count. This sort option surfaces courses with the highest demand, helping indecisive learners follow the wisdom of the crowd.

**Acceptance Criteria:**
- **Given** I select "Most Popular" from the Sort By dropdown, **When** the sort is applied, **Then** courses are reordered by descending enrollment count.
- **Given** two courses have identical enrollment counts, **When** the sort is applied, **Then** they are ordered alphabetically as a tiebreaker.
- **Given** I change the sort selection, **When** the new sort is applied, **Then** the grid reorders within 500 ms.
- **Given** I apply a sort and then add a filter, **When** the filtered results load, **Then** the sort order is preserved within the filtered set.

**Priority:** Should Have
**Story Points:** 2
**Notes / Assumptions:** Enrollment count is periodically cached; not real-time.

---

### US-4-2 · Sort by Highest Rated

**Title:** Sort courses by learner rating

**User Story:**
As a **Learner**, I want to sort courses by their average rating, so that I can prioritize the most highly reviewed content.

**Description:**
Rating-based sorting helps learners identify high-quality courses. Courses with fewer than a minimum number of ratings (e.g., 5) may be ranked below rated courses to avoid misleading single-review outliers.

**Acceptance Criteria:**
- **Given** I select "Highest Rated" from the Sort By dropdown, **When** the sort is applied, **Then** courses are reordered by descending average star rating.
- **Given** a course has fewer than 5 ratings, **When** it is sorted alongside rated courses, **Then** it is ranked after courses with sufficient ratings.
- **Given** I select this sort, **When** the grid updates, **Then** it reorders within 500 ms.

**Priority:** Should Have
**Story Points:** 2
**Notes / Assumptions:** Rating data is the same periodically cached average shown on the card.

---

### US-4-3 · Sort by Newest

**Title:** Sort courses by publication date

**User Story:**
As a **Learner**, I want to sort courses by how recently they were published or updated, so that I can discover the latest content on emerging AI topics.

**Description:**
Sorting by recency helps learners who want up-to-date material. The sort is based on the course's publication date or last significant update date, whichever is more recent.

**Acceptance Criteria:**
- **Given** I select "Newest" from the Sort By dropdown, **When** the sort is applied, **Then** courses are reordered by descending publication/update date.
- **Given** a course was recently updated, **When** I sort by Newest, **Then** it appears ahead of older, unmodified courses.
- **Given** I select this sort, **When** the grid updates, **Then** it reorders within 500 ms.

**Priority:** Could Have
**Story Points:** 2
**Notes / Assumptions:** "Updated" date reflects significant content changes, not minor metadata edits.

---

### US-4-4 · Sort Alphabetically

**Title:** Sort courses alphabetically by title

**User Story:**
As a **Learner**, I want to sort courses alphabetically (A–Z or Z–A), so that I can manually browse or locate a specific course by name.

**Description:**
Alphabetical sorting is especially useful when a learner knows the name of the course they are looking for or when they want a predictable, consistent ordering for browsing.

**Acceptance Criteria:**
- **Given** I select "A–Z" from the Sort By dropdown, **When** the sort is applied, **Then** courses are ordered alphabetically by title from A to Z.
- **Given** I select "Z–A", **When** the sort is applied, **Then** courses are ordered in reverse alphabetical order.
- **Given** a course title begins with a number, **When** sorted A–Z, **Then** it appears before alphabetical titles (numeric-first ordering).

**Priority:** Could Have
**Story Points:** 1
**Notes / Assumptions:** Sort is case-insensitive.

---

## Feature 5: Course Enrollment and Access

---

### US-5-1 · One-Click Enrollment

**Title:** Enroll in a course directly from the catalog card

**User Story:**
As a **Learner**, I want to enroll in a course by clicking a button on its card, so that I can start learning without navigating to the course detail page first.

**Description:**
The "Enroll Now" button on unenrolled course cards provides the fastest path to enrollment. It reduces the number of steps required and improves conversion from browsing to learning.

**Acceptance Criteria:**
- **Given** I am not enrolled in a course, **When** I view its card, **Then** an "Enroll Now" button is visible.
- **Given** I click "Enroll Now", **When** the click is registered, **Then** an enrollment confirmation modal appears.
- **Given** I confirm enrollment in the modal, **When** enrollment is processed, **Then** a success toast notification appears and the card button updates to "Start Course".
- **Given** enrollment fails due to a system error, **When** the error occurs, **Then** an error message is shown and no enrollment is recorded.
- **Given** I am already enrolled, **When** I view the card, **Then** the "Enroll Now" button is not shown.

**Priority:** Must Have
**Story Points:** 5
**Notes / Assumptions:** Enrollment is idempotent; multiple clicks must not create duplicate records.

---

### US-5-2 · Enrollment Confirmation

**Title:** Confirm enrollment via a modal dialog

**User Story:**
As a **Learner**, I want to see a confirmation dialog before enrollment is finalized, so that I can avoid accidental enrollments.

**Description:**
The confirmation modal displays the course name and a brief summary, along with "Confirm" and "Cancel" buttons. This creates a deliberate pause point that reduces accidental enrollments.

**Acceptance Criteria:**
- **Given** I click "Enroll Now" on a card, **When** the modal opens, **Then** I see the course title, a short description, and "Confirm" and "Cancel" buttons.
- **Given** the modal is open, **When** I click "Cancel" or press Escape, **Then** the modal closes and no enrollment is created.
- **Given** the modal is open, **When** I click "Confirm", **Then** enrollment is submitted and the modal closes on success.
- **Given** the modal is open, **When** I click outside the modal, **Then** the modal closes without enrolling.

**Priority:** Must Have
**Story Points:** 2
**Notes / Assumptions:** Modal is accessible — focus trapped inside, Escape key dismisses.

---

### US-5-3 · Start Course Action

**Title:** Start an enrolled course from the catalog

**User Story:**
As a **Learner**, I want to click a "Start Course" button on courses I have enrolled in but not yet started, so that I can begin learning immediately from the catalog.

**Description:**
Once enrolled but not yet started, the card CTA changes from "Enroll Now" to "Start Course", navigating the learner directly to the first lesson of the course.

**Acceptance Criteria:**
- **Given** I am enrolled in a course and have not started it, **When** I view its card, **Then** the button reads "Start Course".
- **Given** I click "Start Course", **When** the action is triggered, **Then** I am navigated to the first lesson of the course.
- **Given** I navigate to the first lesson, **When** the lesson page loads, **Then** course progress is initialized and set to "In Progress".

**Priority:** Must Have
**Story Points:** 3
**Notes / Assumptions:** "Not started" is defined as 0% progress recorded.

---

### US-5-4 · Continue Learning

**Title:** Resume an in-progress course from the catalog

**User Story:**
As a **Learner**, I want to click a "Continue" button on courses I have already started, so that I can resume learning from where I left off without navigating through the course structure.

**Description:**
The "Continue" button removes navigation friction by deep-linking directly to the last accessed lesson, respecting the learner's saved position.

**Acceptance Criteria:**
- **Given** I have started a course and made progress, **When** I view its card, **Then** the button reads "Continue".
- **Given** I click "Continue", **When** the action is triggered, **Then** I am navigated to the last lesson I accessed in that course.
- **Given** my last session ended mid-lesson, **When** I click "Continue", **Then** I am taken to the beginning of that lesson (not mid-video).
- **Given** I have completed all lessons but the course is marked "In Progress", **When** I click "Continue", **Then** I am taken to the final lesson or summary page.

**Priority:** Must Have
**Story Points:** 3
**Notes / Assumptions:** Last-accessed lesson is stored per user per course in the progress record.

---

### US-5-5 · Completed Course Access

**Title:** Access a completed course from the catalog

**User Story:**
As a **Learner**, I want to see a "Review Course" option on courses I have completed, so that I can revisit the content or access my certificate.

**Description:**
Completing a course changes the card CTA to "Review Course", linking to the course summary or certificate page. This acknowledges achievement and provides ongoing access to course materials.

**Acceptance Criteria:**
- **Given** I have completed all lessons in a course, **When** I view its card, **Then** the button reads "Review Course" and a completion badge is visible.
- **Given** I click "Review Course", **When** the action is triggered, **Then** I am navigated to the course summary page where I can access the certificate and revisit lessons.
- **Given** a certificate was generated, **When** I reach the summary page, **Then** a "Download Certificate" button is visible and functional.

**Priority:** Should Have
**Story Points:** 3
**Notes / Assumptions:** Certificate generation is handled by a separate service; this story covers UI access only.

---

### US-5-6 · Enrollment State Recognition

**Title:** Show context-appropriate CTA based on enrollment state

**User Story:**
As a **Learner**, I want the action button on each course card to reflect my current enrollment status, so that I always see the most relevant next step without ambiguity.

**Description:**
The card CTA is dynamic and state-driven: "Enroll Now" → "Start Course" → "Continue" → "Review Course". This ensures every card is always actionable and contextually accurate.

**Acceptance Criteria:**
- **Given** I am not enrolled, **When** I view the card, **Then** the CTA reads "Enroll Now".
- **Given** I am enrolled but have 0% progress, **When** I view the card, **Then** the CTA reads "Start Course".
- **Given** I have progress between 1% and 99%, **When** I view the card, **Then** the CTA reads "Continue".
- **Given** I have 100% progress, **When** I view the card, **Then** the CTA reads "Review Course".
- **Given** my enrollment state changes (e.g., I just enrolled), **When** the page re-renders or refreshes, **Then** the CTA updates to reflect the new state.

**Priority:** Must Have
**Story Points:** 3
**Notes / Assumptions:** State is determined by the enrollment and progress API response for the authenticated user.

---

## Feature 6: Progress Tracking

---

### US-6-1 · Per-Card Progress Bar

**Title:** Display a progress bar on in-progress course cards

**User Story:**
As a **Learner**, I want to see a progress bar on each course I have started, so that I can check my completion status at a glance from the catalog.

**Description:**
A horizontal progress bar below the course card body shows the completion percentage (e.g., 65% complete). This visual indicator motivates continued learning and helps learners manage their active courses.

**Acceptance Criteria:**
- **Given** I have started a course and have between 1–99% progress, **When** I view its card, **Then** a progress bar is displayed showing my completion percentage.
- **Given** progress is at 0%, **When** I view the card, **Then** no progress bar is shown (the course is shown as "Not started").
- **Given** progress reaches 100%, **When** the card is rendered, **Then** the progress bar shows as full and a completion indicator replaces it.
- **Given** I complete a lesson, **When** the catalog page is reloaded, **Then** the progress bar reflects the updated completion percentage within 1 minute.
- **Given** I am not enrolled, **When** I view the card, **Then** no progress bar is shown.

**Priority:** Must Have
**Story Points:** 3
**Notes / Assumptions:** Progress is synced from the lesson tracking service. Updates may have up to 1 minute of delay.

---

### US-6-2 · Progress Persistence

**Title:** Persist and restore learner progress across sessions

**User Story:**
As a **Learner**, I want my course progress to be saved automatically and restored when I return, so that I never lose my place regardless of when or where I access the platform.

**Description:**
Progress must be stored server-side against the user's account, not in browser storage, so it is accessible from any device and survives browser restarts or device changes.

**Acceptance Criteria:**
- **Given** I complete a lesson, **When** I log out and log back in, **Then** my progress is shown correctly on the course card.
- **Given** I access the platform from a different device, **When** I view the catalog, **Then** my progress data is identical to what I saw on my previous device.
- **Given** a network interruption occurs during a lesson, **When** connectivity is restored, **Then** my progress up to the last checkpoint is preserved.
- **Given** the progress service is unavailable, **When** I view the catalog, **Then** progress bars are hidden gracefully and no error is shown to the user.

**Priority:** Must Have
**Story Points:** 5
**Notes / Assumptions:** Progress is stored per user per course per lesson on the back end. Client syncs on lesson completion events.

---

## Feature 7: Wishlist / Course Bookmarking

---

### US-7-1 · Bookmark Toggle

**Title:** Add or remove a course from the wishlist via a card icon

**User Story:**
As a **Learner**, I want to bookmark a course by clicking a heart/bookmark icon on its card, so that I can save courses for later without enrolling right away.

**Description:**
The bookmark icon is always visible on course cards. Toggling it adds or removes the course from the user's personal Wishlist with immediate visual feedback (icon fills/unfills with animation).

**Acceptance Criteria:**
- **Given** a course is not in my Wishlist, **When** I click the bookmark icon, **Then** the icon fills (active state), the course is added to my Wishlist, and a toast confirms "Added to Wishlist".
- **Given** a course is already in my Wishlist, **When** I click the bookmark icon, **Then** the icon reverts to inactive state and a toast confirms "Removed from Wishlist".
- **Given** I toggle the bookmark, **When** I reload the page, **Then** the bookmark state is preserved (server-side persistence).
- **Given** I am not authenticated, **When** I click the bookmark icon, **Then** I am redirected to the login page with a prompt to sign in to save courses.

**Priority:** Should Have
**Story Points:** 3
**Notes / Assumptions:** Wishlist is stored server-side per user. Max wishlist size is not limited in this phase.

---

### US-7-2 · Wishlist Access

**Title:** View saved courses from the user profile menu

**User Story:**
As a **Learner**, I want to access my Wishlist from the profile menu, so that I can view all courses I have saved and decide which to enroll in next.

**Description:**
A "My Courses" or "Wishlist" link in the profile dropdown navigates the user to a filtered view of their saved courses, enabling quick retrieval without re-browsing the full catalog.

**Acceptance Criteria:**
- **Given** I open the profile dropdown menu, **When** I click "My Courses" or "Wishlist", **Then** I am navigated to a page or filtered view showing only my bookmarked courses.
- **Given** my Wishlist is empty, **When** I open the Wishlist view, **Then** an empty-state message with a "Browse Courses" CTA is shown.
- **Given** a bookmarked course has been removed from the catalog by an admin, **When** I view my Wishlist, **Then** the removed course is shown with a "No longer available" label.

**Priority:** Should Have
**Story Points:** 3
**Notes / Assumptions:** Wishlist view reuses the catalog card component with a filtered data source.

---

## Feature 8: User Account and Session Management

---

### US-8-1 · User Avatar / Profile Menu

**Title:** Open the profile dropdown menu via the user avatar

**User Story:**
As an **authenticated User**, I want to click my avatar in the top-right corner to open a dropdown menu, so that I can access my profile, courses, settings, and logout quickly from any page.

**Description:**
The avatar dropdown is always accessible in the header. It adapts its menu items based on the user's role, showing role-appropriate options without cluttering the interface.

**Acceptance Criteria:**
- **Given** I am logged in, **When** I click my avatar/initials, **Then** a dropdown menu appears with role-appropriate navigation items.
- **Given** the dropdown is open, **When** I click outside of it or press Escape, **Then** the dropdown closes.
- **Given** I am a Learner, **When** the dropdown opens, **Then** I see: My Profile, My Courses, Settings, Logout.
- **Given** I am an Admin, **When** the dropdown opens, **Then** I additionally see an "Admin Panel" link.

**Priority:** Must Have
**Story Points:** 3
**Notes / Assumptions:** Dropdown is keyboard-accessible and WCAG 2.1 AA compliant.

---

### US-8-2 · My Profile

**Title:** Access and manage the personal profile page

**User Story:**
As an **authenticated User**, I want to navigate to my profile page from the dropdown menu, so that I can view and update my personal information.

**Description:**
The profile page allows users to update their display name, avatar, email, and password. Changes are saved with confirmation feedback.

**Acceptance Criteria:**
- **Given** I click "My Profile" in the dropdown, **When** the action is triggered, **Then** I am navigated to my profile page.
- **Given** I update my display name and save, **When** the save is successful, **Then** the new name is reflected in the header avatar tooltip and throughout the platform.
- **Given** I attempt to save with an invalid email format, **When** the form is submitted, **Then** a validation error is shown and the form is not submitted.

**Priority:** Should Have
**Story Points:** 5
**Notes / Assumptions:** Password change requires current password confirmation. Email change triggers a verification email.

---

### US-8-3 · My Courses

**Title:** View enrolled and in-progress courses from the profile menu

**User Story:**
As a **Learner**, I want to access all my enrolled courses from the profile dropdown, so that I can quickly jump back into learning without searching the full catalog.

**Description:**
"My Courses" shows all courses the learner is enrolled in, regardless of status (not started, in progress, completed). It provides a personal learning dashboard view.

**Acceptance Criteria:**
- **Given** I click "My Courses" in the dropdown, **When** the action is triggered, **Then** I am navigated to a page listing all my enrolled courses with their current status and progress.
- **Given** I have no enrolled courses, **When** I open "My Courses", **Then** an empty state with a "Browse Catalog" CTA is shown.
- **Given** a course I enrolled in is unpublished by an Admin, **When** I view "My Courses", **Then** it is still visible with an "Unavailable" label and I retain access to completed content.

**Priority:** Must Have
**Story Points:** 5
**Notes / Assumptions:** "My Courses" is a filtered catalog view scoped to the authenticated user's enrollments.

---

### US-8-4 · Platform Settings

**Title:** Access notification and display settings

**User Story:**
As an **authenticated User**, I want to access platform settings from the dropdown, so that I can customize my notification preferences and display options.

**Description:**
The settings page allows users to manage email notification preferences (course updates, new content, marketing), and display preferences (language, theme if supported).

**Acceptance Criteria:**
- **Given** I click "Settings" in the dropdown, **When** the action is triggered, **Then** I am navigated to the settings page.
- **Given** I toggle email notifications off, **When** the preference is saved, **Then** I no longer receive marketing emails and a confirmation toast appears.
- **Given** I save settings, **When** the save is successful, **Then** the new preferences take effect immediately.

**Priority:** Could Have
**Story Points:** 5
**Notes / Assumptions:** This story covers UI preferences only; email unsubscribe is handled by the notification service.

---

### US-8-5 · Logout

**Title:** Securely end the user session

**User Story:**
As an **authenticated User**, I want to log out of the platform from the dropdown menu, so that my account is secured when I finish using the platform.

**Description:**
Logout invalidates the server-side session and clears local tokens/cookies, redirecting the user to the login page with a confirmation message.

**Acceptance Criteria:**
- **Given** I click "Logout" in the dropdown, **When** the action is triggered, **Then** my session is terminated, all auth tokens are cleared, and I am redirected to the login page.
- **Given** I am logged out and try to navigate to a protected page via URL, **When** the page loads, **Then** I am redirected to the login page.
- **Given** I log out, **When** I press the browser's Back button, **Then** the protected page is not shown (session is truly invalidated).

**Priority:** Must Have
**Story Points:** 2
**Notes / Assumptions:** Session invalidation is server-side. HttpOnly cookie is cleared on logout response.

---

## Feature 9: Role-Based Experience

---

### US-9-1 · Learner Role Feature Set

**Title:** Show Learner-appropriate actions and hide management controls

**User Story:**
As a **Learner**, I want to see only the features relevant to my learning journey, so that the interface is not cluttered with administrative or instructor controls I cannot use.

**Description:**
Learner role enforcement ensures that management actions (edit, publish, delete) are never rendered in the UI. The Learner sees enrollment, progress, wishlist, and profile features only.

**Acceptance Criteria:**
- **Given** I am logged in as a Learner, **When** I view a course card, **Then** no "Edit Course", "Unpublish", or "Delete" buttons are shown.
- **Given** I am a Learner, **When** I open the profile dropdown, **Then** no "Admin Panel" link is visible.
- **Given** I attempt to access an admin route directly via URL, **When** the authorization check runs, **Then** I receive a 403 Forbidden response and am redirected to the catalog.

**Priority:** Must Have
**Story Points:** 3
**Notes / Assumptions:** Role is determined by the authenticated user's JWT claims. Client-side hiding is complemented by server-side enforcement.

---

### US-9-2 · Instructor Role Feature Set

**Title:** Show Instructor-specific creation and editing controls

**User Story:**
As an **Instructor**, I want to see course authoring and editing controls in addition to all learner features, so that I can manage my own courses while also accessing the catalog as a learner.

**Description:**
Instructors see an "Edit Course" button on cards they authored and a "Create New Course" button in the header. They do not see admin-only controls such as publishing other instructors' courses or accessing the Admin Panel.

**Acceptance Criteria:**
- **Given** I am logged in as an Instructor, **When** I view a course card for a course I authored, **Then** an "Edit Course" button is shown on the card.
- **Given** I am an Instructor, **When** I view a course card authored by another instructor, **Then** the "Edit Course" button is not shown.
- **Given** I am an Instructor, **When** I view the header, **Then** a "Create New Course" button is visible.
- **Given** I attempt to edit a course I did not author via URL manipulation, **When** the authorization check runs, **Then** I receive a 403 Forbidden response.

**Priority:** Must Have
**Story Points:** 5
**Notes / Assumptions:** Authorship is determined by the `authorId` field on the course record matching the authenticated user's ID.

---

### US-9-3 · Administrator Role Feature Set

**Title:** Show all management controls for Administrators

**User Story:**
As an **Administrator**, I want access to full platform management controls from the catalog, so that I can govern course content, user access, and platform settings from one place.

**Description:**
Admins see all instructor-level features plus the ability to publish/unpublish/delete any course, access the Admin Panel via the profile dropdown, and manage featured course placement.

**Acceptance Criteria:**
- **Given** I am logged in as an Admin, **When** I view any course card, **Then** a context menu with "Edit", "Publish/Unpublish", and "Delete" options is accessible.
- **Given** I am an Admin, **When** I open the profile dropdown, **Then** an "Admin Panel" link is visible and functional.
- **Given** I click "Unpublish" on a course, **When** the action is confirmed, **Then** the course is removed from the public catalog and marked as unpublished.
- **Given** I click "Delete" on a course, **When** I confirm the destructive action, **Then** the course is permanently removed from the platform and all enrolled learners are notified.

**Priority:** Must Have
**Story Points:** 8
**Notes / Assumptions:** Delete is a soft-delete followed by a scheduled hard-delete after 30 days to allow recovery.

---

### US-9-4 · Role Indicator Badge

**Title:** Display the current user's role as a visible badge

**User Story:**
As an **authenticated User**, I want to see my current role displayed near my avatar, so that I am always aware of what permissions and capabilities are active in my session.

**Description:**
A small role badge (e.g., "Learner", "Instructor", "Admin") is displayed adjacent to the user avatar in the header. This is especially useful for users who can switch roles or for admins managing the platform.

**Acceptance Criteria:**
- **Given** I am logged in, **When** I view the header, **Then** a badge showing my current role is visible next to my avatar.
- **Given** my role is "Admin", **When** the badge renders, **Then** it is visually distinct (e.g., different color) from the Learner badge.
- **Given** my role changes (e.g., after an admin grants a promotion), **When** I next log in, **Then** the badge reflects my updated role.

**Priority:** Should Have
**Story Points:** 2
**Notes / Assumptions:** Role badges are read-only display; role changes are managed via the Admin Panel.

---

## Feature 10: Catalog Navigation

---

### US-10-1 · Pagination / Load More

**Title:** Navigate through additional pages of course results

**User Story:**
As a **Learner**, I want to navigate to additional pages of course results or click "Load More", so that I can access all courses in the catalog beyond the initial visible set.

**Description:**
Pagination prevents performance degradation from loading all courses at once. Controls at the bottom of the grid allow navigation between pages or incremental loading of additional cards.

**Acceptance Criteria:**
- **Given** more than 24 courses match the current search/filter state, **When** I reach the bottom of the grid, **Then** pagination controls or a "Load More" button is visible.
- **Given** I click "Next Page" or "Load More", **When** the action is triggered, **Then** the next set of courses loads within 1 second without a full page reload.
- **Given** I navigate to page 3, **When** I reload the page, **Then** I return to page 3 (page state preserved in URL).
- **Given** I am on the last page, **When** I view the pagination controls, **Then** the "Next" button is disabled or hidden.

**Priority:** Must Have
**Story Points:** 5
**Notes / Assumptions:** Page size is 24. "Load More" (infinite scroll variant) is an alternative implementation — team to decide during sprint planning.

---

### US-10-2 · Responsive Grid Layout

**Title:** Adapt the course grid layout to different screen sizes

**User Story:**
As a **Learner on any device**, I want the course catalog to display correctly on my screen size, so that I can browse and interact with courses comfortably on desktop, tablet, or mobile.

**Description:**
The grid adapts from 3–4 columns on desktop, to 2 columns on tablet, to 1 column on mobile. All card interactions (CTA, bookmark, filter) remain fully usable on touch devices.

**Acceptance Criteria:**
- **Given** I access the catalog on a viewport wider than 1200px, **When** the grid renders, **Then** courses are shown in a 3–4 column layout.
- **Given** I access the catalog on a viewport between 768px and 1200px, **When** the grid renders, **Then** courses are shown in a 2-column layout.
- **Given** I access the catalog on a viewport narrower than 768px, **When** the grid renders, **Then** courses are shown in a single-column layout with no horizontal overflow.
- **Given** I am on a touch device, **When** I tap the bookmark icon, **Then** the toggle works correctly without requiring a hover state.

**Priority:** Must Have
**Story Points:** 3
**Notes / Assumptions:** Breakpoints follow the existing EPAMSuite design system grid specification.

---

### US-10-3 · Platform Logo / Home Link

**Title:** Return to the catalog home via the platform logo

**User Story:**
As a **User**, I want to click the platform logo in the header to return to the course catalog, so that I can easily navigate home from any page without using the browser's Back button.

**Description:**
The platform logo acts as a universal home navigation anchor. It is present on all platform pages and always navigates to the catalog root, clearing any active filters or search terms.

**Acceptance Criteria:**
- **Given** I am on any page of the platform, **When** I click the platform logo, **Then** I am navigated to the course catalog with default state (no filters, no search, default sort).
- **Given** the logo is focused via keyboard, **When** I press Enter, **Then** the same navigation occurs.
- **Given** a screen reader is active, **When** the logo is read, **Then** it is announced as "Home – [Platform Name]".

**Priority:** Must Have
**Story Points:** 1
**Notes / Assumptions:** Logo image includes descriptive alt text for accessibility compliance.

---

## Feature 11: Course Content Management (Instructor / Admin)

---

### US-11-1 · Create New Course

**Title:** Initiate the creation of a new course from the catalog header

**User Story:**
As an **Instructor** or **Administrator**, I want to click a "Create New Course" button in the header, so that I can begin building a new course without leaving the catalog context.

**Description:**
The "Create New Course" button is visible only to Instructors and Admins and opens the course creation wizard or editor. The course is saved as a draft until explicitly published.

**Acceptance Criteria:**
- **Given** I am logged in as an Instructor or Admin, **When** I view the header, **Then** a "Create New Course" button is visible.
- **Given** I click "Create New Course", **When** the action is triggered, **Then** I am navigated to the course creation form/wizard.
- **Given** I am a Learner, **When** I view the header, **Then** the "Create New Course" button is not rendered.
- **Given** a new course is saved as a draft, **When** I return to the catalog, **Then** the draft course is not visible to Learners.

**Priority:** Must Have (for Instructor/Admin scope)
**Story Points:** 8
**Notes / Assumptions:** Course creation is a multi-step wizard (title, description, content, settings). This story covers the entry point only.

---

### US-11-2 · Edit Existing Course

**Title:** Edit a course directly from the catalog card

**User Story:**
As an **Instructor** (for my own courses) or **Administrator** (for any course), I want to click "Edit Course" on a course card, so that I can update its content and metadata without searching for it separately.

**Description:**
The "Edit Course" button appears on course cards only for authorized users. It opens the course editor pre-populated with the current course content.

**Acceptance Criteria:**
- **Given** I am an Instructor viewing a course I authored, **When** I view the card, **Then** an "Edit Course" button is visible.
- **Given** I click "Edit Course", **When** the action is triggered, **Then** I am navigated to the course editor for that course, pre-filled with current data.
- **Given** I am an Admin, **When** I view any course card, **Then** an "Edit Course" option is available.
- **Given** I save changes in the editor, **When** the save is successful, **Then** the updated metadata (title, description) is reflected on the catalog card within 5 minutes.

**Priority:** Must Have (for Instructor/Admin scope)
**Story Points:** 8
**Notes / Assumptions:** Editor is an existing component; this story covers the catalog entry point and authorization layer.

---

### US-11-3 · Publish / Unpublish Course

**Title:** Toggle course visibility in the public catalog

**User Story:**
As an **Administrator**, I want to publish or unpublish a course from the catalog card context menu, so that I can control which courses are visible to learners without deleting content.

**Description:**
Publishing makes a draft or unpublished course visible in the learner catalog. Unpublishing hides it from learners while preserving the course for the author. Enrolled learners can still access in-progress content.

**Acceptance Criteria:**
- **Given** I am an Admin and a course is in "Draft" or "Unpublished" state, **When** I click "Publish" from the card context menu, **Then** the course becomes visible in the learner catalog immediately.
- **Given** I am an Admin and a course is "Published", **When** I click "Unpublish" from the card context menu, **Then** the course is hidden from the public catalog but remains accessible to already-enrolled learners.
- **Given** I publish or unpublish a course, **When** the action is confirmed, **Then** the course card updates its status badge and a toast confirms the action.

**Priority:** Must Have (for Admin scope)
**Story Points:** 5
**Notes / Assumptions:** Enrolled learners receive an in-app notification when a course they are enrolled in is unpublished.

---

### US-11-4 · Delete Course

**Title:** Permanently remove a course from the platform

**User Story:**
As an **Administrator**, I want to delete a course from the platform via the card context menu, so that I can remove outdated or inappropriate content entirely.

**Description:**
Deletion is a destructive, irreversible action (after a 30-day soft-delete recovery window). It requires explicit confirmation and triggers notifications to enrolled learners.

**Acceptance Criteria:**
- **Given** I am an Admin, **When** I click "Delete" from a course card's context menu, **Then** a confirmation dialog appears warning that the action is permanent.
- **Given** I confirm deletion, **When** the action is processed, **Then** the course is immediately removed from the catalog and all enrolled learners receive an in-app and email notification.
- **Given** I cancel the deletion dialog, **When** the dialog is dismissed, **Then** no changes are made.
- **Given** a course is deleted, **When** an enrolled learner visits their "My Courses" page, **Then** the deleted course shows as "No longer available" for 30 days, then is fully removed.

**Priority:** Must Have (for Admin scope)
**Story Points:** 5
**Notes / Assumptions:** Soft-delete retained for 30 days for data recovery purposes. Hard-delete scheduled after 30 days.

---

### US-11-5 · Featured / Pinned Course Management

**Title:** Pin specific courses to the top of the catalog

**User Story:**
As an **Administrator**, I want to pin or feature specific courses at the top of the catalog, so that I can promote high-priority content to all learners regardless of their active sort order.

**Description:**
Featured courses appear in a dedicated "Featured" section above the main grid or are pinned to the top of sorted results. This allows admins to run promotions, highlight new content, or surface mandatory training.

**Acceptance Criteria:**
- **Given** I am an Admin, **When** I click "Feature Course" from the card context menu, **Then** the course is marked as featured and pinned to the top of the catalog for all users.
- **Given** a course is featured, **When** any learner opens the catalog, **Then** the featured course appears first regardless of their selected sort order.
- **Given** I remove a course from featured, **When** the change is applied, **Then** the course returns to its natural sort position for all users.
- **Given** multiple courses are featured, **When** the catalog renders, **Then** they appear in the order they were featured (FIFO) at the top of the grid.

**Priority:** Could Have
**Story Points:** 5
**Notes / Assumptions:** Maximum of 3 featured courses at any one time. Feature configuration is done via the Admin Panel or card context menu.

---

## Summary

This document contains **40 user stories** covering all 11 features and their sub-features from the AI Courses Catalog feature decomposition. Stories follow a consistent template including role, action, benefit, acceptance criteria (Given/When/Then), MoSCoW priority, and story point estimates. The collection is ready to be imported into a backlog management tool (e.g., Jira, Azure DevOps) as the foundation for sprint planning.

| Feature | Stories | Total Story Points |
|---|---|---|
| 1. Course Discovery & Browsing | 4 | 13 |
| 2. Search | 2 | 8 |
| 3. Filtering | 5 | 16 |
| 4. Sorting | 4 | 7 |
| 5. Enrollment & Access | 6 | 19 |
| 6. Progress Tracking | 2 | 8 |
| 7. Wishlist / Bookmarking | 2 | 6 |
| 8. Account & Session Management | 5 | 20 |
| 9. Role-Based Experience | 4 | 18 |
| 10. Catalog Navigation | 3 | 9 |
| 11. Content Management | 5 | 31 |
| **Total** | **42** | **155** |
