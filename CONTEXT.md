# Project Context and Terminology

Context for the thesis implementation prototype described in `README.md`. This file records terminology that is sufficiently established to be relied upon. Entries marked **provisional** may still change; entries marked **deferred** are placeholders that must not be treated as settled.

This file is a terminology and context reference, not a specification. Detailed schemas, algorithms, and design decisions belong elsewhere (`docs/adr/`).

## Knowledge-Based Validation Service

The independent research service implemented by the PhD thesis. It analyzes artifacts supplied by the external subsystem and produces evidence-backed assessments of Scenario–Test relationships.

## External Camunda-Based Subsystem

The separately developed system responsible for modeling and test-management UI, execution-related capabilities, artifact management, external link persistence, and integration APIs. Also referred to as *the external subsystem*.

## Requirement

A stakeholder/business need, rule, expectation, or intended behavior. **Research context only:** it is not a V0 operational input entity. V0 models no Requirement entities, no Requirement IDs, and no Requirement-to-Scenario mappings.

The supplied Gherkin Scenario is the operational behavioral reference. Service findings are phrased relative to the supplied behavioral specification, not as absolute requirement correctness or requirement coverage. Explicit requirement traceability may be added later as a new input/domain concept if needed.

## Verification (thesis-specific)

Determining whether the **BPMN model itself** is built correctly and is technically/structurally valid: deadlocks or control-flow defects, exception handling, required services/dependencies, structural/technical soundness or executability.

Conceptually: "Is the model built correctly?" Verification is **not** the responsibility of the Knowledge-Based Validation Service. This thesis-specific meaning must not be confused with the standard software-engineering usage (conformance of an implementation to a specification).

## Validation

Determining whether modeled and tested behavior corresponds to the expected behavior expressed by the supplied behavioral Scenarios.

```text
Scenario             -> expected behavior
BPMN Process Model   -> representation of that behavior
Existing Test Case(s)-> potential evidence for validating that behavior
```

Core question: for each concrete Scenario, which existing Test Case or combination of Test Cases provides sufficient evidence to validate the expected behavior, in the context of its representation in the target BPMN Process model?

The **origin of a Test Case is irrelevant**: it may be manually authored, generated, or produced by another testing mechanism. The service evaluates the available Test Case and evidence, not how it was created.

The service performs evidence-based Validation Assessment of Scenario behavior; it does not perform BPMN-model Verification.

## Feature

A lightweight organizational grouping for Scenarios originating from the same Gherkin specification. **Grouping/provenance context only.**

- Not a Validation Claim subject and receives no Validation Assessment.
- Not a Process, and no Feature–Process mapping is inferred.
- Not part of the validation/reasoning model; no Feature-level reasoning or first-class persisted conclusions.
- Any future Feature-level summary is derived from member Scenario outcomes.

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

## Behavioral Example

The general concept of a concrete example illustrating intended behavior. A Scenario or Scenario Instance is a Behavioral Example; an Example Row alone is not.

## Scenario

A concrete, structured example of expected system behavior in a particular context. It preserves **Given** (context/preconditions), **When** (action/event/trigger), **Then** (expected outcome), and **And/But** (continuation of the corresponding clause type).

A plain Gherkin `Scenario` directly represents one concrete Scenario and is one validation subject. A Scenario is not a Requirement, and must not be flattened into an unstructured text blob.

## Scenario Outline

A parameterized behavioral template. It is not itself a concrete analysis subject.

## Example Row

A row in a Gherkin Examples table that supplies concrete values. It is not by itself a Behavioral Example.

## Scenario Instance

The concrete scenario produced by combining one Scenario Outline with one Example Row. Each instance is independently assessable, because different rows may be supported by different Test Cases.

A Scenario Instance and a plain Scenario play the same validation-subject role, but their provenance differs; they are **not** unconditional synonyms.

## Process

A domain/business process. Distinct from any BPMN artifact: an artifact is a representation of the Process at a particular revision. Conceptual process identity must not be collapsed into a physical serialization.

## BPMN Artifact

A supplied BPMN representation of a Process at an artifact revision. One artifact may represent more than one Process (for example, a collaboration). Distinct revisions are distinct artifact versions.

## Target Process

The primary Process of an Analysis Scope, at one declared authoritative revision. V0 analyzes one target process revision per scope and does not compare alternative representations or multiple revisions of it inside one scope.

Sub-Processes, Call Activities, and explicitly supplied called/supporting Processes remain allowed and do not change the single-target assumption.

## Scenario–Test Relationship

An umbrella term for a relationship between a behavioral scenario and one or more test cases. In the analysis domain it takes distinct forms: Candidate Relationship (hypothesis), Analytical Validation Relationship (analyzed relationship), and External Scenario–Test Link (subsystem-owned persisted link). A Scenario–Test Relationship is never automatically semantic validation.

## Test Case

A definition of how some behavior is tested: relevant conditions, inputs/actions, and expected assertions/outcomes. Not a Scenario: a Scenario states expected behavior; a Test Case states how that behavior is checked.

Cardinality is not one-to-one: one Scenario may require multiple Test Cases, and one Test Case may provide evidence relevant to multiple Scenarios. Test origin (manual, generated, other mechanism) is irrelevant to the domain.

## Test Execution

A particular execution/observation of a Test Case. A Test Case is the definition; a Test Execution is an instance of running it. The thesis service does not execute tests.

## Evidence

Traceable information that may support, weaken, contradict, or leave unresolved a Validation Claim. Potential sources include supplied test definitions, assertions, execution results, observed/expected outcomes, and artifact correspondences — subject to the Analysis Signal boundary.

Evidence is not automatically sufficient merely because it exists. The exact evidence model and sufficiency criteria are deferred.

## Analysis Signal

Information used to discover, prioritize, or reason about possible relationships or evidence. An Analysis Signal is **not** automatically Validation Evidence.

Embedding similarity, structural correspondence, graph proximity/path, mappings, Cypher query results, and LLM suggestions/confidence are discovery signals; none is semantic validation proof by itself. "Analysis Signal" is a conceptual distinction in V0, not a modeled or persisted first-class entity.

## Candidate Relationship

A hypothesized Scenario–Test relationship that merits further analysis: "this Test Case may be relevant to this Scenario." It is not a validated relationship.

Similarity, graph matching, or LLM reasoning may propose a Candidate Relationship; proposal alone does not establish semantic validation.

## Validation Claim

An evaluable proposition that a Test Case or combination of Test Cases provides relevant and sufficiently strong evidence for validating a Scenario within a particular Analysis Scope and artifact state.

Validation Claims are formulated **internally** by the service; they are analysis-domain propositions, not externally authored inputs. The claim subject is a concrete Scenario (a plain Scenario or a Scenario Instance). Exact claim decomposition/cardinality per Scenario is deferred. Conceptual form: "Tests T1 and T2 provide sufficient evidence for validating Scenario S within Scope A at artifact state R."

## Validation Assessment

The analytical conclusion produced by evaluating a Validation Claim against available evidence: Claim → evidence-based analysis → Assessment. The exact assessment/status vocabulary is deferred.

## Analytical Validation Relationship

The analyzed Scenario–Test relationship **within the context of the target Process model, Analysis Scope, and artifact state**. It is not a context-free Scenario–Test link: the analysis preserves the path

```text
Scenario behavior -> its representation in the BPMN Process model -> relevant Test Case(s) -> available validation evidence
```

The BPMN model is constitutive context, not incidental metadata. The relationship may have a positive, insufficient, or otherwise unresolved analytical outcome; it is not limited to successful validation.

Candidate Relationship (pre-analysis hypothesis) ≠ Analytical Validation Relationship (analyzed, model-grounded) ≠ External Scenario–Test Link (subsystem-persisted). Its precise relation to Validation Claims and Assessments is deferred.

## Analysis Scope

The analysis unit, modeled as a declared scope rather than a permanently isolated BPMN artifact. V0 is centered on **one Target Process at one declared authoritative revision**, plus explicitly supplied contained/subordinate process structures and called/reused supporting Processes, the scenario set and test case set declared for the scope, and associated evidence.

Declared membership is authoritative and is owned by the external subsystem; the service must not silently expand it. The concept must not preclude later composite or application-level scopes (ADR-0007, ADR-0013).

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

A defensible structural correspondence between the behavior expressed by a Scenario, the representation of that behavior in the target BPMN Process model, and at least one supplied Test Case:

```text
Scenario -> relevant modeled behavior -> Test Case
```

Textual similarity, an arbitrary external link, or an unsupported Scenario–Test association does **not** establish structural traceability.

Structural traceability is distinct from semantic validation and is **not semantic validation evidence by itself**: it indicates that a test is structurally connected to the modeled behavior relevant to the scenario, not that the test provides sufficient evidence that the intended behavior is validated. Complete step-by-step validation of every Given/When/Then clause is not required at this stage; partial coverage of relevant modeled behavior is recorded as analytical context and may feed Semantic Validation Insufficiency rather than automatically becoming a Traceability Gap.

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

## Validation-Failure Taxonomy (V0)

The V0 taxonomy is **staged**, not three co-occurring labels. Each branch stops at its first failing condition.

```text
Specified behavior
  -> Represented?            No  -> Representation Gap (stop)
  -> Structurally traced?    No  -> Traceability Gap (stop)
  -> Sufficient semantic
     validation evidence?    No  -> Semantic Validation Insufficiency (the MBTT condition) (stop)
  -> Validated
```

- **Representation Gap** — behavior expressed by the supplied behavioral specification is not sufficiently represented in the supplied process model(s). Judged relative to the supplied specification and Analysis Scope; it is not a claim of absolute stakeholder truth.
- **Traceability Gap** — represented behavior lacks a defensible model-grounded structural relation to supplied tests (see *Structural Traceability*). Textual similarity or an unsupported association does not count. Structural traceability is not semantic validation. Partial structural coverage is not automatically relabeled as a Traceability Gap; it is recorded as analytical context and may feed the next stage.
- **Semantic Validation Insufficiency** — applies only after the behavior is represented **and** structurally traced, but the available evidence is insufficient to establish that the test validates the specified behavior. The term must not be broadened to missing representation or missing traceability. (Replaces the earlier provisional name "semantic validation gap".)
- **MBTT** — the research interpretation corresponding **exactly** to the third failure stage: represented + structurally traced + insufficient semantic validation evidence. It is **not** the primary persisted status of an Analysis Result, and not a label for stages 1–2. The operational outcome is Semantic Validation Insufficiency; an explanation may state that this condition corresponds to the Model-Bounded Testing Trap. MBTT may exist even when structural traceability appears complete.
- **Validated** — terminal stage: sufficient evidence was found, relative to the supplied Scenario, the declared BPMN process/artifact state, the available Test Cases and evidence, and the declared Analysis Scope. It is **not** absolute proof of stakeholder correctness, and it does not finalize the persisted status vocabulary.

The stages are not simultaneous labels: a behavior is classified at the first stage where it fails, and the branch stops there.

V0 introduces **no** Contradictory Evidence or Validation Contradiction concept, and no contradiction taxonomy. The service does not adjudicate whether a Scenario, a Test Case, or a stakeholder expectation is wrong, nor which artifact should be repaired. It answers only whether the available Test Cases and supplied evidence provide sufficient evidence to validate the behavior expressed by the Scenario. If not sufficient, the behavior is not established as validated; the service may explain which expected behavior was unsupported. Evidence may still weaken or contradict a claim in the general sense, but that is not a V0 gap or status classification.

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
- evidence types, evidence-source selection, and sufficiency criteria;
- semantic validation criteria;
- the semantic-link lifecycle and its state names;
- request/response payload shapes for the REST contract;
- the artifact-identity metadata schema and the status vocabulary;
- exact Validation Claim decomposition/cardinality and the traceability relation's precise semantics;
- the ground-truth construction and adjudication methodology;
- UKG physical versioning (snapshot vs delta), retention policy, and analysis-result caching;
- identifier formats, UUID schemes, database keys, and content-hash algorithms;
- physical analysis-result storage, retention/deletion, and whether intermediate reasoning artifacts are persisted;
- reusable scenarios/tests across processes, composite multi-process and application-level scope design, and the abstractions (e.g. substitutable Analysis Scope) that will support them.
