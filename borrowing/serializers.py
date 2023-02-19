from django.core.exceptions import ValidationError
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
            "book",
            "user",
        )


class BorrowingDetailSerializer(ReadSerializer, BorrowingListSerializer):
    user = UserIdSerializer(many=False, read_only=True)
    book = ReadSerializer(many=False, read_only=True)

    class Meta:
        model = Borrowing
        fields = (
            "id",
            "borrow_date",
            "expected_return_date",
            "actual_return_date",
            "user",
            "book",
        )


class BorrowingCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrowing
        fields = (
            "borrow_date",
            "expected_return_date",
            "user",
            "book",
        )

    def get_count(self):
        request = self.context.get("request")
        user = request.user.id

        return user

    def validate(self, attrs):
        user = attrs["user"]
        request_user = self.get_count()

        if user.id != request_user:
            raise serializers.ValidationError(
                "You can not create borrowings for another users"
            )

        book = attrs["book"]
        if book.inventory == 0:
            raise serializers.ValidationError("Not enough books")

        book.inventory = book.inventory - 1
        book.save()

        return attrs


class BorrowingReturnSerializer(serializers.ModelSerializer):

    class Meta:
        model = Borrowing
        fields = ("actual_return_date",)

    def validate(self, attrs):
        if self.instance.actual_return_date:
            raise ValidationError("This book is already returned")
        return attrs
