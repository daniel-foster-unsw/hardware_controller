"""
Main application class.
"""

from src.configuration.configuration_manager import ConfigurationManager
from src.logger.logger_manager import LoggerManager
from src.communication.mock_transport import MockTransport
from src.communication.transport_factory import TransportFactory
from src.motor.motor_manager import MotorManager




class Application:
    """Main application."""

    @property
    def initialised(self) -> bool:
        """Return True if the application has been initialised."""

        return self._initialised

    def __init__(self):

        self.configuration = ConfigurationManager()
        self.logger_manager = LoggerManager()

        self.logger = None

        self.transport = None

        self.motor_manager = None

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

            self.logger = self.logger_manager.logger

            #
            # Transport
            #
            self.transport = TransportFactory.create(
                self.configuration.transport
            )

            self.transport.initialise()

            #
            # Motor Manager
            #
            self.motor_manager = MotorManager(
                transport=self.transport,
                motor_count=self.configuration.motor_count,
            )

            self.motor_manager.initialise()

            self.logger.info("Application initialised.")

            self.logger.info("Application ready.")

            self._initialised = True

        except Exception:

            #
            # Clean up partially initialised resources.
            #

            self.shutdown()

            raise

    def run(self) -> None:
        """Run the application."""

        if not self._initialised:
            raise RuntimeError(
                "Application has not been initialised."
            )

        self.logger.info("Application running.")

    def shutdown(self) -> None:
        """Shutdown the application."""
        try:

            if self.motor_manager is not None:

                self.motor_manager.shutdown()
                self.motor_manager = None

            if self.transport is not None:

                self.transport.shutdown()      
                self.transport = None
        finally:
            if self.logger is not None:

                self.logger.info("Application shutdown.")

            if self.logger_manager is not None:

                self.logger_manager.shutdown()

            self._initialised = False

        
        