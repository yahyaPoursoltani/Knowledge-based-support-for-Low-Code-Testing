# ADR-0007: Analysis scope with a process-level default, not single-model isolation

- **Status:** Accepted (amends ADR-0002)
- **Date:** 2026-10-26
- **Scope:** Knowledge-Based Validation Service (thesis implementation)

## Context

ADR-0002 defined the analysis unit as one BPMN process model with its scenarios, tests, and evidence. That is too narrow: BPMN processes can contain sub-processes, invoke reusable processes via Call Activities, and participate in larger applications. A higher-level scenario may describe behavior realized across contained or called processes, and a test owned by a called process may provide evidence for a scenario owned by the caller.

Conversely, the initial prototype does not need reusable scenarios or application-level analysis. It does need a model that does not preclude them.

## Decision

Prototype V0 uses a **process-level default**:

- behavioral scenarios are defined at the process level;
- test cases are defined at the process level;
- each scenario and test case has one declared owning process.

The analysis unit is modeled as an **Analysis Scope**, which may contain:

- one root process;
- its explicitly supplied contained/subordinate process structures;
- explicitly supplied called/reused processes required for the intended analysis;
- the scenario set declared for the scope;
- the test case set declared for the scope;
- associated evidence.

**Ownership is not participation.** Scenario/test ownership determines declared belonging, not which validation claim the artifact can support. A test owned by P2 may contribute evidence to a scenario owned by P1 within the same scope.

**Membership rules:**

- the external subsystem declares scope membership; it is authoritative;
- the service may infer relationships *inside* the declared scope;
- references to artifacts outside the scope produce explicit diagnostics (e.g. a Call Activity to an unsupplied P3 is reported, not fetched);
- silent scope expansion by names, tags, semantic similarity, graph connectivity, or embedded references is prohibited.

**Extensibility constraint:** the analysis core must not hard-code a permanent single-process assumption. It must remain able to support reusable scenarios/test cases across processes, composite multi-process analysis, and application-level analysis without rewriting the analytical core. Abstractions (e.g. substitutable Analysis Scope implementations, OCP/DIP) are to be designed in a later design session, not here.

## Consequences

- The request/result contract is expressed in terms of a scope, not a model.
- Scope membership and out-of-scope references need explicit representation (request echo and diagnostics).
- Scenario–Test assessment must be able to cross owning processes.
- UKG versions are keyed to scope state, so scope identity affects version identity.
- A later generalisation can extend scope kinds without changing the analysis pipeline.

## Alternatives considered

- **Keep single-model isolation** — simpler, but cannot represent cross-process behavior or cross-process evidence.
- **Auto-expand the scope by following Call Activities** — convenient, but hides missing inputs and violates declared-membership authority.
- **Adopt application-level scope immediately** — premature for V0; adds reusable-artifact semantics that are not designed.
- **Model membership as graph connectivity alone** — conflates declared membership with inferred relationships.

## Open questions (not decided by this ADR)

- How scope identity is derived and versioned.
- Whether a scope may contain multiple roots or only one.
- How applications composed of several processes are expressed.
- Whether the full call graph must always be supplied or only the needed subset.
- How reusable scenarios/tests across processes will be modeled.
- The abstraction design for substitutable scope kinds.
