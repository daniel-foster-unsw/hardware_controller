"""
Scanner API command definitions.
"""

from enum import Enum


class ScannerCommand(Enum):
    """Commands exposed by the scanner API."""

    PING = "PING"

    GET_STATUS = "GET_STATUS"

    CREATE_SCAN = "CREATE_SCAN"

    START_SCAN = "START_SCAN"

    STOP_SCAN = "STOP_SCAN"