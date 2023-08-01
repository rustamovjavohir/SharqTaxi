from apps.billing.models import Promotion
from rest_framework import serializers


class PromotionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Promotion
        fields = (
            'id',
            'name',
            'description',
            'discount',
            'percentage',
            'start_date',
            'end_date',
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


class MiniPromotionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Promotion
        fields = (
            'id',
            'name',
            'description',
            'discount',
            'percentage',
            'is_active',
        )
        read_only_fields = (
            'id',
        )
