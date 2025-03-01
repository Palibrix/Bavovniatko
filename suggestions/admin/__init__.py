# flake8: noqa
from .antenna_suggestion_admin import *
from .camera_suggestion_admin import *
from .frame_suggestion_admin import *
from .motor_suggestion_admin import *
from .propeller_suggestion_admin import *
from .receiver_suggestion_admin import *
from .stack_suggestion_admin import *
from .transmitter_suggestion_admin import *

__all__ = [
    # Antenna Suggestion Admins
    'AntennaSuggestionAdmin',
    'AntennaTypeSuggestionAdmin',
    'AntennaConnectorSuggestionAdmin',
    'ExistingAntennaDetailSuggestionAdmin',

    # Camera Suggestion Admins
    'CameraSuggestionAdmin',
    'VideoFormatSuggestionAdmin',
    'ExistingCameraDetailSuggestionAdmin',

    # Frame Suggestion Admins
    'FrameSuggestionAdmin',
    'ExistingFrameCameraDetailSuggestionAdmin',
    'ExistingFrameMotorDetailSuggestionAdmin',
    'ExistingFrameVTXDetailSuggestionAdmin',

    # Motor Suggestion Admins
    'MotorSuggestionAdmin',
    'RatedVoltageSuggestionAdmin',
    'ExistingMotorDetailSuggestionAdmin',

    # Propeller Suggestion Admins
    'PropellerSuggestionAdmin',

    # Receiver Suggestion Admins
    'ReceiverSuggestionAdmin',
    'ReceiverProtocolTypeSuggestionAdmin',
    'ExistingReceiverDetailSuggestionAdmin',

    # Stack Suggestion Admins
    'FlightControllerSuggestionAdmin',
    'SpeedControllerSuggestionAdmin',
    'StackSuggestionAdmin',
    'GyroSuggestionAdmin',
    'FlightControllerFirmwareSuggestionAdmin',
    'SpeedControllerFirmwareSuggestionAdmin',
    'SpeedControllerProtocolSuggestionAdmin',

    # Transmitter Suggestion Admins
    'TransmitterSuggestionAdmin',
    'OutputPowerSuggestionAdmin',
]