# Study Resources — Index and Authority Map

`Study Resources/` is a **reference library**. It is not the specification of the project, and it does not own the project's terminology or architecture.

Working rules:

- Do **not** recursively inspect the whole library during normal work.
- Use **targeted source inspection** based on the current research/design question.
- Prefer the smallest source that answers the question; cite the file you consulted.
- When a design decision and a source disagree, follow the authority order in `AGENTS.md`.

The root file `resource-structure.txt` is a folder-listing snapshot. Treat it as a convenience only; prefer a live directory listing when accuracy matters.

## Primary Thesis Sources

### `PhD Proposal Docs/proposal.pdf`

**Role:** approved thesis research baseline.

Use for:

- approved research scope;
- research objectives/questions;
- research motivation;
- proposed high-level solution;
- intended evaluation direction.

**Authority:** HIGH for thesis scope.

### `PhD Proposal Docs/sosym-Article.pdf`

**Role:** precise formal problem-description reference.

Use for:

- formal terminology;
- formal definitions;
- the distinction between model representation, test coverage, and semantic validation;
- reasoning about the Model-Bounded Testing Trap.

**Warning:** the manuscript was rejected. Its formalization may be used as a precise description of the research problem, but its propositions and contribution must **not** be treated as empirically validated results.

### `PhD Proposal Docs/Sosym Reject Reasons.txt`

**Role:** critical research/evaluation guidance.

Use for:

- identifying weaknesses in the previous paper;
- avoiding contributions that merely restate definitions;
- ensuring the implementation enables meaningful empirical or case-based validation;
- improving the technical and evaluation contribution.

## Behavioral Specification Reference

### `Books/Software Engineering/BDD in Action.pdf`

**Role:** primary conceptual reference for BDD and behavioral-scenario semantics.

Use especially for:

- Feature; Story (where relevant); concrete examples;
- Scenario; Given / When / Then; And / But;
- Scenario Outline; Examples;
- executable specifications; expressive scenarios;
- the relationship between requirements, examples, scenarios, and acceptance criteria.

**Project rule:** do not flatten a behavioral specification into an arbitrary text blob if the source representation contains meaningful BDD structure.

Detailed internal modeling remains a later design decision.

## Knowledge Graph References

Books under `Books/LLMs and KG/Knowledge Graphs/`.

Use for targeted questions involving:

- knowledge graph modeling;
- graph integration;
- entity/concept alignment;
- provenance;
- graph retrieval;
- GraphRAG;
- graph-oriented evaluation.

These books provide technical guidance. They do **not** define thesis-specific domain semantics.

## LLM and Agentic AI References

Books under `Books/LLMs and KG/Agentic AI/`.

Use only when the current design question involves:

- LLM-based information extraction;
- LLM/KG interaction;
- prompt engineering;
- agentic workflows;
- query generation;
- GraphRAG orchestration.

The presence of these sources does **not** imply that an LLM must be used. In particular, LLM-generated Cypher is currently a hypothesis, not an architectural requirement.

## Research Papers

`ResearchPapers/` is organized thematically. Papers should be selected through targeted searches according to the current question; this index does not summarize individual PDFs.

Categories currently present:

- `AI and LLM in LCDPs`
- `BDD and Low-Code`
- `challenges in Low-Code Development`
- `Citizen Developers` (with a nested `LCDP-Process` folder)
- `Executive DSL`
- `Lowcomote Reports`
- `Patterns and Best Practices`
- `Practical Usage`
- `Review`
- `Test and QA` (with nested `Testing in LCDP and BPMN`, which contains `BPMN Test`, `LCDP QA`, `LCDP Test`, and `other Related`)

Example mappings:

| Question | Start here |
| --- | --- |
| BDD / scenario semantics | `BDD and Low-Code` |
| BPMN / testing | `Test and QA/Testing in LCDP and BPMN` |
| Low-code testing | `Test and QA` |
| Citizen-developer context | `Citizen Developers` |
| LLM usage in low-code | `AI and LLM in LCDPs` |
| Low-code challenges | `challenges in Low-Code Development` |

## Dataset separation

- `Study Resources/` contains knowledge and references for understanding and design.
- `Dataset/` contains empirical material for evaluation.

The Dataset must **not** be used as the authority for domain definitions or architecture.
