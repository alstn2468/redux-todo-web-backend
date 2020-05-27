class JsonWebTokenMiddleWare(object):
    """Custom JWT auth middleware
    Inherit :
        object
    Method :
        __init__ : Object constructor
        __call__ : Excuted by each request
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path != "/signup" or request.path != "/login":
            # Except signup and login
            # Verify request access token at headers
            headers = request.headers
            access_token = headers.get("access_token", None)

        response = self.get_response(request)

        # SignUp or Login
        # Create access token from request payload

        return response
