#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import dotenv
from pathlib import Path, PurePath


def get_environ():
    server_env = os.environ['SERVER_ENV']
    dotenv_name = f'.{server_env}.env'
    root_path = Path(__file__).parent.absolute()
    dotenv_path = PurePath(root_path, dotenv_name)
    dotenv.read_dotenv(dotenv_path)


def main():
    """Run administrative tasks."""
    get_environ()
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.base')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
