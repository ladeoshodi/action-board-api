from rest_framework import status

from . import BaseTest
from tags.models import Tag


class TagTest(BaseTest):

    def test_get_tags(self):
        """
        Ensure we can get the tags
        """
        url = "/api/tags/"
        response = self.client.get(
            url, HTTP_AUTHORIZATION=f"Bearer {self.token}")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Tag.objects.get(
            user=self.user).name, "Test Tag")

    def test_get_single_tag(self):
        """
        Ensure we can get a single tag
        """
        url = f"/api/tags/{self.tag.id}/"
        response = self.client.get(
            url, HTTP_AUTHORIZATION=f"Bearer {self.token}")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Tag.objects.get(
            user=self.user).name, "Test Tag")

    def test_create_tag(self):
        """
        Ensure we can create a new tag
        """
        url = "/api/tags/"
        data = {
            "name": "New Test Tag"
        }

        response = self.client.post(
            url, data, format='json', HTTP_AUTHORIZATION=f"Bearer {self.token}")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Tag.objects.get(
            name="New Test Tag").name, 'New Test Tag')

    def test_delete_tag(self):
        """
        Ensure we can delete a tag
        """
        url = f"/api/tags/{self.tag.id}/"
        response = self.client.delete(
            url, HTTP_AUTHORIZATION=f"Bearer {self.token}")

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        with self.assertRaises(Tag.DoesNotExist):
            Tag.objects.get(name="Updated Test Tag")
