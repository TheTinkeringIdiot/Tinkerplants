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
            symbs = Symbiant.objects.filter(ql__gte=low_ql, ql__lte=high_ql, family__in=families)
        else:
            symbs = Symbiant.objects.filter(ql__gte=low_ql, ql__lte=high_ql, family__in=families, slot__in=slots)

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