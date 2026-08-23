from rest_framework.viewsets import ModelViewSet
from drf_spectacular.utils import extend_schema, extend_schema_view

from books.models import Book
from books.permissions import IsAdminOrReadOnly
from books.serializers import BookSerializer


@extend_schema_view(
    list=extend_schema(
        summary="List all books",
        description="Retrieve a list of all available books.",
    ),
    retrieve=extend_schema(
        summary="Retrieve a book",
        description="Retrieve details of a specific book.",
    ),
    create=extend_schema(
        summary="Create a book",
        description="Create a new book. Available to admin users only.",
    ),
    update=extend_schema(
        summary="Update a book",
        description="Update an existing book. Available to admin users only.",
    ),
    partial_update=extend_schema(
        summary="Partially update a book",
        description="Partially update an existing book. Available to admin users only.",
    ),
    destroy=extend_schema(
        summary="Delete a book",
        description="Delete an existing book. Available to admin users only.",
    ),
)
class BookViewSet(ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAdminOrReadOnly]
