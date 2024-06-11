import base64

from django.test import RequestFactory, TestCase

from baipw.exceptions import Unauthorized
from baipw.utils import authorize


class TestAuthorize(TestCase):
    def setUp(self):
        self.request = RequestFactory().get("/")

    def test_authorise_with_no_password(self):
        with self.assertRaises(Unauthorized) as e:
            authorize(self.request, "somelogin", "somepassword")
        self.assertEqual(
            str(e.exception),
            '"HTTP_AUTHORIZATION" is not present in the request object.',
        )

    def test_authorise_with_wrong_credentials(self):
        self.request.META["HTTP_AUTHORIZATION"] = "Basic {}".format(
            base64.b64encode("somelogin:somepassword".encode("utf-8")).decode("utf-8")
        )
        with self.assertRaises(Unauthorized) as e:
            authorize(self.request, "somelogin", "wrongpassword")
        self.assertEqual(
            str(e.exception), "Basic authentication credentials are invalid."
        )

    def test_authorise_with_correct_credentials(self):
        self.request.META["HTTP_AUTHORIZATION"] = "Basic {}".format(
            base64.b64encode("somelogin:correctpassword".encode("utf-8")).decode(
                "utf-8"
            )
        )
        self.assertTrue(authorize(self.request, "somelogin", "correctpassword"))

    def test_authorise_with_invalid_header(self):
        self.request.META["HTTP_AUTHORIZATION"] = "Basic"
        with self.assertRaises(Unauthorized) as e:
            authorize(self.request, "somelogin", "wrongpassword")
        self.assertEqual(
            str(e.exception), "Invalid format of the authorization header."
        )
