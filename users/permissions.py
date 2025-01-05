from rest_framework.permissions import BasePermission

class HasAcceptDeny(BasePermission):
    message = "You're not allowed to perform this action"

    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, obj):
        if request.method == 'POST' and view.action in ('accept', 'deny'):
            if request.user.is_superuser:
                return True
            return False

        return True