from unittest import mock
from unittest.mock import MagicMock

from django.core.exceptions import PermissionDenied
from django.test import RequestFactory, TestCase, override_settings

from baipw.middleware import BasicAuthIPWhitelistMiddleware
from baipw.response import HttpUnauthorizedResponse
from baipw.tests.response import TestResponse


class TestMiddleware(TestCase):
    def setUp(self):
        self.get_response_mock = MagicMock()
        self.middleware = BasicAuthIPWhitelistMiddleware(
            self.get_response_mock
        )
        self.request = RequestFactory().get('/')

    def test_no_settings_returns_permission_denied(self):
        with self.assertRaises(PermissionDenied):
            self.middleware(self.request)

    @override_settings(
        BASIC_AUTH_LOGIN='testlogin',
        BASIC_AUTH_PASSWORD='testpassword',
    )
    def test_basic_auth_returns_401(self):
        response = self.middleware(self.request)
        self.assertEqual(response.status_code, 401)

    @override_settings(
        BASIC_AUTH_LOGIN='testlogin',
    )
    def test_is_basic_auth_configured_if_only_login_set(self):
        self.assertFalse(self.middleware._is_basic_auth_configured())

    @override_settings(
        BASIC_AUTH_PASSWORD='testpassword',
    )
    def test_is_basic_auth_configured_if_only_password_set(self):
        self.assertFalse(self.middleware._is_basic_auth_configured())

    @override_settings(
        BASIC_AUTH_LOGIN='testlogin',
        BASIC_AUTH_PASSWORD='testpassword',
    )
    def test_is_basic_auth_configured_if_login_and_password_set(self):
        self.assertTrue(self.middleware._is_basic_auth_configured())

    def test_get_whitelisted_networks_when_none_set(self):
        networks = list(self.middleware._get_whitelisted_networks())
        self.assertEqual(len(networks), 0)

    @override_settings(
        BASIC_AUTH_WHITELISTED_IP_NETWORKS=[
            '192.168.0.0/24',
            '2001:db00::0/24',
        ]
    )
    def test_whitelisted_networks_when_set(self):
        networks = list(self.middleware._get_whitelisted_networks())
        self.assertEqual(len(networks), 2)

    @override_settings(
        BASIC_AUTH_WHITELISTED_IP_NETWORKS=[
            '192.168.0.0/24',
            '2001:db00::0/24',
        ]
    )
    def test_is_ip_whitelisted(self):
        self.request.META['REMOTE_ADDR'] = '192.168.0.25'
        self.assertTrue(self.middleware._is_ip_whitelisted(self.request))
        self.request.META['REMOTE_ADDR'] = '2001:db00::33'
        self.assertTrue(self.middleware._is_ip_whitelisted(self.request))

    @override_settings(
        BASIC_AUTH_WHITELISTED_IP_NETWORKS=[
            '192.168.0.0/24',
            '2001:db00::0/24',
        ]
    )
    def test_is_ip_whitelisted_invalid_ip(self):
        self.request.META['REMOTE_ADDR'] = '192.168.1.25'
        self.assertFalse(self.middleware._is_ip_whitelisted(self.request))
        self.request.META['REMOTE_ADDR'] = '2002:eb00::33'
        self.assertFalse(self.middleware._is_ip_whitelisted(self.request))

    @override_settings(
        BASIC_AUTH_LOGIN='randomlogin',
        BASIC_AUTH_PASSWORD='somepassword',
    )
    def test_basic_auth_credentials_settings(self):
        self.assertEqual(self.middleware.basic_auth_login, 'randomlogin')
        self.assertEqual(self.middleware.basic_auth_password, 'somepassword')

    @override_settings(
        BASIC_AUTH_LOGIN='somelogin',
        BASIC_AUTH_PASSWORD='somepassword',
        BASIC_AUTH_WHITELISTED_IP_NETWORKS=[
            '45.21.123.0/24',
        ]
    )
    def test_basic_auth_not_used_if_on_whitelisted_network(self):
        self.request.META['REMOTE_ADDR'] = '45.21.123.45'
        self.assertTrue(self.middleware._is_basic_auth_configured())
        with mock.patch(
            'baipw.middleware.BasicAuthIPWhitelistMiddleware.'
            '_basic_auth_response'
        ) as m:
            with mock.patch(
                'baipw.middleware.BasicAuthIPWhitelistMiddleware.'
                '_is_ip_whitelisted'
            ) as ip_check_m:
                self.middleware(self.request)
        # Make sure middleware did not try to evaluate basic auth.
        m.assert_not_called()
        # But it called the IP check.
        ip_check_m.assert_called_once_with(self.request)

    @override_settings(
        BASIC_AUTH_GET_CLIENT_IP_FUNCTION=(
            'baipw.tests.utils.custom_get_client_ip'
        ),
    )
    def test_get_custom_get_client_ip(self):
        with mock.patch('baipw.tests.utils.custom_get_client_ip') as m:
            with mock.patch('baipw.utils.get_client_ip') as default_m:
                self.middleware._get_client_ip(self.request)
        m.self_assert_called_once_with(self.request)
        default_m.assert_not_called()

    def test_whitelisted_http_host_setting_when_setting_not_set(self):
        self.assertFalse(list(self.middleware._get_whitelisted_http_hosts()))

    @override_settings(
        BASIC_AUTH_WHITELISTED_HTTP_HOSTS=['dgg.gg']
    )
    def test_whitelisted_http_host_setting_when_setting_set(self):
        self.assertEqual(
            list(self.middleware._get_whitelisted_http_hosts()),
            ['dgg.gg'],
        )

    @override_settings(
        BASIC_AUTH_WHITELISTED_HTTP_HOSTS=['dgg.gg', 'kernel.org']
    )
    def test_whitelisted_http_host_setting_when_setting_set_multiple(self):
        self.assertEqual(
            set(self.middleware._get_whitelisted_http_hosts()),
            {'kernel.org', 'dgg.gg'},
        )

    def test_http_host_whitelist_check_when_settings_empty(self):
        self.assertFalse(
            self.middleware._is_http_host_whitelisted(self.request)
        )

    @override_settings(
        ALLOWED_HOSTS=['kernel.org'],
        BASIC_AUTH_WHITELISTED_HTTP_HOSTS=['kernel.org', 'dgg.gg']
    )
    def test_http_host_whitelist_passes_check_when_configured_(self):
        self.request.META['HTTP_HOST'] = 'kernel.org'
        self.assertTrue(
            self.middleware._is_http_host_whitelisted(self.request)
        )

    @override_settings(
        ALLOWED_HOSTS=['google.com'],
        BASIC_AUTH_WHITELISTED_HTTP_HOSTS=['kernel.org', 'dgg.gg']
    )
    def test_http_host_whitelist_fails_check_when_configured_(self):
        self.request.META['HTTP_HOST'] = 'google.com'
        self.assertFalse(
            self.middleware._is_http_host_whitelisted(self.request)
        )

    @override_settings(
        BASIC_AUTH_WHITELISTED_HTTP_HOSTS=['kernel.org', 'dgg.gg']
    )
    def test_http_host_whitelist_fails_check_with_no_host(self):
        with self.assertRaises(PermissionDenied):
            self.middleware(self.request)

    @override_settings(
        ALLOWED_HOSTS=['www.example.com'],
        BASIC_AUTH_WHITELISTED_HTTP_HOSTS=['kernel.org', 'dgg.gg']
    )
    def test_http_host_whitelist_fails_check_with_wrong_host(self):
        self.request.META['HTTP_HOST'] = 'www.example.com'
        with self.assertRaises(PermissionDenied):
            self.middleware(self.request)

    @override_settings(
        BASIC_AUTH_LOGIN='somelogin',
        BASIC_AUTH_PASSWORD='somepassword',
        BASIC_AUTH_WHITELISTED_IP_NETWORKS=['45.21.123.0/24'],
        BASIC_AUTH_WHITELISTED_HTTP_HOSTS=['kernel.org', 'dgg.gg'],
        ALLOWED_HOSTS=['dgg.gg'],
    )
    def test_http_host_whitelist_has_precedence_over_basic_auth(self):
        self.request.META['HTTP_HOST'] = 'dgg.gg'
        # It does not raise.
        self.middleware(self.request)

    def test_get_response_class_when_none_set(self):
        self.assertIs(self.middleware.get_response_class(),
                      HttpUnauthorizedResponse)

    @override_settings(
        BASIC_AUTH_RESPONSE_CLASS='baipw.tests.response.TestResponse'
    )
    def test_get_response_class_when_set(self):
        self.assertIs(self.middleware.get_response_class(),
                      TestResponse)

    @override_settings(
        BASIC_AUTH_LOGIN='testlogin',
        BASIC_AUTH_PASSWORD='testpassword',
        BASIC_AUTH_RESPONSE_CLASS='baipw.tests.response.TestResponse'
    )
    def test_middleware_when_custom_response_set(self):
        response = self.middleware(self.request)
        self.assertIs(response.__class__, TestResponse)
        self.assertEqual(response.content, b'Test message. :P')

    @override_settings(
        BASIC_AUTH_LOGIN='test',
        BASIC_AUTH_PASSWORD='test',
    )
    def test_skip_basic_auth_ip_whitelist_middleware_check_attribute_set(self):
        self.assertFalse(
            hasattr(self.request,
                    '_skip_basic_auth_ip_whitelist_middleware_check')
        )
        self.middleware(self.request)
        self.assertTrue(
            self.request._skip_basic_auth_ip_whitelist_middleware_check
        )

    @override_settings(
        BASIC_AUTH_LOGIN='test',
        BASIC_AUTH_PASSWORD='test',
    )
    def test_the_attribute_skips(self):
        setattr(
            self.request,
            '_skip_basic_auth_ip_whitelist_middleware_check',
            True
        )
        self.middleware(self.request)
        self.get_response_mock.assert_called_once_with(self.request)
