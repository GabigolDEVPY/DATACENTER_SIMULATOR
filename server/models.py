from django.db import models
from user.models import InventoryItem
from user.models import User


class Datacenter(models.Model):
    name = models.CharField(max_length=80, blank=False)
    updates = models.IntegerField(blank=False, null=False, default=1)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="datacenter")

    def __str__(self):
        return f" {self.name}"

# Create your models here.
class Rack(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="racks")
    name = models.CharField(max_length=80, blank=False)
    bay = models.IntegerField(blank=False, null=False, default=16)
    position = models.IntegerField(blank=False, null=False, default=0)
    is_selected = models.BooleanField(default=False)
    type = models.CharField(max_length=20, blank=False, default="rack")


    def __str__(self):
        return f" {self.name}"


class Bay(models.Model):
    name = models.CharField(max_length=80, blank=False)
    rack = models.ForeignKey(Rack, on_delete=models.CASCADE, related_name="bays", null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bays")
    position = models.IntegerField(blank=False, null=False, default=0)
    is_selected = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    last_time_active = models.DateTimeField(null=True)
    type = models.CharField(max_length=20, blank=False, default="bay")


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

class StorageAllocation(models.Model):
    bay = models.ForeignKey(
        Bay,
        on_delete=models.CASCADE,
        related_name="storage_allocations"
    )

    ai_model = models.ForeignKey(
        "model.AIModel",
        on_delete=models.CASCADE,
        related_name="storage_allocations"
    )

    allocated_gb = models.BigIntegerField()
    




class EnergyEquipment(models.Model):
    class Type(models.TextChoices):
        SOLAR_PANEL = "solar", "Solar Panel"
        WIND_TURBINE = "turbina", "Wind Turbine"
        GENERATOR = "gerador", "Power Generator"
        CEMIG_ENERGY = "cemig", "CEMIG Energy"

    name = models.CharField(max_length=100)
    type = models.CharField(max_length=20, choices=Type.choices)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    max_level = models.PositiveSmallIntegerField(default=6)
    power_kw = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    maintenance_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    class Meta:
        ordering = ["type", "name"]

    def __str__(self):
        return self.name


class EnergyEquipmentLevel(models.Model):
    equipment = models.ForeignKey(EnergyEquipment, on_delete=models.CASCADE, related_name="levels")
    level = models.PositiveSmallIntegerField()
    power_kw = models.DecimalField(max_digits=10, decimal_places=2)
    upgrade_cost = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    class Meta:
        ordering = ["equipment", "level"]
        constraints = [
            models.UniqueConstraint(fields=["equipment", "level"], name="unique_level_per_equipment")
        ]

    def __str__(self):
        return f"{self.equipment.name} - Level {self.level}"


class CeilingCooler(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    max_level = models.PositiveSmallIntegerField(default=6)
    cooling_capacity_kw = models.DecimalField(max_digits=10, decimal_places=2, default=4)
    power_consumption_kw = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    maintenance_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class CeilingCoolerLevel(models.Model):
    cooler = models.ForeignKey(CeilingCooler, on_delete=models.CASCADE, related_name="levels")
    level = models.PositiveSmallIntegerField()
    cooling_capacity_kw = models.DecimalField(max_digits=10, decimal_places=2)
    upgrade_cost = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    class Meta:
        ordering = ["cooler", "level"]
        constraints = [
            models.UniqueConstraint(fields=["cooler", "level"], name="unique_level_per_cooler")
        ]

    def __str__(self):
        return f"{self.cooler.name} - Level {self.level}"


class UserCeilingCooler(models.Model):
    cooler = models.ForeignKey(CeilingCooler, on_delete=models.CASCADE, related_name="users")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="ceiling_coolers")
    level = models.PositiveSmallIntegerField(default=1)
    type = models.CharField(max_length=20, default="cooler")
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.username} - {self.cooler.name} (Level {self.level})"


class UserEnergyEquipment(models.Model):
    equipment = models.ForeignKey(EnergyEquipment, on_delete=models.CASCADE, related_name="users")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="energy_equipment")
    level = models.PositiveSmallIntegerField(default=1)
    type = models.CharField(
        max_length=20,
        choices=EnergyEquipment.Type.choices,
        default=EnergyEquipment.Type.SOLAR_PANEL,
    )
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.username} - {self.equipment.name} (Level {self.level})"