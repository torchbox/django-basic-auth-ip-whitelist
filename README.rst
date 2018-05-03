django-basic-auth-ip-whitelist
==============================

This simple package ships middleware that lets you to set basic auth and
IP whitelisting via settings.

Use case
--------

This package has been created in mind for staging and demo sites that
need to be completely hidden from the Internet behind a password or IP
range.

Requirements
------------

-  Django 1.11 or 2.0
-  Python 3.4, 3.5, 3.6

Installation
------------

The package is on
`PyPI <https://pypi.org/project/django-basic-auth-ip-whitelist/>`__.

.. code:: bash

    pip install django-basic-auth-ip-whitelist

Configuration
-------------

In your Django settings you can configure the following settings.

``BASIC_AUTH_LOGIN`` and ``BASIC_AUTH_PASSWORD``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Credentials that you want to use with your basic authentication.

``BASIC_AUTH_WHITELISTED_IP_NETWORKS``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Set a list of network ranges (strings) compatible with Python’s
`ipaddress.ip_network <https://docs.python.org/3.6/library/ipaddress.html#ipaddress.ip_network>`__
that you want to be able to access the website without authentication
from. It must be either a string with networks separated by comma or
Python iterable.

Example settings
~~~~~~~~~~~~~~~~

.. code:: python

    MIDDLEWARE += [
        'baipw.middleware.BasicAuthIPWhitelistMiddleware'
    ]
    BASIC_AUTH_LOGIN = 'somelogin'
    BASIC_AUTH_PASSWORD = 'greatpassword'
    BASIC_AUTH_WHITELISTED_IP_NETWORKS = [
        '192.168.0.0/28',
        '2001:db00::0/24',
    ]

Advanced customisation
----------------------

Getting IP
~~~~~~~~~~

If you want to have a custom behaviour when getting IP, you can create a
custom function that takes request as a parameter and specify path to it
in the ``BASIC_AUTH_GET_CLIENT_IP_FUNCTION`` settings, e.g.

.. code:: python

    BASIC_AUTH_GET_CLIENT_IP_FUNCTION = 'utils.ip.get_client_ip'

