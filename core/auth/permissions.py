from rest_framework.permissions import BasePermission, SAFE_METHODS


class UserPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_anonymous:
            return request.method in SAFE_METHODS

        if view.basename in ['event']:
            return bool(request.user and request.user.is_authenticated)

        if view.basename in ['event-board']:
            if request.method in ['DELETE']:
                return bool(
                    request.user.is_superuser
                    or request.user in [obj.operator, obj.event.admin]
                    )

            return bool(request.user and request.user.is_authenticated)

        if view.basename in ['account']:
            if request.method in SAFE_METHODS:
                return True
            return bool(request.user.id == obj.id)

        return False

    def has_permission(self, request, view):
        if view.basename in ['event', 'event-board', 'account', 'auth-logout']:
            if request.user.is_anonymous:
                return request.method in SAFE_METHODS

            return bool(request.user and request.user.is_authenticated)

        return False
