from django.urls import path
from accounts.views import *


urlpatterns = [
    path('login', Login.as_view(), name='login'),
    path('profile-details', ProfileDetails.as_view(), name='profile-details'),
]

