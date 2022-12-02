from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
import chat.routing
from django.core.asgi import get_asgi_application
from channels.security.websocket import AllowedHostsOriginValidator



application = ProtocolTypeRouter({
    'websocket': AllowedHostsOriginValidator(
    	AuthMiddlewareStack(URLRouter(chat.routing.websocket_urlpatterns))
    ),
    "http": get_asgi_application(),
})

