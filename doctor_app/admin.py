from django.contrib import admin
from doctor_app.models import *

# Register your models here.

admin.site.register(DoctorDetails)
admin.site.register(DoctorReviews)
admin.site.register(DoctorAvailability)

