"""
Custom exceptions.
"""


class ScannerControllerError(Exception):
    """Base application exception."""


class PacketError(ScannerControllerError):
    """Packet encoding/decoding error."""


class ConfigurationError(ScannerControllerError):
    """Configuration loading error."""


class TransportError(ScannerControllerError):
    """Communication transport error."""