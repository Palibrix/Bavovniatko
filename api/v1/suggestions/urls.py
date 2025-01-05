from rest_framework.routers import DefaultRouter

from api.v1.suggestions.views.antenna_suggestions_views import AntennaSuggestionAPIViewSet

app_name = 'api-v1-suggestions'
router = DefaultRouter(trailing_slash=True)
router.register(r'antennas', AntennaSuggestionAPIViewSet, basename="antenna")


urlpatterns = [

] + router.urls
