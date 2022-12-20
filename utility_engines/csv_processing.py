import csv
from observer.models import *
from django.conf import settings
from datetime import datetime

def read_user_type_file(user_type_file):

    # read user_type_file as csv
    user_type_list = []

    with open(user_type_file, 'r') as file:
        reader = csv.reader(file)
        first = True

        codes = set()

        for row in reader:
            if first:
                first = False
                pass
            else:
                data = {}
                data['code'] = row[0]
                data['committee'] = row[1]
                data['description'] = row[2]

                if data['code'] in codes:
                    raise Exception('Duplicate user type code: ' + data['code'])
                else:
                    codes.add(data['code'])

                user_type_list.append(data)


    return user_type_list


def read_agency_file(agency_file):
    # read agency_file as csv
    agency_list = []

    with open(agency_file, 'r') as file:
        reader = csv.reader(file)
        first = True

        codes = set()

        for row in reader:
            if first:
                first = False
                pass
            else:
                data = {}
                data['code'] = row[0]
                data['name'] = row[1]
                data['type'] = row[2]
                data['description'] = row[3]

                if data['code'] in codes:
                    raise Exception('Duplicate agency code: ' + data['code'])
                else:
                    codes.add(data['code'])

                print(data)

                agency_list.append(data)

    
    return agency_list


def read_projects_file(project_file):
    # fill rest like last function
    project_list = []
    locations = set()

    with open(project_file, 'r') as file:
        reader = csv.reader(file)
        first = True

        codes = set()

        for row in reader:
            if first:
                first = False
                pass
            else:
                data = {}
                data['name'] = row[0]
                data['location'] = row[1]
                data['latitude'] = float(row[2])
                data['longitude'] = float(row[3])
                data['exec'] = row[4]
                data['cost'] = float(row[5])
                data['timespan'] = int(row[6])
                data['project_id'] = row[7]
                data['goal'] = row[8]
                print(row)
                data['start_date'] = datetime.strptime(row[9], '%Y-%m-%d')
                data['completion'] = float(row[10])
                data['actual_cost'] = float(row[11])

                if data['project_id'] in codes:
                    raise Exception('Duplicate project code: ' + data['code'])
                elif not data['project_id'].startswith('proj'):
                    raise Exception('Invalid project code: ' + data['code'])
                else:
                    codes.add(data['project_id'])

                locations.add(data['location'])

                project_list.append(data)

    return project_list, locations


def fill_initial_data():
    if UserTypes.objects.count() == 0:
        user_types = read_user_type_file(settings.BASE_DIR / 'Dataset/user_types.csv')
        for user_type in user_types:
            u = UserTypes.objects.create(
                code=user_type['code'],
                committee=user_type['committee'],
                description=user_type['description']
            )
            u.save()

    if Agency.objects.count() == 0:
        agencies = read_agency_file(settings.BASE_DIR / 'Dataset/agencies.csv')
        for agency in agencies:
            a = Agency.objects.create(
                code=agency['code'],
                name=agency['name'],
                type=agency['type'],
                description=agency['description']
            )
            a.save()

    if Approved_Project.objects.count() == 0:
        projects, locations = read_projects_file(settings.BASE_DIR / 'Dataset/projects.csv')

        print(locations)