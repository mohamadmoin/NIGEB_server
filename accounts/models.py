# accounts/models.py
from django.db import models
from django.contrib.auth.models import User
import uuid


ROLE_CHOICES = (
    ("technician", "Technician"),
    ("manager", "Manager"),
    ("admin", "Administrator"),
)


def user_directory_path(instance, filename):
    # Files will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return f"user_{instance.user.id}/{filename}"

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    # Basic fields from earlier steps:
    lab = models.ForeignKey('labs.Lab', on_delete=models.CASCADE, null=True, blank=True)
    
    # Extended fields
    phone_number = models.CharField(max_length=50, blank=True)
    address = models.TextField(blank=True)
    profile_image = models.ImageField(upload_to=user_directory_path, null=True, blank=True)
    
    # Additional placeholders from "UsersDetaileds"
    other_1 = models.CharField(max_length=100, blank=True)
    other_2 = models.CharField(max_length=100, blank=True)
    other_3 = models.CharField(max_length=100, blank=True)

   
    # New 'role' field
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="technician")
    
    class Meta:
           ordering = ['id']  # or any other field you want to order by

    def __str__(self):
        return f"{self.user.username} Profile ({self.role})"
    
    
class PasswordResetToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reset_tokens')
    token = models.UUIDField(default=uuid.uuid4, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    used = models.BooleanField(default=False)
    
    class Meta:
           ordering = ['id']  # or any other field you want to order by

    def __str__(self):
        return f"ResetToken for {self.user.username} - {self.token}"