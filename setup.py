from setuptools import setup


setup(
    name='django-basic-auth-ip-whitelist',
    description=(
        'Hide your Django site behind basic authentication mechanism with IP '
        'whitelisting support.'
    ),
    version='0.1',
    license='BSD-2',
    packages=['baipw'],
    install_requires=[
        'Django>=1.11,<=2.1'
    ],
    author='Tomasz Knapik',
    author_email='tmkn@tmkn.uk',
    url='https://github.com/tm-kn/django-basic-auth-ip-whitelist',
    keywords=[
        'basic',
        'authentication',
        'auth',
        'ip',
        'whitelist',
        'whitelisting',
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Internet :: WWW/HTTP',
        'Framework :: Django',
        'Framework :: Django :: 1.11',
        'Framework :: Django :: 2.0',
    ]
)
