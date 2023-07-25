from json import loads
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from io import StringIO, BytesIO
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from docx import Document
import json
from apps.main.models import Patient, TestRec


@login_required
@csrf_exempt


def create_action(request, patient_id):
    if request.method == 'GET':
        return render(request, 'med_tests/create.html', {'patient_id': patient_id})
    elif request.method == 'POST':
        # Retrieve form data
        name = request.POST.get('name')
        test_date = request.POST.get('test_date')
        summary = request.POST.get('summary')
        info = request.POST.get('info')

        # Create MedTest object
        med_test = TestRec.objects.create(
            test_name=request.POST.get('test_name'),
            normal_value=request.POST.get('normal_value'),
            results=request.POST.get('results'),
            units=request.POST.get('units'),
            test_date=test_date,
            summary=summary,
            info=info,
            patient_id=patient_id
        )

        # Redirect to the med_test show view
        return redirect(reverse('med_tests:show', kwargs={'test_id': med_test.id}))

    return redirect(reverse('patients:create', kwargs={'patient_id': patient_id}))



@login_required
def show_action(request, test_id):
    test_rec = TestRec.objects.get(pk=test_id)

    patient = test_rec.patient
    
    
    return render(
        request,
        'med_tests/show.html',
        {
            'test_rec': test_rec,
            'patient': patient,
            
            
        }
    )


@login_required
def delete_action(request, test_id):
    test_rec = TestRec.objects.get(pk=test_id)
    test_rec.delete()
    return redirect(reverse('patients:list'))


@login_required
def dynamics_action(request, patient_id=None):
    return render(
        request,
        'med_tests/dynamics.html',
        {
            'patient': Patient.objects.get(pk=patient_id)
        }
    )


def val2str(val):
    if val is None:
        return ''
    return str(val)


@login_required
def report_action(request, test_id):
    test_rec = TestRec.objects.get(pk=test_id)
    patient = test_rec.patient

    # Create a buffer to receive the PDF data
    buffer = BytesIO()

    # Create the PDF object, using the buffer as its "file"
    doc = SimpleDocTemplate(buffer, pagesize=letter)

    # Create a list to store the contents of the PDF
    elements = []

    # Add heading
    styles = getSampleStyleSheet()
    elements.append(Paragraph(test_rec.name, styles['Heading1']))

    # Create patient table
    data = [
        ['Full name', Patient.get_name],
        ['Gender', patient.address],
        # ['Age', str(patient.age)],
        ['Date of analysis', str(test_rec.test_date)]
    ]
    table = Table(data)
    elements.append(table)

    # Add the table with test details
    test_data = [
        ['Test Name', 'Normal Value', 'Results', 'Units']
    ]
    test_data.append([
        test_rec.test_name,
        test_rec.normal_value,
        test_rec.results,
        test_rec.units
    ])
    test_table = Table(test_data)
    elements.append(test_table)

    # # Add real indicators if available
    # if test_rec.real_inds and len(test_rec.real_inds.keys()) != 0:
    #     elements.append(Paragraph('Real indicators', styles['Heading2']))
    #     data = [
    #         ['Indicator', 'Value', 'Norm', 'Unit dimensions']
    #     ]
    #     for ind, ind_value in test_rec.real_inds.items():
    #         data.append([
    #             ind_value.get('name'),
    #             str(ind_value.get('value')),
    #             '%s - %s' % (val2str(ind_value.get('min_norm', '')), val2str(ind_value.get('max_norm', ''))),
    #             val2str(ind_value.get('unit', ' - '))
    #         ])
    #     table = Table(data)
    #     elements.append(table)

    # # Add whole figures if available
    # if test_rec.int_inds and len(test_rec.int_inds.keys()) != 0:
    #     elements.append(Paragraph('Whole figures', styles['Heading2']))
    #     data = [
    #         ['Indicator', 'Value', 'Norm', 'Unit dimensions']
    #     ]
    #     for ind, ind_value in test_rec.int_inds.items():
    #         data.append([
    #             ind_value.get('name'),
    #             str(ind_value.get('value')),
    #             '%s - %s' % (val2str(ind_value.get('min_norm', '')), val2str(ind_value.get('max_norm', ''))),
    #             val2str(ind_value.get('unit', ' - '))
    #         ])
    #     table = Table(data)
    #     elements.append(table)

    # # Add string indicators if available
    # if test_rec.text_inds and len(test_rec.text_inds.keys()) != 0:
    #     elements.append(Paragraph('String indicators', styles['Heading2']))
    #     data = [
    #         ['Name', 'Value']
    #     ]
    #     for ind, ind_value in test_rec.text_inds.items():
    #         data.append([
    #             ind_value.get('name'),
    #             ind_value.get('value')
    #         ])
    #     table = Table(data)
    #     elements.append(table)

    # Build the PDF document
    doc.build(elements)

    # Get the value of the buffer
    pdf_data = buffer.getvalue()
    buffer.close()

    # Create the HTTP response with PDF content type
    response = HttpResponse(content_type='application/pdf')

    # Set the content disposition
    response['Content-Disposition'] = 'inline; filename="%s - %s (%s).pdf"' % (
        Patient.get_name, test_rec.name, test_rec.test_date
    )

    # Set the PDF content
    response.write(pdf_data)

    return response
