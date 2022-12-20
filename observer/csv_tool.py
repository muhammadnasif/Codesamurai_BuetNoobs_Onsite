import csv
from django.conf import settings
from datetime import datetime
from .models import *

def fill_db(project_list):
    agencies = []
    for project in project_list:
        agencies += project['affiliated_agency']
    agencies = set(agencies)

    for agency in agencies:
        a = Agency.objects.create(name=agency)
        # print(a)
        a.save()

    for project in project_list:
        p = Project.objects.create(
            name=project['project_name'],
            category=project['category'],
            description=project['description'],
            start_time=project['project_start_time'],
            completion_time=project['project_completion_time'],
            total_budget=project['total_budget'],
            completion_percentage=project['completion_percentage'],
        )

        p.affiliated_agencies.add(*[Agency.objects.get(name=agency) for agency in project['affiliated_agency']])
        p.save()
    
    for project in project_list:
        for coord in project['location_coordinates']:
            l = Location.objects.create(
                longitude=coord[0],
                latitude=coord[1],
                project=Project.objects.get(name=project['project_name'])
            )
            l.save()


def read_data():
    project_list = []
    with open(settings.BASE_DIR / 'projects.csv', 'r') as file:
        reader = csv.reader(file)
        row_count = 0
        for row in reader:
            if row_count == 0:
                attributes = row
            else:
                data = {}
                for i in range(len(attributes)):
                    data[attributes[i]] = row[i]
                data['id'] = row_count

                locs = data['location_coordinates']
                data['location_coordinates'] = []

                while locs:
                    l = locs.find('(')
                    if l == -1:
                        break
                    r = locs.find(')')
                    coord = [float(x) for x in locs[l+1:r].split(', ')]
                    data['location_coordinates'].append(coord)
                    locs = locs[r+1:]

                data['project_start_time'] = datetime.strptime(data['project_start_time'], '%Y-%m-%d')
                data['project_completion_time'] = datetime.strptime(data['project_completion_time'], '%Y-%m-%d')
                data['completion_percentage'] = float(data['completion_percentage'][:-1])
                data['affiliated_agency'] = data['affiliated_agency'].split(', ')
                data['total_budget'] = int(data['total_budget'][4:-1])*1000000

                project_list.append(data)
            row_count += 1

    if Project.objects.all().count() == 0:
        fill_db(project_list)

    return project_list
