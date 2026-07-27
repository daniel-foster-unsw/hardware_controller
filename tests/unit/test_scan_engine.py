"""
Unit tests for ScanEngine.
"""

from src.scan.engine.scan_engine import (
    ScanEngine,
)
from tests.helpers.configuration_factory import (
    create_scan_configuration,
)


def test_create_engine() -> None:
    """
    Engine can be created.
    """

    engine = ScanEngine(
        create_scan_configuration(),
    )

    assert (
        engine.context.configuration
        == create_scan_configuration()
    )

    assert (
        engine.context.geometry.camera_count
        == 5
    )

    assert (
        engine.context.log.configuration
        == create_scan_configuration()
    )

    assert (
        engine.context.session.configuration
        == create_scan_configuration()
    )