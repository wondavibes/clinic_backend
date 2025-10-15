import os
import sys
from pathlib import Path

# Add your project directory to Python path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

# Set Django settings module
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "clinic_api.settings")

# Initialize Django
import django
from django.core.wsgi import get_wsgi_application

django.setup()

# Get WSGI application
application = get_wsgi_application()

# Vercel expects a WSGI callable named 'application'
# This imports your clinic_api/wsgi.py indirectly through Django's get_wsgi_application()
