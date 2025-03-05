# from django_filters import rest_framework as filters
# from .models import Sample

# class SampleFilter(filters.FilterSet):
#     sample_code = filters.CharFilter(field_name='sample_code', lookup_expr='icontains')
#     status = filters.CharFilter(field_name='status', lookup_expr='exact')
#     patient_name = filters.CharFilter(method='filter_patient_name')

#     class Meta:
#         model = Sample
#         fields = ['sample_code', 'status']

#     def filter_patient_name(self, queryset, name, value):
#         return queryset.filter(patient__first_name__icontains=value) | \
#                queryset.filter(patient__last_name__icontains=value)
# filters.py (if you have a dedicated filter set)
import django_filters
from .models import Sample

class SampleFilter(django_filters.FilterSet):
    status = django_filters.CharFilter(field_name='status', lookup_expr='iexact')
    origin_lab = django_filters.NumberFilter(field_name='origin_lab__id', lookup_expr='exact')
    sample_date__gte = django_filters.DateTimeFilter(field_name='sample_date', lookup_expr='gte')
    sample_date__lte = django_filters.DateTimeFilter(field_name='sample_date', lookup_expr='lte')
    # Now add a "patient" filter:
    patient = django_filters.NumberFilter(field_name='patient__id', lookup_expr='exact')
    
    # Add a "receiver_lab" filter if you wish
    receiver_lab = django_filters.NumberFilter(field_name='receiver_lab__id', lookup_expr='exact')
    

    class Meta:
        model = Sample
        fields = ['patient', 'origin_lab', 'receiver_lab', 'status']

# In SampleViewSet, you already have:
# filterset_class = SampleFilter
# search_fields = ['sample_code', 'patient__first_name', 'patient__last_name']

# Add searching by patient.national_id, too:
search_fields = [
    'sample_code',
    'patient__first_name',
    'patient__last_name',
    'patient__national_id',
]

# Then, in get_queryset(), handle user-lab vs. admin logic:
def get_queryset(self):
    user = self.request.user
    queryset = super().get_queryset()
    # If not superuser/staff, filter only by user's lab
    if not (user.is_superuser or user.is_staff):
        user_lab = getattr(user.profile, 'lab', None)
        if user_lab:
            queryset = queryset.filter(origin_lab=user_lab)
        else:
            # No lab => return none
            queryset = queryset.none()
    return queryset
