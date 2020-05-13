from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("", include("todo.urls", namespace="todo")),
    path("admin/", admin.site.urls),
]
