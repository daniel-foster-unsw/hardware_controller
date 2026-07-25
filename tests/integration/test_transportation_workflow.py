"""
Integration tests for the communication transport workflow.
"""

from src.communication.mock_transport import MockTransport
from src.communication.packet import Packet

#---------------------------------------------------------
#Test 1 Initialisation
#---------------------------------------------------------
def test_transport_initialises() -> None:
    """Transport initialises correctly."""

    transport = MockTransport()

    transport.initialise()

    assert transport.connected()



#---------------------------------------------------------
#Test 2 Send Packet
#---------------------------------------------------------
def test_send_packet() -> None:
    """Packets can be transmitted."""

    transport = MockTransport()

    transport.initialise()

    packet = Packet.stop(3)

    transport.send(packet)

    assert transport.transmitted() == [

        packet,
    ]



#---------------------------------------------------------
#Test 3 Receive Packet
#---------------------------------------------------------
def test_receive_packet() -> None:
    """Injected packets can be received."""

    transport = MockTransport()

    transport.initialise()

    packet = Packet.stop(5)

    transport.inject(packet)

    assert transport.receive() == packet



#---------------------------------------------------------
#Test 4 FIFO Ordering
#---------------------------------------------------------
def test_receive_fifo_order() -> None:
    """Packets are received in FIFO order."""

    transport = MockTransport()

    transport.initialise()

    packets = [

        Packet.stop(0),

        Packet.stop(1),

        Packet.stop(2),

        Packet.stop(3),
    ]

    for packet in packets:

        transport.inject(packet)

    received = [

        transport.receive(),

        transport.receive(),

        transport.receive(),

        transport.receive(),
    ]

    assert received == packets


#---------------------------------------------------------
#Test 5 Multiple Sends
#---------------------------------------------------------
def test_multiple_send_order() -> None:
    """Packets are transmitted in order."""

    transport = MockTransport()

    transport.initialise()

    packets = [

        Packet.move(0, 100),

        Packet.move(1, 200),

        Packet.move(2, 300),
    ]

    for packet in packets:

        transport.send(packet)

    assert transport.transmitted() == packets

#---------------------------------------------------------
#Test 6 Receive Empty Queue
#---------------------------------------------------------
def test_receive_empty_queue() -> None:
    """Receiving from an empty queue returns None."""

    transport = MockTransport()

    transport.initialise()

    assert transport.receive() is None

#---------------------------------------------------------
#Test 7 Shutdown
#---------------------------------------------------------
def test_shutdown() -> None:
    """Transport disconnects correctly."""

    transport = MockTransport()

    transport.initialise()

    transport.shutdown()

    assert not transport.connected()


#---------------------------------------------------------
#Test 8 Queue Cleared On Shutdown
#---------------------------------------------------------
def test_shutdown_clears_queues() -> None:
    """Shutdown clears transmit and receive queues."""

    transport = MockTransport()

    transport.initialise()

    transport.send(
        Packet.stop(0)
    )

    transport.inject(
        Packet.stop(1)
    )

    transport.shutdown()

    assert transport.transmitted_count == 0

    assert transport.pending_count == 0


#---------------------------------------------------------
#Test 9 Reinitialise
#---------------------------------------------------------
def test_reinitialise() -> None:
    """Transport can be reinitialised."""

    transport = MockTransport()

    transport.initialise()

    transport.shutdown()

    transport.initialise()

    assert transport.connected()


#---------------------------------------------------------
#Test 10 Large Packet Sequence
#---------------------------------------------------------
def test_large_packet_sequence() -> None:
    """Transport handles multiple packets."""

    transport = MockTransport()

    transport.initialise()

    for controller in range(8):

        transport.send(
            Packet.move(controller, 500)
        )

    assert transport.transmitted_count == 8