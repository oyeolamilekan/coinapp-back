from rest_framework import serializers
from .models import AcceptedCrypto


class AcceptedCryptoSerializer(serializers.ModelSerializer):
    class Meta:
        model = AcceptedCrypto
        fields = ("title", "short_title", "is_live")
