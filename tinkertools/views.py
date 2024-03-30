from django.shortcuts import render, HttpResponseRedirect
from tinkertools.models import *
from tinkertools.utils import *
from tinkertools.InterpItem import *
from tinkertools.CriterionHandler import *

from django.db.models import Q, F
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank

import math, re

def index(request):
    return render(request, 'tinkertools/index.html')

def strain(request, id):
    data = {}
    try:
        
        nanos = Item.objects.filter(is_nano=True, stats__stat=75, stats__value=id).all()

        data['StrainName'] = NANO_STRAIN[id]
        data['Items'] = []
        
        for nano in nanos:
            nanoData = {}
            nanoData['Name'] = nano.name
            nanoData['AOID'] = nano.aoid
            try:
                nanoData['Icon'] = nano.stats.filter(stat=79).first().value
            except:
                nanoData['Icon'] = 273470

            nanoData['QL'] = nano.ql

            try:
                nanoData['StackingOrder'] = nano.stats.filter(stat=551).first().value
            except:
                nanoData['StackingOrder'] = 0
            data['Items'].append(nanoData)

        # breakpoint()

        
        return render(request, 'tinkertools/strain.html', data)

    except:
        return render(request, 'tinkertools/item_not_found.html')

def search(request):
    query = request.GET.get('query')

    if query is None or len(query) <= 0:
        return render(request, 'tinkertools/index.html')

    q = None
    for word in query.split(' '):
        if q is None:
            q = Q(name__icontains=word)
        else:
            q &= Q(name__icontains=word)

    results = Item.objects.filter(q).all()
    # results = Item.objects.filter(name__icontains=query).all()
    # results = Item.objects.annotate(rank=SearchRank(SearchVector('name', 'description'), SearchQuery(query))).filter(rank__gte=0.01).order_by('-rank').all()
    # results = Item.objects.filter(name__search=query).all()

    data = {}
    data['Items'] = []
    for result in results:
        item = {}
        try:
            item['Icon'] = result.stats.filter(stat=79).first().value
        except:
            item['Icon'] = 273470

        item['AOID'] = result.aoid
        item['Name'] = result.name
        item['QL'] = result.ql
        if result.itemClass == 1: # Item is a weapon
            try:
                minDmg = item.stats.filter(stat=286).first().value
            except:
                minDmg = 0
            
            try:
                maxDmg = item.stats.filter(stat=285).first().value
            except:
                maxDmg = 0

            try:
                critDmg = item.stats.filter(stat=284).first().value
            except:
                critDmg = 0

            item['Damage'] = f'{minDmg}-{maxDmg} ({critDmg})'
            data['HasWeapons'] = True

        data['Items'].append(item)

    try:
        return render(request, 'tinkertools/search.html', data)
    except Exception as thing:
        return render(request, 'tinkertools/item_not_found.html')
    
def advanced_search(request):
    data = {}
    data['requirements'] = REQUIREMENTS.items()
    data['spell_stats'] = SPELL_MODIFIED_STATS.items()
    return render(request, 'tinkertools/advanced_search.html', data)

def adv_search(request):
    if request.method == 'POST':
        data = request.POST

        results = {}
        modStats = []

        items = Item.objects.all()

        if len(data['name']) > 0:
            q = None
            for word in data['name'].split(' '):
                if q is None:
                    q = Q(name__icontains=word)
                else:
                    q &= Q(name__icontains=word)

            items = items.filter(q)
            # items = items.annotate(rank=SearchRank(SearchVector('name', 'description'), SearchQuery(data['name']))).filter(rank__gte=0.01).order_by('-rank').all()

        if int(data['min_ql']) >= 0 and int(data['max_ql']) <= 1000:
            items = items.filter(ql__gte=int(data['min_ql'])).filter(ql__lte=int(data['max_ql']))

        if int(data['item_class']) != -1:
            if int(data['item_class']) == 4:
                items = items.filter(is_nano=True)
            else:
                items = items.filter(stats__stat=76, stats__value=int(data['item_class']))

            if int(data['slot']) != -1:
                items = items.filter(stats__stat = 298).annotate(flag_check=F('stats__value').bitand(2**int(data['slot']))).exclude(flag_check=0)

        if int(data['profession']) != -1:
            items = items.filter(actions__criteria__value1=60, actions__criteria__value2=int(data['profession']))

        if int(data['faction']) != -1:
            items = items.filter(actions__criteria__value1=33, actions__criteria__value2=int(data['faction']))

        if int(data['breed']) != -1:
            items = items.filter(actions__criteria__value1=4, actions__criteria__value2=int(data['breed']))

        if int(data['gender']) != -1:
            items = items.filter(actions__criteria__value1=59, actions__criteria__value2=int(data['gender']))

        # Froob flag

        if data.get('froob') is not None:
            items = items.exclude(actions__criteria__value1=54, actions__criteria__value2__gte=201)
            items = items.exclude(actions__criteria__value1=389)

        # None Flags

        if data.get('nodrop') is not None:
            items = items.filter(stats__stat = 0).annotate(flag_check=F('stats__value').bitand(2**26)).exclude(flag_check=0)

        if data.get('unique') is not None:
            items = items.filter(stats__stat = 0).annotate(flag_check=F('stats__value').bitand(2**27)).exclude(flag_check=0)

        # CAN Flags

        if data.get('with_social') is not None:
            items = items.filter(stats__stat = 30).annotate(flag_check=F('stats__value').bitand(2**28)).exclude(flag_check=0)

        if data.get('flingshot') is not None:
            items = items.filter(stats__stat = 30).annotate(flag_check=F('stats__value').bitand(2**12)).exclude(flag_check=0)

        if data.get('burst') is not None:
            items = items.filter(stats__stat = 30).annotate(flag_check=F('stats__value').bitand(2**11)).exclude(flag_check=0)

        if data.get('fullauto') is not None:
            items = items.filter(stats__stat = 30).annotate(flag_check=F('stats__value').bitand(2**13)).exclude(flag_check=0)

        if data.get('aimedshot') is not None:
            items = items.filter(stats__stat = 30).annotate(flag_check=F('stats__value').bitand(2**14)).exclude(flag_check=0)

        if data.get('fastattack') is not None:
            items = items.filter(stats__stat = 30).annotate(flag_check=F('stats__value').bitand(2**18)).exclude(flag_check=0)

        if data.get('brawl') is not None:
            items = items.filter(stats__stat = 30).annotate(flag_check=F('stats__value').bitand(2**25)).exclude(flag_check=0)

        if data.get('dimach') is not None:
            items = items.filter(stats__stat = 30).annotate(flag_check=F('stats__value').bitand(2**26)).exclude(flag_check=0)

        if data.get('sneakattack') is not None:
            items = items.filter(stats__stat = 30).annotate(flag_check=F('stats__value').bitand(2**17)).exclude(flag_check=0)

        # Stat checks

        if data.get('strength') is not None:
            items = items.filter(spellData__spells__spellParams__Stat=16, spellData__spells__spellParams__Amount__gte=1)
            modStats.append(16)

        if data.get('stamina') is not None:
            items = items.filter(spellData__spells__spellParams__Stat=18, spellData__spells__spellParams__Amount__gte=1)
            modStats.append(18)

        if data.get('agility') is not None:
            items = items.filter(spellData__spells__spellParams__Stat=17, spellData__spells__spellParams__Amount__gte=1)
            modStats.append(17)

        if data.get('sense') is not None:
            items = items.filter(spellData__spells__spellParams__Stat=20, spellData__spells__spellParams__Amount__gte=1)
            modStats.append(20)

        if data.get('intelligence') is not None:
            items = items.filter(spellData__spells__spellParams__Stat=19, spellData__spells__spellParams__Amount__gte=1)
            modStats.append(19)

        if data.get('psychic') is not None:
            items = items.filter(spellData__spells__spellParams__Stat=21, spellData__spells__spellParams__Amount__gte=1)
            modStats.append(21)

        if data.get('treatment') is not None:
            items = items.filter(spellData__spells__spellParams__Stat=124, spellData__spells__spellParams__Amount__gte=1)
            modStats.append(124)

        if data.get('complit') is not None:
            items = items.filter(spellData__spells__spellParams__Stat=161, spellData__spells__spellParams__Amount__gte=1)
            modStats.append(161)

        data = dict(data.lists())
        for i in range(len(data['func_select'])):
            if data['value'][i] == '': continue

            func = int(data['func_select'][i])
            stat = int(data['stat_select'][i])
            op = int(data['op_select'][i])
            value = int(data['value'][i])

            if func == 0: # Requires - criterion
                if op == 0:
                    items = items.filter(actions__criteria__value1=stat, actions__criteria__value2__exact=value-1, actions__criteria__operator=op)
                if op == 1:
                    items = items.filter(actions__criteria__value1=stat, actions__criteria__value2__lte=value-1, actions__criteria__operator=op)
                if op == 2:
                    items = items.filter(actions__criteria__value1=stat, actions__criteria__value2__gte=value-1, actions__criteria__operator=op)
                if op == 0:
                    items = items.filter(actions__criteria__value1=stat).exclude(actions__criteria__value2__exact=value-1)

            elif func == 1: # Modifies - spell effect
                modStats.append(stat)
                if op == 0:
                    items = items.filter(spellData__spells__spellParams__Stat=stat, spellData__spells__spellParams__Amount__exact=value)
                elif op == 1:
                    items = items.filter(spellData__spells__spellParams__Stat=stat, spellData__spells__spellParams__Amount__lte=value)
                elif op == 2:
                    items = items.filter(spellData__spells__spellParams__Stat=stat, spellData__spells__spellParams__Amount__gte=value)
                elif op == 24:
                    items = items.filter(spellData__spells__spellParams__Stat=stat).exclude(spellData__spells__spellParams__Amount__exact=value)

        
        # Add ModStats for table header
        for stat in modStats:
            if results.get('ModStats') is None:
                results['ModStats'] = [STAT[stat]]
            else:
                results['ModStats'].append(STAT[stat])

        results['Items'] = []
        for item in items:
            result = {}
            try:
                result['Icon'] = item.stats.filter(stat=79).first().value
            except:
                result['Icon'] = 273470

            result['AOID'] = item.aoid
            result['Name'] = item.name
            result['QL'] = item.ql
            if item.itemClass == 1: # Item is a weapon, include damage stats
                try:
                    minDmg = item.stats.filter(stat=286).first().value
                except:
                    minDmg = 0
                
                try:
                    maxDmg = item.stats.filter(stat=285).first().value
                except:
                    maxDmg = 0

                try:
                    critDmg = item.stats.filter(stat=284).first().value
                except:
                    critDmg = 0

                result['Damage'] = f'{minDmg}-{maxDmg} ({critDmg})'
                results['HasWeapons'] = True

            # get ModStats values for the item
            for stat in modStats:
                val = item.spellData.filter(spells__spellParams__Stat=stat).first().spells.filter(spellParams__Stat=stat).first().spellParams['Amount']
                if result.get('ModStats') is None:
                    result['ModStats'] = [val]
                else:
                    result['ModStats'].append(val)

            results['Items'].append(result)
                
        try:
            return render(request, 'tinkertools/search.html', results)
        except Exception as thing:
            return render(request, 'tinkertools/item_not_found.html')

    else:
        data = {}
        data['requirements'] = REQUIREMENTS.items()
        data['spell_stats'] = SPELL_MODIFIED_STATS.items()
        return render(request, 'tinkertools/advanced_search.html', data)
    

def item(request, id, ql=0):
    
    data = {}
    
    try:
        item = InterpItem(id, ql)
    except:
        return render(request, 'tinkertools/item_not_found.html')
    
    # breakpoint()

    data['AOID'] = id
    data['Name'] = item.name
    data['Description'] = item.description
    data['QL'] = item.ql
    data['LowQL'] = item.low_ql
    data['HighQL'] = item.high_ql

    for stat in item.stats():
        if STAT[stat.stat] == 'Can':
            canItems = str(CANFLAG(stat.value)).replace('CANFLAG.', '').split('|')
            data['Can'] = canItems

        elif STAT[stat.stat] == 'None':
            if item.is_nano:
                data['Flags'] = str(NANO_NONE_FLAG(stat.value)).replace('NANO_NONE_FLAG.', '').split('|')
            else:
                data['Flags'] = str(ITEM_NONE_FLAG(stat.value)).replace('ITEM_NONE_FLAG.', '').split('|')

        elif STAT[stat.stat] == 'ItemClass':
            if not item.is_nano:
                data['ItemClass'] = ITEM_CLASS[stat.value]
            else:
                data['ItemClass'] = 'Nano'

        elif STAT[stat.stat] == 'AttackDelay':
            data['AttackDelay'] = f'{stat.value / 100:.2f}s'
            data['AttackDelay_Value'] = stat.value

        elif STAT[stat.stat] == 'AttackDelayCap':
            data['AttackDelayCap'] = f'{stat.value / 100:.2f}s'

        elif STAT[stat.stat] == 'RechargeDelay':
            data['RechargeDelay'] = f'{stat.value / 100:.2f}s'
            data['RechargeDelay_Value'] = stat.value

        elif STAT[stat.stat] == 'Duration':
            duration = stat.value / 100
            if duration > 3600:
                data['Duration'] = f'{duration / 3600:.2f}h'
            elif duration > 60:
                data['Duration'] = f'{duration / 60:.2f}m'
            else:
                data['Duration'] = f'{duration:.2f}s'

        elif STAT[stat.stat] == 'CooldownTime1':
            data['CooldownTime1'] = f'{stat.value / 100:.2f}s'

        elif STAT[stat.stat] == 'InitiativeType':
            data['InitiativeType'] = STAT[stat.value]

        elif STAT[stat.stat] == 'AmmoType':
            data['AmmoType'] = AMMOTYPE[stat.value]

        elif STAT[stat.stat] == 'Slot':
            if ITEM_CLASS[item.itemClass] == 'Weapon':
                if item.aoid in [202726, 202727, 202728, 202729, 202730, 202731, 290619, 290625, 290626, 290627]: # Slot on this item is -1, set it manually
                    slots = str(WEAPON_SLOT(2**9)).replace('WEAPON_SLOT.', '').split('|')
                else:
                    slots = str(WEAPON_SLOT(stat.value)).replace('WEAPON_SLOT.', '').split('|')
                data['Slot'] = slots
            elif ITEM_CLASS[item.itemClass] == 'Armor':
                slots = str(ARMOR_SLOT(stat.value)).replace('ARMOR_SLOT.', '').split('|')
                data['Slot'] = slots
            elif ITEM_CLASS[item.itemClass] == 'Implant':
                slots = str(IMPLANT_SLOT(stat.value)).replace('IMPLANT_SLOT.', '').split('|')
                data['Slot'] = slots

        elif STAT[stat.stat] == 'DamageType2':
            data['DamageType'] = STAT[stat.value]

        elif STAT[stat.stat] == 'NanoStrain':
            data['NanoStrain'] = NANO_STRAIN[stat.value]
            data['NanoStrain_Value'] = stat.value

        else:
            data[STAT[stat.stat]] = stat.value

    if data.get('Icon') is None:
        if data.get('EffectIcon') is not None:
            data['Icon'] = data['EffectIcon']
        else:
            data['Icon'] = 273470

    if data.get('ItemClass') is None:
        if item.is_nano:
            data['ItemClass'] = 'Nano'
        else:
            data['ItemClass'] = 'None'

    if item.atkdef is not None:
        data['AttackSkills'] = []
        for sv in item.atkdef.attack.all():
            data['AttackSkills'].append([STAT[sv.stat], f'{sv.value}%'])

        data['DefenseSkills'] = []
        for sv in item.atkdef.defense.all():
            data['DefenseSkills'].append([STAT[sv.stat], f'{sv.value}%'])

    data['Specials'] = {}
    if data.get('Can') is not None and 'FlingShot' in data['Can']:
        data['Specials']['FlingShot'] = calculate_fling(data['AttackDelay_Value'])

    if data.get('Can') is not None and 'Burst' in data['Can']:
        if data.get('Burst') is not None:
            data['Specials']['Burst'] = calculate_burst(data['AttackDelay_Value'], data['RechargeDelay_Value'], data['Burst'])
        elif data.get('BurstRecharge') is not None:
            data['Specials']['Burst'] = calculate_burst(data['AttackDelay_Value'], data['RechargeDelay_Value'], data['BurstRecharge'])
        else:
            data['Specials']['Burst'] = calculate_burst(data['AttackDelay_Value'], data['RechargeDelay_Value'], 0)

    if data.get('Can') is not None and 'FullAuto' in data['Can']:
        if data.get('FullAuto') is not None:
            data['Specials']['FullAuto'] = calculate_full_auto(data['AttackDelay_Value'], data['RechargeDelay_Value'], data['FullAuto'])
        elif data.get('FullAutoRecharge') is not None:
            data['Specials']['FullAuto'] = calculate_full_auto(data['AttackDelay_Value'], data['RechargeDelay_Value'], data['FullAutoRecharge'])
        else:
            data['Specials']['FullAuto'] = calculate_full_auto(data['AttackDelay_Value'], data['RechargeDelay_Value'], 0)

    if data.get('Can') is not None and 'AimedShot' in data['Can']:
        data['Specials']['AimedShot'] = calculate_aimed_shot(data['RechargeDelay_Value'])
    if data.get('Can') is not None and 'FastAttack' in data['Can']:
        data['Specials']['FastAttack'] = calculate_fast_attack(data['AttackDelay_Value'])

    data['Actions'] = []
    for actionData in item.actions:
        action = {}
        if actionData.action == 0: # these are useless
            continue
        action['Action'] = TEMPLATE_ACTION[actionData.action]
        action['Criteria'] = []
        criteria = CriterionHandler([x for x in actionData.criteria()]).parse_criteria()
     
        if len(criteria) > 0:
            action['Criteria'].extend(criteria)

        if len(action['Criteria']) > 0:
            data['Actions'].append(action)

    data['SpellData'] = []
    for spellData in item.spellData:
        spellEvent= {}
        spellEvent['Event'] = TEMPLATE_EVENT[spellData.event]
        spellEvent['Spells'] = []
        for spell in spellData.spells():
            
            newSpell = {}
            newSpell['Target'] = TARGET[spell.target]
            newSpell['spellID'] = spell.spellID
            spellFormat = SPELL_FORMATS[spell.spellID]
            spellTokens = spellFormat.split('|')

            newSpell['Criteria'] = CriterionHandler([x for x in spell.criteria()]).parse_criteria()

            for idx, token in enumerate(spellTokens):

                formatParams = {}
                formatParams['TickCount'] = spell.tickCount
                formatParams['TickInterval'] = spell.tickInterval / 100
                tags = re.findall('(\{[A-z0-9]{1,}\})', token)
                tags = [re.sub('[\{\}]', '', x) for x in tags]

                for tag in tags:

                    if tag == 'Location':
                        formatParams[tag] = f'{TEXTURELOCATION[spell.spellParams[tag]]}'

                    elif tag == 'Stat' or tag == 'Skill':
                        formatParams[tag] = f'{STAT[spell.spellParams[tag]]}'

                    elif tag == 'Duration':
                        if not spell.spellID in [53033, 53187, 53177]:
                            formatParams[tag] = int(spell.spellParams[tag] / 100)
                        else:
                            formatParams[tag] = spell.spellParams[tag]

                    elif tag == 'NanoID' or tag == 'Proc':
                        aoid = spell.spellParams[tag]
                        try:
                            nano = Item.objects.get(aoid=aoid)
                        except:
                            formatParams[tag] = 'Unknown'
                            continue
                        
                        if nano is not None:
                            formatParams[tag] = f'<a href="/item/{aoid}">{nano.name}</a>'
                        else:
                            formatParams[tag] = f'<a href="/item/{aoid}">{aoid}</a>'

                    elif tag == 'BitNum':
                        stat = spell.spellParams['Stat']
                        if stat in [1, 62, 65, 179, 181, 198, 215, 224, 251, 256, 257, 301, 471, 472, 545, 583, 585, 586, 618, 686]:
                            formatParams[tag] = spell.spellParams[tag]
                        elif stat in [467]:
                            formatParams[tag] = str(SL_ZONE_PROTECTION(spell.spellParams[tag])).replace('SL_ZONE_PROTECTION.', '')
                        elif stat in [355]:
                            formatParams[tag] = str(WORN_ITEM(2**spell.spellParams['BitNum'])).replace('WORN_ITEM.', '')
                        elif stat in [0]:
                            formatParams[tag] = str(ITEM_NONE_FLAG(spell.spellParams['BitNum'])).replace('ITEM_NONE_FLAG.', '')

                    elif tag == 'Message':
                        if spell.spellParams.get(tag) is not None:
                            formatParams[tag] = spell.spellParams[tag]
                        else:
                            formatParams[tag] = spell.spellParams['MessageName']

                    elif tag == 'Target' and spell.spellID == 53254:
                        formatParams[tag] = 'Self'

                    elif tag == 'TickCount' or tag == 'TickInterval':
                        pass

                    elif tag == 'Action':
                        formatParams[tag] = str(ACTION_FLAG(spell.spellParams[tag])).replace('ACTION_FLAG.', '')

                    else:
                        formatParams[tag] = spell.spellParams[tag]
                            
                        
                if idx == 0:
                    newSpell['Description'] = token.format(**formatParams)
                else:
                    newSpell['Amount'] = token.format(**formatParams)

            spellEvent['Spells'].append(newSpell)
        data['SpellData'].append(spellEvent)

    # breakpoint()
    
    try:
        return render(request, 'tinkertools/item.html', data)
    except Exception as thing:
        return render(request, 'tinkertools/item_not_found.html')

def calculate_fling(attack_time):
    cap = math.floor(6 + (attack_time / 100))
    skill = round(1600 * (attack_time / 100) - (cap * 100))
    cycle = (skill, cap)
    return cycle

def calculate_burst(attack_time, rech_time, burst_cycle):
    cap = math.floor(8 + (attack_time / 100))
    skill = round(((rech_time / 100) * 20 + (burst_cycle / 100) - cap) * 25)
    cycle = (skill, cap)
    return cycle

def calculate_full_auto(attack_time, rech_time, fa_cycle):
    cap = math.floor(10 + (attack_time / 100))
    if fa_cycle == 0:
        fa_cycle = 1000
    skill = round(((rech_time / 100) * 40 + (fa_cycle / 100) - 11) * 25)
    cycle = (skill, cap)
    return cycle

def calculate_aimed_shot(rech_time):
    cap = math.floor(10 + (rech_time / 100))
    skill = round(((rech_time / 100) * 40 - cap) * 100 / 3)
    cycle = (skill, cap)
    return cycle

def calculate_fast_attack(attack_time):
    cap = math.floor(6 + (attack_time / 100))
    skill = round(((attack_time / 100) * 15 - cap) * 100)
    cycle = (skill, cap)
    return cycle