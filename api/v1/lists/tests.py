from django.db.models import Count
from mixer.backend.django import mixer
from rest_framework.reverse import reverse

from api.v1.tests import BaseAPITest
from components.models import Antenna, Camera
from favorites.models import List, AntennaListItem, CameraListItem


class TestListAPIView(BaseAPITest):
    def setUp(self):
        # Create and log in a test user
        self.user_1 = self.create_and_login(username="test1",
                                            email="test1@email.com")

        # Create another user for testing permissions
        self.user_2 = mixer.blend('auth.User', username="test2")

        # Create test components
        self.antenna = mixer.blend(Antenna)
        self.camera = mixer.blend(Camera)

        # Create lists for the current user
        self.list_1 = mixer.blend(List, name="My First List", owner=self.user_1)
        self.list_2 = mixer.blend(List, name="My Second List", owner=self.user_1)

        # Create a list for another user
        self.other_user_list = mixer.blend(List, name="Other User List", owner=self.user_2)

        # Add components to the lists
        self.antenna_item_1 = mixer.blend(AntennaListItem,
                                          list=self.list_1,
                                          component=self.antenna)
        self.camera_item_1 = mixer.blend(CameraListItem,
                                         list=self.list_1,
                                         component=self.camera)

        # Data for creating a new list
        self.create_data = {
            "name": "New Test List",
            "description": "A new list for testing"
        }

    def test_list(self):
        """Test retrieving all lists for the current user"""
        url = reverse("api:v1:favorites:list-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get("count"), List.objects.filter(owner=self.user_1).count())

    def test_detail(self):
        """Test retrieving a specific list"""
        url = reverse("api:v1:favorites:list-detail", args={self.list_1.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["name"], self.list_1.name)
        self.assertEqual(response.data["owner"], self.user_1.id)

    def test_detail_not_owner(self):
        """Test that users cannot access lists they don't own"""
        url = reverse("api:v1:favorites:list-detail", args={self.other_user_list.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_create_new(self):
        """Test creating a new list"""
        url = reverse("api:v1:favorites:list-list")
        response = self.client.post(url, data=self.create_data)
        self.assertEqual(response.status_code, 201)

        # Verify the list was created
        new_list = List.objects.get(id=response.data['id'])
        self.assertEqual(new_list.name, self.create_data["name"])
        self.assertEqual(new_list.owner, self.user_1)

    def test_update(self):
        """Test updating a list"""
        update_data = {
            "name": "Updated List Name",
            "description": "Updated description"
        }
        url = reverse("api:v1:favorites:list-detail", args={self.list_1.id})
        response = self.client.put(url, data=update_data)
        self.assertEqual(response.status_code, 200)

        # Verify the list was updated
        self.list_1.refresh_from_db()
        self.assertEqual(self.list_1.name, update_data["name"])
        self.assertEqual(self.list_1.description, update_data["description"])

    def test_partial_update(self):
        """Test partially updating a list"""
        update_data = {
            "name": "Partially Updated List"
        }
        url = reverse("api:v1:favorites:list-detail", args={self.list_1.id})
        response = self.client.patch(url, data=update_data)
        self.assertEqual(response.status_code, 200)

        # Verify only the name was updated
        self.list_1.refresh_from_db()
        self.assertEqual(self.list_1.name, update_data["name"])
        self.assertNotEqual(self.list_1.description, "")  # Description should remain unchanged

    def test_delete(self):
        """Test deleting a list"""
        url = reverse("api:v1:favorites:list-detail", args={self.list_1.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)

        # Verify the list was deleted
        with self.assertRaises(List.DoesNotExist):
            List.objects.get(id=self.list_1.id)

        # Verify related items were also deleted
        self.assertEqual(AntennaListItem.objects.filter(list=self.list_1).count(), 0)
        self.assertEqual(CameraListItem.objects.filter(list=self.list_1).count(), 0)

    def test_same_name_different_users(self):
        """Test that different users can have lists with the same name"""
        self.create_data["name"] = self.other_user_list.name  # Same name as other user's list
        url = reverse("api:v1:favorites:list-list")
        response = self.client.post(url, data=self.create_data)
        self.assertEqual(response.status_code, 201)

    def test_same_name_same_user(self):
        """Test that a user cannot have two lists with the same name"""
        self.create_data["name"] = self.list_1.name  # Same name as existing list
        url = reverse("api:v1:favorites:list-list")
        response = self.client.post(url, data=self.create_data)
        self.assertEqual(response.status_code, 400)  # Should return validation error

    def test_get_list_items(self):
        """Test retrieving all items in a list"""
        url = reverse("api:v1:favorites:list-items", args={self.list_1.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        # Check that both items are returned
        self.assertEqual(len(response.data), 2)

        # Check that items are ordered by added_at (newest first)
        self.assertTrue(response.data[0]["added_at"] >= response.data[1]["added_at"])

    def test_list_total_items(self):
        """Test that list response includes total_items count"""
        url = reverse("api:v1:favorites:list-detail", args={self.list_1.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["total_items"], 2)


class TestListItemAPIView(BaseAPITest):
    def setUp(self):
        # Create and log in a test user
        self.user_1 = self.create_and_login(username="test1",
                                            email="test1@email.com")

        # Create another user for testing permissions
        self.user_2 = mixer.blend('auth.User', username="test2")

        # Create test components
        self.antenna = mixer.blend(Antenna)
        self.camera = mixer.blend(Camera)
        self.antenna_2 = mixer.blend(Antenna)

        # Create lists
        self.list_1 = mixer.blend(List, name="My List", owner=self.user_1)
        self.other_user_list = mixer.blend(List, name="Other User List", owner=self.user_2)

        # Add a component to the first list
        self.antenna_item = mixer.blend(AntennaListItem,
                                        list=self.list_1,
                                        component=self.antenna)

    def test_add_antenna_to_list(self):
        """Test adding an antenna to a list"""
        url = reverse("api:v1:favorites:list-add-antenna", args={self.list_1.id})
        data = {"component_id": self.antenna_2.id}
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 201)

        # Verify the antenna was added
        self.assertEqual(AntennaListItem.objects.filter(
            list=self.list_1,
            component=self.antenna_2
        ).count(), 1)

    def test_add_camera_to_list(self):
        """Test adding a camera to a list"""
        url = reverse("api:v1:favorites:list-add-camera", args={self.list_1.id})
        data = {"component_id": self.camera.id}
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 201)

        # Verify the camera was added
        self.assertEqual(CameraListItem.objects.filter(
            list=self.list_1,
            component=self.camera
        ).count(), 1)

    def test_add_duplicate_component(self):
        """Test that adding the same component twice fails"""
        url = reverse("api:v1:favorites:list-add-antenna", args={self.list_1.id})
        data = {"component_id": self.antenna.id}  # Already in the list
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 400)  # Should return validation error

    def test_add_to_other_user_list(self):
        """Test that users cannot add to lists they don't own"""
        url = reverse("api:v1:favorites:list-add-antenna", args={self.other_user_list.id})
        data = {"component_id": self.antenna.id}
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 404)  # Should not find the list

    def test_remove_antenna_from_list(self):
        """Test removing an antenna from a list"""
        url = reverse("api:v1:favorites:list-remove-antenna", args={self.list_1.id})
        data = {"component_id": self.antenna.id}
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 204)

        # Verify the antenna was removed
        self.assertEqual(AntennaListItem.objects.filter(
            list=self.list_1,
            component=self.antenna
        ).count(), 0)

    def test_remove_nonexistent_component(self):
        """Test removing a component that's not in the list"""
        url = reverse("api:v1:favorites:list-remove-camera", args={self.list_1.id})
        data = {"component_id": self.camera.id}  # Not in the list
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 404)  # Should not find the item

    def test_filter_items_by_type(self):
        """Test filtering list items by component type"""
        # Add a camera to the list
        mixer.blend(CameraListItem, list=self.list_1, component=self.camera)

        # Get all antennas in the list
        url = reverse("api:v1:favorites:list-items", args={self.list_1.id})
        response = self.client.get(url, {"component_type": "antenna"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["component_type"], "antenna")

        # Get all cameras in the list
        response = self.client.get(url, {"component_type": "camera"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["component_type"], "camera")

    def test_items_include_component_details(self):
        """Test that item responses include component details"""
        url = reverse("api:v1:favorites:list-items", args={self.list_1.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        # Check that component details are included
        self.assertIn("component_details", response.data[0])
        self.assertEqual(response.data[0]["component_details"]["manufacturer"],
                         self.antenna.manufacturer)