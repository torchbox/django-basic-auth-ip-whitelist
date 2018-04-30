from django.test import RequestFactory, TestCase

from baipw.utils import authorize  # noqa


class TestAuthorize(TestCase):
    def setUp(self):
        self.request = RequestFactory().get('/')
