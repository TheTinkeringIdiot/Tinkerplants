from django.db import models

# Create your models here.
class Symbiant(models.Model):
    aoid = models.IntegerField()
    ql = models.IntegerField()
    name = models.CharField(max_length=256)
    slot = models.CharField(max_length=32)
    family = models.CharField(max_length=32)
    reqs = models.JSONField()
    effects = models.JSONField()

class Pocketboss(models.Model):
    name = models.CharField(max_length=32)
    level = models.IntegerField()
    playfield = models.CharField(max_length=128)
    location = models.CharField(max_length=265)
    mobs = models.CharField(max_length=256)
    drops = models.ManyToManyField(Symbiant, related_name='dropped_by')

