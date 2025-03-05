from dataclasses import field
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import  TestInfos, TestResults, Samples,Patients,SampleLists,FileTables,UsersDetaileds
from django.contrib.auth.models import User

class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username','is_active','groups']


# class NoteSerializer(ModelSerializer):
#     class Meta:
#         model = Note
#         fields = '__all__' 

# class PatientSerializer(ModelSerializer):
#     class Meta:
#         model = Patient
#         fields = '__all__'

class SampleInfoSerializer(serializers.Serializer):
    samples_received = serializers.IntegerField()
    samples_sent = serializers.IntegerField()


class UsersDetailedsSerializer(ModelSerializer):
    class Meta:
        model = UsersDetaileds
        fields = '__all__'
        

class FileSerializer(ModelSerializer):
    class Meta:
        model = FileTables
        fields = '__all__'
        
class PatientsSerializer(ModelSerializer):
    class Meta:
        model = Patients
        fields = '__all__'
        

class SampleListsSerializer(ModelSerializer):
    class Meta:
        model = SampleLists
        fields = '__all__'

class SamplesSerializer(ModelSerializer):
    class Meta:
        model = Samples
        fields = '__all__'
        
class TestInfosSerializer(ModelSerializer):
    class Meta:
        model = TestInfos
        fields = '__all__'
        
class TestResultsSerializer(ModelSerializer):
    class Meta:
        model = TestResults
        fields = '__all__'


# class ConstantTablesSerializer(ModelSerializer):
#     class Meta:
#         model = ConstantTables
#         fields = '__all__'

# class DashTablesSerializer(ModelSerializer):
#     class Meta:
#         model = DashTables
#         fields = '__all__'

# class HarisTablesSerializer(ModelSerializer):
#     class Meta:
#         model = HarisTables
#         fields = '__all__'

# class SFTablesSerializer(ModelSerializer):
#     class Meta:
#         model = SFTables
#         fields = '__all__'

# class VASTablesSerializer(ModelSerializer):
#     class Meta:
#         model = VASTables
#         fields = '__all__'

# class TreatmentTablesSerializer(ModelSerializer):
#     class Meta:
#         model = TreatmentTables
#         fields = '__all__'

# class ImagingTablesSerializer(ModelSerializer):
#     image_url = serializers.ImageField(required=False)

#     class Meta:
#         model = ImagingTables
#         fields = '__all__'

# class InjuryTablesSerializer(ModelSerializer):
#     class Meta:
#         model = InjuryTables
#         fields = '__all__'

# class FollowradsSerializer(ModelSerializer):
#     class Meta:
#         model = Followrads
#         fields = '__all__'

# class FollowhumsSerializer(ModelSerializer):
#     class Meta:
#         model = Followhums
#         fields = '__all__'

# class FollowfemsSerializer(ModelSerializer):
#     class Meta:
#         model = Followfems
#         fields = '__all__'
# class WomacsSerializer(ModelSerializer):
#     class Meta:
#         model = Womacs
#         fields = '__all__'

