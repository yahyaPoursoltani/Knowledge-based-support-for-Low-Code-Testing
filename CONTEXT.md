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

The UKG is **persistent and versioned**: a UKG version represents one analysis-scope artifact state. A change in any relevant artifact revision produces a new UKG version; the previous version remains distinguishable. The UKG is not semantically a continuously mutated graph — incremental construction is only an implementation optimization. Persistence technology and physical schema are not yet selected, and whether the artifact-specific graphs are persisted independently is undecided (see `docs/adr/0001-persist-the-unified-knowledge-graph.md` and `docs/adr/0005-version-the-ukg-per-artifact-state.md`).

## Artifact Version

The identity/revision of a supplied source artifact (BPMN model, scenario set, test set, evidence) as supplied by the external subsystem. Distinct from a UKG version.

## Request/Correlation Identifier

An optional transport-level identifier supplied by the external subsystem for tracing a request. The service may echo it, but it is **not** the Analysis Run identifier.

## Analysis Run

One execution of the analysis core that produces an Analysis Result. The service mints its identifier. A run is traceable to the artifact versions it consumed and the UKG version it was computed against. Distinct from artifact versions, the UKG version, and any request/correlation identifier.

## Behavioral Scenario

A behavioral specification expressed using BDD/Gherkin concepts.

Its exact domain representation is deferred to the BDD/domain-model design work. The project must preserve meaningful Given/When/Then and related BDD semantics rather than collapsing scenarios into unstructured text.

## Scenario–Test Relationship

A possible relationship between a behavioral scenario and one or more test cases.

Do not equate this automatically with semantic validation.

## Evidence

Information that may support or contradict a validation claim. The exact evidence model is not yet defined.

## Analysis Scope

The analysis unit, modeled as a declared scope rather than a permanently isolated BPMN artifact. Prototype V0 defaults to process-level analysis: one root process plus explicitly supplied contained/subordinate process structures and called/reused processes required for the analysis, the scenario set and test case set declared for the scope, and associated evidence. Declared membership is authoritative and is owned by the external subsystem; the service must not silently expand it. The concept must not preclude later composite or application-level scopes.

## Owning Process

The process that a scenario or test case is declared to belong to. Ownership does not determine participation: a test owned by one process may contribute evidence to a scenario owned by another process within the same Analysis Scope.

## Analysis Request

The single input of an operational analysis, covering one Analysis Scope. The request is **self-contained**: it carries the actual artifacts rather than identifiers to be resolved by fetching. Each artifact also carries stable source identity (see *Artifact Identity*).

## Analysis Result

The single output of an analysis: a structured and explainable assessment of Scenario–Test relationships for the requested Analysis Scope. Conceptually it can express, per behavioral scenario: the relevant test case(s); the relationship assessment; supporting or contradicting evidence; insufficient/unknown evidence; and the explanation.

A completed run's result is persisted immutably and is addressable by its Analysis Run. It is **not** an external Scenario–Test validation link. Its exact schema and status vocabulary are not yet defined.

## External Scenario–Test Link

A user-facing validation link between a behavioral scenario and test case(s) that is persisted, presented, and lifecycle-managed by the external subsystem. It is distinct from the Analysis Result and from the Scenario–Test Relationship assessed by the service.

## Artifact Identity

Stable metadata that ties a supplied artifact to its exact counterpart in the external subsystem: artifact identifier, artifact type, source-system identifier, version/revision, and possibly a content hash. The exact metadata schema is not yet defined.

## Analysis Core

The analysis logic that produces an Analysis Result from an Analysis Request. Invoked both by the operational service (on demand) and by the evaluation harness (repeatedly, during research evaluation).

## Evaluation Harness

A separate driver for empirical evaluation. It invokes the same Analysis Core repeatedly over a research dataset. It is a supporting external system in the research evaluation context, not part of the operational Camunda integration flow and not an operational mode of the service.

## Structural Traceability

Documented structural linkage between behavioral elements/scenarios and tests. Structural traceability is distinct from semantic validation: it indicates that a test relates to a requirement, not that the test provides sufficient evidence that the requirement is met.

## Request-Level Fatal Failure

A failure that aborts the whole analysis because the request is structurally unusable: invalid envelope, unidentifiable analysis unit, missing required identity/revision metadata needed to establish the analysis-unit artifact state, missing required BPMN input, or BPMN so unreadable that process knowledge cannot be constructed. Missing metadata for optional or nonessential evidence is an artifact-level diagnostic, not automatically fatal. Always explicit; never silently normalized.

## Input Diagnostic

A provenance-aware report that a supplied artifact is incomplete, inconsistent, unresolved, missing required evidence, or locally unparseable. An input diagnostic is **not** a research-level gap by itself; it may reflect an incomplete request package. Diagnostics may limit conclusions, and only evidence-supported interpretations become higher-level findings.

## Input Failure

Another name for a request-level fatal failure: the request is structurally unusable, so nothing is analyzed.

## Completed Analysis

An analysis that finished over the usable supplied artifacts. Its result may still contain unresolved, partial, or insufficient-evidence conclusions caused by artifact/evidence deficiencies; those are legitimate semantic outputs, not failures.

## Execution Failure

A valid request whose analysis did not complete because of an operational limit (timeout, cancellation, resource exhaustion, other cutoff). It is distinct from artifact/evidence incompleteness, and no incomplete semantic result may be presented as a validation conclusion.

## Analysis Reproducibility

Reconstructability of the analysis context: which external artifact identities/revisions, which UKG version, and which analysis run produced a result. It does not imply deterministic or byte-identical analytical output, and it does not imply idempotent retries.

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
- UKG physical versioning (snapshot vs delta), retention policy, and analysis-result caching;
- identifier formats, UUID schemes, database keys, and content-hash algorithms;
- physical analysis-result storage, retention/deletion, and whether intermediate reasoning artifacts are persisted;
- reusable scenarios/tests across processes, composite multi-process and application-level scope design, and the abstractions (e.g. substitutable Analysis Scope) that will support them.
