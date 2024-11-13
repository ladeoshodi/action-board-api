from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth import get_user_model

User = get_user_model()


class UserTest(APITestCase):

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

    def test_register_user(self):
        """
        Ensure we can successfully register a new user
        """

        url = "/api/user/register/"
        data = {
            "email": "testuser1@example.com",
            "username": "testuser1",
            "first_name": "Test1",
            "last_name": "User1",
            "password": "testuser1",
            "password_confirmation": "testuser1"
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.get(
            email="testuser1@example.com").username, 'testuser1')

    def test_login_user(self):
        """
        Ensure we can successfully login an existing user
        """

        url = "/api/user/login/"
        data = {
            "email": "testuser@example.com",
            "password": "testuser"
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("token", response.data)

    def test_login_user_invalid_password(self):
        """
        Ensure we can't login an existing user with invalid password
        """

        url = "/api/user/login/"
        data = {
            "email": ""
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_current_user(self):
        """
        Ensure we can get the current user
        """

        url = "/api/user/"
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("email"), "testuser@example.com")

    def test_update_current_user(self):
        """
        Ensure we can update the current user
        """

        url = "/api/user/"
        data = {
            "email": "newemail@example.com"
        }
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        self.assertEqual(User.objects.get(
            username="testuser").email, "newemail@example.com")

    def test_delete_current_user(self):
        """
        Ensure we can delete the current user
        """

        url = "/api/user/"
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

        response = self.client.delete(url)
        self.assertFalse(User.objects.get(
            email="testuser@example.com").is_active, False)
