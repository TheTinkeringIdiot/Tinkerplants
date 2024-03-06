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
            if ITEM_CLASS[item.itemClass] == 'Weapon':
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
    if 'FlingShot' in data['Can']:
        data['Specials']['FlingShot'] = calculate_fling(data['AttackDelay_Value'])
    if 'Burst' in data['Can']:
        if data.get('Burst') is not None:
            data['Specials']['Burst'] = calculate_burst(data['AttackDelay_Value'], data['RechargeDelay_Value'], data['Burst'])
        elif data.get('BurstRecharge') is not None:
            data['Specials']['Burst'] = calculate_burst(data['AttackDelay_Value'], data['RechargeDelay_Value'], data['BurstRecharge'])
    if 'FullAuto' in data['Can']:
        data['Specials']['FullAuto'] = calculate_full_auto(data['RechargeDelay_Value'], data['FullAuto'])
    if 'AimedShot' in data['Can']:
        data['Specials']['AimedShot'] = calculate_aimed_shot(data['RechargeDelay_Value'])
    if 'FastAttack' in data['Can']:
        data['Specials']['FastAttack'] = calculate_fast_attack(data['AttackDelay_Value'])

    data['Actions'] = []
    for actionData in item.actions.all():
        action = {}
        action['Action'] = TEMPLATE_ACTION[actionData.action]
        criteria = []

        op_idx = 0
        for actioncriterion in actionData.actioncriterion_set.order_by('order').select_related('criterion').all():
            criterion = actioncriterion.criterion
            if criterion.value1 == 0:
                if criterion.operator in USE_ON_OPERATOR.keys():
                    criteria.append([USE_ON_OPERATOR[criterion.operator]])
                else:
                    criteria[op_idx].append(GROUPING_OPERATOR[criterion.operator])
                op_idx += 1
            else:
                crit = []
                val1 = STAT[criterion.value1]
                crit.append(val1)

                if val1 == 'Profession':
                    val2 = PROFESSION[criterion.value2]
                elif val1 == 'Faction':
                    val2 = FACTION[criterion.value2]
                else:
                    val2 = criterion.value2
                
                compare = OPERATOR[criterion.operator]
                if compare == 'StatEqual' or compare == 'StatBitSet':
                    crit.append('==')
                    crit.append(val2)
                if compare == 'StatGreaterThan':
                    crit.append('>=')
                    crit.append(val2 + 1)
                elif compare == 'StatLessThan':
                    crit.append('<=')
                    crit.append(val2 - 1)
                elif compare == 'StatNotEqual':
                    crit.append('!=')
                    crit.append(val2)
                criteria.append(crit)

        action['Criteria'] = criteria
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
                        if not spell.spellID == 53033:
                            formatParams[tag] = int(spell.spellParams[tag] / 100)
                        else:
                            formatParams[tag] = spell.spellParams[tag]

                    elif tag == 'NanoID':
                        aoid = spell.spellParams[tag]
                        nano = Item.objects.get(aoid=aoid)
                        if nano is not None:
                            formatParams[tag] = f'<a href="/item/{aoid}">{nano.name}</a>'
                        else:
                            formatParams[tag] = f'<a href="/item/{aoid}">{aoid}</a>'

                    elif tag == 'BitNum':
                        formatParams[tag] = str(WORN_ITEM(2**spell.spellParams['BitNum'])).replace('WORN_ITEM.', '')

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