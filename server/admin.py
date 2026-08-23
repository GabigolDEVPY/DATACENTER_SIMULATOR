from django.contrib import admin
from .models import Rack, Bay

# Register your models here.
@admin.register(Rack)
class RackAdmin(admin.ModelAdmin):
    list_display = ["name"]
    
@admin.register(Bay)
class BayAdmin(admin.ModelAdmin):
    list_display = ["name", "rack", "is_active", "last_time_active", "get_power", "get_total_watts", "get_total_price", "get_total_ram", "get_total_vram", "get_total_processors", "get_total_storage"]