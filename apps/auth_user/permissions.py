from rest_framework.permissions import BasePermission, SAFE_METHODS
from utils.choices import UserRoleChoices


def check_user_role(request, role):
    """ Checks if request user has specific role """

    return bool(request.user
                and request.user.is_authenticated
                and request.user.user_roles.filter(role=role).exists())


def check_user_type(request, _type):
    """ Checks if request user is specific type """

    return bool(request.user
                and request.user.is_authenticated
                and getattr(request.user, _type, False))


class DenyAll(BasePermission):

    def has_permission(self, request, view):
        return False


class IsSuperUser(BasePermission):
    """
    Allows access only to superusers.
    """

    def has_permission(self, request, view):
        return bool(check_user_type(request=request, _type='is_superuser'))


class IsSuperAdmin(BasePermission):
    """
    Allows access only to superadmins.
    """

    def has_permission(self, request, view):
        return check_user_role(request=request, role=UserRoleChoices.SUPER_ADMIN)


class IsAdmin(BasePermission):
    """
    Allows access only to admins.
    """

    def has_permission(self, request, view):
        return check_user_role(request=request, role=UserRoleChoices.ADMIN)


class IsDriver(BasePermission):
    """
    Allows access only to Drivers.
    """

    def has_permission(self, request, view):
        return bool(check_user_type(request=request, _type='is_driver')
                    or check_user_type(request=request, _type='is_superuser'))


class IsClient(BasePermission):
    """
    Allows access only to Clients.
    """

    def has_permission(self, request, view):
        return bool(check_user_type(request=request, _type='is_client')
                    or check_user_type(request=request, _type='is_superuser'))


class IsStaff(BasePermission):
    """
    Allows access only to Staff.
    """

    def has_permission(self, request, view):
        return bool(check_user_type(request=request, _type='is_staff')
                    or check_user_type(request=request, _type='is_superuser'))


class IsOwnerOrReadOnlyClient(BasePermission):
    """
    Allows access only to object owner.
    """

    def has_object_permission(self, request, view, obj):
        return bool(obj.client == request.user
                    or check_user_type(request=request, _type='is_superuser'))


class IsOwnerClientCard(BasePermission):
    """
    Allows access only to object owner.
    """

    def has_object_permission(self, request, view, obj):
        return bool(obj.client == request.user.user_client
                    or check_user_type(request=request, _type='is_superuser'))
