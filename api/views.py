from asyncio import constants
import os
import subprocess

from django.forms import ImageField
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, render, redirect

from .models import TestInfos, TestResults, Samples, Patients,SampleLists, FileTables, UsersDetaileds
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import   PatientsSerializer, SamplesSerializer, UserSerializer,SampleInfoSerializer, TestResultsSerializer, TestInfosSerializer,SampleListsSerializer,FileSerializer,UsersDetailedsSerializer
from .forms import UploadFileForm,DocumentForm
from rest_framework import permissions
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User

from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth import authenticate, login, logout

from django.contrib import messages

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group

from .forms import CreateUserForm
from .decorators import unauthenticated_user, allowed_users, admin_only
from api import serializers
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from api import samples_import

# Create your views here.

@api_view(['GET'])
def getRoutes(request):
    routes = [
        {
            'Endpoint': '/trauma/',
            'method': 'GET',
            'body': None,
            'description': 'Returns an arry of trauma'
        },
        {
            'Endpoint': '/trauma/id',
            'method': 'GET',
            'body': None,
            'description': 'Returns a single note object'
        },
        # {
        #     'Endpoint': '/trauma/create/',
        #     'method': 'POST',
        #     'body': {'body': ""},
        #     'description': 'Creates new note with data sent in post request'
        # },
        # {
        #     'Endpoint': '/trauma/id/update',
        #     'method': 'PUT',
        #     'body': {'body': ""},
        #     'description': 'Creates an existing note with data sent in'
        # },
        # {
        #     'Endpoint': '/trauma/id/delete',
        #     'method': 'DELETE',
        #     'body': None,
        #     'description': 'Deletes and exiting note'
        # },
    ]
    return Response(routes)

@api_view(['GET'])
def connectioncheck(request):
    return Response(status=status.HTTP_201_CREATED)

@unauthenticated_user
def registerPage(request):

    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')


            messages.success(request, 'Account was created for ' + username)

            return redirect('login2')
        

    context = {'form':form}
    return render(request, 'register.html', context)

def loginPage2(request):
    context = {}
    return render(request, 'register.html', context)

@csrf_exempt
@api_view(('GET','POST'))
@renderer_classes((JSONRenderer,))
@unauthenticated_user
def loginPage(request):
    
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password =request.POST.get('password')
        

        user = authenticate(request, username=username, password=password)
        d = User.objects.get(username = username)

        if user is not None:
            login(request, user)
   
            
            return JsonResponse({'auth': 1,'id': user.id,'username':user.username,
                        'is_active':user.is_active,
                        'token':Token.objects.get(user=user).key,'is_staff':d.is_staff,'first_name':user.first_name})
        else:
            
            messages.info(request, 'Username OR password is incorrect')

    context = {}
    return render(request, 'login.html',context)

def logoutUser(request):
    logout(request)
    return redirect('login')

@api_view(['GET'])
def loginConf(request,pk, *args, **kwargs):
    user = User.objects.get(username = pk)
    token = Token.objects.get(user=user).key
    serializer =UserSerializer(user,many = False)
    
    data = {}
    data['id'] = user.id
    data['username'] = user.username
    data['is_active'] = user.is_staff
   # data['is_staff'] = user.is_staff
    data['token'] =token
    
   
    return Response(data)


@api_view(['POST'])
def adddata(request):
    samples_import.import_books("patient_data.csv")
    
    return Response("serializer.data")


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes((IsAuthenticated, ))
def getPatients(request):
    patients = Patients.objects.all()
    serializer = PatientsSerializer(patients, many = True)
    return Response(serializer.data)

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes((IsAuthenticated, ))
def getPatient(request, pk):
    patient = Patients.objects.get(id_id = pk)
    serializer = PatientsSerializer(patient, many = False,)
    return Response(serializer.data)

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes((IsAuthenticated, ))
def createPatient(request):
    data = request.data
    userr = User.objects.get(id = data['userCreatorId'])
    
    patient = Patients.objects.create(
        id_id = data['id_id'],
        user = userr,
        name = data['name'],
        #userCreatorName = data['userCreatorName'],
        surname = data['surname'],
        kodmeli = data['kodmeli'],
        gender = data['gender'],
        birth = data['birth'],
        is_imported = data['is_imported'],
        date_created = data['date_created'],
        phone_number = data['phone_number']
    )
    serializer = PatientsSerializer(patient, many = False)
    return Response(serializer.data)

@api_view(['PUT'])
@authentication_classes([TokenAuthentication])
@permission_classes((IsAuthenticated, ))
def updatePatients(request, pk):
    data = request.data
    
    patient = Patients.objects.get(id_id = pk)
    serializer = PatientsSerializer(patient, data = request.data)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)

@api_view(['DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes((IsAuthenticated, ))
def deletePatients(request, pk):
    patient = Patients.objects.get(id_id = pk)
    patient.delete()

    return Response("data deleted")


################UsersDetaileds###################################################################################################


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes((IsAuthenticated, ))
def getUsersDetaileds(request):
    usersDetaileds = UsersDetaileds.objects.all()
    serializer = UsersDetailedsSerializer(usersDetaileds, many = True)
    return Response(serializer.data)

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes((IsAuthenticated, ))
def getUsersDetailed(request, pk):
    usersDetailed = UsersDetaileds.objects.get(id_id = pk)
    serializer = UsersDetailedsSerializer(usersDetailed, many = False,)
    return Response(serializer.data)

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes((IsAuthenticated, ))
def createUsersDetailedFile(request):
    data = request.data
    userr = User.objects.get(id = data['userCreatorId'])
    
    usersDetailed = UsersDetaileds.objects.create(
        id_id = data['id_id'],
        isempty = data['isempty'],
        userCreatorId = data['userCreatorId'],
        user = userr,
        name =    data['name'],
        userName = data['userName'],
        image_loc =    data['image_loc'],
        other_1 = data['other_1'],
        other_2 = data['other_2'],
        other_3 = data['other_3'],
        user_Main_Img = request.FILES['file'],
    )
    serializer = UsersDetailedsSerializer(usersDetailed, many = False)
    return Response(serializer.data)


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes((IsAuthenticated, ))
def createUsersDetailed(request):
    data = request.data
    userr = User.objects.get(id = data['userCreatorId'])
    
    usersDetailed = UsersDetaileds.objects.create(
        id_id = data['id_id'],
        isempty = data['isempty'],
        userCreatorId = data['userCreatorId'],
        user = userr,
        name =    data['name'],
        image_loc =    data['image_loc'],
        other_1 = data['other_1'],
        other_2 = data['other_2'],
        other_3 = data['other_3'],
    )
    serializer = UsersDetailedsSerializer(usersDetailed, many = False)
    return Response(serializer.data)

@api_view(['PUT'])
@authentication_classes([TokenAuthentication])
@permission_classes((IsAuthenticated, ))
def updateUsersDetaileds(request, pk):
    data = request.data
    
    usersDetailed = UsersDetaileds.objects.get(id_id = pk)
    serializer = UsersDetailedsSerializer(usersDetailed, data = request.data)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)

@api_view(['PUT'])
@authentication_classes([TokenAuthentication])
@permission_classes((IsAuthenticated, ))
def updateUsersDetailedsFile(request, pk):
    data = request.data
    
    usersDetailed = UsersDetaileds.objects.get(id_id = pk)
    usersDetailed.sample_Main_Img = request.FILES['file']
    serializer = UsersDetailedsSerializer(usersDetailed, data = request.data)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)

@api_view(['DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes((IsAuthenticated, ))
def deleteUsersDetaileds(request, pk):
    usersDetailed = UsersDetaileds.objects.get(id_id = pk)
    usersDetailed.delete()

    return Response("data deleted")



################SampleList###################################################################################################


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes((IsAuthenticated, ))
def getSampleLists(request):
    sampleLists = SampleLists.objects.all()
    serializer = SampleListsSerializer(sampleLists, many = True)
    return Response(serializer.data)

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes((IsAuthenticated, ))
def getSampleList(request, pk):
    sampleList = SampleLists.objects.get(id_id = pk)
    serializer = SampleListsSerializer(sampleList, many = False,)
    return Response(serializer.data)

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes((IsAuthenticated, ))
def createSampleList(request):
    data = request.data
    userr = User.objects.get(id = data['userCreatorId'])
    
    sampleList = SampleLists.objects.create(
        id_id = data['id_id'],
        user = userr,
        name = data['name'],
        #userCreatorName = data['userCreatorName'],
        jsonList = data['jsonList'],
        
        date_created = data['date_created'],
    )
    serializer = SampleListsSerializer(sampleList, many = False)
    return Response(serializer.data)

@api_view(['PUT'])
@authentication_classes([TokenAuthentication])
@permission_classes((IsAuthenticated, ))
def updateSampleLists(request, pk):
    data = request.data
    
    sampleList = SampleLists.objects.get(id_id = pk)
    serializer = SampleListsSerializer(sampleList, data = request.data)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)

@api_view(['DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes((IsAuthenticated, ))
def deleteSampleLists(request, pk):
    sampleList = SampleLists.objects.get(id_id = pk)
    sampleList.delete()

    return Response("data deleted")


################Sample###################################################################################################

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes((IsAuthenticated, ))
def getSamples(request):
    samples = Samples.objects.all().order_by('-sample_date')
    serializer = SamplesSerializer(samples, many = True)
    return Response(serializer.data)

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes((IsAuthenticated, ))
def getSample(request, pk):
    samples = Samples.objects.get(id_id = pk)
    serializer = SamplesSerializer(samples, many = False,)
    return Response(serializer.data)

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes((IsAuthenticated, ))
def getSamplesReceived(request, pk):
    samples_recieved = list(Samples.objects.filter(receiver_lab = pk).order_by('-sample_date'))
    serializer = SamplesSerializer(samples_recieved, many = True,)
    return Response(serializer.data)


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes((IsAuthenticated, ))
def getSampleWithPatient(request, pk):
    pati = Patients.objects.get(id_id = pk)
    samples = list(Samples.objects.filter(patient = pati).order_by('-sample_date'))
    serializer = SamplesSerializer(samples, many = True,)
    return Response(serializer.data)


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes((IsAuthenticated, ))
def getSamplesSent(request, pk):
    samples_sent = list(Samples.objects.filter(origin_lab = pk).order_by('-sample_date'))
    serializer = SamplesSerializer(samples_sent, many = True,)
    return Response(serializer.data)



@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes((IsAuthenticated, ))
def getSampleInfo(request, pk):
    samples_recieved = list(Samples.objects.filter(receiver_lab = pk).order_by('-sample_date'))

    samples_sent = list(Samples.objects.filter(origin_lab = pk))
    class SampleInfo:
        def __init__(self, samples_received, samples_sent, ):
            self.samples_received = samples_received
            self.samples_sent = samples_sent

    sampleInfo = SampleInfo(samples_received=len(samples_recieved), samples_sent=len(samples_sent))
    
    serializer = SampleInfoSerializer(sampleInfo)
    
    return Response(serializer.data)

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes((IsAuthenticated, ))
def createSamples(request):
    data = request.data
    pati = Patients.objects.get(id_id = data['patientId'])
    
    samples = Samples.objects.create(
        id_id = data['id_id'],
        userCreatorId = data['userCreatorId'],
        patient = pati,
        kodmeli = data['kodmeli'],
        name = data['name'],
        surname = data['surname'],
        sample_code = data['sample_code'],
        gender = data['gender'],
        birth = data['birth'],
        is_imported = data['is_imported'],
        sample_date = data['sample_date'],
        expected_result_date = data['expected_result_date'],
        result_date = data['result_date'],
        origin_lab = data['origin_lab'],
        is_sent = data['is_sent'],
        is_received = data['is_received'],
        is_reported = data['is_reported'],
        file_name = data['file_name'],
        is_started = data['is_started'],
        is_confirmed = data['is_confirmed'],
        receiver_lab = data['receiver_lab'],
        emergent_status = data['emergent_status'],
        sample_hour = data['sample_hour'],
        result_hour = data['result_hour'],
        patientId = data['patientId'],
        history = data['history'],
        phone_number = data['phone_number'],
        sample_type = data['sample_type'],
        history_file_name = data['history_file_name'],
        
     )
    serializer = SamplesSerializer(samples, many = False)
    return Response(serializer.data)

@api_view(['PUT'])
@authentication_classes([TokenAuthentication])
@permission_classes((IsAuthenticated, ))
def updateSamples(request, pk):
    data = request.data
    
    samples = Samples.objects.get(id_id = pk)
    serializer = SamplesSerializer(samples, data = request.data)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)

@api_view(['DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes((IsAuthenticated, ))
def deleteSamples(request, pk):
    samples = Samples.objects.get(id_id = pk)
    samples.delete()

    return Response("data deleted")







# ###############TestInfo###################################################################################################

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes((IsAuthenticated, ))
def getTestInfos(request):
    testInfos = TestInfos.objects.all()
    serializer = TestInfosSerializer(testInfos, many = True)
    return Response(serializer.data)

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes((IsAuthenticated, ))
def getTestInfo(request, pk):
    testInfos = TestInfos.objects.get(id_id = pk)
    serializer = TestInfosSerializer(testInfos, many = False,)
    return Response(serializer.data)

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes((IsAuthenticated, ))
def createTestInfos(request):
    data = request.data
 
    testInfos = TestInfos.objects.create(
        id_id = data['id_id'],
        group = data['group'],
        testCode = data['testCode'],
        testName = data['testName'],
        description = data['description'],
        unit = data['unit'],
        normal_range = data['normal_range'],
        k_total = data['k_total'],
        k_fani = data['k_fani'],
        k_herfe = data['k_herfe'],
        testCost1 = data['testCost1'],
        testCost2 = data['testCost2'],
        testCost3 = data['testCost3'],
        testCost4 = data['testCost4'],
     )
    serializer = TestInfosSerializer(testInfos, many = False)
    return Response(serializer.data)

@api_view(['PUT'])
@authentication_classes([TokenAuthentication])
@permission_classes((IsAuthenticated, ))
def updateTestInfos(request, pk):
    data = request.data
    
    testInfos = TestInfos.objects.get(id_id = pk)
    serializer = TestInfosSerializer(testInfos, data = request.data)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)

@api_view(['DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes((IsAuthenticated, ))
def deleteTestInfos(request, pk):
    testInfos = TestInfos.objects.get(id_id = pk)
    testInfos.delete()

    return Response("data deleted")



# ###############TestResult###################################################################################################


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes((IsAuthenticated, ))
def getTestResults(request):
    testResults = TestResults.objects.all()
    serializer = TestResultsSerializer(testResults, many = True)
    return Response(serializer.data)

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes((IsAuthenticated, ))
def getTestResult(request, pk):
    testResults = TestResults.objects.get(id_id = pk)
    serializer = TestResultsSerializer(testResults, many = False,)
    return Response(serializer.data)

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes((IsAuthenticated, ))
def getTestResultWithSample(request, pk):
    pati = Samples.objects.get(id_id = pk)
    testResultd = list(TestResults.objects.filter(patient = pati))
    serializer = TestResultsSerializer(testResultd, many = True,)
    return Response(serializer.data)

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes((IsAuthenticated, ))
def createTestResults(request):
    data = request.data
    pati = Samples.objects.get(id_id = data['sampleId'])
    testResults = TestResults.objects.create(
        sampleCode = data['sampleCode'],
        patient = pati,
        id_id = data['id_id'],
        testCode = data['testCode'],
        testResult = data['testResult'],
        dateReceived = data['dateReceived'],
        dateResultExpect = data['dateResultExpect'],
        dateResultSent = data['dateResultSent'],
        sampleId = data['sampleId'],
        testMethod = data['testMethod'],
        )
    serializer = TestResultsSerializer(testResults, many = False)
    return Response(serializer.data)

@api_view(['PUT'])
@authentication_classes([TokenAuthentication])
@permission_classes((IsAuthenticated, ))
def updateTestResults(request, pk):
    data = request.data
    
    testResults = TestResults.objects.get(id_id = pk)
    serializer = TestResultsSerializer(testResults, data = request.data)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)

@api_view(['DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes((IsAuthenticated, ))
def deleteTestResults(request, pk):
    testResults = TestResults.objects.get(id_id = pk)
    testResults.delete()

    return Response("data deleted")



# ###############FileTables###################################################################################################

parser_classes = (MultiPartParser, FormParser)
class FileView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        file_serializer = FileSerializer(data=request.data)
        if file_serializer.is_valid():
            file_serializer.save()
            return Response(file_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
def getim(request):
    file_serializer = FileSerializer(data=request.data)
    if file_serializer.is_valid():
        file_serializer.save()
        return Response(file_serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@csrf_exempt
@authentication_classes([TokenAuthentication])
@permission_classes((IsAuthenticated, ))
def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            form.save
            return Response(form.fields)
            #return Response(form.data)#HttpResponseRedirect('/success/url/')
        

    else:
        form = UploadFileForm()
    return Response(form.data)#render(request, 'upload.html', {'form': form})

def model_form_upload(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return Response(form.data)
    else:
        form = DocumentForm()
    return Response(form.data)


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes((IsAuthenticated, ))
def getFileTables(request):
    fileTables = FileTables.objects.all()
    serializer = FileSerializer(fileTables, many = True)
    return Response(serializer.data)

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes((IsAuthenticated, ))
def getFileTable(request, pk):
    fileTables = FileTables.objects.get(id_id = pk)
    serializer = FileSerializer(fileTables, many = False,)
    return Response(serializer.data)

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes((IsAuthenticated, ))
def getFileWithSample(request, pk):
    pati = Samples.objects.get(id_id = pk)
    filetable = list(FileTables.objects.filter(sample = pati))
    serializer = FileSerializer(filetable, many = True,)
    return Response(serializer.data)


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes((IsAuthenticated, ))
def createFileTable(request):
    data = request.data
    pati = Samples.objects.get(id_id = data['userCreatorId'])
    fileTables = FileTables.objects.create(
        id_id = data['id_id'],
        isempty = data['isempty'],
        userCreatorId = data['userCreatorId'],
        sample = pati,
        use_case = data['use_case'],
        # kodmeli =    data['kodmeli'],
        # name =    data['name'],
        # surname =    data['surname'],
        file_date =    data['file_date'],
        file_loc = data['file_loc'],
        sample_Main_Img = request.FILES['file'],
    )
    serializer = FileSerializer(fileTables, many = False)
    return Response(serializer.data)

@api_view(['PUT'])
@authentication_classes([TokenAuthentication])
@permission_classes((IsAuthenticated, ))
def updateFileTables(request, pk):
    data = request.data
    
    fileTables = FileTables.objects.get(id_id = pk)
    fileTables.sample_Main_Img = request.FILES['file']
    serializer = FileSerializer(fileTables, data = request.data,)
   #  serializer.image_url = request.FILES['file']

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)

@api_view(['DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes((IsAuthenticated, ))
def deleteFileTables(request, pk):
    fileTables = FileTables.objects.get(id_id = pk)
    fileTables.delete()

    return Response("data deleted")


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes((IsAuthenticated, ))
def createFileTableExcel(request):
    data = request.data
    pati = Samples.objects.get(id_id = data['userCreatorId'])
    fileTables = FileTables.objects.create(
        id_id = data['id_id'],
        isempty = data['isempty'],
        userCreatorId = data['userCreatorId'],
        sample = pati,
        use_case = data['use_case'],
        # kodmeli =    data['kodmeli'],
        # name =    data['name'],
        # surname =    data['surname'],
        file_date =    data['file_date'],
        file_loc = data['file_loc'],
        sample_Main_Img = request.FILES['file'],
    )
    

    new_file = FileTables.objects.get(id_id = data['id_id']) 
    venv_python = '/usr/local/bin/python3.10'

    script_path = '/Users/macbookpro/nigeb_server/api/test_import.py'
    input_value = new_file.sample_Main_Img.name

    subprocess.run([venv_python,script_path,input_value])
    
    
    serializer = FileSerializer(fileTables, many = False)
    return Response(serializer.data)
# # @authentication_classes([TokenAuthentication])
# # @permission_classes((IsAuthenticated, ))
# def serve_protected_document(request, file):
#     document = get_object_or_404(FileTables, file_loc= file)
#     path, file_name = os.path.split(file)
#     response = HttpResponse()
#     response["Content-Disposition"] = f"attachment; filename= {file_name}"
#     response["X-Accel-Redirect"] =  document.name  # Path to the file
#     return response


# ###############CONSTANT###################################################################################################
# @api_view(['GET'])
# @authentication_classes([TokenAuthentication])
# @permission_classes((IsAuthenticated, ))
# def getConstants(request):
#     constant = ConstantTables.objects.all()
#     serializer = ConstantTablesSerializer(constant, many = True)
#     return Response(serializer.data)

# @api_view(['GET'])
# @authentication_classes([TokenAuthentication])
# @permission_classes((IsAuthenticated, ))
# def getConstant(request, pk):
#     constant = ConstantTables.objects.get(id_id = pk)
#     serializer = ConstantTablesSerializer(constant, many = False,)
#     return Response(serializer.data)

# @api_view(['POST'])
# @authentication_classes([TokenAuthentication])
# @permission_classes((IsAuthenticated, ))
# def createConstants(request):
#     data = request.data
#     pati = Patients.objects.get(id_id = data['userCreatorId'])

#     constant = ConstantTables.objects.create(
#         id_id = data['id_id'],
#         isempty = data['isempty'],
#         userCreatorId = data['userCreatorId'],
#         patient = pati,
#         kodmeli =    data['kodmeli'],
#         name =    data['name'],
#         surname =    data['surname'],
#         date =    data['date'],
#         #time =    data['time'],
#         pain =    data['pain'],
#         armposi =    data['armposi'],
#         strenabd =    data['strenabd'],
#         ffrom =    data['ffrom'],
#         lerom =    data['lerom'],
#         errom =    data['errom'],
#         irrom =    data['irrom'],
#         int_armposi = data['int_armposi'],
#         int_strenabd = data['int_strenabd'],
#         int_ffrom = data['int_ffrom'],
#         int_lerom = data['int_lerom'],
#         int_errom = data['int_errom'],
#         int_irrom = data['int_irrom'],
#         #int_pain = data['int_pain'],
#         int_activity_sleep =    data['int_activity_sleep'],
#         int_activity_sport =    data['int_activity_sport'],
#         int_activity_work =    data['int_activity_work'],
#         #constant_score = data['constant_score'],
#     )
#     serializer = ConstantTablesSerializer(constant, many = False)
#     return Response(serializer.data)

# @api_view(['PUT'])
# @authentication_classes([TokenAuthentication])
# @permission_classes((IsAuthenticated, ))
# def updateConstants(request, pk):
#     data = request.data
    
#     constant = ConstantTables.objects.get(id_id = pk)
#     serializer = ConstantTablesSerializer(constant, data = request.data)

#     if serializer.is_valid():
#         serializer.save()

#     return Response(serializer.data)

# @api_view(['DELETE'])
# @authentication_classes([TokenAuthentication])
# @permission_classes((IsAuthenticated, ))
# def deleteConstants(request, pk):
#     constant = ConstantTables.objects.get(id_id = pk)
#     constant.delete()

#     return Response("data deleted")




# ###############DashTables##############################################################################################
# @api_view(['GET'])
# @authentication_classes([TokenAuthentication])
# @permission_classes((IsAuthenticated, ))
# def getDashTables(request):
#     dashTables = DashTables.objects.all()
#     serializer = DashTablesSerializer(dashTables, many = True)
#     return Response(serializer.data)

# @api_view(['GET'])
# @authentication_classes([TokenAuthentication])
# @permission_classes((IsAuthenticated, ))
# def getDashTable(request, pk):
#     dashTables = DashTables.objects.get(id_id = pk)
#     serializer = DashTablesSerializer(dashTables, many = False,)
#     return Response(serializer.data)

# @api_view(['POST'])
# @authentication_classes([TokenAuthentication])
# @permission_classes((IsAuthenticated, ))
# def createDashTables(request):
#     data = request.data
#     pati = Patients.objects.get(id_id = data['userCreatorId'])
#     dashTables = DashTables.objects.create(
#         id_id = data['id_id'],
#         isempty = data['isempty'],
#         userCreatorId = data['userCreatorId'],
#         patient = pati,
#         kodmeli =    data['kodmeli'],
#         name =    data['name'],
#         surname =    data['surname'],
#         dash_score = data['dash_score'],
#         ghuti = data['ghuti'],
#         ruzmar = data['ruzmar'],
#         kif = data['kif'],
#         posht = data['posht'],
#         chaghu = data['chaghu'],
#         tafrih = data['tafrih'],
#         ejtema = data['ejtema'],
#         kar = data['kar'],
#         dard_bazu = data['dard_bazu'],
#         gezgez = data['gezgez'],
#         khab = data['khab'],
#         dash_date =    data['dash_date'],
#         #dash_time =    data['dash_time'],
#     )
#     serializer = DashTablesSerializer(dashTables, many = False)
#     return Response(serializer.data)

# @api_view(['PUT'])
# @authentication_classes([TokenAuthentication])
# @permission_classes((IsAuthenticated, ))
# def updateDashTables(request, pk):
#     data = request.data
    
#     dashTables = DashTables.objects.get(id_id = pk)
#     serializer = DashTablesSerializer(dashTables, data = request.data)

#     if serializer.is_valid():
#         serializer.save()

#     return Response(serializer.data)

# @api_view(['DELETE'])
# @authentication_classes([TokenAuthentication])
# @permission_classes((IsAuthenticated, ))
# def deleteDashTables(request, pk):
#     dashTables = DashTables.objects.get(id_id = pk)
#     dashTables.delete()

#     return Response("data deleted")


# ###############HarisTables###################################################################################################
# @api_view(['GET'])
# @authentication_classes([TokenAuthentication])
# @permission_classes((IsAuthenticated, ))
# def getHarisTables(request):
#     harisTables = HarisTables.objects.all()
#     serializer = HarisTablesSerializer(harisTables, many = True)
#     return Response(serializer.data)

# @api_view(['GET'])
# @authentication_classes([TokenAuthentication])
# @permission_classes((IsAuthenticated, ))
# def getHarisTable(request, pk):
#     harisTables = HarisTables.objects.get(id_id = pk)
#     serializer = HarisTablesSerializer(harisTables, many = False,)
#     return Response(serializer.data)

# @api_view(['POST'])
# @authentication_classes([TokenAuthentication])
# @permission_classes((IsAuthenticated, ))
# def createHarisTables(request):
#     data = request.data
#     pati = Patients.objects.get(id_id = data['userCreatorId'])
#     harisTables = HarisTables.objects.create(
#         id_id = data['id_id'],
#         isempty = data['isempty'],
#         userCreatorId = data['userCreatorId'],
#         patient = pati,
#         kodmeli =    data['kodmeli'],
#         name =    data['name'],
#         surname =    data['surname'],
#         date =    data['date'],
#         #time =    data['time'],
#         seco_pain = data['seco_pain'],
#         seco_dist_walk = data['seco_dist_walk'],
#         seco_activities =    data['seco_activities'],
#         seco_pub_trans =    data['seco_pub_trans'],
#         seco_support = data['seco_support'],
#         seco_limb =    data['seco_limb'],
#         seco_stair =    data['seco_stair'],
#         seco_sitting =    data['seco_sitting'],
#         sect_flec = data['sect_flec'],
#         sect_add = data['sect_add'],
#         sect_rot = data['sect_rot'],
#         sect_length = data['sect_length'],
#         sectr_fdegree = data['sectr_fdegree'],
#         sectr_abdegree = data['sectr_abdegree'],
#         sectr_exrdegree = data['sectr_exrdegree'],
#         sectr_addegre = data['sectr_addegre'],
#         string_sectr_fdegree =    data['string_sectr_fdegree'],
#         string_sectr_abdegree =    data['string_sectr_abdegree'],
#         string_sectr_exrdegree =    data['string_sectr_exrdegree'],
#         string_sectr_addegre =    data['string_sectr_addegre'],
#         string_seco_pain =    data['string_seco_pain'],
#         string_seco_dist_walk =    data['string_seco_dist_walk'],
#         string_seco_supp =    data['string_seco_supp'],
#         #hipscore = data['hipscore'],
#     )
#     serializer = HarisTablesSerializer(harisTables, many = False)
#     return Response(serializer.data)

# @api_view(['PUT'])
# @authentication_classes([TokenAuthentication])
# @permission_classes((IsAuthenticated, ))
# def updateHarisTables(request, pk):
#     data = request.data
    
#     harisTables = HarisTables.objects.get(id_id = pk)
#     serializer = HarisTablesSerializer(harisTables, data = request.data)

#     if serializer.is_valid():
#         serializer.save()

#     return Response(serializer.data)

# @api_view(['DELETE'])
# @authentication_classes([TokenAuthentication])
# @permission_classes((IsAuthenticated, ))
# def deleteHarisTables(request, pk):
#     harisTables = HarisTables.objects.get(id_id = pk)
#     harisTables.delete()

#     return Response("data deleted")



# ###############SFTables###################################################################################################
# @api_view(['GET'])
# @authentication_classes([TokenAuthentication])
# @permission_classes((IsAuthenticated, ))
# def getSFTables(request):
#     sFTables = SFTables.objects.all()
#     serializer = SFTablesSerializer(sFTables, many = True)
#     return Response(serializer.data)

# @api_view(['GET'])
# @authentication_classes([TokenAuthentication])
# @permission_classes((IsAuthenticated, ))
# def getSFTable(request, pk):
#     sFTables = SFTables.objects.get(id_id = pk)
#     serializer = SFTablesSerializer(sFTables, many = False,)
#     return Response(serializer.data)

# @api_view(['POST'])
# @authentication_classes([TokenAuthentication])
# @permission_classes((IsAuthenticated, ))
# def createSFTables(request):
#     data = request.data
#     pati = Patients.objects.get(id_id = data['userCreatorId'])
#     sFTables = SFTables.objects.create(
#         id_id = data['id_id'],
#         isempty = data['isempty'],
#         userCreatorId = data['userCreatorId'],
#         patient = pati,
#         kodmeli =    data['kodmeli'],
#         name =    data['name'],
#         surname =    data['surname'],
#         date =    data['date'],
#         #time =    data['time'],
#         koli =    data['koli'],
#         #integer_koli = data['integer_koli'],
#         mogha =    data['mogha'],
#         integer_mogha = data['integer_mogha'],
#         rozan_shad = data['rozan_shad'],
#         rozan_motev = data['rozan_motev'],
#         rozan_kharid = data['rozan_kharid'],
#         rozan_chand_pele = data['rozan_chand_pele'],
#         rozan_yek_pele = data['rozan_yek_pele'],
#         rozan_kham = data['rozan_kham'],
#         rozan_piade_km = data['rozan_piade_km'],
#         rozan_piade_chandsad = data['rozan_piade_chandsad'],
#         rozan_piade_sad = data['rozan_piade_sad'],
#         rozan_hamum = data['rozan_hamum'],
#         jesm_kar_kam =    data['jesm_kar_kam'],
#         jesm_kamtar_vaght =    data['jesm_kamtar_vaght'],
#         jesm_khas =    data['jesm_khas'],
#         jesm_adi =    data['jesm_adi'],
#         ravani_kar_kam =    data['ravani_kar_kam'],
#         ravani_kamtar_vaght =    data['ravani_kamtar_vaght'],
#         ravani_deghat =    data['ravani_deghat'],
#         integer_ravani_ekhtelal = data['integer_ravani_ekhtelal'],
#         ravani_ekhtelal =    data['ravani_ekhtelal'],
#         integer_dard = data['integer_dard'],
#         dard =    data['dard'],
#         integer_dard_mane = data['integer_dard_mane'],
#         dard_mane =    data['dard_mane'],
#         nazdik_rohie = data['nazdik_rohie'],
#         nazdik_asabi = data['nazdik_asabi'],
#         nazdik_asabi_nakhosh = data['nazdik_asabi_nakhosh'],
#         nazdik_aramesh = data['nazdik_aramesh'],
#         nazdik_energy = data['nazdik_energy'],
#         nazdik_farsude = data['nazdik_farsude'],
#         nazdik_gham = data['nazdik_gham'],
#         nazdik_khosh = data['nazdik_khosh'],
#         nazdik_khaste = data['nazdik_khaste'],
#         integer_jesmi_va_atefi = data['integer_jesmi_va_atefi'],
#         jesmi_va_atefi =    data['jesmi_va_atefi'],
#         sadegh_zood = data['sadegh_zood'],
#         sadegh_salamt_darhad = data['sadegh_salamt_darhad'],
#         sadegh_badtar = data['sadegh_badtar'],
#         sadegh_ali = data['sadegh_ali'],
#     )
#     serializer = SFTablesSerializer(sFTables, many = False)
#     return Response(serializer.data)

# @api_view(['PUT'])
# @authentication_classes([TokenAuthentication])
# @permission_classes((IsAuthenticated, ))
# def updateSFTables(request, pk):
#     data = request.data
    
#     sFTables = SFTables.objects.get(id_id = pk)
#     serializer = SFTablesSerializer(sFTables, data = request.data)

#     if serializer.is_valid():
#         serializer.save()

#     return Response(serializer.data)

# @api_view(['DELETE'])
# @authentication_classes([TokenAuthentication])
# @permission_classes((IsAuthenticated, ))
# def deleteSFTables(request, pk):
#     sFTables = SFTables.objects.get(id_id = pk)
#     sFTables.delete()

#     return Response("data deleted")



# ###############VASTables###################################################################################################
# @api_view(['GET'])
# @authentication_classes([TokenAuthentication])
# @permission_classes((IsAuthenticated, ))
# def getVASTables(request):
#     patients = VASTables.objects.all()
#     serializer = VASTablesSerializer(patients, many = True)
#     return Response(serializer.data)

# @api_view(['GET'])
# @authentication_classes([TokenAuthentication])
# @permission_classes((IsAuthenticated, ))
# def getVASTable(request, pk):
#     vASTables = VASTables.objects.get(id_id = pk)
#     serializer = VASTablesSerializer(vASTables, many = False,)
#     return Response(serializer.data)

# @api_view(['POST'])
# @authentication_classes([TokenAuthentication])
# @permission_classes((IsAuthenticated, ))
# def createVASTables(request):
#     data = request.data
#     pati = Patients.objects.get(id_id = data['userCreatorId'])
#     vASTables = VASTables.objects.create(
#         id_id = data['id_id'],
#         isempty = data['isempty'],
#         userCreatorId = data['userCreatorId'],
#         patient = pati,
#         kodmeli =    data['kodmeli'],
#         name =    data['name'],
#         surname =    data['surname'],
#         vas_score = data['vas_score'],
#         vas_date =    data['vas_date'],
#         #vas_time =    data['vas_time'],
#     )
#     serializer = VASTablesSerializer(vASTables, many = False)
#     return Response(serializer.data)

# @api_view(['PUT'])
# @authentication_classes([TokenAuthentication])
# @permission_classes((IsAuthenticated, ))
# def updateVASTables(request, pk):
#     data = request.data
    
#     vASTables = VASTables.objects.get(id_id = pk)
#     serializer = VASTablesSerializer(vASTables, data = request.data)

#     if serializer.is_valid():
#         serializer.save()

#     return Response(serializer.data)

# @api_view(['DELETE'])
# @authentication_classes([TokenAuthentication])
# @permission_classes((IsAuthenticated, ))
# def deleteVASTables(request, pk):
#     vASTables = VASTables.objects.get(id_id = pk)
#     vASTables.delete()

#     return Response("data deleted")



# ###############TreatmentTables###################################################################################################
# @api_view(['GET'])
# @authentication_classes([TokenAuthentication])
# @permission_classes((IsAuthenticated, ))
# def getTreatmentTables(request):
#     treatmentTables = TreatmentTables.objects.all()
#     serializer = TreatmentTablesSerializer(treatmentTables, many = True)
#     return Response(serializer.data)

# @api_view(['GET'])
# @authentication_classes([TokenAuthentication])
# @permission_classes((IsAuthenticated, ))
# def getTreatmentTable(request, pk):
#     treatmentTables = TreatmentTables.objects.get(id_id = pk)
#     serializer = TreatmentTablesSerializer(treatmentTables, many = False,)
#     return Response(serializer.data)

# @api_view(['POST'])
# @authentication_classes([TokenAuthentication])
# @permission_classes((IsAuthenticated, ))
# def createTreatmentTables(request):
#     data = request.data
#     pati = Patients.objects.get(id_id = data['userCreatorId'])
#     treatmentTables = TreatmentTables.objects.create(
#         id_id = data['id_id'],
#         isempty = data['isempty'],
#         userCreatorId = data['userCreatorId'],
#         patient = pati,
#         kodmeli =    data['kodmeli'],
#         name =    data['name'],
#         surname =    data['surname'],
#         treat_date =    data['treat_date'],
#         treat_non = data['treat_non'],
#         treat_hip_external = data['treat_hip_external'],
#         treat_hip_orif_dyn = data['treat_hip_orif_dyn'],
#         treat_hip_orif_cond =    data['treat_hip_orif_cond'],
#         treat_hip_orif_anat =    data['treat_hip_orif_anat'],
#         treat_hip_orif_cephal =    data['treat_hip_orif_cephal'],
#         treat_arthro = data['treat_arthro'],
#         treat_humer_crif = data['treat_humer_crif'],
#         treat_humer_orif_pin =    data['treat_humer_orif_pin'],
#         treat_humer_orif_plate =    data['treat_humer_orif_plate'],
#         treat_dist_crif_pin =    data['treat_dist_crif_pin'],
#         treat_dist_crif_external =    data['treat_dist_crif_external'],
#         treat_dist_orif = data['treat_dist_orif'],
#         treat_dist_pin = data['treat_dist_pin'],
#         surgen =    data['surgen'],
#         surgen_name =    data['surgen_name'],
#         lot_num = data['lot_num'],
#         ref_num = data['ref_num'],
#         irc_num = data['irc_num'],
#     )
#     serializer = TreatmentTablesSerializer(treatmentTables, many = False)
#     return Response(serializer.data)

# @api_view(['PUT'])
# @authentication_classes([TokenAuthentication])
# @permission_classes((IsAuthenticated, ))
# def updateTreatmentTables(request, pk):
#     data = request.data
    
#     treatmentTables = TreatmentTables.objects.get(id_id = pk)
#     serializer = TreatmentTablesSerializer(treatmentTables, data = request.data)

#     if serializer.is_valid():
#         serializer.save()

#     return Response(serializer.data)

# @api_view(['DELETE'])
# @authentication_classes([TokenAuthentication])
# @permission_classes((IsAuthenticated, ))
# def deleteTreatmentTables(request, pk):
#     treatmentTables = TreatmentTables.objects.get(id_id = pk)
#     treatmentTables.delete()

#     return Response("data deleted")



# ###############ImagingTables###################################################################################################
# parser_classes = (MultiPartParser, FormParser)
# class FileView(APIView):
#     parser_classes = (MultiPartParser, FormParser)

#     def post(self, request, *args, **kwargs):
#         file_serializer = ImagingTablesSerializer(data=request.data)
#         if file_serializer.is_valid():
#             file_serializer.save()
#             return Response(file_serializer.data, status=status.HTTP_201_CREATED)
#         else:
#             return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# def getim(request):
#     file_serializer = ImagingTablesSerializer(data=request.data)
#     if file_serializer.is_valid():
#         file_serializer.save()
#         return Response(file_serializer.data, status=status.HTTP_201_CREATED)
#     else:
#         return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# @api_view(['POST'])
# @csrf_exempt
# @authentication_classes([TokenAuthentication])
# @permission_classes((IsAuthenticated, ))
# def upload_file(request):
#     if request.method == 'POST':
#         form = UploadFileForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save
#             return Response(form.fields)
#             #return Response(form.data)#HttpResponseRedirect('/success/url/')
        

#     else:
#         form = UploadFileForm()
#     return Response(form.data)#render(request, 'upload.html', {'form': form})

# def model_form_upload(request):
#     if request.method == 'POST':
#         form = DocumentForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return Response(form.data)
#     else:
#         form = DocumentForm()
#     return Response(form.data)


# @api_view(['GET'])
# @authentication_classes([TokenAuthentication])
# @permission_classes((IsAuthenticated, ))
# def getImagingTables(request):
#     imagingTables = ImagingTables.objects.all()
#     serializer = ImagingTablesSerializer(imagingTables, many = True)
#     return Response(serializer.data)

# @api_view(['GET'])
# @authentication_classes([TokenAuthentication])
# @permission_classes((IsAuthenticated, ))
# def getImagingTable(request, pk):
#     imagingTables = ImagingTables.objects.get(id_id = pk)
#     serializer = ImagingTablesSerializer(imagingTables, many = False,)
#     return Response(serializer.data)

# @api_view(['POST'])
# @authentication_classes([TokenAuthentication])
# @permission_classes((IsAuthenticated, ))
# def createImagingTable(request):
#     data = request.data
#     pati = Patients.objects.get(id_id = data['userCreatorId'])
#     imagingTables = ImagingTables.objects.create(
#         id_id = data['id_id'],
#         isempty = data['isempty'],
#         userCreatorId = data['userCreatorId'],
#         patient = pati,
#         # kodmeli =    data['kodmeli'],
#         # name =    data['name'],
#         # surname =    data['surname'],
#         # image_date =    data['image_date'],
#         image_loc = data['image_loc'],
#         patient_Main_Img = request.FILES['file'],
#     )
#     serializer = ImagingTablesSerializer(imagingTables, many = False)
#     return Response(serializer.data)

# @api_view(['PUT'])
# @authentication_classes([TokenAuthentication])
# @permission_classes((IsAuthenticated, ))
# def updateImagingTables(request, pk):
#     data = request.data
    
#     imagingTables = ImagingTables.objects.get(id_id = pk)
#     imagingTables.patient_Main_Img = request.FILES['file']
#     serializer = ImagingTablesSerializer(imagingTables, data = request.data,)
#    #  serializer.image_url = request.FILES['file']

#     if serializer.is_valid():
#         serializer.save()

#     return Response(serializer.data)

# @api_view(['DELETE'])
# @authentication_classes([TokenAuthentication])
# @permission_classes((IsAuthenticated, ))
# def deleteImagingTables(request, pk):
#     imagingTables = ImagingTables.objects.get(id_id = pk)
#     imagingTables.delete()

#     return Response("data deleted")

# #user registration 


# ###############InjuryTables###################################################################################################
# @api_view(['GET'])
# @authentication_classes([TokenAuthentication])
# @permission_classes((IsAuthenticated, ))
# def getInjuryTables(request):
#     injuryTables = InjuryTables.objects.all()
#     serializer = InjuryTablesSerializer(injuryTables, many = True)
#     return Response(serializer.data)

# @api_view(['GET'])
# @authentication_classes([TokenAuthentication])
# @permission_classes((IsAuthenticated, ))
# def getInjuryTable(request, pk):
#     injuryTables = InjuryTables.objects.get(id_id = pk)
#     serializer = InjuryTablesSerializer(injuryTables, many = False,)
#     return Response(serializer.data)

# @api_view(['POST'])
# @authentication_classes([TokenAuthentication])
# @permission_classes((IsAuthenticated, ))
# def createInjuryTables(request):
#     data = request.data
#     pati = Patients.objects.get(id_id = data['userCreatorId'])
#     injuryTables = InjuryTables.objects.create(
#         id_id = data['id_id'],
#         isempty = data['isempty'],
#         userCreatorId = data['userCreatorId'],
#         patient = pati,
#         kodmeli =    data['kodmeli'],
#         name =    data['name'],
#         surname =    data['surname'],
#         inj_type =    data['inj_type'],
#         inj_open =    data['inj_open'],
#         inj_side =    data['inj_side'],
#         int_inj_type =    data['int_inj_type'],
#         int_inj_open =    data['int_inj_open'],
#         int_inj_side =    data['int_inj_side'],

#     )
#     serializer = InjuryTablesSerializer(injuryTables, many = False)
#     return Response(serializer.data)

# @api_view(['PUT'])
# @authentication_classes([TokenAuthentication])
# @permission_classes((IsAuthenticated, ))
# def updateInjuryTables(request, pk):
#     data = request.data
    
#     injuryTables = InjuryTables.objects.get(id_id = pk)
#     serializer = InjuryTablesSerializer(injuryTables, data = request.data)

#     if serializer.is_valid():
#         serializer.save()

#     return Response(serializer.data)

# @api_view(['DELETE'])
# @authentication_classes([TokenAuthentication])
# @permission_classes((IsAuthenticated, ))
# def deleteInjuryTables(request, pk):
#     injuryTables = InjuryTables.objects.get(id_id = pk)
#     injuryTables.delete()

#     return Response("data deleted")




# ###############Followrads###################################################################################################
# @api_view(['GET'])
# @authentication_classes([TokenAuthentication])
# @permission_classes((IsAuthenticated, ))
# def getFollowrads(request):
#     followrads = Followrads.objects.all()
#     serializer = FollowradsSerializer(followrads, many = True)
#     return Response(serializer.data)

# @api_view(['GET'])
# @authentication_classes([TokenAuthentication])
# @permission_classes((IsAuthenticated, ))
# def getFollowrad(request, pk):
#     followrads = Followrads.objects.get(id_id = pk)
#     serializer = FollowradsSerializer(followrads, many = False,)
#     return Response(serializer.data)

# @api_view(['POST'])
# @authentication_classes([TokenAuthentication])
# @permission_classes((IsAuthenticated, ))
# def createFollowrads(request):
#     data = request.data
#     pati = Patients.objects.get(id_id = data['userCreatorId'])
#     followrads = Followrads.objects.create(
#         id_id = data['id_id'],
#         isempty = data['isempty'],
#         userCreatorId = data['userCreatorId'],
#         patient = pati,
#         kodmeli =    data['kodmeli'],
#         name =    data['name'],
#         surname =    data['surname'],
#         followdate =    data['followdate'],
#         #followtime =    data['followtime'],
#         inf_less = data['inf_less'],
#         inf_more = data['inf_more'],
#         non_uni = data['non_uni'],
#         non_uni_date =    data['non_uni_date'],
#         mal_uni = data['mal_uni'],
#         mal_uni_date =    data['mal_uni_date'],
#         fixf_less = data['fixf_less'],
#         fixf_more = data['fixf_more'],
#         exten = data['exten'],
#         flec =    data['flec'],
#         sup =    data['sup'],
#         pron =    data['pron'],
#         count_pain =    data['count_pain'],
#         sym_sen =    data['sym_sen'],
#         sym_vaso =    data['sym_vaso'],
#         sym_edem =    data['sym_edem'],
#         sym_motor =    data['sym_motor'],
#         si_sen =    data['si_sen'],
#         si_vaso =    data['si_vaso'],
#         si_edem =    data['si_edem'],
#         si_motor =    data['si_motor'],
#         diag =    data['diag'],
#     )
#     serializer = FollowradsSerializer(followrads, many = False)
#     return Response(serializer.data)

# @api_view(['PUT'])
# @authentication_classes([TokenAuthentication])
# @permission_classes((IsAuthenticated, ))
# def updateFollowrads(request, pk):
#     data = request.data
    
#     followrads = Followrads.objects.get(id_id = pk)
#     serializer = FollowradsSerializer(followrads, data = request.data)

#     if serializer.is_valid():
#         serializer.save()

#     return Response(serializer.data)

# @api_view(['DELETE'])
# @authentication_classes([TokenAuthentication])
# @permission_classes((IsAuthenticated, ))
# def deleteFollowrads(request, pk):
#     followrads = Followrads.objects.get(id_id = pk)
#     followrads.delete()

#     return Response("data deleted")




# ###############Followhums###################################################################################################
# @api_view(['GET'])
# @authentication_classes([TokenAuthentication])
# @permission_classes((IsAuthenticated, ))
# def getFollowhums(request):
#     followhums = Followhums.objects.all()
#     serializer = FollowhumsSerializer(followhums, many = True)
#     return Response(serializer.data)

# @api_view(['GET'])
# @authentication_classes([TokenAuthentication])
# @permission_classes((IsAuthenticated, ))
# def getFollowhum(request, pk):
#     followhums = Followhums.objects.get(id_id = pk)
#     serializer = FollowhumsSerializer(followhums, many = False,)
#     return Response(serializer.data)

# @api_view(['POST'])
# @authentication_classes([TokenAuthentication])
# @permission_classes((IsAuthenticated, ))
# def createFollowhums(request):
#     data = request.data
#     pati = Patients.objects.get(id_id = data['userCreatorId'])
#     followhums = Followhums.objects.create(
#         id_id = data['id_id'],
#         isempty = data['isempty'],
#         userCreatorId = data['userCreatorId'],
#         patient = pati,
#         kodmeli =    data['kodmeli'],
#         name =    data['name'],
#         surname =    data['surname'],
#         followdate =    data['followdate'],
#         #followtime =    data['followtime'],
#         inf_less = data['inf_less'],
#         inf_more = data['inf_more'],
#         non_uni = data['non_uni'],
#         non_uni_date =    data['non_uni_date'],
#         mal_uni = data['mal_uni'],
#         mal_uni_date =    data['mal_uni_date'],
#         fixf_less = data['fixf_less'],
#         fixf_more = data['fixf_more'],
#         exten =    data['exten'],
#         flec =    data['flec'],
#         introt =    data['introt'],
#         extrot =    data['extrot'],
#         elev =    data['elev'],
#         abd =    data['abd'],
#         froz =    data['froz'],
#     )
#     serializer = FollowhumsSerializer(followhums, many = False)
#     return Response(serializer.data)

# @api_view(['PUT'])
# @authentication_classes([TokenAuthentication])
# @permission_classes((IsAuthenticated, ))
# def updateFollowhums(request, pk):
#     data = request.data
    
#     followhums = Followhums.objects.get(id_id = pk)
#     serializer = FollowhumsSerializer(followhums, data = request.data)

#     if serializer.is_valid():
#         serializer.save()

#     return Response(serializer.data)

# @api_view(['DELETE'])
# @authentication_classes([TokenAuthentication])
# @permission_classes((IsAuthenticated, ))
# def deleteFollowhums(request, pk):
#     followhums = Followhums.objects.get(id_id = pk)
#     followhums.delete()

#     return Response("data deleted")




# ###############Followfems###################################################################################################
# @api_view(['GET'])
# @authentication_classes([TokenAuthentication])
# @permission_classes((IsAuthenticated, ))
# def getFollowfems(request):
#     followfems = Followfems.objects.all()
#     serializer = FollowfemsSerializer(followfems, many = True)
#     return Response(serializer.data)

# @api_view(['GET'])
# @authentication_classes([TokenAuthentication])
# @permission_classes((IsAuthenticated, ))
# def getFollowfem(request, pk):
#     followfems = Followfems.objects.get(id_id = pk)
#     serializer = FollowfemsSerializer(followfems, many = False,)
#     return Response(serializer.data)

# @api_view(['POST'])
# @authentication_classes([TokenAuthentication])
# @permission_classes((IsAuthenticated, ))
# def createFollowfems(request):
#     data = request.data
#     pati = Patients.objects.get(id_id = data['userCreatorId'])

#     followfems = Followfems.objects.create(
#         id_id = data['id_id'],
#         isempty = data['isempty'],
#         userCreatorId = data['userCreatorId'],
#         patient = pati,
#         kodmeli =    data['kodmeli'],
#         name =    data['name'],
#         surname =    data['surname'],
#         followdate =    data['followdate'],
#         #followtime =    data['followtime'],
#         inf_less = data['inf_less'],
#         inf_more = data['inf_more'],
#         non_uni = data['non_uni'],
#         non_uni_date =    data['non_uni_date'],
#         mal_uni = data['mal_uni'],
#         mal_uni_date =    data['mal_uni_date'],
#         fixf_less = data['fixf_less'],
#         fixf_more = data['fixf_more'],
#         conver = data['conver'],
#         heal = data['heal'],
#         death = data['death'],
#         exten =    data['exten'],
#         flec =    data['flec'],
#         introt =    data['introt'],
#         extrot =    data['extrot'],
#         add =    data['add'],
#         abd =    data['abd'],
#         limp =    data['limp'],
#     )
#     serializer = FollowfemsSerializer(followfems, many = False)
#     return Response(serializer.data)

# @api_view(['PUT'])
# @authentication_classes([TokenAuthentication])
# @permission_classes((IsAuthenticated, ))
# def updateFollowfems(request, pk):
#     data = request.data
    
#     followfems = Followfems.objects.get(id_id = pk)
#     serializer = FollowfemsSerializer(followfems, data = request.data)

#     if serializer.is_valid():
#         serializer.save()

#     return Response(serializer.data)

# @api_view(['DELETE'])
# @authentication_classes([TokenAuthentication])
# @permission_classes((IsAuthenticated, ))
# def deleteFollowfems(request, pk):
#     followfems = Followfems.objects.get(id_id = pk)
#     followfems.delete()

#     return Response("data deleted")

# ###############ًWomacTables##############################################################################################
# @api_view(['GET'])
# @authentication_classes([TokenAuthentication])
# @permission_classes((IsAuthenticated, ))
# def getWomacs(request):
#     womacs = Womacs.objects.all()
#     serializer = WomacsSerializer(womacs, many = True)
#     return Response(serializer.data)

# @api_view(['GET'])
# @authentication_classes([TokenAuthentication])
# @permission_classes((IsAuthenticated, ))
# def getWomac(request, pk):
#     womacs = Womacs.objects.get(id_id = pk)
#     serializer = WomacsSerializer(womacs, many = False,)
#     return Response(serializer.data)

# @api_view(['POST'])
# @authentication_classes([TokenAuthentication])
# @permission_classes((IsAuthenticated, ))
# def createWomacs(request):
#     data = request.data
#     pati = Patients.objects.get(id_id = data['userCreatorId'])
#     womacs = Womacs.objects.create(
#         id_id = data['id_id'],
#         isempty = data['isempty'],
#         userCreatorId = data['userCreatorId'],
#         patient = pati,
#         kodmeli =    data['kodmeli'],
#         name =    data['name'],
#         surname =    data['surname'],
#         pain_walk = data['pain_walk'],
#         pain_stair = data['pain_stair'],
#         pain_nocturnal = data['pain_nocturnal'],
#         pain_rest = data['pain_rest'],
#         pain_weight = data['pain_weight'],
#         stiff_morning = data['stiff_morning'],
#         stiff_later = data['stiff_later'],
#         Physical_stair_descend = data['Physical_stair_descend'],
#         physical_stair_ascend = data['physical_stair_ascend'],
#         physical_rising_sitting = data['physical_rising_sitting'],
#         physical_standing = data['physical_standing'],
#         physical_bending = data['physical_bending'],
#         physical_walking_flat = data['physical_walking_flat'],
#         physical_getting_in_car = data['physical_getting_in_car'],
#         physical_shopping = data['physical_shopping'],
#         physical_socks_in = data['physical_socks_in'],
#         physical_lying_bed = data['physical_lying_bed'],
#         physical_socks_out = data['physical_socks_out'],
#         physical_rising_bed = data['physical_rising_bed'],
#         physical_bath = data['physical_bath'],
#         physical_sitting = data['physical_sitting'],
#         physical_toilet = data['physical_toilet'],
#         physical_home_heavy = data['physical_home_heavy'],
#         physical_home_light = data['physical_home_light'],
#         womac_score = data['womac_score'],
#         womacdate = data['womacdate'],
#         #womactime = data['womactime']
#     )
#     serializer = WomacsSerializer(womacs, many = False)
#     return Response(serializer.data)

# @api_view(['PUT'])
# @authentication_classes([TokenAuthentication])
# @permission_classes((IsAuthenticated, ))
# def updateWomacs(request, pk):
#     data = request.data
    
#     womacs = Womacs.objects.get(id_id = pk)
#     serializer = WomacsSerializer(womacs, data = request.data)

#     if serializer.is_valid():
#         serializer.save()

#     return Response(serializer.data)

# @api_view(['DELETE'])
# @authentication_classes([TokenAuthentication])
# @permission_classes((IsAuthenticated, ))
# def deleteWomacs(request, pk):
#     womacs = Womacs.objects.get(id_id = pk)
#     womacs.delete()

#     return Response("data deleted")
















# @api_view(['GET'])
# def getNotes(request):
#     notes = Note.objects.all()
#     serializer = NoteSerializer(notes, many = True)
#     return Response(serializer.data)

# @api_view(['GET'])
# def getNote(request, pk):
#     notes = Note.objects.get(id_id = pk)
#     serializer = NoteSerializer(notes, many = False)
#     return Response(serializer.data)

# @api_view(['POST'])
# def createNote(request):
#     data = request.data
#     pati = Patients.objects.get(id = data['patient'])

#     note = Note.objects.create(
#         body = data['body'],
#         patient = pati
#     )
#     serializer = NoteSerializer(note, many = False)
#     return Response(serializer.data)

# @api_view(['PUT'])
# def updateNote(request, pk):
#     data = request.data
    
#     note = Note.objects.get(id = pk)
#     serializer = NoteSerializer(note, data = request.data)

#     if serializer.is_valid():
#         serializer.save()

#     return Response(serializer.data)


# @api_view(['DELETE'])
# def deleteNote(request, pk):
#     note = Note.objects.get(id = pk)
#     note.delete()

#     return Response("data deleted")


