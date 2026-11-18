from django import test


class TestIntegration(test.SimpleTestCase):
    def setUp(self):
        self.client = test.Client()

    def test_basic_auth_not_configured(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 401)

    @test.override_settings(
        BASIC_AUTH_LOGIN="test",
        BASIC_AUTH_PASSWORD="test2",
    )
    def test_basic_auth_configured(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 401)
