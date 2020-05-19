from django.urls import path
from todo.views import todo_list

app_name = "todo"

urlpatterns = [path("todo", todo_list, name="todo_list")]
