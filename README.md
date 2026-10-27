# Knowledge-Based Validation Service for Behavioral Requirements and Model-Based Tests

Implementation prototype of a PhD thesis. This repository holds the thesis research documentation, the planned implementation of the **Knowledge-Based Validation Service**, and the empirical evaluation material. There is no application code yet; the project is in the research-design phase.

## Research problem

Model-based and low-code testing can produce tests that provide evidence that an implementation conforms to its conceptual/process model, while still failing to establish that the conceptual model correctly represents stakeholder and domain expectations.

Three concerns must not be conflated:

- **model-based testing** — does the implementation behave as the process model prescribes? (context, not the service's analytical claim);
- **Verification (thesis-specific)** — is the BPMN model itself technically/structurally sound (deadlocks, control flow, exception handling, service wiring)? Out of scope;
- **Validation** — do the available Test Cases and evidence provide sufficient evidence to validate the expected behavior expressed by the supplied Scenarios, given its representation in the target BPMN model? This is the thesis concern.

This thesis investigates the third concern. Findings are relative to the supplied Scenarios and available evidence, not absolute stakeholder correctness. The thesis does **not** claim that the problem is already empirically solved.

## System boundary

The thesis implementation is an independent **Knowledge-Based Validation Service**. It is *not* part of the modeling tooling.

The external collaborating subsystem is a **Camunda-based environment**, developed separately (undergraduate project). It is responsible for capabilities such as:

- Camunda Desktop Modeler integration;
- BPMN editing and management;
- management of Gherkin behavioral specifications;
- management and execution of test cases;
- presentation of validation information to the end user;
- persistence of externally managed Scenario–Test links;
- exposing and consuming integration REST APIs.

The thesis service must not depend directly on:

- Camunda Modeler internals;
- Camunda plugin APIs;
- React components;
- the internal Java/Spring architecture of the external subsystem;
- the external subsystem's database schema.

## Actors and system contexts

### Operational context

```text
End User
   -> External Camunda-Based Subsystem
        <-> Knowledge-Based Validation Service
```

The external subsystem is currently the **only external system actor** in the operational flow. The end user is an **indirect** actor: they interact with the subsystem, never directly with the thesis service.

The service must not access the subsystem's internal database, plugin internals, or implementation-specific stores. It receives what it needs through the analysis request.

### Internal thesis infrastructure

The service's own **persisted UKG store** is internal infrastructure, not an external actor. Accessing it is expected; the persistence technology is still undecided (ADR-0001).

- direct access to the subsystem's internal store: **not allowed**;
- access to the thesis service's own persisted UKG: **allowed and expected**.

### Research/evaluation context

```text
Researcher
   -> Evaluation Harness
        -> same Knowledge-Based Validation analysis capability
```

The evaluation harness is a supporting/external system in the **research evaluation context only**; it is not part of the operational Camunda integration flow. The researcher is an evaluation actor, not an operational service actor.

Stakeholders and domain experts are **not runtime actors** of the service. They may provide authoritative behavioral intent, requirements knowledge, and expert judgment that contribute to constructing or adjudicating evaluation ground truth. Ground truth is not assumed to come from a single domain expert; the methodology remains open.

The following are **not** external operational actors unless a later design decision introduces them: external LLM provider, external embedding service, external solver, external vector database, external test runner, external modeler service. If one becomes required, update this context explicitly rather than assuming it.

## Scope of responsibility

In scope for the thesis service:

- knowledge extraction from BPMN, behavioral scenarios, and tests;
- integration into the persistent UKG with provenance;
- candidate Scenario–Test relationship discovery;
- structural traceability analysis where relevant;
- evidence-based semantic validation assessment;
- identification of representation, coverage/traceability, and semantic-validation deficiencies where supported;
- explainable results returned to the external subsystem.

Explicitly out of scope:

- executing test cases;
- generating test cases or test scripts;
- authoring or editing BPMN process models;
- authoring or editing Gherkin behavioral specifications;
- owning the end-user UI;
- owning the persistence store for external Scenario–Test links;
- implementing Camunda Modeler plugins or other internal components of the external subsystem;
- operating, deploying, or administering the external Camunda-based subsystem;
- defining stakeholder requirements on behalf of stakeholders;
- independently declaring a BPMN process model absolutely "business-correct";
- verifying the technical/structural correctness of the BPMN model itself (deadlocks, control flow, exception handling, service/dependency wiring) — that is Verification, not Validation;
- generating the empirical ground truth used to evaluate the thesis method;
- acting as an autonomous substitute for stakeholder/domain-expert judgment when artifacts and evidence are insufficient.

Structural coverage and traceability are **not** excluded as analysis. The research uses a staged validation-failure taxonomy (details in `CONTEXT.md`):

1. behavior specified but **not represented** in the process model -> Representation Gap (branch stops);
2. represented but **not structurally traced** to tests -> Traceability Gap (branch stops);
3. represented and structurally traced but **insufficient semantic validation evidence** -> Semantic Validation Insufficiency (the MBTT condition; branch stops);
4. sufficient evidence -> Validated relative to the supplied behavioral specification, declared artifact state, available Test Cases/evidence, and Analysis Scope.

Structural traceability/coverage is a model-grounded signal; it is **not** semantic validation evidence by itself.

The service may compute and expose structural coverage/traceability information when it is needed for Scenario–Test assessment, gap classification, evidence analysis, or explanation. It must not become a general-purpose coverage management/reporting subsystem, and conventional coverage metrics are not the primary thesis deliverable. It may assess whether BPMN behavior, scenarios, tests, and evidence are mutually supportive or inconsistent, but it must not claim absolute business correctness from the BPMN model alone, and it does not adjudicate which artifact is "wrong".

## Failure and deficiency levels

The service distinguishes three levels; they must not be collapsed.

**1. Request-level fatal failure.** The whole analysis fails only when the request is structurally unusable: invalid envelope; unidentifiable analysis unit; missing required identity/revision metadata needed to establish the analysis-unit artifact state; missing required BPMN input; or a BPMN representation so unreadable that process knowledge cannot be constructed. Missing metadata for optional or nonessential evidence is an artifact-level diagnostic, not automatically fatal. These failures are explicit and are never silently normalized.

**2. Artifact-level or analysis-level deficiency.** When individual artifacts are incomplete, inconsistent, missing evidence, or locally unparseable, the service continues with what remains analyzable and returns partial results plus explicit artifact-level failures and the limitations they impose. Example: one unparseable scenario still yields results for the valid scenarios, an explicit failure for that scenario, and stated limits on conclusions. Missing execution evidence is not fatal; it leaves an assessment unresolved rather than validating or invalidating it.

**3. Research-level gap or validation conclusion.** Only evidence-supported interpretations become representation, traceability, or semantic-validation conclusions. Input inconsistency does **not** automatically equal a research-level gap: a test referencing a scenario not included in the request may indicate an incomplete request package, not an absent requirement.

Rules: analyze usable information best-effort; preserve provenance of deficiencies; expose unresolved references explicitly; return partial or unresolved conclusions where necessary; never invent missing information; never silently normalize inconsistencies; never treat absence of evidence as evidence of absence; never automatically map every input inconsistency to a gap.

## Transport and outcome classes

V0 uses **synchronous request/response**: the subsystem sends one analysis request, the service completes the analysis, and the same interaction returns one structured result. No asynchronous job creation, polling, callbacks, or job-state management are introduced unless empirical performance later shows synchronous execution is impractical. Asynchronous transport may later be added as a separate adapter around the same analysis core.

Three outcome classes are distinct:

1. **Input Failure** — the request is structurally unusable (request-level fatal failure, see above). Explicit; nothing is analyzed.
2. **Completed Analysis** — the analysis finished over the usable supplied artifacts. The result may legitimately contain unresolved, partial, or insufficient-evidence conclusions caused by artifact/evidence incompleteness (e.g. missing execution evidence for one test case).
3. **Execution Failure** — the request was valid, but the analysis did not complete because of an operational limit (timeout, cancellation, resource exhaustion, other cutoff). No incomplete semantic result may be presented as a validation conclusion; the service returns an explicit execution/operational failure.

Artifact/evidence incompleteness and analysis-execution incompleteness therefore have different semantics and must never be conflated. Error codes, HTTP statuses, and concrete timeout values are not defined yet; the execution limit remains an operational configuration concern.

## Operational mode and analysis scope

The service is **on-demand**: the external subsystem decides when an analysis is required, sends **one analysis request**, and receives **one structured, explainable analysis result**. The initial prototype does not poll, re-analyze in the background, or synchronize event-driven.

The analysis unit is modeled as an **Analysis Scope**, not as a permanently isolated BPMN artifact. Prototype V0 uses a **process-level default**: behavioral scenarios are defined at the process level, test cases are defined at the process level, and each scenario and test case has one declared owning process. A process may nevertheless contain sub-processes or invoke reusable processes, so a higher-level scenario may be realized across contained or called processes.

An Analysis Scope may contain:

- one target process at one declared authoritative revision;
- its explicitly supplied contained/subordinate process structures;
- explicitly supplied called/reused supporting processes required for the intended analysis;
- the scenario set declared for that scope;
- the test case set declared for that scope;
- associated evidence.

V0 analyzes a single target process revision per scope; it does not compare alternative BPMN representations or multiple revisions of that target within one scope. Sub-processes, Call Activities, and supplied called processes remain in scope.

**Ownership is not participation.** A scenario owned by P1 may be validated by a test owned by P2 when both are in the same scope. For example, with root P1 and scope {P1, P2}, scenarios S1/S2 owned by P1, and tests T1 (owned by P1) and T2 (owned by P2), the service may determine that T2 contributes evidence to S1.

**Declared scope membership is authoritative.** The external subsystem declares it. The service must not silently expand scope by inferring additional process, scenario, or test membership from names, tags, semantic similarity, graph connectivity, or embedded references. It may inspect supplied artifact relationships and report missing dependencies as diagnostics — e.g. a Call Activity from P1 to P3 where P3 is not supplied is reported, not fetched or added.

- declared scope membership -> authoritative;
- relationships inside that scope -> may be inferred by the service;
- references outside that scope -> diagnostics;
- silent scope expansion -> prohibited.

**Extensibility constraint.** The analysis core must not hard-code a permanent single-process assumption. The design must remain open to reusable scenarios and test cases across processes, composite multi-process analysis, and application-level analysis composed of several processes. Appropriate abstractions (e.g. substitutable Analysis Scope implementations, OCP/DIP) are to be designed later; they are not designed in this document.

This operational boundary is distinct from the **research evaluation workflow**: a separate evaluation harness invokes the same analysis core repeatedly over a research dataset (e.g. BPMN-for-Research). Offline evaluation is **not** a second external operational mode of the service.

## Request and result boundary

**Input is self-contained.** The subsystem sends the actual analysis inputs — the BPMN model representation, the relevant Gherkin behavioral specifications, the existing test-case definitions, and available relevant test/execution evidence. The service does not fetch these back from the subsystem.

**Self-contained is not identity-free.** Every supplied artifact retains stable source identity so results can refer unambiguously to the exact Scenario, Test Case, BPMN artifact, and evidence item in the external subsystem. The future contract must be able to carry artifact identifier, artifact type, source-system identifier, version/revision, and possibly a content hash; the exact metadata schema is not yet defined.

**Output integration remains.** The subsystem consumes the analysis result to persist and/or present Scenario–Test validation information. For each behavioral scenario the result must be able to express:

- the relevant test case or combination of test cases;
- the assessment of the Scenario–Test relationship;
- the evidence supporting or contradicting that assessment;
- insufficient/unknown evidence where applicable;
- an explanation of why the relationship was assessed that way.

The status vocabulary and evidence schema are deferred. Whether validation links are persisted by the service calling a separate subsystem REST operation, or by the subsystem after receiving the response, is **not** decided.

## High-level thesis processing concept

Current established research direction (exact schemas and algorithms are not settled):

```text
BPMN Model                        -> BPMN Knowledge Graph
Gherkin Behavioral Specifications -> Scenario Knowledge Graph
Existing Test Cases + evidence    -> Test Knowledge Graph
                                       |
                    alignment / integration
                                       v
                        Unified Knowledge Graph (UKG)
                                       |
                retrieval / reasoning / evidence analysis
                                       v
                  Scenario–Test validation assessment
                                       |
                            explainable result
```

The exact graph schemas, alignment algorithms, evidence model, query mechanism, and validation criteria remain open design questions.

## Persistent UKG

Persistence of the Unified Knowledge Graph is an established architectural requirement (see `docs/adr/0001-persist-the-unified-knowledge-graph.md`).

The graph database, persistence technology, versioning approach, and update strategy are **not** selected. It is also **not** assumed that the three artifact-specific KGs must each be persisted independently.

## UKG versioning

The persistent UKG is a **versioned representation of an analysis scope's artifact state**, not one continuously mutated graph in which knowledge from different revisions may mix.

```text
BPMN revision A + Scenario-set revision B + Test-set revision C + evidence revisions
   -> UKG version N
```

- If the same artifact revisions are analyzed again, a compatible UKG version may be reused.
- If any relevant input revision changes, the service produces a new identifiable UKG version. The previous version remains distinguishable so earlier results stay traceable to the knowledge state they were computed against.
- Semantically: **changed artifact state -> new UKG version**. Incremental extraction/update may later be used as an implementation optimization, but incremental graph mutation is **not** the semantic model.
- An analysis result is traceable to the source artifact identities/revisions, the exact UKG version used, and the specific analysis run/result.

These are distinct concepts: **Artifact Version ≠ UKG Version ≠ Analysis Run / Analysis Result** (e.g. BPMN r7 + Scenario-set r12 + Test-set r20 -> UKG v31 -> run 108; a later run may reuse UKG v31).

Not yet decided: physical snapshot vs delta storage; graph-database versioning mechanism; retention/deletion of historical versions; whether artifact-specific KGs are versioned/persisted independently; whether new UKG construction is physically full or incremental; analysis-result caching.

## Identity and versioning responsibilities

Identifier ownership follows ownership of the concept.

**The external subsystem owns external identity** and supplies, authoritatively:

- Analysis Scope identifier;
- process identifiers;
- scenario identifiers;
- test case identifiers;
- artifact revision/version identifiers;
- identifiers for externally owned evidence where applicable.

The service preserves and echoes these identifiers; it does not mint replacements for externally owned artifacts.

**The thesis service owns internal analysis identity** and mints:

- UKG version identifiers;
- analysis run identifiers.

Every analysis result is traceable across both identity domains:

```text
external scope/artifact identities + revisions
  -> UKG version -> analysis run -> analysis result
```

Example: scope S, process P r5, scenario SC-12 r3, test TC-41 r8 -> UKG v31 -> run 108; the result preserves all references.

Keep distinct: **Request/Correlation Identifier ≠ Analysis Run Identifier ≠ UKG Version Identifier**. A transport-level request/correlation identifier supplied by the subsystem may be echoed but is not the analysis run id. A future internal content fingerprint may support deduplication or reproducibility but must never replace subsystem-owned artifact identity. Identifier formats, UUID schemes, database keys, and hash algorithms are not defined.

## Concurrency, retry, and determinism

Repeated and concurrent requests for the same declared scope and the same artifact revisions are allowed. **Each accepted request produces its own Analysis Run**; a compatible persisted UKG version may be reused across those runs, but a UKG version is not a run.

```text
UKG v31 -> run 101
        -> run 102
        -> run 103
```

V0 does **not** promise: duplicate-request suppression, per-scope serialization, ordering between concurrent runs, locking semantics, exactly-once execution, or exact replay of a previous run. The operation is therefore not described as strictly idempotent: the service has internal persistent state (UKG versions, run identities), and a retry after a lost response may create a new run.

Retries are nonetheless operationally acceptable because the analysis request itself does not mutate BPMN models, scenarios, test cases, or external Scenario–Test links. If exact retry deduplication is later needed, a request/idempotency key is a separate contract decision.

No deterministic analytical output is promised yet. The reasoning mechanism is unselected; probabilistic components (e.g. an LLM) could make two runs over the same UKG differ. What is required is traceability and reproducibility of the **analysis context** — artifact identities/revisions, UKG version, run — not byte-identical output.

## Analysis result persistence

Completed Analysis Results are **first-class persistent research state** of the thesis service. Each completed run has an immutable, run-addressable result linked to the exact context that produced it:

```text
artifact identities + revisions -> UKG version -> analysis run -> immutable result
```

A persisted result is traceable to the Analysis Scope; the relevant process, scenario, test case, and evidence identities; their revisions; the UKG version; and the analysis run.

**Analysis Result ≠ external Scenario–Test validation link.** The service owns the history of analytical results; the external subsystem continues to own user-facing link persistence, presentation, and any externally managed link lifecycle. Retaining results does not transfer link ownership.

Completed results are never overwritten. A later run over changed artifacts, a new UKG version, or a changed analysis method produces a new result; earlier results remain intact.

A completed result may contain supported, contradicted, unresolved, or insufficient-evidence conclusions plus artifact-level diagnostics, and is persisted. A run that fails (timeout, cancellation, resource exhaustion, other cutoff) keeps only run/failure metadata; no incomplete semantic result is persisted or presented as valid.

Not yet decided: physical result storage, retention duration, deletion/archival, compression, whether intermediate reasoning artifacts (prompts, raw LLM responses, queries, embeddings, logs) are persisted, and result caching/reuse.

## Primary analytical goal

For each behavioral scenario, determine which existing test case, or combination of test cases, provides relevant and sufficient evidence for validating that scenario.

The following must **not** automatically be treated as proof of semantic validation:

- a candidate relationship;
- structural traceability;
- graph connectivity;
- semantic similarity;
- LLM output;
- a query result.

## Validation links

The external subsystem manages persisted Scenario–Test links. The thesis service provides the research logic for determining whether such a link should potentially be:

- proposed;
- confirmed;
- updated;
- rejected;
- removed;
- left unresolved.

The lifecycle terminology is not finalized. Whether link mutations are automatic, recommendation-only, or human-confirmed is still undecided.

## Integration boundary

Communication between the thesis service and the external subsystem occurs through explicit REST contracts. Endpoint paths and detailed JSON schemas are not defined yet.

## Evaluation

`Dataset/` contains the empirical evaluation material, including a local copy of the Camunda `bpmn-for-research` repository as a candidate base dataset. The evaluation methodology is not defined in this document.

## Important open questions

- Exact BDD domain model.
- Graph schemas for the three artifact-specific graphs.
- Graph alignment/integration strategy.
- Evidence model and semantic validation criteria.
- UKG persistence technology.
- Graph querying/reasoning strategy.
- Possible use of Cypher.
- Possible LLM-assisted query generation.
- GraphRAG.
- Semantic-link lifecycle.
- Versioning and artifact consistency.
- Evaluation methodology.

## Repository guide

| Path | Purpose |
| --- | --- |
| `CONTEXT.md` | Project context and established terminology |
| `AGENTS.md` | Working rules for AI sessions, incl. research/source policy |
| `docs/adr/` | Accepted architectural decisions |
| `Study Resources/INDEX.md` | Navigation and authority map for the reference library |
| `Study Resources/` | Reference library (knowledge and design input) |
| `Dataset/` | Empirical evaluation material (not a design authority) |
