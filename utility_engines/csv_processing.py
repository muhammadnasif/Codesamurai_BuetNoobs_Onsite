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

                # print(data)

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
                data['location'] = row[1].split(',')
                data['latitude'] = float(row[2])
                data['longitude'] = float(row[3])
                data['exec'] = row[4]
                data['cost'] = float(row[5])
                data['timespan'] = int(row[6])
                data['project_id'] = row[7]
                data['goal'] = row[8]
                data['start_date'] = datetime.strptime(row[9], '%Y-%m-%d')
                data['completion'] = float(row[10])
                data['actual_cost'] = float(row[11])

                if data['project_id'] in codes:
                    raise Exception('Duplicate project code: ' + data['code'])
                elif not data['project_id'].startswith('proj'):
                    raise Exception('Invalid project code: ' + data['code'])
                else:
                    codes.add(data['project_id'])

                for l in data['location']:
                    locations.add(l)

                project_list.append(data)

    return project_list, locations


# create read_proposals_file like read_projects_file
def read_proposals_file(proposals_file):
    # fill rest like last function
    project_list = []
    locations = set()

    with open(proposals_file, 'r') as file:
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
                data['location'] = row[1].split(',')
                data['latitude'] = float(row[2])
                data['longitude'] = float(row[3])
                data['exec'] = row[4]
                data['cost'] = float(row[5])
                data['timespan'] = int(row[6])
                data['project_id'] = row[7]
                data['goal'] = row[8]
                data['proposal_date'] = datetime.strptime(row[9], '%Y-%m-%d')

                if data['project_id'] in codes:
                    raise Exception('Duplicate project code: ' + data['code'])
                elif not data['project_id'].startswith('prop'):
                    raise Exception('Invalid project code: ' + data['code'])
                else:
                    codes.add(data['project_id'])

                for l in data['location']:
                    locations.add(l)

                project_list.append(data)

    return project_list, locations


def read_component_file(component_file):
    component_list = []

    with open(component_file, 'r') as file:
        reader = csv.reader(file)
        first = True

        codes = set()

        for row in reader:
            if first:
                first = False
                pass
            else:
                data = {}
                data['project_id'] = row[0]
                data['executing_agency'] = row[1]
                data['component_id'] = row[2]
                data['component_type'] = row[3]
                data['depends_on'] = row[4]
                data['budget_ratio'] = float(row[5])


                if data['component_id'] in codes:
                    raise Exception('Duplicate component code: ' + data['component_id'])
                elif not data['component_id'].startswith('comp'):
                    raise Exception('Invalid component code: ' + data['component_id'])
                else:
                    codes.add(data['component_id'])

                component_list.append(data)

    return component_list


def read_constraint_file(constraint_file):
    # fill like last function
    constraint_list = []

    with open(constraint_file, 'r') as file:
        reader = csv.reader(file)

        first = True

        for row in reader:
            if first:
                first = False
                pass
            else:
                data = {}
                data['code'] = row[0]
                data['max_limit'] = int(row[1])
                data['constraint_type'] = row[2]

                constraint_list.append(data)

    return constraint_list



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

        print("FILLING USER TYPES")

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

        print("FILLING AGENCIES")

    if Approved_Project.objects.count() == 0:
        projects, locations = read_projects_file(settings.BASE_DIR / 'Dataset/projects.csv')
        project_mapping = {}

        for location in locations:
            if not Location.objects.filter(name=location).exists():
                l = Location.objects.create(name=location)
                l.save()
        

        for project in projects:
            # create project core
            project_mapping[project['project_id']] = project
            core = Project_Core.objects.create(
                name=project['name'],
                project_code = project['project_id'],
                executing_agency = Agency.objects.get(code=project['exec']),
                latitude=project['latitude'],
                longitude=project['longitude'],
                expected_cost = int(project['cost'] * 10000000),
                timespan = project['timespan'],
                goal = project['goal'],
                is_approved = True
            )

            for l in project['location']:
                core.locations.add(Location.objects.get(name=l))

            core.save()

            p = Approved_Project.objects.create(
                project=core,
                start_date=project['start_date'],
                actual_cost=int(project['actual_cost'])
            )

            p.save()

        print("FILLING PROJECTS")

    if Proposed_Project.objects.count() == 0:
        projects, locations = read_proposals_file(settings.BASE_DIR / 'Dataset/proposals.csv')

        for location in locations:
            if not Location.objects.filter(name=location).exists():
                l = Location.objects.create(name=location)
                l.save()

        for project in projects:
            # create project core
            core = Project_Core.objects.create(
                name=project['name'],
                project_code = project['project_id'],
                executing_agency = Agency.objects.get(code=project['exec']),
                latitude=project['latitude'],
                longitude=project['longitude'],
                expected_cost = int(project['cost'] * 10000000),
                timespan = project['timespan'],
                goal = project['goal'],
                is_approved = False
            )

            for l in project['location']:
                core.locations.add(Location.objects.get(name=l))

            core.save()

            p = Proposed_Project.objects.create(
                project=core,
                proposed_date=project['proposal_date']
            )

            p.save()

        print("FILLING PROPOSALS")

    if Component.objects.all().count() == 0:
        assert project_mapping is not None
        components = read_component_file(settings.BASE_DIR / 'Dataset/components.csv')
        for component in components:
            p = Project_Core.objects.get(project_code=component['project_id'])
            c = Component.objects.create(
                project = p,
                executing_agency=Agency.objects.get(code=component['executing_agency']),
                component_id=component['component_id'],
                type=component['component_type'],
                dependancy=None,
                budget_ratio=component['budget_ratio'],
                completion = (project_mapping[p.project_code]['completion'] if p.is_approved else 0)
            )
            c.save()

        for component in components:
            c = Component.objects.get(component_id=component['component_id'])
            if component['depends_on'] != '':
                c.dependancy = Component.objects.get(component_id=component['depends_on'])
                c.save()

        print("FILLING COMPONENTS")


    if Location_Constraint.objects.all().count() == 0 or Agency_Constraint.objects.all().count() == 0 or Yearly_Funding_Constraint.objects.all().count() == 0:
        constraints = read_constraint_file(settings.BASE_DIR / 'Dataset/constraints.csv')
        for constraint in constraints:
            if constraint['constraint_type'] == 'location_limit':
                c = Location_Constraint.objects.create(
                    location=Location.objects.get(name=constraint['code']),
                    max_limit=constraint['max_limit']
                )
                c.save()
            elif constraint['constraint_type'] == 'executing_agency_limit':
                c = Agency_Constraint.objects.create(
                    agency=Agency.objects.get(code=constraint['code']),
                    max_limit=constraint['max_limit']
                )
                c.save()
            elif constraint['constraint_type'] == 'yearly_funding':
                c = Yearly_Funding_Constraint.objects.create(
                    agency=Agency.objects.get(code=constraint['code']),
                    max_funding=constraint['max_limit'] * 10000000
                )
                c.save()
            else:
                raise Exception('Invalid constraint type: ' + constraint['type'])

        print("FILLING CONSTRAINTS")

    



def create_csv(query_obj):
    pass