from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from books.models import Books
from books.permissions import IsAdminOrIfAuthenticatedReadOnly
from books.serializers import BooksSerializer, BooksListSerializer


class BooksViewSet(viewsets.ModelViewSet):
    queryset = Books.objects.all()
    serializer_class = BooksSerializer
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)

    def get_permissions(self):
        if self.request.method in ["GET", "RETRIEVE"]:
            return [AllowAny()]
        return super().get_permissions()

    def get_serializer_class(self):
        if self.action == "list":
            return BooksListSerializer

        return self.serializer_class
