import requests, json, time
from bs4 import BeautifulSoup

# Create your tests here.
IMP_TESTS = {
    'Eye' : {
        'Shiny' : [
            'Empty',
            'Aimed Shot',
            'Elec. Engi',
            'Map Navig',
            'RangeInc. Weapon',
            'Rifle',
            'Tutoring',
            'Vehicle Air',

        ], 
        'Bright' : [
            'Empty',
            'Chemistry',
            'Comp. Liter',
            'Grenade',
            'Heavy Weapons',
            'Intelligence',
            'Mech. Engi',
            'Mult. Melee',
            'Nano Progra',
            'NanoC. Init',
            'Perception',
            'Pharma Tech',
            'Psycho Modi',
            'Quantum FT',
            'Ranged Ener',
            'Sensory Impr',
            'Treatment',
            'Vehicle Grnd',
            'Vehicle Hydr',
        ],
        'Faded' : [
            'Empty',
            'Assault Rif',
            'Bow',
            'Concealment',
            'Matter Crea',
            'Multi Ranged',
            'Pistol',
            'Psychology',
            'Sharp Obj',
            'Sneak Atck',
            'Time & Space',
            'Weapon Smt',
        ]
    },
    'Head' : {
        'Shiny' : [
            'Empty',
            'Bio.Metamor',
            'Bow Spc Att',
            'Chemistry',
            'Comp. Liter',
            'Disease AC',
            'First Aid',
            'Intelligence',
            'Matt.Metam',
            'Matter Crea',
            'Max Nano',
            'Mech. Engi',
            'Melee Ener',
            'Nano Progra',
            'Nano Resist',
            'NanoC. Init',
            'Pharma Tech',
            'Psychic',
            'Psycho Modi',
            'Psychology',
            'Quantum FT',
            'Ranged Ener',
            'Sensory Impr',
            'Time & Space',
            'Treatment',
            'Vehicle Grnd',
            'Vehicle Hydr',
        ], 
        'Bright' : [
            'Empty',
            'Dimach',
            'Elec. Engi',
            'Map Navig',
            'Nano Pool',
            'Ranged. Init',
            'Weapon Smt',
        ],
        'Faded' : [
            'Empty',
            'Perception',
            'Sense',
            'Trap Disarm',
            'Tutoring',
            'Vehicle Air',
        ]
    },
    'Ear' : {
        'Shiny' : [
            'Empty',
            'Add. Xp',
            'Max NCU',
            'Perception',
        ], 
        'Bright' : [
            'Empty',
            'Concealment',
            'Nano Point Cost Modifier',
            'Psychology',
            'Tutoring',
            'Vehicle Air',
        ],
        'Faded' : [
            'Empty',
            'Intelligence',
            'Map Navig',
            'Psychic',
            'Psycho Modi',
            'Vehicle Grnd',
            'Vehicle Hydr',
        ]
    },
    'Right-Arm' : {
        'Shiny' : [
            'Empty',
            '1h Blunt',
            '1h Edged Weapon',
            '2h Blunt',
            '2h Edged',
            'Assault Rif',
            'Bow',
            'Break & Entry',
            'Burst',
            'Fling Shot',
            'Full Auto',
            'Grenade',
            'Heavy Weapons',
            'MG / SMG',
            'Piercing',
            'Shotgun',
            'Strength',
        ], 
        'Bright' : [
            'Empty',
            'Add All Def.',
            'Add All Off',
            'Brawling',
            'Chemical AC',
            'Nano Delta',
            'Physic. Init',
            'Swimming',
        ],
        'Faded' : [
            'Empty',
            'Fast Attack',
            'Mech. Engi',
            'Parry',
            'Radiation AC',
            'RangeInc. NF',
            'RangeInc. Weapon',
            'Riposte',
        ]
    },
    'Chest' : {
        'Shiny' : [
            'Empty',
            'Body Dev',
            'Dimach',
            'Energy AC',
            'Max Health',
            'Melee/Ma AC',
            'Nano Pool',
            'Sense',
            'Stamina',
        ], 
        'Bright' : [
            'Empty',
            'Bio.Metamor',
            'Imp/Proj AC',
            'Matt.Metam',
            'Psychic',
        ],
        'Faded' : [
            'Empty',
            '2h Blunt',
            'Adventuring',
            'Break & Entry',
            'Disease AC',
            'MG / SMG',
            'Max Nano',
            'Nano Formula Interrupt Modifier',
            'NanoC. Init',
            'Sensory Impr',
            'Skill Time Lock Modifier',
            'Strength',
        ]
    },
    'Left-Arm' : {
        'Shiny' : [
            'Empty',
            'Add All Def.',
            'Add All Off',
            'Brawling',
            'Heal Delta',
            'RangeInc. NF',
        ], 
        'Bright' : [
            'Empty',
            '2h Blunt',
            '2h Edged',
            'Bow',
            'Break & Entry',
            'Piercing',
            'Radiation AC',
            'Strength',
        ],
        'Faded' : [
            'Empty',
            'Chemical AC',
            'Matt.Metam',
            'Nano Point Cost Modifier',
            'Physic. Init',
            'Swimming',
        ]
    },
    'Right-Wrist' : {
        'Shiny' : [
            'Empty',
            'Nano Delta',
            'Parry',
            'Pistol',
            'Ranged. Init',
            'Riposte',
            'Run Speed',
            'Sharp Obj',
        ], 
        'Bright' : [
            'Empty',
            '1h Blunt',
            '1h Edged Weapon',
            'Aimed Shot',
            'Burst',
            'Full Auto',
            'Max NCU',
            'Multi Ranged',
            'Nano Resist',
            'Rifle',
            'Sneak Atck',
        ],
        'Faded' : [
            'Empty',
            'Add. Chem. Dam.',
            'Add. Energy Dam.',
            'Add. Fire Dam.',
            'Add. Melee Dam.',
            'Add. Poison Dam.',
            'Add. Proj. Dam.',
            'Add.Rad. Dam.',
            'Bow Spc Att',
            'Fling Shot',
            'Melee Ener',
            'Mult. Melee',
        ]
    },
    'Waist' : {
        'Shiny' : [
            'Empty',
            'Chemical AC',
            'Cold AC',
            'Fire AC',
            'Nano Point Cost Modifier',
            'Radiation AC',
        ], 
        'Bright' : [
            'Empty',
            'Adventuring',
            'Body Dev',
            'Duck-Exp',
            'Max Health',
            'Max Nano',
            'Melee/Ma AC',
            'Sense',
        ],
        'Faded' : [
            'Empty',
            '2h Edged',
            'Agility',
            'Bio.Metamor',
            'Brawling',
            'Dimach',
            'Dodge-Rng',
            'Energy AC',
            'Evade-ClsC',
            'Full Auto',
            'Imp/Proj AC',
            'Melee. Init',
            'Nano Pool',
            'Piercing',
            'Shotgun',
            'Stamina',
        ]
    },
    'Left-Wrist' : {
        'Shiny' : [
            'Empty',
            'Mult. Melee',
            'Multi Ranged',
            'Shield Energy AC',
            'Shield Fire AC',
            'Shield Projectile AC',
            'Shield Radiation AC',
        ], 
        'Bright' : [
            'Empty',
            'Add. Chem. Dam.',
            'Add. Energy Dam.',
            'Add. Fire Dam.',
            'Add. Melee Dam.',
            'Add. Poison Dam.',
            'Add. Proj. Dam.',
            'Add.Rad. Dam.',
            'Melee Ener',
            'Parry',
            'Riposte',
            'Run Speed',
        ],
        'Faded' : [
            'Empty',
            'Nano Resist',
            'Rifle',
            'Shield Chemical AC',
            'Shield Cold AC',
            'Shield Melee AC',
            'Shield Poison AC',
        ]
    },
    'Right-Hand' : {
        'Shiny' : [
            'Empty',
            'Add. Chem. Dam.',
            'Add. Energy Dam.',
            'Add. Fire Dam.',
            'Add. Melee Dam.',
            'Add. Poison Dam.',
            'Add. Proj. Dam.',
            'Add.Rad. Dam.',
            'Martial Arts',
            'Trap Disarm',
            'Weapon Smt',
        ], 
        'Bright' : [
            'Empty',
            'Assault Rif',
            'Bow Spc Att',
            'Cold AC',
            'Fast Attack',
            'First Aid',
            'Fling Shot',
            'MG / SMG',
            'Matter Crea',
            'Pistol',
            'Sharp Obj',
            'Shotgun',
            'Time & Space',
        ],
        'Faded' : [
            'Empty',
            '1h Blunt',
            '1h Edged Weapon',
            'Aimed Shot',
            'Burst',
            'Chemistry',
            'Comp. Liter',
            'Elec. Engi',
            'Fire AC',
            'Grenade',
            'Heavy Weapons',
            'Nano Progra',
            'Pharma Tech',
            'Quantum FT',
            'Ranged. Init',
            'Treatment',
        ]
    },
    'Leg' : {
        'Shiny' : [
            'Empty',
            'Adventuring',
            'Agility',
            'Dodge-Rng',
            'Duck-Exp',
            'Imp/Proj AC',
            'Nano Formula Interrupt Modifier',
            'Skill Time Lock Modifier',
            'Swimming',
        ], 
        'Bright' : [
            'Empty',
            'Disease AC',
            'Energy AC',
            'Evade-ClsC',
            'Melee. Init',
            'Stamina',
        ],
        'Faded' : [
            'Empty',
            'Add. Xp',
            'Body Dev',
            'Heal Delta',
            'Max Health',
            'Max NCU',
            'Melee/Ma AC',
            'Run Speed',
            'Shield Energy AC',
            'Shield Fire AC',
            'Shield Projectile AC',
            'Shield Radiation AC',
        ]
    },
    'Left-Hand' : {
        'Shiny' : [
            'Empty',
            'Fast Attack',
            'Shield Chemical AC',
            'Shield Cold AC',
            'Shield Melee AC',
            'Shield Poison AC',
        ], 
        'Bright' : [
            'Empty',
            'Fire AC',
            'Nano Formula Interrupt Modifier',
            'RangeInc. NF',
            'Shield Energy AC',
            'Shield Fire AC',
            'Shield Projectile AC',
            'Shield Radiation AC',
            'Skill Time Lock Modifier',
            'Trap Disarm',
        ],
        'Faded' : [
            'Empty',
            'Cold AC',
            'First Aid',
            'Martial Arts',
            'Ranged Ener',
        ]
    },
    'Feet' : {
        'Shiny' : [
            'Empty',
            'Concealment',
            'Evade-ClsC',
            'Melee. Init',
            'Physic. Init',
            'Sneak Atck',
        ], 
        'Bright' : [
            'Empty',
            'Add. Xp',
            'Agility',
            'Dodge-Rng',
            'Heal Delta',
            'Martial Arts',
            'RangeInc. Weapon',
            'Shield Chemical AC',
            'Shield Cold AC',
            'Shield Melee AC',
            'Shield Poison AC',
        ],
        'Faded' : [
            'Empty',
            'Add All Def.',
            'Add All Off',
            'Duck-Exp',
            'Nano Delta',
        ]
    },
}


def test_implants():
    s = requests.Session()
    response = s.get('http://127.0.0.1:8000/tinkerplants/')
    soup = BeautifulSoup(response.content, 'html.parser')
    element = soup.find('input')
    if element['name'] == 'csrfmiddlewaretoken':
        token = element['value']
        s.headers.update({'X-CSRFToken' : token})

    for imp_slot, clusters in IMP_TESTS.items():
        for shiny_skill in clusters['Shiny']:
            send_update(s, imp_slot, 'Shiny', shiny_skill)

            for bright_skill in clusters['Bright']:
                send_update(s, imp_slot, 'Bright', bright_skill)

                for faded_skill in clusters['Faded']:
                    send_update(s, imp_slot, 'Faded', faded_skill)

        # for cluster_slot, skill_list in clusters.items():
        #     for skill in skill_list:
        #         imp = '{}-{}'.format(imp_slot, cluster_slot)
        #         #print('{}: {}'.format(imp, skill))
        #         s.headers.update({'Content-Type' : 'application/json'})
        #         response = s.post(url='http://127.0.0.1:8000/tinkerplants/update_imps', json={'slot' : imp, 'value' : skill})
        #         resp = response.json()
        #         assert resp['success']
        #         print('{}: {} {} {}'.format(imp_slot, resp['implants'][imp_slot]['Shiny'], resp['implants'][imp_slot]['Bright'], resp['implants'][imp_slot]['Faded']))

def send_update(s, imp_slot, cluster_slot, skill):
    imp = '{}-{}'.format(imp_slot, cluster_slot)
    s.headers.update({'Content-Type' : 'application/json'})
    response = s.post(url='http://127.0.0.1:8000/tinkerplants/update_imps', json={'slot' : imp, 'value' : skill})
    resp = response.json()
    print('{}: {} {} {}'.format(imp_slot, resp['implants'][imp_slot]['Shiny'], resp['implants'][imp_slot]['Bright'], resp['implants'][imp_slot]['Faded']))
    assert resp['success']
    
    

if __name__ == '__main__':
    test_implants()