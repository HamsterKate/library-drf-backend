from datetime import date

from rest_framework import serializers

from borrowings.models import Borrowing
from books.serializers import BookSerializer


class BorrowingSerializer(serializers.ModelSerializer):
    book = BookSerializer(read_only=True)

    class Meta:
        model = Borrowing
        fields = (
            "id",
            "borrow_date",
            "expected_return_date",
            "actual_return_date",
            "book",
            "user",
        )


class BorrowingCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrowing
        fields = (
            "id",
            "book",
            "expected_return_date",
        )

    def validate_book(self, book):
        if book.inventory == 0:
            raise serializers.ValidationError(
                "Book is not available for borrowing."
            )

        return book

    def create(self, validated_data):
        book = validated_data["book"]
        user = self.context["request"].user

        borrowing = Borrowing.objects.create(
            user=user,
            borrow_date=date.today(),
            **validated_data,
        )

        book.inventory -= 1
        book.save(update_fields=["inventory"])

        return borrowing
