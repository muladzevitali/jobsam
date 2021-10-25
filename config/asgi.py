"""
ASGI config for config project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""

import os

import django
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter
from channels.routing import URLRouter
from channels.security.websocket import (AllowedHostsOriginValidator)
from django.core.asgi import get_asgi_application

import apps.chat.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

django.setup()

application = ProtocolTypeRouter(
    dict(
        http=get_asgi_application(),
        websocket=AllowedHostsOriginValidator(
            AuthMiddlewareStack(
                URLRouter(
                    apps.chat.routing.websocket_urlpatterns
                )
            )
        )
    )
)
