from django.http import JsonResponse
from todo.models import Todo


def todo_list(request):
    try:
        todos = Todo.objects.all()
        todos = todos.extra(select={"isCompleted": "is_completed"})
        data = {"data": list(todos.values("id", "text", "isCompleted"))}
        
    except Exception:
        data = {"error": "Can't get todo list."}

    return JsonResponse(data)
