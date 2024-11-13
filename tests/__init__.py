from rest_framework.test import APITestCase, APIClient

from django.contrib.auth import get_user_model
from tasklists.models import TaskList

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
