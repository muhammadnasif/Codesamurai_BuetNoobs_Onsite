from django.shortcuts import render, redirect
from django.urls import reverse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import *
from .csv_tool import read_data
from .models import *
from utility_engines.timeframe_estimation import suggest_timeframe
from utility_engines.views import update_ends

def review_project_proposal(request):
    allProposed = Proposed_Project.objects.all()
    revisedProposed = []
    for p in allProposed:
            newP = {
                'core_id': p.project.id,
                'name': p.project.name,
                'location': [l.name for l in p.project.locations.all()],
                'cost': p.project.expected_cost,
                'timespan': p.project.timespan,
                'goal': p.project.goal,
                'proposed_date': p.proposed_date
            }
            revisedProposed.append(newP)
    return render(request, 'components/review_proposal.html', {"context": revisedProposed})


def approve_proposal(request, pk):
    proposed_project = Proposed_Project.objects.get(id=pk)
    estimate_time = suggest_timeframe(proposed_project)
    project = proposed_project.project
    project.is_approved = True
    approveProject = Approved_Project.objects.create(project=project, start_date=estimate_time[0], actual_cost=project.expected_cost, expected_end=estimate_time[1])
    approveProject.save()
    return redirect(reverse('observer:review-project-proposal'))
def detail_project_proposal(request, pk):
    proposed_project = Proposed_Project.objects.get(project__id=pk)
    estimate_time = suggest_timeframe(proposed_project)
    print(estimate_time)
    start, end = -1, -1
    if estimate_time:
        start = estimate_time[0]
        end = estimate_time[1]
    proposed_project = {
        'id':proposed_project.id,
        'name': proposed_project.project.name,
        'area': proposed_project.project.locations.all()[0].name,
        'lat': proposed_project.project.latitude,
        'long': proposed_project.project.longitude,
        'cost': proposed_project.project.expected_cost,
        'goal': proposed_project.project.goal,
        'timespan': proposed_project.project.timespan,
        'proposed_date': proposed_project.proposed_date,
        'estimate_start': start,
        'estimated_end': end

    }
    return render(request, 'components/single_proposal.html', {"data": proposed_project})

def detail_running_project(request, pk):
    proposed_project = Approved_Project.objects.get(id=pk)
    estimate_time = suggest_timeframe(proposed_project)
    print(estimate_time)
    start, end = -1, -1
    if estimate_time:
        start = estimate_time[0]
        end = estimate_time[1]
    proposed_project = {
        'id':proposed_project.id,
        'name': proposed_project.project.name,
        'area': proposed_project.project.locations.all()[0].name,
        'lat': proposed_project.project.latitude,
        'long': proposed_project.project.longitude,
        'cost': proposed_project.project.expected_cost,
        'goal': proposed_project.project.goal,
        'timespan': proposed_project.project.timespan,
        'proposed_date': proposed_project.proposed_date,
        'estimate_start': start,
        'estimated_end': end

    }
    return render(request, 'components/single_proposal.html', {"data": proposed_project})

def running_project(request):
    update_ends()
    allApproved = Approved_Project.objects.all()
    revisedApproved = []
    for p in allApproved:
            newP = {
                'id': p.id,
                'core_id': p.project.id,
                'name': p.project.name,
                'location': [l.name for l in p.project.locations.all()],
                'cost': p.project.expected_cost,
                'timespan': p.project.timespan,
                'goal': p.project.goal,
                'start_date': p.start_date,
                'actual_cost': p.actual_cost,
                'expected_end': p.expected_end
            }
            revisedApproved.append(newP)
    return render(request, 'components/running_project.html', {"context": revisedApproved})
