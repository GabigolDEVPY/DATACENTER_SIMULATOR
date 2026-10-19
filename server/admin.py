from django.contrib import admin
from .models import Rack, Bay, StorageAllocation, Datacenter

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