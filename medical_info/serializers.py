from rest_framework.serializers import ModelSerializer
from medical_info.models import *


# MedicalReports model serializer
class MedicalReportsSerializer(ModelSerializer):

    class Meta:
        model = MedicalReports
        fields = '__all__'


# DiseaseInfo model serializer
class DiseaseInfoSerializer(ModelSerializer):

    class Meta:
        model = DiseaseInfo
        fields = '__all__'

