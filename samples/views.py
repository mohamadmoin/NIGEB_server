from rest_framework import viewsets
from rest_framework import permissions
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

from .models import Sample, SampleTest, Attachment
from .serializers import SampleSerializer, SampleTestSerializer, AttachmentSerializer
from .permissions import IsSampleLabMemberOrReadOnly
from .filters import SampleFilter  # if using FilterSet

from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q  # Add this import


class SampleViewSet(viewsets.ModelViewSet):
    queryset = Sample.objects.all()
    serializer_class = SampleSerializer
    permission_classes = [IsSampleLabMemberOrReadOnly]

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = SampleFilter
    search_fields = ['sample_code', 'patient__first_name', 'patient__last_name']
    ordering_fields = ['sample_date', 'result_date']

    def get_queryset(self):
        """
        Optionally restrict the queryset to the user's lab
        if you want to apply it globally.
        """
        user = self.request.user
        if user.is_superuser or user.is_staff:
            return Sample.objects.all()
        else:
            # For a normal user, return only samples relevant to that user's lab
            user_lab = getattr(user.profile, 'lab', None)  # Use 'profile' to access UserProfile
            if user_lab:
                return Sample.objects.filter(origin_lab=user_lab) | Sample.objects.filter(receiver_lab=user_lab)
            return Sample.objects.none()
    
    @action(detail=True, methods=['post'])
    def transition(self, request, pk=None):
        """Example custom endpoint to handle transitions in a controlled manner."""
        sample = self.get_object()
        new_status = request.data.get('status')
        
        valid_transitions = {
            'CREATED': ['SENT'],
            'SENT': ['RECEIVED'],
            'RECEIVED': ['IN_PROGRESS'],
            'IN_PROGRESS': ['COMPLETED'],
            'COMPLETED': ['REPORTED'],
            'REPORTED': []
        }
        
        if new_status in valid_transitions.get(sample.status, []):
            sample.status = new_status
            sample.save()
            return Response({"detail": f"Transitioned to {new_status}"}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Invalid transition"}, status=status.HTTP_400_BAD_REQUEST)
        
    # def finalize_response(self, request, response, *args, **kwargs):
    #     # Print the response data
    #     print("Response data:", response.data)
    #     return super().finalize_response(request, response, *args, **kwargs)
################SHACK
class IsReceiverLabOrAdmin(permissions.BasePermission):
        def has_object_permission(self, request, view, obj):
            if request.user.is_superuser or request.user.is_staff:
                return True
            user_lab = getattr(request.user.userprofile, 'lab', None)
            return (user_lab == obj.sample.receiver_lab)

class SampleTestViewSet(viewsets.ModelViewSet):
    queryset = SampleTest.objects.all()
    serializer_class = SampleTestSerializer
    
    
    def get_queryset(self):
        qs = super().get_queryset()
        sample_id = self.request.query_params.get('sample')
        if sample_id:
            qs = qs.filter(sample_id=sample_id)
        # Optional: filter by group or search
        group = self.request.query_params.get('test_group')
        if group:
            qs = qs.filter(test_info__group__iexact=group)
        search = self.request.query_params.get('search')
        if search:
            # Example: search test_name or result_value
            qs = qs.filter(
                Q(test_info__test_name__icontains=search) |
                Q(result_value__icontains=search)
            )
        return qs
    
    def get_permissions(self):
        # Everyone must be authenticated due to global DRF settings.
        # Additional custom check: only the 'receiver_lab' should update result_value
        if self.action in ['update', 'partial_update', 'destroy']:
            return [IsReceiverLabOrAdmin()]
        return [permissions.IsAuthenticated()]

class AttachmentViewSet(viewsets.ModelViewSet):
    queryset = Attachment.objects.all()
    serializer_class = AttachmentSerializer




# For example, we can add filtering to the SamplesViewSet:
# # samples/views.py
# import django_filters
# from rest_framework import viewsets, permissions
# from rest_framework.filters import SearchFilter
# from .models import Sample
# from .serializers import SampleSerializer

# class SampleFilter(django_filters.FilterSet):
#     name = django_filters.CharFilter(field_name='name', lookup_expr='icontains', label="Search by Sample Name")
#     sample_code = django_filters.CharFilter(field_name='sample_code', lookup_expr='icontains', label="Search by Sample Code")
#     patient_name = django_filters.CharFilter(field_name='patient__name', lookup_expr='icontains', label="Search by Patient Name")
#     is_sent = django_filters.BooleanFilter(field_name='is_sent', label="Filter by Sent Status")
#     result_date = django_filters.DateFilter(field_name='result_date', lookup_expr='exact', label="Filter by Result Date")

#     class Meta:
#         model = Sample
#         fields = ['name', 'sample_code', 'patient_name', 'is_sent', 'result_date']

# class SampleViewSet(viewsets.ModelViewSet):
#     queryset = Sample.objects.all()
#     serializer_class = SampleSerializer
#     permission_classes = [permissions.IsAuthenticated]
#     filter_backends = (SearchFilter, django_filters.rest_framework.DjangoFilterBackend)
#     filterset_class = SampleFilter

#     def get_queryset(self):
#         queryset = super().get_queryset()
#         # Optionally, filter by the logged-in user
#         user = self.request.user
#         if user.is_authenticated:
#             return queryset.filter(user=user)
#         return queryset