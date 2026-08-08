from src.camera.services.mock_capture_service import (
    MockCaptureService,
)

from src.camera.services.mock_download_service import (
    MockDownloadService,
)

from src.scan.scan_manager import (
    ScanManager,
)

from src.scanner.services.mock_motion_service import (
    MockMotionService,
)

from tests.helpers.scan_context_factory import (
    create_scan_context,
)

from tests.helpers.configuration_factory import (
    create_scan_configuration,
)

from tests.helpers.scan_engine_factory import (
    create_scan_engine,
)


def test_scan_manager_starts_without_scan():

    manager = ScanManager()

    assert manager.context is None

    assert manager.engine is None

    assert manager.active is False


def test_create_scan_creates_context():

    manager = ScanManager()

    configuration = (
        create_scan_configuration()
    )

    geometry = (
        create_scan_engine()
        .context
        .geometry
    )

    motion = MockMotionService()

    capture = MockCaptureService()

    download = MockDownloadService()

    context = manager.create_scan(
        configuration=configuration,
        geometry=geometry,
        motion_service=motion,
        capture_service=capture,
        download_service=download,
    )

    assert manager.active is True

    assert manager.context is context

    assert manager.engine is not None

    assert context.configuration is configuration


def test_create_scan_creates_scan_engine():

    manager = ScanManager()

    fixture = create_scan_engine()

    context = manager.create_scan(
        configuration=fixture.context.configuration,
        geometry=fixture.context.geometry,
        motion_service=fixture.motion,
        capture_service=fixture.capture,
        download_service=fixture.download,
    )

    assert manager.engine is not None

    assert manager.engine.context is context


def test_create_scan_cannot_replace_active_scan():

    manager = ScanManager()

    fixture = create_scan_engine()

    manager.create_scan(
        configuration=fixture.context.configuration,
        geometry=fixture.context.geometry,
        motion_service=fixture.motion,
        capture_service=fixture.capture,
        download_service=fixture.download,
    )

    second_fixture = create_scan_engine()

    try:

        manager.create_scan(
            configuration=(
                second_fixture.context.configuration
            ),
            geometry=(
                second_fixture.context.geometry
            ),
            motion_service=second_fixture.motion,
            capture_service=second_fixture.capture,
            download_service=second_fixture.download,
        )

        assert False, (
            "Expected RuntimeError."
        )

    except RuntimeError as exception:

        assert str(exception) == (
            "A scan is already active."
        )


def test_start_scan_executes_scan():

    manager = ScanManager()

    fixture = create_scan_engine()

    manager.create_scan(
        configuration=fixture.context.configuration,
        geometry=fixture.context.geometry,
        motion_service=fixture.motion,
        capture_service=fixture.capture,
        download_service=fixture.download,
    )

    manager.start_scan()

    assert fixture.motion.homed is True

    assert (
        len(fixture.motion.visited_positions)
        == fixture.context.session.total_positions
    )


def test_start_scan_without_scan_raises():

    manager = ScanManager()

    try:

        manager.start_scan()

        assert False, (
            "Expected RuntimeError."
        )

    except RuntimeError as exception:

        assert str(exception) == (
            "No scan has been created."
        )


def test_stop_scan_calls_motion_stop():

    manager = ScanManager()

    fixture = create_scan_engine()

    manager.create_scan(
        configuration=fixture.context.configuration,
        geometry=fixture.context.geometry,
        motion_service=fixture.motion,
        capture_service=fixture.capture,
        download_service=fixture.download,
    )

    manager.stop_scan()

    assert fixture.motion.initialised is False


def test_clear_scan_removes_current_scan():

    manager = ScanManager()

    fixture = create_scan_engine()

    manager.create_scan(
        configuration=fixture.context.configuration,
        geometry=fixture.context.geometry,
        motion_service=fixture.motion,
        capture_service=fixture.capture,
        download_service=fixture.download,
    )

    assert manager.active is True

    manager.clear_scan()

    assert manager.active is False

    assert manager.context is None

    assert manager.engine is None