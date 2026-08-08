from src.communication.scanner.scanner_command import (
    ScannerCommand,
)

from src.communication.scanner.scanner_request import (
    ScannerRequest,
)


def test_create_request_uses_default_version():

    request = ScannerRequest.create(
        command=ScannerCommand.PING,
    )

    assert request.version == "1.0"


def test_create_request_uses_command():

    request = ScannerRequest.create(
        command=ScannerCommand.START_SCAN,
    )

    assert request.command == ScannerCommand.START_SCAN


def test_create_request_defaults_to_empty_parameters():

    request = ScannerRequest.create(
        command=ScannerCommand.PING,
    )

    assert request.parameters == {}


def test_create_request_preserves_parameters():

    parameters = {
        "scan_id": "TEST001",
        "scan_name": "Test Scan",
    }

    request = ScannerRequest.create(
        command=ScannerCommand.CREATE_SCAN,
        parameters=parameters,
    )

    assert request.parameters == parameters


def test_create_request_accepts_custom_version():

    request = ScannerRequest.create(
        command=ScannerCommand.PING,
        version="1.1",
    )

    assert request.version == "1.1"