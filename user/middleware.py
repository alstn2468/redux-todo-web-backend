from django.contrib.auth.models import User
import os
import jwt


class JsonWebTokenMiddleWare(object):
    """Custom JWT auth middleware
    Inherit :
        object
    Member :
        JWT_ALGORITHM : JWT encryption method
        SECRET_KEY    : JWT encryption key
    Method :
        __init__ : Object constructor
        __call__ : Excuted by each request
    """

    def __init__(self, get_response):
        self.get_response = get_response
        self.JWT_ALGORITHM = os.environ.get("JWT_ALGORITHM")
        self.SECRET_KEY = os.environ.get("SECRET_KEY")

    def __call__(self, request):
        if request.path != "/signup" or request.path != "/login":
            # Except signup and login
            headers = request.headers
            # Get Authorization header or None
            access_token = headers.get("Authorization", None)

            # If access_token is exist
            if access_token:
                # Decode JWT token
                payload = jwt.decode(
                    access_token, self.SECRET_KEY, algorithms=[self.JWT_ALGORITHM]
                )

                # Get user from decoded jwt payload
                username = payload.get("user", None)

                # If username is exist
                if username:
                    # Get user object using username
                    User.objects.get(username=username)

        response = self.get_response(request)

        # SignUp or Login
        # Create access token from request payload

        return response
