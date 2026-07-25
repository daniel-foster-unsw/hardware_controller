"""
Protocol regression tests.

These tests verify that packet encoding remains compatible
with the ESP32 firmware protocol.
"""

from src.communication.packet import Packet

def packet_to_int(packet: bytes) -> int:
    """Convert a packet to a 32-bit integer."""

    return int.from_bytes(
        packet,
        byteorder="little",
    )

def test_move_controller0_position0():

    assert packet_to_int(
        Packet.move(0, 0)
    ) == 0x00000000

def test_move_controller3_position500():

    assert packet_to_int(
        Packet.move(3, 500)
    ) == 0x000019F4

def test_move_controller7_position1060():

    assert packet_to_int(
        Packet.move(7, 1060)
    ) == 0x00003C24

def test_stop_controller0():

    assert packet_to_int(
        Packet.stop(0)
    ) == 0x00008000

def test_stop_controller5():

    assert packet_to_int(
        Packet.stop(5)
    ) == 0x0000A800

def test_led_green():

    assert packet_to_int(
        Packet.led(2, 0b001)
    ) == 0x00005001


def test_led_all():

    assert packet_to_int(
        Packet.led(2, 0b111)
    ) == 0x00005007


def test_aux_aux1():

    assert packet_to_int(
        Packet.aux(1, 0b0001)
    ) == 0x0000C801

def test_aux_all():

    assert packet_to_int(
        Packet.aux(1, 0b1111)
    ) == 0x0000C80F

def test_packet_size():

    assert len(Packet.move(0, 0)) == 4

    assert len(Packet.stop(0)) == 4

    assert len(Packet.led(0, 0)) == 4

    assert len(Packet.aux(0, 0)) == 4