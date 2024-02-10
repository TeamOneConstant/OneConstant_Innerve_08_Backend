import json
from django.db import transaction
from django.http import HttpResponse, JsonResponse

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from accounts.helpers import formatDate

from backend import settings
from accounts.models import *
from doctor_app.serializers import DoctorDetailsSerializer
from medical_info.models import *
from medical_info.serializers import *
from doctor_app.models import *

import os, uuid
from django.core.files.storage import FileSystemStorage


# google cloud and llm model
import vertexai
from vertexai.language_models import TextGenerationModel
from google.cloud import aiplatform
from google.oauth2 import service_account




# key_path = f"{settings.BASE_DIR}/service_account_key.json"
# client = aiplatform.gapic.JobServiceClient.from_service_account_json(key_path)



credentials = settings.GS_CREDENTIALS


def test(request):

    vertexai.init(project="585421955813", location="us-central1", credentials=credentials)
    parameters = {
        "candidate_count": 1,
        "max_output_tokens": 1024,
        "temperature": 0.2,
        "top_p": 0.8,
        "top_k": 40
    }
    model = TextGenerationModel.from_pretrained("text-bison@001")
    model = model.get_tuned_model("projects/585421955813/locations/us-central1/models/382698216186970112")
    response = model.predict(
        # """im having chest pain, shortness of breathing, fatigue, cough with phlegm, fever and bluish lips or face give me response in json format only include disease name as key 'disease', its description as key 'description', its first aid as key 'first_aid' and all medicine details as key 'medicines'. response must be in pure json format only don't include anything other than json in response.""",
        """im having chest pain, shortness of breathing, fatigue, cough with phlegm, fever and bluish lips or face give me response in json format only include disease name as key \'disease\', its description as key \'description\', its first aid as key \'first_aid\' and all medicine details as key \'medicines\'.""",
        **parameters
    )

    print(f"Response from Model text: {response.text}")
    resps = str(str(response.text).replace('`', '').replace('json', ''))
    print(f"Response from Model json updated: {resps}")

    try:
        resps = json.loads(resps)
    except Exception as err:
        print("Error :: ", err)
        resps = json.dumps(resps)

    print(f"Response from Model json: {resps}")
    print(f"Response type: {type(resps)}")

    return JsonResponse(resps)





temp_response = {
    "disease": "Pneumonia",
    "description": "Pneumonia is an infection of the lungs that causes inflammation and fluid buildup in the air sacs.",
    "first_aid": [
        "Seek medical attention immediately.",
        "In the meantime, rest and stay hydrated.",
        "Avoid contact with others to prevent the spread of infection."
    ],
    "medicines": [
        {
        "name": "Antibiotics",
        "type": "Prescribed by a doctor",
        "usage": "To treat the underlying bacterial infection."
        },
        {
        "name": "Pain relievers",
        "type": "Over-the-counter",
        "usage": "To manage pain and discomfort."
        },
        {
        "name": "Cough suppressants",
        "type": "Over-the-counter",
        "usage": "To relieve coughing."
        }
    ]
}

tr = {
    "disease": "Tuberculosis",
    "description": "Tuberculosis is an infectious disease caused by bacteria that most commonly affects the lungs. It can also affect other parts of the body, such as the brain, kidneys, and spine.",
    "first_aid": [
        "Avoid contact with people who have active TB.",
        "Seek medical attention immediately if you have symptoms of TB.",
        "Complete the full course of treatment as prescribed by your doctor."
    ],
    "medicines": [
        {
        "name": "Isoniazid",
        "type": "Antibiotic",
        "usage": "Used to treat tuberculosis. May be given in combination with other antibiotics."
        },
        {
        "name": "Rifampicin",
        "type": "Antibiotic",
        "usage": "Used to treat tuberculosis. May be given in combination with other antibiotics."
        },
        {
        "name": "Pyrazinamide",
        "type": "Antibiotic",
        "usage": "Used to treat tuberculosis. May be given in combination with other antibiotics."
        },
        {
        "name": "Ethambutol",
        "type": "Antibiotic",
        "usage": "Used to treat tuberculosis. May be given in combination with other antibiotics."
        }
    ]
}



class PredictDisease(APIView):

    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    @transaction.atomic
    def post(self, request):

        rd = request.data
        print("rd :: ", rd)

        user = request.user
        print("user :: ",user)

        # disease prediction here

        vertexai.init(project="585421955813", location="us-central1", credentials=credentials)
        parameters = {
            "candidate_count": 1,
            "max_output_tokens": 1024,
            "temperature": 0.2,
            "top_p": 0.8,
            "top_k": 40
        }
        model = TextGenerationModel.from_pretrained("text-bison@001")
        # model = model.get_tuned_model("projects/585421955813/locations/us-central1/models/382698216186970112")
        model = model.get_tuned_model("projects/585421955813/locations/us-central1/models/283689393128996864")
        response = model.predict(
            # """im having chest pain, shortness of breathing, fatigue, cough with phlegm, fever and bluish lips or face give me response in json format only include disease name as key 'disease', its description as key 'description', its first aid as key 'first_aid' and all medicine details as key 'medicines'. response must be in pure json format only don't include anything other than json in response.""",
            f"""im having {rd['symptoms']} give me response in json format only include disease name as key \'disease\', its description as key \'description\', its first aid as key \'first_aid\' and all medicine details as key \'medicines\'.""",
            **parameters
        )

        print("response :: ", response)
        print(f"Response from Model text :: {response.text}")
        resps = str(str(response.text).replace('`', '').replace('json', ''))

        try:
            resps = json.loads(resps)
        except Exception as err:
            print("Error 230 :: ", err)
            try:
                resps = json.loads(response.text)
            except Exception as e:
                print("Error 180 :: ", e)
                return Response({"success": False, "message": "Something went wrong !"})


        print(f"Response from Model json: {resps}")
        print(f"Response type: {type(resps)}")
        print(f"Response from Model json first_aid: {resps['first_aid']}")
        print(f"Response from Model json first_aid: {type(resps['first_aid'])}")

        new_d = DiseaseInfo.objects.create(patient=user, disease=resps['disease'], description=resps['description'],
                                           first_aid=resps['first_aid'], symptoms=rd['symptoms'], medicines=resps['medicines'],
                                           json_response=resps)

        data = DiseaseInfoSerializer(new_d).data

        return Response({"success": True, "message": "Disease predicted !", "data": data})


class UploadMedicalReports(APIView):

    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    @transaction.atomic
    def post(self, request):

        user = request.user
        print("user :: ",user)

        record_list = []

        print("\nlength doc :: ", len(request.FILES.getlist('document')))
        for doc in request.FILES.getlist('document'):
        
            extension = os.path.splitext(str(doc))[1]
            unique_filename = f"{uuid.uuid4().hex}_{uuid.uuid4().hex}"

            if extension.lower() in ['.jpg', '.png', '.jpeg']:
                doc_type = "image"
            
            elif extension.lower() in ['.pdf', '.docx', '.pptx', '.xlsx']:
                doc_type = "file"
            
            elif extension.lower() in ['.mp4']:
                doc_type = "video"
            
            elif extension.lower() in ['.mp3']:
                doc_type = "audio"

            doc.name = f"{doc_type}_{unique_filename}{extension}"
            print("doc.name :: ", doc.name)

            new_report = MedicalReports.objects.create(patient=user, document_type=doc_type, added_by="patient", document_url=doc)

            record_list.append(new_report)

        data = MedicalReportsSerializer(record_list, many=True).data

        return Response({"success": True, "message": "Medical report uploaded!", "data": data})


class PostReportInfo(APIView):

    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    @transaction.atomic
    def post(self, request):

        rd = request.data
        print("rd :: ", rd)

        user = request.user
        print("user :: ",user)

        mr = MedicalReports.objects.filter(id=rd['mr_id']).first()
        ReportInfo.objects.create(report=mr, patient=user, information=rd['info'])

        return Response({"success": True, "message": "Report information saved !"})


class AppointmentAPI(APIView):

    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    @transaction.atomic
    def get(self, request):

        a_id = request.GET.get('a_id', None)

        if a_id is not None:
            appointment = Appointment.objects.filter(id=a_id).first()
            data = AppointmentSerializer(appointment).data
            return Response({"success": True, "message": "Appointment fetched !", "data": data})

        return Response({"success": False, "message": "Something went wrong !"})


    @transaction.atomic
    def post(self, request):

        rd = request.data
        print("rd :: ", rd)

        user = request.user
        print("user :: ",user)

        if Appointment.objects.filter(state="booked", date=formatDate(rd['date']), time=rd['time'], booking_for=rd['booking_for']).exists():
            return Response({"success": False, "message": "Appointment already booked !"})


        if rd['booking_for'] == "other":
            new_a = Appointment.objects.create(date=formatDate(rd['date']), time=rd['time'], booking_for=rd['booking_for'], 
                                               name=rd['name'], gender=rd['gender'], age=rd['age'])
        elif rd['booking_for'] == "self":
            new_a = Appointment.objects.create(patient=user, date=formatDate(rd['date']), time=rd['time'], booking_for=rd['booking_for'],)

        else:
            new_a = None

        data = AppointmentSerializer(new_a).data

        return Response({"success": True, "message": "Appointment booked successfully !", "data": data})









