import base64

from django.test import RequestFactory, TestCase

from baipw.exceptions import Unauthorized
from baipw.utils import authorize, get_client_ip


class TestAuthorize(TestCase):
    def setUp(self):
        self.request = RequestFactory().get('/')

    def test_authorise_with_no_password(self):
        with self.assertRaises(Unauthorized) as e:
            authorize(self.request, 'somelogin', 'somepassword')
        self.assertEqual(
            str(e.exception),
            '"HTTP_AUTHORIZATION" is not present in the request object.'
        )

    def test_authorise_with_wrong_credentials(self):
        self.request.META['HTTP_AUTHORIZATION'] = 'Basic {}'.format(
            base64.b64encode(
                'somelogin:somepassword'.encode('utf-8')
            ).decode('utf-8')
        )
        with self.assertRaises(Unauthorized) as e:
            authorize(self.request, 'somelogin', 'wrongpassword')
        self.assertEqual(
            str(e.exception),
            'Basic authentication credentials are invalid.'
        )

    def test_authorise_with_correct_credentials(self):
        self.request.META['HTTP_AUTHORIZATION'] = 'Basic {}'.format(
            base64.b64encode(
                'somelogin:correctpassword'.encode('utf-8')
            ).decode('utf-8')
        )
        self.assertTrue(
            authorize(self.request, 'somelogin', 'correctpassword')
        )

    def test_authorise_with_invalid_header(self):
        self.request.META['HTTP_AUTHORIZATION'] = 'Basic'
        with self.assertRaises(Unauthorized) as e:
            authorize(self.request, 'somelogin', 'wrongpassword')
        self.assertEqual(
            str(e.exception),
            'Invalid format of the authorization header.'
        )


class TestGetClientIP(TestCase):
    def setUp(self):
        self.request = RequestFactory().get('/')

    def test_get_client_ip_from_remote_addr(self):
        self.request.META['REMOTE_ADDR'] = '192.168.0.17'
        self.assertNotIn('HTTP_X_FORWARDED_FOR', self.request.META)
        self.assertIn('REMOTE_ADDR', self.request.META)
        self.assertEqual(get_client_ip(self.request), '192.168.0.17')

    def test_get_client_ip_if_no_remote_addr_or_x_forwaded_for(self):
        del self.request.META['REMOTE_ADDR']
        self.assertNotIn('HTTP_X_FORWARDED_FOR', self.request.META)
        self.assertNotIn('REMOTE_ADDR', self.request.META)
        self.assertIsNone(get_client_ip(self.request))

    def test_get_client_ip_from_x_forwaded_for(self):
        self.request.META['HTTP_X_FORWARDED_FOR'] = '72.123.123.89'
        self.assertIn('HTTP_X_FORWARDED_FOR', self.request.META)
        self.assertIn('REMOTE_ADDR', self.request.META)
        self.assertEqual(get_client_ip(self.request), '72.123.123.89')

    def test_get_client_ip_from_x_forwaded_for_when_multiple_values(self):
        self.request.META['HTTP_X_FORWARDED_FOR'] = '72.123.123.89,5.123.2.45'
        self.assertIn('HTTP_X_FORWARDED_FOR', self.request.META)
        self.assertIn('REMOTE_ADDR', self.request.META)
        # Should use the last IP from the list.
        self.assertEqual(get_client_ip(self.request), '5.123.2.45')

    def test_get_client_ip_prioritises_cloudflare_ip(self):
        self.request.META['HTTP_CF_CONNECTING_IP'] = '72.123.123.90'
        self.request.META['HTTP_X_FORWARDED_FOR'] = '110.123.123.89'
        self.assertIn('REMOTE_ADDR', self.request.META)
        self.assertEqual(get_client_ip(self.request), '72.123.123.90')
