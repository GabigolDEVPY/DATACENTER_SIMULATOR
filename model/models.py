from django.db import models

# Create your models here.
class AIModel(models.Model):
    name = models.CharField(max_length=100)
    level = models.IntegerField(default=1)
    # Requisitos de hardware
    gpu_vram = models.IntegerField()         
    ram_gb = models.IntegerField()           
    storage_gb = models.IntegerField()      
    price = models.DecimalField(max_digits=10, decimal_places=2)
    base_revenue = models.DecimalField(max_digits=10, decimal_places=2)
    params = models.IntegerField() 
    
    def __str__(self):
        return f"{self.name} level: {self.level}"