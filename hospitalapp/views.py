
import stripe
from django.conf import settings
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse

from .models import Patient, Doctor, Appointment, Department, Prescription, Medicine
from .forms import PatientForm, DoctorForm, AppointmentForm, DepartmentForm, UserregistrationForm, \
    PatientRegistrationForm, PatientDetailForm, DoctorRegistrationForm, AdminSignup, UserForm, PrescriptionForm, \
    MedicineForm

from . import forms,models

# Create your views here.

def index(request):
    return render(request,'home.html')

def admin(request):
    return render(request,'index-2.html')

def patienthome(request):
    return render(request,'patient-home.html')
# Patient Views

def AdminSignup(request):
    if request.method == 'POST':
        form = forms.AdminSignup(request.POST)
        if form.is_valid():
            user = form.save()
            user.set_password(form.cleaned_data['password'])
            user.save()
            return redirect('admin-loginview')
    else:
        form = forms.AdminSignup()
    return render(request, 'admin-signup1.html', {'form': form})
def adminloginviewform(request):
    return render(request,'admin-loginview.html')
def adminloginview(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('admin-dashboard')
        else:
            messages.error(request, "Invalid username or password.")

    return render(request, 'admin-loginview.html')


def totalcountofpatients(request):
    patients = Patient.objects.all()
    patient_count = patients.count()
    doctors=Doctor.objects.all()
    doctors_count=doctors.count()
    appoinments= Appointment.objects.all()
    appoinments_count=appoinments.count()
    return render(request, 'patientlist.html', {'patients': patients, 'patient_count': patient_count, 'doctors_count': doctors_count, 'appoinments_count' : appoinments_count })


#patient
def patientSignup(request):
    if request.method == 'POST':
        user_form = UserregistrationForm(request.POST)
        if user_form.is_valid():
            password = user_form.cleaned_data['password']
            cpassword = user_form.cleaned_data['cpassword']

            if password != cpassword:
                messages.error(request, "Passwords do not match!")
                return render(request, 'patient-register.html', {'user_form': user_form})
            else:

                user = User(username=user_form.cleaned_data['username'])
                user.set_password(password)
                user.save()


                patient = Patient.objects.create(
                    user=user,
                    name=user_form.cleaned_data['name'],
                    date_of_birth=user_form.cleaned_data['date_of_birth'],
                    gender=user_form.cleaned_data['gender'],
                    address=user_form.cleaned_data['address'],
                    mobile=user_form.cleaned_data['mobile'],
                    email=user_form.cleaned_data['email'],

                )

                messages.success(request, "Account created successfully. You can now log in.")
                return redirect('patient-login')
    else:
        user_form = UserregistrationForm()

    return render(request, 'patient-register.html', {'user_form': user_form})


def patientLoginView(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)


            try:
                patient = Patient.objects.get(user=user)

                return render(request, 'submit_patientdetails.html', {'patient': patient})
            except Patient.DoesNotExist:
                messages.error(request, "Patient profile not found.")
                return redirect('patient-login')
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, 'patient-login.html')



def appointment_list_by_patient(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    appointments = Appointment.objects.filter(patient=patient).order_by('-date')

    context = {
        'patient': patient,
        'appointments': appointments,
    }
    return render(request, 'appointment_list_by_patient.html', context)


def patient_viewdetails(request):
    patient = get_object_or_404(Patient, user=request.user)


    form = PatientDetailForm(instance=patient)

    context = {
        'form': form,
        'user': request.user,
    }
    return render(request, 'submit_patientdetails.html', context)


def patient_adddetails(request):
    patient = get_object_or_404(Patient, user=request.user)

    if request.method == 'POST':
        form = PatientDetailForm(request.POST, instance=patient)

        if form.is_valid():
            form.save()
            messages.success(request, "Details updated successfully!")
            return redirect('submit-details')
        else:
            messages.error(request, "There was an error with the details provided.")

    else:
        form = PatientDetailForm(instance=patient)

    context = {
        'form': form,
        'user': request.user,
    }
    return render(request, 'submit_patientdetails.html', context)


def view_patient(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    return render(request, 'view_patient.html', {'patient': patient})



def book_appointment(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)

    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.patient = patient
            appointment.save()

            messages.success(request, 'Appointment booked successfully!')
            return redirect('view-appoinments', patient_id=patient.id)
    else:

        initial_data = {
            'status': 'pending'
        }
        form = AppointmentForm(initial=initial_data)  # Pass initial data to the form


    doctors = Doctor.objects.all()

    return render(request, 'book_appointment.html', {
        'form': form,
        'patient_name': patient.name,
        'doctors': doctors,
        'patient': patient
    })


def view_appointments(request, patient_id):
    # Get the patient object based on the ID
    patient = get_object_or_404(Patient, id=patient_id)
    appointments = Appointment.objects.filter(patient=patient).prefetch_related(
        'prescription_set')
    return render(request, 'view_appointments.html', {
        'patient': patient,
        'appointments': appointments
    })



def admin_appointmentlist(request):
    appointments = Appointment.objects.all().select_related('doctor', 'patient')
    if request.method == 'POST':
        appointment_id = request.POST.get('appointment_id')
        new_status = request.POST.get('status')

        appointment = get_object_or_404(Appointment, id=appointment_id)
        appointment.status = new_status
        appointment.save()

        return redirect('all-appoinments')

    return render(request, 'admin-appoinments.html', {
        'appointments': appointments,
    })


def patient_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('add-patient-details')
        else:
            messages.error(request, 'Invalid credentials')
            return redirect('patient_login')
    return render(request, 'login.html')

def add_patient_details(request):
    if request.method == 'POST':
        form = PatientDetailForm(request.POST)
        if form.is_valid():
            patient = form.save(commit=False)
            patient.user = request.user
            patient.save()
            messages.success(request, 'Your details have been submitted successfully!')

    else:
        form = PatientDetailForm()

    return render(request, 'add_patient_details.html', {
        'form': form,
    })

# admin side
def add_patient(request):
    if request.method == 'POST':
        form = PatientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('patient-list')
    else:
        form = PatientForm()
    return render(request, 'admin-add-patient.html', {'form': form})

def patient_list(request):
    patients = Patient.objects.all()
    return render(request, 'patient-list.html', {'patients': patients})


def update_patient_view(request, pk):
    patient = get_object_or_404(Patient, id=pk)

    if request.method == 'POST':
        form = PatientForm(request.POST, instance=patient)
        if form.is_valid():
            form.save()
            return redirect('patient-list')
    else:
        form = PatientForm(instance=patient)

    return render(request, 'update_patient.html', {'form': form, 'patient': patient})

def delete_patient_view(request, pk):
    patient = get_object_or_404(Patient, id=pk)
    patient.delete()
    return redirect('patient-list')

# Doctor Views by admin
def add_doctor(request):
    if request.method == 'POST':
        form = DoctorForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Doctor added successfully!')
            return redirect('doctor-list')
        else:
            # If the form is not valid, you can add this line to see the errors
            messages.error(request, 'Please correct the errors below.')
    else:
        form = DoctorForm()

    return render(request, 'admin-add_doctor.html', {'form': form})


def doctor_list(request):
    doctors = Doctor.objects.all()
    return render(request, 'admin-doctor_list.html', {'doctors': doctors})

def update_doctor_view(request, pk):
    doctor = get_object_or_404(Doctor, id=pk)
    departments = Department.objects.all()

    if request.method == 'POST':
        form = DoctorForm(request.POST, instance=doctor)
        if form.is_valid():
            form.save()
            return redirect('doctor-list')
    else:
        form = DoctorForm(instance=doctor)

    return render(request, 'admin-update_doctor.html', {'form': form, 'doctor': doctor, 'departments': departments})

def delete_doctor_view(request, pk):
    doctor = get_object_or_404(Doctor, id=pk)
    doctor.delete()
    return redirect('doctor-list')

# Appointment Views

def appointment_list(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    appointments = Appointment.objects.filter(patient=patient)
    return render(request, 'appointment_list.html', {
        'patient': patient,
        'appointments': appointments,
    })

#admin
def add_appointment(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('appointment_list')
    else:
        form = AppointmentForm()
    patients = Patient.objects.all()
    doctors = Doctor.objects.all()

    return render(request, 'book_appointment.html', {
        'form': form,
        'patients': patients,
        'doctors': doctors,
    })

# Department Views
def add_department(request):
    if request.method == 'POST':
        form = DepartmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('department_list')
    else:
        form = DepartmentForm()
    return render(request, 'hospital/add_department.html', {'form': form})

def department_list(request):
    departments = Department.objects.all()
    return render(request, 'hospital/department_list.html', {'departments': departments})

#doctor
def doctors_dashboard(request):
    doctor = get_object_or_404(Doctor, user=request.user)
    return render(request, 'doctors_dashboad.html', {'doctor': doctor})

def doctor_signup(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        doctor_form = DoctorForm(request.POST)

        if user_form.is_valid() and doctor_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password'])
            user.save()
            doctor = doctor_form.save(commit=False)
            doctor.user = user
            doctor.save()
            messages.success(request, 'Doctor created successfully.')
            return redirect('doctor-login')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        user_form = UserForm()
        doctor_form = DoctorForm()

    return render(request, 'doctor_signup.html', {
        'user_form': user_form,
        'doctor_form': doctor_form
    })

def doctor_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('doctor-dashboard')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")

    else:
        form = AuthenticationForm()

    return render(request, 'doctor-login.html', {'form': form})

def doctor_appointmentsform(request):
    return render(request,'doctor_appointments.html')
def doctor_appointments(request, doctor_id):
    doctor = get_object_or_404(Doctor, id=doctor_id)
    appointments = Appointment.objects.filter(doctor=doctor, status='approved')

    return render(request, 'doctor_appointments.html', {
        'doctor': doctor,
        'appointments': appointments,
    })

def doctor_patients_records(request, doctor_id):
    doctor = get_object_or_404(Doctor, id=doctor_id)
    patients = Appointment.objects.filter(doctor=doctor).select_related('patient').values(
        'patient__name',
        'symptoms'
    ).distinct()
    context = {
        'doctor': doctor,
        'patients': patients
    }
    return render(request, 'doctor_patients_records.html', context)

def doctor_appointments_with_prescriptions(request, doctor_id):
    doctor = get_object_or_404(Doctor, id=doctor_id)
    appointments = Appointment.objects.filter(doctor=doctor)
    medicines = Medicine.objects.all()  # Fetch all medicines

    if request.method == "POST":
        appointment_id = request.POST.get('appointment_id')
        appointment = get_object_or_404(Appointment, id=appointment_id)
        form = PrescriptionForm(request.POST)

        if form.is_valid():
            prescription = form.save(commit=False)
            prescription.appointment = appointment
            prescription.patient = appointment.patient
            prescription.doctor = doctor
            prescription.save()

            return redirect('doctor_patient_prescriptions', doctor_id=doctor_id)
        else:
            messages.error(request, "Failed to add prescription. Please check your input.")

    context = {
        'doctor': doctor,
        'appointments': appointments,
        'medicines': medicines,
        'form': PrescriptionForm(),
    }
    return render(request, 'doctor_prescriptions.html', context)




def add_medicine(request):
    if request.method == 'POST':
        form = MedicineForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('add_medicine')
    else:
        form = MedicineForm()

    return render(request, 'add_medicine.html', {'form': form})

def medicine_list(request):
    medicines = Medicine.objects.all()
    return render(request, 'medicine_list.html', {'medicines': medicines})

def create_checkout_session(request, appointment_id):
    appointment = Appointment.objects.get(id=appointment_id)
    prescriptions = appointment.prescription_set.all()

    if prescriptions:

        stripe.api_key = settings.STRIPE_SECRET_KEY

        if request.method == 'POST':
            line_items = []
            for prescription in prescriptions:

                line_item = {
                    'price_data': {
                        'currency': 'INR',
                        'unit_amount': int(prescription.amount * 100),
                        'product_data': {
                            'name': prescription.medication,
                        },
                    },
                    'quantity': 1,
                }
                line_items.append(line_item)

            if line_items:
                checkout_session = stripe.checkout.Session.create(
                    payment_method_types=['card'],
                    line_items=line_items,
                    mode='payment',
                    success_url=request.build_absolute_uri(reverse('payment_success')) + '?session_id={CHECKOUT_SESSION_ID}',
                    cancel_url=request.build_absolute_uri(reverse('payment_cancel')),
                )

                return redirect(checkout_session.url, code=303)
    return render(request, 'no_prescriptions.html', {'appointment': appointment})


def payment_success(request):
    session_id = request.GET.get('session_id')
    return render(request, 'payment_success.html', {'session_id': session_id})

def payment_cancel(request):
    return render(request, 'payment_cancel.html')
