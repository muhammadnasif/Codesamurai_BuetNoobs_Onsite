from django.shortcuts import render, redirect
from django.urls import reverse
from djqscsv import render_to_csv_response, write_csv
from rest_framework.response import Response
from rest_framework.decorators import api_view

from utility_engines.timeframe_estimation import suggest_timeframe_forall
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

    if 'username' not in request.session:
        return redirect(reverse('login'))

    context = {
        "projects": projects,
        # "agency": None,  # Agency.objects.get(name=request.session.get('agency')),
        "user": request.session.get('username'),
        # "exec": exec,
    }
    print(request.session)

    return render(request, 'base/home.html', context)


def load_not_found(request):
    return render(request, 'base/404.html')

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





@api_view(['POST'])
def post_feedback(request):

    project_id = request.POST['project_id']
    feedback_msg = request.POST['feedback_msg']

    project = Project_Core.objects.get(id=project_id)

    feedback = Feedback.objects.create(project_core=project, feedback=feedback_msg)
    feedback.save()

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

    if 'username' not in request.session:
        return redirect(reverse('login'))

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
        return render(request, 'base/projects.html', {"context": revisedProposed, 'data': {
            'name': '',
            'area': '',
            'lat': '',
            'long': '',
            'cost': '',
            'goal': '',
            'timespan': '',
        }})
    else:
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
        print(name, lat, long, cost, goal, timespan)

        if Project_Core.objects.filter(name=name).exists():
            project = Project_Core.objects.get(name=name)
            project.locations.clear()
            project.locations.add(location[0].id)
            project.name = name
            project.latitude = lat
            project.longitude = long
            project.expected_cost = cost
            project.goal = goal
            project.timespan = timespan
            print('Saving Project Pre')
            project.save()
        else:
            project = Project_Core.objects.create(name=name, executing_agency=agency, latitude=lat, longitude=long,
                                                  expected_cost=cost,
                                                  goal=goal, timespan=timespan)
            project.save()
            print('Saving Project new')
            location = Location.objects.filter(name=request.POST['propose-form-area'])
            if len(location) == 0:
                new_location = Location.objects.create(name=request.POST['propose-form-area'])
                new_location.save()
            project.locations.add(location[0])
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
        'name': proposed_project.project.name,
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


def csv_file_creator(request):
    if 'is_approved' in request.session:
        projects = Approved_Project.objects.filter(project__name__icontains=request.session['query_param'])
    else:
        projects = Proposed_Project.objects.filter(project__name__icontains=request.session['query_param'])
    with open('foo.csv', 'wb') as csv_file:
        print("csv file open -- foo")
        write_csv(projects, csv_file)
        print("csv file write -- foo")

def export_data_search(request):
    print("export_data_search paisi")
    print(request.POST)
    if 'is_approved' in request.POST:

        request.session['is_approved'] = request.POST['is_approved']
        request.session['query_param'] = request.POST['search']

        approved_projects = Approved_Project.objects.filter(project__name__icontains=request.POST['search'])
        context = {
            'projects': approved_projects
        }
    else:
        request.session['query_param'] = request.POST['search']

        proposed_projects = Proposed_Project.objects.filter(project__name__icontains=request.POST['search'])

        estimator_dict = suggest_timeframe_forall(proposed_projects)
        x = []
        print(estimator_dict)
        for p in proposed_projects:
            print(estimator_dict[p.project.id])
            x = [
                {
                    'project': p.project,
                    'estimation': estimator_dict[p.project.id]
                },
            ]

        print(x)

        context = {
            'projects': proposed_projects
        }
        return render(request, 'export_data_proposed.html', context)
    print(context)
    return render(request, 'base/export_data.html', context)


def test_func(request):
    print("test_func")
    qs = Project_Core.objects.filter(is_approved=False)

    with open('foo.csv', 'wb') as csv_file:
        print("csv file open")
        write_csv(qs, csv_file)
        print("csv file write")
    # return render_to_csv_response(qs)
    return render(request, 'base/export_data.html')
