
from django.contrib import admin
from django.urls import path, include
#from rest_framework.authtoken import views

from trauma import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('api.urls')),
    #path('api-token-auth/', views.obtain_auth_token, name='api-token-auth'),

]+ static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
