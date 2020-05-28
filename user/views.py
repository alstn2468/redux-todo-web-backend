from django.http import JsonResponse, HttpResponseNotAllowed
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from user.utils.jwt import encode_jwt, decode_jwt
from http import HTTPStatus


@csrf_exempt
def login_view(request):
    data = {}
    status = HTTPStatus.OK

    if request.method == "POST":
        data["access_token"] = "test"

    else:
        return HttpResponseNotAllowed(["POST"])

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
