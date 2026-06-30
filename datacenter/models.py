from django.db import models

# Create your models here.
class DataCenterHack(models.Model):
    bays = models.IntegerField(blank=False, null=False)