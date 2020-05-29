from django.urls import path
from user.views import login_view, signup_view

app_name = "user"

urlpatterns = [
    path("login", login_view, name="login_view"),
    path("signup", signup_view, name="signup_view"),
]
