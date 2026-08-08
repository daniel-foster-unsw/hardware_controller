from src.application import Application

from src.communication.scanner.scanner_command import (
    ScannerCommand,
)

from src.communication.scanner.scanner_command_handler import (
    ScannerCommandHandler,
)

from src.communication.scanner.scanner_request import (
    ScannerRequest,
)


def test_ping_returns_success():

    application = Application()

    handler = ScannerCommandHandler(
        application,
    )

    request = ScannerRequest.create(
        command=ScannerCommand.PING,
    )

    response = handler.handle(
        request,
    )

    assert response.success is True

    assert response.message == "PONG"


def test_get_status_reports_uninitialised_application():

    application = Application()

    handler = ScannerCommandHandler(
        application,
    )

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

    assert response.data == {
        "initialised": False,
    }


def test_get_status_reports_initialised_application():

    application = Application()

    application.initialise()

    try:

        handler = ScannerCommandHandler(
            application,
        )

        request = ScannerRequest.create(
            command=ScannerCommand.GET_STATUS,
        )

        response = handler.handle(
            request,
        )

        assert response.success is True

        assert response.data == {
            "initialised": True,
        }

    finally:

        application.shutdown()


def test_create_scan_returns_not_available():

    application = Application()

    handler = ScannerCommandHandler(
        application,
    )

    request = ScannerRequest.create(
        command=ScannerCommand.CREATE_SCAN,
    )

    response = handler.handle(
        request,
    )

    assert response.success is False

    assert response.message == (
        "CREATE_SCAN is not yet available."
    )


def test_start_scan_returns_not_available():

    application = Application()

    handler = ScannerCommandHandler(
        application,
    )

    request = ScannerRequest.create(
        command=ScannerCommand.START_SCAN,
    )

    response = handler.handle(
        request,
    )

    assert response.success is False

    assert response.message == (
        "START_SCAN is not yet available."
    )


def test_stop_scan_returns_not_available():

    application = Application()

    handler = ScannerCommandHandler(
        application,
    )

    request = ScannerRequest.create(
        command=ScannerCommand.STOP_SCAN,
    )

    response = handler.handle(
        request,
    )

    assert response.success is False

    assert response.message == (
        "STOP_SCAN is not yet available."
    )