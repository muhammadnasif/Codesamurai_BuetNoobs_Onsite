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
    if 'agency' in request.session and Agency.objects.get(name=request.session.get('agency')) == 'EXEC':
        exec = True
    else:
        exec = False

    context = {
        "projects": projects,
        "agency": None, #Agency.objects.get(name=request.session.get('agency')),
        "user": request.session.get('username'),
        "exec": exec,
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

    return Response({'status': '1'})


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
                'core_id': p.project.id,
                'name': p.project.name,
                'location': [l.name for l in p.project.locations.all()],
                'cost': p.project.expected_cost,
                'timespan': p.project.timespan,
                'goal': p.project.goal,
                'proposed_date': p.proposed_date
            }
            revisedProposed.append(newP)
    if request.method == 'GET':
        return render(request, 'base/projects.html', {"context": revisedProposed, 'data' : {
            'name' : '',
            'area': '',
            'lat': '',
            'long': '',
            'cost': '',
            'goal': '',
            'timespan': '',
        }})
    else:
        print("adasdasddas")
        print(request.POST)

        location = Location.objects.filter(name=request.POST['propose-form-area'])
        if len(location) == 0:
            new_location = Location.objects.create(name=request.POST['propose-form-area'])
            new_location.save()

        agency = Agency.objects.get(name=request.session.get('agency'))
        name = request.POST['propose-form-name']
        lat = request.POST['propose-form-lat']
        long = request.POST['propose-form-long']
        cost = request.POST['propose-form-cost']
        goal = request.POST['propose-form-goal']
        timespan = request.POST['propose-form-timespan']
        # print(name, lat, long, cost, goal, timespan)

        if Project_Core.objects.filter(name=name).exists():
            project = Project_Core.objects.get(name=name)
            project.locations.clear()
            project.locations.add(location[0].id)
            project.name = name
            project.lat = lat
            project.long = long
            project.cost = cost
            project.goal = goal
            project.timespan = timespan

            project.save()
        else:
            project = Project_Core.objects.create(name=name, executing_agency=agency, latitude=lat, longitude=long, expected_cost=cost,
                               goal=goal, timespan=timespan)
            project.save()
            project.locations.add(location)
            pp = Proposed_Project.objects.create(project=project)
            pp.save()
        return redirect(reverse('observer:project-proposal'))


def update_proposal(request):
    revisedProposed = getRevisedProposed(request.session.get('agency'))
    print(request.POST['core_id'])
    project = Project_Core.objects.get(id=request.POST['core_id'])
    update = {
        'name': project.name,
        'area': project.locations.name,
        'lat': project.latitude,
        'long': project.longitude,
        'cost': project.expected_cost,
        'goal': project.goal,
        'timespan': project.timespan
    }
    print(update)
    return render(request, 'base/projects.html', {"context": revisedProposed, "update": update})


def proposal_update_form(request, pk):
    revisedProposed = getRevisedProposed(request.session.get('agency'))
    proposed_project = Proposed_Project.objects.get(project__id=pk)
    proposed_project = {
        'name' : proposed_project.project.name,
        'area': proposed_project.project.locations.all()[0].name,
        'lat': proposed_project.project.latitude,
        'long': proposed_project.project.longitude,
        'cost': proposed_project.project.expected_cost,
        'goal': proposed_project.project.goal,
        'timespan': proposed_project.project.timespan
    }
    if request.method == 'GET':
        return render(request, 'base/projects.html', {"data": proposed_project, "context": revisedProposed})


def getRevisedProposed(agency):
    allProposed = Proposed_Project.objects.all()
    revisedProposed = []
    for p in allProposed:
        if p.project.executing_agency.name == agency:
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
    return revisedProposed


@api_view(['POST'])
def add_rating(request):
    if request.POST:
        print(request.POST)
        if 'rating' in request.POST:
            rating = Rating.objects.create(rating=request.POST['rating'],
                                           project_core=Project_Core.objects.get(id=request.POST['project_id']))
            rating.save()

            return Response({'status': '1'})

    return Response({'msg': 'no data saved'})


def update_project_proposal(request, pk):
    pass

    proposed_project = Proposed_Project.objects.get(id=pk)
    project = proposed_project.project
    if request.method == 'GET':
        return render(request, 'base/update_project_proposal.html', {'proposed_project': proposed_project})


    return


def export_data(request):

    return render(request, 'base/export_data.html')


def export_data_search(request):
    if request.method == 'POST':
        print(request.POST)
        if 'export' in request.POST:
            print("exporting")
            return Response({'status': '1'})
        else:
            print("searching")
            return Response({'status': '1'})

    return render(request, 'base/export_data.html')