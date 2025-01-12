from rest_framework.routers import DefaultRouter

from api.v1.suggestions.views.antenna_suggestions_views import AntennaSuggestionAPIViewSet, \
    AntennaTypeSuggestionAPIViewSet, AntennaConnectorSuggestionAPIViewSet

app_name = 'api-v1-suggestions'
router = DefaultRouter(trailing_slash=True)
router.register(r'antennas', AntennaSuggestionAPIViewSet, basename="antenna")
router.register(r'antenna_types', AntennaTypeSuggestionAPIViewSet, basename="antenna_type")
router.register(r'antenna_connectors', AntennaConnectorSuggestionAPIViewSet, basename="antenna_connector")


urlpatterns = [

] + router.urls
