"""
WSGI config for clinic_api project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os, sys
from pathlib import Path

from django.core.wsgi import get_wsgi_application

sys.path.append(str(Path(__file__).resolve().parent.parent))


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "clinic_api.settings")

try:
    application = get_wsgi_application()
except:
    # fallback for vercel cold start
    from django.conf import settings

    settings.USE_TZ = True
    application = get_wsgi_application()
