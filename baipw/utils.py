import base64

from django.conf import settings
from django.utils.crypto import constant_time_compare

from .exceptions import Unauthorized


def get_client_ip(request):
    """
    Get the client's IP address

    Note: This is the address connecting to Django, which is likely incorrect.
    """
    return request.META.get("REMOTE_ADDR")


def authorize(request, configured_username, configured_password):
    """
    Match authorization header present in the request against
    configured username and password.
    """
    authentication_header = request.headers.get("authorization")

    if authentication_header is None:
        raise Unauthorized("Missing Authorization header.")

    disable_consumption = getattr(
        settings,
        "BASIC_AUTH_DISABLE_CONSUMING_AUTHORIZATION_HEADER",
        False,
    )
    if not disable_consumption:
        # Delete "Authorization" header so other authentication
        # mechanisms do not try to use it.
        request.META.pop("HTTP_AUTHORIZATION")

        # request.headers is a cached property, so needs invalidating
        del request.headers

    configured_credentials = f"{configured_username}:{configured_password}"

    for authentication in authentication_header.split(","):
        authentication_tuple = authentication.split(" ", 1)
        if len(authentication_tuple) != 2:
            raise Unauthorized("Invalid Authorization header.")
        auth_method = authentication_tuple[0]
        auth = authentication_tuple[1]
        if "basic" != auth_method.lower():
            raise Unauthorized("Invalid Authorization header.")
        auth = base64.b64decode(auth.strip()).decode("utf-8")
        if constant_time_compare(auth, configured_credentials):
            return True

    raise Unauthorized("Basic authentication credentials are invalid.")
