from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),

    path('patient-dashboard/', views.patient_dashboard, name='patient_dashboard'),
    path('doctor-dashboard/', views.doctor_dashboard, name='doctor_dashboard'),

    path('patients/', views.patient_list, name='patient_list'),
    path('patients/add/', views.add_patient, name='add_patient'),

    path('doctors/', views.doctor_list, name='doctor_list'),
    path('doctors/add/', views.add_doctor, name='add_doctor'),

    path('appointments/', views.appointment_list, name='appointment_list'),
    path('appointments/add/', views.add_appointment, name='add_appointment'),

    path('records/', views.record_list, name='record_list'),
    path('records/add/', views.add_record, name='add_record'),

    path('api/patients/', views.api_patients, name='api_patients'),
    path('api/doctors/', views.api_doctors, name='api_doctors'),
    path('api/appointments/', views.api_appointments, name='api_appointments'),
    path('api/records/', views.api_records, name='api_records'),
]