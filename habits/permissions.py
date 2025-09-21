from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):
    """ Проверять, является ли пользователь владельцем привычки """

    message = 'Вы не являетесь автором привычки'

    def has_object_permission(self, request, view, obj):
        if obj.user == request.user:
            return True
        return False