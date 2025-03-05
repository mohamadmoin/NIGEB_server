from django.db import models

# Create your models here.
# attachments/models.py
from django.db import models
from django.contrib.auth.models import User
from samples.models import Sample
from patients.models import Patient

class FileAttachment(models.Model):
    """
    A unified attachment model that can store files for samples or patients.
    """
    # Optionally track who uploaded it:
    uploaded_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)

    # We can keep references to a sample, or a patient, or both, each possibly null:
    sample = models.ForeignKey(Sample, null=True, blank=True, on_delete=models.CASCADE, related_name='file_attachments')
    patient = models.ForeignKey(Patient, null=True, blank=True, on_delete=models.CASCADE, related_name='file_attachments')

    # The actual file:
    file = models.FileField(upload_to='attachments/')

    # If you want to store original path or filename:
    file_name = models.CharField(max_length=200, blank=True)

    # A "use_case" or "category" if you want:
    use_case = models.CharField(max_length=50, blank=True)
    description = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
           ordering = ['id']  # or any other field you want to order by

    def __str__(self):
        return f"FileAttachment(id={self.id}, sample={self.sample}, patient={self.patient})"
