from django.db import models

class naomi(models.Model):
    id = models.IntegerField(primary_key=True)
    uid = models.CharField(max_length=100)
    qn = models.IntegerField(default=0)

class rank(models.Model):
    id = models.IntegerField(primary_key=True)
    uid = models.CharField(max_length=100)
    rank = models.IntegerField(default=0)