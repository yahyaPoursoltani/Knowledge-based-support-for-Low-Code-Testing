# Prototype Architectural Baseline

- **Status:** Accepted — implementation may begin after review
- **Date:** 2026-10-27
- **Scope:** Minimum architecture for the repository skeleton and first runnable vertical slice. Detailed graph schemas, algorithms, API contracts, and evaluation design remain deferred.

## Architecture style

One deployable **Knowledge-Based Validation Service**: a modular monolith using lightweight **Ports-and-Adapters**.

```text
Inbound adapters (REST, CLI, future)
        |
        v
Application core / orchestrator
   |          |            |
analysis   repository   AI/other
  ports       ports       ports
   |          |            |
   +----------+------------+
        |
Infrastructure adapters (Neo4j, parsers, filesystem, future LLM)
```

No microservices, queues, event buses, CQRS, distributed transactions, unit-of-work, generic repository frameworks, DI frameworks, or plugin systems. Composition is plain Python in `bootstrap.py`.

## Repository layout (initial skeleton)

The existing repository root remains the Python project root. `Dataset/` and `Study Resources/` stay in place; they are never package content.

```text
project-root/
├── pyproject.toml
├── README.md
├── CONTEXT.md
├── AGENTS.md
├── .gitignore
├── .env.example
├── docker-compose.yml
├── src/
│   └── validation_service/
│       ├── __init__.py
│       ├── bootstrap.py             # outermost composition/wiring only
│       ├── api/                     # REST inbound adapter
│       │   ├── app.py
│       │   ├── routes.py
│       │   ├── schemas.py
│       │   └── dependencies.py  # FastAPI dependency wiring
│       ├── cli/                 # CLI/file inbound adapter
│       │   └── main.py
│       ├── application/
│       │   ├── analysis_service.py   # orchestrator
│       │   ├── commands.py           # Analysis Request
│       │   ├── results.py            # Analysis Result
│       │   └── ports/
│       │       ├── persistence.py    # UKG + run/result ports
│       │       ├── analysis.py       # stage ports
│       │       └── ai.py             # future AI/LLM port
│       ├── domain/                  # pure domain models
│       │   └── models.py
│       ├── ingestion/               # source-independent normalization
│       │   ├── contracts.py         # parser Protocols
│       │   └── normalization.py
│       ├── analysis/                # stage implementations (placeholders)
│       │   ├── candidate_discovery.py
│       │   ├── structural_traceability.py
│       │   └── validation_assessment.py
│       └── infrastructure/          # concrete adapters
│           ├── config.py
│           ├── neo4j/               # UKG + result adapters
│           ├── parsers/             # BPMN XML, Gherkin, Test JSON
│           └── filesystem/          # dataset/sample access
├── tests/
│   ├── unit/
│   ├── integration/
│   └── fixtures/
├── data/
│   └── sample/                      # tiny dev fixtures only
├── notebooks/
├── Dataset/                         # research data (git-ignored)
├── Study Resources/                 # reference library (git-ignored)
└── docs/
    └── adr/
```

Distribution name `knowledge-validation-service`; import package `validation_service`; `src/` layout; editable install with `pip install -e .`; no manual `PYTHONPATH`.

**Note:** the earlier draft included a top-level `persistence/` directory. Q7 supersedes it: outbound persistence ports live in `application/ports/`, and Neo4j adapters live in `infrastructure/neo4j/`.

## Module responsibilities and dependency rules

| Module | Responsibility | May depend on |
| --- | --- | --- |
| `domain/` | Pure domain models/concepts; no FastAPI, Neo4j, parsing libraries, filesystem, SDKs, or transport concerns. | standard library only |
| `application/` | Orchestrator, Analysis Request/Result, outbound ports (UKG, run/result, stages, AI). Ports live close to the capability that owns them. | `domain` |
| `ingestion/` | Source-independent normalization and parser contracts (Protocols) for BPMN/Gherkin/Test. No source-specific logic (no Camunda, no dataset). | `domain` |
| `analysis/` | Placeholder implementations of the three stages. | `domain`, `application` ports |
| `infrastructure/` | Neo4j adapters, concrete parsers, filesystem/dataset adapter, config, future LLM/embedding/REST adapters. | `application`, `ingestion`, third-party SDKs |
| `bootstrap.py` | **Outermost composition root.** Constructs and wires the orchestrator, Neo4j repositories, parsers, stages, and future adapters. Wiring only: no business logic. | `application`, `ingestion`, `analysis`, `infrastructure` |
| `api/` | REST inbound adapter: HTTP, request/response models, error mapping. Wired by bootstrap, not constructing infrastructure itself. | `application`, `bootstrap` (wiring only) |
| `cli/` | CLI/file inbound adapter: read samples, translate to the same command, invoke, print. Wired by bootstrap. | `application`, `bootstrap` (wiring only) |

The core (`domain`, `application`, `ingestion`, `analysis`) must never import `api`, `cli`, `bootstrap`, `infrastructure`, FastAPI, the Neo4j driver, or parser libraries. Inner layers never depend on outer layers.

Dependency direction:

```text
domain
  <- application / ingestion contracts
  <- analysis implementations + infrastructure adapters
  <- bootstrap (composition)
  <- executable entry points (REST / CLI)
```

## Inbound adapters (REST + CLI)

REST and CLI are independent driving adapters over the same application core. Both are constructed and wired by `bootstrap.py`; neither constructs repositories or parsers itself. They only:

1. obtain input from their context;
2. translate it into the common Analysis Request;
3. invoke the same application service;
4. present/serialize the returned result.

No duplicated domain, validation, persistence, KG, or orchestration logic. Adding another interaction mechanism later means adding another inbound adapter, not modifying the core.

- **REST** validates the operational Camunda integration boundary; it may accept a JSON envelope carrying BPMN XML, Gherkin source, Test Case JSON, and evidence JSON.
- **CLI** is intentionally minimal: it constructs an Analysis Request from `data/sample/`. It is not the evaluation harness, a batch framework, an interactive app, or a second core.

## Ingestion and input paths

```text
Transport adapter != artifact native representation != normalized internal representation
```

- Native BPMN/XML is ingested directly (research dataset path) through the filesystem/dataset adapter.
- REST may carry native artifact content inside JSON; it must not require the subsystem to build thesis-specific semantic/KG entities.
- All sources converge on one Analysis Request and shared normalization; the core is source-independent.
- The service remains independently executable without the Camunda subsystem.

## Persistence

Two narrow ports, both implemented on the **same Neo4j instance** in the first slice:

1. **UKG Version Repository**;
2. **Analysis Run / Result Repository**.

Using one instance is a prototype simplification, not a conceptual merge. UKG knowledge state != Analysis Run/Result history, and result records do not become UKG schema merely by sharing the database.

Rules:

- UKG state required by a completed result exists before the result is persisted.
- Failed runs persist run/failure metadata only; never an incomplete semantic result.
- Results are immutable; applicability is bound to the exact artifact state. Changed relevant state -> new UKG version -> new run -> new result; old results remain historical.
- No SQLite, filesystem JSON, or in-memory result persistence on the primary first-slice path.
- No real graph schema yet; only the minimum representation needed to prove persistence.

## Orchestration (first slice)

```text
start service
  -> receive (REST) or construct (CLI) Analysis Request
  -> validate minimum request structure
  -> create Analysis Run
  -> minimal artifact ingestion
  -> minimal internal representations
  -> construct minimal UKG state
  -> persist/retrieve through Neo4j
  -> Candidate Discovery -> Structural Traceability -> Validation Assessment (placeholders)
  -> produce structured Analysis Result
  -> persist completed result
  -> return/display result
```

Synchronous request/response (ADR-0008). The three stages are extension seams, not algorithms; placeholders must be explicit and must not masquerade as real validation. The Target BPMN Process remains essential analytical context.

## Extension points

- AI/LLM port -> provider adapter; provider, model, prompt, and stage assignment are deferred.
- Embedding/vector port reserved on the same principle.
- Parser ports for BPMN/Gherkin/Test formats.
- Filesystem/dataset adapter with configurable root.
- External REST clients as adapters.
- Future graph/database technology behind the persistence ports.

## Environment and tooling

- Python 3.12, `venv`, `pip`, project-local `.venv/`.
- `pyproject.toml`, `pytest`, `ruff`, type annotations at module boundaries.
- `mypy` deferred; `uv` not required; production logic must not live in notebooks.
- `.idea/` remains git-ignored.
- Neo4j runs locally via Docker Compose; connection data comes from environment variables and/or `.env`; `.env.example` is provided; secrets are never committed.

## First vertical-slice acceptance criteria

1. `python -m venv .venv`, `pip install -e .` succeeds; `from validation_service...` works in tests, CLI, and notebooks.
2. `docker compose up -d` starts Neo4j; the service connects using values from `.env` (no hard-coded credentials/paths).
3. `pytest` runs unit tests without Neo4j; documented integration test runs against the Docker instance; `ruff check` passes.
4. REST `POST` accepts a minimal self-contained Analysis Request (target BPMN XML, Gherkin source, Test JSON, identities/revisions, optional evidence) and returns one structured response.
5. The run mints an Analysis Run id and a UKG version id; the UKG state is persisted in Neo4j and retrieved again.
6. The three stages are invoked in order; the result is clearly a placeholder (unresolved/insufficient), not a fake validation.
7. The completed result is persisted immutably and is addressable by run id; the response echoes external identities/revisions plus the minted UKG version and run id.
8. Repeating the request with unchanged artifact revisions may reuse the compatible UKG version but creates a new run; changing any relevant revision creates a new UKG version and leaves prior results intact.
9. The CLI builds the same Analysis Request from `data/sample/`, invokes the same application service, and prints the result without duplicated core logic.
10. An invalid/unusable request fails explicitly as an Input Failure with no result persisted; failed execution, if triggered, persists run/failure metadata only.
11. Core modules import no FastAPI, Neo4j, parser-library, filesystem APIs, `bootstrap`, or `infrastructure` (verified by a focused architecture test or review); `bootstrap.py` contains wiring only.
12. No real KG schema, alignment, similarity, scoring, or evidence-sufficiency logic is implemented in this slice.

## Deferred

Detailed BPMN/Scenario/Test/UKG schemas and provenance graph; Cypher; merge algorithms; embeddings/vector indexes; GraphRAG; LLM prompting/Cypher/agents; similarity and evidence-sufficiency algorithms; scoring; final assessment vocabulary; detailed REST contract and Camunda/CPT JSON version; evaluation harness/data scanning; ground truth; deployment beyond local Docker; result lifecycle labels; configuration-library choice.
