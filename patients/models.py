from django.db import models

class Patient(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    national_id = models.CharField(max_length=50, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=10, blank=True, null=True)  # M, F, Other
    phone_number = models.CharField(max_length=50, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
           ordering = ['id']  # or any other field you want to order by

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.national_id})"
