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
        'breed' : 6, 
        'profession' : 0,
        'level' : 1,
        'subscription' : 0,
        '1hb' : 1,
        '1he' : 1,
        '2hb' : 1,
        '2he' : 1,
        'martial_arts' : 1,
        'melee_energy' : 1,
        'piercing' : 1,
        'assault_rifle' : 1,
        'bow' : 1,
        'mg_smg' : 1,
        'pistol' : 1,
        're' : 1,
        'rifle' : 1,
        'shotgun' : 1,
        'aimed' : 1,
        'brawl' : 1,
        'burst' : 1,
        'dimach' : 1,
        'fastattack' : 1,
        'fling' : 1,
        'fullauto' : 1,
        'sneak' : 1,
        'melee_init' : 1,
        'phys_init' : 1,
        'ranged_init' : 1,
        'aggdef' : 1,
        'aao' : 0,
        'add_dmg' : 0,
        'target_ac' : 1,
        'dmg_type' : 0,
    }