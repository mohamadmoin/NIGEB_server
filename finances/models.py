# finances/models.py

from django.db import models
from samples.models import Sample

class Invoice(models.Model):
    sample = models.OneToOneField(Sample, on_delete=models.CASCADE, related_name='invoice')
    total_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
           ordering = ['id']  # or any other field you want to order by

    def __str__(self):
        return f"Invoice for Sample {self.sample.sample_code}"


class Payment(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    payment_date = models.DateTimeField(auto_now_add=True)
    payment_method = models.CharField(max_length=50, default='cash')  # 'cash', 'credit_card', etc.
    
    class Meta:
           ordering = ['id']  # or any other field you want to order by

    def __str__(self):
        return f"Payment of {self.amount} for Invoice {self.invoice.id}"
