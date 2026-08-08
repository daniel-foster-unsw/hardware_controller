"""
Scanner API response model.
"""

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class ScannerResponse:
    """
    Response returned to the HMI.
    """

    version: str

    success: bool

    message: str

    data: dict[str, Any] | None = None

    @classmethod
    def success_response(
        cls,
        message: str,
        data: dict[str, Any] | None = None,
        version: str = "1.0",
    ) -> "ScannerResponse":
        """
        Create a successful response.
        """

        return cls(
            version=version,
            success=True,
            message=message,
            data=data,
        )

    @classmethod
    def error_response(
        cls,
        message: str,
        data: dict[str, Any] | None = None,
        version: str = "1.0",
    ) -> "ScannerResponse":
        """
        Create an error response.
        """

        return cls(
            version=version,
            success=False,
            message=message,
            data=data,
        )