from src.communication.scanner.scanner_response import (
    ScannerResponse,
)


def test_success_response_is_successful():

    response = ScannerResponse.success_response(
        message="PONG",
    )

    assert response.success is True


def test_success_response_contains_message():

    response = ScannerResponse.success_response(
        message="PONG",
    )

    assert response.message == "PONG"


def test_success_response_defaults_data_to_none():

    response = ScannerResponse.success_response(
        message="PONG",
    )

    assert response.data is None


def test_success_response_preserves_data():

    data = {
        "state": "Idle",
    }

    response = ScannerResponse.success_response(
        message="Scanner status.",
        data=data,
    )

    assert response.data == data


def test_error_response_is_unsuccessful():

    response = ScannerResponse.error_response(
        message="Scanner is not ready.",
    )

    assert response.success is False


def test_error_response_contains_message():

    response = ScannerResponse.error_response(
        message="Scanner is not ready.",
    )

    assert response.message == (
        "Scanner is not ready."
    )


def test_error_response_defaults_data_to_none():

    response = ScannerResponse.error_response(
        message="Scanner error.",
    )

    assert response.data is None