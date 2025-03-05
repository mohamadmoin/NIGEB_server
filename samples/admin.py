from django.contrib import admin
from .models import Sample, SampleTest, Attachment

@admin.register(Sample)
class SampleAdmin(admin.ModelAdmin):
    list_display = ('sample_code', 'patient', 'origin_lab', 'receiver_lab', 'status', 'created_at')
    list_filter = ('status', 'origin_lab', 'receiver_lab')
    search_fields = ('sample_code',)

@admin.register(SampleTest)
class SampleTestAdmin(admin.ModelAdmin):
    list_display = ('sample', 'test_info', 'result_value', 'started_at', 'completed_at')

@admin.register(Attachment)
class AttachmentAdmin(admin.ModelAdmin):
    list_display = ('sample', 'file', 'uploaded_at', 'use_case')
