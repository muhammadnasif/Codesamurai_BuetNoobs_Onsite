from django.shortcuts import render, redirect
from django.urls import reverse
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .csv_tool import  read_data
from .models import *
# Create your views here.


def load(request):
    if 'username' in request.session:
        return render(request, 'base/base.html')
    else:
        return redirect(reverse('login'))

@api_view(['GET'])
def projects(request):
    read_data()
    project_list = [
        project_convert(p) for p in Project.objects.all()
    ]
    return Response(project_list)


@api_view(['GET'])
def filter_projects(request):
    categories = request.GET.getlist('category')
    project_list = [
        project_convert(p) for p in Project.objects.filter(category__in=categories)
    ]
    return Response(project_list)


def project(request):
    if request.method == "POST":
        print(request.POST)
    return render(request, 'components/project.html')


@api_view(['POST'])
def post_issue(request, pk):
    print(request.POST)
    return Response({'result' : 'ok'})


def project_convert(project):
    return {
        'project_name': project.name,
        'category': project.category,
        'affiliated_agency': [
            [{
                'name': a.name,
                'id': a.id,
            } for a in project.affiliated_agencies.all()]
        ],
        'description': project.description,
        'project_start_time': project.start_time,
        'project_completion_time': project.completion_time,
        'total_budget': project.total_budget,
        'completion_percentage': project.completion_percentage,
        'location_coordinates': [{
            'coord': [loc.longitude, loc.latitude],
            'id': loc.id,
        } for loc in project.location_set.all()],
        'id': project.id,
    }
