from django.urls import path
from .consumers import ChatConsumer

websocket_urlpatterns = [
    path("ws/users/<int:offer_id>/", ChatConsumer.as_asgi()),
]
