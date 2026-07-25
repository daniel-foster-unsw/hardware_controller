"""
Abstract transport interface.
"""

from abc import ABC, abstractmethod


class Transport(ABC):
    """Base class for all communication transports."""

    @abstractmethod
    def initialise(self) -> None:
        """Initialise the transport."""

    @abstractmethod
    def shutdown(self) -> None:
        """Shutdown the transport."""

    @abstractmethod
    def send(self, packet: bytes) -> None:
        """Send a packet."""

    @abstractmethod
    def receive(self) -> bytes | None:
        """Receive a packet."""

    @abstractmethod
    def connected(self) -> bool:
        """Return transport status."""