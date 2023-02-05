BREEDS = {
    1 : 'Solitus',
    2 : 'Opifex',
    3 : 'Nanomage',
    4 : 'Atrox'
}

PROFESSIONS = {
    6 : 'Adventurer',
    5 : 'Agent',
    8 : 'Bureaucrat',
    10 : 'Doctor',
    9 : 'Enforcer',
    3 : 'Engineer',
    4 : 'Fixer',
    14 : 'Keeper',
    2 : 'Martial Artist',
    12 : 'Meta-Physicist',
    11 : 'Nano-Technician',
    15 : 'Shade',
    1 : 'Soldier',
    7 : 'Trader'
}

EXPANSIONS = {
    0 : 'None',
    2 : 'Shadowlands',
    8 : 'Alien Invasion',
    32 : 'Lost Eden',
    128 : 'Legacy of Xan'
}

SUBSCRIPTIONS = {
    0 : 'Free (Froob)',
    2 : 'Shadowlands (Sloob)',
    8 : 'Paid'
}

def initial_weapons():
    return {
        'breed' : 1, 
        'profession' : 6,
        'level' : 1,
        'subscription' : 0,
        '1h Blunt' : 1,
        '1h Edged' : 1,
        '2h Blunt' : 1,
        '2h Edged' : 1,
        'Martial arts' : 1,
        'Melee energy' : 1,
        'Piercing' : 1,
        'Assault rifle' : 1,
        'Bow' : 1,
        'Smg' : 1,
        'Pistol' : 1,
        'Ranged energy' : 1,
        'Rifle' : 1,
        'Shotgun' : 1,
        'Aimed shot' : 1,
        'Brawl' : 1,
        'Burst' : 1,
        'Dimach' : 1,
        'Fast attack' : 1,
        'Fling shot' : 1,
        'Full auto' : 1,
        'Sneak attack' : 1,
        'melee_init' : 1,
        'phys_init' : 1,
        'ranged_init' : 1,
        'aggdef' : 1,
        'aao' : 0,
        'add_dmg' : 0,
        'target_ac' : 1,
        'dmg_type' : 0,
    }