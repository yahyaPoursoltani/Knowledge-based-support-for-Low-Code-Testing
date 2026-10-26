# Knowledge-Based Validation Service for Behavioral Requirements and Model-Based Tests

Implementation prototype of a PhD thesis. This repository holds the thesis research documentation, the planned implementation of the **Knowledge-Based Validation Service**, and the empirical evaluation material. There is no application code yet; the project is in the research-design phase.

## Research problem

Model-based and low-code testing can produce tests that provide evidence that an implementation conforms to its conceptual/process model, while still failing to establish that the conceptual model correctly represents stakeholder and domain expectations.

Two concerns must not be conflated:

- **testing the implementation against the model** — does the running system behave as the process model prescribes?
- **validating model/system behavior against behavioral requirements** — does the modeled behavior express what stakeholders actually require?

This thesis investigates the second concern. It does **not** claim that the problem is already empirically solved.

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
- generating the empirical ground truth used to evaluate the thesis method;
- acting as an autonomous substitute for stakeholder/domain-expert judgment when artifacts and evidence are insufficient.

Structural coverage and traceability are **not** excluded as analysis. The research must distinguish:

1. a behavioral requirement/scenario **not represented** in the process model;
2. a represented requirement/scenario **lacking structural traceability** to tests;
3. a represented and structurally covered requirement/scenario **still lacking sufficient semantic validation evidence**.

The service may compute and expose structural coverage/traceability information when it is needed for Scenario–Test assessment, gap classification, evidence analysis, or explanation. It must not become a general-purpose coverage management/reporting subsystem, and conventional coverage metrics are not the primary thesis deliverable. It may assess whether BPMN behavior, scenarios, tests, and evidence are mutually supportive or inconsistent, but it must not claim absolute business correctness from the BPMN model alone.

## Failure and deficiency levels

The service distinguishes three levels; they must not be collapsed.

**1. Request-level fatal failure.** The whole analysis fails only when the request is structurally unusable: invalid envelope; unidentifiable analysis unit; missing artifact identity/revision information; missing required BPMN input; or a BPMN representation so unreadable that process knowledge cannot be constructed. These failures are explicit and are never silently normalized.

**2. Artifact-level or analysis-level deficiency.** When individual artifacts are incomplete, inconsistent, missing evidence, or locally unparseable, the service continues with what remains analyzable and returns partial results plus explicit artifact-level failures and the limitations they impose. Example: one unparseable scenario still yields results for the valid scenarios, an explicit failure for that scenario, and stated limits on conclusions. Missing execution evidence is not fatal; it leaves an assessment unresolved rather than validating or invalidating it.

**3. Research-level gap or validation conclusion.** Only evidence-supported interpretations become representation, traceability, or semantic-validation conclusions. Input inconsistency does **not** automatically equal a research-level gap: a test referencing a scenario not included in the request may indicate an incomplete request package, not an absent requirement.

Rules: analyze usable information best-effort; preserve provenance of deficiencies; expose unresolved references explicitly; return partial or unresolved conclusions where necessary; never invent missing information; never silently normalize inconsistencies; never treat absence of evidence as evidence of absence; never automatically map every input inconsistency to a gap.

## Operational mode and analysis unit

The service is **on-demand**: the external subsystem decides when an analysis is required, sends **one analysis request**, and receives **one structured, explainable analysis result**. The initial prototype does not poll, re-analyze in the background, or synchronize event-driven.

The **analysis unit** is one BPMN process model together with:

- all behavioral scenarios associated with that model;
- all existing test cases associated with that model;
- any available test/execution evidence for those test cases.

The unit is model-scoped rather than scenario-scoped because the analysis integrates BPMN, Scenario, and Test knowledge into a shared UKG, and because a single scenario may be validated by one test case or by a combination of test cases.

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

The persistent UKG is a **versioned representation of an analysis unit's artifact state**, not one continuously mutated graph in which knowledge from different revisions may mix.

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
