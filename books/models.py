from django.db import models


class Books(models.Model):
    class CoverChoices(models.TextChoices):
        HARD = "Hard"
        SOFT = "Soft"

    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    cover = models.CharField(max_length=40, choices=CoverChoices.choices)
    inventory = models.PositiveIntegerField()
    daily_fee = models.DecimalField(max_digits=4, decimal_places=2)

    class Meta:
        verbose_name_plural = "books"

    def __str__(self):
        return self.title
