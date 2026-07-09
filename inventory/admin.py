from django.contrib import admin
from .models import InventoryItem

# Register your models here.
@admin.register(InventoryItem)
class InventoryItemAdmin(admin.ModelAdmin):
    list_display = ["item"]