from django.shortcuts import render
from tinkertools.models import *
from tinkertools.utils import *

import math, re

# Create your views here.


def index(request):
    return render(request, 'tinkertools/index.html')

def search(request):
    query = request.GET.get('query')

    results = Item.objects.filter(name__icontains=query).all()

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

        try:
            item['QL'] = result.stats.filter(stat=54).first().value
        except:
            item['QL'] = '-'

        data['Items'].append(item)

    # breakpoint()
    try:
        return render(request, 'tinkertools/search.html', data)
    except Exception as thing:
        breakpoint()

def item(request, id, ql=0):
    
    data = {}
    
    try:
        item = Item.objects.get(aoid=id)
    except:
        return render(request, 'tinkertools/item_not_found.html')

    data['Name'] = item.name
    data['Description'] = item.description
    
    for stat in item.stats.all():
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

        elif STAT[stat.stat] == 'RechargeDelay':
            data['RechargeDelay'] = f'{stat.value / 100:.2f}s'
            data['RechargeDelay_Value'] = stat.value

        elif STAT[stat.stat] == 'InitiativeType':
            data['InitiativeType'] = STAT[stat.value]

        elif STAT[stat.stat] == 'AmmoType':
            data['AmmoType'] = AMMOTYPE[stat.value]

        elif STAT[stat.stat] == 'Slot':
            # breakpoint()
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

        else:
            data[STAT[stat.stat]] = stat.value

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

    if data.get('Can') is not None and 'FullAuto' in data['Can']:
        if data.get('FullAuto') is not None:
            data['Specials']['FullAuto'] = calculate_full_auto(data['RechargeDelay_Value'], data['FullAuto'])
        elif data.get('FullAutoRecharge') is not None:
            data['Specials']['FullAuto'] = calculate_full_auto(data['RechargeDelay_Value'], data['FullAutoRecharge'])

    if data.get('Can') is not None and 'AimedShot' in data['Can']:
        data['Specials']['AimedShot'] = calculate_aimed_shot(data['RechargeDelay_Value'])
    if data.get('Can') is not None and 'FastAttack' in data['Can']:
        data['Specials']['FastAttack'] = calculate_fast_attack(data['AttackDelay_Value'])

    data['Actions'] = []
    for actionData in item.actions.all():
        action = {}
        if actionData.action == 0: # these are useless
            continue
        action['Action'] = TEMPLATE_ACTION[actionData.action]
        action['Criteria'] = []
        criteria = []

        for actioncriterion in actionData.actioncriterion_set.order_by('order').select_related('criterion').all():
            criterion = actioncriterion.criterion
            operator = criterion.operator
            # breakpoint()

            try:
                if operator == 42: 
                    if len(criteria) <= 0: continue
                    operand = criteria.pop()
                    operand.append('Not')
                    criteria.append(operand)
                    # result = operand
                
                elif operator == 4:
                    if len(criteria) <= 0: continue
                    oper1 = criteria.pop()
                    oper2 = criteria.pop()
                    oper2.append('And')
                    criteria.extend([oper2, oper1])
                    # result = [oper1, 'And', oper2]

                elif operator == 3:
                    if len(criteria) <= 0: continue
                    oper1 = criteria.pop()
                    oper2 = criteria.pop()
                    oper2.append('Or')
                    criteria.extend([oper2, oper1])
                    # result = [oper1, 'Or', oper2]

                else:
                    result = interpret_criterion(criterion)
                    criteria.append(result)

            except:
                continue
                
        if len(criteria) > 0:
            action['Criteria'].extend(criteria)

        if len(action['Criteria']) > 0:
            data['Actions'].append(action)

    data['SpellData'] = []
    for spellData in item.spellData.all():
        spellEvent= {}
        spellEvent['Event'] = TEMPLATE_EVENT[spellData.event]
        spellEvent['Spells'] = []
        for spell in spellData.spells.all():
            newSpell = {}
            newSpell['Target'] = TARGET[spell.target]
            newSpell['TickCount'] = spell.tickCount
            newSpell['TickInterval'] = spell.tickInterval
            newSpell['spellID'] = spell.spellID
            spellFormat = SPELL_FORMATS[spell.spellID]
            spellTokens = spellFormat.split('|')
            # breakpoint()

            for idx, token in enumerate(spellTokens):

                formatParams = {}
                tags = re.findall('(\{[A-z0-9]{1,}\})', token)
                tags = [re.sub('[\{\}]', '', x) for x in tags]

                for tag in tags:
                    # breakpoint()

                    if tag == 'Location':
                        formatParams[tag] = f'{TEXTURELOCATION[spell.spellParams[tag]]}'

                    elif tag == 'Stat' or tag == 'Skill':
                        # breakpoint()
                        formatParams[tag] = f'{STAT[spell.spellParams[tag]]}'

                    elif tag == 'Duration':
                        if not spell.spellID in [53033, 53187]:
                            formatParams[tag] = int(spell.spellParams[tag] / 100)
                        else:
                            formatParams[tag] = spell.spellParams[tag]

                    elif tag == 'NanoID':
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
                        # breakpoint()
                        stat = spell.spellParams['Stat']
                        if stat in [1, 62, 65, 179, 181, 198, 215, 224, 251, 256, 257, 301, 471, 472, 545, 583, 585, 586, 618, 686]:
                            formatParams[tag] = spell.spellParams[tag]
                        elif stat in [467]:
                            # breakpoint()
                            formatParams[tag] = str(SL_ZONE_PROTECTION(spell.spellParams[tag])).replace('SL_ZONE_PROTECTION.', '')
                        elif stat in [355]:
                            formatParams[tag] = str(WORN_ITEM(2**spell.spellParams['BitNum'])).replace('WORN_ITEM.', '')
                        elif stat in [0]:
                            formatParams[tag] = str(ITEM_NONE_FLAG(spell.spellParams['BitNum'])).replace('ITEM_NONE_FLAG.', '')
                        else:
                            breakpoint()

                    elif tag == 'Message':
                        if spell.spellParams.get(tag) is not None:
                            formatParams[tag] = spell.spellParams[tag]
                        else:
                            formatParams[tag] = spell.spellParams['MessageName']

                    elif tag == 'Target' and spell.spellID == 53254:
                        formatParams[tag] = 'Self'

                    else:
                        # breakpoint()
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
        breakpoint()

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

def calculate_full_auto(rech_time, fa_cycle):
    cap = math.floor(10 + (rech_time / 100))
    skill = round(((rech_time / 100) * 40 + (fa_cycle / 100) - cap) * 25)
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