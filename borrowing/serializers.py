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


class BorrowingCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Borrowing
        fields = (
            "borrow_date",
            "expected_return_date",
            "user_id",
            "book_id",
        )

    def validate(self, attrs):
        book = attrs["book_id"]
        if book.inventory == 0:
            raise serializers.ValidationError("Not enough books")

        book.inventory = book.inventory - 1
        book.save()

        return attrs

    def create(self, validated_data):
        return Borrowing.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.borrow_date = validated_data.get("borrow_date", instance.borrow_date)
        instance.expected_return_date = validated_data.get("expected_return_date", instance.expected_return_date)
        instance.actual_return_date = validated_data.get("actual_return_date", instance.actual_return_date)
        instance.book_id = validated_data.get("book_id", instance.book_id)
        instance.user_id = validated_data.get("user_id", instance.user_id)
        instance.save()

        return instance


class BorrowingReturnSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrowing
        fields = (
            "borrow_date",
            "actual_return_date",
            "user_id",
            "book_id",
        )
