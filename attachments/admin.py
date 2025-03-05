from django.contrib import admin
from .models import FileAttachment

@admin.register(FileAttachment)
class FileAttachmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'sample', 'patient', 'use_case', 'created_at')
    list_filter = ('use_case',)
