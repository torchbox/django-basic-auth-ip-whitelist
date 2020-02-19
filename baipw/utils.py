import base64

from django.conf import settings

from .exceptions import Unauthorized


def get_client_ip(request):
    # IP retrieved from CloudFlare
    cf_connecting_ip = request.META.get('HTTP_CF_CONNECTING_IP')

    # Header usually set by proxies
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')

    # Header set by the connecting party, usually not the actual client making
    # the request, but a web server that the request goes through.
    remote_addr = request.META.get('REMOTE_ADDR')

    # Prioritise IPs from proxies.
    final_ip = (
        cf_connecting_ip or x_forwarded_for or remote_addr
    )

    # If no IP address was attached to the address, return nothing.
    if final_ip is None:
        return

    # If there is a list of IPs provided, use the last one (should be
    # the most recent one). This may not work on Google Cloud.
    return final_ip.split(',')[-1].strip()


def authorize(request, configured_username, configured_password):
    """
    Match authorization header present in the request against
    configured username and password.
    """
    # Use request.META instead of request.headers to make it
    # compatible with Django versions below 2.2.
    if 'HTTP_AUTHORIZATION' not in request.META:
        raise Unauthorized(
            '"HTTP_AUTHORIZATION" is not present in the request object.'
        )

    authentication = request.META['HTTP_AUTHORIZATION']

    disable_consumption = getattr(
        settings,
        'BASIC_AUTH_DISABLE_CONSUMING_AUTHORIZATION_HEADER',
        False,
    )
    if not disable_consumption:
        # Delete "Authorization" header so other authentication
        # mechanisms do not try to use it.
        request.META.pop('HTTP_AUTHORIZATION')

    authentication_tuple = authentication.split(' ', 1)
    if len(authentication_tuple) != 2:
        raise Unauthorized('Invalid format of the authorization header.')
    auth_method = authentication_tuple[0]
    auth = authentication_tuple[1]
    if 'basic' != auth_method.lower():
        raise Unauthorized('"Basic" is not an authorization method.')
    auth = base64.b64decode(auth.strip()).decode('utf-8')
    username, password = auth.split(':', 1)
    if username == configured_username and password == configured_password:
        return True
    raise Unauthorized('Basic authentication credentials are invalid.')
