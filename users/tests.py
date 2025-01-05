import base64
from io import BytesIO

from reportlab.pdfgen import canvas
from PIL import Image
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.utils import timezone

User = get_user_model()

class BaseUserTest(TestCase):

    def create_image(self, filename='test_image.jpg'):
        image = Image.new('RGB', (10, 10))
        image_io = BytesIO()
        image.save(image_io, format='JPEG')
        return SimpleUploadedFile(filename, image_io.getvalue(), content_type="image/jpeg")

    def create_base64_image(self, filename='test_image.jpg'):
        return base64.b64encode(self.create_image(filename).read())

    def create_simple_pdf(self, filename='test_pdf.pdf'):
        buffer = BytesIO()
        p = canvas.Canvas(buffer)
        p.drawString(100, 750, "Test text")
        p.showPage()
        p.save()
        pdf_content = buffer.getvalue()
        buffer.close()
        return SimpleUploadedFile(filename, pdf_content, content_type="application/pdf")

    def create_base64_pdf(self, filename='test_pdf.pdf'):
        return base64.b64encode(self.create_simple_pdf(filename).read())

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

        return user