from django.contrib import admin
from .models import CPU, GPU, SSD, RAM, Brand

# Register your models here.
@admin.register(CPU)
class CPUAdmin(admin.ModelAdmin):
    list_display = ('type', 'model', 'brand', 'price', 'watts', 'score_bottleneck', 'get_power')
    pass

@admin.register(GPU)
class GPUAdmin(admin.ModelAdmin):
    list_display = ('type', 'model', 'brand', 'price', 'watts', 'score_bottleneck', 'get_power')
    pass

@admin.register(RAM)
class RAMAdmin(admin.ModelAdmin):
    list_display = ('type', 'model', 'brand', 'price', 'watts', 'get_power')
    pass


@admin.register(SSD)
class SSDAdmin(admin.ModelAdmin):
    list_display = ('type', 'model', 'brand', 'price', 'watts', 'get_power')
    pass


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)
    pass