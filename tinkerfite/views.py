from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, FileResponse, HttpResponseRedirect

from tinkerfite.models import *
from tinkerfite.utils import *
from aobase.settings import *

import json, math

# Create your views here.
def index(request):
    if request.session.get('stats') is None:
        request.session['stats'] = initial_weapons()
        print('Session setup')
    return render(request, 'tinkerfite/index.html')

def update_display(request):
    if request.session.get('stats') is None:
        return JsonResponse({'success': False, 'message': 'Session timed out', 'next': ''})

    weapon_list = get_weapon_list(request.session.get('stats'))
    return JsonResponse({'success': True, 'stats': request.session.get('stats'), 'weapons' : json.dumps(weapon_list)})

def update_stats(request):
    if request.method == 'POST':
        try:
            if request.session.get('stats') is None:
                return JsonResponse({'success': False, 'message': 'Session timed out', 'next': ''})

            data = json.loads(request.body)

            breed = int(data.get('breed'))
            if breed is not None and 1 <= breed <= 4: request.session['stats']['breed'] = breed
            profession = int(data.get('profession'))
            if profession is not None and 1 <= profession <= 15: request.session['stats']['profession'] = profession
            level = int(data.get('level'))
            if level is not None and 1 <= level <= 220: request.session['stats']['level'] = level
            subscription = int(data.get('subscription'))
            if subscription is not None and 0 <= subscription <= 128: request.session['stats']['subscription'] = subscription

            onehb = int(data.get('1hb'))
            if onehb is not None and onehb >= 1: request.session['stats']['1hb'] = onehb
            onehe = int(data.get('1he'))
            if onehe is not None and onehe >= 1: request.session['stats']['1he'] = onehe
            twohb = int(data.get('2hb'))
            if twohb is not None and twohb >= 1: request.session['stats']['2hb'] = twohb
            twohe = int(data.get('2he'))
            if twohe is not None and twohe >= 1: request.session['stats']['2he'] = twohe
            martial_arts = int(data.get('martial_arts'))
            if martial_arts is not None and martial_arts >= 1: request.session['stats']['martial_arts'] = martial_arts
            melee_energy = int(data.get('melee_energy'))
            if melee_energy is not None and melee_energy >= 1: request.session['stats']['melee_energy'] = melee_energy
            piercing = int(data.get('piercing'))
            if piercing is not None and piercing >= 1: request.session['stats']['piercing'] = piercing
            
            assault_rifle = int(data.get('assault_rifle'))
            if assault_rifle is not None and assault_rifle >= 1: request.session['stats']['assault_rifle'] = assault_rifle
            bow = int(data.get('bow'))
            if bow is not None and bow >= 1: request.session['stats']['bow'] = bow
            mg_smg = int(data.get('mg_smg'))
            if mg_smg is not None and mg_smg >= 1: request.session['stats']['mg_smg'] = mg_smg
            pistol = int(data.get('pistol'))
            if pistol is not None and pistol >= 1: request.session['stats']['pistol'] = pistol
            re = int(data.get('re'))
            if re is not None and re >= 1: request.session['stats']['re'] = re
            rifle = int(data.get('rifle'))
            if rifle is not None and rifle >= 1: request.session['stats']['rifle'] = rifle
            shotgun = int(data.get('shotgun'))
            if shotgun is not None and shotgun >= 1: request.session['stats']['shotgun'] = shotgun

            aimed = int(data.get('aimed'))
            if aimed is not None and aimed >= 1: request.session['stats']['aimed'] = aimed
            brawl = int(data.get('brawl'))
            if brawl is not None and brawl >= 1: request.session['stats']['brawl'] = brawl
            burst = int(data.get('burst'))
            if burst is not None and burst >= 1: request.session['stats']['burst'] = burst
            dimach = int(data.get('dimach'))
            if dimach is not None and dimach >= 1: request.session['stats']['dimach'] = dimach
            fastattack = int(data.get('fastattack'))
            if fastattack is not None and fastattack >= 1: request.session['stats']['fastattack'] = fastattack
            fling = int(data.get('fling'))
            if fling is not None and fling >= 1: request.session['stats']['fling'] = fling
            fullauto = int(data.get('fullauto'))
            if fullauto is not None and fullauto >= 1: request.session['stats']['fullauto'] = fullauto
            sneak = int(data.get('sneak'))
            if sneak is not None and sneak >= 1: request.session['stats']['sneak'] = sneak

            melee_init = int(data.get('melee_init'))
            if melee_init is not None and melee_init >= 1: request.session['stats']['melee_init'] = melee_init
            phys_init = int(data.get('phys_init'))
            if phys_init is not None and phys_init >= 1: request.session['stats']['phys_init'] = phys_init
            ranged_init = int(data.get('ranged_init'))
            if ranged_init is not None and ranged_init >= 1: request.session['stats']['ranged_init'] = ranged_init
            aggdef = int(data.get('aggdef'))
            if aggdef is not None and aggdef >= 1: request.session['stats']['aggdef'] = aggdef

            aao = int(data.get('aao'))
            if aao is not None and aao >= 1: request.session['stats']['aao'] = aao
            add_dmg = int(data.get('add_dmg'))
            if add_dmg is not None and add_dmg >= 1: request.session['stats']['add_dmg'] = add_dmg

            target_ac = int(data.get('target_ac'))
            if target_ac is not None and target_ac >= 1: request.session['stats']['target_ac'] = target_ac

            weapon_list = get_weapon_list(request.session.get('stats'))

            return JsonResponse({'success': True, 'stats': json.dumps(request.session['stats']), 'weapons' : json.dumps(weapon_list)})

        except Exception as e:
            #if DEBUG:
            import traceback
            traceback.print_exc()

            return JsonResponse({'success': False, 'message': 'If you want to know how it works, just ask'})

def get_weapon_list(stats):
    weapon_list = []
    weapon = ['Name', 'QL', 'Clip', 'Specials', 'Atk/Rch', 'Min', 'Mid', 'Max', 'Crit', 'Min', 'Avg', 'Max']
    weapon_list.append(weapon)
    return weapon_list