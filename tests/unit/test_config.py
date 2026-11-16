"""Configuration tests that do not touch Neo4j."""

import pytest

from validation_service.infrastructure.config import ConfigurationError, Neo4jSettings


def test_settings_require_password() -> None:
    with pytest.raises(ConfigurationError):
        Neo4jSettings.from_env({})


def test_settings_defaults() -> None:
    settings = Neo4jSettings.from_env({"NEO4J_PASSWORD": "test-password"})

    assert settings.uri == "bolt://localhost:7687"
    assert settings.user == "neo4j"
    assert settings.password == "test-password"


def test_settings_explicit_values() -> None:
    settings = Neo4jSettings.from_env(
        {
            "NEO4J_URI": "bolt://example:7687",
            "NEO4J_USER": "alice",
            "NEO4J_PASSWORD": "test-password",
        }
    )

    assert settings.uri == "bolt://example:7687"
    assert settings.user == "alice"
