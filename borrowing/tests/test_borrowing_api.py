from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from books.models import Books
from borrowing.models import Borrowing
from borrowing.serializers import (
    BorrowingListSerializer,
    BorrowingDetailSerializer,
)
from user.models import User

BORROWING_URL = reverse("borrowings:borrowings-list")


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


def sample_borrowing(**params):
    book = sample_book()
    default = {
        "borrow_date": "2023-02-07",
        "expected_return_date": "2023-02-17",
        "actual_return_date": None,
        "book": book,
    }
    default.update(params)
    return Borrowing.objects.create(**default)


def detail_url(borrowing_id):
    return reverse("borrowings:borrowings-detail", args=[borrowing_id])


class UnauthenticatedBorrowingApiTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()

    def test_login_required(self):
        result = self.client.get(BORROWING_URL)
        self.assertEqual(result.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedBorrowingApiTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="test@test.com",
            password="testpass",
            is_staff=False,
        )
        self.client.force_authenticate(self.user)

    def test_borrowings_list(self):
        sample_borrowing(user=self.user)
        result = self.client.get(BORROWING_URL)
        borrowings = Borrowing.objects.all()
        serializer = BorrowingListSerializer(borrowings, many=True)

        self.assertEqual(result.status_code, status.HTTP_200_OK)
        self.assertEqual(result.data, serializer.data)

    def test_retrieve_borrowing_detail(self):
        borrowing = sample_borrowing(user=self.user)
        url = detail_url(borrowing.id)
        result = self.client.get(url)

        serializer = BorrowingDetailSerializer(borrowing)
        self.assertEqual(result.status_code, status.HTTP_200_OK)
        self.assertEqual(result.data, serializer.data)

    def test_create_borrowing_with_valid_data(self):
        payload = {
            "borrow_date": "2023-02-07",
            "expected_return_date": "2023-02-17",
            "actual_return_date": "",
            "user": self.user.id,
            "book": sample_book().id,
        }

        result = self.client.post(BORROWING_URL, payload)
        self.assertEqual(result.status_code, status.HTTP_201_CREATED)
        book = Books.objects.get(pk=result.data["book"])
        self.assertEqual(book.inventory, 2)

    def test_create_borrowing_with_invalid_data(self):
        book = Books.objects.create(
            title="Test book",
            author="Test author",
            cover="Hard",
            inventory=0,
            daily_fee=2.50
        )
        payload = {
            "borrow_date": "2023-02-07",
            "expected_return_date": "2023-02-17",
            "actual_return_date": "",
            "user": self.user.id,
            "book": book.id,
        }
        result = self.client.post(BORROWING_URL, payload)
        self.assertNotEqual(result.status_code, status.HTTP_201_CREATED)
        self.assertEqual(book.inventory, 0)

    def test_return_borrowing_without_return_data(self):
        book = Books.objects.create(
            title="Test book",
            author="Test author",
            cover="Hard",
            inventory=0,
            daily_fee=2.50
        )
        borrowing = Borrowing.objects.create(
            borrow_date="2023-02-07",
            expected_return_date="2023-02-17",
            user=self.user,
            book=book,
        )

        payload = {
            "actual_return_date": "2023-02-27"
        }
        url = f"{BORROWING_URL}{borrowing.id}/return/"
        result = self.client.post(url, payload)
        self.assertEqual(result.status_code, status.HTTP_200_OK)

    def test_return_book_with_valid_return_data(self):
        borrowing = Borrowing.objects.create(
            borrow_date="2023-02-07",
            expected_return_date="2023-02-17",
            actual_return_date="2023-02-27",
            user=self.user,
            book=sample_book()
        )
        payload = {
            "actual_return_date": "2023-02-28"
        }
        url = f"{BORROWING_URL}{borrowing.id}/return/"
        result = self.client.post(url, payload)
        self.assertEqual(result.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(borrowing.book.inventory, 3)

    def test_filter_not_returned_borrowings(self):
        borrowing = Borrowing.objects.create(
            borrow_date="2023-02-07",
            expected_return_date="2023-02-17",
            user=self.user,
            book=sample_book()
        )
        borrowing2 = Borrowing.objects.create(
            borrow_date="2023-02-07",
            expected_return_date="2023-02-17",
            actual_return_date="2023-02-27",
            user=self.user,
            book=sample_book()
        )
        borrowing3 = Borrowing.objects.create(
            borrow_date="2023-02-07",
            expected_return_date="2023-02-17",
            actual_return_date="2023-02-22",
            user=self.user,
            book=sample_book()
        )

        result = self.client.get(f"{BORROWING_URL}?actual_return_date=none")
        serializer = BorrowingListSerializer(borrowing)
        serializer2 = BorrowingListSerializer(borrowing2)
        serializer3 = BorrowingListSerializer(borrowing3)
        self.assertIn(serializer.data, result.data)
        self.assertNotIn(serializer2.data, result.data)
        self.assertNotIn(serializer3.data, result.data)

    def test_user_id_filter_not_allowed_for_users(self):
        test_user = User(
            email="test2@test.com",
            password="test1234",
            is_staff=False
        )
        test_user.save()
        borrowing = Borrowing.objects.create(
            borrow_date="2023-12-07",
            expected_return_date="2023-12-17",
            user=test_user,
            book=sample_book()
        )

        result = self.client.get(f"{BORROWING_URL}?user={test_user.id}")
        serializer = BorrowingListSerializer(borrowing)
        self.assertNotIn(serializer.data, result.data)


class AdminBorrowingApiTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="admin@test.com",
            password="admin_test_pass",
            is_staff=True
        )
        self.client.force_authenticate(self.user)

    def test_filter_by_user_id(self):
        test_user = User(
            email="test@test.com",
            password="test1234",
            is_staff=False
        )
        test_user.save()
        borrowing = Borrowing.objects.create(
            borrow_date="2023-02-07",
            expected_return_date="2023-02-17",
            user=self.user,
            book=sample_book()
        )
        borrowing2 = Borrowing.objects.create(
            borrow_date="2023-02-07",
            expected_return_date="2023-02-17",
            actual_return_date="2023-02-27",
            user=self.user,
            book=sample_book()
        )
        borrowing3 = Borrowing.objects.create(
            borrow_date="2023-02-07",
            expected_return_date="2023-02-17",
            user=test_user,
            book=sample_book()
        )
        result = self.client.get(f"{BORROWING_URL}?user={self.user.id}")
        serializer = BorrowingListSerializer(borrowing)
        serializer2 = BorrowingListSerializer(borrowing2)
        serializer3 = BorrowingListSerializer(borrowing3)
        self.assertIn(serializer.data, result.data)
        self.assertIn(serializer2.data, result.data)
        self.assertNotIn(serializer3.data, result.data)
