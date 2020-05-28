from django.http import JsonResponse, HttpResponseNotAllowed
from django.views.decorators.csrf import csrf_exempt
from http import HTTPStatus
from json import loads
from django.forms.models import model_to_dict
from todo.models import Todo


@csrf_exempt
def todo_view(request):
    status = HTTPStatus.OK
    data = {}

    try:
        if request.method == "GET":
            todos = Todo.objects.order_by("-created_at", "-updated_at")
            todos = todos.extra(select={"isCompleted": "is_completed"})
            data["data"] = list(todos.values("id", "text", "isCompleted"))

        elif request.method == "POST":
            json_body = loads(request.body)
            text = json_body.get("text", None)

            if not text:
                raise Exception()

            todo = Todo.objects.create(text=text)

            todo = model_to_dict(todo)
            todo["isCompleted"] = todo.pop("is_completed")

            data["data"] = todo

        elif request.method == "DELETE":
            Todo.objects.filter(is_completed=True).delete()
            status = HTTPStatus.NO_CONTENT

        else:
            return HttpResponseNotAllowed(["GET", "POST", "DELETE"])

    except Exception:
        data["error"] = "An error has occurred. Please try again."
        status = HTTPStatus.INTERNAL_SERVER_ERROR

    return JsonResponse(data, status=status)


@csrf_exempt
def todo_detail_view(request, id):
    status = HTTPStatus.OK
    data = {}

    try:
        if request.method == "PUT":
            json_body = loads(request.body)

            if "isCompleted" in json_body:
                json_body["isCompleted"] = bool(json_body["isCompleted"])
                json_body["is_completed"] = json_body.pop("isCompleted")

            todo = Todo.objects.get(id=id)

            for key in json_body:
                setattr(todo, key, json_body[key])

            todo.save()

            todo = model_to_dict(todo)
            todo["isCompleted"] = todo.pop("is_completed")
            data["data"] = todo

        elif request.method == "DELETE":
            todo = Todo.objects.get(id=id)
            todo.delete()

            status = HTTPStatus.NO_CONTENT

        else:
            return HttpResponseNotAllowed(["PUT", "DELETE"])

    except Exception:
        data["error"] = "An error has occurred. Please try again."
        status = HTTPStatus.INTERNAL_SERVER_ERROR

    return JsonResponse(data, status=status)
