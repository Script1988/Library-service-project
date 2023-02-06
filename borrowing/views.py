from rest_framework import mixins, viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from books.models import Books
from books.permissions import IsAdminOrIfAuthenticatedReadOnly
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
    queryset = Borrowing.objects.select_related("book_id", "user_id")
    serializer_class = BorrowingCreateSerializer
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)

    def get_serializer_class(self):
        if self.action == "retrieve":
            return BorrowingDetailSerializer
        if self.action == "list":
            return BorrowingListSerializer
        if self.action == "return_borrowing":
            return BorrowingReturnSerializer

        return self.serializer_class

    @action(methods=["post"], detail=True, url_path="return", url_name="return_borrowing")
    def return_borrowing(self, request, pk=None):

        """Endpoint for borrowing returning"""
        borrowing = self.get_object()
        book = borrowing.book_id

        serializer = self.get_serializer(borrowing, data=request.data)

        if serializer.is_valid():
            if borrowing.actual_return_date:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            book.inventory += 1
            book.save()

            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
