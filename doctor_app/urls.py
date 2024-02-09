from django.urls import path
from doctor_app.views import *


urlpatterns = [
    path('get-list', GetDoctorList.as_view(), name="get-doctor-list"),
    path('get-availability', GetDoctorAvailabilityList.as_view(), name="get-doctor-availability"),
]

# ssed1071ki1072ran0144nwifi