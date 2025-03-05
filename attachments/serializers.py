# attachments/serializers.py
from rest_framework import serializers
from .models import FileAttachment

class FileAttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileAttachment
        fields = '__all__'
