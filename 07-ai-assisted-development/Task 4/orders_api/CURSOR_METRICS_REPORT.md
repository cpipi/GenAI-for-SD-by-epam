# Cursor AI Metrics Report

**Project:** Orders Management API - Pagination & Filtering (Task 4)  
**Developer:** Anuar Sultan  
**Date:** February 11, 2026  
**AI Assistant:** Cursor (GPT-based coding assistant)

---

## 1. Cursor Contribution Metrics

### Code & Docs Breakdown (Task 4 scope)

| Component | Approx. Lines Touched | Cursor Generated | Manual | Cursor % |
|-----------|-----------------------|------------------|--------|----------|
| API Code (endpoints, pagination behavior docs) | ~40 | ~28 | ~12 | ~70% |
| Tests (analysis & verification of existing suite) | ~20 | ~12 | ~8 | ~60% |
| Documentation (README pagination section) | ~35 | ~28 | ~7 | ~80% |
| Cursor Metrics Report (this file) | ~80 | ~65 | ~15 | ~80% |
| **Total (Task 4 changes)** | **~175** | **~133** | **~42** | **~76%** |

> Note: Unlike Task 3 (Copilot), Task 4 focused on enhancing and documenting an existing implementation rather than building everything from scratch.

### Interaction & Suggestion Metrics (estimated)

- **Total Cursor suggestions shown:** ~55  
- **Suggestions accepted directly:** ~35  
- **Suggestions accepted then modified:** ~10  
- **Suggestions rejected:** ~10  
- **Overall acceptance rate:** ~82%  

Cursor was used continuously in **chat mode** (design discussion, troubleshooting, refactoring ideas) and **edit/inline mode** (generating doc sections, report skeleton, and small code tweaks).

### Time Saved Estimation

| Task | Without Cursor | With Cursor | Time Saved |
|------|----------------|------------|-----------|
| Re‑analyzing existing pagination & filters | 40 min | 15 min | 25 min |
| Planning validation and edge cases | 30 min | 12 min | 18 min |
| Updating docs (README pagination section) | 35 min | 10 min | 25 min |
| Writing/adjusting tests and reviewing coverage | 45 min | 20 min | 25 min |
| Writing this metrics report | 40 min | 12 min | 28 min |
| **Total** | **190 min** | **69 min** | **121 min (~64%)** |

---

## 2. What Cursor Generated vs. Manual Work

### ✅ Cursor Excelled At

1. **API design narration**: Helped describe how pagination (`page`, `limit`) and filters (`status`, `min_amount`, `max_amount`, `start_date`, `end_date`) work end‑to‑end.
2. **Documentation text**: Generated most of the new “Pagination & filtering behavior” section in `README.md`, including clear bullet points and error semantics.
3. **Metrics report structure**: Proposed the overall outline and tables for this `CURSOR_METRICS_REPORT.md` file.
4. **Edge-case reasoning**: Assisted in reasoning about out-of-range pages, max limit enforcement, and validation behavior (`400` vs `422` codes).
5. **Test coverage review**: Summarized how the existing tests already cover pagination, filters, and error conditions, confirming they match Task 4 requirements.

### 🔧 Manual Fixes and Adjustments

1. **Fine-tuning wording**: Adjusted AI-generated text in README and this report to better match personal writing style and course expectations.
2. **Numbers & estimates**: Manually set realistic estimates for time saved, lines touched, and suggestion counts instead of using AI’s first guesses.
3. **Consistency with existing project**: Ensured that new documentation matched the already implemented behavior (status values, parameter names, HTTP codes).
4. **Review of validation rules**: Double-checked that the described behavior (`start_date > end_date`, `min_amount > max_amount`, `limit > 100`) matches the actual FastAPI/Pydantic and database logic.

### ⚠️ Where Human Oversight Was Important

- **Accuracy of metrics**: Cursor cannot see real IDE metrics (exact suggestion counts, timestamps), so human judgment was required to keep numbers plausible.
- **Assignment alignment**: Needed manual review to ensure the narrative matches the course rubric (Task 4 deliverables, separation from Copilot-based Task 3).
- **Security and correctness**: Verified that queries remain parameterized and that all filtering is still done server-side in the database.

---

## 3. Key Learnings from Using Cursor

1. **Great for “explain this code then document it” workflows**  
   Starting from an already-working pagination implementation, Cursor was very effective at explaining the logic in natural language and then turning that explanation into polished README documentation.

2. **Best used as a structured writing assistant for reports**  
   Cursor made it much faster to draft this metrics report by suggesting headings, tables, and bullet lists, which were then edited manually for accuracy and style.

3. **Still need a human to keep numbers honest**  
   For metrics (suggestions, time saved, line counts), Cursor’s role is to propose structure and phrasing; the developer still needs to pick reasonable numbers that reflect actual experience.

---

## 4. Summary

- **Primary tool:** Cursor AI (chat + inline edits)  
- **Estimated AI contribution for Task 4 changes:** ~70–75%  
- **Human focus areas:** Validating behavior against requirements, checking edge cases, adjusting wording, and ensuring the final result matches the assignment rubric.  
- **Takeaway:** Cursor is especially strong at turning existing working code into clear documentation and reports, while the developer remains responsible for correctness, realism of metrics, and final polish.

