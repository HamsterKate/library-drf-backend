from datetime import date
from decimal import Decimal

from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase

from books.models import Book
from borrowings.models import Borrowing
from payments.models import Payment


User = get_user_model()


class PaymentAPITests(APITestCase):
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
            daily_fee=Decimal("2.50"),
        )
        self.book2 = Book.objects.create(
            title="Book Two",
            author="Author Two",
            cover=Book.Cover.SOFT,
            inventory=3,
            daily_fee=Decimal("3.00"),
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
            book=self.book2,
            user=self.user2,
        )

        self.payment1 = Payment.objects.create(
            status=Payment.Status.PENDING,
            type=Payment.Type.PAYMENT,
            borrowing=self.borrowing1,
            session_url="https://stripe.com/session/payment-1",
            session_id="session_payment_1",
            money_to_pay=Decimal("25.00"),
        )
        self.payment2 = Payment.objects.create(
            status=Payment.Status.PAID,
            type=Payment.Type.PAYMENT,
            borrowing=self.borrowing2,
            session_url="https://stripe.com/session/payment-2",
            session_id="session_payment_2",
            money_to_pay=Decimal("30.00"),
        )

        self.list_url = "/api/payments/"

    def test_list_requires_authentication(self):
        response = self.client.get(self.list_url)

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

    def test_list_returns_only_current_user_payments(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.get(self.list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["id"], self.payment1.id)
        self.assertEqual(
            response.data[0]["borrowing"],
            self.borrowing1.id,
        )

    def test_retrieve_own_payment(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.get(
            f"{self.list_url}{self.payment1.id}/"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], self.payment1.id)

    def test_user_cannot_retrieve_other_user_payment(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.get(
            f"{self.list_url}{self.payment2.id}/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
        )

    def test_staff_can_list_all_payments(self):
        self.client.force_authenticate(user=self.admin)

        response = self.client.get(self.list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertSetEqual(
            {item["id"] for item in response.data},
            {self.payment1.id, self.payment2.id},
        )

    def test_staff_can_retrieve_any_payment(self):
        self.client.force_authenticate(user=self.admin)

        response = self.client.get(
            f"{self.list_url}{self.payment2.id}/"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], self.payment2.id)

    def test_payment_response_contains_all_fields(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.get(
            f"{self.list_url}{self.payment1.id}/"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data,
            {
                "id": self.payment1.id,
                "status": Payment.Status.PENDING,
                "type": Payment.Type.PAYMENT,
                "borrowing": self.borrowing1.id,
                "session_url": "https://stripe.com/session/payment-1",
                "session_id": "session_payment_1",
                "money_to_pay": "25.00",
            },
        )

