from django.http import JsonResponse
from http import HTTPStatus
from json import loads, dumps
from django.forms.models import model_to_dict
from todo.models import Todo


def get_post_todo_view(request):
    status = HTTPStatus.OK
    data = {}

    try:
        if request.method == "GET":
            todos = Todo.objects.all()
            todos = todos.extra(select={"isCompleted": "is_completed"})
            data["data"] = list(todos.values("id", "text", "isCompleted"))

        elif request.method == "POST":
            text = request.POST.get("text", None)

            if not text:
                raise Exception()

            todo = Todo.objects.create(text=text)

            data["data"] = dumps(model_to_dict(todo))

        else:
            raise Exception()

    except Exception:
        data["error"] = "An error has occurred. Please try again."
        status = HTTPStatus.INTERNAL_SERVER_ERROR

    return JsonResponse(data, status=status)


def put_delete_todo_view(request, id):
    status = HTTPStatus.OK
    data = {}

    return JsonResponse(data, status=status)
