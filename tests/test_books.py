from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase

from books.models import Book


class BookAPITests(APITestCase):
    def setUp(self):
        self.user_model = get_user_model()

        self.admin = self.user_model.objects.create_superuser(
            username="admin",
            password="admin123",
        )

        self.book = Book.objects.create(
            title="The Hobbit",
            author="J.R.R. Tolkien",
            cover=Book.Cover.HARD,
            inventory=5,
            daily_fee="2.50",
        )

        self.list_url = "/api/library/books/"
        self.detail_url = f"{self.list_url}{self.book.id}/"

    def test_list_books_unauthenticated(self):
        response = self.client.get(self.list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["title"], self.book.title)

    def test_detail_book_unauthenticated(self):
        response = self.client.get(self.detail_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], self.book.id)
        self.assertEqual(response.data["title"], self.book.title)

    def test_create_book_requires_admin(self):
        data = {
            "title": "1984",
            "author": "George Orwell",
            "cover": Book.Cover.SOFT,
            "inventory": 3,
            "daily_fee": "1.50",
        }

        response = self.client.post(self.list_url, data)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_can_create_book(self):
        self.client.force_authenticate(user=self.admin)

        data = {
            "title": "1984",
            "author": "George Orwell",
            "cover": Book.Cover.SOFT,
            "inventory": 3,
            "daily_fee": "1.50",
        }

        response = self.client.post(self.list_url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 2)
        self.assertEqual(response.data["title"], "1984")

    def test_update_book_requires_admin(self):
        data = {
            "title": "The Hobbit Updated",
            "author": "J.R.R. Tolkien",
            "cover": Book.Cover.HARD,
            "inventory": 10,
            "daily_fee": "3.00",
        }

        response = self.client.put(self.detail_url, data)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_can_update_book(self):
        self.client.force_authenticate(user=self.admin)

        data = {
            "title": "The Hobbit Updated",
            "author": "J.R.R. Tolkien",
            "cover": Book.Cover.SOFT,
            "inventory": 10,
            "daily_fee": "3.00",
        }

        response = self.client.put(self.detail_url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "The Hobbit Updated")
        self.assertEqual(response.data["cover"], Book.Cover.SOFT)
        self.assertEqual(response.data["inventory"], 10)
        self.assertEqual(response.data["daily_fee"], "3.00")

    def test_delete_book_requires_admin(self):
        response = self.client.delete(self.detail_url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(Book.objects.filter(id=self.book.id).exists())

    def test_admin_can_delete_book(self):
        self.client.force_authenticate(user=self.admin)

        response = self.client.delete(self.detail_url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Book.objects.filter(id=self.book.id).exists())

    def test_create_book_with_invalid_cover(self):
        self.client.force_authenticate(user=self.admin)

        data = {
            "title": "1984",
            "author": "George Orwell",
            "cover": "INVALID",
            "inventory": 3,
            "daily_fee": "1.50",
        }

        response = self.client.post(self.list_url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_book_with_negative_daily_fee(self):
        self.client.force_authenticate(user=self.admin)

        data = {
            "title": "1984",
            "author": "George Orwell",
            "cover": Book.Cover.SOFT,
            "inventory": 3,
            "daily_fee": "-1.50",
        }

        response = self.client.post(self.list_url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_book_with_negative_inventory(self):
        self.client.force_authenticate(user=self.admin)

        data = {
            "title": "1984",
            "author": "George Orwell",
            "cover": Book.Cover.SOFT,
            "inventory": -1,
            "daily_fee": "1.50",
        }

        response = self.client.post(self.list_url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
