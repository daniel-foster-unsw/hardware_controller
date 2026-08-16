"""
Configuration manager.
"""

import json
from pathlib import Path

from src.configuration.configuration import (
    Configuration,
)

from src.configuration.camera_configuration import (
    CameraConfiguration,
)

from src.common.exceptions import (
    ConfigurationError,
)


class ConfigurationManager:

    def __init__(self):

        self.configuration = Configuration()

    def initialise(self):

        config_path = Path(
            "config/config.json"
        )

        if not config_path.exists():

            raise ConfigurationError(
                f"Configuration file not found: "
                f"{config_path}"
            )

        self.load(config_path)

    def load(
        self,
        filename: Path,
    ):

        with open(
            filename,
            "r",
            encoding="utf-8",
        ) as file:

            data = json.load(file)

        self.configuration.application_name = \
            data["application"]["name"]

        self.configuration.version = \
            data["application"]["version"]

        self.configuration.transport = \
            data["communication"]["transport"]

        self.configuration.motor_count = \
            data["motors"]["count"]

        self.configuration.scanner_host = \
            data["scanner"]["host"]

        self.configuration.scanner_port = \
            data["scanner"]["port"]

        #
        # Cameras
        #

        camera_data = data["cameras"]

        self.configuration.cameras = {}

        for camera_name, camera in camera_data.items():

            camera_number = int(
                camera_name.replace(
                    "CAM",
                    "",
                )
            )

            self.configuration.cameras[
                camera_number
            ] = CameraConfiguration(
                camera_id=camera_number,
                enabled=camera["enabled"],
                host=camera["host"],
                port=camera["port"],
            )

        #
        # Logging
        #

        self.configuration.log_level = \
            data["logging"]["level"]

        self.configuration.log_file = \
            data["logging"]["file"]

    @property
    def application_name(self):
        return self.configuration.application_name

    @property
    def version(self):
        return self.configuration.version

    @property
    def transport(self):
        return self.configuration.transport

    @property
    def motor_count(self):
        return self.configuration.motor_count

    @property
    def scanner_host(self):
        return self.configuration.scanner_host

    @property
    def scanner_port(self):
        return self.configuration.scanner_port

    @property
    def cameras(self):
        return dict(
            self.configuration.cameras
        )

    @property
    def log_level(self):
        return self.configuration.log_level

    @property
    def log_file(self):
        return self.configuration.log_file