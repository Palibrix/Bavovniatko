from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView, TokenBlacklistView

from api.v1.authentication.views import SignUpAPIView
from api.v1.builds.views import DroneAPIViewSet

app_name = 'api-v1-authentication'
router = DefaultRouter(trailing_slash=True)

urlpatterns = [
    path('signup/', SignUpAPIView.as_view(), name='signup'),

    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),

    path('token/blacklist/', TokenBlacklistView.as_view(), name='token_blacklist'),
] + router.urls
