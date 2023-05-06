from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from accounts.models import CustomUser
from django.db.models import Count
from django.utils import timezone
import json
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from chat.serializers import ChatRoomSerializer
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

@login_required
def home(request):
    return render(request, 'home/home.html')



