from django.db import models

<<<<<<< HEAD
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User
from froala_editor.fields import FroalaField


# Create your models here.
department = (
    ('Physician', 'Physician'),
    ('Dentistry', "Dentistry"),
    ('Cardiology', "Cardiology"),
    ('ENT Specialists', "ENT Specialists"),
    ('Dietitian', 'Dietitian'),
    ('Endocrinology', 'Endocrinology'),
    ('Blood Screening', 'Blood Screening'),
    ('Eye Care', 'Eye Care'),
    ('Physical Therapy', 'Physical Therapy'),
    ('Neurology', 'Neurology'),
    ('Gynaecology', 'Gynaecology'),
    ('Pediatrics', 'Pediatrics'),
    ('Ophthalmology', 'Ophthalmology'),
    ('Orthopedic', 'Orthopedic'),
    ('Pulmonologist','Pulmonologist'),
    ('Radiologist','Radiologist'),
    ('General Surgeon','General Surgeon')
)

class doctor(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    profile_pic= models.ImageField(upload_to='profile_pic/DoctorProfilePic/',null=True,blank=True)
    description=models.TextField(default="")
    address = models.CharField(max_length=100,default="")
    shift_start_time = models.TimeField(max_length=10)
    shift_end_time = models.TimeField(max_length=10)
    qualification_name = models.CharField(max_length=100)
    nmc_number = models.CharField(max_length=10, default="")
    education_training = models.TextField(default="")
    hospital_name = models.CharField(max_length=100)
    department= models.CharField(max_length=50,choices=department,default='Physician')
    professional_experience = models.TextField(default="")
    created_at = models.DateTimeField(default=timezone.now)
    email = models.CharField(max_length=100)
    mobile = models.CharField(max_length=20,null=True)
    
    @property
    def get_name(self):
        return self.user.first_name+" "+self.user.last_name
    @property
    def get_id(self):
        return self.user.id
    def __str__(self):
        return "{} ({})".format(self.user.first_name,self.department)
=======
# Create your models here.
>>>>>>> master
