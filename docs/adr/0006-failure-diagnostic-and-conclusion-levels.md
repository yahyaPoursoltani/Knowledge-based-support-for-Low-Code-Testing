# ADR-0006: Separate request failure, input diagnostics, and research conclusions

- **Status:** Accepted
- **Date:** 2026-10-26
- **Scope:** Knowledge-Based Validation Service (thesis implementation)

## Context

Requests arrive as self-contained packages (ADR-0003) built by the external subsystem. Such packages can be incomplete or internally inconsistent in ways that matter to the research: a scenario absent from the model, a test without traceability, missing execution evidence, a test referencing a scenario that was not included.

Two naive policies are both wrong for this thesis. Failing the entire request on any inconsistency destroys exactly the signals the research needs. Silently normalizing inconsistencies fabricates coherence and would let an incomplete request package appear as a research finding.

Additionally, a scenario referenced by a test but not supplied does **not** prove that the scenario is absent from the requirements; it may simply mean the request package was incomplete.

## Decision

The service distinguishes three levels.

**1. Request-level fatal failure** — aborts the analysis only when the request is structurally unusable: invalid envelope; unidentifiable analysis unit; missing required artifact identity/revision; missing required BPMN input; or BPMN so unreadable that process knowledge cannot be constructed. Such failures are explicit and never silently normalized.

**2. Artifact-level / analysis-level deficiency** — when individual artifacts are incomplete, inconsistent, missing evidence, or locally unparseable, the service continues with the analyzable parts and reports the deficiency with provenance, plus the limitations it imposes on conclusions. Missing execution evidence is not fatal: the assessment stays unresolved rather than becoming validation or invalidation.

**3. Research-level gap or validation conclusion** — produced only when the available evidence supports the interpretation. Input inconsistency is not automatically a representation, traceability, or semantic-validation gap.

Resulting rules: analyze best-effort; preserve provenance of deficiencies; expose unresolved references; allow partial and unresolved conclusions; never invent missing information; never silently normalize; never treat absence of evidence as evidence of absence; never auto-map every input inconsistency to a gap.

Detailed error codes and response schemas are not defined here.

## Consequences

- The result contract must carry diagnostics and limitations alongside assessments.
- Partial results are valid outputs, so the subsystem must tolerate unresolved scenarios and assessments.
- Fatal and non-fatal failure are separate channels; transport-level error handling cannot double as deficiency reporting.
- Reasonable-looking but unsupported conclusions become harder to produce, which is intended.
- The evaluation harness must distinguish method output from incomplete input when scoring.

## Alternatives considered

- **Fail fast on any inconsistency** — simple contract, but discards research signals and penalizes incomplete packages.
- **Silently normalize and proceed** — maximizes "successful" responses by fabricating coherence; unacceptable for this research.
- **Treat every inconsistency as a research gap** — over-claims from incomplete packages; confuses request quality with artifact quality.
- **Treat missing evidence as negative evidence** — rejected; absence of evidence is not evidence of absence.

## Open questions (not decided by this ADR)

- Error/diagnostic taxonomy and codes.
- How limitations on conclusions are expressed in the result.
- How the subsystem and evaluation harness distinguish fatal from partial outcomes.
- Whether diagnostics affect UKG version identity.
- How to represent locally unparseable artifacts inside the UKG (if at all).
