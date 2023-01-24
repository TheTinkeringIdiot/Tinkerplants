#from models import *

import xml.etree.ElementTree as ET
import math


NP_MODS = {'1h Blunt' : 1.8, '1h Edged Weapon' : 1.9, '2h Blunt' : 1.8, '2h Edged' : 1.9, 'Adventuring' : 1.5, 'Agility' : 2.25, 
'Aimed Shot' : 2.1, 'Assault Rif' : 2.25, 'Bio.Metamor' : 2.4, 'Body Dev' : 2.0, 'Bow' : 2.0, 'Bow Spc Att' : 2.0, 'Brawling' : 1.65, 
'Break & Entry' : 2.0, 'Burst' : 2.1, 'Chemical AC' : 2.0, 'Chemistry' : 2.0, 'Cold AC' : 2.0, 'Comp. Liter' : 2.0, 'Concealment' : 1.8, 
'Dimach' : 2.25, 'Disease AC' : 1.75, 'Dodge-Rng' : 2.0, 'Duck-Exp' : 2.0, 'Elec. Engi' : 2.0, 'Energy AC' : 2.25, 'Evade-ClsC' : 2.0, 
'Fast Attack' : 1.9, 'Fire AC' : 2.0, 'First Aid' : 1.8, 'Fling Shot' : 1.8, 'Full Auto' : 2.25, 'Grenade' : 1.9, 'Heavy Weapons' : 1.0, 
'Imp/Proj AC' : 2.25, 'Intelligence' : 2.25, 'Map Nav' : 1.25, 'Martial Arts' : 2.5, 'Matter Crea' : 2.4, 'Matt.Metam' : 2.4, 'Max Health' : 2.5, 
'Max Nano' : 2.5, 'Mech. Engi' : 2.0, 'Melee Ener' : 2.0, 'Melee. Init' : 2.0, 'Melee AC' : 2.25, 'MG / SMG' : 2.0, 'Mult. Melee' : 2.25, 
'Multi Ranged' : 2.0, 'NanoC. Init' : 2.0, 'Nano Pool' : 3.0, 'Nano Progra' : 2.0, 'Nano Resist' : 2.0, 'Parry' : 2.1, 'Perception' : 2.0, 
'Pharma Tech' : 2.0, 'Physic. Init' : 2.0, 'Piercing' : 1.6, 'Pistol' : 2.0, 'Psychic' : 2.25, 'Psycho Modi' : 2.4, 'Psychology' : 2.0, 
'Quantum FT' : 2.0, 'Radiation AC' : 2.0, 'Ranged Energy' : 2.0, 'Ranged Init' : 2.0, 'Rifle' : 2.25, 'Riposte' : 2.5, 'Run Speed' : 2.0, 
'Sense' : 2.25, 'Sensory Impr' : 2.20, 'Sharp Obj' : 1.25, 'Shotgun' : 1.7, 'Sneak Atck' : 2.5, 'Stamina' : 2.25, 'Strength' : 2.25, 
'Swimming' : 1.25, 'Time & Space' : 2.4, 'Trap Disarm' : 1.8, 'Treatment' : 2.15, 'Tutoring' : 1.3, 'Vehicle Air' : 1.0, 'Vehicle Ground' : 1.5, 
'Vehicle Water' : 1.2, 'Weapon Smt' : 2.0}

JOBE_SKILL = {
    'Add All Def.' : 'Psychology', 
    'Add All Off' : 'Psychology', 
    'Add. Chem. Dam.' : 'Quantum FT', 
    'Add. Energy Dam.' : 'Quantum FT', 
    'Add. Fire Dam.' : 'Quantum FT', 
    'Add. Melee Dam.' : 'Quantum FT', 
    'Add. Poison Dam.' : 'Quantum FT', 
    'Add. Proj. Dam.' : 'Quantum FT',  
    'Add.Rad. Dam.' : 'Quantum FT', 
    'Add. Xp' : 'Psychology', 
    'Heal Delta' : 'Pharma Tech', 
    'Max NCU' : 'Computer Literacy', 
    'Nano Delta' : 'Pharma Tech', 
    'Nano Point Cost Modifier' : 'Quantum FT', 
    'NF Interrupt' : 'Psychology', 
    'Nano Formula Interrupt Modifier' : 'Nanoprogramming', 
    'RangeInc. NF' : 'Nanoprogramming', 
    'RangeInc. Weapon' : 'Weaponsmithing', 
    'Shield Chemical AC' : 'Quantum FT', 
    'Shield Cold AC' : 'Quantum FT', 
    'Shield Melee AC' : 'Quantum FT', 
    'Shield Poison AC' : 'Quantum FT', 
    'Shield Energy AC' : 'Quantum FT', 
    'Shield Fire AC' : 'Quantum FT', 
    'Shield Projectile AC' : 'Quantum FT', 
    'Shield Radiation AC' : 'Quantum FT', 
    'Skill Time Lock Modifier' : 'Psychology'}

JOBE_MODS = {'Shiny' : 6.25, 'Bright' : 4.75, 'Faded' : 3.25}

ALL_SKILLS = ['Empty', 'Shield Energy AC', 'Fast Attack', 'Fire AC', 'Heavy Weapons', 'Skill Time Lock Modifier', 'Riposte', 'Bow Spc Att', 'Melee/Ma AC', 'Shield Cold AC', 'Vehicle Grnd', 'Mult. Melee', 'Add. Energy Dam.', 'Rifle', 'Weapon Smt', 'NanoC. Init', 'Dimach', 'Concealment', 'Sharp Obj', 'Bow', 'Elec. Engi', 'Add All Off', 'Time & Space', 'Add. Proj. Dam.', '1h Blunt', 'Add. Chem. Dam.', '1h Edged Weapon', 'Duck-Exp', 'Add. Xp', 'Ranged Ener', 'Nano Delta', 'Psychic', 'Imp/Proj AC', 'Full Auto', 'Evade-ClsC', 'Strength', '2h Edged', 'Energy AC', 'Body Dev', 'Shield Fire AC', 'Disease AC', 'Melee Ener', 'RangeInc. NF', 'Pistol', 'Piercing', 'Adventuring', 'Nano Progra', 'Sense', 'Nano Point Cost Modifier', 'Vehicle Hydr', 'Break & Entry', 'Comp. Liter', 'Nano Formula Interrupt Modifier', 'RangeInc. Weapon', 'Add. Fire Dam.', 'Max Nano', 'Agility', 'Matt.Metam', 'Shield Melee AC', 'Stamina', 'Add. Melee Dam.', 'Ranged. Init', 'Map Navig', 'Pharma Tech', 'Grenade', 'First Aid', 'Matter Crea', 'Bio.Metamor', 'Max Health', 'Vehicle Air', 'Heal Delta', 'Shield Radiation AC', 'Mech. Engi', 'Shield Poison AC', 'Treatment', 'Add. Poison Dam.', 'Chemistry', 'Run Speed', 'Sneak Atck', 'Add.Rad. Dam.', 'Dodge-Rng', 'Physic. Init', 'Psychology', 'Psycho Modi', 'Burst', 'Melee. Init', 'Trap Disarm', 'Swimming', 'Shield Projectile AC', 'MG / SMG', 'Cold AC', 'Nano Pool', 'Radiation AC', 'Quantum FT', 'Perception', 'Aimed Shot', 'Max NCU', 'Tutoring', 'Assault Rif', 'Parry', 'Chemical AC', 'Multi Ranged', 'Add All Def.', '2h Blunt', 'Shotgun', 'Martial Arts', 'Brawling', 'Shield Chemical AC', 'Sensory Impr', 'Fling Shot', 'Nano Resist', 'Intelligence'
]

IMP_SLOT_INDEX = {
    'Eye' : 1,
    'Head' : 2,
    'Ear' : 3,
    'Right-Arm' : 4,
    'Right arm' : 4,
    'Chest' : 5,
    'Body' : 5,
    'Left-Arm' : 6,
    'Left arm' : 6,
    'Right-Wrist' : 7,
    'Right wrist' : 7,
    'Waist' : 8,
    'Left-Wrist' : 9,
    'Left wrist' : 9,
    'Right-Hand' : 10,
    'Right hand' : 10,
    'Leg' : 11,
    'Legs' : 11,
    'Left-Hand' : 12,
    'Left hand' : 12,
    'Feet' : 13
}

IMP_SLOTS = [
    'Eye',
    'Head',
    'Ear',
    'Right-Arm',
    'Chest',
    'Left-Arm',
    'Right-Wrist',
    'Waist',
    'Left-Wrist',
    'Right-Hand',
    'Leg',
    'Left-Hand',
    'Feet'
]

IMP_SKILLS = {
    'Eye' : {
        'Shiny' : ['Empty','Aimed Shot','Elec. Engi','Map Navig','RangeInc. Weapon','Rifle','Tutoring','Vehicle Air'],
        'Bright' : ['Empty','Chemistry','Comp. Liter','Grenade','Heavy Weapons','Intelligence','Mech. Engi','Mult. Melee','Nano Progra','NanoC. Init','Perception','Pharma Tech','Psycho Modi','Quantum FT','Ranged Ener','Sensory Impr','Treatment','Vehicle Grnd','Vehicle Hydr'],
        'Faded' : ['Empty','Assault Rif','Bow','Concealment','Matter Crea','Multi Ranged','Pistol','Psychology','Sharp Obj','Sneak Atck','Time & Space','Weapon Smt']
    },
    'Head' : {
        'Shiny' : ['Empty','Bio.Metamor','Bow Spc Att','Chemistry','Comp. Liter','Disease AC','First Aid','Intelligence','Matt.Metam','Matter Crea','Max Nano','Mech. Engi','Melee Ener','Nano Progra','Nano Resist','NanoC. Init','Pharma Tech','Psychic','Psycho Modi','Psychology','Quantum FT','Ranged Ener','Sensory Impr','Time & Space','Treatment','Vehicle Grnd','Vehicle Hydr'],
        'Bright' : ['Empty','Dimach','Elec. Engi','Map Navig','Nano Pool','Ranged. Init','Weapon Smt'],
        'Faded' : ['Empty','Perception','Sense','Trap Disarm','Tutoring','Vehicle Air']
    },
    'Ear' : {
        'Shiny' : ['Empty','Add. Xp','Max NCU','Perception'],
        'Bright' : ['Empty','Concealment','Nano Point Cost Modifier','Psychology','Tutoring','Vehicle Air'],
        'Faded' : ['Empty','Intelligence','Map Navig','Psychic','Psycho Modi','Vehicle Grnd','Vehicle Hydr']
    },
    'Right-Arm' : {
        'Shiny' : ['Empty','1h Blunt','1h Edged Weapon','2h Blunt','2h Edged','Assault Rif','Bow','Break & Entry','Burst','Fling Shot','Full Auto','Grenade','Heavy Weapons','MG / SMG','Piercing','Shotgun','Strength'],
        'Bright' : ['Empty','Add All Def.','Add All Off','Brawling','Chemical AC','Nano Delta','Physic. Init','Swimming'],
        'Faded' : ['Empty','Fast Attack','Mech. Engi','Parry','Radiation AC','RangeInc. NF','RangeInc. Weapon','Riposte']
    },
    'Chest' : {
        'Shiny' : ['Empty','Body Dev','Dimach','Energy AC','Max Health','Melee/Ma AC','Nano Pool','Sense','Stamina'],
        'Bright' : ['Empty','Bio.Metamor','Imp/Proj AC','Matt.Metam','Psychic'],
        'Faded' : ['Empty','2h Blunt','Adventuring','Break & Entry','Disease AC','MG / SMG','Max Nano','Nano Formula Interrupt Modifier','NanoC. Init','Sensory Impr','Skill Time Lock Modifier','Strength']
    },
    'Left-Arm' : {
        'Shiny' : ['Empty','Add All Def.','Add All Off','Brawling','Heal Delta','RangeInc. NF'],
        'Bright' : ['Empty','2h Blunt','2h Edged','Bow','Break & Entry','Piercing','Radiation AC','Strength'],
        'Faded' : ['Empty','Chemical AC','Matt.Metam','Nano Point Cost Modifier','Physic. Init','Swimming']
    },
    'Right-Wrist' : {
        'Shiny' : ['Empty','Nano Delta','Parry','Pistol','Ranged. Init','Riposte','Run Speed','Sharp Obj'],
        'Bright' : ['Empty','1h Blunt','1h Edged Weapon','Aimed Shot','Burst','Full Auto','Max NCU','Multi Ranged','Nano Resist','Rifle','Sneak Atck'],
        'Faded' : ['Empty','Add. Chem. Dam.','Add. Energy Dam.','Add. Fire Dam.','Add. Melee Dam.','Add. Poison Dam.','Add. Proj. Dam.','Add.Rad. Dam.','Bow Spc Att','Fling Shot','Melee Ener','Mult. Melee']
    },
    'Waist' : {
        'Shiny' : ['Empty','Chemical AC','Cold AC','Fire AC','Nano Point Cost Modifier','Radiation AC'],
        'Bright' : ['Empty','Adventuring','Body Dev','Duck-Exp','Max Health','Max Nano','Melee/Ma AC','Sense'],
        'Faded' : ['Empty','2h Edged','Agility','Bio.Metamor','Brawling','Dimach','Dodge-Rng','Energy AC','Evade-ClsC','Full Auto','Imp/Proj AC','Melee. Init','Nano Pool','Piercing','Shotgun','Stamina']
    },
    'Left-Wrist' : {
        'Shiny' : ['Empty','Mult. Melee','Multi Ranged','Shield Energy AC','Shield Fire AC','Shield Projectile AC','Shield Radiation AC'],
        'Bright' : ['Empty','Add. Chem. Dam.','Add. Energy Dam.','Add. Fire Dam.','Add. Melee Dam.','Add. Poison Dam.','Add. Proj. Dam.','Add.Rad. Dam.','Melee Ener','Parry','Riposte','Run Speed'],
        'Faded' : ['Empty','Nano Resist','Rifle','Shield Chemical AC','Shield Cold AC','Shield Melee AC','Shield Poison AC']
    },
    'Right-Hand' : {
        'Shiny' : ['Empty','Add. Chem. Dam.','Add. Energy Dam.','Add. Fire Dam.','Add. Melee Dam.','Add. Poison Dam.','Add. Proj. Dam.','Add.Rad. Dam.','Martial Arts','Trap Disarm','Weapon Smt'],
        'Bright' : ['Empty','Assault Rif','Bow Spc Att','Cold AC','Fast Attack','First Aid','Fling Shot','MG / SMG','Matter Crea','Pistol','Sharp Obj','Shotgun','Time & Space'],
        'Faded' : ['Empty','1h Blunt','1h Edged Weapon','Aimed Shot','Burst','Chemistry','Comp. Liter','Elec. Engi','Fire AC','Grenade','Heavy Weapons','Nano Progra','Pharma Tech','Quantum FT','Ranged. Init','Treatment']
    },
    'Leg' : {
        'Shiny' : ['Empty','Adventuring','Agility','Dodge-Rng','Duck-Exp','Imp/Proj AC','Nano Formula Interrupt Modifier','Skill Time Lock Modifier','Swimming'],
        'Bright' : ['Empty','Disease AC','Energy AC','Evade-ClsC','Melee. Init','Stamina'],
        'Faded' : ['Empty','Add. Xp','Body Dev','Heal Delta','Max Health','Max NCU','Melee/Ma AC','Run Speed','Shield Energy AC','Shield Fire AC','Shield Projectile AC','Shield Radiation AC']
    },
    'Left-Hand' : {
        'Shiny' : ['Empty','Fast Attack','Shield Chemical AC','Shield Cold AC','Shield Melee AC','Shield Poison AC'],
        'Bright' : ['Empty','Fire AC','Nano Formula Interrupt Modifier','RangeInc. NF','Shield Energy AC','Shield Fire AC','Shield Projectile AC','Shield Radiation AC','Skill Time Lock Modifier','Trap Disarm'],
        'Faded' : ['Empty','Cold AC','First Aid','Martial Arts','Ranged Ener']
    },
    'Feet' : {
        'Shiny' : ['Empty','Concealment','Evade-ClsC','Melee. Init','Physic. Init','Sneak Atck'],
        'Bright' : ['Empty','Add. Xp','Agility','Dodge-Rng','Heal Delta','Martial Arts','RangeInc. Weapon','Shield Chemical AC','Shield Cold AC','Shield Melee AC','Shield Poison AC'],
        'Faded' : ['Empty','Add All Def.','Add All Off','Duck-Exp','Nano Delta']
    }
}

CLUSTER_SLOTS = {
    'Shiny' : 0,
    'Bright' : 1,
    'Faded' : 2
}

CLUSTER_MIN_QL = {
    'Shiny' : 0.86,
    'Bright' : 0.84,
    'Faded' : 0.82  
}

def initial_implants():
    implants = {}
    for slot in IMP_SLOTS:
        imp_stats = {
            'Shiny' : 'Empty',
            'Bright' : 'Empty',
            'Faded' : 'Empty',
            'ql' : 1,
            'attrib_name' : '',
            'attrib_value' : 1,
            'treatment_value' : 1,
            'tl' : 1,
            'np_req' : 1,
            'shiny_benefit' : 0,
            'bright_benefit' : 0,
            'faded_benefit' : 0,
            'jobe_reqs' : {}
        }
        implants[slot] = imp_stats
    
    return implants

def initial_prefs():
    prefs = {
        'Agility' : False,
        'Intelligence' : False,
        'Psychic' : False,
        'Sense' : False,
        'Stamina' : False,
        'Strength' : False
    }

    return prefs

def pick_faded_cluster(slot):
    skills = list(IMP_SKILLS[slot]['Faded'])
    skills.remove('Empty')

    chosen = ''
    chosen_val = 0.0

    for skill in skills:
        try:
            if NP_MODS[skill] > chosen_val:
                chosen = skill
                chosen_val = NP_MODS[skill]
        except:
            pass # JOBE clusters can't be cleaned, so don't select them

    return chosen

def rk_cluster_np(skill, slot, ql):
    slot_mod = 1.0
    if slot == 'Shiny':
        slot_mod = 2.0
    elif slot == 'Bright':
        slot_mod = 1.5
    elif slot == 'Faded':
        slot_mod = 1.0

    return round(NP_MODS[skill] * ql * slot_mod)

def jobe_cluster_skill(skill, slot, ql):
    slot_mod = 1.0
    if skill != 'Nano Delta':
        if slot == 'Shiny':
            slot_mod = 6.25
        elif slot == 'Bright':
            slot_mod = 4.75
        elif slot == 'Faded':
            slot_mod = 3.25

    else:
        if slot == 'Shiny':
            slot_mod = 5.25
        elif slot == 'Bright':
            slot_mod = 4.0
        elif slot == 'Faded':
            slot_mod = 2.75

    return round(ql * slot_mod)

def rk_ql_bump(np_skill, skill, slot, ql):
    np_req = rk_cluster_np(skill, slot, ql)
    if np_skill < np_req:
        return False, 0
    bumps = 0
    if slot == 'Shiny':
        over_factor = 300
    elif slot == 'Bright':
        over_factor = 200
    elif slot == 'Faded':
        over_factor = 100
    else:
        return False, 0

    bumps = int((np_skill - np_req) / over_factor)

    if ql in range(1, 50):
        bumps = 0
    elif ql in range(50, 100):
        bumps = 1 if bumps >= 1 else bumps
    elif ql in range(100, 150):
        bumps = 2 if bumps >= 2 else bumps
    elif ql in range(150, 200):
        bumps = 3 if bumps >= 3 else bumps
    elif ql in range(200, 250):
        bumps = 4 if bumps >= 4 else bumps
    elif ql in range(250, 300):
        bumps = 5 if bumps >= 5 else bumps

    return True, bumps

def jobe_ql_bump(combine_skill, skill, slot, ql):
    skill_req = jobe_cluster_skill(skill, slot, ql)
    if combine_skill < skill_req:
        return False, 0
    bumps = 0
    if slot == 'Shiny':
        over_factor = 400
    elif slot == 'Bright':
        over_factor = 300
    elif slot == 'Faded':
        over_factor = 200
    else:
        return False, 0

    bumps = int((combine_skill - skill_req) / over_factor)

    if ql in range(1, 99):
        bumps = 0
    elif ql == 99:
        bumps = 1 if bumps >= 1 else bumps
    elif ql in range(100, 150):
        bumps = 2 if bumps >= 2 else bumps
    elif ql in range(150, 200):
        bumps = 3 if bumps >= 3 else bumps
    elif ql in range(200, 250):
        bumps = 4 if bumps >= 4 else bumps
    elif ql in range(250, 300):
        bumps = 5 if bumps >= 5 else bumps

    return True, bumps

def rk_cluster_ql_bump(slot, skill, combine_skills, cur_ql, min_ql):
    start_ql = cur_ql

    np_skill = int(combine_skills.get('Nanoprogramming'))

    enuf_skill, bumps = rk_ql_bump(np_skill, skill, slot, start_ql)
    if not enuf_skill:
        return ['Your nanoprogramming skill is too low to build this implant.'], start_ql, False

    temp_ql = start_ql - bumps
    enuf_skill, check_bumps = rk_ql_bump(np_skill, skill, slot, temp_ql)
    cur_ql = start_ql - check_bumps

    if cur_ql < min_ql or temp_ql < min_ql:
        return ['Your nanoprogramming skill is too high to build this implant.'], start_ql, False

    cluster_ql = math.ceil(CLUSTER_MIN_QL[slot] * cur_ql)
    if cluster_ql < min_ql:
        cluster_ql = min_ql

    return 'Add a QL {}+ {} {} cluster. The result is QL {}.'.format(cluster_ql, slot, skill, start_ql), cur_ql, True

def jobe_cluster_ql_bump(slot, skill, combine_skills, cur_ql, min_ql):
    start_ql = cur_ql

    req_skill = JOBE_SKILL[skill]

    combine_skill = int(combine_skills.get(req_skill))

    enuf_skill, bumps = jobe_ql_bump(combine_skill, skill, slot, start_ql)
    if not enuf_skill:
        return ['Your {} is too low to build this implant.'.format(req_skill)], start_ql, False

    temp_ql = start_ql - bumps
    enuf_skill, check_bumps = jobe_ql_bump(combine_skill, skill, slot, temp_ql)
    cur_ql = start_ql - check_bumps

    if cur_ql < min_ql or temp_ql < min_ql:
        return ['Your {} skill is too high to build this implant.'.format(req_skill)], start_ql, False

    cluster_ql = math.ceil(CLUSTER_MIN_QL[slot] * cur_ql)

    return 'Add a QL {}+ {} {} cluster. The result is QL {}.'.format(cluster_ql, slot, skill, start_ql), cur_ql, True

