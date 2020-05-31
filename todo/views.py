from django.http import JsonResponse, HttpResponseNotAllowed
from django.views.decorators.csrf import csrf_exempt
from django.forms.models import model_to_dict
from django.contrib.auth.models import User
from user.utils.jwt import decode_jwt
from todo.models import Todo
from http import HTTPStatus
from json import loads


def get_user_from_access_token(request):
    headers = request.headers
    access_token = headers.get("Authorization")
    payload = decode_jwt(access_token)

    return payload["aud"]


@csrf_exempt
def todo_view(request):
    status = HTTPStatus.OK
    data = {}

    try:
        username = get_user_from_access_token(request)
        user = User.objects.get(username=username)

        if request.method == "GET":
            todos = user.todo_set.order_by("-created_at", "-updated_at")
            todos = todos.extra(select={"isCompleted": "is_completed"})
            data["data"] = list(todos.values("id", "text", "isCompleted"))

        elif request.method == "POST":
            json_body = loads(request.body)
            text = json_body.get("text", None)

            if not text:
                raise Exception()

            todo = Todo.objects.create(text=text, user=user)

            todo = model_to_dict(todo)
            todo["isCompleted"] = todo.pop("is_completed")

            data["data"] = todo

        elif request.method == "DELETE":
            user.todo_set.filter(is_completed=True).delete()
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
        username = get_user_from_access_token(request)
        user = User.objects.get(username=username)

        if request.method == "PUT":
            json_body = loads(request.body)

            if "isCompleted" in json_body:
                json_body["isCompleted"] = bool(json_body["isCompleted"])
                json_body["is_completed"] = json_body.pop("isCompleted")

            todo = user.todo_set.get(id=id)

            for key in json_body:
                if key != "user":
                    setattr(todo, key, json_body[key])

            todo.save()

            todo = model_to_dict(todo)
            todo["isCompleted"] = todo.pop("is_completed")
            data["data"] = todo

        elif request.method == "DELETE":
            todo = user.todo_set.get(id=id)
            todo.delete()

            status = HTTPStatus.NO_CONTENT

        else:
            return HttpResponseNotAllowed(["PUT", "DELETE"])

    except Exception as e:
        print(e)
        data["error"] = "An error has occurred. Please try again."
        status = HTTPStatus.INTERNAL_SERVER_ERROR

    return JsonResponse(data, status=status)
