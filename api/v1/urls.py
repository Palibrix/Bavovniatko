from django.urls import path, include

app_name = 'api-v1'
urlpatterns = [
    # path(r'user/', include('api.v1.user.urls', namespace='user')),
    path(r'auth/', include('api.v1.authentication.urls', namespace='auth')),
    path(r'components/', include('api.v1.components.urls', namespace='components')),
    path(r'suggestions/', include('api.v1.suggestions.urls', namespace='suggestions')),
    path(r'builds/', include('api.v1.builds.urls', namespace='builds')),
    path(r'lists/', include('api.v1.lists.urls', namespace='lists')),
]
