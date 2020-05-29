from django.test import TestCase
from user.utils.jwt import decode_jwt, encode_jwt


class JsonWebTokenUtilTest(TestCase):
    def setUp(self):
        """Run only once when running JsonWebTokenUtilTest
        Initialize test data and test jwt
        """
        self.data = {"key": "value"}
        self.jwt = (
            "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9"
            + ".eyJrZXkiOiJ2YWx1ZSJ9"
            + ".CYiwVVQYrlTkyXh-0X_CXdFKxgHcg5j2fuJ4fruiXE8"
        )

    def test_encode_jwt(self):
        """encode_jwt method test
        Check encoded byte string is equal to self.jwt
        """
        jwt = encode_jwt(self.data)
        self.assertEqual(jwt, self.jwt)

    def test_decode_jwt(self):
        """decode_jwt method test
        Check decoded dict is equal to self.data
        """
        data = decode_jwt(self.jwt)
        self.assertEqual(self.data, data)
