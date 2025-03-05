# from rest_framework import viewsets
# from .models import Patient
# from .serializers import PatientSerializer

# class PatientViewSet(viewsets.ModelViewSet):
#     queryset = Patient.objects.all()
#     serializer_class = PatientSerializer


from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Patient
from .serializers import PatientSerializer

class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    permission_classes = [AllowAny]  # Add this line to require authentication
    
    
    