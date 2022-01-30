#from models import *

import xml.etree.ElementTree as ET


NP_MODS = {'1h Blunt' : 1.8, '1h Edged Weapon' : 1.9, '2h Blunt' : 1.8, '2h Edged' : 1.9, 'Adventuring' : 1.5, 'Agility' : 2.25, 
'Aimed Shot' : 2.1, 'Assault Rif' : 2.25, 'Bio.Metamor' : 2.4, 'Body Dev' : 2.0, 'Bow' : 2.0, 'Bow Spc Att' : 2.0, 'Brawling' : 1.65, 
'Break & Entry' : 2.0, 'Burst' : 2.1, 'Chemical AC' : 2.0, 'Chemistry' : 2.0, 'Cold AC' : 2.0, 'Comp Lit' : 2.0, 'Concealment' : 1.8, 
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

JOBE_SKILL = {'Add All Def.' : 'Psychology', 'Add All Off' : 'Psychology', 'Add. Chem. Dam.' : 'Quantum FT', 'Add. Energy Dam.' : 'Quantum FT', 
'Add. Fire Dam.' : 'Quantum FT', 'Add. Melee Dam.' : 'Quantum FT', 'Add. Poison Dam.' : 'Quantum FT', 'Add. Proj. Dam.' : 'Quantum FT',  
'Add.Rad. Dam.' : 'Quantum FT', 'Add. Xp' : 'Psychology', 
'Heal Delta' : 'Pharma Tech', 'Max NCU' : 'Computer Literacy', 'Nano Delta' : 'Pharma Tech', 'Nano Point Cost Modifier' : 'Quantum FT', 
'NF Interrupt' : 'Psychology', 'Nano Formula Interrupt Modifier' : 'Nanoprogramming', 'RangeInc. NF' : 'Nanoprogramming', 'RangeInc. Weapon' : 'Weaponsmithing', 'Shield Chemical AC' : 'Quantum FT', 
'Shield Cold AC' : 'Quantum FT', 'Shield Melee AC' : 'Quantum FT', 'Shield Poison AC' : 'Quantum FT', 'Shield Energy AC' : 'Quantum FT', 
'Shield Fire AC' : 'Quantum FT', 'Shield Projectile AC' : 'Quantum FT', 'Shield Radiation AC' : 'Quantum FT', 'Skill Time Lock Modifier' : 'Psychology'}

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

CLUSTER_SLOTS = {
    'Shiny' : 0,
    'Bright' : 1,
    'Faded' : 2
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

