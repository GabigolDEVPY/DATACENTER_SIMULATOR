from django.db import models
from django.core.exceptions import ValidationError
from hardware.models import RAM, CPU, GPU, SSD

# Create your models here.
class Rack(models.Model):
    name = models.CharField(max_length=80, blank=False)
    bay = models.IntegerField(blank=False, null=False)
    
    
    def __str__(self):
        return f" {self.name}"    


class Bay(models.Model):
    name = models.CharField(max_length=80, blank=False)
    rack = models.ForeignKey(Rack, on_delete=models.CASCADE, related_name="bays")
    
    class WattsTier(models.TextChoices):
        VERY_LOW = "1KW", "Very Low (1KW)" 
        LOW = "2KW", "Low (2KW)" 
        MEDIUM = "4KW", "Medium (4KW)" 
        HIGH = "8KW", "HIGH (8KW)" 
        VERY_HIGH = "16KW", "HIGH (16KW)" 
    
    is_active = models.BooleanField(default=False)    
    watts = models.CharField(max_length=10, choices=WattsTier.choices, default=WattsTier.LOW)
    
    WATTS_PRICE = {
        WattsTier.VERY_LOW: 12000,
        WattsTier.LOW: 28000,
        WattsTier.MEDIUM: 58000,
        WattsTier.HIGH: 120000,
        WattsTier.VERY_HIGH: 280000,
    }
    
    RAM = models.ForeignKey(RAM, on_delete=models.CASCADE, null=True, blank=True)
    CPU = models.ForeignKey(CPU, on_delete=models.CASCADE, null=True, blank=True)
    GPU = models.ForeignKey(GPU, on_delete=models.CASCADE, null=True, blank=True)
    SSD = models.ForeignKey(SSD, on_delete=models.CASCADE, null=True, blank=True)
    
    
    @property
    def price(self):
        return self.WATTS_PRICE.get(self.watts, 0)

    def __str__(self):
        return f" {self.name}"