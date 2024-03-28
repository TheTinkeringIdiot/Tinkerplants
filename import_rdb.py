
import os, json, asyncio
import django
from django import db
from django.db import connection
from multiprocessing import Pool
from tinkerplants.utils import *

os.environ['DJANGO_SETTINGS_MODULE'] = 'aobase.settings'
django.setup()

from tinkertools.models import *

class RDBImporter:
    itemData = None
    nanoData = None
    totalData = None

    chunkSize = 100

    items = []
    statValues = []
    itemStatValues = []
    atkdefs = []
    atkdefAttacks = []
    atkdefDefenses = []
    actions = []
    actionCriterions = []
    criteria = []
    itemShopHashes = []
    shopHashes = []
    aniMeshes = []

    spellTuples = []
    itemSpellDatas = []
    spellDatas = []
    spellDataSpell = []
    spells = []
    spellCriteria = []

    def __init__(self, itemData, nanoData):
        self.itemData = itemData
        self.nanoData = nanoData
        self.totalData = itemData + nanoData

        print('Initializing DB...')
        self.initDB()

        print('Getting Item Singletons...')
        itemSV, itemCrit, itemHashes = self.get_singletons(itemData)

        print('Getting Nano Singletons...')
        nanoSV, nanoCrit, nanoHashes = self.get_singletons(nanoData)

        statVals = list(set(itemSV + nanoSV))
        criteria = list(set(itemCrit + nanoCrit))
        hashes = list(set(itemHashes + nanoHashes))

        print('Creating StatValue, Criterion, and ShopHash')
        self.statValues = self.makeStatValues(statVals)
        self.criteria = self.makeCriterions(criteria)
        self.shopHashes = self.makeShopHashes(hashes)

        print('Sending StatValue, Criterion, and ShopHash')
        StatValue.objects.bulk_create(self.statValues)
        Criterion.objects.bulk_create(self.criteria)
        ShopHash.objects.bulk_create(self.shopHashes)

        print('Getting AnimationMeshes...')
        anituples = self.get_animeshes(itemData + nanoData)
        anituples = list(set(anituples))
        self.aniMeshes = self.makeAnimationMeshes(anituples)

        print('Sending AnimationMeshes...')
        AnimationMesh.objects.bulk_create(self.aniMeshes)

        print('Getting Spells...')
        spelltuples = self.get_spells(self.itemData)
        # breakpoint()
        self.spellTuples = list(set(spelltuples))
        self.spells, self.spellCriteria = self.makeSpells(self.spellTuples)

        print('Sending Spells...')
        # breakpoint()
        Spell.objects.bulk_create(self.spells)
        Spell.criteria.through.objects.bulk_create(self.spellCriteria, ignore_conflicts=True)

        # breakpoint()


        itemChunks = [self.totalData[i:i + self.chunkSize] for i in range(0, len(self.totalData), self.chunkSize)]

        print('Importing items...')

        # result = self.import_items(itemData)
        # asyncio.run(result)
        self.import_items(self.totalData)

        # breakpoint()

        print('Sending Items...')
        Item.objects.bulk_create(self.items)
        Item.stats.through.objects.bulk_create(self.itemStatValues, ignore_conflicts=True)
        Item.shopHash.through.objects.bulk_create(self.itemShopHashes, ignore_conflicts=True)
        Item.spellData.through.objects.bulk_create(self.itemSpellDatas, ignore_conflicts=True)

        AttackDefense.attack.through.objects.bulk_create(self.atkdefAttacks, ignore_conflicts=True)
        AttackDefense.defense.through.objects.bulk_create(self.atkdefDefenses, ignore_conflicts=True)
        AttackDefense.objects.bulk_create(self.atkdefs)

        Action.objects.bulk_create(self.actions)
        ActionCriterion.objects.bulk_create(self.actionCriterions, ignore_conflicts=True)
        
        # print('Importing nanos...')
        # result = import_nanos(nanoData)
        # asyncio.run(result)

        # db.connections.close_all()
        # with Pool(15) as pool:
        #     result = pool.map(self.import_items, itemChunks)


    def initDB(self):
        
        self.clearTables()
        self.resetCounters()

    def clearTables(self):
        # Clear out the old data entirely
        StatValue.objects.all().delete()
        Criterion.objects.all().delete()
        Spell.objects.all().delete()
        SpellData.objects.all().delete()
        AttackDefense.objects.all().delete()
        AnimationMesh.objects.all().delete()
        Item.objects.all().delete()
        Action.objects.all().delete()

    def resetCounters(self):
        with connection.cursor() as cursor:

            # python3 manage.py sqlsequencereset tinkertools
            cursor.execute('''
                BEGIN;
                SELECT setval(pg_get_serial_sequence('"tinkertools_statvalue"','id'), coalesce(max("id"), 1), max("id") IS NOT null) FROM "tinkertools_statvalue";
                SELECT setval(pg_get_serial_sequence('"tinkertools_criterion"','id'), coalesce(max("id"), 1), max("id") IS NOT null) FROM "tinkertools_criterion";
                SELECT setval(pg_get_serial_sequence('"tinkertools_spell_criteria"','id'), coalesce(max("id"), 1), max("id") IS NOT null) FROM "tinkertools_spell_criteria";
                SELECT setval(pg_get_serial_sequence('"tinkertools_spell"','id'), coalesce(max("id"), 1), max("id") IS NOT null) FROM "tinkertools_spell";
                SELECT setval(pg_get_serial_sequence('"tinkertools_spelldata_spells"','id'), coalesce(max("id"), 1), max("id") IS NOT null) FROM "tinkertools_spelldata_spells";
                SELECT setval(pg_get_serial_sequence('"tinkertools_spelldata"','id'), coalesce(max("id"), 1), max("id") IS NOT null) FROM "tinkertools_spelldata";
                SELECT setval(pg_get_serial_sequence('"tinkertools_attackdefense_attack"','id'), coalesce(max("id"), 1), max("id") IS NOT null) FROM "tinkertools_attackdefense_attack";
                SELECT setval(pg_get_serial_sequence('"tinkertools_attackdefense_defense"','id'), coalesce(max("id"), 1), max("id") IS NOT null) FROM "tinkertools_attackdefense_defense";
                SELECT setval(pg_get_serial_sequence('"tinkertools_attackdefense"','id'), coalesce(max("id"), 1), max("id") IS NOT null) FROM "tinkertools_attackdefense";
                SELECT setval(pg_get_serial_sequence('"tinkertools_animationmesh"','id'), coalesce(max("id"), 1), max("id") IS NOT null) FROM "tinkertools_animationmesh";
                SELECT setval(pg_get_serial_sequence('"tinkertools_shophash"','id'), coalesce(max("id"), 1), max("id") IS NOT null) FROM "tinkertools_shophash";
                SELECT setval(pg_get_serial_sequence('"tinkertools_item_stats"','id'), coalesce(max("id"), 1), max("id") IS NOT null) FROM "tinkertools_item_stats";
                SELECT setval(pg_get_serial_sequence('"tinkertools_item_spellData"','id'), coalesce(max("id"), 1), max("id") IS NOT null) FROM "tinkertools_item_spellData";
                SELECT setval(pg_get_serial_sequence('"tinkertools_item_shopHash"','id'), coalesce(max("id"), 1), max("id") IS NOT null) FROM "tinkertools_item_shopHash";
                SELECT setval(pg_get_serial_sequence('"tinkertools_item"','id'), coalesce(max("id"), 1), max("id") IS NOT null) FROM "tinkertools_item";
                SELECT setval(pg_get_serial_sequence('"tinkertools_action"','id'), coalesce(max("id"), 1), max("id") IS NOT null) FROM "tinkertools_action";
                SELECT setval(pg_get_serial_sequence('"tinkertools_actioncriterion"','id'), coalesce(max("id"), 1), max("id") IS NOT null) FROM "tinkertools_actioncriterion";
                COMMIT;
            ''')

    def import_items(self, chunk):
        asyncio.run(self.import_rdb(chunk))

    def import_nanos(self, chunk):
        asyncio.run(self.import_rdb(chunk, True))

    def import_rdb(self, data):

        item_idx = 0
        for item in data:
            if item_idx % 1000 == 0:
                print(f'Item {item_idx}...')
            # newItem, created = await Item.objects.aget_or_create(aoid = item['AOID'])
            item_idx += 1
            newItem = Item(id=item_idx)

            newItem.name = item.get('Name')
            newItem.description = item.get('Description')
            nano = item.get('Nano')
            if nano is not None:
                newItem.is_nano = True
            else:
                newItem.is_nano = False

            # await newItem.asave()

            # breakpoint()

            for sv in item.get('StatValues'):
                stat = sv.get('Stat')
                value = sv.get('RawValue')
                if stat == 76:
                    newItem.itemClass = value
                elif stat == 54:
                    newItem.ql = value
                # statValue, create = StatValue.objects.get_or_create(stat=stat, value=value)
                self.itemStatValues.append(Item.stats.through(item_id=newItem.id, statvalue_id=self.statValues.index(StatValue(stat=stat, value=value)) + 1))
                # await newItem.stats.aadd(self.statValues.index(StatValue(stat=stat, value=value)) + 1)

            if newItem.ql is None:
                newItem.ql = 1

            if newItem.itemClass is None:
                newItem.itemClass = 0

            atkdef = item.get('AttackDefenseData')
            if atkdef is not None:
                newAtkDef = AttackDefense(id=len(self.atkdefs) + 1)
                # await newAtkDef.asave()
                for atk in atkdef.get('Attack'):
                    # sv, create = StatValue.objects.get_or_create(stat=atk.get('Stat'), value=atk.get('RawValue'))
                    stat_idx = self.statValues.index(StatValue(stat=atk.get('Stat'), value=atk.get('RawValue'))) + 1
                    self.atkdefAttacks.append(AttackDefense.attack.through(attackdefense_id=newAtkDef.id, statvalue_id=stat_idx))
                    # newAtkDef.attack_id = self.statValues.index(StatValue(stat=atk.get('Stat'), value=atk.get('RawValue'))) + 1
                for atk in atkdef.get('Defense'):
                    # sv, create = StatValue.objects.get_or_create(stat=atk.get('Stat'), value=atk.get('RawValue'))
                    stat_idx = self.statValues.index(StatValue(stat=atk.get('Stat'), value=atk.get('RawValue'))) + 1
                    self.atkdefDefenses.append(AttackDefense.defense.through(attackdefense_id=newAtkDef.id, statvalue_id=stat_idx))
                    # newAtkDef.defense_id =self.statValues.index(StatValue(stat=atk.get('Stat'), value=atk.get('RawValue'))) + 1

                # await newAtkDef.asave()
                self.atkdefs.append(newAtkDef)
                newItem.atkdef_id = newAtkDef.id
                # atkdefs.append(newAtkDef)
                # newItem.atkdef_id = len(atkdefs)

            actionData = item.get('ActionData')
            if actionData is not None:
                actions = actionData.get('Actions')
                if actions is not None:
                    for action in actions:
                        newAction = Action(id=len(self.actions) + 1)
                        newAction.action = action['Action']
                        # await newAction.asave()
                        crit_idx = 0
                        for criterion in action.get('Criteria'):
                            ac = ActionCriterion(id=len(self.actionCriterions) + 1)
                            # crit, create = Criterion.objects.get_or_create(value1=criterion['Value1'], value2=criterion['Value2'], operator=criterion['Operator'])
                            crit = self.criteria.index(Criterion(value1=criterion['Value1'], value2=criterion['Value2'], operator=criterion['Operator'])) + 1
                            ac.action_id = newAction.id
                            ac.criterion_id = crit
                            ac.order = crit_idx
                            # actionCriteria.append(ac)
                            # await ac.asave()
                            self.actionCriterions.append(ac)
                            # await newAction.criteria.aadd(crit)

                            crit_idx += 1
                        
                        newAction.item_id = newItem.id
                        # actions.append(newAction)
                        # await newAction.asave()
                        self.actions.append(newAction)


            for spellData in item.get('SpellData'):
                newSpellData = SpellData(id=len(self.spellDatas) + 1)
                newSpellData.event = spellData['Event']
                # await newSpellData.asave()

                for spell in spellData['Items']:
                    interspell = spell.copy()
                    if spell.get('Item') is not None:
                        interspell['Item'] = spell['Item']['Text']
                    if spell.get('MonsterHash') is not None:
                        interspell['MonsterHash'] = spell['MonsterHash']['Text']
                    if spell.get('Quest') is not None and isinstance(spell['Quest'], dict) and spell['Quest'].get('Text') is not None:
                        interspell['Quest'] = spell['Quest']['Text']
                    if spell.get('B') is not None and isinstance(spell['B'], dict) and spell['B'].get('Text') is not None:
                        interspell['B'] = spell['B']['Text']
                    if spell.get('Spawnee') is not None:
                        interspell['Spawnee'] = spell['Spawnee']['Text']
                    if spell.get('Monster') is not None:
                        interspell['Monster'] = spell['Monster']['Text']
                    if spell.get('Auto3') is not None:
                        interspell['Auto3'] = spell['Auto3']['Text']

                    interspell['Criteria'] = tuple((x['Value1'], x['Value2'], x['Operator']) for x in spell['Criteria'])

                    spellString = frozenset(interspell.items())

                    spell_idx = self.spellTuples.index(spellString) + 1
                    self.spellDataSpell.append(SpellData.spells.through(spelldata_id=newSpellData.id, spell_id=spell_idx))
                    # await SpellData.spells.through.objects.acreate(spelldata_id=newSpellData.id, spell_id=spell_idx)
                self.spellDatas.append(newSpellData)
                self.itemSpellDatas.append(Item.spellData.through(item_id=newItem.id, spelldata_id=newSpellData.id))


                
                # for spell in spellData['Items']:
                #     newSpell = Spell()
                #     newSpell.spellID = spell['SpellID']
                #     spell.pop('SpellID', None)
                #     newSpell.target = spell['Target']
                #     spell.pop('Target', None)
                #     newSpell.tickCount = spell['TickCount']
                #     spell.pop('TickCount', None)
                #     newSpell.tickInterval = spell['TickInterval']
                #     spell.pop('TickInterval', None)
                #     newSpell.spellFormat = spell['SpellFormat']
                #     spell.pop('SpellFormat', None)
                #     await newSpell.asave()

                #     for criterion in spell['Criteria']:
                #         # crit, create = Criterion.objects.get_or_create(value1=criterion['Value1'], value2=criterion['Value2'], operator=criterion['Operator'])
                #         await newSpell.criteria.aadd(self.criteria.index(Criterion(value1=criterion['Value1'], value2=criterion['Value2'], operator=criterion['Operator'])) + 1)

                #     newSpell.spellParams = spell
                    # spells.append(newSpell)
                    # await newSpell.asave()
                    # newSpellData.spells.add(len(spells))
                # await newSpellData.asave()
                # spellDatas.append(newSpellData)
                
                # await newItem.spellData.aadd(newSpellData)

            shopHashData = item.get('ShopHashData')
            if shopHashData is not None:
                for shopItem in shopHashData['Items']:

                    hash_idx = (self.shopHashes.index(ShopHash(hash=shopItem['Hash']['Text'],
                                                                minLevel=shopItem['MinLevel'],
                                                                maxLevel=shopItem['MaxLevel'],
                                                                baseAmount=shopItem['BaseAmount'],
                                                                regenAmount=shopItem['RegenAmount'],
                                                                regenInterval=shopItem['RegenInterval'],
                                                                spawnChance=shopItem['SpawnChance'])) + 1)
                    self.itemShopHashes.append(Item.shopHash.through(item_id=newItem.id, shophash_id=hash_idx))

            animesh = item.get('AnimationMesh')
            if animesh is not None:
                # newAniMesh = await AnimationMesh.objects.acreate()
                animation = animesh.get('Animation')
                # await newAniMesh.asave()
                if animation is not None:
                    # sv, create = StatValue.objects.get_or_create(stat=animation['Stat'], value=animation['RawValue'])
                    # newAniMesh.animation_id = self.statValues.index(StatValue(stat=animation['Stat'], value=animation['RawValue'])) + 1
                    animation_id = self.statValues.index(StatValue(stat=animation['Stat'], value=animation['RawValue'])) + 1
                else:
                    animation_id = self.statValues.index(StatValue(stat=0, value=0)) + 1

                mesh = animesh.get('Mesh')
                if mesh is not None:
                    # sv, create = StatValue.objects.get_or_create(stat=mesh['Stat'], value=mesh['RawValue'])
                    # newAniMesh.mesh_id = self.statValues.index(StatValue(stat=mesh['Stat'], value=mesh['RawValue'])) + 1
                    mesh_id = self.statValues.index(StatValue(stat=mesh['Stat'], value=mesh['RawValue'])) + 1
                else:
                    mesh_id = self.statValues.index(StatValue(stat=0, value=0)) + 1
                # await newAniMesh.asave()
                animesh_id = self.aniMeshes.index(AnimationMesh(animation_id=animation_id, mesh_id=mesh_id)) + 1
                    
                # animeshes.append(newAniMesh)
                # newItem.animationMesh = newAniMesh
                newItem.animationMesh_id = animesh_id

            self.items.append(newItem)
            # await newItem.asave()

        # breakpoint()
            
    def get_spells(self, data):
        spells = []
        for item in data:
            for spellData in item.get('SpellData'):
                for spell in spellData['Items']:
                    interspell = spell.copy()
                    if spell.get('Item') is not None:
                        interspell['Item'] = spell['Item']['Text']
                    if spell.get('MonsterHash') is not None:
                        interspell['MonsterHash'] = spell['MonsterHash']['Text']
                    if spell.get('Quest') is not None and isinstance(spell['Quest'], dict) and spell['Quest'].get('Text') is not None:
                        interspell['Quest'] = spell['Quest']['Text']
                    if spell.get('B') is not None and isinstance(spell['B'], dict) and spell['B'].get('Text') is not None:
                        interspell['B'] = spell['B']['Text']
                    if spell.get('Spawnee') is not None:
                        interspell['Spawnee'] = spell['Spawnee']['Text']
                    if spell.get('Monster') is not None:
                        interspell['Monster'] = spell['Monster']['Text']
                    if spell.get('Auto3') is not None:
                        interspell['Auto3'] = spell['Auto3']['Text']

                    interspell['Criteria'] = tuple((x['Value1'], x['Value2'], x['Operator']) for x in spell['Criteria'])
                    # if len(interspell['Criteria']) > 0:
                    #     breakpoint()
                    # if item['AOID'] == 249883:
                    #     breakpoint()
                    try:
                        spells.append(frozenset(interspell.items()))
                    except:
                        breakpoint()

        return spells

    def get_animeshes(self, data):
        animeshes = []
        for item in data:
            animesh = item.get('AnimationMesh')
            if animesh is not None:
                animation = animesh.get('Animation')
                if animation is not None:   
                    anistat = animation.get('Stat')
                    anivalue = animation.get('RawValue')
                else:
                    anistat = 0
                    anivalue = 0

                mesh = animesh.get('Mesh')
                if mesh is not None:
                    meshstat = mesh.get('Stat')
                    meshvalue = mesh.get('RawValue')
                else:
                    meshstat = 0
                    meshvalue = 0

                animeshes.append((anistat, anivalue, meshstat, meshvalue))
        
        return animeshes

    def get_singletons(self, data):

        statVals = []
        criteria = []
        shopHashes = []

        for item in data:

            for sv in item.get('StatValues'):
                stat = sv.get('Stat')
                value = sv.get('RawValue')
                statVals.append((stat, value))

            atkdef = item.get('AttackDefenseData')
            if atkdef is not None:
                for atk in atkdef.get('Attack'):
                    statVals.append((atk.get('Stat'), atk.get('RawValue')))

                for atk in atkdef.get('Defense'):
                    statVals.append((atk.get('Stat'), atk.get('RawValue')))


            actionData = item.get('ActionData')
            if actionData is not None:
                actions = actionData.get('Actions')
                if actions is not None:
                    for action in actions:
                        for criterion in action.get('Criteria'):
                            criteria.append((criterion['Value1'], criterion['Value2'], criterion['Operator']))

            for spellData in item.get('SpellData'):
                
                for spell in spellData['Items']:

                    for criterion in spell['Criteria']:
                        criteria.append((criterion['Value1'], criterion['Value2'], criterion['Operator']))

            animesh = item.get('AnimationMesh')
            if animesh is not None:
                animation = animesh.get('Animation')
                if animation is not None:
                    statVals.append((animation['Stat'], animation['RawValue']))
                mesh = animesh.get('Mesh')
                if mesh is not None:
                    statVals.append((mesh['Stat'], mesh['RawValue']))

            shopHashData = item.get('ShopHashData')
            if shopHashData is not None:
                for shopItem in shopHashData['Items']:
                    shopHashes.append((shopItem['Hash']['Text'], 
                                    shopItem['MinLevel'], 
                                    shopItem['MaxLevel'], 
                                    shopItem['BaseAmount'], 
                                    shopItem['RegenAmount'], 
                                    shopItem['RegenInterval'], 
                                    shopItem['SpawnChance']))

        return statVals, criteria, shopHashes

    def makeStatValues(self, data):
        statVals = []
        for item in data:
            sv = StatValue(stat=item[0], value=item[1])
            statVals.append(sv)

        return statVals

    def makeCriterions(self, data):
        criteria = []
        for item in data:
            crit = Criterion(value1=item[0], value2=item[1], operator=item[2])
            criteria.append(crit)

        return criteria

    def makeShopHashes(self, data):
        shopHashes = []
        for item in data:
            sh = ShopHash(hash=item[0], minLevel=item[1], maxLevel=item[2], baseAmount=item[3], regenAmount=item[4], regenInterval=item[5], spawnChance=item[6])
            shopHashes.append(sh)

        return shopHashes
    
    def makeAnimationMeshes(self, data):
        animeshes = []
        for item in data:
            anim_id = self.statValues.index(StatValue(stat=item[0], value=item[1])) + 1
            mesh_id = self.statValues.index(StatValue(stat=item[2], value=item[3])) + 1
            ani = AnimationMesh(animation_id=anim_id, mesh_id=mesh_id)
            animeshes.append(ani)

        return animeshes
    
    def makeSpells(self, data):
        spells = []
        spellCrits = []
        for item in data:
            item = dict(item)
            criteria = [{'Value1' : x[0], 'Value2' : x[1], 'Operator' : x[2]} for x in item['Criteria']]
            
            newSpell = Spell()
            newSpell.spellID = item['SpellID']
            item.pop('SpellID', None)
            newSpell.target = item['Target']
            item.pop('Target', None)
            newSpell.tickCount = item['TickCount']
            item.pop('TickCount', None)
            newSpell.tickInterval = item['TickInterval']
            item.pop('TickInterval', None)
            newSpell.spellFormat = item['SpellFormat']
            item.pop('SpellFormat', None)

            spell_idx = len(spells) + 1 # plus the one about to be added, plus one for len counter
            # if spell_idx == 60:
            #     breakpoint()
            for criterion in criteria:
                # crit, create = Criterion.objects.get_or_create(value1=criterion['Value1'], value2=criterion['Value2'], operator=criterion['Operator'])
                crit_idx = self.criteria.index(Criterion(value1=criterion['Value1'], value2=criterion['Value2'], operator=criterion['Operator'])) + 1
                spellCrit = Spell.criteria.through(spell_id=spell_idx, criterion_id=crit_idx)
                spellCrits.append(spellCrit)

            item.pop('Criteria', None)
            newSpell.spellParams = item

            spells.append(newSpell)

        return spells, spellCrits


if __name__ == "__main__":

    print('Loading Data...')
    with open('items.json', 'r') as fd:
        itemData = json.loads(fd.read())

    with open('nanos.json', 'r') as fd:
        nanoData = json.loads(fd.read())

    for item in nanoData:
        item['Nano'] = True

    importer = RDBImporter(itemData, nanoData)


    
    

    

    


    # itemChunks = [itemData[i:i + chunkSize] for i in range(0, len(itemData), chunkSize)]

    # print('Importing items...')

    # # result = import_items(itemData)
    # # asyncio.run(result)

    # # print('Importing nanos...')
    # # result = import_nanos(nanoData)
    # # asyncio.run(result)

    # db.connections.close_all()
    # with Pool(15) as pool:
    #     result = pool.map(import_items, itemChunks)

    # nanoChunks = [nanoData[i:i + chunkSize] for i in range(0, len(nanoData), chunkSize)]

    # print('Importing nanos...')
    # db.connections.close_all()
    # with Pool(15) as pool:
    #     result = pool.map(import_nanos, nanoChunks)



        

    # breakpoint()
    

    


        

