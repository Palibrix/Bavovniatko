from django.contrib.auth import get_user_model
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny

from api.v1.authentication.serializers import SignUpUserSerializer

User = get_user_model()

class SignUpAPIView(CreateAPIView):
    serializer_class = SignUpUserSerializer
    permission_classes = (AllowAny,)