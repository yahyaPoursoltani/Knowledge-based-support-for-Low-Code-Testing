# ADR-0017: Real Neo4j persistence from the first slice, via two narrow ports

- **Status:** Accepted
- **Date:** 2026-10-27
- **Scope:** Prototype persistence

## Context

The UKG is persistent and versioned (ADR-0001, ADR-0005). Promising persistence without exercising it risks discovering adapter problems only after the orchestration is built. Neo4j is the accepted prototype graph technology.

Two distinct states exist: versioned UKG knowledge, and immutable analysis runs/results. They have different lifecycles and must not be conflated.

## Decision

- Run a real **Neo4j** instance from the first vertical slice, preferably via Docker Compose.
- Neo4j is an **infrastructure adapter**, never a domain type; the core must not import driver APIs, Cypher, or Neo4j-specific entities.
- Define two narrow ports:
  1. **UKG Version Repository**;
  2. **Analysis Run / Result Repository**.
- Use the **same Neo4j instance** for both in the first slice. This is an implementation simplification, not a conceptual merge: UKG knowledge state != Analysis Run/Result history, and result records do not become part of the UKG semantic schema merely because they share a database.
- No generic CRUD repository, ORM abstraction, unit-of-work, or distributed transactions.
- The UKG state required by a completed result is persisted before that result.
- Failed runs persist only run/failure metadata; never an incomplete semantic result.
- The first slice uses only the minimum graph representation needed to prove persistence; the real schema is deferred.
- SQLite, filesystem JSON, and in-memory result persistence are not on the primary first-slice development path.

## Consequences

- Persistence and retrieval are proven end-to-end early.
- Orchestration depends on interfaces, so an in-memory or alternative adapter remains possible.
- Docker becomes a local development requirement for persistence tests.
- Two adapters share one Neo4j instance without pretending they are transactionally unified.

## Alternatives considered

- **In-memory persistence for the slice** — fastest, but does not validate the accepted technology.
- **Filesystem/JSON persistence** — simple, but defers Neo4j integration risk.
- **One generic repository** — hides the lifecycle difference between UKG versions and results.
- **Unit of work across stores** — unnecessary and misleading for a single-node prototype.

## Open questions

- Neo4j image/version and local credentials.
- Minimum placeholder graph representation for the slice.
- How result records are separated from UKG records inside the instance.
- Retention and historical access.
