from django.utils.crypto import get_random_string
from lib.flutterwave import bill
from lib.quidax import quidax
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from core.models import Bills, BillsRecharge, Transaction, TransactionStatus


class CreateBillAPIView(APIView):
    def post(self, request):
        destination_id = request.data.get("destination_id", None)
        bill_type = request.data.get("bill_type", None)
        transaction_receipt_email = request.data.get("transaction_receipt_email", None)
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
                data={"message": "error in getting it done."},
                status=status.HTTP_200_OK,
            )
        current_price_ticker_obj = quidax.markets.fetch_market_ticker(
            f"{transaction_currency}ngn"
        )
        current_price = current_price_ticker_obj.get("data").get("ticker").get("last")
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
        estimated_amount = round(float(bills_obj.amount) / float(current_price), 3)
        reference_id = f"COIN-APP-{get_random_string(length=20)}"
        data = {
            "bills_type": bills_obj,
            "reference": reference_id,
            "recieving_id": destination_id,
            "transaction_receipt_email": transaction_receipt_email,
            "expected_amount": estimated_amount,
            "desposit_address": wallet_address,
            "recieving_currency": transaction_currency.upper(),
        }
        bills_recharge = BillsRecharge.objects.create(**data)
        bills_recharge.save()
        return Response(
            data={
                "status": "success",
                "message": f"kindly deposit {bills_recharge.expected_amount} to {bills_recharge.desposit_address}.",
                "reference_id": reference_id,
            },
            status=status.HTTP_200_OK,
        )


class ReceiveWebhooks(APIView):
    def post(self, request):
        if request.data["event"] == "deposit.successful":
            recieved_amount = float(request.data.get("data").get("amount"))

            wallet_address = (
                request.data.get("data").get("payment_address").get("address")
            )
            bill_recharge_obj = BillsRecharge.objects.get(
                desposit_address=wallet_address
            )
            if recieved_amount < float(bill_recharge_obj.expected_amount):
                return Response(
                    data={
                        "message": "amount rejected due it being less that expected amount."
                    },
                    status=status.HTTP_200_OK,
                )

            instant_order_object = quidax.instant_orders.create_instant_order(
                "me",
                bid="ngn",
                ask=bill_recharge_obj.recieving_currency.lower(),
                type="sell",
                volume=float(bill_recharge_obj.expected_amount),
                unit=bill_recharge_obj.recieving_currency.lower(),
            )
            bill_recharge_obj.is_paid = True
            bill_recharge_obj.save()
            instant_order_object_id = instant_order_object.get("data").get("id")
            confirm_instant_object = quidax.instant_orders.confirm_instant_orders(
                "me",
                instant_order_object_id,
            )
            total_amount = (
                confirm_instant_object.get("data").get("receive").get("amount")
            )
            response = bill.buy_airtime(
                bill_recharge_obj.recieving_id,
                float(bill_recharge_obj.bills_type.amount),
            )
            data = {
                "bill": bill_recharge_obj,
                "amount": total_amount,
                "status": TransactionStatus.SUCCESS,
            }
            if response.get("status") != "success":
                data["reason"] = "airtime could not be released."
                data["status"] = TransactionStatus.FAILED
            transaction_obj = Transaction.objects.create(**data)
            transaction_obj.save()

        return Response(
            data={"message": "successfully recieved payments."},
            status=status.HTTP_200_OK,
        )
