from django.urls import path
from .views import test_api, upload_resume

urlpatterns = [
    path('test/', test_api, name='test_api'),
    path('upload-resume/',upload_resume),
]