# from rest_framework import viewsets
# from .models import UserProfile
# from .serializers import UserProfileSerializer

# class UserProfileViewSet(viewsets.ModelViewSet):
#     queryset = UserProfile.objects.all()
#     serializer_class = UserProfileSerializer
# accounts/views.py
from rest_framework import viewsets, permissions
from .models import UserProfile
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import generics, status
from rest_framework.response import Response
from .serializers import RegisterSerializer, ForgotPasswordSerializer, ResetPasswordSerializer, UserProfileSerializer
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny




class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]  # for image uploads
    pagination_class = None

    def get_queryset(self):
        user = self.request.user
        # Example: let users only see/edit their own profile or an admin sees all
        if user.is_superuser:
            return UserProfile.objects.all()
        return UserProfile.objects.filter(user=user)





class RegisterView(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]  # Allow access without authentication

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "message": "User created successfully",
            "user_id": user.id,
            "username": user.username,
            "email": user.email
        }, status=status.HTTP_201_CREATED)



class ForgotPasswordView(generics.GenericAPIView):
    serializer_class = ForgotPasswordSerializer
    permission_classes = [AllowAny]  # Allow access without authentication

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "Reset token created. Check your email."}, status=status.HTTP_200_OK)


class ResetPasswordView(generics.GenericAPIView):
    serializer_class = ResetPasswordSerializer
    permission_classes = [AllowAny]  # Allow access without authentication

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "Password reset successful."}, status=status.HTTP_200_OK)
