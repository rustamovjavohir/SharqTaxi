from django_filters.rest_framework import FilterSet
from apps.vehicle.models import Car


class CarFilter(FilterSet):
    class Meta:
        model = Car
        fields = (
            'id',
            'name',
            'number',
            'brand',
        )
