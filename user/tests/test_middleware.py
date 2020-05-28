from django.test import TestCase
from json import loads
from http import HTTPStatus
from datetime import datetime, timedelta
from user.utils.jwt import encode_jwt
from django.contrib.auth.models import User
from django.http import JsonResponse
from user.middleware import JsonWebTokenMiddleWare

JWT = encode_jwt(
    {
        "iat": datetime.now().timestamp(),
        "exp": (datetime.now() + timedelta(days=7)).timestamp(),
        "user": "Jone Doe",
    }
).decode("utf-8")

JWT_WITHOUT_USER = encode_jwt(
    {
        "iat": datetime.now().timestamp(),
        "exp": (datetime.now() + timedelta(days=7)).timestamp(),
    }
).decode("utf-8")


class MockedRequest(object):
    def __init__(self, path, headers={}):
        self.path = path
        self.headers = headers


class JsonWebTokenMiddleWareTest(TestCase):
    def mocked_get_response(self, request):
        if request.path == "/signup" or request.path == "/login":
            return JsonResponse({"access_token": JWT}, status=HTTPStatus.OK)

        return JsonResponse({"data": "Test"}, status=HTTPStatus.OK)

    def setUp(self):
        """Run only once when running JsonWebTokenMiddleWareTest
        Create JsonWebTokenMiddleWare class with client.get get_response method
        Create user that username is Jone Doe
        """
        self.middleware = JsonWebTokenMiddleWare(self.mocked_get_response)
        User.objects.create_user(username="Jone Doe")

    def test_json_web_token_middleware_without_access_token(self):
        """JsonWebTokenMiddleWare without access token test
        Check middleware return unauthorized response with error
        """
        self.assertEqual("mocked_get_response", self.middleware.get_response.__name__)
        self.assertEqual("JsonWebTokenMiddleWare", self.middleware.__class__.__name__)

        response = self.middleware.__call__(MockedRequest("/todo"))
        self.assertIsInstance(response, JsonResponse)
        self.assertEqual(response.status_code, HTTPStatus.UNAUTHORIZED)

        response_content = loads(response.content)

        self.assertIn("error", response_content.keys())
        self.assertIn("Authorization Error", response_content["error"])

    def test_json_web_token_middleware_without_user(self):
        """JsonWebTokenMiddleWare without user test
        Check middleware return unauthorized response with error
        """
        self.assertEqual("mocked_get_response", self.middleware.get_response.__name__)
        self.assertEqual("JsonWebTokenMiddleWare", self.middleware.__class__.__name__)

        response = self.middleware.__call__(
            MockedRequest("/todo", {"Authorization": JWT_WITHOUT_USER})
        )
        self.assertIsInstance(response, JsonResponse)
        self.assertEqual(response.status_code, HTTPStatus.UNAUTHORIZED)

        response_content = loads(response.content)

        self.assertIn("error", response_content.keys())
        self.assertIn("Authorization Error", response_content["error"])

    def test_json_web_token_middleware_another_path(self):
        """JsonWebTokenMiddleWare excpt '/signup', '/login' path test
        Check middleware excute else block when path is '/todo'
        """
        self.assertEqual("mocked_get_response", self.middleware.get_response.__name__)
        self.assertEqual("JsonWebTokenMiddleWare", self.middleware.__class__.__name__)

        response = self.middleware.__call__(
            MockedRequest("/todo", {"Authorization": JWT})
        )
        self.assertIsInstance(response, JsonResponse)
        self.assertEqual(response.status_code, HTTPStatus.OK)

        response_content = loads(response.content)

        self.assertIn("data", response_content.keys())
        self.assertIn("Test", response_content["data"])

    def test_json_web_token_middleware_signup_path(self):
        """JsonWebTokenMiddleWare '/signup' path test
        Check middleware excute if block when path is '/signup'
        """
        self.assertEqual("mocked_get_response", self.middleware.get_response.__name__)
        self.assertEqual("JsonWebTokenMiddleWare", self.middleware.__class__.__name__)

        response = self.middleware.__call__(MockedRequest("/signup"))
        self.assertIsInstance(response, JsonResponse)
        self.assertEqual(response.status_code, HTTPStatus.OK)

        response_content = loads(response.content)

        self.assertIn("access_token", response_content.keys())
        self.assertIn(JWT, response_content["access_token"])

    def test_json_web_token_middleware_login_path(self):
        """JsonWebTokenMiddleWare '/login' path test
        Check middleware excute if block when path is '/login'
        """
        self.assertEqual("mocked_get_response", self.middleware.get_response.__name__)
        self.assertEqual("JsonWebTokenMiddleWare", self.middleware.__class__.__name__)

        response = self.middleware.__call__(MockedRequest("/login"))
        self.assertIsInstance(response, JsonResponse)
        self.assertEqual(response.status_code, HTTPStatus.OK)

        response_content = loads(response.content)

        self.assertIn("access_token", response_content.keys())
        self.assertIn(JWT, response_content["access_token"])
