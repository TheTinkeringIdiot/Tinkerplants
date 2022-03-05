
BREEDS = {
    0 : 'Solitus',
    1 : 'Opifex',
    2 : 'Nanomage',
    3 : 'Atrox'
}

DECKS = {
    0 : '',
    0 : 'Worn Cyberdeck',
    1 : 'Basic Cyberdeck',
    2 : 'Augmented Cyberdeck',
    4 : 'Jobe-chipped Cyberdeck',
    8 : 'Izgimmer Modified Cyberdeck'
}

HUMIDITY = {
    0 : 0,
    1 : 0.333333,
    2 : 1.4,
    3 : 3.4,
    4 : 6.8,
    5 : 8.733333,
    6 : 12.7333,
    7 : 15.66666
}

CRUNCHCOM = {
    0 : 0,
    1 : 6,
    2 : 9,
    3 : 11,
    4 : 13,
    5 : 18,
    6 : 22,
    7 : 28
}

NOTUM_SIPHON = {
    0 : 0.0,
    1 : 5.0,
    2 : 9.0,
    3 : 14.4444,
    4 : 21.1111,
    5 : 25.0,
    6 : 26.875,
    7 : 34.2857,
    8 : 37.1428,
    9 : 42.8571,
    10 : 83.4
}

CHANNELING_OF_NOTUM = {
    0 : 0.0,
    1 : 1.7857,
    2 : 4.6153,
    3 : 7.5,
    4 : 15.4545
}

ENHANCE_NANO_DAMAGE = {
    0 : 0,
    1 : 2,
    2 : 4,
    3 : 7,
    4 : 10,
    5 : 13,
    6 : 18
}

ANCIENT_MATRIX = {
    0 : 0,
    1 : 0,
    2 : 0,
    3 : 1,
    4 : 1,
    5 : 1,
    6 : 2,
    7 : 2,
    8 : 2,
    9 : 3,
    10 : 3
}

DAMAGE_TYPES = {
    0 : 'All',
    1 : 'Chemical',
    2 : 'Cold',
    3 : 'Energy',
    4 : 'Fire',
    5 : 'Melee',
    6 : 'Poison',
    7 : 'Projectile',
    8 : 'Radiation'
}

def initial_nukes():
    return {
        'breed' : 0,
        'level' : 1,
        'mc' : 1,
        'nano_init' : 1,
        'max_nano' : 1,
        'aggdef' : 100,
        'max_nano' : 100,
        'he' : 0,
        'NS' : 0,
        'CoN' : 0,
        'END' : 0,
        'AM' : 0,
        'crunchcom' : 0,
        'deck' : 0,
        'spec' : 0,
        'nano_dmg' : 0,
        'cost_pct' : 0,
        'body_dev' : 1,
        'psychic' : 1,
        'nano_delta' : 0
    }