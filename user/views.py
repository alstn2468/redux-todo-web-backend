from django.http import JsonResponse, HttpResponseNotAllowed
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from user.utils.jwt import encode_jwt, decode_jwt
from datetime import datetime, timedelta
from json import loads
from http import HTTPStatus


def generate_access_token(username):
    iat = datetime.now()
    exp = iat + timedelta(days=7)

    data = {"iat": iat.timestamp(), "exp": exp.timestamp(), "user": username}

    return encode_jwt(data)


@csrf_exempt
def login_view(request):
    data = {}
    status = HTTPStatus.OK

    try:
        if request.method == "POST":
            json_body = loads(request.body)

            username = json_body.get("user", None)
            password = json_body.get("password", None)

            if not username or not password:
                raise ValueError()

            user = User.objects.get(username=username)

            if not user.check_password(password):
                raise ValueError()

            data["access_token"] = generate_access_token(username)

        else:
            return HttpResponseNotAllowed(["POST"])

    except (ValueError, User.DoesNotExist):
        data["error"] = "An error has occurred. Please try again."
        status = HTTPStatus.BAD_REQUEST

    return JsonResponse(data, status=status)


@csrf_exempt
def signup_view(request):
    data = {}
    status = HTTPStatus.CREATED

    if request.method == "POST":
        data["access_token"] = "test"

    else:
        return HttpResponseNotAllowed(["POST"])

    return JsonResponse(data, status=status)


@csrf_exempt
def logout_view(request):
    data = {}
    status = HTTPStatus.NO_CONTENT

    if request.method == "POST":
        pass

    else:
        return HttpResponseNotAllowed(["POST"])

    return JsonResponse(data, status=status)
