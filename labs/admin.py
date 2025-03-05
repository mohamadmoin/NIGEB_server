from django.contrib import admin
from .models import Lab

@admin.register(Lab)
class LabAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone_number', 'address', 'created_at')
