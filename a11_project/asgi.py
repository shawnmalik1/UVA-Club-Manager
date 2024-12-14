"""
ASGI config for a11_project project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

#the asgi.py file was created for the live chat feature

import os
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
import a11_project.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'a11_project.settings')

application = get_asgi_application()

"""
asgi.py for live chat
application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "https": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            a11_project.routing.websocket_urlpatterns
        )
    ),
})"""
