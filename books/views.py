from rest_framework import viewsets, mixins

from books.permissions import IsAdminOrIfAuthenticatedReadOnly
from books.serializers import BooksSerializer


class BooksViewSet(viewsets.ModelViewSet):
    serializer_class = BooksSerializer
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)
