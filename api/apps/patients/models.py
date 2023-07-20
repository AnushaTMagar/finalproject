from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.core.validators import MaxValueValidator
from datetime import date



GENDER = (
    ('Male', 'Male'),
    ('Female', 'Female'),
    ('Others','Others')
)

BLOOD_GROUP = (
    ('O-', 'O-'),
    ('O+', 'O+'),
    ('A-', 'A-'),
    ('A+', 'A+'),
    ('B-','B-'),
    ('B+','B+'),
    ('AB-','AB-'),
    ('AB+','AB+')
)

RH_FACTOR = (
    ('Rh+', 'Rh+'),
    ('Rh-', 'Rh-')
)

class Patient(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    profile_pic= models.ImageField(upload_to='profile_pic/PatientProfilePic/',null=True,blank=True)
    name = models.CharField(verbose_name=_('Name'), max_length=50)
    surname = models.CharField(verbose_name=_('Last Name'), max_length=50)
    gender = models.CharField(verbose_name=_('Gender'), max_length=20, choices=GENDER)
    date_of_birth = models.DateField(
        validators=[MaxValueValidator(limit_value=date.today)])
    address = models.CharField(max_length=40)
    mobile = models.CharField(max_length=20,null=False)
    email = models.CharField(verbose_name=_('Email'), max_length=30, unique=True)
    symptoms = models.CharField(max_length=100,null=False)
    assignedDoctorId = models.PositiveIntegerField(null=True)
    admitDate=models.DateField(auto_now=True)
    blood_group = models.CharField(verbose_name=_('Blood Group'), max_length=20, choices=BLOOD_GROUP, blank=True,
                                   null=True)
    rh_factor = models.CharField(verbose_name=_('Rh factor'), max_length=20, choices=RH_FACTOR, blank=True,
                                 null=True)
    is_disabled = models.BooleanField(verbose_name=_('Disability'), default=False)
    status=models.BooleanField(default=False)
    @property
    def get_name(self):
        return self.user.first_name+" "+self.user.last_name
    @property
    def get_id(self):
        return self.user.id
    def __str__(self):
        return self.user.first_name+" ("+self.symptoms+")"