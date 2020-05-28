from django.test import TestCase
from django.urls import resolve
from user.views import login_view, signup_view, logout_view


class UserUrlTest(TestCase):
    def test_url_resolves_to_login_view(self):
        """User application '/login' pattern url test
        Check '/login' pattern resolved func is login_view
        """
        found = resolve("/login")
        self.assertEqual(found.func, login_view)

    def test_url_resolves_to_signup_view(self):
        """User application '/signup' pattern url test
        Check '/signup' pattern resolved func is signup_view
        """
        found = resolve("/signup")
        self.assertEqual(found.func, signup_view)

    def test_url_resolves_to_logout_view(self):
        """User application '/logout' pattern url test
        Check '/logout' pattern resolved func is logout_view
        """
        found = resolve("/logout")
        self.assertEqual(found.func, logout_view)
