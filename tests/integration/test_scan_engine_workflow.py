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

    assert fixture.motion.homed

    assert fixture.capture.capture_count > 0

    assert fixture.download.downloaded

    assert (
    fixture.context.log.capture_count
    == fixture.context.configuration.capture_count
)



def test_all_positions_are_visited() -> None:
    """
    Every planned position is visited.
    """

    fixture = create_scan_engine()

    expected = tuple(
        fixture.context.session.position_generator
    )

    fixture.engine.execute()

    assert (
        fixture.motion.visited_positions
        == expected
    )




def test_every_position_is_captured() -> None:
    """
    One capture occurs at every position.
    """

    fixture = create_scan_engine()

    fixture.engine.execute()

    assert (

        fixture.capture.capture_count

        == fixture.context.log.capture_count

    )


def test_scan_log_contains_all_captures() -> None:
    """
    ScanLog stores every capture.
    """

    fixture = create_scan_engine()

    fixture.engine.execute()

    assert (

        fixture.context.log.capture_count

        == fixture.capture.capture_count

    )

    assert (

        fixture.context.log.image_count

        == fixture.capture.capture_count * 5

    )


def test_scan_log_contains_every_image() -> None:
    """
    ScanLog image count matches CaptureService.
    """

    fixture = create_scan_engine()

    fixture.engine.execute()

    assert (
        fixture.context.log.image_count
        == fixture.capture.image_count
    )

def test_downloads_complete() -> None:
    """
    Images are downloaded.
    """

    fixture = create_scan_engine()

    fixture.engine.execute()

    assert fixture.download.downloaded

    assert (

        fixture.download.download_count

        == fixture.context.log.image_count

    )

def test_capture_indices_are_sequential() -> None:
    """
    Capture indices are sequential.
    """

    fixture = create_scan_engine()

    fixture.engine.execute()

    indices = [

        capture.capture_index

        for capture

        in fixture.capture.captures

    ]

    assert indices == list(

        range(

            1,

            fixture.capture.capture_count + 1,

        )

    )


def test_image_names_are_unique() -> None:
    """
    Every image name is unique.
    """

    fixture = create_scan_engine()

    fixture.engine.execute()

    names = []

    for capture in fixture.capture.captures:

        names.extend(

            capture.image_names

        )

    assert len(names) == len(set(names))



def test_every_capture_contains_five_images() -> None:
    """
    Every CaptureRecord contains one image from each camera.
    """

    fixture = create_scan_engine()

    fixture.engine.execute()

    for capture in fixture.capture.captures:

        assert (
            capture.camera_count
            ==
            len(fixture.context.geometry.cameras)
        )

def test_download_count() -> None:
    """
    All images are downloaded.
    """

    fixture = create_scan_engine()
    fixture.engine.execute()

    assert (

    fixture.download.download_count

    == fixture.capture.image_count

)


def test_every_capture_is_successful() -> None:
    """
    All mock captures succeed.
    """

    fixture = create_scan_engine()

    fixture.engine.execute()

    for capture in fixture.capture.captures:

        assert capture.successful

        assert capture.failed_captures == 0


def test_capture_count_matches_motion() -> None:
    """
    Every movement produces one capture.
    """

    fixture = create_scan_engine()

    fixture.engine.execute()

    assert (
        len(
            fixture.motion.visited_positions
        )
        ==
        fixture.capture.capture_count
    )

def test_download_matches_scan_log() -> None:
    """
    Download count matches the ScanLog.
    """

    fixture = create_scan_engine()

    fixture.engine.execute()

    assert (
        fixture.download.download_count
        ==
        fixture.context.log.image_count
    )

def test_capture_records_match_scan_log() -> None:
    """
    CaptureService and ScanLog contain the same CaptureRecords.
    """

    fixture = create_scan_engine()

    fixture.engine.execute()

    assert (
        tuple(
            fixture.context.log.captures
        )
        ==
        fixture.capture.captures
    )