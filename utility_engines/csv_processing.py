import csv
from observer.models import *
from django.conf import settings

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

                print(data)


    return user_type_list

def fill_initial_data():
    if UserTypes.objects.count() != 0:
        return

    user_types = read_user_type_file(settings.BASE_DIR / 'Dataset/user_types.csv')
    for user_type in user_types:
        u = UserTypes.objects.create(
            code=user_type['code'],
            committee=user_type['committee'],
            description=user_type['description']
        )
        u.save()