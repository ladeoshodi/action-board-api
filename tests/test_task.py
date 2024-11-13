from rest_framework import status

from . import BaseTest
from tasks.models import Task


class TaskTest(BaseTest):

    def test_get_tasks(self):
        """
        Ensure we can get tasks
        """
        url = "/api/tasks/"
        response = self.client.get(
            url, HTTP_AUTHORIZATION=f"Bearer {self.token}")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Task.objects.get(
            user=self.user).name, "Test Task")

    def test_get_single_task(self):
        """
        Ensure we can get a single task
        """
        url = f"/api/tasks/{self.task.id}/"
        response = self.client.get(
            url, HTTP_AUTHORIZATION=f"Bearer {self.token}")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Task.objects.get(
            user=self.user).name, "Test Task")

    def test_create_task(self):
        """
        Ensure we can create a new task
        """
        url = "/api/tasks/"
        data = {
            "name": "New Test Task",
            "description": "New Test Task Description",
            "task_list": self.tasklist.id,
            "tags": [self.tag.id]
        }

        response = self.client.post(
            url, data, format='json', HTTP_AUTHORIZATION=f"Bearer {self.token}")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.get(
            name="New Test Task").name, 'New Test Task')

    def test_update_task(self):
        """
        Ensure we can update a task
        """
        url = f"/api/tasks/{self.task.id}/"
        data = {
            "name": "Updated Test Task"
        }

        response = self.client.put(
            url, data, format='json', HTTP_AUTHORIZATION=f"Bearer {self.token}")

        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        self.assertEqual(Task.objects.get(
            user=self.user).name, 'Updated Test Task')

    def test_delete_task(self):
        """
        Ensure we can delete a task
        """
        url = f"/api/tasks/{self.task.id}/"
        response = self.client.delete(
            url, HTTP_AUTHORIZATION=f"Bearer {self.token}")

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Task.objects.count(), 0)
