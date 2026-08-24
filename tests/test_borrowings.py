from datetime import date

from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase

from books.models import Book
from borrowings.models import Borrowing


User = get_user_model()


class BorrowingAPITests(APITestCase):
    def setUp(self):
        self.admin = User.objects.create_user(
            email="admin@example.com",
            password="adminpass123",
            is_staff=True,
        )
        self.user = User.objects.create_user(
            email="user@example.com",
            password="userpass123",
        )
        self.user2 = User.objects.create_user(
            email="user2@example.com",
            password="user2pass123",
        )

        self.book1 = Book.objects.create(
            title="Book One",
            author="Author One",
            cover=Book.Cover.HARD,
            inventory=5,
            daily_fee=2.50,
        )
        self.book2 = Book.objects.create(
            title="Book Two",
            author="Author Two",
            cover=Book.Cover.SOFT,
            inventory=3,
            daily_fee=3.00,
        )

        self.borrowing1 = Borrowing.objects.create(
            borrow_date=date(2026, 8, 20),
            expected_return_date=date(2026, 8, 30),
            book=self.book1,
            user=self.user,
        )
        self.borrowing2 = Borrowing.objects.create(
            borrow_date=date(2026, 8, 21),
            expected_return_date=date(2026, 8, 31),
            actual_return_date=date(2026, 8, 29),
            book=self.book2,
            user=self.user2,
        )

        self.list_url = "/api/borrowings/"

    def test_list_requires_authentication(self):
        response = self.client.get(self.list_url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_returns_only_current_user_borrowings(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.get(self.list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["id"], self.borrowing1.id)
        self.assertEqual(response.data[0]["user"], self.user.id)

    def test_list_returns_detailed_book_information(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.get(self.list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        book_data = response.data[0]["book"]

        self.assertEqual(book_data["id"], self.book1.id)
        self.assertEqual(book_data["title"], "Book One")
        self.assertEqual(book_data["author"], "Author One")
        self.assertEqual(book_data["cover"], Book.Cover.HARD)
        self.assertEqual(book_data["inventory"], 5)
        self.assertEqual(book_data["daily_fee"], "2.50")

    def test_retrieve_own_borrowing(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.get(
            f"{self.list_url}{self.borrowing1.id}/"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], self.borrowing1.id)

    def test_user_cannot_retrieve_other_user_borrowing(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.get(
            f"{self.list_url}{self.borrowing2.id}/"
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_staff_can_list_all_borrowings(self):
        self.client.force_authenticate(user=self.admin)

        response = self.client.get(self.list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_staff_can_filter_borrowings_by_user(self):
        self.client.force_authenticate(user=self.admin)

        response = self.client.get(
            self.list_url,
            {"user_id": self.user.id},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["user"], self.user.id)

    def test_staff_can_retrieve_any_borrowing(self):
        self.client.force_authenticate(user=self.admin)

        response = self.client.get(
            f"{self.list_url}{self.borrowing2.id}/"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], self.borrowing2.id)

    def test_user_id_filter_does_not_affect_regular_user(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.get(
            self.list_url,
            {"user_id": self.user2.id},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["id"], self.borrowing1.id)
        self.assertEqual(response.data[0]["user"], self.user.id)

    def test_expected_return_date_cannot_be_before_borrow_date(self):
        borrowing = Borrowing(
            borrow_date=date(2026, 8, 30),
            expected_return_date=date(2026, 8, 20),
            book=self.book1,
            user=self.user,
        )

        with self.assertRaises(ValidationError):
            borrowing.full_clean()

    def test_actual_return_date_cannot_be_before_borrow_date(self):
        borrowing = Borrowing(
            borrow_date=date(2026, 8, 30),
            expected_return_date=date(2026, 9, 5),
            actual_return_date=date(2026, 8, 20),
            book=self.book1,
            user=self.user,
        )

        with self.assertRaises(ValidationError):
            borrowing.full_clean()