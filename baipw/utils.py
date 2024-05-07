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
    # Use request.META instead of request.headers to make it
    # compatible with Django versions below 2.2.
    if "HTTP_AUTHORIZATION" not in request.META:
        raise Unauthorized('"HTTP_AUTHORIZATION" is not present in the request object.')

    authentication = request.META["HTTP_AUTHORIZATION"]

    disable_consumption = getattr(
        settings,
        "BASIC_AUTH_DISABLE_CONSUMING_AUTHORIZATION_HEADER",
        False,
    )
    if not disable_consumption:
        # Delete "Authorization" header so other authentication
        # mechanisms do not try to use it.
        request.META.pop("HTTP_AUTHORIZATION")

    authentication_tuple = authentication.split(" ", 1)
    if len(authentication_tuple) != 2:
        raise Unauthorized("Invalid format of the authorization header.")
    auth_method = authentication_tuple[0]
    auth = authentication_tuple[1]
    if "basic" != auth_method.lower():
        raise Unauthorized('"Basic" is not an authorization method.')
    auth = base64.b64decode(auth.strip()).decode("utf-8")
    username, password = auth.split(":", 1)
    username_valid = constant_time_compare(username, configured_username)
    password_valid = constant_time_compare(password, configured_password)
    if username_valid & password_valid:
        return True
    raise Unauthorized("Basic authentication credentials are invalid.")
