from django.urls import path
from todo.views import get_post_todo_view

app_name = "todo"

urlpatterns = [path("todo", get_post_todo_view, name="todo_view")]
