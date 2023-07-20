from django import forms
from django.contrib.auth.models import User
from . import models

#for doctor related form
class DoctorUserForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','username','password']
        widgets = {
        'password': forms.PasswordInput()
        }
class DoctorForm(forms.ModelForm):
    class Meta:
        model=models.doctor
        fields=['nmc_number', 'full_name', 'profile_pic', 'address',
                  'shift_start_time', 'shift_end_time', 'department', 'professional_experience','email','mobile']