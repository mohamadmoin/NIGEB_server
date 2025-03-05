
# You may want certain endpoints (like finances or test definitions) to allow only managers or admins to create/edit. 
# Let’s show a permission class that checks role:
# 
# 
# accounts/permissions.py
from rest_framework import permissions

class IsManagerOrAdmin(permissions.BasePermission):
    """
    Custom permission: Only allow users with role=='manager' or role=='admin'.
    """

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        user_profile = getattr(request.user, 'profile', None)
        if not user_profile:
            return False

        return user_profile.role in ("manager", "admin")




# Then in a ViewSet (e.g., for finances or test definitions):
# # finances/views.py
# from rest_framework import viewsets
# from accounts.permissions import IsManagerOrAdmin
# from rest_framework.permissions import IsAuthenticated

# class InvoiceViewSet(viewsets.ModelViewSet):
#     permission_classes = [IsAuthenticated, IsManagerOrAdmin]
#     ...