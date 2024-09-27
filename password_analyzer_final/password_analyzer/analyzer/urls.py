from django.urls import path
from . import views

urlpatterns = [
    path('', views.analyze_password, name='analyze_password'),
]