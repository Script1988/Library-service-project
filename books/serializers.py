from rest_framework import serializers

from books.models import Books


class BooksSerializer(serializers.ModelSerializer):
    class Meta:
        model = Books
        fields = ("title", "author", "cover", "inventory", "daily_fee")


class BooksListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Books
        fields = ("title", "author", "inventory", "daily_fee")
