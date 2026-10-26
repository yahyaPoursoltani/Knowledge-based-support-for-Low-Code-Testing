# ADR-0001: Persist the Unified Knowledge Graph

- **Status:** Accepted
- **Date:** 2026-10-26
- **Scope:** Knowledge-Based Validation Service (thesis implementation)

## Context

The service integrates knowledge extracted from three artifact types (BPMN models, Gherkin behavioral specifications, and existing test cases with available evidence) into a Unified Knowledge Graph (UKG), then analyzes Scenario–Test relationships against that graph.

Analysis depends on knowledge that spans artifacts: a scenario's steps, a model's behavioral elements, and a test's observed or intended behavior must be comparable across repeated queries. Treating the graph as a transient by-product of a single analysis would discard that accumulated structure.

## Decision

The Unified Knowledge Graph is **persistent research state**: it must survive individual analysis operations and be maintained across them.

This decision establishes persistence as a requirement. It does not select how persistence is implemented.

Reasons include:

- inspectability of extracted knowledge;
- provenance tracing back to original artifacts;
- reproducibility of analyses;
- repeated analytical queries without re-extraction;
- comparison of analysis results over time;
- support for later empirical evaluation;
- explainability of validation assessments.

## Consequences

- The service needs a lifecycle for creating, updating, and querying persisted graph state.
- Provenance from UKG elements to originating artifacts must be retained across persistence.
- Storage and schema evolution become project concerns, even though their mechanisms are undecided.
- Analysis results can be audited and compared, but stale or partially updated state becomes a real risk that must be addressed later.

## Alternatives considered

- **Ephemeral in-memory graph per analysis request** — simple, but loses accumulated structure and makes inspection, provenance tracing, and cross-run comparison impractical.
- **Rebuild the graph from artifacts on every analysis** — avoids persistence complexity, but repeats extraction work and prevents stable references across analyses.
- **Persist only final analysis results (not the graph)** — keeps the output but discards the intermediate knowledge needed for explanation and re-querying.

## Open questions (not decided by this ADR)

- Neo4j vs. another graph database vs. a non-graph store.
- Property graph vs. RDF.
- Storage topology and deployment shape.
- Whether the artifact-specific graphs are persisted separately from the UKG.
- Update and version strategy.
- Transaction model.
- Whether Cypher is required.
