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
        if request.path == "/signup" or request.path == "/login":
            # 회원 가입 시 토큰 생성 및 로그인
            # 로그인 시 토큰 생성
            pass

        else:
            # 나머지 토큰 검증
            pass

        response = self.get_response(request)

        return response
