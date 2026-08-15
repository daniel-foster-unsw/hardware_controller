"""
Scanner API response model.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class ScannerResponse:
    """
    Response returned to the HMI.
    """

    version: str

    status: str

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
            status="OK",
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
            status="ERROR",
            message=message,
            data=data,
        )