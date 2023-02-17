from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model

from user.models import Payment, User
from user.serializers import PaymentListSerializer, PaymentDetailSerializer

PAYMENT_API = reverse("users:payments-list")


def detail_url(borrowing_id):
    return reverse("users:payments-detail", args=[borrowing_id])


def sample_payment(**params):
    default = {
        "amount": 10.50,
    }
    default.update(**params)
    return Payment.objects.create(**default)


class UnauthenticatedPaymentApiTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()

    def test_login_required(self):
        result = self.client.get(PAYMENT_API)
        self.assertEqual(result.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedPaymentApi(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="test@test.com",
            password="testpass",
            is_staff=False,
        )
        self.client.force_authenticate(self.user)

    def test_payment_list(self):
        sample_payment(user=self.user)
        result = self.client.get(PAYMENT_API)
        payments = Payment.objects.all()
        serializer = PaymentListSerializer(payments, many=True)
        self.assertEqual(result.status_code, status.HTTP_200_OK)
        self.assertEqual(result.data, serializer.data)

    def test_retrieve_payment_detail(self):
        payment = sample_payment(user=self.user)
        url = detail_url(payment.id)
        result = self.client.get(url)

        serializer = PaymentDetailSerializer(payment)
        self.assertEqual(result.status_code, status.HTTP_200_OK)
        self.assertEqual(result.data, serializer.data)

    def test_only_user_payments_response(self):
        test_user = User(
            email="test2@test.com",
            password="1234test",
            is_staff=False,
        )
        test_user.save()
        user_payment = sample_payment(user=self.user)
        test_payment = sample_payment(user=test_user)
        result = self.client.get(PAYMENT_API)
        serializer = PaymentListSerializer(user_payment)
        serializer2 = PaymentListSerializer(test_payment)
        self.assertIn(serializer.data, result.data)
        self.assertNotIn(serializer2.data, result.data)


class AdminPaymentApiTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="admin@test.com",
            password="admin_test_pass",
            is_staff=True
        )
        self.client.force_authenticate(self.user)

    def test_all_users_payments_response(self):
        test_user = User(
            email="test@test.com",
            password="test1234",
            is_staff=False
        )
        test_user.save()
        admin_payment = sample_payment(user=self.user)
        user_payment = sample_payment(user=test_user)
        result = self.client.get(PAYMENT_API)
        serializer = PaymentListSerializer(admin_payment)
        serializer2 = PaymentListSerializer(user_payment)
        self.assertIn(serializer.data, result.data)
        self.assertIn(serializer2.data, result.data)

