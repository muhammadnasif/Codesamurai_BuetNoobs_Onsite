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
    print(request.session)

    return render(request, 'base/home.html', context)


@api_view(['GET'])
def projects(request):
    fill_initial_data()

    project_list = [
        approved_project_convert(p) for p in Project_Core.objects.filter(is_approved=True)
    ]
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
def post_feedback(request):
    # id = request.POST['coord']
    # location = Location.objects.get(id=id)

    # # print(request.POST['coord'])
    # # latlong = request.POST['coord'].split(',')
    # # location = Location.objects.get(longitude=latlong[0], latitude=latlong[1])
    # # print(location)
    # issue = Issue.objects.create(location=location, description=request.POST['issue_msg'])
    # issue.save()

    project_id = request.POST['project_id']
    feedback_msg = request.POST['feedback_msg']

    project = Project_Core.objects.get(id=project_id)

    feedback = Feedback.objects.create(project_core=project, feedback=feedback_msg)
    feedback.save()

    # feedback saved

    return Response({'result': 'ok'})


def project_convert(project):
    return {
        'project_id': project.id,
        'project_name': project.name,
        'project_code': project.project_code,
        'lat': project.latitude,
        'lng': project.longitude,
        'expected_cost': project.expected_cost,
        'timespan': project.timespan,
        'goal': project.goal,
        'agency': project.executing_agency.name,

    }

@api_view(['GET'])
def all_projects(request):
    fill_initial_data()
    project_list = [
        approved_project_convert(p) for p in Approved_Project.objects.all()
    ]
    return Response(project_list)

def approved_project_convert(approved_project):
    return {
        'project_id': approved_project.project.id,
        'project_name': approved_project.project.name,
        'project_code': approved_project.project.project_code,
        'lat': approved_project.project.latitude,
        'lng': approved_project.project.longitude,
        'expected_cost': approved_project.project.expected_cost,
        'timespan': approved_project.project.timespan,
        'goal': approved_project.project.goal,
        'agency': approved_project.project.executing_agency.name,
        'start_time': approved_project.start_date,
        'completion': approved_project.completion,
        'actual_cost': approved_project.actual_cost,
    }


def project_proposal(request):
    agency = request.session.get('agency')
    print(agency)
    allProposed = Proposed_Project.objects.all()
    revisedProposed = []
    for p in allProposed:
        if p.project.executing_agency.name == agency:
            newP = {
                'core_id':p.project.id,
                'name': p.project.name,
                'location':[l.name for l in p.project.locations.all()],
                'cost':p.project.expected_cost,
                'timespan':p.project.timespan,
                'goal': p.project.goal,
                'proposed_date':p.proposed_date
            }
            revisedProposed.append(newP)
    return render(request, 'base/projects.html', {"context": revisedProposed})
