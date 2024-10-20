from rest_framework import permissions


class OrderPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        # Allow authenticated users to list/retrieve
        if not request.user.is_authenticated:
            return False

        # Superusers and staff can see all
        if request.user.is_superuser or request.user.is_staff:
            return True

        # Regular users can only see their own
        return True

    def has_object_permission(self, request, view, obj):
        # Superusers and staff can access any order
        if request.user.is_superuser or request.user.is_staff:
            return True

        # Regular users can only access their own orders
        return obj.customer.user == request.user
