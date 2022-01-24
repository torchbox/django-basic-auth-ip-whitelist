IN DEVELOPMENT
~~~~~~~~~~~~~~

* Make default response use "never cache" header.
* Add Django 4.0 support.

0.3.4 - 22nd June 2020
~~~~~~~~~~~~~~~~~~~~~~

* Fix potential timing attack if basic authentication is enabled (GHSA-m38j-pmg3-v5x5).

0.3.3 - 20th February 2020
~~~~~~~~~~~~~~~~~~~~~~~~~~

* Do not include tests in the package.

0.3.3a0 - 20th February 2020
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* Add `BASIC_AUTH_DISABLE_CONSUMING_AUTHORIZATION_HEADER` setting.

0.3.2a0 - 5th December 2019
~~~~~~~~~~~~~~~~~~~~~~~~~~~

* Add Django 3 support.

0.3.1 - 18th July 2019
~~~~~~~~~~~~~~~~~~~~~~

* Include HTML and textual files in the package.
* Delete "Authorization" header when it is used by the middleware.
* Use CF-Connecting-IP HTTP header for checking the client's IP address.
* Add `BASIC_AUTH_WHITELISTED_PATHS` setting.

0.3a0 - 23rd September 2018
~~~~~~~~~~~~~~~~~~~~~~~~~~~

* Don't crash on wrong authorization header format.
* Add support for old-fashioned MIDDLEWARE_CLASSES.
* Add overall Django 1.8, 1.9, 1.10 and 1.11 support.

0.2.1 - 20th July 2018
~~~~~~~~~~~~~~~~~~~~~~

* Use HttpRequest.get_host instead of HTTP_HOST.

0.2 - 7th June 2018
~~~~~~~~~~~~~~~~~~~

* Add HTTP host header whitelist (``BASIC_AUTH_RESPONSE_TEMPLATE``).
* Add the ``BASIC_AUTH_REALM`` setting.
* Add the ``BASIC_AUTH_RESPONSE_TEMPLATE`` setting.
* Add the ``BASIC_AUTH_RESPONSE_CLASS`` setting.
* Add an option to skip the middleware by setting ``_skip_basic_auth_ip_whitelist_middleware_check`` attribute on the request.


0.1 - Initial release
~~~~~~~~~~~~~~~~~~~~~
