from src.communication.mock_transport import MockTransport
from src.communication.packet import Packet



#Initialisation
def test_transport_initialises():

    transport = MockTransport()

    transport.initialise()

    assert transport.connected()

#Initialisation
def test_transport_initialises():

    transport = MockTransport()

    transport.initialise()

    assert transport.connected()

#Send
def test_send_packet():

    transport = MockTransport()

    transport.initialise()

    packet = Packet.stop(3)

    transport.send(packet)

    assert transport.transmitted_count == 1

    assert transport.transmitted()[0] == packet

#Receive
def test_receive_packet():

    transport = MockTransport()

    transport.initialise()

    packet = Packet.stop(2)

    transport.inject(packet)

    assert transport.pending_count == 1

    assert transport.receive() == packet

    assert transport.pending_count == 0

#Empty Queue
def test_receive_empty_queue():

    transport = MockTransport()

    transport.initialise()

    assert transport.receive() is None

#Shutdown
def test_shutdown():

    transport = MockTransport()

    transport.initialise()

    transport.shutdown()

    assert not transport.connected()


