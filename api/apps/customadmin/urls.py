# from django.contrib import admin
# from django.urls import path, include

# urlpatterns = [
#     path(r'^$', index_view, name='index'),
#     path(r'', include(('apps.main.urls','main'), namespace='main')),
# ]

from django.contrib import admin
from django.urls import path, include




from .views import *


urlpatterns = [

    
    path('admin-dashboard', admin_dashboard_view,name='admin-dashboard'),

    path('admin-doctor', admin_doctor_view,name='admin-doctor'),
    path('admin-view-doctor', admin_view_doctor_view,name='admin-view-doctor'),
    path('delete-doctor-from-hospital/<int:pk>',  delete_doctor_from_doctor_view,name='delete-doctor-from-hospital'),
    path('update-doctor/<int:pk>',  update_doctor_view,name='update-doctor'),
    path('admin-add-doctor',  admin_add_doctor_view,name='admin-add-doctor'),
    path('admin-approve-doctor',  admin_approve_doctor_view,name='admin-approve-doctor'),
    path('approve-doctor/<int:pk>',  approve_doctor_view,name='approve-doctor'),
    path('reject-doctor/<int:pk>',  reject_doctor_view,name='reject-doctor'),
    path('admin-view-doctor-specialisation', admin_view_doctor_specialisation_view,name='admin-view-doctor-specialisation'),


    path('admin-patient',  admin_patient_view,name='admin-patient'),
    path('admin-view-patient',  admin_view_patient_view,name='admin-view-patient'),
    path('delete-patient-from-hospital/<int:pk>',  delete_patient_from_patient_view,name='delete-patient-from-hospital'),
    path('update-patient/<int:pk>',  update_patient_view,name='update-patient'),
    path('admin-add-patient',  admin_add_patient_view,name='admin-add-patient'),
    path('admin-approve-patient',  admin_approve_patient_view,name='admin-approve-patient'),
    path('approve-patient/<int:pk>',  approve_patient_view,name='approve-patient'),
    path('reject-patient/<int:pk>',  reject_patient_view,name='reject-patient'),
    path('admin-discharge-patient',  admin_discharge_patient_view,name='admin-discharge-patient'),
    path('discharge-patient/<int:pk>',  discharge_patient_view,name='discharge-patient'),
    path('download-pdf/<int:pk>',  download_pdf_view,name='download-pdf'),


    path('admin-appointment',  admin_appointment_view,name='admin-appointment'),
    path('admin-view-appointment',  admin_view_appointment_view,name='admin-view-appointment'),
    path('admin-add-appointment',  admin_add_appointment_view,name='admin-add-appointment'),
    path('admin-approve-appointment',  admin_approve_appointment_view,name='admin-approve-appointment'),
    path('approve-appointment/<int:pk>',  approve_appointment_view,name='approve-appointment'),
    path('reject-appointment/<int:pk>',  reject_appointment_view,name='reject-appointment'),
]
