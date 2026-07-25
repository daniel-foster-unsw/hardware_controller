"""
Transport factory.
"""

from src.communication.mock_transport import MockTransport
from src.communication.transport import Transport




class TransportFactory:
    """Creates transport implementations."""

    _TRANSPORTS: dict[str, type[Transport]] = {}

    @classmethod
    def register(
        cls,
        name: str,
        transport: type[Transport],
    ) -> None:
        """
        Register a transport implementation.
        """
        cls._TRANSPORTS[name.lower()] = transport




    @classmethod
    def create(
        cls,
        name: str,
    ) -> Transport:
        """
        Create a transport implementation.

        Args:
            transport_type: Name of the transport.

        Returns:
            Transport instance.

        Raises:
            ValueError: Unknown transport type.
        """

        try:
            transport_class = cls._TRANSPORTS[name.lower()]
            

        except KeyError as exc:

            raise ValueError(
                f"Unknown transport '{name}'."
            ) from exc

        return transport_class()


# ----------------------------------------------------------------------
# Register built-in transport implementations
# ----------------------------------------------------------------------

TransportFactory.register(
    "mock",
    MockTransport,
)