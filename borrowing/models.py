from django.contrib.auth.models import User
from django.db import models

from books.models import Books


class Borrowing(models.Model):
    borrow_date = models.DateField(auto_now_add=True)
    expected_return_date = models.DateField()
    actual_return_date = models.DateField(null=True, blank=True)
    book_id = models.OneToOneField(Books, on_delete=models.DO_NOTHING, related_name="book")
    user_id = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="user")
