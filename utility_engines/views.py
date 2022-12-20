from django.shortcuts import render, HttpResponse
from observer.models import *
from utility_engines.timeframe_estimation import suggest_timeframe
from rest_framework.response import Response
from rest_framework.decorators import api_view

# Create your views here.

@api_view(['GET'])
def suggest_query(request, pk):
    project = Proposed_Project.objects.get(project__id=pk)
    res = suggest_timeframe(project)
    if res is None:
        return Response({
            'cycle' : True
        })
    else:
        return Response({
            'cycle' : False,
            'start' : res[0],
            'end' : res[1],
        })