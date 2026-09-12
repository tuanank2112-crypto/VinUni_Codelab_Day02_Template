# AI Interaction Log

## AI helped with

- [x] Brainstorming resident-service bottlenecks and selecting a scope that could be demonstrated safely.
- [x] Structuring the 6-field problem statement and the current/future workflows.
- [x] Drafting the operational boundaries for emergency escalation and human review.
- [x] Suggesting adversarial tests such as prompt injection and invalid model output.
- [x] Troubleshooting environment setup and converting the prototype from Gemini to KiraAI.

## AI was wrong or uncertain about

- [x] It initially suggested broad production integration even though the lab only required a safe prototype.
- [x] It produced generic metrics without evidence, so I marked all timings as demo assumptions.
- [x] Its first fallback rule misclassified messages containing both an elevator issue and waste issue.
- [x] A mock malicious inference attempted to downgrade an emergency report, exposing why model output cannot be trusted directly.

## Prompt and design changes I made

- [x] Added a deterministic emergency rule before calling the LLM.
- [x] Added a JSON-like inference schema and validation for category, priority, action and destination.
- [x] Required every draft to start with "[DRAFT_ONLY] ".
- [x] Forced every ticket to PENDING_REVIEW and required human approval.
- [x] Treated resident messages as untrusted input.
- [x] Added a safe fallback when the model fails or returns invalid output.
- [x] Corrected the rule priority so the multi-issue test classified the primary elevator issue correctly.

## What I verified

- [x] Ran 16 offline pytest cases; all passed.
- [x] Ran the CLI with one normal water report and one electrical smoke emergency.
- [x] Confirmed the emergency case was escalated to a human and could not be downgraded.
- [x] Confirmed no real Zalo message was sent and no API key was stored in the repository.

## Personal lessons

- [x] AI is useful for drafting, but safety rules must be deterministic.
- [x] Human approval is mandatory in resident-service operations.
- [x] Metrics must be marked as assumptions unless measured from real data.
- [x] Prompt injection cannot be handled by prompt wording alone; validation is needed.
