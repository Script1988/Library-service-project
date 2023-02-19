from rest_framework import routers

from borrowing.views import BorrowingView

router = routers.DefaultRouter()
router.register("", BorrowingView, basename="borrowings")

urlpatterns = router.urls

app_name = "borrowings"
