from django.urls import reverse
from mixer.backend.django import mixer
from rest_framework import status

from api.v1.tests import BaseAPITest
from components.models import Antenna, Camera
from lists.models import List, AntennaListItem, CameraListItem


class ListAPITest(BaseAPITest):
    def setUp(self):
        self.user = self.create_and_login(username="testuser", email="test@example.com")
        self.other_user = self.create(username="otheruser", email="other@example.com")

        self.antenna = mixer.blend(Antenna,
                                   model="Test Antenna",
                                   manufacturer="AntennaManufacturer",
                                   center_frequency=1.5,
                                   bandwidth_min=1.0,
                                   bandwidth_max=2.0)

        self.camera = mixer.blend(Camera,
                                  model="Test Camera",
                                  manufacturer="CameraManufacturer",
                                  fov=180,
                                  voltage_min=5.0,
                                  voltage_max=12.0)

        self.user_list = mixer.blend(List,
                                     owner=self.user,
                                     name="My Test List",
                                     description="My test list description")

        self.other_list = mixer.blend(List,
                                      owner=self.other_user,
                                      name="Other User's List")

        self.antenna_item = mixer.blend(AntennaListItem,
                                        list=self.user_list,
                                        component=self.antenna)

    def test_list_lists(self):
        """Test retrieving all user's lists."""
        # Create another list for the same user
        mixer.blend(List, owner=self.user, name="Second List")

        url = reverse("api:v1:lists:list-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        # Should find exactly 2 lists for the current user
        self.assertEqual(response.data['count'], 2)
        # Check that the first list has the correct name
        self.assertTrue(any(l['name'] == "My Test List" for l in response.data['results']))
        # Check that the first list has the correct parts count
        list_data = next(l for l in response.data['results'] if l['name'] == "My Test List")
        self.assertEqual(list_data['parts_count'], 1)

    def test_create_list(self):
        """Test creating a new list."""
        url = reverse("api:v1:lists:list-list")
        data = {
            "name": "New List",
            "description": "A new list description"
        }

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['name'], "New List")
        self.assertEqual(response.data['description'], "A new list description")
        self.assertEqual(response.data['owner']['username'], self.user.username)

        # Verify the list was saved to the database
        self.assertTrue(List.objects.filter(name="New List", owner=self.user).exists())

    def test_get_list_detail(self):
        """Test retrieving a specific list with its items."""
        url = reverse("api:v1:lists:list-detail", args=[self.user_list.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'], "My Test List")
        self.assertEqual(response.data['description'], "My test list description")
        self.assertEqual(len(response.data['items']), 1)

        # Check the item details
        item = response.data['items'][0]
        self.assertEqual(item['component_type'], "antenna")
        self.assertEqual(item['component_id'], self.antenna.id)
        self.assertTrue('display_name' in item)

        # Check the parts count by type
        self.assertEqual(response.data['parts_count_by_type']['antenna'], 1)
        if 'camera' in response.data['parts_count_by_type']:
            self.assertEqual(response.data['parts_count_by_type']['camera'], 0)

    def test_cannot_access_other_user_list(self):
        """Test that a user cannot access another user's list."""
        url = reverse("api:v1:lists:list-detail", args=[self.other_list.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 404)

    def test_update_list(self):
        """Test updating a list's information."""
        url = reverse("api:v1:lists:list-detail", args=[self.user_list.id])
        data = {
            "name": "Updated List Name",
            "description": "Updated description"
        }

        response = self.client.put(url, data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'], "Updated List Name")
        self.assertEqual(response.data['description'], "Updated description")

        # Verify the database was updated
        self.user_list.refresh_from_db()
        self.assertEqual(self.user_list.name, "Updated List Name")
        self.assertEqual(self.user_list.description, "Updated description")

    def test_partial_update_list(self):
        """Test partially updating a list."""
        url = reverse("api:v1:lists:list-detail", args=[self.user_list.id])
        data = {
            "name": "Partially Updated List"
        }

        response = self.client.patch(url, data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'], "Partially Updated List")
        # Description should remain unchanged
        self.assertEqual(response.data['description'], "My test list description")

        # Verify the database was updated correctly
        self.user_list.refresh_from_db()
        self.assertEqual(self.user_list.name, "Partially Updated List")
        self.assertEqual(self.user_list.description, "My test list description")

    def test_delete_list(self):
        """Test deleting a list."""
        url = reverse("api:v1:lists:list-detail", args=[self.user_list.id])
        response = self.client.delete(url)

        self.assertEqual(response.status_code, 204)

        # Verify the list was deleted
        self.assertFalse(List.objects.filter(id=self.user_list.id).exists())

        # Verify that the list items were also deleted
        self.assertEqual(AntennaListItem.objects.filter(list=self.user_list.id).count(), 0)

    def test_add_component(self):
        """Test adding a component to a list."""
        url = reverse("api:v1:lists:list-add-component", args=[self.user_list.id])
        data = {
            "component_type": "camera",
            "component_id": self.camera.id
        }

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, 201)

        # Verify the component was added to the database
        self.assertTrue(self.user_list.camera_items.filter(component=self.camera).exists())

        # Now list should have two items (antenna and camera)
        self.assertEqual(self.user_list.count_all, 2)

    def test_add_invalid_component(self):
        """Test adding a component that doesn't exist."""
        url = reverse("api:v1:lists:list-add-component", args=[self.user_list.id])
        data = {
            "component_type": "camera",
            "component_id": 999999  # Non-existent ID
        }

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, 400)
        self.assertIn("does not exist", str(response.data))

    def test_add_duplicate_component(self):
        """Test that adding the same component twice fails."""
        url = reverse("api:v1:lists:list-add-component", args=[self.user_list.id])
        data = {
            "component_type": "antenna",
            "component_id": self.antenna.id
        }

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, 400)
        self.assertIn("already in the list", str(response.data['detail']))

    def test_remove_component(self):
        """Test removing a single component from a list."""
        url = reverse("api:v1:lists:list-remove-components", args=[self.user_list.id])
        data = {
            "component_type": "antenna",
            "component_id": self.antenna.id
        }

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, 200)

        # Verify the component was removed
        self.assertFalse(self.user_list.antenna_items.filter(component=self.antenna).exists())
        self.assertEqual(self.user_list.count_all, 0)

    def test_remove_nonexistent_component(self):
        """Test trying to remove a component that's not in the list."""
        url = reverse("api:v1:lists:list-remove-components", args=[self.user_list.id])
        data = {
            "component_type": "camera",  # No camera in the list yet
            "component_id": self.camera.id
        }

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, 404)
        self.assertIn("not found", str(response.data['detail']))

    def test_bulk_remove_components(self):
        """Test removing multiple components at once."""
        # Add a camera to the list first
        mixer.blend(CameraListItem, list=self.user_list, component=self.camera)

        # Verify we have 2 items before removal
        self.assertEqual(self.user_list.count_all, 2)

        url = reverse("api:v1:lists:list-remove-components", args=[self.user_list.id])
        data = {
            "items": [
                {"component_type": "antenna", "component_id": self.antenna.id},
                {"component_type": "camera", "component_id": self.camera.id}
            ]
        }

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("Removed 2 components", str(response.data['detail']))

        # Verify both components were removed
        self.assertEqual(self.user_list.antenna_items.count(), 0)
        self.assertEqual(self.user_list.camera_items.count(), 0)
        self.assertEqual(self.user_list.count_all, 0)

    def test_bulk_remove_partial_success(self):
        """Test bulk removal with some valid and some invalid items."""
        url = reverse("api:v1:lists:list-remove-components", args=[self.user_list.id])
        data = {
            "items": [
                {"component_type": "antenna", "component_id": self.antenna.id},
                {"component_type": "camera", "component_id": 99999},  # Non-existent
                {"component_type": "invalid_type", "component_id": 1}  # Invalid type
            ]
        }

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("Removed 1 components", str(response.data['detail']))

        # Only the antenna should have been removed
        self.assertEqual(self.user_list.antenna_items.count(), 0)

    def test_filter_by_type(self):
        """Test filtering list items by component type."""
        # Add a camera to the list
        mixer.blend(CameraListItem, list=self.user_list, component=self.camera)

        # First, filter for antennas
        url = reverse("api:v1:lists:list-filter-by-type", args=[self.user_list.id])
        response = self.client.get(url, {"type": "antenna"})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['component_type'], "antenna")

        # Now, filter for cameras
        response = self.client.get(url, {"type": "camera"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['component_type'], "camera")

        # Test with invalid type
        response = self.client.get(url, {"type": "invalid_type"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Test with missing type parameter
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
