from django.conf import settings
from django.http import HttpResponse

AUTH_TEMPLATE = (
    '<title>Authentication Required</title><h1>Authentication required</h1>'
)


class HttpUnauthorizedResponse(HttpResponse):
    def __init__(self, content=AUTH_TEMPLATE, *args, **kwargs):
        kwargs.setdefault('content_type', 'text/html')
        kwargs.setdefault('status', 401)
        super().__init__(content, *args, **kwargs)
        self['WWW-Authenticate'] = self.get_www_authenticate_value()

    def get_www_authenticate_value(self):
        value = "Basic"
        realm = getattr(settings, 'BASIC_AUTH_REALM', '')
        if realm:
            realm = realm.replace('"', '\\"')
            value += ' realm="{realm}"'.format(realm=realm)
        return value
