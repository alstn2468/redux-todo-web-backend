from django.contrib import admin
from todo.models import Todo


@admin.register(Todo)
class TodoAdmin(admin.ModelAdmin):
    """Register model classes inherited from the AbstractItem model"""

    list_display = ("id", "user", "text", "is_completed", "created_at", "updated_at")
