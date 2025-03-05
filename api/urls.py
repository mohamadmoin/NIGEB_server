import statistics
from django.urls import include, path, re_path
from django.contrib.auth import views as auth_views
#from django.conf.urls import url


from . import views

urlpatterns = [
    path('', views.getRoutes),

    path('patients/',views.getPatients),
    path('patients/create/', views.createPatient),
    path('patients/<str:pk>/',views.getPatient),
    path('patients/<str:pk>/update', views.updatePatients),
    path('patients/<str:pk>/delete', views.deletePatients),
    
    path('sampleLists/',views.getSampleLists),
    path('sampleLists/create/', views.createSampleList),
    path('sampleLists/<str:pk>/',views.getSampleList),
    path('sampleLists/<str:pk>/update', views.updateSampleLists),
    path('sampleLists/<str:pk>/delete', views.deleteSampleLists),
    
    path('samples/',views.getSamples),
    path('samples/create/', views.createSamples),
    path('samples/<str:pk>/',views.getSample),
    path('samples/<str:pk>/info',views.getSampleInfo),
    path('samples/<str:pk>/recieved',views.getSamplesReceived),
    path('samples/<str:pk>/sent',views.getSamplesSent),
    path('samples/<str:pk>/withpatient',views.getSampleWithPatient),
    path('samples/<str:pk>/update', views.updateSamples),
    path('samples/<str:pk>/delete', views.deleteSamples),
    
    path('testinfos/',views.getTestInfos),
    path('testinfos/create/', views.createTestInfos),
    path('testinfos/<str:pk>/',views.getTestInfo),
    path('testinfos/<str:pk>/update', views.updateTestInfos),
    path('testinfos/<str:pk>/delete', views.deleteTestInfos),
    
    
    path('testresults/',views.getTestResults),
    path('testresults/create/', views.createTestResults),
    path('testresults/<str:pk>/',views.getTestResult),
    path('testresults/<str:pk>/withsample',views.getTestResultWithSample),

    path('testresults/<str:pk>/update', views.updateTestResults),
    path('testresults/<str:pk>/delete', views.deleteTestResults),
    
    path('filetables/',views.getFileTables),
    path('filetables/create/', views.createFileTable),
    path('filetables/createexcel/', views.createFileTableExcel),
    path('filetables/<str:pk>/',views.getFileTable),
    path('filetables/<str:pk>/withsample', views.getFileWithSample),
    path('filetables/<str:pk>/update', views.updateFileTables),
    path('filetables/<str:pk>/delete', views.deleteFileTables),
    
    
    path('usersdetailed/',views.getUsersDetaileds),
    path('usersdetailed/create/', views.createUsersDetailed),
    path('usersdetailed/createfile/', views.createUsersDetailedFile),

    path('usersdetailed/<str:pk>/',views.getUsersDetailed),
    path('usersdetailed/<str:pk>/update', views.updateUsersDetaileds),
    path('usersdetailed/<str:pk>/updatefile', views.updateUsersDetailedsFile),

    path('usersdetailed/<str:pk>/delete', views.deleteUsersDetaileds),
    
    # path('protected/<str:file>/', views.serve_protected_document, name='serve_protected_document'),
    
    #path('protected/', include('protected_media.urls')),


    # path('constanttables/',views.getConstants),
    # path('constanttables/create/', views.createConstants),
    # path('constanttables/<str:pk>/',views.getConstant),
    # path('constanttables/<str:pk>/update', views.updateConstants),
    # path('constanttables/<str:pk>/delete', views.deleteConstants),

    # path('dashtables/',views.getDashTables),
    # path('dashtables/create/', views.createDashTables),
    # path('dashtables/<str:pk>/',views.getDashTable),
    # path('dashtables/<str:pk>/update', views.updateDashTables),
    # path('dashtables/<str:pk>/delete', views.deleteDashTables),

    # path('haristables/',views.getHarisTables),
    # path('haristables/create/', views.createHarisTables),
    # path('haristables/<str:pk>/',views.getHarisTable),
    # path('haristables/<str:pk>/update', views.updateHarisTables),
    # path('haristables/<str:pk>/delete', views.deleteHarisTables),

    # path('sftables/',views.getSFTables),
    # path('sftables/create/', views.createSFTables),
    # path('sftables/<str:pk>/',views.getSFTable),
    # path('sftables/<str:pk>/update', views.updateSFTables),
    # path('sftables/<str:pk>/delete', views.deleteSFTables),

    # path('vastables/',views.getVASTables),
    # path('vastables/create/', views.createVASTables),
    # path('vastables/<str:pk>/',views.getVASTable),
    # path('vastables/<str:pk>/update', views.updateVASTables),
    # path('vastables/<str:pk>/delete', views.deleteVASTables),

    # path('treatmenttables/',views.getTreatmentTables),
    # path('treatmenttables/create/', views.createTreatmentTables),
    # path('treatmenttables/<str:pk>/',views.getTreatmentTable),
    # path('treatmenttables/<str:pk>/update', views.updateTreatmentTables),
    # path('treatmenttables/<str:pk>/delete', views.deleteTreatmentTables),

    # 
    # path('injurytables/',views.getInjuryTables),
    # path('injurytables/create/', views.createInjuryTables),
    # path('injurytables/<str:pk>/',views.getInjuryTable),
    # path('injurytables/<str:pk>/update', views.updateInjuryTables),
    # path('injurytables/<str:pk>/delete', views.deleteInjuryTables),

    # path('followrads/',views.getFollowrads),
    # path('followrads/create/', views.createFollowrads),
    # path('followrads/<str:pk>/',views.getFollowrad),
    # path('followrads/<str:pk>/update', views.updateFollowrads),
    # path('followrads/<str:pk>/delete', views.deleteFollowrads),

    # path('followhums/',views.getFollowhums),
    # path('followhums/create/', views.createFollowhums),
    # path('followhums/<str:pk>/',views.getFollowhum),
    # path('followhums/<str:pk>/update', views.updateFollowhums),
    # path('followhums/<str:pk>/delete', views.deleteFollowhums),

    # path('followfems/',views.getFollowfems),
    # path('followfems/create/', views.createFollowfems),
    # path('followfems/<str:pk>/',views.getFollowfem),
    # path('followfems/<str:pk>/update', views.updateFollowfems),
    # path('followfems/<str:pk>/delete', views.deleteFollowfems),
    
    # path('womacs/',views.getWomacs),
    # path('womacs/create/', views.createWomacs),
    # path('womacs/<str:pk>/',views.getWomac),
    # path('womacs/<str:pk>/update', views.updateWomacs),
    # path('womacs/<str:pk>/delete', views.deleteWomacs),

    # path('trauma/',views.getNotes),
    # path('trauma/create/', views.createNote),
    # path('trauma/<str:pk>/update', views.updateNote),
    # path('trauma/<str:pk>/delete', views.deleteNote),
    # path('trauma/<str:pk>/',views.getNote),

    # re_path(r'^image/$', FileView.as_view(), name='file-upload'),

    # path('image2/', views.upload_file),


    path('connectioncheck/', views.connectioncheck, name="concheck"),
    
    path('register/', views.registerPage, name="register"),
	path('login/', views.loginPage, name="login"),  
    path('login2/', views.loginPage2, name="login2"),  
   # path('loginconf/<str:pk>/', views.loginConf, name="loginConf"),  
	path('logout/', views.logoutUser, name="logout"),


    path('reset_password/',
     auth_views.PasswordResetView.as_view(template_name="password_reset.html"),
     name="reset_password"),

    path('reset_password_sent/', 
        auth_views.PasswordResetDoneView.as_view(template_name="password_reset_sent.html"), 
        name="password_reset_done"),

    path('reset/<uidb64>/<token>/',
     auth_views.PasswordResetConfirmView.as_view(template_name="password_reset_form.html"), 
     name="password_reset_confirm"),

    path('reset_password_complete/', 
        auth_views.PasswordResetCompleteView.as_view(template_name="password_reset_done.html"), 
        name="password_reset_complete"),

]

#if settings.DEBUG:
       # urlpatterns 
