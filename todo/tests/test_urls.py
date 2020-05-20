from django.test import TestCase
from django.urls import resolve
from todo.views import get_post_todo_view, put_delete_todo_view


class TodoUrlTest(TestCase):
    def test_url_resolves_to_get_post_todo_view(self):
        """Todo application '/todo' pattern url test
        Check '/todo' pattern resolved func is get_post_todo_view
        """
        found = resolve("/todo")
        self.assertEqual(found.func, get_post_todo_view)

    def test_url_resolves_to_put_delete_todo_view(self):
        """Todo application '/todo/1' pattern url test
        Check '/todo' pattern resolved func is put_delete_todo_view
        """
        found = resolve("/todo/1")
        self.assertEqual(found.func, put_delete_todo_view)
