"""
Motor controller.
"""

from src.communication.packet import Packet
#from src.communication.transport import Transport
from src.common.protocols import PacketSender


class MotorController:
    """Controls a single scanner motor."""
    """
    def __init__(
        self,
        controller_id: int,
        transport: Transport,
    ):
    """
    def __init__(
        self,
        controller_id: int,
        transport: PacketSender,
    ):

        self._controller_id = controller_id
        self._transport = transport
    #Private
    @property
    def controller_id(self) -> int:
        """Return the controller ID."""

        return self._controller_id

    def _send(self, packet: bytes) -> None:
        """
        Send a packet via the configured transport.
        """
        """"
        #data logging
        self._logger.debug(
            "Controller %d -> %s",
            self._controller_id,
            packet.hex(),
        )
        """
        """
        #Retry support
        for attempt in range(3):

        try:

            self._transport.send(packet)

            return

        except TransportError:

            if attempt == 2:
                raise
        
        
        
        """
        self._transport.send(packet)

    #Public methods
    def move(self, position_mm: int) -> None:
        """Move the motor to the requested position."""

        self._send(
            Packet.move(
                self._controller_id,
                position_mm,
            )
        )

    def stop(self) -> None:
        """Stop the motor."""

        self._send(
            Packet.stop(
                self._controller_id
            )
        )  

    def led(self, state: int) -> None:
        """Set the controller LEDs."""

        self._send(
            Packet.led(
                self._controller_id,
                state,
            )
        )

    def aux(self, state: int) -> None:
        """Set the AUX outputs."""

        self._send(
            Packet.aux(
                self._controller_id,
                state,
            )
        )