from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.upload_certificate, name='upload_certificate'),
    path('share/', views.certificate_share, name='certificate_share'),
    path('lookup/<str:cert_id>/', views.lookup_certificate, name='lookup_certificate'),
    path('my/<slug:slug>/', views.my_certificate, name='my_certificate'),
]
