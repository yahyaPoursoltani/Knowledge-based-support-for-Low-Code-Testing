"""Minimal Neo4j connection handling.

This module deliberately contains no graph/domain logic. It only creates a
driver, verifies connectivity with a trivial query, and closes the driver.
"""

from __future__ import annotations

from types import TracebackType

from neo4j import Driver, GraphDatabase

from validation_service.infrastructure.config import Neo4jSettings


class Neo4jConnection:
    """Owns the lifecycle of a Neo4j driver for infrastructure use."""

    def __init__(self, settings: Neo4jSettings) -> None:
        self._settings = settings
        self._driver: Driver | None = None

    def connect(self) -> Driver:
        """Create the driver lazily and return it."""
        if self._driver is None:
            self._driver = GraphDatabase.driver(
                self._settings.uri,
                auth=(self._settings.user, self._settings.password),
                connection_timeout=5.0,
            )
        return self._driver

    def verify(self) -> int:
        """Verify connectivity by running a trivial query and return its result."""
        driver = self.connect()
        driver.verify_connectivity()
        with driver.session() as session:
            record = session.run("RETURN 1 AS ok").single()
        if record is None:
            raise RuntimeError("Neo4j connectivity check returned no record")
        return int(record["ok"])

    def close(self) -> None:
        """Close the driver; safe to call more than once."""
        if self._driver is not None:
            self._driver.close()
            self._driver = None

    def __enter__(self) -> Neo4jConnection:
        self.connect()
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        self.close()
