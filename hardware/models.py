from django.conf import settings
from django.db import models


class HardwareBrand(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Hardware(models.Model):
    
    class Type(models.TextChoices):
        GPU = "cpu", "CPU"
        SSD = "ssd", "SSD"
        RAM = "ram", "RAM"
        CPU = "cpu", "CPU"
    
    name = models.CharField(max_length=100, unique=True)
    brand = models.ForeignKey('HardwareBrand', on_delete=models.PROTECT)
    type = models.CharField(max_length=10, choices=Type.choices)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    watts = models.IntegerField()
    rarity = models.CharField(max_length=30)
    
    class Meta:
        ordering = ["type", "price"]

        
    def __str__(self):
        return f"{self.brand.name} {self.name}"


class CPU(models.Model):
    hardware = models.OneToOneField(Hardware, on_delete=models.CASCADE, related_name="cpu_specs")
    cores = models.PositiveIntegerField()
    threads = models.PositiveIntegerField()
    cpu_ghz = models.IntegerField()
    cpu_score_bottleneck = models.IntegerField()



class GPU(models.Model):
    hardware = models.OneToOneField(Hardware, on_delete=models.CASCADE, related_name="gpu_specs")
    gpu_score_bottleneck = models.PositiveIntegerField()
    vram_gb = models.PositiveIntegerField()
    gpu_mhz = models.PositiveIntegerField()

    

class RAM(models.Model):
    hardware = models.OneToOneField(Hardware, on_delete=models.CASCADE, related_name="ram_specs")
    capacity_gb = models.IntegerField()
    frequency_mhz = models.IntegerField()



class SSD(models.Model):
    hardware = models.OneToOneField(Hardware, on_delete=models.CASCADE, related_name="ssd_specs")
    capacity_gb = models.PositiveIntegerField()
    speed = models.PositiveIntegerField()


class HardwareInstance(models.Model):
    owner = models.ForeignKey("user.User", on_delete=models.CASCADE, related_name="hardware_instances")
    hardware = models.ForeignKey(Hardware,on_delete=models.PROTECT,related_name="instances",)
    is_equiped = models.BooleanField(default=False)
    type = models.CharField(max_length=20, blank=False, default="inventory_item")

    def __str__(self):
        return f"{self.item.model} (Equipped: {self.is_equiped})"