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

            onehb = int(data.get('1h Blunt'))
            if onehb is not None and onehb >= 1: request.session['stats']['1h Blunt'] = onehb
            onehe = int(data.get('1h Edged'))
            if onehe is not None and onehe >= 1: request.session['stats']['1h Edged'] = onehe
            twohb = int(data.get('2h Blunt'))
            if twohb is not None and twohb >= 1: request.session['stats']['2h Blunt'] = twohb
            twohe = int(data.get('2h Edged'))
            if twohe is not None and twohe >= 1: request.session['stats']['2h Edged'] = twohe
            martial_arts = int(data.get('Martial arts'))
            if martial_arts is not None and martial_arts >= 1: request.session['stats']['Martial arts'] = martial_arts
            melee_energy = int(data.get('Melee energy'))
            if melee_energy is not None and melee_energy >= 1: request.session['stats']['Melee energy'] = melee_energy
            piercing = int(data.get('Piercing'))
            if piercing is not None and piercing >= 1: request.session['stats']['Piercing'] = piercing
            
            assault_rifle = int(data.get('Assault rifle'))
            if assault_rifle is not None and assault_rifle >= 1: request.session['stats']['Assault rifle'] = assault_rifle
            bow = int(data.get('Bow'))
            if bow is not None and bow >= 1: request.session['stats']['Bow'] = bow
            mg_smg = int(data.get('Smg'))
            if mg_smg is not None and mg_smg >= 1: request.session['stats']['Smg'] = mg_smg
            pistol = int(data.get('Pistol'))
            if pistol is not None and pistol >= 1: request.session['stats']['Pistol'] = pistol
            re = int(data.get('Ranged energy'))
            if re is not None and re >= 1: request.session['stats']['Ranged energy'] = re
            rifle = int(data.get('Rifle'))
            if rifle is not None and rifle >= 1: request.session['stats']['Rifle'] = rifle
            shotgun = int(data.get('Shotgun'))
            if shotgun is not None and shotgun >= 1: request.session['stats']['Shotgun'] = shotgun

            aimed = int(data.get('Aimed shot'))
            if aimed is not None and aimed >= 1: request.session['stats']['Aimed shot'] = aimed
            brawl = int(data.get('Brawl'))
            if brawl is not None and brawl >= 1: request.session['stats']['Brawl'] = brawl
            burst = int(data.get('Burst'))
            if burst is not None and burst >= 1: request.session['stats']['Burst'] = burst
            dimach = int(data.get('Dimach'))
            if dimach is not None and dimach >= 1: request.session['stats']['Dimach'] = dimach
            fastattack = int(data.get('Fast attack'))
            if fastattack is not None and fastattack >= 1: request.session['stats']['Fast attack'] = fastattack
            fling = int(data.get('Fling shot'))
            if fling is not None and fling >= 1: request.session['stats']['Fling shot'] = fling
            fullauto = int(data.get('Full auto'))
            if fullauto is not None and fullauto >= 1: request.session['stats']['Full auto'] = fullauto
            sneak = int(data.get('Sneak attack'))
            if sneak is not None and sneak >= 1: request.session['stats']['Sneak attack'] = sneak

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
    atk_skill = get_weapon_skill(stats)

    breakpoint()

    weapon_list = []
    weapon = ['Name', 'QL', 'Clip', 'Specials', 'Atk/Rch', 'Min', 'Mid', 'Max', 'Crit', 'Min', 'Avg', 'Max']
    weapon_list.append(weapon)
    return weapon_list

def get_weapon_skill(stats): 
    weapon_skills = {
        '1h Blunt' : stats['1h Blunt'],
        '1h Edged' : stats['1h Edged'],
        '2h Blunt' : stats['2h Blunt'],
        '2h Edged' : stats['2h Edged'],
        'Martial arts' : stats['Martial arts'],
        'Melee energy' : stats['Melee energy'],
        'Piercing' : stats['Piercing'],
        'Assault rifle' : stats['Assault rifle'],
        'Bow' : stats['Bow'],
        'Smg' : stats['Smg'],
        'Pistol' : stats['Pistol'],
        'Ranged energy' : stats['Ranged energy'],
        'Rifle' : stats['Rifle'],
        'Shotgun' : stats['Shotgun']
    }

    return max(weapon_skills, key=weapon_skills.get)