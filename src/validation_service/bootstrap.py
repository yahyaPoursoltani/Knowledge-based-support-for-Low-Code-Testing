"""Composition root: plain-Python wiring of infrastructure adapters."""

from __future__ import annotations

from validation_service.infrastructure.config import Neo4jSettings
from validation_service.infrastructure.neo4j.connection import Neo4jConnection


def create_neo4j_settings() -> Neo4jSettings:
    """Read Neo4j settings from the process environment."""
    return Neo4jSettings.from_env()


def create_neo4j_connection(settings: Neo4jSettings | None = None) -> Neo4jConnection:
    """Construct a Neo4j connection for the connectivity smoke test."""
    return Neo4jConnection(settings or create_neo4j_settings())
