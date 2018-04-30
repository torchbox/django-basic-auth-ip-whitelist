from django.core.exceptions import PermissionDenied


class Unauthorized(PermissionDenied):
    pass
