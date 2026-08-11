from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_lead, name='create_lead'),
    path('list/', views.list_leads, name='list_leads'),
]
