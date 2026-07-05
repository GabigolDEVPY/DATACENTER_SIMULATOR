from django.contrib import admin
from .models import Rack, Bay

# Register your models here.
@admin.register(Rack)
class RackAdmin(admin.ModelAdmin):
    list_display = ["name"]
    
@admin.register(Bay)
class BayAdmin(admin.ModelAdmin):
    list_display = ["name", "rack", "watts"]