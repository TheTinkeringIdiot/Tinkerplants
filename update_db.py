
import os, json
import django
from tinkerplants.utils import *

os.environ['DJANGO_SETTINGS_MODULE'] = 'aobase.settings'
django.setup()

from tinkerplants.models import *
from tinkernukes.models import *
from tinkerfite.models import *
from tinkerpocket.models import *
from tinkernanos.models import *

# Clear out the old data entirely
Implant.objects.all().delete()
Cluster.objects.all().delete()
Nuke.objects.all().delete()
Weapon.objects.all().delete()
Symbiant.objects.all().delete()
Pocketboss.objects.all().delete()
Nano.objects.all().delete()

with open('data.json', 'r') as fd:
    data = json.loads(fd.read())

clusters = data['data']['clusters']
implants = data['data']['implants']
nt_nukes = data['data']['nt_nukes']
nanos = data['data']['nanos']
weapons = data['data']['weapons']
symbiants = data['data']['symbiants']
bosses = data['data']['bosses']

new_clusters = []
new_implants = []
new_nukes = []
new_nanos = []
new_weapons = []
new_symbs = []
new_bosses = []

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

for aiod, vals in nt_nukes.items():
    nuke = Nuke()
    nuke.name = vals['name']
    nuke.ql = vals['ql']
    nuke.mc = vals['mc']
    nuke.attack = vals['attack']
    nuke.recharge = vals['recharge']
    nuke.cost = vals['cost']
    nuke.low_dmg = vals['low_dmg']
    nuke.high_dmg = vals['high_dmg']
    nuke.ac = vals['ac']
    nuke.nr_pct = vals['nr_pct']

    if vals.get('nt_dot') is not None:
        nuke.nt_dot = vals['nt_dot']
    else:
        nuke.nt_dot = False

    if vals.get('nt_dot') is not None:
        nuke.nt_dot = vals['nt_dot']
    else:
        nuke.nt_dot = False

    if vals.get('level_req') is not None:
        nuke.level = vals['level_req']
    else:
        nuke.level = 0

    if vals.get('spec') is not None:
        nuke.spec = vals['spec']
    else:
        nuke.spec = 0

    if vals.get('deck') is not None:
        nuke.deck = vals['deck']
    else:
        nuke.deck = 0

    if vals.get('atk_cap') is not None:
        nuke.atk_cap = vals['atk_cap']
    else:
        nuke.atk_cap = 0

    if vals.get('dot_hits') is not None:
        nuke.dot_hits = vals['dot_hits']
    else:
        nuke.dot_hits = 0

    if vals.get('dot_delay') is not None:
        nuke.dot_delay = vals['dot_delay']
    else:
        nuke.dot_delay = 0

    if vals.get('strain_cd') is not None:
        nuke.strain_cd = vals['strain_cd']
    else:
        nuke.strain_cd = 0

    new_nukes.append(nuke)

Nuke.objects.bulk_create(new_nukes)

for aoid, vals in nanos.items():
    nano = Nano()
    nano.aoid = int(aoid)
    nano.name = vals['name']
    nano.icon = vals['icon']
    nano.school = vals['school']
    nano.strain = vals['strain']
    nano.strain_name = vals['strain_name']
    nano.profession = vals['profession']
    nano.ql = vals['ql']
    nano.uploaded_by = vals['uploaded_by']

    if vals.get('Specialization') is not None:
        nano.spec = vals['Specialization']

    if vals.get('Expansion sets') is not None:
        nano.expansion = vals['Expansion sets']

    if vals.get('level_req') is not None:
        nano.level = vals['level_req']

    if vals.get('location') is not None:
        nano.location = vals['location']

    if vals.get('Matter metamorphosis') is not None:
        nano.mm = vals['Matter metamorphosis']

    if vals.get('Biological metamorphosis') is not None:
        nano.bm = vals['Biological metamorphosis']

    if vals.get('Matter creation') is not None:
        nano.mc = vals['Matter creation']

    if vals.get('Time and space') is not None:
        nano.ts = vals['Time and space']

    if vals.get('Psychological modifications') is not None:
        nano.pm = vals['Psychological modifications']

    if vals.get('Sensory improvement') is not None:
        nano.si = vals['Sensory improvement']

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

for aoid, vals in symbiants.items():
    symb = Symbiant()
    symb.aoid = aoid
    symb.ql = vals['ql']
    symb.name = vals['name']
    symb.slot = vals['slot']
    symb.family = vals['family']
    symb.reqs = vals['reqs']
    symb.effects = vals['effects']

    new_symbs.append(symb)

Symbiant.objects.bulk_create(new_symbs)

for name, vals in bosses.items():
    boss = Pocketboss()
    boss.name = name
    boss.level = vals['level']
    boss.playfield = vals['playfield']
    boss.location = vals['location']
    boss.mobs = vals['mobs']

    boss.save()

    drops = Symbiant.objects.filter(aoid__in=vals['drops'])

    boss.drops.add(*drops)
    boss.save()
