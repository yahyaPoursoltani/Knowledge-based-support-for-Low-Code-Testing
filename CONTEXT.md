# Project Context and Terminology

Context for the thesis implementation prototype described in `README.md`. This file records terminology that is sufficiently established to be relied upon. Entries marked **provisional** may still change; entries marked **deferred** are placeholders that must not be treated as settled.

This file is a terminology and context reference, not a specification. Detailed schemas, algorithms, and design decisions belong elsewhere (`docs/adr/`).

## Knowledge-Based Validation Service

The independent research service implemented by the PhD thesis. It analyzes artifacts supplied by the external subsystem and produces evidence-backed assessments of Scenario–Test relationships.

## External Camunda-Based Subsystem

The separately developed system responsible for modeling and test-management UI, execution-related capabilities, artifact management, external link persistence, and integration APIs. Also referred to as *the external subsystem*.

## BPMN Knowledge Graph

A knowledge representation extracted from a BPMN artifact. Its detailed schema is not yet defined.

## Scenario Knowledge Graph

A knowledge representation extracted from behavioral specifications expressed using BDD/Gherkin concepts. Its detailed schema is not yet defined.

## Test Knowledge Graph

A knowledge representation extracted from existing test cases and available associated evidence. Its detailed schema is not yet defined.

## Unified Knowledge Graph (UKG)

The integrated knowledge representation combining knowledge from the BPMN, Scenario, and Test domains while preserving provenance.

The UKG is **persistent and versioned**: a UKG version represents one analysis-unit artifact state. A change in any relevant artifact revision produces a new UKG version; the previous version remains distinguishable. The UKG is not semantically a continuously mutated graph — incremental construction is only an implementation optimization. Persistence technology and physical schema are not yet selected, and whether the artifact-specific graphs are persisted independently is undecided (see `docs/adr/0001-persist-the-unified-knowledge-graph.md` and `docs/adr/0005-version-the-ukg-per-artifact-state.md`).

## Artifact Version

The identity/revision of a supplied source artifact (BPMN model, scenario set, test set, evidence) as supplied by the external subsystem. Distinct from a UKG version.

## Analysis Run

One execution of the analysis core that produces an Analysis Result. A run is traceable to the artifact versions it consumed and the UKG version it was computed against. Distinct from both artifact versions and the UKG version.

## Behavioral Scenario

A behavioral specification expressed using BDD/Gherkin concepts.

Its exact domain representation is deferred to the BDD/domain-model design work. The project must preserve meaningful Given/When/Then and related BDD semantics rather than collapsing scenarios into unstructured text.

## Scenario–Test Relationship

A possible relationship between a behavioral scenario and one or more test cases.

Do not equate this automatically with semantic validation.

## Evidence

Information that may support or contradict a validation claim. The exact evidence model is not yet defined.

## Analysis Unit

The scope of one analysis: one BPMN process model, all behavioral scenarios associated with that model, all existing test cases associated with that model, and any available test/execution evidence for those test cases. Model-scoped on purpose: a scenario may be validated by one test case or by a combination of test cases.

## Analysis Request

The single input of an operational analysis, covering one Analysis Unit. The request is **self-contained**: it carries the actual artifacts rather than identifiers to be resolved by fetching. Each artifact also carries stable source identity (see *Artifact Identity*).

## Analysis Result

The single output of an analysis: a structured and explainable assessment of Scenario–Test relationships for the requested Analysis Unit. Conceptually it can express, per behavioral scenario: the relevant test case(s); the relationship assessment; supporting or contradicting evidence; insufficient/unknown evidence; and the explanation. Its exact schema and status vocabulary are not yet defined.

## Artifact Identity

Stable metadata that ties a supplied artifact to its exact counterpart in the external subsystem: artifact identifier, artifact type, source-system identifier, version/revision, and possibly a content hash. The exact metadata schema is not yet defined.

## Analysis Core

The analysis logic that produces an Analysis Result from an Analysis Request. Invoked both by the operational service (on demand) and by the evaluation harness (repeatedly, during research evaluation).

## Evaluation Harness

A separate driver for empirical evaluation. It invokes the same Analysis Core repeatedly over a research dataset. It is a supporting external system in the research evaluation context, not part of the operational Camunda integration flow and not an operational mode of the service.

## Structural Traceability

Documented structural linkage between behavioral elements/scenarios and tests. Structural traceability is distinct from semantic validation: it indicates that a test relates to a requirement, not that the test provides sufficient evidence that the requirement is met.

## Request-Level Fatal Failure

A failure that aborts the whole analysis because the request is structurally unusable: invalid envelope, unidentifiable analysis unit, missing artifact identity/revision, missing required BPMN input, or BPMN so unreadable that process knowledge cannot be constructed. Always explicit; never silently normalized.

## Input Diagnostic

A provenance-aware report that a supplied artifact is incomplete, inconsistent, unresolved, missing required evidence, or locally unparseable. An input diagnostic is **not** a research-level gap by itself; it may reflect an incomplete request package. Diagnostics may limit conclusions, and only evidence-supported interpretations become higher-level findings.

## Assessed gap situations

Three conceptually distinct situations the analysis must distinguish, asserted only when the available evidence supports them. Names are provisional; the final vocabulary is deferred.

- **Representation gap** — a behavioral requirement/scenario is not represented in the process model.
- **Traceability gap** — a represented requirement/scenario lacks structural traceability to tests.
- **Semantic validation gap** — a represented and structurally covered requirement/scenario still lacks sufficient semantic validation evidence.

## End User

The person who interacts with the external subsystem. An indirect actor of the thesis service: the end user never interacts with the service directly.

## Researcher

The actor who drives empirical evaluation through the evaluation harness. An evaluation actor, not an operational service actor.

## Evaluation Ground Truth

Authoritative judgments about expected Scenario–Test relationships, used to evaluate the method. It may draw on stakeholder/domain-expert input, but its construction methodology is open and is not assumed to come from a single expert.

## Deferred terminology

The following are deliberately **not** defined yet; do not introduce stabilizing definitions for them outside a design session that explicitly addresses them:

- the precise representation of BDD structures (Feature, Scenario Outline, Examples, steps);
- graph node/edge schemas and alignment concepts;
- evidence types and sufficiency criteria;
- semantic validation criteria;
- the semantic-link lifecycle and its state names;
- request/response payload shapes for the REST contract;
- the artifact-identity metadata schema and the status vocabulary;
- the final naming of the assessed gap situations and the traceability relation semantics;
- the ground-truth construction and adjudication methodology;
- UKG physical versioning (snapshot vs delta), retention policy, and analysis-result caching.
