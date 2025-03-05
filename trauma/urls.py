
# from django.contrib import admin
# from django.urls import path, include
# #from rest_framework.authtoken import views

from trauma import settings
from django.conf.urls.static import static

# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('',include('api.urls')),
#     #path('api-token-auth/', views.obtain_auth_token, name='api-token-auth'),

# ]+ static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
from django.contrib import admin
from django.urls import path, include
from .api_urls import urlpatterns as api_urls
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(api_urls)),  # Our API endpoints
    
    # JWT token endpoints
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]+ static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
