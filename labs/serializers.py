from rest_framework import serializers
from .models import Lab

class LabSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lab
        fields = '__all__'
        # or list specific fields, e.g.: fields = ('id', 'name', 'address', 'phone_number')
