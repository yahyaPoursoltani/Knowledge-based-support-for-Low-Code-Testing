"""Minimal package/import checks that do not require Neo4j."""

import importlib

from validation_service import __version__


def test_package_version() -> None:
    assert __version__ == "0.1.0"


def test_core_packages_import() -> None:
    for module_name in (
        "validation_service.analysis",
        "validation_service.api",
        "validation_service.application",
        "validation_service.application.ports",
        "validation_service.cli",
        "validation_service.domain",
        "validation_service.ingestion",
    ):
        importlib.import_module(module_name)
