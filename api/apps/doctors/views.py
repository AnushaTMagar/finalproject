<<<<<<< HEAD
from django.shortcuts import render,redirect,reverse

from apps.main.views import is_doctor
from . import forms,models
from django.db.models import Sum
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required,user_passes_test
from datetime import datetime,timedelta,date
from django.conf import settings
from django.db.models import Q


@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def doctor_dashboard_view(request):
    #for three cards
    patientcount=models.Patient.objects.all().filter(status=True,assignedDoctorId=request.user.id).count()
    appointmentcount=models.Appointment.objects.all().filter(status=True,doctorId=request.user.id).count()
    patientdischarged=models.PatientDischargeDetails.objects.all().distinct().filter(assignedDoctorName=request.user.first_name).count()

    #for  table in doctor dashboard
    appointments=models.Appointment.objects.all().filter(status=True,doctorId=request.user.id).order_by('-id')
    patientid=[]
    for a in appointments:
        patientid.append(a.patientId)
    patients=models.Patient.objects.all().filter(status=True,user_id__in=patientid).order_by('-id')
    appointments=zip(appointments,patients)
    mydict={
    'patientcount':patientcount,
    'appointmentcount':appointmentcount,
    'patientdischarged':patientdischarged,
    'appointments':appointments,
    'doctor':models.Doctor.objects.get(user_id=request.user.id), #for profile picture of doctor in sidebar
    }
    return render(request,'hospital/doctor_dashboard.html',context=mydict)



@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def doctor_patient_view(request):
    mydict={
    'doctor':models.Doctor.objects.get(user_id=request.user.id), #for profile picture of doctor in sidebar
    }
    return render(request,'hospital/doctor_patient.html',context=mydict)





@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def doctor_view_patient_view(request):
    patients=models.Patient.objects.all().filter(status=True,assignedDoctorId=request.user.id)
    doctor=models.Doctor.objects.get(user_id=request.user.id) #for profile picture of doctor in sidebar
    return render(request,'hospital/doctor_view_patient.html',{'patients':patients,'doctor':doctor})


@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def search_view(request):
    doctor=models.Doctor.objects.get(user_id=request.user.id) #for profile picture of doctor in sidebar
    # whatever user write in search box we get in query
    query = request.GET['query']
    patients=models.Patient.objects.all().filter(status=True,assignedDoctorId=request.user.id).filter(Q(symptoms__icontains=query)|Q(user__first_name__icontains=query))
    return render(request,'hospital/doctor_view_patient.html',{'patients':patients,'doctor':doctor})



@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def doctor_view_discharge_patient_view(request):
    dischargedpatients=models.PatientDischargeDetails.objects.all().distinct().filter(assignedDoctorName=request.user.first_name)
    doctor=models.Doctor.objects.get(user_id=request.user.id) #for profile picture of doctor in sidebar
    return render(request,'hospital/doctor_view_discharge_patient.html',{'dischargedpatients':dischargedpatients,'doctor':doctor})



@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def doctor_appointment_view(request):
    doctor=models.Doctor.objects.get(user_id=request.user.id) #for profile picture of doctor in sidebar
    return render(request,'hospital/doctor_appointment.html',{'doctor':doctor})



@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def doctor_view_appointment_view(request):
    doctor=models.Doctor.objects.get(user_id=request.user.id) #for profile picture of doctor in sidebar
    appointments=models.Appointment.objects.all().filter(status=True,doctorId=request.user.id)
    patientid=[]
    for a in appointments:
        patientid.append(a.patientId)
    patients=models.Patient.objects.all().filter(status=True,user_id__in=patientid)
    appointments=zip(appointments,patients)
    return render(request,'hospital/doctor_view_appointment.html',{'appointments':appointments,'doctor':doctor})



@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def doctor_delete_appointment_view(request):
    doctor=models.Doctor.objects.get(user_id=request.user.id) #for profile picture of doctor in sidebar
    appointments=models.Appointment.objects.all().filter(status=True,doctorId=request.user.id)
    patientid=[]
    for a in appointments:
        patientid.append(a.patientId)
    patients=models.Patient.objects.all().filter(status=True,user_id__in=patientid)
    appointments=zip(appointments,patients)
    return render(request,'hospital/doctor_delete_appointment.html',{'appointments':appointments,'doctor':doctor})



@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def delete_appointment_view(request,pk):
    appointment=models.Appointment.objects.get(id=pk)
    appointment.delete()
    doctor=models.Doctor.objects.get(user_id=request.user.id) #for profile picture of doctor in sidebar
    appointments=models.Appointment.objects.all().filter(status=True,doctorId=request.user.id)
    patientid=[]
    for a in appointments:
        patientid.append(a.patientId)
    patients=models.Patient.objects.all().filter(status=True,user_id__in=patientid)
    appointments=zip(appointments,patients)
    return render(request,'hospital/doctor_delete_appointment.html',{'appointments':appointments,'doctor':doctor})

=======
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from apps.main.models import Doctor
from apps.main.models import Patient, TestRec, Appointment, Diagnosis
from apps.main.forms import PatientForm
import logging
logger = logging.getLogger(__name__)

User = get_user_model()

def index(request):
    if request.method == 'GET':
        return render(request, 'patients/PatientHomepage.html' )
    
# @login_required
# def appointment_action(request):
#     patients = request.user.patients.all()


@login_required
def list_action(request):
    search_full_name = request.GET.get('search_full_name', '')
    doctor=Doctor.objects.get(user_id=request.user.id)
    patients=Patient.objects.all().filter(status=True,assignedDoctorId=request.user.id)
    
    
    return render(
        request,
        'doctors/list.html',
        {
            'patients': patients,
            'patients_count': patients.count()
        }
    )


@login_required
def tests_action(request):
    doctor=Doctor.objects.get(user_id=request.user.id)
    patients=Patient.objects.all().filter(status=True,assignedDoctorId=request.user.id)
    tests = TestRec.objects.filter(patient__in=patients)
    return render(
        request,
        'doctors/tests.html',
        {
            'patients_count': patients.count(),
            'tests': tests,
             
        }
    )


@login_required
def patient_test_action(request, patient_id):
    patient = Patient.objects.get(pk=patient_id)
    tests = patient.test_recs
    return render(
        request,
        'doctors/patient_tests.html',
        {
            'patient': patient,
            'tests': tests
        }
    )


@login_required
def patient_dynamics_action(request, patient_id):
    patient = Patient.objects.get(pk=patient_id)
    tests = patient.test_recs
    return render(
        request,
        'doctors/patient_dynamics.html',
        {
            'patient': patient,
            'tests': tests
        }
    )


@login_required
def appointments_action(request):
    patientcount=Patient.objects.all().filter(status=True,assignedDoctorId=request.user.id).count()
    patient_id = 123
    appointments = Appointment.objects.filter(patientId=patient_id)
    context = {'appointments': appointments}
    return render(request, 'doctors/appointments.html', context)


@login_required
def patient_appointments_action(request, patient_id):
    patientcount=Patient.objects.all().filter(status=True,assignedDoctorId=request.user.id).count()
    patient = Patient.objects.get(pk=patient_id)
    return render(
        request,
        'doctors/patient_appointments.html',
        {
            'patients_count': patientcount,
            'patient': patient
        }
    )


@login_required
def patient_diagnosis_action(request, patient_id):
    patients=Patient.objects.all().filter(status=True,assignedDoctorId=request.user.id)
    doctor=Doctor.objects.get(user_id=request.user.id)
    return render(
        request,
        'doctors/patient_diagnosis.html',
        {
            'patients_count': patients,
            'patient': doctor
        }
    )


# @login_required
# def create_action(request):
#     logger.info("nurse")
#     if request.method == 'POST':
#         form = PatientForm(request)
#         if form.is_valid():
#             form.save()
#         return redirect(reverse('patients:list'))
#     else:
#         return render(request, 'patients/create.html', {})


@login_required
def show_action(request, patient_id):
    patient = Patient.objects.get(pk=patient_id)
    return render(request, 'doctors/show.html', {
        'patient': patient
    })


@login_required
def update_action(request):
    patient_id = None
    if request.method == 'POST':
        patient_id = int(request.POST['patient_id'])
        form = PatientForm(request)
        if form.is_valid():
            form.update()
    return redirect(reverse('doctors:show', kwargs={'patient_id': patient_id}))


@login_required
def delete_action(request, patient_id):
    if request.method == 'POST':
        patient = Patient.objects.get(pk=patient_id)
        patient.delete()
        return HttpResponseRedirect(reverse('doctors:list'))
    return redirect(reverse('doctors:show', kwargs={'patient_id': patient_id}))
>>>>>>> master
