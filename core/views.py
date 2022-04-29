import json
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from core.models import Bills, BillsRecharge
from lib.quidax import quidax
from lib.flutterwave import bill


class CreateBillAPIView(APIView):
    def post(self, request):
        destination_id = request.data.get("destination_id", None)
        bill_type = request.data.get("bill_type", None)
        if not all([destination_id, bill_type]):
            return Response(
                data={"message": "error in getting it done."},
                status=status.HTTP_200_OK,
            )
        bills_obj = Bills.objects.get(slug=bill_type)
        bills_recharge = BillsRecharge.objects.create(
            bill_type=bills_obj,
            recieving_id=destination_id,
        )
        bills_recharge.save()
        return Response(
            data={"message": "success"},
            status=status.HTTP_200_OK,
        )


class ReceiveWebhooks(APIView):
    def post(self, request):
        if request.data["event"] == "deposit.successful":
            amount = float(request.data.get("data").get("amount"))
            instant_order_object = quidax.instant_orders.create_instant_order(
                "me",
                bid="ngn",
                ask="trx",
                type="sell",
                volume=amount,
                unit="trx",
            )
            instant_order_object_id = instant_order_object.get("data").get("id")
            confirm_instant_object = quidax.instant_orders.confirm_instant_orders(
                "me",
                instant_order_object_id,
            )
            total_amount = confirm_instant_object.get("data").get("receive").get("amount")
            response = bill.buy_airtime("+2348087307896", total_amount)
        return Response(
            data={"message": "successfully recieved payments."},
            status=status.HTTP_200_OK,
        )
