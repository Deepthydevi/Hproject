from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User

class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,null=True, blank=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    date_of_birth = models.DateField(max_length=100, null=True, blank=True)
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')], null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    mobile = models.CharField(max_length=15, null=True, blank=True)
    email = models.EmailField(unique=True, null=True, blank=True)



    def __str__(self):
        return self.name if self.name else "No Name"

# Department Model

class Department(models.Model):
    department_choices = [
        ('Emergency', 'Emergency'),
        ('Pediatrics', 'Pediatrics'),
        ('Oncology', 'Oncology'),
        ('Radiology', 'Radiology'),
    ]
    departments = models.CharField(max_length=30, choices=department_choices, blank=True, null=True)
    description = models.TextField()

    def __str__(self):
        return self.departments

# Doctor Model
class Doctor(models.Model):
    STATUS_CHOICES = (
        ('Active', 'Active'),
        ('Inactive', 'Inactive'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE,null=True, blank=True)  # Link to the User mod
    name = models.CharField(max_length=100, null=True, blank=True)
    departments = models.ForeignKey(Department, on_delete=models.CASCADE)
    address = models.CharField(max_length=255, null=True, blank=True)
    mobile = models.CharField(max_length=15, null=True, blank=True)
    email = models.EmailField(unique=True, null=True, blank=True)
    specialization = models.CharField(max_length=100, null=True, blank=True)
    experience = models.PositiveIntegerField()  # Years of experience
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Active')

    def __str__(self):
        return self.name if self.name else "No Name"

# Appointment Model



class Appointment(models.Model):
    STATUS_CHOICES = [
            ('pending', 'Pending'),
            ('approved', 'Approved'),
            ('rejected', 'Rejected'),
        ]
    appointment_date = models.DateField(null=True, blank=True)
    symptoms = models.TextField(max_length=100, null=True, blank=True)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE,null=True, blank=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE,null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')


    def __str__(self):
        return f"Appointment with {self.doctor.name} on {self.appointment_date}"

class Prescription(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE, null=True, blank=True)
    date_issued = models.DateField(auto_now_add=True)
    medication = models.TextField()
    dosage = models.CharField(max_length=100)
    instructions = models.TextField()
    notes = models.TextField(null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)

    def __str__(self):
        return f"Prescription for {self.patient.name} by Dr. {self.doctor.name}"

class Medicine(models.Model):
    name = models.CharField(max_length=255)
    quantity = models.IntegerField()
    expiry_date = models.DateField()
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name




# Billing Model
class Billing(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_status = models.CharField(max_length=20, choices=[('Paid', 'Paid'), ('Pending', 'Pending'), ('Cancelled', 'Cancelled')], default='Pending')
    date_billed = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Bill for {self.patient.name} - {self.total_amount}"

