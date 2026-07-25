"""
Configuration manager.
"""

import json
from pathlib import Path

from src.configuration.configuration import Configuration
from src.common.exceptions import ConfigurationError

class ConfigurationManager:

    def __init__(self):

        self.configuration = Configuration()

    def initialise(self):

        config_path = Path("config/config.json")

        if not config_path.exists():
            raise ConfigurationError(
                f"Configuration file not found: {config_path}"
            )

        self.load(config_path)


    def load(self, filename: Path):

        with open(filename, "r", encoding="utf-8") as file:
            data = json.load(file)

        self.configuration.application_name = \
            data["application"]["name"]

        self.configuration.version = \
            data["application"]["version"]

        self.configuration.transport = \
            data["communication"]["transport"]

        self.configuration.motor_count = \
            data["motors"]["count"]

        self.configuration.log_level = \
            data["logging"]["level"]

        self.configuration.log_file = \
            data["logging"]["file"]


    #properties
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
    def log_level(self):
        return self.configuration.log_level


    @property
    def log_file(self):
        return self.configuration.log_file