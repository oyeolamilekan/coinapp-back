from django.urls import path

from .views import ReceiveWebhooks, CreateBillAPIView

urlpatterns = [
    path("webhook_reciever/", ReceiveWebhooks.as_view(), name="webhook_reciever"),
    path("create_deposit_address/", CreateBillAPIView.as_view(), name="create_deposit_address")
]