# finances/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from samples.models import SampleTest
from .models import Invoice

@receiver(post_save, sender=SampleTest)
def create_or_update_invoice(sender, instance, created, **kwargs):
    """
    Whenever a SampleTest is created or updated, recalc invoice total.
    """
    sample = instance.sample
    invoice, _ = Invoice.objects.get_or_create(sample=sample)
    # Recalculate total cost from all SampleTests:
    tests = sample.sample_tests.all()
    total_cost = 0
    for s_test in tests:
        if s_test.test_info and s_test.test_info.test_cost:
            total_cost += s_test.test_info.test_cost
    invoice.total_cost = total_cost
    invoice.save()
