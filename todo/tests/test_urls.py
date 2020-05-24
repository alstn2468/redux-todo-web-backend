from django.test import TestCase
from django.urls import resolve
from todo.views import todo_view, todo_detail_view


class TodoUrlTest(TestCase):
    def test_url_resolves_to_todo_view(self):
        """Todo application '/todo' pattern url test
        Check '/todo' pattern resolved func is todo_view
        """
        found = resolve("/todo")
        self.assertEqual(found.func, todo_view)

    def test_url_resolves_to_todo_detail_view(self):
        """Todo application '/todo/1' pattern url test
        Check '/todo' pattern resolved func is todo_detail_view
        """
        found = resolve("/todo/1")
        self.assertEqual(found.func, todo_detail_view)
