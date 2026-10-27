# Domain Concepts & Ubiquitous Language Summary

- **Session:** Domain Concepts & Ubiquitous Language (closed)
- **Date:** 2026-10-26
- **Scope:** V0 domain semantics only. No graph schema, API, algorithm, evidence scoring, or implementation design.
- **Source note:** `fig_Validation_Fail_Taxonomy.pdf` was referenced by the researcher but is not present in the repository; the staged flow is recorded from the researcher's statement (ADR-0012).

## Research-context terms

### Requirement

A stakeholder/business need, rule, expectation, or intended behavior.

- **Not** a V0 operational input entity: no Requirement entities, IDs, or Requirement-to-Scenario mappings.
- A Requirement may be illustrated by multiple Scenarios (research context only).
- Findings are relative to the supplied behavioral specification, never "requirement coverage" or absolute requirement correctness.
- Explicit requirement traceability may be added later as a new concept.

### Verification (thesis-specific)

Whether the BPMN model itself is technically/structurally valid: deadlocks, control-flow defects, exception handling, service/dependency wiring, executability.

- "Is the model built correctly?"
- **Out of scope** for the service; not the standard "implementation vs specification" meaning (ADR-0015).

### Validation

Whether modeled and tested behavior corresponds to the expected behavior expressed by the supplied Scenarios.

- Questions: which existing Test Case(s) provide sufficient evidence to validate a Scenario's behavior, given its representation in the target BPMN model?
- Test Case origin (manual/generated/other) is irrelevant.
- The service performs evidence-based Validation Assessment, **not** BPMN-model Verification.
- "Validated" is relative to Scenario, artifact state, scope, tests, and available evidence — not absolute stakeholder correctness.

## Specification terms

### Feature

Lightweight organizational grouping for Scenarios from the same Gherkin specification.

- Not a reasoning entity, not a Validation Claim subject, not a Process.
- No Feature–Process mapping; no Feature-level persisted conclusions. Derived roll-ups only.

### Behavioral Example

The general concept of a concrete example illustrating intended behavior. A Scenario or Scenario Instance is a Behavioral Example; an Example Row alone is not.

### Scenario

A concrete, structured example of expected behavior in context, preserving Given (context/preconditions), When (action/event/trigger), Then (expected outcome), and And/But (clause continuation).

- A plain Gherkin `Scenario` directly represents one concrete Scenario and is one validation subject.
- Never flattened into unstructured text; not a Requirement and not a Test Case.

### Scenario Outline

A parameterized behavioral template. Not itself a concrete analysis subject.

### Example Row

A row in a Gherkin Examples table supplying concrete values. Not by itself a Behavioral Example.

### Scenario Instance

The concrete scenario produced by Scenario Outline + one Example Row.

- Independently assessable, because different rows may be covered by different tests.
- Same validation-subject role as a plain Scenario; provenance differs. Scenario and Scenario Instance are **not unconditional synonyms**.

## Process and scope terms

### Process

A domain/business process. Distinct from any BPMN artifact; conceptual identity must not collapse into a serialization.

### BPMN Artifact

A supplied BPMN representation of a Process at an artifact revision. One artifact may represent more than one Process (e.g. collaboration). Different revisions are different artifact versions.

### Target Process

The primary Process of an Analysis Scope, at one declared authoritative revision.

- V0: one target process revision per scope.
- No comparison of alternative representations or multiple revisions of the target inside one scope (ADR-0013).
- Sub-Processes, Call Activities, and supplied supporting Processes remain allowed.

### Application

A higher-level software/business context that may contain or coordinate multiple Processes. Application ≠ Analysis Scope.

### Analysis Scope

The explicitly declared artifact boundary over which one analysis may reason.

- Contains one Target Process (+ revision), supplied contained/supporting processes, the declared Scenario set, Test Case set, and evidence.
- Declared membership is authoritative; relationships inside may be inferred; out-of-scope references are diagnostics; silent expansion prohibited (ADR-0007).

### Owning Process

The Process a Scenario or Test Case is declared to belong to. Ownership ≠ participation: a test owned by one process may provide evidence for a scenario owned by another, within the same scope.

## Test and evidence terms

### Test Case

A definition of how behavior is checked: conditions, inputs/actions, expected assertions/outcomes.

- Scenario states expected behavior; Test Case states how it is checked.
- No one-to-one cardinality: one Scenario may need several Test Cases; one Test Case may serve several Scenarios.
- Origin is irrelevant.

### Test Execution

A particular execution/observation of a Test Case. Test Case ≠ Test Execution; the service does not execute tests.

### Evidence

Traceable information that may support, weaken, contradict, or leave unresolved a Validation Claim.

- Candidate sources: relevant test definitions, assertions, expected/observed outcomes, execution results.
- Existence ≠ sufficiency; the evidence model and sufficiency criteria are deferred.

### Analysis Signal

Information used to discover, prioritize, or reason about possible relationships or evidence — structural correspondence, graph paths, similarity, mappings, LLM suggestions.

- Analysis Signal ≠ Validation Evidence; not semantic validation proof by itself.
- Conceptual distinction only; **not** a modeled/persisted first-class entity in V0.

### Structural Traceability

A defensible structural correspondence between Scenario behavior, its representation in the target BPMN model, and at least one supplied Test Case.

- Textual similarity, arbitrary external links, or unsupported associations do not establish it.
- Structural Traceability ≠ Semantic Validation, and it is **not semantic validation evidence by itself**; complete step-level validation is not required at this stage.
- Partial coverage is analytical context and may feed Semantic Validation Insufficiency, not automatically a Traceability Gap (ADR-0014).

## Analysis terms

### Candidate Relationship

A pre-analysis hypothesis that a Test Case may be relevant to a Scenario. Not a validated relationship; proposal by similarity/matching/LLM does not establish validation.

### Validation Claim

An internally formulated, evaluable proposition that a Test Case or combination provides relevant and sufficiently strong evidence for validating a Scenario within a scope and artifact state.

- Subject: one concrete Scenario (plain Scenario or Scenario Instance).
- Decomposition/cardinality per Scenario: deferred.

### Validation Assessment

The analytical conclusion produced by evaluating a Validation Claim against available evidence. Exact status vocabulary: deferred.

### Analytical Validation Relationship

The analyzed Scenario–Test relationship in the context of the target Process model, Analysis Scope, and artifact state:

```text
Scenario behavior -> representation in the BPMN model -> Test Case(s) -> available evidence
```

- May have a positive, insufficient, or otherwise unresolved analytical outcome.
- Candidate Relationship ≠ Analytical Validation Relationship ≠ External Scenario–Test Link (ADR-0014).

### Scenario–Test Relationship

Umbrella term for a relationship between a Scenario and one or more Test Cases; takes the candidate, analytical, or external-link form. Never automatically semantic validation.

## Staged validation-failure taxonomy

Staged, with stop branches — not simultaneous labels (ADR-0012):

```text
Specified behavior
  -> Represented?                       No -> Representation Gap (stop)
  -> Structurally traced?               No -> Traceability Gap (stop)
  -> Sufficient semantic evidence?      No -> Semantic Validation Insufficiency (stop)
  -> Validated (relative to available evidence)
```

- **Representation Gap** — supplied behavioral specification not sufficiently represented in the process model(s); relative to the scope, not absolute truth.
- **Traceability Gap** — represented behavior lacks a defensible model-grounded structural relation to supplied tests.
- **Semantic Validation Insufficiency** — represented and structurally traced, but evidence insufficient to establish that the test validates the specified behavior. Replaces the provisional "semantic validation gap"; not broadened.
- **MBTT** — research interpretation corresponding exactly to the third failure stage. Not a persisted status; explanations may name the correspondence. Not applicable to representation or traceability failures.
- **Validated** — sufficient evidence relative to Scenario, declared BPMN artifact state, available Test Cases/evidence, and scope. Not absolute stakeholder correctness.

V0 has no Contradictory Evidence or Validation Contradiction concept, no contradiction taxonomy, and no artifact-repair adjudication. If evidence is insufficient, the behavior is not established as validated.

## Result and link terms

### Analysis Result

Persisted, immutable, run-addressable analytical output for a scope. Not an External Scenario–Test Link; status vocabulary deferred.

### External Scenario–Test Link

A persisted, user-facing Scenario–Test relationship owned and lifecycle-managed by the external subsystem. Analysis Result ≠ External Link; link-mutation authority remains deferred.

## Established relationships/cardinalities

- Requirement may be illustrated by multiple Scenarios (research context only).
- Feature groups Scenarios; never a validation subject.
- Scenario Outline + 1 Example Row = 1 Scenario Instance.
- Scenario ↔ Test Case: many-to-many (no one-to-one assumption).
- Test Case 1 → 0..* Test Executions.
- Analysis Scope: exactly 1 target Process at 1 authoritative revision; 0..* supporting Processes; declared Scenario/Test sets; evidence.
- Validation Claim subject: exactly 1 concrete Scenario; claim decomposition deferred.
- Analytical Validation Relationship: 1 Scenario ↔ 1..* Test Cases, grounded in the target model and artifact state.
- Taxonomy: exactly one failure stage per behavior (first failing stage).

## Rejected synonyms

- Requirement = Scenario
- Feature = Process
- Feature = reasoning/validation entity
- Process = BPMN artifact
- Scenario Outline = Example Row = Scenario Instance
- Scenario = Scenario Instance (unconditionally)
- Scenario = Test Case
- Test Case = Test Execution
- Analysis Signal = Validation Evidence
- Candidate Relationship = Analytical/validated relationship
- Validation Claim = Validation Assessment
- Analysis Result = External Validation Link
- Analytical Validation Relationship = External Validation Link
- Structural Traceability = Semantic Validation
- Representation Gap = Traceability Gap = Semantic Validation Insufficiency
- MBTT = Traceability Gap or any missing test
- Verification = Validation
- Validated = absolute stakeholder correctness

## Unresolved/deferred domain questions

- Validation Claim decomposition/cardinality per Scenario.
- Evidence model, evidence-source selection across executions, and sufficiency criteria.
- What makes a structural correspondence "defensible"; directionality/multiplicity of trace relations.
- How partial representation/trace coverage is recorded as analytical context.
- Precise relation between Analytical Validation Relationship and the Claim/Assessment pair.
- Persisted status vocabulary; explanation structure.
- Whether/how Requirements become traceable inputs later.
- External link lifecycle and mutation authority.
- Composite/application-level scopes, reusable scenarios/tests.
- Whether model-quality findings from external tools could enter as context.
- Add `fig_Validation_Fail_Taxonomy.pdf` for source cross-checking.
