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

    def list(self, request, *args, **kwargs):
        """List of all books in the library"""
        return super(BooksViewSet, self).list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        """Create a new book"""
        return super(BooksViewSet, self).create(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        """Get detailed book information by id"""
        return super(BooksViewSet, self).retrieve(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        """Update all information of the concrete book"""
        return super(BooksViewSet, self).update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        """Partial update of the book"""
        return super(BooksViewSet, self).partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        """Delete book by id"""
        return super(BooksViewSet, self).destroy(request, *args, **kwargs)
