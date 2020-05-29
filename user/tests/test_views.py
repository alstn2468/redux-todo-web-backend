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
        Check login_view return JsonResponse with access_token
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

        self.assertIn("aud", decode_jwt(access_token).keys())
        self.assertEqual("test", decode_jwt(access_token)["aud"])

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

        self.assertEqual("Invalid form. Please fill it out again.", data)

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

        self.assertEqual("Invalid form. Please fill it out again.", data)

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

        self.assertEqual("Invalid form. Please fill it out again.", data)

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

        self.assertEqual("Invalid form. Please fill it out again.", data)

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

        self.assertEqual("Invalid form. Please fill it out again.", data)

    def test_login_view_except_post_method(self):
        """User application login_view another method test
        Check login_view return HttpResponseNotAllowed
        """
        response = self.client.get("/login")
        self.assertIsInstance(response, HttpResponseNotAllowed)
        self.assertEqual(HTTPStatus.METHOD_NOT_ALLOWED, response.status_code)

    def test_signup_view_post_method_success(self):
        """User application signup_view post method success test
        Check signup_view return JsonResponse with access_token
        """
        response = self.client.post(
            "/signup",
            data={
                "user": "test_user",
                "password": "testpwd2020@",
                "passwordConfirm": "testpwd2020@",
            },
            content_type="application/json",
        )
        self.assertIsInstance(response, JsonResponse)
        self.assertEqual(HTTPStatus.CREATED, response.status_code)

        json_response = response.json()

        self.assertIn("access_token", json_response.keys())

        access_token = json_response["access_token"]

        self.assertIn("aud", decode_jwt(access_token).keys())
        self.assertEqual("test_user", decode_jwt(access_token)["aud"])

    def test_signup_view_post_method_without_user(self):
        """User application signup_view post method without user test
        Check signup_view return JsonResponse with bad request response
        """
        response = self.client.post(
            "/signup",
            data={"password": "testpwd2020@", "passwordConfirm": "testpwd2020@"},
            content_type="application/json",
        )
        self.assertIsInstance(response, JsonResponse)
        self.assertEqual(HTTPStatus.BAD_REQUEST, response.status_code)

        json_response = response.json()

        self.assertIn("error", json_response.keys())
        self.assertEqual(
            "Invalid form. Please fill it out again.", json_response["error"]
        )

    def test_signup_view_post_method_without_password(self):
        """User application signup_view post method without password test
        Check signup_view return JsonResponse with bad request response
        """
        response = self.client.post(
            "/signup",
            data={"user": "test_user", "password": "testpwd2020@"},
            content_type="application/json",
        )
        self.assertIsInstance(response, JsonResponse)
        self.assertEqual(HTTPStatus.BAD_REQUEST, response.status_code)

        json_response = response.json()

        self.assertIn("error", json_response.keys())
        self.assertEqual(
            "Invalid form. Please fill it out again.", json_response["error"]
        )

    def test_signup_view_post_method_not_match_password(self):
        """User application signup_view post method didn't match password test
        Check signup_view return JsonResponse with bad request response
        """
        response = self.client.post(
            "/signup",
            data={
                "user": "test_user",
                "password": "testpwd2020@",
                "passwordConfirm": "testpwd2020",
            },
            content_type="application/json",
        )
        self.assertIsInstance(response, JsonResponse)
        self.assertEqual(HTTPStatus.BAD_REQUEST, response.status_code)

        json_response = response.json()

        self.assertIn("error", json_response.keys())
        self.assertEqual(
            "Invalid form. Please fill it out again.", json_response["error"]
        )

    def test_signup_view_post_method_invalid_password(self):
        """User application signup_view post method invalid password test
        Check signup_view return JsonResponse with bad request response
        """
        response = self.client.post(
            "/signup",
            data={"user": "test_user", "password": "1234", "passwordConfirm": "1234"},
            content_type="application/json",
        )
        self.assertIsInstance(response, JsonResponse)
        self.assertEqual(HTTPStatus.BAD_REQUEST, response.status_code)

        json_response = response.json()

        self.assertIn("error", json_response.keys())
        self.assertEqual(type(json_response["error"]), list)
        self.assertEqual(len(json_response["error"]), 3)

    def test_signup_view_post_method_duplicate_user(self):
        """User application signup_view post method duplicate user test
        Check signup_view return JsonResponse with bad request response
        """
        response = self.client.post(
            "/signup",
            data={
                "user": "test",
                "password": "fakepwd0128@",
                "passwordConfirm": "fakepwd0128@",
            },
            content_type="application/json",
        )
        self.assertIsInstance(response, JsonResponse)
        self.assertEqual(HTTPStatus.BAD_REQUEST, response.status_code)

        json_response = response.json()

        self.assertIn("error", json_response.keys())
        self.assertEqual(
            "Duplicate user name. Please use a different name.", json_response["error"]
        )

    def test_signup_view_except_post_method(self):
        """User application signup_view another method test
        Check signup_view return HttpResponseNotAllowed
        """
        response = self.client.get("/signup")
        self.assertIsInstance(response, HttpResponseNotAllowed)
        self.assertEqual(HTTPStatus.METHOD_NOT_ALLOWED, response.status_code)
