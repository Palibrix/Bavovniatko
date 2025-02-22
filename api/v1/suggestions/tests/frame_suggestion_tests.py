from mixer.backend.django import mixer
from rest_framework.reverse import reverse

from api.v1.tests import BaseAPITest
from components.models import Frame, FrameCameraDetail, FrameMotorDetail, FrameVTXDetail
from galleries.models import FrameGallery
from suggestions.models import FrameSuggestion, ExistingFrameCameraDetailSuggestion, ExistingFrameMotorDetailSuggestion, \
    ExistingFrameVTXDetailSuggestion, SuggestedFrameCameraDetailSuggestion, SuggestedFrameMotorDetailSuggestion, \
    SuggestedFrameVTXDetailSuggestion


class TestFrameSuggestionAPIView(BaseAPITest):
    def setUp(self):
        self.user_1 = self.create_and_login(username="test1",
                                          email="test1@email.com")

        self.frame = mixer.blend(Frame)

        self.frame_suggestion_1 = mixer.blend(FrameSuggestion,
                                            prop_size='5 inch',
                                            size='220mm',
                                            material=Frame.MaterialChoice.FIBRE,
                                            configuration=Frame.ConfigurationChoice.X,
                                            user=self.user_1,
                                            )
        mixer.blend(FrameGallery, suggestion=self.frame_suggestion_1)

        self.frame_suggestion_2 = mixer.blend(FrameSuggestion,
                                            prop_size='5 inch',
                                            size='220mm',
                                            material=Frame.MaterialChoice.FIBRE,
                                            configuration=Frame.ConfigurationChoice.X)

        mixer.blend(FrameGallery, suggestion=self.frame_suggestion_2)

        self.camera_detail_1 = mixer.blend(SuggestedFrameCameraDetailSuggestion, suggestion=self.frame_suggestion_1)
        self.camera_detail_2 = mixer.blend(SuggestedFrameCameraDetailSuggestion, suggestion=self.frame_suggestion_1)
        self.motor_detail_1 = mixer.blend(SuggestedFrameMotorDetailSuggestion, suggestion=self.frame_suggestion_1)
        self.vtx_detail_1 = mixer.blend(SuggestedFrameVTXDetailSuggestion, suggestion=self.frame_suggestion_1)

        self.create_data = {
            "model": "Model 1",
            "manufacturer": "Manufacturer 2",
            "description": "Description 1",
            "prop_size": "5 inch",
            "size": "220mm",
            "weight": 150.5,
            "material": Frame.MaterialChoice.FIBRE,
            "configuration": Frame.ConfigurationChoice.X,
            "suggested_camera_details": [
                {
                    "camera_mount_height": 20,
                    "camera_mount_width": 20
                }
            ],
            "suggested_motor_details": [
                {
                    "motor_mount_height": 30,
                    "motor_mount_width": 30
                }
            ],
            "suggested_vtx_details": [
                {
                    "vtx_mount_height": 15,
                    "vtx_mount_width": 15
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
        url = reverse("api:v1:suggestions:frame-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get("count"), FrameSuggestion.objects.filter(user=self.user_1).count())

    def test_detail(self):
        url = reverse("api:v1:suggestions:frame-detail", args={self.frame_suggestion_1.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["suggested_camera_details"]),
                        SuggestedFrameCameraDetailSuggestion.objects.filter(suggestion=self.frame_suggestion_1).count())
        self.assertEqual(len(response.data["suggested_motor_details"]),
                        SuggestedFrameMotorDetailSuggestion.objects.filter(suggestion=self.frame_suggestion_1).count())
        self.assertEqual(len(response.data["suggested_vtx_details"]),
                        SuggestedFrameVTXDetailSuggestion.objects.filter(suggestion=self.frame_suggestion_1).count())

    def test_detail_not_owner(self):
        url = reverse("api:v1:suggestions:frame-detail", args={self.frame_suggestion_2.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_create_new(self):
        response = self.client.post(reverse("api:v1:suggestions:frame-list"), data=self.create_data)
        self.assertEqual(response.status_code, 201)
        suggestion = FrameSuggestion.objects.get(id=response.data['id'])
        self.assertEqual(FrameGallery.objects.filter(suggestion=response.data['id']).count(), 1)
        self.assertEqual(suggestion.status, 'pending')

    def test_update(self):
        url = reverse("api:v1:suggestions:frame-detail", args={self.frame_suggestion_1.pk})
        response = self.client.put(url, data=self.create_data)
        self.assertEqual(response.status_code, 200)
        self.frame_suggestion_1.refresh_from_db()

        self.assertEqual(self.frame_suggestion_1.prop_size, self.create_data["prop_size"])
        self.assertEqual(self.frame_suggestion_1.suggested_images.count(), 1)
        self.assertEqual(self.frame_suggestion_1.suggested_camera_details.count(), 1)
        self.assertEqual(self.frame_suggestion_1.suggested_motor_details.count(), 1)
        self.assertEqual(self.frame_suggestion_1.suggested_vtx_details.count(), 1)
        self.assertEqual(self.frame_suggestion_1.suggested_documents.count(), 1)

    def test_partial_update(self):
        update_data = {
            "model": "New Model Name",
            "suggested_images": [
                {
                    'id': 1,
                    "image": self.create_base64_image('test_test.jpg'),
                    "order": 1
                }
            ]
        }
        url = reverse("api:v1:suggestions:frame-detail", args={self.frame_suggestion_1.id})
        response = self.client.patch(url, data=update_data)
        self.assertEqual(response.status_code, 200)
        self.frame_suggestion_1.refresh_from_db()
        self.assertEqual(self.frame_suggestion_1.suggested_images.count(), 1)
        self.assertEqual(self.frame_suggestion_1.model, update_data["model"])

    def test_partial_update_wrong_image(self):
        update_data = {
            "suggested_images": [
                {
                    'id': 3,
                    "image": self.create_base64_image('test_test.jpg'),
                    "order": 1
                },
            ]}
        url = reverse("api:v1:suggestions:frame-detail", args={self.frame_suggestion_1.id})
        response = self.client.patch(url, data=update_data)
        self.assertEqual(response.status_code, 400)

    def test_delete(self):
        url = reverse("api:v1:suggestions:frame-detail", args={self.frame_suggestion_1.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)

    def test_accept_not_admin(self):
        url = reverse("api:v1:suggestions:frame-accept", args={self.frame_suggestion_1.id})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(Frame.objects.count(), 1)

    def test_accept(self):
        self.logout()
        self.create_and_login('test_superuser', is_super=True)

        url = reverse("api:v1:suggestions:frame-accept", args={self.frame_suggestion_1.id})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Frame.objects.count(), 2)
        self.frame_suggestion_1.refresh_from_db()
        self.assertEqual(self.frame_suggestion_1.status, 'approved')
        self.assertEqual(Frame.objects.filter(id=self.frame_suggestion_1.related_instance.id).get().images.count(), 1)
        self.assertEqual(FrameGallery.objects.get(id=1).accepted, True)

    def test_deny(self):
        self.logout()
        self.create_and_login('test_superuser', is_super=True)

        comment = "Needs more details"
        url = reverse("api:v1:suggestions:frame-deny", args={self.frame_suggestion_1.id})
        response = self.client.post(url, {'admin_comment': comment})
        self.assertEqual(response.status_code, 200)

        self.frame_suggestion_1.refresh_from_db()
        self.assertEqual(self.frame_suggestion_1.status, 'denied')
        self.assertEqual(self.frame_suggestion_1.admin_comment, comment)

    def test_cannot_modify_approved_suggestion(self):
        self.frame_suggestion_1.status = 'approved'
        self.frame_suggestion_1.save()

        update_data = {"model": "New Model"}
        url = reverse("api:v1:suggestions:frame-detail", args={self.frame_suggestion_1.id})
        response = self.client.patch(url, data=update_data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data[0], "Cannot modify approved suggestion")

    def test_denied_becomes_pending_on_update(self):
        self.frame_suggestion_1.status = 'denied'
        self.frame_suggestion_1.save()

        update_data = {"model": "New Model"}
        url = reverse("api:v1:suggestions:frame-detail", args={self.frame_suggestion_1.id})
        response = self.client.patch(url, data=update_data)
        self.assertEqual(response.status_code, 200)

        self.frame_suggestion_1.refresh_from_db()
        self.assertEqual(self.frame_suggestion_1.status, 'pending')


class TestExistingFrameMotorDetailSuggestionAPIView(BaseAPITest):
    def setUp(self):
        self.user_1 = self.create_and_login(username="test1", email="test1@email.com")
        self.frame = mixer.blend(Frame)

        self.motor_detail = mixer.blend(FrameMotorDetail, frame=self.frame)

        self.suggestion_1 = mixer.blend(ExistingFrameMotorDetailSuggestion,
                                        frame=self.frame,
                                        user=self.user_1)
        self.suggestion_2 = mixer.blend(ExistingFrameMotorDetailSuggestion,
                                        frame=self.frame)

        self.create_data = {
            'frame': self.frame.pk,
            'motor_mount_height': 30.0,
            'motor_mount_width': 30.0
        }

    def test_list(self):
        url = reverse("api:v1:suggestions:frame_motor_detail-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get("count"),
                         ExistingFrameMotorDetailSuggestion.objects.filter(user=self.user_1).count())

    def test_detail(self):
        url = reverse("api:v1:suggestions:frame_motor_detail-detail", args={self.suggestion_1.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_detail_not_owner(self):
        url = reverse("api:v1:suggestions:frame_motor_detail-detail", args={self.suggestion_2.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_create(self):
        url = reverse("api:v1:suggestions:frame_motor_detail-list")
        response = self.client.post(url, data=self.create_data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(ExistingFrameMotorDetailSuggestion.objects.count(), 3)

    def test_update(self):
        url = reverse("api:v1:suggestions:frame_motor_detail-detail", args={self.suggestion_1.pk})
        response = self.client.put(url, data=self.create_data)
        self.assertEqual(response.status_code, 200)
        self.suggestion_1.refresh_from_db()
        self.assertEqual(self.suggestion_1.motor_mount_height, self.create_data["motor_mount_height"])

    def test_partial_update(self):
        update_data = {'motor_mount_height': 35.0}
        url = reverse("api:v1:suggestions:frame_motor_detail-detail", args={self.suggestion_1.pk})
        response = self.client.patch(url, data=update_data)
        self.assertEqual(response.status_code, 200)
        self.suggestion_1.refresh_from_db()
        self.assertEqual(self.suggestion_1.motor_mount_height, update_data["motor_mount_height"])

    def test_delete(self):
        url = reverse("api:v1:suggestions:frame_motor_detail-detail", args={self.suggestion_1.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)

    def test_accept_not_admin(self):
        url = reverse("api:v1:suggestions:frame_motor_detail-accept", args={self.suggestion_1.id})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(FrameMotorDetail.objects.count(), 1)

    def test_accept(self):
        self.logout()
        self.create_and_login('test_superuser', is_super=True)
        url = reverse("api:v1:suggestions:frame_motor_detail-accept", args={self.suggestion_1.id})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(FrameMotorDetail.objects.count(), 2)
        self.suggestion_1.refresh_from_db()
        self.assertEqual(self.suggestion_1.status, 'approved')

    def test_deny(self):
        self.logout()
        self.create_and_login('test_superuser', is_super=True)
        comment = "Needs more details"
        url = reverse("api:v1:suggestions:frame_motor_detail-deny", args={self.suggestion_1.id})
        response = self.client.post(url, {'admin_comment': comment})
        self.assertEqual(response.status_code, 200)
        self.suggestion_1.refresh_from_db()
        self.assertEqual(self.suggestion_1.status, 'denied')
        self.assertEqual(self.suggestion_1.admin_comment, comment)

    def test_cannot_modify_approved_suggestion(self):
        self.suggestion_1.status = 'approved'
        self.suggestion_1.save()
        update_data = {"motor_mount_height": 25.0}
        url = reverse("api:v1:suggestions:frame_motor_detail-detail", args={self.suggestion_1.id})
        response = self.client.patch(url, data=update_data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data[0], "Cannot modify approved suggestion")

    def test_denied_becomes_pending_on_update(self):
        self.suggestion_1.status = 'denied'
        self.suggestion_1.save()
        update_data = {"motor_mount_height": 25.0}
        url = reverse("api:v1:suggestions:frame_motor_detail-detail", args={self.suggestion_1.id})
        response = self.client.patch(url, data=update_data)
        self.assertEqual(response.status_code, 200)
        self.suggestion_1.refresh_from_db()
        self.assertEqual(self.suggestion_1.status, 'pending')


class TestExistingFrameVTXDetailSuggestionAPIView(BaseAPITest):
    def setUp(self):
        self.user_1 = self.create_and_login(username="test1", email="test1@email.com")
        self.frame = mixer.blend(Frame)

        self.vtx_detail = mixer.blend(FrameVTXDetail, frame=self.frame)

        self.suggestion_1 = mixer.blend(ExistingFrameVTXDetailSuggestion,
                                        frame=self.frame,
                                        user=self.user_1)
        self.suggestion_2 = mixer.blend(ExistingFrameVTXDetailSuggestion,
                                        frame=self.frame)

        self.create_data = {
            'frame': self.frame.pk,
            'vtx_mount_height': 15.0,
            'vtx_mount_width': 15.0
        }

    def test_list(self):
        url = reverse("api:v1:suggestions:frame_vtx_detail-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get("count"),
                         ExistingFrameVTXDetailSuggestion.objects.filter(user=self.user_1).count())

    def test_detail(self):
        url = reverse("api:v1:suggestions:frame_vtx_detail-detail", args={self.suggestion_1.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_detail_not_owner(self):
        url = reverse("api:v1:suggestions:frame_vtx_detail-detail", args={self.suggestion_2.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_create(self):
        url = reverse("api:v1:suggestions:frame_vtx_detail-list")
        response = self.client.post(url, data=self.create_data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(ExistingFrameVTXDetailSuggestion.objects.count(), 3)

    def test_update(self):
        url = reverse("api:v1:suggestions:frame_vtx_detail-detail", args={self.suggestion_1.pk})
        response = self.client.put(url, data=self.create_data)
        self.assertEqual(response.status_code, 200)
        self.suggestion_1.refresh_from_db()
        self.assertEqual(self.suggestion_1.vtx_mount_height, self.create_data["vtx_mount_height"])

    def test_partial_update(self):
        update_data = {'vtx_mount_height': 20.0}
        url = reverse("api:v1:suggestions:frame_vtx_detail-detail", args={self.suggestion_1.pk})
        response = self.client.patch(url, data=update_data)
        self.assertEqual(response.status_code, 200)
        self.suggestion_1.refresh_from_db()
        self.assertEqual(self.suggestion_1.vtx_mount_height, update_data["vtx_mount_height"])

    def test_delete(self):
        url = reverse("api:v1:suggestions:frame_vtx_detail-detail", args={self.suggestion_1.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)

    def test_accept_not_admin(self):
        url = reverse("api:v1:suggestions:frame_vtx_detail-accept", args={self.suggestion_1.id})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(FrameVTXDetail.objects.count(), 1)

    def test_accept(self):
        self.logout()
        self.create_and_login('test_superuser', is_super=True)
        url = reverse("api:v1:suggestions:frame_vtx_detail-accept", args={self.suggestion_1.id})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(FrameVTXDetail.objects.count(), 2)
        self.suggestion_1.refresh_from_db()
        self.assertEqual(self.suggestion_1.status, 'approved')

    def test_deny(self):
        self.logout()
        self.create_and_login('test_superuser', is_super=True)
        comment = "Needs more details"
        url = reverse("api:v1:suggestions:frame_vtx_detail-deny", args={self.suggestion_1.id})
        response = self.client.post(url, {'admin_comment': comment})
        self.assertEqual(response.status_code, 200)
        self.suggestion_1.refresh_from_db()
        self.assertEqual(self.suggestion_1.status, 'denied')
        self.assertEqual(self.suggestion_1.admin_comment, comment)

    def test_cannot_modify_approved_suggestion(self):
        self.suggestion_1.status = 'approved'
        self.suggestion_1.save()
        update_data = {"vtx_mount_height": 25.0}
        url = reverse("api:v1:suggestions:frame_vtx_detail-detail", args={self.suggestion_1.id})
        response = self.client.patch(url, data=update_data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data[0], "Cannot modify approved suggestion")

    def test_denied_becomes_pending_on_update(self):
        self.suggestion_1.status = 'denied'
        self.suggestion_1.save()
        update_data = {"vtx_mount_height": 25.0}
        url = reverse("api:v1:suggestions:frame_vtx_detail-detail", args={self.suggestion_1.id})
        response = self.client.patch(url, data=update_data)
        self.assertEqual(response.status_code, 200)
        self.suggestion_1.refresh_from_db()
        self.assertEqual(self.suggestion_1.status, 'pending')