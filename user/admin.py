from django.contrib import admin
from user.models import Inventory, InventoryItem
# Register your models here.

@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    list_display = ['user', 'id']
    
@admin.register(InventoryItem)
class InventoryItemAdmin(admin.ModelAdmin):
    list_display = ['item', 'quantity', 'is_equiped']