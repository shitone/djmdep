from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter, ChannelNameRouter
from apps.cimiss import routing as cimissrouting

application = ProtocolTypeRouter({
    'websocket': AuthMiddlewareStack(
        URLRouter(
            cimissrouting.websocket_urlpatterns
        )
    ),
    # "channel": ChannelNameRouter({
    #     "aws": cimiss.ws.,
    # }),
})
