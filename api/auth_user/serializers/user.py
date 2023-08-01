from django.db import transaction
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema_field

from api.billing.serializers.card import BankCardSerializer
from api.billing.serializers.promotion import PromotionSerializer, MiniPromotionSerializer
from api.vehicle.serializers.car import CarSerializer, CarUpdateSerializer
from api.vehicle.serializers.license import DriverLicenseSerializer
from apps.auth_user.models import User, UserRole, UserDriver, UserClient, UserDriverStatus
from rest_framework import serializers

from apps.vehicle.models import Car, DriverLicense
from service.auth_user import UserServices
from utils.generates import generate_unique_code


class _UserRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserRole
        fields = ('id', 'role')


class UserSerializer(serializers.ModelSerializer):
    user_roles = _UserRoleSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = (
            'id',
            'full_name',
            'phone_number',
            'password',
            'email',
            'birthday',
            'is_superuser',
            'is_active',
            'is_staff',
            'is_driver',
            'is_client',
            'created_at',
            'user_roles',
        )
        read_only_fields = (
            'id',
            'is_superuser',
            'is_active',
            'is_staff',
            'is_driver',
            'is_client',
            'created_at',
            'user_roles',
        )

        extra_kwargs = {
            'password': {'write_only': True}
        }


class MiniUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'full_name',
            'phone_number',
            'email',
            'birthday',
            'password',
            'created_at',
            'updated_at',
        )

        read_only_fields = (
            'updated_at',
            'created_at',
        )

        extra_kwargs = {
            'password': {'write_only': True}
        }


class _MiniUserSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField(required=False)
    email = serializers.EmailField(required=False)

    class Meta:
        model = User
        fields = (
            'id',
            'full_name',
            'phone_number',
            'email',
            'birthday',
            'created_at',
            'updated_at',
        )

        read_only_fields = (
            'updated_at',
            'created_at',
        )


class UserUpdateSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField(required=False)
    email = serializers.EmailField(required=False)
    password = serializers.CharField(required=False, write_only=True)

    class Meta:
        model = User
        fields = UserSerializer.Meta.fields
        read_only_fields = UserSerializer.Meta.read_only_fields


class UserDriverStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserDriverStatus
        fields = (
            'id',
            'status',
            'created_at',
            'updated_at'
        )
        read_only_fields = (
            'id',
            'created_at',
            'updated_at'
        )


class UserDriverSerializer(serializers.ModelSerializer):
    user_service = UserServices()

    user = MiniUserSerializer(required=False)
    car = CarSerializer(required=False)
    license = DriverLicenseSerializer(required=False)
    driver_status = serializers.ManyRelatedField(child_relation=UserDriverStatusSerializer(), read_only=True)

    def validate_driver_id(self, value):
        if value == '':
            return generate_unique_code()
        return value

    class Meta:
        model = UserDriver
        fields = (
            'id',
            'user',
            'driver_id',
            'car',
            'license',
            'is_working',
            'driver_status',
            'created_at',
            'updated_at'
        )
        read_only_fields = (
            'id',
            'driver_status',
            'driver_id',
            'created_at',
            'updated_at'
        )

    @transaction.atomic
    def create(self, validated_data):
        user_service = UserServices()
        return user_service.create_driver(**validated_data)


class UserDriverUpdateSerializer(serializers.ModelSerializer):
    user_service = UserServices()

    user = _MiniUserSerializer(required=False)
    car = CarUpdateSerializer(required=False)
    license = DriverLicenseSerializer(required=False)
    driver_status = serializers.ManyRelatedField(child_relation=UserDriverStatusSerializer(), read_only=True)

    class Meta:
        model = UserDriver
        fields = UserDriverSerializer.Meta.fields
        read_only_fields = UserDriverSerializer.Meta.read_only_fields

    @transaction.atomic
    def update(self, instance, validated_data):
        user_serializer = UserSerializer(instance.user, data=validated_data.pop('user', {}), partial=True)
        car_serializer = CarSerializer(instance.car, data=validated_data.pop('car', {}), partial=True)
        license_serializer = DriverLicenseSerializer(instance.license, data=validated_data.pop('license', {}),
                                                     partial=True)
        user_serializer.save() if user_serializer.is_valid() else None
        car_serializer.save() if car_serializer.is_valid() else None
        license_serializer.save() if license_serializer.is_valid() else None

        instance = super().update(instance, validated_data)
        return instance


class MiniUserClientSerializer(serializers.ModelSerializer):
    user = MiniUserSerializer(required=False)

    class Meta:
        model = UserClient
        fields = (
            'id',
            'user',
            'status',
            'client_id',
            'created_at',
            'updated_at'
        )
        read_only_fields = (
            'id',
            'status',
            'client_id',
            'created_at',
            'updated_at'
        )


class UserClientSerializer(serializers.ModelSerializer):
    user_service = UserServices()

    user = MiniUserSerializer(required=True)
    promotions = serializers.SerializerMethodField(method_name='get_promotion')
    cards = BankCardSerializer(many=True, required=False)

    class Meta:
        model = UserClient
        fields = (
            'id',
            'user',
            'client_id',
            'promotions',
            'cards',
            'created_at',
            'updated_at'
        )
        read_only_fields = (
            'id',
            'client_id',
            'created_at',
            'updated_at'
        )

    @extend_schema_field(serializers.ListField(child=MiniPromotionSerializer()))
    def get_promotion(self, obj):
        active_promo = obj.promotions.filter(is_active=True)
        serializer = MiniPromotionSerializer(active_promo, many=True)
        return serializer.data

    @transaction.atomic
    def create(self, validated_data):
        user_service = UserServices()
        return user_service.create_client(**validated_data)

    @transaction.atomic
    def update(self, instance, validated_data):
        user_serializer = UserSerializer(instance.user, data=validated_data.pop('user', {}), partial=True)
        user_serializer.save() if user_serializer.is_valid() else None

        instance = super().update(instance, validated_data)
        return instance


class UserClientUpdateSerializer(serializers.ModelSerializer):
    user_service = UserServices()

    user = _MiniUserSerializer(required=True)
    promotions = serializers.SerializerMethodField(method_name='get_promotion')
    cards = BankCardSerializer(many=True, required=False)

    class Meta:
        model = UserClient
        fields = (
            'id',
            'user',
            'client_id',
            'promotions',
            'cards',
            'created_at',
            'updated_at'
        )

        read_only_fields = (
            'id',
            'client_id',
            'created_at',
            'updated_at'
        )

    @extend_schema_field(serializers.ListField(child=MiniPromotionSerializer()))
    def get_promotion(self, obj):
        active_promo = obj.promotions.filter(is_active=True)
        serializer = MiniPromotionSerializer(active_promo, many=True)
        return serializer.data

    @transaction.atomic
    def update(self, instance, validated_data):
        user_serializer = UserSerializer(instance.user, data=validated_data.pop('user', {}), partial=True)
        user_serializer.save() if user_serializer.is_valid() else None

        instance = super().update(instance, validated_data)
        return instance


class UserClientRetailSerializer(serializers.ModelSerializer):
    user_service = UserServices()

    user = MiniUserSerializer(required=True)
    promotions = serializers.SerializerMethodField(method_name='get_promotion')
    cards = BankCardSerializer(many=True, required=False)

    class Meta:
        model = UserClient
        fields = (
            'id',
            'user',
            'client_id',
            'promotions',
            'cards',
            'created_at',
            'updated_at'
        )
        read_only_fields = (
            'id',
            'client_id',
            'created_at',
            'updated_at'
        )

    @extend_schema_field(serializers.ListField(child=MiniPromotionSerializer()))
    def get_promotion(self, obj):
        active_promo = obj.promotions.filter(is_active=True)
        serializer = MiniPromotionSerializer(active_promo, many=True)
        return serializer.data
