from django.contrib import admin
from user.models import Inventory, InventoryItem, User
# Register your models here.

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'money', 'actual_rate', 'last_refresh_balance']

@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    list_display = ['user', 'id']
    
@admin.register(InventoryItem)
class InventoryItemAdmin(admin.ModelAdmin):
    list_display = ['item', 'quantity', 'is_equiped']