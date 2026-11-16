"""Infrastructure configuration read from environment variables."""

from __future__ import annotations

import os
from collections.abc import Mapping
from dataclasses import dataclass, field


class ConfigurationError(RuntimeError):
    """Raised when required configuration is missing or invalid."""


@dataclass(frozen=True, slots=True)
class Neo4jSettings:
    """Connection settings for the local Neo4j instance."""

    uri: str
    user: str
    password: str = field(repr=False)

    @classmethod
    def from_env(cls, env: Mapping[str, str] | None = None) -> Neo4jSettings:
        """Build settings from environment variables.

        ``NEO4J_PASSWORD`` is required. ``NEO4J_URI`` and ``NEO4J_USER`` fall back
        to local-development defaults.
        """
        values = os.environ if env is None else env
        password = (values.get("NEO4J_PASSWORD") or "").strip()
        if not password:
            raise ConfigurationError(
                "NEO4J_PASSWORD must be set (see .env.example) and exported to the process."
            )

        uri = (values.get("NEO4J_URI") or "").strip() or "bolt://localhost:7687"
        user = (values.get("NEO4J_USER") or "").strip() or "neo4j"
        return cls(uri=uri, user=user, password=password)
