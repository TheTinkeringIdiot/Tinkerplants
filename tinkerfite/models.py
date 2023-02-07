from django.db import models

# Create your models here.

class Weapon(models.Model):
    aoid = models.IntegerField()
    ql = models.IntegerField()
    name = models.CharField(max_length=256)
    atk_time = models.IntegerField()
    rech_time = models.IntegerField()
    dmg_min = models.IntegerField()
    dmg_max = models.IntegerField()
    dmg_crit = models.IntegerField()
    dmg_type = models.IntegerField(default=0)
    clipsize = models.IntegerField()
    props = models.JSONField()
    reqs = models.JSONField()
    atk_skills = models.JSONField()
    other = models.JSONField()