from django.urls import re_path

from apps.med_tests.views import *

urlpatterns = [
    re_path(r'^med_tests/(?P<patient_id>\d+)/create/$', create_action, name='create'),
    re_path(r'^show/(?P<test_id>\d+)/report$', report_action, name='report'),
    re_path(r'^show/(?P<test_id>\d+)$', show_action, name='show'),
    re_path(r'^delete/(?P<test_id>\d+)$', delete_action, name='delete'),
    re_path(r'^dynamics$', dynamics_action, name='dynamics')
]
