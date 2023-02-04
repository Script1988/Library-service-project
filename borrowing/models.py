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

    # def validate(self, number_of_books: int = 1):
    #     if self.book_id.inventory - number_of_books < 0:
    #         raise f"You can borrow only {number_of_books} book"
    #     self.book_id.inventory -= number_of_books
    #     self.save()
    #
    # def clean(self):
    #     Borrowing.validate()

