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

    #weapon_list = get_weapon_list(request.session.get('stats'))
    weapon_list = []
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
            crit = int(data.get('crit'))
            if crit is not None and crit >= 0: request.session['stats']['crit'] = crit

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
            timeandspace = int(data.get('Time and space'))
            if timeandspace is not None and timeandspace >= 1: request.session['stats']['Time and space'] = timeandspace
            
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
            if aggdef is not None and -100 <= aggdef <= 100: request.session['stats']['aggdef'] = aggdef

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
    candidate_weapons = get_candidate_weapons(atk_skill) # weapons that primarily use atk_skill
    equipable_weapons = get_equipable_weapons(candidate_weapons, stats)

    weapon_list = []
    #weapon = ['Name', 'QL', 'Clip', 'Specials', 'Atk/Rch', 'Min', 'Max', 'Crit', 'Min', 'Avg', 'Max']
    for weapon in equipable_weapons:
        this_weapon = []
        this_weapon.append(weapon.name)
        this_weapon.append(weapon.ql)

        if weapon.clipsize <= 0:
            this_weapon.append('N/A')
        else:
            this_weapon.append(weapon.clipsize)

        this_weapon.append(', '.join(x for x in weapon.props))

        atk_time, rech_time = calculate_speeds(weapon, stats)
        this_weapon.append('{:.2f}/{:.2f}'.format(atk_time / 100, rech_time / 100))
        this_weapon.append(weapon.dmg_min)

        mid_dmg = round(weapon.dmg_min + (weapon.dmg_max - weapon.dmg_min) / 2)
        this_weapon.append(weapon.dmg_max)
        this_weapon.append(weapon.dmg_crit)
        this_weapon.append(0)
        this_weapon.append(0)
        this_weapon.append(0)
        weapon_list.append(this_weapon)
    
    return weapon_list

def calculate_speeds(weapon, stats):
    atk_time = weapon.atk_time
    rech_time = weapon.rech_time
    atk_time = atk_time - (stats['aggdef'] - 75)
    if atk_time < 100: atk_time = 100
    rech_time = rech_time - (stats['aggdef'] - 75)
    if rech_time < 100: rech_time = 100

    atk_time = round(atk_time - (stats[INITS[weapon.other.get('Initiative skill')]] / 6))
    if atk_time < 100: atk_time = 100
    rech_time = round(rech_time - (stats[INITS[weapon.other.get('Initiative skill')]] / 3))
    if rech_time < 100: rech_time = 100

    return atk_time, rech_time

def get_equipable_weapons(weapons, stats):
    equipable_weapons = []
    skip_duplicate = 0
    for weapon in weapons:
        if skip_duplicate > 0: # Assumes that all qls of same weapon are next to each other in the list
            skip_duplicate -= 1
            continue

        same_weapons = weapons.filter(name=weapon.name)
        eval_weapon = None
        if len(same_weapons) == 1:
            eval_weapon = weapon
        else:
            skip_duplicate = len(same_weapons) - 1 # skip all iterations of this weapon

            for i in range(len(same_weapons) - 1, 1, -1): # walk through list from high to low ql
                eval_weapon = interpolate(same_weapons[i-1], same_weapons[i], stats)
                if eval_weapon is not None:
                    break

        if eval_weapon is None: # Don't meet lo_weapon reqs, skip the rest
            continue

        if check_requirements(eval_weapon, stats):
            equipable_weapons.append(eval_weapon)

    return equipable_weapons

def interpolate(lo_weapon, hi_weapon, stats):
    if check_requirements(hi_weapon, stats):
        return hi_weapon
    elif not check_requirements(lo_weapon, stats):
        return None

    lo_ql = lo_weapon.ql
    hi_ql = hi_weapon.ql
    ql_delta = hi_ql - lo_ql
    min_dmg_delta = (hi_weapon.dmg_min - lo_weapon.dmg_min) / ql_delta
    max_dmg_delta = (hi_weapon.dmg_max - lo_weapon.dmg_max) / ql_delta
    crit_dmg_delta = (hi_weapon.dmg_crit - lo_weapon.dmg_crit) / ql_delta
    
    lo_ar_cap = lo_weapon.other.get('Attack rating cap')
    hi_ar_cap = hi_weapon.other.get('Attack rating cap')
    if lo_ar_cap is not None and hi_ar_cap is not None:
        ar_cap_delta = (hi_ar_cap - lo_ar_cap) / ql_delta
    else:
        ar_cap_delta = 0

    for i in range(hi_ql - lo_ql, 1, -1):
        
        weapon = Weapon()
        weapon.ql = lo_ql + i
        weapon.name = lo_weapon.name
        weapon.atk_time = lo_weapon.atk_time
        weapon.rech_time = lo_weapon.rech_time
        weapon.dmg_min = round(lo_weapon.dmg_min + (i * min_dmg_delta))
        weapon.dmg_max= round(lo_weapon.dmg_max + (i * max_dmg_delta))
        weapon.dmg_crit = round(lo_weapon.dmg_crit + (i * crit_dmg_delta))
        weapon.clipsize = lo_weapon.clipsize
        weapon.props = lo_weapon.props
        weapon.atk_skills = lo_weapon.atk_skills

        other = {}
        for key, val in lo_weapon.other.items():
            if key == 'Attack rating cap':
                other['Attack rating cap'] = round(val + (i * ar_cap_delta))
            else:
                other[key] = val
        weapon.other = other

        reqs = {}
        for key, val in lo_weapon.reqs.items():
            if key == 'Breed':
                reqs['Breed'] = val
            elif key == 'Profession':
                reqs['Profession'] = val
            elif key == 'Expansion sets':
                reqs['Expansion sets'] = val
            elif key == 'Level':
                reqs['Level'] = val
            else:
                reqs[key] = round(val + (i * ((hi_weapon.reqs.get(key) - val) / ql_delta)))
        weapon.reqs = reqs

        if check_requirements(weapon, stats):
            return weapon

def check_requirements(weapon, stats):
    for key, val in weapon.reqs.items():

        if key == 'Breed':
            if len(val) != 0:
                if not stats.get('breed') in val:
                    return False

        elif key == 'Profession':
            if len(val) != 0:
                if not stats.get('profession') in val:
                    return False

        elif key == 'Expansion sets':
            if 0 <= stats['subscription'] <= 2: # Froob and Sloob
                if val > stats['subscription']:
                    return False

        elif key == 'Level':
            if val > stats['level']:
                return False

        elif key == 'Cyberdeck': # MP QL215 weapon
            continue

        elif key == 'Faction':
            continue

        elif key == 'NPC type':
            return False

        else:
            try:
                if not stats.get(key) >= val:
                    return False
            except Exception as e:
                breakpoint()
                print(e)

    return True

def get_candidate_weapons(atk_skill):
    candidates = Weapon.objects.filter(atk_skills__has_key=atk_skill)
    weapons = candidates.filter(**{'atk_skills__' + atk_skill + '__gte' : 50}) # atk_skill is 50% or more of attack skill
    return weapons

def get_weapon_skill(stats): 
    weapon_skills = {
        '1h Blunt' : stats['1h Blunt'],
        '1h Edged' : stats['1h Edged'],
        '2h Blunt' : stats['2h Blunt'],
        '2h Edged' : stats['2h Edged'],
        'Martial arts' : stats['Martial arts'],
        'Melee energy' : stats['Melee energy'],
        'Piercing' : stats['Piercing'],
        'Time and space' : stats['Time and space'],
        'Assault rifle' : stats['Assault rifle'],
        'Bow' : stats['Bow'],
        'Smg' : stats['Smg'],
        'Pistol' : stats['Pistol'],
        'Ranged energy' : stats['Ranged energy'],
        'Rifle' : stats['Rifle'],
        'Shotgun' : stats['Shotgun']
    }

    return max(weapon_skills, key=weapon_skills.get)