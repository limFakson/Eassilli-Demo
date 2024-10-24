"""
ASGI config for base project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from fastapi import FastAPI
from starlette.middleware.wsgi import WSGIMiddleware
from starlette.routing import Mount
from ..core import base, base_read


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "base.settings")

application = get_asgi_application()
