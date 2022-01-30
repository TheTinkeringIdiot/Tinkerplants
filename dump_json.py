import xml.etree.ElementTree as ET
import argparse
import json
import os
import sys

from tinkerplants.utils import *

NANODELTA_JOBE_MOD = {'Shiny' : 5.25, 'Bright' : 4.0, 'Faded' : 2.75}

SKILL_NAMES = {
 '' : 'Nano Delta',
 '1 Hand Blunt Weapons' : '1h Blunt',
 '1 Hand Edged Weapons' : '1h Edged Weapon',
 '2 Handed Blunt Weapons' : '2h Blunt',
 '2 Handed Edged Weapons' : '2h Edged',
 'Adventuring' : 'Adventuring',
 'Agility' : 'Agility',
 'Aimed Shot' : 'Aimed Shot',
 'Assault Rifle' : 'Assault Rif',
 'Biological Metamorphoses' : 'Bio.Metamor',
 'Body Development' : 'Body Dev',
 'BodyDevelopment' : 'Body Dev',
 'Bow' : 'Bow',
 'Bow Special Attack' : 'Bow Spc Att',
 'Brawling' : 'Brawling',
 'Breaking and Entering' : 'Break & Entry',
 'Burst' : 'Burst',
 'Chemical Armor-Class' : 'Chemical AC',
 'Chemistry' : 'Chemistry',
 'Cold Armor-Class' : 'Cold AC',
 'Computer Literacy' : 'Comp. Liter',
 'Concealment' : 'Concealment',
 'Dimach (Soul Attack)' : 'Dimach',
 'Disease and Poison Armor-Class' : 'Disease AC',
 'Dodge' : 'Dodge-Rng',
 'Dodge Ranged Attacks' : 'Dodge-Rng',
 'Duck Explosions and Thrown Objects' : 'Duck-Exp',
 'Electrical Engineering' : 'Elec. Engi',
 'Empty' : 'Empty',
 'Energy Attack Armor-Class' : 'Energy AC',
 'Evade' : 'Evade-ClsC',
 'Evade Close Combat and Martial Art Attacks' : 'Evade-ClsC',
 'Fast Attack' : 'Fast Attack',
 'Fire Armor-Class' : 'Fire AC',
 'First Aid' : 'First Aid',
 'Fling Shot' : 'Fling Shot',
 'Full Auto' : 'Full Auto',
 'Grenade or Lumping Throwing' : 'Grenade',
 'Health Regeneration Add' : 'Heal Delta',
 'Impact and Projectile Weapon Armor-Class' : 'Imp/Proj AC',
 'Intelligence' : 'Intelligence',
 'Knife or Sharp Obj Throwing' : 'Sharp Obj',
 'Knife or Sharp Object Throwing' : 'Sharp Obj',
 'Life' : 'Max Health',
 'Machine Guns (MG) and Sub Machine Guns (SMG)' : 'MG / SMG',
 'Map Navigation' : 'Map Navig',
 'Martial Arts' : 'Martial Arts',
 'Matter Creations' : 'Matter Crea',
 'Matter Metamorphoses' : 'Matt.Metam',
 'Max Nano' : 'Max Nano',
 'Mechanical Enginering' : 'Mech. Engi',
 'Melee Attacks and Martial Art Armor-Class' : 'Melee/Ma AC',
 'Melee Energy Weapons' : 'Melee Ener',
 'Melee Init.' : 'Melee Init',
 'Melee Weapons Initiative' : 'Melee. Init',
 'Multiple Melee Weapons' : 'Mult. Melee',
 'Multiple Ranged Weapons' : 'Multi Ranged',
 'NCU Count' : 'Max NCU',
 'Nano Energy Pool' : 'Nano Pool',
 'Nano Execution Cost Percentage Change' : 'Nano Point Cost Modifier',
 'Nano Execution Init' : 'NanoC. Init',
 'Nano Resistance' : 'Nano Resist',
 'Nano-Bot Programming' : 'Nano Progra',
 'Operate Heavy Machinery' : 'Heavy Weapons',
 'Parry' : 'Parry',
 'Percentage Added to all Defencive Rolls' : 'Add All Def.',
 'Percentage Added to all Offensive Rolls' : 'Add All Off',
 'Percentage Additional Experience' : 'Add. Xp',
 'Percentage Change in Skill Timer Lock' : 'Skill Time Lock Modifier',
 'Percentage Change in chance of being interrupted while Executing Nanos' : 'Nano Formula Interrupt Modifier',
 'Perception and spotting' : 'Perception',
 'Pharmacological Technology' : 'Pharma Tech',
 'Physical Prowess and Martial Arts Initiative' : 'Physic. Init',
 'Piercing Weapons' : 'Piercing',
 'Pistol' : 'Pistol',
 'Points Added to Chemical Damage' : 'Add. Chem. Dam.',
 'Points Added to Energy Damage' : 'Add. Energy Dam.',
 'Points Added to Fire Damage' : 'Add. Fire Dam.',
 'Points Added to Melee Damage' : 'Add. Melee Dam.',
 'Points Added to Poison Damage' : 'Add. Poison Dam.',
 'Points Added to Projectile Damage' : 'Add. Proj. Dam.',
 'Points Added to Radiation Damage' : 'Add.Rad. Dam.',
 'Psychic' : 'Psychic',
 'Psychological Modifications' : 'Psycho Modi',
 'Psychology' : 'Psychology',
 'Quantum Force field Technology' : 'Quantum FT',
 'Radiation Armor-Class' : 'Radiation AC',
 'Range Increaser Nano Formula' : 'RangeInc. NF',
 'Range Increaser Weapon' : 'RangeInc. Weapon',
 'Ranged Energy Weapons' : 'Ranged Ener',
 'Ranged Weapons Initiative' : 'Ranged. Init',
 'Rifle and Sniper-Rifle' : 'Rifle',
 'Riposte' : 'Riposte',
 'Run Speed' : 'Run Speed',
 'RunSpeed' : 'Run Speed',
 'Sense' : 'Sense',
 'Sensory Improvement and Modification' : 'Sensory Impr',
 'Shield Chemical AC' : 'Shield Chemical AC',
 'Shield Cold AC' : 'Shield Cold AC',
 'Shield Energy AC' : 'Shield Energy AC',
 'Shield Fire AC' : 'Shield Fire AC',
 'Shield Melee AC' : 'Shield Melee AC',
 'Shield Poison AC' : 'Shield Poison AC',
 'Shield Projectile AC' : 'Shield Projectile AC',
 'Shield Radiation AC' : 'Shield Radiation AC',
 'Shotgun' : 'Shotgun',
 'Sneak Attack' : 'Sneak Atck',
 'Stamina' : 'Stamina',
 'Strength' : 'Strength',
 'Swimming' : 'Swimming',
 'Time and Space Alteration' : 'Time & Space',
 'Trap Disarmament' : 'Trap Disarm',
 'Treatment' : 'Treatment',
 'Tutoring' : 'Tutoring',
 'Vehicle Navigation, Airborne' : 'Vehicle Air',
 'Vehicle Navigation, Ground' : 'Vehicle Grnd',
 'Vehicle Navigation, Waterbased' : 'Vehicle Hydr',
 'Weapon Smithing' : 'Weapon Smt',
 'life' : 'Max Health',
}

def write_json(clusters, implants, out_name):
    writeme = {'data' : {'clusters' : clusters, 'implants' : implants}}

    with open(out_name, 'w') as fd:
        fd.write(json.dumps(writeme))

def parse_xml(in_name, out_name):
    tree = ET.parse(in_name)

    root = tree.getroot()

    implants = {}
    clusters = {}

    for item in root.findall('item'):
        name = item.find('name').text
        if name is None:
            continue
        item_type = int(item.find('type').text)

        if item_type == 0 and 'Cluster' in name: # Item is a cluster, store it
            idx = name.find(' - ')
            if idx <= 0:
                print('Invalid cluster, moving on')
                continue
            slots = name[idx+3:].strip().split()
            if len(slots) < 2:
                print('Malformed cluster name, moving on')
                continue
            clusterslot = slots[0]
            impslot = IMP_SLOT_INDEX.get(slots[1].strip('()'))

            ql = int(item.find('ql').text)

            if 'Refined' in name:
                idx = name.find('Refined')
                skill = name[:idx].strip().strip('% ')
            elif 'Jobe' in name:
                idx = name.find('Jobe')
                skill = name[:idx].strip().strip('% ') # plays hell with the database
            elif 'Cluster' in name:
                idx = name.find('Cluster')
                skill = name[:idx].strip()

            if not clusters.get(skill):
                clusters[skill] = {}

            if ql == 1 or ql == 200:
                qltype = 'normal'
            elif ql == 201 or ql == 300:
                qltype = 'refined'

            if not clusters[skill].get(qltype):
                clusters[skill][qltype] = {}

            if not clusters[skill][qltype].get(clusterslot):
                clusters[skill][qltype][clusterslot] = {}

            clusters[skill][qltype][clusterslot]['impslot'] = impslot

            effects = item.find('effects')
            if effects is None: # fix up some breaks in the data dump
                print('{} is broken, making a guess'.format(name))
                if ql == 201:
                    if clusterslot == 'Faded':
                        value = 42
                    elif clusterslot == 'Bright':
                        value = 63
                    elif clusterslot == 'Shiny':
                        value = 106
                elif ql == 300:
                    if clusterslot == 'Faded':
                        value = 57
                    elif clusterslot == 'Bright':
                        value = 85
                    elif clusterslot == 'Shiny':
                        value = 141
            else:
                for child in effects:
                    value = child.get('value')

            if ql == 1 or ql == 201:
                clusters[skill][qltype][clusterslot]['loval'] = int(value)
            elif ql == 200 or ql == 300:
                clusters[skill][qltype][clusterslot]['hival'] = int(value)


            jobeskill = JOBE_SKILL.get(skill, '')
            npmod = NP_MODS.get(skill, 0.0)
            if 'Jobe' in name and not 'Nano Delta' in name:
                jobemod = JOBE_MODS.get(clusterslot, 0.0)
            elif 'Jobe' in name and 'Nano Delta' in name:
                jobemod = NANODELTA_JOBE_MOD.get(clusterslot, 0.0)
            else:
                jobemod = 0.0

            clusters[skill]['npmod'] = npmod
            clusters[skill]['jobeskill'] = jobeskill
            clusters[skill][qltype][clusterslot]['jobemod'] = jobemod

        elif item_type == 3 and 'Implant' in name: # Item is an implant, store it
            ql = int(item.find('ql').text)
            
            # combine the low and high ql versions of each implant
            if ql != 200 and ql != 300:
                aoid = int(item.get('aoid'))
            else:
                aoid = int(item.get('aoid')) - 1

            if not implants.get(aoid):
                implants[aoid] = {}

            implants[aoid]['name'] = name

            if ql > 200:
                implants[aoid]['refined'] = True
            else:
                implants[aoid]['refined'] = False
                
            slot = IMP_SLOT_INDEX.get(item.find('slots').text)
            if slot is None: # skip some implants which don't have a single slot
                continue
            icon = item.find('icon').text

            implants[aoid]['slot'] = slot
            implants[aoid]['icon'] = icon

            if not implants[aoid].get('reqs'):
                implants[aoid]['reqs'] = {}

            requires = item.find('requirements')

            if requires is not None:
                for req in requires:
                    attrib = req.get('attribute')
                    if not implants[aoid]['reqs'].get(attrib):
                        implants[aoid]['reqs'][attrib] = {}
                    if ql == 1 or ql == 201:
                        implants[aoid]['reqs'][attrib]['loval'] = int(req.get('value'))
                    elif ql == 200 or ql == 300:
                        implants[aoid]['reqs'][attrib]['hival'] = int(req.get('value'))

            installed = item.find('description').text.split('\n')
            try:
                implants[aoid]['faded'] = SKILL_NAMES[installed[1].split(':')[1].strip()]
                implants[aoid]['bright'] = SKILL_NAMES[installed[2].split(':')[1].strip()]
                implants[aoid]['shiny'] = SKILL_NAMES[installed[3].split(':')[1].strip()]
            except:
                pass

    return implants, clusters

def remove_old(out_name):
    if os.path.exists(out_name):
        os.remove(out_name)

if __name__ == '__main__':
    parser = argparse.ArgumentParser('dump_json.py -f <xml input> -o <json output>\n')
    parser.add_argument('-f', '--file', type=str, required=True)
    parser.add_argument('-o', '--output', type=str, required=True)
    args = parser.parse_args()

    if not os.path.exists(args.file):
        print('Input file does not exist!')
        sys.exit(1)

    else:
        remove_old(args.output)
        implants, clusters = parse_xml(args.file, args.output)
        write_json(clusters, implants, args.output)


