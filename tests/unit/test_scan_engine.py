"""
Unit tests for ScanEngine.
"""

from src.scan.engine.scan_engine import (
    ScanEngine,
)
from tests.helpers.configuration_factory import (
    create_scan_configuration,
)

from tests.helpers.scan_context_factory import (
    create_scan_context,
)

from src.scan.models.scan_context import ScanContext
from src.camera.services.mock_capture_service import MockCaptureService
from src.camera.services.mock_download_service import MockDownloadService
from src.scanner.services.mock_motion_service import MockMotionService

def test_create_engine() -> None:
    """
    Engine can be created.
    """

    engine = ScanEngine(
        context=create_scan_context(),
        motion_service=MockMotionService(),
        capture_service=MockCaptureService(),
        download_service=MockDownloadService(),
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