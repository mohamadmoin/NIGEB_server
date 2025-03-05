from rest_framework import permissions

class IsSampleLabMemberOrReadOnly(permissions.BasePermission):
    """
    Custom permission to allow only the origin_lab or receiver_lab members
    (or superuser/staff) to edit a Sample. Read-Only for others.
    """

    def has_object_permission(self, request, view, obj):
        # Allow safe methods (GET, HEAD, OPTIONS)
        if request.method in permissions.SAFE_METHODS:
            return True

        # If the user is admin or staff, allow
        if request.user.is_staff or request.user.is_superuser:
            return True

        # Otherwise, check if the user belongs to either the origin_lab or receiver_lab
        user_profile = getattr(request.user, 'userprofile', None)
        if not user_profile or not user_profile.lab:
            return False

        # If the user's lab is either the sample's origin_lab or receiver_lab
        return (
            user_profile.lab == obj.origin_lab or
            user_profile.lab == obj.receiver_lab
        )
