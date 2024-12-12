from drf_yasg import openapi

SignUpAPIViewSchema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'username': openapi.Schema(type=openapi.TYPE_STRING, description='Username'),
        'email': openapi.Schema(type=openapi.TYPE_STRING, description='Email'),
        'password': openapi.Schema(type=openapi.TYPE_STRING, description='Password'),
        'first_name': openapi.Schema(type=openapi.TYPE_STRING, description='First name user'),
        'last_name': openapi.Schema(type=openapi.TYPE_STRING, description='Last name user'),
    }
)