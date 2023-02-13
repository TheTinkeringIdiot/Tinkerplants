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

INITS = {
    120 : 'phys_init',
    118 : 'melee_init',
    119 : 'ranged_init'
}

DMG_TYPES = {
    0 : '-',
    90 : 'Projectile',
    91 : 'Melee',
    92 : 'Energy',
    93 : 'Chemical',
    94 : 'Radiation',
    95 : 'Cold',
    96 : 'Poison',
    97 : 'Fire'
}

BANNED_IDS = [
    303423, 303424, # Junior Ofab Bear
    303405, 303406, # Junior Ofab Boar
    303409, 303410, # Junior Ofab Cobra
    303413, 303414, # Junior Ofab Hawk
    303421, 303422, # Junior Ofab Mongoose
    303403, 303404, # Junior Ofab Panther
    303407, 303408, # Junior Ofab Peregrine
    303411, 303412, # Junior Ofab Shark
    303415, 303416, # Junior Ofab Silverback
    303425, 303426, # Junior Ofab Tiger
    303417, 303418, # Junior Ofab Viper
    303419, 303420, # Junior Ofab Wolf
    275607, # Alien Vortex Spinning Weapon
    280460, # Crazy Xanboss Weapon
    269377, # Metaing's Pink Pocket Knife
    295603, # Michizure's Boomstick!
    306174, # Bone of a Champion
    228373, # High Novictum Katana of Innocence
    228369, 228370, # Low Novictum Katana of Innocence
    228371, 228372, # Novictum Katana of Innocence
    281185, # A.F.D. Twohander
    164638, # Andrew's Uber Test Weapon
    227455, # Bent Fuzzys Poke Technique
]

SKIPPED_REQS = [
    'Gender', 
    'Nano programming', 
    'Mechanical engineering', 
    'Weapon smithing', 
    'Parry', 
    'Riposte', 
    'Wielded weapons', 
    '64', 
    'Form', 
    'Psychological modifications', 
    'Profession level',
    'Strength',
    'Cyberdeck',
    'Psychology',
]

def initial_weapons():
    return {
        'breed' : 1, 
        'profession' : 0,
        'level' : 1,
        'subscription' : 0,
        'crit' : 0,
        '1h Blunt' : 1,
        '1h Edged' : 1,
        '2h Blunt' : 1,
        '2h Edged' : 1,
        'Martial arts' : 1,
        'Melee energy' : 1,
        'Piercing' : 1,
        'Time and space' : 1,
        'Assault rifle' : 1,
        'Bow' : 1,
        'Grenade' : 1,
        'Heavy weapons' : 1,
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
        'aggdef' : 75,
        'aao' : 0,
        'add_dmg' : 0,
        'target_ac' : 1,
    }