from mixer.backend.django import mixer
from rest_framework.reverse import reverse

from api.v1.tests import BaseAPITest
from components.models import VideoFormat
from suggestions.models import VideoFormatSuggestion


class TestVideoFormatSuggestionAPIView(BaseAPITest):
    def setUp(self):
        self.user_1 = self.create_and_login(username="test1",
                                            email="test1@email.com")
        self.format_suggestion_1 = mixer.blend(VideoFormatSuggestion,
                                             user=self.user_1,)
        self.format_suggestion_2 = mixer.blend(VideoFormatSuggestion)
        self.format = mixer.blend(VideoFormat)

        self.create_data = {
            'format': 'New Format',
        }

    def test_list(self):
        url = reverse("api:v1:suggestions:video_format-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get("count"), VideoFormatSuggestion.objects.filter(user=self.user_1).count())

    def test_detail(self):
        url = reverse("api:v1:suggestions:video_format-detail", args={self.format_suggestion_1.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_detail_not_owner(self):
        url = reverse("api:v1:suggestions:video_format-detail", args={self.format_suggestion_2.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_create_new(self):
        url = reverse("api:v1:suggestions:video_format-list")
        response = self.client.post(url, data=self.create_data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(VideoFormatSuggestion.objects.count(), 3)

    def test_update(self):
        url = reverse("api:v1:suggestions:video_format-detail", args={self.format_suggestion_1.pk})
        response = self.client.put(url, data=self.create_data)
        self.assertEqual(response.status_code, 200)
        self.format_suggestion_1.refresh_from_db()
        self.assertEqual(self.format_suggestion_1.format, self.create_data["format"])

    def test_partial_update(self):
        update_data = {
            'format': self.create_data["format"],
        }
        url = reverse("api:v1:suggestions:video_format-detail", args={self.format_suggestion_1.pk})
        response = self.client.patch(url, data=update_data)
        self.assertEqual(response.status_code, 200)
        self.format_suggestion_1.refresh_from_db()
        self.assertEqual(self.format_suggestion_1.format, self.create_data["format"])

    def test_delete(self):
        url = reverse("api:v1:suggestions:video_format-detail", args={self.format_suggestion_1.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)

    def test_accept_not_admin(self):
        url = reverse("api:v1:suggestions:video_format-accept", args={self.format_suggestion_1.id})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(VideoFormat.objects.count(), 1)

    def test_accept(self):
        self.logout()
        self.create_and_login('test_superuser', is_super=True)

        url = reverse("api:v1:suggestions:video_format-accept", args={self.format_suggestion_1.id})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(VideoFormat.objects.count(), 2)
        self.format_suggestion_1.refresh_from_db()
        self.assertTrue(self.format_suggestion_1.status, 'approved')

    def test_deny(self):
        self.logout()
        self.create_and_login('test_superuser', is_super=True)

        url = reverse("api:v1:suggestions:video_format-deny", args={self.format_suggestion_1.id})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(VideoFormat.objects.count(), 1)
        self.format_suggestion_1.refresh_from_db()
        self.assertTrue(self.format_suggestion_1.status, 'denied')

    def test_cannot_modify_approved_suggestion(self):
        """Test that approved suggestions cannot be modified"""
        self.format_suggestion_1.status = 'approved'
        self.format_suggestion_1.save()

        update_data = {"format": 'New Format'}
        url = reverse("api:v1:suggestions:video_format-detail",
                      args={self.format_suggestion_1.id})
        response = self.client.patch(url, data=update_data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data[0], "Cannot modify approved suggestion")

    def test_denied_becomes_pending_on_update(self):
        """Test that denied suggestion becomes pending when modified"""
        self.format_suggestion_1.status = 'denied'
        self.format_suggestion_1.save()

        update_data = {"format": 'New Format'}
        url = reverse("api:v1:suggestions:video_format-detail",
                      args={self.format_suggestion_1.id})
        response = self.client.patch(url, data=update_data)
        self.assertEqual(response.status_code, 200)

        self.format_suggestion_1.refresh_from_db()
        self.assertEqual(self.format_suggestion_1.status, 'pending')