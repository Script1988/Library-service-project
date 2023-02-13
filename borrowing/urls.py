from django.urls import path, include
from rest_framework import routers

from borrowing.views import BorrowingView

router = routers.DefaultRouter()
router.register("borrowings", BorrowingView, basename="borrowings")

urlpatterns = [path("", include(router.urls)), ]

app_name = "borrowings"
