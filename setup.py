from setuptools import setup


setup(
    name='django-basic-auth-ip-whitelist',
    description=(
        'Hide your Django site behind basic authentication mechanism with IP '
        'whitelisting support.'
    ),
    version='0.1a3',
    license='BSD-2',
    packages=['baipw'],
    install_requires=[
        'Django>=1.11,<=2.1'
    ],
    author='Tomasz Knapik',
    author_email='tmkn@tmkn.uk',
    url='https://github.com/tm-kn/django-basic-auth-ip-whitelist',
)
