from rest_framework import permissions


class AuthorOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        auth = request.user.is_authenticated
        if request.method in permissions.SAFE_METHODS or not auth:
            return True
        return obj.author == request.user
