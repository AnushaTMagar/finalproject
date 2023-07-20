from django.contrib import admin
from .models import doctor
# Register your models here.
class DoctorAdmin(admin.ModelAdmin):
    pass
admin.site.register(doctor, DoctorAdmin)