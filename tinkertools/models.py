from django.db import models

# Create your models here.
class StatValue(models.Model):
    stat = models.IntegerField()
    value = models.IntegerField()

    class Meta:
        models.UniqueConstraint(
            fields = ['stat', 'value'],
            name = 'unique_stat_value'
        )

    def __eq__(self, other):
        return self.stat == other.stat and self.value == other.value
    
    def __hash__(self):
        return super().__hash__()

class Criterion(models.Model):
    value1 = models.IntegerField()
    value2 = models.IntegerField()
    operator = models.IntegerField()

    class Meta:
        models.UniqueConstraint(
            fields = ['value1', 'value2', 'operator'],
            name = 'unique_criterion'
        )

    def __eq__(self, other):
        return self.value1 == other.value1 and self.value2 == other.value2 and self.operator == other.operator
    
    def __hash__(self):
        return super().__hash__()

class Spell(models.Model):
    target = models.IntegerField(null=True)
    tickCount = models.IntegerField(null=True)
    tickInterval = models.IntegerField(null=True)
    spellID = models.IntegerField(null=True)
    spellFormat = models.CharField(max_length=512, null=True)
    criteria = models.ManyToManyField(Criterion)
    spellParams = models.JSONField(default=list)

class SpellData(models.Model):
    event = models.IntegerField(null=True)
    spells = models.ManyToManyField(Spell)

class AttackDefense(models.Model):
    attack = models.ManyToManyField(StatValue, related_name='atkdef_attack')
    defense = models.ManyToManyField(StatValue, related_name='atkdef_defense')

class AnimationMesh(models.Model):
    animation = models.ForeignKey(StatValue, on_delete=models.CASCADE, related_name='animesh_animation', null=True)
    mesh = models.ForeignKey(StatValue, on_delete=models.CASCADE, related_name='animesh_mesh', null=True)

class ShopHash(models.Model):
    hash = models.CharField(4)
    minLevel = models.IntegerField(null=True)
    maxLevel = models.IntegerField(null=True)
    baseAmount = models.IntegerField(null=True)
    regenAmount = models.IntegerField(null=True)
    regenInterval = models.IntegerField(null=True)
    spawnChance = models.IntegerField(null=True)

class Item(models.Model):
    aoid = models.IntegerField(null=True)
    name = models.CharField(max_length=128)
    ql = models.IntegerField(null=True)
    description = models.CharField(max_length=8192)
    itemClass = models.IntegerField(null=True)
    is_nano = models.BooleanField(default=False)
    stats = models.ManyToManyField(StatValue)
    atkdef = models.ForeignKey(AttackDefense, on_delete=models.CASCADE, null=True)
    animationMesh = models.ForeignKey(AnimationMesh, on_delete=models.CASCADE, null=True)
    spellData = models.ManyToManyField(SpellData)
    shopHash = models.ManyToManyField(ShopHash)

class Action(models.Model):
    action = models.IntegerField(null=True)
    criteria = models.ManyToManyField(Criterion, through='ActionCriterion')
    item = models.ForeignKey(Item, related_name='actions', on_delete=models.CASCADE, null=True)

class ActionCriterion(models.Model):
    action = models.ForeignKey(Action, on_delete=models.CASCADE, null=True)
    criterion = models.ForeignKey(Criterion, on_delete=models.CASCADE, null=True)
    order = models.IntegerField(null=True)



