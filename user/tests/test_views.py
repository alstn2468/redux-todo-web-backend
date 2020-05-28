from django.test import TestCase
from django.http import JsonResponse, HttpResponseNotAllowed
from django.contrib.auth.models import User
from http import HTTPStatus


class UserViewTest(TestCase):
    def test_login_view(self):
        """User application login_view post method test
        Check login_view return JsonResponse with access_token
        """
        response = self.client.post("/login")
        self.assertIsInstance(response, JsonResponse)
        self.assertEqual(HTTPStatus.OK, response.status_code)

        json_response = response.json()

        self.assertIn("access_token", json_response.keys())

        data = json_response["access_token"]

        self.assertEqual("test", data)

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
