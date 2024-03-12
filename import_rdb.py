
import os, json
import django
from django import db
from multiprocessing import Pool
from tinkerplants.utils import *

os.environ['DJANGO_SETTINGS_MODULE'] = 'aobase.settings'
django.setup()

from tinkertools.models import *

# Clear out the old data entirely

StatValue.objects.all().delete()
Criterion.objects.all().delete()
Spell.objects.all().delete()
SpellData.objects.all().delete()
AttackDefense.objects.all().delete()
AnimationMesh.objects.all().delete()
Item.objects.all().delete()
Action.objects.all().delete()

def import_items(chunk):
    import_rdb(chunk, False)

def import_nanos(chunk):
    import_rdb(chunk, True)

def import_rdb(data, is_nano):

    for item in data:
        newItem, created = Item.objects.get_or_create(aoid=item['AOID'])
        # print(newItem.aoid)

        newItem.name = item.get('Name')
        newItem.description = item.get('Description')
        newItem.is_nano = is_nano

        newItem.save()

        for sv in item.get('StatValues'):
            stat = sv.get('Stat')
            value = sv.get('RawValue')
            if stat == 76:
                newItem.itemClass = value
            elif stat == 54:
                newItem.ql = value
            statValue, create = StatValue.objects.get_or_create(stat=stat, value=value)
            newItem.stats.add(statValue)

        if newItem.ql is None:
            newItem.ql = 1

        if newItem.itemClass is None:
            newItem.itemClass = 0

        atkdef = item.get('AttackDefenseData')
        if atkdef is not None:
            newAtkDef = AttackDefense.objects.create()
            for atk in atkdef.get('Attack'):
                sv, create = StatValue.objects.get_or_create(stat=atk.get('Stat'), value=atk.get('RawValue'))
                newAtkDef.attack.add(sv)
            for atk in atkdef.get('Defense'):
                sv, create = StatValue.objects.get_or_create(stat=atk.get('Stat'), value=atk.get('RawValue'))
                newAtkDef.defense.add(sv)
            newItem.atkdef = newAtkDef

        actionData = item.get('ActionData')
        if actionData is not None:
            actions = actionData.get('Actions')
            if actions is not None:
                for action in actions:
                    newAction = Action()
                    newAction.action = action['Action']
                    newAction.save()
                    crit_idx = 0
                    for criterion in action.get('Criteria'):
                        ac = ActionCriterion()
                        crit, create = Criterion.objects.get_or_create(value1=criterion['Value1'], value2=criterion['Value2'], operator=criterion['Operator'])
                        ac.action = newAction
                        ac.criterion = crit
                        ac.order = crit_idx
                        ac.save()
                        newAction.criteria.add(crit)

                        crit_idx += 1
                    
                    newAction.item = newItem
                    newAction.save()


        for spellData in item.get('SpellData'):
            newSpellData = SpellData()
            newSpellData.event = spellData['Event']
            newSpellData.save()
            
            for spell in spellData['Items']:
                newSpell = Spell.objects.create()
                newSpell.spellID = spell['SpellID']
                spell.pop('SpellID', None)
                newSpell.target = spell['Target']
                spell.pop('Target', None)
                newSpell.tickCount = spell['TickCount']
                spell.pop('TickCount', None)
                newSpell.tickInterval = spell['TickInterval']
                spell.pop('TickInterval', None)
                newSpell.spellFormat = spell['SpellFormat']
                spell.pop('SpellFormat', None)
                newSpell.save()

                for criterion in spell['Criteria']:
                    crit, create = Criterion.objects.get_or_create(value1=criterion['Value1'], value2=criterion['Value2'], operator=criterion['Operator'])
                    newSpell.criteria.add(crit)

                newSpell.spellParams = spell
                newSpell.save()
                newSpellData.spells.add(newSpell)
            newSpellData.save()
            
            newItem.spellData.add(newSpellData)

        shopHashData = item.get('ShopHashData')
        if shopHashData is not None:
            for shopItem in shopHashData['Items']:
                shopHash = ShopHash()
                shopHash.hash = shopItem['Hash']['Text']
                shopHash.minLevel = shopItem['MinLevel']
                shopHash.maxLevel = shopItem['MaxLevel']
                shopHash.baseAmount = shopItem['BaseAmount']
                shopHash.regenAmount = shopItem['RegenAmount']
                shopHash.regenInterval = shopItem['RegenInterval']
                shopHash.spawnChance = shopItem['SpawnChance']
                shopHash.save()

                newItem.shopHash.add(shopHash)

        animesh = item.get('AnimationMesh')
        if animesh is not None:
            newAniMesh = AnimationMesh()
            animation = animesh.get('Animation')
            newAniMesh.save()
            if animation is not None:
                sv, create = StatValue.objects.get_or_create(stat=animation['Stat'], value=animation['RawValue'])
                newAniMesh.animation = sv
            mesh = animesh.get('Mesh')
            if mesh is not None:
                sv, create = StatValue.objects.get_or_create(stat=mesh['Stat'], value=mesh['RawValue'])
                newAniMesh.mesh = sv
            newAniMesh.save()
            newItem.animationMesh = newAniMesh

        newItem.save()

def get_singletons(data):

    statVals = []
    criteria = []

    idx = 0
    for item in data:
        if idx % 1000 == 0:
            print(idx)

        for sv in item.get('StatValues'):
            stat = sv.get('Stat')
            value = sv.get('RawValue')
            # sv = StatValue(stat=stat, value=value)
            statVals.append((stat, value))

        atkdef = item.get('AttackDefenseData')
        if atkdef is not None:
            for atk in atkdef.get('Attack'):
                # sv = StatValue(stat=atk.get('Stat'), value=atk.get('RawValue'))
                statVals.append((atk.get('Stat'), atk.get('RawValue')))

            for atk in atkdef.get('Defense'):
                # sv = StatValue(stat=atk.get('Stat'), value=atk.get('RawValue'))
                statVals.append((atk.get('Stat'), atk.get('RawValue')))


        actionData = item.get('ActionData')
        if actionData is not None:
            actions = actionData.get('Actions')
            if actions is not None:
                for action in actions:
                    for criterion in action.get('Criteria'):
                        # crit = Criterion(value1=criterion['Value1'], value2=criterion['Value2'], operator=criterion['Operator'])
                        criteria.append((criterion['Value1'], criterion['Value2'], criterion['Operator']))

        for spellData in item.get('SpellData'):
            
            for spell in spellData['Items']:

                for criterion in spell['Criteria']:
                    # crit = Criterion(value1=criterion['Value1'], value2=criterion['Value2'], operator=criterion['Operator'])
                    criteria.append((criterion['Value1'], criterion['Value2'], criterion['Operator']))

        animesh = item.get('AnimationMesh')
        if animesh is not None:
            animation = animesh.get('Animation')
            if animation is not None:
                # sv = StatValue(stat=animation['Stat'], value=animation['RawValue'])
                statVals.append((animation['Stat'], animation['RawValue']))
            mesh = animesh.get('Mesh')
            if mesh is not None:
                # sv = StatValue(stat=mesh['Stat'], value=mesh['RawValue'])
                statVals.append((mesh['Stat'], mesh['RawValue']))

        idx += 1

    return statVals, criteria

def make_statvalues(data):
    data = list(set(data))
    statVals = []
    for item in data:
        sv = StatValue(stat=item[0], value=item[1])
        statVals.append(sv)

    return statVals

def make_criterion(data):
    data = list(set(data))
    criteria = []
    for item in data:
        crit = Criterion(value1=item[0], value2=item[1], operator=item[2])
        criteria.append(crit)

    return criteria

chunkSize = 100

if __name__ == "__main__":

    print('Getting Item Singletons...')
    with open('items.json', 'r') as fd:
        itemData = json.loads(fd.read())

    itemSV, itemCrit = get_singletons(itemData)

    print('Getting Nano Singletons...')
    with open('nanos.json', 'r') as fd:
        nanoData = json.loads(fd.read())

    nanoSV, nanoCrit = get_singletons(nanoData)

    statVals = itemSV + nanoSV
    criteria = itemCrit + nanoCrit

    print('Creating StatValue and Criterion')
    statVals = make_statvalues(statVals)
    criteria = make_criterion(criteria)

    print('Sending StatValue and Criterion')
    StatValue.objects.bulk_create(statVals)
    Criterion.objects.bulk_create(criteria)


    itemChunks = [itemData[i:i + chunkSize] for i in range(0, len(itemData), chunkSize)]

    print('Importing items...')

    db.connections.close_all()
    with Pool(15) as pool:
        pool.map(import_items, itemChunks)
    
    nanoChunks = [nanoData[i:i + chunkSize] for i in range(0, len(nanoData), chunkSize)]

    print('Importing nanos...')
    db.connections.close_all()
    with Pool(15) as pool:
        pool.map(import_nanos, nanoChunks)



        

    # breakpoint()
    

    


        

