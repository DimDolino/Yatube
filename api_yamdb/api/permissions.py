from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminOrSuperUser(BasePermission):

    def has_permission(self, request, view):
        user = request.user
        return user.is_authenticated and user.is_admin


class IsAdminOrReadOnly(BasePermission):

    def has_permission(self, request, view):
        user = request.user
        return (
            request.method in SAFE_METHODS
            or (user.is_authenticated and user.is_admin)
        )


class IsAdminOrModeratorOrAuthor(BasePermission):

    def has_object_permission(self, request, view, obj):
        user = request.user
        return (
            user.is_anonymous or obj.author == user
            or user.is_admin or user.is_moderator
        )
