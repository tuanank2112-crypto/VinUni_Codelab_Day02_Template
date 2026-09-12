# Deep Dive - ResidentCare Zalo

## Problem Statement

| Field | Content |
|---|---|
| Actor | Vinhomes duty operator, supported by the ResidentCare AI copilot. |
| Current workflow | Resident reports through Zalo -> operator reads manually -> operator extracts details -> operator routes or asks clarification -> human sends response. |
| Bottleneck | Manual reading, classification and drafting under time pressure. |
| Business impact | Prototype goal: reduce assumed triage time from 5 minutes to under 1 minute and keep 100% of emergency-keyword reports under human review. These are demo targets, not measured enterprise metrics. |
| Success metric | 100% draft replies start with "[DRAFT_ONLY] "; 100% tickets require human review; emergency keyword never downgraded; all invalid AI output falls back safely. |
| Operational boundary | AI may classify, summarize, extract missing details and draft replies. It must not claim resolution, promise timing, send messages, or bypass human review. |

## Current-State Workflow

1. Resident sends Zalo text message. **Assumed time:** 1 minute.
2. Operator reads and normalizes the report. **Assumed time:** 2 minutes.
3. Operator asks for missing building/location. **Assumed time:** 2 minutes.
4. Operator classifies and routes. **Assumed time:** 1 minute.
5. Human reviews and replies. **Assumed time:** 2 minutes.

**Assumed total:** approximately 8 minutes per report. These timings are demo assumptions, not measured enterprise data.

## AI Fit Comparison

| Option | Fit | Limit |
|---|---|---|
| Rule only | Very reliable for emergency keywords and deterministic routing. | Cannot understand vague language or draft a useful resident-facing reply. |
| LLM feature | Good at classification, summary and missing-details detection. | Can hallucinate or produce invalid JSON without validation. |
| Agentic loop | Could automate more steps. | Too broad for this safety-sensitive prototype. |

**Decision:** hybrid rule engine + LLM feature + human review.

## Future-State Workflow

1. ZaloClaw receives text.
2. Input normalization.
3. Emergency rule engine.
4. KiraAI GLM 5.3 classification.
5. JSON/schema validation.
6. Policy validation.
7. Ticket is created as "PENDING_REVIEW".
8. Human approves or rejects.
9. Approved text is returned through ZaloClaw.

If AI fails, returns invalid JSON, or attempts to downgrade an emergency, the system uses a deterministic fallback ticket and keeps human review mandatory.

## Evaluation

AI readiness checklist:

1. [x] Simulated message data is available.
2. [x] AI risk is controlled by schema, policy and human review.
3. [x] Prototype workflow can be tested offline.
4. [ ] Production data, Vinhomes system integration and operational sign-off are not available.

**Decision:** GO for offline prototype; NOT YET for production.
