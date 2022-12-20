from observer.models import *
from datetime import datetime, timedelta
import math

def suggest_timeframe(project):
    components = Component.objects.filter(project__is_approved=True, completion__lt=100)

    components = [convert_approved_component(c) for c in components]
    components.sort(key=lambda c: c['start_date'])

    project_components = [convert_proposed_component(c) for c in project.project.component_set.all()]

    list_components = components + project_components
    all_components = {c['id']: c for c in list_components}

    required = len(project_components)
    done = 0

    if check_cycle(all_components):
        return None
    
    agencies = Agency.objects.all()
    agencies = {
        a.id:{
            'id': a.id,
            'budget_used': a.budget_used if a.last_usage_updated.year == datetime.now().year else 0,
            'usage' : a.usage if a.last_usage_updated.year == datetime.now().year else 0,
            'max_limit': a.agency_constraint_set.all()[0].max_limit if a.agency_constraint_set.count() > 0 else 1000000,
            'max_funding': a.yearly_funding_constraint_set.all()[0].max_funding if a.yearly_funding_constraint_set.count() > 0 else 10000000000000000000000,
        }
        for a in agencies
    }
    
    locations = Location.objects.all()
    locations = {
        l.id: {
            'id': l.id,
            'usage': l.usage if l.last_usage_updated.year == datetime.now().year else 0,
            'max_limit': l.location_constraint_set.all()[0].max_limit if l.location_constraint_set.count() > 0 else 1000000,
        } for l in locations
    }

    timeframe = [None, None]
    tim = datetime.now()

    while True:
        for c in list_components:
            if c['remaining'] <= 0:
                continue
            if c['dependancy'] is not None and all_components[c['dependancy']]['remaining'] > 0:
                # print("COULD NOT WORK ", c['id'], " BECAUSE OF DEPENDENCY ON ", c['dependancy'])
                continue
            todo = min(c['remaining'], (datetime(tim.year+1, 1, 1) - tim).days/365.25)
            if c['dependancy'] is not None and all_components[c['dependancy']].get('done', 0) > 0:
                todo -= all_components[c['dependancy']].get('done', 0)
            
            if agencies[c['agency']]['usage'] + 1 > agencies[c['agency']]['max_limit']:
                # print('COULD NOT WORK ', c['id'], ' BECAUSE OF AGENCY LIMIT')
                continue
            if agencies[c['agency']]['budget_used'] + c['budget'] * todo / c['timespan'] > agencies[c['agency']]['max_funding']:
                # print('COULD NOT WORK ', c['id'], ' BECAUSE OF AGENCY BUDGET')
                continue
            if any(locations[l]['usage'] + 1 > locations[l]['max_limit'] for l in c['locations']):
                # print('COULD NOT WORK ', c['id'], ' BECAUSE OF LOCATION LIMIT')
                continue
            c['remaining'] -= todo

            c['done'] = todo + (all_components[c['dependancy']].get('done', 0) if c['dependancy'] is not None else 0)

            if c['project'] == project.project.id:
                if timeframe[0] is None:
                    timeframe[0] = tim
            # print('working ', c['id'], ' for ', todo, ' years')
            agencies[c['agency']]['usage'] += 1
            agencies[c['agency']]['budget_used'] += c['budget'] * todo / c['timespan']
            for l in c['locations']:
                locations[l]['usage'] += 1
            if c['remaining'] <= 0 and c['project'] == project.project.id:
                # print(c['id'], ' done ', c['project'], ' ', project.id)
                done += 1

                if done == required:
                    # increment tim by todo years
                    timeframe[1] = tim + timedelta(days=365.25 * c['done'])
                    break
        
        for c in list_components:
            c['done'] = 0
    
        tim = datetime(tim.year+1, 1, 1)
        if done == required:
            break

        for a in agencies:
            agencies[a]['usage'] = 0
            agencies[a]['budget_used'] = 0
        
        for l in locations:
            locations[l]['usage'] = 0


    return timeframe

def convert_approved_component(c):
    return {
        'project' : c.project.id,
        'start_date' : c.project.approved_project_set.all()[0].start_date,
        'agency' : c.executing_agency.id,
        'id': c.id,
        'dependancy': c.dependancy.id if c.dependancy else None,
        'budget': c.budget_ratio * (c.project.expected_cost - c.project.approved_project_set.all()[0].actual_cost),
        'remaining': c.project.timespan * (100 - c.completion)/100,
        'locations': [l.id for l in c.project.locations.all()],
        'timespan': c.project.timespan,

    }

def convert_proposed_component(c):
    return {
        'project' : c.project.id,
        'agency' : c.executing_agency.id,
        'id': c.id,
        'dependancy': c.dependancy.id if c.dependancy else None,
        'budget': c.budget_ratio * (c.project.expected_cost),
        'remaining': c.project.timespan,
        'locations': [l.id for l in c.project.locations.all()],
        'timespan': c.project.timespan,
    }


def check_cycle(all_components):
    seen = {}
    cycle = False
    for c in all_components.values():
        cur = c
        
        while cur is not None:
            if seen.get(cur['id'], -1) == c['id']:
                cycle = True
                break
            if seen.get(cur['id'], -1) != -1:
                break
            seen[cur['id']] = c['id']
            cur = all_components.get(cur['dependancy'])
        if cycle:
            break

    if cycle:
        return True
    else:
        return False


def compute_expected_ends():
    components = Component.objects.filter(project__is_approved=True, completion__lt=100)

    components = [convert_approved_component(c) for c in components]
    components.sort(key=lambda c: c['start_date'])

    all_components = {c['id']: c for c in components}
    projects = {}

    for c in components:
        projects[c['project']] = projects.get(c['project'], 0) + 1

    if check_cycle(all_components):
        return None
    
    agencies = Agency.objects.all()
    agencies = {
        a.id:{
            'id': a.id,
            'budget_used': a.budget_used if a.last_usage_updated.year == datetime.now().year else 0,
            'usage' : a.usage if a.last_usage_updated.year == datetime.now().year else 0,
            'max_limit': a.agency_constraint_set.all()[0].max_limit if a.agency_constraint_set.count() > 0 else 1000000,
            'max_funding': a.yearly_funding_constraint_set.all()[0].max_funding if a.yearly_funding_constraint_set.count() > 0 else 10000000000000000000000,
        }
        for a in agencies
    }
    
    locations = Location.objects.all()
    locations = {
        l.id: {
            'id': l.id,
            'usage': l.usage if l.last_usage_updated.year == datetime.now().year else 0,
            'max_limit': l.location_constraint_set.all()[0].max_limit if l.location_constraint_set.count() > 0 else 1000000,
        } for l in locations
    }

    tim = datetime.now()
    ends = {}
    done = 0

    while True:
        for c in components:
            if c['remaining'] <= 0:
                continue
            if c['dependancy'] is not None and all_components[c['dependancy']]['remaining'] > 0:
                # print("COULD NOT WORK ", c['id'], " BECAUSE OF DEPENDENCY ON ", c['dependancy'])
                continue
            todo = min(c['remaining'], (datetime(tim.year+1, 1, 1) - tim).days/365.25)
            if c['dependancy'] is not None and all_components[c['dependancy']].get('done', 0) > 0:
                todo -= all_components[c['dependancy']].get('done', 0)
            
            if agencies[c['agency']]['usage'] + 1 > agencies[c['agency']]['max_limit']:
                # print('COULD NOT WORK ', c['id'], ' BECAUSE OF AGENCY LIMIT')
                continue
            if agencies[c['agency']]['budget_used'] + c['budget'] * todo / c['timespan'] > agencies[c['agency']]['max_funding']:
                # print('COULD NOT WORK ', c['id'], ' BECAUSE OF AGENCY BUDGET')
                continue
            if any(locations[l]['usage'] + 1 > locations[l]['max_limit'] for l in c['locations']):
                # print('COULD NOT WORK ', c['id'], ' BECAUSE OF LOCATION LIMIT')
                continue
            c['remaining'] -= todo

            c['done'] = todo + (all_components[c['dependancy']].get('done', 0) if c['dependancy'] is not None else 0)

            # print('working ', c['id'], ' for ', todo, ' years')
            agencies[c['agency']]['usage'] += 1
            agencies[c['agency']]['budget_used'] += c['budget'] * todo / c['timespan']
            for l in c['locations']:
                locations[l]['usage'] += 1
            if c['remaining'] <= 0:
                done+=1
                # print(c['id'], ' done ', c['project'], ' ', project.id)
                projects[c['project']] -=1

                if projects[c['project']] == 0:
                    ends[c['project']] = tim + timedelta(days=365.25 * c['done'])

            
        
        for c in components:
            c['done'] = 0
    
        tim = datetime(tim.year+1, 1, 1)
        if done == len(components):
            break

        for a in agencies:
            agencies[a]['usage'] = 0
            agencies[a]['budget_used'] = 0
        
        for l in locations:
            locations[l]['usage'] = 0


    return ends