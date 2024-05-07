from .frame_admin import *
from .antenna_admin import *
from .battery_admin import *
from .camera_admin import *
from .receiver_admin import *
from .propeller_admin import *
from .transmitter_admin import *
from .motor_admin import *
from .stack_admin import *


__all__ = [
    'AntennaAdmin',
    'AntennaTypeAdmin',
    'AntennaConnectorAdmin',

    'BatteryAdmin',

    'CameraAdmin',

    'FrameAdmin',
    'FlightControllerAdmin',

    'MotorAdmin',
    'RatedVoltageAdmin',

    'PropellerAdmin',

    'ReceiverAdmin',

    'StackAdmin',
    'SpeedControllerAdmin',

    'TransmitterAdmin',
]
