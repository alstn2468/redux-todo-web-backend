from django.test import TestCase
from django.http import JsonResponse
from django.contrib.auth.models import User
from http import HTTPStatus


class UserViewTest(TestCase):
    def test_login_view(self):
        response = self.client.get("/login")
        self.assertIsInstance(response, JsonResponse)
        self.assertEqual(HTTPStatus.OK, response.status_code)

        json_response = response.json()

        self.assertIn("test", json_response.keys())

        data = json_response["test"]

        self.assertEqual("test", data)

    def test_signup_view(self):
        response = self.client.get("/signup")
        self.assertIsInstance(response, JsonResponse)
        self.assertEqual(HTTPStatus.OK, response.status_code)

        json_response = response.json()

        self.assertIn("test", json_response.keys())

        data = json_response["test"]

        self.assertEqual("test", data)

    def test_logout_view(self):
        response = self.client.get("/logout")
        self.assertIsInstance(response, JsonResponse)
        self.assertEqual(HTTPStatus.OK, response.status_code)

        json_response = response.json()

        self.assertIn("test", json_response.keys())

        data = json_response["test"]

        self.assertEqual("test", data)
