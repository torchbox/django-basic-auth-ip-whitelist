from django.conf import settings
from django.http import HttpResponse
from django.template.loader import render_to_string

DEFAULT_AUTH_TEMPLATE = (
    '<title>Authentication Required</title><h1>Authentication required</h1>'
)


class HttpUnauthorizedResponse(HttpResponse):
    def __init__(self, content=None, request=None, *args, **kwargs):
        self._request = request
        self._content = content
        kwargs.setdefault('content_type', 'text/html')
        kwargs.setdefault('status', 401)
        super().__init__(self.get_response_content(), *args, **kwargs)
        self['WWW-Authenticate'] = self.get_www_authenticate_value()

    def get_www_authenticate_value(self):
        value = "Basic"
        realm = getattr(settings, 'BASIC_AUTH_REALM', '')
        if realm:
            realm = realm.replace('"', '\\"')
            value += ' realm="{realm}"'.format(realm=realm)
        return value

    def get_response_content(self):
        if self._content:
            return self._content
        try:
            template = settings.BASIC_AUTH_RESPONSE_TEMPLATE
        except AttributeError:
            return DEFAULT_AUTH_TEMPLATE
        return render_to_string(template, {}, request=self._request)
