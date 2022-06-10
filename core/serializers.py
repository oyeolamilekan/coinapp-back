from rest_framework import serializers
from .models import AcceptedCrypto, Bills, Network, WalletAddress

from rest_framework.fields import SerializerMethodField

class AcceptedCryptoSerializer(serializers.ModelSerializer):
    class Meta:
        model = AcceptedCrypto
        fields = ("title", "image", "short_title", "is_live")


class NetworkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Network
        fields = ("title", "image", "slug")

class WalletAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = WalletAddress
        fields = ("blockchain_type", "desposit_address")

class BillsSerializer(serializers.ModelSerializer):

    amount = SerializerMethodField()

    class Meta:
        model = Bills
        fields = (
            "title",
            "slug",
            "types",
            "amount",
        )
    
    def get_amount(self, obj):
        return f"{int(obj.amount):,}"