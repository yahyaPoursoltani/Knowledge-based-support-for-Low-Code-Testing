# ADR-0018: Source-independent ingestion through one application-level request

- **Status:** Accepted
- **Date:** 2026-10-27
- **Scope:** Prototype input architecture

## Context

Artifacts arrive from different sources: the operational Camunda-based subsystem over REST/JSON, and the research dataset as BPMN/XML files. The core must not care which source produced an artifact, and the undergraduate subsystem must not be responsible for constructing thesis-specific semantic/KG entities.

Treating the input question as "XML vs JSON" conflates transport with representation. Tests, scenarios, and BPMN each have native representations.

## Decision

Keep three layers distinct:

```text
Transport adapter != artifact native representation != normalized internal representation
```

- **Native representations:** BPMN/XML, Gherkin source, Test Case JSON (including Camunda/CPT JSON when the contract is finalized), execution-evidence JSON.
- **Transport:** REST/JSON envelope operationally; filesystem/dataset adapter for research data.
- **Normalized internal representation:** produced by shared ingestion components; the analysis core consumes only this.

All adapters converge on one application-level **Analysis Request** carrying scope identity, target process/revision, artifacts, scenario/test identities and revisions, optional evidence, and provenance identifiers. Different adapters translate into the same request.

The core must not depend on Camunda, and the dataset path must not be hard-coded. Exact REST paths, JSON field names, Camunda/CPT versions, payload limits, and error codes are deferred.

## Consequences

- Multiple input adapters can feed the same core.
- The service remains independently executable without the Camunda subsystem.
- Ingestion is the shared normalization boundary, not a per-source code path in analysis.
- Transport and parsing changes do not touch the analysis orchestration.
- Native format support (especially BPMN/XML) is a first-class requirement.

## Alternatives considered

- **Thesis-specific JSON as the only input** — forces the subsystem to build semantic entities and breaks dataset ingestion.
- **XML vs JSON as the organizing distinction** — conflates transport with artifact format.
- **One adapter per source directly invoking analysis** — duplicates orchestration and normalization.

## Open questions

- Exact Camunda/CPT JSON schema and version.
- Minimal request envelope for the first slice.
- Where format-specific parsers live relative to `ingestion/`.
- Payload size strategy for large artifacts.
