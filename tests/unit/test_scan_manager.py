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

from tests.helpers.configuration_factory import (
    create_scan_configuration,
)

from tests.helpers.scan_engine_factory import (
    create_scan_engine,
)

from src.scan.models.scan_state import (
    ScanState,
)


def test_scan_manager_starts_without_scan():

    try:

        manager = ScanManager()

        assert manager.context is None

        assert manager.engine is None

        assert manager.active is False

    except Exception as exception:

        assert False, (
            f"Unexpected exception: {exception}"
        )


def test_create_scan_creates_context():

    try:

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

        #assert manager.active is True
        assert manager.scan_created is True

        assert manager.context is context

        assert manager.engine is not None

        assert context.configuration is configuration

    except Exception as exception:

        assert False, (
            f"Unexpected exception: {exception}"
        )


def test_create_scan_creates_scan_engine():

    try:

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

    except Exception as exception:

        assert False, (
            f"Unexpected exception: {exception}"
        )


def test_create_scan_cannot_replace_active_scan():

    try:

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
                "A scan is already created."
            )

    except Exception as exception:

        assert False, (
            f"Unexpected exception: {exception}"
        )


def test_start_scan_executes_scan():

    try:

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

        manager.wait_for_completion()

        assert fixture.motion.homed is True

        assert (
            len(fixture.motion.visited_positions)
            == fixture.context.session.total_positions
        )

    except Exception as exception:

        assert False, (
            f"Unexpected exception: {exception}"
        )


def test_start_scan_without_scan_raises():

    try:

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

    except Exception as exception:

        assert False, (
            f"Unexpected exception: {exception}"
        )


def test_stop_scan_calls_motion_stop():

    try:

        manager = ScanManager()

        fixture = create_scan_engine(
            block_motion=True,
        )

        manager.create_scan(
            configuration=fixture.context.configuration,
            geometry=fixture.context.geometry,
            motion_service=fixture.motion,
            capture_service=fixture.capture,
            download_service=fixture.download,
        )


        manager.start_scan()

        assert fixture.motion.started_event.wait(
            timeout=1.0,
        )

        manager.stop_scan()

        manager.wait_for_completion()

        assert fixture.motion.stopped is True

    except Exception as exception:

        assert False, (
            f"Unexpected exception: {exception}"
        )


def test_clear_scan_removes_current_scan():

    try:

        manager = ScanManager()

        fixture = create_scan_engine()

        manager.create_scan(
            configuration=fixture.context.configuration,
            geometry=fixture.context.geometry,
            motion_service=fixture.motion,
            capture_service=fixture.capture,
            download_service=fixture.download,
        )

        #assert manager.active is True
        assert manager.scan_created is True

        manager.clear_scan()

        assert manager.active is False

        assert manager.context is None

        assert manager.engine is None

    except Exception as exception:

        assert False, (
            f"Unexpected exception: {exception}"
        )


def test_start_scan_returns_immediately():
    """
    Starting a scan does not block the caller.
    """

    try:

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

        #assert manager.active is True
        assert manager.scan_created is True

        manager.wait_for_completion()

    except Exception as exception:

        assert False, (
            f"Unexpected exception: {exception}"
        )


def test_scan_eventually_completes():
    """
    Background scan eventually reaches COMPLETE.
    """

    try:

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

        manager.wait_for_completion()

        assert manager.active is False

        assert manager.state == ScanState.COMPLETE

    except Exception as exception:

        assert False, (
            f"Unexpected exception: {exception}"
        )


def test_scan_cannot_be_started_twice():
    """
    A running scan cannot be started again.
    """

    try:

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

        try:

            manager.start_scan()

            assert False, (
                "Expected RuntimeError."
            )

        except RuntimeError as exception:

            assert str(exception) == (
                "A scan is already running."
            )

        finally:

            manager.wait_for_completion()

    except Exception as exception:

        assert False, (
            f"Unexpected exception: {exception}"
        )


def test_stop_scan_sets_aborted_state():
    """
    Stop requests scanner termination.
    """

    try:

        manager = ScanManager()

        fixture = create_scan_engine(
            block_motion=True,
        )

        manager.create_scan(
            configuration=fixture.context.configuration,
            geometry=fixture.context.geometry,
            motion_service=fixture.motion,
            capture_service=fixture.capture,
            download_service=fixture.download,
        )

        manager.start_scan()

        assert fixture.motion.started_event.wait(
            timeout=1.0,
        )

        manager.stop_scan()

        manager.wait_for_completion()

        assert manager.active is False

        assert manager.state == ScanState.ABORTED

    except Exception as exception:

        assert False, (
            f"Unexpected exception: {exception}"
        )


def test_stop_scan_without_running_scan_raises():
    """
    Stopping an idle manager raises an error.
    """

    try:

        manager = ScanManager()

        try:

            manager.stop_scan()

            assert False, (
                "Expected RuntimeError."
            )

        except RuntimeError as exception:

            assert str(exception) == (
                "No scan is currently running."
            )

    except Exception as exception:

        assert False, (
            f"Unexpected exception: {exception}"
        )


def test_clear_running_scan_raises():
    """
    A running scan cannot be cleared.
    """

    try:

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

        try:

            manager.clear_scan()

            assert False, (
                "Expected RuntimeError."
            )

        except RuntimeError as exception:

            assert str(exception) == (
                "Cannot clear a running scan."
            )

        finally:

            manager.wait_for_completion()

    except Exception as exception:

        assert False, (
            f"Unexpected exception: {exception}"
        )

