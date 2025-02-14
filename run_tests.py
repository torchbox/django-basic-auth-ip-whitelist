#!/usr/bin/env python

import os
import sys

import django
from django.core.management import execute_from_command_line

os.environ["DJANGO_SETTINGS_MODULE"] = "baipw.tests.settings"


def runtests():
    execute_from_command_line([sys.argv[0], "check"])
    # Makemigrations does not return proper error
    # code on Django < 1.10.
    if django.VERSION >= (1, 10):
        execute_from_command_line(
            [
                sys.argv[0],
                "makemigrations",
                "--noinput",
                "--check",
            ]
        )
    execute_from_command_line([sys.argv[0], "test"] + sys.argv[1:])


if __name__ == "__main__":
    runtests()
