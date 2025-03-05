# attachments/views.py
from rest_framework import viewsets, permissions
from .models import FileAttachment
from .serializers import FileAttachmentSerializer

class FileAttachmentViewSet(viewsets.ModelViewSet):
    queryset = FileAttachment.objects.all()
    serializer_class = FileAttachmentSerializer
    permission_classes = [permissions.IsAuthenticated]
    # Optionally override get_queryset to filter by user if needed
