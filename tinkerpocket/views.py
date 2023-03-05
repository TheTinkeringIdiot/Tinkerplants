from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, FileResponse, HttpResponseRedirect

from tinkerpocket.models import *
# from tinkerpocket.utils import *


import json

# Create your views here.
def index(request):
    if request.session.get('stats') is None:
        # request.session['stats'] = initial_weapons()
        print('Session setup')
    return render(request, 'tinkerpocket/index.html')

def boss_info(request):
    if request.method == 'POST':
        boss_data = json.loads(request.body)
        name = boss_data['name']

        boss = Pocketboss.objects.filter(name=name)
        if boss is None or len(boss) != 1:
            return JsonResponse({'success': False, 'message': 'If you want to know how it works, just ask'})

        boss = boss[0]

        info = {}
        info['name'] = boss.name
        info['level'] = boss.level
        info['mobs'] = boss.mobs
        info['playfield'] = boss.playfield
        info['location'] = boss.location
        info['drops'] = []

        # if name == 'The Night Heart':
        #     breakpoint()

        for drop in boss.drops.all():
            info['drops'].append([drop.aoid, drop.name, drop.ql])
        
        return JsonResponse({'success': True, 'data': info})
    
    else:
        return JsonResponse({'success': False, 'message': 'If you want to know how it works, just ask'})

def filter(request):
    if request.method == 'POST':
        data = json.loads(request.body)

        low_ql = int(data.get('low_ql', 0))
        high_ql = int(data.get('high_ql', 300))
        if high_ql < low_ql: 
            return JsonResponse({'success': False, 'message': 'If you want to know how it works, just ask'})

        if data.get('sloob'):
            expansions = 2
        else:
            expansions = 512

        families = []
        if data['artillery']: families.append('Artillery')
        if data['control']: families.append('Control')
        if data['extermination']: families.append('Extermination')
        if data['infantry']: families.append('Infantry')
        if data['support']: families.append('Support')

        if len(families) <= 0:
            return JsonResponse({'success': False, 'message': 'If you want to know how it works, just ask'})

        slots = []
        if data['eye']: slots.append('Eye')
        if data['head']: slots.append('Head')
        if data['ear']: slots.append('Ear')
        if data['right_arm']: slots.append('Right arm')
        if data['chest']: slots.append('Chest')
        if data['left_arm']: slots.append('Left arm')
        if data['right_wrist']: slots.append('Right wrist')
        if data['waist']: slots.append('Waist')
        if data['left_wrist']: slots.append('Left wrist')
        if data['right_hand']: slots.append('Right hand')
        if data['leg']: slots.append('Legs')
        if data['left_hand']: slots.append('Left hand')
        if data['feet']: slots.append('Feet')

        if len(slots) <= 0:
            symbs = Symbiant.objects.filter(ql__gte=low_ql, ql__lte=high_ql, family__in=families, reqs__Expansion_sets__lte=expansions)
        else:
            symbs = Symbiant.objects.filter(ql__gte=low_ql, ql__lte=high_ql, family__in=families, slot__in=slots, reqs__Expansion_sets__lte=expansions)

        retlist = []
        for symb in symbs:
            entry = []
            entry.append(symb.aoid)
            entry.append(symb.slot)
            entry.append(symb.name)
            entry.append(symb.ql)

            dropped_by = []
            for boss in symb.dropped_by.all():
                dropped_by.append(boss.name)

            entry.append(dropped_by)
            retlist.append(entry)

        return JsonResponse({'success': True, 'data': retlist})

    else:
        return JsonResponse({'success': False, 'message': 'If you want to know how it works, just ask'})

def match(request):
    if request.method == 'POST':
        data = json.loads(request.body)

        level = int(data.get('Level', 1))
        profession = int(data.get('Profession', 0))
        slot = data.get('Slot')
        if data.get('Sloob'):
            expansions = 2
        else:
            expansions = 512

        stats = {
            'Strength' : int(data.get('Strength', 1)),
            'Stamina' : int(data.get('Stamina', 1)),
            'Sense' : int(data.get('Sense', 1)),
            'Agility' : int(data.get('Agility', 1)),
            'Intelligence' : int(data.get('Intelligence', 1)),
            'Psychic' : int(data.get('Psychic', 1)),
            'Treatment' : int(data.get('Treatment', 1)),
        }

        if profession == 0:
            return JsonResponse({'success': False, 'message': 'If you want to know how it works, just ask'})

        candidates = Symbiant.objects.filter(reqs__Level__lte=level, reqs__Profession__contains=profession, reqs__Expansion_sets__lte=expansions, slot=slot)

        breakpoint()

        retlist = []

        qual_symbs = {}

        for candidate in candidates:
            if check_requirements(candidate, stats):
                entry = [
                    candidate.aoid,
                    candidate.name,
                    candidate.slot,
                    candidate.ql,
                ]

                dropped_by = []
                for boss in candidate.dropped_by.all():
                    dropped_by.append(boss.name)

                entry.append(dropped_by)
                
                if qual_symbs.get(candidate.slot) is None:
                    qual_symbs[candidate.slot] = []

                qual_symbs[candidate.slot].append(entry)

        top_x = 6

        for key, vals in qual_symbs.items():
            sorted_list = sorted(qual_symbs[key], key=lambda x:x[3], reverse=True)

            if len(sorted_list) > top_x:
                retlist.extend(sorted_list[:top_x])
            else:
                retlist.extend(sorted_list)

        return JsonResponse({'success': True, 'data': retlist})

    else:
        return JsonResponse({'success': False, 'message': 'If you want to know how it works, just ask'})
    
def compare(request):
    if request.method == 'POST':
        data = json.loads(request.body)

        retlist = {}
        symbs = []

        retlist['names'] = []
        retlist['benefits'] = {}

        for key, val in data.items():
            if val is not None and len(val) > 0:
                symb = Symbiant.objects.get(name=val)

                if symb is not None:
                    symbs.append(symb)
                    retlist['names'].append(val)

        retlist['benefits'] = build_compare(symbs)

        breakpoint()

        return JsonResponse({'success': True, 'data': retlist})
    
    else:
        return JsonResponse({'success': False, 'message': 'If you want to know how it works, just ask'})
    
def build_compare(symbs):
    benefit_list = []

    for symb in symbs:
        benefit_list += symb.effects.keys()

    benefit_list = list(set(benefit_list)) # strip out duplicates
    benefit_list = sorted(benefit_list)
    benefits = {}

    for benefit in benefit_list:
        if benefits.get(benefit) is None:
            benefits[benefit] = []

        for symb in symbs:
            benefit_value = symb.effects.get(benefit)
            if benefit_value is None:
                benefits[benefit].append(0)
            else:
                benefits[benefit].append(benefit_value)

    return benefits

def check_requirements(symb, stats):
    for key, val in symb.reqs.items():

        if key in ['Profession', 'Level', 'Expansion_sets']:
            continue

        elif key == 'Level':
            continue

        else:
            try:
                if not stats.get(key) >= val:
                    return False
            except Exception as e:
                print('TINKERPOCKET: MISSING KEY: {} on {}'.format(key, symb.name))
                print(e)

    return True
