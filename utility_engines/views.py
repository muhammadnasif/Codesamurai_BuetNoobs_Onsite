from django.shortcuts import render, HttpResponse
from observer.models import *
from utility_engines.timeframe_estimation import suggest_timeframe, compute_expected_ends, suggest_timeframe_forall, compute_expected_ends_detailed
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


@api_view(['POST'])
def expected_ends_post(request):
    ends = compute_expected_ends()
    if ends:
        # update all approved projects with new expected ends
        for project in Approved_Project.objects.all():
            if project.project.id in ends:
                project.expected_end = ends[project.project.id]
                project.save()
                
        return Response({
            'success' : True,
            'cycle' : False,
        })
    else:
        return Response({
            'success' : False,
            'cycle' : True,
        })


def update_ends():
    ends = compute_expected_ends()
    if ends:
        # update all approved projects with new expected ends
        for project in Approved_Project.objects.all():
            if project.project.id in ends:
                project.expected_end = ends[project.project.id]
                project.save()
                
@api_view(['GET'])
def expected_ends_with(request, pk):
    project = Proposed_Project.objects.get(project__id=pk)
    ends = compute_expected_ends_detailed(project)
    if ends is None:
        return Response({
            'cycle' : True,
            'ends' : []
        })
    else:
        return Response({
            'cycle' : False,
            'ends' : ends
        })
    
@api_view(['GET'])
def suggest_all(request):
    projects = Proposed_Project.objects.all()
    res = suggest_timeframe_forall(projects)
    return Response(res)
