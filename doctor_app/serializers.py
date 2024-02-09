from rest_framework.serializers import ModelSerializer
from doctor_app.models import *


# DoctorDetails model serializer
class DoctorDetailsSerializer(ModelSerializer):

    class Meta:
        model = DoctorDetails
        fields = '__all__'


# DoctorAvailability model serializer
class DoctorAvailabilitySerializer(ModelSerializer):

    class Meta:
        model = DoctorAvailability
        fields = '__all__'

