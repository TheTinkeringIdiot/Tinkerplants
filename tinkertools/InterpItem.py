from tinkertools.models import *
from tinkertools.utils import *

class InterpItem:
    aoid = 0
    lo_item = None
    hi_item = None

    name = ''
    description = ''
    is_nano = False
    itemClass = 0

    ql = 0
    low_ql = 0
    high_ql = 0
    ql_delta = 0
    ql_delta_full = 0
    interpolating = False

    actions = []
    spellData = []
    
    def __init__(self, aoid, ql = 0):
        item = Item.objects.get(aoid=aoid)
        self.actions = []
        self.spellData = []

        # matching description and name together accounts for implants with the same name
        items = Item.objects.filter(name=item.name, description=item.description).order_by('ql').all()
        
        if items[len(items)-1].ql == item.ql or len(items) == 1: # No interpolation
            self.lo_item = item
            self.ql = item.ql
            self.low_ql = item.ql
            self.high_ql = item.ql

        else:
            self.interpolating = True
            
            if ql == 0: # QL not specified, default to lowest QL for this item
                ql = items[0].ql

            for i in range(len(items)):
                if items[i].ql <= ql and items[i+1].ql > ql:
                    self.lo_item = items[i]
                    self.hi_item = items[i+1]

            self.ql = ql
            self.ql_delta_full = self.hi_item.ql - self.lo_item.ql
            self.ql_delta = ql - self.lo_item.ql
            self.low_ql = self.lo_item.ql
            self.high_ql = self.hi_item.ql - 1

        self.name = self.lo_item.name
        self.description = self.lo_item.description
        self.aoid = self.lo_item.aoid
        self.is_nano = self.lo_item.is_nano
        self.itemClass = self.lo_item.itemClass
        self.atkdef = self.lo_item.atkdef

        for lo_actionData in self.lo_item.actions.all():
            if self.interpolating:
                hi_actionData = self.hi_item.actions.filter(action=lo_actionData.action).first()
                self.actions.append(self.InterpAction(self, lo_actionData, hi_actionData))
            else:
                self.actions.append(self.InterpAction(self, lo_actionData))

        for lo_spellData in self.lo_item.spellData.all():
            if self.interpolating:
                hi_spellData = self.hi_item.spellData.filter(event=lo_spellData.event).first()
                self.spellData.append(self.InterpSpell(self, lo_spellData, hi_spellData))
            else:
                self.spellData.append(self.InterpSpell(self, lo_spellData))

            
    def stats(self):
        if not self.interpolating:
            for stat in self.lo_item.stats.all():
                yield stat
        
        else:
            for lo_stat in self.lo_item.stats.all():
                hi_stat = self.hi_item.stats.filter(stat=lo_stat.stat).first()

                if lo_stat == hi_stat:
                    yield lo_stat

                elif lo_stat.stat in INTERP_STATS:
                    newval = self.interpolate_value(lo_stat.value, hi_stat.value)
                    yield StatValue(stat=lo_stat.stat, value=newval)

                else:
                    yield lo_stat

    def interpolate_value(self, lo_val, hi_val):
        val_per_ql = (hi_val - lo_val) / self.ql_delta_full
        newval = round(lo_val + (val_per_ql * self.ql_delta))
        return newval

    class InterpAction: # Inner class for actions and criterion
        outer = None
        action = 0
        criterions = []

        def __init__(self, outer, lo_actionData, hi_actionData = None):
            self.outer = outer
            self.action = lo_actionData.action
            self.criterions = []

            if self.outer.interpolating and hi_actionData is not None:
                lo_criteria = [x.criterion for x in lo_actionData.actioncriterion_set.order_by('order').select_related('criterion').all()]
                hi_criteria = [x.criterion for x in hi_actionData.actioncriterion_set.order_by('order').select_related('criterion').all()]

                for idx, lo_crit in enumerate(lo_criteria):
                    hi_crit = hi_criteria[idx]

                    if lo_crit == hi_crit:
                        self.criterions.append(lo_crit)

                    elif lo_crit.value1 == hi_crit.value1 and lo_crit.value1 in INTERP_STATS:
                        newVal2 = self.outer.interpolate_value(lo_crit.value2, hi_crit.value2)
                        self.criterions.append(Criterion(value1=lo_crit.value1, value2=newVal2, operator=lo_crit.operator))

                    else:
                        self.criterions.append(lo_crit)

            else:
                self.criterions.extend([x.criterion for x in lo_actionData.actioncriterion_set.order_by('order').select_related('criterion').all()])


        def criteria(self):
            for criterion in self.criterions:
                yield criterion

    class InterpSpell: # Inner class for SpellData and Spells
        outer = None
        event = 0
        interpSpells = []

        def __init__(self, outer, lo_spellData, hi_spellData = None):
            self.outer = outer
            self.event = lo_spellData.event
            self.interpSpells = []

            if self.outer.interpolating and hi_spellData is not None:
                lo_spells = [x for x in lo_spellData.spells.all()]

                for lo_spell in lo_spells:
                    if lo_spell.spellID in [53012, 53014, 53045, 53175]: # Stat | Amount
                        hi_spell = hi_spellData.spells.filter(spellID=lo_spell.spellID, spellParams__Stat=lo_spell.spellParams['Stat']).first()
                        newVal = self.outer.interpolate_value(lo_spell.spellParams['Amount'], hi_spell.spellParams['Amount'])

                        newSpell = Spell(
                            target = lo_spell.target,
                            tickCount = lo_spell.tickCount,
                            tickInterval = lo_spell.tickInterval,
                            spellID = lo_spell.spellID,
                            spellParams = lo_spell.spellParams,
                            criteria = lo_spell.criteria
                            )
                        newSpell.spellParams['Amount'] = newVal 
                        self.interpSpells.append(newSpell)

                    elif lo_spell.spellID in [53026, 53028]: # Skill | Amount
                        hi_spell = hi_spellData.spells.filter(spellID=lo_spell.spellID, spellParams__Stat=lo_spell.spellParams['Skill']).first()
                        newVal = self.outer.interpolate_value(lo_spell.spellParams['Amount'], hi_spell.spellParams['Amount'])

                        newSpell = Spell(
                            target = lo_spell.target,
                            tickCount = lo_spell.tickCount,
                            tickInterval = lo_spell.tickInterval,
                            spellID = lo_spell.spellID,
                            spellParams = lo_spell.spellParams,
                            criteria = lo_spell.criteria
                            )
                        newSpell.spellParams['Amount'] = newVal 
                        self.interpSpells.append(newSpell)

                    elif lo_spell.spellID in [53184, 53237]: # Stat | Percent
                        hi_spell = hi_spellData.spells.filter(spellID=lo_spell.spellID, spellParams__Stat=lo_spell.spellParams['Stat']).first()
                        newVal = self.outer.interpolate_value(lo_spell.spellParams['Percent'], hi_spell.spellParams['Percent'])

                        newSpell = Spell(
                            target = lo_spell.target,
                            tickCount = lo_spell.tickCount,
                            tickInterval = lo_spell.tickInterval,
                            spellID = lo_spell.spellID,
                            spellParams = lo_spell.spellParams,
                            criteria = lo_spell.criteria
                            )
                        newSpell.spellParams['Percent'] = newVal 
                        self.interpSpells.append(newSpell)

                    else:
                        self.interpSpells.append(lo_spell)

            else:
                self.interpSpells.extend([x for x in lo_spellData.spells.all()])

        def spells(self):
            for spell in self.interpSpells:
                yield spell
            




            



