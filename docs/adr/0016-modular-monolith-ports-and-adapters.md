# ADR-0016: Modular monolith with ports and adapters

- **Status:** Accepted
- **Date:** 2026-10-27
- **Scope:** Prototype architecture

## Context

The service must remain an independent research implementation while using replaceable infrastructure (Neo4j, FastAPI, future LLM/embedding providers, filesystem, external REST). Research logic will evolve faster than infrastructure, and later experiments may replace persistence or reasoning technologies.

Microservices, queues, and enterprise abstractions would add operational cost without a current requirement. A single deployable with explicit boundaries is sufficient for V0.

## Decision

Use one deployable **modular monolith** with lightweight **Ports-and-Adapters**:

```text
application/domain core -> ports (Protocols) -> infrastructure adapters
```

- `domain/` has no external dependencies.
- `application/` owns the orchestration and defines the outbound ports it needs (UKG, run/result, analysis stages, AI), kept close to the capability that owns them.
- `ingestion/` owns source-independent normalization and parser contracts (Protocols); concrete parsers live in `infrastructure/`.
- `infrastructure/` implements ports using third-party SDKs.
- `bootstrap.py` is the outermost composition root: it constructs the orchestrator, adapters, parsers, and stages. It contains wiring only, never business logic.
- `api/` and `cli/` are inbound (driving) adapters over the application, wired by `bootstrap`.
- Dependencies point inward; the core never imports infrastructure, `bootstrap`, `api`, or `cli`.
- Composition is plain Python in `bootstrap.py`; no DI framework.

Dependency direction: `domain <- application/ingestion <- analysis/infrastructure <- bootstrap <- REST/CLI entry points`.

There is no separate top-level `ports/` package and no top-level `persistence/` package: persistence ports live in `application/`, Neo4j adapters live in `infrastructure/`.

No microservices, message queues, event buses, CQRS, distributed transactions, unit-of-work, generic repository frameworks, or plugin systems.

## Consequences

- Infrastructure can be replaced without rewriting orchestration.
- The first slice stays small and locally runnable.
- Ports must be kept narrow to avoid framework-shaped abstractions.
- Cross-boundary refactors require deliberate changes at the port boundary, not incidental imports.

## Alternatives considered

- **Layered monolith without explicit ports** — fewer files, but infrastructure leaks into core over time.
- **Hexagonal architecture with heavy abstraction layers** — unnecessary ceremony for V0.
- **Microservices** — operational complexity with no established need.
- **Dependency-injection framework** — hides wiring that plain composition shows explicitly.

## Open questions

- Exact port granularity for parsers and AI adapters.
- When (if ever) ports need asynchronous semantics.
