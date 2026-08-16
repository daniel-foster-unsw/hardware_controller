"""
Application configuration.
"""

from src.configuration.camera_configuration import (
    CameraConfiguration,
)


class Configuration:
    """Application configuration."""

    def __init__(self):

        self.application_name = ""
        self.version = ""

        self.transport = ""

        self.motor_count = 0

        self.scanner_host = ""
        self.scanner_port = 0

        self.cameras: dict[
            int,
            CameraConfiguration,
        ] = {}

        self.log_level = ""
        self.log_file = ""