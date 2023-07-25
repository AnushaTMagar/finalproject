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
