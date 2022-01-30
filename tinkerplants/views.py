from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

from tinkerplants.models import *
from tinkerplants.utils import *
from aobase.settings import *

import json

def index(request):
    if request.session.get('implants') is None:
        request.session['implants'] = initial_implants()
        print('Session setup')
    return render(request, 'tinkerplants/index.html')

def update_display(request):
    return JsonResponse({'success': True, 'implants' : request.session.get('implants')})

def update_implants(request):
    if request.method == 'POST':
        try:
            if request.session.get('implants') is None:
                return JsonResponse({'success': False, 'message': 'Session timed out', 'next': ''})

            data = json.loads(request.body)
            slot = data.get('slot')
            idx = slot.rfind('-')

            imp_slot = slot[:idx]
            if not imp_slot in IMP_SLOTS:
                return JsonResponse({'success': False, 'message': 'Not a valid implant'})

            cluster_slot = slot[idx:].strip('-')
            if not cluster_slot in CLUSTER_SLOTS.keys():
                return JsonResponse({'success': False, 'message': 'Not a valid cluster position'})

            skill = data.get('value')
            if not skill in ALL_SKILLS:
                return JsonResponse({'success': False, 'message': 'Not a valid skill'})

            request.session['implants'][imp_slot][cluster_slot] = skill

            if not calc_implants(request, imp_slot):
                return JsonResponse({'success': False, 'message': 'Unable to update implant'})

            return JsonResponse({'success': True, 'implants' : request.session.get('implants')})
        except Exception as e:
            if DEBUG:
                import traceback
                traceback.print_exc()

            return JsonResponse({'success': False, 'message': 'If you want to know how it works, just ask'})

    else:
        if DEBUG:
            import traceback
            traceback.print_exc()
        return JsonResponse({'success': False, 'message': 'Quit tinkering, that''s my job'})

def update_ql(request):
    if request.method == 'POST':
        try:
            if request.session.get('implants') is None:
                return JsonResponse({'success': False, 'message': 'Session timed out', 'next': ''})

            data = json.loads(request.body)
            slot = data.get('slot')
            idx = slot.rfind('-')

            imp_slot = slot[:idx]
            if not imp_slot in IMP_SLOTS:
                return JsonResponse({'success': False, 'message': 'Not a valid implant'})

            try:
                ql = int(data.get('value'))
            except:
                return JsonResponse({'success': False, 'message': 'Not a valid QL'})

            if ql < 1 or ql > 300:
                return JsonResponse({'success': False, 'message': 'Not a valid QL'})

            request.session['implants'][imp_slot]['ql'] = ql

            if not calc_implants(request, imp_slot):
                return JsonResponse({'success': False, 'message': 'Unable to update ql'})

            return JsonResponse({'success': True, 'implants' : request.session.get('implants')})
        except:
            if DEBUG:
                import traceback
                traceback.print_exc()
            return JsonResponse({'success': False, 'message': 'If you want to know how it works, just ask'})

    else:
        if DEBUG:
            import traceback
            traceback.print_exc()
        return JsonResponse({'success': False, 'message': 'Quit tinkering, that''s my job'})

def calc_implants(request, imp_slot):
    key = imp_slot
    val = request.session['implants'][key]
        
    if val['Shiny'] == 'Empty' and val['Bright'] == 'Empty' and val['Faded'] == 'Empty': # empty implant, set to default
        request.session['implants'][key]['treatment_value'] = 1
        request.session['implants'][key]['tl'] = 1
        request.session['implants'][key]['np_req'] = 1
        request.session['implants'][key]['jobe_skill'] = ''
        request.session['implants'][key]['jobe_skill_req'] = 1
        return True

    implants = Implant.objects.filter(shiny=val['Shiny'], bright=val['Bright'], faded=val['Faded'])
    if len(implants) <= 0:
        print('IMPLANT NOT FOUND:\nImplant: {}\nShiny: {}\nBright: {}\nFaded: {}'.format(key, val['Shiny'], val['Bright'], val['Faded']))
        breakpoint()
        return False
    target_ql = val['ql']

    for item in implants:
        if item.ql == 1 and target_ql < 201: # normal implant
            implant = item
            level_range = 199
            low_ql = 1
        elif item.ql == 201 and target_ql >= 201: # refined implant
            implant = item
            level_range = 99
            low_ql = 201

    for skill, req_vals in implant.reqs.items(): # equip requirements
        loval = req_vals['loval']
        hival = req_vals['hival']

        has_tl = False

        if skill == 'Treatment':
            if target_ql == 1 or target_ql == 201:
                request.session['implants'][key]['treatment_value'] = loval
            elif target_ql == 200 or target_ql == 300:
                request.session['implants'][key]['treatment_value'] = hival
            else:
                skill_per_ql = (hival - loval) / level_range
                treatment_req = round(skill_per_ql * (target_ql - low_ql)) + loval
                request.session['implants'][key]['treatment_value'] = treatment_req

        elif skill == 'Title level':
            has_tl = True
            if target_ql == 100:
                request.session['implants'][key]['tl'] = 3
            elif target_ql > 100 and target_ql <= 200:
                request.session['implants'][key]['tl'] = 4
            elif target_ql > 200 and target_ql <= 250:
                request.session['implants'][key]['tl'] = 5
            elif target_ql > 250:
                request.session['implants'][key]['tl'] = 6

        else:
            request.session['implants'][key]['attrib_name'] = skill
            if target_ql == 1 or target_ql == 201:
                request.session['implants'][key]['attrib_value'] = loval
            elif target_ql == 200 or target_ql == 300:
                request.session['implants'][key]['attrib_value'] = hival
            else:
                skill_per_ql = (hival - loval) / level_range
                attrib_req = round(skill_per_ql * (target_ql - low_ql)) + loval
                request.session['implants'][key]['attrib_value'] = attrib_req

        if not has_tl:
            request.session['implants'][key]['tl'] = 1
    
    # nanoprogramming requirements

    shiny_np, shiny_jobe, shiny_jobe_req, shiny_benefit = get_cluster_info(implant.shiny, target_ql, 'Shiny')
    bright_np, bright_jobe, bright_jobe_req, bright_benefit = get_cluster_info(implant.bright, target_ql, 'Bright')
    faded_np, faded_jobe, faded_jobe_req, faded_benefit = get_cluster_info(implant.faded, target_ql, 'Faded')

    np_reqs = [shiny_np, bright_np, faded_np]

    request.session['implants'][key]['np_req'] = round(max(np_reqs))

    request.session['implants'][key]['shiny_benefit'] = shiny_benefit
    request.session['implants'][key]['bright_benefit'] = bright_benefit
    request.session['implants'][key]['faded_benefit'] = faded_benefit

    jobe_reqs = {}
    if shiny_jobe != '':
        jobe_reqs[shiny_jobe] = shiny_jobe_req
    if bright_jobe != '':
        jobe_reqs[bright_jobe] = bright_jobe_req
    if faded_jobe != '':
        jobe_reqs[faded_jobe] = faded_jobe_req

    request.session['implants'][key]['jobe_reqs'] = jobe_reqs

    return True

def get_cluster_info(skill, ql, slot):
    if skill == 'Empty':
        return 0, '', 0, 0

    if ql < 201:
        target_ql = 1
        level_range = 199
    else:
        target_ql = 201
        level_range = 99

    cluster = Cluster.objects.get(skill=skill, clusterslot=CLUSTER_SLOTS[slot], ql=target_ql)

    jobe_skill = cluster.jobeskill

    if slot == 'Shiny':
        slot_mod = 2.0
        jobe_mod = cluster.jobemod
    elif slot == 'Bright':
        slot_mod = 1.5
        jobe_mod = cluster.jobemod
    elif slot == 'Faded':
        slot_mod = 1.0
        jobe_mod = cluster.jobemod

    np_req = ql * cluster.npmod * slot_mod
    jobe_skill_req = round(ql * jobe_mod)

    bene_per_ql = (cluster.hival - cluster.loval) / level_range
    benefit = round(((ql - 1) * bene_per_ql) + cluster.loval)

    return np_req, jobe_skill, jobe_skill_req, benefit
