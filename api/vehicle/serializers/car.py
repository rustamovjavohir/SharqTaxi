from rest_framework import serializers

from api.file.serializers.image import ImageSerializer
from api.vehicle.serializers.brand import BrandSerializer
from apps.vehicle.models import Car
from utils.utils import get_json_data


class CarSerializer(serializers.ModelSerializer):
    brand = BrandSerializer(many=False, read_only=True)
    image = ImageSerializer(many=True, read_only=True)

    class Meta:
        model = Car
        fields = (
            'id',
            'name',
            'slug',
            'number',
            'year',
            'color',
            'brand',
            'main_image',
            'image',
        )


class CarUpdateSerializer(serializers.ModelSerializer):
    number = serializers.CharField(required=False)

    class Meta:
        model = Car
        fields = CarSerializer.Meta.fields


class CarMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = CarSerializer.Meta.fields
