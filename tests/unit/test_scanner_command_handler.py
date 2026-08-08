from src.camera.services.mock_capture_service import (
    MockCaptureService,
)

from src.camera.services.mock_download_service import (
    MockDownloadService,
)

from src.communication.scanner.scanner_command import (
    ScannerCommand,
)

from src.communication.scanner.scanner_command_handler import (
    ScannerCommandHandler,
)

from src.communication.scanner.scanner_request import (
    ScannerRequest,
)

from src.scan.models.scan_state import (
    ScanState,
)

from src.scan.scan_manager import (
    ScanManager,
)

from tests.helpers.scan_engine_factory import (
    create_scan_engine,
)


def create_handler():

    fixture = create_scan_engine()

    manager = ScanManager()

    handler = ScannerCommandHandler(
        scan_manager=manager,
        geometry=fixture.context.geometry,
        motion_service=fixture.motion,
        capture_service=fixture.capture,
        download_service=fixture.download,
    )

    return handler, manager, fixture


def create_scan_request():

    return ScannerRequest.create(
        command=ScannerCommand.CREATE_SCAN,
        parameters={
            "scan_id": "TEST001",
            "scan_name": "Test Scan",
            "start_position_mm": 0,
            "end_position_mm": 1000,
            "capture_spacing_mm": 50,
            "motor_speed_mm_s": 100,
            "capture_delay_s": 0.5,
            "enabled_cameras": [
                1,
                2,
                3,
                4,
                5,
            ],
            "reset_before_scan": True,
            "reset_after_scan": True,
            "auto_download": True,
            "delete_remote_files": False,
        },
    )


def test_ping_returns_success():

    try:

        handler, _, _ = create_handler()

        request = ScannerRequest.create(
            command=ScannerCommand.PING,
        )

        response = handler.handle(
            request,
        )

        assert response.success is True

        assert response.message == "PONG"

    except Exception as exception:

        assert False, (
            f"Unexpected exception: {exception}"
        )


def test_get_status_reports_no_scan():

    try:

        handler, _, _ = create_handler()

        request = ScannerRequest.create(
            command=ScannerCommand.GET_STATUS,
        )

        response = handler.handle(
            request,
        )

        assert response.success is True

        assert response.message == (
            "Scanner status."
        )

        assert response.data["scan_created"] is False

        assert response.data["active"] is False

        assert response.data["state"] == (
            ScanState.IDLE.value
        )

        assert response.data["error"] is None

    except Exception as exception:

        assert False, (
            f"Unexpected exception: {exception}"
        )


def test_create_scan_creates_scan():

    try:

        handler, manager, _ = create_handler()

        request = create_scan_request()

        response = handler.handle(
            request,
        )

        assert response.success is True

        assert response.message == (
            "Scan created."
        )

        assert manager.scan_created is True

        assert manager.active is False

        assert response.data["scan_id"] == (
            "TEST001"
        )

        assert response.data["scan_name"] == (
            "Test Scan"
        )

    except Exception as exception:

        assert False, (
            f"Unexpected exception: {exception}"
        )


def test_create_scan_updates_status():

    try:

        handler, _, _ = create_handler()

        create_response = handler.handle(
            create_scan_request(),
        )

        assert create_response.success is True

        status_request = ScannerRequest.create(
            command=ScannerCommand.GET_STATUS,
        )

        status_response = handler.handle(
            status_request,
        )

        assert status_response.success is True

        assert status_response.data[
            "scan_created"
        ] is True

        assert status_response.data[
            "active"
        ] is False

        assert status_response.data[
            "state"
        ] == ScanState.CREATE_SCAN.value

    except Exception as exception:

        assert False, (
            f"Unexpected exception: {exception}"
        )


def test_start_scan_starts_scan():

    try:

        handler, manager, fixture = (
            create_handler()
        )

        create_response = handler.handle(
            create_scan_request(),
        )

        assert create_response.success is True

        start_request = ScannerRequest.create(
            command=ScannerCommand.START_SCAN,
        )

        response = handler.handle(
            start_request,
        )

        assert response.success is True

        assert response.message == (
            "Scan started."
        )

        manager.wait_for_completion()

        assert manager.active is False

        assert manager.state == (
            ScanState.COMPLETE
        )

        assert fixture.motion.homed is True

    except Exception as exception:

        assert False, (
            f"Unexpected exception: {exception}"
        )


def test_start_scan_without_scan_returns_error():

    try:

        handler, _, _ = create_handler()

        request = ScannerRequest.create(
            command=ScannerCommand.START_SCAN,
        )

        response = handler.handle(
            request,
        )

        assert response.success is False

        assert response.message == (
            "No scan has been created."
        )

    except Exception as exception:

        assert False, (
            f"Unexpected exception: {exception}"
        )


def test_stop_scan_without_running_scan_returns_error():

    try:

        handler, _, _ = create_handler()

        request = ScannerRequest.create(
            command=ScannerCommand.STOP_SCAN,
        )

        response = handler.handle(
            request,
        )

        assert response.success is False

        assert response.message == (
            "No scan is currently running."
        )

    except Exception as exception:

        assert False, (
            f"Unexpected exception: {exception}"
        )


def test_get_status_after_scan_complete():

    try:

        handler, manager, _ = (
            create_handler()
        )

        create_response = handler.handle(
            create_scan_request(),
        )

        assert create_response.success is True

        start_response = handler.handle(
            ScannerRequest.create(
                command=ScannerCommand.START_SCAN,
            ),
        )

        assert start_response.success is True

        manager.wait_for_completion()

        status_response = handler.handle(
            ScannerRequest.create(
                command=ScannerCommand.GET_STATUS,
            ),
        )

        assert status_response.success is True

        assert status_response.data[
            "scan_created"
        ] is True

        assert status_response.data[
            "active"
        ] is False

        assert status_response.data[
            "state"
        ] == ScanState.COMPLETE.value

        assert status_response.data[
            "error"
        ] is None

    except Exception as exception:

        assert False, (
            f"Unexpected exception: {exception}"
        )