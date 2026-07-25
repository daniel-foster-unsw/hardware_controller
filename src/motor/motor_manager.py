from collections.abc import Iterator

from src.common.protocols import PacketSender
from src.motor.motor_controller import MotorController


class MotorManager:
    """Manages all motor controllers."""

    def __init__(
        self,
        transport: PacketSender,
        motor_count: int,
    ) -> None:

        self._transport = transport

        self._motor_count = motor_count

        self._controllers: dict[int, MotorController] = {}


    def initialise(self) -> None:
        """Create all motor controllers."""

        self._controllers.clear()

        for controller_id in range(self._motor_count):

            self._controllers[controller_id] = MotorController(
                controller_id=controller_id,
                transport=self._transport,
            )

    def shutdown(self) -> None:
        """Shutdown the manager."""

        self._controllers.clear()

    #Controller Lookup
    def controller(
        self,
        controller_id: int,
    ) -> MotorController:
        """Return a motor controller."""

        return self._controllers[controller_id]

    @property
    def count(self) -> int:

        return len(self._controllers)

    #----------------------------------------------------------------------
    #Python Collection Interface
    #----------------------------------------------------------------------
    def __len__(self) -> int:
        """Return the number of controllers."""

        return len(self._controllers)

    def __iter__(self) -> Iterator[MotorController]:
        """Iterate over all controllers."""

        return iter(self._controllers.values())

    def __getitem__(self, motor_id: int) -> MotorController:
        try:
            return self._controllers[motor_id]
        except KeyError:
            raise KeyError(f"Motor {motor_id} does not exist")
    
    #----------------------------------------------------------------------
    #Broadcast Methods
    #----------------------------------------------------------------------
    def stop_all(self) -> None:

        for controller in self:

            controller.stop()

    def move_all(
        self,
        position_mm: int,
    ) -> None:

        for controller in self:

            controller.move(position_mm)

    def led_all(
        self,
        state: int,
    ) -> None:

        for controller in self:

            controller.led(state)


    def aux_all(
        self,
        state: int,
    ) -> None:

        for controller in self:

            controller.aux(state)