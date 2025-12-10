"""
ASGI config for welfare_watch project.
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'welfare_watch.settings')

application = get_asgi_application()

