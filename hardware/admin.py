from django.contrib import admin
from .models import CPU, GPU, SSD, RAM, Brand

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
class GPUAdmin(admin.ModelAdmin):
    list_display = ('type', 'model', 'brand', 'price', 'watts', 'score_bottleneck')
    pass

@admin.register(SSD)
class GPUAdmin(admin.ModelAdmin):
    list_display = ('type', 'model', 'brand', 'price', 'watts', 'score_bottleneck')
    pass


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)
    pass