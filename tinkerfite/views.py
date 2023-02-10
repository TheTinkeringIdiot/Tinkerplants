from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, FileResponse, HttpResponseRedirect

from tinkerfite.models import *
from tinkerfite.utils import *
from aobase.settings import *

import json, math, base64, pickle

# Create your views here.
def index(request):
    if request.session.get('stats') is None:
        request.session['stats'] = initial_weapons()
        print('Session setup')
    return render(request, 'tinkerfite/index.html')

def save_stats(request):
    if request.session.get('stats') is None:
        return JsonResponse({'success': False, 'message': 'Session timed out', 'next': ''})

    stats = []
    for key, val in request.session['stats'].items():
        stats.append(val)

    stat_pickle = pickle.dumps(stats)

    return JsonResponse({'success': True, 'stats': request.session.get('stats'), 'save_link' : base64.b64encode(stat_pickle).decode('ascii')})

def restore_stats(request):
    # breakpoint()
    if request.method == 'GET':
        b64_stats = request.GET.get('stats')
        if b64_stats is None:
            return JsonResponse({'success': False, 'message': 'If you want to know how it works, just ask'})

        decoded_stats = base64.b64decode(b64_stats)
        stat_vals = list(pickle.loads(decoded_stats))

        stats = initial_weapons()

        for i, key in enumerate(stats):
            stats[key] = stat_vals[i]

        request.session['stats'] = stats

        return HttpResponseRedirect('/tinkerfite')

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

            try: breed = int(data.get('breed'))
            except: breed = 1
            if breed is not None and 1 <= breed <= 4: request.session['stats']['breed'] = breed
            try: profession = int(data.get('profession'))
            except: profession = 0
            if profession is not None and 0 <= profession <= 15: request.session['stats']['profession'] = profession
            try: level = int(data.get('level'))
            except: level = 1
            if level is not None and 1 <= level <= 220: request.session['stats']['level'] = level
            try: subscription = int(data.get('subscription'))
            except: subscription = 0
            if subscription is not None and 0 <= subscription <= 128: request.session['stats']['subscription'] = subscription
            try: crit = int(data.get('crit'))
            except: crit = 0
            if crit is not None and crit >= 0: request.session['stats']['crit'] = crit

            try: onehb = int(data.get('1h Blunt'))
            except: onehb = 1
            if onehb is not None and onehb >= 1: request.session['stats']['1h Blunt'] = onehb
            try: onehe = int(data.get('1h Edged'))
            except: onehe = 1
            if onehe is not None and onehe >= 1: request.session['stats']['1h Edged'] = onehe
            try: twohb = int(data.get('2h Blunt'))
            except: twohb = 1
            if twohb is not None and twohb >= 1: request.session['stats']['2h Blunt'] = twohb
            try: twohe = int(data.get('2h Edged'))
            except: twohe = 1
            if twohe is not None and twohe >= 1: request.session['stats']['2h Edged'] = twohe
            try: martial_arts = int(data.get('Martial arts'))
            except: martial_arts = 1
            if martial_arts is not None and martial_arts >= 1: request.session['stats']['Martial arts'] = martial_arts
            try: melee_energy = int(data.get('Melee energy'))
            except: melee_energy = 1
            if melee_energy is not None and melee_energy >= 1: request.session['stats']['Melee energy'] = melee_energy
            try: piercing = int(data.get('Piercing'))
            except: piercing = 1
            if piercing is not None and piercing >= 1: request.session['stats']['Piercing'] = piercing
            try: timeandspace = int(data.get('Time and space'))
            except: timeandspace = 1
            if timeandspace is not None and timeandspace >= 1: request.session['stats']['Time and space'] = timeandspace
            
            try: assault_rifle = int(data.get('Assault rifle'))
            except: assault_rifle = 1
            if assault_rifle is not None and assault_rifle >= 1: request.session['stats']['Assault rifle'] = assault_rifle
            try: bow = int(data.get('Bow'))
            except: bow = 1
            if bow is not None and bow >= 1: request.session['stats']['Bow'] = bow
            try: grenade = int(data.get('Grenade'))
            except: grenade = 1
            if grenade is not None and grenade >= 1: request.session['stats']['Grenade'] = grenade
            try: mg_smg = int(data.get('Smg'))
            except: mg_smg = 1
            if mg_smg is not None and mg_smg >= 1: request.session['stats']['Smg'] = mg_smg
            try: pistol = int(data.get('Pistol'))
            except: pistol = 1
            if pistol is not None and pistol >= 1: request.session['stats']['Pistol'] = pistol
            try: re = int(data.get('Ranged energy'))
            except: re = 1
            if re is not None and re >= 1: request.session['stats']['Ranged energy'] = re
            try: rifle = int(data.get('Rifle'))
            except: rifle = 1
            if rifle is not None and rifle >= 1: request.session['stats']['Rifle'] = rifle
            try: shotgun = int(data.get('Shotgun'))
            except: shotgun = 1
            if shotgun is not None and shotgun >= 1: request.session['stats']['Shotgun'] = shotgun

            try: aimed = int(data.get('Aimed shot'))
            except: aimed = 1
            if aimed is not None and aimed >= 1: request.session['stats']['Aimed shot'] = aimed
            try: brawl = int(data.get('Brawl'))
            except: brawl = 1
            if brawl is not None and brawl >= 1: request.session['stats']['Brawl'] = brawl
            try: burst = int(data.get('Burst'))
            except: burst = 1
            if burst is not None and burst >= 1: request.session['stats']['Burst'] = burst
            try: dimach = int(data.get('Dimach'))
            except: dimach = 1
            if dimach is not None and dimach >= 1: request.session['stats']['Dimach'] = dimach
            try: fastattack = int(data.get('Fast attack'))
            except: fastattack = 1
            if fastattack is not None and fastattack >= 1: request.session['stats']['Fast attack'] = fastattack
            try: fling = int(data.get('Fling shot'))
            except: fling = 1
            if fling is not None and fling >= 1: request.session['stats']['Fling shot'] = fling
            try: fullauto = int(data.get('Full auto'))
            except: fullauto = 1
            if fullauto is not None and fullauto >= 1: request.session['stats']['Full auto'] = fullauto
            try: sneak = int(data.get('Sneak attack'))
            except: sneak = 1
            if sneak is not None and sneak >= 1: request.session['stats']['Sneak attack'] = sneak

            try: melee_init = int(data.get('melee_init'))
            except: melee_init = 1
            if melee_init is not None and melee_init >= 1: request.session['stats']['melee_init'] = melee_init
            try: phys_init = int(data.get('phys_init'))
            except: phys_init = 1
            if phys_init is not None and phys_init >= 1: request.session['stats']['phys_init'] = phys_init
            try: ranged_init = int(data.get('ranged_init'))
            except: ranged_init
            if ranged_init is not None and ranged_init >= 1: request.session['stats']['ranged_init'] = ranged_init
            try: aggdef = int(data.get('aggdef'))
            except: aggdef = 75
            if aggdef is not None and -100 <= aggdef <= 100: request.session['stats']['aggdef'] = aggdef

            try: aao = int(data.get('aao'))
            except: aao = 0
            if aao is not None and aao >= 1: request.session['stats']['aao'] = aao
            try: add_dmg = int(data.get('add_dmg'))
            except: add_dmg = 0
            if add_dmg is not None and add_dmg >= 1: request.session['stats']['add_dmg'] = add_dmg

            try: target_ac = int(data.get('target_ac'))
            except: target_ac = 1
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
    #weapon = ['AOID', 'Name', 'QL', 'Clip', 'Specials', 'Atk/Rch', 'Min', 'Avg', 'Max', 'Crit', 'Min', 'Avg', 'Max']
    for weapon in equipable_weapons:
        this_weapon = []
        this_weapon.append(weapon.aoid)
        this_weapon.append(weapon.name)
        this_weapon.append(weapon.ql)

        if weapon.clipsize <= 0:
            this_weapon.append('N/A')
        else:
            this_weapon.append(weapon.clipsize)

        this_weapon.append(DMG_TYPES[weapon.dmg_type])
        this_weapon.append(', '.join(x for x in weapon.props))

        atk_time, rech_time, min_dmg, avg_dmg, max_dmg, min_dps, avg_dps, max_dps = calculate_dps(weapon, stats)

        this_weapon.append('{:.2f}/{:.2f}'.format(atk_time / 100, rech_time / 100))
        this_weapon.append(min_dmg)
        
        this_weapon.append(avg_dmg)
        this_weapon.append(max_dmg)
        this_weapon.append(weapon.dmg_crit)
        this_weapon.append(min_dps)
        this_weapon.append(avg_dps)
        this_weapon.append(max_dps)
        weapon_list.append(this_weapon)
    
    return weapon_list

def calculate_dps(weapon, stats):
    sample_len = 60
    atk_time, rech_time = calculate_speeds(weapon, stats)
    cycle_time = (atk_time / 100) + (rech_time / 100)
    num_basic_attacks = math.floor(sample_len / cycle_time)
    ar_bonus = calculate_ar_bonus(weapon, stats)

    min_dmg = round((weapon.dmg_min * ar_bonus) + stats['add_dmg'])
    max_dmg = round((weapon.dmg_max * ar_bonus) + stats['add_dmg'] - (stats['target_ac'] / 10))
    if max_dmg < min_dmg: max_dmg = min_dmg
    avg_dmg = round(min_dmg + (max_dmg - min_dmg) / 2)

    num_crits = math.floor(num_basic_attacks * (stats['crit'] / 100))
    num_basic_attacks = num_basic_attacks - num_crits

    crit_min_dmg = round(((weapon.dmg_min + weapon.dmg_crit) * ar_bonus) + stats['add_dmg'])
    crit_dmg = round(((weapon.dmg_max + weapon.dmg_crit) * ar_bonus) + stats['add_dmg']  - (stats['target_ac'] / 10))
    if crit_dmg < crit_min_dmg: crit_dmg = crit_min_dmg

    min_special_dmg = 0
    avg_special_dmg = 0
    max_special_dmg = 0
    for special in weapon.props:
        if special == "Fling Shot":
            cycle_cap = math.floor(6 + (weapon.atk_time / 100))
            cycle_time = 1600 * (weapon.atk_time / 100) - stats['Fling shot'] / 100
            if cycle_time < cycle_cap: cycle_time = cycle_cap

            num_attacks = math.floor(sample_len / cycle_time)
            min_special_dmg += round(min_dmg * num_attacks)
            avg_special_dmg += round(avg_dmg * num_attacks)
            max_special_dmg += round(max_dmg * num_attacks)

        elif special == "Burst":
            cycle_cap = math.floor(8 + (weapon.atk_time / 100))
            burst_cycle = weapon.other.get('Burst cycle')
            if burst_cycle is None:
                burst_cycle = 0

            cycle_time = (weapon.rech_time / 100) * 20 + (burst_cycle / 100) - (stats['Burst'] / 25)
            if cycle_time < cycle_cap: cycle_time = cycle_cap

            num_attacks = math.floor(sample_len / cycle_time)
            min_special_dmg += round(min_dmg * 3 * num_attacks)
            avg_special_dmg += round(avg_dmg * 3 * num_attacks)
            max_special_dmg += round(max_dmg * 3 * num_attacks)

        elif special == "Full Auto":
            cycle_cap = math.floor(10 + (weapon.rech_time / 100))
            fa_cycle = weapon.other.get('Fullauto cycle')
            if fa_cycle is None: 
                fa_cycle = 0

            cycle_time = ((weapon.rech_time / 100) * 40) + (fa_cycle / 100) - (stats['Full auto'] / 25)
            if cycle_time < cycle_cap: cycle_time = cycle_cap

            num_rounds = 5 + (stats['Full auto'] / 100)
            if num_rounds > 15: num_rounds = 15
            if weapon.clipsize < num_rounds: num_rounds = weapon.clipsize

            min_fa_dmg = calculate_fa_dmg(min_dmg, num_rounds)
            avg_fa_dmg = calculate_fa_dmg(avg_dmg, num_rounds)
            max_fa_dmg = calculate_fa_dmg(max_dmg, num_rounds)

            num_attacks = math.floor(sample_len / cycle_time)
            min_special_dmg += round(min_fa_dmg * num_attacks)
            avg_special_dmg += round(avg_fa_dmg * num_attacks)
            max_special_dmg += round(max_fa_dmg * num_attacks)

        elif special == 'Aimed shot':
            # These are commented for posterity, since Tinkerfite uses PVE rules and AS will only fire once per fight
            # cycle_cap = math.floor(10 + (weapon.rech_time / 100))
            # cycle_time = (weapon.rech_time / 100) * 40 - (3 * stats['Aimed shot'] / 100)
            # if cycle_time < cycle_cap: cycle_time = cycle_cap

            as_dmg = round((weapon.dmg_max * ar_bonus) + stats['add_dmg'])
            as_bonus = stats['Aimed shot'] / 95
            as_dmg = as_dmg * as_bonus
            if as_dmg > 13000: as_dmg = 13000

            min_special_dmg += as_dmg
            avg_special_dmg += as_dmg
            max_special_dmg += as_dmg

        elif special == 'Fast attack':
            cycle_cap = math.floor(6 + (weapon.atk_time / 100))
            cycle_time = (weapon.atk_time / 100) * 15 - stats['Fast attack'] / 100
            if cycle_time < cycle_cap: cycle_time = cycle_cap

            num_attacks = math.floor(sample_len / cycle_time)
            min_special_dmg += round(min_dmg * num_attacks)
            avg_special_dmg += round(avg_dmg * num_attacks)
            max_special_dmg += round(max_dmg * num_attacks)

        elif special == 'Brawl':
            brawl_weapons = Weapon.objects.filter(name='Brawl Item')
            brawl_weapon = None
            
            for i in range(len(brawl_weapons) - 1, 0, -1): # walk through list from high to low ql
                brawl_weapon = interpolate(brawl_weapons[i-1], brawl_weapons[i], stats)
                if brawl_weapon is not None:
                    break

            min_brawl = round((brawl_weapon.dmg_min * ar_bonus) + stats['add_dmg'])
            max_brawl = round((brawl_weapon.dmg_max * ar_bonus) + stats['add_dmg'] - (stats['target_ac'] / 10))
            if max_brawl < min_brawl: max_brawl = min_brawl
            avg_brawl = round(min_brawl + (max_brawl - min_brawl) / 2)
            
            cycle_time = 15
            num_attacks = math.floor(sample_len / cycle_time)
            min_special_dmg += round(min_brawl * num_attacks)
            avg_special_dmg += round(avg_brawl * num_attacks)
            max_special_dmg += round(max_brawl * num_attacks)

        elif special == 'Dimach':
            pass

        elif special == 'Sneak attack':
            #cycle_time = 40
            sneak_bonus = round(stats['Sneak attack'] / 95)
            min_sneak_dmg = round(min_dmg * sneak_bonus)
            if min_sneak_dmg > 13000: min_sneak_dmg = 13000
            avg_sneak_dmg = round(avg_dmg * sneak_bonus)
            if avg_sneak_dmg > 13000: avg_sneak_dmg = 13000
            max_sneak_dmg = round(max_dmg * sneak_bonus)
            if max_sneak_dmg > 13000: max_sneak_dmg = 13000

            min_special_dmg += min_sneak_dmg
            avg_special_dmg += avg_sneak_dmg
            max_special_dmg += max_sneak_dmg

    min_dps = round(((min_dmg * num_basic_attacks) + (crit_dmg * num_crits) + min_special_dmg) / sample_len)
    avg_dps = round(((avg_dmg * num_basic_attacks) + (crit_dmg * num_crits) + avg_special_dmg) / sample_len)
    max_dps = round(((max_dmg * num_basic_attacks) + (crit_dmg * num_crits) + max_special_dmg) / sample_len)

    return atk_time, rech_time, min_dmg, avg_dmg, max_dmg, min_dps, avg_dps, max_dps

def calculate_fa_dmg(dmg, num_rounds):
    fa_dmg = dmg * num_rounds

    if fa_dmg > 10000:
        remain = round((fa_dmg - 10000) / 2)
        fa_dmg = 10000

        if remain > 1500:
            remain = round((remain - 1500) / 2)
            fa_dmg = 11500

            if remain > 1500:
                remain = round((remain - 1500) / 2)
                fa_dmg = 13000

                if remain > 1500:
                    remain = round((remain - 1500) / 2)
                    fa_dmg = 14500

                    if remain > 500:
                        fa_dmg = 15000

                else:
                    fa_dmg += remain
            else:
                fa_dmg += remain
        else:
            fa_dmg += remain
    
    return fa_dmg

def calculate_ar_bonus(weapon, stats):
    atk_skill = 0
    for key, val in weapon.atk_skills.items():
        try:
            atk_skill += round(stats.get(key) * (val / 100))
        except: # weird attack skills like nanoprogramming
            continue
    atk_skill += stats['aao']
    ar_cap = weapon.other.get('Attack rating cap')
    if ar_cap is not None and atk_skill > ar_cap: # MBS
        atk_skill = ar_cap

    ar_bonus = 1 + (atk_skill / 400)
    if atk_skill > 1000:
        ar_bonus += (atk_skill - 1000) / 1200

    return ar_bonus

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
    processed_weapons = []
    for weapon in weapons:
        if weapon.name in processed_weapons: 
            continue

        if weapon.name != 'Martial Arts Item':
            same_weapons = weapons.filter(name=weapon.name)
        elif stats['profession'] != 0:
            same_weapons = weapons.filter(name=weapon.name, reqs__Profession__contains=stats['profession'])
        else:
            same_weapons = weapons.filter(name=weapon.name, reqs__Profession__contains=1) # the 'Any' profession

        eval_weapon = None
        if len(same_weapons) == 1:
            if check_requirements(weapon, stats):
                equipable_weapons.append(weapon)
                continue
        else:
            processed_weapons.append(weapon.name) # skip all future iterations of this weapon

            for i in range(len(same_weapons) - 1, 0, -1): # walk through list from high to low ql
                eval_weapon = interpolate(same_weapons[i-1], same_weapons[i], stats)
                if eval_weapon is not None:
                    equipable_weapons.append(eval_weapon)
                    break

        if eval_weapon is None: # Don't meet lo_weapon reqs, skip the rest
            continue

    return equipable_weapons

def interpolate(lo_weapon, hi_weapon, stats):
    if check_requirements(hi_weapon, stats):
        return hi_weapon
    elif not check_requirements(lo_weapon, stats):
        return None

    lo_ql = lo_weapon.ql
    hi_ql = hi_weapon.ql
    ql_delta = hi_ql - lo_ql
    if ql_delta <= 0:
        return hi_weapon
    min_dmg_delta = (hi_weapon.dmg_min - lo_weapon.dmg_min) / ql_delta
    max_dmg_delta = (hi_weapon.dmg_max - lo_weapon.dmg_max) / ql_delta
    crit_dmg_delta = (hi_weapon.dmg_crit - lo_weapon.dmg_crit) / ql_delta
    
    lo_ar_cap = lo_weapon.other.get('Attack rating cap')
    hi_ar_cap = hi_weapon.other.get('Attack rating cap')
    if lo_ar_cap is not None and hi_ar_cap is not None:
        ar_cap_delta = (hi_ar_cap - lo_ar_cap) / ql_delta
    else:
        ar_cap_delta = 0

    for i in range(hi_ql - lo_ql, -1, -1):

        weapon = Weapon()
        weapon.aoid = hi_weapon.aoid
        weapon.ql = lo_ql + i
        weapon.name = lo_weapon.name
        weapon.atk_time = lo_weapon.atk_time
        weapon.rech_time = lo_weapon.rech_time
        weapon.dmg_min = round(lo_weapon.dmg_min + (i * min_dmg_delta))
        weapon.dmg_max= round(lo_weapon.dmg_max + (i * max_dmg_delta))
        weapon.dmg_crit = round(lo_weapon.dmg_crit + (i * crit_dmg_delta))
        weapon.dmg_type = lo_weapon.dmg_type
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
            if len(val) != 0 and not stats.get('profession') == 0:
                if not stats.get('profession') in val:
                    return False

        elif key == 'Expansion sets':
            if 0 <= stats['subscription'] <= 2: # Froob and Sloob
                if val > stats['subscription']:
                    return False

        elif key == 'Level':
            if val > stats['level']:
                return False

        elif key == 'Title level':
            if val == 7 and stats['level'] < 205:
                return False
            elif val == 6 and stats['level'] < 190:
                return False
            elif val == 5 and stats['level'] < 150:
                return False
            elif val == 4 and stats['level'] < 100:
                return False
            elif val == 3 and stats['level'] < 50:
                return False
            elif val == 2 and stats['level'] < 15:
                return False

        elif key == 'Cyberdeck': # MP QL215 weapon
            continue
        
        elif 'Faction' in key:
            continue

        elif key in ['Gender', 'Nano programming', 'Mechanical engineering', 'Weapon smithing', 'Parry', 'Riposte', 'Wielded weapons', '64', 'Form', 'Psychological modifications', 'Profession level']: # ignore these keys
            continue

        elif key == 'NPC type':
            return False

        else:
            try:
                if not stats.get(key) >= val:
                    return False
            except Exception as e:
                print('TINKERFITE: MISSING KEY: {} on {}'.format(key, weapon.name))
                print(e)

    return True

def get_candidate_weapons(atk_skill):
    candidates = Weapon.objects.filter(atk_skills__has_key=atk_skill)
    weapons = candidates.filter(**{'atk_skills__' + atk_skill + '__gte' : 50}) # atk_skill is 50% or more of attack skill
    weapons = weapons.exclude(aoid__in=BANNED_IDS)
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
        'Grenade' : stats['Grenade'],
        'Heavy weapons' : stats['Heavy weapons'],
        'Smg' : stats['Smg'],
        'Pistol' : stats['Pistol'],
        'Ranged energy' : stats['Ranged energy'],
        'Rifle' : stats['Rifle'],
        'Shotgun' : stats['Shotgun']
    }

    return max(weapon_skills, key=weapon_skills.get)