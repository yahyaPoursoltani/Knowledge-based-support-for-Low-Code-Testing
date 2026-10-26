# ADR-0002: On-demand, model-scoped analysis requests

- **Status:** Accepted
- **Date:** 2026-10-26
- **Scope:** Knowledge-Based Validation Service (thesis implementation)

## Context

The external Camunda-based subsystem owns artifact management, test execution, and the presentation of validation information. It decides when validation analysis is needed. The thesis service must integrate BPMN, Scenario, and Test knowledge into a shared UKG before it can assess Scenario–Test relationships.

Two boundary questions followed from that division: how the service is invoked, and how much context one invocation carries.

Scenario-level invocation was rejected as the default because the analysis integrates multi-artifact knowledge and because one scenario may be validated by a combination of test cases. Separating batch evaluation from the operational interface keeps the service's external contract to a single mode.

## Decision

The service operates **on demand**: the external subsystem sends one analysis request and receives one structured, explainable analysis result. There is no polling, automatic background re-analysis, or event-driven synchronization in the initial prototype.

One analysis unit is:

- one BPMN process model;
- all behavioral scenarios associated with that model;
- all existing test cases associated with that model;
- any available test/execution evidence for those test cases.

Empirical evaluation is performed by a **separate evaluation harness** that invokes the same analysis core repeatedly over a research dataset (for example, BPMN-for-Research). Offline batch evaluation is not a second external operational mode of the service.

## Consequences

- The subsystem controls invocation timing and sees only request/response semantics.
- Each request must carry (or unambiguously reference) enough context for a model-scoped analysis.
- Cross-scenario and cross-test reasoning is possible within one result.
- No incremental or event-consistency guarantees exist between artifact changes and analyses.
- The analysis core must be invocable without the service boundary, so the evaluation harness does not duplicate analysis logic.
- A long-running analysis may require the response semantics (sync vs. deferred) to be revisited later.

## Alternatives considered

- **Scenario-scoped requests** — simpler results, but prevents reasoning about test-case combinations and weakens knowledge integration.
- **Event-driven re-analysis** — fresher results, but adds synchronization and invalidation concerns that are out of scope for the prototype.
- **Batch analysis as the operational mode** — fits evaluation, but does not match how the collaborating subsystem needs validation information.
- **Two operational modes (on-demand plus batch)** — rejected at this stage to keep one external contract.

## Open questions (not decided by this ADR)

- Whether request artifacts are embedded in the payload or referenced by identifier (and how evidence is obtained).
- The Analysis Result schema and explanation structure.
- Behaviour on repeated requests for the same or a changed analysis unit.
- Relationship between a request and UKG state (create, extend, or reuse).
- Transport details of the REST contract.
- Whether a synchronous response remains adequate for large models.
