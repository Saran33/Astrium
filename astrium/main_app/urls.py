
from django.urls import path, include
from . import views
from main_app.dash_apps.chart_apps import line_chart

urlpatterns = [
    path('', views.SecuritySelector, name = 'securityselector'),
    path('securitytracker/', views.SecurityTracker, name = 'securitytracker'),
]
