from django.http import JsonResponse
from django.shortcuts import render, redirect
from .models import Patient, Doctor, Appointment, PatientRecord, Notification
from .forms import PatientForm, DoctorForm, AppointmentForm, PatientRecordForm


def home(request):
    return render(request, 'hospital/home.html', {
        'patients': Patient.objects.count(),
        'doctors': Doctor.objects.count(),
        'appointments': Appointment.objects.count(),
        'records': PatientRecord.objects.count(),
        'notifications': Notification.objects.filter(is_read=False).count(),
    })


def patient_dashboard(request):
    patients = Patient.objects.all()
    appointments = Appointment.objects.all().order_by('-appointment_date')
    records = PatientRecord.objects.all().order_by('-visit_date')
    notifications = Notification.objects.all().order_by('-created_at')

    return render(request, 'hospital/patients_dashboard.html', {
        'patients': patients,
        'appointments': appointments,
        'records': records,
        'notifications': notifications,
    })


def doctor_dashboard(request):
    doctors = Doctor.objects.all()
    appointments = Appointment.objects.all().order_by('-appointment_date')
    records = PatientRecord.objects.all().order_by('-visit_date')

    return render(request, 'hospital/doctor_dashboard.html', {
        'doctors': doctors,
        'appointments': appointments,
        'records': records,
    })


def patient_list(request):
    patients = Patient.objects.all()
    return render(request, 'hospital/patient_list.html', {'patients': patients})


def add_patient(request):
    form = PatientForm(request.POST or None)

    if form.is_valid():
        patient = form.save()
        Notification.objects.create(
            patient=patient,
            message="Registration successful. Welcome to the Healthcare System."
        )
        return redirect('patient_list')

    return render(request, 'hospital/form.html', {
        'form': form,
        'title': 'Patient Registration',
    })


def doctor_list(request):
    search = request.GET.get('search', '')
    doctors = Doctor.objects.all()

    if search:
        doctors = doctors.filter(specialization__icontains=search)

    return render(request, 'hospital/doctor_list.html', {
        'doctors': doctors,
        'search': search,
    })


def add_doctor(request):
    form = DoctorForm(request.POST or None)

    if form.is_valid():
        form.save()
        return redirect('doctor_list')

    return render(request, 'hospital/form.html', {
        'form': form,
        'title': 'Add Doctor Profile',
    })


def appointment_list(request):
    appointments = Appointment.objects.all().order_by('-appointment_date')
    return render(request, 'hospital/appointment_list.html', {
        'appointments': appointments,
    })


def add_appointment(request):
    form = AppointmentForm(request.POST or None)

    if form.is_valid():
        appointment = form.save()
        Notification.objects.create(
            patient=appointment.patient,
            message=f"Appointment booked with Dr. {appointment.doctor.name} on {appointment.appointment_date}."
        )
        return redirect('appointment_list')

    return render(request, 'hospital/form.html', {
        'form': form,
        'title': 'Book Appointment',
    })


def record_list(request):
    records = PatientRecord.objects.all().order_by('-visit_date')
    return render(request, 'hospital/records_list.html', {'records': records})


def add_record(request):
    form = PatientRecordForm(request.POST or None)

    if form.is_valid():
        record = form.save()
        Notification.objects.create(
            patient=record.patient,
            message="New medical record and prescription added."
        )
        return redirect('record_list')

    return render(request, 'hospital/form.html', {
        'form': form,
        'title': 'Add Medical History / Prescription',
    })


def api_patients(request):
    data = list(Patient.objects.values())
    return JsonResponse(data, safe=False)


def api_doctors(request):
    data = list(Doctor.objects.values())
    return JsonResponse(data, safe=False)


def api_appointments(request):
    data = list(Appointment.objects.values(
        'id',
        'patient__name',
        'doctor__name',
        'appointment_date',
        'appointment_time',
        'reason',
        'status'
    ))
    return JsonResponse(data, safe=False)


def api_records(request):
    data = list(PatientRecord.objects.values(
        'id',
        'patient__name',
        'doctor__name',
        'diagnosis',
        'treatment',
        'prescription',
        'visit_date',
        'notes'
    ))
    return JsonResponse(data, safe=False)
