from io import BytesIO

from PIL import Image
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.utils import timezone

User = get_user_model()

class BaseUserTest(TestCase):

    def create_image(self):
        image = Image.new('RGB', (10, 10))
        image_io = BytesIO()
        image.save(image_io, format='JPEG')
        return SimpleUploadedFile("test_image.jpg", image_io.getvalue(), content_type="image/jpeg")

    def create(self, username="test", email='test@mail.com', password='test_password'):
        user = User.objects.create_user(username=username, email=email, password=password)
        user.last_login = timezone.now()
        user.is_active = True
        user.save()

        return user

    def create_super_user(self, username="test", email='test@mail', password='test_password'):
        user = User.objects.create_superuser(username=username, email=email, password=password)
        user.last_login = timezone.now()
        user.is_active = True
        user.save()