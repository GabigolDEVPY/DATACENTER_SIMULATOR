from django.contrib import admin
from .models import CPU, GPU, RAM, SSD, Brand

# Register your models here.
@admin.register(CPU)
class CPUAdmin(admin.ModelAdmin):
    list_display = ('type', 'model', 'brand', 'price', 'watts', 'score_bottleneck')
    pass

@admin.register(GPU)
class GPUAdmin(admin.ModelAdmin):
    list_display = ('type', 'model', 'brand', 'price', 'watts', 'score_bottleneck')
    pass

@admin.register(RAM)
class RAMAdmin(admin.ModelAdmin):
    list_display = ('type', 'model', 'brand', 'price', 'watts')
    pass

@admin.register(SSD)
class SSDAdmin(admin.ModelAdmin):
    list_display = ('type', 'model', 'brand', 'price', 'watts')
    pass

@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('name',)
    pass