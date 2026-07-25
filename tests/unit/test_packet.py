#------------------------------------------------------------------
# iMPORTS
#------------------------------------------------------------------

import pytest

from dataclasses import FrozenInstanceError

from src.communication.packet import Packet, PacketStatus
from src.common.constants import (
    MOVE,
    STOP,
    LED,
    AUX,
    ACTION_SHIFT,
    CONTROLLER_SHIFT,
    POSITION_MASK,
    MOTOR_POSITION,
)

from src.common.constants import (
    MOTOR_STOPPED,
    RESET_DONE,
    RESET_NOT_DONE,
    MOTOR_AT_FWD_LIMIT,
    MOTOR_AT_REV_LIMIT,
    MOTOR_POSITION,
    MOTOR_RESET,
    MOTOR_DRIVING,
)



from src.common.exceptions import PacketError
#------------------------------------------------------------------
#helper
#------------------------------------------------------------------
def packet_to_int(packet: bytes) -> int:
    """Convert a packet into an integer for comparison."""
    return int.from_bytes(packet, byteorder="little")
#------------------------------------------------------------------
#Move Packet Tests
#------------------------------------------------------------------

#Position 0
def test_move_packet_position_zero():

    packet = Packet.move(0, 0)

    expected = (
        (MOVE << ACTION_SHIFT)
        | (0 << CONTROLLER_SHIFT)
        | 0
    )

    assert packet_to_int(packet) == expected

#Position 500
def test_move_packet_position_500():

    packet = Packet.move(3, 500)

    expected = (
        (MOVE << ACTION_SHIFT)
        | (3 << CONTROLLER_SHIFT)
        | (500 & POSITION_MASK)
    )

    assert packet_to_int(packet) == expected

#Maximum Position
def test_move_packet_max_position():

    packet = Packet.move(7, 1060)

    expected = (
        (MOVE << ACTION_SHIFT)
        | (7 << CONTROLLER_SHIFT)
        | (1060 & POSITION_MASK)
    )

    assert packet_to_int(packet) == expected


#Verify Representative Valid Positions

@pytest.mark.parametrize(
    "position",
    [
        0,
        1,
        250,
        500,
        750,
        1060,
    ],
)
def test_valid_positions(position):

    packet = Packet.move(0, position)

    assert len(packet) == 4

#------------------------------------------------------------------
#Stop Packet TESTS
#------------------------------------------------------------------
def test_stop_packet():

    packet = Packet.stop(5)

    expected = (
        (STOP << ACTION_SHIFT)
        | (5 << CONTROLLER_SHIFT)
    )

    assert packet_to_int(packet) == expected

#------------------------------------------------------------------
#LED Packet TESTS
#------------------------------------------------------------------
def test_led_packet():

    packet = Packet.led(2, 0b101)

    expected = (
        (LED << ACTION_SHIFT)
        | (2 << CONTROLLER_SHIFT)
        | 0b101
    )

    assert packet_to_int(packet) == expected

#------------------------------------------------------------------
#AUX Packet TESTS
#------------------------------------------------------------------
def test_aux_packet():

    packet = Packet.aux(6, 0b0101)

    expected = (
        (AUX << ACTION_SHIFT)
        | (6 << CONTROLLER_SHIFT)
        | 0b0101
    )

    assert packet_to_int(packet) == expected

#------------------------------------------------------------------
#Validation Tests
#------------------------------------------------------------------

#Invalid Controller IDs
@pytest.mark.parametrize("controller", [-1, 8, 100])
def test_invalid_controller(controller):

    with pytest.raises(PacketError):

        Packet.stop(controller)

#Invalid Positions
@pytest.mark.parametrize("position", [-1, 1061, 5000])
def test_invalid_position(position):

    with pytest.raises(PacketError):

        Packet.move(0, position)


# verify all valid ID
@pytest.mark.parametrize(
    "controller",
    range(8),
)
def test_valid_controller_ids(controller):

    packet = Packet.stop(controller)

    assert len(packet) == 4

#Position Validation
@pytest.mark.parametrize(
    "position",
    [
        0,
        1,
        250,
        500,
        750,
        1060,
    ],
)
def test_valid_positions(position):

    packet = Packet.move(0, position)

    assert len(packet) == 4

#Packet Length

@pytest.mark.parametrize(
    "packet",
    [
        Packet.move(0, 0),
        Packet.stop(0),
        Packet.led(0, 0),
        Packet.aux(0, 0),
    ],
)
def test_packet_length(packet):

    assert len(packet) == 4

#------------------------------------------------------------------
#Decode Tests
#------------------------------------------------------------------
"""
Construct a realistic status packet:

Position = 500
Controller = 4
Event = Position Report
"""

def test_decode_status_packet():

    packet = bytes([
        500 & 0xFF,
        (500 >> 8) & 0x07,
        4,
        MOTOR_POSITION,
    ])

    status = Packet.decode(packet)

    assert isinstance(status, PacketStatus)

    assert status.controller_id == 4

    assert status.position_mm == 500

    assert status.event == MOTOR_POSITION

    #Invalid Packet Length

@pytest.mark.parametrize(
    "packet",
    [
        b"",
        b"\x01",
        b"\x01\x02",
        b"\x01\x02\x03",
        b"\x01\x02\x03\x04\x05",
    ],
)
def test_invalid_packet_length(packet):

    with pytest.raises(PacketError):

        Packet.decode(packet)


#Decode All Events
@pytest.mark.parametrize(
    "event",
    [
        MOTOR_STOPPED,
        RESET_DONE,
        RESET_NOT_DONE,
        MOTOR_AT_FWD_LIMIT,
        MOTOR_AT_REV_LIMIT,
        MOTOR_POSITION,
        MOTOR_RESET,
        MOTOR_DRIVING,
    ],
)
def test_decode_all_events(event):

    packet = bytes([
        0xF4,
        0x01,
        3,
        event,
    ])

    status = Packet.decode(packet)

    assert status.controller_id == 3
    assert status.position_mm == 500
    assert status.event == event



#Decode Position Boundaries
@pytest.mark.parametrize(
    "position",
    [
        0,
        1,
        500,
        1060,
    ],
)
def test_decode_position(position):

    packet = bytes([
        position & 0xFF,
        (position >> 8) & 0x07,
        2,
        MOTOR_POSITION,
    ])

    status = Packet.decode(packet)

    assert status.position_mm == position

#Invalid Packet Sizes
@pytest.mark.parametrize(
    "size",
    [0, 1, 2, 3, 5, 6, 10],
)
def test_invalid_packet_sizes(size):

    with pytest.raises(PacketError):

        Packet.decode(bytes(size))

#Immutability Test
def test_packet_status_is_immutable():

    status = Packet.decode(
        bytes([
            0,
            0,
            1,
            MOTOR_POSITION,
        ])
    )

    with pytest.raises(FrozenInstanceError):
        status.position_mm = 100


#------------------------------------------------------------------
#Boundary Tests
#------------------------------------------------------------------
@pytest.mark.parametrize(
    "controller,position",
    [
        (0, 0),
        (0, 1060),
        (7, 0),
        (7, 1060),
        (3, 500),
    ],
)
def test_move_packet_boundaries(controller, position):

    packet = Packet.move(controller, position)

    expected = (
        (MOVE << ACTION_SHIFT)
        | (controller << CONTROLLER_SHIFT)
        | (position & POSITION_MASK)
    )

    assert packet_to_int(packet) == expected
