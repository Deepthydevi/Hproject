from django import forms
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from .models import Patient, Doctor, Prescription, Medicine, Billing
from .models import Patient, Doctor, Appointment, Department,Prescription


class AdminSignup(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','username','password']
        widgets = {
        'password': forms.PasswordInput()
        }

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    cpassword = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'password', 'cpassword']



class PatientRegistrationForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['name', 'date_of_birth', 'gender', 'address', 'mobile', 'email']

class DoctorRegistrationForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = ['name', 'departments', 'address', 'mobile', 'email', 'specialization', 'experience', 'status']

class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = '__all__'

class DoctorForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = ['name', 'departments', 'address', 'mobile', 'email', 'specialization', 'experience', 'status']

        # Optional: Add custom widgets if you want to style the dropdown or other fields
        widgets = {
            'departments': forms.Select(attrs={'class': 'form-control'}),  # To style the dropdown
        }

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['appointment_date', 'symptoms', 'doctor']

    doctor = forms.ModelChoiceField(
        queryset=Doctor.objects.all(),
        to_field_name='id',  # Use the id of the doctor
        empty_label="Select a Doctor"
    )

class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = '__all__'

class PatientDetailForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = '__all__' # Add other fields as needed

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password']
        widgets = {
            'password': forms.PasswordInput(),
        }
class PrescriptionForm(forms.ModelForm):
    class Meta:
        model = Prescription
        fields = ['medication', 'dosage', 'instructions', 'notes', 'amount']

class MedicineForm(forms.ModelForm):
    class Meta:
        model = Medicine
        fields = ['name',  'quantity', 'expiry_date', 'description']


class UserregistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    cpassword = forms.CharField(widget=forms.PasswordInput)

    # Fields related to the Patient model
    name = forms.CharField(max_length=100)
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    gender = forms.ChoiceField(choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')])
    address = forms.CharField(max_length=255)
    mobile = forms.CharField(max_length=15)
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'password', 'cpassword', 'name', 'date_of_birth', 'gender', 'address', 'mobile', 'email']

class BillingForm(forms.ModelForm):
    class Meta:
         model = Billing
         fields = ['total_amount', 'payment_status']