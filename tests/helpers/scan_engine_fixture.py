"""
Shared ScanEngine fixture for tests.
"""

from dataclasses import dataclass

from src.camera.services.mock_capture_service import (
    MockCaptureService,
)
from src.camera.services.mock_download_service import (
    MockDownloadService,
)
from src.scan.engine.scan_engine import (
    ScanEngine,
)
from src.scan.models.scan_context import (
    ScanContext,
)
from src.scanner.services.mock_motion_service import (
    MockMotionService,
)


@dataclass(
    frozen=True,
    slots=True,
)
class ScanEngineFixture:
    """
    ScanEngine test fixture.
    """

    engine: ScanEngine

    context: ScanContext

    motion: MockMotionService

    capture: MockCaptureService

    download: MockDownloadService