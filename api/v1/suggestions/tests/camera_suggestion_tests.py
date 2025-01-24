from mixer.backend.django import mixer
from rest_framework.reverse import reverse

from api.v1.tests import BaseAPITest
from components.models import VideoFormat, Camera, CameraDetail
from galleries.models import CameraGallery
from suggestions.models import VideoFormatSuggestion, CameraSuggestion, SuggestedCameraDetailSuggestion, \
    ExistingCameraDetailSuggestion


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


class TestCameraSuggestionAPIView(BaseAPITest):
    def setUp(self):
        self.user_1 = self.create_and_login(username="test1",
                                            email="test1@email.com")

        self.camera = mixer.blend(Camera)
        self.video_format = mixer.blend(VideoFormat)

        self.camera_suggestion_1 = mixer.blend(CameraSuggestion,
                                               tvl=1200,
                                               voltage_min=5.0,
                                               voltage_max=12.0,
                                               fov=90,
                                               user=self.user_1)
        mixer.blend(CameraGallery, suggestion=self.camera_suggestion_1)

        self.camera_suggestion_2 = mixer.blend(CameraSuggestion,
                                               tvl=1200,
                                               voltage_min=5.0,
                                               voltage_max=12.0,
                                               fov=90)
        mixer.blend(CameraGallery, suggestion=self.camera_suggestion_2)

        self.camera_1_detail_1 = mixer.blend(SuggestedCameraDetailSuggestion,
                                             suggestion=self.camera_suggestion_1)
        self.camera_1_detail_2 = mixer.blend(SuggestedCameraDetailSuggestion,
                                             suggestion=self.camera_suggestion_1)
        self.camera_2_detail_1 = mixer.blend(SuggestedCameraDetailSuggestion,
                                             suggestion=self.camera_suggestion_2)

        self.create_data = {
            "model": "Model 1",
            "manufacturer": "Manufacturer 2",
            "description": "Description 1",
            "tvl": 1200,
            "voltage_min": 5.0,
            "voltage_max": 12.0,
            "ratio": "4:3",
            "fov": 90,
            "output_type": "A",
            "light_sens": "normal",
            "weight": 50,
            "video_formats": [self.video_format.pk],
            "suggested_details": [
                {
                    "height": 20,
                    "width": 20
                }
            ],
            "suggested_images": [
                {
                    "image": self.create_base64_image('test_test.jpg'),
                    "order": 1
                }
            ],
            "suggested_documents": [
                {
                    "file": self.create_base64_pdf()
                }
            ]
        }

    def test_list(self):
        url = reverse("api:v1:suggestions:camera-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get("count"), CameraSuggestion.objects.filter(user=self.user_1).count())

    def test_detail(self):
        url = reverse("api:v1:suggestions:camera-detail", args={self.camera_suggestion_1.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["suggested_details"]),
                         SuggestedCameraDetailSuggestion.objects.filter(
                             suggestion=self.camera_suggestion_1).count())

    def test_detail_not_owner(self):
        url = reverse("api:v1:suggestions:camera-detail", args={self.camera_suggestion_2.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_create_new(self):
        url = reverse("api:v1:suggestions:camera-list")
        response = self.client.post(url, data=self.create_data)
        self.assertEqual(response.status_code, 201)
        suggestion = CameraSuggestion.objects.get(id=response.data['id'])
        self.assertEqual(CameraGallery.objects.filter(suggestion=response.data['id']).count(), 1)
        self.assertEqual(suggestion.status, 'pending')

    def test_update(self):
        url = reverse("api:v1:suggestions:camera-detail", args={self.camera_suggestion_1.pk})
        response = self.client.put(url, data=self.create_data)
        self.assertEqual(response.status_code, 200)
        self.camera_suggestion_1.refresh_from_db()
        self.assertEqual(self.camera_suggestion_1.tvl, self.create_data["tvl"])
        self.assertEqual(self.camera_suggestion_1.suggested_details.count(), 1)
        self.assertEqual(self.camera_suggestion_1.suggested_documents.count(), 1)

    def test_partial_update(self):
        update_data = {"model": "New Model Name"}
        url = reverse("api:v1:suggestions:camera-detail", args={self.camera_suggestion_1.id})
        response = self.client.patch(url, data=update_data)
        self.assertEqual(response.status_code, 200)
        self.camera_suggestion_1.refresh_from_db()
        self.assertEqual(self.camera_suggestion_1.model, update_data["model"])

    def test_delete(self):
        url = reverse("api:v1:suggestions:camera-detail", args={self.camera_suggestion_1.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)

    def test_accept(self):
        self.logout()
        self.create_and_login('test_superuser', is_super=True)
        url = reverse("api:v1:suggestions:camera-accept", args={self.camera_suggestion_1.id})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Camera.objects.count(), 2)
        self.camera_suggestion_1.refresh_from_db()
        self.assertEqual(self.camera_suggestion_1.status, 'approved')

    def test_deny(self):
        self.logout()
        self.create_and_login('test_superuser', is_super=True)
        comment = "Needs more details"
        url = reverse("api:v1:suggestions:camera-deny", args={self.camera_suggestion_1.id})
        response = self.client.post(url, {'admin_comment': comment})
        self.assertEqual(response.status_code, 200)
        self.camera_suggestion_1.refresh_from_db()
        self.assertEqual(self.camera_suggestion_1.status, 'denied')
        self.assertEqual(self.camera_suggestion_1.admin_comment, comment)

    def test_cannot_modify_approved_suggestion(self):
        """Test that approved suggestions cannot be modified"""
        self.camera_suggestion_1.status = 'approved'
        self.camera_suggestion_1.save()

        update_data = {"model": "New Model"}
        url = reverse("api:v1:suggestions:camera-detail",
                      args={self.camera_suggestion_1.id})
        response = self.client.patch(url, data=update_data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data[0], "Cannot modify approved suggestion")

    def test_denied_becomes_pending_on_update(self):
        """Test that denied suggestion becomes pending when modified"""
        self.camera_suggestion_1.status = 'denied'
        self.camera_suggestion_1.save()

        update_data = {"model": "New Model"}
        url = reverse("api:v1:suggestions:camera-detail",
                      args={self.camera_suggestion_1.id})
        response = self.client.patch(url, data=update_data)
        self.assertEqual(response.status_code, 200)

        self.camera_suggestion_1.refresh_from_db()
        self.assertEqual(self.camera_suggestion_1.status, 'pending')

    def test_partial_update_wrong_image(self):
        update_data = {
            "suggested_images": [
                {
                    'id': 3,
                    "image": self.create_base64_image('test_test.jpg'),
                    "order": 1
                },
            ]}
        url = reverse("api:v1:suggestions:camera-detail", args={self.camera_suggestion_1.id})
        response = self.client.patch(url, data=update_data)
        self.assertEqual(response.status_code, 400)

    def test_images_become_accepted_after_suggestion_accepted(self):
        """
        Gallery images should become accepted after suggestion is accepted
        """
        gallery = mixer.blend(CameraGallery,
                              image=self.create_image(),
                              suggestion=self.camera_suggestion_1,
                              accepted=False,
                              odrder=1)
        self.camera_suggestion_1.accept()
        gallery.refresh_from_db()
        self.assertTrue(gallery.accepted)
        self.assertEqual(gallery.object, self.camera_suggestion_1.related_instance)


class TestExistingCameraDetailSuggestionAPIView(BaseAPITest):
    def setUp(self):
        self.camera = mixer.blend(Camera)
        self.detail = mixer.blend(CameraDetail, camera=self.camera)

        self.user_1 = self.create_and_login(username="test1",
                                            email="test1@email.com")
        self.detail_suggestion_1 = mixer.blend(ExistingCameraDetailSuggestion,
                                               user=self.user_1,
                                               camera=self.camera)
        self.detail_suggestion_2 = mixer.blend(ExistingCameraDetailSuggestion,
                                               camera=self.camera)

        self.create_data = {
            'camera': self.camera.pk,
            'height': 20.0,
            'width': 20.0
        }

    def test_list(self):
        url = reverse("api:v1:suggestions:camera_detail-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get("count"),
                         ExistingCameraDetailSuggestion.objects.filter(user=self.user_1).count())

    def test_detail(self):
        url = reverse("api:v1:suggestions:camera_detail-detail", args={self.detail_suggestion_1.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_detail_not_owner(self):
        url = reverse("api:v1:suggestions:camera_detail-detail", args={self.detail_suggestion_2.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_create_new(self):
        url = reverse("api:v1:suggestions:camera_detail-list")
        response = self.client.post(url, data=self.create_data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(ExistingCameraDetailSuggestion.objects.count(), 3)

    def test_update(self):
        url = reverse("api:v1:suggestions:camera_detail-detail", args={self.detail_suggestion_1.pk})
        response = self.client.put(url, data=self.create_data)
        self.assertEqual(response.status_code, 200)
        self.detail_suggestion_1.refresh_from_db()
        self.assertEqual(self.detail_suggestion_1.height, self.create_data["height"])

    def test_partial_update(self):
        update_data = {'height': 30.0}
        url = reverse("api:v1:suggestions:camera_detail-detail", args={self.detail_suggestion_1.pk})
        response = self.client.patch(url, data=update_data)
        self.assertEqual(response.status_code, 200)
        self.detail_suggestion_1.refresh_from_db()
        self.assertEqual(self.detail_suggestion_1.height, update_data["height"])

    def test_delete(self):
        url = reverse("api:v1:suggestions:camera_detail-detail", args={self.detail_suggestion_1.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)

    def test_accept(self):
        self.logout()
        self.create_and_login('test_superuser', is_super=True)
        url = reverse("api:v1:suggestions:camera_detail-accept", args={self.detail_suggestion_1.id})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(CameraDetail.objects.count(), 2)
        self.detail_suggestion_1.refresh_from_db()
        self.assertEqual(self.detail_suggestion_1.status, 'approved')

    def test_cannot_modify_approved_suggestion(self):
        """Test that approved suggestions cannot be modified"""
        self.detail_suggestion_1.status = 'approved'
        self.detail_suggestion_1.save()

        update_data = {"height": 25.0}
        url = reverse("api:v1:suggestions:camera_detail-detail",
                      args={self.detail_suggestion_1.id})
        response = self.client.patch(url, data=update_data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data[0], "Cannot modify approved suggestion")

    def test_denied_becomes_pending_on_update(self):
        """Test that denied suggestion becomes pending when modified"""
        self.detail_suggestion_1.status = 'denied'
        self.detail_suggestion_1.save()

        update_data = {"height": 25.0}
        url = reverse("api:v1:suggestions:camera_detail-detail",
                      args={self.detail_suggestion_1.id})
        response = self.client.patch(url, data=update_data)
        self.assertEqual(response.status_code, 200)

        self.detail_suggestion_1.refresh_from_db()
        self.assertEqual(self.detail_suggestion_1.status, 'pending')
