from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.v1.lists.views import ListViewSet

router = DefaultRouter()
router.register(r'', ListViewSet, basename='list')

app_name = 'lists'

urlpatterns = [
    path('', include(router.urls)),
]