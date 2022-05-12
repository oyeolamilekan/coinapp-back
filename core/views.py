from django.http import JsonResponse
from django.utils.crypto import get_random_string
from lib.flutterwave import bill
from lib.pusher import RealTimeService
from lib.quidax import quidax
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.conf import settings
import traceback

from core.models import (
    AcceptedCrypto,
    Bills,
    BillsRecharge,
    InstantOrderStatus,
    Network,
    Transaction,
    TransactionStatus,
)
from core.serializers import (
    AcceptedCryptoSerializer,
    BillsSerializer,
    NetworkSerializer,
)


class CreateBillAPIView(APIView):
    def post(self, request):
        try:
            destination_id = request.data.get("destination_id", None)
            bill_type = request.data.get("bill_type", None)
            transaction_receipt_email = request.data.get(
                "transaction_receipt_email", None
            )
            transaction_currency = request.data.get("transaction_currency", None)

            if not all(
                [
                    destination_id,
                    bill_type,
                    transaction_receipt_email,
                    transaction_currency,
                ]
            ):
                return Response(
                    data={
                        "message": "credentials not complete, kindly provide all the needed info."
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
            accepted_curreny_obj = AcceptedCrypto.objects.get(
                short_title=transaction_currency
            )

            current_price_ticker_obj = quidax.markets.fetch_market_ticker(
                accepted_curreny_obj.ticker
            )

            current_price = (
                current_price_ticker_obj.get("data").get("ticker").get("low")
            )

            generate_wallet_address_for_payment_obj = (
                quidax.wallets.create_payment_address_for_a_cryptocurrency(
                    "me", transaction_currency
                )
            )

            wallet_address_obj = quidax.wallets.get_payment_address_by_id(
                "me",
                transaction_currency,
                generate_wallet_address_for_payment_obj.get("data").get("id"),
            )

            wallet_address = wallet_address_obj.get("data").get("address")

            bills_obj = Bills.objects.get(slug=bill_type)

            estimated_amount = round(float(bills_obj.amount) / float(current_price), 5)

            reference_id = f"COIN-APP-{get_random_string(length=20)}"

            currency_obj = AcceptedCrypto.objects.get(short_title=transaction_currency)

            data = {
                "bills_type": bills_obj,
                "reference": reference_id,
                "recieving_id": destination_id,
                "transaction_receipt_email": transaction_receipt_email,
                "expected_amount": estimated_amount,
                "desposit_address": wallet_address,
                "related_currency": currency_obj,
            }

            bills_recharge = BillsRecharge.objects.create(**data)

            bills_recharge.save()

            return Response(
                data={
                    "status": "success",
                    "address": bills_recharge.desposit_address,
                    "blockchain": currency_obj.title,
                    "amount": bills_recharge.expected_amount,
                    "message": f"kindly deposit {bills_recharge.expected_amount} to {bills_recharge.desposit_address}.",
                    "reference_id": reference_id,
                },
                status=status.HTTP_200_OK,
            )

        except AcceptedCrypto.DoesNotExist:
            traceback.print_exc()
            return Response(
                data={"message": "Crypto does not exit."},
                status=status.HTTP_404_NOT_FOUND,
            )

        except:
            traceback.print_exc()
            return Response(
                data={"message": "Something bad happended"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class ListNetworksAPIView(APIView):
    def get(self, request):
        try:
            network_object = Network.objects.all()
            network_object_serialized_obj = NetworkSerializer(network_object, many=True)
            return Response(
                data=network_object_serialized_obj.data,
                status=status.HTTP_200_OK,
            )
        except:
            traceback.print_exc()
            return Response(
                data={"message": "error in fetching networks"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class ListBillsAPIView(APIView):
    def get(self, request, bill_type):
        try:
            bills_object = Bills.objects.filter(network__slug=bill_type).order_by(
                "amount"
            )
            bills_object_serialized_obj = BillsSerializer(bills_object, many=True)
            return Response(
                data=bills_object_serialized_obj.data,
                status=status.HTTP_200_OK,
            )
        except:
            traceback.print_exc()
            return Response(
                data={"message": "error in fetching networks"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class ListAcceptedCryptoAPIView(APIView):
    def get(self, request):
        try:

            accepted_crypto_object = AcceptedCrypto.objects.filter(is_live=True)
            accepted_crypto_serialized_obj = AcceptedCryptoSerializer(
                accepted_crypto_object, many=True
            )
            return Response(
                data=accepted_crypto_serialized_obj.data,
                status=status.HTTP_200_OK,
            )
        except:
            traceback.print_exc()
            return Response(
                data={"message": "error in fetching accepted cryptos"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class ReceiveWebhooks(APIView):
    def post(self, request):
        try:
            quidax_secret = request.META.get("HTTP_QUIDAX_SIGNATURE", None)

            if quidax_secret != settings.WEBHOOK_SECRET:
                return Response(
                    data={"message": "No be me you run street guy."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            realtime_service = RealTimeService()

            if request.data["event"] == "deposit.transaction.confirmation":

                wallet_address = (
                    request.data.get("data").get("payment_address").get("address")
                )

                bill_recharge_obj = BillsRecharge.objects.get(
                    desposit_address=wallet_address
                )

                realtime_service.push_event_to_frontend(
                    "coinapp",
                    "onRecieve",
                    {
                        "message": "crypto has been detected, and we are awaiting final confirmation.",
                        "reference_id": bill_recharge_obj.recieving_id,
                        "action": "PENDING",
                    },
                )

            if request.data["event"] == "instant_order.cancelled":
                instant_order_id = request.data.get("data").get("id")

                transaction_obj = Transaction.objects.get(
                    instant_order_id=instant_order_id
                )

                transaction_obj.instant_order_status = InstantOrderStatus.CANCELLED

                transaction_obj.save()

                return Response(
                    data={"message": "order cancelled"},
                    status=status.HTTP_200_OK,
                )

            if request.data["event"] == "instant_order.done":
                instant_order_id = request.data.get("data").get("id")

                transaction_obj = Transaction.objects.get(
                    instant_order_id=instant_order_id
                )

                transaction_obj.instant_order_status = InstantOrderStatus.DONE

                transaction_obj.save()

                return Response(
                    data={"message": "order done and successfully fufilled."},
                    status=status.HTTP_200_OK,
                )

            if request.data["event"] == "deposit.successful":
                recieved_amount = float(request.data.get("data").get("amount"))

                wallet_address = (
                    request.data.get("data").get("payment_address").get("address")
                )

                bill_recharge_obj = BillsRecharge.objects.get(
                    desposit_address=wallet_address
                )

                if recieved_amount < float(bill_recharge_obj.expected_amount):
                    realtime_service.push_event_to_frontend(
                        "coinapp",
                        "onRecieve",
                        {
                            "message": "amount rejected due it being less that expected amount.",
                            "reference_id": bill_recharge_obj.recieving_id,
                            "action": "REJECTED",
                        },
                    )
                    return Response(
                        data={
                            "message": "amount rejected due it being less that expected amount."
                        },
                        status=status.HTTP_200_OK,
                    )

                instant_order_object = quidax.instant_orders.create_instant_order(
                    "me",
                    bid="ngn",
                    ask=bill_recharge_obj.related_currency.short_title.lower(),
                    type="sell",
                    volume=float(bill_recharge_obj.expected_amount),
                    unit=bill_recharge_obj.related_currency.short_title.lower(),
                )

                instant_order_object_id = instant_order_object.get("data").get("id")

                confirm_instant_object = quidax.instant_orders.confirm_instant_orders(
                    "me",
                    instant_order_object_id,
                )

                bill_recharge_obj.is_paid = True

                bill_recharge_obj.save()

                total_amount = (
                    confirm_instant_object.get("data").get("receive").get("amount")
                )

                response = bill.buy_airtime(
                    bill_recharge_obj.recieving_id,
                    float(bill_recharge_obj.bills_type.amount),
                )

                bill_amount = float(bill_recharge_obj.bills_type.amount)

                buying_amount = bill_amount - (bill_amount * 0.03)

                data = {
                    "bill": bill_recharge_obj,
                    "recieve_amount": total_amount,
                    "buying_amount": buying_amount,
                    "instant_order_response": confirm_instant_object,
                    "bill_payment_response": response,
                    "instant_order_id": instant_order_object_id,
                    "bill_payment_status": TransactionStatus.SUCCESS,
                    "instant_order_status": InstantOrderStatus.CONFIRM,
                }

                if response.get("status") != "success":
                    realtime_service.push_event_to_frontend(
                        "coinapp",
                        "onRecieve",
                        {
                            "message": "Crypto recieved and liquidated, but partner account failed. would manually credit your account",
                            "action": "REJECTED",
                        },
                    )
                    data["reason"] = "airtime could not be released."
                    data["bill_payment_status"] = TransactionStatus.FAILED

                transaction_obj = Transaction.objects.create(**data)

                transaction_obj.save()

                realtime_service.push_event_to_frontend(
                    "coinapp",
                    "onRecieve",
                    {
                        "message": "Oshee, oba crypto, transaction has been successful.",
                        "action": "ACCEPTED",
                    },
                )

            return Response(
                data={"message": "successfully recieved payments."},
                status=status.HTTP_200_OK,
            )

        except:
            traceback.print_exc()
            return Response(
                data={"message": "error in processing"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class DispatchConfirmationRealTimeAPIView(APIView):
    def get(self, request):

        reference_id = f"COIN-APP-{get_random_string(length=20)}"

        realtime_service = RealTimeService()

        realtime_service.push_event_to_frontend(
            "coinapp",
            "onRecieve",
            {
                "message": "Oshee, oba crypto, you money don reach blockchain, we just confirm am.",
                "reference_id": reference_id,
                "action": "PENDING",
            },
        )
        return Response(
            data={"message": "Dispatched realtime"},
            status=status.HTTP_200_OK,
        )


class DispatchSuccessRealTimeAPIView(APIView):
    def get(self, request):
        realtime_service = RealTimeService()

        reference_id = f"COIN-APP-{get_random_string(length=20)}"

        realtime_service.push_event_to_frontend(
            "coinapp",
            "onRecieve",
            {
                "message": "Oshee, oba crypto, your money has been successfully processed.",
                "reference_id": reference_id,
                "action": "SUCCESS",
            },
        )
        return Response(
            data={"message": "Dispatched realtime"},
            status=status.HTTP_200_OK,
        )


def not_found(request, exception, *args, **kwargs):
    """
    Generic 400 error handler.
    """
    data = {"error": "Not found (404)"}
    return JsonResponse(data, status=status.HTTP_400_BAD_REQUEST)
