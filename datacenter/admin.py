from django.contrib import admin
from .models import DataCenterHack, Bay

# Register your models here.
@admin.register(DataCenterHack)
class DataCenterHackAdmin(admin.ModelAdmin):
    list_display = ["bay"]
    
@admin.register(Bay)
class BayAdmin(admin.ModelAdmin):
    list_display = ["name", "data_center_hack", "watts"]