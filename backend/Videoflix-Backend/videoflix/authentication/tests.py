from django.test import TestCase

# Create your tests here.
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework.views import status
from django.contrib.auth.tokens import default_token_generator


User = get_user_model()


class TestViews(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.test_user = User.objects.create_user(
            username="testuser",
            email="testuser@test.com",
            password="testpassword",
        )
        self.test_user.is_active = False
        self.test_user.save()

    def test_register(self):
        response = self.client.post(
            reverse("register"),
            {
                "username": "newuser",
                "email": "newuser@test.com",
                "password": "newpassword12345",
                "password_again": "newpassword12345",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(User.objects.count(), 2)
        self.assertEqual(User.objects.get(username="newuser").email, "newuser@test.com")

    def test_confirm_email(self):
        token = default_token_generator.make_token(self.test_user)
        response = self.client.get(reverse("confirm_email", args=[token]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.test_user.refresh_from_db()
        self.assertEqual(self.test_user.is_active, True)

    def test_login(self):
        self.test_user.is_active = True
        self.test_user.save()
        response = self.client.post(
            reverse("login"), {"email": "testuser@test.com", "password": "testpassword"}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(response.data.get("token"))

    def test_logout(self):
        self.client.login(username="testuser", password="testpassword")
        response = self.client.post(reverse("logout"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
