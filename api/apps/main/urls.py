from django.urls import path, include
from apps.main.views import *
from django.contrib.auth.views import LoginView,LogoutView

urlpatterns = [
    path(r'', index_view, name='index'),
    path(r'^about$', about_view, name='about'),
    path(r'^help$', help_view, name='help'),
    path(r'homepage',index_view, name ='index'),
    
    
    path(r'adminclick',adminclick_view ),
    path(r'doctorclick',doctorclick_view),
    path(r'patientclick',patientclick_view),
    
    path('adminlogin', LoginView.as_view(template_name='customadmin/adminlogin.html')),
    path('doctorlogin', LoginView.as_view(template_name='doctors/doctorlogin.html')),
    path('patientlogin', LoginView.as_view(template_name='patient/patientlogin.html')),
    
    path(r'doctorsignup', doctor_signup_view, name = 'doctorsignup'),
    path(r'pateintsignup', patient_signup_view),

    path(r'afterlogin', afterlogin_view, name = 'afterlogin'),
    
]
