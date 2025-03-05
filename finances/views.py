# finances/views.py

from rest_framework import viewsets, status
from rest_framework.response import Response

from finances.permissions import IsInvoiceLabMemberOrAdmin
from .models import Invoice, Payment
from .serializers import InvoiceSerializer, PaymentSerializer
from rest_framework.permissions import IsAuthenticated

class InvoiceViewSet(viewsets.ModelViewSet):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer
    permission_classes = [IsAuthenticated, IsInvoiceLabMemberOrAdmin] # Or custom permission
# permission_classes = [IsAuthenticated, IsManagerOrAdmin]
  
  
    # Optionally override get_queryset to filter by user lab, etc.
    # def get_queryset(self):
    #     user_lab = getattr(self.request.user.userprofile, 'lab', None)
    #     # Return only invoices for samples of that lab, or all if staff
    #     ...

class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]
