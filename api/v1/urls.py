from django.urls import path, include

app_name = 'api-v1'
urlpatterns = [

    path(r'components/', include('api.v1.components.urls', namespace='components')),
]
