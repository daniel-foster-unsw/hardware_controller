"""
Integration tests for ScanEngine.
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
from tests.helpers.scan_engine_factory import (create_scan_engine)
from tests.helpers.scan_engine_fixture import ScanEngineFixture
def test_complete_scan() -> None:
    """
    Complete scan executes successfully.
    """

    fixture = create_scan_engine()

    fixture.engine.execute()
    

    assert not fixture.motion.initialised
    assert not fixture.capture.initialised

    assert fixture.motion.homed

    assert fixture.capture.capture_count > 0

    assert fixture.download.downloaded

    assert fixture.context.log.capture_count == (
        fixture.capture.capture_count
    )



def test_all_positions_are_visited() -> None:
    """
    Every scan position is visited.
    """

    fixture = create_scan_engine()

    fixture.engine.execute()

    

    expected = tuple(

        fixture.context.session.position_generator

    )

    assert (
        fixture.motion.visited_positions
        == expected
    )




def test_every_position_is_captured() -> None:
    """
    Every scan position generates one CaptureRecord.
    """

    fixture = create_scan_engine()
   
    fixture.engine.execute()

    expected = len(

        tuple(
            fixture.context.session.position_generator
        )

    )

    assert (
        fixture.capture.capture_count
        == expected
    )


def test_scan_log_contains_every_capture() -> None:
    """
    ScanLog contains every CaptureRecord.
    """

    fixture = create_scan_engine()
    fixture.engine.execute()

    expected = len(

        tuple(
            fixture.context.session.position_generator
        )

    )

    assert (
        fixture.context.log.capture_count
        == expected
    )


def test_download_count() -> None:
    """
    All images are downloaded.
    """

    fixture = create_scan_engine()
    fixture.engine.execute()

    assert (
        fixture.download.download_count
        == fixture.context.log.image_count
    )