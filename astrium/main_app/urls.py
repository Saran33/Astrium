
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.SecuritySelector, name = 'securityselector'),
    path('securitytracker/', views.SecurityTracker, name = 'securitytracker'),
]
