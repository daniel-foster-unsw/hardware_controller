"""
Communication protocol constants.
"""

# Action Types (Byte 1 bits 6-7)
MOVE = 0b00
LED = 0b01
STOP = 0b10
AUX = 0b11

# Controller IDs
MIN_CONTROLLER_ID = 0
MAX_CONTROLLER_ID = 7

# Motion Limits
MIN_POSITION = 0
MAX_POSITION = 1060

# Bit Positions
ACTION_SHIFT = 14
CONTROLLER_SHIFT = 11
#CONTROLLER_SHIFT = 10
POSITION_MASK = 0x07FF

# Status Events
MOTOR_STOPPED = 0x01
RESET_DONE = 0x02
RESET_NOT_DONE = 0x03
MOTOR_AT_FWD_LIMIT = 0x04
MOTOR_AT_REV_LIMIT = 0x05
MOTOR_POSITION = 0x06
MOTOR_RESET = 0x07
MOTOR_DRIVING = 0x08

# Packet
PACKET_SIZE = 3


"""
The comments in the .ino explicitly define the packet layout:

Byte1 bits 6-7 : Action
Byte1 bits 3-5 : Motor Controller ID
Byte1 bits 0-2 : Position bits 8-10

Byte0 bits 0-7 : Position bits 0-7

For LED control:

Byte1 bits 6-7 : LED control
Byte1 bits 3-5 : Motor Controller ID
Byte0 bits 0-2 : LED state

For AUX:

Byte1 bits 6-7 : AUX control
Byte1 bits 3-5 : Motor Controller ID
Byte0 bits 0-3 : AUX state
"""