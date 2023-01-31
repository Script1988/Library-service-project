from rest_framework import mixins, viewsets

from books.permissions import IsAdminOrIfAuthenticatedReadOnly
from borrowing.models import Borrowing
from borrowing.serializers import BorrowingListSerializer, BorrowingDetailSerializer


class BorrowingView(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Borrowing.objects.select_related("book_id", "user_id")
    serializer_class = BorrowingListSerializer
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)

    def get_serializer_class(self):
        if self.action == "retrieve":
            return BorrowingDetailSerializer

        return self.serializer_class
