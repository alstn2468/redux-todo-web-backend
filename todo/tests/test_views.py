from django.test import TestCase
from django.http import JsonResponse
from http import HTTPStatus
from unittest import mock
from todo.models import Todo


class TodoViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        """Run only once when running TodoViewTest
        Test Object 1 Fields :
            id           : 1
            text         : Todo Text 1
            is_completed : True

        Test Object 2 Fields :
            id           : 2
            text         : Todo Text 2
            is_completed : False (default)
        """
        Todo.objects.create(text="Todo Text 1", is_completed=True)
        Todo.objects.create(text="Todo Text 2")

    def test_get_post_todo_view_view_success(self):
        """Todo application get_post_todo_view get method success test
        Check get_post_todo_view return JsonResponse with todo objects
        """
        response = self.client.get("/todo")
        self.assertIsInstance(response, JsonResponse)
        self.assertEqual(HTTPStatus.OK, response.status_code)

        json_response = response.json()

        self.assertIn("data", json_response.keys())

        data = json_response["data"]

        self.assertEqual(2, len(data))
        self.assertIn("id", data[0].keys())
        self.assertIn("isCompleted", data[0].keys())
        self.assertIn("text", data[0].keys())

    def test_get_post_todo_view_view_fail(self):
        """Todo application get_post_todo_view get method fail test
        Check get_post_todo_view return JsonResponse with error
        """
        todos = Todo.objects

        with mock.patch.object(todos, "all", side_effect=Exception()):
            response = self.client.get("/todo")

            self.assertIsInstance(response, JsonResponse)
            self.assertEqual(HTTPStatus.INTERNAL_SERVER_ERROR, response.status_code)

            json_response = response.json()

            self.assertIn("error", json_response.keys())
            self.assertEqual(
                "An error has occurred. Please try again.", json_response["error"]
            )

    def test_get_post_todo_view_post_success(self):
        """Todo application get_post_todo_view post method success test
        Check get_post_todo_view return JsonResponse with created object
        """
        response = self.client.post("/todo", data={"text": "Todo Text 3"})
        self.assertIsInstance(response, JsonResponse)
        self.assertEqual(HTTPStatus.OK, response.status_code)

        json_response = response.json()

        self.assertIn("data", json_response.keys())
        self.assertEqual(
            '{"id": 3, "text": "Todo Text 3", "is_completed": false}',
            json_response["data"],
        )

        todo = Todo.objects.get(text="Todo Text 3")

        self.assertIsNotNone(todo)
        self.assertEqual("Todo Text 3", todo.text)
        self.assertFalse(todo.is_completed)

    def test_get_post_todo_view_post_fail(self):
        """Todo application get_post_todo_view post method fail test
        Check get_post_todo_view return JsonResponse with error
        """
        response = self.client.post("/todo")
        self.assertIsInstance(response, JsonResponse)
        self.assertEqual(HTTPStatus.INTERNAL_SERVER_ERROR, response.status_code)

        json_response = response.json()

        self.assertIn("error", json_response.keys())
        self.assertEqual(
            "An error has occurred. Please try again.", json_response["error"]
        )

    def test_get_post_todo_view_another_method(self):
        """Todo application get_post_todo_view another method test
        Check get_post_todo_view return JsonResponse with error
        """
        response = self.client.delete("/todo")
        self.assertIsInstance(response, JsonResponse)
        self.assertEqual(HTTPStatus.INTERNAL_SERVER_ERROR, response.status_code)

        json_response = response.json()

        self.assertIn("error", json_response.keys())
        self.assertEqual(
            "An error has occurred. Please try again.", json_response["error"]
        )

    def test_put_delete_todo_view_put_success(self):
        """Todo application put_delete_todo_view view put method test
        Check put_delete_todo_view return JsonResponse with updated data
        """
        response = self.client.put(
            "/todo/1", data='{"text": "Edit Text", "isCompleted": "true"}'
        )
        self.assertIsInstance(response, JsonResponse)
        self.assertEqual(HTTPStatus.OK, response.status_code)

        json_response = response.json()

        self.assertIn("data", json_response.keys())
        self.assertEqual(
            '{"id": 1, "text": "Edit Text", "is_completed": true}',
            json_response["data"],
        )

        todo = Todo.objects.get(id=1)

        self.assertIsNotNone(todo)
        self.assertEqual("Edit Text", todo.text)
        self.assertTrue(todo.is_completed)

    def test_put_delete_todo_view_delete_success(self):
        """Todo application put_delete_todo_view view delete method test
        Check put_delete_todo_view return JsonResponse with success status
        """
        response = self.client.delete("/todo/1")
        self.assertIsInstance(response, JsonResponse)
        self.assertEqual(HTTPStatus.OK, response.status_code)

        json_response = response.json()

        self.assertIn("data", json_response.keys())
        self.assertTrue(json_response["data"])

    def test_put_delete_todo_view_another_method(self):
        """Todo application put_delete_todo_view another method test
        Check put_delete_todo_view return JsonResponse with error
        """
        response = self.client.get("/todo/1")
        self.assertIsInstance(response, JsonResponse)
        self.assertEqual(HTTPStatus.INTERNAL_SERVER_ERROR, response.status_code)

        json_response = response.json()

        self.assertIn("error", json_response.keys())
        self.assertEqual(
            "An error has occurred. Please try again.", json_response["error"]
        )
