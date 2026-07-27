"""
Scan state definitions.
"""

from enum import Enum


class ScanState(Enum):
    """Lifecycle states for a scan."""

    IDLE = "Idle"

    CREATE_SCAN = "Create Scan"

    RESET_MOTORS = "Reset Motors"

    MOVE = "Move"

    WAIT_FOR_MOTION = "Wait For Motion"

    CAPTURE = "Capture"

    WAIT_FOR_CAPTURE = "Wait For Capture"

    LOG_POSITION = "Log Position"

    DOWNLOAD = "Download"

    CLEANUP = "Cleanup"

    COMPLETE = "Complete"

    ERROR = "Error"

    PAUSED = "Paused"

    ABORTED = "Aborted"