from django.http import JsonResponse
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from http import HTTPStatus


@csrf_exempt
def login_view(request):
    return JsonResponse({"test": "test"}, status=HTTPStatus.OK)


@csrf_exempt
def signup_view(request):
    return JsonResponse({"test": "test"}, status=HTTPStatus.OK)


@csrf_exempt
def logout_view(request):
    return JsonResponse({"test": "test"}, status=HTTPStatus.OK)
