from django.test import TestCase
from django.urls import reverse
from mixer.backend.django import mixer
from rest_framework.test import APIClient

from api.v1.compatibility.checkers import CameraFrameCompatibilityChecker
from api.v1.compatibility.services import CompatibilityService
from components.models import Camera, Frame


class CompatibilityViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        mixer.register(Frame,
                       description='TestFrame',
                       )
        mixer.register(Camera,
                       description='TestCamera',
                       voltage_min=2,
                       voltage_max=10,
                       fov=180)

        # Create a frame with specific camera mount dimensions
        self.frame = mixer.blend(Frame, manufacturer="Frame Manufacturer", model="Test Frame")
        self.frame_camera_detail = mixer.blend(
            'components.FrameCameraDetail',
            frame=self.frame,
            camera_mount_height=20.0,
            camera_mount_width=20.0
        )

        # Create a compatible camera
        self.compatible_camera = mixer.blend(Camera, manufacturer="Compatible Camera", model="Model A")
        mixer.blend(
            'components.CameraDetail',
            camera=self.compatible_camera,
            height=20.0,
            width=20.0
        )

        # Create an incompatible camera
        self.incompatible_camera = mixer.blend(Camera, manufacturer="Incompatible Camera", model="Model B")
        mixer.blend(
            'components.CameraDetail',
            camera=self.incompatible_camera,
            height=30.0,
            width=30.0
        )

    def test_check_compatibility_endpoint(self):
        """Test the compatibility check endpoint"""
        url = reverse("api:v1:compatibility:check")

        # Test with compatible camera and frame
        data = {
            "configuration": {
                "camera": self.compatible_camera.id,
                "frame": self.frame.id
            }
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.data['is_compatible'])
        self.assertEqual(len(response.data['issues']), 0)

        # Test with incompatible camera and frame
        data = {
            "configuration": {
                "camera": self.incompatible_camera.id,
                "frame": self.frame.id
            }
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.data['is_compatible'])
        self.assertEqual(len(response.data['issues']), 1)

        # Check that issue contains the right component references
        self.assertIn('camera', response.data['issues'][0]['component_refs'])
        self.assertIn('frame', response.data['issues'][0]['component_refs'])

    def test_incremental_compatibility_check(self):
        """Test incremental compatibility checking via API"""
        url = reverse("api:v1:compatibility:check")

        # Initial configuration with incompatible camera
        data1 = {
            "configuration": {
                "camera": self.incompatible_camera.id,
                "frame": self.frame.id
            }
        }

        response1 = self.client.post(url, data1, format='json')
        self.assertEqual(response1.status_code, 200)
        self.assertFalse(response1.data['is_compatible'])

        # Update to compatible camera with incremental check
        data2 = {
            "configuration": {
                "camera": self.compatible_camera.id,
                "frame": self.frame.id
            },
            "previous_configuration": data1["configuration"],
            "previous_results": response1.data
        }

        response2 = self.client.post(url, data2, format='json')
        self.assertEqual(response2.status_code, 200)
        self.assertTrue(response2.data['is_compatible'])

        # Verify only camera_frame pair was checked (should be in pair_results)
        self.assertIn('camera_frame', response2.data['pair_results'])

    def test_compatible_components_endpoint(self):
        """Test the endpoint for getting compatible components"""
        url = reverse("api:v1:compatibility:compatible_components", args=["camera"])

        # Get cameras compatible with frame
        data = {
            "configuration": {
                "frame": self.frame.id
            }
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 200)

        # Check results contain compatibility info
        self.assertTrue(all('compatibility' in item for item in response.data))

        # Identify compatible and incompatible cameras in results
        compatible = [item for item in response.data
                      if item['compatibility']['is_compatible']]
        incompatible = [item for item in response.data
                        if not item['compatibility']['is_compatible']]

        # Compatible camera should be marked as compatible
        self.assertTrue(any(item['id'] == self.compatible_camera.id
                            for item in compatible))

        # Incompatible camera should be marked as incompatible
        self.assertTrue(any(item['id'] == self.incompatible_camera.id
                            for item in incompatible))

        # Test reverse relationship (frames compatible with camera)
        url = reverse("api:v1:compatibility:compatible_components", args=["frame"])

        data = {
            "configuration": {
                "camera": self.compatible_camera.id
            }
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 200)

        # Our test frame should be compatible with compatible_camera
        compatible_frames = [item for item in response.data
                             if item['compatibility']['is_compatible']]
        self.assertTrue(any(item['id'] == self.frame.id
                            for item in compatible_frames))
