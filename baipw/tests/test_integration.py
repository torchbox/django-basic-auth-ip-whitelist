import django
from django import test

SETTINGS = {}

if django.VERSION < (1, 10):
    SETTINGS['MIDDLEWARE_CLASSES'] = [
        'baipw.middleware.BasicAuthIPWhitelistMiddleware',
        'django.middleware.security.SecurityMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
    ]
else:
    SETTINGS['MIDDLEWARE'] = [
        'baipw.middleware.BasicAuthIPWhitelistMiddleware',
        'django.middleware.security.SecurityMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
    ]


@test.override_settings(**SETTINGS)
class TestIntegration(test.TestCase):
    def setUp(self):
        self.client = test.Client()

    def test_basic_auth_not_configured(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 403)

    @test.override_settings(
        BASIC_AUTH_LOGIN='test',
        BASIC_AUTH_PASSWORD='test2',
    )
    def test_basic_auth_configured(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 401)
