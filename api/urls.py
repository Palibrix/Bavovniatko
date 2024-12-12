from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

app_name = 'api'
urlpatterns = [
    path(r'v1/', include('api.v1.urls', namespace='v1')),
]
