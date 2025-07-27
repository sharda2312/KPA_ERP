from django.urls import path
from . import views

urlpatterns = [
    path('forms/wheel-specifications', views.WheelSpecifications.as_view(), name='wheel_specifications'),
    ]