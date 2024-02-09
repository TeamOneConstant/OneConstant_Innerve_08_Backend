from django.db import models
from accounts.models import CustomUser
from doctor_app.models import DoctorDetails
from django.contrib.postgres.fields import ArrayField

# Create your models here.


class DiseaseInfo(models.Model):

    patient = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    disease = models.CharField(max_length=512, blank=True, null=True)
    description = models.TextField(max_length=1024, blank=True, null=True)
    first_aid = ArrayField(models.CharField(max_length=512, blank=True), size=30, null=True, blank=True)
    medicines = models.JSONField(max_length=2048, blank=True, null=True)
    symptoms = models.TextField(max_length=1024)

    text_response = models.TextField(max_length=2048, blank=True, null=True)
    json_response = models.JSONField(max_length=2048, blank=True, null=True)

    # timestamps
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)


class MedicalReports(models.Model):

    patient = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    document_type = models.CharField(max_length=16)
    document_url = models.FileField(upload_to="medical_reports", null=True, blank=True)
    # added_by => patient | doctor
    added_by = models.CharField(max_length=32, null=True, blank=True)
    doctor = models.ForeignKey(DoctorDetails, on_delete=models.CASCADE, null=True, blank=True)

    # timestamps
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)


class ReportInfo(models.Model):

    patient = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    report = models.ForeignKey(MedicalReports, on_delete=models.CASCADE)
    information = models.TextField(max_length=2048, blank=True, null=True)

    # timestamps
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

