from django.db import models

class Brand(models.Model):
    name = models.CharField(max_length=100, null=False)

class Hardware(models.Model):
    type = models.CharField(max_length=300)
    model = models.CharField(max_length=100)
    brand = models.ForeignKey('Brand', on_delete=models.CASCADE)
    price = models.IntegerField()
    watts = models.IntegerField()
    is_active = models.BooleanField(default=False)
    
    
class CPU(Hardware):
    cores = models.IntegerField()
    threads = models.IntegerField()
    ghz = models.FloatField()
    score_bottleneck = models.IntegerField()
    
class GPU(Hardware):
    score_bottleneck = models.IntegerField()
    vram = models.IntegerField()
    mhz = models.FloatField()
    
class RAM(Hardware):
    gb = models.IntegerField()
    mhz = models.IntegerField()

class SSD(Hardware):
    gb = models.IntegerField()
    speed = models.IntegerField()

