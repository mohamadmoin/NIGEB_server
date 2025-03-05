# finances/serializers.py

from rest_framework import serializers
from .models import Invoice, Payment

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'

    def create(self, validated_data):
        payment = super().create(validated_data)
        # After payment creation, recalc invoice
        invoice = payment.invoice
        total_paid = sum(p.amount for p in invoice.payments.all())
        if total_paid >= invoice.total_cost:
            invoice.paid = True
            invoice.save()
        return payment


class InvoiceSerializer(serializers.ModelSerializer):
    payments = PaymentSerializer(many=True, read_only=True)

    class Meta:
        model = Invoice
        fields = '__all__'
