from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api.v1.users.views import UserProfileViewSet

app_name = 'api-v1-users'
router = DefaultRouter(trailing_slash=True)
router.register(r'profiles', UserProfileViewSet, basename="profile")

urlpatterns = [
] + router.urls