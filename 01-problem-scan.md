# Problem Scan - ResidentCare Zalo

## Scan

| # | Subsidiary | Lens | Bottleneck |
|---|---|---|---|
| 1 | Vinhomes | Repetitive | Resident reports are copied manually between chat, hotline and operations tools. |
| 2 | Vinhomes | Time-consuming | Duty staff read long chat threads to extract location, issue type and urgency. |
| 3 | Vinhomes | Error-prone | Emergency wording is missed during peak hours, delaying escalation. |
| 4 | Vinhomes | Language-heavy | Vague resident messages need clarification before routing. |
| 5 | Vinhomes | Human bottleneck | Every draft reply requires staff to rewrite the same acknowledgement message. |

## Quick Problem Cards

### Card 1 - Resident Report Intake

- **Actor:** Vinhomes resident and duty operator.
- **Current workflow:** resident sends Zalo message -> operator reads -> asks missing information -> routes ticket.
- **Bottleneck:** manual reading and data extraction.
- **AI support:** classify report, summarize it, detect missing details, draft reply.
- **Metric:** reduce manual triage time from an assumed 5 minutes to under 1 minute.
- **Architecture:** hybrid rule engine + LLM + human review.

### Card 2 - Emergency Escalation

- **Actor:** security/technical duty team.
- **Current workflow:** operator recognizes emergency -> calls duty team -> creates ticket.
- **Bottleneck:** delayed recognition during peak hours.
- **AI support:** deterministic keyword rule forces emergency classification and human escalation.
- **Metric:** 100% emergency-keyword messages are escalated to human review.
- **Architecture:** rule-first safety layer, not model discretion.

### Card 3 - Missing Information Collection

- **Actor:** resident and customer service staff.
- **Current workflow:** staff manually asks for building, unit and exact issue.
- **Bottleneck:** repeated clarification questions.
- **AI support:** structured extraction and missing-details list.
- **Metric:** reduce clarification round-trips from an assumed 2 rounds to 1 round.
- **Architecture:** LLM feature with schema validation.

## Selection

ResidentCare is selected because it can be demonstrated safely with simulated data, has clear routing categories, and still requires human approval before sending any reply.
