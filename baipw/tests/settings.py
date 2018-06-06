from os.path import abspath, dirname, join

from django.utils.crypto import get_random_string

TESTS_PATH = dirname(abspath(__file__))

SECRET_KEY = get_random_string(50)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'db.sqlite3',
    }
}

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            join(TESTS_PATH, 'templates'),
        ],
    },
]
