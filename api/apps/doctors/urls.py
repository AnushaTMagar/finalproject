<<<<<<< HEAD
from django.contrib import admin
from django.urls import path
from doctors import views
from django.contrib.auth.views import LoginView,LogoutView


urlpatterns =[
    path('doctor-dashboard', views.doctor_dashboard_view,name='doctor-dashboard'),
    path('search', views.search_view,name='search'),

    path('doctor-patient', views.doctor_patient_view,name='doctor-patient'),
    path('doctor-view-patient', views.doctor_view_patient_view,name='doctor-view-patient'),
    path('doctor-view-discharge-patient',views.doctor_view_discharge_patient_view,name='doctor-view-discharge-patient'),

    path('doctor-appointment', views.doctor_appointment_view,name='doctor-appointment'),
    path('doctor-view-appointment', views.doctor_view_appointment_view,name='doctor-view-appointment'),
    path('doctor-delete-appointment',views.doctor_delete_appointment_view,name='doctor-delete-appointment'),
    path('delete-appointment/<int:pk>', views.delete_appointment_view,name='delete-appointment'),
]
=======
from django.urls import re_path

from apps.doctors.views import *

urlpatterns = [
    re_path("index/", index, name="index"),
    re_path(r'^list$', list_action, name='list'),
    re_path(r'^tests$', tests_action, name='tests'),
    re_path(r'^appointments$', appointments_action, name='appointments'),
    # re_path(r'^create$', create_action, name='create'),
    re_path(r'^update$', update_action, name='update'),
    re_path(r'^show/(?P<patient_id>\d+)$', show_action, name='show'),
    re_path(r'^delete/(?P<patient_id>\d+)$', delete_action, name='delete'),
    re_path(r'(?P<patient_id>\d+)/tests$', patient_test_action, name='patient_tests'),
    re_path(r'(?P<patient_id>\d+)/dynamics$', patient_dynamics_action, name='patient_dynamics'),
    re_path(r'(?P<patient_id>\d+)/appointments$', patient_appointments_action, name='patient_appointments'),
    re_path(r'(?P<patient_id>\d+)/diagnosis$', patient_diagnosis_action, name='patient_diagnosis'),
]
>>>>>>> master
