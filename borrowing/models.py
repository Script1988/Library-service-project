from django.db import models

from books.models import Books
from library_service_project import settings


class Borrowing(models.Model):
    borrow_date = models.DateField(auto_now_add=True)
    expected_return_date = models.DateField()
    actual_return_date = models.DateField(blank=True, null=True)
    book_id = models.ForeignKey(Books, on_delete=models.DO_NOTHING, related_name="book")
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, related_name="user")

    def __str__(self):
        return f"{self.book_id.title}"

