from django.db import models
from user.models import InventoryItem
from user.models import User



# Create your models here.
class Rack(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="racks")
    name = models.CharField(max_length=80, blank=False)
    bay = models.IntegerField(blank=False, null=False)


    def __str__(self):
        return f" {self.name}"


class Bay(models.Model):
    name = models.CharField(max_length=80, blank=False)
    rack = models.ForeignKey(Rack, on_delete=models.CASCADE, related_name="bays")
    is_active = models.BooleanField(default=False)
    last_time_active = models.DateTimeField(null=True)


    cpu = models.ForeignKey(InventoryItem, on_delete=models.SET_NULL, null=True, blank=True, related_name="cpu_bay")
    ssd = models.ForeignKey(InventoryItem, on_delete=models.SET_NULL, null=True, blank=True, related_name="ssd_bay")
    
    gpu1 = models.ForeignKey(InventoryItem, on_delete=models.SET_NULL, null=True, blank=True, related_name="gpu_bay1")
    gpu2 = models.ForeignKey(InventoryItem, on_delete=models.SET_NULL, null=True, blank=True, related_name="gpu_bay2")
    gpu3 = models.ForeignKey(InventoryItem, on_delete=models.SET_NULL, null=True, blank=True, related_name="gpu_bay3")
    
    ram1 = models.ForeignKey(InventoryItem, on_delete=models.SET_NULL, null=True, blank=True, related_name="ram_bay1")
    ram2 = models.ForeignKey(InventoryItem, on_delete=models.SET_NULL, null=True, blank=True, related_name="ram_bay2")
    ram3 = models.ForeignKey(InventoryItem, on_delete=models.SET_NULL, null=True, blank=True, related_name="ram_bay3")


    def __str__(self):
        return f" {self.name}"

