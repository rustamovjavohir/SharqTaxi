from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from apps.billing.models import BankCard
from service.auth_user import UserServices


class BankCardUpdateSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField(source='client.user.phone_number', required=False, read_only=True)

    class Meta:
        model = BankCard
        fields = (
            'id',
            'client',
            'phone_number',
            'pan',
            'card_holder',
            'expiration_date',
            'cvv',
            'created_at',
            'updated_at'
        )
        read_only_fields = (
            'id',
            'client',
            'phone_number',
            'created_at',
            'updated_at'
        )


class BankCardSerializer(serializers.ModelSerializer):
    user_services = UserServices()

    number = serializers.SerializerMethodField()

    phone_number = serializers.CharField(source='client.user.phone_number', required=True)

    class Meta:
        model = BankCard
        fields = (
            'id',
            'client',
            'phone_number',
            'number',
            'pan',
            'card_holder',
            'expiration_date',
            'cvv',
            'is_active',
            'created_at',
            'updated_at'
        )
        read_only_fields = (
            'id',
            'client',
            'is_active',
            'created_at',
            'updated_at'
        )
        extra_kwargs = {
            'pan': {'write_only': True}
        }

    @extend_schema_field(serializers.CharField)
    def get_number(self, obj):
        return obj.secret_pan  # TODO change to musk_pan

    def create(self, validated_data):
        validated_data['client'] = self.user_services.get_client_by_phone_number(
            validated_data['client']['user']['phone_number'])
        return super().create(validated_data)
