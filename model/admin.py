from django.contrib import admin
from .models import AIModel, MarkModel, AIInstance, AIInstanceBay
# Register your models here.

@admin.register(MarkModel)
class MarkModelAdmin(admin.ModelAdmin):
    list_display = ('name',)
    
@admin.register(AIModel)
class AIModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'level', 'gpu_vram', 'ram_gb', 'storage_gb', 'price', 'base_revenue', 'params')
    
@admin.register(AIInstance)
class AIInstanceAdmin(admin.ModelAdmin):
    list_display = ('model', 'bay', 'status', 'started_at')
    

@admin.register(AIInstanceBay)
class AIInstanceBayAdmin(admin.ModelAdmin):
    list_display = ('ai_instance', 'bay')