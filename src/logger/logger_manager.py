"""
Application logger manager.
"""

import logging
from pathlib import Path
from typing import Optional


class LoggerManager:
    """Initialises and manages the application logger."""

    def __init__(self) -> None:

        self._logger: Optional[logging.Logger] = logging.getLogger("ScannerController")

    @property
    def logger(self) -> Optional[logging.Logger]:
        return self._logger


    def initialise(self, level: str, filename: str):

        log_path = Path(filename)

        log_path.parent.mkdir(parents=True, exist_ok=True)

        self._logger.setLevel(getattr(logging, level.upper()))

        self._logger.handlers.clear()

        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
            "%Y-%m-%d %H:%M:%S"
        )

        console = logging.StreamHandler()
        console.setFormatter(formatter)

        file = logging.FileHandler(log_path)
        file.setFormatter(formatter)

        self._logger.addHandler(console)
        self._logger.addHandler(file)

        self._logger.info("Logger initialised.")

    def shutdown(self) -> None:
        """Shutdown the logging system."""

        if self._logger is not None:
            self._logger.info("Logger shutdown.")

        logging.shutdown()

        #self._logger = None