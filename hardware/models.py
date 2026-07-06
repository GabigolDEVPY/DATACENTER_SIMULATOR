from django.db import models

# Create your models here.
class CPU(models.Model):
    type = models.CharField(max_length=300)
    model = models.CharField(max_length=100)
    brand = models.ForeignKey('Brand', on_delete=models.CASCADE)
    price = models.IntegerField()
    watts = models.IntegerField()
    is_active = models.BooleanField(default=False)
    score_bottleneck = models.IntegerField()
    
class GPU(models.Model):
    type = models.CharField(max_length=300)
    model = models.CharField(max_length=100)
    brand = models.ForeignKey('Brand', on_delete=models.CASCADE)
    price = models.IntegerField()
    watts = models.IntegerField()
    is_active = models.BooleanField(default=False)
    score_bottleneck = models.IntegerField()
    
class RAM(models.Model):
    type = models.CharField(max_length=300)
    model = models.CharField(max_length=100)
    brand = models.ForeignKey('Brand', on_delete=models.CASCADE)
    price = models.IntegerField()
    is_active = models.BooleanField(default=False)
    watts = models.IntegerField()
    
class SSD(models.Model):
    type = models.CharField(max_length=300)
    model = models.CharField(max_length=100)
    brand = models.ForeignKey('Brand', on_delete=models.CASCADE)
    price = models.IntegerField()
    is_active = models.BooleanField(default=False)
    watts = models.IntegerField()

class Brand(models.Model):
    name = models.CharField(max_length=100, null=False)