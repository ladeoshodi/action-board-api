from rest_framework.test import APITestCase, APIClient

from django.contrib.auth import get_user_model
from tasklists.models import TaskList
from tags.models import Tag
from tasks.models import Task

User = get_user_model()


class BaseTest(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            email="testuser@example.com",
            username="testuser",
            first_name="Test",
            last_name="User",
            password="testuser"
        )

        # Obtain token for authenticated requests
        client = APIClient()
        url = "/api/user/login/"
        data = {
            "email": "testuser@example.com",
            "password": "testuser"
        }
        response = client.post(url, data, format='json')
        cls.token = response.data['token']

        # create tasklist
        cls.tasklist = TaskList.objects.create(
            name="Test TaskList",
            user=cls.user)

        # create tag
        cls.tag = Tag.objects.create(
            name="Test Tag",
            user=cls.user)

        # create task
        cls.task = Task.objects.create(
            name="Test Task",
            description="Test Task Description",
            user=cls.user,
            task_list=cls.tasklist
        )
        # add tag to task
        cls.task.tags.add(cls.tag)
