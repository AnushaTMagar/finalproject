from django.contrib import admin
from .models import *
from django.utils.translation import gettext_lazy as _
from django_json_widget.widgets import JSONEditorWidget


# Register your models here.
class DoctorAdmin(admin.ModelAdmin):
    pass
admin.site.register(Doctor, DoctorAdmin)

class PatientAdmin(admin.ModelAdmin):
    pass
admin.site.register(Patient, PatientAdmin)

class AppointmentAdmin(admin.ModelAdmin):
    pass
admin.site.register(Appointment, AppointmentAdmin)

class PatientDischargeDetailsAdmin(admin.ModelAdmin):
    pass
admin.site.register(PatientDischargeDetails, PatientDischargeDetailsAdmin)

@admin.register(MedArea)
class MedAreaAdmin(admin.ModelAdmin):
    list_display = ('name', 'short_name', 'description')
    ordering = ('name',)
    search_fields = ('name',)


@admin.register(MedTest)
class MedTestAdmin(admin.ModelAdmin):
    list_display = ('name', 'short_name', 'description', '_view_med_area')
    ordering = ('name',)
    search_fields = ('name',)
    

    def _view_med_area(self, med_test):
        return med_test.med_area

    _view_med_area.short_description = _('medical field')











@admin.register(TestRec)
class TestRecAdmin(admin.ModelAdmin):
    list_display = ('name', 'summary', 'info', 'test_date', '_view_patient')
    ordering = ('test_date',)
    list_filter = ('name',)
    formfield_overrides = {
        JSONField: {'widget': JSONEditorWidget},
    }

    def _view_patient(self, rec):
        return rec.patient.short_info

    _view_patient.short_description = _('Patient')



@admin.register(Diagnosis)
class DiagnosisAdmin(admin.ModelAdmin):
    list_display = ('diagnosis_date', 'diagnosis_type', 'diagnosis', '_view_patient')
    ordering = ('diagnosis_date',)
    list_filter = ('diagnosis_type',)

    def _view_patient(self, diagnosis):
        return diagnosis.patient.short_info

    _view_patient.short_description = _('Patient')


@admin.register(Treatment)
class TreatmentAdmin(admin.ModelAdmin):
    list_display = ('start_date', 'finish_date', 'summary', '_view_diagnosis', '_view_patient')
    ordering = ('start_date',)

    def _view_diagnosis(self, treatment):
        if treatment.diagnosis is not None:
            return treatment.diagnosis.diagnosis
        return '-'

    def _view_patient(self, treatment):
        return treatment.patient.short_info

    _view_patient.short_description = _('Patient')
    _view_diagnosis.short_description = _('Diagnosis')