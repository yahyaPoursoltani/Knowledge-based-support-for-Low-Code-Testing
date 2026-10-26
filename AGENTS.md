# AGENTS.md

## Current state
- Research-design phase: documentation only. No application source, manifests, lockfiles, or CI yet.
- Do not assume a language or toolchain. List the directory before proposing commands, and never invent build/test/lint commands.
- Do not create application code, API endpoints, graph schemas, or framework projects unless the researcher explicitly asks.
- When tooling is added, replace the "Commands" section below with the real, verified commands and delete this note.

## Environment gotchas
- Platform is Windows with PowerShell 5.1. `&&` and `||` are unsupported; chain with `; if ($?) { ... }`.
- The working path contains a space (`D:\PhD Thesis Solution`) — always quote paths.
- Git repo exists (initialized on `main`, no commits yet). Keep generated artifacts out of version control via `.gitignore`.

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
Not defined yet. Fill in once tooling exists, including how to run a single test:

```text
install:
run:
test:
test (single):
lint:
typecheck:
```

## Structure
Documentation foundation only (no code yet):

- `README.md` — project orientation, research problem, system boundary, open questions.
- `CONTEXT.md` — established terminology (source-of-truth vocabulary); deferred terms are marked.
- `docs/adr/` — accepted architectural decisions, numbered (`0001-...`).
- `Study Resources/` — reference library; navigate via `Study Resources/INDEX.md`, inspect targets only.
- `Dataset/` — empirical evaluation material (candidate base: `bpmn-for-research-master`); not a design authority.
- `resource-structure.txt` — stale folder-listing snapshot; verify with a live listing before relying on it.

When code appears, record real entrypoints and package boundaries here.
