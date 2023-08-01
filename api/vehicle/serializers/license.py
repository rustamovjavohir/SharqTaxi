from apps.vehicle.models import DriverLicense
from rest_framework import serializers
from drf_extra_fields.fields import Base64ImageField


class DriverLicenseSerializer(serializers.ModelSerializer):
    image = Base64ImageField(required=False)

    class Meta:
        model = DriverLicense
        fields = ('id',
                  'given_by',
                  'number',
                  'date_of_issue',
                  'date_of_expiration',
                  'image',
                  'is_active',
                  'created_at',
                  'updated_at')
        read_only_fields = ('id', 'is_active', 'created_at', 'updated_at')


class DriverLicenseCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = DriverLicense
        fields = ('id',
                  'given_by',
                  'number',
                  'date_of_issue',
                  'date_of_expiration',
                  'image',
                  'is_active',
                  'created_at',
                  'updated_at')
        read_only_fields = ('id', 'is_active', 'created_at', 'updated_at')
