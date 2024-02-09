from django.db import models
from accounts.models import CustomUser
from django.contrib.postgres.fields import ArrayField





class DoctorDetails(models.Model):

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    speciality = ArrayField(models.CharField(max_length=32), size=10)
    diseases_can_treat = ArrayField(models.CharField(max_length=32), size=30, blank=True, null=True)
    experience = models.CharField(max_length=16)
    patient_count = models.IntegerField(default=0)
    is_verified = models.BooleanField(default=False)
    consultation_fees = models.IntegerField(default=0)

    rating = models.FloatField(default=0)

    clinic_name = models.CharField(max_length=64)
    clinic_website = models.CharField(max_length=128)
    clinic_phone_number = models.CharField(max_length=16)
    clinic_address = models.TextField(max_length=1024)

    # timestamps
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)




class DoctorReviews(models.Model):

    doctor = models.ForeignKey(DoctorDetails, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)
    review = models.TextField(max_length=2048, blank=True, null=True)
    added_by = models.CharField(max_length=64, default="Anonymous")

    # timestamps
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)




class DoctorAvailability(models.Model):

    doctor = models.ForeignKey(DoctorDetails, on_delete=models.CASCADE)
    day = models.CharField(max_length=16)
    from_time = models.TimeField()
    to_time = models.TimeField()
    hospital_name = models.CharField(max_length=256)
    is_own_clinic = models.BooleanField(default=False)

    # timestamps
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)



