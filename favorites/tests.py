# favorites/tests/test_models.py
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta

from mixer.backend.django import mixer

from components.models import Antenna, Camera
from favorites.models import List, AntennaListItem, CameraListItem

User = get_user_model()


class ListModelTests(TestCase):
    def setUp(self):
        mixer.register(Antenna,
                       description='Test Antenna',
                       bandwidth_min=10,
                       bandwidth_max=15,
                       center_frequency=12,
                       )
        mixer.register(Camera,
                       description='Test Camera',
                       fov=180,
                       voltage_min=10,
                       voltage_max=12)

        self.list = mixer.blend(List, name='Test List')
        self.antenna = mixer.blend(Antenna)
        self.camera = mixer.blend(Camera)

    def test_mixed_components_list(self):
        """Test creating a list with different types of components"""
        mixer.blend(AntennaListItem,
            list=self.list,
            component=self.antenna,
            added_at=timezone.now() - timedelta(minutes=5)
        )
        mixer.blend(CameraListItem,
            list=self.list,
            component=self.camera
        )

        # Verify both items are in the list
        self.assertEqual(self.list.count_by_type()['antenna'], 1)
        self.assertEqual(self.list.count_by_type()['camera'], 1)
        self.assertEqual(self.list.count_all, 2)

    def test_items_ordering(self):
        """Test that items are returned in correct order by added_at"""
        antenna_item = mixer.blend(AntennaListItem,
            list=self.list,
            component=self.antenna,
            added_at=timezone.now() - timedelta(minutes=5)
        )
        camera_item = mixer.blend(CameraListItem,
            list=self.list,
            component=self.camera
        )

        items = self.list.get_all_items()

        self.assertEqual(items[0], camera_item)
        self.assertEqual(items[1], antenna_item)

    def test_delete_specific_item(self):
        """Test removing a single item from a list"""
        antenna_item = mixer.blend(AntennaListItem,
            list=self.list,
            component=self.antenna,
        )
        camera_item = mixer.blend(CameraListItem,
            list=self.list,
            component=self.camera
        )

        antenna_item.delete()

        self.assertEqual(self.list.antenna_items.count(), 0)
        self.assertEqual(self.list.camera_items.count(), 1)

        remaining_item = self.list.camera_items.first()
        self.assertEqual(remaining_item, camera_item)