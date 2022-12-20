from django.shortcuts import render, redirect
from django.urls import reverse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import *
from .csv_tool import read_data
from .models import *
from utility_engines.csv_processing import fill_initial_data


# Create your views here.


# def load(request):
#     if 'username' in request.session:
#
#         # Displaying distinct categories
#         projects = Project.objects.values('category').distinct()
#
#         context = {
#             "projects": projects,
#         }
#
#         return render(request, 'base/base.html', context)
#     else:
#         return redirect(reverse('login'))

def load(request):
    # Displaying distinct categories
    # projects = Project.objects.values('category').distinct()

    projects = []

    context = {
        "projects": projects,
    }

    return render(request, 'base/base.html', context)


@api_view(['GET'])
def projects(request):
    fill_initial_data()
    project_list = read_data()
    return Response(project_list)


@api_view(['GET'])
def filter_projects(request):
    categories = request.GET.getlist('category')
    project_list = [
        # project_convert(p) for p in Project.objects.filter(category__in=categories)
    ]
    return Response(project_list)


def project(request):
    if request.method == "POST":
        print(request.POST)
    return render(request, 'components/project.html')


@api_view(['POST'])
def post_issue(request):
    # id = request.POST['coord']
    # location = Location.objects.get(id=id)

    # # print(request.POST['coord'])
    # # latlong = request.POST['coord'].split(',')
    # # location = Location.objects.get(longitude=latlong[0], latitude=latlong[1])
    # # print(location)
    # issue = Issue.objects.create(location=location, description=request.POST['issue_msg'])
    # issue.save()
    return Response({'result': 'ok'})

