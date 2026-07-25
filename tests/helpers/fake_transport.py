"""
Fake transport used by unit tests.
"""


class FakeTransport:
    """Simple packet collector."""

    def __init__(self) -> None:

        self.packets: list[bytes] = []

    def send(self, packet: bytes) -> None:

        self.packets.append(packet)

    def clear(self) -> None:

        self.packets.clear()