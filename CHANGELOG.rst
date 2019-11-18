0.3.2 - In development
~~~~~~~~~~~~~~~~~~~~~~

* Add Django 3 support.

0.3.1 - 18 July 2019
~~~~~~~~~~~~~~~~~~~~

* Include HTML and textual files in the package.
* Delete "Authorization" header when it is used by the middleware (`#11 <https://gitlab.com/tmkn/django-basic-auth-ip-whitelist/issues/11>`_)
* Use CF-Connecting-IP HTTP header for checking the client's IP address.
* Add `BASIC_AUTH_WHITELISTED_PATHS` setting.

0.3a0 - 23rd September 2018
~~~~~~~~~~~~~~~~~~~~~~~~~~~

* Don't crash on wrong authorization header format (`!8 <https://gitlab.com/tmkn/django-basic-auth-ip-whitelist/merge_requests/8/>`_)
* Add support for old-fashioned MIDDLEWARE_CLASSES (`!7 <https://gitlab.com/tmkn/django-basic-auth-ip-whitelist/merge_requests/7/>`_)
* Add overall Django 1.8, 1.9, 1.10 and 1.11 support (`!9 <https://gitlab.com/tmkn/django-basic-auth-ip-whitelist/merge_requests/9/>`_)

0.2.1 - 20th July 2018
~~~~~~~~~~~~~~~~~~~~~~

* Use HttpRequest.get_host instead of HTTP_HOST

0.2 - 7th June 2018
~~~~~~~~~~~~~~~~~~~

* Add HTTP host header whitelist (``BASIC_AUTH_RESPONSE_TEMPLATE``) (`!2 <https://gitlab.com/tmkn/django-basic-auth-ip-whitelist/merge_requests/2>`_)
* Add the ``BASIC_AUTH_REALM`` setting (`!3 <https://gitlab.com/tmkn/django-basic-auth-ip-whitelist/merge_requests/3>`_)
* Add the ``BASIC_AUTH_RESPONSE_TEMPLATE`` setting (`!4 <https://gitlab.com/tmkn/django-basic-auth-ip-whitelist/merge_requests/4>`_)
* Add the ``BASIC_AUTH_RESPONSE_CLASS`` setting (`!5 <https://gitlab.com/tmkn/django-basic-auth-ip-whitelist/merge_requests/5>`_)
* Add an option to skip the middleware by setting ``_skip_basic_auth_ip_whitelist_middleware_check`` attribute on the request (`!6 <https://gitlab.com/tmkn/django-basic-auth-ip-whitelist/merge_requests/6>`_)


0.1 - Initial release
~~~~~~~~~~~~~~~~~~~~~
