from django.db import models
from django.core.exceptions import ValidationError

# Create your models here.
class DataCenterHack(models.Model):
    name = models.CharField(max_length=80, blank=False)
    bay = models.IntegerField(blank=False, null=False)
    
    
    def __str__(self):
        return f" {self.name}"    


class Bay(models.Model):
    name = models.CharField(max_length=80, blank=False)
    data_center_hack = models.ForeignKey(DataCenterHack, on_delete=models.CASCADE, related_name="bays")
    
    class WattsTier(models.TextChoices):
        VERY_LOW = "1KW", "Very Low (1KW)" 
        LOW = "2KW", "Low (2KW)" 
        MEDIUM = "4KW", "Medium (4KW)" 
        HIGH = "8KW", "HIGH (8KW)" 
        VERY_HIGH = "16KW", "HIGH (16KW)" 
        
    watts = models.CharField(max_length=10, choices=WattsTier.choices, default=WattsTier.LOW)
    

    def __str__(self):
        return f" {self.name}"