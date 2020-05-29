from django.test import TestCase
from django.http import JsonResponse, HttpResponseNotAllowed
from django.contrib.auth.models import User
from user.utils.jwt import decode_jwt
from http import HTTPStatus


class UserViewTest(TestCase):
    def setUp(self):
        """Run only once when running UserViewTest
        Test User Object Fields :
            id       : 1
            username : test
            password : 123456
        """
        User.objects.create_user(username="test", password="123456")

    def test_login_view_post_method_success(self):
        """User application login_view post method without user test
        Check login_view return JsonResponse with bad request error
        """
        response = self.client.post(
            "/login",
            data={"user": "test", "password": "123456"},
            content_type="application/json",
        )
        self.assertIsInstance(response, JsonResponse)
        self.assertEqual(HTTPStatus.OK, response.status_code)

        json_response = response.json()

        self.assertIn("access_token", json_response.keys())

        access_token = json_response["access_token"]

        self.assertIn("user", decode_jwt(access_token).keys())
        self.assertEqual("test", decode_jwt(access_token)["user"])

    def test_login_view_post_method_nonexist_user(self):
        """User application login_view post method nonexist user test
        Check login_view return JsonResponse with bad request error
        """
        response = self.client.post(
            "/login",
            data={"user": "test2", "password": "123456"},
            content_type="application/json",
        )
        self.assertIsInstance(response, JsonResponse)
        self.assertEqual(HTTPStatus.BAD_REQUEST, response.status_code)

        json_response = response.json()

        self.assertIn("error", json_response.keys())

        data = json_response["error"]

        self.assertEqual("An error has occurred. Please try again.", data)

    def test_login_view_post_method_wrong_password(self):
        """User application login_view post method wrong password test
        Check login_view return JsonResponse with bad request error
        """
        response = self.client.post(
            "/login",
            data={"user": "test", "password": "12345678"},
            content_type="application/json",
        )
        self.assertIsInstance(response, JsonResponse)
        self.assertEqual(HTTPStatus.BAD_REQUEST, response.status_code)

        json_response = response.json()

        self.assertIn("error", json_response.keys())

        data = json_response["error"]

        self.assertEqual("An error has occurred. Please try again.", data)

    def test_login_view_post_method_without_user(self):
        """User application login_view post method without user test
        Check login_view return JsonResponse with bad request error
        """
        response = self.client.post(
            "/login", data={"password": "123456"}, content_type="application/json"
        )
        self.assertIsInstance(response, JsonResponse)
        self.assertEqual(HTTPStatus.BAD_REQUEST, response.status_code)

        json_response = response.json()

        self.assertIn("error", json_response.keys())

        data = json_response["error"]

        self.assertEqual("An error has occurred. Please try again.", data)

    def test_login_view_post_method_without_password(self):
        """User application login_view post method without password test
        Check login_view return JsonResponse with bad request error
        """
        response = self.client.post(
            "/login", data={"user": "test"}, content_type="application/json"
        )
        self.assertIsInstance(response, JsonResponse)
        self.assertEqual(HTTPStatus.BAD_REQUEST, response.status_code)

        json_response = response.json()

        self.assertIn("error", json_response.keys())

        data = json_response["error"]

        self.assertEqual("An error has occurred. Please try again.", data)

    def test_login_view_post_method_witout_body(self):
        """User application login_view post method without body test
        Check login_view return JsonResponse with bad request error
        """
        response = self.client.post("/login")
        self.assertIsInstance(response, JsonResponse)
        self.assertEqual(HTTPStatus.BAD_REQUEST, response.status_code)

        json_response = response.json()

        self.assertIn("error", json_response.keys())

        data = json_response["error"]

        self.assertEqual("An error has occurred. Please try again.", data)

    def test_login_view_except_post_method(self):
        """User application login_view another method test
        Check login_view return HttpResponseNotAllowed
        """
        response = self.client.get("/login")
        self.assertIsInstance(response, HttpResponseNotAllowed)
        self.assertEqual(HTTPStatus.METHOD_NOT_ALLOWED, response.status_code)

    def test_signup_view(self):
        """User application signup_view post method test
        Check signup_view return JsonResponse with access_token
        """
        response = self.client.post("/signup")
        self.assertIsInstance(response, JsonResponse)
        self.assertEqual(HTTPStatus.CREATED, response.status_code)

        json_response = response.json()

        self.assertIn("access_token", json_response.keys())

        data = json_response["access_token"]

        self.assertEqual("test", data)

    def test_signup_view_except_post_method(self):
        """User application signup_view another method test
        Check signup_view return HttpResponseNotAllowed
        """
        response = self.client.get("/signup")
        self.assertIsInstance(response, HttpResponseNotAllowed)
        self.assertEqual(HTTPStatus.METHOD_NOT_ALLOWED, response.status_code)

    def test_logout_view(self):
        """User application logout_view post method test
        Check logout_view return NO_CONTENT JsonResponse
        """
        response = self.client.post("/logout")
        self.assertIsInstance(response, JsonResponse)
        self.assertEqual(HTTPStatus.NO_CONTENT, response.status_code)

    def test_logout_view_except_post_method(self):
        """User application logout_view another method test
        Check logout_view return HttpResponseNotAllowed
        """
        response = self.client.get("/logout")
        self.assertIsInstance(response, HttpResponseNotAllowed)
        self.assertEqual(HTTPStatus.METHOD_NOT_ALLOWED, response.status_code)
