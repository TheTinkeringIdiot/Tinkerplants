from django.db import models

# Create your models here.

class Cluster(models.Model):
    ql = models.IntegerField()
    clusterslot = models.IntegerField()
    impslot = models.IntegerField()
    skill = models.CharField(max_length=32)
    loval = models.IntegerField(default=0)
    hival = models.IntegerField(default=0)
    jobeskill = models.CharField(max_length=32)
    npmod = models.FloatField()
    jobemod = models.FloatField()

class Implant(models.Model):
    aoid = models.IntegerField()
    name = models.CharField(max_length=256)
    ql = models.IntegerField()
    slot = models.IntegerField()
    icon = models.IntegerField()
    shiny = models.CharField(max_length=32)
    bright = models.CharField(max_length=32)
    faded = models.CharField(max_length=32)
    reqs = models.JSONField()
    



# class AODB(models.Model):
#     xid = models.IntegerField()
#     hash = models.IntegerField()
#     metatype = models.CharField(max_length=1)
#     aoid = models.IntegerField()
#     patch = models.IntegerField()
#     current = models.BooleanField()
#     flags = models.IntegerField()
#     props = models.IntegerField()
#     ql = models.IntegerField()
#     type = models.IntegerField()
#     slot = models.IntegerField()
#     patchadded = models.IntegerField()
#     name = models.CharField(max_length=256)
#     info = models.CharField(max_length=4096)

# class AODB_EFF(models.Model):
#     xid = models.IntegerField()
#     hook = models.IntegerField()
#     type = models.IntegerField()
#     reqid = models.IntegerField()
#     hits = models.IntegerField()
#     delay = models.IntegerField()
#     target = models.IntegerField()
#     value1 = models.IntegerField()
#     value2 = models.IntegerField()
#     value3 = models.IntegerField()
#     value4 = models.IntegerField()
#     value5 = models.IntegerField()
#     test = models.CharField(max_length=1024)

# class AODB_EXT(models.Model):
#     xid = models.IntegerField()
#     icon = models.IntegerField()
#     defslot = models.IntegerField()
#     value = models.IntegerField()
#     tequip = models.IntegerField()
#     tattack = models.IntegerField()
#     trecharge = models.IntegerField()
#     dmin = models.IntegerField()
#     dmax = models.IntegerField()
#     dcrit = models.IntegerField()
#     dtype = models.IntegerField()
#     clip = models.IntegerField()
#     atype = models.IntegerField()
#     duration = models.IntegerField()
#     range = models.IntegerField()




