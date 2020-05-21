from .base import *

DEBUG = False

ALLOWED_HOSTS = []

CORS_ORIGIN_WHITELIST = [
    "https://alstn2468.github.io/Redux_ToDo_Web/"
]
CORS_ALLOW_METHODS = ["GET", "POST", "PUT", "DELETE"]
CORS_ALLOW_CREDENTIALS = True

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
    }
}
