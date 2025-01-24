from rest_framework.routers import DefaultRouter

from api.v1.suggestions.views.antenna_suggestion_views import AntennaSuggestionAPIViewSet, \
    AntennaTypeSuggestionAPIViewSet, AntennaConnectorSuggestionAPIViewSet, ExistingAntennaDetailSuggestionAPIViewSet
from api.v1.suggestions.views.camera_suggestion_views import VideoFormatSuggestionAPIViewSet, \
    CameraSuggestionAPIViewSet, ExistingCameraDetailSuggestionAPIViewSet

app_name = 'api-v1-suggestions'
router = DefaultRouter(trailing_slash=True)
router.register(r'antennas', AntennaSuggestionAPIViewSet, basename="antenna")
router.register(r'antenna_types', AntennaTypeSuggestionAPIViewSet, basename="antenna_type")
router.register(r'antenna_connectors', AntennaConnectorSuggestionAPIViewSet, basename="antenna_connector")
router.register(r'antenna_details', ExistingAntennaDetailSuggestionAPIViewSet, basename="antenna_detail")

router.register(r'video_formats', VideoFormatSuggestionAPIViewSet, basename="video_format")
router.register(r'cameras', CameraSuggestionAPIViewSet, basename="camera")
router.register(r'camera_details', ExistingCameraDetailSuggestionAPIViewSet, basename="camera_detail")

urlpatterns = [

] + router.urls
