from django.urls import path
from todo.views import todo_view, todo_detail_view

app_name = "todo"

urlpatterns = [
    path("todo", todo_view, name="get_post_todo"),
    path("todo/<int:id>", todo_detail_view, name="put_delete_toto"),
]
