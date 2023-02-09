
import os, json
import django
from tinkerplants.utils import *

os.environ['DJANGO_SETTINGS_MODULE'] = 'aobase.settings'
django.setup()

from tinkerplants.models import *
from tinkernukes.models import *
from tinkerfite.models import *

# Clear out the old data entirely
Implant.objects.all().delete()
Cluster.objects.all().delete()
Nano.objects.all().delete()
Weapon.objects.all().delete()

with open('data.json', 'r') as fd:
    data = json.loads(fd.read())

clusters = data['data']['clusters']
implants = data['data']['implants']
nanos = data['data']['nanos']
weapons = data['data']['weapons']

new_clusters = []
new_implants = []
new_nanos = []
new_weapons = []

for name, vals in clusters.items():
    if not vals.get('normal'): # what the....skip it
        continue

    jobeskill = vals.get('jobeskill', '')
    npmod = vals.get('npmod', '')
    
    for clusterslot, clustervals in vals['normal'].items():
        cluster = Cluster()
        cluster.ql = 1
        cluster.clusterslot = CLUSTER_SLOTS[clusterslot]
        cluster.impslot = clustervals.get('impslot', '')
        cluster.skill = name
        cluster.loval = clustervals.get('loval')
        cluster.hival = clustervals.get('hival')
        cluster.jobemod = clustervals.get('jobemod', '')
        cluster.jobeskill = jobeskill
        cluster.npmod = npmod

        new_clusters.append(cluster)

    if not vals.get('refined'):
        continue

    for clusterslot, clustervals in vals['refined'].items():
        cluster = Cluster()
        cluster.ql = 201
        cluster.clusterslot = CLUSTER_SLOTS[clusterslot]
        cluster.impslot = clustervals.get('impslot', '')
        cluster.skill = name
        cluster.loval = clustervals.get('loval', 0)
        cluster.hival = clustervals.get('hival', 0)
        cluster.jobemod = clustervals.get('jobemod', '')
        cluster.jobeskill = jobeskill
        cluster.npmod = npmod

        new_clusters.append(cluster)

# Add Nano Delta clusters that don't appear in Auno's dump
new_clusters.append(Cluster(
    ql = 1,
    clusterslot = CLUSTER_SLOTS['Bright'],
    impslot = 4,
    skill = 'Nano Delta',
    loval = 3,
    hival = 33,
    jobemod = 4.0,
    jobeskill = 'Pharma Tech',
    npmod = 0.0
))

new_clusters.append(Cluster(
    ql = 1,
    clusterslot = CLUSTER_SLOTS['Shiny'],
    impslot = 7,
    skill = 'Nano Delta',
    loval = 5,
    hival = 55,
    jobemod = 5.25,
    jobeskill = 'Pharma Tech',
    npmod = 0.0
))

Cluster.objects.bulk_create(new_clusters)

for aoid, vals in implants.items():
    implant = Implant()
    implant.aoid = aoid
    implant.name = vals.get('name', '')
    if vals['refined']:
        implant.ql = 201
    else:
        implant.ql = 1
    implant.slot = vals.get('slot', 0)
    implant.icon = vals.get('icon', 0)
    implant.shiny = vals.get('shiny', 'Empty')
    implant.bright = vals.get('bright', 'Empty')
    implant.faded = vals.get('faded', 'Empty')

    # fix up some inconsistencies from the data dump
    reqs = vals.get('reqs', {})
    for key, val in reqs.items():
        if val.get('loval') is None:
            if key == 'Treatment':
                if implant.ql == 1:
                    reqs[key]['loval'] = 11
                elif implant.ql == 201:
                    reqs[key]['loval'] = 1001
            elif key == 'Title level':
                if implant.ql == 1:
                    reqs[key]['loval'] = 1
                elif implant.ql == 201:
                    reqs[key]['loval'] = 5
            else:
                if implant.ql == 1:
                    reqs[key]['loval'] = 6
                elif implant.ql == 201:
                    reqs[key]['loval'] = 426
        if val.get('hival') is None:
            if key == 'Treatment':
                if implant.ql == 1:
                    reqs[key]['hival'] = 451
                elif implant.ql == 201:
                    reqs[key]['hival'] = 2051
            elif key == 'Title level':
                if implant.ql == 1:
                    reqs[key]['hival'] = 1
                elif implant.ql == 201:
                    reqs[key]['hival'] = 6
            else:
                if implant.ql == 1:
                    reqs[key]['hival'] = 404
                elif implant.ql == 201:
                    reqs[key]['hival'] = 1095

    implant.reqs = reqs

    new_implants.append(implant)

Implant.objects.bulk_create(new_implants)
        
shiny_nd_fixed = []
shiny_nd = Implant.objects.filter(name__contains='Nano Delta, Shiny Jobe')
for entry in shiny_nd:
    entry.shiny = 'Nano Delta'
    shiny_nd_fixed.append(entry)

Implant.objects.bulk_update(shiny_nd_fixed, ['shiny'])

bright_nd_fixed = []
bright_nd = Implant.objects.filter(name__contains='Nano Delta, Bright Jobe')
for entry in bright_nd:
    entry.bright = 'Nano Delta'
    bright_nd_fixed.append(entry)

Implant.objects.bulk_update(bright_nd_fixed, ['bright'])

for aiod, vals in nanos.items():
    nano = Nano()
    nano.name = vals['name']
    nano.ql = vals['ql']
    nano.mc = vals['mc']
    nano.attack = vals['attack']
    nano.recharge = vals['recharge']
    nano.cost = vals['cost']
    nano.low_dmg = vals['low_dmg']
    nano.high_dmg = vals['high_dmg']
    nano.ac = vals['ac']
    nano.nr_pct = vals['nr_pct']

    if vals.get('nt_dot') is not None:
        nano.nt_dot = vals['nt_dot']
    else:
        nano.nt_dot = False

    if vals.get('nt_dot') is not None:
        nano.nt_dot = vals['nt_dot']
    else:
        nano.nt_dot = False

    if vals.get('level_req') is not None:
        nano.level = vals['level_req']
    else:
        nano.level = 0

    if vals.get('spec') is not None:
        nano.spec = vals['spec']
    else:
        nano.spec = 0

    if vals.get('deck') is not None:
        nano.deck = vals['deck']
    else:
        nano.deck = 0

    if vals.get('atk_cap') is not None:
        nano.atk_cap = vals['atk_cap']
    else:
        nano.atk_cap = 0

    if vals.get('dot_hits') is not None:
        nano.dot_hits = vals['dot_hits']
    else:
        nano.dot_hits = 0

    if vals.get('dot_delay') is not None:
        nano.dot_delay = vals['dot_delay']
    else:
        nano.dot_delay = 0

    if vals.get('strain_cd') is not None:
        nano.strain_cd = vals['strain_cd']
    else:
        nano.strain_cd = 0

    new_nanos.append(nano)

Nano.objects.bulk_create(new_nanos)

for aoid, vals in weapons.items():
    weapon = Weapon()
    weapon.aoid = aoid
    weapon.ql = vals['ql']
    weapon.name = vals['name']
    weapon.atk_time = vals['times']['attack']
    weapon.rech_time = vals['times']['recharge']
    weapon.dmg_min = vals['damage']['minimum']
    weapon.dmg_max = vals['damage']['maximum']
    weapon.dmg_crit = vals['damage']['critical']
    weapon.dmg_type = vals['damage']['type']
    weapon.clipsize = vals['clipsize']
    weapon.props = vals['props']
    weapon.reqs = vals['reqs']
    weapon.atk_skills = vals['attack_skills']
    weapon.other = vals['other']

    new_weapons.append(weapon)

Weapon.objects.bulk_create(new_weapons)
