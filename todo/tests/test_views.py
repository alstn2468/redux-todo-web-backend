from django.test import TestCase
from todo.models import Todo


class TodoViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        """Run only once when running TodoModelTest
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

    def test_todo_list_view(self):
        response = self.client.get("/todo")
        json_response = response.json()

        self.assertIn("data", json_response.keys())

        data = json_response["data"]

        self.assertEqual(2, len(data))
        self.assertIn("id", data[0].keys())
        self.assertIn("isCompleted", data[0].keys())
        self.assertIn("text", data[0].keys())
