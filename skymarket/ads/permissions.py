from django.http import Http404
from rest_framework.permissions import BasePermission

from ads.models import Ad


class IsOwner(BasePermission):
    message = "No permission"

    def has_permission(self, request, view):
        try:
            entity = Ad.objects.get(pk=view.kwargs['pk'])
        except Ad.DoesNotExist:
            raise Http404

        if entity.user_id == request.user.id:
            return True

        return False


class IsAdmin(BasePermission):
    message = "No permission"

    def has_permission(self, request, view):
        if request.user.role in ["admin"]:
            return True
        return False
