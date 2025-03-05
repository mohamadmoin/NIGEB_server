# finances/permissions.py
from rest_framework import permissions

class IsInvoiceLabMemberOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser or request.user.is_staff:
            return True
        user_lab = getattr(request.user.userprofile, 'lab', None)
        return user_lab and (user_lab == obj.sample.origin_lab or user_lab == obj.sample.receiver_lab)
