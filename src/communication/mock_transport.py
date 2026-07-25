from collections import deque

from src.communication.transport import Transport
from src.common.exceptions import TransportError


class MockTransport(Transport):
    """Mock transport implementation used for unit and integration testing."""

    def __init__(self):

        self._connected = False

        self._tx_queue = deque()

        self._rx_queue = deque()

    def initialise(self):

        self._connected = True

        self._tx_queue.clear()

        self._rx_queue.clear()

    def shutdown(self):

        self._connected = False

        self._tx_queue.clear()
        self._rx_queue.clear()

    def connected(self):

        return self._connected

    def send(self, packet: bytes):

        if not self._connected:
            raise RuntimeError("Transport not initialised.")

        self._tx_queue.append(packet)

    def receive(self):

        if not self._connected:
            raise RuntimeError("Transport not initialised.")

        if not self._rx_queue:
            return None

        return self._rx_queue.popleft()


    #Testing Helpers

    def inject(self, packet: bytes) -> None:
        """Inject an incoming packet into the receive queue."""

        self._rx_queue.append(packet)
        


    def transmitted(self) -> list[bytes]:
        """Return a snapshot of transmitted packets."""

        return list(self._tx_queue)

    def clear_history(self) -> None:
        """Clear transmitted packet history."""

        self._tx_queue.clear()


#Optional Queue Inspection
    @property
    def transmitted_count(self) -> int:
        return len(self._tx_queue)


    @property
    def pending_count(self) -> int:
        return len(self._rx_queue)