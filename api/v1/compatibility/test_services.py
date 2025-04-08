from django.test import TestCase
from mixer.backend.django import mixer

from api.v1.compatibility.checkers import CameraFrameCompatibilityChecker
from api.v1.compatibility.services import CompatibilityService
from components.models import Camera, Frame


class CompatibilityServiceTests(TestCase):
    def setUp(self):
        self.service = CompatibilityService()
        self.camera_frame_checker = CameraFrameCompatibilityChecker()
        mixer.register(Frame,
                       description='TestFrame',
                       )
        mixer.register(Camera,
                       description='TestCamera',
                       voltage_min=2,
                       voltage_max=10,
                       fov=180)

        # Create a frame with specific camera mount dimensions
        self.frame = mixer.blend(Frame, manufacturer="Test Frame Manufacturer", model="Test Frame")
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

    def test_camera_frame_compatibility(self):
        """Test direct camera-frame compatibility check"""
        # Test compatible camera-frame pair
        result = self.camera_frame_checker.check_compatibility(
            self.compatible_camera, self.frame)
        self.assertTrue(result['is_compatible'])
        self.assertEqual(len(result['issues']), 0)

        # Test incompatible camera-frame pair
        result = self.camera_frame_checker.check_compatibility(
            self.incompatible_camera, self.frame)
        self.assertFalse(result['is_compatible'])
        self.assertEqual(len(result['issues']), 1)
        self.assertEqual(result['issues'][0]['type'], 'dimension_mismatch')

    def test_get_component_pairs(self):
        """Test generation of component pairs for compatibility checking"""
        # Empty configuration should return empty list
        pairs = self.service._get_component_pairs({})
        self.assertEqual(len(pairs), 0)

        # Configuration with only one component should return empty list
        pairs = self.service._get_component_pairs({"camera": self.compatible_camera.id})
        self.assertEqual(len(pairs), 0)

        # Configuration with camera and frame should return one pair
        pairs = self.service._get_component_pairs({
            "camera": self.compatible_camera.id,
            "frame": self.frame.id
        })
        self.assertEqual(len(pairs), 1)

        # Pair should contain correct component types and IDs
        expected_pair = ("camera", self.compatible_camera.id, "frame", self.frame.id)
        self.assertIn(expected_pair, pairs)

        # Configuration with unrelated components should not return pairs
        pairs = self.service._get_component_pairs({
            "camera": self.compatible_camera.id,
            "speed_controller": 1  # Not directly related to camera
        })
        self.assertEqual(len(pairs), 0)

    def test_incremental_compatibility(self):
        """Test incremental compatibility checking with previous results"""
        # Initial configuration with compatible camera and frame
        config1 = {
            "camera": self.compatible_camera.id,
            "frame": self.frame.id
        }

        # Check initial compatibility
        results1 = self.service.check_compatibility(config1)
        self.assertTrue(results1['is_compatible'])

        # New configuration with incompatible camera and same frame
        config2 = {
            "camera": self.incompatible_camera.id,
            "frame": self.frame.id
        }

        # Check incremental compatibility
        results2 = self.service.check_compatibility(
            config2, previous_configuration=config1, previous_results=results1)
        self.assertFalse(results2['is_compatible'])

        # New configuration with only frame (camera removed)
        config3 = {
            "frame": self.frame.id
        }

        # Check compatibility after camera removed
        results3 = self.service.check_compatibility(
            config3, previous_configuration=config2, previous_results=results2)
        self.assertTrue(results3['is_compatible'])
        self.assertEqual(len(results3['issues']), 0)

        # Check that camera_frame result was removed
        self.assertNotIn('camera_frame', results3['pair_results'])