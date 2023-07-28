from django.db import models
from django.contrib.auth.models import User
from django.forms import JSONField
from transliterate import slugify, translit
from django.utils.translation import gettext_lazy as _



departments = [
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
]

DIAGNOSIS_TYPE = (
    ('Preliminary', 'Preliminary'),
    ('Clinical', 'Clinical'),
    ('Final', 'Final')
)

class Doctor(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    profile_pic= models.ImageField(upload_to='profile_pic/DoctorProfilePic/',null=True,blank=True)
    address = models.CharField(max_length=40)
    mobile = models.CharField(max_length=20,null=True)
    department= models.CharField(max_length=50,choices=departments,default='Cardiologist')
    status=models.BooleanField(default=False)
    @property
    def get_name(self):
        return self.user.first_name+" "+self.user.last_name
    @property
    def get_id(self):
        return self.user.id
    def __str__(self):
        return "{} ({})".format(self.user.first_name,self.department)



class Patient(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    profile_pic= models.ImageField(upload_to='profile_pic/PatientProfilePic/',null=True,blank=True)
    address = models.CharField(max_length=40)
    
    mobile = models.CharField(max_length=20,null=False)
    symptoms = models.CharField(max_length=100,null=False)
    assignedDoctorId = models.PositiveIntegerField(null=True)
    admitDate=models.DateField(auto_now=True)
    
    status=models.BooleanField(default=False)
    
    @property
    def get_name(self):
        return self.user.first_name+" "+self.user.last_name
    @property
    def get_id(self):
        return self.user.id
    def __str__(self):
        return self.user.first_name+" ("+self.symptoms+")"


class Appointment(models.Model):
    patientId=models.PositiveIntegerField(null=True)
    doctorId=models.PositiveIntegerField(null=True)
    patientName=models.CharField(max_length=40,null=True)
    doctorName=models.CharField(max_length=40,null=True)
    appointmentDate = models.DateTimeField()
    description=models.TextField(max_length=500)
    status=models.BooleanField(default=False)



class PatientDischargeDetails(models.Model):
    patientId=models.PositiveIntegerField(null=True)
    patientName=models.CharField(max_length=40)
    assignedDoctorName=models.CharField(max_length=40)
    address = models.CharField(max_length=40)
    mobile = models.CharField(max_length=20,null=True)
    symptoms = models.CharField(max_length=100,null=True)

    admitDate=models.DateField(null=False)
    releaseDate=models.DateField(null=False)
    daySpent=models.PositiveIntegerField(null=False)

    roomCharge=models.PositiveIntegerField(null=False)
    medicineCost=models.PositiveIntegerField(null=False)
    doctorFee=models.PositiveIntegerField(null=False)
    OtherCharge=models.PositiveIntegerField(null=False)
    total=models.PositiveIntegerField(null=False)



#medtest

class BaseMedType(models.Model):
    name = models.CharField(max_length=200, verbose_name=_('Name'))
    short_name = models.CharField(max_length=200, unique=True, blank=True, null=True, verbose_name=_('Identifier'))
    description = models.CharField(max_length=255, blank=True, null=True, verbose_name=_('Description'))

    def __str__(self):
        return self.name

    class Meta:
        abstract = True

class MedArea(BaseMedType):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if self.short_name is None or self.short_name == '':
            self.short_name = translit(self.name, 'en', reversed=True).lower().replace(' ', '_')
        super(MedArea, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'med_area'
        verbose_name = _('Med_area')
        verbose_name_plural = _('Med_areas')   

  

class MedTest(BaseMedType):
    med_area = models.ForeignKey(MedArea, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    short_name = models.CharField(max_length=100, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.short_name:
            # Generate a default short_name based on med_area and name
            slug = slugify(self.name)[:50]  # Use slugify to create a URL-friendly version of the name
            self.short_name = f"{self.med_area.short_name}_{slug}"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'med_test'
        verbose_name = _('Med_test')
        verbose_name_plural = _('Med_tests')
        
class PatientMedTest(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    med_test = models.ForeignKey(MedTest, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.patient.get_name} - {self.med_test.name}"

    class Meta:
        db_table = 'patient_med_test'
        verbose_name = _('Patient_med_test')
        verbose_name_plural = _('Patient_med_tests')   
class Treatment(models.Model):
    start_date = models.DateField(verbose_name=_('Start Date'))
    finish_date = models.DateField(verbose_name=_('Finish Date'))
    summary = models.CharField(max_length=255, verbose_name=_('Summary'))
    info = models.TextField(blank=True, null=True, verbose_name=_('Information'))
    diagnosis = models.ForeignKey('main.Diagnosis', on_delete=models.CASCADE, verbose_name=_('Diagnosis'), blank=True,
                                  null=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)

    class Meta:
        db_table = 'treatment'
        verbose_name = _('Treatment')
        verbose_name_plural = _('Treatments')


class TestRec(models.Model):
    name = models.CharField(max_length=200, verbose_name=_('Test'))
    short_name = models.CharField(max_length=200, verbose_name=_('Short Name)'))
    description = models.CharField(max_length=255, blank=True, null=True, verbose_name=_('Discription'))
    summary = models.CharField(max_length=100, blank=True, null=True, verbose_name=_('Summary'))
    info = models.TextField(blank=True, null=True, verbose_name=_('Information'))
    test_date = models.DateField(verbose_name=_('Test Date'))
    patient = models.ForeignKey('main.Patient', on_delete=models.CASCADE, related_name='test_recs',
                                verbose_name=_('Patient'))
    
     # New fields for test details
    test_name = models.CharField(max_length=200, verbose_name=_('Test Name'),null=True)
    normal_value = models.CharField(max_length=200, verbose_name=_('Normal Value'),null = True)
    results = models.CharField(max_length=200, verbose_name=_('Results'),null = True)
    units = models.CharField(max_length=50, verbose_name=_('Units'),null = True)

    class Meta:
        db_table = 'test_rec'
        verbose_name = _('Test_rec')
        verbose_name_plural = _('Test_recs')

class Diagnosis(models.Model):
    diagnosis = models.CharField(max_length=300, verbose_name=_('Diagnosis'))
    diagnosis_type = models.CharField(max_length=30, verbose_name=_('Diagnosis Type'),
                                      default='Preliminary', choices=DIAGNOSIS_TYPE)
    other_diseases = models.TextField(verbose_name=_('Other Disease'), blank=True, null=True)
    summary = models.TextField(max_length=120, blank=True, null=True)
    info = models.TextField(verbose_name=_('Information'), blank=True, null=True)
    complications = models.TextField(verbose_name=_('Complication'), blank=True, null=True)
    diagnosis_date = models.DateField(verbose_name=_('Diagnosis Date'))
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)

    class Meta:
        db_table = 'diagnosis'
        verbose_name = _('Diagnosis')
        verbose_name_plural = _('Diagnosis')
        