from django.urls import path
from apps.diagnosis.views import *

urlpatterns = [
    path(r'^show/(?P<diagnosis_id>\d+)$', show_action, name='show'),
    path(r'^(?P<patient_id>\d+)/create$', create_action, name='create'),
    path(r'^delete/(?P<diagnosis_id>\d+)$', delete_action, name='delete')
]