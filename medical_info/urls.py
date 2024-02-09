from django.urls import path
from medical_info.views import *


urlpatterns = [
    path('predict-disease', PredictDisease.as_view(), name="predict-disease"),
    path('upload-report', UploadMedicalReports.as_view(), name="upload-report"),
    path('report-ocr-info', PostReportInfo.as_view(), name="report-ocr-info"),
    path('appointment', AppointmentAPI.as_view(), name="appointment"),

]


