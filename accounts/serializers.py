# from rest_framework import serializers
# from .models import UserProfile
# from django.contrib.auth.models import User
# from labs.serializers import LabSerializer  # If needed to nest lab info

# class UserSerializer(serializers.ModelSerializer):
#     # For demonstration, let's show how to expose user fields
#     class Meta:
#         model = User
#         fields = ('id', 'username', 'email', 'first_name', 'last_name')

# class UserProfileSerializer(serializers.ModelSerializer):
#     user = UserSerializer(read_only=True)  
#     # Or you could allow creation of user inline. 
#     # lab = LabSerializer(read_only=True) # If you want to nest the Lab object

#     class Meta:
#         model = UserProfile
#         fields = '__all__'


# accounts/serializers.py
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserProfile
from django.contrib.auth.password_validation import validate_password
import uuid
from .models import PasswordResetToken
from django.core.mail import send_mail
from labs.models import Lab


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name')


class LabSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lab
        fields = ['id', 'name']  # Include fields you want

class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    profile_image = serializers.ImageField(required=False)
    lab = LabSerializer(read_only=True)  # Use nested serializer for lab


    class Meta:
        model = UserProfile
        fields = '__all__'
        # Or specify fields if you don't want them all

# accounts/serializers.py



# class RegisterSerializer(serializers.Serializer):
#     username = serializers.CharField(required=True, max_length=150)
#     email = serializers.EmailField(required=True)
#     password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
#     password2 = serializers.CharField(write_only=True, required=True)
#     role = serializers.CharField(required=False)  # 'technician', 'manager', 'admin' if you want them to pick

#     def validate(self, attrs):
#         # Check password match
#         if attrs['password'] != attrs['password2']:
#             raise serializers.ValidationError({"password": "Passwords didn't match."})
#         return attrs

#     def create(self, validated_data):
#         # Remove password2 from data
#         password = validated_data.pop('password')
#         validated_data.pop('password2', None)

#         # Extract role if provided
#         role = validated_data.pop('role', None)

#         # Create user
#         user = User(username=validated_data['username'], email=validated_data['email'])
#         user.set_password(password)
#         user.save()

#         # Optionally create a user profile
#         user_profile = UserProfile.objects.create(user=user)
#         if role:
#             user_profile.role = role
# #             user_profile.save()
# #         return user
# class RegisterSerializer(serializers.Serializer):
#     username = serializers.CharField(required=True, max_length=150)
#     email = serializers.EmailField(required=True)
#     password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
#     password2 = serializers.CharField(write_only=True, required=True)
#     role = serializers.CharField(required=False)  # 'technician', 'manager', 'admin' if you want them to pick
#     lab_id = serializers.IntegerField(required=False)  # New field for lab association

#     def validate(self, attrs):
#         # Check password match
#         if attrs['password'] != attrs['password2']:
#             raise serializers.ValidationError({"password": "Passwords didn't match."})
#         return attrs

#     def create(self, validated_data):
#         # Remove password2 from data
#         password = validated_data.pop('password')
#         validated_data.pop('password2', None)

#         # Extract role and lab_id if provided
#         role = validated_data.pop('role', None)
#         lab_id = validated_data.pop('lab_id', None)

#         # Create user
#         user = User(username=validated_data['username'], email=validated_data['email'])
#         user.set_password(password)
#         user.save()

#         # Create a user profile
#         user_profile = UserProfile.objects.create(user=user)

#         # Set role if provided
#         if role:
#             user_profile.role = role

#         # Associate with a lab if lab_id is provided
#         if lab_id:
#             try:
#                 lab = Lab.objects.get(id=lab_id)
#                 user_profile.lab = lab
#             except Lab.DoesNotExist:
#                 raise serializers.ValidationError({"lab_id": "Lab not found."})

#         user_profile.save()
#         return user

class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField(required=True, max_length=150)
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    role = serializers.CharField(required=False)  # 'technician', 'manager', 'admin' if you want them to pick
    lab_name = serializers.CharField(required=False)  # New field for lab name
    lab_address = serializers.CharField(required=False, allow_blank=True)  # New field for lab address
    lab_phone_number = serializers.CharField(required=False, allow_blank=True)  # New field for lab phone number
    lab_email = serializers.EmailField(required=False, allow_blank=True)  # New field for lab email

    def validate(self, attrs):
        # Check password match
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Passwords didn't match."})
        return attrs

    def create(self, validated_data):
        # Remove password2 from data
        password = validated_data.pop('password')
        validated_data.pop('password2', None)

        # Extract role and lab details if provided
        role = validated_data.pop('role', None)
        lab_name = validated_data.pop('lab_name', None)
        lab_address = validated_data.pop('lab_address', '')
        lab_phone_number = validated_data.pop('lab_phone_number', '')
        lab_email = validated_data.pop('lab_email', '')

        # Create user
        user = User(username=validated_data['username'], email=validated_data['email'])
        user.set_password(password)
        user.save()

        # Create a user profile
        user_profile = UserProfile.objects.create(user=user)

        # Set role if provided
        if role:
            user_profile.role = role

        # Create a new lab if lab_name is provided
        if lab_name:
            lab = Lab.objects.create(
                name=lab_name,
                address=lab_address,
                phone_number=lab_phone_number,
                email=lab_email
            )
            user_profile.lab = lab
        else:
            lab = Lab.objects.create(
                name= validated_data.pop('username','') ,
                address="",
                phone_number="",
                email= validated_data.pop('email','')
            )
            user_profile.lab = lab
            

        user_profile.save()
        return user

class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

    def validate_email(self, value):
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError("No user with that email.")
        return value

    def save(self):
        email = self.validated_data['email']
        user = User.objects.get(email=email)
        # Create token
        reset_token = PasswordResetToken.objects.create(user=user)
        # Send email (or just print it for dev)
        token_str = str(reset_token.token)
        # Example: in dev, print token to console
        print(f"[DEV] Password reset token for {email}: {token_str}")

        # If you want to actually send an email:
        send_mail(
            subject="Password Reset Request",
            message=f"Your reset token is {token_str}",
            from_email="noreply@mydomain.com",
            recipient_list=[email],
        )
        return reset_token


class ResetPasswordSerializer(serializers.Serializer):
    token = serializers.UUIDField(required=True)
    password = serializers.CharField(write_only=True, required=True)
    password2 = serializers.CharField(write_only=True, required=True)

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Passwords do not match"})
        return attrs

    def save(self):
        token = self.validated_data['token']
        password = self.validated_data['password']
        # Find token
        try:
            reset_token = PasswordResetToken.objects.get(token=token, used=False)
        except PasswordResetToken.DoesNotExist:
            raise serializers.ValidationError("Invalid or used token.")

        # Set password
        user = reset_token.user
        user.set_password(password)
        user.save()

        # Mark token as used
        reset_token.used = True
        reset_token.save()

        return user
