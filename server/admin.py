from django.contrib import admin
from .models import (
    EnergyEquipmentLevel, Rack, Bay, StorageAllocation, Datacenter, 
    CeilingCooler, EnergyEquipment, UserCeilingCooler, 
    UserEnergyEquipment, CeilingCoolerLevel
    )

# Register your models here.
@admin.register(Rack)
class RackAdmin(admin.ModelAdmin):
    list_display = ["name"]
    
@admin.register(Bay)
class BayAdmin(admin.ModelAdmin):
    list_display = ["name", "rack", "is_active", "last_time_active"]
    
@admin.register(StorageAllocation)
class StorageAllocationAdmin(admin.ModelAdmin):
    list_display = ["bay", "ai_model", "allocated_gb"]
    
@admin.register(Datacenter)
class DatacenterAdmin(admin.ModelAdmin):
    list_display = ["name", "updates", "user"]
    
@admin.register(UserCeilingCooler)
class UserCeilingCoolerAdmin(admin.ModelAdmin):
    list_display = ["user", "type", "level"]
    
@admin.register(UserEnergyEquipment)
class UserEnergyEquipmentAdmin(admin.ModelAdmin):
    list_display = ["user",  "level"]
    
@admin.register(CeilingCooler)
class CeilingCoolerAdmin(admin.ModelAdmin):
    list_display = ["name", "price"]

@admin.register(EnergyEquipment)
class EnergyEquipmentAdmin(admin.ModelAdmin):
    list_display = ["name", "price"]
    
@admin.register(EnergyEquipmentLevel)
class EnergyEquipmentLevelAdmin(admin.ModelAdmin):
    list_display = ["equipment", "level", "upgrade_cost"]
    
@admin.register(CeilingCoolerLevel)
class CeilingCoolerLevelAdmin(admin.ModelAdmin):
    list_display = ["cooler", "level", "upgrade_cost"]