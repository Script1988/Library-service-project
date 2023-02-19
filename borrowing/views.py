from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import mixins, viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from borrowing.models import Borrowing
from borrowing.serializers import (
    BorrowingListSerializer,
    BorrowingDetailSerializer,
    BorrowingCreateSerializer,
    BorrowingReturnSerializer,
)


class BorrowingView(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Borrowing.objects.select_related("book", "user")
    serializer_class = BorrowingCreateSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        queryset = self.queryset

        if self.request.user.is_staff is False:
            queryset = queryset.filter(user=self.request.user)

        is_active = self.request.query_params.get("actual_return_date")
        user = self.request.query_params.get("user")

        if is_active:
            queryset = queryset.filter(actual_return_date=None)

        if user and self.request.user.is_staff:
            queryset = queryset.filter(user=int(user))

        return queryset

    def get_serializer_class(self):
        if self.action == "retrieve":
            return BorrowingDetailSerializer
        if self.action == "list":
            return BorrowingListSerializer
        if self.action == "return_borrowing":
            return BorrowingReturnSerializer

        return self.serializer_class

    @action(
        methods=["post"],
        detail=True,
        url_path="return",
        url_name="return_borrowing"
    )
    def return_borrowing(self, request, pk=None):

        """Endpoint for borrowing returning"""
        borrowing = self.get_object()
        book = borrowing.book
        serializer = self.get_serializer(borrowing, data=request.data)

        if serializer.is_valid():
            book.inventory += 1
            book.save()
            serializer.save()

            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                "actual_return_date",
                description="Shows all books, with None status",
                type={"type": "list", "items": {"type": "None"}},
            ),
            OpenApiParameter(
                "user",
                description="Shows all borrowings of the concrete user, "
                            "available only for admin",
                type={"type": "list", "items": {"type": "int"}},
            ),
        ]
    )
    # Created for documentation purpose
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
