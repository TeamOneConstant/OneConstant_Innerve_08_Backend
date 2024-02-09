from rest_framework.serializers import ModelSerializer
from accounts.models import *


# CustomUser model serializer
class CustomUserSerializer(ModelSerializer):

    class Meta:
        model = CustomUser
        exclude = ('password', 'is_active', 'is_staff', 'is_superuser', 'user_permissions', 'groups')

