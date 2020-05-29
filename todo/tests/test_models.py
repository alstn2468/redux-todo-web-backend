from django.test import TestCase
from unittest import mock
from pytz import utc
from datetime import datetime
from todo.models import Todo
from django.contrib.auth.models import User


class TodoModelTest(TestCase):
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
        user = User.objects.create_user(username="test")
        mocked = datetime(2020, 5, 19, 0, 0, 0, tzinfo=utc)

        with mock.patch("django.utils.timezone.now", mock.Mock(return_value=mocked)):
            Todo.objects.create(text="Todo Text 1", is_completed=True, user=user)
            Todo.objects.create(text="Todo Text 2", user=user)

    def test_todo_create_success(self):
        """Todo model creation success test
        Check objects field and instance's class name
        """
        todo = Todo.objects.get(id=1)

        self.assertEqual("Todo", todo.__class__.__name__)
        self.assertEqual("Todo Text 1", todo.text)
        self.assertTrue(todo.is_completed)

    def test_todo_create_default_is_completed(self):
        """Todo model default is_completed field test
        Check is_completed field's default value is False
        """
        todo = Todo.objects.get(id=2)

        self.assertFalse(todo.is_completed)

    def test_todo_time_stamp_created_at(self):
        """TimeStamp model created_at test
        Check Todo Text 1's created_at field equal mocked datetime (2020.05.19)
        """
        todo = Todo.objects.get(id=1)
        mocked = datetime(2020, 5, 19, 0, 0, 0, tzinfo=utc)
        self.assertEqual(todo.created_at, mocked)

    def test_todo_time_stamp_updated_at(self):
        """TimeStamp model updated_at test
        Check Todo Text 1's updated_at field equal mocked datetime (2020.05.19)
        """
        todo = Todo.objects.get(id=1)
        mocked = datetime(2020, 5, 20, 0, 0, 0, tzinfo=utc)

        with mock.patch("django.utils.timezone.now", mock.Mock(return_value=mocked)):
            todo.is_completed = not todo.is_completed
            todo.save()
            self.assertFalse(todo.is_completed)
            self.assertEqual(todo.updated_at, mocked)

    def test_todo_str_method(self):
        """Todo model str method test
        Check str method equal todo instance text field
        """
        todo = Todo.objects.get(id=1)
        self.assertEqual(str(todo), todo.text)
