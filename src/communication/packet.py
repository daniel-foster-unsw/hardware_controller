"""
Packet encoder and decoder.
"""

from dataclasses import dataclass

from src.common.constants import (
    MOVE,
    LED,
    STOP,
    AUX,
    ACTION_SHIFT,
    CONTROLLER_SHIFT,
    POSITION_MASK,
    MIN_CONTROLLER_ID,
    MAX_CONTROLLER_ID,
    MIN_POSITION,
    MAX_POSITION,
)
from src.common.exceptions import PacketError


@dataclass(frozen=True)
class PacketStatus:
    """Decoded status packet returned by a controller."""

    controller_id: int
    position_mm: int
    event: int


class Packet:
    """Encodes and decodes scanner controller packets."""



    #Validation Helpers
    @staticmethod
    def _validate_controller(controller_id: int) -> None:
        if not MIN_CONTROLLER_ID <= controller_id <= MAX_CONTROLLER_ID:
            raise PacketError(
                f"Controller ID must be between "
                f"{MIN_CONTROLLER_ID} and {MAX_CONTROLLER_ID}."
            )


    #Encoding Helper
    @staticmethod
    def _validate_position(position_mm: int) -> None:
        if not MIN_POSITION <= position_mm <= MAX_POSITION:
            raise PacketError(
                f"Position must be between "
                f"{MIN_POSITION} and {MAX_POSITION} mm."
            )

    @staticmethod
    def _encode(action: int,
                controller_id: int,
                payload: int = 0) -> bytes:

        command = (
            (action << ACTION_SHIFT)
            | (controller_id << CONTROLLER_SHIFT)
            | payload
        )

        return command.to_bytes(4, byteorder="little")


    #Packets
    @staticmethod
    def move(controller_id: int,
             position_mm: int) -> bytes:

        Packet._validate_controller(controller_id)
        Packet._validate_position(position_mm)

        return Packet._encode(
            MOVE,
            controller_id,
            position_mm & POSITION_MASK,
        )

    @staticmethod
    def stop(controller_id: int) -> bytes:

        Packet._validate_controller(controller_id)

        return Packet._encode(
            STOP,
            controller_id,
        )

    @staticmethod
    def led(controller_id: int, state: int) -> bytes:

        Packet._validate_controller(controller_id)

        return Packet._encode(
            LED,
            controller_id,
            state,
        )


    @staticmethod
    def aux(controller_id: int,
            state: int) -> bytes:

        Packet._validate_controller(controller_id)

        return Packet._encode(
            AUX,
            controller_id,
            state,
        )




    

    #Decode
    @staticmethod
    def decode(packet: bytes) -> PacketStatus:

        if len(packet) != 4:
            raise PacketError(
                "Status packet must contain exactly 4 bytes."
            )

        position = packet[0] | ((packet[1] & 0x07) << 8)

        controller = packet[2]

        event = packet[3]

        return PacketStatus(
            controller_id=controller,
            position_mm=position,
            event=event,
        )

