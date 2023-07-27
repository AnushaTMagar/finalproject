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

    #patient=Patient.objects.get(user_id=request.user.id) #for profile picture of patient in sidebar
    appointments=Appointment.objects.all().filter(doctorId=request.user.id)
    return render(request,'doctors/appointments.html',{'appointments':appointments})


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
        print('delete init')
        patient = Patient.objects.get(pk=patient_id)
        patient.delete()
        return HttpResponseRedirect(reverse('doctors:list'))
    return redirect(reverse('doctors:show', kwargs={'patient_id': patient_id}))
