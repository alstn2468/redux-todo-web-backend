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
        response = self.get_response(request)

        return response
