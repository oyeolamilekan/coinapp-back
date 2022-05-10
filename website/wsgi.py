import os
import platform

from django.core.wsgi import get_wsgi_application

if platform.system() == "Linux":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "website.settings.prod")
else:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "website.settings.local")

application = get_wsgi_application()
