from apps.auth_user.permissions import DenyAll
from utils.responses import Response


class ActionSerializerMixin(object):
    """
        Mixin for declaring per action serializers for Viewset.
    """

    ACTION_SERIALIZERS = {}

    def get_serializer_class(self):
        if self.action in self.ACTION_SERIALIZERS:
            return self.ACTION_SERIALIZERS[self.action]

        return super().get_serializer_class()

    def get_paginate_list(self, queryset):
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return serializer


class ActionPermissionMixin(object):
    """
        Mixin for declaring per action serializers for Viewset.
    """

    DEFAULT_PERMISSION_CLASS = DenyAll
    ACTION_PERMISSIONS: dict = {}

    def get_permissions(self):
        if self.action in self.ACTION_PERMISSIONS:
            return [permission() for permission in self.ACTION_PERMISSIONS[self.action]]

        return [self.DEFAULT_PERMISSION_CLASS()]

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()


class ReturnResponseMixin(object):
    """
        Mixin for returning response.
    """

    def list(self, request, message=None, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def create(self, request, message=None, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return Response(data=response.data, message=message, status=response.status_code)

    def retrieve(self, request, message=None, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)
        return Response(data=response.data, message=message, status=response.status_code)

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()

    def destroy(self, request, message=None, *args, **kwargs):
        response = super().destroy(request, *args, **kwargs)
        return Response(data=response.data, message=message, status=response.status_code)

    def update(self, request, message=None, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        return Response(data=response.data, message=message, status=response.status_code)

    def partial_update(self, request, message=None, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    def handle_exception(self, exc):
        error = str(exc)
        if getattr(exc, 'detail', None):
            error = exc.detail
        elif getattr(exc, 'message', None):
            error = exc.message
        return Response(error=error, status=getattr(exc, 'status_code', 400), success=False)


class HandleExceptionMixin(object):

    def handle_exception(self, exc):
        error = str(exc)
        if getattr(exc, 'detail', None):
            error = exc.detail
        elif getattr(exc, 'message', None):
            error = exc.message
        return Response(error=error, status=getattr(exc, 'status_code', 400), success=False)
