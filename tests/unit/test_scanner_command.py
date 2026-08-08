from src.communication.scanner.scanner_command import (
    ScannerCommand,
)


def test_ping_command():

    assert ScannerCommand.PING.value == "PING"


def test_get_status_command():

    assert ScannerCommand.GET_STATUS.value == "GET_STATUS"


def test_create_scan_command():

    assert ScannerCommand.CREATE_SCAN.value == "CREATE_SCAN"


def test_start_scan_command():

    assert ScannerCommand.START_SCAN.value == "START_SCAN"


def test_stop_scan_command():

    assert ScannerCommand.STOP_SCAN.value == "STOP_SCAN"