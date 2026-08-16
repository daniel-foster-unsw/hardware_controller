import json
import socket

from unittest.mock import MagicMock

from src.camera.services.mock_capture_service import (
    MockCaptureService,
)

from src.camera.services.mock_download_service import (
    MockDownloadService,
)

from src.communication.scanner.scanner_command_handler import (
    ScannerCommandHandler,
)

from src.communication.scanner.scanner_server import (
    ScannerServer,
)

from src.scan.scan_manager import (
    ScanManager,
)

from tests.helpers.scan_engine_factory import (
    create_scan_engine,
)


def create_server():
    """Create a scanner server for testing."""

    fixture = create_scan_engine()

    manager = ScanManager()

    handler = ScannerCommandHandler(
        scan_manager=manager,
        geometry=fixture.context.geometry,
        motion_service=fixture.motion,
        capture_service=fixture.capture,
        download_service=fixture.download,
    )

    logger = MagicMock()

    server = ScannerServer(
        host="127.0.0.1",
        port=0,
        command_handler=handler,
        logger=logger,
    )

    return server, manager, fixture


def send_request(
    server,
    request,
):
    """
    Send one request and return the response.
    """

    client = socket.create_connection(
        (
            server.host,
            server.port,
        ),
        timeout=2.0,
    )

    try:

        message = json.dumps(
            request,
            separators=(
                ",",
                ":",
            ),
        )

        client.sendall(
            (
                message
                + "\n"
            ).encode(
                "utf-8",
            )
        )

        file = client.makefile(
            "r",
            encoding="utf-8",
        )

        try:

            response_line = (
                file.readline()
            )

        finally:

            file.close()

        return json.loads(
            response_line,
        )

    finally:

        client.close()


def test_server_starts():

    try:

        server, _, _ = create_server()

        assert server.running is False

        server.start()

        assert server.running is True

    except Exception as exception:

        assert False, (
            f"Unexpected exception: {exception}"
        )

    finally:

        server.stop()


def test_server_stops():

    try:

        server, _, _ = create_server()

        server.start()

        assert server.running is True

        server.stop()

        assert server.running is False

    except Exception as exception:

        assert False, (
            f"Unexpected exception: {exception}"
        )

    finally:

        server.stop()


def test_server_ping():

    try:

        server, _, _ = create_server()

        server.start()

        response = send_request(
            server,
            {
                "version": "1.0",
                "command": "PING",
                "parameters": {},
            },
        )

        assert response["version"] == "1.0"

        assert response["success"] is True

        assert response["message"] == "PONG"

        assert response["data"] is None

    except Exception as exception:

        assert False, (
            f"Unexpected exception: {exception}"
        )

    finally:

        server.stop()


def test_server_get_status():

    try:

        server, _, _ = create_server()

        server.start()

        response = send_request(
            server,
            {
                "version": "1.0",
                "command": "GET_STATUS",
                "parameters": {},
            },
        )

        assert response["success"] is True

        assert response["data"][
            "scan_created"
        ] is False

        assert response["data"][
            "active"
        ] is False

    except Exception as exception:

        assert False, (
            f"Unexpected exception: {exception}"
        )

    finally:

        server.stop()


def test_server_invalid_command():

    try:

        server, _, _ = create_server()

        server.start()

        response = send_request(
            server,
            {
                "version": "1.0",
                "command": "INVALID_COMMAND",
                "parameters": {},
            },
        )

        assert response["success"] is False

        assert (
            "Unsupported command"
            in response["message"]
        )

    except Exception as exception:

        assert False, (
            f"Unexpected exception: {exception}"
        )

    finally:

        server.stop()


def test_server_invalid_json():

    try:

        server, _, _ = create_server()

        server.start()

        client = socket.create_connection(
            (
                server.host,
                server.port,
            ),
            timeout=2.0,
        )

        try:

            client.sendall(
                b"not valid json\n"
            )

            file = client.makefile(
                "r",
                encoding="utf-8",
            )

            try:

                response = json.loads(
                    file.readline(),
                )

            finally:

                file.close()

        finally:

            client.close()

        assert response["success"] is False

        assert response["data"] is None

    except Exception as exception:

        assert False, (
            f"Unexpected exception: {exception}"
        )

    finally:

        server.stop()

def test_server_create_scan():

    try:

        server, manager, _ = create_server()

        server.start()

        response = send_request(
            server,
            {
                "version": "1.0",
                "command": "CREATE_SCAN",
                "parameters": {
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
            },
        )

        assert response["success"] is True

        assert response["message"] == (
            "Scan created."
        )

        assert response["data"]["scan_id"] == (
            "TEST001"
        )

        assert manager.scan_created is True

    except Exception as exception:

        assert False, (
            f"Unexpected exception: {exception}"
        )

    finally:

        server.stop()