from ctypes import cast
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, FileResponse, HttpResponseRedirect

from tinkernukes.utils import *
from tinkernukes.models import *
from tinkernukes.utils import *
from aobase.settings import *

import json, math

# Create your views here.
def index(request):
    if request.session.get('stats') is None:
        request.session['stats'] = initial_nukes()
        print('Session setup')
    return render(request, 'tinkernukes/index.html')

def update_display(request):
    if request.session.get('stats') is None:
        return JsonResponse({'success': False, 'message': 'Session timed out', 'next': ''})

    nano_list = get_nano_list(request.session.get('stats'))
    return JsonResponse({'success': True, 'stats': request.session.get('stats'), 'nukes' : json.dumps(nano_list)})

def update_stats(request):
    if request.method == 'POST':
        try:
            if request.session.get('stats') is None:
                return JsonResponse({'success': False, 'message': 'Session timed out', 'next': ''})

            data = json.loads(request.body)

            breed = int(data.get('breed'))
            if breed is not None and breed >= 0 and breed <= 3:
                request.session['stats']['breed'] = breed

            level = int(data.get('level'))
            if level is not None and level > 0 and level <= 220:
                request.session['stats']['level'] = level

            mc = int(data.get('mc'))
            if mc is not None and mc > 0:
                request.session['stats']['mc'] = mc

            nano_init = int(data.get('nano_init'))
            if nano_init is not None and nano_init > 0:
                request.session['stats']['nano_init'] = nano_init

            max_nano = int(data.get('max_nano'))
            if max_nano is not None and max_nano > 0:
                request.session['stats']['max_nano'] = max_nano
            
            aggdef = int(data.get('aggdef'))
            if aggdef is not None and aggdef == 0 or aggdef == 100:
                request.session['stats']['aggdef'] = aggdef

            spec = int(data.get('spec'))
            if spec is not None and spec >= 0 and spec <= 4:
                request.session['stats']['spec'] = spec
            
            deck = int(data.get('deck'))
            if deck is not None and deck >= 0 and deck <= 8:
                request.session['stats']['deck'] = deck

            cost_pct = int(data.get('cost_pct'))
            if cost_pct is not None and cost_pct >= 0:
                request.session['stats']['cost_pct'] = cost_pct

            nano_dmg = int(data.get('nano_dmg'))
            if nano_dmg is not None and nano_dmg >= 0:
                request.session['stats']['nano_dmg'] = nano_dmg

            body_dev = int(data.get('body_dev'))
            if body_dev is not None and body_dev >= 1:
                request.session['stats']['body_dev'] = body_dev

            psychic = int(data.get('psychic'))
            if psychic is not None and psychic >= 1:
                request.session['stats']['psychic'] = psychic

            nano_delta = int(data.get('nano_delta'))
            if nano_delta is not None and nano_delta >= 0:
                request.session['stats']['nano_delta'] = nano_delta

            he = int(data.get('he'))
            if he is not None and he >= 0 and he <= 7:
                request.session['stats']['he'] = he

            crunchcom = int(data.get('crunchcom'))
            if crunchcom is not None and crunchcom >= 0 and crunchcom <= 7:
                request.session['stats']['crunchcom'] = crunchcom

            ns = int(data.get('ns'))
            if ns is not None and ns >= 0 and ns <= 10:
                request.session['stats']['NS'] = ns

            CoN = int(data.get('con'))
            if CoN is not None and CoN >= 0 and CoN <= 10:
                request.session['stats']['CoN'] = CoN

            END = int(data.get('end'))
            if END is not None and END >= 0 and END <= 10:
                request.session['stats']['END'] = END

            AM = int(data.get('am'))
            if AM is not None and AM >= 0 and AM <= 10:
                request.session['stats']['AM'] = AM

            target_ac = int(data.get('target_ac'))
            if target_ac is not None and target_ac >= 0:
                request.session['stats']['target_ac'] = target_ac

            dmg_type = int(data.get('dmg_type'))
            if dmg_type is not None and dmg_type >= 0 and dmg_type <= 9:
                request.session['stats']['dmg_type'] = dmg_type

            nano_list = get_nano_list(request.session.get('stats'))

            return JsonResponse({'success': True, 'stats': json.dumps(request.session['stats']), 'nukes' : json.dumps(nano_list)})

        except Exception as e:
            #if DEBUG:
            import traceback
            traceback.print_exc()

            return JsonResponse({'success': False, 'message': 'If you want to know how it works, just ask'})

def get_nano_list(stats):
    nano_regen = get_nano_regen(stats)
    pct_dmg = get_pct_dmg(stats)
    cost_pct = get_cost_pct(stats)
    atk_reduce = calc_atk_reduction(stats)

    nano_list = []

    db_nanos = Nano.objects.filter(mc__lte=stats['mc'])
    for db_nano in db_nanos:
        nano = []
        nano.append(db_nano.name)
        nano.append(db_nano.mc)
        nano.append(db_nano.nr_pct)
        nano.append(db_nano.ac)
        nano.append(db_nano.ql)

        if db_nano.deck > stats['deck']:
            continue
        if db_nano.deck == 0:
            nano.append('')
        else:
            nano.append(DECKS[db_nano.deck][0:2])

        if db_nano.level > stats['level']:
            continue
        if db_nano.level == 0:
            nano.append('')
        else:
            nano.append(db_nano.level)

        if db_nano.spec > stats['spec']:
            continue
        if db_nano.spec == 0:
            nano.append('')
        elif db_nano.spec == 8:
            nano.append(4)
        else:
            nano.append(db_nano.spec)

        if stats['dmg_type'] != 0:
            if db_nano.ac != DAMAGE_TYPES[stats['dmg_type']]:
                continue

        nano_cost = round(db_nano.cost * (1 - cost_pct / 100))
        nano.append(nano_cost)

        atk_speed = db_nano.attack - atk_reduce
        if atk_speed < db_nano.atk_cap:
            atk_speed = db_nano.atk_cap

        atk_rch = '{:.2f}/{:.2f}'.format(atk_speed / 100, db_nano.recharge / 100)

        nano.append(atk_rch) # atk/recharge

        ac_reduce = 0
        if stats['target_ac'] > 0:
            ac_reduce = round(stats['target_ac'] / 10)

        dmg_multiplier = 1 + (pct_dmg / 100)
        low_dmg = round(db_nano.low_dmg * dmg_multiplier)
        high_dmg = round(db_nano.high_dmg * dmg_multiplier) - ac_reduce
        if high_dmg < low_dmg:
            high_dmg = low_dmg
        avg_dmg = round((low_dmg + high_dmg) / 2)

        nano.append(low_dmg)
        nano.append(avg_dmg)
        nano.append(high_dmg)

        cast_time = (atk_speed + db_nano.recharge) / 100
        min_dps = round(low_dmg / cast_time)
        avg_dps = round(avg_dmg / cast_time)
        high_dps = round(high_dmg / cast_time)

        nano.append(min_dps)
        nano.append(avg_dps)
        nano.append(high_dps)

        nps = round(nano_cost / cast_time)
        nano.append(nps)

        if nano_regen >= nps:
            nano.append('∞')
        else:
            nano.append('{}s'.format(round(stats['max_nano'] / (nps - nano_regen))))
        

        nano_list.append(nano)

    return nano_list

def calc_atk_reduction(stats):
    init = stats['nano_init']
    reduction = 0

    if init > 1200:
        reduction = 600
        init = init - 1200
        reduction += init / 6
    else:
        reduction = init / 2

    if stats['aggdef'] == 100:
        reduction += 25
    elif stats['aggdef'] == 0:
        reduction -= 125

    return reduction

def get_nano_regen(stats):
    regen = 0
    regen += CRUNCHCOM[stats['crunchcom']]
    regen += HUMIDITY[stats['he']]
    regen += NOTUM_SIPHON[stats['NS']]
    regen += CHANNELING_OF_NOTUM[stats['CoN']]

    nano_delta = 0
    if stats['breed'] == 0 or stats['breed'] == 1: # Solitus and Opifex
        nano_delta = 3
    elif stats['breed'] == 2: # Nanomage
        nano_delta = 4
    elif stats['breed'] == 3: # Atrox
        nano_delta = 2

    nano_delta += math.floor(stats['body_dev'] / 100)
    nano_delta += stats['nano_delta']

    tick_sec = 28 - (math.floor((stats['psychic'] - 1) / 60) * 2)

    regen += round(nano_delta / tick_sec)

    return regen

def get_pct_dmg(stats):
    pct_dmg = 0
    pct_dmg += ENHANCE_NANO_DAMAGE[stats['END']]
    pct_dmg += ANCIENT_MATRIX[stats['AM']]
    pct_dmg += stats['nano_dmg']

    return pct_dmg

def get_cost_pct(stats):
    cost_pct = 0
    cost_pct += CRUNCHCOM[stats['crunchcom']]
    cost_pct += stats['cost_pct']

    if stats['breed'] == 0 or stats['breed'] == 1: # Solitus and Opifex
        if cost_pct > 50:
            cost_pct = 50
    elif stats['breed'] == 2: # Nanomage
        if cost_pct > 55:
            cost_pct = 55
    elif stats['breed'] == 3: # Atrox
        if cost_pct > 45:
            cost_pct = 45

    return cost_pct