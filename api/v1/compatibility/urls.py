from django.urls import path

from api.v1.compatibility.views import CompatibilityCheckView, CompatibleComponentsView

app_name = 'api-v1-compatibility'

urlpatterns = [
    path('check/', CompatibilityCheckView.as_view(), name='check'),
    path('components/<str:component_type>/', CompatibleComponentsView.as_view(), name='compatible_components'),
]