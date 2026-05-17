# CareConnect Prioritization — Task 1 Solution

## Section A — 1st Output from Model (including model questions)

### Model Output (Round 1)
Based on your use case (healthcare platform, mixed qualitative factors, fixed `Now` capacity of 30 SP, and objective to maximize value while minimizing delivery risk), the most suitable method is likely **Weighted Scoring** (optionally paired with a release-bucket cut: Now/Next/Then).

Before final scoring, I need clarifications:

1. Should **regulatory/compliance impact** be weighted more than user experience?
2. Is the `Now` release expected to include at least one major compliance feature?
3. Should technical risk be treated as a negative factor (higher risk = lower score)?
4. Is effort/cost a hard constraint only (30 SP) or also part of weighted scoring?
5. For stakeholder need, should `Critical` > `Strong` > `Important` > `Requested/Supported`?
6. Do you want the final recommendation to be:
   - strict top-3 by score, or
   - top-3 that also fits best into the 30 SP `Now` capacity?

---

## Section B — My Responses to Model Questions

1. Yes, compliance should be weighted higher than UX.
2. Yes, `Now` should include at least one major compliance-driven item.
3. Yes, technical risk should reduce priority score.
4. Both: include effort in scoring and also respect 30 SP hard cap.
5. Yes, use that ordering for stakeholder need.
6. Use top-3 recommendation that is practical for the next release and respects risk/capacity.

---

## Section C — 2nd Output (Technique + Prioritization Matrix + Top 3)

## 1) Chosen technique and justification

### Technique: **Weighted Scoring + Now/Next/Then release buckets**

**Why this fits best:**
- Input is multi-factor and mixed (value, urgency, compliance, risk, UX, effort).
- You need transparent trade-offs, not just categorical tags.
- `Now` has a hard capacity constraint (30 SP), so score ranking alone is not enough.
- Healthcare context needs explicit compliance emphasis.

Compared with alternatives:
- **MoSCoW** is simple but too coarse for close trade-offs.
- **WSJF** is strong for economic sequencing, but your inputs are mostly qualitative and compliance-heavy; weighted scoring is easier to justify to broad stakeholders.

---

## 2) Scoring model used

### Criteria weights
- Business Value: **25%**
- Stakeholder Need: **15%**
- Urgency: **15%**
- Regulatory Impact: **20%**
- User Experience Gain: **10%**
- Delivery Feasibility (inverse of effort): **10%**
- Technical Risk (inverse): **5%**

### Normalization scale
- Very High = 5
- High = 4
- Medium = 3
- Low = 2
- Very Low = 1

Additional mapping:
- Stakeholder Need: Critical=5, Strong=4, Important/Supported=3, Requested=2
- Feasibility (from effort): Low effort=5, Medium=3, High=1
- Risk factor (inverse): Low risk=5, Medium=3, High=1

Weighted score formula:

$$
\text{Score} = \sum (\text{Criterion Score} \times \text{Weight})
$$

Max possible score = $500$.

---

## 3) Prioritization matrix

| Feature | BV | Need | Urgency | Regulatory | UX | Feasibility | Risk (inv.) | Effort (SP) | Weighted Score (/500) | Normalized (/100) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| EMR Integration Enhancements | 5 | 5 | 4 | 4 | 3 | 1 | 1 | 13 | **385** | **77** |
| User Access Audit Logs | 4 | 4 | 5 | 5 | 2 | 1 | 3 | 13 | **380** | **76** |
| Secure Image Sharing | 4 | 4 | 3 | 3 | 4 | 3 | 3 | 8 | **350** | **70** |
| Care Pathway Templates | 4 | 3 | 2 | 2 | 3 | 5 | 5 | 5 | **320** | **64** |
| Auto-Translation in Chat | 3 | 3 | 3 | 2 | 4 | 3 | 3 | 8 | **290** | **58** |
| Patient Mood Tracker | 3 | 2 | 2 | 2 | 3 | 5 | 5 | 3 | **280** | **56** |

---

## 4) Recommended top 3 features for next release (Now)

### Capacity constraint
`Now` capacity = **30 SP**.

Strict top-3 by score are: EMR (13), Audit Logs (13), Secure Image Sharing (8) = **34 SP** (over capacity).

So the recommended **practical top-3 for next release** is:

1. **User Access Audit Logs** (13 SP)
2. **Secure Image Sharing** (8 SP)
3. **Care Pathway Templates** (5 SP)

Total = **26 SP** (fits `Now`, leaves 4 SP buffer for hardening/integration/testing).

### Justification
- **User Access Audit Logs**: highest compliance urgency (Very High regulatory + Very High urgency), critical in healthcare governance.
- **Secure Image Sharing**: high clinical value and UX gain; directly improves care coordination and diagnostic communication.
- **Care Pathway Templates**: strong value-to-effort ratio, low risk, and helps standardize care workflows quickly.

This mix maximizes stakeholder value while minimizing delivery risk and preserving release reliability.

---

## 5) Suggested release buckets

### Now (<=30 SP)
- User Access Audit Logs (13)
- Secure Image Sharing (8)
- Care Pathway Templates (5)
- Buffer: 4 SP (integration fixes, security testing, UAT support)

### Next
- EMR Integration Enhancements (13) — highest value but high technical dependency risk; plan once interface contracts and integration sandbox are stable.
- Auto-Translation in Chat (8) — accessibility value, medium complexity.

### Then
- Patient Mood Tracker (3) — useful but lower urgency and lower strategic pressure vs core care/compliance capabilities.

---

## 6) Final recommendation summary
Use **Weighted Scoring** as the primary method and apply `Now/Next/Then` as release execution framing. For the upcoming release, prioritize:

1. **User Access Audit Logs**
2. **Secure Image Sharing**
3. **Care Pathway Templates**

This recommendation is value-driven, compliance-aware, risk-balanced, and capacity-feasible.
