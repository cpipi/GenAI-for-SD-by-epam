# AI-Driven Testing and Quality Assurance - PT1
## Test Plan, Checklist and Test Cases

**Module:** AI-Driven Testing and Quality Assurance (PT1)  
**Website Under Test:** https://solutionshub.epam.com/  
**Prepared by:** Anuar Sultan  
**Date:** March 2026

---

## 1) Test Plan Overview

### 1.1 Objective
Validate 5 mandatory tabs and their behavior per requirements:
- Solutions
- Assets
- Guides
- Blog
- About

### 1.2 In Scope
- Tab visibility and accessibility
- URL correctness
- Content relevance
- Tab-specific behavior
- Responsiveness (desktop/tablet/mobile)
- Localization behavior (if multi-language exists)
- Empty/error state handling

### 1.3 Out of Scope
- Backend source-code verification
- Load/stress testing at infrastructure level
- Security penetration testing

### 1.4 Test Types
- Functional testing
- UI/UX testing
- Navigation testing
- Responsive testing
- Negative/empty-state testing

### 1.5 Environments
- Browsers: Chrome, Firefox, Edge, Safari
- Devices: Desktop (1920x1080), Tablet (768x1024), Mobile (375x667)
- OS: Windows/macOS + Android/iOS (for responsive check)

---

## 2) Requirements Traceability

| Req ID | Requirement | Covered In |
|---|---|---|
| GR-01 | 5 tabs must be visible and accessible on all pages | Global Checklist, TC-GEN-001..003 |
| GR-02 | Clicking tab must open corresponding page | TC-GEN-004..008 |
| GR-03 | URL must update correctly (/assets, /guides, etc.) | TC-GEN-009..013 |
| GR-04 | Active tab should be highlighted | TC-GEN-014 |
| GR-05 | Navigation must be error-free and without delay | TC-GEN-015 |
| SOL-01 | Solutions list and short descriptions | TC-SOL-001, 002 |
| SOL-02 | Solution detail page from list item | TC-SOL-003 |
| SOL-03 | Solutions filter/search correctness (if present) | TC-SOL-004, 005 |
| ABT-01 | About content: company/mission/goals/team | TC-ABT-001, 002 |
| ABT-02 | Contact info presence (if applicable) | TC-ABT-003 |
| ABT-03 | Data relevance / not outdated | TC-ABT-004 |
| BLG-01 | Blog list has title/date/short description | TC-BLG-001, 002 |
| BLG-02 | Open full article via title/read-more | TC-BLG-003 |
| BLG-03 | Blog sort/filter correctness (if present) | TC-BLG-004 |
| BLG-04 | Comments flow (if available) | TC-BLG-005 |
| AST-01 | Assets list with description/icon | TC-AST-001, 002 |
| AST-02 | Asset details or file download | TC-AST-003 |
| AST-03 | Assets filter/search correctness (if present) | TC-AST-004 |
| GUD-01 | Guides list with short description | TC-GUD-001 |
| GUD-02 | Open full guide/detail page | TC-GUD-002 |
| GUD-03 | Guides filter/search correctness (if present) | TC-GUD-003 |
| ADD-01 | Responsive behavior on all tabs | TC-ADD-001 |
| ADD-02 | Localization switch and content correctness (if supported) | TC-ADD-002 |
| ADD-03 | Empty states for tabs with no data | TC-ADD-003 |

---

## 3) Global Checklist (All 5 Tabs)

- [ ] All 5 tabs are visible in navigation
- [ ] Each tab is clickable
- [ ] Correct page opens on click
- [ ] URL changes correctly for each tab
- [ ] Active tab is visually highlighted
- [ ] No console/UI error during tab switch
- [ ] Tab switch time is acceptable (no visible lag)
- [ ] Content shown is relevant to tab name
- [ ] Works on desktop/tablet/mobile
- [ ] Empty state UI is handled properly
- [ ] Localization switch works (if enabled)

---

## 4) Tab-by-Tab Checklist + Test Cases

## A) Solutions Tab

### Checklist
- [ ] Solutions list is displayed
- [ ] Each item has short description
- [ ] Each item has link/button to details
- [ ] Details page opens correctly
- [ ] Filters work (if present)
- [ ] Search works (if present)
- [ ] Filter/search results are accurate

### Test Cases

| ID | Title | Priority | Steps | Expected Result |
|---|---|---|---|---|
| TC-SOL-001 | Verify solutions list rendering | High | Open Solutions tab | List of solutions is visible |
| TC-SOL-002 | Verify solution item metadata | High | Check several cards | Each has title + short description |
| TC-SOL-003 | Open solution details | High | Click item/details link | Detail page opens with full info |
| TC-SOL-004 | Validate filter behavior | Medium | Apply one and multiple filters | Results match selected filter values |
| TC-SOL-005 | Validate search behavior | Medium | Search by known keyword | Relevant solutions are returned |

---

## B) Assets Tab

### Checklist
- [ ] Assets list is displayed
- [ ] Assets include short description/icon
- [ ] Detail page or download option exists per asset
- [ ] Download action works (if available)
- [ ] Filters/search work correctly (if present)

### Test Cases

| ID | Title | Priority | Steps | Expected Result |
|---|---|---|---|---|
| TC-AST-001 | Verify assets list rendering | High | Open Assets tab | Assets list is shown |
| TC-AST-002 | Verify asset card fields | High | Check multiple assets | Title + description/icon is visible |
| TC-AST-003 | Validate detail/download flow | High | Click asset details or download | Correct detail view or file download starts |
| TC-AST-004 | Validate assets filter/search | Medium | Apply filter and run search | Results are accurate |

---

## C) Guides Tab

### Checklist
- [ ] Guides list is displayed
- [ ] Each guide has short description
- [ ] Guide click opens full guide/detail page
- [ ] Filters/search work correctly (if present)

### Test Cases

| ID | Title | Priority | Steps | Expected Result |
|---|---|---|---|---|
| TC-GUD-001 | Verify guides list rendering | High | Open Guides tab | Guides list appears |
| TC-GUD-002 | Open full guide/details | High | Click a guide | Full guide or detail page opens |
| TC-GUD-003 | Validate guides filter/search | Medium | Filter/search by keyword | Matching guides are shown |

---

## D) Blog Tab

### Checklist
- [ ] Blog posts list is displayed
- [ ] Each post has title, date, short description
- [ ] Post title/Read more opens full article
- [ ] Sorting/filtering works (if present)
- [ ] Comments work (if implemented)

### Test Cases

| ID | Title | Priority | Steps | Expected Result |
|---|---|---|---|---|
| TC-BLG-001 | Verify blog list rendering | High | Open Blog tab | Posts list is visible |
| TC-BLG-002 | Verify post metadata | High | Inspect several posts | Title + date + short description shown |
| TC-BLG-003 | Open full blog article | High | Click title/Read more | Full article opens |
| TC-BLG-004 | Validate sorting/filtering | Medium | Sort/filter by date/tag | Correct ordering/filter result |
| TC-BLG-005 | Validate comments flow | Low | Add/view comment (if available) | Comment behavior works as designed |

---

## E) About Tab

### Checklist
- [ ] Company/platform information exists
- [ ] Mission/goals/team details exist
- [ ] Contact information exists (if applicable)
- [ ] Content appears up-to-date (no outdated references)

### Test Cases

| ID | Title | Priority | Steps | Expected Result |
|---|---|---|---|---|
| TC-ABT-001 | Verify company info blocks | High | Open About tab | Company/platform info is visible |
| TC-ABT-002 | Verify mission/goals/team blocks | High | Review section content | Mission/goals/team sections are present |
| TC-ABT-003 | Verify contact info presence | Medium | Inspect About page footer/body | Contact details exist if required |
| TC-ABT-004 | Validate information relevance | Medium | Check dates/names/phrasing | No obviously outdated information |

---

## 5) Additional Test Cases (Cross-Cutting)

| ID | Title | Priority | Steps | Expected Result |
|---|---|---|---|---|
| TC-ADD-001 | Responsive check across 5 tabs | High | Open each tab on desktop/tablet/mobile | Layout remains usable and correct |
| TC-ADD-002 | Localization switch validation | Medium | Change language on each tab (if available) | Translations and switched language are consistent |
| TC-ADD-003 | Empty state validation | High | Navigate to empty data scenario | Friendly empty state shown, no crash |

---

## 6) General Navigation Test Cases

| ID | Title | Priority | Steps | Expected Result |
|---|---|---|---|---|
| TC-GEN-001 | Tabs visible on home | High | Open home page | All 5 required tabs visible |
| TC-GEN-002 | Tabs visible on internal pages | High | Open each tab and inspect header | Same 5 tabs remain visible |
| TC-GEN-003 | Tabs are accessible | High | Keyboard + mouse navigation | Tabs can be focused and activated |
| TC-GEN-004 | Open Solutions page | High | Click Solutions | Solutions page opens |
| TC-GEN-005 | Open Assets page | High | Click Assets | Assets page opens |
| TC-GEN-006 | Open Guides page | High | Click Guides | Guides page opens |
| TC-GEN-007 | Open Blog page | High | Click Blog | Blog page opens |
| TC-GEN-008 | Open About page | High | Click About | About page opens |
| TC-GEN-009 | URL check for Solutions | High | Open Solutions | URL matches expected pattern |
| TC-GEN-010 | URL check for Assets | High | Open Assets | URL includes /assets |
| TC-GEN-011 | URL check for Guides | High | Open Guides | URL includes /guides |
| TC-GEN-012 | URL check for Blog | High | Open Blog | URL includes /blog |
| TC-GEN-013 | URL check for About | High | Open About | URL includes /about |
| TC-GEN-014 | Active tab highlight | Medium | Switch tabs one by one | Active tab is visually highlighted |
| TC-GEN-015 | Smooth/error-free navigation | High | Rapidly switch tabs | No crash/error/major delay |

---

## 7) Exit Criteria

- 100% execution of High-priority cases
- 0 open Critical defects
- High defects have workaround or fix plan
- No blocker in tab navigation or tab content loading

---

## 8) Notes

- If Assets or Guides are absent in production navigation, log as requirement gap.

---