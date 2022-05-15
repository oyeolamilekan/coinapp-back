from rest_framework import serializers
from .models import AcceptedCrypto, Bills, Network

from rest_framework.fields import SerializerMethodField

class AcceptedCryptoSerializer(serializers.ModelSerializer):
    class Meta:
        model = AcceptedCrypto
        fields = ("title", "image", "short_title", "is_live")


class NetworkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Network
        fields = ("title", "image", "slug")


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
        return int(obj.amount)