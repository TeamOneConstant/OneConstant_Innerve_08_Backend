from django.db import transaction
from django.http import HttpResponse

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated

from medical_info.models import *
from doctor_app.models import *
from doctor_app.serializers import *




class GetDoctorList(APIView):

    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    @transaction.atomic
    def get(self, request):

        user = request.user
        print("user :: ",user)

        disease = DiseaseInfo.objects.filter(patient=user).order_by('id').last()
        print("disease :: ", disease.disease)
        
        doctors = DoctorDetails.objects.filter(diseases_can_treat__contains=[disease.disease]).order_by('-rating')
        data = DoctorDetailsSerializer(doctors, many=True).data

        return Response({"success": True, "message": "Doctors list fetched !", "data": data})


class GetDoctorAvailabilityList(APIView):

    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    @transaction.atomic
    def get(self, request):

        user = request.user
        print("user :: ",user)

        doc = DoctorDetails.objects.filter(user__id=user.id).first()
        dv = DoctorAvailability.objects.filter(doctor=doc)

        data = DoctorAvailabilitySerializer(dv, many=True)

        return Response({"success": True, "message": "Doctors list fetched !", "data": data})






