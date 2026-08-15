"""
Scanner command handler.
"""

from typing import Any

from src.camera.services.capture_service import (
    CaptureService,
)

from src.camera.services.download_service import (
    DownloadService,
)

from src.communication.scanner.scanner_command import (
    ScannerCommand,
)

from src.communication.scanner.scanner_request import (
    ScannerRequest,
)

from src.communication.scanner.scanner_response import (
    ScannerResponse,
)

from src.scan.models.scan_configuration import (
    ScanConfiguration,
)

from src.scan.scan_manager import (
    ScanManager,
)

from src.scanner.models.scanner_geometry import (
    ScannerGeometry,
)

from src.scanner.services.motion_service import (
    MotionService,
)


class ScannerCommandHandler:
    """
    Handles commands received from the scanner HMI.
    """

    def __init__(
        self,
        scan_manager: ScanManager,
        geometry: ScannerGeometry,
        motion_service: MotionService,
        capture_service: CaptureService,
        download_service: DownloadService,
    ) -> None:
        """
        Initialise the command handler.
        """

        self._scan_manager = scan_manager

        self._geometry = geometry

        self._motion_service = motion_service

        self._capture_service = capture_service

        self._download_service = download_service

    def handle(
        self,
        request: ScannerRequest,
    ) -> ScannerResponse:
        """
        Handle a scanner request.
        """

        try:

            if request.command == ScannerCommand.PING:

                return self._handle_ping()

            if request.command == ScannerCommand.GET_STATUS:

                return self._handle_get_status()

            if request.command == ScannerCommand.CREATE_SCAN:

                return self._handle_create_scan(request)

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

        except Exception as exception:

            return ScannerResponse.error_response(
                message=str(exception),
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
        Return the current scanner status.
        """

        data = {
            "scan_created":
                self._scan_manager.scan_created,

            "active":
                self._scan_manager.active,

            "state":
                self._scan_manager.state.value,

            "error":
                (
                    str(self._scan_manager.error)
                    if self._scan_manager.error is not None
                    else None
                ),
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
        Create a scan from the supplied parameters.
        """

        configuration = (
            self._create_configuration(
                request.parameters,
            )
        )

        context = (
            self._scan_manager.create_scan(
                configuration=configuration,
                geometry=self._geometry,
                motion_service=self._motion_service,
                capture_service=self._capture_service,
                download_service=self._download_service,
            )
        )

        return ScannerResponse.success_response(
            message="Scan created.",
            data={
                "scan_id":
                    context.configuration.scan_id,

                "scan_name":
                    context.configuration.scan_name,
            },
        )

    def _handle_start_scan(
        self,
    ) -> ScannerResponse:
        """
        Start the current scan.
        """

        self._scan_manager.start_scan()

        return ScannerResponse.success_response(
            message="Scan started.",
            data={
                "state":
                    self._scan_manager.state.value,
            },
        )

    def _handle_stop_scan(
        self,
    ) -> ScannerResponse:
        """
        Stop the current scan.
        """

        self._scan_manager.stop_scan()

        return ScannerResponse.success_response(
            message="Scan stop requested.",
            data={
                "state":
                    self._scan_manager.state.value,
            },
        )

    @staticmethod
    def _create_configuration(
        parameters: dict[str, Any],
    ) -> ScanConfiguration:
        """
        Create a ScanConfiguration from request parameters.
        """

        return ScanConfiguration(
            scan_id=parameters["scan_id"],
            scan_name=parameters["scan_name"],
            start_position_mm=(
                parameters["start_position_mm"]
            ),
            end_position_mm=(
                parameters["end_position_mm"]
            ),
            capture_spacing_mm=(
                parameters["capture_spacing_mm"]
            ),
            motor_speed_mm_s=(
                parameters["motor_speed_mm_s"]
            ),
            capture_delay_s=(
                parameters["capture_delay_s"]
            ),
            enabled_cameras=tuple(
                parameters["enabled_cameras"]
            ),
            reset_before_scan=(
                parameters["reset_before_scan"]
            ),
            reset_after_scan=(
                parameters["reset_after_scan"]
            ),
            auto_download=(
                parameters["auto_download"]
            ),
            delete_remote_files=(
                parameters["delete_remote_files"]
            ),
        )