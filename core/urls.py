from django.urls import path

from .views import ReceiveWebhooks

urlpatterns = [
    path("webhook_reciever/", ReceiveWebhooks.as_view(), name="webhook_reciever")
]