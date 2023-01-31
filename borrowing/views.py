from rest_framework import generics, mixins, viewsets

from books.models import Books
from books.permissions import IsAdminOrIfAuthenticatedReadOnly
from borrowing.models import Borrowing
from borrowing.serializers import BorrowingListSerializer, BorrowingDetailSerializer, ReadSerializer


class BorrowingView(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Borrowing.objects.select_related("book_id", "user_id")
    serializer_class = BorrowingListSerializer
    # queryset = Books.objects.all()
    # serializer_class = ReadSerializer
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)

    def get_serializer_class(self):
        if self.action == "retrieve":
            return BorrowingDetailSerializer

        return self.serializer_class

