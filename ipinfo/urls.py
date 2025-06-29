from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('process-ips/', views.process_ips, name='process_ips'),
]