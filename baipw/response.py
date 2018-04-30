from django.http import HttpResponse

AUTH_TEMPLATE = (
    '<title>Authentication Required</title><h1>Authentication required</h1>'
)


class HttpUnauthorizedResponse(HttpResponse):
    def __init__(self, content=AUTH_TEMPLATE, *args, **kwargs):
        kwargs.setdefault('content_type', 'text/html')
        kwargs.setdefault('status', 401)
        super().__init__(content, *args, **kwargs)
        self['WWW-Authenticate'] = 'Basic realm="restricted"'
