from django.shortcuts import render, redirect
from django.urls import reverse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import *
from .csv_tool import read_data
from .models import *


def review_project_proposal(request):
    return render(request, 'components/review_proposal.html')

def running_project(request):
    return render(request, 'components/running_project.html')
