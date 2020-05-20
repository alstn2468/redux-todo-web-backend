from django.urls import path
from todo.views import get_post_todo_view, put_delete_todo_view

app_name = "todo"

urlpatterns = [
    path("todo", get_post_todo_view, name="get_post_todo"),
    path("todo/<int:id>", put_delete_todo_view, name="put_delete_toto"),
]
