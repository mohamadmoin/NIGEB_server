from rest_framework import serializers
from .models import Sample, SampleTest, Attachment
from patients.serializers import PatientSerializer  # or define a simpler serializer


# class SampleSerializer(serializers.ModelSerializer):
#     # If you want nested detail:
#     # sample_tests = SampleTestSerializer(many=True, read_only=True)
#     # attachments = AttachmentSerializer(many=True, read_only=True)

#     class Meta:
#         model = Sample
#         fields = '__all__'

class SampleSerializer(serializers.ModelSerializer):
    patient_data = PatientSerializer(source='patient', read_only=True)
    # or if you want a minimal subset, create a small PatientMiniSerializer
    class Meta:
        model = Sample
        fields = [
            'id',
            'sample_code',
            'status',
            'patient',       # keep the raw FK if you need
            'patient_data',  # for name, last_name, national_id
            'sample_date',
            'expected_result_date',
            'result_date',
            'note',
            'emergent_status',
            'history',
            'sample_type',
            'origin_lab',
            'history_file',
            'receiver_lab',
            'created_at'
            # etc. other fields
        ]

class AttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attachment
        fields = '__all__'

class SampleTestSerializer(serializers.ModelSerializer):
    class Meta:
        model = SampleTest
        fields = '__all__'


