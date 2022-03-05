from django.db import models

# Create your models here.
class Nano(models.Model):
    name = models.CharField(max_length=64)
    ql = models.IntegerField()
    mc = models.IntegerField(default=0)
    attack = models.IntegerField(default=0)
    recharge = models.IntegerField(default=0)
    cost = models.IntegerField()
    low_dmg = models.IntegerField()
    high_dmg = models.IntegerField()
    ac = models.CharField(max_length=32)
    nr_pct = models.IntegerField(default=0)
    atk_cap = models.IntegerField(default=0)
    spec = models.IntegerField(default=0)
    deck = models.IntegerField(default=0)
    level = models.IntegerField(default=0)

