# favorites/tests/test_models.py
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta

from mixer.backend.django import mixer

from components.models import Antenna, Camera
from lists.models import List, AntennaListItem, CameraListItem

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
        self.antenna1 = mixer.blend(Antenna, model='Antenna One')
        self.antenna2 = mixer.blend(Antenna, model='Antenna Two')
        self.camera1 = mixer.blend(Camera, model='Camera One')
        self.camera2 = mixer.blend(Camera, model='Camera Two')

    def test_mixed_components_list(self):
        """Test creating a list with different types of components"""
        mixer.blend(AntennaListItem,
            list=self.list,
            component=self.antenna1,
            added_at=timezone.now() - timedelta(minutes=5)
        )
        mixer.blend(CameraListItem,
            list=self.list,
            component=self.camera1
        )

        # Verify both items are in the list
        self.assertEqual(self.list.count_by_type()['antenna'], 1)
        self.assertEqual(self.list.count_by_type()['camera'], 1)
        self.assertEqual(self.list.count_all, 2)

    def test_items_ordering(self):
        """Test that items are returned in correct order by added_at"""
        antenna_item = mixer.blend(AntennaListItem,
            list=self.list,
            component=self.antenna1,
            added_at=timezone.now() - timedelta(minutes=5)
        )
        camera_item = mixer.blend(CameraListItem,
            list=self.list,
            component=self.camera1
        )

        items = self.list.get_all_items()

        self.assertEqual(items[0], camera_item)
        self.assertEqual(items[1], antenna_item)

    def test_delete_specific_item(self):
        """Test removing a single item from a list"""
        antenna_item = mixer.blend(AntennaListItem,
            list=self.list,
            component=self.antenna1,
        )
        camera_item = mixer.blend(CameraListItem,
            list=self.list,
            component=self.camera1
        )

        antenna_item.delete()

        self.assertEqual(self.list.antenna_items.count(), 0)
        self.assertEqual(self.list.camera_items.count(), 1)

        remaining_item = self.list.camera_items.first()
        self.assertEqual(remaining_item, camera_item)

    def test_component_registry(self):
        """Test that all component types are registered correctly."""
        from lists.registry import ComponentRegistry
        from lists.models import AntennaListItem, CameraListItem

        # Test getting a model by type
        self.assertEqual(ComponentRegistry.get_model('antenna'), AntennaListItem)
        self.assertEqual(ComponentRegistry.get_model('camera'), CameraListItem)

        # Test unknown type
        self.assertIsNone(ComponentRegistry.get_model('unknown_type'))

        # Test all types are registered
        all_types = ComponentRegistry.get_all_types()
        self.assertIn('antenna', all_types)
        self.assertIn('camera', all_types)

    def test_bulk_remove_items(self):
        """Test removing multiple items at once from a list"""
        # Add several items to the list
        antenna_item1 = mixer.blend(AntennaListItem,
                                    list=self.list,
                                    component=self.antenna1
                                    )
        antenna_item2 = mixer.blend(AntennaListItem,
                                    list=self.list,
                                    component=self.antenna2
                                    )
        camera_item1 = mixer.blend(CameraListItem,
                                   list=self.list,
                                   component=self.camera1
                                   )
        camera_item2 = mixer.blend(CameraListItem,
                                   list=self.list,
                                   component=self.camera2
                                   )

        # Initial count verification
        self.assertEqual(self.list.count_all, 4)

        # Define items to remove (multiple component types)
        items_to_remove = [
            {'component_type': 'antenna', 'component_id': self.antenna1.id},
            {'component_type': 'camera', 'component_id': self.camera1.id}
        ]

        # Call the bulk remove method
        removed_count = self.list.remove_items_bulk(items_to_remove)

        # Verify correct number of items were removed
        self.assertEqual(removed_count, 2)

        # Verify remaining items
        self.assertEqual(self.list.antenna_items.count(), 1)
        self.assertEqual(self.list.camera_items.count(), 1)
        self.assertEqual(self.list.antenna_items.first().component, self.antenna2)
        self.assertEqual(self.list.camera_items.first().component, self.camera2)

    def test_bulk_remove_nonexistent_items(self):
        """Test removing items that don't exist or invalid types"""
        # Add one item
        antenna_item = mixer.blend(AntennaListItem,
                                   list=self.list,
                                   component=self.antenna1
                                   )

        # Try to remove items that don't exist or have invalid types
        items_to_remove = [
            {'component_type': 'antenna', 'component_id': 99999},  # Non-existent ID
            {'component_type': 'invalid_type', 'component_id': 1},  # Invalid type
            {'component_type': 'camera', 'component_id': self.camera1.id},  # Not in list
            {}  # Empty item data
        ]

        # Should not raise errors
        removed_count = self.list.remove_items_bulk(items_to_remove)

        # Should return 0 as nothing was removed
        self.assertEqual(removed_count, 0)

        # Original item should still be there
        self.assertEqual(self.list.antenna_items.count(), 1)