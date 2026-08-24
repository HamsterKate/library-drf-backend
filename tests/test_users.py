from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase

User = get_user_model()


class UserAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="user@example.com",
            password="testpassword123",
            first_name="John",
            last_name="Doe",
        )

        self.admin = User.objects.create_superuser(
            email="admin@example.com",
            password="adminpassword123",
            first_name="Admin",
            last_name="User",
        )

    def test_create_user(self):
        data = {
            "email": "new@example.com",
            "password": "newpassword123",
            "first_name": "New",
            "last_name": "User",
        }

        response = self.client.post("/api/users/", data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 3)

        user = User.objects.get(email="new@example.com")
        self.assertTrue(user.check_password("newpassword123"))

    def test_create_user_cannot_set_staff_status(self):
        data = {
            "email": "new@example.com",
            "password": "newpassword123",
            "first_name": "New",
            "last_name": "User",
            "is_staff": True,
        }

        response = self.client.post("/api/users/", data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        user = User.objects.get(email="new@example.com")
        self.assertFalse(user.is_staff)

    def test_list_users_requires_admin(self):
        response = self.client.get("/api/users/")

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_admin_can_list_users(self):
        self.client.force_authenticate(user=self.admin)

        response = self.client.get("/api/users/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_can_retrieve_self(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.get(f"/api/users/{self.user.id}/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["email"], self.user.email)

    def test_user_cannot_retrieve_other_user(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.get(f"/api/users/{self.admin.id}/")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_regular_user_cannot_list_users(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.get("/api/users/")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_can_update_self(self):
        self.client.force_authenticate(user=self.user)

        data = {
            "email": "updated@example.com",
            "first_name": "Updated",
            "last_name": "User",
        }

        response = self.client.patch(
            f"/api/users/{self.user.id}/",
            data,
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.email, "updated@example.com")
        self.assertEqual(self.user.first_name, "Updated")

    def test_user_cannot_update_other_user(self):
        self.client.force_authenticate(user=self.user)

        data = {
            "email": "hacked@example.com",
            "first_name": "Hacked",
            "last_name": "User",
        }

        response = self.client.put(
            f"/api/users/{self.admin.id}/",
            data,
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)