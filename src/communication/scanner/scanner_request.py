"""
Scanner API request model.
"""

from dataclasses import dataclass
from typing import Any

from src.communication.scanner.scanner_command import (
    ScannerCommand,
)


@dataclass(frozen=True)
class ScannerRequest:
    """
    Request received from the HMI.
    """

    version: str

    command: ScannerCommand

    parameters: dict[str, Any]

    @classmethod
    def create(
        cls,
        command: ScannerCommand,
        parameters: dict[str, Any] | None = None,
        version: str = "1.0",
    ) -> "ScannerRequest":
        """
        Create a scanner request.
        """

        return cls(
            version=version,
            command=command,
            parameters=(
                parameters
                if parameters is not None
                else {}
            ),
        )