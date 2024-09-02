import os
from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.urls import re_path

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DatabaseChannel.settings')

# Initialize Django ASGI application
django_asgi_app = get_asgi_application()

# Import your consumers and middleware after initializing Django
from ChannelApp import consumers
from ChannelApp.middlewares import TokenAuthMiddleware

# Define the ASGI application with routing and middleware
application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": TokenAuthMiddleware(
        AllowedHostsOriginValidator(
            AuthMiddlewareStack(
                URLRouter([
                    re_path(r"^ws/chat/(?P<groupname>\w+)/$", consumers.ChatConsumer.as_asgi()),
                ])
            )
        )
    ),
})
