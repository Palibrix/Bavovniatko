# flake8: noqa
from .antenna_suggestions import AntennaSuggestion, AntennaTypeSuggestion, AntennaConnectorSuggestion, ExistingAntennaDetailSuggestion, SuggestedAntennaDetailSuggestion
from .camera_suggestions import CameraSuggestion, SuggestedCameraDetailSuggestion, ExistingCameraDetailSuggestion, VideoFormatSuggestion

__all__ = [
    'AntennaSuggestion',
    'AntennaConnectorSuggestion',
    'AntennaTypeSuggestion',
    'ExistingAntennaDetailSuggestion',
    'SuggestedAntennaDetailSuggestion',

    'CameraSuggestion',
    'SuggestedCameraDetailSuggestion',
    'ExistingCameraDetailSuggestion',
    'VideoFormatSuggestion'
]
