"""
Main application class.
"""

import time

from src.camera.services.mock_capture_service import (
    MockCaptureService,
)

from src.camera.services.mock_download_service import (
    MockDownloadService,
)

from src.communication.mock_transport import (
    MockTransport,
)

from src.communication.scanner.scanner_command_handler import (
    ScannerCommandHandler,
)

from src.communication.scanner.scanner_server import (
    ScannerServer,
)

from src.communication.transport_factory import (
    TransportFactory,
)

from src.configuration.configuration_manager import (
    ConfigurationManager,
)

from src.logger.logger_manager import (
    LoggerManager,
)

from src.motor.motor_manager import (
    MotorManager,
)

from src.scan.scan_manager import (
    ScanManager,
)

from src.scanner.factories.scanner_geometry_factory import (
    create_scanner_geometry,
)

from src.scanner.services.mock_motion_service import (
    MockMotionService,
)


class Application:
    """Main application."""

    @property
    def initialised(self) -> bool:
        """Return True if the application has been initialised."""

        return self._initialised

    def __init__(self):

        self.configuration = (
            ConfigurationManager()
        )

        self.logger_manager = (
            LoggerManager()
        )

        self.logger = None

        self.transport = None

        self.motor_manager = None

        #
        # Scanner components.
        #

        self.scan_manager = None

        self.scanner_geometry = None

        self.motion_service = None

        self.capture_service = None

        self.download_service = None

        self.scanner_command_handler = None

        self.scanner_server = None

        self._initialised = False

    def initialise(self) -> None:
        """Initialise the application."""

        try:

            #
            # Configuration
            #

            self.configuration.initialise()

            #
            # Logger
            #

            self.logger_manager.initialise(
                self.configuration.log_level,
                self.configuration.log_file,
            )

            self.logger = (
                self.logger_manager.logger
            )

            #
            # Transport
            #

            self.transport = (
                TransportFactory.create(
                    self.configuration.transport,
                )
            )

            self.transport.initialise()

            #
            # Motor Manager
            #

            self.motor_manager = MotorManager(
                transport=self.transport,
                motor_count=(
                    self.configuration.motor_count
                ),
            )

            self.motor_manager.initialise()

            #
            # Scanner geometry
            #
            # The geometry factory currently provides
            # the project's default five-camera geometry.
            #

            self.scanner_geometry = (
                create_scanner_geometry()
            )

            #
            # Scanner services
            #
            # These are mock implementations until
            # Camera Integration and Motion Integration.
            #

            self.motion_service = (
                MockMotionService()
            )

            self.capture_service = (
                MockCaptureService()
            )

            self.download_service = (
                MockDownloadService()
            )

            #
            # Scan manager
            #

            self.scan_manager = (
                ScanManager()
            )

            #
            # Scanner command handler
            #

            self.scanner_command_handler = (
                ScannerCommandHandler(
                    scan_manager=(
                        self.scan_manager
                    ),
                    geometry=(
                        self.scanner_geometry
                    ),
                    motion_service=(
                        self.motion_service
                    ),
                    capture_service=(
                        self.capture_service
                    ),
                    download_service=(
                        self.download_service
                    ),
                )
            )

            #
            # Scanner server
            #

            self.scanner_server = (
                ScannerServer(
                    host=(
                        self.configuration.scanner_host
                    ),
                    port=(
                        self.configuration.scanner_port
                    ),
                    command_handler=(
                        self.scanner_command_handler
                    ),
                )
            )

            self.logger.info(
                "Application initialised."
            )

            self.logger.info(
                "Application ready."
            )

            self._initialised = True

        except Exception:

            #
            # Clean up partially initialised
            # resources.
            #

            self.shutdown()

            raise

    def run(self) -> None:
        """Run the application."""

        if not self._initialised:

            raise RuntimeError(
                "Application has not been initialised."
            )

        if self.scanner_server is None:

            raise RuntimeError(
                "Scanner server has not been initialised."
            )

        #
        # Start the scanner API.
        #

        self.scanner_server.start()

        self.logger.info(
            "Scanner server listening on "
            f"{self.scanner_server.host}:"
            f"{self.scanner_server.port}"
        )

        self.logger.info(
            "Application running."
        )

        try:

            while self.scanner_server.running:

                time.sleep(0.5)

        except KeyboardInterrupt:

            self.logger.info(
                "Shutdown requested."
            )





    def shutdown(self) -> None:
        """Shutdown the application."""

        try:

            #
            # Scanner server
            #

            if self.scanner_server is not None:

                self.scanner_server.stop()

                self.scanner_server = None

            #
            # Scan manager
            #

            if self.scan_manager is not None:

                if self.scan_manager.active:

                    self.scan_manager.stop_scan()

                    self.scan_manager.wait_for_completion()

                self.scan_manager.clear_scan()

                self.scan_manager = None

            #
            # Scanner services
            #

            self.motion_service = None

            self.capture_service = None

            self.download_service = None

            self.scanner_command_handler = None

            self.scanner_geometry = None

            #
            # Motor manager
            #

            if self.motor_manager is not None:

                self.motor_manager.shutdown()

                self.motor_manager = None

            #
            # Transport
            #

            if self.transport is not None:

                self.transport.shutdown()

                self.transport = None

        finally:

            if self.logger is not None:

                self.logger.info(
                    "Application shutdown."
                )

            if self.logger_manager is not None:

                self.logger_manager.shutdown()

            self.logger = None

            self._initialised = False