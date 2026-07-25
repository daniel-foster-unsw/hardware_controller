"""
Integration tests for the motor workflow.
"""

from src.communication.mock_transport import MockTransport
from src.communication.packet import Packet
from src.motor.motor_manager import MotorManager

#-----------------------------------------------------
# Test 1 - Motor Workflow
#-----------------------------------------------------
def test_move_all():

    transport = MockTransport()

    transport.initialise()

    manager = MotorManager(
        transport=transport,
        motor_count=2,
    )

    manager.initialise()

    manager.move_all(500)

    assert transport.transmitted() == [

        Packet.move(0, 500),

        Packet.move(1, 500),
    ]

#-----------------------------------------------------
# Test 2 - Stop Workflow
#-----------------------------------------------------
def test_stop_all():

    transport = MockTransport()

    transport.initialise()

    manager = MotorManager(
        transport=transport,
        motor_count=3,
    )

    manager.initialise()

    manager.stop_all()

    assert transport.transmitted() == [

        Packet.stop(0),

        Packet.stop(1),

        Packet.stop(2),
    ]

#-----------------------------------------------------
# Test 3 - LED Workflow
#-----------------------------------------------------

def test_led_all():

    transport = MockTransport()

    transport.initialise()

    manager = MotorManager(
        transport=transport,
        motor_count=2,
    )

    manager.initialise()

    manager.led_all(0b101)

    assert transport.transmitted() == [

        Packet.led(0, 0b101),

        Packet.led(1, 0b101),
    ]

#-----------------------------------------------------
# Test 4 - AUX Workflow
#-----------------------------------------------------

def test_aux_all():

    transport = MockTransport()

    transport.initialise()

    manager = MotorManager(
        transport=transport,
        motor_count=2,
    )

    manager.initialise()

    manager.aux_all(0b0011)

    assert transport.transmitted() == [

        Packet.aux(0, 0b0011),

        Packet.aux(1, 0b0011),
    ]

#-----------------------------------------------------
# Test 5 - Mixed Commands
#-----------------------------------------------------
def test_command_sequence():

    transport = MockTransport()

    transport.initialise()

    manager = MotorManager(
        transport=transport,
        motor_count=2,
    )

    manager.initialise()

    manager.move_all(500)

    manager.led_all(0b001)

    manager.stop_all()

    assert transport.transmitted() == [

        Packet.move(0, 500),

        Packet.move(1, 500),

        Packet.led(0, 0b001),

        Packet.led(1, 0b001),

        Packet.stop(0),

        Packet.stop(1),
    ]

#-----------------------------------------------------
# Test 6 - Shutdown
#-----------------------------------------------------
def test_shutdown():

    transport = MockTransport()

    transport.initialise()

    manager = MotorManager(
        transport=transport,
        motor_count=4,
    )

    manager.initialise()

    manager.shutdown()

    assert len(manager) == 0

#-----------------------------------------------------
# Test 7 - Transport Still Works
#-----------------------------------------------------
def test_transport_connected():

    transport = MockTransport()

    transport.initialise()

    manager = MotorManager(
        transport=transport,
        motor_count=2,
    )

    manager.initialise()

    manager.move_all(500)

    assert transport.connected()

#-----------------------------------------------------
# Test 8 - Receive Path
#-----------------------------------------------------