from django.test import TestCase, override_settings

from baipw.response import HttpUnauthorizedResponse


class TestHttpUnauthorizedResponse(TestCase):
    def test_default_realm(self):
        response = HttpUnauthorizedResponse()
        self.assertEqual(response['WWW-Authenticate'], 'Basic')

    @override_settings(
        BASIC_AUTH_REALM='Custom realm'
    )
    def test_custom_realm(self):
        response = HttpUnauthorizedResponse()
        self.assertEqual(response['WWW-Authenticate'],
                         'Basic realm="Custom realm"')

    @override_settings(
        BASIC_AUTH_REALM='"Custom realm"'
    )
    def test_custom_realm_with_doublequotes(self):
        response = HttpUnauthorizedResponse()
        self.assertEqual(response['WWW-Authenticate'],
                         'Basic realm="\\"Custom realm\\""')
