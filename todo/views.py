from django.http import JsonResponse
from todo.models import Todo


def todo_list(request):
    todos = Todo.objects.all()
    todos = todos.extra(select={"isCompleted": "is_completed"})
    data = {"data": list(todos.values("id", "text", "isCompleted"))}

    return JsonResponse(data)
