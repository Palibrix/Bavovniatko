# flake8: noqa
from .antenna_suggestion import AntennaSuggestion, AntennaTypeSuggestion, AntennaConnectorSuggestion, ExistingAntennaDetailSuggestion, SuggestedAntennaDetailSuggestion
from .camera_suggestion import CameraSuggestion, SuggestedCameraDetailSuggestion, ExistingCameraDetailSuggestion, VideoFormatSuggestion
from .frame_suggestion import FrameSuggestion, SuggestedFrameVTXDetailSuggestion, SuggestedFrameMotorDetailSuggestion, SuggestedFrameCameraDetailSuggestion, SuggestionFilesDeletionMixin, ExistingFrameVTXDetailSuggestion, ExistingFrameCameraDetailSuggestion, ExistingFrameMotorDetailSuggestion
from .motor_suggestion import MotorSuggestion, SuggestedMotorDetailSuggestion, ExistingMotorDetailSuggestion, RatedVoltageSuggestion
from .propeller_suggestion import PropellerSuggestion
from .receiver_suggestion import ReceiverSuggestion, ReceiverProtocolTypeSuggestion, SuggestedReceiverDetailSuggestion, ExistingReceiverDetailSuggestion
from .stack_suggestion import StackSuggestion, GyroSuggestion, SpeedControllerSuggestion, FlightControllerSuggestion, FlightControllerFirmwareSuggestion, SpeedControllerFirmwareSuggestion, SpeedControllerProtocolSuggestion
__all__ = [
    'AntennaSuggestion',
    'AntennaConnectorSuggestion',
    'AntennaTypeSuggestion',
    'ExistingAntennaDetailSuggestion',
    'SuggestedAntennaDetailSuggestion',

    'CameraSuggestion',
    'SuggestedCameraDetailSuggestion',
    'ExistingCameraDetailSuggestion',
    'VideoFormatSuggestion',

    'FrameSuggestion',
    'ExistingFrameMotorDetailSuggestion',
    'ExistingFrameVTXDetailSuggestion',
    'ExistingFrameCameraDetailSuggestion',
    'SuggestionFilesDeletionMixin',
    'SuggestedFrameVTXDetailSuggestion',
    'SuggestedFrameMotorDetailSuggestion',
    'SuggestedFrameCameraDetailSuggestion',

    'MotorSuggestion',
    'SuggestedMotorDetailSuggestion',
    'ExistingMotorDetailSuggestion',
    'RatedVoltageSuggestion',

    'PropellerSuggestion',

    'ReceiverSuggestion',
    'SuggestedReceiverDetailSuggestion',
    'ExistingReceiverDetailSuggestion',
    'ReceiverProtocolTypeSuggestion',

    'StackSuggestion',
    'SpeedControllerProtocolSuggestion',
    'SpeedControllerSuggestion',
    'SpeedControllerFirmwareSuggestion',
    'GyroSuggestion',
    'FlightControllerSuggestion',
    'FlightControllerFirmwareSuggestion'

]
