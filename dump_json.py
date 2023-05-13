import xml.etree.ElementTree as ET
import argparse
import csv
import json
import os
import sys
import re

from tinkerplants.utils import *

CSV_FILE = 'symbiants.csv'

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

SPECIAL_ATTACKS = ['Brawl', 'Dimach', 'Fast Attack', 'Fling Shot', 'Burst', 'Full Auto', 'Sneak Attack', 'Aimed Shot']

SYMBIANT_IDS = [219135, 235792, 235825, 235826, 235827, 235842, 235586, 235711, 235612, 236297, 236312, 236313, 236250, 235487, 235625, 236117, 236118, 236119, 236136, 
236157, 235559, 235810, 235812, 235417, 235811, 235828, 235844, 235438, 235560, 235592, 235964, 235965, 235966, 235916, 235516, 236342, 236357, 236358, 236359, 236341, 
236048, 236113, 235450, 235638, 236047, 236065, 236049, 235726, 235414, 235892, 235893, 235909, 235604, 235911, 235415, 235605, 235910, 235911, 235927, 235928, 235929, 
235455, 235950, 235963, 236000, 235574, 235591, 235880, 235983, 235434, 235607, 235962, 235978, 235979, 235995, 235997, 235977, 235501, 235503, 235671, 236322, 236323, 
236324, 236325, 236340, 236196, 236194, 236209, 235654, 236195, 219130, 219132, 235449, 235621, 235719, 235720, 235734, 235735, 235752, 235555, 235641, 236114, 236113, 
236116, 236115, 236103, 235433, 235947, 235960, 235961, 235949, 235948, 235606, 235608, 236001, 236002, 236018, 236019, 236033, 235456, 235454, 235455, 235591, 235980, 
235913, 235914, 235931, 235981, 235982, 235430, 235872, 235873, 235891, 235907, 235499, 235856, 235741, 235839, 235906, 235871, 235924, 235428, 235820, 235445, 236044, 
235991, 235677, 235678, 236378, 236397, 236398, 235540, 236379, 236380, 235447, 235667, 235686, 235718, 219131, 235704, 235703, 235467, 235517, 235653, 236175, 236176, 
236178, 236192, 236193, 219137, 219136, 235439, 235644, 235662, 235630, 235577, 235727, 235759, 235761, 235595, 236162, 236182, 236217, 236233, 236234, 236243, 236259, 
236260, 236261, 236244, 235486, 235760, 219133, 235773, 235774, 235805, 235584, 235790, 235791, 235501, 235669, 236276, 236277, 236291, 236292, 236293, 236020, 236054, 
235593, 236053, 236037, 235629, 236399, 236364, 236382, 236381, 236383, 235465, 236131, 236132, 236133, 236134, 235744, 235435, 235996, 235997, 235998, 236015, 235622, 
235999, 235488, 235626, 236158, 236179, 236180, 236181, 236198, 235589, 235843, 235857, 235858, 235413, 235859, 235874, 235489, 235627, 236215, 236216, 236231, 236232, 
236245, 235933, 236055, 235985, 235541, 235504, 235643, 236245, 236246, 236247, 236248, 236265, 236266, 235689, 236428, 236445, 236446, 236447, 235520, 236448, 235466, 
236154, 236155, 236156, 236175, 235652, 236153, 235451, 236066, 236067, 236068, 236069, 235639, 236082, 235517, 236372, 236373, 236374, 236375, 235673, 235737, 235555, 
236485, 236499, 236500, 235691, 236501, 235692, 235679, 235623, 236030, 236031, 236017, 236032, 235484, 235655, 236210, 236211, 236212, 236213, 236099, 236100, 236102, 
235452, 236101, 235640, 235557, 235709, 235420, 235876, 235877, 235878, 235560, 235863, 235864, 235742, 235521, 235659, 236278, 236279, 236294, 236310, 236326, 236327, 
236344, 235658, 235518, 235687, 236392, 236393, 236411, 235695, 235490, 235506, 235677, 236328, 236344, 236345, 236362, 236107, 236249, 236346, 236379, 235419, 235524, 
235796, 235830, 235845, 235860, 235861, 235862, 235525, 235986, 235436, 236122, 236139, 236140, 235594, 236141, 235461, 235497, 235512, 235416, 235558, 235775, 235776, 
235777, 235793, 235794, 235736, 235463, 235769, 235771, 235409, 235753, 235770, 235410, 235464, 235786, 235804, 235787, 235772, 219140, 236502, 235710, 236470, 236486, 
236107, 236137, 235490, 235611, 236120, 236159, 236249, 235693, 236417, 236431, 236432, 236453, 235471, 236433, 219130, 235620, 235651, 235429, 235603, 235621, 235637, 
235556, 235690, 235692, 235539, 236466, 236467, 236468, 236469, 235690, 236484, 235522, 235659, 236310, 236327, 236343, 236361, 236377, 236395, 219134, 235585, 235806, 
235807, 235450, 235824, 235808, 235470, 235471, 235610, 236050, 236052, 236067, 236070, 236071, 236084, 236085, 236339, 236355, 235550, 236319, 236338, 235756, 235740, 
235755, 235722, 235571, 235587, 235738, 235535, 235705, 236463, 236464, 236465, 236480, 236481, 235757, 235573, 235724, 235694, 235469, 236034, 236003, 235609, 236051, 
236035, 236036, 235841, 235412, 235552, 235925, 235908, 235823, 236011, 236012, 236014, 236029, 235448, 235569, 235553, 235708, 235725, 235743, 235778, 235779, 235795, 
235796, 235418, 235507, 235829, 235537, 235707, 235590, 235879, 235895, 235912, 235913, 235930, 235437, 235538, 235675, 236430, 236452, 236449, 236450, 236451, 235523, 
235674, 236414, 236415, 236416, 236429, 236430, 235588, 235739, 235519, 235688, 236413, 236426, 236425, 236427, 236412, 235758, 235943, 235944, 235945, 235431, 235572, 
235723, 235896, 235915, 235472, 235575, 235897, 235881, 235501, 236307, 236308, 236309, 235502, 235670, 236306, 236321, 235505, 236216, 236280, 236295, 235676, 236267, 
236296, 235485, 236225, 236226, 236227, 236228, 236229, 235993, 235432, 235568, 235959, 235975, 236371, 236443, 236407, 235628, 236329, 236363, 236347, 236330, 236348, 
235570, 235721, 235500, 235668, 236261, 236262, 236263, 236275, 235707, 236483, 236498, 236497, 235706, 235542, 236199, 235469, 235471, 235624, 236086, 236087, 236104, 
236105, 236106, 235648, 236237, 236287, 235923, 235940, 235408, 235685, 235715, 235731, 219128, 235702, 236204, 236042, 236025, 235837, 236351, 236403, 236076, 236110, 
236422, 235564, 235714, 235816, 235919, 235920, 235938, 235733, 235936, 236058, 236144, 236237, 236301, 236421, 235887, 235767, 236110, 236352, 219126, 236388, 219127, 
235566, 235636, 236390, 236406, 235889, 235498, 236126, 236334, 235699, 236369, 236335, 235635, 236026, 235461, 236353, 236148, 236256, 236222, 235701, 235749, 236303, 
235480, 236149, 235548, 235600, 235496, 236302, 235956, 236095, 236188, 235458, 235802, 236337, 236203, 236318, 235650, 235546, 235800, 236075, 235615, 235903, 235783, 
235495, 235531, 235904, 235567, 236354, 236170, 236371, 235681, 236144, 236335, 235764, 235731, 236059, 235477, 236254, 235599, 235784, 236255, 236336, 235853, 235701, 
236206, 235617, 235618, 236061, 235513, 235636, 236352, 236007, 236094, 235955, 236370, 236128, 219128, 236459, 236041, 236184, 236185, 236219, 236298, 236282, 235660, 
236434, 236435, 236418, 236088, 236121, 235576, 236072, 236073, 236089, 235712, 236090, 236368, 235598, 235851, 236077, 235685, 235889, 235941, 235661, 236454, 236503, 
236504, 236471, 235411, 235821, 235483, 235840, 235854, 235855, 235822, 235407, 236454, 236486, 236471, 236503, 236418, 236504, 236383, 236400, 236365, 236488, 236401, 
236436, 236366, 236331, 236299, 236505, 236314, 236384, 236489, 236437, 236473, 236349, 236455, 236402, 236420, 219139, 235440, 235457, 235473, 235475, 235492, 235491, 
235509, 235526, 235527, 235544, 235562, 235577, 235578, 235579, 235596, 235613, 235614, 235561, 235474, 235422, 236330, 236348, 236472, 235849, 235865, 235866, 235882, 
235883, 235898, 235900, 235918, 235934, 235935, 235952, 235968, 235969, 235983, 235984, 235987, 236004, 236005, 236021, 236022, 236023, 236036, 236037, 236038, 236039, 
236057, 235696, 235663, 235631, 235646, 235680, 235727, 235728, 235762, 235763, 235781, 235797, 235798, 235814, 235815, 235831, 235833, 236074, 236123, 236124, 236142, 
236143, 236161, 236164, 236200, 236218, 236235, 236252, 236268, 236284, 235713, 235832, 219138, 235421, 235543, 236380, 235881, 236053, 235897, 235899, 235967, 235917, 
235951, 235901, 235780, 235745, 235746, 236281, 236163, 236251, 236183, 235508, 236040, 235729, 236487, 235932, 235645, 236091, 235847, 235444, 235865, 235831, 235846, 
235508, 235934, 235967]

def write_json(clusters, implants, nanos, weapons, symbiants, bosses, out_name):
    writeme = {'data' : {'clusters' : clusters, 'implants' : implants, 'nanos' : nanos, 'weapons' : weapons, 'symbiants' : symbiants, 'bosses' : bosses}}

    with open(out_name, 'w') as fd:
        fd.write(json.dumps(writeme))

def parse_xml(in_name):
    tree = ET.parse(in_name)

    root = tree.getroot()

    implants = {}
    clusters = {}
    crystals = {}
    weapons = {}
    symbiants = {}

    symb_count = 0

    for item in root.findall('item'):
        name = item.find('name').text
        if name is None:
            continue
        aoid = int(item.get('aoid'))
        if aoid is None:
            continue
        item_type = int(item.find('type').text)
        icon = int(item.find('icon').text)

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

        elif aoid in SYMBIANT_IDS or (item_type == 3 and 'Xan' in name and ('Alpha' in name or 'Beta' in name)) or (item_type == 3 and 'Intelligent' in name): # Item is a symbiant
            ql = int(item.find('ql').text)

            symbiants[aoid] = {}
            symbiants[aoid]['name'] = name
            symbiants[aoid]['ql'] = ql

            slot = item.find('slots').text
            if slot == 'Body':
                symbiants[aoid]['slot'] = 'Chest'
            else:
                symbiants[aoid]['slot'] = slot

            tokens = name.split(',')
            tokens = tokens[1].split()
            symbiants[aoid]['family'] = tokens[0].strip()

            reqs = item.find('requirements')
            symbiants[aoid]['reqs'] = {}
            if reqs is not None:
                profs = []
                for child in reqs:
                    attrib = child.get('attribute')
                    if attrib == 'Profession' or attrib == 'Visual profession':
                        profs.append(int(child.get('value')))
                    elif attrib == 'Expansion sets':
                        symbiants[aoid]['reqs']['Expansion_sets'] = int(child.get('value'))
                    else:
                        symbiants[aoid]['reqs'][attrib] = int(child.get('value'))

                symbiants[aoid]['reqs']['Profession'] = profs

            effects = item.find('effects')
            symbiants[aoid]['effects'] = {}
            if effects is not None:
                for child in effects:
                    attrib = child.get('attribute')
                    if attrib == 'Item':
                        continue
                    elif 'Nano strain' in attrib:
                        val = child.get('value')
                        val = re.sub('%', '', val)
                        symbiants[aoid]['effects'][attrib] = int(val)
                    else:
                        symbiants[aoid]['effects'][attrib] = int(child.get('value'))
                    

        elif item_type == 0 and ('Crystal' in name or 'Nano Cube' in name) and not 'Supercharged' in name: # Item is a nano crystal, grab the QL
            ql = int(item.find('ql').text)

            requires = item.find('requirements')

            # if 'Izgimmer\'s Cataclysm' in name:
            #     breakpoint()

            if requires is not None:
                for req in requires:
                    attrib = req.get('attribute')
                    value = req.get('value')
                    if attrib == 'Visual profession' or attrib == 'Profession':
                        if value == '11':
                            effects = item.find('effects')
                            for eff in effects:
                                if eff.get('action') == 'Upload':
                                    val = eff.get('value')
                                    crystals[val] = ql

        elif item.find('skillmap') is not None and icon != 0: # Item is a weapon
            # if int(item.get('aoid')) == 211404: breakpoint()
            damage = item.find('damage')
            if damage is None:
                continue
            if int(damage.get('maximum')) <= 1: # filter out social items
                continue

            if 'Otek ' in name: # not in game
                continue

            try:
                if aoid in [302624, 304910]:
                    continue
                
                if not weapons.get(aoid):
                    weapons[aoid] = {'name' : name}

                ql = int(item.find('ql').text)
                weapons[aoid]['ql'] = ql

                times = item.find('times')
                weapons[aoid]['times'] = {
                    'attack' : int(times.get('attack')),
                    'recharge' : int(times.get('recharge'))
                }

                weapons[aoid]['damage'] = {
                    'minimum' : int(damage.get('minimum')),
                    'maximum' : int(damage.get('maximum')),
                    'critical' : int(damage.get('critical')),
                    'type' : int(damage.get('type'))
                }

                ammo = item.find('ammo')
                if ammo is not None:
                    weapons[aoid]['clipsize'] = int(ammo.get('clipsize'))
                else:
                    weapons[aoid]['clipsize'] = -1

                bitfields = item.findall('bitfield')
                for bitfield in bitfields:
                    if bitfield.get('type') == 'props':
                        props = bitfield.text
                        prop_items = props.split(',')
                        weapons[aoid]['props'] = [x.strip() for x in prop_items if x.strip() in SPECIAL_ATTACKS]

                reqs = item.find('requirements')
                weapons[aoid]['reqs'] = {}
                if reqs is not None:
                    profs = []
                    breeds = []
                    for child in reqs:
                        attrib = child.get('attribute')
                        if attrib == 'Profession' or attrib == 'Visual profession':
                            profs.append(int(child.get('value')))
                        elif attrib == 'Breed':
                            breeds.append(int(child.get('value')))
                        else:
                            weapons[aoid]['reqs'][attrib] = int(child.get('value'))

                    weapons[aoid]['reqs']['Profession'] = profs
                    weapons[aoid]['reqs']['Breed'] = breeds

                    # Set reqs for brawl
                    if aoid == 70292:
                        weapons[aoid]['reqs']['Brawl'] = 1
                    if aoid == 70293:
                        weapons[aoid]['reqs']['Brawl'] = 1000
                    if aoid == 211401:
                        weapons[aoid]['reqs']['Brawl'] = 1001
                    if aoid == 211402:
                        weapons[aoid]['reqs']['Brawl'] = 2000
                    if aoid == 211403:
                        weapons[aoid]['reqs']['Brawl'] = 2001
                    if aoid == 211404:
                        weapons[aoid]['reqs']['Brawl'] = 3000

                else: 
                    # add proper reqs to MA items
                    if aoid in [211352, 211353, 211354, 211357, 211358, 211363, 211364]: # Martial Artist
                        weapons[aoid]['reqs']['Profession'] = [2]
                    elif aoid in [211349, 211350, 211351, 211359, 211360, 211365, 211366]: # Shade
                        weapons[aoid]['reqs']['Profession'] = [15]
                    elif aoid in [43712, 144745,  43713, 211355, 211356, 211361, 211362]: # Other
                        weapons[aoid]['reqs']['Profession'] = [1, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]

                    if aoid in [211349, 211352, 43712]:
                        weapons[aoid]['reqs']['Martial arts'] = 1
                    elif aoid in [211353, 211350, 144745]:
                        weapons[aoid]['reqs']['Martial arts'] = 200
                    elif aoid in [211354, 211351, 43713]:
                        weapons[aoid]['reqs']['Martial arts'] = 1000
                    elif aoid in [211357, 211359, 211355]:
                        weapons[aoid]['reqs']['Martial arts'] = 1001
                    elif aoid in [211358, 211360, 211356]:
                        weapons[aoid]['reqs']['Martial arts'] = 2000
                    elif aoid in [211363, 211365, 211361]:
                        weapons[aoid]['reqs']['Martial arts'] = 2001
                    elif aoid in [211364, 211366, 211362]:
                        weapons[aoid]['reqs']['Martial arts'] = 3000

                skillmaps = item.findall('skillmap')
                if skillmaps is not None:
                    for map in skillmaps:
                        if map.get('type') == 'attack':
                            weapons[aoid]['attack_skills'] = {}
                            for child in map:
                                weapons[aoid]['attack_skills'][child.get('name')] = int(child.get('percentage'))

                other = item.find('other')
                weapons[aoid]['other'] = {}
                if other is not None:
                    for child in other:
                        key = child.get('key')
                        weapons[aoid]['other'][key] = int(child.get('value'))

            except (AttributeError, TypeError):
                print('Weapon error ({}), moving on'.format(name))

    print(symb_count)
                
    return implants, clusters, crystals, weapons, symbiants

def parse_nanos(in_name, crystals):
    tree = ET.parse(in_name)

    root = tree.getroot()

    nanos = {}

    for item in root.findall('item'):
        aoid = item.get('aoid')
        nano = {}
        nano['name'] = item.find('name').text

        nt_nano = False

        nanoclass = item.find('nanoclass')
        if nanoclass is None:
            continue
        if nanoclass.get('school') != 'Combat':
            continue

        requires = item.find('requirements')
        if requires is not None:
            for req in requires:
                attrib = req.get('attribute')
                if attrib == 'Profession' or attrib == 'Visual profession':
                    if req.get('value') == '11':
                        nt_nano = True
                        try:
                            nano['ql'] = crystals[aoid]
                        except:
                            if 'Izgimmer\'s Cataclysm' in nano['name']:
                                nano['ql'] = 219
                            elif 'Garuk\'s Improved Viral Assault' in nano['name']:
                                nano['ql'] = 215
                            else:
                                breakpoint()

                elif attrib == 'Level':
                    nano['level_req'] = int(req.get('value'))
                
                elif attrib == 'Matter creation':
                    nano['mc'] = int(req.get('value'))

                elif attrib == 'Specialization':
                    nano['spec'] = int(req.get('value'))

                elif attrib == 'Cyberdeck':
                    nano['deck'] = int(req.get('value'))

        times = item.find('times')
        nano['attack'] = int(times.get('attack'))
        nano['recharge'] = int(times.get('recharge'))
        nano['cost'] = int(item.find('nanodata').get('nanocost'))

        effects = item.find('effects')
        if effects is not None:
            for eff in effects:
                if eff.find('requirements') is None and eff.get('action') == 'Hit':
                    vals = eff.get('value').split()
                    if len(vals) >= 4:
                        nano['low_dmg'] = abs(int(vals[0]))
                        nano['high_dmg'] = abs(int(vals[2]))
                        nano['ac'] = vals[3]

                    if eff.get('hits') is not None:
                        hits = int(eff.get('hits'))
                        nano['dot_hits'] = hits
                        if hits > 1:
                            nano['nt_dot'] = True

                    if eff.get('delay') is not None:
                        nano['dot_delay'] = int(eff.get('delay'))

        if nano.get('low_dmg') is None: # not a nuke, skip it
            nt_nano = False
            continue

        skillmaps = item.findall('skillmap')
        for sm in skillmaps:
            if sm.get('type') == 'defense':
                nano['nr_pct'] = int(sm.find('skill').get('percentage'))

        other = item.find('other')
        if other is not None:
            for attrib in other:
                if attrib.get('key') == 'Attack time cap':
                    nano['atk_cap'] = int(attrib.get('value'))
                if attrib.get('key') == '643': # School cooldown
                    nano['strain_cd'] = int(attrib.get('value'))

        if nt_nano:
            nanos[aoid] = nano

    return nanos

def parse_pocketbosses(pbcsv):
    pocketbosses = {}

    with open(pbcsv) as fp:

        reader = csv.reader(fp, delimiter=';')
        for line in reader:
            name = line[3]
            if pocketbosses.get(name) is None:
                pocketbosses[name] = {}
            
            pocketbosses[name]['level'] = int(line[7])
            pocketbosses[name]['playfield'] = line[4]
            pocketbosses[name]['location'] = line[5]
            pocketbosses[name]['mobs'] = line[6]

            if pocketbosses[name].get('drops') is None:
                pocketbosses[name]['drops'] = []

            url = line[10]
            tokens = url.split('>')
            aoid = int(tokens[0][-6:])
            pocketbosses[name]['drops'].append(aoid)

    return pocketbosses

def remove_old(out_name):
    if os.path.exists(out_name):
        os.remove(out_name)

if __name__ == '__main__':
    parser = argparse.ArgumentParser('dump_json.py -i <items input> -n <nano input> -o <json output>\n')
    parser.add_argument('-i', '--items', type=str, required=True)
    parser.add_argument('-n', '--nanos', type=str, required=True)
    parser.add_argument('-o', '--output', type=str, required=True)
    args = parser.parse_args()

    if not os.path.exists(args.items):
        print('Items file does not exist!')
        sys.exit(1)

    if not os.path.exists(args.nanos):
        print('Nanos file does not exist!')
        sys.exit(1)

    else:
        remove_old(args.output)
        implants, clusters, crystals, weapons, symbiants = parse_xml(args.items)
        nanos = parse_nanos(args.nanos, crystals)
        bosses = parse_pocketbosses(CSV_FILE)
        write_json(clusters, implants, nanos, weapons, symbiants, bosses, args.output)


