from rest_framework.routers import DefaultRouter

from api.v1.builds.views import DroneAPIViewSet

app_name = 'api-v1-builds'
router = DefaultRouter(trailing_slash=True)
router.register(r'drones', DroneAPIViewSet, basename="drone")

urlpatterns = [

] + router.urls
