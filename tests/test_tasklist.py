from rest_framework import status

from . import BaseTest
from tasklists.models import TaskList


class TaskListTest(BaseTest):

    def test_get_tasklists(self):
        """
        Ensure we can get tasklists
        """
        url = "/api/tasklists/"
        response = self.client.get(
            url, HTTP_AUTHORIZATION=f"Bearer {self.token}")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(TaskList.objects.get(
            user=self.user).name, "Test TaskList")

    def test_get_single_tasklist(self):
        """
        Ensure we can get a single tasklist
        """
        url = f"/api/tasklists/{self.tasklist.id}/"
        response = self.client.get(
            url, HTTP_AUTHORIZATION=f"Bearer {self.token}")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(TaskList.objects.get(
            user=self.user).name, "Test TaskList")

    def test_create_tasklist(self):
        """
        Ensure we can create a new tasklist
        """
        url = "/api/tasklists/"
        data = {
            "name": "New Test TaskList"
        }

        response = self.client.post(
            url, data, format='json', HTTP_AUTHORIZATION=f"Bearer {self.token}")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(TaskList.objects.get(
            name="New Test TaskList").name, 'New Test TaskList')

    def test_update_tasklist(self):
        """
        Ensure we can update a tasklist
        """
        url = f"/api/tasklists/{self.tasklist.id}/"
        data = {
            "name": "Updated Test TaskList"
        }

        response = self.client.put(
            url, data, format='json', HTTP_AUTHORIZATION=f"Bearer {self.token}")

        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        self.assertEqual(TaskList.objects.get(
            user=self.user).name, 'Updated Test TaskList')

    def test_delete_tasklist(self):
        """
        Ensure we can delete a tasklist
        """
        url = f"/api/tasklists/{self.tasklist.id}/"
        response = self.client.delete(
            url, HTTP_AUTHORIZATION=f"Bearer {self.token}")

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(TaskList.objects.count(), 0)
