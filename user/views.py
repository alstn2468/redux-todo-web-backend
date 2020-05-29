from django.http import JsonResponse, HttpResponseNotAllowed
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.password_validation import validate_password
from user.utils.jwt import encode_jwt
from datetime import datetime, timedelta
from json import loads
from http import HTTPStatus


def generate_access_token(username):
    iat = datetime.now()
    exp = iat + timedelta(days=7)

    data = {
        "iat": iat.timestamp(),
        "exp": exp.timestamp(),
        "aud": username,
        "iss": "Redux Todo Web Backend",
    }

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
            data["user"] = username

        else:
            return HttpResponseNotAllowed(["POST"])

    except (ValueError, User.DoesNotExist):
        # Login request validation exception
        data["error"] = "Invalid form. Please fill it out again."
        status = HTTPStatus.BAD_REQUEST

    return JsonResponse(data, status=status)


@csrf_exempt
def signup_view(request):
    data = {}
    status = HTTPStatus.CREATED

    try:
        if request.method == "POST":
            json_body = loads(request.body)

            username = json_body.get("user", None)
            password = json_body.get("password", None)
            password_confirm = json_body.get("passwordConfirm", None)

            if not username or not password or not password_confirm:
                raise ValueError()

            if password != password_confirm:
                raise ValueError()

            validate_password(password)

            user = User.objects.create_user(username=username)
            user.set_password(password)
            user.save()

            data["access_token"] = generate_access_token(user.username)
            data["user"] = username

        else:
            return HttpResponseNotAllowed(["POST"])

    except ValidationError as e:
        # Password validation exception
        data["error"] = e.messages
        status = HTTPStatus.BAD_REQUEST

    except IntegrityError:
        # Duplicate user name exception
        data["error"] = "Duplicate user name. Please use a different name."
        status = HTTPStatus.BAD_REQUEST

    except ValueError:
        # Invalid user request exception
        data["error"] = "Invalid form. Please fill it out again."
        status = HTTPStatus.BAD_REQUEST

    return JsonResponse(data, status=status)
