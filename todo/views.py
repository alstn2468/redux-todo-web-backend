from django.http import JsonResponse
from http import HTTPStatus
from todo.models import Todo


def get_post_todo_view(request):
    status = HTTPStatus.OK
    data = {}

    try:
        if request.method == "GET":
            todos = Todo.objects.all()
            todos = todos.extra(select={"isCompleted": "is_completed"})
            data = {"data": list(todos.values("id", "text", "isCompleted"))}

        elif request.method == "POST":
            pass

        else:
            raise Exception()

    except Exception:
        data = {"error": "An error has occurred. Please try again."}
        status = HTTPStatus.INTERNAL_SERVER_ERROR

    return JsonResponse(data, status=status)
