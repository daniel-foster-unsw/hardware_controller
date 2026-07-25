"""
Unit tests for the MotorManager.
"""

import pytest

from src.communication.packet import Packet
from src.motor.motor_manager import MotorManager


class FakeTransport:
    """Simple transport for unit testing."""

    def __init__(self) -> None:
        self.packets: list[bytes] = []

    def send(self, packet: bytes) -> None:
        self.packets.append(packet)


def test_initialise_creates_all_controllers() -> None:
    """MotorManager creates the configured number of controllers."""

    transport = FakeTransport()

    manager = MotorManager(
        transport=transport,
        motor_count=8,
    )

    manager.initialise()

    assert len(manager) == 8

def test_shutdown_removes_all_controllers() -> None:
    """Shutdown removes all controllers."""

    transport = FakeTransport()

    manager = MotorManager(
        transport=transport,
        motor_count=8,
    )

    manager.initialise()

    manager.shutdown()

    assert len(manager) == 0


def test_controller_lookup() -> None:
    """Controllers can be retrieved by ID."""

    transport = FakeTransport()

    manager = MotorManager(
        transport=transport,
        motor_count=8,
    )

    manager.initialise()

    controller = manager[3]

    assert controller.controller_id == 3


@pytest.mark.parametrize("motor_count", [1, 2, 4, 8])
def test_iteration_returns_all_controllers(
    motor_count: int,
) -> None:
    """Iteration returns every controller."""

    transport = FakeTransport()

    manager = MotorManager(
        transport=transport,
        motor_count=motor_count,
    )

    manager.initialise()

    ids = [
        controller.controller_id
        for controller in manager
    ]

    assert ids == list(range(motor_count))


def test_stop_all() -> None:
    """Broadcast stop command."""

    transport = FakeTransport()

    manager = MotorManager(
        transport=transport,
        motor_count=4,
    )

    manager.initialise()

    manager.stop_all()

    assert transport.packets == [

        Packet.stop(0),

        Packet.stop(1),

        Packet.stop(2),

        Packet.stop(3),
    ]

def test_move_all() -> None:
    """Broadcast move command."""

    transport = FakeTransport()

    manager = MotorManager(
        transport=transport,
        motor_count=4,
    )

    manager.initialise()

    manager.move_all(500)

    assert transport.packets == [

        Packet.move(0, 500),

        Packet.move(1, 500),

        Packet.move(2, 500),

        Packet.move(3, 500),
    ]


def test_led_all() -> None:
    """Broadcast LED command."""

    transport = FakeTransport()

    manager = MotorManager(
        transport=transport,
        motor_count=4,
    )

    manager.initialise()

    manager.led_all(0b101)

    assert transport.packets == [

        Packet.led(0, 0b101),

        Packet.led(1, 0b101),

        Packet.led(2, 0b101),

        Packet.led(3, 0b101),
    ]

def test_aux_all() -> None:
    """Broadcast AUX command."""

    transport = FakeTransport()

    manager = MotorManager(
        transport=transport,
        motor_count=4,
    )

    manager.initialise()

    manager.aux_all(0b0011)

    assert transport.packets == [

        Packet.aux(0, 0b0011),

        Packet.aux(1, 0b0011),

        Packet.aux(2, 0b0011),

        Packet.aux(3, 0b0011),
    ]

def test_multiple_broadcast_commands() -> None:
    """Broadcast commands preserve packet order."""

    transport = FakeTransport()

    manager = MotorManager(
        transport=transport,
        motor_count=2,
    )

    manager.initialise()

    manager.move_all(250)

    manager.stop_all()

    assert transport.packets == [

        Packet.move(0, 250),

        Packet.move(1, 250),

        Packet.stop(0),

        Packet.stop(1),
    ]

def test_invalid_controller_lookup() -> None:
    """Looking up an invalid controller raises KeyError."""

    transport = FakeTransport()

    manager = MotorManager(
        transport=transport,
        motor_count=4,
    )

    manager.initialise()

    with pytest.raises(KeyError):

        _ = manager[99]


