"""Neo4j connectivity integration test.

Requires a running Neo4j instance (``docker compose up -d``) and exported
``NEO4J_*`` environment variables. Skipped when the password is not configured.
"""

import pytest

from validation_service.infrastructure.config import ConfigurationError, Neo4jSettings
from validation_service.infrastructure.neo4j.connection import Neo4jConnection

pytestmark = pytest.mark.integration


def test_neo4j_connectivity() -> None:
    try:
        settings = Neo4jSettings.from_env()
    except ConfigurationError as exc:
        pytest.skip(str(exc))

    with Neo4jConnection(settings) as connection:
        assert connection.verify() == 1
