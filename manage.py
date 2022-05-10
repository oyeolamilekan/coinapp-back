import os
import sys

import platform

def main():
    """Run administrative tasks."""
    if platform.system() == "Linux":
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "website.settings.prod")
    else:
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "website.settings.local")
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
