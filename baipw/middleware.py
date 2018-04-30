import ipaddress

from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.utils.module_loading import import_string

from .exceptions import Unauthorized
from .response import HttpUnauthorizedResponse
from .utils import authorize, get_client_ip


class BasicAuthIPWhitelistMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check if IP is whitelisted
        if self._is_ip_whitelisted(request):
            return self.get_response(request)
        # Fallback to basic auth if configured.
        if self._is_basic_auth_configured():
            return self._basic_auth_response(request)
        # Otherwise just deny the access to the website
        raise PermissionDenied

    @property
    def basic_auth_login(self):
        return getattr(settings, 'BASIC_AUTH_LOGIN', None)

    @property
    def basic_auth_password(self):
        return getattr(settings, 'BASIC_AUTH_PASSWORD', None)

    def _basic_auth_response(self, request):
        try:
            authorize(request, self.basic_auth_login, self.basic_auth_password)
        except Unauthorized:
            return HttpUnauthorizedResponse()
        return self.get_response(request)

    def _get_client_ip(self, request):
        function_path = getattr(
            settings, 'BASIC_AUTH_GET_CLIENT_IP_FUNCTION', None
        )
        func = get_client_ip
        if function_path is not None:
            func = import_string(function_path)
        return func(request)

    def _get_whitelisted_networks(self):
        networks = getattr(settings, 'BASIC_AUTH_WHITELISTED_IP_NETWORKS', [])
        # If we get a list, users probably passed a list of strings in
        #  the settings, probably from the environment.
        if isinstance(networks, str):
            networks = networks.split(',')
        # Otherwise assume that the list is iterable.
        for network in networks:
            network = network.strip()
            if not network:
                continue
            yield ipaddress.ip_network(network)

    def _is_ip_whitelisted(self, request):
        """
        Check if IP is on the whitelisted network.
        """
        ip_address = ipaddress.ip_address(self._get_client_ip(request))
        for network in self._get_whitelisted_networks():
            if ip_address in network:
                return True
        return False

    def _is_basic_auth_configured(self):
        """
        Check basic authentication username and password are
        configured.
        """
        return self.basic_auth_login and self.basic_auth_password
