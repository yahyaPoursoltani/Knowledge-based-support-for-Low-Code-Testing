# ADR-0009: Identifier ownership across the two systems

- **Status:** Accepted
- **Date:** 2026-10-26
- **Scope:** Knowledge-Based Validation Service / external subsystem boundary

## Context

Results must be traceable to the exact external artifacts and to the knowledge state and execution that produced them (ADR-0003, ADR-0005). Two identity domains are involved: the external subsystem's entities and revisions, and the thesis service's UKG versions and analysis runs.

If the service minted replacement identifiers for external artifacts, provenance could not be reconstructed on the subsystem side. If the subsystem minted analysis run identifiers, the service's internal execution history would depend on an external actor.

Transport-level tracing identifiers are a third, unrelated concern: they identify a request exchange, not an analysis or a knowledge state.

## Decision

Identifier ownership follows ownership of the concept.

**The external subsystem owns external identity** and supplies, authoritatively:

- Analysis Scope identifier;
- process identifiers;
- scenario identifiers;
- test case identifiers;
- artifact revision/version identifiers;
- identifiers for externally owned evidence where applicable.

**The thesis service owns internal analysis identity** and mints:

- UKG version identifiers;
- analysis run identifiers.

The service preserves and echoes external identifiers rather than minting replacements. Each Analysis Result is traceable across both domains:

```text
external scope/artifact identities + revisions
  -> UKG version -> analysis run -> analysis result
```

Keep distinct: **Request/Correlation Identifier != Analysis Run Identifier != UKG Version Identifier**. A subsystem-supplied request or correlation identifier may be echoed for transport tracing but is not the analysis run id. A future internal content fingerprint may support deduplication or reproducibility but must never replace subsystem-owned artifact identity.

Identifier formats, UUID schemes, database keys, and hash algorithms are not defined here.

## Consequences

- Provenance can be reconstructed on both sides without inventing foreign identifiers.
- The request contract must carry external identities and revisions for every supplied artifact and for the scope.
- The result must echo external identities plus the minted UKG version and run id.
- The service may internally key data by external identity, but correctness must not depend on undocumented identifier semantics.
- Any future fingerprinting is additive and cannot become the primary external identity.

## Alternatives considered

- **Service mints all identifiers** — uniform internally, but breaks subsystem-side provenance and duplicates identity.
- **Subsystem mints run identifiers** — external control of internal execution history; rejected.
- **Use one identifier for scope, UKG version, and run** — conflates artifact state, knowledge state, and execution.
- **Treat request/correlation id as run id** — conflates transport with analysis.

## Open questions (not decided by this ADR)

- Identifier formats and generation schemes.
- Whether the subsystem's scope identifier is stable across scope revisions.
- How external evidence identities are represented when evidence has no natural id.
- Whether content fingerprints are needed for deduplication.
- How identity mismatches (same id, different revision) are diagnosed.
