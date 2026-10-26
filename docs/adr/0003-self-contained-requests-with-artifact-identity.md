# ADR-0003: Self-contained requests with stable artifact identity

- **Status:** Accepted
- **Date:** 2026-10-26
- **Scope:** Knowledge-Based Validation Service (thesis implementation) — input boundary

## Context

The service is invoked on demand by the external Camunda-based subsystem with a model-scoped analysis unit (ADR-0002). The service must integrate BPMN, Scenario, and Test knowledge, and later report conclusions that the subsystem can attach to the exact entities it owns.

If artifacts were resolved by reference instead of supplied, every analysis would depend on the subsystem being reachable during analysis, and reproducing an analysis would require reconstructing subsystem state. If artifacts were supplied without identity, results could not be traced back to the entities the subsystem persists.

The output side is different: the subsystem remains the owner of presentation and link persistence, so the service does not become independent of it.

## Decision

Analysis requests are **self-contained**. The request carries the actual inputs:

- the BPMN model representation;
- the relevant Gherkin behavioral specifications;
- the existing test-case definitions;
- available relevant test/execution evidence, when it exists.

For Prototype V0, the service does not call back to the subsystem merely to fetch BPMN models, scenarios, test cases, or ordinary execution evidence.

Self-contained does **not** mean identity-free. Every supplied artifact carries stable source identity information so the result can refer unambiguously to the exact Scenario, Test Case, BPMN artifact, and evidence item. The contract must be able to carry artifact identifier, artifact type, source-system identifier, version/revision, and possibly a content hash. The exact metadata schema is deferred.

The output side remains integrated: the subsystem consumes the result to persist and/or present Scenario–Test validation relationships. Whether link persistence is performed by the service through a separate subsystem REST operation, or by the subsystem after receiving the response, is **not** decided here.

## Consequences

- An analysis is reproducible from the request alone, and the evaluation harness can build equivalent payloads without a live subsystem.
- Requests duplicate subsystem content; identity metadata lets the subsystem detect and reconcile staleness or version mismatch.
- Payload size can grow with evidence volume; how much evidence to embed remains open.
- The contract needs an identity/metadata schema before it can be specified.
- The service cannot rely on subsystem state during analysis, which reduces hidden coupling.
- Returning the result to the subsystem is expected; result transport does not imply the service owns link persistence.

## Alternatives considered

- **Referential requests** — smaller payloads and no duplication, but coupling to subsystem availability and harder reproducibility.
- **Hybrid (artifacts embedded, evidence fetched)** — viable later if evidence is large, but introduces a partial dependency that V0 does not need.
- **Embedded artifacts without identity** — simplest transport, but breaks traceability and reconciliation.

## Open questions (not decided by this ADR)

- The identity metadata schema and version/revision semantics.
- Size limits and treatment of large execution evidence.
- Authentication/authorization of the transport.
- Whether any future fetch-back is allowed, and for what.
- Status vocabulary and evidence schema of the result.
- Link-persistence authority (service-side REST call vs. subsystem after response).
