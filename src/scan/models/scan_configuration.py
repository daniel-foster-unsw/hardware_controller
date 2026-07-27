"""
Scan configuration.
"""

from dataclasses import dataclass


@dataclass(
    frozen=True,
    slots=True,
)
class ScanConfiguration:
    """Configuration for a scan."""

    #
    # Scan
    #

    scan_id: str

    scan_name: str

    #
    # Motion
    #

    start_position_mm: int

    end_position_mm: int

    capture_spacing_mm: int

    motor_speed_mm_s: int

    #
    # Camera
    #

    capture_delay_s: float

    enabled_cameras: tuple[int, ...]

    #
    # Behaviour
    #

    reset_before_scan: bool

    reset_after_scan: bool

    auto_download: bool

    delete_remote_files: bool

    def __post_init__(self) -> None:
        """Validate the configuration."""

        self._validate_scan()

        self._validate_motion()

        self._validate_camera()

    #
    # Properties
    #

    @property
    def scan_range_mm(self) -> int:
        """Return the scan range."""

        return (
            self.end_position_mm
            - self.start_position_mm
        )

    @property
    def capture_count(self) -> int:
        """Return the number of capture positions."""

        return (
            self.scan_range_mm
            // self.capture_spacing_mm
        ) + 1

    @property
    def camera_count(self) -> int:
        """Return the number of enabled cameras."""

        return len(self.enabled_cameras)

    @property
    def estimated_image_count(self) -> int:
        """Return the total number of images."""

        return (
            self.capture_count
            * self.camera_count
        )

    #
    # Validation
    #

    def _validate_scan(self) -> None:

        if not self.scan_id.strip():

            raise ValueError(
                "Scan ID cannot be empty."
            )

        if not self.scan_name.strip():

            raise ValueError(
                "Scan name cannot be empty."
            )

    def _validate_motion(self) -> None:

        if self.start_position_mm < 0:

            raise ValueError(
                "Start position must be non-negative."
            )

        if self.end_position_mm <= self.start_position_mm:

            raise ValueError(
                "End position must be greater than the start position."
            )

        if self.capture_spacing_mm <= 0:

            raise ValueError(
                "Capture spacing must be positive."
            )

        if self.motor_speed_mm_s <= 0:

            raise ValueError(
                "Motor speed must be positive."
            )

        if self.capture_count < 2:

            raise ValueError(
                "Capture spacing must produce at least two capture positions."
            )

    def _validate_camera(self) -> None:

        if self.capture_delay_s < 0:

            raise ValueError(
                "Capture delay cannot be negative."
            )

        if not self.enabled_cameras:

            raise ValueError(
                "At least one camera must be enabled."
            )

        if len(self.enabled_cameras) != len(
            set(self.enabled_cameras)
        ):

            raise ValueError(
                "Duplicate camera IDs."
            )

        if any(
            camera <= 0
            for camera in self.enabled_cameras
        ):

            raise ValueError(
                "Camera IDs must be positive."
            )