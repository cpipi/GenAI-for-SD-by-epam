# Feature Decomposition: Functionality Interface Sample

## Prompt Used in EPAM DIAL (GPT-4o)

> You are an expert Business Analyst. I have attached a screenshot of an application interface prototype.
>
> Please analyze it and create a **detailed business feature decomposition** in Markdown format.
>
> Requirements:
> 1. Identify all main business features that are visible or clearly implied by the interface.
> 2. Break each main feature into specific sub-features.
> 3. Use hierarchical numeric indexing: 1, 1.1, 1.2, 2, 2.1, etc.
> 4. Focus on **business functionality and user goals**, not just UI element descriptions.
> 5. Provide a short, clear description for every main feature and sub-feature.
> 6. Structure the output so it can directly feed into user story creation.
> 7. Include only features that are supported by or reasonably inferred from the interface shown.
>
> Output format:
> - **Main Feature Number. Feature Name**
>   - Description (1–2 sentences)
>   - **Sub-feature Number. Sub-feature Name** — Description

---

## Outcome of Prompt Execution

*(Based on the attached Functionality Interface Sample.png — an AI Courses Catalog platform)*

---

### 1. Course Discovery and Browsing

**Description:** Enables users to explore the available AI course catalog and quickly identify learning options relevant to their goals.

#### 1.1 Course Catalog Grid View
**Description:** Displays all available courses as a responsive grid of cards, giving users a scannable overview of the full catalog at a glance.

#### 1.2 Course Card Summary
**Description:** Each course card presents key metadata — title, category tag, difficulty badge, duration, instructor name, rating, and learner count — so users can evaluate a course without navigating away.

#### 1.3 Results Count Display
**Description:** Shows the total number of courses matching the current search/filter state (e.g., "Showing 24 of 87 courses") to help users understand the scope of results.

#### 1.4 Course Detail Navigation
**Description:** Clicking a course card navigates the user to a dedicated Course Detail page for in-depth information before committing to enrollment.

---

### 2. Search

**Description:** Allows users to find specific courses quickly by entering keywords related to course title, topic, or technology.

#### 2.1 Keyword-Based Search
**Description:** A prominent search bar accepts free-text input and filters the course grid in real time as the user types, matching titles, topics, and relevant keywords.

#### 2.2 Live Search Results
**Description:** Results update dynamically after a minimum character threshold (e.g., 2+ characters), eliminating the need for a manual search trigger.

---

### 3. Filtering

**Description:** Enables users to narrow the course catalog to only the most relevant results by applying one or more criteria simultaneously.

#### 3.1 Category Filter
**Description:** Allows users to filter courses by subject domain such as Generative AI, Machine Learning, NLP, Computer Vision, or Data Science.

#### 3.2 Difficulty Level Filter
**Description:** Allows users to display only courses matching their proficiency: Beginner, Intermediate, or Advanced.

#### 3.3 Duration Filter
**Description:** Allows users to limit results by estimated course length (e.g., under 2 hours, 2–5 hours, 5–10 hours, 10+ hours).

#### 3.4 Multi-Filter Combination
**Description:** Multiple filters can be applied simultaneously using AND logic, progressively narrowing results to match all selected criteria at once.

#### 3.5 Active Filter Chips
**Description:** Applied filters are shown as removable tags/chips below the filter bar, giving users a clear view of what is active and allowing quick removal of individual filters.

---

### 4. Sorting

**Description:** Allows users to reorder the course catalog to surface the most relevant or preferred results first.

#### 4.1 Sort by Most Popular
**Description:** Orders courses by enrollment count so the most widely taken courses appear first.

#### 4.2 Sort by Highest Rated
**Description:** Orders courses by average learner rating to surface the most positively reviewed content.

#### 4.3 Sort by Newest
**Description:** Orders courses by publication or update date to surface the most recently added content.

#### 4.4 Sort Alphabetically
**Description:** Orders courses A–Z or Z–A by title for users who prefer manual browsing.

---

### 5. Course Enrollment and Access

**Description:** Supports the complete learner journey from initial enrollment through course completion, with context-aware actions on every course card.

#### 5.1 One-Click Enrollment
**Description:** An "Enroll Now" button on each course card allows unenrolled learners to begin enrollment directly from the catalog without navigating to the detail page.

#### 5.2 Enrollment Confirmation
**Description:** A modal confirmation dialog prevents accidental enrollment and confirms the action before it is committed.

#### 5.3 Start Course Action
**Description:** For enrolled learners who have not yet started, a "Start Course" button navigates directly to the first lesson.

#### 5.4 Continue Learning
**Description:** For courses already in progress, a "Continue" button resumes the learner at their last accessed lesson.

#### 5.5 Completed Course Access
**Description:** For finished courses, a "Review Course" button gives access to the course summary or certificate page.

#### 5.6 Enrollment State Recognition
**Description:** The call-to-action button label and behavior on each card dynamically reflect the current enrollment state: not enrolled, enrolled, in progress, or completed.

---

### 6. Progress Tracking

**Description:** Gives learners a visual indication of how far they have progressed in any course they have already started.

#### 6.1 Per-Card Progress Bar
**Description:** A horizontal progress bar on each in-progress course card shows the learner's completion percentage (e.g., 65% complete) for at-a-glance status monitoring.

#### 6.2 Progress Persistence
**Description:** Progress state is stored and restored across sessions so learners can return at any time and see accurate completion data.

---

### 7. Wishlist / Course Bookmarking

**Description:** Allows learners to save courses for future consideration without enrolling immediately.

#### 7.1 Bookmark Toggle
**Description:** A heart or bookmark icon on each course card lets users add or remove the course from their personal Wishlist with a single click and a visual confirmation animation.

#### 7.2 Wishlist Access
**Description:** Saved courses are accessible from the user's profile menu under "My Courses" or a dedicated Wishlist section.

---

### 8. User Account and Session Management

**Description:** Provides access to the user's personal profile, enrolled courses, platform settings, and secure session termination.

#### 8.1 User Avatar / Profile Menu
**Description:** A user avatar or initials badge in the top-right corner opens a dropdown menu with role-appropriate navigation options.

#### 8.2 My Profile
**Description:** Navigates the user to their account profile page where personal details can be viewed or edited.

#### 8.3 My Courses
**Description:** Provides a direct shortcut to the learner's list of enrolled and in-progress courses.

#### 8.4 Platform Settings
**Description:** Allows users to access notification preferences, display settings, and account configuration.

#### 8.5 Logout
**Description:** Ends the authenticated session securely and redirects the user to the login page.

---

### 9. Role-Based Experience

**Description:** Adapts the interface, available actions, and visible controls based on the authenticated user's assigned role.

#### 9.1 Learner Role
**Description:** Learners see enrollment, progress, and wishlist actions. Management controls (edit, publish, delete) are hidden.

#### 9.2 Instructor Role
**Description:** Instructors see all Learner actions plus an "Edit Course" button on courses they authored and a "Create New Course" button in the header.

#### 9.3 Administrator Role
**Description:** Administrators see all Instructor actions plus full management controls: an Admin Panel link in the profile menu and options to publish, unpublish, or delete any course from its card context menu.

#### 9.4 Role Indicator Badge
**Description:** A visible badge near the user avatar displays the current user's role (e.g., "Learner", "Instructor", "Admin") so the user is always aware of their active permission context.

---

### 10. Catalog Navigation

**Description:** Supports navigation through a large inventory of courses without degrading usability or performance.

#### 10.1 Pagination / Load More
**Description:** Controls at the bottom of the grid allow users to navigate to additional pages of results or load more course cards incrementally.

#### 10.2 Responsive Grid Layout
**Description:** The card grid adapts from multi-column (desktop) to a reduced or single-column layout (tablet/mobile) to ensure usability across device sizes.

#### 10.3 Platform Logo / Home Link
**Description:** The platform logo in the header acts as a home link, returning the user to the catalog or platform home from any page.

---

### 11. Course Content Management (Instructor / Admin)

**Description:** Supports authorized users in creating, editing, and managing the lifecycle of course content on the platform.

#### 11.1 Create New Course
**Description:** Authorized users (Instructors, Admins) can initiate the creation of a new course via a dedicated button in the header navigation.

#### 11.2 Edit Existing Course
**Description:** An "Edit Course" button (visible on course cards for the author or admins) allows authorized users to update course content, metadata, and settings.

#### 11.3 Publish / Unpublish Course
**Description:** Administrators can toggle a course's visibility in the catalog by publishing or unpublishing it, controlling learner access without deleting content.

#### 11.4 Delete Course
**Description:** Administrators can permanently remove a course from the platform via the card's context menu, subject to a confirmation step.

#### 11.5 Featured / Pinned Course Management
**Description:** Administrators can feature or pin specific courses to the top of the catalog, overriding the default sort order for all users platform-wide.

---

## Summary

The **Functionality Interface Sample** represents an AI-focused learning platform catalog. The feature set covers the full learner journey — from course discovery, search, filtering, and sorting through enrollment, progress tracking, and completion — alongside role-based experience layers for Instructors and Administrators who manage content. The decomposition is structured to serve directly as input for Epic and User Story creation.
