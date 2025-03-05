# my_lab_platform/api_urls.py

from django.urls import path
from rest_framework.routers import DefaultRouter
from labs.views import LabViewSet
from patients.views import PatientViewSet
from tests_definitions.views import TestInfoViewSet, FavoriteTestGroupViewSet
from samples.views import SampleViewSet, SampleTestViewSet, AttachmentViewSet
from finances.views import InvoiceViewSet, PaymentViewSet
from attachments.views import FileAttachmentViewSet
from accounts.views import RegisterView, ForgotPasswordView, ResetPasswordView, UserProfileViewSet



# finances if used
# from finances.views import InvoiceViewSet

router = DefaultRouter()
router.register(r'users-profiles', UserProfileViewSet, basename='userprofile')
router.register(r'labs', LabViewSet, basename='lab')
router.register(r'patients', PatientViewSet, basename='patient')
router.register(r'tests-info', TestInfoViewSet, basename='testinfo')
router.register(r'favorite-test-groups', FavoriteTestGroupViewSet, basename='favoritetestgroup')
router.register(r'samples', SampleViewSet, basename='sample')
router.register(r'sample-tests', SampleTestViewSet, basename='sampletest')
router.register(r'attachments', AttachmentViewSet, basename='attachment')
router.register(r'invoices', InvoiceViewSet, basename='invoice')
router.register(r'payments', PaymentViewSet, basename='payment')
router.register(r'file-attachments', FileAttachmentViewSet, basename='fileattachment')
# path('register/', RegisterView.as_view(), name='register'),
# path('forgot-password/', ForgotPasswordView.as_view(), name='forgot_password'),
# path('reset-password/', ResetPasswordView.as_view(), name='reset_password'),
urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('forgot-password/', ForgotPasswordView.as_view(), name='forgot_password'),
    path('reset-password/', ResetPasswordView.as_view(), name='reset_password'),
]
# router.register(r'invoices', InvoiceViewSet, basename='invoice')

urlpatterns += router.urls
