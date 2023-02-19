from rest_framework import routers

from books.views import BooksViewSet

router = routers.DefaultRouter()
router.register("books", BooksViewSet, basename="books")

urlpatterns = router.urls

app_name = "books"
