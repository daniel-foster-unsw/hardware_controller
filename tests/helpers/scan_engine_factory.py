"""
Shared ScanEngine factory.
"""

from src.camera.services.mock_capture_service import (
    MockCaptureService,
)

from src.camera.services.mock_download_service import (
    MockDownloadService,
)

from src.scan.engine.scan_engine import (
    ScanEngine,
)

from src.scanner.services.mock_motion_service import (
    MockMotionService,
)

from tests.helpers.scan_context_factory import (
    create_scan_context,
)

from tests.helpers.scan_engine_fixture import (
    ScanEngineFixture,
)


def create_scan_engine(
    block_motion: bool = False,
) -> ScanEngineFixture:
    """
    Create a ScanEngine with mock services.
    """

    context = create_scan_context()

    motion = MockMotionService(
        block_motion=block_motion,
    )

    capture = MockCaptureService()

    download = MockDownloadService()

    engine = ScanEngine(
        context=context,
        motion_service=motion,
        capture_service=capture,
        download_service=download,
    )

    return ScanEngineFixture(
        engine=engine,
        context=context,
        motion=motion,
        capture=capture,
        download=download,
    )