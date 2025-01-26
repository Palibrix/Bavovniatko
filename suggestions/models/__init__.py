# flake8: noqa
from .antenna_suggestion import AntennaSuggestion, AntennaTypeSuggestion, AntennaConnectorSuggestion, ExistingAntennaDetailSuggestion, SuggestedAntennaDetailSuggestion
from .camera_suggestion import CameraSuggestion, SuggestedCameraDetailSuggestion, ExistingCameraDetailSuggestion, VideoFormatSuggestion
from .frame_suggestion import FrameSuggestion, SuggestedFrameVTXDetailSuggestion, SuggestedFrameMotorDetailSuggestion, SuggestedFrameCameraDetailSuggestion, SuggestionFilesDeletionMixin, ExistingFrameVTXDetailSuggestion, ExistingFrameCameraDetailSuggestion, ExistingFrameMotorDetailSuggestion
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
    'SuggestedFrameCameraDetailSuggestion'
]
