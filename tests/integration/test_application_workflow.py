"""
Integration tests for the application workflow.
"""

import pytest

from src.application import Application
from src.communication.packet import Packet



#---------------------------------------------------------
#Test 1 Application Initialises
#---------------------------------------------------------
def test_application_initialises() -> None:
    """Application initialises successfully."""

    app = Application()

    app.initialise()

    assert app.configuration is not None
    assert app.logger_manager is not None
    assert app.transport is not None
    assert app.motor_manager is not None

#---------------------------------------------------------
#Test 2 Transport Connected
#---------------------------------------------------------
def test_transport_initialised() -> None:
    """Transport is connected after application startup."""

    app = Application()

    app.initialise()

    assert app.transport.connected()
#---------------------------------------------------------
#Test 3 Motor Manager Created
#---------------------------------------------------------
def test_motor_manager_initialised() -> None:
    """MotorManager creates every configured controller."""

    app = Application()

    app.initialise()

    assert len(app.motor_manager) == app.configuration.motor_count



#---------------------------------------------------------
#Test 4 Controller Lookup
#---------------------------------------------------------
def test_controller_lookup() -> None:
    """Controllers are accessible through the manager."""
    """Controllers can be accessed by ID."""

    app = Application()

    app.initialise()

    controller = app.motor_manager[3]

    assert controller.controller_id == 3

#---------------------------------------------------------
#Test 5 Command Flow
#---------------------------------------------------------



def test_command_flow() -> None:
    """Commands flow through the application."""

    app = Application()

    app.initialise()

    app.motor_manager.move_all(500)

    assert app.transport.transmitted() == [

        Packet.move(0, 500),

        Packet.move(1, 500),

        Packet.move(2, 500),

        Packet.move(3, 500),

        Packet.move(4, 500),

        #Packet.move(5, 500),

        #Packet.move(6, 500),

        #Packet.move(7, 500),
    ]

#---------------------------------------------------------
#Test 6 Shutdown
#---------------------------------------------------------
def test_application_shutdown() -> None:
    """Application shuts down cleanly."""

    app = Application()

    app.initialise()

    app.shutdown()

    #assert len(app.motor_manager) == 0
    #assert not app.transport.connected()

    assert app.transport is None
    assert app.motor_manager is None

#---------------------------------------------------------
#Test 7 Restart
#---------------------------------------------------------
def test_restart() -> None:
    """Application can be restarted."""

    app = Application()

    app.initialise()

    app.shutdown()

    app.initialise()

    assert app.transport.connected()

    assert len(app.motor_manager) == (
        app.configuration.motor_count
    )

#---------------------------------------------------------
#Test 8 Run Before Initialise
#---------------------------------------------------------
def test_run_before_initialise() -> None:
    """Running before initialise raises an error."""

    app = Application()

    with pytest.raises(RuntimeError):

        app.run()

#---------------------------------------------------------
#Test 9 Initialised Flag
#---------------------------------------------------------
def test_initialised_flag() -> None:
    """Application tracks its lifecycle."""

    app = Application()

    assert not app.initialised

    app.initialise()

    assert app.initialised

    app.shutdown()

    assert not app.initialised

#---------------------------------------------------------
#Test 10 Multiple Start/Stop Cycles
#---------------------------------------------------------
def test_multiple_start_stop_cycles() -> None:
    """Application survives repeated start/stop cycles."""

    app = Application()

    for _ in range(3):

        app.initialise()

        assert app.initialised

        app.shutdown()

        assert not app.initialised

#---------------------------------------------------------
#Test 11 Motor Count
#---------------------------------------------------------
def test_motor_manager_created() -> None:
    """Motor manager creates every configured controller."""

    app = Application()

    app.initialise()

    assert len(app.motor_manager) == (
        app.configuration.motor_count
    )
