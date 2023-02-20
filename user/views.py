from rest_framework import generics, mixins, viewsets
from rest_framework.permissions import IsAuthenticated

from user.models import Payment
from user.serializers import (
    UserSerializer,
    PaymentListSerializer,
    PaymentDetailSerializer
)


class CreateUserView(generics.CreateAPIView):
    serializer_class = UserSerializer


class ManageUserView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user


class PaymentView(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Payment.objects.select_related("user")
    serializer_class = PaymentListSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        queryset = self.queryset

        if self.request.user.is_staff is False:
            queryset = queryset.filter(user=self.request.user)

        return queryset

    def get_serializer_class(self):
        if self.action == "retrieve":
            return PaymentDetailSerializer

        return self.serializer_class

    # Created for documentation purpose
    def list(self, request, *args, **kwargs):
        """Get all payments of the current user"""
        return super(PaymentView, self).list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        """Create a new payment"""
        return super(PaymentView, self).create(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        """Get detailed payment information by id"""
        return super(PaymentView, self).retrieve(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        """Delete payment by id"""
        return super(PaymentView, self).destroy(request, *args, **kwargs)
