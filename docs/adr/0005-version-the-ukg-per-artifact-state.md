# ADR-0005: Version the UKG per analysis-unit artifact state

- **Status:** Accepted
- **Date:** 2026-10-26
- **Scope:** Knowledge-Based Validation Service (thesis implementation)

## Context

The UKG is persistent research state (ADR-0001) and analyses must remain reproducible and explainable. A single evolving graph would mix knowledge extracted from different artifact revisions whenever the subsystem re-sends a model, scenario set, or test set. That would make provenance ambiguous: a result could not be tied to one coherent knowledge state.

The subsystem supplies a self-contained request whose artifacts carry identity and revision metadata (ADR-0003). That enables treating artifact state as the input to UKG construction.

## Decision

The persistent UKG is a **versioned representation of an analysis unit's artifact state**, not a continuously mutated graph.

- Same relevant artifact revisions -> a compatible existing UKG version may be reused.
- Any changed relevant artifact revision -> a new, identifiable UKG version representing the new analysis-unit state.
- Previous UKG versions remain distinguishable, so earlier analysis results stay traceable to the knowledge state against which they were produced.

Semantically:

```text
changed artifact state -> new UKG version
```

Incremental extraction or update may later optimize construction of a new version, but incremental graph mutation is **not** the semantic model.

Each analysis result is ultimately traceable to:

- the relevant source artifact identities and revisions;
- the exact UKG version used;
- the specific analysis run/result.

Keep these distinct:

```text
Artifact Version != UKG Version != Analysis Run / Analysis Result
```

Example: BPMN r7 + Scenario-set r12 + Test-set r20 -> UKG v31 -> analysis run 108. A later run may reuse UKG v31 while the artifact state is unchanged.

## Consequences

- Previous results remain explainable after artifacts change.
- Analysis results need explicit references to artifact versions and the UKG version.
- Storage grows with artifact history; retention must eventually be decided.
- Freshness checks compare artifact revisions rather than patching graph state.
- The version identity scheme (how a UKG version is derived and recognized) must be designed before implementation.

## Alternatives considered

- **One incrementally mutated graph per model** — simple to query, but silently mixes revisions and weakens provenance.
- **Rebuild without version identity** — avoids mixed state, but makes earlier results untraceable.
- **Version at artifact level only (no UKG version)** — cannot express the combined artifact state that a result actually used.
- **Treat an analysis run as the version boundary** — conflates "knowledge state" with "execution", preventing reuse of an unchanged UKG.

## Open questions (not decided by this ADR)

- Full physical snapshot vs delta-based storage.
- Graph-database versioning mechanism.
- Retention/deletion policy for historical UKG versions.
- Whether artifact-specific KGs are independently versioned/persisted.
- Whether constructing a new UKG version is physically a full rebuild or incremental.
- Analysis-result caching.
- How a UKG version is identified/recognized as compatible.
