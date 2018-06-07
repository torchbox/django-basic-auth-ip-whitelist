from django.http import HttpResponse


class TestResponse(HttpResponse):
    def __init__(self, *args, **kwargs):
        del kwargs['request']
        super().__init__('Test message. :P', *args, **kwargs)
