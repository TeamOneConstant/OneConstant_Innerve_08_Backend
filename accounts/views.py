from django.db import transaction

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated

from accounts.models import *
from accounts.helpers import *
from accounts.serializers import *




class Login(APIView):

    permission_classes = []
    authentication_classes = []

    @transaction.atomic
    def post(self, request):

        rd = request.data
        print("rd :: ", rd)

        user = CustomUser.objects.filter(mobile_number=rd['mobile_number']).first()
        print("user :: ",user)

        isNewUser = False
        if user == None:
            CustomUser.objects.create_user(mobile_number=rd['mobile_number'])
            user = CustomUser.objects.filter(mobile_number=rd['mobile_number']).first()
            print("new_user :: ", user)
            isNewUser = True

        data = CustomUserSerializer(user).data
        token = RefreshToken.for_user(user)

        return Response({"success": True, "message": "Login successful !", "data": data,
                        "isNewUser": isNewUser,
                        "authToken": {
                            'type': 'Bearer',
                            'access': str(token.access_token),
                            'refresh': str(token),
                        }})


class ProfileDetails(APIView):

    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    @transaction.atomic
    def post(self, request):

        rd = request.data
        print("rd :: ", rd)

        user = request.user
        print("user :: ",user)

        user_obj = CustomUser.objects.filter(id=user.id).first()
        user_obj.full_name = rd['full_name']
        user_obj.birth_date = formatDate(rd['birth_date'])
        user_obj.gender = rd['gender']
        user_obj.email = rd['email']
        user_obj.address = rd['address']
        user_obj.save()

        data = CustomUserSerializer(user_obj).data

        return Response({"success": True, "message": "Profile Details updated !", "data": data})






