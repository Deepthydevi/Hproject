from django.urls import path
from hospitalapp import views
urlpatterns = [
    #admin
    path('', views.index, name='index'),
    path('admin-signup/', views.AdminSignup, name='admin-signup'),
    path('admin-loginviewform', views.adminloginviewform, name='admin-loginview1'),
    path('admin-loginview', views.adminloginview, name='admin-loginview'),
    path('admin-dashboard/', views.admin, name='admin-dashboard'),
    path('admin-patientlist/', views.totalcountofpatients, name='totalpatients'),
    path('add-patient/', views.add_patient, name='add-patient'),
    path('view-patient/', views.patient_list, name='patient-list'),
    path('update-patient/<int:pk>/', views.update_patient_view, name='update-patient'),
    path('delete-patient/<int:pk>/', views.delete_patient_view, name='delete-patient'),
    path('add-doctor/', views.add_doctor, name='add-doctor'),
    path('doctor-list/', views.doctor_list, name='doctor-list'),
    path('update-doctor/<int:pk>/', views.update_doctor_view, name='update-doctor'),
    path('delete-doctor/<int:pk>/', views.delete_doctor_view, name='delete-doctor'),
    path('all-appoinments/', views.admin_appointmentlist, name='all-appoinments'),
    #patients
    #path('patient-login/', views.patienthome, name='patient-login'),
    path('patient_dashboard/', views.patienthome, name='patient_dashboard'),
    path('patient-register/', views.patientSignup, name='register'),
    path('patient-form/', views.patient_login, name='login'),
    path('patient-login/', views.patientLoginView, name='patient-login'),
    path('submit-details/', views.patient_viewdetails, name='submit-details'),
    path('view-patient/<int:patient_id>/', views.view_patient, name='view_patient'),
   # path('list_patient_details_by_patient/', views.list_patient_details_by_patient, name='list_patient_details_by_patient'),
    path('add-patient-details/<int:patient_id>/', views.add_patient_details, name='add-patient-details'),
    #path('appointment_list_by_patient/', views.appointment_list_by_patient, name='appointment_list_by_patient'),

    path('book-appointment/<int:patient_id>/', views.book_appointment, name='book_appointment'),
    #path('register_patient/', views.register_patient, name='register_patient')
    path('appointment_list/<int:patient_id>/', views.appointment_list, name='appointment_list'),
    path('view-appoinments/<int:patient_id>/', views.view_appointments, name='view-appoinments'),
    path('doctor-registration/', views.doctor_signup, name='doctor-registration'),
    path('doctor-login/', views.doctor_login, name='doctor-login'),
    path('doctor-dashboard/', views.doctors_dashboard, name='doctor-dashboard'),
    path('doctor_appointments/', views.doctor_appointmentsform, name='doctor_appointmentsform'),
    path('doctor-appoinments/<int:doctor_id>/', views.doctor_appointments, name='doctor-appoinments'),
    path('doctor_patients_records/<int:doctor_id>/', views.doctor_patients_records, name='doctor_patients_records'),
    # Modify the existing pattern
    path('doctor/<int:doctor_id>/prescriptions/', views.doctor_appointments_with_prescriptions, name='doctor_patient_prescriptions'),
    path('add_medicine/', views.add_medicine, name='add_medicine'),
    path('medicine_list/', views.medicine_list, name='medicine_list'),
    path('create-checkout-session/<int:appointment_id>/', views.create_checkout_session, name='create_checkout_session'),
    path('payment_success/', views.payment_success, name='payment_success'),
    path('payment_cancel/', views.payment_cancel, name='payment_cancel')



]
