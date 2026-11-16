# AGENTS.md

## Current state
- Implementation Step 1 is complete: `src/validation_service` skeleton, editable install, Neo4j connectivity adapter, unit + integration tests. No REST API, orchestrator, or vertical slice yet.
- Follow `docs/prototype-architecture-baseline.md` and ADR-0016–0020. Do not add graph schemas, Cypher, evidence algorithms, or LLM code before the relevant design step.
- Commands below are verified; use `.venv` and never invent alternatives.

## Environment gotchas
- Platform is Windows with PowerShell 5.1. `&&` and `||` are unsupported; chain with `; if ($?) { ... }`.
- The working path contains a space (`D:\PhD Thesis Solution`) — always quote paths.
- Git repo exists on `main` with commits; keep generated artifacts out of version control via `.gitignore`.
- Neo4j runs through Docker Compose (`neo4j:2026.05-community`, locally cached). The Python code reads `NEO4J_*` from the process environment; `.env` is read by Docker Compose only (no dotenv dependency), so export the same values for tests/PyCharm.

## Conventions
- Owner preferences (apply unless the project establishes otherwise):
  - Python: type hints, PEP 8, docstrings for public functions, descriptive names.
  - Prefer comprehensions/functional style when it stays readable.
  - Semantic commit messages (`feat:`, `fix:`, `docs:`); work on feature branches, not `main`/`master`; run tests before committing.
- Never commit or push unless explicitly asked.
- Review and test AI-generated code, and mark it as AI-generated when added.
- Global instructions live in `C:\Users\yahya\.config\opencode\AGENTS.md` and already apply — don't duplicate them here; only record project-specific differences.

## Research and Source Policy

### Repository boundary
- Normal inspection must remain inside `D:\PhD Thesis Solution`.
- Do not inspect unrelated directories or drives. Do not perform broad filesystem discovery.

### Targeted research only
- Do not recursively scan all of `Study Resources/` or `Dataset/`.
- Use targeted file inspection based on the active question.
- If additional evidence is needed, name the relevant source category (`Study Resources/INDEX.md`) before performing a broader search.

### Source authority order
When sources or assumptions conflict, use this priority:

1. Explicit decisions made by the researcher during the current Grill/design process.
2. Approved thesis proposal for research scope and approved objectives.
3. Accepted project `CONTEXT.md` terminology and accepted ADRs.
4. SoSyM manuscript for formal problem definitions and terminology.
5. Thesis-specific progress/planning documents, when available.
6. Undergraduate-project documentation for the external Camunda subsystem boundary and integration responsibilities.
7. Books and research papers for conceptual and technical guidance.
8. Dataset material for empirical evaluation only.

Later explicit researcher decisions override earlier implementation assumptions.

### Conflicts
- Never silently reconcile conflicting sources. Identify the disagreement, state which source has higher authority, explain the consequence, and ask the researcher when a design choice is still required.

### Research claims vs engineering decisions
- Do not infer a research claim from an implementation convenience.
- Keep established research claims, research hypotheses, empirical findings, architectural decisions, and implementation choices distinct.

### LLM discipline
- Do not assume LLM usage unless the current design justifies it.
- Never treat an LLM answer, embedding similarity, graph-path existence, or a Cypher result as semantic-validation evidence by itself.

### Evidence discipline
- Do not convert absence of evidence into evidence of absence.
- Represent insufficient or unknown evidence explicitly.

### Dataset discipline
- Do not inspect `Dataset/` during ordinary architecture/domain sessions unless explicitly requested.
- Do not train, tune, or derive domain definitions from the evaluation dataset unless that is explicitly part of the designed methodology.

## Commands
Verified on Windows/PowerShell 5.1 from the repository root:

```text
install:      python -m venv .venv
              .\.venv\Scripts\python.exe -m pip install -e ".[dev]"
neo4j:        docker compose up -d          # needs NEO4J_PASSWORD in env/.env
stack:        .\run.bat                     # restarts Neo4j if running + connectivity check
stack stop:   .\run.bat stop
run:          not defined yet (no service entrypoint)
test:         .\.venv\Scripts\python.exe -m pytest -m "not integration"
test (single): .\.venv\Scripts\python.exe -m pytest tests/unit/test_config.py::test_settings_defaults
test (ne4j):  .\.venv\Scripts\python.exe -m pytest -m integration
lint:         .\.venv\Scripts\ruff.exe check .
typecheck:    not configured (mypy deferred)
```

Integration tests require `docker compose up -d` and exported `NEO4J_URI`, `NEO4J_USER`, `NEO4J_PASSWORD`.

## Structure
Python `src/` layout with the accepted modular layers:

- `src/validation_service/` — package root:
  - `domain/` pure models; `application/` orchestrator + `ports/`; `ingestion/` contracts/normalization; `analysis/` stage placeholders; `infrastructure/` Neo4j + config; `api/` and `cli/` inbound placeholders.
  - `bootstrap.py` — only composition root; imports infrastructure, never imported by core.
- `tests/unit/`, `tests/integration/`, `tests/fixtures/`.
- `data/sample/` — small development fixtures only. `Dataset/` and `Study Resources/` are not package content and must not be scanned by ordinary tests.
- `pyproject.toml`, `docker-compose.yml`, `.env.example` — project/tooling/Neo4j setup.
- `docs/adr/`, `docs/prototype-architecture-baseline.md`, `CONTEXT.md`, `README.md` — decisions and terminology.

No service entrypoint exists yet (no FastAPI app, orchestrator, or vertical slice).
