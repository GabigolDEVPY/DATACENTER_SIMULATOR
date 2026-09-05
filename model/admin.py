from django.contrib import admin
from .models import AIModel
# Register your models here.

@admin.register(AIModel)
class AIModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'level', 'gpu_vram', 'ram_gb', 'storage_gb', 'price', 'base_revenue', 'params')