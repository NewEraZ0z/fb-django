"""
ASGI config for yomamabot project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/asgi/
"""

# import os

# from django.core.asgi import get_asgi_application

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'yomamabot.settings')

# application = get_asgi_application()

import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import fb_yomamabot.routing  # replace 'chatapp' with the name of your Django app

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'yomamabot.settings')  # replace 'myproject' with the name of your Django project

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            fb_yomamabot.routing.websocket_urlpatterns  # replace 'chatapp' with the name of your Django app
        )
    ),
})
