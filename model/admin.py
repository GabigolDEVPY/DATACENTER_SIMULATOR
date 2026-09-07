from django.contrib import admin
from .models import AIModel, MarkModel
# Register your models here.

@admin.register(MarkModel)
class MarkModelAdmin(admin.ModelAdmin):
    list_display = ('name',)
    
@admin.register(AIModel)
class AIModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'level', 'gpu_vram', 'ram_gb', 'storage_gb', 'price', 'base_revenue', 'params')