from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status

from books.models import Books
from books.serializers import BooksListSerializer

BOOK_URL = reverse("books:books-list")


def sample_book(**params):
    default = {
        "title": "Test book",
        "author": "Test author",
        "cover": "Hard",
        "inventory": 3,
        "daily_fee": 2.50,
    }

    default.update(params)
    return Books.objects.create(**default)


class UnauthenticatedBookApiTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()

    def test_login_required(self):
        result = self.client.get(BOOK_URL)
        self.assertEqual(result.status_code, status.HTTP_200_OK)


class AuthenticatedBookApiTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="test@test.com",
            password="testpass",
        )
        self.client.force_authenticate(self.user)

    def test_create_book_forbidden(self):
        default = {
            "title": "Test book",
            "author": "Test author",
            "cover": "Hard",
            "inventory": 3,
            "daily_fee": 2.50,
        }
        result = self.client.post(BOOK_URL, default)
        self.assertEqual(result.status_code, status.HTTP_403_FORBIDDEN)

    def test_list_books(self):
        sample_book()
        sample_book()
        result = self.client.get(BOOK_URL)
        books = Books.objects.all()
        serializer = BooksListSerializer(books, many=True)
        self.assertEqual(result.status_code, status.HTTP_200_OK)
        self.assertEqual(result.data, serializer.data)


class AdminBooksApiTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="admin@admin.com",
            password="testpass",
            is_staff=True,
        )
        self.client.force_authenticate(self.user)

    def test_create_book_allowed(self):
        default = {
            "title": "Test book",
            "author": "Test author",
            "cover": "Hard",
            "inventory": 3,
            "daily_fee": 2.50,
        }
        result = self.client.post(BOOK_URL, default)
        self.assertEqual(result.status_code, status.HTTP_201_CREATED)
