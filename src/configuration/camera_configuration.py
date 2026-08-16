"""
Camera configuration.
"""

from dataclasses import dataclass


@dataclass(
    frozen=True,
    slots=True,
)
class CameraConfiguration:
    """Configuration for one camera."""

    camera_id: int

    enabled: bool

    host: str

    port: int