from src.communication.packet import Packet
from src.motor.motor_controller import MotorController

from src.common.exceptions import TransportError


class FakeTransport:
    """Simple transport used for unit testing."""

    def __init__(self):

        self.packets = []

    def send(self, packet: bytes) -> None:

        self.packets.append(packet)

#Test Construction
def test_controller_id():

    transport = FakeTransport()

    controller = MotorController(
        controller_id=3,
        transport=transport,
    )

    assert controller.controller_id == 3


#Move Test
def test_move():

    transport = FakeTransport()

    controller = MotorController(
        controller_id=2,
        transport=transport,
    )

    controller.move(500)

    assert len(transport.packets) == 1

    assert transport.packets[0] == Packet.move(2, 500)

#Stop Test
def test_stop():

    transport = FakeTransport()

    controller = MotorController(
        controller_id=5,
        transport=transport,
    )

    controller.stop()

    assert transport.packets == [
        Packet.stop(5)
    ]


#LED Test
def test_led():

    transport = FakeTransport()

    controller = MotorController(
        controller_id=1,
        transport=transport,
    )

    controller.led(0b101)

    assert transport.packets == [
        Packet.led(1, 0b101)
    ]

#AUX Test
def test_aux():

    transport = FakeTransport()

    controller = MotorController(
        controller_id=7,
        transport=transport,
    )

    controller.aux(0b0011)

    assert transport.packets == [
        Packet.aux(7, 0b0011)
    ]

#Multiple Commands
def test_multiple_commands():

    transport = FakeTransport()

    controller = MotorController(
        controller_id=4,
        transport=transport,
    )

    controller.move(250)

    controller.led(0b001)

    controller.stop()

    controller.aux(0b1000)

    assert transport.packets == [

        Packet.move(4, 250),

        Packet.led(4, 0b001),

        Packet.stop(4),

        Packet.aux(4, 0b1000),
    ]

#Invalid Position
import pytest

from src.common.exceptions import PacketError


def test_invalid_position():

    transport = FakeTransport()

    controller = MotorController(
        controller_id=0,
        transport=transport,
    )

    with pytest.raises(PacketError):

        controller.move(2000)

#Invalid Controller
def test_invalid_controller():

    transport = FakeTransport()

    controller = MotorController(
        controller_id=99,
        transport=transport,
    )

    with pytest.raises(PacketError):

        controller.stop()

#Transport Failure
class FailingTransport:

    def send(self, packet: bytes) -> None:

        raise TransportError("Communication failure.")

def test_transport_failure():

    controller = MotorController(
        controller_id=2,
        transport=FailingTransport(),
    )

    with pytest.raises(TransportError):

        controller.move(100)