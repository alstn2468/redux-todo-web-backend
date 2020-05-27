from django.test import TestCase
from http import HTTPStatus
from django.http import JsonResponse
from user.middleware import JsonWebTokenMiddleWare


class JsonWebTokenMiddleWareTest(TestCase):
    def setUp(self):
        """Run only once when running JsonWebTokenMiddleWareTest
        Create JsonWebTokenMiddleWare class with client.get get_response method
        """
        self.middleware = JsonWebTokenMiddleWare(self.client.get)

    def test_json_web_token_middleware(self):
        """JsonWebTokenMiddleWare creation test
        Check middleware's member and method equal to expected value
        """
        self.assertEqual(
            self.client.get.__name__, self.middleware.get_response.__name__
        )
        self.assertEqual("JsonWebTokenMiddleWare", self.middleware.__class__.__name__)

        response = self.middleware.__call__("/todo")
        self.assertIsInstance(response, JsonResponse)
        self.assertEqual(response.status_code, HTTPStatus.OK)
