from django.test import TestCase
from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponseNotAllowed
from http import HTTPStatus
from unittest import mock
from todo.models import Todo
from user.views import generate_access_token


class TodoViewTest(TestCase):
    @classmethod
    def setUp(cls):
        """Run each test case in TodoViewTest
        Test User Object 1 Fields :
            id           : 1
            username     : test1
        Test User Object 2 Fields :
            id           : 2
            username     : test2

        Test Todo Object 1 ~ 5 Fields :
            id           : 1 ~ 5
            text         : Todo Text 1 ~ 5
            is_completed : False
            user         : test1

        Test Todo Object 2 Fields :
            id           : 6 ~ 10
            text         : Todo Text 6 ~ 10
            is_completed : True
            user         : test2
        """
        user1 = User.objects.create_user(username="test")
        user1.save()

        user2 = User.objects.create_user(username="test2")
        user2.save()

        for i in range(5):
            todo = Todo.objects.create(text=f"Todo Text {i + 1}", user=user1)
            todo.save()

            todo = Todo.objects.create(
                text=f"Todo Text {i + 6}", user=user2, is_completed=True
            )
            todo.save()

    def test_todo_view_get_success(self):
        """Todo application todo_view get method success test
        Check todo_view return JsonResponse with todo objects
        """
        user1 = User.objects.get(id=1)
        user1_access_token = generate_access_token(user1.username)

        response = self.client.get("/todo", HTTP_AUTHORIZATION=user1_access_token)

        self.assertIsInstance(response, JsonResponse)
        self.assertEqual(HTTPStatus.OK, response.status_code)

        json_response = response.json()

        self.assertIn("data", json_response.keys())

        data = json_response["data"]

        self.assertEqual(5, len(data))
        self.assertIn("id", data[0].keys())
        self.assertIn("isCompleted", data[0].keys())
        self.assertIn("text", data[0].keys())

    def test_todo_view_post_success(self):
        """Todo application todo_view post method success test
        Check todo_view return JsonResponse with created object
        """
        user1 = User.objects.get(id=1)
        user1_access_token = generate_access_token(user1.username)

        response = self.client.post(
            "/todo",
            data={"text": "Todo Text 11"},
            content_type="application/json",
            HTTP_AUTHORIZATION=user1_access_token,
        )

        self.assertIsInstance(response, JsonResponse)
        self.assertEqual(HTTPStatus.OK, response.status_code)

        json_response = response.json()

        self.assertIn("data", json_response.keys())
        self.assertEqual(
            {"id": 11, "text": "Todo Text 11", "isCompleted": False, "user": 1},
            json_response["data"],
        )

        todo = Todo.objects.get(text="Todo Text 11")

        self.assertIsNotNone(todo)
        self.assertEqual("Todo Text 11", todo.text)
        self.assertFalse(todo.is_completed)

    def test_todo_view_post_fail(self):
        """Todo application todo_view post method fail test
        Check todo_view return JsonResponse with error
        """
        user1 = User.objects.get(id=1)
        user1_access_token = generate_access_token(user1.username)

        response = self.client.post(
            "/todo",
            data={"no_text": "no_text"},
            content_type="application/json",
            HTTP_AUTHORIZATION=user1_access_token,
        )

        self.assertIsInstance(response, JsonResponse)
        self.assertEqual(HTTPStatus.INTERNAL_SERVER_ERROR, response.status_code)

        json_response = response.json()

        self.assertIn("error", json_response.keys())
        self.assertEqual(
            "An error has occurred. Please try again.", json_response["error"]
        )

    def test_todo_view_delete_success(self):
        """Todo application todo_view delete method success test
        Check todo_view return JsonResponse with error
        """
        user2 = User.objects.get(id=2)
        user2_access_token = generate_access_token(user2.username)

        response = self.client.delete("/todo", HTTP_AUTHORIZATION=user2_access_token)

        self.assertIsInstance(response, JsonResponse)
        self.assertEqual(HTTPStatus.NO_CONTENT, response.status_code)

        todos = user2.todo_set.all()

        self.assertEqual(0, len(todos))

    def test_todo_view_another_method(self):
        """Todo application todo_view another method test
        Check todo_view return return HttpResponseNotAllowed
        """
        user1 = User.objects.get(id=1)
        user1_access_token = generate_access_token(user1.username)

        response = self.client.put("/todo", HTTP_AUTHORIZATION=user1_access_token,)

        self.assertIsInstance(response, HttpResponseNotAllowed)
        self.assertEqual(HTTPStatus.METHOD_NOT_ALLOWED, response.status_code)

    def test_todo_detail_view_put_success(self):
        """Todo application todo_detail_view view put method success test
        Check todo_detail_view return JsonResponse with updated data
        """
        user1 = User.objects.get(id=1)
        user1_access_token = generate_access_token(user1.username)

        response = self.client.put(
            "/todo/1",
            data={"text": "Edit Text", "isCompleted": True},
            content_type="application/json",
            HTTP_AUTHORIZATION=user1_access_token,
        )

        self.assertIsInstance(response, JsonResponse)
        self.assertEqual(HTTPStatus.OK, response.status_code)

        json_response = response.json()

        self.assertIn("data", json_response.keys())
        self.assertEqual(
            {"id": 1, "text": "Edit Text", "isCompleted": True, "user": 1},
            json_response["data"],
        )

        todo = Todo.objects.get(id=1)

        self.assertIsNotNone(todo)
        self.assertEqual("Edit Text", todo.text)
        self.assertTrue(todo.is_completed)

    def test_todo_detail_view_put_fail(self):
        """Todo application todo_detail_view view put method fail test
        Check todo_detail_view return JsonResponse with error
        """
        user1 = User.objects.get(id=1)
        user1_access_token = generate_access_token(user1.username)

        response = self.client.put(
            "/todo/11",
            data={"text": "Edit Text", "isCompleted": True},
            content_type="application/json",
            HTTP_AUTHORIZATION=user1_access_token,
        )

        self.assertIsInstance(response, JsonResponse)
        self.assertEqual(HTTPStatus.INTERNAL_SERVER_ERROR, response.status_code)

        json_response = response.json()

        self.assertIn("error", json_response.keys())
        self.assertEqual(
            "An error has occurred. Please try again.", json_response["error"],
        )

    def test_todo_detail_view_delete_success(self):
        """Todo application todo_detail_view view delete method success test
        Check todo_detail_view return JsonResponse with success status
        """
        user1 = User.objects.get(id=1)
        user1_access_token = generate_access_token(user1.username)

        response = self.client.delete("/todo/1", HTTP_AUTHORIZATION=user1_access_token)

        self.assertIsInstance(response, JsonResponse)
        self.assertEqual(HTTPStatus.NO_CONTENT, response.status_code)

        with self.assertRaises(Todo.DoesNotExist):
            Todo.objects.get(id=1)

        todos = Todo.objects.all()
        self.assertEqual(9, len(todos))

    def test_todo_detail_view_delete_fail(self):
        """Todo application todo_detail_view view delete method fail test
        Check todo_detail_view return JsonResponse with error
        """
        user1 = User.objects.get(id=1)
        user1_access_token = generate_access_token(user1.username)

        response = self.client.delete("/todo/11", HTTP_AUTHORIZATION=user1_access_token)

        self.assertIsInstance(response, JsonResponse)
        self.assertEqual(HTTPStatus.INTERNAL_SERVER_ERROR, response.status_code)

        json_response = response.json()

        self.assertIn("error", json_response.keys())
        self.assertEqual(
            "An error has occurred. Please try again.", json_response["error"],
        )

    def test_todo_detail_view_another_method(self):
        """Todo application todo_detail_view another method test
        Check todo_detail_view return HttpResponseNotAllowed
        """
        user1 = User.objects.get(id=1)
        user1_access_token = generate_access_token(user1.username)

        response = self.client.get("/todo/1", HTTP_AUTHORIZATION=user1_access_token)

        self.assertIsInstance(response, HttpResponseNotAllowed)
        self.assertEqual(HTTPStatus.METHOD_NOT_ALLOWED, response.status_code)
