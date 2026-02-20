# import os
# from channels.routing import ProtocolTypeRouter, URLRouter
# from channels.auth import AuthMiddlewareStack
# from django.core.asgi import get_asgi_application
# import communication.routing

# # os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chat_app.settings')
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chat.settings')

# application = ProtocolTypeRouter({
#     "http": get_asgi_application(),
#     "websocket": AuthMiddlewareStack(
#         URLRouter(communication.routing.websocket_urlpatterns)
#     ),
# })


import os

# ✅ THIS MUST COME FIRST
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chat.settings')

import django
django.setup()

from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.core.asgi import get_asgi_application
import communication.routing

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            communication.routing.websocket_urlpatterns
        )
    ),
})