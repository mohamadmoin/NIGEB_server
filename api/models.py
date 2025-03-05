from email.policy import default
#from tkinter import CASCADE
import uuid
from django.db import models
from django.forms import FloatField
from django.contrib.auth.models import User
from django.conf import settings

from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
class SampleLists(models.Model):
    id = models.AutoField(primary_key=True)
    id_id = models.CharField(max_length=100, default="")
    user = models.ForeignKey(User,null=True,blank = True,on_delete=models.DO_NOTHING)
    userCreatorName = models.CharField(max_length=100, default="--")
    name = models.CharField(max_length=50, default="")
    jsonList = models.TextField( default="")
    
    date_created = models.CharField(max_length=50, default="")

    def __str__(self):
        return f"SampleList {self.id}"
class UsersDetaileds(models.Model):
    id = models.AutoField(primary_key=True)
    id_id = models.CharField(max_length=100, default="")
    user = models.ForeignKey(User,null=True,blank = True,on_delete=models.DO_NOTHING)
    userCreatorId = models.IntegerField(null=True,blank = True)
    userName = models.CharField(max_length=50, default="")

    name = models.CharField(max_length=50, default="")
    user_Main_Img = models.FileField(upload_to='profiles/',null = True,blank = True)
    image_loc = models.CharField(max_length=50, default="")
    other_1 = models.CharField(max_length=50, default="")
    other_2 = models.CharField(max_length=50, default="")
    other_3 = models.CharField(max_length=50, default="")

    def __str__(self):
        return f"UsersDetailed {self.id}"
class Patients(models.Model):
    id = models.AutoField(primary_key=True)
    id_id = models.CharField(max_length=100, default="")
    user = models.ForeignKey(User,null=True,blank = True,on_delete=models.DO_NOTHING)
    userCreatorName = models.CharField(max_length=100, default="--")
    name = models.CharField(max_length=50, default="")
    surname = models.CharField(max_length=50, default="")
    kodmeli = models.CharField(max_length=50, default="")
    gender = models.CharField(max_length=50, default="")
    birth = models.CharField(max_length=50, default="")
    is_imported = models.BooleanField(default=False)
    date_created = models.CharField(max_length=50, default="")
    phone_number = models.CharField(max_length=50, default="")


    def __str__(self):
        return f"Patient {self.id}"
class Samples(models.Model):
    id = models.AutoField(primary_key=True)
    id_id = models.CharField(max_length=100, default="")
    userCreatorId = models.CharField(max_length=50, default="")
    patient = models.ForeignKey(Patients,null=True,blank = True,on_delete=models.CASCADE)
    sample_code = models.CharField(max_length=50, default="")
    name = models.CharField(max_length=50, default="")
    file_name = models.CharField(max_length=50, default="")
    
    surname = models.CharField(max_length=50, default="")
    kodmeli = models.CharField(max_length=50, default="")
    gender = models.CharField(max_length=50, default="")
    birth = models.CharField(max_length=50, default="")
   
    is_imported = models.BooleanField(default=False)
    sample_date = models.CharField(max_length=50, default="")
    expected_result_date = models.CharField(max_length=50, default="")
    result_date = models.CharField(max_length=50, default="")
    origin_lab = models.CharField(max_length=50, default="")
    is_sent = models.BooleanField(default=False)
    is_received = models.BooleanField(default=False)  
    is_reported = models.BooleanField(default=False)
    is_started = models.BooleanField(default=False)  
    is_confirmed = models.BooleanField(default=False)
    receiver_lab = models.CharField(max_length=50, default="")
    emergent_status = models.CharField(max_length=50, default="")
    sample_hour = models.CharField(max_length=50, default="")
    result_hour = models.CharField(max_length=50, default="")
    patientId = models.CharField(max_length=50, default="")
    history = models.TextField( default="")
    phone_number = models.CharField(max_length=50, default="")
    sample_type = models.CharField(max_length=50, default="")
    history_file_name = models.CharField(max_length=50, default="")

    def __str__(self):
        return f"Sample {self.id}"
class TestResults(models.Model):
    id = models.AutoField(primary_key=True)
    sampleCode = models.CharField(max_length=50, default="")
    patient = models.ForeignKey(Samples,null=True,blank = True,on_delete=models.CASCADE)
    id_id = models.CharField(max_length=50, default="")
    testCode = models.CharField(max_length=50, default="")
    testResult = models.CharField(max_length=50, default="")
    dateReceived = models.CharField(max_length=50, default="")
    dateResultExpect = models.CharField(max_length=50, default="")
    dateResultSent = models.CharField(max_length=50, default="")
    sampleId = models.CharField(max_length=50, default="")
    testMethod = models.CharField(max_length=50, default="")

    def __str__(self):
        return f"TestResult {self.id}"


class TestInfos(models.Model):
    id = models.AutoField(primary_key=True)
    id_id = models.CharField(max_length=50, default="")
    group = models.CharField(max_length=50, default="")
    testCode = models.CharField(max_length=50, default="")
    testName = models.CharField(max_length=50, default="")
    unit = models.CharField(max_length=50, default="")
    description = models.CharField(max_length=50, default="")
    normal_range = models.TextField( default="")
    k_total = models.CharField(max_length=50, default="")
    k_fani = models.CharField(max_length=50, default="")
    k_herfe = models.CharField(max_length=50, default="")
    testCost1 = models.CharField(max_length=50, default="")
    testCost2 = models.CharField(max_length=50, default="")
    testCost3 = models.CharField(max_length=50, default="")
    testCost4 = models.CharField(max_length=50, default="")

    def __str__(self):
        return f"TestInfo {self.id}"
    
class FileTables (models.Model):
    id_id = models.TextField(null = True,blank = True,default = "",max_length=100)

    isempty = models.BooleanField(default=True)

    userCreatorId = models.IntegerField(null=True,blank = True)

    sample = models.ForeignKey(Samples,null=True,blank = True,on_delete=models.CASCADE)

    kodmeli =    models.TextField(null = True,blank = True,default = "",max_length=50)

    name =    models.TextField(null = True,blank = True,default = "",max_length=50)

    surname =    models.TextField(null = True,blank = True,default = "",max_length=50)

    file_date =    models.TextField(null = True,blank = True,default = "",max_length=50)
    
    use_case = models.CharField(max_length=50, default="")

    file_loc = models.TextField(null = True,blank = True,default = "",max_length=200)

    sample_Main_Img = models.FileField(upload_to='files/',null = True,blank = True)
    
class Document(models.Model):
    description = models.CharField(max_length=255, blank=True)
    document = models.FileField(upload_to='documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

# class Patient(models.Model):
#     id_id = models.TextField(null = True,blank = True,default = "",max_length=100)
#     name = models.TextField(max_length= 50, default="", null = True,blank = True)
#     age = models.IntegerField(default = 0)


# class Patients (models.Model):
  # id_id = models.IntegerField(default = 0) 
  
  # user = models.ForeignKey(User,null=True,blank = True,on_delete=models.DO_NOTHING)
  
  # userCreatorName = models.TextField(max_length= 50, default="--",null=True,blank = True)
  
  # iscompleted = models.BooleanField(default= False)

  # name = models.TextField(max_length= 50, default="",null=True,blank = True)

  # surname = models.TextField(max_length= 50, default="", null = True,blank = True)

  # kodmeli = models.TextField(max_length= 50, default="", null = True,blank = True)

  # gender = models.TextField(max_length= 50, default="", null = True,blank = True)

  # birth = models.TextField(max_length= 50, default="", null = True,blank = True)

  # domhand = models.TextField(max_length= 50, default="", null = True,blank = True)

  # job = models.TextField(max_length= 50, default="", null = True,blank = True)

  # int_job = models.IntegerField(default = 0)


  # edu = models.TextField(max_length= 50, default="", null = True,blank = True)

  # hight = models.IntegerField(default = 0)

  # weight = models.IntegerField(default = 0)

  # bmi = models.FloatField(default = 0.0)

  # is_imported = models.BooleanField(default= False)

  # ao_ex_ul_st = models.BooleanField(default= False)

  # ao_ex_ul_si = models.BooleanField(default= False)

  # ao_ex_ul_mu = models.BooleanField(default= False)

  # ao_ex_rad_no = models.BooleanField(default= False)

  # ao_ex_rad_dor = models.BooleanField(default= False)

  # ao_ex_rad_vol = models.BooleanField(default= False)

  # ao_ex_radw = models.BooleanField(default= False)

  # ao_pa_rad_si = models.BooleanField(default= False)

  # ao_pa_rad_mul = models.BooleanField(default= False)

  # ao_pa_rad_inv = models.BooleanField(default= False)

  # ao_pa_rad_sim = models.BooleanField(default= False)

  # ao_pa_rad_fra = models.BooleanField(default= False)

  # ao_pa_rad_wit = models.BooleanField(default= False)

  # ao_pa_radvol = models.BooleanField(default= False)

  # ao_ca_sim = models.BooleanField(default= False)

  # ao_ca_art = models.BooleanField(default= False)

  # ao_ca_mult = models.BooleanField(default= False)

  # is_ao_set = models.BooleanField(default= False)

  # humer_tuber_gn = models.BooleanField(default= False)

  # humer_tuber_gd = models.BooleanField(default= False)

  # humer_tuber_l = models.BooleanField(default= False)

  # humer_surgi_i = models.BooleanField(default= False)

  # humer_surgi_n = models.BooleanField(default= False)

  # humer_surgi_tub_g = models.BooleanField(default= False)

  # humer_surgi_tub_l = models.BooleanField(default= False)

  # humer_surgi_tub_no = models.BooleanField(default= False)

  # humer_surgi_tub_disp = models.BooleanField(default= False)

  # humer_four = models.BooleanField(default= False)

  # femor_inter_1a = models.BooleanField(default= False)

  # femor_inter_1b = models.BooleanField(default= False)

  # femor_inter_2a = models.BooleanField(default= False)

  # femor_inter_2b = models.BooleanField(default= False)

  # femor_sub = models.BooleanField(default= False)

  # femor_head_1 = models.BooleanField(default= False)

  # femor_head_2 = models.BooleanField(default= False)

  # femor_head_3 = models.BooleanField(default= False)

  # femor_head_4 = models.BooleanField(default= False)

  # femor_neck_non = models.BooleanField(default= False)

  # femor_neck_dis = models.BooleanField(default= False)

  # femor_neck_sub = models.BooleanField(default= False)

  # femor_neck_trans = models.BooleanField(default= False)

  # reg_type = models.IntegerField(default= 1)

  # neer = models.TextField(max_length= 50, default="", null = True,blank = True)

  # date_modif = models.TextField(max_length= 50, default="", null = True,blank = True)


# class ConstantTables (models.Model):
#   id_id = models.TextField(null = True,blank = True,default = "",max_length=100)

#   isempty = models.BooleanField(default=True)

#   userCreatorId = models.IntegerField(null=True,blank = True)

#   patient = models.ForeignKey(Patients,null=True,blank = True,on_delete=models.CASCADE)

#   kodmeli =    models.TextField(null = True,blank = True,default = "",max_length=50)

#   name =    models.TextField(null = True,blank = True,default = "",max_length=50)

#   surname =    models.TextField(null = True,blank = True,default = "",max_length=50)

#   date =    models.TextField(null = True,blank = True,default = "",max_length=50)

#   time =    models.TextField(null = True,blank = True,default = "",max_length=50)

#   pain =    models.TextField(null = True,blank = True,default = "",max_length=50)

#   armposi =    models.TextField(null = True,blank = True,default = "",max_length=50)

#   strenabd =    models.TextField(null = True,blank = True,default = "",max_length=50)

#   ffrom =    models.TextField(null = True,blank = True,default = "",max_length=50)

#   lerom =    models.TextField(null = True,blank = True,default = "",max_length=50)

#   errom =    models.TextField(null = True,blank = True,default = "",max_length=50)

#   irrom =    models.TextField(null = True,blank = True,default = "",max_length=50)

#   int_armposi = models.IntegerField(default=0)

#   int_strenabd = models.IntegerField(default=0)

#   int_ffrom = models.IntegerField(default=0)

#   int_lerom = models.IntegerField(default=0)

#   int_errom = models.IntegerField(default=0)

#   int_irrom = models.IntegerField(default=0)

#   int_pain = models.IntegerField(default=0)

#   int_activity_sleep =    models.TextField(null = True,blank = True,default = "",max_length=50)

#   int_activity_sport =    models.TextField(null = True,blank = True,default = "",max_length=50)

#   int_activity_work =    models.TextField(null = True,blank = True,default = "",max_length=50)

#   constant_score = models.IntegerField(default=0)


# class DashTables (models.Model):
#   id_id = models.TextField(null = True,blank = True,default = "",max_length=100)

#   isempty = models.BooleanField(default=True)

#   userCreatorId = models.IntegerField(null=True,blank = True)

#   patient = models.ForeignKey(Patients,null=True,blank = True,on_delete=models.CASCADE)

#   kodmeli =    models.TextField(null = True,blank = True,default = "",max_length=50)

#   name =    models.TextField(null = True,blank = True,default = "",max_length=50)

#   surname =    models.TextField(null = True,blank = True,default = "",max_length=50)

#   dash_score = models.IntegerField(default=0)

#   ghuti = models.IntegerField(default=0)

#   ruzmar = models.IntegerField(default=0)

#   kif = models.IntegerField(default=0)

#   posht = models.IntegerField(default=0)

#   chaghu = models.IntegerField(default=0)

#   tafrih = models.IntegerField(default=0)

#   ejtema = models.IntegerField(default=0)

#   kar = models.IntegerField(default=0)

#   dard_bazu = models.IntegerField(default=0)

#   gezgez = models.IntegerField(default=0)

#   khab = models.IntegerField(default=0)

#   dash_date =    models.TextField(null = True,blank = True,default = "",max_length=50)

#   dash_time =    models.TextField(null = True,blank = True,default = "",max_length=50)


# class HarisTables (models.Model):
#   id_id = models.TextField(null = True,blank = True,default = "",max_length=100)

#   isempty = models.BooleanField(default=True)

#   userCreatorId = models.IntegerField(null=True,blank = True)

#   patient = models.ForeignKey(Patients,null=True,blank = True,on_delete=models.CASCADE)

#   kodmeli =    models.TextField(null = True,blank = True,default = "",max_length=50)

#   name =    models.TextField(null = True,blank = True,default = "",max_length=50)

#   surname =    models.TextField(null = True,blank = True,default = "",max_length=50)

#   date =    models.TextField(null = True,blank = True,default = "",max_length=50)

#   time =    models.TextField(null = True,blank = True,default = "",max_length=50)

#   seco_pain = models.IntegerField(default=0)

#   seco_dist_walk = models.IntegerField(default=0)

#   seco_activities =    models.TextField(null = True,blank = True,default = "",max_length=50)

#   seco_pub_trans =    models.TextField(null = True,blank = True,default = "",max_length=50)

#   seco_support = models.IntegerField(default=0)

#   seco_limb =    models.TextField(null = True,blank = True,default = "",max_length=50)

#   seco_stair =    models.TextField(null = True,blank = True,default = "",max_length=50)

#   seco_sitting =    models.TextField(null = True,blank = True,default = "",max_length=50)

#   sect_flec = models.IntegerField(default=0)

#   sect_add = models.IntegerField(default=0)

#   sect_rot = models.IntegerField(default=0)

#   sect_length = models.IntegerField(default=0)

#   sectr_fdegree = models.IntegerField(default=0)

#   sectr_abdegree = models.IntegerField(default=0)

#   sectr_exrdegree = models.IntegerField(default=0)

#   sectr_addegre = models.IntegerField(default=0)

#   string_sectr_fdegree =    models.TextField(null = True,blank = True,default = "",max_length=50)

#   string_sectr_abdegree =    models.TextField(null = True,blank = True,default = "",max_length=50)

#   string_sectr_exrdegree =    models.TextField(null = True,blank = True,default = "",max_length=50)

#   string_sectr_addegre =    models.TextField(null = True,blank = True,default = "",max_length=50)

#   string_seco_pain =    models.TextField(null = True,blank = True,default = "",max_length=50)

#   string_seco_dist_walk =    models.TextField(null = True,blank = True,default = "",max_length=50)

#   string_seco_supp =    models.TextField(null = True,blank = True,default = "",max_length=50)

#   hipscore = models.IntegerField(default=0)


# class SFTables (models.Model):
#   id_id = models.TextField(null = True,blank = True,default = "",max_length=100)

#   isempty = models.BooleanField(default=True)

#   userCreatorId = models.IntegerField(null=True,blank = True)

#   patient = models.ForeignKey(Patients,null=True,blank = True,on_delete=models.CASCADE)

#   kodmeli =    models.TextField(null = True,blank = True,default = "",max_length=50)

#   name =    models.TextField(null = True,blank = True,default = "",max_length=50)

#   surname =    models.TextField(null = True,blank = True,default = "",max_length=50)

#   date =    models.TextField(null = True,blank = True,default = "",max_length=50)

#   time =    models.TextField(null = True,blank = True,default = "",max_length=50)

#   koli =    models.TextField(null = True,blank = True,default = "",max_length=50)

#   integer_koli = models.IntegerField(default=0)

#   mogha =    models.TextField(null = True,blank = True,default = "",max_length=50)

#   integer_mogha = models.IntegerField(default=0)

#   rozan_shad = models.IntegerField(default=0)

#   rozan_motev = models.IntegerField(default=0)

#   rozan_kharid = models.IntegerField(default=0)

#   rozan_chand_pele = models.IntegerField(default=0)

#   rozan_yek_pele = models.IntegerField(default=0)

#   rozan_kham = models.IntegerField(default=0)

#   rozan_piade_km = models.IntegerField(default=0)

#   rozan_piade_chandsad = models.IntegerField(default=0)

#   rozan_piade_sad = models.IntegerField(default=0)

#   rozan_hamum = models.IntegerField(default=0)

#   jesm_kar_kam =    models.TextField(null = True,blank = True,default = "",max_length=50)

#   jesm_kamtar_vaght =    models.TextField(null = True,blank = True,default = "",max_length=50)

#   jesm_khas =    models.TextField(null = True,blank = True,default = "",max_length=50)

#   jesm_adi =    models.TextField(null = True,blank = True,default = "",max_length=50)

#   ravani_kar_kam =    models.TextField(null = True,blank = True,default = "",max_length=50)

#   ravani_kamtar_vaght =    models.TextField(null = True,blank = True,default = "",max_length=50)

#   ravani_deghat =    models.TextField(null = True,blank = True,default = "",max_length=50)

#   integer_ravani_ekhtelal = models.IntegerField(default=0)

#   ravani_ekhtelal =    models.TextField(null = True,blank = True,default = "",max_length=50)

#   integer_dard = models.IntegerField(default=0)

#   dard =    models.TextField(null = True,blank = True,default = "",max_length=50)

#   integer_dard_mane = models.IntegerField(default=0)

#   dard_mane =    models.TextField(null = True,blank = True,default = "",max_length=50)

#   nazdik_rohie = models.IntegerField(default=0)

#   nazdik_asabi = models.IntegerField(default=0)

#   nazdik_asabi_nakhosh = models.IntegerField(default=0)

#   nazdik_aramesh = models.IntegerField(default=0)

#   nazdik_energy = models.IntegerField(default=0)

#   nazdik_farsude = models.IntegerField(default=0)

#   nazdik_gham = models.IntegerField(default=0)

#   nazdik_khosh = models.IntegerField(default=0)

#   nazdik_khaste = models.IntegerField(default=0)

#   integer_jesmi_va_atefi = models.IntegerField(default=0)

#   jesmi_va_atefi =    models.TextField(null = True,blank = True,default = "",max_length=50)

#   sadegh_zood = models.IntegerField(default=0)

#   sadegh_salamt_darhad = models.IntegerField(default=0)

#   sadegh_badtar = models.IntegerField(default=0)

#   sadegh_ali = models.IntegerField(default=0)


# class VASTables (models.Model):
#   id_id = models.TextField(null = True,blank = True,default = "",max_length=100)

#   isempty = models.BooleanField(default=True)

#   userCreatorId = models.IntegerField(null=True,blank = True)

#   patient = models.ForeignKey(Patients,null=True,blank = True,on_delete=models.CASCADE)

#   kodmeli =    models.TextField(null = True,blank = True,default = "",max_length=50)

#   name =    models.TextField(null = True,blank = True,default = "",max_length=50)

#   surname =    models.TextField(null = True,blank = True,default = "",max_length=50)

#   vas_score = models.IntegerField(default=0)

#   vas_date =    models.TextField(null = True,blank = True,default = "",max_length=50)

#   vas_time =    models.TextField(null = True,blank = True,default = "",max_length=50)


# class TreatmentTables (models.Model):
#   id_id = models.TextField(null = True,blank = True,default = "",max_length=100)

#   isempty = models.BooleanField(default=True)

#   userCreatorId = models.IntegerField(null=True,blank = True)

#   patient = models.ForeignKey(Patients,null=True,blank = True,on_delete=models.CASCADE)

#   kodmeli =    models.TextField(null = True,blank = True,default = "",max_length=50)

#   name =    models.TextField(null = True,blank = True,default = "",max_length=50)

#   surname =    models.TextField(null = True,blank = True,default = "",max_length=50)

#   treat_date =    models.TextField(null = True,blank = True,default = "",max_length=50)

#   treat_non = models.BooleanField(default=False)

#   treat_hip_external = models.BooleanField(default=False)

#   treat_hip_orif_dyn = models.BooleanField(default=False)

#   treat_hip_orif_cond =    models.BooleanField(default=False)

#   treat_hip_orif_anat =    models.BooleanField(default=False)

#   treat_hip_orif_cephal =    models.BooleanField(default=False)

#   treat_arthro = models.BooleanField(default=False)

#   treat_humer_crif = models.BooleanField(default=False)

#   treat_humer_orif_pin =    models.BooleanField(default=False)

#   treat_humer_orif_plate =    models.BooleanField(default=False)

#   treat_dist_crif_pin =    models.BooleanField(default=False)

#   treat_dist_crif_external =    models.BooleanField(default=False)

#   treat_dist_orif = models.BooleanField(default=False)

#   treat_dist_pin = models.BooleanField(default=False)

#   surgen =    models.TextField(null = True,blank = True,default = "",max_length=50)

#   surgen_name =    models.TextField(null = True,blank = True,default = "",max_length=50)

#   lot_num = models.IntegerField(default=0)

#   ref_num = models.IntegerField(default=0)

#   irc_num = models.IntegerField(default=0)







# class InjuryTables (models.Model):
#   id_id = models.TextField(null = True,blank = True,default = "",max_length=100)

#   isempty = models.BooleanField(default=True)

#   userCreatorId = models.IntegerField(null=True,blank = True)

#   patient = models.ForeignKey(Patients,null=True,blank = True,on_delete=models.CASCADE)

#   kodmeli =    models.TextField(null = True,blank = True,default = "",max_length=50)

#   name =    models.TextField(null = True,blank = True,default = "",max_length=50)

#   surname =    models.TextField(null = True,blank = True,default = "",max_length=50)

#   inj_type =    models.TextField(null = True,blank = True,default = "",max_length=50)

#   inj_open =    models.TextField(null = True,blank = True,default = "",max_length=50)

#   inj_side =    models.TextField(null = True,blank = True,default = "",max_length=50)

#   int_inj_type =    models.IntegerField(null=True,blank = True)

#   int_inj_open =    models.IntegerField(null=True,blank = True)

#   int_inj_side =    models.IntegerField(null=True,blank = True)


# class Followrads (models.Model):
#   id_id = models.TextField(null = True,blank = True,default = "",max_length=100)

#   isempty = models.BooleanField(default=True)

#   userCreatorId = models.IntegerField(null=True,blank = True)

#   patient = models.ForeignKey(Patients,null=True,blank = True,on_delete=models.CASCADE)

#   kodmeli =    models.TextField(null = True,blank = True,default = "",max_length=50)

#   name =    models.TextField(null = True,blank = True,default = "",max_length=50)

#   surname =    models.TextField(null = True,blank = True,default = "",max_length=50)

#   followdate =    models.TextField(null = True,blank = True,default = "",max_length=50)

#   followtime =    models.TextField(null = True,blank = True,default = "",max_length=50)

#   inf_less = models.IntegerField(default=0)

#   inf_more = models.IntegerField(default=0)

#   non_uni = models.IntegerField(default=0)

#   non_uni_date =    models.TextField(null = True,blank = True,default = "",max_length=50)

#   mal_uni = models.IntegerField(default=0)

#   mal_uni_date =    models.TextField(null = True,blank = True,default = "",max_length=50)

#   fixf_less = models.IntegerField(default=0)

#   fixf_more = models.IntegerField(default=0)

#   exten =    models.TextField(null = True,blank = True,default = "",max_length=50)

#   flec =    models.TextField(null = True,blank = True,default = "",max_length=50)

#   sup =    models.TextField(null = True,blank = True,default = "",max_length=50)

#   pron =    models.TextField(null = True,blank = True,default = "",max_length=50)

#   count_pain =    models.TextField(null = True,blank = True,default = "",max_length=50)

#   sym_sen =    models.TextField(null = True,blank = True,default = "",max_length=50)

#   sym_vaso =    models.TextField(null = True,blank = True,default = "",max_length=50)

#   sym_edem =    models.TextField(null = True,blank = True,default = "",max_length=50)

#   sym_motor =    models.TextField(null = True,blank = True,default = "",max_length=50)

#   si_sen =    models.TextField(null = True,blank = True,default = "",max_length=50)

#   si_vaso =    models.TextField(null = True,blank = True,default = "",max_length=50)

#   si_edem =    models.TextField(null = True,blank = True,default = "",max_length=50)

#   si_motor =    models.TextField(null = True,blank = True,default = "",max_length=50)

#   diag =    models.TextField(null = True,blank = True,default = "",max_length=50)


# class Followhums (models.Model):
#   id_id = models.TextField(null = True,blank = True,default = "",max_length=100)

#   isempty = models.BooleanField(default=True)

#   userCreatorId = models.IntegerField(null=True,blank = True)

#   patient = models.ForeignKey(Patients,null=True,blank = True,on_delete=models.CASCADE)

#   kodmeli =    models.TextField(null = True,blank = True,default = "",max_length=50)

#   name =    models.TextField(null = True,blank = True,default = "",max_length=50)

#   surname =    models.TextField(null = True,blank = True,default = "",max_length=50)

#   followdate =    models.TextField(null = True,blank = True,default = "",max_length=50)

#   followtime =    models.TextField(null = True,blank = True,default = "",max_length=50)

#   inf_less = models.IntegerField(default=0)

#   inf_more = models.IntegerField(default=0)

#   non_uni = models.IntegerField(default=0)

#   non_uni_date =    models.TextField(null = True,blank = True,default = "",max_length=50)

#   mal_uni = models.IntegerField(default=0)

#   mal_uni_date =    models.TextField(null = True,blank = True,default = "",max_length=50)

#   fixf_less = models.IntegerField(default=0)

#   fixf_more = models.IntegerField(default=0)
#   exten =    models.TextField(null = True,blank = True,default = "",max_length=50)

#   flec =    models.TextField(null = True,blank = True,default = "",max_length=50)

#   introt =    models.TextField(null = True,blank = True,default = "",max_length=50)

#   extrot =    models.TextField(null = True,blank = True,default = "",max_length=50)

#   elev =    models.TextField(null = True,blank = True,default = "",max_length=50)

#   abd =    models.TextField(null = True,blank = True,default = "",max_length=50)

#   froz =    models.TextField(null = True,blank = True,default = "",max_length=50)


# class Followfems (models.Model):
#   id_id = models.TextField(null = True,blank = True,default = "",max_length=100)

#   isempty = models.BooleanField(default=True)

#   userCreatorId = models.IntegerField(null=True,blank = True)

#   patient = models.ForeignKey(Patients,null=True,blank = True,on_delete=models.CASCADE)

#   kodmeli =    models.TextField(null = True,blank = True,default = "",max_length=50)

#   name =    models.TextField(null = True,blank = True,default = "",max_length=50)

#   surname =    models.TextField(null = True,blank = True,default = "",max_length=50)

#   followdate =    models.TextField(null = True,blank = True,default = "",max_length=50)

#   followtime =    models.TextField(null = True,blank = True,default = "",max_length=50)

#   inf_less = models.IntegerField(default=0)

#   inf_more = models.IntegerField(default=0)

#   non_uni = models.IntegerField(default=0)

#   non_uni_date =    models.TextField(null = True,blank = True,default = "",max_length=50)

#   mal_uni = models.IntegerField(default=0)

#   mal_uni_date =    models.TextField(null = True,blank = True,default = "",max_length=50)

#   fixf_less = models.IntegerField(default=0)

#   fixf_more = models.IntegerField(default=0)

#   conver = models.IntegerField(default=0)

#   heal = models.IntegerField(default=0)

#   death = models.IntegerField(default=0)

#   exten =    models.TextField(null = True,blank = True,default = "",max_length=50)

#   flec =    models.TextField(null = True,blank = True,default = "",max_length=50)

#   introt =    models.TextField(null = True,blank = True,default = "",max_length=50)

#   extrot =    models.TextField(null = True,blank = True,default = "",max_length=50)

#   add =    models.TextField(null = True,blank = True,default = "",max_length=50)

#   abd =    models.TextField(null = True,blank = True,default = "",max_length=50)

#   limp =    models.TextField(null = True,blank = True,default = "",max_length=50)

# class Womacs (models.Model):
#   id_id = models.TextField(null = True,blank = True,default = "",max_length=100)

#   isempty = models.BooleanField(default=True)

#   userCreatorId = models.IntegerField(null=True,blank = True)

#   patient = models.ForeignKey(Patients,null=True,blank = True,on_delete=models.CASCADE)

#   kodmeli =    models.TextField(null = True,blank = True,default = "",max_length=50)

#   name =    models.TextField(null = True,blank = True,default = "",max_length=50)

#   surname =    models.TextField(null = True,blank = True,default = "",max_length=50)

#   pain_walk = models.IntegerField(default=0)
#   pain_stair = models.IntegerField(default=0)
#   pain_nocturnal = models.IntegerField(default=0)
#   pain_rest = models.IntegerField(default=0)
#   pain_weight = models.IntegerField(default=0)
#   stiff_morning = models.IntegerField(default=0)
#   stiff_later = models.IntegerField(default=0)
#   Physical_stair_descend = models.IntegerField(default=0)
#   physical_stair_ascend = models.IntegerField(default=0)
#   physical_rising_sitting = models.IntegerField(default=0)
#   physical_standing = models.IntegerField(default=0)
#   physical_bending = models.IntegerField(default=0)
#   physical_walking_flat = models.IntegerField(default=0)
#   physical_getting_in_car = models.IntegerField(default=0)
#   physical_shopping = models.IntegerField(default=0)
#   physical_socks_in = models.IntegerField(default=0)
#   physical_lying_bed = models.IntegerField(default=0)
#   physical_socks_out = models.IntegerField(default=0)
#   physical_rising_bed = models.IntegerField(default=0)
#   physical_bath = models.IntegerField(default=0)
#   physical_sitting = models.IntegerField(default=0)
#   physical_toilet = models.IntegerField(default=0)
#   physical_home_heavy = models.IntegerField(default=0)
#   physical_home_light = models.IntegerField(default=0)
#   womac_score = models.IntegerField(default=0)
#   womacdate =    models.TextField(null = True,blank = True,default = "",max_length=50)

#   womactime =    models.TextField(null = True,blank = True,default = "",max_length=50)




# class Note(models.Model):
#     patient = models.ForeignKey(Patient, null = True,blank = True, on_delete=models.CASCADE)
#     body = models.TextField(max_length= 50, default="", null = True,blank = True)
#     updated = models.DateTimeField(auto_now=True)
#     created = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.body[0:50]

#     class Meta:
#         ordering = ['-updated']
        

    

