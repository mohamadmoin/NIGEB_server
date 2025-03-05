from django.db import models
from django.utils import timezone
from labs.models import Lab
from patients.models import Patient
from tests_definitions.models import TestInfo

SAMPLE_STATUSES = (
    ("CREATED", "Created"),
    ("SENT", "Sent"),
    ("RECEIVED", "Received"),
    ("IN_PROGRESS", "In Progress"),
    ("COMPLETED", "Completed"),
    ("REPORTED", "Reported"),
)

class Sample(models.Model):
    sample_code = models.CharField(max_length=50, unique=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='samples')

    origin_lab = models.ForeignKey(Lab, on_delete=models.CASCADE, related_name='origin_samples')
    receiver_lab = models.ForeignKey(Lab, on_delete=models.CASCADE, related_name='received_samples',
                                     null=True, blank=True)

    status = models.CharField(max_length=20, choices=SAMPLE_STATUSES, default="CREATED")
    emergent_status = models.BooleanField(default=False)
    history = models.TextField(blank=True, null=True)  # e.g., clinical history

    sample_type = models.CharField(max_length=50, blank=True, null=True)
    sample_date = models.DateTimeField(default=timezone.now)
    expected_result_date = models.DateTimeField(blank=True, null=True)
    result_date = models.DateTimeField(blank=True, null=True)

    # If you only want 1 "history file" per sample:
    history_file = models.FileField(upload_to='history_files/', blank=True, null=True)
    note = models.TextField(blank=True, null=True)  # receiver's note to sender


    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
           ordering = ['id']  # or any other field you want to order by

    def __str__(self):
        return f"Sample {self.sample_code} for {self.patient}"

class SampleTest(models.Model):
    sample = models.ForeignKey(Sample, on_delete=models.CASCADE, related_name='sample_tests')
    test_info = models.ForeignKey(TestInfo, on_delete=models.CASCADE)

    result_value = models.CharField(max_length=100, blank=True, null=True)
    result_file = models.FileField(upload_to='test_results/', blank=True, null=True)
    started_at = models.DateTimeField(blank=True, null=True)
    completed_at = models.DateTimeField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    
    class Meta:
           ordering = ['id']  # or any other field you want to order by

    def __str__(self):
        return f"{self.sample.sample_code} - {self.test_info.test_name}"

class Attachment(models.Model):
    sample = models.ForeignKey(Sample, on_delete=models.CASCADE, related_name='attachments')
    file = models.FileField(upload_to='attachments/')
    use_case = models.CharField(max_length=50, blank=True)  # e.g., "report", "additional_info"
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
           ordering = ['id']  # or any other field you want to order by

    def __str__(self):
        return f"Attachment for {self.sample.sample_code}"
