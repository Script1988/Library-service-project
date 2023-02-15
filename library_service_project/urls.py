"""library_service_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/library/", include("books.urls", namespace="library")),
    path("api/users/", include("user.urls", namespace="users")),
    path("api/borrowings/", include("borrowing.urls", namespace="borrowings")),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/schema/swagger/",
         SpectacularSwaggerView.as_view(
             url_name="schema"), name="swagger"
         ),
    path("api/schema/redoc/",
         SpectacularRedocView.as_view(
             url_name="schema"), name="redoc"
         ),
]
