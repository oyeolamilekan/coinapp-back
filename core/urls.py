from django.urls import path

from .views import ReceiveWebhooks, CreateBillAPIView, ListAcceptedCryptoAPIView

urlpatterns = [
    path(
        "list_accepted_crypto/",
        ListAcceptedCryptoAPIView.as_view(),
        name="list_accepted_crypto",
    ),
    path(
        "webhook_reciever/",
        ReceiveWebhooks.as_view(),
        name="webhook_reciever",
    ),
    path(
        "create_deposit_address/",
        CreateBillAPIView.as_view(),
        name="create_deposit_address",
    ),
]
