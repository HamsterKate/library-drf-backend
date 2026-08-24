from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models

from books.models import Book


class Borrowing(models.Model):
    borrow_date = models.DateField()
    expected_return_date = models.DateField()
    actual_return_date = models.DateField(null=True, blank=True)

    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        related_name="borrowings",
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="borrowings",
    )

    def clean(self):
        if self.expected_return_date < self.borrow_date:
            raise ValidationError(
                "Expected return date cannot be earlier than borrow date."
            )

        if (
            self.actual_return_date
            and self.actual_return_date < self.borrow_date
        ):
            raise ValidationError(
                "Actual return date cannot be earlier than borrow date."
            )

    def __str__(self):
        return f"{self.user} - {self.book}"