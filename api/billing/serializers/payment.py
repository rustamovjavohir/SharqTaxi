from api.auth_user.serializers.user import MiniUserClientSerializer
from apps.billing.models import UserPayment
from rest_framework import serializers


class UserPaymentSerializer(serializers.ModelSerializer):
    client = MiniUserClientSerializer(read_only=True)

    class Meta:
        model = UserPayment
        fields = (
            'id',
            'client',
            'payment_method',
            'amount',
            'currency',
            'is_active',
            'created_at',
            'updated_at'
        )
        read_only_fields = (
            'id',
            'is_active',
            'created_at',
            'updated_at'
        )
