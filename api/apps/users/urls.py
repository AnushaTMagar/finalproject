from django.urls import re_path
from apps.users.views import *

urlpatterns = [
    re_path(r'^show$', show_action, name='show'),
    re_path(r'^create$', create_action, name='create'),
    re_path(r'^update$', update_action, name='update'),
    re_path(r'^change_password$', change_password_action, name='change_password'),
    re_path(r'^reset_password$', reset_password_action, name='reset_password'),
    re_path(r'^delete$', delete_action, name='delete'),
    re_path(r'^logout$', logout_action, name='logout'),
    re_path(r'^dashboard$', dashboard_action, name='dashboard')
]
