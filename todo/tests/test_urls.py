from django.test import TestCase
from django.urls import resolve
from todo.views import get_post_todo_view


class TodoUrlTest(TestCase):
    def test_url_resolves_to_todo_list(self):
        """Todo application '/todo' pattern url test
        Check '/todo' pattern resolved func is todo_list
        """
        found = resolve("/todo")
        self.assertEqual(found.func, get_post_todo_view)
