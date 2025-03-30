from rest_framework import permissions


class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object or admin users to edit or delete it.
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD, or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return request.user.is_authenticated

        # Allow post if user is authenticated
        if request.method == 'POST':
            return request.user.is_authenticated

        # Write permissions are only allowed to the owner of the object or admin users.
        is_owner = (
            hasattr(obj, 'owner_username') and obj.owner_username == request.user or
            hasattr(obj, 'username') and obj.username == request.user.username
        )
        is_admin = request.user.is_staff or request.user.is_superuser

        return is_owner or is_admin


class AdminWriteElseAuthenticated(permissions.BasePermission):
    """
    Custom permission to only allow admin users to write to an object
    but allow authenicated users to read it.
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return request.user.is_authenticated

        return request.user.is_staff or request.user.is_superuser
