from rest_framework.serializers import ModelSerializer
from apps.vehicle.models import Brand


class BrandSerializer(ModelSerializer):
    class Meta:
        model = Brand
        fields = (
            'id',
            'name',
        )

