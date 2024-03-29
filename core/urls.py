from django.urls import path

from .views import (
    ConfirmBillRechargeAPIView,
    CreateBillAPIView,
    ListAcceptedCryptoAPIView,
    ListBillsAPIView,
    ListNetworksAPIView,
    ReceiveWebhooks,
)

urlpatterns = [
    path(
        "list_networks/",
        ListNetworksAPIView.as_view(),
        name="list_networks",
    ),
    path(
        "list_bills/<slug:bill_type>/",
        ListBillsAPIView.as_view(),
        name="list_bills",
    ),
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
        "confirm_bill_recharge/<slug:reference>/",
        ConfirmBillRechargeAPIView.as_view(),
        name="confirm_bill_recharge",
    ),
    path(
        "create_deposit_address/",
        CreateBillAPIView.as_view(),
        name="create_deposit_address",
    ),
   
]
