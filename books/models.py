from django.db import models
from django.core.validators import MinValueValidator


class Book(models.Model):
    class Cover(models.TextChoices):
        HARD = "HARD"
        SOFT = "SOFT"

    title = models.CharField(max_length=200, blank=False)
    author = models.CharField(max_length=200, blank=False)
    cover = models.CharField(
        max_length=10,
        choices=Cover.choices,
    )
    inventory = models.PositiveIntegerField()
    daily_fee = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
    )

    class Meta:
        verbose_name = "Book"
        verbose_name_plural = "Books"
        ordering = ["title"]
