from django.urls import path

from . import views

app_name = 'certificates'

urlpatterns = [
    path('download/<str:certificate_id>/', views.download_certificate, name='download'),
    path('verify/<str:certificate_id>/', views.verify_certificate, name='verify'),
]
