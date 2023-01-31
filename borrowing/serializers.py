from rest_framework import serializers

from books.models import Books
from borrowing.models import Borrowing
from user.models import User


class ReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Books
        fields = ("id", "title", "author", "cover", "inventory", "daily_fee",)


class UserIdSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "first_name", "last_name", "username", "email")


class BorrowingListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Borrowing
        fields = (
            "id",
            "borrow_date",
            "expected_return_date",
            "actual_return_date",
            "book_id",
            "user_id",
        )


class BorrowingDetailSerializer(ReadSerializer, BorrowingListSerializer):
    user_id = UserIdSerializer(many=False, read_only=True)
    book_id = ReadSerializer(many=False, read_only=True)

    class Meta:
        model = Borrowing
        fields = (
            "id",
            "borrow_date",
            "expected_return_date",
            "actual_return_date",
            "user_id",
            "book_id",
        )
