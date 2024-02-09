from django.contrib import admin
from medical_info.models import *

# Register your models here.


admin.site.register(DiseaseInfo)
admin.site.register(MedicalReports)
admin.site.register(ReportInfo)
admin.site.register(Appointment)

