from drf_spectacular.utils import extend_schema
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated

from apps.vehicle import constants
from utils.responses import Response

from api.vehicle.paginations import CarPagination
from apps.vehicle.models import Car
from rest_framework.viewsets import ModelViewSet
from api.vehicle.filters import CarFilter
from api.mixins import ActionPermissionMixin, ActionSerializerMixin
from api.vehicle.serializers import car
from utils.swagger_tags import Mobile
from utils.utils import get_json_data


class CarViewSet(ActionPermissionMixin, ActionSerializerMixin, ModelViewSet):
    queryset = Car.objects.filter(is_active=True)
    filter_class = CarFilter
    serializer_class = car.CarSerializer
    pagination_class = CarPagination
    DEFAULT_PERMISSION_CLASS = AllowAny
    ACTION_SERIALIZERS = {
        'list': car.CarSerializer,
        'mini_list': car.CarMiniSerializer,
    }

    ACTION_PERMISSIONS = {
        'list': (AllowAny,)
    }

    @extend_schema(tags=[Mobile.Car.PREFIX])
    @action(methods=['get'], detail=False)
    def mini_list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @extend_schema(tags=[Mobile.Car.PREFIX])
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(tags=[Mobile.Car.PREFIX])
    def retrieve(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)
        return Response(data=response.data, status=response.status_code)

    @extend_schema(tags=[Mobile.Car.PREFIX])
    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return Response(data=response.data, message=constants.CAR_SUCCESSFULLY_CREATED, status=response.status_code)

    @extend_schema(tags=[Mobile.Car.PREFIX])
    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        return Response(data=response.data, message=constants.CAR_SUCCESSFULLY_UPDATED, status=response.status_code)

    @extend_schema(tags=[Mobile.Car.PREFIX])
    def partial_update(self, request, *args, **kwargs):
        response = super().partial_update(request, *args, **kwargs)
        return Response(data=response.data, message=constants.CAR_SUCCESSFULLY_UPDATED, status=response.status_code)

    @extend_schema(tags=[Mobile.Car.PREFIX])
    def destroy(self, request, *args, **kwargs):
        response = super().destroy(request, *args, **kwargs)
        return Response(data=response.data, message=constants.CAR_SUCCESSFULLY_DELETED, status=response.status_code)

    def handle_exception(self, exc):
        if getattr(exc, 'detail', None):
            return Response(error=exc.detail, success=False, status=exc.status_code)
        return Response(error=str(exc), success=False, status=exc.status_code)
