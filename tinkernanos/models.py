from django.db import models

# Create your models here.
class Nano(models.Model):
    aoid = models.IntegerField()
    name = models.CharField(max_length=128)
    icon = models.CharField(max_length=12)
    school = models.CharField(max_length=24)
    strain = models.IntegerField()
    strain_name = models.CharField(max_length=32)
    profession = models.IntegerField(default=0)
    location = models.CharField(max_length=256)
    ql = models.IntegerField(default=1)
    spec = models.IntegerField(default=0)
    level = models.IntegerField(default=1)
    expansion = models.IntegerField(default=0)
    uploaded_by = models.JSONField(default=list)
    mm = models.IntegerField(default=0)
    bm = models.IntegerField(default=0)
    mc = models.IntegerField(default=0)
    ts = models.IntegerField(default=0)
    pm = models.IntegerField(default=0)
    si = models.IntegerField(default=0)


