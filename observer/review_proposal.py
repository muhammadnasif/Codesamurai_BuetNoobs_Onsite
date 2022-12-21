from django.shortcuts import render, redirect
from django.urls import reverse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import *
from .csv_tool import read_data
from .models import *


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

def running_project(request):
    allApproved= Approved_Project.objects.all()
    revisedApproved = []
    for p in allApproved:
            newP = {
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
