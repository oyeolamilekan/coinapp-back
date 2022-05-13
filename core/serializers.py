from rest_framework import serializers
from .models import AcceptedCrypto, Bills, Network


class AcceptedCryptoSerializer(serializers.ModelSerializer):
    class Meta:
        model = AcceptedCrypto
        fields = ("title", "image", "short_title", "is_live")


class NetworkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Network
        fields = ("title", "image", "slug")


class BillsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bills
        fields = (
            "title",
            "slug",
            "types",
            "amount",
        )