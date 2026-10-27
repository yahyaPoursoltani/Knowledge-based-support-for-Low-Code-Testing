# ADR-0020: REST and CLI as inbound adapters over one application core

- **Status:** Accepted
- **Date:** 2026-10-27
- **Scope:** Prototype inbound interaction architecture

## Context

The service must serve two immediately different contexts:

- the operational integration with the external Camunda-based subsystem (REST/JSON);
- independent execution for research/evaluation (starting with local sample files).

Duplicating validation, orchestration, or persistence logic in each entry point would create two cores. A single entry point would either couple research usage to the subsystem or postpone a required capability.

## Decision

Support **two inbound (driving) adapters** in the first slice:

```text
REST adapter  --\
                 -> Analysis Request -> application service/orchestrator
CLI adapter   --/
```

- Both translate source-specific input into the same application-level Analysis Request and invoke the same application service.
- Both are constructed and wired by `bootstrap.py`; adapters do not construct repositories or parsers themselves.
- Adapters contain only: input acquisition, translation to the request, invocation, and result presentation.
- They must not duplicate domain logic, validation logic, persistence logic, KG logic, or orchestration logic.
- REST validates the operational boundary. The CLI is minimal and reads controlled files under `data/sample/`.
- The CLI is not the evaluation harness, not a batch framework, not an interactive application, and not a second core.
- Adding another interaction mechanism later should normally mean adding another inbound adapter, not modifying the analysis core.

## Consequences

- The core can be exercised without Camunda (CLI) and through the real integration boundary (REST).
- Input translation differs by adapter; everything after the request is shared.
- Adapter tests verify translation and presentation, while core tests cover analysis behavior.
- Keeping the CLI small is an explicit design obligation.

## Alternatives considered

- **REST only** — simplest, but does not prove subsystem-independent execution.
- **CLI only** — proves independence but not the operational boundary.
- **Shared entrypoint helper with duplicated validation** — creates a second core by stealth.
- **Notebook-driven entry** — unsuitable as a production boundary.

## Open questions

- Minimal CLI file layout under `data/sample/`.
- Exact REST envelope and CLI arguments (deferred with the detailed contract).
- Whether a future dataset batch runner is a third adapter or part of the evaluation harness.
