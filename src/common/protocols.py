"""
Shared application protocols.
"""

from typing import Protocol


class PacketSender(Protocol):
    """Protocol for objects capable of sending packets."""

    def send(self, packet: bytes) -> None:
        """Send a packet."""
        ...