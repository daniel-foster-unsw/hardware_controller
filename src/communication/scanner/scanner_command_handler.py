"""
Scanner command handler.
"""

from src.communication.scanner.scanner_command import (
    ScannerCommand,
)

from src.communication.scanner.scanner_request import (
    ScannerRequest,
)

from src.communication.scanner.scanner_response import (
    ScannerResponse,
)


class ScannerCommandHandler:
    """
    Handles commands received from the scanner HMI.
    """

    def __init__(self, application) -> None:
        """
        Initialise the command handler.
        """

        self._application = application

    def handle(
        self,
        request: ScannerRequest,
    ) -> ScannerResponse:
        """
        Handle a scanner request.
        """

        if request.command == ScannerCommand.PING:

            return self._handle_ping()

        if request.command == ScannerCommand.GET_STATUS:

            return self._handle_get_status()

        if request.command == ScannerCommand.CREATE_SCAN:

            return self._handle_create_scan(
                request,
            )

        if request.command == ScannerCommand.START_SCAN:

            return self._handle_start_scan()

        if request.command == ScannerCommand.STOP_SCAN:

            return self._handle_stop_scan()

        return ScannerResponse.error_response(
            message=(
                "Unsupported scanner command: "
                f"{request.command.value}"
            ),
        )

    def _handle_ping(
        self,
    ) -> ScannerResponse:
        """
        Handle PING.
        """

        return ScannerResponse.success_response(
            message="PONG",
        )

    def _handle_get_status(
        self,
    ) -> ScannerResponse:
        """
        Return the current application status.
        """

        data = {
            "initialised": self._application.initialised,
        }

        return ScannerResponse.success_response(
            message="Scanner status.",
            data=data,
        )

    def _handle_create_scan(
        self,
        request: ScannerRequest,
    ) -> ScannerResponse:
        """
        Handle scan creation.

        Scan creation will be connected to the scan
        context/session lifecycle in the next step.
        """

        return ScannerResponse.error_response(
            message=(
                "CREATE_SCAN is not yet available."
            ),
        )

    def _handle_start_scan(
        self,
    ) -> ScannerResponse:
        """
        Handle scan start.

        Scan execution will be connected to the
        ScanEngine in the next step.
        """

        return ScannerResponse.error_response(
            message=(
                "START_SCAN is not yet available."
            ),
        )

    def _handle_stop_scan(
        self,
    ) -> ScannerResponse:
        """
        Handle scan stop.

        Stop behaviour will be connected to the
        ScanEngine in the next step.
        """

        return ScannerResponse.error_response(
            message=(
                "STOP_SCAN is not yet available."
            ),
        )