from django.contrib.auth.models import User
from django.http import JsonResponse
from django.core.exceptions import PermissionDenied
from user.utils.jwt import decode_jwt
from jwt.exceptions import ExpiredSignatureError
from http import HTTPStatus


class JsonWebTokenMiddleWare(object):
    """Custom JWT auth middleware
    Inherit :
        object
    Method :
        __init__ : Object constructor
        __call__ : Excuted by each request
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            if request.path != "/signup" and request.path != "/login":
                # Except signup and login
                headers = request.headers
                # Get Authorization header or None
                access_token = headers.get("Authorization", None)

                # If access_token isn't exist
                if not access_token:
                    raise PermissionDenied()

                # Decode JWT token
                payload = decode_jwt(access_token)

                # Get user from decoded jwt payload
                username = payload.get("user", None)

                # If username is None
                if not username:
                    raise PermissionDenied()

                # Get user object using username
                User.objects.get(username=username)

            response = self.get_response(request)

            return response

        except (PermissionDenied, User.DoesNotExist, ExpiredSignatureError):
            return JsonResponse(
                {"error": "Authorization Error"}, status=HTTPStatus.UNAUTHORIZED
            )
